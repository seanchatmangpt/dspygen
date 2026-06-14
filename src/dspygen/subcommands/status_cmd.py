"""dspygen status — show system health, metrics, and configuration."""
import os

import typer

app = typer.Typer(help="Show dspygen system status.")

_STATUS_ICONS = {"ok": "[OK]   ", "warn": "[WARN] ", "fail": "[FAIL] "}


@app.callback(invoke_without_command=True)
def status(ctx: typer.Context) -> None:
    """Display health checks, metrics, LM config, and server status."""
    if ctx.invoked_subcommand is not None:
        return

    _print_health()
    _print_metrics()
    _print_lm_config()
    _print_module_count()
    _print_server_status()


# ---------------------------------------------------------------------------
# Sections
# ---------------------------------------------------------------------------

def _print_health() -> None:
    typer.echo("\n=== Health Checks ===")
    try:
        from dspygen.observability.health import check_all
        results = check_all()
        for r in results:
            icon = _STATUS_ICONS.get(r.status, "[????]  ")
            typer.echo(f"  {icon}{r.name:<28} {r.message}  ({r.duration_ms:.1f} ms)")
        overall = "ok" if all(r.status != "fail" for r in results) else "DEGRADED"
        typer.echo(f"\n  Overall: {overall}")
    except Exception as exc:
        typer.echo(f"  Could not run health checks: {exc}", err=True)


def _print_metrics() -> None:
    typer.echo("\n=== Metrics ===")
    try:
        from dspygen.observability.metrics import get_all_metrics
        data = get_all_metrics()
        if not data:
            typer.echo("  (no metrics collected yet)")
            return
        for name, meta in data.items():
            typer.echo(f"  {name}: {meta['value']}  [{meta['type']}]")
    except Exception as exc:
        typer.echo(f"  Could not retrieve metrics: {exc}", err=True)


def _print_lm_config() -> None:
    typer.echo("\n=== LM Configuration ===")
    try:
        import dspy
        lm = dspy.settings.lm  # type: ignore[attr-defined]
        if lm is None:
            typer.echo("  No LM configured (dspy.settings.lm is None)")
        else:
            typer.echo(f"  Model   : {getattr(lm, 'model', lm)}")
            typer.echo(f"  Provider: {getattr(lm, 'provider', 'unknown')}")
    except Exception as exc:
        typer.echo(f"  Could not read LM settings: {exc}", err=True)


def _print_module_count() -> None:
    typer.echo("\n=== DSPy Modules ===")
    try:
        from dspygen.utils.file_tools import dspy_modules_dir
        modules_dir = dspy_modules_dir()
        count = sum(1 for f in os.listdir(modules_dir) if f.endswith("_module.py"))
        typer.echo(f"  Modules found: {count}  (in {modules_dir})")
    except Exception as exc:
        typer.echo(f"  Could not count modules: {exc}", err=True)


def _print_server_status() -> None:
    typer.echo("\n=== MCP / LSP Servers ===")
    _probe("MCP server (mcp)", "mcp")
    _probe("LSP server (pygls)", "pygls")
    typer.echo("")


def _probe(label: str, package: str) -> None:
    import importlib.util
    available = importlib.util.find_spec(package) is not None
    icon = "[OK]   " if available else "[WARN] "
    state = "importable" if available else "not installed"
    typer.echo(f"  {icon}{label:<30} {state}")
