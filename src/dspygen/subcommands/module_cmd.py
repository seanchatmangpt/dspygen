"""Generate DSPy module"""
from importlib import import_module

import os

import inflection
import typer

from dspygen.dsl.dsl_pipeline_executor import execute_pipeline
from dspygen.modules.gen_dspy_module import  DSPyModuleTemplate, SignatureDspyModuleModule
from dspygen.utils.cli_tools import chatbot
from dspygen.utils.dspy_tools import init_dspy
from dspygen.utils.file_tools import dspy_modules_dir, source_dir, get_source

app = typer.Typer(help="Generate DSPy Modules or call exist ones.")


@app.command(name="new")
def new_module(
        class_name: str = typer.Option(..., "--class-name", "-cn", help="The name of the module class"),
        inputs: str = typer.Option(None, "--inputs", "-i", help="A comma-separated list of input names"),
        output: str = typer.Option(None, "--output", "-o", help="Output name for the module"),
):
    """Generate a new dspy.Module. Inputs and output will be static."""
    if len(inputs) == 0 or output is None:
        raise ValueError("Please provide a signature or input and output.")

    mdl = DSPyModuleTemplate(class_name=class_name, inputs=inputs.split(','), output=output)

    source = SignatureDspyModuleModule().forward(mdl)

    file_name = f"{inflection.underscore(class_name)}_module.py"

    with open(dspy_modules_dir() / file_name, "w") as file:
        file.write(source)

    print(source)

    print(f"Module saved to {dspy_modules_dir() / file_name}")


def load_commands(directory: str = "modules"):
    subcommands_dir = source_dir() / directory

    for filename in os.listdir(subcommands_dir):
        if filename.endswith("_module.py"):
            module_name = f'{__name__.split(".")[0]}.{directory}.{filename[:-3]}'
            module = import_module(module_name)
            if hasattr(module, "app"):
                app.add_typer(module.app, name=filename[:-10])


def main():
    inputs = ["input1", "input2", "input3"]
    output = "output"
    print()


if __name__ == "__main__":
    main()
else:
    load_commands()


@app.command("help")
def cli_help(question: str):
    """Answers the user questions with a helpful chatbot."""
    chatbot(question, get_source(__file__))


