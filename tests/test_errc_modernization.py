from __future__ import annotations

import json
import sys
import types
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


class PipelineTests(unittest.TestCase):
    def test_single_input_composition_executes(self):
        from dspygen.modules.pipeline import pipe_modules

        class Source:
            def __init__(self):
                self.forward_args = {"text": "hello"}
                self.output = None

            def forward(self, text):
                return text.upper()

        class Target:
            def __init__(self):
                self.forward_args = {}
                self.output = None

            def forward(self, text):
                return f"[{text}]"

        result = pipe_modules(Source(), Target())
        self.assertEqual(result.output, "[HELLO]")

    def test_ambiguous_binding_is_refused(self):
        from dspygen.modules.pipeline import PipelineRefusal, pipe_forward

        class Target:
            forward_args = {}

            def forward(self, left, right):
                return left + right

        with self.assertRaisesRegex(PipelineRefusal, "PIPE_INPUT_AMBIGUOUS"):
            pipe_forward(Target(), "value")

    def test_legacy_placeholder_is_repaired_but_custom_pipe_is_preserved(self):
        fake_dspy = types.ModuleType("dspy")

        class Module:
            pass

        fake_dspy.Module = Module
        previous = sys.modules.get("dspy")
        sys.modules["dspy"] = fake_dspy
        try:
            from dspygen.modules.pipeline import install_legacy_pipeline_compat

            install_legacy_pipeline_compat(Module)

            class Legacy(Module):
                __module__ = "dspygen.modules.legacy_fixture"

                def __init__(self):
                    self.forward_args = {}
                    self.output = None

                def forward(self, text):
                    return text.upper()

                def pipe(self, input_str):
                    raise NotImplementedError(
                        "Please implement the pipe method for DSL support."
                    )

            class Custom(Module):
                __module__ = "dspygen.modules.custom_fixture"

                def pipe(self, value):
                    return f"custom:{value}"

            self.assertEqual(Legacy().pipe("admitted"), "ADMITTED")
            self.assertTrue(Legacy.__dspygen_legacy_pipe_repaired__)
            self.assertEqual(Custom().pipe("x"), "custom:x")
        finally:
            if previous is None:
                sys.modules.pop("dspy", None)
            else:
                sys.modules["dspy"] = previous


class GeneratorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if "dspy" not in sys.modules:
            fake_dspy = types.ModuleType("dspy")

            class Module:
                pass

            fake_dspy.Module = Module
            sys.modules["dspy"] = fake_dspy

    def test_generation_is_complete_deterministic_and_compilable(self):
        from dspygen.modules.gen_dspy_module import (
            DSPyModuleTemplate,
            render_dspy_module,
        )

        model = DSPyModuleTemplate(
            class_name="TextSummary", inputs=["text"], output="summary"
        )
        first = render_dspy_module(model)
        second = render_dspy_module(model)
        self.assertEqual(first, second)
        self.assertNotIn("NotImplementedError", first)
        self.assertIn("pipe_forward", first)
        compile(first, "generated_text_summary.py", "exec")

    def test_generation_refuses_invalid_identifiers(self):
        from pydantic import ValidationError
        from dspygen.modules.gen_dspy_module import DSPyModuleTemplate

        with self.assertRaises(ValidationError):
            DSPyModuleTemplate(
                class_name="Bad Name", inputs=["valid", "not-valid"], output="result"
            )


class ProjectTests(unittest.TestCase):
    def test_project_materialization_is_offline_and_receipted(self):
        from dspygen.project import materialize_project, plan_project

        with TemporaryDirectory() as tmp:
            plan = plan_project("My-Agent Project", output_dir=tmp)
            receipt = materialize_project(plan)
            self.assertEqual(receipt.status, "ALIVE")
            self.assertEqual(plan.package_name, "my_agent_project")
            self.assertEqual(set(receipt.file_hashes), set(plan.files))
            self.assertTrue(
                (Path(plan.output_dir) / "src/my_agent_project/__init__.py").is_file()
            )
            json.loads(receipt.to_json())

    def test_existing_project_is_refused(self):
        from dspygen.project import ProjectRefusal, materialize_project, plan_project

        with TemporaryDirectory() as tmp:
            plan = plan_project("existing", output_dir=tmp)
            materialize_project(plan)
            with self.assertRaisesRegex(ProjectRefusal, "PROJECT_EXISTS"):
                materialize_project(plan)


class PipelineDefinitionTests(unittest.TestCase):
    def test_explicit_module_pipeline_executes(self):
        from dspygen.modules.dspygen_dsl_pipeline import execute_pipeline_definition

        fixture = types.ModuleType("dspygen.modules.test_fixtures")

        class First:
            def __init__(self, text):
                self.forward_args = {"text": text}
                self.output = None

            def forward(self, text):
                return text.upper()

        class Second:
            def __init__(self):
                self.forward_args = {}
                self.output = None

            def forward(self, text):
                return f"<{text}>"

        fixture.First = First
        fixture.Second = Second
        sys.modules[fixture.__name__] = fixture
        try:
            result = execute_pipeline_definition(
                {
                    "dspy_modules": [
                        {
                            "module": "dspygen.modules.test_fixtures:First",
                            "args": {"text": "hello"},
                        },
                        {
                            "module": "dspygen.modules.test_fixtures:Second",
                            "args": {},
                        },
                    ]
                }
            )
        finally:
            sys.modules.pop(fixture.__name__, None)
        self.assertEqual(result, "<HELLO>")

    def test_external_namespace_is_refused(self):
        from dspygen.modules.dspygen_dsl_pipeline import (
            PipelineDefinitionRefusal,
            execute_pipeline_definition,
        )

        with self.assertRaisesRegex(
            PipelineDefinitionRefusal, "PIPELINE_MODULE_NAMESPACE_REFUSED"
        ):
            execute_pipeline_definition(
                {"dspy_modules": [{"module": "os:path", "args": {}}]}
            )


if __name__ == "__main__":
    unittest.main()
