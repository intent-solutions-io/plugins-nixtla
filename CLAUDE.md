# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

**Business showcase for Nixtla CEO** demonstrating Claude Code plugins and AI skills for time-series forecasting workflows.

**Version**: 1.4.1 | **Status**: 3 working plugins + 8 Claude Skills

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

# Skills compliance validator
python tests/basic_validator.py
```

## Architecture

### Three-Layer Plugin/Skill System

1. **Claude Skills** (`skills-pack/.claude/skills/nixtla-*/`)
   - AI prompts that transform Claude's behavior
   - Auto-activate when Claude detects relevant context
   - 8 skills: timegpt-lab, experiment-architect, schema-mapper, etc.

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

### Doc-Filing v3.0

All docs in `000-docs/` follow: `NNN-CC-ABCD-description.md`

**Category Codes**: PP (Planning), AT (Architecture), AA (Audits), OD (Overview), QA (Quality)

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
- `skills-installer-ci.yml` - Skills installer tests
- `nixtla-baseline-lab-ci.yml` - Baseline lab plugin
- `ci.yml` - Main validation pipeline

## Critical Messaging

**This is experimental/prototype work** for business development:
- Use: "experimental", "prototype", "showcase", "demonstrates value"
- Avoid: "production-ready", "enterprise-grade", "guaranteed"

## Version & Release

**Current**: 1.4.1 (CI/CD Alignment with Global Standard)

See `CHANGELOG.md` for full history. Release process:
1. Update `VERSION` file
2. Update `CHANGELOG.md`
3. Create release AAR in `000-docs/`
4. Tag: `git tag -a v1.X.Y -m "Release v1.X.Y"`
