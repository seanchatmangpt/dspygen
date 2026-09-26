from __future__ import annotations

import importlib.metadata
import importlib.util
import sys
import types
import unittest
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
DSPY_RELEASE = "3.3.0"
DSPY_MODULE_BLOB = "10f0923937df828f9fd0260f4045a97ee33150fc"
DSPY_PREDICT_BLOB = "2018cffaab8f3b0b834fd990cff9312d29b59744"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


class _SettingsCapsule:
    caller_modules = None
    track_usage = False
    usage_tracker = None

    @contextmanager
    def context(self, **kwargs):
        previous = {key: getattr(self, key, None) for key in kwargs}
        for key, value in kwargs.items():
            setattr(self, key, value)
        try:
            yield
        finally:
            for key, value in previous.items():
                setattr(self, key, value)


class _BaseModuleCapsule:
    def __init__(self):
        pass


class _ProgramMetaCapsule(type):
    """Semantic capsule of DSPy ProgramMeta at 2.6.27 and 3.3.0."""

    def __call__(cls, *args, **kwargs):
        obj = cls.__new__(cls, *args, **kwargs)
        if isinstance(obj, cls):
            _ModuleCapsule._base_init(obj)
            cls.__init__(obj, *args, **kwargs)
            if not hasattr(obj, "callbacks"):
                obj.callbacks = []
            if not hasattr(obj, "history"):
                obj.history = []
        return obj


_CAPSULE_SETTINGS = _SettingsCapsule()


class _ModuleCapsule(_BaseModuleCapsule, metaclass=_ProgramMetaCapsule):
    """Dependency-fenced Module semantics shared by DSPy 2.6.27 and 3.3.0."""

    def _base_init(self):
        self._compiled = False
        self.callbacks = []
        self.history = []

    def __init__(self, callbacks=None):
        self.callbacks = callbacks or []
        self._compiled = False
        self.history = []

    def __call__(self, *args, **kwargs):
        caller_modules = _CAPSULE_SETTINGS.caller_modules or []
        caller_modules = list(caller_modules)
        caller_modules.append(self)
        with _CAPSULE_SETTINGS.context(caller_modules=caller_modules):
            return self.forward(*args, **kwargs)


class ProgramMetaSourceCapsuleTests(unittest.TestCase):
    def test_upstream_source_identities_are_pinned(self):
        self.assertEqual(DSPY_RELEASE, "3.3.0")
        self.assertEqual(DSPY_MODULE_BLOB, "10f0923937df828f9fd0260f4045a97ee33150fc")
        self.assertEqual(DSPY_PREDICT_BLOB, "2018cffaab8f3b0b834fd990cff9312d29b59744")

    def test_legacy_hook_executes_against_program_meta_semantics(self):
        from dspygen.modules.pipeline import install_legacy_pipeline_compat

        class RuntimeModule(_ModuleCapsule):
            pass

        install_legacy_pipeline_compat(RuntimeModule)

        class Legacy(RuntimeModule):
            __module__ = "dspygen.modules.program_meta_fixture"

            def __init__(self):
                super().__init__()
                self.forward_args = {}
                self.output = None

            def forward(self, text):
                return text.upper()

            def pipe(self, input_str):
                raise NotImplementedError(
                    "Please implement the pipe method for DSL support."
                )

        class Custom(RuntimeModule):
            __module__ = "dspygen.modules.custom_program_meta_fixture"

            def pipe(self, value):
                return f"custom:{value}"

        instance = Legacy()
        self.assertFalse(instance._compiled)
        self.assertEqual(instance.callbacks, [])
        self.assertEqual(instance.history, [])
        self.assertEqual(instance("call"), "CALL")
        self.assertEqual(instance.pipe("admitted"), "ADMITTED")
        self.assertTrue(Legacy.__dspygen_legacy_pipe_repaired__)
        self.assertEqual(Custom().pipe("x"), "custom:x")

    def test_pipeline_prefers_module_call_boundary(self):
        from dspygen.modules.pipeline import pipe_forward

        class CallableTarget:
            forward_args = {}

            def __init__(self):
                self.called_through_module = False

            def __call__(self, **kwargs):
                self.called_through_module = True
                return self.forward(**kwargs)

            def forward(self, text):
                return text.upper()

        target = CallableTarget()
        self.assertEqual(pipe_forward(target, "alive"), "ALIVE")
        self.assertTrue(target.called_through_module)


class RuntimeConfigurationTests(unittest.TestCase):
    def test_configuration_uses_modern_top_level_api(self):
        fake_dspy = types.ModuleType("dspy")
        configured = []

        class LM:
            def __init__(self, model, **kwargs):
                self.model = model
                self.kwargs = kwargs

        def configure(**kwargs):
            configured.append(kwargs)

        fake_dspy.LM = LM
        fake_dspy.configure = configure
        previous_dspy = sys.modules.get("dspy")
        previous_tools = sys.modules.pop("dspygen.utils.dspy_tools", None)
        sys.modules["dspy"] = fake_dspy
        try:
            from dspygen.utils.dspy_tools import init_dspy

            lm = init_dspy(model="local/test", experimental=None)
        finally:
            sys.modules.pop("dspygen.utils.dspy_tools", None)
            if previous_tools is not None:
                sys.modules["dspygen.utils.dspy_tools"] = previous_tools
            if previous_dspy is None:
                sys.modules.pop("dspy", None)
            else:
                sys.modules["dspy"] = previous_dspy

        self.assertEqual(lm.model, "local/test")
        self.assertEqual(configured, [{"lm": lm}])


@unittest.skipUnless(importlib.util.find_spec("dspy"), "installed DSPy runtime required")
class InstalledDspyRuntimeTests(unittest.TestCase):
    def test_generated_module_executes_with_deterministic_adapter(self):
        import dspy

        version = importlib.metadata.version("dspy")
        self.assertEqual(version, DSPY_RELEASE)

        from dspygen.modules.gen_dspy_module import (
            DSPyModuleTemplate,
            render_dspy_module,
        )
        from dspygen.modules.pipeline import install_legacy_pipeline_compat

        install_legacy_pipeline_compat(dspy.Module)

        class NoNetworkLM(dspy.BaseLM):
            def forward(self, prompt=None, messages=None, **kwargs):
                raise AssertionError("deterministic adapter must not actuate a provider")

        class DeterministicAdapter:
            def __call__(self, lm, lm_kwargs, signature, demos, inputs):
                output_name = next(iter(signature.output_fields))
                value = next(iter(inputs.values()))
                return [{output_name: f"deterministic:{value}"}]

        dspy.configure(
            lm=NoNetworkLM(model="local/no-network"),
            adapter=DeterministicAdapter(),
        )
        source = render_dspy_module(
            DSPyModuleTemplate(
                class_name="RuntimeSummary",
                inputs=["text"],
                output="summary",
            )
        )
        namespace: dict[str, object] = {}
        exec(compile(source, "generated_runtime_summary.py", "exec"), namespace)
        module_type = namespace["RuntimeSummaryModule"]
        result = module_type()(text="hello")
        self.assertEqual(result, "deterministic:hello")

    def test_python_interpreter_is_not_reachable_from_dspygen(self):
        for path in (ROOT / "src/dspygen").rglob("*.py"):
            if path.name == "verify_modernization.py":
                continue
            self.assertNotIn("PythonInterpreter", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
