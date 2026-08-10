"""POWL 2.0 algebra for DSPyGen.

This is a deliberately small, dependency-free process algebra distilled from
AutoFDE-Lab's POWL 2.0 implementation.  POWL describes structure only; it has
no ambient execution authority.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, NewType, TypeAlias, Union

NodeId = NewType("NodeId", int)
MAX_POWL_DEPTH = 8


class PowlRefusal(ValueError):
    """Typed refusal for invalid or unbounded POWL structures."""

    def __init__(self, code: str, detail: str = "") -> None:
        self.code = code
        self.detail = detail
        super().__init__(f"{code}{': ' + detail if detail else ''}")


@dataclass(frozen=True, slots=True, order=True)
class OrderEdge:
    src: NodeId
    dst: NodeId


@dataclass(frozen=True, slots=True, order=True)
class ChoiceGraphEdge:
    src: NodeId
    dst: NodeId


def _check_order_edges(edges: frozenset[OrderEdge], n: int) -> None:
    for edge in edges:
        if not isinstance(edge, OrderEdge):
            raise PowlRefusal("POWL-EDGE-TYPE-MISMATCH", type(edge).__name__)
        if not (0 <= edge.src < n and 0 <= edge.dst < n):
            raise PowlRefusal("POWL-DANGLING-REFERENCE", f"{edge.src}->{edge.dst}/{n}")


def transitive_closure(edges: frozenset[OrderEdge], n: int) -> frozenset[OrderEdge]:
    edges = frozenset(edges)
    _check_order_edges(edges, n)
    reach = [[False] * n for _ in range(n)]
    for edge in edges:
        reach[edge.src][edge.dst] = True
    for k in range(n):
        for i in range(n):
            if reach[i][k]:
                for j in range(n):
                    if reach[k][j]:
                        reach[i][j] = True
    for i in range(n):
        if reach[i][i]:
            raise PowlRefusal("POWL-CYCLIC-PARTIAL-ORDER", str(i))
    return frozenset(
        OrderEdge(NodeId(i), NodeId(j))
        for i in range(n)
        for j in range(n)
        if reach[i][j]
    )


def transitive_reduction(edges: frozenset[OrderEdge], n: int) -> frozenset[OrderEdge]:
    closure = transitive_closure(edges, n)
    reach = [[False] * n for _ in range(n)]
    for edge in closure:
        reach[edge.src][edge.dst] = True
    return frozenset(
        edge
        for edge in closure
        if not any(
            k != edge.src
            and k != edge.dst
            and reach[edge.src][k]
            and reach[k][edge.dst]
            for k in range(n)
        )
    )


@dataclass(frozen=True, slots=True)
class Frequency:
    minimum: int = 1
    maximum: int | None = 1

    def __post_init__(self) -> None:
        if self.minimum < 0:
            raise PowlRefusal("POWL-INVALID-FREQUENCY", f"minimum={self.minimum}")
        if self.maximum is not None and self.maximum < self.minimum:
            raise PowlRefusal(
                "POWL-INVALID-FREQUENCY", f"{self.minimum}>{self.maximum}"
            )

    def allows(self, n: int) -> bool:
        return n >= self.minimum and (self.maximum is None or n <= self.maximum)


ONCE = Frequency(1, 1)
OPTIONAL = Frequency(0, 1)
ONE_OR_MORE = Frequency(1, None)
ZERO_OR_MORE = Frequency(0, None)


@dataclass(frozen=True, slots=True)
class Start:
    pass


@dataclass(frozen=True, slots=True)
class End:
    pass


@dataclass(frozen=True, slots=True)
class Silent:
    pass


@dataclass(frozen=True, slots=True)
class Atom:
    label: str
    action: Any = field(default=None, compare=False)
    bindings: Mapping[str, Any] = field(default_factory=dict, compare=False)

    def __post_init__(self) -> None:
        if not self.label:
            raise PowlRefusal("POWL-EMPTY-ATOM-LABEL")


@dataclass(frozen=True, slots=True)
class PartialOrder:
    children: tuple["PowlNode", ...]
    order: frozenset[OrderEdge] = frozenset()
    frequency: Frequency = ONCE
    _closure: frozenset[OrderEdge] = field(
        init=False, compare=False, repr=False, hash=False, default=frozenset()
    )
    _depth: int = field(init=False, compare=False, repr=False, hash=False, default=1)

    def __post_init__(self) -> None:
        n = len(self.children)
        if n < 2:
            raise PowlRefusal("POWL-INVALID-PARTIAL-ORDER-ARITY", str(n))
        closure = transitive_closure(frozenset(self.order), n)
        object.__setattr__(self, "order", transitive_reduction(closure, n))
        object.__setattr__(self, "_closure", closure)
        object.__setattr__(self, "_depth", _composite_depth(self.children))

    @property
    def closure(self) -> frozenset[OrderEdge]:
        return self._closure

    @property
    def depth(self) -> int:
        return self._depth


@dataclass(frozen=True, slots=True)
class ChoiceGraph:
    children: tuple["PowlNode", ...]
    edges: frozenset[ChoiceGraphEdge]
    start: int = 0
    end: int = 1
    frequency: Frequency = ONCE
    _depth: int = field(init=False, compare=False, repr=False, hash=False, default=1)

    def __post_init__(self) -> None:
        n = len(self.children)
        if n < 2:
            raise PowlRefusal("POWL-INVALID-CHOICE-ARITY", str(n))
        if self.start == self.end or not (0 <= self.start < n and 0 <= self.end < n):
            raise PowlRefusal("POWL-INVALID-CHOICE-BOUNDARY")
        for edge in self.edges:
            if not isinstance(edge, ChoiceGraphEdge):
                raise PowlRefusal("POWL-EDGE-TYPE-MISMATCH", type(edge).__name__)
            if not (0 <= edge.src < n and 0 <= edge.dst < n):
                raise PowlRefusal("POWL-DANGLING-REFERENCE", f"{edge.src}->{edge.dst}/{n}")
            if edge.dst == self.start or edge.src == self.end:
                raise PowlRefusal("POWL-MULTI-BOUNDARY-CHOICE-GRAPH")
        _validate_choice_reachability(self)
        object.__setattr__(self, "_depth", _composite_depth(self.children))

    @property
    def depth(self) -> int:
        return self._depth


PowlNode: TypeAlias = Union[Start, End, Atom, Silent, PartialOrder, ChoiceGraph]


def node_depth(node: PowlNode) -> int:
    return node.depth if isinstance(node, (PartialOrder, ChoiceGraph)) else 1


def _composite_depth(children: tuple[PowlNode, ...]) -> int:
    depth = 1 + max((node_depth(child) for child in children), default=0)
    if depth > MAX_POWL_DEPTH:
        raise PowlRefusal("POWL-MAX-DEPTH-EXCEEDED", f"{depth}>{MAX_POWL_DEPTH}")
    return depth


def _validate_choice_reachability(node: ChoiceGraph) -> None:
    n = len(node.children)
    succ: list[set[int]] = [set() for _ in range(n)]
    pred: list[set[int]] = [set() for _ in range(n)]
    for edge in node.edges:
        succ[edge.src].add(edge.dst)
        pred[edge.dst].add(edge.src)

    def walk(start: int, graph: list[set[int]]) -> set[int]:
        seen = {start}
        stack = [start]
        while stack:
            cur = stack.pop()
            for nxt in graph[cur] - seen:
                seen.add(nxt)
                stack.append(nxt)
        return seen

    forward = walk(node.start, succ)
    backward = walk(node.end, pred)
    if len(forward) != n or len(backward) != n:
        raise PowlRefusal(
            "POWL-UNREACHABLE-CHOICE-NODE",
            f"forward={sorted(set(range(n)) - forward)},backward={sorted(set(range(n)) - backward)}",
        )
