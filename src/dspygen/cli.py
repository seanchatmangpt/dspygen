"""dspygen CLI."""
import sys
from importlib import import_module

import dspy
import os

from pathlib import Path

import typer

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


README = """DSPyGen: Streamlining AI Development
DSPyGen, influenced by the efficiency and modularity of Ruby on Rails, is a powerful command-line interface (CLI) 
designed to revolutionize AI development by leveraging DSPy modules. This tool simplifies the process of creating, 
developing, and deploying language model (LM) pipelines, embodying the Ruby on Rails philosophy of 
"Convention over Configuration" for AI projects.

Features
Quick Initialization: Set up your DSPyGen project in seconds, echoing Ruby on Rails' ease of starting new projects.
Modular Approach: Inspired by Ruby on Rails' modular design, DSPyGen allows for the easy generation and enhancement of 
DSPy modules.
Intuitive Command Structure: With user-friendly commands, managing your AI development workflow becomes as 
straightforward as web development with Ruby on Rails.
Embedded Chatbot Assistance: For guidance and support, DSPyGen includes a chatbot, making it easier to navigate 
through your development process."""


@app.command("help")
def cli_help(question: str):
    """Answers the user questions with a helpful chatbot."""
    chatbot(question, README)


def gbot(question, context):
    from groq import Groq

    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"you are a helpful assistant. This is what you help with: {context}",
            },
            {
                "role": "user",
                "content": f"{question}",
            },
        ],
        model="llama2-70b-4096",
    )

    print(chat_completion.choices[0].message.content.rstrip())


def chatbot(question, context, history=""):
    init_dspy(max_tokens=2000)

    qa = dspy.ChainOfThought("question, context -> answer")
    response = qa(question=question, context=context).answer
    history += response
    print(f"Chatbot: {response}")
    confirmed = False
    while not confirmed:
        confirm = typer.prompt("Did this answer your question? [y/N]", default="N")

        if confirm.lower() in ["y", "yes"]:
            confirmed = True
        else:
            want = typer.prompt("How can I help more?")

            question = f"{history}\n{want}"
            question = question[-1000:]

            response = qa(question=question, context=README).answer
            history += response
            print(f"Chatbot: {response}")

    return history


# @app.command(name="tutor", help="Guide you through developing a project with DSPyGen.")

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
