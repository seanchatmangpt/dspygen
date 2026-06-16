"""Parametrized module tests — 10 representative modules × 5 structural checks."""
import ast
from pathlib import Path

import pytest

pytestmark = pytest.mark.slow  # already marked slow, keep it

MODULES_DIR = Path(__file__).parent.parent / "src/dspygen/modules"

# Representative sample — cover different categories
SAMPLE_MODULES = [
    "gen_dspy_module",
    "natural_language_to_sql_module",
    "chatbot_response_generator_module",
    "document_summarizer_module",
    "gen_pydantic_class",
    "mermaid_js_module",
    "cobol_to_python_module",
    "json_module",
    "blog_module",
    "checker_module",
]

SAMPLE_FILES = [
    MODULES_DIR / f"{name}.py"
    for name in SAMPLE_MODULES
    if (MODULES_DIR / f"{name}.py").exists()
]


def _parse(module_file: Path) -> ast.Module:
    """Return parsed AST for a module file."""
    source = module_file.read_text(encoding="utf-8")
    return ast.parse(source)


def _classes(tree: ast.Module):
    return [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]


# ---------------------------------------------------------------------------
# 1. File is valid Python
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("module_file", SAMPLE_FILES, ids=[f.stem for f in SAMPLE_FILES])
def test_module_is_valid_python(module_file: Path):
    """Each sample module must parse as valid Python without SyntaxError."""
    source = module_file.read_text(encoding="utf-8")
    try:
        ast.parse(source)
    except SyntaxError as exc:
        pytest.fail(f"{module_file.name} raised SyntaxError: {exc}")


# ---------------------------------------------------------------------------
# 2. At least one class definition
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("module_file", SAMPLE_FILES, ids=[f.stem for f in SAMPLE_FILES])
def test_module_has_class_definition(module_file: Path):
    """Each sample module must define at least one class."""
    tree = _parse(module_file)
    classes = _classes(tree)
    assert len(classes) >= 1, f"{module_file.name} has no class definitions"


# ---------------------------------------------------------------------------
# 3. forward() method present in at least one class
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("module_file", SAMPLE_FILES, ids=[f.stem for f in SAMPLE_FILES])
def test_module_forward_method_present(module_file: Path):
    """Each sample module must have at least one class containing a forward() method."""
    tree = _parse(module_file)
    for cls_node in _classes(tree):
        method_names = {
            n.name for n in ast.walk(cls_node) if isinstance(n, ast.FunctionDef)
        }
        if "forward" in method_names:
            return  # found it — pass
    pytest.fail(f"{module_file.name}: no class defines a forward() method")


# ---------------------------------------------------------------------------
# 4. Module-level or class-level docstring present
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("module_file", SAMPLE_FILES, ids=[f.stem for f in SAMPLE_FILES])
def test_module_has_docstring(module_file: Path):
    """Each sample module must have a module-level docstring or at least one class docstring."""
    tree = _parse(module_file)
    if ast.get_docstring(tree):
        return  # module-level docstring found
    for cls_node in _classes(tree):
        if ast.get_docstring(cls_node):
            return  # class-level docstring found
    pytest.fail(f"{module_file.name}: no module or class docstring found")


# ---------------------------------------------------------------------------
# 5. No bare pass as the entire body of forward()
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("module_file", SAMPLE_FILES, ids=[f.stem for f in SAMPLE_FILES])
def test_module_no_bare_pass_forward(module_file: Path):
    """forward() methods must not consist solely of a bare 'pass' statement."""
    tree = _parse(module_file)
    for cls_node in _classes(tree):
        for fn_node in ast.walk(cls_node):
            if not isinstance(fn_node, ast.FunctionDef) or fn_node.name != "forward":
                continue
            body = fn_node.body
            # Strip docstring (if any) then check for bare pass
            non_docstring_body = [
                stmt for stmt in body
                if not (
                    isinstance(stmt, ast.Expr)
                    and isinstance(stmt.value, ast.Constant)
                    and isinstance(stmt.value.value, str)
                )
            ]
            if len(non_docstring_body) == 1 and isinstance(non_docstring_body[0], ast.Pass):
                pytest.fail(
                    f"{module_file.name}: {cls_node.name}.forward() is a bare pass"
                )
