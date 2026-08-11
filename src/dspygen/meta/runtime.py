"""Bounded execution runtime for admitted DSPy meta-programs."""
from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from dspygen.meta.model import MetaObservation, MetaReceipt, MetaRefusal, ProcessSpec, content_id

StageCallable = Callable[..., Any]


class MetaProgram:
    """Execute an admitted process graph over registered stage callables."""

    def __init__(
        self,
        process: ProcessSpec,
        stages: Mapping[str, StageCallable],
        *,
        max_total_calls: int | None = None,
    ) -> None:
        missing = set(process.topological_order()) - set(stages)
        if missing:
            raise MetaRefusal("META-MISSING-STAGE-IMPLEMENTATION", ",".join(sorted(missing)))
        self.process = process
        self.stages = dict(stages)
        self.max_total_calls = max_total_calls or sum(stage.max_calls for stage in process.stages)
        if self.max_total_calls < 1:
            raise MetaRefusal("META-INVALID-RUNTIME-BOUND")

    def __call__(
        self,
        observation: MetaObservation,
        *,
        candidate_id: str = "baseline",
        inputs: Mapping[str, Any] | None = None,
    ) -> tuple[dict[str, Any], MetaReceipt]:
        if observation.process_digest != self.process.digest:
            raise MetaRefusal("META-OBSERVATION-PROCESS-MISMATCH")
        context: dict[str, Any] = dict(inputs or {})
        output_digests: list[tuple[str, str]] = []
        calls = 0
        specs = {stage.stage_id: stage for stage in self.process.stages}
        completed: set[str] = set()

        for stage_id in self.process.topological_order():
            spec = specs[stage_id]
            if not set(spec.requires) <= completed:
                raise MetaRefusal("META-DEPENDENCY-NOT-COMPLETE", stage_id)
            if calls + 1 > self.max_total_calls:
                raise MetaRefusal("META-RUNTIME-BOUND-EXHAUSTED", stage_id)
            kwargs = context if not spec.input_keys else {key: context[key] for key in spec.input_keys}
            result = self.stages[stage_id](**kwargs)
            calls += 1
            if isinstance(result, Mapping):
                context.update(result)
            else:
                context[stage_id] = result
            output_digests.append((stage_id, content_id("stage-output", result)))
            completed.add(stage_id)

        receipt = MetaReceipt(
            process_digest=self.process.digest,
            observation_id=observation.observation_id,
            candidate_id=candidate_id,
            stage_outputs=tuple(output_digests),
            calls_used=calls,
            standing="ALIVE",
        )
        return context, receipt
