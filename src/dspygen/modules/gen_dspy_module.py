"""Deterministic DSPy module source manufacture."""
from __future__ import annotations

import keyword
import re
from typing import Any

from pydantic import BaseModel, Field, field_validator

try:
    import dspy
except ModuleNotFoundError:  # Source generation does not require the DSPy runtime.
    class _ModuleBase:
        pass
else:
    _ModuleBase = dspy.Module

_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


class DSPyModuleTemplate(BaseModel):
    """Admitted model for a generated ``dspy.Module``."""

    inputs: list[str] = Field(..., min_length=1)
    output: str
    class_name: str

    @field_validator("inputs")
    @classmethod
    def validate_inputs(cls, values: list[str]) -> list[str]:
        normalized = [value.strip() for value in values]
        if len(set(normalized)) != len(normalized):
            raise ValueError("input names must be unique")
        for value in normalized:
            _validate_identifier(value, "input")
        return normalized

    @field_validator("output", "class_name")
    @classmethod
    def validate_identifier(cls, value: str, info: Any) -> str:
        value = value.strip()
        _validate_identifier(value, info.field_name)
        return value


def _validate_identifier(value: str, field: str) -> None:
    if not _IDENTIFIER.fullmatch(value) or keyword.iskeyword(value):
        raise ValueError(f"{field} must be a valid non-keyword Python identifier: {value!r}")


def _snake_case(value: str) -> str:
    value = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", value)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value).lower()


def render_dspy_module(model: DSPyModuleTemplate) -> str:
    """Render byte-deterministic source without an LLM or template-engine dependency."""

    class_name = f"{model.class_name}Module"
    variable_name = _snake_case(model.class_name)
    inputs = ", ".join(model.inputs)
    kwargs = ", ".join(f"{name}={name}" for name in model.inputs)
    signature = f"{inputs} -> {model.output}"
    call_args = ", ".join(f"{name}: str" for name in model.inputs)
    call_kwargs = ", ".join(f"{name}={name}" for name in model.inputs)

    return f'''"""{class_name}: {signature}."""
from __future__ import annotations

import dspy
from typer import Typer

from dspygen.modules.pipeline import pipe_forward, pipe_modules
from dspygen.utils.dspy_tools import init_dspy

app = Typer()


class {class_name}(dspy.Module):
    """{signature}"""

    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def __or__(self, other):
        return pipe_modules(self, other)

    def forward(self, {inputs}):
        pred = dspy.Predict("{signature}")
        self.output = pred({kwargs}).{model.output}
        return self.output

    def pipe(self, input_value):
        return pipe_forward(self, input_value)


def {variable_name}_call({call_args}):
    return {class_name}()({call_kwargs})


@app.command()
def call({call_args}):
    """Execute {class_name}."""
    init_dspy()
    print({variable_name}_call({call_kwargs}))


def main():
    init_dspy()
    raise SystemExit("Provide inputs through the CLI or {variable_name}_call().")


if __name__ == "__main__":
    app()
'''


# Retained public symbol for callers that imported the old template constant.
dspy_module_template = "rendered by render_dspy_module(DSPyModuleTemplate)"


class SignatureDspyModuleModule(_ModuleBase):
    """Manufacture a complete DSPy module from an admitted template model."""

    def forward(self, tmpl_model: DSPyModuleTemplate) -> str:
        return render_dspy_module(tmpl_model)
