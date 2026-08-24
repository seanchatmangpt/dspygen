"""Stable machine-readable operational entry points for G0-G9."""
from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict, replace
from pathlib import Path
from typing import Any

from dspygen.architecture.cmd_kernel import coverage_report, enumerate_candidates, make_plan
from dspygen.architecture.cmd_materializer import materialize, replay_materialization
from dspygen.architecture.cmd_observer import observe
from dspygen.architecture.cmd_repository import load_constraints, load_dimensions, policy_digest
from dspygen.architecture.cmd_types import (
    ArchitectureRefusal,
    Artifact,
    CandidateState,
    Ownership,
    Reversal,
    Standing,
)
from dspygen.architecture.cmd_verifier import verify_crown, write_report


def _dump(value: Any) -> None:
    print(json.dumps(value, indent=2, sort_keys=True, default=lambda item: getattr(item, "value", str(item))))


def _candidate_set(root: Path, domain: str):
    observation = observe(root)
    dimensions = load_dimensions(root, domain)
    constraints = load_constraints(root, domain)
    digest = policy_digest(root)
    candidates = enumerate_candidates(dimensions, constraints, observation.tree_digest, digest)
    return observation, dimensions, constraints, candidates, digest


def _manufacture_plan(root: Path, domain: str, index: int, authorized: bool = False):
    _, _, _, candidates, digest = _candidate_set(root, domain)
    candidate = replace(
        candidates[index],
        state=CandidateState.AUTHORIZED if authorized else CandidateState.VERIFIED,
    )
    artifact = Artifact(
        path=f"plans/{domain}/{candidate.signature}.json",
        body=json.dumps({"candidate": candidate.option_map()}, sort_keys=True) + "\n",
        ownership=Ownership.EXCLUSIVE,
        owner="dspygen-cmd-kernel",
        reversal=Reversal.REVERSIBLE_WITH_SNAPSHOT,
    )
    return make_plan(candidate, digest, (artifact,))


def dispatch(command: str, root: Path, **kwargs: Any) -> dict[str, Any]:
    root = root.resolve()
    if command == "observe":
        return {"schema": "cmd.observation.v1", **observe(root).to_dict()}
    if command == "fence-verify":
        observation = observe(root)
        failures = [
            entry.path
            for entry in observation.entries
            if "UNKNOWN"
            in {
                entry.semantic_owner,
                entry.operational_owner,
                entry.mutation_authority,
                entry.evidence_authority,
                entry.retirement_dependency,
            }
        ]
        return {
            "schema": "cmd.fence-report.v1",
            "revision": observation.revision,
            "failures": failures,
            "standing": Standing.PARTIAL_ALIVE.value if not failures else Standing.BUILD_BROKEN.value,
        }
    if command == "ontology-validate":
        required = [
            root / ".specify/cmd/repository.ttl",
            root / ".specify/cmd/shapes/cmd-shapes.ttl",
            root / ".specify/cmd/architecture.toml",
        ]
        missing = [str(path.relative_to(root)) for path in required if not path.is_file()]
        return {
            "schema": "cmd.ontology-report.v1",
            "missing": missing,
            "standing": Standing.ALIVE.value if not missing else Standing.BUILD_BROKEN.value,
        }
    if command in {"candidates-enumerate", "candidates-coverage"}:
        domain = kwargs.get("domain", "internal")
        _, dimensions, _, candidates, _ = _candidate_set(root, domain)
        if command == "candidates-enumerate":
            return {
                "schema": "cmd.candidates.v1",
                "domain": domain,
                "count": len(candidates),
                "candidates": [candidate.__dict__ for candidate in candidates],
            }
        mode = "exhaustive" if domain == "internal" else "pairwise"
        return {
            "schema": "cmd.coverage.v1",
            "domain": domain,
            **coverage_report(dimensions, candidates, mode),
        }
    if command == "plan":
        domain = kwargs.get("domain", "internal")
        plan = _manufacture_plan(root, domain, int(kwargs.get("index", 0)))
        return {"schema": "cmd.plan.v1", **plan.to_dict()}
    if command == "materialize":
        if kwargs.get("grant") != "local-filesystem-broker":
            raise ArchitectureRefusal("AUTH-GRANT-MISSING", "local-filesystem-broker")
        domain = kwargs.get("domain", "internal")
        plan = _manufacture_plan(root, domain, int(kwargs.get("index", 0)), authorized=True)
        output_root = Path(kwargs.get("output_root") or root).resolve()
        receipt = materialize(output_root, plan)
        return {
            "schema": "cmd.materialize-result.v1",
            "plan_id": plan.plan_id,
            "receipt": {**asdict(receipt), "standing_result": receipt.standing_result.value, "receipt_id": receipt.receipt_id},
            "standing": Standing.ALIVE.value,
        }
    if command in {"verifier-report", "crown"}:
        exact_head = kwargs.get("exact_head_sha") or os.environ.get("DSPYGEN_EXACT_HEAD_SHA")
        detached = bool(kwargs.get("detached_replay") or os.environ.get("DSPYGEN_DETACHED_REPLAY") == "1")
        report = verify_crown(root, exact_head_sha=exact_head, detached_replay=detached)
        if command == "verifier-report":
            output = kwargs.get("output")
            path = write_report(root, report, Path(output) if output else None)
            return {"schema": "cmd.verifier-write.v1", "path": str(path), "report": report.to_dict()}
        return report.to_dict()
    if command in {"receipt-verify", "replay"}:
        receipt_path = Path(kwargs["receipt"]).resolve()
        ok, result = replay_materialization(root, receipt_path)
        return {
            "schema": "cmd.replay-report.v1",
            "ok": ok,
            "result": result,
            "standing": Standing.ALIVE.value if ok else Standing.BUILD_BROKEN.value,
        }
    raise ValueError(command)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dspygen-cmd")
    parser.add_argument("--root", type=Path, default=Path("."))
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("observe", "fence-verify", "ontology-validate", "verifier-report", "crown"):
        command = sub.add_parser(name)
        if name == "verifier-report":
            command.add_argument("--output")
        if name in {"verifier-report", "crown"}:
            command.add_argument("--exact-head-sha")
            command.add_argument("--detached-replay", action="store_true")
    for name in ("candidates-enumerate", "candidates-coverage", "plan", "materialize"):
        command = sub.add_parser(name)
        command.add_argument("--domain", choices=("internal", "external"), default="internal")
        if name in {"plan", "materialize"}:
            command.add_argument("--index", type=int, default=0)
        if name == "materialize":
            command.add_argument("--grant", required=True)
            command.add_argument("--output-root")
    for name in ("receipt-verify", "replay"):
        command = sub.add_parser(name)
        command.add_argument("--receipt", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = vars(build_parser().parse_args(argv))
    command = args.pop("command")
    root = args.pop("root")
    payload = dispatch(command, root, **args)
    _dump(payload)
    standing = payload.get("standing") or payload.get("aggregate_standing") or payload.get("report", {}).get("aggregate_standing")
    return 0 if standing not in {Standing.BUILD_BROKEN.value, Standing.BLOCKED.value} else 1


if __name__ == "__main__":
    raise SystemExit(main())
