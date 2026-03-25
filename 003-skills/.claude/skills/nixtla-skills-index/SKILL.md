---
name: nixtla-skills-index
description: "Analyze and categorize installed Nixtla Skills for forecasting guidance. Use when seeing available skills or selecting the right one. Trigger with 'list nixtla skills' or 'what skills'."
allowed-tools: "Read,Glob"
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
compatible-with: claude-code
tags: [nixtla, time-series, skills-management, discovery, documentation]
---

# Nixtla Skills Index

List all installed Nixtla Skills and provide usage guidance for selecting the right skill.

## Overview

This skill generates a directory of available Nixtla Skills:

- **Discovery**: Scans `.claude/skills/nixtla-*/` directories for installed skills
- **Classification**: Categorizes by type (mode, utility, infrastructure) based on skill metadata
- **Guidance**: Recommends skills based on user tasks using description matching
- **Formatted output**: Human-readable index table with skill names, descriptions, and trigger phrases

## Prerequisites

**Required**:
- Nixtla Skills installed via `nixtla-skills init`
- Skills in `.claude/skills/nixtla-*/` directories

**No Additional Packages**: Uses only Read and Glob tools for zero-dependency operation.

## Instructions

### Step 1: Scan for Skills

Find all Nixtla skill directories by searching for SKILL.md files:
```
Glob pattern: .claude/skills/nixtla-*/SKILL.md
```

### Step 2: Read Frontmatter

For each skill, extract metadata fields:
- `name`: Skill identifier used for activation
- `description`: Purpose, trigger phrases, and usage context
- `mode`: Whether it is a mode skill that changes overall behavior
- `version`: Current installed version number

### Step 3: Classify Skills

Organize discovered skills into categories for clear presentation:
- **Mode Skills**: Change overall Claude behavior (e.g., forecasting expert mode)
- **Utility Skills**: Perform specific tasks (e.g., data transformation, experiment setup)
- **Infrastructure Skills**: System operations (e.g., install, update, index)

### Step 4: Generate Index

Output a formatted markdown table with skill details, organized by category.

## Output

Formatted markdown listing organized by category:

```markdown
## Nixtla Skills Index

| Skill | Description | When to Use |
|-------|-------------|-------------|
| nixtla-timegpt-lab | Forecasting expert mode | Starting Nixtla work |
| nixtla-schema-mapper | Data transformation | Converting data format |
| nixtla-experiment-architect | Experiment setup | Model comparisons |
```

## Error Handling

1. **Error**: `No skills found`
   **Solution**: Run `nixtla-skills init` to install the Nixtla skills suite

2. **Error**: `Malformed SKILL.md`
   **Solution**: Run `nixtla-skills update` to refresh corrupted skill files

3. **Error**: `Skills directory not found`
   **Solution**: Verify `.claude/skills/` exists in the project root

4. **Error**: `Permission denied`
   **Solution**: Check read permissions on the skills directory

## Examples

See [examples](references/examples.md) for detailed usage scenarios.

## Resources

- Skills Directory: `.claude/skills/nixtla-*/`
- Installer: `pip install nixtla-claude-skills-installer`

**Related Skills**:
- `nixtla-skills-bootstrap`: Install or update skills
