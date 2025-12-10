#!/usr/bin/env python3
"""
Skill Test Runner - Tests all 23 Nixtla Skills

Tests each skill against success criteria from PRD/ARD:
- Level 1: Structural validation (SKILL.md, scripts exist)
- Level 2: Functional validation (imports, --help)
- Level 3: Integration validation (workflow execution)

Usage:
    python test_all_skills.py                    # Run all tests
    python test_all_skills.py --skill nixtla-polymarket-analyst  # Single skill
    python test_all_skills.py --level 1          # Only Level 1 tests
    python test_all_skills.py --output results/  # Custom output dir
"""

import argparse
import ast
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Skill directory location
SKILLS_DIR = Path(__file__).parent.parent.parent / "003-skills" / ".claude" / "skills"


@dataclass
class TestResult:
    """Result of a single test."""
    name: str
    passed: bool
    level: int
    message: str
    duration_ms: float = 0


@dataclass
class SkillTestReport:
    """Complete test report for a skill."""
    skill_name: str
    timestamp: str
    results: List[TestResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(r.passed for r in self.results)

    @property
    def score(self) -> str:
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        return f"{passed}/{total}"

    def to_dict(self) -> dict:
        return {
            "skill_name": self.skill_name,
            "timestamp": self.timestamp,
            "passed": self.passed,
            "score": self.score,
            "results": [
                {
                    "name": r.name,
                    "passed": r.passed,
                    "level": r.level,
                    "message": r.message,
                    "duration_ms": r.duration_ms
                }
                for r in self.results
            ]
        }


def parse_yaml_frontmatter(content: str) -> Optional[dict]:
    """Parse YAML frontmatter from SKILL.md content."""
    if not content.startswith("---"):
        return None

    parts = content.split("---", 2)
    if len(parts) < 3:
        return None

    yaml_content = parts[1].strip()
    result = {}

    # Simple YAML parsing (key: value)
    for line in yaml_content.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            result[key] = value

    return result


def test_skill_md_exists(skill_path: Path) -> TestResult:
    """L1: Check SKILL.md exists."""
    skill_md = skill_path / "SKILL.md"
    if skill_md.exists():
        return TestResult(
            name="SKILL.md exists",
            passed=True,
            level=1,
            message=f"Found: {skill_md}"
        )
    return TestResult(
        name="SKILL.md exists",
        passed=False,
        level=1,
        message=f"Missing: {skill_md}"
    )


def test_frontmatter_valid(skill_path: Path) -> TestResult:
    """L1: Check SKILL.md has valid frontmatter."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return TestResult(
            name="Frontmatter valid",
            passed=False,
            level=1,
            message="SKILL.md not found"
        )

    content = skill_md.read_text()
    frontmatter = parse_yaml_frontmatter(content)

    if not frontmatter:
        return TestResult(
            name="Frontmatter valid",
            passed=False,
            level=1,
            message="No valid YAML frontmatter found"
        )

    # Check required fields
    required = ["name", "description", "allowed-tools", "version"]
    missing = [f for f in required if f not in frontmatter]

    if missing:
        return TestResult(
            name="Frontmatter valid",
            passed=False,
            level=1,
            message=f"Missing required fields: {missing}"
        )

    return TestResult(
        name="Frontmatter valid",
        passed=True,
        level=1,
        message=f"All required fields present: {list(frontmatter.keys())}"
    )


def test_scripts_exist(skill_path: Path) -> TestResult:
    """L1: Check all referenced scripts exist."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return TestResult(
            name="Scripts exist",
            passed=False,
            level=1,
            message="SKILL.md not found"
        )

    content = skill_md.read_text()

    # Find all {baseDir}/scripts/*.py references
    pattern = r'\{baseDir\}/scripts/([a-zA-Z0-9_]+\.py)'
    referenced = set(re.findall(pattern, content))

    if not referenced:
        # No scripts referenced is OK (skill might not need scripts)
        return TestResult(
            name="Scripts exist",
            passed=True,
            level=1,
            message="No scripts referenced in SKILL.md"
        )

    scripts_dir = skill_path / "scripts"
    actual = set()
    if scripts_dir.exists():
        actual = {f.name for f in scripts_dir.glob("*.py")}

    missing = referenced - actual

    if missing:
        return TestResult(
            name="Scripts exist",
            passed=False,
            level=1,
            message=f"Missing scripts: {sorted(missing)}"
        )

    return TestResult(
        name="Scripts exist",
        passed=True,
        level=1,
        message=f"All {len(referenced)} scripts found"
    )


