#!/usr/bin/env python3
"""
validate_skills.py

Nixtla Skills - SKILL.md Validator (v2.3.0 ENGINEERING-COMPLETE)

Validates Claude SKILL definitions against:
- Anthropic Agent Skills official specification
- Lee Han Chung Deep Dive (October 2025 - NEWEST SOURCE)
- Nixtla internal standards (SKILLS-STANDARD-COMPLETE.md v2.3.0)

Usage:
  python scripts/validate_skills.py [--strict-labs]

Exit codes:
  0 = all skills valid (no errors)
  1 = one or more errors

Sources:
- https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/
- https://claude.com/blog/skills
- https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- 000-docs/skills-schema/SKILLS-STANDARD-COMPLETE.md v2.3.0
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════
# CONFIGURATION (Based on Lee Han Chung + Anthropic Official)
# ═══════════════════════════════════════════════════════════

# Discovery paths (Lee Han Chung spec, October 2025)
# ONLY production skills in 003-skills - these are LIVE and must be correct
PROD_SKILLS_ROOT = Path("003-skills") / ".claude" / "skills"

# Anthropic official constraints
NAME_REGEX = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
MAX_NAME_LEN = 64
MAX_DESC_CHARS = 1024  # Per skill (Anthropic platform docs)
TOTAL_DESC_BUDGET = 15000  # Across ALL skills (Lee + v2.3.0)
RESERVED_WORDS = ["anthropic", "claude"]

# Body constraints (v2.3.0 standard)
MAX_BODY_WORDS = 5000
TARGET_TOKENS = 2500
MAX_TOKENS = 5000
TOKEN_MULTIPLIER = 1.3  # Rough estimate: 1.3 tokens per word

# Recommended sections (v2.3.0 - progressive disclosure allows variations)
RECOMMENDED_HEADINGS = [
    "overview",
    "prerequisites",
    "instructions",
    "error handling",
    "examples",
    "resources",
]

# Anti-patterns (v2.3.0 Section 15)
SECOND_PERSON_PHRASES = [
    "you should",
    "you need to",
    "you must",
    "you will",
    "you can",
    "we should",
    "we need to",
    "we must",
    "we will",
    "i will",
    "i should",
    "don't forget",
    "remember to",
]

FIRST_PERSON_PHRASES = ["I ", "We ", "My ", "Our "]
SECOND_PERSON_SUBJECTS = ["You ", "Your "]


# ═══════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════


@dataclass
class SkillIssue:
    level: str  # "ERROR" | "WARN"
    message: str


@dataclass
class SkillReport:
    path: Path
    is_prod: bool
    frontmatter: Dict = field(default_factory=dict)
    body: str = ""
    issues: List[SkillIssue] = field(default_factory=list)

    def add_error(self, msg: str) -> None:
        self.issues.append(SkillIssue("ERROR", msg))

    def add_warning(self, msg: str) -> None:
        self.issues.append(SkillIssue("WARN", msg))

    @property
    def has_errors(self) -> bool:
        return any(i.level == "ERROR" for i in self.issues)

    @property
    def has_warnings(self) -> bool:
        return any(i.level == "WARN" for i in self.issues)


# ═══════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════


def load_skill_file(path: Path) -> Tuple[Dict, str]:
    """Parse YAML frontmatter + markdown body from SKILL.md."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    if not lines or lines[0].strip() != "---":
        raise ValueError("Missing YAML frontmatter opening '---'")

    fm_end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            fm_end_idx = i
            break

    if fm_end_idx is None:
        raise ValueError("Missing YAML frontmatter closing '---'")

    fm_text = "\n".join(lines[1:fm_end_idx])
    body = "\n".join(lines[fm_end_idx + 1 :])

    frontmatter = yaml.safe_load(fm_text) or {}
    if not isinstance(frontmatter, dict):
        raise ValueError("Frontmatter must parse to a YAML mapping/object")

    return frontmatter, body


def iter_skill_files() -> List[Tuple[Path, bool]]:
    """Yield (path, is_prod) pairs for PRODUCTION SKILL.md files ONLY."""
    results: List[Tuple[Path, bool]] = []

    # ONLY production skills in 003-skills - these are LIVE and must be correct
    if PROD_SKILLS_ROOT.is_dir():
        for p in PROD_SKILLS_ROOT.rglob("SKILL.md"):
            results.append((p, True))

    return sorted(results, key=lambda t: str(t[0]))


# ═══════════════════════════════════════════════════════════
# VALIDATION FUNCTIONS
# ═══════════════════════════════════════════════════════════


