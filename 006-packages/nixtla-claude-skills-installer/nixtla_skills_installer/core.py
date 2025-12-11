"""
Core functionality for Nixtla skills installation and updates.

This module handles:
- Locating the skills source directory
- Ensuring target directories exist
- Copying skills to user projects
- Listing installed skills
- Extracting version information from SKILL.md files
"""

import os
import re
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def locate_skills_source() -> Path:
    """
    Locate the Nixtla skills source directory.

    In development mode:
        Looks for skills-pack/.claude/skills relative to this package.
        This assumes the package is installed in editable mode from the repo.

    In packaged mode (TODO):
        Skills should be bundled as package data.
        Use importlib.resources to access bundled skills.
        See: https://docs.python.org/3/library/importlib.resources.html

    Returns:
        Path to skills source directory

    Raises:
        FileNotFoundError: If skills source cannot be located
    """
    # TODO: In packaged mode, use importlib.resources to access bundled skills
    # For now, assume development mode and locate repo root

    # Try to find repo root by walking up from this file
    current = Path(__file__).resolve()

    # Walk up to find 003-skills directory
    for parent in [current] + list(current.parents):
        skills_path = parent / "003-skills" / ".claude" / "skills"
        if skills_path.exists() and skills_path.is_dir():
            print(f"ℹ️  Located skills source: {skills_path}")
            return skills_path

    # If not found, raise error
    raise FileNotFoundError(
        "Could not locate skills source directory.\n"
        "Expected: 003-skills/.claude/skills relative to repo root.\n"
        "\n"
        "Are you running this in development mode from the nixtla repo?\n"
        "If you installed from PyPI, this is a packaging issue (skills not bundled)."
    )


def ensure_skills_directory(project_dir: Path) -> Path:
    """
    Ensure .claude/skills directory exists in the project.

    Args:
        project_dir: Path to project root (typically current working directory)

    Returns:
        Path to .claude/skills directory

    Creates:
        .claude/skills/ if it doesn't exist
    """
    skills_dir = project_dir / ".claude" / "skills"

    if not skills_dir.exists():
        print(f"📁 Creating .claude/skills directory: {skills_dir}")
        skills_dir.mkdir(parents=True, exist_ok=True)
    else:
        print(f"✓ Found existing .claude/skills directory: {skills_dir}")

    return skills_dir


def list_nixtla_skills(directory: Path) -> List[str]:
    """
    List all Nixtla skill directories in the given path.

    Args:
        directory: Path to search for nixtla-* directories

    Returns:
        List of skill names (e.g., ['nixtla-timegpt-lab', 'nixtla-schema-mapper'])
    """
    if not directory.exists():
        return []

    nixtla_skills = []
    for item in directory.iterdir():
        if item.is_dir() and item.name.startswith("nixtla-"):
            nixtla_skills.append(item.name)

    return sorted(nixtla_skills)


def extract_skill_version(skill_dir: Path) -> Optional[str]:
    """
    Extract version from a skill's SKILL.md frontmatter.

    Args:
        skill_dir: Path to skill directory (e.g., .claude/skills/nixtla-timegpt-lab)

    Returns:
        Version string if found (e.g., "0.3.0"), None otherwise
    """
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.exists():
        return None

    try:
        with open(skill_md, "r", encoding="utf-8") as f:
            content = f.read(1000)  # Read first 1000 chars (frontmatter should be near top)

        # Look for version: in YAML frontmatter
        # Matches: version: "0.3.0" or version: 0.3.0
        match = re.search(r'version:\s*["\']?([0-9]+\.[0-9]+\.[0-9]+)["\']?', content)
        if match:
            return match.group(1)

    except Exception:
        pass  # Silently fail if can't read file

    return None


def get_skill_versions(skills_dir: Path, skill_names: List[str]) -> Dict[str, Optional[str]]:
    """
    Get versions for multiple skills.

    Args:
        skills_dir: Directory containing skills
        skill_names: List of skill names

    Returns:
        Dict mapping skill name to version (or None if not found)
    """
    versions = {}
    for skill in skill_names:
        skill_path = skills_dir / skill
        versions[skill] = extract_skill_version(skill_path)
    return versions


def preview_install(source_dir: Path, target_dir: Path) -> Tuple[List[str], List[str], List[str]]:
    """
    Preview what will happen during install/update.

    Args:
        source_dir: Skills source directory
        target_dir: Target .claude/skills directory

    Returns:
        Tuple of (new_skills, existing_skills, all_skills)
        - new_skills: Skills that don't exist in target
        - existing_skills: Skills that already exist (will be overwritten)
        - all_skills: All skills in source
    """
    source_skills = list_nixtla_skills(source_dir)
    target_skills = list_nixtla_skills(target_dir)

    new_skills = [s for s in source_skills if s not in target_skills]
    existing_skills = [s for s in source_skills if s in target_skills]

    return (new_skills, existing_skills, source_skills)


