from __future__ import annotations

import ast
import sys
import types
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODE_ACTION = ROOT / "src/dspygen/lsp/providers/code_action.py"


class LSPModernizationTests(unittest.TestCase):
    def test_forward_quick_fix_is_executable_not_a_stub(self):
        source = CODE_ACTION.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(CODE_ACTION))
        implementation = None
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "_action_add_forward_stub":
                for child in ast.walk(node):
                    if (
                        isinstance(child, ast.Constant)
                        and isinstance(child.value, str)
                        and "def forward(self, **inputs)" in child.value
                    ):
                        implementation = child.value
                        break
        self.assertIsNotNone(implementation)
        assert implementation is not None
        self.assertNotIn("NotImplementedError", implementation)
        self.assertIn("dspy.Prediction(**inputs)", implementation)

        fake_dspy = types.ModuleType("dspy")

        class Module:
            pass

        class Prediction(dict):
            def __init__(self, **values):
                super().__init__(values)

        fake_dspy.Module = Module
        fake_dspy.Prediction = Prediction
        namespace = {"dspy": fake_dspy}
        generated = "class Example(dspy.Module):\n" + implementation.lstrip("\n")
        compile(generated, "lsp_generated_forward.py", "exec")
        exec(generated, namespace)
        result = namespace["Example"]().forward(value="admitted")
        self.assertEqual(result, {"value": "admitted"})


if __name__ == "__main__":
    unittest.main()
