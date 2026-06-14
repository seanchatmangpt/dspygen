"""
LSP feature providers for the dspygen language server.
"""

from .completion import register_completion
from .hover import register_hover
from .diagnostics import register_diagnostics
from .definition import register_definition

__all__ = [
    "register_completion",
    "register_hover",
    "register_diagnostics",
    "register_definition",
]
