import httpx
import os

import dspy
from dsp import LM
from sungen.utils.dspy_tools import init_dspy

default_model = "llama3.1-70b"


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

        # No environments variable or SDK; use direct HTTP requests
        self.client = httpx.Client(base_url='https://api.cerebras.ai/v1')

    def basic_request(self, prompt, **kwargs):
        # Implementation placeholder for other potential requests
        pass

    def __call__(self, prompt, only_completed=True, return_sorted=False, **kwargs):
        # Define the headers
        headers = {
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': 'Bearer demo-xmyc249jrym6xx6r5ty3k4cfkn6rpvyj48dj5k3hffcf2pp5',
            'content-type': 'application/json',
            'dnt': '1',
            'origin': 'https://inference.cerebras.ai',
            'priority': 'u=1, i',
            'referer': 'https://inference.cerebras.ai/',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'x-stainless-arch': 'unknown',
            'x-stainless-lang': 'js',
            'x-stainless-os': 'Unknown',
            'x-stainless-package-version': '1.0.1',
            'x-stainless-runtime': 'browser:chrome',
            'x-stainless-runtime-version': '128.0.0'
        }

        # Prepare the payload
        data = {
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "model": kwargs.get("model", self.model),
            "stream": False,
            "temperature": kwargs.get("temperature", self.kwargs['temperature']),
            "top_p": kwargs.get("top_p", 1),
            "max_tokens": kwargs.get("max_tokens", self.kwargs['max_tokens'])
        }

        # Make the request to the Cerebras API
        response = self.client.post('/chat/completions', headers=headers, json=data)

        # Handle response and extract content
        if response.status_code == 200:
            response_data = response.json()
            return [response_data['choices'][0]['message']['content']]
        else:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")


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
