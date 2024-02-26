"""dspygen CLI."""
from importlib import import_module

import os

from pathlib import Path

import typer

app = typer.Typer()


# Load existing subcommands
def load_commands(directory: str = "subcommands"):
    script_dir = Path(__file__).parent
    subcommands_dir = script_dir / directory

    for filename in os.listdir(subcommands_dir):
        if filename.endswith("_cmd.py"):
            module_name = f'{__name__.split(".")[0]}.{directory}.{filename[:-3]}'
            module = import_module(module_name)
            if hasattr(module, "app"):
                app.add_typer(module.app, name=filename[:-7])


load_commands()


@app.command("init")
def init(project_name: str):
    """Initialize the DSPygen project."""
    typer.echo(f"Initializing {project_name}.")


@app.command("help")
def cli_help(question: str):
    """Answers the user questions with a helpful chatbot."""
    typer.echo(f"TODO: Answer {question}.")
