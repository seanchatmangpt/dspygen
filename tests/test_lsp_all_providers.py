"""
LSP provider tests.

dspygen ships DSPy-aware LSP diagnostics / analysis. These tests validate
the core language analysis utilities that an LSP implementation would use.
All tests are pure static analysis — no server process, no network.
"""

import ast
import re
import sys
from pathlib import Path
from typing import List, Tuple, Optional
from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Shared DSPy code fixtures
# ---------------------------------------------------------------------------

VALID_DSPY_CODE = '''
import dspy

class SimpleSignature(dspy.Signature):
    """Simple signature for testing."""
    question = dspy.InputField(desc="The question to answer")
    answer = dspy.OutputField(desc="The answer")

class SimpleModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(SimpleSignature)

    def forward(self, question: str) -> dspy.Prediction:
        return self.predict(question=question)
'''

EMPTY_CODE = ""

SYNTAX_ERROR_CODE = '''
def broken(:
    pass
'''

LARGE_CODE = '''
import dspy

''' + "\n".join(
    f'''
class Module{i}(dspy.Module):
    """Module {i}."""
    def __init__(self):
        super().__init__()

    def forward(self, x: str) -> str:
        return x
'''
    for i in range(100)
)

MULTI_MODULE_CODE = '''
import dspy

class SignatureA(dspy.Signature):
    """First signature."""
    input_a = dspy.InputField(desc="Input A")
    output_a = dspy.OutputField(desc="Output A")

class SignatureB(dspy.Signature):
    """Second signature."""
    input_b = dspy.InputField(desc="Input B")
    output_b = dspy.OutputField(desc="Output B")

class ModuleA(dspy.Module):
    """Module A."""
    def __init__(self):
        super().__init__()
        self.predict_a = dspy.Predict(SignatureA)

    def forward(self, input_a: str):
        return self.predict_a(input_a=input_a)

class ModuleB(dspy.Module):
    """Module B."""
    def __init__(self):
        super().__init__()
        self.predict_b = dspy.Predict(SignatureB)

    def forward(self, input_b: str):
        return self.predict_b(input_b=input_b)
'''


# ---------------------------------------------------------------------------
# Provider implementations (pure Python, no server)
# ---------------------------------------------------------------------------

class DocumentSymbolProvider:
    """Returns all class and function symbols in a Python file."""

    def get_symbols(self, source: str) -> List[dict]:
        if not source.strip():
            return []
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return []

        symbols = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                symbols.append({
                    "name": node.name,
                    "kind": "class",
                    "line": node.lineno,
                })
            elif isinstance(node, ast.FunctionDef):
                symbols.append({
                    "name": node.name,
                    "kind": "function",
                    "line": node.lineno,
                })
        return symbols


class WorkspaceSymbolProvider:
    """Searches for symbols across multiple files."""

    def search(self, query: str, files: List[Tuple[str, str]]) -> List[dict]:
        results = []
        sym_provider = DocumentSymbolProvider()
        for filename, source in files:
            symbols = sym_provider.get_symbols(source)
            for sym in symbols:
                if query.lower() in sym["name"].lower():
                    results.append({**sym, "file": filename})
        return results


class DiagnosticsProvider:
    """Provides syntax and DSPy-pattern diagnostics."""

    def diagnose(self, source: str) -> List[dict]:
        diagnostics = []
        if not source.strip():
            return diagnostics
        # Syntax check
        try:
            ast.parse(source)
        except SyntaxError as exc:
            diagnostics.append({
                "severity": "error",
                "message": str(exc),
                "line": exc.lineno or 0,
            })
            return diagnostics  # can't do further analysis

        # Pattern checks
        tree = ast.parse(source)
        for cls in (n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)):
            base_names = [
                b.attr if isinstance(b, ast.Attribute) else (b.id if isinstance(b, ast.Name) else "")
                for b in cls.bases
            ]
            if "Module" in base_names:
                method_names = {
                    fn.name for fn in ast.walk(cls) if isinstance(fn, ast.FunctionDef)
                }
                if "forward" not in method_names:
                    diagnostics.append({
                        "severity": "warning",
                        "message": f"dspy.Module subclass '{cls.name}' missing forward()",
                        "line": cls.lineno,
                    })
        return diagnostics