def validate_name(value: Optional[str], report: SkillReport) -> None:
    """Validate 'name' field (Anthropic spec + v2.3.0)."""
    if not value:
        report.add_error("Missing required 'name' in frontmatter.")
        return

    if not isinstance(value, str):
        report.add_error(f"'name' must be a string, got {type(value).__name__}")
        return

    # Length constraint
    if len(value) > MAX_NAME_LEN:
        report.add_error(f"'name' is too long ({len(value)} chars). Max allowed is {MAX_NAME_LEN}.")

    # Format constraint (lowercase, hyphens, alphanumeric start/end)
    if not NAME_REGEX.match(value):
        report.add_error(
            "'name' must be lowercase, 1–64 chars, start/end with alphanumeric, "
            "and only contain a–z, 0–9, or single hyphens (no spaces or uppercase)."
        )

    # Reserved words (v2.3.0 Section 4)
    if any(word in value.lower() for word in RESERVED_WORDS):
        report.add_error(f"'name' contains reserved word. Avoid: {RESERVED_WORDS}")


def validate_description(value: Optional[str], report: SkillReport) -> None:
    """Validate 'description' field (Lee + v2.3.0)."""
    if not value:
        # Lee: "Must have either description OR when_to_use"
        # Check handled in validate_discovery_fields()
        return

    if not isinstance(value, str):
        report.add_error(f"'description' must be a string, got {type(value).__name__}")
        return

    # Length constraint (per skill)
    if len(value) > MAX_DESC_CHARS:
        report.add_error(
            f"'description' is too long ({len(value)} chars). " f"Max allowed is {MAX_DESC_CHARS}."
        )

    # Third-person voice requirement (v2.3.0 Section 4)
    # Use word boundaries to avoid false positives (e.g., "CI/CD" contains "I ")
    bad_voice = []
    for phrase in FIRST_PERSON_PHRASES + SECOND_PERSON_SUBJECTS:
        # Check with word boundary to avoid matching within acronyms
        pattern = r"\b" + re.escape(phrase.strip()) + r"\b"
        if re.search(pattern, value, re.IGNORECASE):
            bad_voice.append(phrase.strip())

    if bad_voice:
        report.add_error(
            f"'description' must use third person. Found: {bad_voice}. "
            "Use 'This skill...', 'Guides...', 'Analyzes...', 'Transforms...'"
        )

    # Plain text (no Markdown - Lee spec)
    if "\n" in value:
        report.add_warning(
            "'description' contains newline characters. It should be a single "
            "plain-text paragraph (no Markdown formatting)."
        )

    if any(ch in value for ch in ("#", "*", "`", "[", "]")):
        report.add_warning("'description' appears to contain Markdown. It should be plain text.")


def validate_discovery_fields(fm: Dict, report: SkillReport) -> None:
    """Validate that skill has discovery metadata (Lee spec)."""
    # Lee: "Skill must have either description OR when_to_use to appear in Skill tool"
    has_desc = bool(fm.get("description"))
    has_when = bool(fm.get("when_to_use"))

    if not has_desc and not has_when:
        report.add_error(
            "Must have either 'description' OR 'when_to_use' for skill discovery. "
            "Missing both will filter skill from Claude's Skill tool."
        )

    # Warn about deprecated when_to_use (Lee: "avoid in production")
    if has_when:
        report.add_warning(
            "'when_to_use' field is undocumented and may change. "
            "Prefer using 'description' only for production skills."
        )


def validate_allowed_tools(fm: Dict, report: SkillReport) -> None:
    """Validate 'allowed-tools' field (Lee + v2.3.0 Section 6)."""
    # Lee: "Fields use hyphens in YAML, not underscores"
    raw = None
    field_name = None

    if "allowed-tools" in fm:
        raw = fm["allowed-tools"]
        field_name = "allowed-tools"
    elif "allowed_tools" in fm:
        raw = fm["allowed_tools"]
        field_name = "allowed_tools"
        report.add_warning(
            "Use 'allowed-tools' (hyphen) not 'allowed_tools' (underscore). "
            "Underscore version may not be recognized on all platforms."
        )

    if raw is None:
        report.add_error("Missing required 'allowed-tools' in frontmatter.")
        return

    # Parse tools (Lee: comma-separated string OR list)
    tools: List[str] = []
    if isinstance(raw, str):
        tools = [t.strip() for t in raw.split(",") if t.strip()]
    elif isinstance(raw, list):
        bad = [t for t in raw if not isinstance(t, str)]
        if bad:
            report.add_error(
                f"'allowed-tools' list must contain only strings (found {len(bad)} non-strings)."
            )
        tools = [str(t).strip() for t in raw]
    else:
        report.add_error(
            f"'allowed-tools' must be a string or list of strings, got {type(raw).__name__}."
        )
        return

    if not tools:
        report.add_error("'allowed-tools' must not be empty.")
        return

    # Validate scoped Bash syntax (Lee: "Bash(git:*)" pattern)
    scoped_bash_pattern = re.compile(r"^Bash\([a-z][a-z0-9-]*:\*\)$")
    for tool in tools:
        # Check for unscoped Bash (v2.3.0 Section 6)
        if tool == "Bash":
            report.add_warning(
                "Found unscoped 'Bash' in allowed-tools. Consider scoping for security: "
                "Bash(git:*), Bash(python:*), Bash(npm:*)"
            )
        # Validate scoped Bash syntax
        elif tool.startswith("Bash("):
            if not scoped_bash_pattern.match(tool):
                report.add_warning(
                    f"Invalid Bash scope syntax: '{tool}'. "
                    f"Use pattern: Bash(command:*) e.g., Bash(git:*)"
                )


