#!/usr/bin/env python3
"""Execute the independent DSPyGen architecture verifier."""
from __future__ import annotations

import json

from dspygen.architecture.verification import verify


def main() -> int:
    report = verify()
    print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
