#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROGRAM = ROOT / "src/dspy_program.py"
OPTIMIZE = ROOT / "src/dspy_optimize.py"
FACTORY_SHA = "ddfa602bfbab57b7ed5150f61b0acac7a41e3020"


def _call_name(node: ast.Call) -> str | None:
    func = node.func
    if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
        return f"{func.value.id}.{func.attr}"
    if isinstance(func, ast.Name):
        return func.id
    return None


def _has_pipeline_topology(tree: ast.AST) -> bool:
    """Verify the generated Retrieve -> ChainOfThought pipeline structurally.

    The dspy-pack owns the generated class naming convention, so consumer
    qualification must not depend on the textual spelling/casing of that
    generated class. A pipeline is admitted when one generated dspy.Module
    class contains both the retrieval and reasoning constructors required by
    the canonical consumer ontology.
    """
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        bases = {
            f"{base.value.id}.{base.attr}"
            for base in node.bases
            if isinstance(base, ast.Attribute) and isinstance(base.value, ast.Name)
        }
        if "dspy.Module" not in bases:
            continue
        calls = {
            name
            for child in ast.walk(node)
            if isinstance(child, ast.Call) and (name := _call_name(child)) is not None
        }
        if {"dspy.Retrieve", "dspy.ChainOfThought"}.issubset(calls):
            return True
    return False


def main() -> int:
    failures: list[str] = []
    parsed: dict[Path, ast.AST] = {}
    for path in (PROGRAM, OPTIMIZE):
        if not path.is_file():
            failures.append(f"missing projection: {path.relative_to(ROOT)}")
            continue
        try:
            parsed[path] = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            failures.append(f"invalid python: {path.name}: {exc}")

    program = PROGRAM.read_text(encoding="utf-8") if PROGRAM.is_file() else ""
    optimize = OPTIMIZE.read_text(encoding="utf-8") if OPTIMIZE.is_file() else ""

    required_program = {
        "Predict": "dspy.Predict(",
        "ChainOfThought": "dspy.ChainOfThought(",
        "ProgramOfThought": "dspy.ProgramOfThought(",
        "RLM": "dspy.RLM(",
        "Retrieve": "dspy.Retrieve(",
    }
    required_optimizer = {
        "COPRO": "dspy.COPRO(",
        "MIPROv2": "dspy.MIPROv2(",
        "SIMBA": "dspy.SIMBA(",
        "InferRules": "dspy.InferRules(",
        "LabeledFewShot": "dspy.LabeledFewShot(",
    }
    for name, needle in required_program.items():
        if needle not in program:
            failures.append(f"missing program topology: {name}")
    if PROGRAM in parsed and not _has_pipeline_topology(parsed[PROGRAM]):
        failures.append("missing program topology: Pipeline[Retrieve->ChainOfThought]")
    for name, needle in required_optimizer.items():
        if needle not in optimize:
            failures.append(f"missing optimizer family: {name}")

    # Two independent optimizer targets × five optimizer families = ten
    # explicit experiments before any expensive optimization is executed.
    expected_experiments = [
        "predict_copro", "predict_mipro", "predict_simba", "predict_rules", "predict_fewshot",
        "cot_copro", "cot_mipro", "cot_simba", "cot_rules", "cot_fewshot",
    ]
    missing_experiments = [name for name in expected_experiments if name not in optimize]
    if missing_experiments:
        failures.append("missing experiments: " + ", ".join(missing_experiments))

    receipt = {
        "status": "ALIVE" if not failures else "BUILD_BROKEN",
        "authority": "CONSTRUCT_ONLY",
        "actuation": "REFUSED",
        "pack_source": f"seanchatmangpt/ggen@{FACTORY_SHA}:packs/dspy-pack",
        "reasoning_topologies": [*required_program, "Pipeline"],
        "optimizer_families": list(required_optimizer),
        "explicit_optimizer_experiments": len(expected_experiments),
        "failures": failures,
    }
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
