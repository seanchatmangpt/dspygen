from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "verify_modernization", ROOT / "scripts/verify_modernization.py"
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class VerifierTests(unittest.TestCase):
    def test_current_tree_is_alive(self):
        report = MODULE.verify(ROOT)
        self.assertEqual(report["status"], "ALIVE", report)
        self.assertTrue(all(report["checks"].values()), report)

    def test_nonruntime_python_roots_are_fenced(self):
        self.assertEqual(
            MODULE.EXCLUDED_PYTHON_ROOTS,
            ("src/dspygen/experiments/", "src/dspygen/wip/"),
        )
        self.assertFalse(
            MODULE._is_admitted_python(
                ROOT, ROOT / "src/dspygen/experiments/example.py"
            )
        )
        self.assertFalse(
            MODULE._is_admitted_python(ROOT, ROOT / "src/dspygen/wip/example.py")
        )
        self.assertTrue(
            MODULE._is_admitted_python(
                ROOT, ROOT / "src/dspygen/architecture/model.py"
            )
        )


if __name__ == "__main__":
    unittest.main()
