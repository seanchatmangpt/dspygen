"""help"""
import subprocess

import typer

from dspygen.utils.cli_tools import chatbot

app = typer.Typer(help="Help chatbot and realtime help file update.")


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


@app.command("bot")
def cli_help(question: str = ""):
    """Answers the user questions with a helpful chatbot."""
    chatbot(question, README)


# Define a command to gather and save help text for subcommands
@app.command(name="gather")
def gather_help(output_file: str = "help.txt"):
    """
    Gather and save help text for subcommands to a file.
    Example usage: python your_app.py gather-help help_output.txt
    """
    help_text = subprocess.check_output(["dspygen", "--help"], text=True)
    help_text += "\n\n"

    # Iterate through registered subcommands and gather their help text
    for command in app.registered_commands:
        try:
            # Run the CLI with the --help flag for the current subcommand
            if command.name:
                subcommand_help = subprocess.check_output(["dspygen", command.name, "--help"], text=True)
                help_text += f"Command: {command.name}\n"
                help_text += f"{subcommand_help}\n\n"
        except subprocess.CalledProcessError:
            typer.echo(f"Error gathering help text for subcommand '{command.name}'")

    # Save the gathered help text to the specified output file
    try:
        with open(output_file, "w") as file:
            file.write(help_text)
        typer.echo(f"Help text for subcommands saved to '{output_file}'.")
    except Exception as e:
        typer.echo(f"Error saving help text: {str(e)}")


def main():
    output_file = "help.txt"
    help_text = subprocess.check_output(["dspygen", "--help"], text=True)
    help_text += "\n\n"

    # Iterate through registered subcommands and gather their help text
    for command in app.registered_commands:
        try:
            # Run the CLI with the --help flag for the current subcommand
            if command.name:
                subcommand_help = subprocess.check_output(["dspygen", command.name, "--help"], text=True)
                help_text += f"Command: {command.name}\n"
                help_text += f"{subcommand_help}\n\n"
        except subprocess.CalledProcessError:
            typer.echo(f"Error gathering help text for subcommand '{command.name}'")

    # Save the gathered help text to the specified output file
    try:
        with open(output_file, "w") as file:
            file.write(help_text)
        typer.echo(f"Help text for subcommands saved to '{output_file}'.")
    except Exception as e:
        typer.echo(f"Error saving help text: {str(e)}")


if __name__ == '__main__':
    main()
