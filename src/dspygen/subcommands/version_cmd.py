"""version — show dspygen and dependency version information."""
import json
import sys
from importlib.metadata import version as pkg_version, PackageNotFoundError

import typer

app = typer.Typer(help="Show dspygen and dependency version information.")


def _get_version(package: str) -> str:
    try:
        return pkg_version(package)
    except PackageNotFoundError:
        return "not installed"


@app.callback(invoke_without_command=True)
def version_info(
    ctx: typer.Context,
    as_json: bool = typer.Option(False, "--json", help="Output version info as JSON"),
):
    """Show dspygen version and key dependency versions."""
    if ctx.invoked_subcommand is not None:
        return

    data = {
        "dspygen": _get_version("dspygen"),
        "python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "dspy": _get_version("dspy-ai") or _get_version("dspy"),
        "mcp": _get_version("mcp"),
        "pygls": _get_version("pygls"),
    }

    # dspy ships under different dist names depending on the version
    if data["dspy"] == "not installed":
        data["dspy"] = _get_version("dspy")

    if as_json:
        typer.echo(json.dumps(data, indent=2))
        return

    typer.echo(f"\ndspygen  {typer.style(data['dspygen'], fg=typer.colors.CYAN, bold=True)}")
    typer.echo("─" * 36)
    typer.echo(f"  {'python':<12} {data['python']}")
    typer.echo(f"  {'dspy':<12} {data['dspy']}")
    typer.echo(f"  {'mcp':<12} {data['mcp']}")
    typer.echo(f"  {'pygls':<12} {data['pygls']}")
    typer.echo("")


def main():
    app()


if __name__ == "__main__":
    main()
