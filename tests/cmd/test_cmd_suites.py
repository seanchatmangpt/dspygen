"""Distinct executable CMD verifier suites."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from dspygen.architecture.cmd_broker import execute
from dspygen.architecture.cmd_kernel import enumerate_candidates
from dspygen.architecture.cmd_materializer import InjectedFailure, materialize, replay_materialization
from dspygen.architecture.cmd_observer import observe
from dspygen.architecture.cmd_types import (
    ArchitectureRefusal,
    Artifact,
    Candidate,
    CandidateState,
    Consent,
    Dimension,
    EvidenceSet,
    Grant,
    Intent,
    Lifecycle,
    Ownership,
    Plan,
    Reversal,
    Standing,
    content_id,
)
from dspygen.architecture.cmd_verifier import verify_crown

ROOT = Path(__file__).resolve().parents[2]


class BenchmarkTests(unittest.TestCase):
    def test_1024_candidates_under_budget(self):
        dimensions = tuple(Dimension(f"d{i}", f"d{i}", "owner", ("0", "1")) for i in range(10))
        start = time.perf_counter()
        values = enumerate_candidates(dimensions, (), "observation", "policy")
        elapsed = time.perf_counter() - start
        self.assertEqual(len(values), 1024)
        self.assertLess(elapsed, 5.0)


class ChaosTests(unittest.TestCase):
    def test_every_boundary_keeps_pointer_unpublished(self):
        candidate = Candidate(
            "candidate:test",
            (("runtime", "native"),),
            "tree",
            "policy",
            "0" * 64,
            CandidateState.VERIFIED,
        )
        plan = Plan(
            "plan:test",
            "tree",
            "policy",
            candidate.candidate_id,
            (Artifact("a", "x", Ownership.EXCLUSIVE, "owner", Reversal.REVERSIBLE),),
            (),
        )
        for boundary in (
            "after_intent_receipt",
            "after_stage",
            "after_validation",
            "after_result_receipt",
            "before_publish",
        ):
            with self.subTest(boundary=boundary), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                with self.assertRaises(InjectedFailure):
                    materialize(root, plan, fail_at=boundary)
                self.assertFalse((root / ".ggen/current.json").exists())


class E2ETests(unittest.TestCase):
    def run_cmd(self, *args):
        env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "dspygen.architecture.cmd_entry",
                "--root",
                str(ROOT),
                *args,
            ],
            env=env,
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(result.stdout)

    def test_observe_black_box(self):
        payload = self.run_cmd("observe")
        self.assertEqual(payload["schema"], "cmd.observation.v1")

    def test_candidate_and_crown_black_box(self):
        coverage = self.run_cmd("candidates-coverage", "--domain", "external")
        self.assertTrue(coverage["covered"])
        head = subprocess.check_output(
            ["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True
        ).strip()
        crown = self.run_cmd(
            "crown",
            "--exact-head-sha",
            head,
            "--detached-replay",
        )
        self.assertEqual(crown["aggregate_standing"], "ALIVE")


class IntegrationTests(unittest.TestCase):
    def test_exact_git_observer(self):
        observation = observe(ROOT)
        self.assertEqual(len(observation.revision), 40)
        self.assertGreater(len(observation.entries), 20)
        self.assertFalse(observation.unresolved)

    def test_transaction_and_replay(self):
        candidate = Candidate(
            "candidate:x",
            (("runtime", "native"),),
            "tree",
            "policy",
            "0" * 64,
            CandidateState.VERIFIED,
        )
        artifact = Artifact(
            "out/a.txt",
            "hello\n",
            Ownership.EXCLUSIVE,
            "test",
            Reversal.REVERSIBLE_WITH_SNAPSHOT,
        )
        plan = Plan("plan:x", "tree", "policy", candidate.candidate_id, (artifact,), ())
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            receipt = materialize(root, plan)
            receipt_path = next((root / ".ggen/receipts").glob("receipt-*.json"))
            ok, result = replay_materialization(root, receipt_path)
            self.assertTrue(ok, result)
            self.assertEqual(result, receipt.receipt_id)


class PropertyTests(unittest.TestCase):
    def test_dimension_order_does_not_change_candidate_signatures(self):
        dimensions = (
            Dimension("a", "a", "owner", ("1", "2")),
            Dimension("b", "b", "owner", ("x", "y")),
        )
        first = {c.signature for c in enumerate_candidates(dimensions, (), "o", "p")}
        second = {
            c.signature for c in enumerate_candidates(tuple(reversed(dimensions)), (), "o", "p")
        }
        self.assertEqual(first, second)

    def test_bounded_products_have_unique_signatures(self):
        for width in range(1, 7):
            dimensions = tuple(
                Dimension(f"d{i}", f"d{i}", "owner", ("0", "1")) for i in range(width)
            )
            values = enumerate_candidates(dimensions, (), "o", "p")
            self.assertEqual(len(values), 2**width)
            self.assertEqual(len(values), len({value.signature for value in values}))


class ProtocolTests(unittest.TestCase):
    def test_identity_is_content_addressed(self):
        self.assertEqual(
            content_id("x", {"b": 2, "a": 1}),
            content_id("x", {"a": 1, "b": 2}),
        )

    def test_lifecycle_and_standing_are_orthogonal(self):
        self.assertNotIn(Standing.ALIVE.value, {state.value for state in Lifecycle})
        self.assertEqual(EvidenceSet(True, True, True, True, True).standing(), Standing.ALIVE)

    def test_empty_dimension_is_typed_refusal(self):
        with self.assertRaises(ArchitectureRefusal) as caught:
            enumerate_candidates((Dimension("x", "x", "owner", ()),), (), "o", "p")
        self.assertEqual(caught.exception.code, "CMD-DIMENSION-MISSING")


class ReplayTests(unittest.TestCase):
    def test_tamper_is_refused(self):
        candidate = Candidate(
            "candidate:test",
            (("runtime", "native"),),
            "tree",
            "policy",
            "0" * 64,
            CandidateState.VERIFIED,
        )
        plan = Plan(
            "plan:test",
            "tree",
            "policy",
            candidate.candidate_id,
            (Artifact("a.txt", "x", Ownership.EXCLUSIVE, "owner", Reversal.REVERSIBLE),),
            (),
        )
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            materialize(root, plan)
            receipt = next((root / ".ggen/receipts").glob("receipt-*.json"))
            pointer = json.loads((root / ".ggen/current.json").read_text())
            (root / pointer["payload"] / "a.txt").write_text("tampered")
            ok, reason = replay_materialization(root, receipt)
            self.assertFalse(ok)
            self.assertTrue(reason.startswith("RCP-ARTIFACT-TAMPER"))


class SecurityTests(unittest.TestCase):
    @staticmethod
    def future() -> str:
        return (datetime.now(timezone.utc) + timedelta(minutes=5)).isoformat()

    def test_path_traversal_refused(self):
        candidate = Candidate(
            "candidate:test",
            (("runtime", "native"),),
            "tree",
            "policy",
            "0" * 64,
            CandidateState.VERIFIED,
        )
        plan = Plan(
            "plan:test",
            "tree",
            "policy",
            candidate.candidate_id,
            (Artifact("../escape", "x", Ownership.EXCLUSIVE, "owner", Reversal.REVERSIBLE),),
            (),
        )
        with tempfile.TemporaryDirectory() as temp, self.assertRaises(ArchitectureRefusal) as caught:
            materialize(Path(temp), plan)
        self.assertEqual(caught.exception.code, "OWN-PATH-ESCAPE")

    def test_consent_scope_refused(self):
        intent = Intent(
            "intent:test",
            "candidate:test",
            "external.echo",
            {},
            "tree",
            {},
            ("external.echo",),
            {"max_calls": 1},
            self.future(),
            "idem",
        )
        grant = Grant(
            "grant:test",
            intent.intent_id,
            "approver",
            "p" * 64,
            ("external.echo",),
            ("resource",),
            {"max_calls": 1},
            self.future(),
            "tree",
        )
        consent = Consent(
            "subject",
            "wrong",
            ("resource",),
            "purpose",
            "subject",
            datetime.now(timezone.utc).isoformat(),
            self.future(),
            "active",
            "e" * 64,
        )
        with self.assertRaises(ArchitectureRefusal) as caught:
            execute(
                intent,
                grant,
                consent,
                adapter=lambda value: {},
                observe_postcondition=lambda value, result: True,
                idempotency_ledger={},
            )
        self.assertEqual(caught.exception.code, "EXT-CONSENT-SCOPE")


class StressTests(unittest.TestCase):
    def test_4096_candidate_lattice(self):
        dimensions = tuple(
            Dimension(f"d{i}", f"d{i}", "owner", ("0", "1")) for i in range(12)
        )
        candidates = enumerate_candidates(dimensions, (), "o", "p", max_candidates=4096)
        self.assertEqual(len(candidates), 4096)

    def test_over_budget_refused(self):
        dimensions = tuple(
            Dimension(f"d{i}", f"d{i}", "owner", ("0", "1")) for i in range(13)
        )
        with self.assertRaises(ArchitectureRefusal) as caught:
            enumerate_candidates(dimensions, (), "o", "p", max_candidates=4096)
        self.assertEqual(caught.exception.code, "CMD-RESOURCE-BOUND")


class VerifierReportTests(unittest.TestCase):
    def test_all_gall_checkpoints_close(self):
        head = subprocess.check_output(
            ["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True
        ).strip()
        report = verify_crown(ROOT, exact_head_sha=head, detached_replay=True)
        self.assertEqual(
            [checkpoint.checkpoint for checkpoint in report.checkpoints],
            [f"G{i}" for i in range(10)],
        )
        self.assertEqual(report.aggregate_standing, Standing.ALIVE, report.to_dict())
        self.assertEqual(report.external_standing, Standing.UNKNOWN)


if __name__ == "__main__":
    unittest.main()
