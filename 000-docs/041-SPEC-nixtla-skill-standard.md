# Nixtla SKILL Standard Specification

**Document ID**: 041-SPEC-nixtla-skill-standard.md
**Version**: 2.0.0
**Status**: Active
**Created**: 2025-12-01
**Updated**: 2025-12-06
**Standard Reference**: [Claude Skills Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)

---

## Overview

This document defines the **Nixtla SKILL standard** for all Claude Code skills in the Nixtla Skills Pack. All skills MUST conform to this specification to ensure consistency, discoverability, and compliance with Claude Code's skill architecture.

---

## 1. YAML Frontmatter Specification

Every Nixtla skill MUST have a YAML frontmatter section at the top of `SKILL.md` with the following structure:

### 1.1 Complete Schema

```yaml
---
# 🔴 REQUIRED FIELDS
name: nixtla-<short-name>                     # 64 chars max, lowercase + hyphens
description: >                                 # 1024 chars max, LLM selection trigger
  Action-oriented description with "Use when" context.
  Must be explicit enough for Claude's LLM reasoning to match user intent.

# 🟡 OPTIONAL FIELDS (all functional in Claude Code)
allowed-tools: "Read,Write,Glob,Grep,Edit"    # Tools accessible during execution
model: inherit                                 # Model override (or specific model ID)
version: "1.0.0"                              # Semantic versioning
license: "Proprietary"                        # License reference (if needed)

# 🟠 BEHAVIORAL FLAGS
mode: false                                    # true = mode skill (prominent UI section)
disable-model-invocation: false                # true = requires manual /skill-name
---
```

### 1.2 Field Reference

| Field | Type | Required | Max | Purpose |
|-------|------|----------|-----|---------|
| `name` | string | 🔴 YES | 64 chars | Skill identifier; becomes `Skill` tool's `command` input |
| `description` | string | 🔴 YES | 1024 chars | Triggers skill selection via LLM reasoning |
| `allowed-tools` | CSV string | 🟡 Recommended | - | Tools accessible during execution |
| `model` | string | 🟡 No | - | Model override (e.g., `"claude-opus-4-20250514"` or `"inherit"`) |
| `version` | string | 🟡 No | - | Semantic versioning for tracking |
| `license` | string | 🟡 No | - | License terms reference |
| `mode` | boolean | 🟡 No | - | If `true`, appears in prominent UI section |
| `disable-model-invocation` | boolean | 🟡 No | - | If `true`, requires manual `/skill-name` |

### 1.3 Allowed-Tools Syntax

```yaml
# Multiple tools (comma-separated)
allowed-tools: "Read,Write,Bash,Glob,Grep,Edit"

# Scoped bash commands (restrict to specific commands)
allowed-tools: "Bash(git status:*),Bash(git diff:*),Read"

# Minimal read-only
allowed-tools: "Read,Glob,Grep"
```

**Design principle:** Include only tools actually needed to minimize attack surface.

### 1.4 Forbidden Fields

These fields MUST NOT be used in Nixtla skills:

| Field | Reason |
|-------|--------|
| `author` | Not in Claude Skills standard |
| `priority` | Not in Claude Skills standard |
| `audience` | Not in Claude Skills standard |
| `when_to_use` | ⚠️ Undocumented, status unclear - use `description` instead |

---

## 2. Markdown Body Structure

The markdown body of `SKILL.md` MUST follow this section order:

```markdown
# Purpose

Brief statement of what this skill does (1-2 sentences).

## Overview

When to use this skill, what problems it solves, and key capabilities.

## Prerequisites

Required tools, files, API keys, environment setup, and dependencies.

## Instructions

Step-by-step workflow with imperative verbs.
Break into numbered steps and subsections for complex workflows.

## Output

What artifacts this skill produces (files, configs, reports, etc.).

## Error Handling

Common failure scenarios and how to handle them.

## Examples

At least 1-2 concrete usage examples with expected inputs/outputs.

## Resources

Links to files in references/, scripts/, assets/ using {baseDir} variable.
```

