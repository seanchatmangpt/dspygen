"""Shared console and output utilities."""
import json
import sys
from contextlib import contextmanager

import typer

try:
    from rich import print as rprint
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.syntax import Syntax
    from rich.table import Table

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    Console = None
    Panel = None
    Progress = None
    SpinnerColumn = None
    TextColumn = None
    Syntax = None
    Table = None
    rprint = None

console = Console(stderr=True) if RICH_AVAILABLE else None  # type: ignore[misc]


def print_success(msg: str) -> None:
    """Print a success message with a green checkmark prefix."""
    if RICH_AVAILABLE and console is not None:
        console.print(f"[bold green]✓[/bold green] {msg}")
    else:
        typer.echo(typer.style(f"✓ {msg}", fg=typer.colors.GREEN, bold=True))


def print_error(msg: str) -> None:
    """Print an error message with a red X prefix."""
    if RICH_AVAILABLE and console is not None:
        console.print(f"[bold red]✗[/bold red] {msg}")
    else:
        typer.echo(typer.style(f"✗ {msg}", fg=typer.colors.RED, bold=True), err=True)


def print_warning(msg: str) -> None:
    """Print a warning message with a yellow warning prefix."""
    if RICH_AVAILABLE and console is not None:
        console.print(f"[bold yellow]⚠[/bold yellow]  {msg}")
    else:
        typer.echo(typer.style(f"⚠  {msg}", fg=typer.colors.YELLOW, bold=True))


def print_info(msg: str) -> None:
    """Print an informational message with a blue info prefix."""
    if RICH_AVAILABLE and console is not None:
        console.print(f"[bold blue]ℹ[/bold blue]  {msg}")
    else:
        typer.echo(typer.style(f"ℹ  {msg}", fg=typer.colors.BLUE, bold=True))


def print_table(headers: list, rows: list, title: str = "") -> None:
    """Print data in a formatted table.

    Args:
        headers: Column header labels.
        rows: List of row tuples/lists matching the headers.
        title: Optional table title displayed above the table.
    """
    if RICH_AVAILABLE and console is not None:
        table = Table(title=title or None, show_header=True, header_style="bold cyan")
        for header in headers:
            table.add_column(str(header))
        for row in rows:
            table.add_row(*[str(cell) for cell in row])
        console.print(table)
    else:
        if title:
            typer.echo(typer.style(title, bold=True))
        col_widths = [len(str(h)) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    col_widths[i] = max(col_widths[i], len(str(cell)))
        header_line = "  ".join(str(h).ljust(col_widths[i]) for i, h in enumerate(headers))
        typer.echo(typer.style(header_line, bold=True))
        typer.echo("-" * len(header_line))
        for row in rows:
            typer.echo("  ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)))


def print_json(data: dict) -> None:
    """Print a dictionary as formatted JSON.

    Args:
        data: Dictionary to render as JSON.
    """
    if RICH_AVAILABLE and console is not None:
        from rich.json import JSON

        console.print(JSON(json.dumps(data, indent=2, default=str)))
    else:
        typer.echo(json.dumps(data, indent=2, default=str))


def print_code(code: str, language: str = "python") -> None:
    """Print syntax-highlighted source code.

    Args:
        code: The source code string to display.
        language: The programming language for syntax highlighting (default: python).
    """
    if RICH_AVAILABLE and console is not None and Syntax is not None:
        syntax = Syntax(code, language, theme="monokai", line_numbers=True)
        console.print(syntax)
    else:
        typer.echo(code)


@contextmanager
def spinner(message: str):
    """Context manager that shows a spinner during long operations.

    Args:
        message: Text to display alongside the spinner.

    Yields:
        The progress instance (rich Progress) or None if rich is unavailable.

    Example:
        with spinner("Loading data..."):
            load_data()
    """
    if RICH_AVAILABLE and Progress is not None:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
            console=console,
        ) as progress:
            progress.add_task(description=message, total=None)
            yield progress
    else:
        typer.echo(f"... {message}")
        yield None
