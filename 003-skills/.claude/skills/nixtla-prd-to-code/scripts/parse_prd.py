#!/usr/bin/env python3
"""
PRD to Code Parser

Transforms Product Requirements Documents into actionable implementation tasks.
Extracts functional requirements, identifies dependencies, generates task lists.

Usage:
    python parse_prd.py --prd PATH [--output FILE] [--format json|yaml|markdown]

Author: Jeremy Longshore <jeremy@intentsolutions.io>
Version: 1.0.0
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class PRDParser:
    """Parse PRD markdown files and extract implementation tasks."""

    def __init__(self, prd_path: Path):
        self.prd_path = prd_path
        self.content = prd_path.read_text()
        self.plugin_name = self._extract_plugin_name()

    def _extract_plugin_name(self) -> str:
        """Extract plugin name from PRD header."""
        plugin_match = re.search(r"\*\*Plugin:\*\*\s+([a-z0-9-]+)", self.content)
        if plugin_match:
            return plugin_match.group(1)
        return "unknown-plugin"

    def extract_functional_requirements(self) -> List[Dict[str, any]]:
        """Extract all FR-X functional requirements from PRD."""
        requirements = []

        # Find Functional Requirements section
        fr_section_match = re.search(
            r"## Functional Requirements\s*\n(.+?)(?=\n##|\n---|\Z)", self.content, re.DOTALL
        )

        if not fr_section_match:
            return requirements

        fr_content = fr_section_match.group(1)

        # Extract individual FR-X items
        fr_pattern = r"### (FR-(\d+)):\s*(.+?)\n(.+?)(?=\n###|\Z)"
        fr_matches = re.finditer(fr_pattern, fr_content, re.DOTALL)

        for match in fr_matches:
            fr_id = match.group(1)  # e.g., "FR-1"
            fr_number = int(match.group(2))  # e.g., 1
            fr_title = match.group(3).strip()  # e.g., "Cost Input Collection"
            fr_description = match.group(4).strip()

            # Extract sub-items (bullet points)
            sub_items = re.findall(r"^-\s+(.+)$", fr_description, re.MULTILINE)

            requirements.append(
                {
                    "id": fr_id,
                    "number": fr_number,
                    "title": fr_title,
                    "description": fr_description,
                    "sub_items": sub_items,
                    "priority": "P0" if fr_number <= 3 else "P1",  # First 3 are P0
                    "complexity": self._estimate_complexity(sub_items),
                }
            )

        return requirements

    def _estimate_complexity(self, sub_items: List[str]) -> str:
        """Estimate task complexity based on sub-items count."""
        count = len(sub_items)
        if count <= 2:
            return "low"
        elif count <= 4:
            return "medium"
        else:
            return "high"

    def generate_tasks(self) -> List[Dict[str, any]]:
        """Generate implementation tasks from functional requirements."""
        requirements = self.extract_functional_requirements()
        tasks = []

        for i, req in enumerate(requirements):
            # Create main task for requirement
            task_id = f"{self.plugin_name}-{req['id'].lower()}"

            task = {
                "id": task_id,
                "title": f"Implement {req['title']}",
                "description": (
                    req["description"][:200] + "..."
                    if len(req["description"]) > 200
                    else req["description"]
                ),
                "priority": req["priority"],
                "complexity": req["complexity"],
                "functional_requirement": req["id"],
                "dependencies": [],
            }

            # Simple dependency heuristic: tasks depend on previous FR items
            if i > 0:
                prev_req = requirements[i - 1]
                task["dependencies"].append(f"{self.plugin_name}-{prev_req['id'].lower()}")

            tasks.append(task)

            # Create sub-tasks for each bullet point
            for j, sub_item in enumerate(req["sub_items"]):
                sub_task_id = f"{task_id}-{j+1}"
                sub_task = {
                    "id": sub_task_id,
                    "title": sub_item,
                    "description": f"Subtask of {req['title']}: {sub_item}",
                    "priority": req["priority"],
                    "complexity": "low",
                    "functional_requirement": req["id"],
                    "parent_task": task_id,
                    "dependencies": [task_id],  # Depends on parent
                }
                tasks.append(sub_task)

        return tasks

    def extract_nonfunctional_requirements(self) -> List[str]:
        """Extract non-functional requirements (NFRs)."""
        nfrs = []

        # Find Non-Functional Requirements section
        nfr_section_match = re.search(
            r"## Non-Functional Requirements\s*\n(.+?)(?=\n##|\n---|\Z)", self.content, re.DOTALL
        )

        if not nfr_section_match:
            return nfrs

        nfr_content = nfr_section_match.group(1)

        # Extract NFR-X items
        nfr_pattern = r"### (NFR-\d+):\s*(.+?)\n(.+?)(?=\n###|\Z)"
        nfr_matches = re.finditer(nfr_pattern, nfr_content, re.DOTALL)

        for match in nfr_matches:
            nfr_id = match.group(1)
            nfr_title = match.group(2).strip()
            nfrs.append(f"{nfr_id}: {nfr_title}")

        return nfrs


class TaskFormatter:
    """Format tasks into various output formats."""

    @staticmethod
    def to_json(tasks: List[Dict], pretty: bool = True) -> str:
        """Format tasks as JSON."""
        indent = 2 if pretty else None
        return json.dumps({"tasks": tasks}, indent=indent)

    @staticmethod
    def to_yaml(tasks: List[Dict]) -> str:
        """Format tasks as YAML."""
        try:
            import yaml

            return yaml.dump({"tasks": tasks}, default_flow_style=False, sort_keys=False)
        except ImportError:
            raise ImportError("pyyaml required for YAML output. Install: pip install pyyaml")

    @staticmethod
    def to_markdown(tasks: List[Dict], plugin_name: str) -> str:
        """Format tasks as Markdown checklist."""
        md = f"# {plugin_name.replace('-', ' ').title()} - Implementation Plan\n\n"

        # Group by priority
        p0_tasks = [t for t in tasks if t["priority"] == "P0" and "parent_task" not in t]
        p1_tasks = [t for t in tasks if t["priority"] == "P1" and "parent_task" not in t]

        if p0_tasks:
            md += "## Phase 1: Core Features (P0)\n\n"
            for task in p0_tasks:
                md += f"- [ ] **{task['title']}** ({task['complexity']} complexity)\n"
                md += f"  - Requirement: {task['functional_requirement']}\n"
                if task["dependencies"]:
                    md += f"  - Depends on: {', '.join(task['dependencies'])}\n"
                md += "\n"

        if p1_tasks:
            md += "## Phase 2: Additional Features (P1)\n\n"
            for task in p1_tasks:
                md += f"- [ ] **{task['title']}** ({task['complexity']} complexity)\n"
                md += f"  - Requirement: {task['functional_requirement']}\n"
                if task["dependencies"]:
                    md += f"  - Depends on: {', '.join(task['dependencies'])}\n"
                md += "\n"

        return md

    @staticmethod
    def to_todowrite_format(tasks: List[Dict]) -> List[Dict]:
        """Format tasks for TodoWrite tool integration."""
        todos = []
        for task in tasks:
            if "parent_task" in task:
                continue  # Skip sub-tasks for TodoWrite (too granular)

            todos.append(
                {
                    "content": task["title"],
                    "activeForm": f"Implementing {task['title']}",
                    "status": "pending",
                    "metadata": {
                        "priority": task["priority"],
                        "complexity": task["complexity"],
                        "functional_requirement": task["functional_requirement"],
                    },
                }
            )
        return todos


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Transform PRD into implementation tasks")
    parser.add_argument("--prd", type=Path, required=True, help="Path to PRD markdown file")
    parser.add_argument("--output", type=Path, help="Output file path (default: stdout)")
    parser.add_argument(
        "--format",
        choices=["json", "yaml", "markdown", "todowrite"],
        default="json",
        help="Output format (default: json)",
    )
    parser.add_argument("--verbose", action="store_true", help="Print verbose progress information")

    args = parser.parse_args()

    # Validate PRD exists
    if not args.prd.exists():
        print(f"ERROR: PRD file not found: {args.prd}", file=sys.stderr)
        return 1

    try:
        if args.verbose:
            print(f"Parsing PRD: {args.prd}", file=sys.stderr)

        # Parse PRD
        prd_parser = PRDParser(args.prd)
        tasks = prd_parser.generate_tasks()

        if args.verbose:
            print(f"Extracted {len(tasks)} tasks", file=sys.stderr)

        # Format output
        formatter = TaskFormatter()

        if args.format == "json":
            output = formatter.to_json(tasks)
        elif args.format == "yaml":
            output = formatter.to_yaml(tasks)
        elif args.format == "markdown":
            output = formatter.to_markdown(tasks, prd_parser.plugin_name)
        elif args.format == "todowrite":
            todos = formatter.to_todowrite_format(tasks)
            output = json.dumps(todos, indent=2)

        # Write output
        if args.output:
            args.output.write_text(output)
            if args.verbose:
                print(f"Wrote output to: {args.output}", file=sys.stderr)
        else:
            print(output)

        return 0

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        if args.verbose:
            import traceback

            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
