"""doctor — environment health check for dspygen."""
import os
import sys

import typer

app = typer.Typer(help="Check the dspygen environment and report status.")

# Critical checks that affect exit code
CRITICAL = {"python_version", "dspy", "mcp_server", "lsp_server"}


def _ok(label: str) -> str:
    return typer.style("✓", fg=typer.colors.GREEN) + f"  {label}"


def _fail(label: str) -> str:
    return typer.style("✗", fg=typer.colors.RED) + f"  {label}"


def _warn(label: str) -> str:
    return typer.style("!", fg=typer.colors.YELLOW) + f"  {label}"


@app.callback(invoke_without_command=True)
def doctor(ctx: typer.Context):
    """Check the dspygen environment and report status."""
    if ctx.invoked_subcommand is not None:
        return

    failures: list[str] = []

    typer.echo("\ndspygen doctor\n" + "─" * 40)

    # --- Python version ---
    major, minor = sys.version_info.major, sys.version_info.minor
    py_ver = f"Python {major}.{minor}.{sys.version_info.micro}"
    if (major, minor) >= (3, 10):
        typer.echo(_ok(py_ver))
    else:
        typer.echo(_fail(f"{py_ver}  (need >=3.10)"))
        failures.append("python_version")

    # --- Poetry ---
    import shutil
    if shutil.which("poetry"):
        typer.echo(_ok("poetry found"))
    else:
        typer.echo(_warn("poetry not found in PATH"))

    # --- API keys ---
    for key in ("OPENAI_API_KEY", "GROQ_API_KEY"):
        if os.environ.get(key):
            typer.echo(_ok(f"{key} is set"))
        else:
            typer.echo(_warn(f"{key} is not set"))

    # --- dspy ---
    try:
        import dspy
        typer.echo(_ok(f"dspy {dspy.__version__}"))
    except Exception as exc:
        typer.echo(_fail(f"dspy not importable: {exc}"))
        failures.append("dspy")

    # --- mcp ---
    try:
        import mcp
        version = getattr(mcp, "__version__", "unknown")
        typer.echo(_ok(f"mcp {version}"))
    except Exception as exc:
        typer.echo(_warn(f"mcp not importable: {exc}"))

    # --- pygls ---
    try:
        import pygls
        version = getattr(pygls, "__version__", "unknown")
        typer.echo(_ok(f"pygls {version}"))
    except Exception as exc:
        typer.echo(_warn(f"pygls not importable: {exc}"))

    # --- Ollama ---
    try:
        import urllib.request
        ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        req = urllib.request.urlopen(f"{ollama_host}/api/tags", timeout=2)
        req.read()
        typer.echo(_ok(f"Ollama reachable at {ollama_host}"))
    except Exception:
        typer.echo(_warn("Ollama not reachable (set OLLAMA_HOST if non-default)"))

    # --- ChromaDB ---
    try:
        import chromadb  # noqa: F401
        typer.echo(_ok("chromadb importable"))
    except Exception as exc:
        typer.echo(_warn(f"chromadb not importable: {exc}"))

    # --- dspygen MCP server ---
    try:
        from dspygen.mcp.server import server  # noqa: F401
        typer.echo(_ok("dspygen.mcp.server importable"))
    except Exception as exc:
        typer.echo(_fail(f"dspygen.mcp.server: {exc}"))
        failures.append("mcp_server")

    # --- dspygen LSP server ---
    try:
        from dspygen.lsp.server import server  # noqa: F401
        typer.echo(_ok("dspygen.lsp.server importable"))
    except Exception as exc:
        typer.echo(_fail(f"dspygen.lsp.server: {exc}"))
        failures.append("lsp_server")

    typer.echo("─" * 40)
    critical_failures = [f for f in failures if f in CRITICAL]
    if critical_failures:
        typer.echo(
            typer.style(
                f"\n{len(critical_failures)} critical check(s) failed: {', '.join(critical_failures)}",
                fg=typer.colors.RED,
            )
        )
        raise typer.Exit(code=1)
    else:
        typer.echo(typer.style("\nAll critical checks passed.", fg=typer.colors.GREEN))
        raise typer.Exit(code=0)


def main():
    app()


if __name__ == "__main__":
    main()
