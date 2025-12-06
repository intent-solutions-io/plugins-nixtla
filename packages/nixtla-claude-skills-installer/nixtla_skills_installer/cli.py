"""
CLI interface for Nixtla Claude Skills installer.

Commands:
    nixtla-skills init    - First-time installation of skills in current project
    nixtla-skills update  - Update existing skills in current project
"""

import sys
import argparse
from pathlib import Path

from .core import (
    locate_skills_source,
    ensure_skills_directory,
    copy_skills_to_project,
    print_installed_skills_summary
)


def cmd_init(args):
    """
    Install Nixtla skills in the current project (first-time setup).

    This command:
    1. Locates the skills source directory
    2. Creates .claude/skills if it doesn't exist
    3. Copies all Nixtla skills to .claude/skills/nixtla-*
    4. Lists installed skills

    Skills are copied locally and persist until explicitly updated or removed.
    """
    print("=" * 60)
    print("🚀 Nixtla Skills Installer - INIT")
    print("=" * 60)
    print()

    project_dir = Path.cwd()
    print(f"📂 Project directory: {project_dir}")
    print()

    try:
        # Locate skills source
        print("🔍 Locating skills source...")
        source_dir = locate_skills_source()
        print()

        # Ensure target directory exists
        print("📁 Preparing target directory...")
        target_dir = ensure_skills_directory(project_dir)
        print()

        # Copy skills
        copied_count = copy_skills_to_project(
            source_dir,
            target_dir,
            force=args.force
        )

        if copied_count > 0:
            print(f"\n✅ Successfully installed {copied_count} Nixtla skills!")

            # List installed skills
            print_installed_skills_summary(project_dir)

            print("\n📝 Next steps:")
            print("   1. Skills are now available in Claude Code")
            print("   2. They will auto-activate when forecasting topics arise")
            print("   3. Update skills with: nixtla-skills update")
            print()

        else:
            print("\n⚠️  No skills were installed.")
            print("   This may be due to:")
            print("   - User cancelled the operation")
            print("   - No Nixtla skills found in source")
            print()

    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    except PermissionError as e:
        print(f"\n❌ Permission error: {e}")
        print("   Try running with appropriate permissions.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


def cmd_update(args):
    """
    Update existing Nixtla skills in the current project.

    This command:
    1. Locates the skills source directory
    2. Checks for existing skills in .claude/skills
    3. Shows preview of new vs existing skills
    4. Prompts for confirmation before overwriting
    5. Updates skills to latest versions

    Existing skill files will be replaced with newer versions from source.
    """
    print("=" * 60)
    print("🔄 Nixtla Skills Installer - UPDATE")
    print("=" * 60)
    print()

    project_dir = Path.cwd()
    print(f"📂 Project directory: {project_dir}")
    print()

    try:
        # Locate skills source
        print("🔍 Locating skills source...")
        source_dir = locate_skills_source()
        print()

        # Ensure target directory exists
        print("📁 Checking target directory...")
        target_dir = ensure_skills_directory(project_dir)
        print()

        # Copy/update skills
        copied_count = copy_skills_to_project(
            source_dir,
            target_dir,
            force=args.force
        )

        if copied_count > 0:
            print(f"\n✅ Successfully updated {copied_count} Nixtla skills!")

            # List installed skills
            print_installed_skills_summary(project_dir)

            print("\n📝 Skills are now up to date!")
            print("   Latest versions copied from source.")
            print()

        else:
            print("\n⚠️  No skills were updated.")
            print("   This may be due to:")
            print("   - User cancelled the operation")
            print("   - No Nixtla skills found in source")
            print()

    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    except PermissionError as e:
        print(f"\n❌ Permission error: {e}")
        print("   Try running with appropriate permissions.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


def create_parser() -> argparse.ArgumentParser:
    """
    Create CLI argument parser.

    Returns:
        Configured ArgumentParser
    """
    parser = argparse.ArgumentParser(
        prog='nixtla-skills',
        description='Install and update Nixtla Claude Skills in your projects',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # First-time install in current project
  nixtla-skills init

  # Update existing skills to latest versions
  nixtla-skills update

  # Force update without confirmation prompts
  nixtla-skills update --force

Per-Project Persistence:
  Skills are installed into .claude/skills/nixtla-* in the current directory.
  They persist there until you run 'nixtla-skills update' or remove them manually.

  This allows different projects to have different skill versions if needed.

For more info: https://github.com/intent-solutions-io/plugins-nixtla
        """
    )

    subparsers = parser.add_subparsers(
        title='commands',
        description='Available commands',
        dest='command',
        required=True
    )

    # Init command
    parser_init = subparsers.add_parser(
        'init',
        help='Install Nixtla skills in current project (first-time setup)',
        description='Install Nixtla Claude Skills in the current project.'
    )
    parser_init.add_argument(
        '--force',
        action='store_true',
        help='Skip confirmation prompts (overwrite existing skills without asking)'
    )
    parser_init.set_defaults(func=cmd_init)

    # Update command
    parser_update = subparsers.add_parser(
        'update',
        help='Update existing Nixtla skills in current project',
        description='Update Nixtla Claude Skills to latest versions.'
    )
    parser_update.add_argument(
        '--force',
        action='store_true',
        help='Skip confirmation prompts (overwrite existing skills without asking)'
    )
    parser_update.set_defaults(func=cmd_update)

    return parser


def main():
    """
    Main CLI entry point.

    Called when user runs: nixtla-skills <command>
    """
    parser = create_parser()
    args = parser.parse_args()

    # Execute command
    args.func(args)


if __name__ == "__main__":
    main()
