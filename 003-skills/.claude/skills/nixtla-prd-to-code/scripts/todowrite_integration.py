#!/usr/bin/env python3
"""
TodoWrite Integration Example

Demonstrates how to use parse_prd.py output with TodoWrite tool in conversation context.
This script shows the integration pattern but requires running in Claude Code conversation.

Usage:
    # In Claude Code conversation context:
    python todowrite_integration.py --prd PATH

Author: Jeremy Longshore <jeremy@intentsolutions.io>
Version: 1.0.0
"""

import argparse
import json
import sys
from pathlib import Path

from parse_prd import PRDParser, TaskFormatter


def demonstrate_todowrite_integration(prd_path: Path):
    """
    Demonstrate TodoWrite integration pattern.

    NOTE: This function shows the pattern but TodoWrite tool is only
    available in Claude Code conversation context, not standalone scripts.
    """
    print("=" * 60)
    print("TodoWrite Integration Example")
    print("=" * 60)
    print()

    # Parse PRD
    parser = PRDParser(prd_path)
    tasks = parser.generate_tasks()

    print(f"Parsed {len(tasks)} tasks from PRD: {prd_path.name}")
    print()

    # Format for TodoWrite
    formatter = TaskFormatter()
    todos = formatter.to_todowrite_format(tasks)

    print(f"Generated {len(todos)} TodoWrite items (excluding sub-tasks)")
    print()

    print("TodoWrite Integration Code:")
    print("-" * 60)
    print("# This code would be used in Claude Code conversation:")
    print()
    print("from TodoWrite import TodoWrite")
    print()
    print("todos = [")
    for i, todo in enumerate(todos[:3]):  # Show first 3 as example
        print(f"    {json.dumps(todo, indent=4)},")
    if len(todos) > 3:
        print(f"    # ... {len(todos) - 3} more todos")
    print("]")
    print()
    print("# Populate TodoWrite tool")
    print("TodoWrite(todos=todos)")
    print()
    print("-" * 60)
    print()

    print("Full TodoWrite JSON output:")
    print(json.dumps(todos, indent=2))


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Demonstrate TodoWrite integration with PRD tasks")
    parser.add_argument("--prd", type=Path, required=True, help="Path to PRD markdown file")

    args = parser.parse_args()

    if not args.prd.exists():
        print(f"ERROR: PRD file not found: {args.prd}", file=sys.stderr)
        return 1

    try:
        demonstrate_todowrite_integration(args.prd)
        return 0

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