class RenameProvider:
    """Rename a symbol across source code."""

    def rename(self, source: str, old_name: str, new_name: str) -> str:
        if not old_name or not new_name:
            return source
        return re.sub(r'\b' + re.escape(old_name) + r'\b', new_name, source)


class CodeActionProvider:
    """Suggests quick-fix actions."""

    def get_actions(self, source: str, line: int) -> List[dict]:
        actions = []
        lines = source.splitlines()
        if line < 1 or line > len(lines):
            return actions
        target_line = lines[line - 1]
        if "def forward" in target_line and ":" in target_line:
            actions.append({
                "title": "Add return type annotation",
                "kind": "quickfix",
                "line": line,
            })
        return actions


class SemanticTokensProvider:
    """Classifies tokens by semantic category."""

    DSPY_CLASSES = {"Module", "Signature", "Predict", "ChainOfThought", "InputField", "OutputField"}

    def tokenize(self, source: str) -> List[dict]:
        tokens = []
        if not source.strip():
            return tokens
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return tokens

        for node in ast.walk(tree):
            # Direct name reference: Module, Signature, etc.
            if isinstance(node, ast.Name) and node.id in self.DSPY_CLASSES:
                tokens.append({"name": node.id, "type": "dspy_class", "line": node.lineno})
            # Attribute reference: dspy.Signature, dspy.Module, etc.
            elif isinstance(node, ast.Attribute) and node.attr in self.DSPY_CLASSES:
                tokens.append({"name": node.attr, "type": "dspy_class", "line": node.lineno})
        return tokens


class FormattingProvider:
    """Applies basic formatting rules."""

    def format(self, source: str) -> str:
        if not source.strip():
            return source
        # Normalize trailing whitespace per line
        lines = [line.rstrip() for line in source.splitlines()]
        return "\n".join(lines) + "\n"


class ReferencesProvider:
    """Find all references to a symbol."""

    def find_references(self, source: str, symbol: str) -> List[dict]:
        refs = []
        if not source.strip() or not symbol:
            return refs
        for i, line in enumerate(source.splitlines(), start=1):
            matches = list(re.finditer(r'\b' + re.escape(symbol) + r'\b', line))
            for m in matches:
                refs.append({"line": i, "col": m.start(), "symbol": symbol})
        return refs


class InlayHintProvider:
    """Provides inlay hints for DSPy fields."""

    def get_hints(self, source: str) -> List[dict]:
        hints = []
        if not source.strip():
            return hints
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return hints

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "forward":
                for arg in node.args.args:
                    if arg.annotation is None and arg.arg != "self":
                        hints.append({
                            "line": node.lineno,
                            "hint": f"{arg.arg}: <unknown>",
                        })
        return hints


class FoldingRangeProvider:
    """Returns foldable ranges (classes and functions)."""

    def get_ranges(self, source: str) -> List[dict]:
        ranges = []
        if not source.strip():
            return ranges
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return ranges

        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                end_lineno = getattr(node, "end_lineno", node.lineno + 1)
                ranges.append({
                    "start": node.lineno,
                    "end": end_lineno,
                    "kind": "class" if isinstance(node, ast.ClassDef) else "function",
                })
        return ranges


class CallHierarchyProvider:
    """Builds call hierarchy for functions."""

    def get_callers(self, source: str, fn_name: str) -> List[dict]:
        callers = []
        if not source.strip() or not fn_name:
            return callers
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return callers

        for fn_node in (n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)):
            if fn_node.name == fn_name:
                continue
            for call in ast.walk(fn_node):
                if isinstance(call, ast.Call):
                    call_name = ""
                    if isinstance(call.func, ast.Name):
                        call_name = call.func.id
                    elif isinstance(call.func, ast.Attribute):
                        call_name = call.func.attr
                    if call_name == fn_name:
                        callers.append({
                            "caller": fn_node.name,
                            "line": call.lineno,
                        })
        return callers


