#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def find_skill_root(target: Path) -> Path | None:
    p = target.resolve()
    if p.is_file():
        p = p.parent
    for parent in [p, *p.parents]:
        if (parent / "SKILL.md").exists():
            return parent
    return None


def validate_skill_root(skill_root: Path) -> list[str]:
    missing: list[str] = []

    required_dirs = [
        "agents",
        "assets",
        "references",
        "scripts",
    ]
    for d in required_dirs:
        if not (skill_root / d).exists():
            missing.append(f"missing_dir:{d}")

    required_files = [
        # Core skill definition
        "SKILL.md",
        # Phase prompts (subagents)
        "agents/phase-1-discover.md",
        "agents/phase-2-structural.md",
        "agents/phase-3-behavioral.md",
        "agents/phase-4-verify.md",
        "agents/phase-5-synthesize.md",
        # Procedures (how-to)
        "references/01-discover.md",
        "references/02-structural.md",
        "references/03-behavioral.md",
        "references/04-verify.md",
        "references/05-synthesize.md",
        # Deterministic runner and helpers
        "scripts/run_validator_suite.py",
        "scripts/discover_scope.py",
        "scripts/validate_skill_scaffold.py",
        "scripts/validate_phase_contract.py",
        "scripts/validate_evidence_bundle.py",
        # Check catalog (profiles)
        "scripts/profiles/default.json",
        # Output templates
        "assets/templates/phase-report.md",
    ]
    for f in required_files:
        if not (skill_root / f).exists():
            missing.append(f"missing_file:{f}")

    return missing


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True, help="Skill dir or any path under it")
    args = ap.parse_args()

    target = Path(args.target)
    skill_root = find_skill_root(target)
    if skill_root is None:
        sys.stderr.write(f"skill scaffold: no SKILL.md found under {target}\n")
        return 2

    missing = validate_skill_root(skill_root)
    if missing:
        sys.stderr.write(f"skill scaffold: FAIL ({skill_root})\n")
        for item in missing:
            sys.stderr.write(f"- {item}\n")
        return 1

    sys.stdout.write(f"skill scaffold: OK ({skill_root})\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
