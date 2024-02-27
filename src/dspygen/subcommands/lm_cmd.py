"""lm"""
import typer


app = typer.Typer("Generate Language Models")


@app.command(name="new")
def new_lm():
    """Generates a new language model."""
    typer.echo("Uses jinja and dspy module to create a language model.")
    