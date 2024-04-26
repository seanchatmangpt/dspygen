import os

import dspy
from dsp import LM

from dspygen.utils.dspy_tools import init_dspy

from groq import Groq as GroqClient

default_model = "llama3-70b-8192"

class Groq(LM):
    def __init__(self, model=default_model, **kwargs):  #model="mixtral-8x7b-32768", **kwargs):
        # TODO - check of passed model is in list of Groq - if not set to some Groq default
        #model="llama3-70b-8192" # this is a fix cs somewhere the the model getting still set to openai gpt-3.5-turbo-instruct
        super().__init__(model)
        
        print("Groq model used today: " + model)
        self.provider = "default"
        self.history = []
        groq_api_key = os.environ.get("GROQ_API_KEY")

        if groq_api_key is None:
            raise ValueError("GROQ_API_KEY environment variable not found")

        self.client = GroqClient(api_key=os.environ.get("GROQ_API_KEY"))

    def basic_request(self, prompt, **kwargs):
        pass

    def __call__(self, prompt, only_completed=True, return_sorted=False, **kwargs):
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            model=self.kwargs.get("model", default_model),
        )
        return [chat_completion.choices[0].message.content]


def main():
    init_dspy(Groq, model=default_model, max_tokens=2000)
    # init_dspy(max_tokens=2000)
    pred = dspy.Predict("prompt -> code")(prompt="Fast API CRUD endpoint for fire alarm global IoT network")
    print(pred.code)


if __name__ == '__main__':
    main()
