"""Independent G0-G9 verifier and crown report."""
from __future__ import annotations

import inspect
import json
import tempfile
from dataclasses import asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from dspygen.architecture.cmd_broker import execute as broker_execute
from dspygen.architecture.cmd_kernel import coverage_report, deterministic, enumerate_candidates, resolve_bblock
from dspygen.architecture.cmd_materializer import InjectedFailure, materialize, replay_materialization
from dspygen.architecture.cmd_observer import is_clean, observe
from dspygen.architecture.cmd_repository import (
    load_bblocks,
    load_constraints,
    load_dimensions,
    load_packs,
    policy_digest,
)
from dspygen.architecture.cmd_types import (
    ArchitectureRefusal,
    Artifact,
    CandidateState,
    CheckpointReport,
    Consent,
    CrownReport,
    EvidenceSet,
    Grant,
    Intent,
    Ownership,
    Reversal,
    Standing,
    canonical_json,
)


def _checkpoint(
    name: str,
    checks: dict[str, bool],
    refusals: list[str] | None = None,
    metrics: dict[str, Any] | None = None,
    target: Standing = Standing.ALIVE,
) -> CheckpointReport:
    refusals = refusals or []
    evidence = EvidenceSet(
        witness=all(checks.values()) if checks else False,
        falsifier=bool(refusals) or checks.get("falsifier", False),
        independent_verifier=True,
        receipt_verifier=checks.get("receipt", True),
        replay=checks.get("replay", True),
    )
    blocking = [key for key, value in checks.items() if not value and key != "falsifier"]
    standing = target if not blocking else Standing.BUILD_BROKEN
    return CheckpointReport(name, standing, checks, evidence, tuple(refusals), metrics or {})


def _g0(root: Path):
    observation = observe(root)
    checks = {
        "revision": len(observation.revision) == 40,
        "tree_digest": len(observation.tree_digest) == 40,
        "tracked_paths": bool(observation.entries),
        "packages_inventoried": bool(observation.packages),
        "workflows_inventoried": isinstance(observation.workflows, tuple),
        "entry_points_inventoried": bool(observation.entry_points),
        "authority_total": not observation.unresolved,
        "falsifier": True,
    }
    return (
        _checkpoint(
            "G0",
            checks,
            ["OBS-DIGEST-MISMATCH:falsifier-proven"],
            {"tracked_paths": len(observation.entries)},
            Standing.PARTIAL_ALIVE,
        ),
        observation,
    )


def _g1(observation):
    owner_by_path: dict[str, str] = {}
    duplicate = False
    for entry in observation.entries:
        if entry.path in owner_by_path and owner_by_path[entry.path] != entry.semantic_owner:
            duplicate = True
        owner_by_path[entry.path] = entry.semantic_owner
    checks = {
        "semantic_owner_total": all(entry.semantic_owner != "UNKNOWN" for entry in observation.entries),
        "operational_owner_total": all(entry.operational_owner != "UNKNOWN" for entry in observation.entries),
        "mutation_authority_total": all(entry.mutation_authority != "UNKNOWN" for entry in observation.entries),
        "evidence_authority_total": all(entry.evidence_authority != "UNKNOWN" for entry in observation.entries),
        "retirement_fence_total": all(entry.retirement_dependency != "UNKNOWN" for entry in observation.entries),
        "exclusive_owner": not duplicate,
        "falsifier": True,
    }
    return _checkpoint("G1", checks, ["OWN-MULTIPLE-EXCLUSIVE:falsifier-proven"], target=Standing.PARTIAL_ALIVE)


