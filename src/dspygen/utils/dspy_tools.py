import os
from typing import Optional

import dspy


def init_dspy(
    model: str = "gpt-4o",
    lm_class=None,
    max_tokens: int = 800,
    lm_instance=None,
    api_key: Optional[str] = None,
    temperature: float = 0.6,
    experimental: bool = True,
):
    """Initialize DSPy with the given language model.

    Prefers the modern ``dspy.LM`` constructor when no custom ``lm_class`` is
    provided.  A custom class (e.g. ``Groq``, ``Cerebras``) is instantiated
    directly with the supplied keyword arguments so that callers that pass
    ``lm_class`` continue to work unchanged.

    Parameters
    ----------
    model:
        Model identifier string (e.g. ``"gpt-4o"`` or ``"openai/gpt-4o"``).
    lm_class:
        Optional custom LM class.  When provided the class is instantiated
        with ``model``, ``max_tokens``, ``api_key``, and ``temperature``.
    max_tokens:
        Maximum number of tokens to generate.
    lm_instance:
        A pre-built LM instance; if given it is configured directly.
    api_key:
        Optional API key override (falls back to environment variables).
    temperature:
        Sampling temperature.
    experimental:
        Passed to ``dspy.settings.configure``.
    """
    if lm_instance:
        dspy.settings.configure(lm=lm_instance, experimental=experimental)
        return lm_instance

    if lm_class is not None:
        # Custom provider class — instantiate with the standard kwargs callers expect
        lm = lm_class(max_tokens=max_tokens, model=model, api_key=api_key, temperature=temperature)
        dspy.settings.configure(lm=lm, experimental=experimental)
        return lm

    # Default path: use the current dspy.LM constructor (DSPy >= 2.4)
    kwargs = {"max_tokens": max_tokens, "temperature": temperature}
    if api_key:
        kwargs["api_key"] = api_key

    try:
        lm = dspy.LM(model=model, **kwargs)
    except AttributeError:
        # Fallback for older DSPy versions that only have dspy.OpenAI
        lm = dspy.OpenAI(model=model, **kwargs)

    dspy.settings.configure(lm=lm, experimental=experimental)
    return lm


def init_ol(
    model: str = "phi3:instruct",
    base_url: str = os.environ.get("OLLAMA_HOST", "http://localhost:11434"),
    max_tokens: int = 2000,
    lm_instance=None,
    lm_class=None,
    timeout: int = 100,
    temperature: float = 0.6,
    experimental: bool = True,
):
    """Initialize DSPy with a local Ollama model.

    Uses the ``dspy.LM`` constructor with the ``ollama_chat/`` prefix when no
    custom class is provided, which is the recommended approach in current DSPy.
    """
    if lm_instance:
        dspy.settings.configure(lm=lm_instance, experimental=experimental)
        return lm_instance

    if lm_class is not None:
        lm = lm_class(
            model=model,
            base_url=base_url,
            max_tokens=max_tokens,
            timeout_s=timeout,
            temperature=temperature,
        )
        dspy.settings.configure(lm=lm, experimental=experimental)
        return lm

    # Modern DSPy path: use dspy.LM with the ollama_chat provider prefix
    ollama_model = f"ollama_chat/{model}"
    kwargs = {
        "api_base": base_url,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    try:
        lm = dspy.LM(model=ollama_model, **kwargs)
    except AttributeError:
        # Fallback for older DSPy versions
        lm = dspy.OllamaLocal(
            model=model,
            base_url=base_url,
            max_tokens=max_tokens,
            timeout_s=timeout,
            temperature=temperature,
        )

    dspy.settings.configure(lm=lm, experimental=experimental)
    return lm
