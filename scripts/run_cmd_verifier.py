#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
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
args = parser.parse_args()
report = verify_crown(
    args.root,
    exact_head_sha=args.exact_head_sha,
    detached_replay=args.detached_replay,
)
path = write_report(args.root, report, args.output)
print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
print(f"VERIFIER_REPORT={path}")
raise SystemExit(
    0 if report.aggregate_standing in {Standing.ALIVE, Standing.PARTIAL_ALIVE} else 1
)
