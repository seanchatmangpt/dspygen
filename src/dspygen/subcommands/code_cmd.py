"""code"""
import typer
from dspygen.modules.python_source_code_module import python_source_code_call
from dspygen.utils.dspy_tools import init_dspy

app = typer.Typer(help="Code subcommands.")


@app.command(name="create")
def _create(todo: str = typer.Argument(..., help="What to do?")):
    """create"""
    init_dspy()
    code = python_source_code_call(todo)
    typer.echo(code)
