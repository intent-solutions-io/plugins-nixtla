#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GitStatus:
    git_available: bool
    staged: int
    unstaged: int
    untracked: int


def _run_git(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        text=True,
        capture_output=True,
        check=False,
    )


def detect_repo_root(start: Path) -> Path | None:
    p = start.resolve()
    for parent in [p, *p.parents]:
        if (parent / ".git").exists():
            return parent
    return None


def git_status(repo_root: Path) -> GitStatus:
    version = _run_git(["--version"], repo_root)
    if version.returncode != 0:
        return GitStatus(git_available=False, staged=0, unstaged=0, untracked=0)

    porcelain = _run_git(["status", "--porcelain"], repo_root)
    staged = 0
    unstaged = 0
    untracked = 0
    for line in porcelain.stdout.splitlines():
        if not line:
            continue
        if line.startswith("??"):
            untracked += 1
            continue
        if len(line) >= 2:
            if line[0] != " ":
                staged += 1
            if line[1] != " ":
                unstaged += 1
    return GitStatus(git_available=True, staged=staged, unstaged=unstaged, untracked=untracked)


def classify_target(target: Path, repo_root: Path) -> str:
    try:
        rel = target.resolve().relative_to(repo_root.resolve())
    except Exception:
        rel = target

    if (target / "SKILL.md").exists():
        return "skill"
    if "005-plugins" in rel.parts:
        return "plugin"
    if (repo_root / ".git").exists() and target.resolve() == repo_root.resolve():
        return "repo"
    return "unknown"


def main() -> int:
    target = Path(".") if len(sys.argv) < 2 else Path(sys.argv[1])
    repo_root = detect_repo_root(target) or Path.cwd().resolve()

    out = {
        "repo_root": str(repo_root),
        "target": str(target),
        "target_type": classify_target(target, repo_root),
        "git": git_status(repo_root).__dict__,
    }
    sys.stdout.write(json.dumps(out, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
