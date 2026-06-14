"""dspygen doctor command — check environment health."""
import importlib
import os
import sys

import typer

from dspygen.ui.console import print_error, print_info, print_success, print_table, print_warning, spinner

app = typer.Typer(help="Check your dspygen environment for common issues.")

# (package_name, import_name, required)
_CHECKS: list[tuple[str, str, bool]] = [
    ("dspy-ai", "dspy", True),
    ("openai", "openai", True),
    ("rich", "rich", False),
    ("typer", "typer", True),
    ("loguru", "loguru", True),
    ("pydantic", "pydantic", True),
    ("chromadb", "chromadb", False),
]

_ENV_CHECKS: list[tuple[str, bool]] = [
    ("OPENAI_API_KEY", False),
    ("DSPYGEN_HOME", False),
]


def _check_package(import_name: str) -> bool:
    """Return True if *import_name* can be imported."""
    try:
        importlib.import_module(import_name)
        return True
    except ImportError:
        return False


@app.callback(invoke_without_command=True)
def doctor(ctx: typer.Context) -> None:
    """Run all environment health checks and report results."""
    if ctx.invoked_subcommand is not None:
        return

    print_info("Running dspygen environment checks…")

    rows: list[tuple[str, str, str]] = []
    failures = 0

    with spinner("Checking packages…"):
        for pkg_name, import_name, required in _CHECKS:
            ok = _check_package(import_name)
            status = "✓" if ok else ("✗" if required else "–")
            level = "required" if required else "optional"
            rows.append((pkg_name, level, status))
            if not ok and required:
                failures += 1

    print_table(
        headers=["Package", "Level", "Status"],
        rows=rows,
        title="Package Checks",
    )

    env_rows: list[tuple[str, str]] = []
    for var, required in _ENV_CHECKS:
        present = var in os.environ and bool(os.environ[var])
        status = "✓ set" if present else ("✗ missing" if required else "– not set")
        env_rows.append((var, status))
        if not present and required:
            failures += 1

    print_table(headers=["Environment Variable", "Status"], rows=env_rows, title="Environment Variables")

    if failures:
        print_error(f"{failures} required check(s) failed. See above for details.")
        raise typer.Exit(code=1)
    else:
        print_success("All required checks passed.")
