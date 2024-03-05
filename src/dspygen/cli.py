"""dspygen CLI."""
import sys
from importlib import import_module

import dspy
import os

from pathlib import Path

import typer

from dspygen.utils.cli_tools import chatbot
from dspygen.utils.dspy_tools import init_dspy
from dspygen.utils.module_tools import module_to_dict

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




@app.command("init")
def init(project_name: str):
    """Initialize the DSPygen project."""
    typer.echo(f"Initializing {project_name}.")





TUTOR_CONTEXT = """DSPyGen: AI Development Simplified
DSPyGen revolutionizes AI development by bringing the "Convention over Configuration" philosophy to language model (LM) pipelines. Inspired by Ruby on Rails, it offers a CLI for creating, developing, and deploying with DSPy modules, emphasizing quick setup and modular design for streamlined project workflows.

Key Features:

Quick Initialization: Rapidly configure your AI project, mirroring the simplicity of Ruby on Rails.
Modular Design: Generate and enhance DSPy modules with ease, promoting a scalable and flexible development environment.
User-Friendly Commands: Manage your AI projects effortlessly through an intuitive command structure.
Chatbot Assistance: Embedded support to guide through the development process, enhancing user experience.
Using DSPyGen Modules:
DSPyGen's core lies in its modules, designed for seamless integration and code optimization. Here’s how to leverage them:

Generate New Modules: Use dspygen module new "<inputs -> outputs>" --class-name="<ClassName>" to create modules tailored to specific functionalities.
Optimize Python Code: Beautify and adhere to PEP8 standards using dspygen module python_source_code call "<code>".
Integrate with Web Apps: Employ dspygen module react_jsx call "ComponentName" for React app development with AI features.
Engage on Social Media: Transform insights into engaging content with dspygen module insight_tweet call "Message"."""

@app.command(name="tutor")
def tutor(question: str = ""):
    """Guide you through developing a project with DSPyGen."""
    chatbot(question, TUTOR_CONTEXT)


def main():
    import json
    import yaml

    current_module = sys.modules[__name__]
    module_dict = module_to_dict(current_module, include_docstring=False)
    print(yaml.dump(module_dict))
    # print(json.dumps(module_dict, indent=2))



if __name__ == '__main__':
    main()
else:
    load_commands()
