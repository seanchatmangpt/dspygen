"""Bounded, deterministic execution of admitted POWL 2.0 structures."""
from __future__ import annotations

from collections import Counter
from collections.abc import Callable, Mapping
from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Any

from dspygen.powl.algebra import Atom, ChoiceGraph, End, PartialOrder, PowlNode, Silent, Start
from dspygen.powl.algebra import PowlRefusal


def _digest(value: Any) -> str:
    body = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return sha256(body.encode()).hexdigest()


@dataclass(frozen=True, slots=True)
class ExecutionBound:
    max_atom_calls: int = 64
    max_choice_visits: int = 8

    def __post_init__(self) -> None:
        if self.max_atom_calls < 1 or self.max_choice_visits < 1:
            raise PowlRefusal("POWL-INVALID-EXECUTION-BOUND")


@dataclass(frozen=True, slots=True)
class PowlReceipt:
    graph_digest: str
    executed_atoms: tuple[str, ...]
    output_digests: tuple[tuple[str, str], ...]
    atom_calls: int
    choice_visits: int
    standing: str = "ALIVE"
    typed_refusals: tuple[str, ...] = ()

    @property
    def receipt_id(self) -> str:
        return f"powl-receipt:{_digest(asdict(self))}"


@dataclass(slots=True)
class _State:
    context: dict[str, Any]
    atoms: Mapping[str, Callable[..., Any]]
    bound: ExecutionBound
    executed: list[str]
    outputs: list[tuple[str, str]]
    atom_calls: int = 0
    choice_visits: int = 0


def graph_digest(node: PowlNode) -> str:
    """Stable structural identity; callable bodies are identified by names, not repr addresses."""

    def encode(item: PowlNode) -> Any:
        if isinstance(item, Start):
            return {"kind": "Start"}
        if isinstance(item, End):
            return {"kind": "End"}
        if isinstance(item, Silent):
            return {"kind": "Silent"}
        if isinstance(item, Atom):
            return {"kind": "Atom", "label": item.label, "bindings": dict(item.bindings)}
        if isinstance(item, PartialOrder):
            return {
                "kind": "PartialOrder",
                "children": [encode(c) for c in item.children],
                "order": sorted((int(e.src), int(e.dst)) for e in item.order),
                "frequency": (item.frequency.minimum, item.frequency.maximum),
            }
        if isinstance(item, ChoiceGraph):
            return {
                "kind": "ChoiceGraph",
                "children": [encode(c) for c in item.children],
                "edges": sorted((int(e.src), int(e.dst)) for e in item.edges),
                "start": item.start,
                "end": item.end,
                "frequency": (item.frequency.minimum, item.frequency.maximum),
            }
        raise PowlRefusal("POWL-UNKNOWN-NODE", type(item).__name__)

    return f"powl:{_digest(encode(node))}"


def execute(
    node: PowlNode,
    atoms: Mapping[str, Callable[..., Any]],
    *,
    inputs: Mapping[str, Any] | None = None,
    bound: ExecutionBound | None = None,
    choose: Callable[[ChoiceGraph, tuple[int, ...], Mapping[str, Any]], int] | None = None,
) -> tuple[dict[str, Any], PowlReceipt]:
    """Execute one bounded POWL run.

    Partial orders use a deterministic topological linearization for actuation while
    preserving the graph's true partial-order identity. A ChoiceGraph delegates each
    branch selection to ``choose``; absent a selector, the smallest enabled successor
    is chosen. Cycles are legal but bounded by ``max_choice_visits``.
    """
    state = _State(dict(inputs or {}), atoms, bound or ExecutionBound(), [], [])
    _run(node, state, choose)
    receipt = PowlReceipt(
        graph_digest=graph_digest(node),
        executed_atoms=tuple(state.executed),
        output_digests=tuple(state.outputs),
        atom_calls=state.atom_calls,
        choice_visits=state.choice_visits,
    )
    return state.context, receipt


def _run(
    node: PowlNode,
    state: _State,
    choose: Callable[[ChoiceGraph, tuple[int, ...], Mapping[str, Any]], int] | None,
) -> None:
    if isinstance(node, (Start, End, Silent)):
        return
    if isinstance(node, Atom):
        if state.atom_calls >= state.bound.max_atom_calls:
            raise PowlRefusal("POWL-ATOM-CALL-BOUND-EXHAUSTED", node.label)
        fn = state.atoms.get(node.label)
        if fn is None:
            raise PowlRefusal("POWL-MISSING-ATOM", node.label)
        kwargs = dict(state.context)
        kwargs.update(node.bindings)
        result = fn(**kwargs)
        state.atom_calls += 1
        state.executed.append(node.label)
        if isinstance(result, Mapping):
            state.context.update(result)
        else:
            state.context[node.label] = result
        state.outputs.append((node.label, _digest(result)))
        return
    if isinstance(node, PartialOrder):
        for _ in _frequency_count(node.frequency, state.bound.max_choice_visits):
            for idx in _topological_indices(node):
                _run(node.children[idx], state, choose)
        return
    if isinstance(node, ChoiceGraph):
        for _ in _frequency_count(node.frequency, state.bound.max_choice_visits):
            _run_choice(node, state, choose)
        return
    raise PowlRefusal("POWL-UNKNOWN-NODE", type(node).__name__)


def _frequency_count(freq: Any, cap: int) -> range:
    # A single run chooses the minimum lawful multiplicity. Unbounded frequencies
    # are therefore executable without guessing an infinite stopping policy.
    if freq.minimum > cap:
        raise PowlRefusal("POWL-FREQUENCY-BOUND-EXHAUSTED", f"{freq.minimum}>{cap}")
    return range(freq.minimum)


def _topological_indices(node: PartialOrder) -> tuple[int, ...]:
    n = len(node.children)
    deps = {i: {int(e.src) for e in node.closure if int(e.dst) == i} for i in range(n)}
    result: list[int] = []
    ready = sorted(i for i, incoming in deps.items() if not incoming)
    while ready:
        cur = ready.pop(0)
        result.append(cur)
        for other in range(n):
            if cur in deps[other]:
                deps[other].remove(cur)
                if not deps[other] and other not in result and other not in ready:
                    ready.append(other)
                    ready.sort()
    if len(result) != n:  # construction should have refused this already
        raise PowlRefusal("POWL-CYCLIC-PARTIAL-ORDER")
    return tuple(result)


def _run_choice(
    node: ChoiceGraph,
    state: _State,
    choose: Callable[[ChoiceGraph, tuple[int, ...], Mapping[str, Any]], int] | None,
) -> None:
    succ: dict[int, tuple[int, ...]] = {}
    for src in range(len(node.children)):
        succ[src] = tuple(sorted(int(e.dst) for e in node.edges if int(e.src) == src))
    visits: Counter[int] = Counter()
    cur = node.start
    while True:
        if state.choice_visits >= state.bound.max_choice_visits:
            raise PowlRefusal("POWL-CHOICE-VISIT-BOUND-EXHAUSTED", str(cur))
        visits[cur] += 1
        state.choice_visits += 1
        _run(node.children[cur], state, choose)
        if cur == node.end:
            return
        enabled = succ.get(cur, ())
        if not enabled:
            raise PowlRefusal("POWL-DEAD-END", str(cur))
        nxt = choose(node, enabled, state.context) if choose else enabled[0]
        if nxt not in enabled:
            raise PowlRefusal("POWL-INVALID-CHOICE", f"{nxt} not in {enabled}")
        cur = nxt
