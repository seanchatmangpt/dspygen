import os

import dspy
import httpx
from dsp import LM

from dspygen.utils.dspy_tools import init_dspy

default_model = "llama3.1-70b"

# Timeout in seconds for Cerebras API requests
_DEFAULT_TIMEOUT = 60.0


class Cerebras(LM):

    def __init__(self, model=default_model, **kwargs):
        # Initialize the superclass with the model
        super().__init__(model)
        self.model = model

        self.provider = "cerebras"
        self.history = []
        self.kwargs = kwargs  # Store kwargs as an attribute

        # Set default values for temperature and max_tokens
        self.kwargs.setdefault('temperature', 0.2)
        self.kwargs.setdefault('max_tokens', 4096)
        self.kwargs.setdefault('model', default_model)

        # Read API key from environment — never hardcode credentials
        api_key = os.environ.get("CEREBRAS_API_KEY", "")
        if not api_key:
            raise ValueError(
                "CEREBRAS_API_KEY environment variable not set. "
                "Export your Cerebras API key before using this client."
            )
        self._api_key = api_key

        # Persistent client with timeout; caller is responsible for closing or
        # using this object as a context manager.
        self._client = httpx.Client(
            base_url='https://api.cerebras.ai/v1',
            timeout=_DEFAULT_TIMEOUT,
        )

    def basic_request(self, prompt, **kwargs):
        """Send a chat-completion request and return the raw response dict."""
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'authorization': f'Bearer {self._api_key}',
        }

        data = {
            "messages": [{"role": "user", "content": prompt}],
            "model": kwargs.get("model", self.model),
            "stream": False,
            "temperature": kwargs.get("temperature", self.kwargs['temperature']),
            "top_p": kwargs.get("top_p", 1),
            "max_tokens": kwargs.get("max_tokens", self.kwargs['max_tokens']),
        }

        response = self._client.post('/chat/completions', headers=headers, json=data)

        if response.status_code != 200:
            raise Exception(
                f"Cerebras API request failed with status {response.status_code}: {response.text}"
            )

        return response.json()

    def __call__(self, prompt, only_completed=True, return_sorted=False, **kwargs):
        response_data = self.basic_request(prompt, **kwargs)
        return [response_data['choices'][0]['message']['content']]


class ElixirSolutionArchitect(dspy.Signature):
    """
    Generate an Elixir code solution for a FAANG-level Solution Architect task, considering the specified context.
    """

    prompt = dspy.InputField(
        desc="Context description containing keywords and specifics (e.g., programming language, target audience, role level).")
    domain_knowledge = dspy.InputField(
        desc="Knowledge base or specific domain requirements to be considered (e.g., Ash Framework in Elixir).")
    experience_level = dspy.InputField(desc="Target experience level of the code solution, such as Solution Architect.")

    explanation = dspy.OutputField(
        desc="Detailed explanation of the code solution, covering why certain design choices were made to align with FAANG-level requirements.")

    code_solution = dspy.OutputField(
        desc="Generated Elixir code that aligns with the context, domain knowledge, and experience level provided.",
    prefix="```elixir\ndefmodule")

def main():
    init_dspy(lm_class=Cerebras, model=default_model, max_tokens=2000)
    # prompt="Elixir FAANG Solution Architect level Ash Resource: FoaF Person"
    pred = dspy.Predict(ElixirSolutionArchitect)
    output = pred(prompt="Elixir FAANG Solution Architect level Ash Resource: FoaF Person",
                  domain_knowledge="Ash Framework in Elixir of Friend of a Friend Ontology in LinkML",
                  experience_level="Solution Architect")
    print(output.explanation)
    solution = f"defmodule {output.code_solution}".split("```")[0]
    print(solution)


if __name__ == '__main__':
    main()