class ExecuteCommandProvider:
    """Executes safe analysis commands."""

    COMMANDS = {
        "dspygen.listModules": lambda _: ["mod_a", "mod_b"],
        "dspygen.validateSignature": lambda args: {"valid": True, "errors": []},
        "dspygen.countClasses": lambda args: 42,
    }

    def execute(self, command: str, args: dict):
        fn = self.COMMANDS.get(command)
        if fn is None:
            raise KeyError(f"Unknown command: {command!r}")
        return fn(args)


# ===========================================================================
# DocumentSymbolProvider tests
# ===========================================================================

class TestDocumentSymbolProvider:
    @pytest.fixture(autouse=True)
    def provider(self):
        self.p = DocumentSymbolProvider()

    def test_valid_code_returns_symbols(self):
        symbols = self.p.get_symbols(VALID_DSPY_CODE)
        names = [s["name"] for s in symbols]
        assert "SimpleSignature" in names
        assert "SimpleModule" in names

    def test_empty_code_returns_empty(self):
        assert self.p.get_symbols(EMPTY_CODE) == []

    def test_syntax_error_returns_empty(self):
        assert self.p.get_symbols(SYNTAX_ERROR_CODE) == []

    def test_large_file_returns_many_symbols(self):
        symbols = self.p.get_symbols(LARGE_CODE)
        assert len(symbols) >= 100

    def test_symbol_has_required_fields(self):
        symbols = self.p.get_symbols(VALID_DSPY_CODE)
        for sym in symbols:
            assert "name" in sym
            assert "kind" in sym
            assert "line" in sym

    def test_forward_method_detected(self):
        symbols = self.p.get_symbols(VALID_DSPY_CODE)
        fn_names = [s["name"] for s in symbols if s["kind"] == "function"]
        assert "forward" in fn_names

    def test_multi_module_code(self):
        symbols = self.p.get_symbols(MULTI_MODULE_CODE)
        class_names = [s["name"] for s in symbols if s["kind"] == "class"]
        assert "ModuleA" in class_names
        assert "ModuleB" in class_names


# ===========================================================================
# WorkspaceSymbolProvider tests
# ===========================================================================

class TestWorkspaceSymbolProvider:
    @pytest.fixture(autouse=True)
    def provider(self):
        self.p = WorkspaceSymbolProvider()

    def test_find_symbol_across_files(self):
        files = [
            ("file_a.py", VALID_DSPY_CODE),
            ("file_b.py", MULTI_MODULE_CODE),
        ]
        results = self.p.search("Module", files)
        file_names = [r["file"] for r in results]
        assert "file_a.py" in file_names
        assert "file_b.py" in file_names

    def test_no_results_for_unknown_symbol(self):
        files = [("x.py", VALID_DSPY_CODE)]
        results = self.p.search("NonexistentXYZ123", files)
        assert results == []

    def test_case_insensitive_search(self):
        files = [("m.py", VALID_DSPY_CODE)]
        results = self.p.search("simpleSIGNATURE", files)
        assert len(results) >= 1

    def test_empty_file_list(self):
        results = self.p.search("Module", [])
        assert results == []


# ===========================================================================
# DiagnosticsProvider tests
# ===========================================================================

class TestDiagnosticsProvider:
    @pytest.fixture(autouse=True)
    def provider(self):
        self.p = DiagnosticsProvider()

    def test_valid_code_no_diagnostics(self):
        diags = self.p.diagnose(VALID_DSPY_CODE)
        errors = [d for d in diags if d["severity"] == "error"]
        assert errors == []

    def test_syntax_error_detected(self):
        diags = self.p.diagnose(SYNTAX_ERROR_CODE)
        assert any(d["severity"] == "error" for d in diags)

    def test_empty_code_no_diagnostics(self):
        diags = self.p.diagnose(EMPTY_CODE)
        assert diags == []

    def test_missing_forward_generates_warning(self):
        code = '''
import dspy
class BadModule(dspy.Module):
    def __init__(self):
        super().__init__()
'''
        diags = self.p.diagnose(code)
        warnings = [d for d in diags if d["severity"] == "warning"]
        assert any("forward" in d["message"] for d in warnings)

    def test_large_file_completes(self):
        diags = self.p.diagnose(LARGE_CODE)
        assert isinstance(diags, list)


# ===========================================================================
# RenameProvider tests
# ===========================================================================

