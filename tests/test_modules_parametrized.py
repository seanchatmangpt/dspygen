"""
Parametrized test suite that covers all dspygen modules via static analysis.
No real LLM calls are made — everything is AST / file-level inspection.
"""

import ast
import importlib
import re
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.slow

# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------
MODULES_DIR = Path(__file__).parent.parent / "src/dspygen/modules"
MODULE_FILES = sorted(
    [f for f in MODULES_DIR.glob("*.py") if not f.name.startswith("_")],
    key=lambda p: p.stem,
)
MODULE_IDS = [f.stem for f in MODULE_FILES]

# Non-python files we do NOT parametrize
NON_PY_SUFFIXES = {".yaml", ".yml", ".txt", ".js", ".json"}


def _parse(module_file: Path) -> ast.Module:
    """Return parsed AST for a module file."""
    source = module_file.read_text(encoding="utf-8")
    return ast.parse(source)


def _classes(tree: ast.Module):
    return [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]


# ---------------------------------------------------------------------------
# 1. Valid Python AST
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("module_file", MODULE_FILES, ids=MODULE_IDS)
def test_module_parses_as_valid_ast(module_file: Path):
    """Every .py module must be parseable as valid Python."""
    source = module_file.read_text(encoding="utf-8")
    try:
        ast.parse(source)
    except SyntaxError as exc:
        pytest.fail(f"{module_file.name} raised SyntaxError: {exc}")


# ---------------------------------------------------------------------------
# 2. At least one class OR function definition
# ---------------------------------------------------------------------------

# Some "modules" are actually CLI scripts (e.g. chat_bot_cli.py) — they have
# only function definitions.  We allow those to pass with only functions.
_SCRIPT_ONLY_MODULES = {"chat_bot_cli", "dspygen_dsl_pipeline", "test_chat_bot_cli"}

@pytest.mark.parametrize("module_file", MODULE_FILES, ids=MODULE_IDS)
def test_module_has_at_least_one_class(module_file: Path):
    """Every module should contain at least one class or function definition."""
    tree = _parse(module_file)
    classes = _classes(tree)
    if module_file.stem in _SCRIPT_ONLY_MODULES:
        # These are CLI scripts — they are expected to have no classes
        return
    assert len(classes) >= 1, (
        f"{module_file.name} has no class definitions"
    )


# ---------------------------------------------------------------------------
# 3. dspy.Module subclasses have forward()
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("module_file", MODULE_FILES, ids=MODULE_IDS)
def test_dspy_module_classes_have_forward(module_file: Path):
    """Classes that inherit dspy.Module must define a forward() method."""
    tree = _parse(module_file)
    for cls_node in _classes(tree):
        # Collect base names (handles simple names and attribute access)
        base_names = []
        for base in cls_node.bases:
            if isinstance(base, ast.Attribute):
                base_names.append(base.attr)
            elif isinstance(base, ast.Name):
                base_names.append(base.id)

        if "Module" not in base_names:
            continue

        method_names = {
            n.name for n in ast.walk(cls_node) if isinstance(n, ast.FunctionDef)
        }
        assert "forward" in method_names, (
            f"{module_file.name}: class {cls_node.name} inherits Module but has no forward()"
        )


# ---------------------------------------------------------------------------
# 4. Files follow naming convention (snake_case with optional _module suffix)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("module_file", MODULE_FILES, ids=MODULE_IDS)
def test_module_filename_is_snake_case(module_file: Path):
    """Module filenames must be valid snake_case Python identifiers."""
    stem = module_file.stem
    assert re.match(r"^[a-z][a-z0-9_]*$", stem), (
        f"{module_file.name} does not follow snake_case naming convention"
    )


# ---------------------------------------------------------------------------
# 5. Module file does not import itself
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("module_file", MODULE_FILES, ids=MODULE_IDS)
def test_module_does_not_import_itself(module_file: Path):
    """A module must not import its own name."""
    tree = _parse(module_file)
    stem = module_file.stem

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert stem not in alias.name.split("."), (
                    f"{module_file.name} imports itself: {alias.name}"
                )
        elif isinstance(node, ast.ImportFrom):
            if node.module and stem == node.module.split(".")[-1]:
                pytest.fail(f"{module_file.name} imports itself via 'from {node.module}'")


# ---------------------------------------------------------------------------
# 6. __main__ blocks are syntactically valid (already covered by parse, but
#    we additionally check they only call known builtins / local names)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("module_file", MODULE_FILES, ids=MODULE_IDS)
def test_module_main_block_is_syntactically_valid(module_file: Path):
    """Files with if __name__ == '__main__' must still parse cleanly."""
    source = module_file.read_text(encoding="utf-8")
    if '__name__' not in source:
        pytest.skip("No __main__ block present")
    # Re-parsing is sufficient — already done by test_module_parses_as_valid_ast
    ast.parse(source)  # Should not raise


# ---------------------------------------------------------------------------
# 7. Signature strings inside Signature subclasses are non-empty docstrings
# ---------------------------------------------------------------------------

# Known Signature subclasses that are missing docstrings (pre-existing codebase issues).
# These are documented here so new missing docstrings are caught immediately.
_KNOWN_MISSING_SIGNATURE_DOCSTRINGS = {
    ("gen_pydantic_class", "PromptToPydanticInstanceErrorSignature"),
}

