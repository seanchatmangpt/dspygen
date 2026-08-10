"""Bounded process inference from observed successful execution traces."""
from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Sequence

from dspygen.meta.model import MetaRefusal, ProcessSpec, StageSpec


def infer_process(
    traces: Iterable[Sequence[str]],
    *,
    process_id: str = "inferred-process",
    min_support: int = 1,
) -> ProcessSpec:
    """Infer a partial order while preserving observed concurrency."""
    if min_support < 1:
        raise MetaRefusal("META-INVALID-SUPPORT", str(min_support))
    normalized = [tuple(trace) for trace in traces if trace]
    if not normalized:
        raise MetaRefusal("META-NO-TRACES")
    nodes = sorted({node for trace in normalized for node in trace})
    before: Counter[tuple[str, str]] = Counter()
    for trace in normalized:
        if len(trace) != len(set(trace)):
            raise MetaRefusal("META-TRACE-REPEATED-STAGE", repr(trace))
        positions = {node: index for index, node in enumerate(trace)}
        for left in positions:
            for right in positions:
                if positions[left] < positions[right]:
                    before[(left, right)] += 1

    edges = {
        (left, right)
        for left in nodes
        for right in nodes
        if left != right
        and before[(left, right)] >= min_support
        and before[(right, left)] == 0
    }

    def reachable(src: str, dst: str, without: tuple[str, str]) -> bool:
        frontier = [src]
        seen = {src}
        while frontier:
            node = frontier.pop()
            for edge_src, edge_dst in edges:
                if (edge_src, edge_dst) == without or edge_src != node:
                    continue
                if edge_dst == dst:
                    return True
                if edge_dst not in seen:
                    seen.add(edge_dst)
                    frontier.append(edge_dst)
        return False

    reduced = {edge for edge in edges if not reachable(edge[0], edge[1], edge)}
    stages = tuple(
        StageSpec(
            stage_id=node,
            requires=tuple(sorted(src for src, dst in reduced if dst == node)),
            tags=("inferred",),
        )
        for node in nodes
    )
    return ProcessSpec(
        process_id=process_id,
        stages=stages,
        metadata={
            "trace_count": len(normalized),
            "min_support": min_support,
            "inference": "unidirectional-precedence-with-concurrency-preservation",
        },
    )
