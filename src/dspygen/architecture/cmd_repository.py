"""Repository adapters for loading CMD ontology projections and policies."""
from __future__ import annotations

import json
import tomllib
from pathlib import Path
from typing import Any

from dspygen.architecture.cmd_types import (
    AtomicPack,
    BuildingBlock,
    Constraint,
    Dimension,
    canonical_json,
)
from dspygen.architecture.digest import blake3_hex


def load_cmd_config(root: Path) -> dict[str, Any]:
    return tomllib.loads((root / ".specify/cmd/architecture.toml").read_text())


def load_dimensions(root: Path, domain: str) -> tuple[Dimension, ...]:
    config = load_cmd_config(root)
    return tuple(
        Dimension(
            dimension_id=item["id"],
            title=item.get("title", item["id"]),
            owner=item["owner"],
            options=tuple(item["options"]),
            risk_class=item.get("risk_class", "normal"),
            coverage_mode=item.get("coverage_mode", "exhaustive"),
        )
        for item in config[domain]["dimensions"]
    )


def load_constraints(root: Path, domain: str) -> tuple[Constraint, ...]:
    config = load_cmd_config(root)
    result = []
    for item in config[domain].get("constraints", []):
        result.append(
            Constraint(
                constraint_id=item["id"],
                when=dict(item.get("when", {})),
                require={k: tuple(v) for k, v in item.get("require", {}).items()},
                exclude={k: tuple(v) for k, v in item.get("exclude", {}).items()},
                refusal_code=item.get("refusal_code", "CMD-CONSTRAINT-VIOLATION"),
            )
        )
    return tuple(result)


def policy_digest(root: Path) -> str:
    files = [
        root / ".specify/cmd/architecture.toml",
        root / ".specify/cmd/authority.toml",
        root / ".specify/cmd/repository.ttl",
        root / ".specify/cmd/shapes/cmd-shapes.ttl",
    ]
    return blake3_hex(b"".join(path.read_bytes() for path in files))


def pack_content_digest(item: dict[str, Any]) -> str:
    payload = {key: value for key, value in item.items() if key != "content_digest"}
    return blake3_hex(canonical_json(payload).encode())


def verify_pack_lock(root: Path) -> tuple[str, ...]:
    failures: list[str] = []
    lock_path = root / ".ggen/packs.lock"
    if not lock_path.is_file():
        return ("RCP-MISSING:packs.lock",)
    lock = json.loads(lock_path.read_text())
    raw_items: dict[str, dict[str, Any]] = {}
    for path in sorted((root / "packs").glob("cmd-*.json")):
        document = json.loads(path.read_text())
        for item in document.get("packs", [document]):
            raw_items[item["identity"]] = item
            if item.get("content_digest") != pack_content_digest(item):
                failures.append(f"RCP-ARTIFACT-TAMPER:{item['identity']}")
    expected_digests = {
        identity: item["content_digest"] for identity, item in sorted(raw_items.items())
    }
    if lock.get("content_digests") != expected_digests:
        failures.append("RPL-ARTIFACT-DIVERGENCE:pack-digests")
    ontology = root / ".specify/cmd/repository.ttl"
    if not ontology.is_file() or lock.get("ontology_digest") != blake3_hex(ontology.read_bytes()):
        failures.append("RPL-SOURCE-DIVERGENCE:ontology")
    if lock.get("policy_digest") != policy_digest(root):
        failures.append("RPL-POLICY-DIVERGENCE")
    packs = load_packs(root)
    blocks = load_bblocks(root)
    if blocks:
        from dspygen.architecture.cmd_kernel import resolve_bblock

        closure = list(resolve_bblock(blocks[0], packs)["closure"])
        if lock.get("resolved_atomic_pack_closure") != closure:
            failures.append("RPL-ARTIFACT-DIVERGENCE:pack-closure")
        expected_root = f"{blocks[0].identity}@{blocks[0].version}"
        if lock.get("root_requests") != [expected_root]:
            failures.append("RPL-SOURCE-DIVERGENCE:root-request")
    return tuple(sorted(failures))


def load_packs(root: Path) -> dict[str, AtomicPack]:
    result: dict[str, AtomicPack] = {}
    for path in sorted((root / "packs").glob("cmd-*.json")):
        document = json.loads(path.read_text())
        items = document.get("packs", [document]) if isinstance(document, dict) else document
        for item in items:
            pack = AtomicPack(
                identity=item["identity"],
                version=item["version"],
                pack_class=item["pack_class"],
                provides=tuple(item["provides"]),
                requires=tuple(item.get("requires", [])),
                owner=item["owner"],
                ownership_claims=tuple(item.get("ownership_claims", [])),
                verifier=item["verifier"],
                trust_floor=item["trust_floor"],
                content_digest=item["content_digest"],
            )
            result[pack.identity] = pack
    return result


def load_bblocks(root: Path) -> tuple[BuildingBlock, ...]:
    result = []
    for path in sorted((root / "bblocks").glob("cmd-*.json")):
        item = json.loads(path.read_text())
        result.append(
            BuildingBlock(
                identity=item["identity"],
                version=item["version"],
                purpose=item["purpose"],
                owner=item["owner"],
                member_packs=tuple(item["member_packs"]),
                dependent_bblocks=tuple(item.get("dependent_bblocks", [])),
                required_capabilities=tuple(item["required_capabilities"]),
                exclusive_capabilities=tuple(item.get("exclusive_capabilities", [])),
                policy_profile=item["policy_profile"],
                verifier_profile=item["verifier_profile"],
                migration_law=item["migration_law"],
                removal_law=item["removal_law"],
                downstream_intents=tuple(item.get("downstream_intents", [])),
                exclusions=tuple(item.get("exclusions", [])),
            )
        )
    return tuple(result)
