# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Task Tracking (Beads / bd)

**All task tracking uses Beads (`bd` CLI)** - no markdown TODO lists.

```bash
# Session start
bd ready                                    # Show unblocked work
bd list --status in_progress                # What was I doing?

# During work
bd update <id> --status in_progress         # Claim task (BEFORE coding)
bd close <id> --reason "Evidence here"      # Complete task (AFTER coding)

# Session end
bd sync                                     # Commit beads to git
git push                                    # Push code changes
```

**Key commands**: `bd ready`, `bd show <id>`, `bd create "Title" -p 1`, `bd sync`

## Repository Overview

**Business showcase for Nixtla CEO** demonstrating Claude Code plugins and AI skills for time-series forecasting.

| Attribute | Value |
|-----------|-------|
| **Version** | 1.8.1 (source: `VERSION`) |
| **Status** | Experimental showcase |
| **Stack** | Python 3.9+, statsforecast, TimeGPT API, pytest, black, isort |
| **Skills** | 30 (in `003-skills/.claude/skills/`) |
| **Plugins** | 13 (in `005-plugins/`) - 3 working |

## Quick Start (5 Minutes)

```bash
# 1. Setup environment
./004-scripts/setup-dev-environment.sh      # Creates venv + .env
# OR manually:
python3 -m venv venv && source venv/bin/activate && pip install -r requirements-dev.txt

# 2. Activate
source venv/bin/activate

# 3. Run tests
pytest -v --tb=short -m "not integration"

# 4. Validate skills
python 004-scripts/validate_skills_v2.py
```

**All pass?** Ready to work. **Failures?** See Troubleshooting section.

## Directory Structure

```
000-docs/           # ALL documentation (AAR system, specs, standards)
001-htmlcov/        # Test coverage reports
002-workspaces/     # Demo projects (notably test-harness-lab/)
003-skills/         # Claude Skills (.claude/skills/nixtla-*/)
004-scripts/        # Automation (validators, generators)
005-plugins/        # Plugin implementations
006-packages/       # Installable packages (skills-installer)
007-tests/          # E2E/integration tests (run explicitly)
009-temp-data/      # Generated/temporary data
010-archive/        # Archived content
tests/              # pytest suite (DEFAULT target)
```

**Key locations**:
- Skills: `003-skills/.claude/skills/nixtla-*/SKILL.md`
- Plugins: `005-plugins/nixtla-*/`
- Master skill standard: `000-docs/000a-skills-schema/SKILLS-STANDARD-COMPLETE.md`

## Commands Reference

### Testing

```bash
# All tests
pytest -v

# With coverage (outputs to 001-htmlcov/)
pytest --cov=005-plugins --cov-report=term -v

# By marker (see pytest.ini)
pytest -m "unit"                # Unit tests only
pytest -m "not integration"     # Skip integration
pytest -m "not slow"            # Skip slow tests
pytest -m "not cloud"           # Skip cloud-dependent
pytest -m "not api"             # Skip external API calls

# Single test
pytest tests/skills/test_all_skills.py::test_l4_quality -v

# Pattern match
pytest -k "test_baseline" -v
```

### Validation

```bash
# Skills validation (strict mode)
python 004-scripts/validate_skills_v2.py --fail-on-warn

# Plugin validation
bash 004-scripts/validate-all-plugins.sh .

# Universal validator (evidence bundle)
python 003-skills/.claude/skills/nixtla-universal-validator/scripts/run_validator_suite.py \
  --target . --project pr-1234 --out reports/pr-1234 --profile default
```

### Formatting

```bash
# Check
black --check . && isort --check-only . && flake8 .

# Fix
black . && isort .
```

### Plugin Development (Baseline Lab)

```bash
cd 005-plugins/nixtla-baseline-lab
./scripts/setup_nixtla_env.sh --venv
source .venv-nixtla-baseline/bin/activate
pip install -r scripts/requirements.txt

# Smoke test (90 sec, offline)
python tests/run_baseline_m4_smoke.py

# In Claude Code:
/nixtla-baseline-m4 demo_preset=m4_daily_small
```

### Skills Installer

```bash
pip install -e 006-packages/nixtla-claude-skills-installer
cd /path/to/your/project
nixtla-skills init      # Install all skills
nixtla-skills update    # Update to latest
```

## Architecture

### Three-Layer System

1. **Claude Skills** (`003-skills/.claude/skills/nixtla-*/`)
   - AI prompts that transform Claude's behavior
   - Auto-activate on relevant context
   - Each has: `SKILL.md` + optional `scripts/`, `assets/templates/`

2. **Plugins** (`005-plugins/*/`)
   - Complete applications with MCP servers, tests, Python backends
   - Working: nixtla-baseline-lab, nixtla-bigquery-forecaster, nixtla-search-to-slack

3. **Slash Commands** (`005-plugins/*/commands/*.md`)
   - User-invoked commands like `/nixtla-baseline-m4`

### MCP Server Pattern

The baseline lab MCP server (`005-plugins/nixtla-baseline-lab/scripts/nixtla_baseline_mcp.py`) exposes:
- `run_baselines` - Run statsforecast models on M4/custom data
- `get_nixtla_compatibility_info` - Library version info
- `generate_benchmark_report` - Markdown report from metrics CSV
- `generate_github_issue_draft` - GitHub issue template

