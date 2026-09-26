"""
DSPy 3.x Groq Language Model Backend

This module provides a Groq LLM backend for DSPy 3.1.3+
Compatible with Groq Cloud API using models like llama3-70b-8192, mixtral-8x7b-32768, etc.

Example usage:
    from dspygen.lm.groq_lm_v3 import Groq
    import dspy

    lm = Groq(model="llama3-70b-8192", api_key="your-api-key")
    dspy.settings.configure(lm=lm)
"""

import os
from typing import Optional, Union, List, Dict, Any

from groq import Groq as GroqClient
import dspy
from dspy.primitives.lm import BaseLM


class Groq(BaseLM):
    """
    Groq LLM backend for DSPy 3.x

    Supports Groq Cloud API with fast inference on models like:
    - llama3-70b-8192
    - llama3-8b-8192
    - mixtral-8x7b-32768
    - gemma-7b-it

    Args:
        model: Model name to use (default: llama3-70b-8192)
        api_key: Groq API key (defaults to GROQ_API_KEY env var)
        base_url: Optional custom base URL
        timeout: Request timeout in seconds (default: 60)
        temperature: Sampling temperature (default: 0.0)
        max_tokens: Maximum tokens in response (default: 4096)
        top_p: Nucleus sampling parameter (default: 1.0)
        **kwargs: Additional arguments passed to Groq API
    """

    DEFAULT_MODEL = "llama3-70b-8192"
    DEFAULT_TIMEOUT = 60
    DEFAULT_TEMPERATURE = 0.0
    DEFAULT_MAX_TOKENS = 4096

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        top_p: float = 1.0,
        **kwargs,
    ):
        super().__init__(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )

        # Get API key from parameter or environment
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GROQ_API_KEY not found. Set GROQ_API_KEY environment variable "
                "or pass api_key parameter."
            )

        # Initialize Groq client
        client_kwargs = {"api_key": self.api_key, "timeout": timeout}
        if base_url:
            client_kwargs["base_url"] = base_url

        self.client = GroqClient(**client_kwargs)
        self.timeout = timeout
        self.top_p = top_p
        self.provider = "groq"

        # Store model parameters
        self.model_kwargs = {
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            **kwargs,
        }

    def _generate(
        self,
        prompt: str,
        **kwargs,
    ) -> List[dspy.Prediction]:
        """
        Generate a response from Groq API

        Args:
            prompt: The input prompt
            **kwargs: Additional generation parameters

        Returns:
            List of dspy.Prediction with generated responses
        """
        # Merge kwargs with model defaults
        generation_kwargs = {**self.model_kwargs, **kwargs}

        try:
            # Create chat completion
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                **generation_kwargs,
            )

            # Extract the generated text
            content = response.choices[0].message.content

            # Get usage statistics if available
            usage = None
            if hasattr(response, "usage") and response.usage:
                usage = {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens,
                }

            # Return as DSPy Prediction
            return [
                dspy.Prediction(
                    text=content,
                    usage=usage,
                    model=self.model,
                )
            ]

        except Exception as e:
            raise RuntimeError(f"Groq API error: {e}") from e

    def _request(
        self,
        prompt: str,
        **kwargs,
    ) -> str:
        """
        Simple request interface for backward compatibility

        Args:
            prompt: The input prompt
            **kwargs: Additional generation parameters

        Returns:
            Generated text as string
        """
        predictions = self._generate(prompt, **kwargs)
        return predictions[0].text

    def __call__(
        self,
        prompt: str,
        **kwargs,
    ) -> List[str]:
        """
        Main entry point for DSPy

        Args:
            prompt: The input prompt
            **kwargs: Additional generation parameters

        Returns:
            List of generated texts
        """
        predictions = self._generate(prompt, **kwargs)
        return [p.text for p in predictions]

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "Groq":
        """
        Create Groq instance from configuration dictionary

        Args:
            config: Configuration dictionary with keys like model, api_key, etc.

        Returns:
            Groq instance
        """
        return cls(**config)

    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model configuration

        Returns:
            Dictionary with model information
        """
        return {
            "provider": self.provider,
            "model": self.model,
            "temperature": self.model_kwargs.get("temperature"),
            "max_tokens": self.model_kwargs.get("max_tokens"),
            "top_p": self.top_p,
        }


def init_groq(
    model: str = Groq.DEFAULT_MODEL,
    api_key: Optional[str] = None,
    temperature: float = Groq.DEFAULT_TEMPERATURE,
    max_tokens: int = Groq.DEFAULT_MAX_TOKENS,
    experimental: bool = True,
) -> Groq:
    """
    Initialize Groq LM and configure DSPy settings

    Args:
        model: Model name to use
        api_key: Groq API key (defaults to GROQ_API_KEY env var)
        temperature: Sampling temperature
        max_tokens: Maximum tokens in response
        experimental: Enable experimental DSPy features

    Returns:
        Configured Groq instance

    Example:
        >>> from dspygen.lm.groq_lm_v3 import init_groq
        >>> lm = init_groq(model="llama3-70b-8192")
        >>> import dspy
        >>> result = dspy.Predict("question -> answer")(question="What is 2+2?")
        >>> print(result.answer)
    """
    lm = Groq(
        model=model,
        api_key=api_key,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    dspy.settings.configure(lm=lm, experimental=experimental)
    return lm


def main():
    """Example usage of Groq LM with DSPy"""
    # Initialize Groq LM
    lm = init_groq(model="llama3-70b-8192", max_tokens=2000)

    # Use DSPy to make a prediction
    result = dspy.Predict("prompt -> code")(
        prompt="Fast API CRUD endpoint for fire alarm global IoT network"
    )
    print(result.code)


if __name__ == "__main__":
    main()
