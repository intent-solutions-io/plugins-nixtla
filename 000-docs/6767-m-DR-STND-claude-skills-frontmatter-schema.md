# Claude Skills Frontmatter Schema Standard

**Document ID**: 6767-m-DR-STND-claude-skills-frontmatter-schema
**Version**: 1.0.0
**Status**: CANONICAL - Cross-Repo Standard
**Created**: 2025-12-06
**Updated**: 2025-12-06

**Master Reference**: `000-docs/077-SPEC-MASTER-claude-skills-standard.md`

---

## Purpose

Canonical specification for Claude Skills YAML frontmatter fields. Use this as the authoritative reference for all skill development across repositories.

---

## Complete YAML Frontmatter Schema

```yaml
---
# ═══════════════════════════════════════════════════════════════
# REQUIRED FIELDS
# ═══════════════════════════════════════════════════════════════

name: skill-name
# Type: string
# Max Length: 64 characters
# Constraints:
#   - Lowercase letters, numbers, and hyphens ONLY
#   - No XML tags
#   - Cannot contain reserved words: "anthropic", "claude"
# Purpose: Command identifier when Claude invokes the Skill tool
# Examples:
#   ✅ processing-pdfs
#   ✅ analyzing-spreadsheets
#   ✅ git-commit-helper
#   ❌ PDF_Processing (uppercase)
#   ❌ claude-helper (reserved word)
#   ❌ my skill (spaces)

description: >
  What this skill does. Key capabilities. Use when [scenarios].
  Trigger with "[phrase 1]", "[phrase 2]".
# Type: string
# Max Length: 1024 characters
# Constraints:
#   - Must be non-empty
#   - No XML tags
#   - MUST use THIRD PERSON voice (injected into system prompt)
# Purpose: Primary signal for Claude's skill selection
# Formula: [Capabilities]. [Features]. Use when [scenarios]. Trigger with "[phrases]".
# Examples:
#   ✅ "Extract text and tables from PDF files, fill forms, merge documents.
#       Use when working with PDF files or when the user mentions PDFs."
#   ✅ "Generate commit messages by analyzing git diffs. Use when writing
#       commit messages or reviewing staged changes."
#   ❌ "I can help you process PDFs" (first person)
#   ❌ "You can use this for data" (second person)
#   ❌ "Helps with documents" (too vague)

# ═══════════════════════════════════════════════════════════════
# OPTIONAL FIELDS
# ═══════════════════════════════════════════════════════════════

allowed-tools: "Read,Write,Glob,Grep,Edit"
# Type: CSV string
# Default: No pre-approved tools (user prompted for each)
# Purpose: Pre-approves tools SCOPED TO SKILL EXECUTION ONLY
# NOTE: Only supported in Claude Code, NOT claude.ai web version
# Syntax Examples:
#   "Read,Write,Glob,Grep,Edit"           # Multiple tools
#   "Bash(git:*),Read,Grep"               # Scoped bash (git only)
#   "Bash(npm:*),Bash(npx:*),Read"        # NPM-scoped
#   "Read,Glob,Grep"                      # Read-only audit

model: inherit
# Type: string
# Default: "inherit" (use session model)
# Purpose: Override session model for skill execution
# Examples:
#   inherit                               # Use current model (default)
#   "claude-opus-4-20250514"              # Force Opus
#   "claude-sonnet-4-20250514"            # Force Sonnet
#   "claude-haiku-3-20250514"             # Force Haiku

version: "1.0.0"
# Type: string (semver)
# Purpose: Version tracking for skill evolution
# Format: MAJOR.MINOR.PATCH
#   MAJOR = Breaking changes
#   MINOR = New features, additive
#   PATCH = Bug fixes, clarifications

license: "MIT"
# Type: string
# Purpose: License terms reference
# Examples:
#   "MIT"
#   "Apache-2.0"
#   "Proprietary - See LICENSE.txt"

mode: false
# Type: boolean
# Default: false
# Purpose: When true, skill appears in prominent "Mode Commands" UI section
# Use Case: Skills that transform Claude's behavior for extended sessions

disable-model-invocation: false
# Type: boolean
# Default: false
# Purpose: When true, removes skill from <available_skills> list
# Effect: Users must invoke manually via /skill-name
# Use Cases:
#   - Dangerous operations (deployments, deletions)
#   - Infrastructure skills
#   - Skills that should NEVER auto-activate

# ═══════════════════════════════════════════════════════════════
# UNDOCUMENTED/EXPERIMENTAL - AVOID IN PRODUCTION
# ═══════════════════════════════════════════════════════════════

# when_to_use: "Additional usage context"
# Status: UNDOCUMENTED - behavior may change without notice
# Behavior: Appends to description with hyphen separator
# Recommendation: Do NOT use. Rely on detailed description field instead.
---
```