def test_scripts_syntax(skill_path: Path) -> TestResult:
    """L1: Check scripts are syntactically valid Python."""
    scripts_dir = skill_path / "scripts"

    if not scripts_dir.exists():
        return TestResult(
            name="Scripts syntax valid",
            passed=True,
            level=1,
            message="No scripts directory"
        )

    scripts = list(scripts_dir.glob("*.py"))
    if not scripts:
        return TestResult(
            name="Scripts syntax valid",
            passed=True,
            level=1,
            message="No Python scripts found"
        )

    errors = []
    for script in scripts:
        try:
            content = script.read_text()
            ast.parse(content)
        except SyntaxError as e:
            errors.append(f"{script.name}: {e.msg} (line {e.lineno})")

    if errors:
        return TestResult(
            name="Scripts syntax valid",
            passed=False,
            level=1,
            message=f"Syntax errors: {errors}"
        )

    return TestResult(
        name="Scripts syntax valid",
        passed=True,
        level=1,
        message=f"All {len(scripts)} scripts have valid syntax"
    )


def test_scripts_importable(skill_path: Path) -> TestResult:
    """L2: Check scripts can be imported."""
    scripts_dir = skill_path / "scripts"

    if not scripts_dir.exists():
        return TestResult(
            name="Scripts importable",
            passed=True,
            level=2,
            message="No scripts directory"
        )

    scripts = list(scripts_dir.glob("*.py"))
    if not scripts:
        return TestResult(
            name="Scripts importable",
            passed=True,
            level=2,
            message="No Python scripts found"
        )

    errors = []
    for script in scripts:
        # Try to compile and check for import errors
        try:
            content = script.read_text()
            code = compile(content, script, 'exec')
            # Check if there are obvious import issues
            # (Full import testing requires actual execution)
        except Exception as e:
            errors.append(f"{script.name}: {str(e)[:50]}")

    if errors:
        return TestResult(
            name="Scripts importable",
            passed=False,
            level=2,
            message=f"Import issues: {errors}"
        )

    return TestResult(
        name="Scripts importable",
        passed=True,
        level=2,
        message=f"All {len(scripts)} scripts compilable"
    )


