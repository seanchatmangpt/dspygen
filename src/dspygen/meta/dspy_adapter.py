"""DSPy adapter for the process-science meta framework."""
from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from dspygen.meta.model import CandidateConfig, ExperimentResult, MetaRefusal


def configure_dspy_candidate(
    program: Any,
    candidate: CandidateConfig,
    optimizers: Mapping[str, Callable[..., Any]],
) -> Any:
    """Compile a DSPy program from a candidate without ambient actuation authority."""
    choices = candidate.as_dict()
    optimizer_name = choices.pop("optimizer", "identity")
    if optimizer_name == "identity":
        return program
    factory = optimizers.get(optimizer_name)
    if factory is None:
        raise MetaRefusal("META-UNKNOWN-DSPY-OPTIMIZER", optimizer_name)
    return factory(**choices).compile(program)


def evaluate_candidate(
    candidate: CandidateConfig,
    program: Callable[..., Any],
    examples: list[Mapping[str, Any]],
    metric: Callable[[Any, Mapping[str, Any]], float],
) -> ExperimentResult:
    """Evaluate one candidate against an explicit admitted example population."""
    if not examples:
        raise MetaRefusal("META-EMPTY-EVALUATION-POPULATION")
    score = 0.0
    succeeded = 0
    for example in examples:
        prediction = program(**dict(example))
        value = float(metric(prediction, example))
        score += value
        succeeded += int(value > 0)
    return ExperimentResult(
        candidate_id=candidate.candidate_id,
        score=score / len(examples),
        metrics={"mean_metric": score / len(examples), "population": len(examples)},
        attempted=len(examples),
        succeeded=succeeded,
        evidence=("explicit-population", "deterministic-candidate-identity"),
    )
