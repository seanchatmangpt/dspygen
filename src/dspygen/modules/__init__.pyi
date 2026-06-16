"""PEP 561 type stubs for dspygen.modules — the 5 most-used module classes."""

from typing import Any, Optional, Type, TypeVar

import dspy
from pydantic import BaseModel

__all__ = [
    "GenPydanticInstance",
    "GenPydanticDict",
    "DGModule",
    "MermaidJSModule",
    "GenSignatureModule",
]

T = TypeVar("T", bound=BaseModel)


class GenPydanticInstance(dspy.Module):
    """Generate and validate Pydantic model instances from natural-language prompts."""

    model: type[T]
    model_sources: str
    validation_error: Exception | None

    def __init__(
        self,
        model: type[T],
        generate_sig: Any = ...,
        correct_generate_sig: Any = ...,
    ) -> None: ...

    def validate_root_model(self, output: str) -> bool: ...
    def validate_output(self, output: str) -> T: ...
    def forward(self, prompt: str) -> T: ...
    def __call__(self, prompt: str) -> T: ...  # type: ignore[override]


class GenPydanticDict(dspy.Module):
    """Generate and validate dicts for Pydantic instances from natural-language prompts."""

    model: type[T]
    model_sources: str
    validation_error: Exception | None

    def __init__(
        self,
        model: type[T],
        generate_sig: Any = ...,
        correct_generate_sig: Any = ...,
    ) -> None: ...

    def validate_root_model(self, output: str) -> bool: ...
    def validate_output(self, output: str) -> dict[str, Any]: ...
    def forward(self, prompt: str) -> dict[str, Any]: ...
    def __call__(self, prompt: str) -> dict[str, Any]: ...  # type: ignore[override]


class DGModule(dspy.Module):
    """Base DSPy module that supports the pipe operator for chaining string processing steps."""

    forward_args: dict[str, Any]
    output: Any | None

    def __init__(self, **forward_args: Any) -> None: ...
    def __or__(self, other: DGModule) -> DGModule: ...
    def forward(self, **kwargs: Any) -> Any: ...
    def pipe(self, dg_module: Any) -> Any: ...


class MermaidJSModule(dspy.Module):
    """Generate MermaidJS diagram code from a natural-language prompt."""

    def forward(self, prompt: str, mermaid_type: Any = ...) -> str: ...


class GenSignatureModule(dspy.Module):
    """Generate a DSPy Signature definition from a concise signature string."""

    def forward(self, signature: str) -> Any: ...
