# Nixtla Claude Skills - DevOps Operations Guide

**Comprehensive guide for installing, updating, versioning, and maintaining Nixtla Claude Skills in production projects**

---

## Document Metadata

| Field | Value |
|-------|-------|
| **Document Type** | OD - Overview & Documentation |
| **Version** | 0.4.0 |
| **Phase** | Phase 4 - Production Readiness |
| **Created** | 2025-12-03 |
| **Status** | Complete |

---

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Updates and Versioning](#updates-and-versioning)
4. [Version Conflicts](#version-conflicts)
5. [Rollback Procedures](#rollback-procedures)
6. [CI/CD Integration](#cicd-integration)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)

---

## Overview

### What Are Nixtla Claude Skills?

Nixtla Claude Skills are AI-powered assistants for Claude Code that accelerate forecasting workflows. They provide:

- **Expert guidance** on TimeGPT and Nixtla libraries
- **Code generation** for experiments, pipelines, and transformations
- **Best practices** for production forecasting systems

### Skills Pack Components

| Component | Description | Version |
|-----------|-------------|---------|
| **Installer CLI** | `nixtla-skills` command for install/update | 0.4.0 |
| **Core Skills** | 3 foundational skills (timegpt-lab, experiment-architect, schema-mapper) | 0.4.0 |
| **Advanced Skills** | 3 production skills (finetune-lab, prod-pipeline, usage-optimizer) | 0.4.0 |
| **Infrastructure** | Bootstrap skill, skills index | 0.4.0 |

### Per-Project Installation Model

Nixtla Skills use a **per-project** installation model:

- Skills installed in `.claude/skills/nixtla-*` within each project
- **Not** global CLI installation
- Each project can have different skill versions
- Version tracked in each SKILL.md frontmatter

---

## Installation

### Prerequisites

- **Python 3.8+** (for installer CLI)
- **Claude Code** installed and configured
- **Git** (for cloning skills pack repo)

### Initial Installation

#### Option 1: From Repository (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/intent-solutions-io/plugins-nixtla.git
cd plugins-nixtla

# 2. Install the CLI tool
cd packages/nixtla-claude-skills-installer
pip install -e .

# 3. Navigate to your project
cd /path/to/your/project

# 4. Install skills
nixtla-skills init

# 5. Verify installation
ls .claude/skills/nixtla-*
```

#### Option 2: From PyPI (When Available)

```bash
# Install CLI globally
pip install nixtla-claude-skills-installer

# Navigate to your project
cd /path/to/your/project

# Install skills
nixtla-skills init
```

### Installation Output

```
Nixtla Claude Skills Installer v0.4.0
=====================================

Installing skills from: /path/to/plugins-nixtla/skills-pack

Skills to install:
   New skills: 7
      + nixtla-timegpt-lab (v0.4.0)
      + nixtla-experiment-architect (v0.4.0)
      + nixtla-schema-mapper (v0.4.0)
      + nixtla-timegpt-finetune-lab (v0.4.0)
      + nixtla-prod-pipeline-generator (v0.4.0)
      + nixtla-usage-optimizer (v0.4.0)
      + nixtla-skills-bootstrap (v0.4.0)

Proceed with installation? [y/N]: y

Copying skills to .claude/skills/...
✓ Installed 7 skills

✅ Installed Nixtla Skills (7):
   - nixtla-timegpt-lab v0.4.0
   - nixtla-experiment-architect v0.4.0
   - nixtla-schema-mapper v0.4.0
   - nixtla-timegpt-finetune-lab v0.4.0
   - nixtla-prod-pipeline-generator v0.4.0
   - nixtla-usage-optimizer v0.4.0
   - nixtla-skills-bootstrap v0.4.0

Skills installed successfully!
```

### Verification

```bash
# Check skills directory
ls -la .claude/skills/nixtla-*/

# Check versions
grep "version:" .claude/skills/nixtla-*/SKILL.md

# Try a skill in Claude Code
# Open Claude Code and type: "Use nixtla-timegpt-lab"
```

---

## Updates and Versioning

### Semantic Versioning

Nixtla Skills follow **semver** (MAJOR.MINOR.PATCH):

```
0.4.0
│ │ │
│ │ └─ PATCH: Bug fixes, doc updates, clarifications
│ └─── MINOR: New features, new skills, additive changes
└───── MAJOR: Breaking changes, architectural shifts
```

### Version Synchronization

All core components share the same version:

| Component | Version | Synchronized |
|-----------|---------|--------------|
| Skills Pack | 0.4.0 | ✅ |
| Installer CLI | 0.4.0 | ✅ |
| Core Skills (3) | 0.4.0 | ✅ |
| Advanced Skills (3) | 0.4.0 | ✅ |
| Infrastructure Skills (2) | 0.4.0 | ✅ |

### Checking for Updates

```bash
# Update skills pack repo
cd /path/to/plugins-nixtla
git pull origin main

# Check current project versions
cd /path/to/your/project
grep "version:" .claude/skills/nixtla-*/SKILL.md | sort -u

# Output:
# version: "0.3.0"  ← Current version
# Latest available: 0.4.0 (from repo)
```

### Updating Skills

```bash
# Navigate to your project
cd /path/to/your/project

# Run update command
nixtla-skills update

# Review changes
# Output shows version transitions (0.3.0 → 0.4.0)
```

#### Update Output

```
Nixtla Claude Skills Installer v0.4.0
=====================================

Updating skills from: /path/to/plugins-nixtla/skills-pack

Current installation found (7 skills)

Skills to update:
   Existing skills (will overwrite): 7
      ↻ nixtla-timegpt-lab (v0.3.0 → v0.4.0)
      ↻ nixtla-experiment-architect (v0.3.0 → v0.4.0)
      ↻ nixtla-schema-mapper (v0.3.0 → v0.4.0)
      ↻ nixtla-timegpt-finetune-lab (v0.3.0 → v0.4.0)
      ↻ nixtla-prod-pipeline-generator (v0.3.0 → v0.4.0)
      ↻ nixtla-usage-optimizer (v0.3.0 → v0.4.0)
      ↻ nixtla-skills-bootstrap (v0.3.0 → v0.4.0)

Proceed with update? [y/N]: y

Copying skills to .claude/skills/...
✓ Updated 7 skills

✅ Updated Nixtla Skills (7):
   - nixtla-timegpt-lab v0.4.0
   - nixtla-experiment-architect v0.4.0
   - nixtla-schema-mapper v0.4.0
   - nixtla-timegpt-finetune-lab v0.4.0
   - nixtla-prod-pipeline-generator v0.4.0
   - nixtla-usage-optimizer v0.4.0
   - nixtla-skills-bootstrap v0.4.0

Skills updated successfully!
```

### Selective Updates

To update only specific skills:

```bash
# Manual update (advanced)
cp -r /path/to/plugins-nixtla/skills-pack/.claude/skills/nixtla-timegpt-lab \
      .claude/skills/

# Verify version
grep "version:" .claude/skills/nixtla-timegpt-lab/SKILL.md
```

---

## Version Conflicts

### Scenario 1: Outdated Skills in Project

**Problem**: Project has v0.2.0, pack has v0.4.0

**Detection**:
```bash
cd /path/to/your/project
nixtla-skills update

# Output shows version mismatch
"↻ nixtla-timegpt-lab (v0.2.0 → v0.4.0)"
```

**Resolution**:
```bash
# Run update
nixtla-skills update
# Accept update when prompted
```

**Impact**: Low (skills are additive, backward compatible in MINOR versions)

### Scenario 2: Modified Skills in Project

**Problem**: Local modifications to skill files

**Detection**:
```bash
git status .claude/skills/nixtla-*

# Output:
# modified: .claude/skills/nixtla-timegpt-lab/SKILL.md
```

**Resolution**:

```bash
# Option A: Backup and update
cp -r .claude/skills/nixtla-timegpt-lab .claude/skills/nixtla-timegpt-lab.backup
nixtla-skills update

# Option B: Keep local modifications
# Don't run update, accept staying on older version
```

**Best Practice**: Don't modify skills directly. Use project-specific configs instead.

### Scenario 3: MAJOR Version Change

**Problem**: Skills pack upgraded to v1.0.0 (MAJOR version)

**Detection**:
```bash
cd /path/to/plugins-nixtla
git pull
cat VERSION

# Output: 1.0.0 (was 0.4.0)
```

**Resolution**:

```bash
# Read CHANGELOG for breaking changes
cat CHANGELOG.md | head -50

# Test in non-production project first
cd /path/to/test/project
nixtla-skills init  # Fresh install of v1.0.0

# Verify compatibility
# Then update production projects
```

**Impact**: High (breaking changes possible)

### Scenario 4: Multiple Projects, Different Versions

**Problem**: Project A has v0.3.0, Project B has v0.4.0

**Resolution**: This is **by design**. Per-project installation allows:

- Project A continues with v0.3.0 (stable)
- Project B uses v0.4.0 (new features)
- Update Project A when ready

**No action needed** unless you want consistent versions across all projects.

---

## Rollback Procedures

### Rollback Strategy

Skills use **file-based rollback** (not package manager rollback).

### Scenario 1: Rollback After Update

**Problem**: Updated to v0.4.0, experiencing issues

**Solution**:

```bash
# 1. Check skills pack repo for previous version
cd /path/to/plugins-nixtla
git log --oneline | head -10

# Find commit for v0.3.0
# Example: abc123 - release(v0.3.0): Phase 3 complete

# 2. Checkout previous version
git checkout abc123

# 3. Update project to old version
cd /path/to/your/project
nixtla-skills update

# This will "update" to the older v0.3.0 from checked-out repo
```

### Scenario 2: Emergency Rollback

**Problem**: Skills completely broken, need immediate fix

**Solution**:

```bash
# Option A: Remove skills entirely
rm -rf .claude/skills/nixtla-*

# Work without skills temporarily

# Option B: Restore from backup (if you made one)
cp -r .claude/skills.backup/nixtla-* .claude/skills/
```

### Scenario 3: Rollback Single Skill

**Problem**: Only one skill (e.g., nixtla-prod-pipeline-generator) has issues

**Solution**:

```bash
# 1. Remove problematic skill
rm -rf .claude/skills/nixtla-prod-pipeline-generator

# 2. Checkout previous version from repo
cd /path/to/plugins-nixtla
git checkout v0.3.0 -- skills-pack/.claude/skills/nixtla-prod-pipeline-generator

# 3. Copy to project
cp -r skills-pack/.claude/skills/nixtla-prod-pipeline-generator \
      /path/to/your/project/.claude/skills/

# 4. Verify
grep "version:" /path/to/your/project/.claude/skills/nixtla-prod-pipeline-generator/SKILL.md
# Output: version: "0.3.0"
```

### Rollback Best Practices

1. **Backup before update**:
   ```bash
   cp -r .claude/skills .claude/skills.backup.$(date +%Y%m%d)
   ```

2. **Test in dev first**:
   - Update dev project first
   - Verify skills work
   - Then update staging/prod

3. **Version control skills directory**:
   ```bash
   # Add to git
   git add .claude/skills
   git commit -m "chore: update Nixtla skills to v0.4.0"
   
   # Rollback via git
   git revert HEAD
   ```

---

## CI/CD Integration

### GitHub Actions

#### Workflow: Install Skills on CI

```yaml
# .github/workflows/install-skills.yml
name: Install Nixtla Skills

on:
  push:
    branches: [main, develop]
  pull_request:

jobs:
  install-skills:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout project repo
        uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Clone Nixtla Skills Pack
        run: |
          git clone https://github.com/intent-solutions-io/plugins-nixtla.git /tmp/plugins-nixtla
      
      - name: Install Nixtla Skills CLI
        run: |
          cd /tmp/plugins-nixtla/packages/nixtla-claude-skills-installer
          pip install -e .
      
      - name: Install skills
        run: |
          nixtla-skills init
      
      - name: Verify installation
        run: |
          ls -la .claude/skills/nixtla-*/
          grep "version:" .claude/skills/nixtla-*/SKILL.md
      
      - name: Run tests
        run: |
          pytest tests/
```

#### Workflow: Check Skills Versions

```yaml
# .github/workflows/check-skills-version.yml
name: Check Skills Version

on: [push, pull_request]

jobs:
  check-version:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Extract skills versions
        id: versions
        run: |
          VERSIONS=$(grep "version:" .claude/skills/nixtla-*/SKILL.md | sort -u)
          echo "versions=$VERSIONS" >> $GITHUB_OUTPUT
      
      - name: Check version consistency
        run: |
          VERSION_COUNT=$(grep "version:" .claude/skills/nixtla-*/SKILL.md | sort -u | wc -l)
          
          if [ $VERSION_COUNT -gt 1 ]; then
            echo "Error: Multiple skill versions detected"
            grep "version:" .claude/skills/nixtla-*/SKILL.md | sort
            exit 1
          fi
          
          echo "✓ All skills have consistent versions"
```

### GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - setup
  - test

install-nixtla-skills:
  stage: setup
  image: python:3.10
  script:
    - git clone https://github.com/intent-solutions-io/plugins-nixtla.git /tmp/plugins-nixtla
    - cd /tmp/plugins-nixtla/packages/nixtla-claude-skills-installer
    - pip install -e .
    - cd $CI_PROJECT_DIR
    - nixtla-skills init
    - ls -la .claude/skills/nixtla-*/
  artifacts:
    paths:
      - .claude/skills/
    expire_in: 1 hour

test:
  stage: test
  dependencies:
    - install-nixtla-skills
  script:
    - pytest tests/
```

### Docker Integration

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install Nixtla Skills
RUN git clone https://github.com/intent-solutions-io/plugins-nixtla.git /tmp/plugins-nixtla && \
    cd /tmp/plugins-nixtla/packages/nixtla-claude-skills-installer && \
    pip install -e . && \
    cd /app && \
    nixtla-skills init && \
    rm -rf /tmp/plugins-nixtla

# Copy project files
COPY . .

# Verify skills installed
RUN ls -la .claude/skills/nixtla-*/

# Your app entrypoint
CMD ["python", "main.py"]
```

---

## Troubleshooting

### Issue 1: `nixtla-skills: command not found`

**Cause**: Installer CLI not installed or not in PATH

**Solution**:
```bash
# Check if installed
pip list | grep nixtla-skills

# If not found, install
cd /path/to/plugins-nixtla/packages/nixtla-claude-skills-installer
pip install -e .

# Verify
nixtla-skills --help
```

### Issue 2: Skills not appearing in Claude Code

**Cause**: Skills not in `.claude/skills/` or incorrect structure

**Solution**:
```bash
# Check structure
ls -la .claude/skills/nixtla-*/

# Should see:
# .claude/skills/nixtla-timegpt-lab/SKILL.md
# .claude/skills/nixtla-experiment-architect/SKILL.md
# etc.

# If missing, reinstall
nixtla-skills init
```

### Issue 3: Version mismatch warnings

**Cause**: Some skills at v0.3.0, others at v0.4.0

**Solution**:
```bash
# Check versions
grep "version:" .claude/skills/nixtla-*/SKILL.md

# Update to sync all
nixtla-skills update
```

### Issue 4: Permission errors during installation

**Cause**: No write access to `.claude/skills/`

**Solution**:
```bash
# Check permissions
ls -ld .claude/skills

# Fix permissions
chmod -R u+w .claude/skills

# Retry
nixtla-skills init
```

### Issue 5: Skills installed but CLI shows older version

**Cause**: CLI version != skills version (expected in transition periods)

**Solution**:
```bash
# Check CLI version
nixtla-skills --version

# Check skills versions
grep "version:" .claude/skills/nixtla-*/SKILL.md

# Update CLI if needed
cd /path/to/plugins-nixtla/packages/nixtla-claude-skills-installer
git pull
pip install -e . --upgrade
```

---

## Best Practices

### 1. Version Control Integration

**Commit skills to git**:
```bash
# Add skills to git
git add .claude/skills/nixtla-*
git commit -m "chore: install Nixtla skills v0.4.0"

# Benefits:
# - Team consistency
# - Version history
# - Easy rollback
```

**Ignore vs. commit**:
```gitignore
# .gitignore

# ❌ DON'T ignore skills if you want team consistency
# .claude/skills/

# ✅ DO commit skills for reproducibility
```

### 2. Update Strategy

**Dev → Staging → Production**:
```bash
# 1. Update dev environment
cd /path/to/dev/project
nixtla-skills update

# 2. Test thoroughly
pytest tests/
python forecasting/experiments.py

# 3. Update staging
cd /path/to/staging/project
nixtla-skills update

# 4. Validate in staging
# Run smoke tests

# 5. Update production
cd /path/to/prod/project
nixtla-skills update
```

### 3. Monitoring and Auditing

**Track versions in monitoring**:
```python
# In your application code
import yaml
from pathlib import Path

def get_skills_versions():
    """Get installed Nixtla skills versions for telemetry"""
    skills_dir = Path('.claude/skills')
    versions = {}
    
    for skill_path in skills_dir.glob('nixtla-*/SKILL.md'):
        skill_name = skill_path.parent.name
        
        with open(skill_path) as f:
            content = f.read(1000)
            
        import re
        match = re.search(r'version:\s*["\']?([0-9]+\.[0-9]+\.[0-9]+)["\']?', content)
        if match:
            versions[skill_name] = match.group(1)
    
    return versions

# Log versions
versions = get_skills_versions()
logger.info(f"Nixtla Skills Versions: {versions}")
# Output: {'nixtla-timegpt-lab': '0.4.0', ...}
```

### 4. Documentation

**Maintain project README**:
```markdown
# Project README

## Nixtla Skills

This project uses Nixtla Claude Skills v0.4.0 for forecasting workflows.

### Installation

```bash
nixtla-skills init
```

### Skills Included

- nixtla-timegpt-lab (v0.4.0) - Forecasting guidance
- nixtla-experiment-architect (v0.4.0) - Experiment setup
- nixtla-schema-mapper (v0.4.0) - Data transformation
- nixtla-timegpt-finetune-lab (v0.4.0) - Fine-tuning workflows
- nixtla-prod-pipeline-generator (v0.4.0) - Production pipelines
- nixtla-usage-optimizer (v0.4.0) - Cost optimization

### Updating

```bash
nixtla-skills update
```
```

### 5. Team Onboarding

**Onboarding checklist**:
```markdown
# New Team Member: Nixtla Skills Setup

- [ ] Install Claude Code
- [ ] Clone project repo: `git clone ...`
- [ ] Install Python dependencies: `pip install -r requirements.txt`
- [ ] Clone Nixtla Skills Pack: `git clone https://github.com/intent-solutions-io/plugins-nixtla.git`
- [ ] Install skills CLI: `cd plugins-nixtla/packages/nixtla-claude-skills-installer && pip install -e .`
- [ ] Install skills in project: `cd /path/to/project && nixtla-skills init`
- [ ] Verify installation: `ls .claude/skills/nixtla-*/`
- [ ] Try a skill: Open Claude Code, "Use nixtla-timegpt-lab"
```

---

## Appendix A: CLI Reference

### `nixtla-skills init`

**Purpose**: Install skills in current project

**Syntax**:
```bash
nixtla-skills init [--source PATH]
```

**Options**:
- `--source PATH`: Override skills source location (default: auto-detect)

**Example**:
```bash
nixtla-skills init
nixtla-skills init --source /custom/path/to/skills-pack
```

### `nixtla-skills update`

**Purpose**: Update skills to latest version

**Syntax**:
```bash
nixtla-skills update [--source PATH]
```

**Options**:
- `--source PATH`: Override skills source location

**Example**:
```bash
nixtla-skills update
```

### `nixtla-skills --version`

**Purpose**: Show CLI version

**Syntax**:
```bash
nixtla-skills --version
```

**Example**:
```bash
$ nixtla-skills --version
nixtla-skills 0.4.0
```

---

## Appendix B: Version History

| Version | Date | Phase | Changes |
|---------|------|-------|---------|
| **0.4.0** | 2025-12-03 | Phase 4 | Advanced skills, demo project, DevOps guide |
| **0.3.0** | 2025-12-03 | Phase 3 | Installer CLI, version tracking, bootstrap skill |
| **0.2.0** | 2025-12-03 | Phase 2 | Core skills to standard (timegpt-lab, experiment-architect, schema-mapper) |
| **0.1.0** | 2025-11-30 | Phase 1 | Skeleton, SKILL standard, compliance |

---

## Appendix C: Support and Contact

**Issues**: https://github.com/intent-solutions-io/plugins-nixtla/issues

**Maintained By**: Intent Solutions (Jeremy Longshore)
- Email: jeremy@intentsolutions.io
- Phone: 251.213.1115

**Sponsored By**: Nixtla (Max Mergenthaler)
- Email: max@nixtla.io

---

**Document Version**: 0.4.0  
**Last Updated**: 2025-12-03  
**Status**: Complete (Phase 4)
