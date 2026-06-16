import os

import dspy
from dsp import LM
from groq import Groq as GroqClient

from dspygen.utils.dspy_tools import init_dspy

# Updated to a current, high-performance Groq-hosted model
default_model = "llama-3.3-70b-versatile"


class Groq(LM):
    def __init__(self, model=default_model, **kwargs):
        super().__init__(model)

        self.provider = "default"
        self.history = []

        groq_api_key = os.environ.get("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError(
                "GROQ_API_KEY environment variable not set. "
                "Export your Groq API key before using this client."
            )

        self.client = GroqClient(api_key=groq_api_key)
        # Store model on instance for use in basic_request / __call__
        self._model = model

    def basic_request(self, prompt, **kwargs):
        """Send a chat-completion request and return the Groq response object."""
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=kwargs.get("model", self._model),
                temperature=kwargs.get("temperature", 0.6),
                max_tokens=kwargs.get("max_tokens", 2048),
            )
            return chat_completion
        except Exception as exc:
            raise RuntimeError(f"Groq API request failed: {exc}") from exc

    def __call__(self, prompt, only_completed=True, return_sorted=False, **kwargs):
        chat_completion = self.basic_request(prompt, **kwargs)
        return [chat_completion.choices[0].message.content]


def main():
    init_dspy(lm_class=Groq, model=default_model, max_tokens=2000)
    pred = dspy.Predict("prompt -> code")(prompt="Fast API CRUD endpoint for fire alarm global IoT network")
    print(pred.code)


if __name__ == '__main__':
    main()
