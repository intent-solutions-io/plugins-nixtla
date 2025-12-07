# Claude Skills Master Standard

**Document ID**: 098-SPEC-MASTER-claude-skills-standard.md
**Version**: 1.0.0
**Status**: AUTHORITATIVE - Single Source of Truth
**Created**: 2025-12-06
**Updated**: 2025-12-06
**Source**: [Lee Han Chung Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/) + Anthropic Official Documentation

---

## Purpose

**This is the MASTER STANDARD for all Claude Skills development.**

All other skill documentation in this repository should defer to this document. Supersedes:
- `041-SPEC-nixtla-skill-standard.md`
- `planned-skills/GLOBAL-STANDARD-SKILL-SCHEMA.md`
- `planned-skills/HOW-TO-MAKE-A-PERFECT-SKILL.md`
- `6767-l-OD-CANON-anthropic-agent-skills-official-standard.md`

---

## Table of Contents

1. [Core Architecture](#1-core-architecture)
2. [SKILL.md Structure](#2-skillmd-structure)
3. [YAML Frontmatter Schema](#3-yaml-frontmatter-schema)
4. [Bundled Resources](#4-bundled-resources)
5. [Skill Selection Mechanism](#5-skill-selection-mechanism)
6. [Three-Stage Execution Pipeline](#6-three-stage-execution-pipeline)
7. [Two-Message Injection Pattern](#7-two-message-injection-pattern)
8. [Tool Permissions](#8-tool-permissions)
9. [Token Budget](#9-token-budget)
10. [Common Patterns](#10-common-patterns)
11. [Critical Gotchas](#11-critical-gotchas)
12. [Best Practices](#12-best-practices)
13. [Validation Checklist](#13-validation-checklist)
14. [Quick Reference Card](#14-quick-reference-card)

---

## 1. Core Architecture

### Skills Are Prompt-Based Meta-Tools

Claude Agent Skills are **NOT**:
- Executable code plugins (that's MCP servers)
- Slash commands (that's `commands/` directory)
- Tools that Claude uses (that's Read, Write, Bash, etc.)

Claude Agent Skills **ARE**:
- **Prompt packages** that modify Claude's reasoning
- **Auto-activating** based on LLM reasoning (no manual triggers)
- **Progressive disclosure** - load only when needed
- **Persistent** - installed once, available forever

### Where Skills Actually Live

**Critical insight**: Skills are NOT in the system prompt.

Skills live in the `tools` array as part of a meta-tool called `Skill`:

```javascript
tools: [
  { name: "Read", ... },
  { name: "Write", ... },
  {
    name: "Skill",                    // Meta-tool (capital S)
    inputSchema: { command: string },
    description: "<available_skills>..." // Dynamic list of all skill names + descriptions
  }
]
```

This enables dynamic loading without system prompt manipulation.

### Discovery Sources (Priority Order)

Skills load from multiple sources (later overrides earlier):

1. **User settings**: `~/.claude/skills/`
2. **Project settings**: `.claude/skills/`
3. **Plugin-provided skills**
4. **Built-in skills**

---

## 2. SKILL.md Structure

Every skill requires a `SKILL.md` file at its root:

```
skill-name/
├── SKILL.md              # REQUIRED - Instructions + YAML frontmatter
├── scripts/              # OPTIONAL - Executable Python/Bash
├── references/           # OPTIONAL - Docs loaded into context
└── assets/               # OPTIONAL - Templates referenced by path
```

### SKILL.md Format

```markdown
---
name: skill-name
description: What this skill does. Use when [conditions]. Trigger with "[phrases]".
---

# Skill Name

Brief purpose statement (1-2 sentences).

## Overview

What this skill does, when to use it, key capabilities.

## Prerequisites

Required tools, APIs, environment variables, dependencies.

## Instructions

### Step 1: [Action Verb]
[Imperative instructions]

### Step 2: [Action Verb]
[More instructions]

## Output

What artifacts this skill produces.

## Error Handling

Common failures and solutions.

## Examples

Concrete usage examples with input/output.

## Resources

Links to files using {baseDir} variable.
```

---

## 3. YAML Frontmatter Schema

### Complete Schema

```yaml
---
# 🔴 REQUIRED FIELDS
name: skill-name                              # 64 chars max, lowercase + hyphens only
description: >                                 # 1024 chars max
  What it does. Key capabilities. Use when [scenarios]. Trigger with "[phrases]".

# 🟡 OPTIONAL FIELDS (all functional in Claude Code)
allowed-tools: "Read,Write,Glob,Grep,Edit"    # CSV of pre-approved tools
model: inherit                                 # Model override or "inherit"
version: "1.0.0"                              # Semantic versioning
license: "Proprietary"                        # License reference

# 🟠 BEHAVIORAL FLAGS
mode: false                                    # true = mode skill (prominent UI section)
disable-model-invocation: false                # true = requires manual /skill-name

# ⚠️ UNDOCUMENTED (avoid in production)
when_to_use: "..."                            # Appended to description; status unclear
---
```

### Field Reference

| Field | Type | Required | Max | Purpose |
|-------|------|----------|-----|---------|
| `name` | string | 🔴 YES | 64 chars | Skill identifier; becomes Skill tool's `command` input |
| `description` | string | 🔴 YES | 1024 chars | Triggers skill selection via LLM reasoning |
| `allowed-tools` | CSV | 🟡 No | - | Tools pre-approved during execution |
| `model` | string | 🟡 No | - | Model override (e.g., `"claude-opus-4-20250514"`) |
| `version` | string | 🟡 No | - | Semantic versioning for tracking |
| `license` | string | 🟡 No | - | License terms reference |
| `mode` | boolean | 🟡 No | - | If `true`, appears in prominent UI section |
| `disable-model-invocation` | boolean | 🟡 No | - | If `true`, requires manual `/skill-name` |

### Naming Requirements

- **Maximum 64 characters**
- **Lowercase letters, numbers, and hyphens only**
- No XML tags
- Cannot include reserved words: `"anthropic"`, `"claude"`

**Good**: `pdf-extractor`, `timegpt-forecaster`, `data-schema-mapper`
**Bad**: `PDF_Extractor` (uppercase), `claude-helper` (reserved), `helper` (too vague)

### Description Quality Formula

**Template**:
```yaml
description: "[Primary capabilities]. [Secondary features]. Use when [scenarios]. Trigger with '[phrases]'."
```

**Example (95/100 quality)**:
```yaml
description: "Analyzes Polymarket prediction market contracts using TimeGPT forecasting. Fetches contract odds, transforms to time series, generates price predictions with confidence intervals, and detects arbitrage opportunities. Use when analyzing prediction markets, forecasting contract prices, identifying mispriced contracts, or comparing Polymarket vs Kalshi odds. Trigger with 'forecast Polymarket odds', 'analyze prediction market', 'find arbitrage opportunities'."
```

**Scoring Criteria**:
| Criterion | Weight | How to Achieve |
|-----------|--------|----------------|
| Action-oriented | 20% | Use strong verbs: "Generates", "Analyzes", "Transforms" |
| Clear triggers | 25% | Include "Use when [scenarios]" |
| Comprehensive | 15% | Cover what + when + scope |
| Natural language | 20% | Include phrases users actually say |
| Specificity | 10% | Be specific without being verbose |
| Technical terms | 10% | Use domain keywords users naturally use |

**Critical**: Use **third person** - descriptions are injected into system prompt:
- ✅ "Processes Excel files and generates reports"
- ❌ "I can help you..." or "You can use this to..."

---

## 4. Bundled Resources

### `/scripts/` Directory

**Purpose**: Executable Python or Bash scripts for deterministic operations.

**Usage**: Claude invokes via Bash tool:
```bash
python {baseDir}/scripts/fetch_data.py --contract-id "0x1234"
```

**Scripts execute, they are NOT read into context** - saves tokens, ensures consistency.

### `/references/` Directory

**Purpose**: Documentation loaded into Claude's context via Read tool.

**Usage**:
```markdown
For API details, see `{baseDir}/references/API_REFERENCE.md`
```

**Token cost**: Content IS loaded into context (consumes tokens).

### `/assets/` Directory

**Purpose**: Templates and static resources referenced by path but NOT loaded.

**Usage**:
```markdown
Use template at `{baseDir}/assets/report_template.md`
```

**Token cost**: None - files referenced by path only.

### Key Distinction

| Directory | Purpose | Loaded into Context? | Token Cost |
|-----------|---------|---------------------|------------|
| `scripts/` | Executable code | No (executed) | None |
| `references/` | Documentation | Yes (Read tool) | High |
| `assets/` | Templates/configs | No (path reference) | None |

---

## 5. Skill Selection Mechanism

**Critical insight**: "There is no algorithmic skill selection or AI-powered intent detection at the code level. The decision-making happens entirely within Claude's reasoning process."

### Process

1. System formats all available skills into text descriptions in the Skill tool's prompt
2. Claude reads the `<available_skills>` list
3. Claude uses **native language understanding** to match user intent
4. Claude invokes: `{"name": "Skill", "input": {"command": "pdf"}}`

**No lexical matching, no embeddings, no classifiers** - pure LLM reasoning.

### Why Descriptions Matter

Descriptions are the ONLY information Claude sees before deciding to activate a skill.

If your description doesn't match the user's natural language, the skill **will never trigger**.

---

## 6. Three-Stage Execution Pipeline

### Stage 1: VALIDATION

1. **Syntax checking** - YAML frontmatter parsing
2. **Skill existence verification** - Does SKILL.md exist?
3. **Frontmatter parsing** - Extract name, description, allowed-tools

**Error codes**:
- Empty command input
- Unknown skill
- File loading failure
- Model invocation disabled
- Non-prompt-based skill

### Stage 2: PERMISSION EVALUATION

1. **Deny rules checked first** (blocking patterns)
2. **Allow rules checked second** (pre-approved tools)
3. **Default**: Prompt user for approval

### Stage 3: LOADING & INJECTION

1. SKILL.md content loaded
2. Two messages injected (visible + hidden)
3. Context modifier applied (tool permissions scoped)
4. Claude executes with modified context

---

## 7. Two-Message Injection Pattern

Skills inject **two separate user messages** into conversation history:

### Message 1: Visible Metadata

```xml
<command-message>The "pdf" skill is loading</command-message>
<command-name>pdf</command-name>
<command-args>report.pdf</command-args>
```

- `isMeta: false` (default)
- **Shown to user** - provides transparency
- ~50-200 characters

### Message 2: Hidden Prompt

Full SKILL.md content with:
- `isMeta: true`
- **Hidden from UI**, sent to API
- ~500-5,000 words
- Provides Claude with detailed instructions

### Why Two Messages?

**Single message problem**:
- `isMeta: false` exposes thousands of words to users (unusable UI)
- `isMeta: true` hides skill activation entirely (no transparency)

**Two message solution**:
- Message 1: User transparency ("The pdf skill is loading")
- Message 2: Claude guidance (detailed skill prompt)

**Dual-channel communication**: transparency for humans, detail for AI.

---

## 8. Tool Permissions

### Permission Scoping

Tools in `allowed-tools` receive pre-approval **during skill execution only**:

```yaml
# ✅ Specific git operations
allowed-tools: "Bash(git status:*),Bash(git diff:*),Read,Grep"

# ✅ File operations only
allowed-tools: "Read,Write,Edit,Glob,Grep"

# ✅ Read-only audit
allowed-tools: "Read,Glob,Grep"

# ❌ Avoid unnecessary surface area
allowed-tools: "Bash,Read,Write,Edit,Glob,Grep,WebSearch,Task,Agent"
```

### Scoped Permission Syntax

```yaml
# All commands of a tool
allowed-tools: "Bash"

# Specific command scoping
allowed-tools: "Bash(git:*)"           # Only git commands
allowed-tools: "Bash(npm:*),Bash(npx:*)"  # Only npm/npx
allowed-tools: "Bash(python:*)"        # Only python commands
```

**Permissions revert** once skill execution completes.

---

## 9. Token Budget

### Budget Allocation

| Level | Content | Token Budget |
|-------|---------|-------------|
| **Level 1** (Discovery) | name + description | ~100 tokens per skill |
| **Level 2** (Activation) | Full SKILL.md body | <5,000 tokens (~500 lines) |
| **Level 3** (Resources) | references/ files | Loaded on-demand |

### Global Limit

The `<available_skills>` section has a **15,000-character default limit**.

If you load too many skills or use verbose descriptions, some will be filtered out silently.

### Guidelines

| Content | Target | Maximum |
|---------|--------|---------|
| Description | ~250 chars | 1,024 chars |
| SKILL.md body | 2,500 tokens | 5,000 tokens (~500 lines) |
| references/ file | <1,000 tokens | As needed |

**Rule**: If SKILL.md exceeds 500 lines, split into referenced files.

---

## 10. Common Patterns

### Pattern 1: Script Automation ⭐

**Flow**: Claude orchestrates → Python/Bash executes → Claude processes results

```markdown
### Step 1: Fetch Data
Run: `python {baseDir}/scripts/fetch_data.py --output data.json`

### Step 2: Transform
Run: `python {baseDir}/scripts/transform.py --input data.json`

### Step 3: Report
Run: `python {baseDir}/scripts/generate_report.py`
```

### Pattern 2: Read-Process-Write

**Flow**: Read input → Apply rules → Write output

### Pattern 3: Search-Analyze-Report

**Flow**: Search → Read matches → Analyze → Generate report

### Pattern 4: Command Chain Execution

**Flow**: Step 1 && Step 2 && Step 3

### Pattern 5: Wizard-Style Workflows

**Flow**: Step 1 → [User Confirm] → Step 2 → [User Confirm] → Step 3

### Pattern 6: Template-Based Generation

**Flow**: Load template from assets/ → Fill placeholders → Write

### Pattern 7: Iterative Refinement

**Flow**: Pass 1 (broad) → Pass 2 (deep) → Pass 3 (recommendations)

### Pattern 8: Context Aggregation

**Flow**: Gather source 1, 2, 3 → Synthesize

---

## 11. Critical Gotchas

### 1. Skills Are NOT Concurrency-Safe

Multiple simultaneous skill invocations may cause context conflicts. Queue skill execution or implement mutual exclusion.

### 2. Skills Don't Live in System Prompts

They're in the `tools` array as part of the Skill meta-tool. This enables dynamic loading without system prompt modification.

### 3. `when_to_use` is Undocumented

Despite appearing in code, this field is not officially documented. It gets appended to description with a hyphen separator but may change or be removed. **Rely on detailed `description` field instead.**

### 4. Hardcoded Paths Break Portability

Using `/home/user/project/config.json` breaks skill portability. **Always use `{baseDir}` variable.**

### 5. Token Budget Filtering

If you load too many skills or use verbose descriptions, some will be **filtered out silently**. Monitor skill count and description length.

### 6. Permission Leakage

Over-specifying `allowed-tools` creates unnecessary security surface. Include only tools the skill actually requires.

### 7. Model Override Costs

Requesting higher-capability models (`claude-opus-4`) increases token costs and latency. Reserve for genuinely complex tasks.

### 8. isMeta Flag Visibility

The `isMeta` flag defaults to `false`. Messages intended for Claude-only visibility MUST explicitly set `isMeta: true` or they'll appear in the UI.

### 9. One-Level-Deep References Only

Avoid nested references (SKILL.md → file1.md → file2.md). Claude may only partially read nested files.

---

## 12. Best Practices

### ✅ Do This

- Keep SKILL.md under 500 lines (5,000 tokens)
- Use `{baseDir}` for all file paths
- Specify only required tools in `allowed-tools`
- Write clear, action-oriented descriptions (150-300 characters)
- Use **third person** in descriptions
- Use imperative language in instructions
- Bundle supporting files in `/scripts/`, `/references/`, `/assets/`
- Include comprehensive examples in SKILL.md
- Document error handling and edge cases
- Test skill with Haiku, Sonnet, and Opus

### ❌ Avoid This

- Hardcoding absolute paths
- Specifying unnecessary tools
- Vague descriptions without triggers
- Embedding everything in SKILL.md
- Using undocumented `when_to_use` field in production
- Skills exceeding 500 lines
- Deeply nested file references
- First or second person descriptions
- Missing error handling

---

## 13. Validation Checklist

### Frontmatter Compliance

- [ ] Has `name` matching folder name (lowercase + hyphens)
- [ ] Has action-oriented `description` with "Use when" and trigger phrases
- [ ] `description` is under 1,024 characters
- [ ] Uses third person voice
- [ ] Has `version` in semver format (optional but recommended)
- [ ] Has minimal `allowed-tools` (only what's needed)
- [ ] NO undocumented fields in production

### Structure Compliance

- [ ] Has SKILL.md at root
- [ ] `scripts/` directory exists (can be empty)
- [ ] `references/` directory exists (can be empty)
- [ ] `assets/` directory exists (can be empty)
- [ ] Uses `{baseDir}` for all path references
- [ ] No hardcoded absolute paths

### Content Compliance

- [ ] SKILL.md under 500 lines
- [ ] Uses imperative language
- [ ] Has all required sections (Purpose, Overview, Prerequisites, Instructions, Output, Error Handling, Examples, Resources)
- [ ] Includes at least 1-2 concrete examples
- [ ] Documents error handling
- [ ] One-level-deep references only

### Testing

- [ ] Trigger phrases activate skill correctly
- [ ] Scripts execute without errors
- [ ] Examples produce expected output
- [ ] Tested with Haiku, Sonnet, and Opus

---

## 14. Quick Reference Card

### Minimal Skill Structure

```
my-skill/
└── SKILL.md
```

### SKILL.md Template

```yaml
---
name: my-skill-name
description: Does X, Y, Z. Use when [conditions]. Trigger with "phrase 1", "phrase 2".
---

# My Skill Name

Brief purpose (1-2 sentences).

## Overview

What + when + capabilities.

## Prerequisites

- Required dependency 1
- `ENV_VAR`: Description

## Instructions

### Step 1: [Action]
[Instructions]

### Step 2: [Action]
[Instructions]

## Output

- Artifact 1
- Artifact 2

## Error Handling

1. **Error**: Common failure
   **Solution**: How to fix

## Examples

### Example 1: [Scenario]
**Input**: [Example]
**Output**: [Result]

## Resources

- Advanced: `{baseDir}/references/ADVANCED.md`
```

### Size Limits

| Element | Limit |
|---------|-------|
| `name` | 64 chars |
| `description` | 1,024 chars |
| SKILL.md body | ~500 lines / 5,000 tokens |
| Total upload | 8MB |
| Available skills budget | 15,000 chars |

### Critical Rules

1. **Descriptions must include**: What it does + "Use when" + trigger phrases
2. **Use third person** in descriptions
3. **Keep SKILL.md under 500 lines**
4. **Use `{baseDir}`** for all paths
5. **Forward slashes only** in file paths
6. **One-level-deep references** only
7. **Execute code, don't read** into context
8. **Test with all models** (Haiku, Sonnet, Opus)

---

## References

### Primary Source

- [Lee Han Chung Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/) - Complete technical reference

### Official Anthropic Documentation

- [Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Agent Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Equipping Agents for the Real World](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

---

**Last Updated**: 2025-12-06
**Maintained By**: Intent Solutions (Jeremy Longshore)
**For**: Nixtla (Max Mergenthaler)
**Status**: MASTER STANDARD - Single Source of Truth
