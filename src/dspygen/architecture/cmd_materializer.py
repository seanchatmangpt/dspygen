"""Transactional local materialization through an immutable payload and atomic manifest pointer."""
from __future__ import annotations

import json
import os
import shutil
from dataclasses import asdict
from pathlib import Path, PurePosixPath
from typing import Callable

from dspygen.architecture.cmd_types import (
    ArchitectureRefusal,
    Plan,
    Receipt,
    Standing,
    canonical_json,
    utc_now,
)
from dspygen.architecture.digest import blake3_hex


class InjectedFailure(RuntimeError):
    pass


def _canonical_relative(path: str) -> str:
    candidate = PurePosixPath(path)
    if candidate.is_absolute() or ".." in candidate.parts or path in {"", "."}:
        raise ArchitectureRefusal("OWN-PATH-ESCAPE", path)
    return candidate.as_posix()


def _digest_tree(paths: list[tuple[str, bytes]]) -> str:
    payload = [(path, blake3_hex(body)) for path, body in sorted(paths)]
    return blake3_hex(canonical_json(payload).encode())


def materialize(
    root: Path,
    plan: Plan,
    *,
    max_outputs: int = 128,
    max_bytes: int = 8 * 1024 * 1024,
    previous_receipt: str | None = None,
    validator: Callable[[Path], None] | None = None,
    fail_at: str | None = None,
) -> Receipt:
    """Publish a complete managed payload by atomically replacing one manifest pointer."""
    root = root.resolve()
    if len(plan.artifacts) > max_outputs:
        raise ArchitectureRefusal("CMD-RESOURCE-BOUND", f"outputs={len(plan.artifacts)}")
    prepared: list[tuple[str, bytes]] = []
    owners: dict[str, str] = {}
    for artifact in plan.artifacts:
        path = _canonical_relative(artifact.path)
        if path in owners and owners[path] != artifact.owner:
            raise ArchitectureRefusal("OWN-MULTIPLE-EXCLUSIVE", path)
        owners[path] = artifact.owner
        prepared.append((path, artifact.body.encode()))
    total_bytes = sum(len(body) for _, body in prepared)
    if total_bytes > max_bytes:
        raise ArchitectureRefusal("CMD-RESOURCE-BOUND", f"bytes={total_bytes}")

    ggen = root / ".ggen"
    transactions = ggen / "transactions"
    receipts = ggen / "receipts"
    transactions.mkdir(parents=True, exist_ok=True)
    receipts.mkdir(parents=True, exist_ok=True)
    transaction = transactions / plan.plan_id.replace(":", "-")
    if transaction.exists():
        shutil.rmtree(transaction)
    payload_root = transaction / "payload"
    payload_root.mkdir(parents=True)
    pre_state = (ggen / "current.json").read_bytes() if (ggen / "current.json").is_file() else b""
    pre_state_digest = blake3_hex(pre_state)
    intent_payload = {"plan": plan.to_dict(), "pre_state_digest": pre_state_digest}
    intent_digest = blake3_hex(canonical_json(intent_payload).encode())
    intent_receipt_path = receipts / f"{plan.plan_id.replace(':', '-')}.intent.json"
    intent_receipt_path.write_text(canonical_json({"schema": "cmd.intent-receipt.v1", **intent_payload}) + "\n")
    if fail_at == "after_intent_receipt":
        raise InjectedFailure(fail_at)

    for path, body in prepared:
        target = payload_root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(body)
    if fail_at == "after_stage":
        raise InjectedFailure(fail_at)
    if validator:
        validator(payload_root)
    if fail_at == "after_validation":
        raise InjectedFailure(fail_at)

    tree_digest = _digest_tree(prepared)
    artifacts = tuple((path, blake3_hex(body)) for path, body in sorted(prepared))
    result = Receipt(
        schema="cmd.receipt.v1",
        operation="filesystem.materialize",
        intent_digest=intent_digest,
        grant_digest=None,
        subject_revision=plan.observation_digest,
        pre_state_digest=pre_state_digest,
        plan_digest=blake3_hex(canonical_json(plan.to_dict()).encode()),
        artifacts=artifacts,
        post_state_digest=tree_digest,
        postcondition="payload-staged-and-verified",
        verifier_report_digest=tree_digest,
        previous_receipt=previous_receipt,
        standing_result=Standing.ALIVE,
        typed_refusals=(),
        issued_at=utc_now(),
    )
    result_path = receipts / f"{result.receipt_id.replace(':', '-')}.json"
    result_path.write_text(
        canonical_json(
            {
                **asdict(result),
                "standing_result": result.standing_result.value,
                "receipt_id": result.receipt_id,
            }
        )
        + "\n"
    )
    if fail_at == "after_result_receipt":
        raise InjectedFailure(fail_at)

    pointer = {
        "schema": "cmd.materialized-pointer.v1",
        "plan_id": plan.plan_id,
        "payload": str(payload_root.relative_to(root)),
        "receipt": str(result_path.relative_to(root)),
        "tree_digest": tree_digest,
    }
    pointer_tmp = ggen / ".current.json.tmp"
    pointer_tmp.write_text(canonical_json(pointer) + "\n")
    if fail_at == "before_publish":
        pointer_tmp.unlink(missing_ok=True)
        raise InjectedFailure(fail_at)
    os.replace(pointer_tmp, ggen / "current.json")
    return result


def replay_materialization(root: Path, receipt_path: Path) -> tuple[bool, str]:
    receipt = json.loads(receipt_path.read_text())
    pointer_path = root / ".ggen/current.json"
    if not pointer_path.is_file():
        return False, "RPL-ARTIFACT-DIVERGENCE"
    pointer = json.loads(pointer_path.read_text())
    payload_root = root / pointer["payload"]
    observed: list[tuple[str, bytes]] = []
    for path, digest in receipt["artifacts"]:
        target = payload_root / path
        if not target.is_file() or blake3_hex(target.read_bytes()) != digest:
            return False, f"RCP-ARTIFACT-TAMPER:{path}"
        observed.append((path, target.read_bytes()))
    if _digest_tree(observed) != receipt["post_state_digest"]:
        return False, "RPL-ARTIFACT-DIVERGENCE"
    return True, receipt["receipt_id"]


def rollback_pointer(root: Path, prior_pointer: dict[str, str]) -> str:
    """Atomically restore a previously receipted materialization pointer."""
    root = root.resolve()
    payload = root / prior_pointer["payload"]
    receipt = root / prior_pointer["receipt"]
    if not payload.is_dir() or not receipt.is_file():
        raise ArchitectureRefusal("RPL-SOURCE-DIVERGENCE", "prior transaction unavailable")
    pointer_tmp = root / ".ggen/.current.rollback.tmp"
    pointer_tmp.write_text(canonical_json(prior_pointer) + "\n")
    os.replace(pointer_tmp, root / ".ggen/current.json")
    return blake3_hex((root / ".ggen/current.json").read_bytes())
