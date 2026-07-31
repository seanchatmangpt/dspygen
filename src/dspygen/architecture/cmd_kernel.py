"""Pure, deterministic CMD kernel. This module performs no actuation."""
from __future__ import annotations

from dataclasses import asdict
from itertools import combinations, product
from typing import Any, Mapping, Sequence

from dspygen.architecture.cmd_types import (
    ArchitectureRefusal,
    AtomicPack,
    BuildingBlock,
    Candidate,
    CandidateState,
    Constraint,
    Dimension,
    Intent,
    Plan,
    canonical_json,
    content_id,
)
from dspygen.architecture.digest import blake3_hex

MAX_CANDIDATES_DEFAULT = 8192
REQUIRED_BROKER = "BRCE"


def _validate_dimensions(dimensions: Sequence[Dimension]) -> None:
    ids = [d.dimension_id for d in dimensions]
    if len(ids) != len(set(ids)):
        raise ArchitectureRefusal("CMD-DIMENSION-DUPLICATE")
    for dimension in dimensions:
        if not dimension.options:
            raise ArchitectureRefusal("CMD-DIMENSION-MISSING", dimension.dimension_id)
        if len(dimension.options) != len(set(dimension.options)):
            raise ArchitectureRefusal("CMD-OPTION-DUPLICATE", dimension.dimension_id)


def candidate_is_valid(selection: Mapping[str, str], constraints: Sequence[Constraint]) -> tuple[bool, str | None]:
    for constraint in constraints:
        if all(selection.get(k) == v for k, v in constraint.when.items()):
            for dimension, allowed in constraint.require.items():
                if selection.get(dimension) not in allowed:
                    return False, constraint.refusal_code
            for dimension, denied in constraint.exclude.items():
                if selection.get(dimension) in denied:
                    return False, constraint.refusal_code
    return True, None


def enumerate_candidates(
    dimensions: Sequence[Dimension],
    constraints: Sequence[Constraint],
    observation_digest: str,
    policy_digest: str,
    max_candidates: int = MAX_CANDIDATES_DEFAULT,
) -> tuple[Candidate, ...]:
    _validate_dimensions(dimensions)
    raw_count = 1
    for dimension in dimensions:
        raw_count *= len(dimension.options)
        if raw_count > max_candidates:
            raise ArchitectureRefusal("CMD-RESOURCE-BOUND", f"raw_candidates={raw_count}")
    candidates: list[Candidate] = []
    dimension_ids = tuple(d.dimension_id for d in dimensions)
    for values in product(*(d.options for d in dimensions)):
        selection = dict(zip(dimension_ids, values))
        valid, _ = candidate_is_valid(selection, constraints)
        if not valid:
            continue
        ordered = tuple(sorted(selection.items()))
        signature = blake3_hex(canonical_json(ordered).encode())
        candidates.append(
            Candidate(
                candidate_id=f"candidate:{signature}",
                options=ordered,
                source_observation_digest=observation_digest,
                constraint_policy_digest=policy_digest,
                signature=signature,
            )
        )
    signatures = [candidate.signature for candidate in candidates]
    if len(signatures) != len(set(signatures)):
        raise ArchitectureRefusal("CMD-CANDIDATE-DUPLICATE")
    return tuple(candidates)


def coverage_report(
    dimensions: Sequence[Dimension],
    candidates: Sequence[Candidate],
    mode: str,
    t: int = 2,
) -> dict[str, Any]:
    observed = [candidate.option_map() for candidate in candidates]
    if mode == "exhaustive":
        raw = 1
        for dimension in dimensions:
            raw *= len(dimension.options)
        return {
            "mode": mode,
            "raw_product": raw,
            "valid_candidates": len(candidates),
            "unique_signatures": len({c.signature for c in candidates}),
            "covered": len(candidates) == len({c.signature for c in candidates}),
        }
    if mode in {"pairwise", "t-wise"}:
        width = 2 if mode == "pairwise" else t
        required: set[tuple[tuple[str, str], ...]] = set()
        covered: set[tuple[tuple[str, str], ...]] = set()
        for selection in observed:
            for dims in combinations(dimensions, width):
                interaction = tuple(sorted((d.dimension_id, selection[d.dimension_id]) for d in dims))
                required.add(interaction)
                covered.add(interaction)
        missing = sorted(required - covered)
        return {
            "mode": mode,
            "t": width,
            "required": len(required),
            "covered_count": len(required & covered),
            "missing": missing,
            "covered": not missing,
        }
    if mode == "constraint-covering":
        return {"mode": mode, "covered": bool(candidates), "valid_candidates": len(candidates)}
    raise ArchitectureRefusal("CMD-COVERAGE-MODE-UNKNOWN", mode)


