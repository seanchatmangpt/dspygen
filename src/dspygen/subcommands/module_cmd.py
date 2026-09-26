"""Generate and inspect DSPy modules without ambient model execution."""
from __future__ import annotations

import hashlib
import json
import keyword
import re
from pathlib import Path

import typer

app = typer.Typer(help="Generate DSPy modules or execute admitted pipeline definitions.")
_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _snake_case(value: str) -> str:
    value = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", value)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value).lower()


def _parse_inputs(value: str) -> list[str]:
    inputs = [item.strip() for item in value.split(",") if item.strip()]
    if not inputs:
        raise typer.BadParameter("at least one input is required")
    if len(set(inputs)) != len(inputs):
        raise typer.BadParameter("input names must be unique")
    for item in inputs:
        if not _IDENTIFIER.fullmatch(item) or keyword.iskeyword(item):
            raise typer.BadParameter(f"invalid Python input identifier: {item!r}")
    return inputs


@app.command(name="new")
def new_module(
    class_name: str = typer.Option(..., "--class-name", "-cn"),
    inputs: str = typer.Option(..., "--inputs", "-i"),
    output: str = typer.Option(..., "--output", "-o"),
    output_dir: Path = typer.Option(Path("."), "--output-dir", "-d"),
    force: bool = typer.Option(False, "--force"),
    print_source: bool = typer.Option(False, "--print-source"),
) -> None:
    """Manufacture a complete composable module and emit a content receipt."""

    from dspygen.modules.gen_dspy_module import (
        DSPyModuleTemplate,
        render_dspy_module,
    )

    try:
        model = DSPyModuleTemplate(
            class_name=class_name,
            inputs=_parse_inputs(inputs),
            output=output,
        )
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc

    source = render_dspy_module(model)
    destination = output_dir.resolve() / f"{_snake_case(class_name)}_module.py"
    if destination.exists() and not force:
        typer.echo(
            json.dumps(
                {
                    "status": "REFUSED",
                    "reason": "MODULE_EXISTS",
                    "path": str(destination),
                }
            )
        )
        raise typer.Exit(code=2)

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(f".{destination.name}.dspygen-tmp")
    data = source.encode("utf-8")
    temporary.write_bytes(data)
    temporary.replace(destination)
    receipt = {
        "status": "ALIVE",
        "path": str(destination),
        "sha256": hashlib.sha256(data).hexdigest(),
        "inputs": model.inputs,
        "output": model.output,
        "class_name": f"{model.class_name}Module",
    }
    if print_source:
        typer.echo(source)
    typer.echo(json.dumps(receipt, indent=2, sort_keys=True))


@app.command(name="pipeline")
def pipeline(yaml_file: Path) -> None:
    """Execute a validated YAML pipeline after explicit model initialization."""

    from dspygen.modules.dspygen_dsl_pipeline import process_yaml_pipeline
    from dspygen.utils.dspy_tools import init_dspy

    init_dspy()
    typer.echo(str(process_yaml_pipeline(yaml_file)))


@app.command("help")
def cli_help(question: str) -> None:
    """Answer a question using the configured local model provider."""

    from dspygen.utils.cli_tools import chatbot

    chatbot(question, Path(__file__).read_text(encoding="utf-8"))
