import subprocess
from typing import List, Optional
from pydantic import BaseModel, Field

from dspygen.experiments.aider_bp.aider_blueprint import AiderBlueprint


def create_aider_command(blueprint: AiderBlueprint) -> List[str]:
    """
    Convert AiderBlueprint to a list of aider CLI command options.

    Args:
        blueprint (AiderBlueprint): The blueprint object to convert.

    Returns:
        List[str]: A list of command line arguments for the aider CLI.
    """
    cmd = ["aider"]

    # Add files to create and edit
    for file in blueprint.files_to_create:
        cmd.extend(["--file", file])

    for file in blueprint.files_to_edit:
        cmd.extend(["--file", file])

    # Add read-only files
    for file in blueprint.read_only_files:
        cmd.extend(["--read", file])

    # Add model options
    if blueprint.model:
        cmd.extend(["--model", blueprint.model])

    # Add other settings
    if blueprint.auto_test:
        cmd.append("--auto-test")
    if blueprint.lint:
        cmd.append("--lint")
    if blueprint.pretty_output:
        cmd.append("--pretty")
    if blueprint.dark_mode:
        cmd.append("--dark-mode")
    if blueprint.message:
        cmd.extend(["--message", blueprint.message])

    # Add additional arguments
    if blueprint.additional_args:
        cmd.extend(blueprint.additional_args)

    return cmd


def send_blueprint_to_aider_cli(blueprint: AiderBlueprint):
    """
    Sends the AiderBlueprint to the aider CLI.

    Args:
        blueprint (AiderBlueprint): The blueprint object to send.
    """
    # Generate the command
    aider_command = create_aider_command(blueprint)

    # Execute the command using subprocess
    try:
        subprocess.run(aider_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing aider CLI: {e}")


if __name__ == "__main__":
    # Example blueprint data
    blueprint = AiderBlueprint(
        files_to_create=["lib/live_twitter/timeline/tweet.ex"],
        files_to_edit=["lib/live_twitter/accounts/user.ex"],
        read_only_files=["README.md", "CONVENTIONS.md"],
        model="gpt-4",
        auto_test=True,
        lint=True,
        pretty_output=True,
        dark_mode=False,
        additional_args=["--verbose"],
        message="Define resources for tweets and likes in the LiveTwitter app."
    )

    # Send the blueprint to the aider CLI
    send_blueprint_to_aider_cli(blueprint)
