"""Validated YAML/dict pipeline construction for DSPyGen modules."""
from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from pathlib import Path
from typing import Any, Mapping, Sequence

from dspygen.modules.pipeline import PipelineRefusal, pipe_modules


@dataclass(frozen=True, slots=True)
class PipelineDefinitionRefusal(ValueError):
    reason: str
    detail: str

    def __str__(self) -> str:
        return f"REFUSED:{self.reason} detail={self.detail}"


def _resolve_module_class(reference: str) -> type[Any]:
    """Resolve an explicit ``module.path:Class`` or a legacy ``Name`` reference."""

    if ":" in reference:
        module_name, class_name = reference.split(":", 1)
    elif "." in reference:
        module_name, _, class_name = reference.rpartition(".")
    else:
        module_name = "dspygen.modules.dspygen_module"
        class_name = f"{reference}DGModule"

    if not module_name.startswith("dspygen.modules"):
        raise PipelineDefinitionRefusal(
            "PIPELINE_MODULE_NAMESPACE_REFUSED",
            module_name,
        )
    try:
        module = import_module(module_name)
        candidate = getattr(module, class_name)
    except (ImportError, AttributeError) as exc:
        raise PipelineDefinitionRefusal(
            "PIPELINE_MODULE_NOT_FOUND",
            f"{reference}: {type(exc).__name__}: {exc}",
        ) from exc
    if not isinstance(candidate, type):
        raise PipelineDefinitionRefusal(
            "PIPELINE_MODULE_INVALID",
            f"{reference} did not resolve to a class",
        )
    return candidate


def _admit_definition(config: Mapping[str, Any]) -> Sequence[Mapping[str, Any]]:
    modules = config.get("dspy_modules")
    if not isinstance(modules, list) or not modules:
        raise PipelineDefinitionRefusal(
            "PIPELINE_STEPS_INVALID",
            "dspy_modules must be a non-empty list",
        )
    admitted: list[Mapping[str, Any]] = []
    for index, item in enumerate(modules):
        if not isinstance(item, Mapping):
            raise PipelineDefinitionRefusal(
                "PIPELINE_STEP_INVALID",
                f"step {index} must be an object",
            )
        reference = item.get("module")
        args = item.get("args", {})
        if not isinstance(reference, str) or not reference.strip():
            raise PipelineDefinitionRefusal(
                "PIPELINE_MODULE_REFERENCE_INVALID",
                f"step {index}",
            )
        if not isinstance(args, Mapping):
            raise PipelineDefinitionRefusal(
                "PIPELINE_ARGS_INVALID",
                f"step {index} args must be an object",
            )
        admitted.append({"module": reference.strip(), "args": dict(args)})
    return admitted


def execute_pipeline_definition(config: Mapping[str, Any]) -> Any:
    """Construct and execute an admitted in-memory pipeline definition."""

    definitions = _admit_definition(config)
    modules = [
        _resolve_module_class(str(item["module"]))(**dict(item["args"]))
        for item in definitions
    ]
    first = modules[0]
    if getattr(first, "output", None) is None:
        args = dict(getattr(first, "forward_args", {}) or {})
        if not args:
            raise PipelineRefusal(
                "PIPE_SOURCE_INPUT_MISSING",
                f"{first.__class__.__module__}.{first.__class__.__qualname__}",
                "first step requires args",
            )
        first.output = first.forward(**args)
    current = first
    for downstream in modules[1:]:
        current = pipe_modules(current, downstream)
    return current.output


def process_yaml_pipeline(yaml_file: str | Path) -> Any:
    """Load YAML safely, admit its structure, and execute the resulting pipeline."""

    try:
        import yaml
    except ModuleNotFoundError as exc:
        raise PipelineDefinitionRefusal(
            "YAML_CAPABILITY_UNAVAILABLE",
            "install PyYAML to load YAML files; dict execution remains available",
        ) from exc

    path = Path(yaml_file)
    try:
        config = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise PipelineDefinitionRefusal(
            "PIPELINE_YAML_INVALID",
            f"{path}: {type(exc).__name__}: {exc}",
        ) from exc
    if not isinstance(config, Mapping):
        raise PipelineDefinitionRefusal(
            "PIPELINE_DOCUMENT_INVALID",
            "top-level YAML value must be an object",
        )
    return execute_pipeline_definition(config)


def main() -> None:
    from dspygen.utils.dspy_tools import init_dspy

    init_dspy()
    print(process_yaml_pipeline("pipeline.yaml"))


if __name__ == "__main__":
    main()
