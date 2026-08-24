"""Deterministic, offline-first DSPyGen project construction."""
from __future__ import annotations

import hashlib
import json
import keyword
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Mapping


@dataclass(frozen=True, slots=True)
class ProjectRefusal(ValueError):
    reason: str
    detail: str

    def __str__(self) -> str:
        return f"REFUSED:{self.reason} detail={self.detail}"


@dataclass(frozen=True, slots=True)
class ProjectPlan:
    project_name: str
    package_name: str
    output_dir: str
    author_name: str
    author_email: str
    files: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ProjectReceipt:
    status: str
    plan: ProjectPlan
    file_hashes: Mapping[str, str]

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, sort_keys=True)


def _package_name(project_name: str) -> str:
    candidate = re.sub(r"[^A-Za-z0-9_]+", "_", project_name.strip()).strip("_").lower()
    if not candidate or candidate[0].isdigit() or keyword.iskeyword(candidate):
        raise ProjectRefusal(
            "PROJECT_NAME_INVALID",
            f"cannot derive a Python package from {project_name!r}",
        )
    return candidate


def plan_project(
    project_name: str,
    *,
    output_dir: Path | str = ".",
    author_name: str = "",
    author_email: str = "todo@todo.com",
) -> ProjectPlan:
    project_name = project_name.strip()
    if not project_name or project_name in {".", ".."}:
        raise ProjectRefusal("PROJECT_NAME_INVALID", repr(project_name))
    package_name = _package_name(project_name)
    root = Path(output_dir).expanduser().resolve() / project_name
    files = (
        ".gitignore",
        "README.md",
        "pyproject.toml",
        f"src/{package_name}/__init__.py",
        f"src/{package_name}/modules/__init__.py",
        "tests/test_smoke.py",
    )
    return ProjectPlan(
        project_name=project_name,
        package_name=package_name,
        output_dir=str(root),
        author_name=author_name.strip(),
        author_email=author_email.strip(),
        files=files,
    )


def _project_files(plan: ProjectPlan) -> dict[str, str]:
    author = plan.author_name or "DSPyGen User"
    return {
        ".gitignore": ".venv/\n__pycache__/\n.pytest_cache/\n*.py[cod]\n.env\n",
        "README.md": (
            f"# {plan.project_name}\n\n"
            "Generated offline by DSPyGen. Add model-provider credentials only through "
            "environment variables or an external secret store.\n"
        ),
        "pyproject.toml": f'''[build-system]\nrequires = ["hatchling"]\nbuild-backend = "hatchling.build"\n\n[project]\nname = "{plan.package_name.replace(chr(95), chr(45))}"\nversion = "0.1.0"\ndescription = "DSPyGen project"\nreadme = "README.md"\nrequires-python = ">=3.10"\nauthors = [{{name = {json.dumps(author)}, email = {json.dumps(plan.author_email)}}}]\ndependencies = ["dspygen"]\n\n[tool.pytest.ini_options]\npythonpath = ["src"]\ntestpaths = ["tests"]\n''',
        f"src/{plan.package_name}/__init__.py": '__version__ = "0.1.0"\n',
        f"src/{plan.package_name}/modules/__init__.py": '"""Project DSPy modules."""\n',
        "tests/test_smoke.py": (
            f"def test_package_import():\n"
            f"    import {plan.package_name}\n\n"
            f"    assert {plan.package_name}.__version__ == \"0.1.0\"\n"
        ),
    }


def materialize_project(plan: ProjectPlan, *, force: bool = False) -> ProjectReceipt:
    """Construct a project without network access or package-manager actuation."""

    root = Path(plan.output_dir)
    if root.exists() and any(root.iterdir()) and not force:
        raise ProjectRefusal("PROJECT_EXISTS", str(root))
    root.mkdir(parents=True, exist_ok=True)

    hashes: dict[str, str] = {}
    for relative, content in _project_files(plan).items():
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists() and not force:
            raise ProjectRefusal("PROJECT_FILE_EXISTS", str(destination))
        temporary = destination.with_name(f".{destination.name}.dspygen-tmp")
        data = content.encode("utf-8")
        temporary.write_bytes(data)
        temporary.replace(destination)
        hashes[relative] = hashlib.sha256(data).hexdigest()

    return ProjectReceipt(status="ALIVE", plan=plan, file_hashes=hashes)
