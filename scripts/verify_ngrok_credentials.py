#!/usr/bin/env python3
"""Fail closed when a tracked ngrok config embeds credential material.

The repository permits ngrok configuration, but credentials must arrive through the
process environment or an external secret store.  This verifier intentionally checks
source text rather than attempting to contact ngrok or inspect any credential value.
"""
from __future__ import annotations

import json
import re
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTHTOKEN = re.compile(r"^\s*authtoken\s*:\s*(?P<value>.*?)\s*$", re.IGNORECASE)
INERT_VALUES = {"", "null", "~", "${NGROK_AUTHTOKEN}", "$NGROK_AUTHTOKEN"}


@dataclass(frozen=True, slots=True)
class Finding:
    path: str
    line: int
    reason: str


def tracked_ngrok_configs() -> tuple[Path, ...]:
    completed = subprocess.run(
        ["git", "ls-files", "-z", "--", "*ngrok*.yml", "*ngrok*.yaml"],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    if completed.returncode != 0:
        raise SystemExit(
            json.dumps(
                {
                    "status": "BUILD_BROKEN",
                    "reason": "GIT_TRACKED_FILE_CENSUS_FAILED",
                    "exit_code": completed.returncode,
                },
                sort_keys=True,
            )
        )
    paths = [ROOT / raw.decode("utf-8") for raw in completed.stdout.split(b"\0") if raw]
    return tuple(sorted(paths))


def inspect(path: Path) -> tuple[Finding, ...]:
    findings: list[Finding] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        match = AUTHTOKEN.match(line)
        if not match:
            continue
        value = match.group("value").strip().strip('"\'')
        if value not in INERT_VALUES:
            findings.append(
                Finding(
                    path=str(path.relative_to(ROOT)),
                    line=line_number,
                    reason="NGROK_AUTHTOKEN_EMBEDDED",
                )
            )
    return tuple(findings)


def main() -> int:
    configs = tracked_ngrok_configs()
    findings = tuple(finding for path in configs for finding in inspect(path))
    payload = {
        "status": "REFUSED" if findings else "ALIVE",
        "policy": "NGROK_CREDENTIALS_EXTERNAL_ONLY",
        "checked_files": [str(path.relative_to(ROOT)) for path in configs],
        "findings": [asdict(finding) for finding in findings],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