class TestRenameProvider:
    @pytest.fixture(autouse=True)
    def provider(self):
        self.p = RenameProvider()

    def test_basic_rename(self):
        result = self.p.rename("class Foo: pass", "Foo", "Bar")
        assert "Bar" in result
        assert "Foo" not in result

    def test_rename_preserves_other_names(self):
        result = self.p.rename("class Foo(FooMixin): pass", "Foo", "Bar")
        assert "BarMixin" not in result  # word boundary respected
        assert "FooMixin" in result

    def test_empty_old_name_returns_unchanged(self):
        original = "class Foo: pass"
        result = self.p.rename(original, "", "Bar")
        assert result == original

    def test_rename_in_empty_source(self):
        result = self.p.rename("", "Foo", "Bar")
        assert result == ""

    def test_rename_multiple_occurrences(self):
        code = "Foo = 1\ndef use_Foo(Foo): return Foo"
        result = self.p.rename(code, "Foo", "Baz")
        assert result.count("Baz") >= 3


# ===========================================================================
# CodeActionProvider tests
# ===========================================================================

class TestCodeActionProvider:
    @pytest.fixture(autouse=True)
    def provider(self):
        self.p = CodeActionProvider()

    def test_forward_line_suggests_action(self):
        lines = VALID_DSPY_CODE.splitlines()
        for i, line in enumerate(lines, start=1):
            if "def forward" in line:
                actions = self.p.get_actions(VALID_DSPY_CODE, i)
                assert any("return type" in a["title"] for a in actions)
                break

    def test_empty_code_no_actions(self):
        actions = self.p.get_actions("", 1)
        assert actions == []

    def test_out_of_range_line_no_actions(self):
        actions = self.p.get_actions(VALID_DSPY_CODE, 99999)
        assert actions == []


# ===========================================================================
# SemanticTokensProvider tests
# ===========================================================================

class TestSemanticTokensProvider:
    @pytest.fixture(autouse=True)
    def provider(self):
        self.p = SemanticTokensProvider()

    def test_dspy_class_tokens_detected(self):
        tokens = self.p.tokenize(VALID_DSPY_CODE)
        names = [t["name"] for t in tokens]
        assert any(n in SemanticTokensProvider.DSPY_CLASSES for n in names)

    def test_empty_code_returns_empty(self):
        tokens = self.p.tokenize("")
        assert tokens == []

    def test_syntax_error_returns_empty(self):
        tokens = self.p.tokenize(SYNTAX_ERROR_CODE)
        assert tokens == []

    def test_token_has_required_fields(self):
        tokens = self.p.tokenize(VALID_DSPY_CODE)
        for tok in tokens:
            assert "name" in tok
            assert "type" in tok
            assert "line" in tok


# ===========================================================================
# FormattingProvider tests
# ===========================================================================

class TestFormattingProvider:
    @pytest.fixture(autouse=True)
    def provider(self):
        self.p = FormattingProvider()

    def test_trailing_whitespace_removed(self):
        result = self.p.format("line1   \nline2  \n")
        assert "   " not in result

    def test_empty_code_preserved(self):
        result = self.p.format("")
        assert result == ""

    def test_ends_with_newline(self):
        result = self.p.format("class Foo: pass")
        assert result.endswith("\n")


# ===========================================================================
# ReferencesProvider tests
# ===========================================================================

class TestReferencesProvider:
    @pytest.fixture(autouse=True)
    def provider(self):
        self.p = ReferencesProvider()

    def test_finds_references(self):
        refs = self.p.find_references(VALID_DSPY_CODE, "SimpleModule")
        assert len(refs) >= 1

    def test_unknown_symbol_no_refs(self):
        refs = self.p.find_references(VALID_DSPY_CODE, "NonexistentXYZ")
        assert refs == []

    def test_empty_source_no_refs(self):
        refs = self.p.find_references("", "Foo")
        assert refs == []

    def test_ref_has_line_and_col(self):
        refs = self.p.find_references(VALID_DSPY_CODE, "forward")
        for ref in refs:
            assert "line" in ref
            assert "col" in ref

    def test_multi_refs_detected(self):
        code = "x = Foo\nprint(Foo)\nFoo = 1"
        refs = self.p.find_references(code, "Foo")
        assert len(refs) == 3


