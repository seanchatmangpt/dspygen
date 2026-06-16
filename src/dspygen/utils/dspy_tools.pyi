"""PEP 561 type stubs for dspygen.utils.dspy_tools."""

from typing import Any, Optional, Type

__all__ = ["init_dspy", "init_ol", "get_model"]


def init_dspy(
    model: str = ...,
    lm_class: type[Any] | None = ...,
    max_tokens: int = ...,
    lm_instance: Any | None = ...,
    api_key: str | None = ...,
    temperature: float = ...,
    experimental: bool = ...,
) -> Any: ...


def init_ol(
    model: str = ...,
    base_url: str = ...,
    max_tokens: int = ...,
    lm_instance: Any | None = ...,
    lm_class: type[Any] | None = ...,
    timeout: int = ...,
    temperature: float = ...,
    experimental: bool = ...,
) -> Any: ...


def get_model(alias: str) -> str: ...
