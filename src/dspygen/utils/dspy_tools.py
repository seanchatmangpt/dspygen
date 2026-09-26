"""
DSPy utility functions for dspygen

Compatible with DSPy 3.1.3+
"""

from typing import Optional, Any

import dspy
from dspy.primitives.lm import BaseLM


def init_dspy(
    model: str = "gpt-4o-mini",
    lm_class: type = dspy.OpenAI,
    max_tokens: int = 800,
    lm_instance: Optional[BaseLM] = None,
    api_key: Optional[str] = None,
    temperature: float = 0.6,
    experimental: bool = True,
) -> BaseLM:
    """
    Initialize DSPy with a language model

    Args:
        model: Model name/identifier
        lm_class: Language model class (e.g., dspy.OpenAI, Groq, etc.)
        max_tokens: Maximum tokens in response
        lm_instance: Pre-configured LM instance (skips initialization)
        api_key: API key for the LLM provider
        temperature: Sampling temperature
        experimental: Enable experimental DSPy features

    Returns:
        Configured language model instance

    Example:
        >>> import dspy
        >>> from dspygen.utils.dspy_tools import init_dspy
        >>> lm = init_dspy(model="gpt-4o-mini", max_tokens=1000)
    """
    if lm_instance:
        dspy.settings.configure(lm=lm_instance, experimental=experimental)
        return lm_instance
    else:
        # Build LM kwargs
        lm_kwargs = {"model": model, "max_tokens": max_tokens, "temperature": temperature}
        if api_key:
            lm_kwargs["api_key"] = api_key

        lm = lm_class(**lm_kwargs)
        dspy.settings.configure(lm=lm, experimental=experimental)
        return lm


def init_ol(
    model: str = "phi4",
    base_url: str = "http://localhost:11434",
    max_tokens: int = 2000,
    lm_instance: Optional[BaseLM] = None,
    lm_class: type = dspy.OllamaLocal,
    timeout: int = 100,
    temperature: float = 0.6,
    experimental: bool = True,
) -> BaseLM:
    """
    Initialize DSPy with Ollama local model

    Args:
        model: Model name (e.g., "phi4", "llama3")
        base_url: Ollama server URL
        max_tokens: Maximum tokens in response
        lm_instance: Pre-configured LM instance
        lm_class: Language model class
        timeout: Request timeout in seconds
        temperature: Sampling temperature
        experimental: Enable experimental DSPy features

    Returns:
        Configured language model instance

    Example:
        >>> from dspygen.utils.dspy_tools import init_ol
        >>> lm = init_ol(model="llama3", base_url="http://localhost:11434")
    """
    if lm_instance:
        dspy.settings.configure(lm=lm_instance, experimental=experimental)
        return lm_instance
    else:
        lm = lm_class(
            model=model,
            base_url=base_url,
            max_tokens=max_tokens,
            timeout_s=timeout,
            temperature=temperature,
        )
        dspy.settings.configure(lm=lm, experimental=experimental)
        return lm


def init_groq(
    model: str = "llama3-70b-8192",
    api_key: Optional[str] = None,
    max_tokens: int = 2000,
    temperature: float = 0.0,
    experimental: bool = True,
) -> BaseLM:
    """
    Initialize DSPy with Groq Cloud API

    Args:
        model: Groq model name (e.g., "llama3-70b-8192", "mixtral-8x7b-32768")
        api_key: Groq API key (defaults to GROQ_API_KEY env var)
        max_tokens: Maximum tokens in response
        temperature: Sampling temperature
        experimental: Enable experimental DSPy features

    Returns:
        Configured Groq language model instance

    Example:
        >>> from dspygen.utils.dspy_tools import init_groq
        >>> lm = init_groq(model="llama3-70b-8192")
        >>> import dspy
        >>> result = dspy.Predict("question -> answer")(question="What is 2+2?")
    """
    from dspygen.lm.groq_lm_v3 import Groq

    lm = Groq(
        model=model,
        api_key=api_key,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    dspy.settings.configure(lm=lm, experimental=experimental)
    return lm


def get_current_lm() -> Optional[BaseLM]:
    """
    Get the currently configured language model

    Returns:
        Current LM instance or None if not configured
    """
    return dspy.settings.lm


def configure_dspy(
    lm: Optional[BaseLM] = None,
    experimental: bool = True,
    **kwargs,
) -> None:
    """
    Configure DSPy settings

    Args:
        lm: Language model instance
        experimental: Enable experimental features
        **kwargs: Additional DSPy settings
    """
    settings_kwargs = {"experimental": experimental, **kwargs}
    if lm is not None:
        settings_kwargs["lm"] = lm
    dspy.settings.configure(**settings_kwargs)


def list_available_models() -> dict[str, list[str]]:
    """
    List available models by provider

    Returns:
        Dictionary mapping provider names to lists of available models
    """
    return {
        "openai": [
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4-turbo",
            "gpt-4",
            "gpt-3.5-turbo",
        ],
        "groq": [
            "llama3-70b-8192",
            "llama3-8b-8192",
            "llama3-70b-versatile",
            "llama-3.1-70b-versatile",
            "llama-3.3-70b-versatile",
            "mixtral-8x7b-32768",
            "gemma-7b-it",
            "gemma2-9b-it",
        ],
        "ollama": [
            "llama3",
            "llama3:70b",
            "mistral",
            "phi4",
            "qwen2",
            "gemma2",
        ],
    }