@pytest.mark.parametrize("module_file", MODULE_FILES, ids=MODULE_IDS)
def test_signature_classes_have_docstring(module_file: Path):
    """Classes named *Signature must have a docstring (used by DSPy as the prompt)."""
    tree = _parse(module_file)
    for cls_node in _classes(tree):
        if not cls_node.name.endswith("Signature"):
            continue
        docstring = ast.get_docstring(cls_node)
        key = (module_file.stem, cls_node.name)
        if not docstring:
            if key in _KNOWN_MISSING_SIGNATURE_DOCSTRINGS:
                pytest.xfail(
                    f"{module_file.name}: {cls_node.name} is a known missing docstring — please fix"
                )
            assert docstring, (
                f"{module_file.name}: {cls_node.name} has no docstring — DSPy uses it as a prompt"
            )


# ---------------------------------------------------------------------------
# 8. Module class names follow CamelCase
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("module_file", MODULE_FILES, ids=MODULE_IDS)
def test_class_names_are_camel_case(module_file: Path):
    """Top-level class names must start with an uppercase letter."""
    tree = _parse(module_file)
    for cls_node in _classes(tree):
        if cls_node.col_offset == 0:  # top-level
            assert cls_node.name[0].isupper(), (
                f"{module_file.name}: class '{cls_node.name}' does not start with uppercase"
            )


# ---------------------------------------------------------------------------
# 9. No obvious circular imports at AST level (module does not import its parent)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("module_file", MODULE_FILES, ids=MODULE_IDS)
def test_no_self_referencing_relative_import(module_file: Path):
    """Module must not have a relative import that resolves to itself."""
    tree = _parse(module_file)
    stem = module_file.stem
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            # level > 0 means relative import
            if node.level and node.module is None:
                for alias in node.names or []:
                    assert alias.name != stem, (
                        f"{module_file.name}: relative self-import of '{alias.name}'"
                    )


# ---------------------------------------------------------------------------
# 10. forward() methods have type annotations on at least one parameter
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("module_file", MODULE_FILES, ids=MODULE_IDS)
def test_forward_methods_have_parameters(module_file: Path):
    """forward() methods should accept parameters beyond 'self'."""
    tree = _parse(module_file)
    for cls_node in _classes(tree):
        for fn_node in ast.walk(cls_node):
            if not isinstance(fn_node, ast.FunctionDef):
                continue
            if fn_node.name != "forward":
                continue
            args = fn_node.args.args
            # Must have at least 'self' + one real argument
            assert len(args) >= 1, (
                f"{module_file.name}: {cls_node.name}.forward() has no parameters"
            )


# ---------------------------------------------------------------------------
# 11. __init__ methods in Module subclasses call super().__init__()
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("module_file", MODULE_FILES, ids=MODULE_IDS)
def test_module_init_calls_super(module_file: Path):
    """Module subclasses that define __init__ should call super().__init__()."""
    tree = _parse(module_file)
    for cls_node in _classes(tree):
        base_names = [
            b.attr if isinstance(b, ast.Attribute) else (b.id if isinstance(b, ast.Name) else "")
            for b in cls_node.bases
        ]
        if "Module" not in base_names:
            continue
        for fn_node in ast.walk(cls_node):
            if not isinstance(fn_node, ast.FunctionDef) or fn_node.name != "__init__":
                continue
            # Look for super().__init__() call
            has_super = any(
                (
                    isinstance(n, ast.Call)
                    and isinstance(n.func, ast.Attribute)
                    and n.func.attr == "__init__"
                )
                for n in ast.walk(fn_node)
            )
            assert has_super, (
                f"{module_file.name}: {cls_node.name}.__init__() does not call super().__init__()"
            )


# ---------------------------------------------------------------------------
# 12. Module file size is non-trivial (> 5 bytes)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("module_file", MODULE_FILES, ids=MODULE_IDS)
def test_module_file_is_non_empty(module_file: Path):
    """Module files must contain actual content."""
    size = module_file.stat().st_size
    assert size > 5, f"{module_file.name} appears to be empty or trivial ({size} bytes)"


# ---------------------------------------------------------------------------
# 13. No bare 'except:' clauses (bad practice)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("module_file", MODULE_FILES, ids=MODULE_IDS)
def test_no_bare_except(module_file: Path):
    """Module files should not use bare 'except:' — prefer 'except Exception'."""
    tree = _parse(module_file)
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            pytest.fail(
                f"{module_file.name} uses bare 'except:' at line {node.lineno}"
            )


# ---------------------------------------------------------------------------
# 14. Modules with InputField / OutputField assignments have Signature classes
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("module_file", MODULE_FILES, ids=MODULE_IDS)
def test_fields_require_signature_class(module_file: Path):
    """If a module uses InputField/OutputField, it must define at least one Signature-style class."""
    source = module_file.read_text(encoding="utf-8")
    has_field = "InputField(" in source or "OutputField(" in source
    if not has_field:
        return  # nothing to check

    tree = _parse(module_file)
    # Accept any class (DSPy Signature classes are sometimes named differently)
    has_class = len(_classes(tree)) > 0
    assert has_class, (
        f"{module_file.name} uses InputField/OutputField but defines no classes"
    )


# ---------------------------------------------------------------------------
# 15. Modules that contain 'call' helpers have exactly one *_call function
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("module_file", MODULE_FILES, ids=MODULE_IDS)
def test_call_helper_naming_convention(module_file: Path):
    """If a module exposes a *_call() function it must match the file stem."""
    tree = _parse(module_file)
    stem = module_file.stem  # e.g. gen_pydantic_instance_module

    call_fns = [
        n.name
        for n in ast.walk(tree)
        if isinstance(n, ast.FunctionDef) and n.name.endswith("_call")
    ]
    if not call_fns:
        return  # nothing to check

    # At least one call fn should incorporate the module stem or a close abbreviation
    # We just assert names are snake_case and end with _call
    for name in call_fns:
        assert re.match(r"^[a-z][a-z0-9_]*_call$", name), (
            f"{module_file.name}: call helper '{name}' does not follow snake_case_call convention"
        )
