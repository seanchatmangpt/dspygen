"""Generate DSPy module"""
from importlib import import_module

import os

import typer

from dspygen.modules.gen_dspy_module import gen_dspy_module_call
from dspygen.modules.file_name_module import file_name_call
from dspygen.utils.dspy_tools import init_dspy
from dspygen.utils.file_tools import dspy_modules_dir, source_dir

app = typer.Typer(help="Generate DSPy Modules or call exist ones.")


@app.command(name="new")
def new_module(signature: str):
    """Generate a new dspy.Module. Example: dspygen module new 'text -> summary'"""
    init_dspy()

    source = gen_dspy_module_call(signature)

    file_name = file_name_call(source + "\nName the file by the class name.", "py")

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
    print('main')


load_commands()

if __name__ == '__main__':
    main()
