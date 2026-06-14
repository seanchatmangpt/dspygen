"""
Shared server state for the dspygen LSP.

Holds the process-wide :class:`~dspygen.lsp.analysis.module_index.ModuleIndex`
singleton so that all providers can import it without circular-import issues.

The index is populated by :func:`build_state` which is called once at startup.
"""

from __future__ import annotations

from .analysis.module_index import ModuleIndex

# Process-wide singleton — providers import ``module_index`` from here.
module_index: ModuleIndex = ModuleIndex()


def build_state(modules_dir: str | None = None) -> None:
    """Populate the module index.  Call this once at server startup."""
    module_index.build(modules_dir)
