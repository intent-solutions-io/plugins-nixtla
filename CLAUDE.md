# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

**Business showcase for Nixtla CEO** demonstrating Claude Code plugins and AI skills for time-series forecasting workflows.

**Version**: 1.6.0 | **Status**: 3 working plugins + 29 Claude Skills (8 core + 21 generated)

## Claude Skills – SKILL.md Structure Reference

All Claude Skills in this repository **must conform** to the canonical skills standard documented in:

- **Master Standard**: `{baseDir}/000-docs/077-SPEC-MASTER-claude-skills-standard.md`
- **Authoring Guide**: `{baseDir}/000-docs/6767-n-DR-GUID-claude-skills-authoring-guide.md`
- **Frontmatter Schema**: `{baseDir}/000-docs/6767-m-DR-STND-claude-skills-frontmatter-schema.md`

### SKILL.md Template

Every `SKILL.md` file follows this structure:

```markdown
---
name: your-skill-name
description: |
  [Primary capabilities]. [Secondary features].
  Use when [scenario 1], [scenario 2], [scenario 3].
  Trigger with "phrase 1", "phrase 2", "phrase 3".
allowed-tools: "Read,Write,Glob,Grep,Edit,Bash(python:*)"
version: "1.0.0"
---

# [Skill Name]

## Purpose
Brief statement of what this skill does (1-2 sentences).

## Overview
High-level description of capabilities and workflow.

## Prerequisites
Required tools, dependencies, environment setup.

## Instructions
Step-by-step guide (imperative voice: "Do X", "Run Y").

## Output
What the skill produces (files, reports, artifacts).

## Error Handling
Common issues and troubleshooting steps.

## Examples
Concrete usage examples with real commands/paths.

## Resources
Links to external docs, related skills, references.
```

### Critical Requirements

- **Descriptions**: Third person only (no "I"/"you"). Follow pattern: capabilities → features → use when → trigger with.
- **Paths**: All paths must use `{baseDir}` for portability (e.g., `{baseDir}/skills-pack/.claude/skills/`).
- **Body Length**: ≤ 500 lines. Extract long code to `scripts/` or `assets/templates/`.
- **Voice**: Use imperative for instructions ("Run the script", "Copy the file").
- **Forbidden Frontmatter**: No `author`, `priority`, `audience`, `when_to_use`, `license` fields.

### Skill File Structure

```
skills-pack/.claude/skills/your-skill-name/
├── SKILL.md              # Main skill definition (required)
├── scripts/              # Extracted Python/shell scripts
├── assets/templates/     # Reusable code templates
├── resources/            # Supporting docs (EXAMPLES.md, TROUBLESHOOTING.md)
└── references/           # External links, citations
```

## Quick Commands

### Testing & CI

```bash
# Run all tests from repo root
pytest -v

# Run with coverage
pytest --cov=plugins --cov=examples --cov-report=term -v

# Lint/format checks (must pass CI)
black --check .
isort --check-only .
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

# Auto-fix formatting
black .
isort .
```

### Plugin Development (Baseline Lab)

```bash
cd plugins/nixtla-baseline-lab
./scripts/setup_nixtla_env.sh --venv
source .venv-nixtla-baseline/bin/activate
pip install -r scripts/requirements.txt

# Run golden task smoke test (90 seconds, offline)
python tests/run_baseline_m4_smoke.py

# In Claude Code, run the slash command:
/nixtla-baseline-m4 demo_preset=m4_daily_small
```

### Skills Pack

```bash
pip install -e packages/nixtla-claude-skills-installer
cd /path/to/your/project
nixtla-skills init    # Install all 8 skills
nixtla-skills update  # Update to latest
```

### Testing Individual Components

```bash
# Skills installer E2E test
python tests/test_skills_installer_e2e.py

# Baseline lab smoke test
python plugins/nixtla-baseline-lab/tests/run_baseline_m4_smoke.py

# Skills compliance validator (strict mode)
python scripts/validate_skills.py
```

### Automation Scripts

```bash
# Generate new skills using Vertex AI Gemini (overnight batch)
python scripts/overnight_skill_generator.py --dry-run  # Preview only
python scripts/overnight_skill_generator.py            # Actually generate

# Extract embedded code from skills to scripts/ folders
python scripts/add_scripts_to_skills.py
```

## Architecture

### Three-Layer Plugin/Skill System

1. **Claude Skills** (`skills-pack/.claude/skills/nixtla-*/` + `000-docs/planned-skills/*/`)
   - AI prompts that transform Claude's behavior
   - Auto-activate when Claude detects relevant context
   - 8 core skills: timegpt-lab, experiment-architect, schema-mapper, usage-optimizer, etc.
   - 21 generated skills: core-forecasting (5), prediction-markets (10), live-retroactive (6)

2. **Plugins** (`plugins/*/`)
   - Complete applications with MCP servers, tests, Python backends
   - Working: nixtla-baseline-lab, nixtla-bigquery-forecaster, nixtla-search-to-slack

3. **Slash Commands** (`plugins/*/commands/*.md`)
   - User-invoked commands like `/nixtla-baseline-m4`

### Key Source Files

| File | Purpose |
|------|---------|
| `plugins/nixtla-baseline-lab/scripts/nixtla_baseline_mcp.py` | MCP server exposing forecasting tools |
| `plugins/nixtla-baseline-lab/tests/run_baseline_m4_smoke.py` | Golden task test harness |
| `packages/nixtla-claude-skills-installer/nixtla_skills_installer/core.py` | Skills installation logic |
| `skills-pack/.claude/skills/*/SKILL.md` | Individual skill definitions |

### MCP Server Pattern

