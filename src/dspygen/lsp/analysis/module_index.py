"""
Module index for dspygen — statically analyses all dspygen modules using `ast`.

Never imports or executes user code.  All analysis is done on the raw source text.
"""

import ast
import os
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from loguru import logger


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class ModuleInfo:
    """Information about a single dspygen module class."""

    name: str
    """Class name, e.g. 'BlogModule'."""

    file_path: str
    """Absolute path to the source file."""

    docstring: str
    """Class-level docstring, or empty string."""

    signature_string: str
    """The most prominent DSPy signature string found in the class, or ''."""

    input_fields: list[str] = field(default_factory=list)
    """Names of input fields derived from the signature string."""

    output_fields: list[str] = field(default_factory=list)
    """Names of output fields derived from the signature string."""


# ---------------------------------------------------------------------------
# AST helpers
# ---------------------------------------------------------------------------


def _get_docstring(node: ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    """Extract the docstring from a class or function node."""
    if (
        node.body
        and isinstance(node.body[0], ast.Expr)
        and isinstance(node.body[0].value, ast.Constant)
        and isinstance(node.body[0].value.value, str)
    ):
        return node.body[0].value.value.strip()
    return ""


def _extract_string_args(call: ast.Call) -> list[str]:
    """Return all string literal positional arguments from a Call node."""
    results: list[str] = []
    for arg in call.args:
        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
            results.append(arg.value)
    return results


def _find_signature_strings_in_class(class_node: ast.ClassDef) -> list[str]:
    """
    Walk the AST of a class body and collect any string arguments passed to
    dspy.Predict / dspy.ChainOfThought that look like signature strings
    (i.e. contain '->').

    Also collect the value of any string-annotated class variable whose name ends
    in 'signature' or 'sig'.
    """
    signatures: list[str] = []

    for node in ast.walk(class_node):
        # dspy.Predict("...") / dspy.ChainOfThought("...")
        if isinstance(node, ast.Call):
            func = node.func
            is_dspy_call = False
            if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
                if func.value.id == "dspy" and func.attr in ("Predict", "ChainOfThought"):
                    is_dspy_call = True
            if is_dspy_call:
                for s in _extract_string_args(node):
                    if "->" in s:
                        signatures.append(s.strip())

    return signatures


def _parse_sig_string(sig: str) -> tuple[list[str], list[str]]:
    """Minimal signature parser to avoid circular imports with signature_parser."""
    if "->" not in sig:
        return [], []
    parts = sig.split("->", 1)
    inputs = [f.strip() for f in parts[0].split(",") if f.strip()]
    outputs = [f.strip() for f in parts[1].split(",") if f.strip()]
    return inputs, outputs


def _base_names(class_node: ast.ClassDef) -> list[str]:
    """Return the simple names of base classes."""
    names: list[str] = []
    for base in class_node.bases:
        if isinstance(base, ast.Name):
            names.append(base.id)
        elif isinstance(base, ast.Attribute):
            names.append(base.attr)
    return names


def _analyse_file(path: Path) -> list[ModuleInfo]:
    """
    Parse *path* with ast and return one ModuleInfo per dspy.Module subclass.
    Returns an empty list on any parse error.
    """
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source, filename=str(path))
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"Could not parse {path}: {exc}")
        return []

    results: list[ModuleInfo] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue

        base_names = _base_names(node)
        # Keep classes that inherit from dspy.Module / Module directly
        if not any(b in ("Module", "dspy.Module") for b in base_names):
            continue

        docstring = _get_docstring(node)
        sig_strings = _find_signature_strings_in_class(node)
        sig_str = sig_strings[0] if sig_strings else ""
        inputs, outputs = _parse_sig_string(sig_str)

        results.append(
            ModuleInfo(
                name=node.name,
                file_path=str(path.resolve()),
                docstring=docstring,
                signature_string=sig_str,
                input_fields=inputs,
                output_fields=outputs,
            )
        )

    return results


