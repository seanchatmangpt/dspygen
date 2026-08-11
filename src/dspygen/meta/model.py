"""Evidence-bounded process model for DSPy meta-programs.

The model is deliberately independent of any particular LM, optimizer, or
execution backend. It represents lawful process structure first; DSPy is an
adapter over that structure rather than the authority that defines it.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


def content_id(prefix: str, value: Any) -> str:
    return f"{prefix}:{sha256(_canonical(value).encode()).hexdigest()}"


class MetaRefusal(ValueError):
    """Typed refusal raised when a meta-program cannot be lawfully admitted."""

    def __init__(self, code: str, detail: str = "") -> None:
        self.code = code
        self.detail = detail
        super().__init__(f"{code}{': ' + detail if detail else ''}")


@dataclass(frozen=True, slots=True)
class StageSpec:
    stage_id: str
    requires: tuple[str, ...] = ()
    input_keys: tuple[str, ...] = ()
    output_keys: tuple[str, ...] = ()
    max_calls: int = 1
    tags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.stage_id:
            raise MetaRefusal("META-EMPTY-STAGE-ID")
        if self.max_calls < 1:
            raise MetaRefusal("META-INVALID-STAGE-BOUND", self.stage_id)


@dataclass(frozen=True, slots=True)
class ProcessSpec:
    process_id: str
    stages: tuple[StageSpec, ...]
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.process_id:
            raise MetaRefusal("META-EMPTY-PROCESS-ID")
        if not self.stages:
            raise MetaRefusal("META-EMPTY-PROCESS", self.process_id)
        ids = [stage.stage_id for stage in self.stages]
        if len(ids) != len(set(ids)):
            raise MetaRefusal("META-DUPLICATE-STAGE-ID", self.process_id)
        known = set(ids)
        for stage in self.stages:
            missing = set(stage.requires) - known
            if missing:
                raise MetaRefusal(
                    "META-UNKNOWN-DEPENDENCY", f"{stage.stage_id}: {sorted(missing)}"
                )
        self.topological_order()

    @property
    def digest(self) -> str:
        return content_id("process", asdict(self))

    def topological_order(self) -> tuple[str, ...]:
        dependencies = {s.stage_id: set(s.requires) for s in self.stages}
        result: list[str] = []
        ready = sorted(k for k, v in dependencies.items() if not v)
        while ready:
            node = ready.pop(0)
            result.append(node)
            for other in sorted(dependencies):
                if node in dependencies[other]:
                    dependencies[other].remove(node)
                    if not dependencies[other] and other not in result and other not in ready:
                        ready.append(other)
                        ready.sort()
        if len(result) != len(dependencies):
            unresolved = sorted(set(dependencies) - set(result))
            raise MetaRefusal("META-CYCLIC-PROCESS", ",".join(unresolved))
        return tuple(result)


@dataclass(frozen=True, slots=True)
class MetaObservation:
    subject: str
    revision: str
    examples_digest: str
    process_digest: str
    scope: tuple[str, ...] = ()

    @property
    def observation_id(self) -> str:
        return content_id("observation", asdict(self))


@dataclass(frozen=True, slots=True)
class CandidateConfig:
    candidate_id: str
    choices: tuple[tuple[str, str], ...]
    source_observation_id: str

    def as_dict(self) -> dict[str, str]:
        return dict(self.choices)


@dataclass(frozen=True, slots=True)
class ExperimentResult:
    candidate_id: str
    score: float
    metrics: Mapping[str, float | int | str]
    attempted: int
    succeeded: int
    evidence: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class MetaReceipt:
    process_digest: str
    observation_id: str
    candidate_id: str
    stage_outputs: tuple[tuple[str, str], ...]
    calls_used: int
    standing: str
    typed_refusals: tuple[str, ...] = ()

    @property
    def receipt_id(self) -> str:
        return content_id("meta-receipt", asdict(self))
