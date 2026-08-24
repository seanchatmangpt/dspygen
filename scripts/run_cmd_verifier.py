#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import unittest
from pathlib import Path

from dspygen.architecture.cmd_types import Standing
from dspygen.architecture.cmd_verifier import verify_crown, write_report

parser = argparse.ArgumentParser()
parser.add_argument("--root", type=Path, default=Path("."))
parser.add_argument("--exact-head-sha", default=os.environ.get("DSPYGEN_EXACT_HEAD_SHA"))
parser.add_argument(
    "--detached-replay",
    action="store_true",
    default=os.environ.get("DSPYGEN_DETACHED_REPLAY") == "1",
)
parser.add_argument("--output", type=Path)
parser.add_argument("--skip-suites", action="store_true")
args = parser.parse_args()
root = args.root.resolve()

if not args.skip_suites:
    suite = unittest.defaultTestLoader.discover(
        str(root / "tests/cmd"),
        pattern="test_*.py",
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)

report = verify_crown(
    root,
    exact_head_sha=args.exact_head_sha,
    detached_replay=args.detached_replay,
)
path = write_report(root, report, args.output)
print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
print(f"VERIFIER_REPORT={path}")
raise SystemExit(
    0 if report.aggregate_standing in {Standing.ALIVE, Standing.PARTIAL_ALIVE} else 1
)
