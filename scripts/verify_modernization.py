#!/usr/bin/env python3
"""Independent verifier for the DSPyGen ERRC modernization boundary."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import tomllib
from pathlib import Path
from typing import Any

LEGACY_PIPE_PLACEHOLDER = "Please implement the pipe method for DSL support."
NGROK_SECRET = re.compile(r"^\s*authtoken\s*:\s*(?!\$|\{|$)(\S+)", re.MULTILINE)
DSPY_RUNTIME = "^3.2.1"
DSPY_CI_PIN = 'dspy==3.3.0'
DSPY_WHEEL_SHA256 = '358cbfb15d13246dc4a289bb2350c0ee602260c8a3869f7f63a48a9d2233e48c'
DSPY_MODULE_BLOB = '10f0923937df828f9fd0260f4045a97ee33150fc'
DSPY_PREDICT_BLOB = '2018cffaab8f3b0b834fd990cff9312d29b59744'


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(root: Path, expected_legacy_placeholders: int | None = None) -> dict[str, Any]:
    modules_root = root / "src/dspygen/modules"
    code_action_path = root / "src/dspygen/lsp/providers/code_action.py"
    dspy_tools_path = root / "src/dspygen/utils/dspy_tools.py"
    pyproject_path = root / "pyproject.toml"
    workflow_path = root / ".github/workflows/test.yml"
    runtime_test_path = root / "tests/test_dspy_runtime_integration.py"
    required = [
        root / "src/dspygen/project.py",
        root / "src/dspygen/cli.py",
        modules_root / "pipeline.py",
        modules_root / "gen_dspy_module.py",
        modules_root / "dspygen_dsl_pipeline.py",
        root / "src/dspygen/subcommands/module_cmd.py",
        code_action_path,
        dspy_tools_path,
        pyproject_path,
        workflow_path,
        runtime_test_path,
        root / "ngrok.yml",
    ]
    missing = [str(path.relative_to(root)) for path in required if not path.is_file()]

    parsed = 0
    legacy_placeholders: list[str] = []
    invalid: list[str] = []
    python_interpreter_references: list[str] = []
    for path in sorted((root / "src").rglob("*.py")):
        text = path.read_text(encoding="utf-8")
        try:
            tree = ast.parse(text, filename=str(path))
        except SyntaxError as exc:
            invalid.append(f"{path.relative_to(root)}: syntax: {exc}")
            continue
        parsed += 1
        relative = str(path.relative_to(root))
        if "PythonInterpreter" in text:
            python_interpreter_references.append(relative)
        if path.name in {"pipeline.py", "gen_dspy_module.py"} or LEGACY_PIPE_PLACEHOLDER not in text:
            continue
        legacy_placeholders.append(relative)
        exact_pipe = False
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "pipe":
                segment = ast.get_source_segment(text, node) or ""
                if LEGACY_PIPE_PLACEHOLDER in segment:
                    exact_pipe = True
                    break
        if not exact_pipe:
            invalid.append(f"{relative}: placeholder outside pipe")

    if expected_legacy_placeholders is not None and len(legacy_placeholders) != expected_legacy_placeholders:
        invalid.append(
            "legacy placeholder count mismatch: "
            f"expected={expected_legacy_placeholders} observed={len(legacy_placeholders)}"
        )

    init_text = (modules_root / "__init__.py").read_text(encoding="utf-8") if (modules_root / "__init__.py").is_file() else ""
    generator_text = (modules_root / "gen_dspy_module.py").read_text(encoding="utf-8") if (modules_root / "gen_dspy_module.py").is_file() else ""
    pipeline_text = (modules_root / "pipeline.py").read_text(encoding="utf-8") if (modules_root / "pipeline.py").is_file() else ""
    cli_text = (root / "src/dspygen/cli.py").read_text(encoding="utf-8") if (root / "src/dspygen/cli.py").is_file() else ""
    code_action_text = code_action_path.read_text(encoding="utf-8") if code_action_path.is_file() else ""
    dspy_tools_text = dspy_tools_path.read_text(encoding="utf-8") if dspy_tools_path.is_file() else ""
    workflow_text = workflow_path.read_text(encoding="utf-8") if workflow_path.is_file() else ""
    runtime_test_text = runtime_test_path.read_text(encoding="utf-8") if runtime_test_path.is_file() else ""
    ngrok_text = (root / "ngrok.yml").read_text(encoding="utf-8") if (root / "ngrok.yml").is_file() else ""

    dependencies: dict[str, Any] = {}
    if pyproject_path.is_file():
        dependencies = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))["tool"]["poetry"]["dependencies"]

    checks = {
        "required_files": not missing,
        "python_syntax": not invalid,
        "legacy_placeholders_are_exact": not invalid,
        "legacy_compat_hook": "install_legacy_pipeline_compat" in init_text,
        "generator_complete": (
            LEGACY_PIPE_PLACEHOLDER not in generator_text
            and "pipe_forward" in generator_text
            and "return {class_name}()({call_kwargs})" in generator_text
        ),
        "module_call_boundary": "invoke = module if callable(module)" in pipeline_text,
        "lsp_does_not_manufacture_runtime_stubs": (
            "raise NotImplementedError" not in code_action_text
            and "dspy.Prediction(**inputs)" in code_action_text
        ),
        "modern_dspy_dependency": (
            dependencies.get("dspy") == DSPY_RUNTIME and "dspy-ai" not in dependencies
        ),
        "modern_dspy_configuration": (
            "dspy.OpenAI" not in dspy_tools_text
            and "dspy.OllamaLocal" not in dspy_tools_text
            and "experimental=experimental" not in dspy_tools_text
            and "getattr(dspy, \"configure\"" in dspy_tools_text
        ),
        "installed_runtime_witness": (
            'DSPY_RELEASE = "3.3.0"' in runtime_test_text
            and "self.assertEqual(version, DSPY_RELEASE)" in runtime_test_text
            and DSPY_MODULE_BLOB in runtime_test_text
            and DSPY_PREDICT_BLOB in runtime_test_text
            and "DeterministicAdapter" in runtime_test_text
            and "NoNetworkLM" in runtime_test_text
        ),
        "ci_pins_runtime_and_executes_witness": (
            DSPY_CI_PIN in workflow_text
            and DSPY_WHEEL_SHA256 in workflow_text
            and "--only-binary=:all:" in workflow_text
            and "sha256sum --check --strict" in workflow_text
            and "test_*runtime*.py" in workflow_text
            and "--expected-legacy-placeholders 45" in workflow_text
        ),
        "vulnerable_interpreter_unreachable": not python_interpreter_references,
        "no_ambient_runtime_install": (
            "check_or_install_packages" not in cli_text
            and "cruft\", \"create" not in cli_text
            and "os.chdir(" not in cli_text
        ),
        "ngrok_secret_removed": NGROK_SECRET.search(ngrok_text) is None,
    }
    status = "ALIVE" if all(checks.values()) else "BUILD_BROKEN"
    return {
        "status": status,
        "checks": checks,
        "runtime_contract": {
            "package": "dspy",
            "poetry_constraint": dependencies.get("dspy"),
            "ci_pin": "3.3.0",
            "wheel_sha256": DSPY_WHEEL_SHA256,
            "upstream_module_blob": DSPY_MODULE_BLOB,
            "upstream_predict_blob": DSPY_PREDICT_BLOB,
            "provider_actuation": "REFUSED:NOT_REQUIRED_FOR_DETERMINISTIC_WITNESS",
            "python_interpreter": "EXCLUDED:UNREACHABLE",
        },
        "missing": missing,
        "parsed_python_files": parsed,
        "legacy_placeholders_covered": len(legacy_placeholders),
        "expected_legacy_placeholders": expected_legacy_placeholders,
        "legacy_placeholder_files": legacy_placeholders,
        "python_interpreter_references": python_interpreter_references,
        "invalid": invalid,
        "hashes": {
            str(path.relative_to(root)): _sha256(path)
            for path in required
            if path.is_file()
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    parser.add_argument("--expected-legacy-placeholders", type=int)
    args = parser.parse_args()
    report = verify(
        args.root.resolve(),
        expected_legacy_placeholders=args.expected_legacy_placeholders,
    )
    payload = json.dumps(report, indent=2, sort_keys=True)
    print(payload)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    return 0 if report["status"] == "ALIVE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
