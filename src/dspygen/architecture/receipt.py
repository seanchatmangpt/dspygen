"""Canonical receipt construction and replay verification."""
from __future__ import annotations

import json
from typing import Mapping

from dspygen.architecture.digest import blake3_hex

RECEIPT_SCHEMA = "dspygen.architecture.receipt.v1"


def canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def output_digests(outputs: Mapping[str, bytes]) -> dict[str, str]:
    return {path: blake3_hex(outputs[path]) for path in sorted(outputs)}


def composition_payload(source: bytes, outputs: Mapping[str, bytes]) -> dict[str, object]:
    return {
        "schema": RECEIPT_SCHEMA,
        "source": {
            "path": ".specify/dspygen-architecture.ttl",
            "blake3": blake3_hex(source),
        },
        "outputs": output_digests(outputs),
        "required_broker": "BRCE",
        "required_evidence": [
            "witness",
            "falsifier",
            "independent_verifier",
            "receipt_verifier",
            "replay",
        ],
    }


def receipt_root(source: bytes, outputs: Mapping[str, bytes]) -> str:
    return blake3_hex(canonical_json(composition_payload(source, outputs)))


def verify_receipt(receipt: Mapping[str, object], source: bytes, outputs: Mapping[str, bytes]) -> tuple[bool, str]:
    expected_payload = composition_payload(source, outputs)
    if receipt.get("schema") != RECEIPT_SCHEMA:
        return False, "RECEIPT_SCHEMA_MISMATCH"
    if receipt.get("composition") != expected_payload:
        return False, "RECEIPT_COMPOSITION_MISMATCH"
    expected_root = blake3_hex(canonical_json(expected_payload))
    if receipt.get("receipt_root") != expected_root:
        return False, "RECEIPT_ROOT_MISMATCH"
    return True, expected_root
