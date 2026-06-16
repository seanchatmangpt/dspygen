"""
LSP feature providers for the dspygen language server.
"""

from .completion import register_completion
from .definition import register_definition
from .diagnostics import register_diagnostics
from .hover import register_hover

__all__ = [
    "register_completion",
    "register_hover",
    "register_diagnostics",
    "register_definition",
]
