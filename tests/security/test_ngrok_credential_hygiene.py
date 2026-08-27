from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "verify_ngrok_credentials.py"
SPEC = importlib.util.spec_from_file_location("verify_ngrok_credentials", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class NgrokCredentialHygieneTests(unittest.TestCase):
    def _inspect(self, content: str):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "ngrok.yml"
            path.write_text(content, encoding="utf-8")
            return MODULE.inspect(path)

    def test_repository_ngrok_config_contains_no_embedded_authtoken(self):
        findings = MODULE.inspect(ROOT / "ngrok.yml")
        self.assertEqual(findings, ())

    def test_concrete_authtoken_is_refused_without_echoing_value(self):
        marker = "credential-material-that-must-not-be-reported"
        findings = self._inspect(f"version: 2\nauthtoken: {marker}\n")
        self.assertEqual(len(findings), 1)
        finding = findings[0]
        self.assertEqual(finding.reason, "NGROK_AUTHTOKEN_EMBEDDED")
        self.assertNotIn(marker, repr(finding))

    def test_environment_reference_is_inert(self):
        findings = self._inspect("version: 2\nauthtoken: ${NGROK_AUTHTOKEN}\n")
        self.assertEqual(findings, ())

    def test_commented_example_is_not_a_credential(self):
        findings = self._inspect("# authtoken: supplied through NGROK_AUTHTOKEN\n")
        self.assertEqual(findings, ())


if __name__ == "__main__":
    unittest.main()
