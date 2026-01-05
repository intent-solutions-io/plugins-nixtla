#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


@dataclass(frozen=True)
class CheckResult:
    name: str
    command: List[str]
    cwd: str
    exit_code: int
    duration_ms: int
    log_path: str
    phase: str
    severity: str
    status: str


def run_check(
    *,
    name: str,
    command: List[str],
    cwd: Path,
    log_path: Path,
    phase: str,
    severity: str,
    timeout_sec: Optional[int] = None,
    env: Optional[Dict[str, str]] = None,
) -> CheckResult:
    start = time.time()
    try:
        proc = subprocess.run(
            command,
            cwd=str(cwd),
            text=True,
            capture_output=True,
            env=env,
            timeout=timeout_sec,
        )
    except subprocess.TimeoutExpired as e:
        duration_ms = int((time.time() - start) * 1000)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text(
            f"$ {' '.join(command)}\n\n--- TIMEOUT ---\nExceeded {timeout_sec}s\n\n--- PARTIAL STDOUT ---\n{e.stdout or ''}\n\n--- PARTIAL STDERR ---\n{e.stderr or ''}\n",
            encoding="utf-8",
        )
        return CheckResult(
            name=name,
            command=command,
            cwd=str(cwd),
            exit_code=124,
            duration_ms=duration_ms,
            log_path=str(log_path),
            phase=phase,
            severity=severity,
            status="failed",
        )
    duration_ms = int((time.time() - start) * 1000)

    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(
        f"$ {' '.join(command)}\n\n--- STDOUT ---\n{proc.stdout}\n\n--- STDERR ---\n{proc.stderr}\n",
        encoding="utf-8",
    )

    status = "passed" if proc.returncode == 0 else "failed"
    return CheckResult(
        name=name,
        command=command,
        cwd=str(cwd),
        exit_code=int(proc.returncode),
        duration_ms=duration_ms,
        log_path=str(log_path),
        phase=phase,
        severity=severity,
        status=status,
    )


def repo_root_from_target(target: Path) -> Path:
    p = target.resolve()
    for parent in [p, *p.parents]:
        if (parent / ".git").exists():
            return parent
    return Path.cwd().resolve()


def skill_root_from_runner() -> Path:
    # scripts/run_validator_suite.py -> <skill_root>/scripts/run_validator_suite.py
    return Path(__file__).resolve().parent.parent


def utc_timestamp() -> str:
    # Avoid external deps; stable, filesystem-safe.
    return time.strftime("%Y-%m-%d_%H%M%S", time.gmtime())


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _substitute(value: str, mapping: Dict[str, str]) -> str:
    for key, repl in mapping.items():
        value = value.replace("{" + key + "}", repl)
    return value


def _should_run_check(check: Dict[str, Any], flags: Dict[str, Any]) -> bool:
    when = check.get("when")
    if not when:
        return True
    # Minimal ruleset: {"flag": "run_tests", "equals": true}
    flag = when.get("flag")
    equals = when.get("equals")
    if flag is None:
        return True
    return flags.get(flag) == equals


def _sanitize_filename(name: str) -> str:
    return "".join(c if (c.isalnum() or c in "._-") else "_" for c in name)


def load_profile(profile_arg: str) -> Tuple[Dict[str, Any], Path]:
    script_dir = Path(__file__).resolve().parent
    profiles_dir = script_dir / "profiles"

    candidate = Path(profile_arg)
    if candidate.exists():
        return _read_json(candidate), candidate.resolve()

    candidate = profiles_dir / f"{profile_arg}.json"
    if candidate.exists():
        return _read_json(candidate), candidate.resolve()

    # Allow passing "default.json"
    candidate = profiles_dir / profile_arg
    if candidate.exists():
        return _read_json(candidate), candidate.resolve()

    raise FileNotFoundError(f"Profile not found: {profile_arg}")


