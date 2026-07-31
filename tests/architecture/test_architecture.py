from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from dspygen.architecture.digest import blake3_hex
from dspygen.architecture.model import (
    ArchitectureRefusal,
    BrokerIntent,
    EvidenceSet,
    LifecycleState,
    Standing,
)
from dspygen.architecture.verification import repository_root, verify


class DigestTests(unittest.TestCase):
    def test_blake3_official_vectors(self) -> None:
        self.assertEqual(
            blake3_hex(b""),
            "af1349b9f5f9a1a6a0404dea36dcc9499bcb25c9adc112b7cc9a93cae41f3262",
        )
        self.assertEqual(
            blake3_hex(b"abc"),
            "6437b3ac38465133ffb63b75273a8db548c558465d79db03fd359c6cd5bd9d85",
        )


class ArchitectureLawTests(unittest.TestCase):
    def test_lifecycle_and_standing_are_orthogonal(self) -> None:
        self.assertNotIn("RETIRED", Standing.__members__)
        self.assertTrue(LifecycleState.DEPRECATED.allows(LifecycleState.RETIRED))
        self.assertFalse(LifecycleState.ARCHIVED.allows(LifecycleState.ACTIVE))

    def test_alive_requires_all_five_evidence_surfaces(self) -> None:
        partial = EvidenceSet(witness=True, falsifier=True, independent_verifier=True)
        self.assertEqual(partial.standing(), Standing.PARTIAL_ALIVE)
        with self.assertRaisesRegex(ArchitectureRefusal, "ALIVE_REFUSED"):
            partial.require_alive()
        complete = EvidenceSet(True, True, True, True, True)
        self.assertEqual(complete.standing(), Standing.ALIVE)
        complete.require_alive()

    def test_non_brce_intent_is_refused(self) -> None:
        intent = BrokerIntent(
            intent_id="test",
            action="evaluate",
            payload_digest="0" * 64,
            authority=(),
            resource_ceiling={},
            broker="direct",
        )
        with self.assertRaisesRegex(ArchitectureRefusal, "DIRECT_ACTUATION_REFUSED"):
            intent.validate()

    def test_brce_intent_is_canonical(self) -> None:
        intent = BrokerIntent(
            intent_id="eval-001",
            action="evaluate",
            payload_digest="a" * 64,
            authority=("dataset:read",),
            resource_ceiling={"max_tokens": 1000, "max_seconds": 30},
        )
        self.assertEqual(intent.to_dict()["broker"], "BRCE")


class RepositoryVerifierTests(unittest.TestCase):
    def test_exact_tree_replays_to_alive(self) -> None:
        report = verify(repository_root())
        self.assertTrue(report.ok, json.dumps(report.to_dict(), indent=2))
        self.assertEqual(report.standing, Standing.ALIVE)

    def test_projection_drift_is_refused(self) -> None:
        root = repository_root()
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory)
            for relative in (
                ".specify/dspygen-architecture.ttl",
                "src/dspygen/architecture/catalog.py",
                "src/dspygen/architecture/model.py",
                "docs/architecture/CATALOG.md",
                "receipts/dspygen-architecture-v1.json",
            ):
                target = copy / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(root / relative, target)
            catalog = copy / "src/dspygen/architecture/catalog.py"
            catalog.write_text(catalog.read_text() + "# drift\n")
            report = verify(copy)
            self.assertEqual(report.standing, Standing.BUILD_BROKEN)
            self.assertTrue(any("ARTIFACT_DRIFT_REFUSED" in failure for failure in report.failures))


if __name__ == "__main__":
    unittest.main()
