"""poet"""
import subprocess

import typer


app = typer.Typer()


@app.command(name="pub")
def _pub():
    """pub"""
    typer.echo("Running pub subcommand.")
    # poetry publish --build
    subprocess.run(["poetry", "publish", "--build"], check=True)
    