---

## Field Reference Table

| Field | Required | Type | Max | Default | Purpose |
|-------|----------|------|-----|---------|---------|
| `name` | **YES** | string | 64 chars | - | Command identifier |
| `description` | **YES** | string | 1024 chars | - | Skill selection signal |
| `allowed-tools` | No | CSV | - | none | Pre-approved tools |
| `model` | No | string | - | `inherit` | Model override |
| `version` | No | semver | - | - | Version tracking |
| `license` | No | string | - | - | License reference |
| `mode` | No | boolean | - | `false` | Mode command flag |
| `disable-model-invocation` | No | boolean | - | `false` | Manual-only flag |

---

## Validation Rules

### Name Field

```
✅ VALID:
- processing-pdfs
- data-analysis-v2
- git-commit-helper
- bigquery-forecaster

❌ INVALID:
- PDF_Processing      → uppercase not allowed
- claude-helper       → reserved word "claude"
- my skill           → spaces not allowed
- anthropic-tools    → reserved word "anthropic"
- a                  → too short (use descriptive names)
- this-is-a-very-long-skill-name-that-exceeds-sixty-four-characters-limit → too long
```

### Description Field

```
✅ VALID (third person, specific, includes triggers):
"Analyzes Excel spreadsheets, creates pivot tables, generates charts.
 Use when analyzing Excel files, spreadsheets, or .xlsx files.
 Trigger with 'analyze this spreadsheet', 'create pivot table'."

❌ INVALID:
"I can help you with Excel"     → first person
"You can use this for data"     → second person
"Helps with documents"          → too vague
"Excel tool"                    → no triggers
```

### Allowed-Tools Syntax

```yaml
# Full tool access
allowed-tools: "Bash"                    # All bash commands (dangerous)

# Scoped tool access (RECOMMENDED)
allowed-tools: "Bash(git:*)"             # Only git commands
allowed-tools: "Bash(git status:*)"      # Only git status
allowed-tools: "Bash(npm:*),Bash(npx:*)" # Only npm/npx

# Multiple tools
allowed-tools: "Read,Write,Glob,Grep,Edit"

# Read-only
allowed-tools: "Read,Glob,Grep"
```

---

## Directory Structure

```
skill-name/
├── SKILL.md              # REQUIRED - Frontmatter + instructions
├── scripts/              # OPTIONAL - Executable code (no token cost)
│   ├── analyze.py
│   └── validate.py
├── references/           # OPTIONAL - Docs loaded into context
│   ├── API_REFERENCE.md
│   └── EXAMPLES.md
├── assets/               # OPTIONAL - Templates (path reference only)
│   └── report_template.md
└── LICENSE.txt           # OPTIONAL - License terms
```

### Token Cost by Directory

| Directory | Loaded Into Context? | Token Cost |
|-----------|---------------------|------------|
| `scripts/` | No (executed via Bash) | **None** |
| `references/` | Yes (via Read tool) | **High** |
| `assets/` | No (path reference only) | **None** |

---

## Minimal Valid SKILL.md

```yaml
---
name: my-skill
description: Does X and Y. Use when [condition]. Trigger with "phrase".
---

# My Skill

Instructions here.
```

---

## Complete Valid SKILL.md

```yaml
---
name: analyzing-spreadsheets
description: |
  Analyzes Excel spreadsheets, creates pivot tables, generates charts and reports.
  Use when working with Excel files, .xlsx data, or tabular analysis.
  Trigger with "analyze this spreadsheet", "create pivot table", "summarize Excel data".
allowed-tools: "Read,Write,Glob,Grep,Edit"
version: "1.0.0"
---

# Analyzing Spreadsheets

[Full instructions follow...]
```

---

## Sources

- [Official Anthropic Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Official Anthropic Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)

---

**Last Updated**: 2025-12-06
**Status**: CANONICAL - Cross-Repo Standard