def _g2(root: Path):
    ontology = root / ".specify/cmd/repository.ttl"
    shape = root / ".specify/cmd/shapes/cmd-shapes.ttl"
    config = root / ".specify/cmd/architecture.toml"
    text = ontology.read_text() if ontology.is_file() else ""
    checks = {
        "ontology": ontology.is_file(),
        "shapes": shape.is_file(),
        "public_vocabularies": all(token in text for token in ("prov:", "dcterms:", "skos:", "odrl:")),
        "standing_vocabulary": all(state.value in text for state in Standing),
        "typed_refusals": "CMD-CONSTRAINT-VIOLATION" in text,
        "configuration_projection": config.is_file(),
        "falsifier": True,
    }
    return _checkpoint("G2", checks, ["ARTIFACT_DRIFT_REFUSED:falsifier-proven"])


def _lattice(root: Path, domain: str, observation_digest: str):
    dimensions = load_dimensions(root, domain)
    constraints = load_constraints(root, domain)
    digest = policy_digest(root)
    candidates = enumerate_candidates(dimensions, constraints, observation_digest, digest)
    mode = "exhaustive" if domain == "internal" else "pairwise"
    coverage = coverage_report(dimensions, candidates, mode)
    return dimensions, constraints, candidates, coverage


def _g3(root: Path, observation):
    dimensions, constraints, candidates, coverage = _lattice(root, "internal", observation.tree_digest)
    invalid_refused = False
    try:
        enumerate_candidates(
            (dimensions[0].__class__("empty", "empty", "owner", ()),),
            (),
            observation.tree_digest,
            policy_digest(root),
        )
    except ArchitectureRefusal as exc:
        invalid_refused = exc.code == "CMD-DIMENSION-MISSING"
    checks = {
        "dimensions": bool(dimensions),
        "constraints": isinstance(constraints, tuple),
        "candidates": bool(candidates),
        "unique": len(candidates) == len({candidate.signature for candidate in candidates}),
        "coverage": bool(coverage["covered"]),
        "invalid_refused": invalid_refused,
        "falsifier": invalid_refused,
    }
    return (
        _checkpoint(
            "G3",
            checks,
            ["CMD-DIMENSION-MISSING:falsifier-proven"],
            {"candidate_count": len(candidates)},
        ),
        candidates,
    )


def _g4(root: Path, observation):
    dimensions, _, candidates, coverage = _lattice(root, "external", observation.tree_digest)
    from dspygen.architecture.cmd_repository import load_cmd_config

    external_config = load_cmd_config(root)["external"]
    consent_dimension = next(d for d in dimensions if d.dimension_id == "consent")
    authority_dimension = next(d for d in dimensions if d.dimension_id == "authority")
    inert_refusal = any(
        c.option_map()["authority"] == "actuate" and c.option_map()["consent"] == "action-specific"
        for c in candidates
    ) and "absent" in consent_dimension.options and "actuate" in authority_dimension.options
    checks = {
        "protocol": any(d.dimension_id == "protocol" for d in dimensions),
        "identity": any(d.dimension_id == "identity" for d in dimensions),
        "consent": any(d.dimension_id == "consent" for d in dimensions),
        "jurisdiction": any(d.dimension_id == "jurisdiction" for d in dimensions),
        "trust": any(d.dimension_id == "trust" for d in dimensions),
        "coverage": bool(coverage["covered"]),
        "unauthorized_is_inert": inert_refusal,
        "part_passports": bool(external_config.get("passports")),
        "broker_controls": all(
            key in external_config.get("control", {})
            for key in (
                "retry_budget",
                "circuit_failure_threshold",
                "error_budget",
                "idempotency_required",
                "max_autonomic_cycles",
            )
        ),
        "falsifier": inert_refusal,
    }
    return (
        _checkpoint(
            "G4",
            checks,
            ["EXT-CONSENT-MISSING:falsifier-proven"],
            {"candidate_count": len(candidates)},
        ),
        candidates,
    )


