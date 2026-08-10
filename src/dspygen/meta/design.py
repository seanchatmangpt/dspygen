"""Combinatorial design operators for DSPy meta-program search."""
from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from itertools import combinations

from dspygen.meta.model import CandidateConfig, MetaRefusal, content_id

Constraint = Callable[[Mapping[str, str]], bool]


def _admitted(config: Mapping[str, str], constraints: Sequence[Constraint]) -> bool:
    return all(rule(config) for rule in constraints)


def second_order_candidates(
    dimensions: Mapping[str, Sequence[str]],
    baseline: Mapping[str, str],
    source_observation_id: str,
    *,
    constraints: Sequence[Constraint] = (),
) -> tuple[CandidateConfig, ...]:
    """Represent a baseline plus lawful one- and two-factor substitutions."""
    names = tuple(sorted(dimensions))
    if set(names) != set(baseline):
        raise MetaRefusal("META-BASELINE-DIMENSION-MISMATCH")
    for name in names:
        if baseline[name] not in dimensions[name]:
            raise MetaRefusal("META-BASELINE-OPTION-UNKNOWN", name)

    raw: list[dict[str, str]] = [dict(baseline)]
    alternatives = {
        name: tuple(option for option in dimensions[name] if option != baseline[name])
        for name in names
    }
    for name in names:
        for option in alternatives[name]:
            config = dict(baseline)
            config[name] = option
            raw.append(config)
    for left, right in combinations(names, 2):
        for left_option in alternatives[left]:
            for right_option in alternatives[right]:
                config = dict(baseline)
                config[left] = left_option
                config[right] = right_option
                raw.append(config)

    seen: set[tuple[tuple[str, str], ...]] = set()
    candidates: list[CandidateConfig] = []
    for config in raw:
        choices = tuple(sorted(config.items()))
        if choices in seen or not _admitted(config, constraints):
            continue
        seen.add(choices)
        candidates.append(
            CandidateConfig(
                candidate_id=content_id("candidate", choices),
                choices=choices,
                source_observation_id=source_observation_id,
            )
        )
    if not candidates:
        raise MetaRefusal("META-NO-ADMITTED-CANDIDATES")
    return tuple(candidates)


def pairwise_coverage(candidate: CandidateConfig) -> frozenset[tuple[str, str, str, str]]:
    choices = candidate.choices
    return frozenset(
        (a_name, a_value, b_name, b_value)
        for (a_name, a_value), (b_name, b_value) in combinations(choices, 2)
    )


def greedy_cover(
    candidates: Iterable[CandidateConfig], *, max_candidates: int
) -> tuple[CandidateConfig, ...]:
    """Select a deterministic bounded portfolio maximizing uncovered pairs."""
    if max_candidates < 1:
        raise MetaRefusal("META-INVALID-EXPERIMENT-BOUND", str(max_candidates))
    remaining = list(candidates)
    selected: list[CandidateConfig] = []
    covered: set[tuple[str, str, str, str]] = set()
    while remaining and len(selected) < max_candidates:
        ranked = sorted(
            remaining,
            key=lambda candidate: (
                -len(pairwise_coverage(candidate) - covered),
                candidate.candidate_id,
            ),
        )
        winner = ranked[0]
        gain = pairwise_coverage(winner) - covered
        if selected and not gain:
            break
        selected.append(winner)
        covered.update(pairwise_coverage(winner))
        remaining.remove(winner)
    return tuple(selected)
