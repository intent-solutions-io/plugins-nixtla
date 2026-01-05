#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--session-dir", required=True, help="reports/<project>/<timestamp> directory")
    args = ap.parse_args()

    session_dir = Path(args.session_dir).expanduser().resolve()
    required_files = [
        session_dir / "summary.json",
        session_dir / "report.md",
    ]
    required_dirs = [
        session_dir / "checks",
    ]

    errors: List[str] = []
    for f in required_files:
        if not f.exists():
            errors.append(f"missing_file:{f}")
        elif f.stat().st_size == 0:
            errors.append(f"empty_file:{f}")
    for d in required_dirs:
        if not d.exists():
            errors.append(f"missing_dir:{d}")

    if (session_dir / "summary.json").exists():
        try:
            summary: Dict[str, Any] = read_json(session_dir / "summary.json")
            if summary.get("status") not in {"complete", "failed"}:
                errors.append("summary.json missing/invalid status")
            checks = summary.get("checks")
            if not isinstance(checks, list) or len(checks) == 0:
                errors.append("summary.json missing/empty checks[]")
        except Exception as e:
            errors.append(f"invalid_summary_json:{e}")

    if errors:
        sys.stderr.write("evidence bundle: FAIL\n")
        for e in errors:
            sys.stderr.write(f"- {e}\n")
        return 1

    sys.stdout.write("evidence bundle: OK\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