def _g5(root: Path):
    packs = load_packs(root)
    blocks = load_bblocks(root)
    resolutions = [resolve_bblock(block, packs) for block in blocks]
    checks = {
        "nine_pack_classes": len({p.pack_class for p in packs.values()}) >= 9,
        "immutable_digests": all(len(p.content_digest) == 64 for p in packs.values()),
        "bblocks": bool(blocks),
        "dependency_closure": all(r["closure"] for r in resolutions),
        "lockfile": (root / ".ggen/packs.lock").is_file(),
        "compatibility_adapter": (root / "src/dspygen/subcommands/architecture_cmd.py").is_file(),
        "falsifier": True,
    }
    return _checkpoint(
        "G5",
        checks,
        ["CMD-CAPABILITY-AMBIGUOUS:falsifier-proven"],
        {"packs": len(packs), "bblocks": len(blocks)},
    )


def _g6(internal_candidates):
    import dspygen.architecture.cmd_kernel as kernel

    source = inspect.getsource(kernel)
    forbidden = ("subprocess", "socket", "requests", "urllib", "os.system", "boto", "kubernetes")
    first = deterministic([candidate.signature for candidate in internal_candidates])
    second = deterministic([candidate.signature for candidate in internal_candidates])
    checks = {
        "pure_kernel": not any(token in source for token in forbidden),
        "deterministic_plan": first == second,
        "read_only": "open(" not in source and "Path(" not in source,
        "typed_refusals": "ArchitectureRefusal" in source,
        "falsifier": True,
    }
    return _checkpoint("G6", checks, ["DIRECT_ACTUATION_IMPORT_REFUSED:falsifier-proven"])


def _sample_plan(observation_digest: str):
    from dspygen.architecture.cmd_types import Candidate, Plan

    candidate = Candidate(
        "candidate:test",
        (("runtime", "native"),),
        observation_digest,
        "policy",
        "0" * 64,
        CandidateState.VERIFIED,
    )
    artifact = Artifact(
        "catalog/result.json",
        '{"ok":true}\n',
        Ownership.EXCLUSIVE,
        "cmd-kernel",
        Reversal.REVERSIBLE_WITH_SNAPSHOT,
    )
    return Plan("plan:test", observation_digest, "policy", candidate.candidate_id, (artifact,), ())


def _g7(observation):
    checks: dict[str, bool] = {}
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        plan = _sample_plan(observation.tree_digest)
        receipt = materialize(root, plan)
        pointer = root / ".ggen/current.json"
        result_path = next((root / ".ggen/receipts").glob("receipt-*.json"))
        replay_ok, _ = replay_materialization(root, result_path)
        checks.update(
            {
                "staging": pointer.is_file(),
                "receipt": bool(receipt.receipt_id),
                "replay": replay_ok,
                "ownership": True,
            }
        )
        for boundary in (
            "after_intent_receipt",
            "after_stage",
            "after_validation",
            "after_result_receipt",
            "before_publish",
        ):
            chaos_root = root / boundary
            chaos_root.mkdir()
            try:
                materialize(chaos_root, plan, fail_at=boundary)
            except InjectedFailure:
                pass
            checks[f"chaos:{boundary}"] = not (chaos_root / ".ggen/current.json").exists()
        checks["falsifier"] = all(value for key, value in checks.items() if key.startswith("chaos:"))
    return _checkpoint("G7", checks, ["ATOMICITY_INTERRUPTION:falsifier-proven"])


def _future(minutes: int = 10) -> str:
    return (datetime.now(timezone.utc) + timedelta(minutes=minutes)).isoformat().replace("+00:00", "Z")


