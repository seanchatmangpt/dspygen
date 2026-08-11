"""DSPy integration for POWL 2.0."""
from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from dspygen.powl.algebra import ChoiceGraph, PowlNode, PowlRefusal
from dspygen.powl.runtime import ExecutionBound, execute

try:  # algebra remains importable in dependency-minimal verification capsules.
    import dspy as _dspy
except ModuleNotFoundError:  # pragma: no cover - exercised by minimal capsules
    _dspy = None


if _dspy is not None:

    class Powl(_dspy.Module):
        """A DSPy Module whose control-flow topology is an admitted POWL 2.0 graph."""

        def __init__(
            self,
            graph: PowlNode,
            atoms: Mapping[str, Callable[..., Any]],
            *,
            bound: ExecutionBound | None = None,
            choose: Callable[[ChoiceGraph, tuple[int, ...], Mapping[str, Any]], int] | None = None,
        ) -> None:
            super().__init__()
            self.graph = graph
            self.atoms = dict(atoms)
            self.bound = bound or ExecutionBound()
            self.choose = choose

        def forward(self, **kwargs: Any) -> Any:
            context, receipt = execute(
                self.graph,
                self.atoms,
                inputs=kwargs,
                bound=self.bound,
                choose=self.choose,
            )
            return _dspy.Prediction(
                **context,
                powl_receipt_id=receipt.receipt_id,
                powl_receipt=receipt,
            )

else:

    class Powl:  # type: ignore[no-redef]
        def __init__(self, *_: Any, **__: Any) -> None:
            raise PowlRefusal("POWL-DSPY-UNAVAILABLE", "install dspy>=3.3.0")


def install_dspy_extension() -> type[Powl]:
    """Explicitly expose this implementation as ``dspy.Powl`` for this process.

    This is opt-in and refuses to overwrite a different future upstream symbol.
    DSPyGen does not mutate the DSPy namespace merely because it was imported.
    """
    if _dspy is None:
        raise PowlRefusal("POWL-DSPY-UNAVAILABLE", "install dspy>=3.3.0")
    current = getattr(_dspy, "Powl", None)
    if current is not None and current is not Powl:
        raise PowlRefusal("POWL-DSPY-SYMBOL-CONFLICT", repr(current))
    setattr(_dspy, "Powl", Powl)
    return Powl
