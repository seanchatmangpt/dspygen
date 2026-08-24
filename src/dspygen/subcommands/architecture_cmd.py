"""Inspect DSPyGen architecture standing and operate the bounded CMD rail."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import typer

from dspygen.architecture.cmd_entry import dispatch
from dspygen.architecture.cmd_types import ArchitectureRefusal, Standing
from dspygen.architecture.digest import blake3_hex
from dspygen.architecture.model import BrokerIntent
from dspygen.architecture.verification import verify

app = typer.Typer(help="Verify ontology projections, CMD checkpoints, receipts, replay, and broker boundaries.")


def _json(value: Any) -> str:
    return json.dumps(
        value,
        indent=2,
        sort_keys=True,
        default=lambda item: getattr(item, "value", str(item)),
    )


def _emit(command: str, root: Path, **kwargs: Any) -> None:
    try:
        payload = dispatch(command, root.resolve(), **kwargs)
    except ArchitectureRefusal as exc:
        typer.echo(_json({"schema": "cmd.refusal.v1", "code": exc.code, "detail": exc.detail}), err=True)
        raise typer.Exit(code=2)
    typer.echo(_json(payload))
    standing = payload.get("standing") or payload.get("aggregate_standing") or payload.get("report", {}).get("aggregate_standing")
    if standing in {Standing.BUILD_BROKEN.value, Standing.BLOCKED.value}:
        raise typer.Exit(code=1)


@app.command("verify")
def verify_command(root: Path = typer.Option(Path("."), exists=True, file_okay=False)) -> None:
    """Preserved v1 read-only architecture projection and receipt verifier."""
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
    """Preserved v1 inert BRCE intent constructor; performs no actuation."""
    intent = BrokerIntent(
        intent_id=intent_id,
        action=action,
        payload_digest=blake3_hex(payload.encode()),
        authority=tuple(sorted(authority)),
        resource_ceiling={"max_seconds": max_seconds, "max_tokens": max_tokens},
    )
    typer.echo(json.dumps(intent.to_dict(), indent=2, sort_keys=True))


@app.command("observe")
def observe_command(root: Path = typer.Option(Path("."), exists=True, file_okay=False)) -> None:
    """Emit the exact Git-object repository census."""
    _emit("observe", root)


@app.command("fence-verify")
def fence_verify_command(root: Path = typer.Option(Path("."), exists=True, file_okay=False)) -> None:
    """Verify total semantic, operational, mutation, evidence, and retirement authority."""
    _emit("fence-verify", root)


@app.command("ontology-validate")
def ontology_validate_command(root: Path = typer.Option(Path("."), exists=True, file_okay=False)) -> None:
    """Validate canonical CMD ontology, shapes, and configuration presence."""
    _emit("ontology-validate", root)


@app.command("candidates-enumerate")
def candidates_enumerate_command(
    domain: str = typer.Option("internal", help="internal or external"),
    root: Path = typer.Option(Path("."), exists=True, file_okay=False),
) -> None:
    """Enumerate the bounded, constraint-pruned candidate lattice."""
    _emit("candidates-enumerate", root, domain=domain)


@app.command("candidates-coverage")
def candidates_coverage_command(
    domain: str = typer.Option("internal", help="internal or external"),
    root: Path = typer.Option(Path("."), exists=True, file_okay=False),
) -> None:
    """Independently recompute exhaustive or pairwise coverage."""
    _emit("candidates-coverage", root, domain=domain)


@app.command("plan")
def plan_command(
    domain: str = typer.Option("internal", help="internal or external"),
    index: int = typer.Option(0, min=0),
    root: Path = typer.Option(Path("."), exists=True, file_okay=False),
) -> None:
    """Manufacture a deterministic, non-mutating plan from a verified candidate."""
    _emit("plan", root, domain=domain, index=index)


@app.command("materialize")
def materialize_command(
    grant: str = typer.Option(..., help="Must be local-filesystem-broker"),
    domain: str = typer.Option("internal", help="internal or external"),
    index: int = typer.Option(0, min=0),
    output_root: Path | None = typer.Option(None, file_okay=False),
    root: Path = typer.Option(Path("."), exists=True, file_okay=False),
) -> None:
    """Apply an authorized local plan through staged, atomic, receipted materialization."""
    _emit(
        "materialize",
        root,
        grant=grant,
        domain=domain,
        index=index,
        output_root=str(output_root) if output_root else None,
    )


@app.command("receipt-verify")
def receipt_verify_command(
    receipt: Path = typer.Option(..., exists=True, dir_okay=False),
    root: Path = typer.Option(Path("."), exists=True, file_okay=False),
) -> None:
    """Verify a local materialization receipt against observed bytes."""
    _emit("receipt-verify", root, receipt=str(receipt))


@app.command("replay")
def replay_command(
    receipt: Path = typer.Option(..., exists=True, dir_okay=False),
    root: Path = typer.Option(Path("."), exists=True, file_okay=False),
) -> None:
    """Replay receipt and state relationships without repeating external consequences."""
    _emit("replay", root, receipt=str(receipt))


@app.command("verifier-report")
def verifier_report_command(
    exact_head_sha: str | None = typer.Option(None),
    detached_replay: bool = typer.Option(False),
    output: Path | None = typer.Option(None, dir_okay=False),
    root: Path = typer.Option(Path("."), exists=True, file_okay=False),
) -> None:
    """Write and emit the machine-readable G0-G9 verifier report."""
    _emit(
        "verifier-report",
        root,
        exact_head_sha=exact_head_sha,
        detached_replay=detached_replay,
        output=str(output) if output else None,
    )


@app.command("crown")
def crown_command(
    exact_head_sha: str | None = typer.Option(None),
    detached_replay: bool = typer.Option(False),
    root: Path = typer.Option(Path("."), exists=True, file_okay=False),
) -> None:
    """Execute the G0-G9 crown; external standing remains independently assigned."""
    _emit("crown", root, exact_head_sha=exact_head_sha, detached_replay=detached_replay)