def dependency_closure(packs: Mapping[str, AtomicPack], roots: Sequence[str]) -> tuple[str, ...]:
    visiting: set[str] = set()
    visited: set[str] = set()
    ordered: list[str] = []

    def visit(identity: str) -> None:
        if identity in visited:
            return
        if identity in visiting:
            raise ArchitectureRefusal("CMD-CYCLE", identity)
        if identity not in packs:
            raise ArchitectureRefusal("CMD-OPTION-UNKNOWN", identity)
        visiting.add(identity)
        for requirement in sorted(packs[identity].requires):
            providers = sorted(p.identity for p in packs.values() if requirement in p.provides)
            if not providers:
                raise ArchitectureRefusal("CMD-CAPABILITY-MISSING", requirement)
            if len(providers) > 1:
                raise ArchitectureRefusal("CMD-CAPABILITY-AMBIGUOUS", requirement)
            visit(providers[0])
        visiting.remove(identity)
        visited.add(identity)
        ordered.append(identity)

    for root in sorted(roots):
        visit(root)
    return tuple(ordered)


def resolve_bblock(block: BuildingBlock, packs: Mapping[str, AtomicPack]) -> dict[str, Any]:
    closure = dependency_closure(packs, block.member_packs)
    capabilities = sorted({capability for identity in closure for capability in packs[identity].provides})
    missing = sorted(set(block.required_capabilities) - set(capabilities))
    if missing:
        raise ArchitectureRefusal("CMD-CAPABILITY-MISSING", ",".join(missing))
    return {
        "bblock": block.identity,
        "version": block.version,
        "closure": closure,
        "capabilities": capabilities,
        "resolution_digest": blake3_hex(canonical_json((block.identity, closure, capabilities)).encode()),
    }


def make_plan(
    candidate: Candidate,
    policy_digest: str,
    artifacts: Sequence[Any],
    external_intents: Sequence[Intent] = (),
) -> Plan:
    if candidate.state not in {CandidateState.CONSTRUCTED, CandidateState.VERIFIED, CandidateState.AUTHORIZED}:
        raise ArchitectureRefusal("AUTH-CANDIDATE-NOT-VERIFIED", candidate.state.value)
    plan_payload = {
        "candidate": candidate.candidate_id,
        "policy": policy_digest,
        "artifacts": [asdict(a) for a in artifacts],
        "external_intents": [asdict(i) for i in external_intents],
    }
    return Plan(
        plan_id=content_id("plan", plan_payload),
        observation_digest=candidate.source_observation_digest,
        policy_digest=policy_digest,
        candidate_id=candidate.candidate_id,
        artifacts=tuple(artifacts),
        external_intents=tuple(external_intents),
    )


def validate_external_intent(intent: Intent) -> None:
    if intent.required_broker != REQUIRED_BROKER:
        raise ArchitectureRefusal("AUTH-BROKER-MISMATCH", intent.required_broker)
    if not intent.required_authority:
        raise ArchitectureRefusal("AUTH-GRANT-MISSING")
    if not intent.expiry:
        raise ArchitectureRefusal("AUTH-GRANT-EXPIRED")
    if not intent.idempotency_key:
        raise ArchitectureRefusal("AUTH-SCOPE-MISMATCH", "missing idempotency key")
    if any(value < 0 for value in intent.resource_budget.values()):
        raise ArchitectureRefusal("CMD-RESOURCE-BOUND")


def deterministic(value: Any) -> str:
    return blake3_hex(canonical_json(value).encode())
