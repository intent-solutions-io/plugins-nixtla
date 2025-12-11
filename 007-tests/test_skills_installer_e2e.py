#!/usr/bin/env python3
"""
Skills Installer End-to-End Test

Purpose: Validate that the Nixtla skills installer works correctly in a fresh project.

This test:
1. Creates a fresh temporary directory
2. Installs the installer package (assumes editable install)
3. Runs 'nixtla-skills init --force' in the temp directory
4. Validates that .claude/skills/nixtla-* structure is created correctly
5. Verifies all expected skills are present with SKILL.md files

Prerequisites:
    pip install -e packages/nixtla-claude-skills-installer

Usage:
    python tests/test_skills_installer_e2e.py

Exit codes:
    0: Success (all checks passed)
    1: Test failure (assertions failed)
    2: Fatal error (unexpected exception)

Created: 2025-12-03 (Phase 02)
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Tuple

# Minimum expected skills (should be at least this many)
# Note: This test dynamically counts skills from source, so it doesn't need updating
MINIMUM_EXPECTED_SKILLS = 8  # At least the original 8 core skills


class TestFailure(Exception):
    """Raised when a test assertion fails."""

    pass


def get_repo_root() -> Path:
    """
    Get repository root directory.

    Returns:
        Path to repo root

    Raises:
        TestFailure: If repo root cannot be found
    """
    # Assume we're in tests/ directory
    current = Path(__file__).resolve().parent
    repo_root = current.parent

    # Verify this looks like the right repo
    if not (repo_root / "005-plugins").exists():
        raise TestFailure(
            f"Could not find repo root. Current path: {current}\n"
            f"Expected to find 005-plugins/ directory in parent."
        )

    return repo_root


def install_package_editable() -> bool:
    """
    Check if nixtla-claude-skills-installer package is installed.

    Returns:
        True if installed, False otherwise
    """
    try:
        result = subprocess.run(
            ["pip", "show", "nixtla-claude-skills-installer"],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode == 0
    except Exception:
        return False


def run_installer_in_temp_dir(temp_dir: Path) -> Tuple[bool, str]:
    """
    Run the installer CLI in a temporary directory.

    Args:
        temp_dir: Path to temporary directory

    Returns:
        Tuple of (success: bool, output: str)
    """
    try:
        # Run installer with --force flag to skip interactive prompts
        result = subprocess.run(
            ["nixtla-skills", "init", "--force"],
            cwd=str(temp_dir),
            capture_output=True,
            text=True,
            check=False,
            timeout=30,  # 30 second timeout
        )

        output = result.stdout + result.stderr
        success = result.returncode == 0

        return (success, output)

    except subprocess.TimeoutExpired:
        return (False, "Installer command timed out after 30 seconds")
    except FileNotFoundError:
        return (False, "nixtla-skills command not found (is package installed?)")
    except Exception as e:
        return (False, f"Unexpected error running installer: {e}")


def get_source_skills_count() -> int:
    """Get count of skills from source directory."""
    try:
        repo_root = get_repo_root()
        source_skills_dir = repo_root / "003-skills" / ".claude" / "skills"
        if not source_skills_dir.exists():
            return 0
        skills = [
            d.name
            for d in source_skills_dir.iterdir()
            if d.is_dir() and d.name.startswith("nixtla-")
        ]
        return len(skills)
    except Exception:
        return MINIMUM_EXPECTED_SKILLS


def validate_skills_structure(temp_dir: Path) -> List[str]:
    """
    Validate that .claude/skills/ structure is correct.

    Args:
        temp_dir: Path to temporary directory

    Returns:
        List of validation errors (empty if all checks pass)

    Checks:
        - .claude directory exists
        - .claude/skills directory exists
        - Skills match source count
        - Each skill has SKILL.md file
    """
    errors = []

    # Check .claude directory
    claude_dir = temp_dir / ".claude"
    if not claude_dir.exists():
        errors.append(".claude directory was not created")
        return errors  # Can't continue without this

    if not claude_dir.is_dir():
        errors.append(".claude exists but is not a directory")
        return errors

    # Check .claude/skills directory
    skills_dir = claude_dir / "skills"
    if not skills_dir.exists():
        errors.append(".claude/skills directory was not created")
        return errors

    if not skills_dir.is_dir():
        errors.append(".claude/skills exists but is not a directory")
        return errors

    # Find all nixtla-* skill directories
    installed_skills = [
        d.name
        for d in skills_dir.iterdir()
        if d.is_dir() and d.name.startswith("nixtla-")
    ]

    # Check count
    if len(installed_skills) == 0:
        errors.append("No Nixtla skills were installed")
        return errors

    # Get expected count from source
    expected_count = get_source_skills_count()
    if len(installed_skills) < MINIMUM_EXPECTED_SKILLS:
        errors.append(
            f"Expected at least {MINIMUM_EXPECTED_SKILLS} skills, found {len(installed_skills)}"
        )
    elif len(installed_skills) != expected_count:
        errors.append(
            f"Expected {expected_count} skills (from source), found {len(installed_skills)}: "
            f"{', '.join(sorted(installed_skills))}"
        )

    # Check that each installed skill has SKILL.md
    for skill_name in installed_skills:
        skill_dir = skills_dir / skill_name
        skill_md = skill_dir / "SKILL.md"

        if not skill_md.exists():
            errors.append(f"Skill {skill_name} missing SKILL.md file")
        elif not skill_md.is_file():
            errors.append(f"Skill {skill_name} has SKILL.md but it's not a file")

    return errors


def run_e2e_test() -> bool:
    """
    Run the complete E2E test.

    Returns:
        True if test passes, False otherwise

    Raises:
        TestFailure: If test fails with specific reason
    """
    print("=" * 40)
    print("Nixtla Skills Installer E2E Test")
    print("=" * 40)
    print()

    # Step 1: Locate repo root
    print("[STEP 1/4] Locating repository root...")
    try:
        repo_root = get_repo_root()
        print(f"✓ Repo root: {repo_root}")
    except TestFailure as e:
        print(f"✗ Failed: {e}")
        raise
    print()

    # Step 2: Verify installer package is installed
    print("[STEP 2/4] Verifying installer package...")
    if not install_package_editable():
        print("✗ Package 'nixtla-claude-skills-installer' is not installed")
        print()
        print("Please install the package first:")
        print("  pip install -e 006-packages/nixtla-claude-skills-installer")
        print()
        raise TestFailure("Installer package not installed")
    print("✓ Package 'nixtla-claude-skills-installer' is installed")
    print()

    # Step 3: Run installer in temp directory
    print("[STEP 3/4] Running installer in temp directory...")
    with tempfile.TemporaryDirectory() as temp_dir_str:
        temp_dir = Path(temp_dir_str)
        print(f"✓ Created temp directory: {temp_dir}")

        success, output = run_installer_in_temp_dir(temp_dir)

        if not success:
            print(f"✗ Installer failed with output:")
            print()
            print(output)
            print()
            raise TestFailure("Installer command failed")

        print(f"✓ Installer executed successfully (exit code 0)")
        print()

        # Step 4: Validate structure
        print("[STEP 4/4] Validating skills structure...")

        # Check .claude directory
        if (temp_dir / ".claude").exists():
            print("✓ .claude directory exists")
        else:
            print("✗ .claude directory not created")
            raise TestFailure(".claude directory missing")

        # Check .claude/skills directory
        if (temp_dir / ".claude" / "skills").exists():
            print("✓ .claude/skills directory exists")
        else:
            print("✗ .claude/skills directory not created")
            raise TestFailure(".claude/skills directory missing")

        # Find installed skills
        skills_dir = temp_dir / ".claude" / "skills"
        installed_skills = sorted(
            [
                d.name
                for d in skills_dir.iterdir()
                if d.is_dir() and d.name.startswith("nixtla-")
            ]
        )

        expected_count = get_source_skills_count()
        if len(installed_skills) == expected_count:
            print(f"✓ Found {len(installed_skills)} Nixtla skills:")
            for skill in installed_skills:
                print(f"   - {skill}")
        else:
            print(
                f"✗ Expected {expected_count} skills, found {len(installed_skills)}"
            )
            raise TestFailure("Wrong number of skills installed")

        # Validate detailed structure
        errors = validate_skills_structure(temp_dir)

        if errors:
            print()
            print("✗ Validation errors:")
            for error in errors:
                print(f"   - {error}")
            print()
            raise TestFailure(f"Structure validation failed: {len(errors)} errors")

        print()
        print(f"✓ All {len(installed_skills)} skills have SKILL.md files")
        print()

    # All checks passed
    expected_count = get_source_skills_count()
    print("=" * 40)
    print("✅ E2E TEST RESULT: PASS")
    print("=" * 40)
    print()
    print("All checks passed!")
    print(f"Installer successfully installed {expected_count} Nixtla skills.")
    print()

    return True


def main():
    """
    Main entry point.

    Exit codes:
        0: Success
        1: Test failure
        2: Fatal error
    """
    try:
        success = run_e2e_test()
        sys.exit(0 if success else 1)

    except TestFailure as e:
        print()
        print("=" * 40)
        print("❌ E2E TEST RESULT: FAIL")
        print("=" * 40)
        print()
        print(f"Test failed: {e}")
        print()
        print("See tests/README.md for troubleshooting.")
        print()
        sys.exit(1)

    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(130)

    except Exception as e:
        print()
        print("=" * 40)
        print("❌ E2E TEST RESULT: FATAL ERROR")
        print("=" * 40)
        print()
        print(f"Unexpected error: {e}")
        print()
        import traceback

        traceback.print_exc()
        print()
        sys.exit(2)


if __name__ == "__main__":
    main()
