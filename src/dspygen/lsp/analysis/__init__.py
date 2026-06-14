"""
Static analysis tools for dspygen/DSPy code.
"""

from .signature_parser import parse_signature, validate_signature, extract_field_names
from .module_index import ModuleIndex, ModuleInfo

__all__ = [
    "parse_signature",
    "validate_signature",
    "extract_field_names",
    "ModuleIndex",
    "ModuleInfo",
]