### 2.1 Content Guidelines

| Guideline | Requirement |
|-----------|-------------|
| Word limit | SKILL.md SHOULD be under 5,000 words |
| Language | Use imperative verbs ("Analyze...", "Generate...", "Validate...") |
| Paths | Use `{baseDir}` variable, NEVER hardcode absolute paths |
| Examples | Include at least 1 concrete example per skill |
| Error handling | Document all anticipated failure modes |

---

## 3. Resource Directory Layout

Every Nixtla skill MUST have this directory structure:

```
skills-pack/.claude/skills/nixtla-<skill-name>/
├── SKILL.md           # Core prompt (required)
├── scripts/           # Executable Python/Bash scripts (optional)
├── references/        # Long-form docs, schemas, guides (optional)
└── assets/            # Templates, configs, static files (optional)
```

### 3.1 Directory Purposes

| Directory | Purpose | Access Pattern |
|-----------|---------|----------------|
| `scripts/` | Executable code for deterministic operations | Invoked via `Bash` tool with `{baseDir}` |
| `references/` | Documentation loaded into context when needed | Read via `Read` tool with `{baseDir}` |
| `assets/` | Templates/configs referenced by path | Referenced by path, not read by default |

### 3.2 Path References

Always use `{baseDir}` variable to reference files:

```markdown
## Resources

- Configuration templates: `{baseDir}/assets/config-template.yml`
- API reference: `{baseDir}/references/api-docs.md`
- Validation script: `{baseDir}/scripts/validate.py`
```

---

## 4. Skill Classification

Nixtla skills are classified into three types:

### 4.1 Mode Skills

**Characteristics**:
- Change Claude's overall behavior for the session
- Set `mode: true` in frontmatter
- Typically broader tool permissions
- Only ONE mode skill: `nixtla-timegpt-lab`

**Example**:
```yaml
---
name: nixtla-timegpt-lab
description: "Mode skill that transforms Claude into a Nixtla TimeGPT forecasting expert"
mode: true
allowed-tools: "Read,Write,Glob,Grep,Edit,Bash"
version: "1.0.0"
---
```

### 4.2 Utility Skills

**Characteristics**:
- Perform specific, focused tasks
- Set `mode: false` (default)
- Minimal tool permissions
- Most Nixtla skills are utility skills

**Examples**:
- `nixtla-schema-mapper` - Data transformation
- `nixtla-experiment-architect` - Experiment scaffolding
- `nixtla-usage-optimizer` - Cost analysis

**Example**:
```yaml
---
name: nixtla-schema-mapper
description: "Infer data schema and generate Nixtla-compatible transformations"
allowed-tools: "Read,Write,Glob,Grep,Edit"
version: "1.0.0"
---
```

### 4.3 Infrastructure/Dangerous Skills

**Characteristics**:
- Run installers, CLI commands, or modify system state
- Set `disable-model-invocation: true`
- Should only be invoked explicitly by user
- Minimal but specific tool permissions

**Examples**:
- `nixtla-skills-bootstrap` - Install/update skills

**Example**:
```yaml
---
name: nixtla-skills-bootstrap
description: "Install or update Nixtla Claude Skills via nixtla-skills CLI"
allowed-tools: "Bash,Read,Glob"
disable-model-invocation: true
version: "1.0.0"
---
```

---

## 5. Tool Permission Guidelines

### 5.1 Principle of Least Privilege

Grant ONLY the tools each skill actually requires:

| Tool | Use Case | Grant When |
|------|----------|------------|
| `Read` | Reading files | Almost always needed |
| `Write` | Creating new files | Skill generates files |
| `Edit` | Modifying existing files | Skill modifies files |
| `Glob` | Finding files by pattern | Skill searches for files |
| `Grep` | Searching file contents | Skill searches within files |
| `Bash` | Running shell commands | Skill runs CLI tools |

### 5.2 Recommended Permission Sets

