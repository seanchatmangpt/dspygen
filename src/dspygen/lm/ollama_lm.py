import os

import dspy
from dsp import LM

from dspygen.utils.dspy_tools import init_dspy

try:
    import ollama as ollama_client
except ImportError:
    ollama_client = None  # optional dependency; raise at runtime if missing

# Default model for Ollama
llama3_inst = "llama3:8b-instruct-q5_1"

mistral_inst = "mistral:instruct"

default_ollama_model = llama3_inst

# Base URL for the local Ollama server
_OLLAMA_BASE_URL = os.environ.get("OLLAMA_HOST", "http://localhost:11434")


def _check_ollama_connection(base_url: str = _OLLAMA_BASE_URL) -> None:
    """Raise RuntimeError if the Ollama server is not reachable."""
    import httpx

    try:
        with httpx.Client(timeout=5.0) as http:
            response = http.get(f"{base_url}/api/tags")
        if response.status_code != 200:
            raise RuntimeError(
                f"Ollama server at {base_url} returned status {response.status_code}"
            )
    except Exception as exc:
        raise RuntimeError(
            f"Cannot connect to Ollama server at {base_url}: {exc}"
        ) from exc


class Ollama(LM):
    def __init__(self, model=default_ollama_model, **kwargs):
        super().__init__(model)

        if ollama_client is None:
            raise ImportError(
                "The 'ollama' package is required. Install it with: pip install ollama"
            )

        self.provider = "default"
        self.history = []
        self._model = model
        self._base_url = kwargs.get("base_url", _OLLAMA_BASE_URL)

        # Verify the Ollama server is reachable before proceeding
        _check_ollama_connection(self._base_url)

        # Use the ollama Python client pointed at the configured host
        self._client = ollama_client.Client(host=self._base_url)

    def basic_request(self, prompt, **kwargs):
        """Send a chat request to Ollama and return the response dict."""
        try:
            response = self._client.chat(
                model=kwargs.get("model", self._model),
                messages=[{"role": "user", "content": prompt}],
            )
            return response
        except Exception as exc:
            raise RuntimeError(f"Ollama request failed: {exc}") from exc

    def __call__(self, prompt, **kwargs):
        response = self.basic_request(prompt, **kwargs)
        # The ollama client returns a dict-like object; extract the text content
        return [response["message"]["content"]]


# Main function to initialize dspy with Ollama and run a prediction
def main():
    # Initialize dspy with the Ollama class and specified model
    init_dspy(lm_class=Ollama, model=default_ollama_model, max_tokens=8000)

    # Generate prediction for a specific prompt
    pred = dspy.Predict("prompt -> code")(prompt="Fast API CRUD endpoint for fire alarm global IoT network")

    # Print the generated code
    print(pred.code)


# Entry point of the script
if __name__ == '__main__':
    main()
