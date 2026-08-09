"""Exact Git-tree observer and Chesterton-fence classifier."""
from __future__ import annotations

import subprocess
from pathlib import Path, PurePosixPath
from typing import Any

import tomllib

from dspygen.architecture.cmd_types import Observation, TreeEntry, content_id, utc_now


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
    )
    return result.stdout.decode("utf-8", errors="surrogateescape")


def _load_policy(root: Path) -> dict[str, Any]:
    path = root / ".specify/cmd/authority.toml"
    if not path.is_file():
        return {
            "default": {
                "semantic_owner": "dspygen-core",
                "operational_owner": "maintainers",
                "mutation_authority": "git",
                "evidence_authority": "cmd-verifier",
                "retirement_dependency": "proof-required",
            },
            "rules": [],
        }
    return tomllib.loads(path.read_text())


def _matches(path: str, pattern: str) -> bool:
    return PurePosixPath(path).match(pattern)


def _classify(path: str, policy: dict[str, Any]) -> tuple[str, dict[str, str]]:
    default = dict(policy.get("default", {}))
    surface = "source"
    for rule in policy.get("rules", []):
        if any(_matches(path, pattern) for pattern in rule.get("patterns", [])):
            default.update({k: str(v) for k, v in rule.items() if k not in {"patterns", "name"}})
            surface = str(rule.get("name", surface))
            break
    return surface, default


def observe(root: Path, freshness_limit_seconds: int = 300) -> Observation:
    root = root.resolve()
    revision = _git(root, "rev-parse", "HEAD").strip()
    tree_digest = _git(root, "rev-parse", "HEAD^{tree}").strip()
    policy = _load_policy(root)
    raw = subprocess.run(
        ["git", "-C", str(root), "ls-tree", "-r", "-z", "--full-tree", "HEAD"],
        check=True,
        capture_output=True,
    ).stdout
    entries: list[TreeEntry] = []
    unresolved: list[str] = []
    for record in raw.split(b"\0"):
        if not record:
            continue
        metadata, path_bytes = record.split(b"\t", 1)
        mode, object_type, object_sha = metadata.decode().split()
        path = path_bytes.decode("utf-8", errors="surrogateescape")
        surface, authority = _classify(path, policy)
        required = (
            "semantic_owner",
            "operational_owner",
            "mutation_authority",
            "evidence_authority",
            "retirement_dependency",
        )
        if any(not authority.get(key) for key in required):
            unresolved.append(path)
        entries.append(
            TreeEntry(
                path=path,
                mode=mode,
                object_type=object_type,
                object_sha=object_sha,
                surface=surface,
                semantic_owner=authority.get("semantic_owner", "UNKNOWN"),
                operational_owner=authority.get("operational_owner", "UNKNOWN"),
                mutation_authority=authority.get("mutation_authority", "UNKNOWN"),
                evidence_authority=authority.get("evidence_authority", "UNKNOWN"),
                retirement_dependency=authority.get("retirement_dependency", "UNKNOWN"),
            )
        )
    paths = tuple(entry.path for entry in entries)
    workflows = tuple(
        sorted(path for path in paths if path.startswith(".github/workflows/") and path.endswith((".yml", ".yaml")))
    )
    packages = tuple(
        sorted(path for path in paths if PurePosixPath(path).name in {"pyproject.toml", "package.json", "Cargo.toml", "go.mod"})
    )
    entry_points = tuple(
        sorted(path for path in paths if path.endswith("_cmd.py") or path in {"src/dspygen/cli.py", "scripts/cmd.py"})
    )
    tokens = {
        "openai": "OpenAI",
        "mqtt": "MQTT",
        "supabase": "Supabase",
        "prefect": "Prefect",
        "mcp": "MCP",
        "http": "HTTP",
        "github": "GitHub",
    }
    lower_paths = "\n".join(paths).lower()
    integrations = tuple(sorted(name for token, name in tokens.items() if token in lower_paths))
    payload = {"revision": revision, "tree": tree_digest, "entries": [entry.__dict__ for entry in entries]}
    return Observation(
        observation_id=content_id("observation", payload),
        subject=str(root),
        revision=revision,
        tree_digest=tree_digest,
        observer_identity="dspygen.cmd.git-object-observer.v1",
        sequence=utc_now(),
        scope=("HEAD",),
        excluded_surfaces=(),
        freshness_limit_seconds=freshness_limit_seconds,
        provenance="git-object-database",
        normalization_policy="git-path-bytes+posix-canonical-v1",
        entries=tuple(entries),
        workflows=workflows,
        packages=packages,
        entry_points=entry_points,
        external_integrations=integrations,
        unresolved=tuple(sorted(unresolved)),
    )


def is_clean(root: Path) -> bool:
    return not _git(root, "status", "--porcelain=v1", "--untracked-files=all").strip()
