"""
Defines a class called GenSignatureModule, which contains a forward function that takes in inputs and output and returns a signature. The gen_signature_call function creates an instance of the InputsoutputModule class and calls its forward function. The app.command() decorator defines a command called "call" that takes in inputs and output and prints the result of calling the gen_signature_call function. The main function initializes dspy and calls the gen_signature_call function with empty inputs and output.
"""
import dspy
from typer import Typer

from dspygen.modules.signature_renderer import generate_signature_from_prompt
from dspygen.utils.dspy_tools import init_dspy


app = Typer()


class GenSignatureModule(dspy.Module):
    """GenSignatureModule"""

    def forward(self, signature):
        return generate_signature_from_prompt(signature)


def gen_signature_call(signature):
    gen_signature = GenSignatureModule()
    return gen_signature.forward(signature)


@app.command()
def call(signature):
    """GenSignatureModule"""
    init_dspy()

    print(gen_signature_call(signature))


def main():
    init_dspy()
    signature = "celebrity, gossip -> tweet"
    print(gen_signature_call(signature))


if __name__ == "__main__":
    main()