def validate_optional_fields(fm: Dict, report: SkillReport) -> None:
    """Validate optional frontmatter fields (Lee + v2.3.0)."""
    # version (recommended)
    if "version" not in fm:
        report.add_warning("Missing recommended 'version' field (e.g., '1.0.0')")
    elif not isinstance(fm["version"], str):
        report.add_error(f"'version' must be a string, got {type(fm['version']).__name__}")

    # license (recommended)
    if "license" not in fm:
        report.add_warning("Missing recommended 'license' field")

    # model (Lee: "inherit" or specific model ID)
    if "model" in fm:
        value = fm["model"]
        if not isinstance(value, str):
            report.add_error(f"'model' must be a string, got {type(value).__name__}")
        # Note: We don't validate specific model IDs since they change frequently

    # disable-model-invocation (Lee: boolean)
    if "disable-model-invocation" in fm:
        value = fm["disable-model-invocation"]
        if not isinstance(value, bool):
            report.add_error(
                f"'disable-model-invocation' must be boolean (true/false), got {type(value).__name__}"
            )

    # mode (Lee: boolean)
    if "mode" in fm:
        value = fm["mode"]
        if not isinstance(value, bool):
            report.add_error(f"'mode' must be boolean, got {type(value).__name__}")


def validate_body_content(body: str, report: SkillReport) -> None:
    """Validate SKILL.md body content (v2.3.0 Section 5)."""
    # Word count and token estimate
    words = re.findall(r"\w+", body)
    word_count = len(words)
    estimated_tokens = int(word_count * TOKEN_MULTIPLIER)

    if word_count > MAX_BODY_WORDS:
        report.add_error(
            f"Body is too long ({word_count} words, ~{estimated_tokens} tokens). "
            f"Max allowed is {MAX_BODY_WORDS} words (~{MAX_TOKENS} tokens). "
            f"Consider moving content to references/."
        )
    elif estimated_tokens > MAX_TOKENS:
        report.add_error(
            f"Body estimated at {estimated_tokens} tokens (>{MAX_TOKENS} max). "
            f"Move content to references/ for progressive disclosure."
        )
    elif estimated_tokens > TARGET_TOKENS:
        report.add_warning(
            f"Body estimated at {estimated_tokens} tokens. "
            f"Target is ~{TARGET_TOKENS} for optimal context efficiency."
        )

    # Recommended section headings (v2.3.0 - warnings, not errors due to progressive disclosure)
    lower_body = body.lower()
    missing_headings = []
    for h in RECOMMENDED_HEADINGS:
        pattern = f"## {h}"
        if pattern not in lower_body:
            missing_headings.append(h)

    if missing_headings:
        msg = (
            "Missing recommended section headings (OK if using progressive disclosure): "
            + ", ".join(f"'## {h.title()}'" for h in missing_headings)
        )
        report.add_warning(msg)

    # Check for hardcoded absolute paths (v2.3.0 Section 15, Anti-Pattern #1)
    # Lee: "Use {baseDir} variable—never hardcode absolute paths"
    hardcoded_paths = []
    if re.search(r"[/\\]home[/\\]", body):
        hardcoded_paths.append("/home/")
    if re.search(r"[/\\]Users[/\\]", body):
        hardcoded_paths.append("/Users/")
    if re.search(r"C:\\", body):
        hardcoded_paths.append("C:\\")

    if hardcoded_paths:
        report.add_error(
            f"Body contains hardcoded absolute paths: {hardcoded_paths}. "
            f"Use {{baseDir}} variable instead for portability. "
            f"Example: {{baseDir}}/scripts/analyzer.py"
        )

    # Second-person / conversational anti-patterns (v2.3.0)
    lb = lower_body
    bad_phrases = [p for p in SECOND_PERSON_PHRASES if p in lb]
    if bad_phrases:
        report.add_warning(
            f"Body contains conversational phrases: {bad_phrases[:5]}. "
            f"Skills should use objective, imperative style."
        )


