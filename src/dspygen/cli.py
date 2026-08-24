"""DSPyGen command-line interface."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from importlib import import_module, metadata
from pathlib import Path
from typing import Any

import typer

from dspygen.project import ProjectRefusal, materialize_project, plan_project

app = typer.Typer(no_args_is_help=True)
_COMMAND_LOAD_FAILURES: dict[str, str] = {}


def version_callback(value: bool) -> None:
    if value:
        try:
            version = metadata.version("dspygen")
        except metadata.PackageNotFoundError:
            version = "source-tree"
        typer.echo(version)
        raise typer.Exit()


@app.callback()
def main_callback(
    version: bool = typer.Option(
        False,
        "--version",
        "-V",
        callback=version_callback,
        is_eager=True,
        help="Show the dspygen version and exit.",
    ),
) -> None:
    """DSPyGen — deterministic construction and orchestration for DSPy programs."""


def load_commands(directory: str = "subcommands") -> dict[str, str]:
    """Load command adapters without allowing one optional surface to kill the CLI."""

    script_dir = Path(__file__).parent
    subcommands_dir = script_dir / directory
    if not subcommands_dir.is_dir():
        return _COMMAND_LOAD_FAILURES

    for path in sorted(subcommands_dir.glob("*_cmd.py")):
        command_name = path.stem.removesuffix("_cmd")
        module_name = f"dspygen.{directory}.{path.stem}"
        try:
            module = import_module(module_name)
        except Exception as exc:  # Each failed adapter is topology, not CLI death.
            _COMMAND_LOAD_FAILURES[command_name] = f"{type(exc).__name__}: {exc}"
            continue
        command_app = getattr(module, "app", None)
        if command_app is not None:
            app.add_typer(command_app, name=command_name)
    return _COMMAND_LOAD_FAILURES


@app.command()
def init(
    project_name: str = typer.Argument(...),
    author_email: str = typer.Argument("todo@todo.com"),
    author_name: str = typer.Argument(""),
    output_dir: Path = typer.Option(Path("."), "--output-dir", "-d"),
    force: bool = typer.Option(False, "--force", help="Replace admitted scaffold files."),
    install: bool = typer.Option(
        False,
        "--install",
        help="Explicitly install the generated project after construction.",
    ),
) -> None:
    """Construct an offline project scaffold and emit a machine-readable receipt."""

    try:
        plan = plan_project(
            project_name,
            output_dir=output_dir,
            author_email=author_email,
            author_name=author_name,
        )
        receipt = materialize_project(plan, force=force)
    except ProjectRefusal as exc:
        typer.echo(json.dumps({"status": "REFUSED", "reason": exc.reason, "detail": exc.detail}))
        raise typer.Exit(code=2) from exc

    payload: dict[str, Any] = json.loads(receipt.to_json())
    if install:
        command = [sys.executable, "-m", "pip", "install", "-e", plan.output_dir]
        completed = subprocess.run(command, check=False)
        payload["install"] = {"command": command, "exit_code": completed.returncode}
        if completed.returncode != 0:
            payload["status"] = "BUILD_BROKEN"
            typer.echo(json.dumps(payload, indent=2, sort_keys=True))
            raise typer.Exit(code=completed.returncode)
    typer.echo(json.dumps(payload, indent=2, sort_keys=True))


@app.command()
def doctor() -> None:
    """Report admitted command surfaces and optional-adapter failures as JSON."""

    payload = {
        "status": "PARTIAL_ALIVE" if _COMMAND_LOAD_FAILURES else "ALIVE",
        "python": sys.version.split()[0],
        "loaded_commands": sorted(
            command.name for command in app.registered_groups if command.name
        ),
        "load_failures": dict(sorted(_COMMAND_LOAD_FAILURES.items())),
        "legacy_pipe_compat_disabled": os.getenv("DSPYGEN_DISABLE_LEGACY_PIPE_COMPAT") == "1",
    }
    typer.echo(json.dumps(payload, indent=2, sort_keys=True))


@app.command(name="tutor")
def tutor(question: str = "") -> None:
    """Guide development through the configured local model provider."""

    from dspygen.utils.cli_tools import chatbot
    from dspygen.utils.dspy_tools import init_ol

    init_ol(max_tokens=3000, model="qwen2:7b-instruct")
    chatbot(question, "")


def configure_injections(broker_url: str) -> None:
    """Configure the explicit realtime adapter; this function does not connect."""

    def config(binder: Any) -> None:
        from dspygen.rdddy.async_realtime_client import AsyncRealtimeClient

        binder.bind(AsyncRealtimeClient, AsyncRealtimeClient(broker_url))

    import inject

    inject.configure(config)


async def run_service_colony(broker_url: str = "ws://localhost:4000/socket/websocket") -> None:
    """Explicitly actuate the legacy service-colony connection."""

    from dspygen.rdddy.service_colony import ServiceColony

    configure_injections(broker_url)
    await ServiceColony().connect()


def main() -> None:
    app()


load_commands()

if __name__ == "__main__":
    main()
