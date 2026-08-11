"""DSPyGen meta-framework: process inference + bounded combinatorial DSPy search."""
from dspygen.meta.design import greedy_cover, pairwise_coverage, second_order_candidates
from dspygen.meta.dspy_adapter import configure_dspy_candidate, evaluate_candidate
from dspygen.meta.model import (
    CandidateConfig,
    ExperimentResult,
    MetaObservation,
    MetaReceipt,
    MetaRefusal,
    ProcessSpec,
    StageSpec,
)
from dspygen.meta.process_inference import infer_process
from dspygen.meta.runtime import MetaProgram

__all__ = [
    "CandidateConfig",
    "ExperimentResult",
    "MetaObservation",
    "MetaProgram",
    "MetaReceipt",
    "MetaRefusal",
    "ProcessSpec",
    "StageSpec",
    "configure_dspy_candidate",
    "evaluate_candidate",
    "greedy_cover",
    "infer_process",
    "pairwise_coverage",
    "second_order_candidates",
]
