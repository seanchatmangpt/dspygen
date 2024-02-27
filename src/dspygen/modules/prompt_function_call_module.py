"""
The `documentation` field is not provided.
"""
import dspy
from typer import Typer
from dspygen.utils.dspy_tools import init_dspy


app = Typer()


class PromptFunctionCallModule(dspy.Module):
    """PromptFunctionCallModule"""

    def forward(self, prompt):
        pred = dspy.Predict("prompt -> function_call")
        result = pred(prompt=prompt).function_call
        return result


def prompt_function_call_call(prompt):
    prompt_function_call = PromptFunctionCallModule()
    return prompt_function_call.forward(prompt=prompt)


@app.command()
def call(prompt):
    """PromptFunctionCallModule"""
    init_dspy()

    print(prompt_function_call_call(prompt=prompt))


def main():
    init_dspy()
    prompt = ""
    print(prompt_function_call_call(prompt=prompt))


if __name__ == "__main__":
    main()
