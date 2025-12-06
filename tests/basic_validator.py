#!/usr/bin/env python3
"""
Basic Repo Structure Validator for Nixtla Claude Plugins

Purpose: Quick sanity check for Nixtla engineers to validate repo health.
Runtime: <1 second
Exit code: 0 on success, non-zero on failure (CI-compatible)

Usage:
    python tests/basic_validator.py

What it checks:
    - Critical directories exist (plugins/, 000-docs/, skills-pack/)
    - Expected plugin directories present
    - Claude Skills present
    - Canonical reference docs present
    - CI workflows present

What it does NOT check:
    - Code quality (linting, types)
    - Test coverage
    - Dependencies installed
    - Plugin functionality

Created: 2025-12-03 (Phase 01)
"""

import sys
from pathlib import Path
from typing import List, Tuple


class ValidationError(Exception):
    """Raised when validation fails."""
    pass


def get_repo_root() -> Path:
    """Get repository root directory."""
    # Assume we're in tests/ directory
    current = Path(__file__).resolve().parent
    repo_root = current.parent

    # Verify this looks like the right repo
    if not (repo_root / "plugins").exists():
        raise ValidationError(
            f"Could not find repo root. Current path: {current}\n"
            f"Expected to find plugins/ directory in parent."
        )

    return repo_root


def check_critical_directories(repo_root: Path) -> Tuple[bool, str]:
    """Check that critical top-level directories exist."""
    required = ["plugins", "000-docs", "skills-pack"]
    missing = []

    for dir_name in required:
        dir_path = repo_root / dir_name
        if not dir_path.exists():
            missing.append(dir_name)

    if missing:
        return False, f"Missing critical directories: {', '.join(missing)}"

    dirs_list = "\n       - ".join(required)
    return True, f"Critical directories present:\n       - {dirs_list}"


def check_plugin_directories(repo_root: Path) -> Tuple[bool, str]:
    """Check that expected plugin directories exist."""
    plugins_dir = repo_root / "plugins"

    if not plugins_dir.exists():
        return False, "plugins/ directory not found"

    # Get all plugin directories (exclude __pycache__, __init__.py, README.md)
    plugin_dirs = [
        d.name for d in plugins_dir.iterdir()
        if d.is_dir() and not d.name.startswith("__") and not d.name.startswith(".")
    ]

    if len(plugin_dirs) == 0:
        return False, "No plugin directories found in plugins/"

    plugins_list = "\n       - ".join(plugin_dirs)
    return True, f"Plugin directories found ({len(plugin_dirs)}):\n       - {plugins_list}"


def check_claude_skills(repo_root: Path) -> Tuple[bool, str]:
    """Check that Claude Skills are present."""
    skills_dir = repo_root / "skills-pack" / ".claude" / "skills"

    if not skills_dir.exists():
        return False, f"Skills directory not found at: {skills_dir}"

    # Get all skill directories (expect names like nixtla-*)
    skill_dirs = [
        d.name for d in skills_dir.iterdir()
        if d.is_dir() and d.name.startswith("nixtla-")
    ]

    if len(skill_dirs) == 0:
        return False, "No Claude Skills found in skills-pack/.claude/skills/"

    # Expected 8 skills based on repo status
    expected_count = 8
    if len(skill_dirs) != expected_count:
        return False, f"Expected {expected_count} skills, found {len(skill_dirs)}"

    skills_list = "\n       - ".join(sorted(skill_dirs))
    return True, f"Claude Skills found ({len(skill_dirs)}):\n       - {skills_list}"


def check_canonical_docs(repo_root: Path) -> Tuple[bool, str]:
    """Check that canonical 6767 reference docs exist."""
    docs_dir = repo_root / "000-docs"

    if not docs_dir.exists():
        return False, "000-docs/ directory not found"

    # Find all files starting with "6767-"
    canonical_docs = [
        f.name for f in docs_dir.iterdir()
        if f.is_file() and f.name.startswith("6767-")
    ]

    if len(canonical_docs) == 0:
        return False, "No canonical 6767 reference docs found"

    # Expected at least 9 canonical docs
    expected_min = 9
    if len(canonical_docs) < expected_min:
        return False, f"Expected at least {expected_min} canonical docs, found {len(canonical_docs)}"

    docs_list = "\n       - ".join(sorted(canonical_docs))
    return True, f"Canonical 6767 reference docs found ({len(canonical_docs)}):\n       - {docs_list}"


def check_ci_workflows(repo_root: Path) -> Tuple[bool, str]:
    """Check that CI workflows are present."""
    workflows_dir = repo_root / ".github" / "workflows"

    if not workflows_dir.exists():
        return False, ".github/workflows/ directory not found"

    # Get all .yml workflow files
    workflow_files = [
        f.name for f in workflows_dir.iterdir()
        if f.is_file() and f.suffix in [".yml", ".yaml"]
    ]

    if len(workflow_files) == 0:
        return False, "No CI workflow files found"

    workflows_list = "\n       - ".join(sorted(workflow_files))
    return True, f"CI workflows present ({len(workflow_files)}):\n       - {workflows_list}"


def run_validation() -> bool:
    """Run all validation checks."""
    print("=" * 40)
    print("Nixtla Repo Structure Validator")
    print("=" * 40)
    print()

    try:
        repo_root = get_repo_root()
    except ValidationError as e:
        print(f"[FAIL] {e}")
        return False

    # Run all checks
    checks = [
        ("Critical directories", check_critical_directories),
        ("Plugin directories", check_plugin_directories),
        ("Claude Skills", check_claude_skills),
        ("Canonical 6767 docs", check_canonical_docs),
        ("CI workflows", check_ci_workflows),
    ]

    all_passed = True

    for check_name, check_func in checks:
        try:
            passed, message = check_func(repo_root)
            if passed:
                print(f"[PASS] {message}")
            else:
                print(f"[FAIL] {check_name}: {message}")
                all_passed = False
        except Exception as e:
            print(f"[ERROR] {check_name}: {e}")
            all_passed = False
        print()

    # Print final result
    print("=" * 40)
    if all_passed:
        print("✅ VALIDATION RESULT: PASS")
        print("=" * 40)
        print()
        print("All critical repo structure checks passed.")
        print("Repo is healthy and ready for development.")
        print()
        print("For deeper validation, run:")
        print("  cd plugins/nixtla-baseline-lab/tests")
        print("  python run_baseline_m4_smoke.py")
    else:
        print("❌ VALIDATION RESULT: FAIL")
        print("=" * 40)
        print()
        print("Some repo structure checks failed.")
        print("Please review the errors above and fix before proceeding.")
        print()
        print("For help, see: tests/README.md")
    print()

    return all_passed


def main():
    """Main entry point."""
    try:
        success = run_validation()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nValidation interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\n[FATAL ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    main()
