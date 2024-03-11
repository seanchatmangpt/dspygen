"""dspygen CLI."""
import sys
from importlib import import_module, metadata
import subprocess


import os

from pathlib import Path

import inflection
import typer

from dspygen.utils.cli_tools import chatbot
from dspygen.utils.file_tools import source_dir
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


def package_installed(package_name, min_version):
    try:
        version = metadata.version(package_name)
        return version >= min_version
    except metadata.PackageNotFoundError:
        return False


def check_or_install_packages():
    packages_requirements = {
        "cruft": "2.12.0",
        "cookiecutter": "2.1.1",
    }

    for package, min_version in packages_requirements.items():
        if not package_installed(package, min_version):
            print(f"{package} not found or version is below {min_version}. Installing/upgrading...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", f"{package}>={min_version}"])
        # else:
        #     print(f"{package} meets the version requirement.")


@app.command()
def init(package_name: str):
    """Initialize the DSPygen project."""
    check_or_install_packages()

    package_name = inflection.underscore(package_name)

    # The template URL and the configuration for the new project
    template_url = "https://github.com/radix-ai/poetry-cookiecutter"
    # Project initialization logic, assuming static configuration for demonstration
    try:
        print(f"Creating new package named {package_name}...")
        subprocess.check_call(["cruft", "create", template_url,
                               "--config-file", source_dir("config.yaml"),
                               "--extra-context", f'{{"package_name": "{package_name}"}}',
                               "--no-input"])

        # We need to install dspygen in the package's virtual environment
        # It uses poetry to manage the virtual environment
        # Change to the package directory
        # Run the command to initialize the virtual environment
        # Run the command to install dspygen in the virtual environment
        package_dir = Path(package_name)
        os.chdir(package_dir)
        subprocess.check_call(["poetry", "install"])
        subprocess.check_call(["poetry", "run", "pip", "install", "-e", "."])
        # Create the virtual environment
        subprocess.check_call(["poetry", "env", "use", "python"])
        # Install the package in the virtual environment
        subprocess.check_call(["poetry", "add", "-D", "dspygen"])
        # Change back to the original directory
        os.chdir("..")

        print(f"Project {package_name} initialized successfully.")
    except subprocess.CalledProcessError:
        print("Failed to initialize the new package.")
        sys.exit(1)


TUTOR_CONTEXT = """DSPyGen: AI Development Simplified
DSPyGen revolutionizes AI development by bringing the "Convention over Configuration" philosophy to language model (LM) pipelines. Inspired by Ruby on Rails, it offers a CLI for creating, developing, and deploying with DSPy modules, emphasizing quick setup and modular design for streamlined project workflows.

Key Features:

Quick Initialization: Rapidly configure your AI project, mirroring the simplicity of Ruby on Rails.
Modular Design: Generate and enhance DSPy modules with ease, promoting a scalable and flexible development environment.
User-Friendly Commands: Manage your AI projects effortlessly through an intuitive command structure.
Chatbot Assistance: Embedded support to guide through the development process, enhancing user experience.
Using DSPyGen Modules:
DSPyGen's core lies in its modules, designed for seamless integration and code optimization. Here’s how to leverage them:

dspygen is a command-line tool.
It helps generate various components for a project.
Usage includes options and commands.
Options like --install-completion, --show-completion, and --help are available.
Commands include actor, assert, browser, command, help, init, lm, module, sig, and tutor.
Each command serves a specific purpose:
actor: Related to actors.
assert: Generates assertions for dspy.
browser: Pertains to browser functionality.
command: Generates or adds subcommands.
help: Provides assistance and updates help files.
init: Initializes a DSPygen project.
lm: Generates language models.
module: Deals with generating or calling DSPy modules.
sig: Generates dspy.Signatures.
tutor: Guides through project development with DSPyGen.

blog: Calls modules related to blogging.
book_appointment: Invokes modules for scheduling appointments.
chat_bot: Initiates module calls for chatbots.
checker: Calls modules for checking or validating.
choose_function: Initiates module calls involving choice or selection functions.
dflss: Related to Six Sigma methodology, possibly for invoking process improvement modules.
gen_cli: Triggers modules for command-line interfaces.
gen_dspy: Calls modules specific to DSPy.
gen_keyword_arguments: Initiates module calls with keyword arguments.
gen_signature: Invokes signature-related modules.
html: For modules related to HTML.
insight_tweet: Calls modules for generating insightful tweets.
message: Initiates module calls for messaging.
module_docstring: Triggers module calls for documenting modules.
product_bot: Invokes module calls for product-related bots.
prompt_function_call: Triggers modules for prompting function calls.
python_expert: For modules related to Python expertise.
python_source_code: Initiates module calls for generating Python source code.
source_code_pep8_docs: Triggers module calls for source code with PEP8 documentation.
subject_destination_audience_newsletter_article: Initiates module calls for newsletter articles.
text_summary_module: Calls modules for summarizing text.
to_elixir: Initiates module calls to convert modules to Elixir format.

Use this information to guide the usage of the DSPyGen CLI and its modules.
"""

@app.command(name="tutor")
def tutor(question: str = ""):
    """Guide you through developing a project with DSPyGen."""
    chatbot(question, TUTOR_CONTEXT, model="gpt-4")


def main():
    print("Welcome to DSPyGen CLI!")
    # init("test_project")

    # import json
    # import yaml

    # current_module = sys.modules[__name__]
    # module_dict = module_to_dict(current_module, include_docstring=False)
    # print(yaml.dump(module_dict))
    # print(json.dumps(module_dict, indent=2))



if __name__ == '__main__':
    main()
else:
    load_commands()
