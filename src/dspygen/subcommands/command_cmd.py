from pathlib import Path

import typer

from dspygen.typetemp.functional import render

app = typer.Typer(help="""Generate new sub commands or add to existing ones.""")


subcommand_template = '''"""{{ subcommand_name }}"""
import typer


app = typer.Typer()


@app.command(name="{{ new_command_name }}")
def {{ sub_command_name }}_{{ new_command_name }}():
    """{{ new_command_name }}"""
    typer.echo("Running {{ new_command_name }} subcommand.")
    
'''


# Define the subcommand to generate subcommand modules
@app.command(
    name="new",
)
def module(subcommand_name: str, new_command_name: str):
    """
    Generate a new subcommand module with the given name.
    Example usage: dspygen command new new_command
    """
    script_dir = Path(__file__).parent

    # Generate the filename for the new subcommand module
    filename = f"{subcommand_name}_cmd.py"
    module_path = script_dir / filename

    # Check if the existing subcommand module file exists
    if module_path.exists():
        typer.echo(f"Subcommand module '{subcommand_name}' already exists.")
        return

    # Create the subcommand module file
    with open(script_dir / filename, "w") as file:
        # You can customize the content of the module here
        source = render(subcommand_template, subcommand_name=subcommand_name, new_command_name=new_command_name)
        file.write(source)

    typer.echo(f"Subcommand module '{subcommand_name}' generated successfully!")


add_template = ''' 
@app.command(name="{{ new_command_name }}")
def {{ sub_command_name }}_{{ new_command_name }}():
    """{{ new_command_name }}"""
    typer.echo("Running {{ new_command_name }} subcommand.")

'''


@app.command(name="add")
def add_command(sub_command_name: str, new_command_name: str):
    """
    Add a new command to an existing subcommand module.
    Example usage: dspygen command add existing_command new_command
    """
    script_dir = Path(__file__).parent

    # Construct the filename for the existing subcommand module
    filename = f"{sub_command_name}_cmd.py"

    # Construct the path to the existing subcommand module
    module_path = script_dir / filename

    # Check if the existing subcommand module file exists
    if not module_path.exists():
        typer.echo(f"Subcommand module '{sub_command_name}' does not exist.")
        return

    # Append the code to the existing subcommand module file
    with open(module_path, "a") as module_file:
        new_command_code = render(
            add_template,
            sub_command_name=sub_command_name,
            new_command_name=new_command_name,
        )
        module_file.write(new_command_code)

    typer.echo(
        f"New command '{new_command_name}' added to subcommand module '{sub_command_name}' successfully!"
    )
