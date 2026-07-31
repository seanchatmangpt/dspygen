"""Repository adapters for loading CMD ontology projections and policies."""
from __future__ import annotations

import json
import tomllib
from pathlib import Path
from typing import Any

from dspygen.architecture.cmd_types import AtomicPack, BuildingBlock, Constraint, Dimension
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