| Skill Type | Recommended Tools |
|------------|-------------------|
| Read-only audit | `"Read,Glob,Grep"` |
| Data transformation | `"Read,Write,Glob,Grep,Edit"` |
| Experiment scaffolding | `"Read,Write,Glob,Grep,Edit,Bash"` |
| CLI/Installer | `"Bash,Read,Glob"` |

### 5.3 Scoped Permissions

For CLI skills, consider scoping Bash permissions:

```yaml
allowed-tools: "Bash(git:*),Read,Glob"  # Only git commands
allowed-tools: "Bash(nixtla-skills:*),Read,Glob"  # Only nixtla-skills CLI
```

---

## 6. Nixtla Skills Inventory

Current Nixtla skills and their classifications:

| Skill | Type | mode | disable-model-invocation | Tools |
|-------|------|------|-------------------------|-------|
| `nixtla-timegpt-lab` | Mode | `true` | `false` | Read,Write,Glob,Grep,Edit,Bash |
| `nixtla-experiment-architect` | Utility | `false` | `false` | Read,Write,Glob,Grep,Edit,Bash |
| `nixtla-schema-mapper` | Utility | `false` | `false` | Read,Write,Glob,Grep,Edit |
| `nixtla-timegpt-finetune-lab` | Utility | `false` | `false` | Read,Write,Glob,Grep,Edit,Bash |
| `nixtla-prod-pipeline-generator` | Utility | `false` | `false` | Read,Write,Glob,Grep,Edit,Bash |
| `nixtla-usage-optimizer` | Utility | `false` | `false` | Read,Glob,Grep |
| `nixtla-skills-bootstrap` | Infra | `false` | `true` | Bash,Read,Glob |
| `nixtla-skills-index` | Utility | `false` | `false` | Read,Glob |

---

## 7. Versioning

### 7.1 Semantic Versioning

All skills use semantic versioning (MAJOR.MINOR.PATCH):

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Breaking changes to interface | MAJOR | 1.0.0 → 2.0.0 |
| New features, additive changes | MINOR | 1.0.0 → 1.1.0 |
| Bug fixes, clarifications | PATCH | 1.0.0 → 1.0.1 |

### 7.2 Version Tracking

- Each skill tracks version in `SKILL.md` frontmatter
- Skills Pack version tracked in `skills-pack/VERSION`
- CHANGELOG maintained at repo root

---

## 8. Validation Checklist

Before merging any skill changes, verify:

### 8.1 Frontmatter Compliance

- [ ] Has `name` matching folder name
- [ ] Has action-oriented `description`
- [ ] Has `version` in semver format
- [ ] Has minimal `allowed-tools`
- [ ] NO deprecated fields (author, priority, audience)
- [ ] `mode: true` only for nixtla-timegpt-lab
- [ ] `disable-model-invocation: true` only for infra skills

### 8.2 Structure Compliance

- [ ] Has `scripts/` directory (can be empty)
- [ ] Has `references/` directory (can be empty)
- [ ] Has `assets/` directory (can be empty)
- [ ] Uses `{baseDir}` for all path references
- [ ] No hardcoded absolute paths

### 8.3 Content Compliance

- [ ] SKILL.md under 5,000 words (or content in references/)
- [ ] Uses imperative language
- [ ] Has all required sections (Purpose, Overview, Prerequisites, etc.)
- [ ] Includes at least 1 concrete example
- [ ] Documents error handling

---

## 9. Related Documents

- [038-AT-ARCH-nixtla-claude-skills-pack.md](038-AT-ARCH-nixtla-claude-skills-pack.md) - Architecture overview
- [085-QA-AUDT-claude-skills-compliance-audit.md](085-QA-AUDT-claude-skills-compliance-audit.md) - Compliance audit
- [Claude Skills Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/) - External standard reference

---

**Last Updated**: 2025-12-01
**Maintained By**: Intent Solutions (Jeremy Longshore)
**For**: Nixtla (Max Mergenthaler)
