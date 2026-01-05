#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        raise ValueError(f"invalid json: {path} ({e})") from e


def require_keys(obj: Dict[str, Any], keys: List[str]) -> List[str]:
    missing: List[str] = []
    for k in keys:
        if k not in obj:
            missing.append(k)
    return missing


def validate_phase_output(data: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    status = data.get("status")
    if status not in {"complete", "failed"}:
        errors.append("status must be 'complete' or 'failed'")

    if status == "failed":
        if not data.get("error"):
            errors.append("failed output must include non-empty 'error'")
        # report_path/partial_work may be absent for hard failures; allow.
        return errors

    missing = require_keys(data, ["status", "report_path"])
    if missing:
        errors.append(f"missing keys: {missing}")
        return errors

    report_path = Path(str(data["report_path"]))
    if not report_path.is_absolute():
        errors.append("report_path must be absolute")
    if not report_path.exists():
        errors.append(f"report_path does not exist: {report_path}")
    elif report_path.stat().st_size == 0:
        errors.append(f"report_path is empty: {report_path}")

    return errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True, help="Path to a phase JSON output file")
    args = ap.parse_args()

    data = read_json(Path(args.json))
    errors = validate_phase_output(data)
    if errors:
        sys.stderr.write("phase contract: FAIL\n")
        for e in errors:
            sys.stderr.write(f"- {e}\n")
        return 1

    sys.stdout.write("phase contract: OK\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