def validate_skill(path: Path, is_prod: bool) -> SkillReport:
    """Validate a single SKILL.md file."""
    report = SkillReport(path=path, is_prod=is_prod)

    try:
        fm, body = load_skill_file(path)
        report.frontmatter = fm
        report.body = body
    except Exception as e:
        report.add_error(f"Failed to parse SKILL.md: {e}")
        return report

    # Frontmatter validations
    validate_name(fm.get("name"), report)
    validate_description(fm.get("description"), report)
    validate_discovery_fields(fm, report)
    validate_allowed_tools(fm, report)
    validate_optional_fields(fm, report)

    # Body validations
    validate_body_content(body, report)

    return report


def validate_total_description_budget(reports: List[SkillReport]) -> Optional[str]:
    """
    Validate total description budget across ALL skills (Lee + v2.3.0 Section 4).

    Lee: "15,000-character budget limit across all loaded skills"
    v2.3.0: "If combined descriptions exceed 15k, Claude silently filters skills"
    """
    total_chars = 0
    skill_descs = []

    for r in reports:
        desc = r.frontmatter.get("description", "")
        if desc:
            total_chars += len(desc)
            skill_descs.append((r.path.name, len(desc)))

    if total_chars > TOTAL_DESC_BUDGET:
        msg = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║ CRITICAL: TOTAL DESCRIPTION BUDGET EXCEEDED                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

Total description length: {total_chars} chars
Budget limit:             {TOTAL_DESC_BUDGET} chars
Overage:                  {total_chars - TOTAL_DESC_BUDGET} chars ({((total_chars - TOTAL_DESC_BUDGET) / TOTAL_DESC_BUDGET * 100):.1f}% over)

⚠️  IMPACT: Claude will SILENTLY FILTER skills when budget is exceeded!
    Skills may randomly fail to activate with no error messages.

BREAKDOWN (top consumers):
"""
        for name, chars in sorted(skill_descs, key=lambda x: x[1], reverse=True)[:10]:
            msg += f"  {name:40s} {chars:4d} chars\n"

        msg += f"""
FIX: Reduce descriptions to 300-400 chars each (not the 1024 max).
     Target: {len(reports)} skills × 400 chars = {len(reports) * 400} chars (safe)
"""
        return msg

    return None


# ═══════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate SKILL.md files for Nixtla Claude skills (v2.3.0 ENGINEERING-COMPLETE)"
    )
    parser.add_argument(
        "--strict-labs",
        action="store_true",
        help="Treat lab (workspaces) warnings as errors.",
    )
    args = parser.parse_args(argv)

    skill_files = iter_skill_files()
    if not skill_files:
        print("⚠️  No PRODUCTION SKILL.md files found")
        print("    Checked path:")
        print(f"      Production: {PROD_SKILLS_ROOT}")
        return 0

    print(f"📋 Found {len(skill_files)} SKILL.md files to validate\n")

    # Validate each skill
    reports: List[SkillReport] = []
    for path, is_prod in skill_files:
        report = validate_skill(path, is_prod=is_prod)
        reports.append(report)

    # Check total description budget (CRITICAL)
    budget_error = validate_total_description_budget(reports)

    # Report results
    total_errors = 0
    total_warnings = 0
    files_with_issues = 0

    for report in reports:
        try:
            rel = report.path.relative_to(Path.cwd())
        except ValueError:
            rel = report.path  # Already relative or outside cwd
        prefix = "[PROD]" if report.is_prod else "[LAB ]"

        if report.has_errors or report.has_warnings:
            files_with_issues += 1
            print(f"{prefix} {rel}")
            for issue in report.issues:
                level = issue.level
                msg = issue.message
                symbol = "❌" if level == "ERROR" else "⚠️ "
                print(f"  {symbol} {level}: {msg}")
            print()

        if report.has_errors:
            total_errors += 1
        if report.has_warnings:
            if report.is_prod or args.strict_labs:
                total_errors += 1  # Treat warnings as errors in strict mode
            else:
                total_warnings += 1

    # Print budget error if present
    if budget_error:
        print(budget_error)
        total_errors += 1

    # Summary
    if total_errors == 0 and total_warnings == 0 and not budget_error:
        print("✅ All SKILL.md files passed validation!")
        print(f"   {len(skill_files)} skills checked")
        return 0

    print("═" * 80)
    print("SUMMARY:")
    print(f"  Files checked:       {len(skill_files)}")
    print(f"  Files with issues:   {files_with_issues}")
    print(f"  Skills with errors:  {total_errors}")
    print(f"  Skills with warnings: {total_warnings}")

    if budget_error:
        print(f"\n  ⚠️  TOTAL DESCRIPTION BUDGET: EXCEEDED (see above)")

    print("═" * 80)

    return 1 if total_errors > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