def list_profiles() -> List[str]:
    script_dir = Path(__file__).resolve().parent
    profiles_dir = script_dir / "profiles"
    if not profiles_dir.exists():
        return []
    return sorted(p.stem for p in profiles_dir.glob("*.json") if p.is_file())


def phase_window(
    phases: List[Dict[str, Any]], start: Optional[str], end: Optional[str]
) -> List[Dict[str, Any]]:
    if not phases:
        return []
    names = [p.get("name") for p in phases]
    start_i = 0 if start is None else names.index(start)
    end_i = len(phases) - 1 if end is None else names.index(end)
    if start_i > end_i:
        raise ValueError("phase window invalid: phase-start occurs after phase-end")
    return phases[start_i : end_i + 1]


def iter_profile_checks(
    profile: Dict[str, Any], *, flags: Dict[str, Any]
) -> Iterable[Tuple[str, Dict[str, Any]]]:
    for phase in profile.get("phases", []):
        phase_name = str(phase.get("name", "unknown"))
        for check in phase.get("checks", []):
            if _should_run_check(check, flags):
                yield phase_name, check


def _run_git(args: List[str], cwd: Path) -> Optional[str]:
    proc = subprocess.run(["git", *args], cwd=str(cwd), text=True, capture_output=True, check=False)
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()


