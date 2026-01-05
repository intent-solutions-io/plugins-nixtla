#!/usr/bin/env python3
"""
Bulk Add Enterprise Fields to SKILL.md Files

Automatically adds or updates author and license fields in SKILL.md frontmatter
while preserving existing formatting and content.

Usage:
    python bulk_add_enterprise_fields.py --dry-run        # Preview changes
    python bulk_add_enterprise_fields.py                  # Apply changes
    python bulk_add_enterprise_fields.py --path DIR       # Specific directory

Author: Jeremy Longshore <jeremy@intentsolutions.io>
Version: 1.0.0
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml required. Install: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


# Default enterprise values
DEFAULT_AUTHOR = "Jeremy Longshore <jeremy@intentsolutions.io>"
DEFAULT_LICENSE = "MIT"


class SkillUpdater:
    """Update SKILL.md files with enterprise fields."""

    def __init__(self, dry_run: bool = False, verbose: bool = False):
        self.dry_run = dry_run
        self.verbose = verbose
        self.updated_count = 0
        self.skipped_count = 0
        self.error_count = 0

    def find_skill_files(self, root: Path) -> List[Path]:
        """Find all SKILL.md files, excluding archives and backups."""
        excluded_dirs = {
            "archive",
            "backups",
            "backup",
            ".git",
            "node_modules",
            "__pycache__",
            ".venv",
            "010-archive",
        }
        results = []
        for p in root.rglob("SKILL.md"):
            if p.is_file():
                parts = p.relative_to(root).parts
                # Exclude any path containing backup or archive patterns
                if not any(part in excluded_dirs or "backup" in part.lower() for part in parts):
                    results.append(p)
        return results

    def parse_frontmatter(self, content: str) -> Tuple[Optional[Dict], str, str]:
        """Parse YAML frontmatter from SKILL.md content."""
        fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)

        if not fm_match:
            return None, "", content

        fm_text = fm_match.group(1)
        body = fm_match.group(2)

        try:
            frontmatter = yaml.safe_load(fm_text)
            return frontmatter, fm_text, body
        except yaml.YAMLError as e:
            print(f"YAML parse error: {e}", file=sys.stderr)
            return None, fm_text, body

    def update_frontmatter(self, frontmatter: Dict, author: str, license: str) -> Tuple[Dict, bool]:
        """Update frontmatter with enterprise fields. Returns (updated_fm, changed)."""
        changed = False
        updated = frontmatter.copy()

        # Add or update author
        if "author" not in updated:
            updated["author"] = author
            changed = True
        elif updated["author"] != author:
            # Only update if different
            if self.verbose:
                print(f"  Updating author: {updated['author']} -> {author}")
            updated["author"] = author
            changed = True

        # Add or update license
        if "license" not in updated:
            updated["license"] = license
            changed = True
        elif updated["license"] != license:
            if self.verbose:
                print(f"  Updating license: {updated['license']} -> {license}")
            updated["license"] = license
            changed = True

        return updated, changed

    def reconstruct_skill_file(self, frontmatter: Dict, body: str) -> str:
        """Reconstruct SKILL.md with updated frontmatter."""
        # Ensure proper field order: name, description, allowed-tools, version, author, license
        ordered_fields = ["name", "description", "allowed-tools", "version", "author", "license"]
        ordered_fm = {}

        # Add fields in order
        for field in ordered_fields:
            if field in frontmatter:
                ordered_fm[field] = frontmatter[field]

        # Add any remaining fields
        for key, value in frontmatter.items():
            if key not in ordered_fm:
                ordered_fm[key] = value

        # Generate YAML with proper formatting
        fm_yaml = yaml.dump(
            ordered_fm, default_flow_style=False, sort_keys=False, allow_unicode=True
        )

        # Remove trailing newline from yaml output
        fm_yaml = fm_yaml.rstrip("\n")

        return f"---\n{fm_yaml}\n---\n\n{body}"

    def update_skill_file(
        self, skill_path: Path, author: str = DEFAULT_AUTHOR, license: str = DEFAULT_LICENSE
    ) -> bool:
        """Update a single SKILL.md file. Returns True if updated."""
        try:
            # Get display path (handle both absolute and relative paths)
            try:
                display_path = skill_path.relative_to(Path.cwd())
            except ValueError:
                display_path = skill_path

            content = skill_path.read_text()
            frontmatter, fm_text, body = self.parse_frontmatter(content)

            if frontmatter is None:
                print(f"❌ {display_path}: No valid frontmatter", file=sys.stderr)
                self.error_count += 1
                return False

            # Update frontmatter
            updated_fm, changed = self.update_frontmatter(frontmatter, author, license)

            if not changed:
                if self.verbose:
                    print(f"⏭️  {display_path}: Already has enterprise fields")
                self.skipped_count += 1
                return False

            # Reconstruct file
            new_content = self.reconstruct_skill_file(updated_fm, body)

            if self.dry_run:
                print(f"🔍 {display_path}: Would update (dry-run)")
                if self.verbose:
                    print(f"  Author: {updated_fm.get('author')}")
                    print(f"  License: {updated_fm.get('license')}")
            else:
                skill_path.write_text(new_content)
                print(f"✅ {display_path}: Updated")

            self.updated_count += 1
            return True

        except Exception as e:
            try:
                display_path = skill_path.relative_to(Path.cwd())
            except (ValueError, AttributeError):
                display_path = skill_path
            print(f"❌ {display_path}: Error - {e}", file=sys.stderr)
            self.error_count += 1
            return False

    def update_all_skills(
        self, root: Path, author: str = DEFAULT_AUTHOR, license: str = DEFAULT_LICENSE
    ):
        """Update all SKILL.md files in directory."""
        skill_files = self.find_skill_files(root)

        print(f"Found {len(skill_files)} SKILL.md files")
        if self.dry_run:
            print("DRY-RUN MODE: No files will be modified\n")
        print()

        for skill_file in sorted(skill_files):
            self.update_skill_file(skill_file, author, license)

        print()
        print("=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Total files: {len(skill_files)}")
        print(f"✅ Updated: {self.updated_count}")
        print(f"⏭️  Skipped: {self.skipped_count}")
        print(f"❌ Errors: {self.error_count}")

        if self.dry_run:
            print()
            print("Run without --dry-run to apply changes")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Bulk add enterprise fields to SKILL.md files")
    parser.add_argument(
        "--path",
        type=Path,
        default=Path("003-skills"),
        help="Root directory to search (default: 003-skills)",
    )
    parser.add_argument(
        "--author", default=DEFAULT_AUTHOR, help=f"Author field value (default: {DEFAULT_AUTHOR})"
    )
    parser.add_argument(
        "--license",
        default=DEFAULT_LICENSE,
        help=f"License field value (default: {DEFAULT_LICENSE})",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview changes without modifying files"
    )
    parser.add_argument("--verbose", action="store_true", help="Print verbose progress information")

    args = parser.parse_args()

    if not args.path.exists():
        print(f"ERROR: Path does not exist: {args.path}", file=sys.stderr)
        return 1

    try:
        updater = SkillUpdater(dry_run=args.dry_run, verbose=args.verbose)
        updater.update_all_skills(args.path, args.author, args.license)

        # Return non-zero if errors occurred
        return 1 if updater.error_count > 0 else 0

    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