The baseline lab MCP server (`nixtla_baseline_mcp.py`) exposes 4 tools:
- `run_baselines` - Run statsforecast models on M4/custom data
- `get_nixtla_compatibility_info` - Library version info
- `generate_benchmark_report` - Markdown report from metrics CSV
- `generate_github_issue_draft` - GitHub issue template with reproducibility info

## Documentation Standards

### Doc-Filing v4.0 + AAR System

**Critical**: All project documentation lives in `000-docs/` (FLAT structure at root level).

**Naming Convention**: `NNN-AA-CODE-descriptive-slug.md`
- `NNN` = 3-digit sequence (001, 026, 169) - never renumber existing docs
- `AA-CODE` = Document type (see below)
- `descriptive-slug` = kebab-case summary (e.g., `phase-02-explainability-bootstrap`)

**Document Types**:
- `AA-REPT` - After-Action Report (narrative summary of completed work)
- `AA-AACR` - After-Action & Completion Record (formal phase completion)
- `AA-STAT` - Status/analysis docs (current state, gap analysis)
- `AA-SITR` - Situation reports (branch status, decision points)
- `AA-PRD` - Product requirements documents
- `AA-ADR` - Architecture decision records
- `AA-AUDT` - Audit reports (read-only analysis)
- `PP` - Planning, `AT` - Architecture, `OD` - Overview, `DR` - Reference, `QA` - Quality

**Required AAR Sections**:
1. Title with doc ID
2. Date/time in CST (America/Chicago)
3. Executive Summary (3-5 bullets)
4. Scope (what touched, what not touched)
5. Changes Made (files + paths)
6. Risks / Unknowns
7. Next Actions
8. Footer: `intent solutions io — confidential IP` / `Contact: jeremy@intentsolutions.io`

**Workflow**:
1. Plan in doc → Code → Update doc
2. All commits reference doc ID (e.g., `git commit -m "082-AA-AUDT: phase 1 audit complete"`)
3. Every significant change has traceability: change → commit → doc

**Current Sequence**: Next doc = 083 (last: 082-AA-AUDT-repo-audit-neuralforecast-explainability.md)

### Per-Plugin Documentation

Each plugin requires 6 standardized docs in `000-docs/planned-plugins/{plugin}/`:
- 01-BUSINESS-CASE.md, 02-PRD.md, 03-ARCHITECTURE.md
- 04-USER-JOURNEY.md, 05-TECHNICAL-SPEC.md, 06-STATUS.md

### Skill Standard Compliance

Skills must comply with `000-docs/041-SPEC-nixtla-skill-standard.md`:

**Required frontmatter**:
```yaml
name: nixtla-<short-name>
description: >
  Action-oriented description with when-to-use context
version: X.Y.Z
allowed-tools: "Read,Write,Glob,Grep,Edit"
```

**Forbidden fields**: author, priority, audience, when_to_use, license

## Nixtla Integration Patterns

```python
# StatsForecast (open source, no API key)
from statsforecast import StatsForecast
from statsforecast.models import AutoETS, AutoTheta, SeasonalNaive
sf = StatsForecast(models=[AutoETS(), AutoTheta()], freq='D')
forecasts = sf.forecast(df=df_train, h=14)

# TimeGPT (requires NIXTLA_TIMEGPT_API_KEY)
from nixtla import NixtlaClient
client = NixtlaClient(api_key='...')
forecast = client.forecast(df=data, h=24, freq='H')
```

## Python Environments

| Component | Python | Location |
|-----------|--------|----------|
| Skills installer | 3.8+ | `packages/nixtla-claude-skills-installer/` |
| Baseline lab | 3.10+ | `plugins/nixtla-baseline-lab/.venv-nixtla-baseline/` |
| BigQuery forecaster | 3.10+ | `plugins/nixtla-bigquery-forecaster/.venv/` |

## CI/CD Workflows

All in `.github/workflows/`:
- `ci.yml` - Main validation pipeline (required to merge)
- `skills-validation.yml` - Claude Skills strict compliance validator
- `nixtla-baseline-lab-ci.yml` - Baseline lab plugin tests
- `skills-installer-ci.yml` - Skills installer tests
- `plugin-validator.yml` - Plugin schema validation
- `gemini-pr-review.yml` - AI code review on PRs
- `gemini-daily-audit.yml` - Daily automated audit
- `deploy-bigquery-forecaster.yml` - BigQuery Cloud Functions deployment

## Critical Messaging

**This is experimental/prototype work** for business development:
- Use: "experimental", "prototype", "showcase", "demonstrates value"
- Avoid: "production-ready", "enterprise-grade", "guaranteed"

## Version & Release

**Current**: 1.6.0 (21 AI Skills + DevOps-First README)

See `CHANGELOG.md` for full history. Release process:
1. Update `VERSION` file
2. Update `CHANGELOG.md` with release highlights, contributors, features
3. Create release AAR in `000-docs/` (After Action Review)
4. Tag: `git tag -a v1.X.Y -m "Release v1.X.Y"`
5. Push tag: `git push origin v1.X.Y`

## Skill Extraction Standard

**New in 1.6+**: Skills must extract embedded Python/shell code to separate files.

- **Scripts location**: `skills-pack/.claude/skills/{skill-name}/scripts/`
- **Templates location**: `skills-pack/.claude/skills/{skill-name}/assets/templates/`
- **Why**: Prevents SKILL.md from becoming unwieldy, enables code reuse
- **Validator**: `python scripts/validate_skills.py` checks compliance

Recent extractions (Dec 2025):
- nixtla-experiment-architect, nixtla-prod-pipeline-generator, nixtla-schema-mapper
- nixtla-timegpt-lab, nixtla-timegpt-finetune-lab, nixtla-usage-optimizer
- nixtla-arbitrage-detector, nixtla-batch-forecaster

See git log for extraction commit pattern: `fix(skills): extract {skill} embedded code to scripts`
