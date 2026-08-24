"""Deterministic, typed pipeline composition for DSPyGen modules.

This module contains no model, provider, filesystem, process, or network actuation.
It only binds an upstream value to a downstream ``forward`` call.
"""
from __future__ import annotations

from dataclasses import dataclass
from inspect import Parameter, Signature, signature
from typing import Any, Callable, cast

LEGACY_PIPE_PLACEHOLDER = "Please implement the pipe method for DSL support."


@dataclass(frozen=True, slots=True)
class PipelineRefusal(ValueError):
    """Typed refusal raised when pipeline binding is ambiguous or invalid."""

    reason: str
    module: str
    detail: str

    def __str__(self) -> str:
        return f"REFUSED:{self.reason} module={self.module} detail={self.detail}"


def _module_name(module: object) -> str:
    return f"{module.__class__.__module__}.{module.__class__.__qualname__}"


def _forward_signature(module: object) -> Signature:
    forward = getattr(module, "forward", None)
    if not callable(forward):
        raise PipelineRefusal(
            "PIPE_FORWARD_MISSING",
            _module_name(module),
            "downstream object has no callable forward method",
        )
    return signature(forward)


def select_pipe_parameter(module: object) -> str:
    """Select the sole lawful parameter that may receive an upstream value.

    Selection order:
    1. explicit ``pipe_input`` / ``__dspygen_pipe_input__`` declaration;
    2. the only unbound required positional-or-keyword/keyword-only parameter;
    3. the only bindable parameter when all are optional.

    Ambiguity is refused rather than guessed.
    """

    sig = _forward_signature(module)
    bindable = [
        parameter
        for parameter in sig.parameters.values()
        if parameter.kind
        in (Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD, Parameter.KEYWORD_ONLY)
        and parameter.name != "self"
    ]
    if not bindable:
        raise PipelineRefusal(
            "PIPE_INPUT_ABSENT",
            _module_name(module),
            f"forward signature {sig} has no bindable input",
        )

    explicit = getattr(module, "__dspygen_pipe_input__", None) or getattr(
        module, "pipe_input", None
    )
    names = {parameter.name for parameter in bindable}
    if explicit is not None:
        if explicit not in names:
            raise PipelineRefusal(
                "PIPE_INPUT_DECLARATION_INVALID",
                _module_name(module),
                f"declared input {explicit!r} not in {sorted(names)}",
            )
        return str(explicit)

    forward_args = dict(getattr(module, "forward_args", {}) or {})
    required_unbound = [
        parameter.name
        for parameter in bindable
        if parameter.default is Parameter.empty and parameter.name not in forward_args
    ]
    if len(required_unbound) == 1:
        return required_unbound[0]
    if len(required_unbound) > 1:
        raise PipelineRefusal(
            "PIPE_INPUT_AMBIGUOUS",
            _module_name(module),
            f"multiple required inputs remain unbound: {required_unbound}",
        )

    if len(bindable) == 1:
        return bindable[0].name

    unbound = [parameter.name for parameter in bindable if parameter.name not in forward_args]
    if len(unbound) == 1:
        return unbound[0]
    raise PipelineRefusal(
        "PIPE_INPUT_AMBIGUOUS",
        _module_name(module),
        f"declare pipe_input; candidates={unbound or sorted(names)}",
    )


def pipe_forward(module: object, input_value: Any) -> Any:
    """Bind ``input_value`` to a downstream module and execute ``forward`` once."""

    parameter = select_pipe_parameter(module)
    kwargs = dict(getattr(module, "forward_args", {}) or {})
    kwargs[parameter] = input_value
    invoke = module if callable(module) else module.forward
    result = invoke(**kwargs)
    cast(Any, module).output = result
    return result


def pipe_modules(left: object, right: object) -> object:
    """Compose two modules while preserving the historical ``a | b`` contract."""

    left_output = getattr(left, "output", None)
    if left_output is None:
        forward_args = dict(getattr(left, "forward_args", {}) or {})
        if not forward_args:
            raise PipelineRefusal(
                "PIPE_SOURCE_INPUT_MISSING",
                _module_name(left),
                "source output is empty and no forward_args were supplied",
            )
        invoke = left if callable(left) else left.forward
        left_output = invoke(**forward_args)
        cast(Any, left).output = left_output

    pipe = getattr(right, "pipe", None)
    if callable(pipe) and not is_legacy_pipe_placeholder(pipe):
        result = pipe(left_output)
    else:
        result = pipe_forward(right, left_output)
    cast(Any, right).output = result
    return right


def is_legacy_pipe_placeholder(function: Callable[..., Any]) -> bool:
    """Return whether ``function`` is the exact generated placeholder implementation."""

    target = getattr(function, "__func__", function)
    code = getattr(target, "__code__", None)
    return bool(code and LEGACY_PIPE_PLACEHOLDER in code.co_consts)


def repair_legacy_pipe_class(cls: type[Any]) -> bool:
    """Replace only the exact historical generated placeholder on ``cls``."""

    pipe = cls.__dict__.get("pipe")
    if pipe is None or not is_legacy_pipe_placeholder(pipe):
        return False

    def _pipe(self: object, input_value: Any) -> Any:
        return pipe_forward(self, input_value)

    _pipe.__name__ = "pipe"
    _pipe.__qualname__ = f"{cls.__qualname__}.pipe"
    _pipe.__doc__ = "Pipe an upstream value into the uniquely admitted forward input."
    cast(Any, cls).pipe = _pipe
    cast(Any, cls).__dspygen_legacy_pipe_repaired__ = True
    return True


def install_legacy_pipeline_compat(module_base: type[Any]) -> None:
    """Install a scoped class-construction hook for legacy generated modules.

    The hook repairs only classes in ``dspygen.modules`` whose ``pipe`` bytecode
    contains the exact historical placeholder string. It does not alter arbitrary
    DSPy modules and can be disabled with ``DSPYGEN_DISABLE_LEGACY_PIPE_COMPAT=1``
    by the package initializer.
    """

    if getattr(module_base, "__dspygen_pipeline_hook_installed__", False):
        return

    original_descriptor = module_base.__dict__.get("__init_subclass__")

    @classmethod
    def _init_subclass(cls: type[Any], **kwargs: Any) -> None:
        if original_descriptor is None:
            super(module_base, cls).__init_subclass__(**kwargs)
        else:
            original_descriptor.__get__(cls, module_base)(**kwargs)
        if cls.__module__.startswith("dspygen.modules."):
            repair_legacy_pipe_class(cls)

    module_base.__init_subclass__ = _init_subclass  # type: ignore[method-assign]
    module_base.__dspygen_pipeline_hook_installed__ = True