def confirm_overwrite(existing_skills: List[str]) -> bool:
    """
    Prompt user to confirm overwriting existing skills.

    Args:
        existing_skills: List of skill names that will be overwritten

    Returns:
        True if user confirms, False otherwise
    """
    if not existing_skills:
        return True  # Nothing to overwrite

    print(f"\n⚠️  The following skills already exist and will be OVERWRITTEN:")
    for skill in existing_skills:
        print(f"   - {skill}")

    print(f"\nℹ️  Existing files will be replaced with newer versions from source.")
    response = input("\nContinue? (yes/no): ").strip().lower()

    return response in ["yes", "y"]


def copy_skills_to_project(source_dir: Path, target_dir: Path, force: bool = False) -> int:
    """
    Copy Nixtla skills from source to target directory.

    Args:
        source_dir: Skills source directory
        target_dir: Target .claude/skills directory
        force: Skip confirmation prompt if True

    Returns:
        Number of skills copied

    Raises:
        FileNotFoundError: If source directory doesn't exist
        PermissionError: If target directory is not writable
    """
    if not source_dir.exists():
        raise FileNotFoundError(f"Skills source not found: {source_dir}")

    if not target_dir.exists():
        raise FileNotFoundError(f"Target directory not found: {target_dir}")

    # Preview install
    new_skills, existing_skills, all_skills = preview_install(source_dir, target_dir)

    if not all_skills:
        print("⚠️  No Nixtla skills found in source directory!")
        return 0

    # Get version information
    source_versions = get_skill_versions(source_dir, all_skills)
    target_versions = get_skill_versions(target_dir, existing_skills) if existing_skills else {}

    # Show preview
    print(f"\n📊 Install Preview:")
    print(f"   Total skills in source: {len(all_skills)}")
    if new_skills:
        print(f"   New skills: {len(new_skills)}")
        for skill in new_skills:
            version = source_versions.get(skill)
            version_str = f" (v{version})" if version else ""
            print(f"      + {skill}{version_str}")
    if existing_skills:
        print(f"   Existing skills (will overwrite): {len(existing_skills)}")
        for skill in existing_skills:
            old_version = target_versions.get(skill)
            new_version = source_versions.get(skill)
            if old_version and new_version and old_version != new_version:
                print(f"      ↻ {skill} (v{old_version} → v{new_version})")
            elif new_version:
                print(f"      ↻ {skill} (→ v{new_version})")
            else:
                print(f"      ↻ {skill}")

    # Confirm if overwriting existing skills (unless force flag)
    if not force and existing_skills:
        if not confirm_overwrite(existing_skills):
            print("\n❌ Installation cancelled by user.")
            return 0

    # Copy skills
    print(f"\n🚀 Copying skills to {target_dir}...")
    copied_count = 0

    for skill_name in all_skills:
        source_skill = source_dir / skill_name
        target_skill = target_dir / skill_name

        try:
            # Remove existing if present
            if target_skill.exists():
                print(f"   ↻ Updating {skill_name}...")
                shutil.rmtree(target_skill)
            else:
                print(f"   + Installing {skill_name}...")

            # Copy skill directory
            shutil.copytree(source_skill, target_skill)
            copied_count += 1

        except Exception as e:
            print(f"   ❌ Error copying {skill_name}: {e}")
            continue

    return copied_count


def list_installed_skills(project_dir: Path) -> List[str]:
    """
    List all installed Nixtla skills in the project.

    Args:
        project_dir: Path to project root

    Returns:
        List of installed skill names
    """
    skills_dir = project_dir / ".claude" / "skills"

    if not skills_dir.exists():
        return []

    return list_nixtla_skills(skills_dir)


def print_installed_skills_summary(project_dir: Path) -> None:
    """
    Print a summary of installed Nixtla skills with version information.

    Args:
        project_dir: Path to project root
    """
    skills = list_installed_skills(project_dir)

    if not skills:
        print("\n📭 No Nixtla skills installed in this project.")
        print("   Run 'nixtla-skills init' to install.")
        return

    # Get versions
    skills_dir = project_dir / ".claude" / "skills"
    versions = get_skill_versions(skills_dir, skills)

    print(f"\n✅ Installed Nixtla Skills ({len(skills)}):")
    for skill in skills:
        version = versions.get(skill)
        version_str = f" v{version}" if version else ""
        print(f"   - {skill}{version_str}")
        print(f"     Location: .claude/skills/{skill}")

    print(f"\nℹ️  These skills are installed locally in this project.")
    print(f"   They will persist until you run 'nixtla-skills update' or remove them manually.")
