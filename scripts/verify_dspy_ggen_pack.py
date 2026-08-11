#!/usr/bin/env python3
"""Independent verifier for DSPyGen's pinned dspy-pack consumer."""

from __future__ import annotations

import argparse
import hashlib
import json
import tomllib
from pathlib import Path

PACK_REPO = "https://github.com/seanchatmangpt/ggen-marketplace.git"
PACK_COMMIT = "465e9462747e489be842c7107fdf537735de5d65"
PACK_SUBDIR = "packs/dspy-pack"
PACK_VERSION = "0.2.0"
EXPECTED_MODULE = "powl_planner"
EXPECTED_SIGNATURE = "PowlPlanner"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def refuse(code: str, detail: str) -> None:
    raise SystemExit(f"REFUSED:{code}:{detail}")


def verify_project(project: Path, rendered: Path | None) -> dict[str, object]:
    manifest_path = project / "ggen.toml"
    ontology_path = project / "ontology.ttl"
    if not manifest_path.is_file():
        refuse("DSPY_PACK_MANIFEST_MISSING", str(manifest_path))
    if not ontology_path.is_file():
        refuse("DSPY_PACK_ONTOLOGY_MISSING", str(ontology_path))

    manifest = tomllib.loads(manifest_path.read_text(encoding="utf-8"))
    pack = manifest.get("packs", {}).get("dspy-pack")
    if not isinstance(pack, dict):
        refuse("DSPY_PACK_REFERENCE_MISSING", "packs.dspy-pack")
    expected = {"git": PACK_REPO, "version": PACK_COMMIT, "subdir": PACK_SUBDIR}
    observed = {key: pack.get(key) for key in expected}
    if observed != expected:
        refuse("DSPY_PACK_IDENTITY_DRIFT", f"observed={observed!r}")

    ontology = ontology_path.read_text(encoding="utf-8")
    required = (
        "dspy:powl-planner-signature a dspy:Signature",
        'dspy:className "PowlPlanner"',
        'dspy:name "powl_planner"',
        'dspy:kind "ChainOfThought"',
        'dspy:name "candidate_powl"',
    )
    missing = [needle for needle in required if needle not in ontology]
    if missing:
        refuse("DSPY_PACK_CONSUMER_GRAPH_INCOMPLETE", ",".join(missing))
    forbidden = ('dspy:kind "ReAct"', "dspy:usesMCPServer")
    present = [needle for needle in forbidden if needle in ontology]
    if present:
        refuse("DSPY_PACK_UNBROKERED_REACT", ",".join(present))

    receipt: dict[str, object] = {
        "schema": "dspygen.dspy-pack-receipt.v1",
        "standing": "PARTIAL_ALIVE" if rendered is None else "ALIVE",
        "pack": {
            "repository": PACK_REPO,
            "commit": PACK_COMMIT,
            "subdir": PACK_SUBDIR,
            "version": PACK_VERSION,
        },
        "inputs": {
            "ggen.toml.sha256": digest(manifest_path),
            "ontology.ttl.sha256": digest(ontology_path),
        },
        "authority": {
            "generated_output_is_projection": True,
            "react_admitted": False,
            "do_path": "BRCE",
        },
    }

    if rendered is not None:
        rendered = rendered.resolve()
        if not rendered.is_file():
            refuse("DSPY_PACK_RENDER_MISSING", str(rendered))
        code = rendered.read_text(encoding="utf-8")
        required_code = (
            f"class {EXPECTED_SIGNATURE}(dspy.Signature):",
            f"{EXPECTED_MODULE} = dspy.ChainOfThought({EXPECTED_SIGNATURE})",
        )
        missing_code = [needle for needle in required_code if needle not in code]
        if missing_code:
            refuse("DSPY_PACK_RENDER_MISMATCH", ",".join(missing_code))

        # The pack itself contains a worked ReAct example, so a complete pack
        # render may include ReAct code. DSPyGen's authority is its consumer
        # ontology above, which deliberately contains no ReAct declaration.
        compile(code, str(rendered), "exec")

        pack_cache = project / ".ggen-v2" / "git-packs" / "dspy-pack"
        pack_manifest = pack_cache / PACK_SUBDIR / "pack.toml"
        pin = pack_cache / ".ggen-git-pin"
        if not pack_manifest.is_file():
            refuse("DSPY_PACK_CACHE_MANIFEST_MISSING", str(pack_manifest))
        pack_meta = tomllib.loads(pack_manifest.read_text(encoding="utf-8"))
        observed_version = pack_meta.get("pack", {}).get("version")
        if observed_version != PACK_VERSION:
            refuse("DSPY_PACK_VERSION_DRIFT", f"observed={observed_version!r}")
        if not pin.is_file():
            refuse("DSPY_PACK_GIT_PIN_MISSING", str(pin))
        observed_pin = pin.read_text(encoding="utf-8").strip()
        if observed_pin != PACK_COMMIT:
            refuse("DSPY_PACK_GIT_PIN_DRIFT", observed_pin)

        receipt["rendered"] = {
            "path": str(rendered),
            "sha256": digest(rendered),
            "syntax": "valid",
        }

    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, default=Path(".specify/dspy-pack"))
    parser.add_argument("--rendered", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    receipt = verify_project(args.project.resolve(), args.rendered)
    payload = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