def _env_snapshot(repo_root: Path) -> Dict[str, Any]:
    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "git_sha": _run_git(["rev-parse", "HEAD"], repo_root),
        "git_dirty": bool(_run_git(["status", "--porcelain"], repo_root)),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True, help="Repo root, plugin dir, or skill dir")
    ap.add_argument("--project", required=True, help="Project/run name for reports/<project>/...")
    ap.add_argument("--out", required=True, help="Base output dir for reports")
    ap.add_argument("--run-tests", action="store_true", help="Also run pytest")
    ap.add_argument("--profile", default="default", help="Profile name or path (default: default)")
    ap.add_argument(
        "--list-profiles", action="store_true", help="List available built-in profiles and exit"
    )
    ap.add_argument("--phase-start", default=None, help="Start phase name (inclusive)")
    ap.add_argument("--phase-end", default=None, help="End phase name (inclusive)")
    ap.add_argument(
        "--session-dir",
        default=None,
        help="Use an existing session dir instead of creating a timestamped one",
    )
    ap.add_argument(
        "--resume", action="store_true", help="Skip checks already recorded in state.json"
    )
    ap.add_argument(
        "--fail-on-warn",
        action="store_true",
        help="Treat warn-severity failures as overall failure",
    )
    ap.add_argument(
        "--max-retries", type=int, default=0, help="Retries per failing check (default: 0)"
    )
    args = ap.parse_args()

    if args.list_profiles:
        for name in list_profiles():
            sys.stdout.write(name + "\n")
        return 0

    target = Path(args.target)
    repo_root = repo_root_from_target(target)
    skill_root = skill_root_from_runner()

    stamp = utc_timestamp()
    if args.session_dir:
        run_dir = Path(args.session_dir).expanduser().resolve()
        stamp = run_dir.name
    else:
        out_base = Path(args.out).expanduser()
        run_dir = (out_base / args.project / stamp).resolve()
    logs_dir = run_dir / "checks"

    flags: Dict[str, Any] = {"run_tests": bool(args.run_tests)}
    profile, profile_path = load_profile(args.profile)
    phases_all = profile.get("phases", [])
    phases_selected = phase_window(phases_all, args.phase_start, args.phase_end)
    profile_selected = {**profile, "phases": phases_selected}

    mapping = {
        "repo_root": str(repo_root),
        "target": str(target),
        "session_dir": str(run_dir),
        "skill_root": str(skill_root),
    }

    results: List[CheckResult] = []
    state_path = run_dir / "state.json"
    prior_state: Dict[str, Any] = {}
    if args.resume and state_path.exists():
        prior_state = _read_json(state_path)

    completed_checks = set(prior_state.get("completed_checks", []))

    overall_failed = False
    warnings_failed = False

    run_dir.mkdir(parents=True, exist_ok=True)
    env = _env_snapshot(repo_root)

    for phase_name, check in iter_profile_checks(profile_selected, flags=flags):
        name = str(check["name"])
        severity = str(check.get("severity", "error"))

        if args.resume and name in completed_checks:
            results.append(
                CheckResult(
                    name=name,
                    command=[str(x) for x in check.get("command", [])],
                    cwd=str(check.get("cwd", repo_root)),
                    exit_code=0,
                    duration_ms=0,
                    log_path=str(logs_dir / f"{_sanitize_filename(name)}.log"),
                    phase=phase_name,
                    severity=severity,
                    status="skipped",
                )
            )
            continue

        raw_command = [str(x) for x in check.get("command", [])]
        command = [_substitute(arg, mapping) for arg in raw_command]
        cwd = Path(_substitute(str(check.get("cwd", repo_root)), mapping))
        timeout_sec = check.get("timeout_sec")
        log_path = logs_dir / f"{_sanitize_filename(name)}.log"

        attempts = 0
        result: Optional[CheckResult] = None
        while True:
            result = run_check(
                name=name,
                command=command,
                cwd=cwd,
                log_path=log_path,
                phase=phase_name,
                severity=severity,
                timeout_sec=int(timeout_sec) if timeout_sec is not None else None,
            )
            attempts += 1
            if result.exit_code == 0 or attempts > (1 + int(args.max_retries)):
                break

        results.append(result)

        # State update after each check (checkpointing)
        completed_checks.add(name)
        state = {
            "profile": profile.get("name"),
            "profile_path": str(profile_path),
            "target": str(target),
            "repo_root": str(repo_root),
            "session_dir": str(run_dir),
            "completed_checks": sorted(completed_checks),
        }
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

        if result.exit_code != 0:
            if severity == "error":
                overall_failed = True
            elif severity == "warn":
                warnings_failed = True

    summary = {
        "project": args.project,
        "timestamp": stamp,
        "target": str(target),
        "repo_root": str(repo_root),
        "profile": {"name": profile.get("name"), "path": str(profile_path)},
        "phase_window": {"start": args.phase_start, "end": args.phase_end},
        "flags": flags,
        "environment": env,
        "status": (
            "failed" if (overall_failed or (warnings_failed and args.fail_on_warn)) else "complete"
        ),
        "checks": [
            {
                "name": r.name,
                "phase": r.phase,
                "severity": r.severity,
                "status": r.status,
                "exit_code": r.exit_code,
                "duration_ms": r.duration_ms,
                "cwd": r.cwd,
                "log_path": r.log_path,
                "command": r.command,
            }
            for r in results
        ],
    }

    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    lines = [
        f"# Validation Report — {args.project}",
        "",
        f"- Timestamp (UTC): `{stamp}`",
        f"- Target: `{target}`",
        f"- Repo root: `{repo_root}`",
        f"- Profile: `{profile.get('name')}` (`{profile_path}`)",
        f"- Status: `{summary['status']}`",
        "",
        "## Checks",
    ]
    for r in results:
        lines.append(
            f"- `{r.phase}` / `{r.name}` ({r.severity}): status={r.status} exit={r.exit_code} "
            f"duration_ms={r.duration_ms} log=`{Path(r.log_path).as_posix()}`"
        )

    (run_dir / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Final evidence bundle validation (post-run).
    # Keep this internal so profiles cannot accidentally fail due to ordering.
    required = [run_dir / "summary.json", run_dir / "report.md"]
    checks_dir = run_dir / "checks"
    if any(not p.exists() for p in required) or not checks_dir.exists():
        return 2

    return 1 if summary["status"] != "complete" else 0


if __name__ == "__main__":
    raise SystemExit(main())
