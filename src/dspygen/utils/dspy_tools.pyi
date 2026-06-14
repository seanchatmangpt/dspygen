"""PEP 561 type stubs for dspygen.utils.dspy_tools."""

from typing import Any, Optional, Type

__all__ = ["init_dspy", "init_ol", "get_model"]


def init_dspy(
    model: str = ...,
    lm_class: Optional[Type[Any]] = ...,
    max_tokens: int = ...,
    lm_instance: Optional[Any] = ...,
    api_key: Optional[str] = ...,
    temperature: float = ...,
    experimental: bool = ...,
) -> Any: ...


def init_ol(
    model: str = ...,
    base_url: str = ...,
    max_tokens: int = ...,
    lm_instance: Optional[Any] = ...,
    lm_class: Optional[Type[Any]] = ...,
    timeout: int = ...,
    temperature: float = ...,
    experimental: bool = ...,
) -> Any: ...


def get_model(alias: str) -> str: ...
