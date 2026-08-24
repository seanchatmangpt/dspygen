"""DSPy runtime configuration with explicit provider boundaries."""
from __future__ import annotations

import os
import warnings
from typing import Any

import dspy


def _configure(lm: Any):
    """Configure the current DSPy runtime without manufacturing unknown settings."""
    configure = getattr(dspy, "configure", None)
    if callable(configure):
        configure(lm=lm)
    else:
        dspy.settings.configure(lm=lm)
    return lm


def init_dspy(
    model: str = "openai/gpt-4o",
    lm_class=None,
    max_tokens: int = 800,
    lm_instance=None,
    api_key: str | None = None,
    temperature: float = 0.6,
    experimental: bool | None = None,
):
    """Configure DSPy with an explicit LM instance or provider model.

    ``experimental`` is retained only for source compatibility. Modern DSPy has
    no such setting, so a non-``None`` value is ignored with a deprecation warning.
    No network call occurs until a predictor is executed.
    """
    if experimental is not None:
        warnings.warn(
            "experimental is obsolete in DSPy 3.x and is ignored",
            DeprecationWarning,
            stacklevel=2,
        )
    if lm_instance is not None:
        return _configure(lm_instance)

    kwargs: dict[str, Any] = {
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    if api_key:
        kwargs["api_key"] = api_key

    if lm_class is not None:
        return _configure(lm_class(model=model, **kwargs))

    lm_type = getattr(dspy, "LM", None)
    if lm_type is None:
        raise RuntimeError("REFUSED:DSPY_LM_UNAVAILABLE runtime has no dspy.LM")
    return _configure(lm_type(model=model, **kwargs))


def init_ol(
    model: str = "phi3:instruct",
    base_url: str = os.environ.get("OLLAMA_HOST", "http://localhost:11434"),
    max_tokens: int = 2000,
    lm_instance=None,
    lm_class=None,
    timeout: int = 100,
    temperature: float = 0.6,
    experimental: bool | None = None,
):
    """Configure a local Ollama-backed DSPy LM without executing a model call."""
    if experimental is not None:
        warnings.warn(
            "experimental is obsolete in DSPy 3.x and is ignored",
            DeprecationWarning,
            stacklevel=2,
        )
    if lm_instance is not None:
        return _configure(lm_instance)

    if lm_class is not None:
        lm = lm_class(
            model=model,
            base_url=base_url,
            max_tokens=max_tokens,
            timeout_s=timeout,
            temperature=temperature,
        )
        return _configure(lm)

    lm_type = getattr(dspy, "LM", None)
    if lm_type is None:
        raise RuntimeError("REFUSED:DSPY_LM_UNAVAILABLE runtime has no dspy.LM")
    lm = lm_type(
        model=f"ollama_chat/{model}",
        api_base=base_url,
        max_tokens=max_tokens,
        temperature=temperature,
        timeout=timeout,
    )
    return _configure(lm)