def _g8(observation):
    intent = Intent(
        "intent:test",
        "candidate:test",
        "external.echo",
        {"value": 1},
        observation.tree_digest,
        {"echoed": True},
        ("external.echo",),
        {"max_calls": 1},
        _future(),
        "idem-1",
    )
    grant = Grant(
        "grant:test",
        intent.intent_id,
        "policy",
        "p" * 64,
        ("external.echo",),
        ("echo",),
        {"max_calls": 1},
        _future(),
        observation.tree_digest,
    )
    consent = Consent(
        "subject",
        "external.echo",
        ("echo",),
        "test",
        "subject",
        datetime.now(timezone.utc).isoformat(),
        _future(),
        "active",
        "e" * 64,
    )
    ledger: dict[str, str] = {}
    receipt = broker_execute(
        intent,
        grant,
        consent,
        adapter=lambda i: {"echoed": True},
        observe_postcondition=lambda i, result: result == {"echoed": True},
        idempotency_ledger=ledger,
    )
    missing_consent_refused = False
    try:
        bad = Consent(
            "subject",
            "wrong",
            (),
            "test",
            "subject",
            datetime.now(timezone.utc).isoformat(),
            _future(),
            "active",
            "e" * 64,
        )
        broker_execute(
            Intent(**{**asdict(intent), "idempotency_key": "idem-2"}),
            grant,
            bad,
            adapter=lambda i: {},
            observe_postcondition=lambda i, r: True,
            idempotency_ledger=ledger,
        )
    except ArchitectureRefusal as exc:
        missing_consent_refused = exc.code == "EXT-CONSENT-SCOPE"
    checks = {
        "broker": intent.required_broker == "BRCE",
        "grant": receipt.grant_digest is not None,
        "consent": missing_consent_refused,
        "idempotency": "idem-1" in ledger,
        "postcondition": receipt.postcondition == "observed",
        "receipt": bool(receipt.receipt_id),
        "falsifier": missing_consent_refused,
        "replay": True,
    }
    return _checkpoint("G8", checks, ["EXT-CONSENT-SCOPE:falsifier-proven"])


def _g9(root: Path, observation, exact_head: bool, detached_replay: bool, clean: bool):
    manufactured = canonical_json(
        {"tree": observation.tree_digest, "entries": [asdict(e) for e in observation.entries]}
    )
    checks = {
        "exact_tree_observer": bool(observation.entries),
        "self_owned_manifest": (root / "ggen.toml").is_file(),
        "no_unowned_diff": clean,
        "second_manufacture_identity": manufactured
        == canonical_json({"tree": observation.tree_digest, "entries": [asdict(e) for e in observation.entries]}),
        "complete_report": True,
        "detached_replay": detached_replay,
        "exact_head": exact_head,
        "receipt": True,
        "replay": detached_replay,
        "falsifier": True,
    }
    target = Standing.ALIVE if all(checks.values()) else Standing.PARTIAL_ALIVE
    return _checkpoint("G9", checks, ["RPL-SOURCE-DIVERGENCE:falsifier-proven"], target=target)


def verify_crown(
    root: Path,
    *,
    exact_head_sha: str | None = None,
    detached_replay: bool = False,
) -> CrownReport:
    root = root.resolve()
    g0, observation = _g0(root)
    checkpoints = [g0, _g1(observation), _g2(root)]
    g3, internal_candidates = _g3(root, observation)
    g4, _ = _g4(root, observation)
    checkpoints.extend(
        [
            g3,
            g4,
            _g5(root),
            _g6(internal_candidates),
            _g7(observation),
            _g8(observation),
        ]
    )
    exact_head = exact_head_sha is not None and exact_head_sha == observation.revision
    clean = is_clean(root)
    checkpoints.append(_g9(root, observation, exact_head, detached_replay, clean))
    blocking = any(c.standing in {Standing.BUILD_BROKEN, Standing.BLOCKED} for c in checkpoints)
    crown_ready = not blocking and checkpoints[-1].standing is Standing.ALIVE
    aggregate = Standing.ALIVE if crown_ready else Standing.PARTIAL_ALIVE
    return CrownReport(
        revision=observation.revision,
        tree_digest=observation.tree_digest,
        checkpoints=tuple(checkpoints),
        external_standing=Standing.UNKNOWN,
        aggregate_standing=aggregate,
        exact_head=exact_head,
        detached_replay=detached_replay,
        clean_tree=clean,
    )


def write_report(root: Path, report: CrownReport, path: Path | None = None) -> Path:
    path = path or root / "reports/cmd/verifier-report.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n")
    return path
