from __future__ import annotations

import importlib
import sys
import types

import pytest

from dspygen.powl.algebra import (
    Atom,
    ChoiceGraph,
    ChoiceGraphEdge,
    End,
    NodeId,
    OrderEdge,
    PartialOrder,
    PowlRefusal,
    Silent,
    Start,
)
from dspygen.powl.runtime import ExecutionBound, execute


def test_partial_order_canonicalizes_reduction_and_executes_dependencies() -> None:
    graph = PartialOrder(
        children=(Atom("observe"), Atom("reason"), Atom("answer")),
        order=frozenset(
            {
                OrderEdge(NodeId(0), NodeId(1)),
                OrderEdge(NodeId(1), NodeId(2)),
                OrderEdge(NodeId(0), NodeId(2)),
            }
        ),
    )
    assert graph.order == frozenset(
        {OrderEdge(NodeId(0), NodeId(1)), OrderEdge(NodeId(1), NodeId(2))}
    )
    context, receipt = execute(
        graph,
        {
            "observe": lambda **_: {"observation": "O*"},
            "reason": lambda observation, **_: {"reasoning": observation + "->R"},
            "answer": lambda reasoning, **_: {"answer": reasoning + "->A"},
        },
    )
    assert context["answer"] == "O*->R->A"
    assert receipt.executed_atoms == ("observe", "reason", "answer")
    assert receipt.standing == "ALIVE"
    assert receipt.receipt_id.startswith("powl-receipt:")


def test_choice_graph_cycles_are_legal_but_execution_is_bounded() -> None:
    graph = ChoiceGraph(
        children=(Start(), Atom("work"), End()),
        edges=frozenset(
            {
                ChoiceGraphEdge(NodeId(0), NodeId(1)),
                ChoiceGraphEdge(NodeId(1), NodeId(1)),
                ChoiceGraphEdge(NodeId(1), NodeId(2)),
            }
        ),
        start=0,
        end=2,
    )
    selections = iter((1, 1, 2))
    context, receipt = execute(
        graph,
        {"work": lambda **kw: {"count": kw.get("count", 0) + 1}},
        choose=lambda _graph, _enabled, _context: next(selections),
        bound=ExecutionBound(max_atom_calls=8, max_choice_visits=8),
    )
    assert context["count"] == 2
    assert receipt.executed_atoms == ("work", "work")


def test_invalid_partial_order_and_missing_atom_refuse() -> None:
    with pytest.raises(PowlRefusal, match="POWL-CYCLIC-PARTIAL-ORDER"):
        PartialOrder(
            children=(Atom("a"), Atom("b")),
            order=frozenset(
                {OrderEdge(NodeId(0), NodeId(1)), OrderEdge(NodeId(1), NodeId(0))}
            ),
        )
    with pytest.raises(PowlRefusal, match="POWL-MISSING-ATOM"):
        execute(PartialOrder((Atom("a"), Silent())), {})


def test_explicit_extension_manufactures_dspy_powl_without_ambient_mutation(monkeypatch) -> None:
    fake = types.ModuleType("dspy")

    class Module:
        def __call__(self, **kwargs):
            return self.forward(**kwargs)

    class Prediction:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    fake.Module = Module
    fake.Prediction = Prediction
    monkeypatch.setitem(sys.modules, "dspy", fake)
    import dspygen.powl.dspy_module as dm

    dm = importlib.reload(dm)
    assert not hasattr(fake, "Powl")
    cls = dm.install_dspy_extension()
    assert fake.Powl is cls

    graph = PartialOrder((Atom("first"), Atom("second")), frozenset({OrderEdge(NodeId(0), NodeId(1))}))
    program = fake.Powl(
        graph,
        {
            "first": lambda seed, **_: {"x": seed + 1},
            "second": lambda x, **_: {"y": x * 2},
        },
    )
    prediction = program(seed=10)
    assert prediction.y == 22
    assert prediction.powl_receipt_id.startswith("powl-receipt:")


def test_real_dspy_module_surface_when_dspy_is_installed() -> None:
    dspy = pytest.importorskip("dspy")
    import dspygen.powl.dspy_module as dm

    dm = importlib.reload(dm)
    # In a real environment the module is a first-class DSPy program.
    assert issubclass(dm.Powl, dspy.Module)
    assert not hasattr(dspy, "Powl") or dspy.Powl is dm.Powl
    assert dm.install_dspy_extension() is dm.Powl
    assert dspy.Powl is dm.Powl
