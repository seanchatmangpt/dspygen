"""User-friendly error formatting for dspygen."""
import sys
import traceback

import typer


class DspygenError(Exception):
    """Base error class for dspygen with actionable context.

    Attributes:
        message: Human-readable description of what went wrong.
        hint: Suggested action or command to resolve the issue.
        docs_url: Optional URL pointing to relevant documentation.
    """

    message: str = "An unexpected dspygen error occurred"
    hint: str = ""
    docs_url: str = ""

    def __init__(
        self,
        message: str | None = None,
        hint: str | None = None,
        docs_url: str | None = None,
    ) -> None:
        self.message = message or self.__class__.message
        self.hint = hint or self.__class__.hint
        self.docs_url = docs_url or self.__class__.docs_url
        super().__init__(self.message)


class LMNotConfiguredError(DspygenError):
    """Raised when a DSPy language model has not been configured.

    This typically means ``init_dspy()`` was not called or the API key
    environment variable is missing.
    """

    message = "DSPy LM not configured"
    hint = "Run init_dspy() or dspygen config set OPENAI_API_KEY <key>"
    docs_url = "https://dspygen.readthedocs.io/configuration"


# Shadow the built-in to provide a dspygen-specific variant.
class ModuleNotFoundError(DspygenError):  # noqa: A001
    """Raised when a requested dspygen module is not found in the registry."""

    message = "Module not found in registry"
    hint = "Run dspygen module list to see available modules"
    docs_url = "https://dspygen.readthedocs.io/modules"


def format_error(exc: Exception) -> str:
    """Format any exception into a human-readable string with context.

    For :class:`DspygenError` instances the hint and docs URL are included
    when present.  For all other exceptions the traceback is appended so the
    user has enough information to report the problem.

    Args:
        exc: The exception to format.

    Returns:
        A multi-line string ready to be printed to the terminal.
    """
    if isinstance(exc, DspygenError):
        lines = [f"Error: {exc.message}"]
        if exc.hint:
            lines.append(f"Hint:  {exc.hint}")
        if exc.docs_url:
            lines.append(f"Docs:  {exc.docs_url}")
        return "\n".join(lines)

    tb = traceback.format_exc()
    return f"Unexpected error: {type(exc).__name__}: {exc}\n\n{tb}"


def handle_error(exc: Exception) -> None:
    """Print a formatted error message and exit with status code 1.

    Attempts to use rich for coloured output when available; falls back to
    plain :func:`typer.echo`.

    Args:
        exc: The exception that was raised.
    """
    msg = format_error(exc)

    try:
        from rich.console import Console
        from rich.panel import Panel

        err_console = Console(stderr=True)
        title = "dspygen error" if isinstance(exc, DspygenError) else "unexpected error"
        err_console.print(Panel(msg, title=title, border_style="red", expand=False))
    except ImportError:
        typer.echo(typer.style(msg, fg=typer.colors.RED), err=True)

    sys.exit(1)
