#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROGRAM = ROOT / "src/dspy_program.py"
OPTIMIZE = ROOT / "src/dspy_optimize.py"


def main() -> int:
    failures: list[str] = []
    for path in (PROGRAM, OPTIMIZE):
        if not path.is_file():
            failures.append(f"missing projection: {path.relative_to(ROOT)}")
            continue
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            failures.append(f"invalid python: {path.name}: {exc}")

    program = PROGRAM.read_text(encoding="utf-8") if PROGRAM.is_file() else ""
    optimize = OPTIMIZE.read_text(encoding="utf-8") if OPTIMIZE.is_file() else ""

    required_program = {
        "Predict": "dspy.Predict(",
        "ChainOfThought": "dspy.ChainOfThought(",
        "ProgramOfThought": "dspy.ProgramOfThought(",
        "RLM": "dspy.RLM(",
        "Pipeline": "class rag_candidate",
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
        "pack_source": "seanchatmangpt/ggen@306ff6903bf53e08d4237ec2cacbe8dab553ae83:packs/dspy-pack",
        "reasoning_topologies": list(required_program),
        "optimizer_families": list(required_optimizer),
        "explicit_optimizer_experiments": len(expected_experiments),
        "failures": failures,
    }
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
