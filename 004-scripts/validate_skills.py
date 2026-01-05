#!/usr/bin/env python3
"""
DEPRECATED: Claude Skills Validator (v1)

This repository's source of truth is `004-scripts/validate_skills_v2.py`.
This wrapper is kept for backwards compatibility with older docs/scripts.

Usage:
    python 004-scripts/validate_skills.py [--verbose|-v] [--fail-on-warn]
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    validator = repo_root / "004-scripts" / "validate_skills_v2.py"
    if not validator.exists():
        print(f"ERROR: missing validator: {validator}", file=sys.stderr)
        return 2
    return subprocess.call([sys.executable, str(validator), *sys.argv[1:]], cwd=str(repo_root))


if __name__ == "__main__":
    raise SystemExit(main())
