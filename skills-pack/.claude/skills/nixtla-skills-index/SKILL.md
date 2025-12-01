---
name: nixtla-skills-index
description: "List all installed Nixtla skills and describe when to use each - invoke when asking about available Nixtla capabilities or which skill to use"
allowed-tools: "Read,Glob"
version: "1.0.0"
---

# Purpose

List all Nixtla skills installed in this project and provide guidance on when to use each skill.

## Overview

This skill scans the `.claude/skills/` directory for `nixtla-*` skill directories, reads their SKILL.md frontmatter, and outputs a human-readable index of available skills with usage guidance.

**Use this skill when**:
- You want to see what Nixtla skills are available
- You need guidance on which skill to use for a specific task
- You want to understand the Nixtla Skills Pack capabilities

## Prerequisites

- Nixtla skills installed via `nixtla-skills init`
- Skills located in `.claude/skills/nixtla-*/`

## Instructions

### Step 1: Scan for Nixtla Skills

Use the Glob tool to find all Nixtla skill directories:

```
Glob pattern: .claude/skills/nixtla-*/SKILL.md
```

### Step 2: Read Skill Frontmatter

For each skill found, read the SKILL.md file and extract:
- `name`: Skill identifier
- `description`: What the skill does and when to use it
- `mode`: Whether this is a mode skill (changes Claude's behavior)
- `disable-model-invocation`: Whether skill requires explicit invocation

### Step 3: Classify and Format

Organize skills into categories:
1. **Mode Skills** (`mode: true`) - Change Claude's overall behavior
2. **Utility Skills** - Perform specific tasks
3. **Infrastructure Skills** (`disable-model-invocation: true`) - System operations

### Step 4: Output Index

Present a formatted index with:
- Skill name (as command)
- Brief description
- When to use it

## Output

Formatted markdown listing all Nixtla skills:

```markdown
## Nixtla Skills Index

### Mode Skills (change Claude's behavior)

| Skill | Description | When to Use |
|-------|-------------|-------------|
| nixtla-timegpt-lab | Transforms Claude into Nixtla forecasting expert | Starting any Nixtla forecasting work |

### Utility Skills (perform specific tasks)

| Skill | Description | When to Use |
|-------|-------------|-------------|
| nixtla-schema-mapper | Map data to Nixtla format | You have data to transform |
| nixtla-experiment-architect | Scaffold experiments | Setting up model comparisons |
| nixtla-timegpt-finetune-lab | Fine-tune TimeGPT | Improving accuracy on your data |
| nixtla-prod-pipeline-generator | Generate pipelines | Deploying to production |
| nixtla-usage-optimizer | Audit and optimize | Reducing costs, understanding usage |
| nixtla-skills-index | List available skills | Finding the right skill |

### Infrastructure Skills (explicit invocation only)

| Skill | Description | When to Use |
|-------|-------------|-------------|
| nixtla-skills-bootstrap | Install/update skills | First-time setup or updating |
```

## Error Handling

### No Skills Found

If no `nixtla-*` directories found in `.claude/skills/`:

```
No Nixtla skills installed in this project.

To install Nixtla skills:
1. pip install nixtla-claude-skills-installer
2. nixtla-skills init

Or ask: "Install Nixtla skills"
```

### Malformed SKILL.md

If a skill's SKILL.md cannot be parsed:

```
⚠️ Warning: Could not read {skill-name}/SKILL.md
   Skill may be corrupted. Try: nixtla-skills update
```

## Examples

### Example 1: List All Skills

**User**: "What Nixtla skills are available?"

**Action**: Scan `.claude/skills/nixtla-*`, read frontmatter, output formatted index.

**Output**: Full skills index table (see Output section).

### Example 2: Find Right Skill

**User**: "Which skill should I use to convert my CSV to Nixtla format?"

**Action**: Scan skills, identify `nixtla-schema-mapper` as best match.

**Output**:
```
For converting CSV to Nixtla format, use: **nixtla-schema-mapper**

This skill:
- Analyzes your data source (CSV, SQL, Parquet)
- Generates transformation code
- Creates schema documentation

To activate: "Use nixtla-schema-mapper on my data.csv"
```

### Example 3: No Skills Installed

**User**: "List Nixtla skills" (in project without skills)

**Action**: Scan `.claude/skills/`, find no `nixtla-*` directories.

**Output**: Installation instructions (see Error Handling).

## Resources

- Skill standard specification: `{baseDir}/../../../000-docs/041-SPEC-nixtla-skill-standard.md`
- Architecture overview: `{baseDir}/../../../000-docs/038-AT-ARCH-nixtla-claude-skills-pack.md`
