"""Inspect DSPyGen architecture standing and construct BRCE intents."""
from __future__ import annotations

import json
from pathlib import Path

import typer

from dspygen.architecture.digest import blake3_hex
from dspygen.architecture.model import BrokerIntent
from dspygen.architecture.verification import verify

app = typer.Typer(help="Verify ontology projections, receipts, replay, and broker boundaries.")


@app.command("verify")
def verify_command(root: Path = typer.Option(Path("."), exists=True, file_okay=False)) -> None:
    """Run the independent read-only architecture verifier."""
    report = verify(root.resolve())
    typer.echo(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    if not report.ok:
        raise typer.Exit(code=1)


@app.command("intent")
def intent_command(
    intent_id: str,
    action: str,
    payload: str,
    authority: list[str] = typer.Option([], "--authority"),
    max_tokens: int = typer.Option(0, min=0),
    max_seconds: int = typer.Option(0, min=0),
) -> None:
    """Construct a bounded intent addressed to BRCE without executing it."""
    intent = BrokerIntent(
        intent_id=intent_id,
        action=action,
        payload_digest=blake3_hex(payload.encode()),
        authority=tuple(sorted(authority)),
        resource_ceiling={"max_seconds": max_seconds, "max_tokens": max_tokens},
    )
    typer.echo(json.dumps(intent.to_dict(), indent=2, sort_keys=True))