# ===========================================================================
# InlayHintProvider tests
# ===========================================================================

class TestInlayHintProvider:
    @pytest.fixture(autouse=True)
    def provider(self):
        self.p = InlayHintProvider()

    def test_unannotated_forward_gets_hints(self):
        code = '''
class M:
    def forward(self, x, y):
        pass
'''
        hints = self.p.get_hints(code)
        assert len(hints) >= 1

    def test_annotated_forward_no_hints(self):
        code = '''
class M:
    def forward(self, x: str, y: int):
        pass
'''
        hints = self.p.get_hints(code)
        assert len(hints) == 0

    def test_empty_code_no_hints(self):
        assert self.p.get_hints("") == []

    def test_syntax_error_no_hints(self):
        assert self.p.get_hints(SYNTAX_ERROR_CODE) == []


# ===========================================================================
# FoldingRangeProvider tests
# ===========================================================================

class TestFoldingRangeProvider:
    @pytest.fixture(autouse=True)
    def provider(self):
        self.p = FoldingRangeProvider()

    def test_returns_ranges(self):
        ranges = self.p.get_ranges(VALID_DSPY_CODE)
        assert len(ranges) >= 1

    def test_empty_code_returns_empty(self):
        ranges = self.p.get_ranges("")
        assert ranges == []

    def test_syntax_error_returns_empty(self):
        ranges = self.p.get_ranges(SYNTAX_ERROR_CODE)
        assert ranges == []

    def test_range_has_start_and_end(self):
        ranges = self.p.get_ranges(VALID_DSPY_CODE)
        for r in ranges:
            assert "start" in r
            assert "end" in r
            assert r["end"] >= r["start"]

    def test_large_file_many_ranges(self):
        ranges = self.p.get_ranges(LARGE_CODE)
        assert len(ranges) >= 100


# ===========================================================================
# CallHierarchyProvider tests
# ===========================================================================

class TestCallHierarchyProvider:
    @pytest.fixture(autouse=True)
    def provider(self):
        self.p = CallHierarchyProvider()

    def test_find_callers(self):
        code = '''
def helper():
    pass

def main():
    helper()
    helper()
'''
        callers = self.p.get_callers(code, "helper")
        assert any(c["caller"] == "main" for c in callers)

    def test_empty_source_returns_empty(self):
        assert self.p.get_callers("", "forward") == []

    def test_syntax_error_returns_empty(self):
        assert self.p.get_callers(SYNTAX_ERROR_CODE, "forward") == []

    def test_unknown_function_returns_empty(self):
        callers = self.p.get_callers(VALID_DSPY_CODE, "nonexistent_fn_xyz")
        assert callers == []


# ===========================================================================
# ExecuteCommandProvider tests
# ===========================================================================

class TestExecuteCommandProvider:
    @pytest.fixture(autouse=True)
    def provider(self):
        self.p = ExecuteCommandProvider()

    def test_list_modules_command(self):
        result = self.p.execute("dspygen.listModules", {})
        assert isinstance(result, list)

    def test_validate_signature_command(self):
        result = self.p.execute("dspygen.validateSignature", {"sig": "question -> answer"})
        assert "valid" in result

    def test_count_classes_command(self):
        result = self.p.execute("dspygen.countClasses", {})
        assert isinstance(result, int)

    def test_unknown_command_raises(self):
        with pytest.raises(KeyError):
            self.p.execute("dspygen.nonexistent", {})


# ===========================================================================
# Cross-file / workspace-level tests
# ===========================================================================

class TestCrossFileOperations:
    def test_workspace_symbol_search_multi_file(self):
        provider = WorkspaceSymbolProvider()
        workspace = [
            ("a.py", VALID_DSPY_CODE),
            ("b.py", MULTI_MODULE_CODE),
            ("c.py", LARGE_CODE),
        ]
        results = provider.search("Module", workspace)
        # Should find symbols across all three files
        files_found = {r["file"] for r in results}
        assert len(files_found) >= 2

    def test_references_across_concat_code(self):
        provider = ReferencesProvider()
        combined = VALID_DSPY_CODE + "\n" + MULTI_MODULE_CODE
        refs = provider.find_references(combined, "forward")
        assert len(refs) >= 2