## Skills Standard (Summary)

**Full spec**: `000-docs/000a-skills-schema/SKILLS-STANDARD-COMPLETE.md`

### Required Frontmatter

```yaml
name: nixtla-<short-name>
description: |
  [Capabilities]. [Features].
  Use when [scenarios].
  Trigger with "phrase 1", "phrase 2".
allowed-tools: "Read,Write,Glob,Grep,Edit,Bash(python:*)"
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: "MIT"
```

### L4 Quality Requirements (100% mandatory)

- Action verb in description (analyze, detect, forecast, generate, validate, etc.)
- "Use when" phrase present
- "Trigger with" phrase present
- 100-300 character description length
- Domain keyword (timegpt, forecast, time series, nixtla, statsforecast)

### Validation

```bash
python 004-scripts/validate_skills_v2.py --verbose
```

## Environment Variables

Create `.env` in repo root (use `./004-scripts/setup-dev-environment.sh`):

```bash
# Optional - TimeGPT features only
NIXTLA_TIMEGPT_API_KEY=your-key

# Optional - GCP features only
PROJECT_ID=your-gcp-project
LOCATION=us-central1
```

**Note**: Baseline lab works fully offline with zero API keys.

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

## Development Workflow

### Commit Messages

Follow Conventional Commits: `<type>(<scope>): <description>`

**Types**: `feat`, `fix`, `docs`, `chore`, `test`, `refactor`, `style`, `perf`
**Scopes**: `skills`, `plugins`, `scripts`, `docs`, `ci`, `tests`, `packages`

```bash
feat(skills): add nixtla-timegpt-lab skill
fix(baseline-lab): correct M4 data loading bug
docs(readme): update installation instructions
```

### Code Style

- **Indentation**: 4 spaces (see `.editorconfig`)
- **Line length**: ≤100 characters (Black/Flake8)
- **Naming**: plugin folders `kebab-case`, Python `snake_case`

### Pre-PR Checklist

```bash
python 004-scripts/validate_skills_v2.py --fail-on-warn
bash 004-scripts/validate-all-plugins.sh .
pytest -v -m "not integration"
black --check . && isort --check-only . && flake8 .
```

## Documentation Standards

### Doc-Filing System

All docs in `000-docs/` use naming: `NNN-AA-CODE-descriptive-slug.md`

- `NNN` = 3-digit sequence (never renumber)
- `AA-CODE` = Type (REPT, AACR, STAT, PRD, ADR, AUDT)

### AAR Required Sections

1. Title with doc ID
2. Date/time (CST)
3. Executive Summary
4. Scope
5. Changes Made
6. Risks/Unknowns
7. Next Actions

## CI/CD Workflows

All in `.github/workflows/`:

| Workflow | Purpose | Required to Merge |
|----------|---------|-------------------|
| `ci.yml` | Main validation | Yes |
| `skills-validation.yml` | Skills compliance | Yes |
| `plugin-validator.yml` | Plugin schema | No |
| `nixtla-baseline-lab-ci.yml` | Plugin tests | No |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: statsforecast` | `pip install -r scripts/requirements.txt` (in plugin dir) |
| `ModuleNotFoundError` (general) | `pip install -e . && pip install -r requirements-dev.txt` |
| Tests fail with import error | `export PYTHONPATH=$PWD` or activate venv |
| Permission denied on script | `chmod +x scripts/*.sh` |
| Plugin not found after install | Restart Claude Code |
| Smoke test timeout | First run downloads M4 data (~30MB) |
| `NIXTLA_TIMEGPT_API_KEY not set` | Only needed for TimeGPT, not baseline lab |
| Validation failures | `python 004-scripts/validate_skills_v2.py --verbose` |
| Virtual environment issues | Delete `venv/`, re-run setup script |

## Post-Compact Context Restoration

**After context compaction, read these files:**

1. `000-docs/000a-skills-schema/SKILLS-STANDARD-COMPLETE.md` - Skills schema
2. Last two AAR docs in `000-docs/` (highest numbered `*-AA-*.md` files)

## Version & Release

**Current**: 1.8.1 (source of truth: `VERSION`)

Release process:
1. Update `VERSION` file
2. Update `CHANGELOG.md`
3. Create release AAR in `000-docs/`
4. Tag: `git tag -a v1.X.Y -m "Release v1.X.Y"`
5. Push: `git push origin v1.X.Y`

---

<!-- bv-agent-instructions-v1 -->

## Beads Workflow Integration

This project uses [beads_viewer](https://github.com/Dicklesworthstone/beads_viewer) for issue tracking.

### Essential Commands

```bash
bd ready              # Unblocked issues
bd list --status=open # All open
bd show <id>          # Full details
bd create --title="..." --type=task --priority=2
bd update <id> --status=in_progress
bd close <id> --reason="Completed"
bd sync               # Commit to git
```

### Workflow

1. **Start**: `bd ready` to find work
2. **Claim**: `bd update <id> --status=in_progress`
3. **Work**: Implement
4. **Complete**: `bd close <id>`
5. **Sync**: `bd sync` before session end

### Priority

P0=critical, P1=high, P2=medium, P3=low, P4=backlog

<!-- end-bv-agent-instructions -->