# ---------------------------------------------------------------------------
# ModuleIndex
# ---------------------------------------------------------------------------


class ModuleIndex:
    """
    Searchable index of all dspygen modules.

    Built once at startup via :meth:`build` and then cached in memory.
    Thread-safe for reads after initialisation.
    """

    def __init__(self) -> None:
        self._modules: list[ModuleInfo] = []
        self._by_name: dict[str, ModuleInfo] = {}
        self._lock = threading.Lock()
        self._built = False

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def build(self, modules_dir: Optional[str] = None) -> None:
        """
        Scan *modules_dir* (defaults to ``src/dspygen/modules/`` relative to
        the package root) and populate the index.

        Safe to call multiple times — subsequent calls rebuild the index.
        """
        if modules_dir is None:
            # Resolve path relative to this file
            # This file: src/dspygen/lsp/analysis/module_index.py
            # Target:    src/dspygen/modules/
            here = Path(__file__).resolve().parent  # analysis/
            modules_dir = str(here.parent.parent / "modules")

        scan_path = Path(modules_dir)
        if not scan_path.is_dir():
            logger.warning(f"ModuleIndex: modules directory not found: {scan_path}")
            return

        collected: list[ModuleInfo] = []
        for py_file in sorted(scan_path.glob("*.py")):
            if py_file.name == "__init__.py":
                continue
            infos = _analyse_file(py_file)
            collected.extend(infos)

        by_name: dict[str, ModuleInfo] = {m.name: m for m in collected}

        with self._lock:
            self._modules = collected
            self._by_name = by_name
            self._built = True

        logger.info(
            f"ModuleIndex: indexed {len(collected)} modules from {scan_path}"
        )

    # ------------------------------------------------------------------
    # Query API
    # ------------------------------------------------------------------

    def search(self, query: str) -> list[ModuleInfo]:
        """
        Return modules whose name or docstring contains *query* (case-insensitive).
        Results are sorted by name.

        Args:
            query: Search query string.

        Returns:
            List of matching :class:`ModuleInfo` instances.
        """
        q = query.lower()
        with self._lock:
            return sorted(
                (
                    m
                    for m in self._modules
                    if q in m.name.lower() or q in m.docstring.lower()
                ),
                key=lambda m: m.name,
            )

    def get_by_name(self, name: str) -> Optional[ModuleInfo]:
        """
        Look up a module by its exact class name.

        Args:
            name: Exact class name, e.g. ``'BlogModule'``.

        Returns:
            :class:`ModuleInfo` or ``None`` if not found.
        """
        with self._lock:
            return self._by_name.get(name)

    def get_all_signatures(self) -> dict[str, str]:
        """
        Return a mapping of class name → signature string for all indexed modules
        that have a non-empty signature string.

        Returns:
            Dict mapping module name to its signature string.
        """
        with self._lock:
            return {
                m.name: m.signature_string
                for m in self._modules
                if m.signature_string
            }

    def all_modules(self) -> list[ModuleInfo]:
        """Return all indexed modules."""
        with self._lock:
            return list(self._modules)

    def all_names(self) -> list[str]:
        """Return all indexed module class names, sorted."""
        with self._lock:
            return sorted(self._by_name.keys())

    @property
    def is_built(self) -> bool:
        return self._built


# ---------------------------------------------------------------------------
# Module-level singleton built lazily at first import
# ---------------------------------------------------------------------------

_DEFAULT_INDEX: Optional[ModuleIndex] = None
_INDEX_LOCK = threading.Lock()


def get_default_index() -> ModuleIndex:
    """
    Return the process-wide singleton :class:`ModuleIndex`, building it on
    first access.
    """
    global _DEFAULT_INDEX
    with _INDEX_LOCK:
        if _DEFAULT_INDEX is None:
            idx = ModuleIndex()
            idx.build()
            _DEFAULT_INDEX = idx
    return _DEFAULT_INDEX