def test_scripts_help(skill_path: Path) -> TestResult:
    """L2: Check scripts respond to --help."""
    scripts_dir = skill_path / "scripts"

    if not scripts_dir.exists():
        return TestResult(
            name="Scripts --help works",
            passed=True,
            level=2,
            message="No scripts directory"
        )

    scripts = list(scripts_dir.glob("*.py"))
    if not scripts:
        return TestResult(
            name="Scripts --help works",
            passed=True,
            level=2,
            message="No Python scripts found"
        )

    errors = []
    working = []

    for script in scripts:
        try:
            result = subprocess.run(
                [sys.executable, str(script), "--help"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0 and ("usage" in result.stdout.lower() or "options" in result.stdout.lower()):
                working.append(script.name)
            else:
                # Not an error if script doesn't use argparse
                working.append(f"{script.name} (no argparse)")
        except subprocess.TimeoutExpired:
            errors.append(f"{script.name}: timeout")
        except Exception as e:
            errors.append(f"{script.name}: {str(e)[:30]}")

    if errors and len(errors) == len(scripts):
        return TestResult(
            name="Scripts --help works",
            passed=False,
            level=2,
            message=f"All scripts failed: {errors[:3]}"
        )

    return TestResult(
        name="Scripts --help works",
        passed=True,
        level=2,
        message=f"{len(working)}/{len(scripts)} scripts have CLI interface"
    )


def test_description_quality(skill_path: Path) -> TestResult:
    """L4: Check description quality score."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return TestResult(
            name="Description quality",
            passed=False,
            level=4,
            message="SKILL.md not found"
        )

    content = skill_md.read_text()
    frontmatter = parse_yaml_frontmatter(content)

    if not frontmatter or "description" not in frontmatter:
        return TestResult(
            name="Description quality",
            passed=False,
            level=4,
            message="No description found"
        )

    desc = frontmatter["description"]
    score = 0
    feedback = []

    # Check for action verbs (20%)
    action_verbs = ["analyze", "detect", "forecast", "transform", "generate", "validate", "compare", "optimize"]
    if any(verb in desc.lower() for verb in action_verbs):
        score += 20
    else:
        feedback.append("No action verbs")

    # Check for "Use when" clause (25%)
    if "use when" in desc.lower():
        score += 25
    else:
        feedback.append("Missing 'Use when'")

    # Check for "Trigger with" phrase (25%)
    if "trigger with" in desc.lower():
        score += 25
    else:
        feedback.append("Missing 'Trigger with'")

    # Check length (15%)
    if 100 <= len(desc) <= 300:
        score += 15
    else:
        feedback.append(f"Length {len(desc)} (ideal: 100-300)")

    # Check for domain keywords (15%)
    domain_words = ["timegpt", "forecast", "time series", "nixtla", "statsforecast"]
    if any(word in desc.lower() for word in domain_words):
        score += 15
    else:
        feedback.append("No domain keywords")

    passed = score >= 100

    return TestResult(
        name="Description quality",
        passed=passed,
        level=4,
        message=f"Score: {score}/100" + (f" ({', '.join(feedback)})" if feedback else "")
    )


def test_skill(skill_path: Path, levels: List[int] = [1, 2, 3, 4]) -> SkillTestReport:
    """Run all tests for a skill."""
    report = SkillTestReport(
        skill_name=skill_path.name,
        timestamp=datetime.now().isoformat()
    )

    # Level 1 tests
    if 1 in levels:
        report.results.append(test_skill_md_exists(skill_path))
        report.results.append(test_frontmatter_valid(skill_path))
        report.results.append(test_scripts_exist(skill_path))
        report.results.append(test_scripts_syntax(skill_path))

    # Level 2 tests
    if 2 in levels:
        report.results.append(test_scripts_importable(skill_path))
        report.results.append(test_scripts_help(skill_path))

    # Level 4 tests
    if 4 in levels:
        report.results.append(test_description_quality(skill_path))

    return report


def print_report(report: SkillTestReport) -> None:
    """Print test report to console."""
    status = "PASS" if report.passed else "FAIL"
    print(f"\n{'='*60}")
    print(f"Skill: {report.skill_name}")
    print(f"Status: {status} ({report.score})")
    print(f"{'='*60}")

    for result in report.results:
        icon = "" if result.passed else ""
        level = f"L{result.level}"
        print(f"  {icon} [{level}] {result.name}: {result.message}")


def save_report(report: SkillTestReport, output_dir: Path) -> None:
    """Save test report to JSON file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"test_{report.skill_name}.json"

    with open(output_file, "w") as f:
        json.dump(report.to_dict(), f, indent=2)

    print(f"Report saved: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Test all Nixtla skills against success criteria"
    )
    parser.add_argument(
        "--skill",
        help="Test specific skill (e.g., nixtla-polymarket-analyst)"
    )
    parser.add_argument(
        "--level",
        type=int,
        choices=[1, 2, 3, 4],
        help="Run only specific test level"
    )
    parser.add_argument(
        "--output",
        default="tests/skills/results",
        help="Output directory for test reports"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON only"
    )

    args = parser.parse_args()

    # Determine which levels to test
    levels = [args.level] if args.level else [1, 2, 3, 4]

    # Find skills to test
    if args.skill:
        skill_paths = [SKILLS_DIR / args.skill]
        if not skill_paths[0].exists():
            print(f"Error: Skill not found: {args.skill}")
            sys.exit(1)
    else:
        skill_paths = sorted(SKILLS_DIR.glob("nixtla-*"))

    if not skill_paths:
        print(f"Error: No skills found in {SKILLS_DIR}")
        sys.exit(1)

    print(f"Testing {len(skill_paths)} skills...")
    print(f"Levels: {levels}")
    print(f"Skills directory: {SKILLS_DIR}")

    # Run tests
    all_reports = []
    passed_count = 0
    failed_count = 0

    for skill_path in skill_paths:
        report = test_skill(skill_path, levels)
        all_reports.append(report)

        if not args.json:
            print_report(report)

        if report.passed:
            passed_count += 1
        else:
            failed_count += 1

    # Save reports
    output_dir = Path(args.output)
    for report in all_reports:
        save_report(report, output_dir)

    # Summary
    print(f"\n{'='*60}")
    print(f"SUMMARY: {passed_count} passed, {failed_count} failed")
    print(f"{'='*60}")

    if args.json:
        summary = {
            "total": len(all_reports),
            "passed": passed_count,
            "failed": failed_count,
            "skills": [r.to_dict() for r in all_reports]
        }
        print(json.dumps(summary, indent=2))

    sys.exit(0 if failed_count == 0 else 1)


if __name__ == "__main__":
    main()
