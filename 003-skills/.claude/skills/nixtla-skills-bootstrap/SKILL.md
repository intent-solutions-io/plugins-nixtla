---
name: nixtla-skills-bootstrap
description: "Generate and configure Nixtla Skills using the CLI for forecasting workflows. Use when installing or updating skills. Trigger with 'install nixtla skills' or 'update nixtla'."
allowed-tools: "Read,Glob,Grep"
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
compatible-with: claude-code
tags: [nixtla, time-series, skills-management, installation, cli]
---

# Nixtla Skills Bootstrap

Install or update Nixtla Skills in the current project using the nixtla-skills CLI.

## Overview

This skill manages Nixtla Skills installation and lifecycle:

- **Init**: First-time installation to `.claude/skills/`, creating all skill directories and SKILL.md files
- **Update**: Refresh existing skills to latest versions while preserving local customizations
- **Verify**: Check installation status, list available skills, and confirm version consistency

Skills persist locally until explicitly updated or removed.

## Prerequisites

**Required**:
- Python 3.8+
- `nixtla-skills` CLI tool

**Installation**:
```bash
pip install nixtla-claude-skills-installer
```

**Verify CLI**:
```bash
which nixtla-skills || echo "NOT_FOUND"
```

## Instructions

### Step 1: Choose Action

Select installation mode based on current state:
- `init` - First-time installation (creates `.claude/skills/` and populates all skill directories)
- `update` - Refresh existing skills to latest available version

### Step 2: Check CLI Availability

Verify nixtla-skills CLI is installed and accessible:
```bash
nixtla-skills --version
```

If not found, install with: `pip install nixtla-claude-skills-installer`

### Step 3: Run Installer

**For init**:
```bash
nixtla-skills init
```

**For update**:
```bash
nixtla-skills update
```

### Step 4: Verify Installation

Confirm all skill directories are present and contain valid SKILL.md files:
```bash
ls -1d .claude/skills/nixtla-* 2>/dev/null | sort
```

## Output

After installation, the following skill directories are created:
- `.claude/skills/nixtla-timegpt-lab/` - Core forecasting skill
- `.claude/skills/nixtla-experiment-architect/` - Experiment scaffolding
- `.claude/skills/nixtla-schema-mapper/` - Data transformation
- `.claude/skills/nixtla-skills-bootstrap/` - This skill (self-referential)

## Error Handling

1. **Error**: `nixtla-skills: command not found`
   **Solution**: `pip install nixtla-claude-skills-installer`

2. **Error**: `Permission denied`
   **Solution**: Check write permissions on `.claude/skills/` directory

3. **Error**: `Skills directory already exists`
   **Solution**: Use `update` instead of `init` to refresh existing skills

4. **Error**: `No skills installed after completion`
   **Solution**: Verify CLI version with `nixtla-skills --version` and check for error output

## Examples

See [examples](references/examples.md) for detailed usage scenarios.

## Resources

- PyPI Package: https://pypi.org/project/nixtla-claude-skills-installer/
- Skills Documentation: See individual skill SKILL.md files
- GitHub: https://github.com/Nixtla/nixtla-claude-skills

**Installed location**: `.claude/skills/nixtla-skills-bootstrap/`
