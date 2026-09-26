"""Authority-transition and operational-entry-point falsifiers."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from dspygen.architecture.cmd_entry import dispatch
from dspygen.architecture.cmd_kernel import make_plan
from dspygen.architecture.cmd_repository import pack_content_digest, verify_pack_lock
from dspygen.architecture.cmd_types import (
    ArchitectureRefusal,
    Artifact,
    Candidate,
    CandidateState,
    Ownership,
    Reversal,
)

ROOT = Path(__file__).resolve().parents[2]


class ProtocolAuthorityTests(unittest.TestCase):
    def test_pack_lock_replays_exact_sources(self):
        self.assertEqual(verify_pack_lock(ROOT), ())

    def test_pack_digest_detects_tamper(self):
        item = {"identity": "x", "version": "1", "content_digest": "0" * 64}
        self.assertNotEqual(pack_content_digest(item), item["content_digest"])

    def test_constructed_candidate_cannot_jump_to_plan(self):
        candidate = Candidate(
            "candidate:test",
            (("runtime", "native"),),
            "tree",
            "policy",
            "0" * 64,
            CandidateState.CONSTRUCTED,
        )
        artifact = Artifact(
            "plan.json",
            "{}\n",
            Ownership.EXCLUSIVE,
            "test",
            Reversal.REVERSIBLE,
        )
        with self.assertRaises(ArchitectureRefusal) as caught:
            make_plan(candidate, "policy", (artifact,))
        self.assertEqual(caught.exception.code, "AUTH-CANDIDATE-NOT-VERIFIED")


class E2EAuthorityTests(unittest.TestCase):
    def test_verified_plan_entry_point_is_non_mutating(self):
        payload = dispatch("plan", ROOT, domain="internal", index=0)
        self.assertEqual(payload["schema"], "cmd.plan.v1")
        self.assertFalse(payload["actuation_performed"])

    def test_materialization_without_exact_local_grant_is_refused(self):
        with self.assertRaises(ArchitectureRefusal) as caught:
            dispatch(
                "materialize",
                ROOT,
                domain="internal",
                index=0,
                grant="wrong-broker",
            )
        self.assertEqual(caught.exception.code, "AUTH-GRANT-MISSING")

    def test_authorized_materialization_is_receipted(self):
        with tempfile.TemporaryDirectory() as temp:
            payload = dispatch(
                "materialize",
                ROOT,
                domain="internal",
                index=0,
                grant="local-filesystem-broker",
                output_root=temp,
            )
            self.assertEqual(payload["schema"], "cmd.materialize-result.v1")
            self.assertEqual(payload["standing"], "ALIVE")
            self.assertTrue((Path(temp) / ".ggen/current.json").is_file())
            self.assertTrue(payload["receipt"]["receipt_id"].startswith("receipt:"))


if __name__ == "__main__":
    unittest.main()
