# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Task Tracking (Beads / bd)

**All task tracking uses Beads (`bd` CLI)** - no markdown TODO lists.

```bash
# Session start
bd ready

# Create task
bd create "Title" -p 1 --description "Context + acceptance criteria"

# Update status
bd update <id> --status in_progress

# Complete task
bd close <id> --reason "Done"

# Session end (flush/import/export + git sync)
bd sync
```

**After upgrading `bd`:**
```bash
bd info --whats-new
bd hooks install  # If warned about hooks
```

**Workspace isolation**: Prefer `BEADS_DIR` environment variable (`BEADS_DB` deprecated).

## Repository Overview

**Business showcase for Nixtla CEO** demonstrating Claude Code plugins and AI skills for time-series forecasting workflows.

**Version**: 1.8.1 | **Status**: Experimental showcase (plugins + skills)

**Tech Stack**: Python 3.9+, statsforecast, TimeGPT API, Nixtla SDK, pytest, black, isort, flake8

**Current Inventory**:
- **30+ Claude Skills** (003-skills/.claude/skills/) - all at 100% L4 quality
- **13+ Plugins** (005-plugins/) - 3 working (baseline-lab, bigquery-forecaster, search-to-slack)

## First 5 Minutes - Health Check

Run this to verify your environment is ready:

```bash
# 1. Check Python version (need 3.9+)
python3 --version

# 2. Setup environment
./004-scripts/setup-dev-environment.sh  # Creates venv + .env
# OR manually:
python3 -m venv venv && source venv/bin/activate && pip install -r requirements-dev.txt

# 3. Activate environment
source venv/bin/activate

# 4. Run smoke tests
pytest -v --tb=short -m "not integration"

# 5. Validate skills
python 004-scripts/validate_skills_v2.py
```

**If all pass**: You're ready to work.
**If failures**: See Troubleshooting section below.

## Directory Structure

The repository uses numbered prefixes for top-level organization. **Root directory is clean** - only numbered directories + essential config files.

```
000-docs/           # ALL documentation (AAR system, specs, community standards)
001-htmlcov/        # ALL test coverage reports (.coverage, coverage.xml, HTML)
002-workspaces/     # Demo projects and workspace templates
003-skills/         # Claude Skills (.claude/skills/nixtla-*/)
004-scripts/        # ALL automation (validators, generators, configs/, emailer/)
005-plugins/        # Plugin implementations (baseline-lab, bigquery-forecaster, search-to-slack)
006-packages/       # Installable packages (skills-installer)
007-tests/          # Additional test utilities (E2E, integration tests run explicitly)
009-temp-data/      # Generated/temporary data (inventories, reports)
010-archive/        # Archived/deprecated content
tests/              # pytest test suite (DEFAULT target for `pytest` command)
```

**Module Organization Rationale**:
- `005-plugins/`: Each plugin has `.claude-plugin/`, `commands/`, `scripts/`, and optionally `src/`, `tests/`, `templates/`
- `003-skills/.claude/skills/`: Reusable Claude skills with SKILL.md + scripts/ + assets/
- `006-packages/`: Installable Python packages (notably `nixtla-claude-skills-installer/`)
- `000-docs/`: Canonical documentation (symlinked for GitHub Community Standards compliance)

### Root Directory (Clean)

**23 items total**: 10 numbered directories + 13 essential files (includes 3 symlinks for GitHub compliance)

**Essential files only:**
- `README.md`, `CLAUDE.md`, `CHANGELOG.md`, `LICENSE`, `VERSION`
- `pyproject.toml`, `pytest.ini`
- `requirements.txt`, `requirements-dev.txt`
- `CODE_OF_CONDUCT.md` → symlink to `000-docs/` (GitHub Community Standards)
- `CONTRIBUTING.md` → symlink to `000-docs/` (GitHub Community Standards)
- `SECURITY.md` → symlink to `000-docs/` (GitHub Community Standards)

## Learning Resources

### Test Harness Lab

**Location**: `002-workspaces/test-harness-lab/`

A comprehensive learning lab teaching the **multi-phase validated workflow pattern** for building production-ready agent systems with empirical verification.

**Quick Start**:
```bash
cd 002-workspaces/test-harness-lab/
cat docs/QUICK-START.md          # 5-minute introduction
cat guides/GUIDE-00-START-HERE.md  # Deep dive (1 hour)
cat docs/NIXTLA-APPLICATIONS.md  # 3 concrete use cases
```

**What you'll learn**:
- How to decompose workflows into validated phases
- Phase 4 pattern: Run deterministic scripts to verify LLM conclusions
- Build release validation, benchmark regression, docs sync workflows
- Deploy skills from lab → 003-skills/ (production)

**Contents**:
- 4 comprehensive guides (~60 pages)
- Complete reference implementation (5-phase schema-optimization)
- Hands-on exercises
- Nixtla-specific applications with working scripts

**See**: `002-workspaces/test-harness-lab/README.md` for full details.

## Environment Variables

Create a `.env` file in the repository root (use `./004-scripts/setup-dev-environment.sh` to auto-generate):

```bash
# Optional - only needed for TimeGPT features
NIXTLA_TIMEGPT_API_KEY=your-timegpt-api-key-here

# Optional - only for BigQuery/GCP features
PROJECT_ID=your-gcp-project-id
LOCATION=us-central1

# Optional - cloud provider credentials for specific plugins
# AWS_ACCESS_KEY_ID=...
# AWS_SECRET_ACCESS_KEY=...
# AZURE_STORAGE_CONNECTION_STRING=...
```

**Important**: `.env` is in `.gitignore` - never commit secrets.

**Baseline Lab Note**: The statsforecast baseline lab works **completely offline** with zero API keys required.

## Claude Skills – SKILL.md Structure Reference

All Claude Skills in this repository **must conform** to the canonical skills standard:

- **📘 Master Standard**: `000-docs/000a-skills-schema/SKILLS-STANDARD-COMPLETE.md` (v2.3.0 ENGINEERING-COMPLETE)
  - Audited against: Lee Han Chung (Oct 2025), Anthropic Platform Docs, Official Blog, Engineering Blog
  - Complete specification: frontmatter fields, body structure, best practices
  - Includes Appendices: Schema Reference, Authoring Guide, Nixtla Strategy

### Automated Validation

**All skills are validated automatically**:
```bash
# Run validator v2 (enterprise + strict quality mode)
python 004-scripts/validate_skills_v2.py

# Verbose mode with detailed errors
python 004-scripts/validate_skills_v2.py --verbose

# CI/CD: Runs on every push/PR
# See: .github/workflows/skills-validation.yml
```

### Universal Validation (Evidence Bundles)

For deterministic, profile-driven validation that writes an evidence bundle (JSON + report + logs):

```bash
python 003-skills/.claude/skills/nixtla-universal-validator/scripts/run_validator_suite.py \
  --target . \
  --project pr-1234 \
  --out reports/pr-1234 \
  --profile default
```

List built-in profiles:

```bash
python 003-skills/.claude/skills/nixtla-universal-validator/scripts/run_validator_suite.py \
  --list-profiles \
  --target . \
  --project pr-1234 \
  --out reports/pr-1234
```

Evidence bundle output:

- `reports/<project>/<timestamp>/summary.json`
- `reports/<project>/<timestamp>/report.md`
- `reports/<project>/<timestamp>/checks/*.log`

**Validator v2 enforces**:
- **Anthropic Spec**: Description ≤1024 chars, third-person voice, proper structure
- **Enterprise Fields**: author, license, version (required for marketplace)
- **Nixtla Strict Quality**:
  - "Use when" + "Trigger with" phrases in description (discovery)
  - Unscoped Bash forbidden (security)
  - Required body sections (8 sections: Overview, Prerequisites, Instructions, etc.)
  - Reserved words forbidden ("anthropic", "claude")
  - L4 quality scoring (100% maintained across all skills)
- **Budget**: <15,000 chars total across ALL skill descriptions
- **Paths**: {baseDir} variable (no hardcoded paths)

**Compliance Rate**: 26/26 production skills (100%)

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
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: "MIT"
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
- **Forbidden Frontmatter**: No `priority`, `audience`, `when_to_use` fields.

### Skill File Structure

```
003-skills/.claude/skills/nixtla-{skill-name}/
├── SKILL.md              # Main skill definition (required)
├── scripts/              # Extracted Python/shell scripts
├── assets/templates/     # Reusable code templates
├── resources/            # Supporting docs (EXAMPLES.md, TROUBLESHOOTING.md)
└── references/           # External links, citations
```

### Planned Templates (Reusable)

- Universal validator (skill template): `000-docs/000a-planned-skills/templates/universal-validator/`
- Universal validator (plugin template): `000-docs/000a-planned-plugins/templates/universal-validator/`

### L4 Quality Scoring (Enforced at 100%)

All skills must achieve **100/100** on L4 quality checks:

| Criteria | Weight | Requirement |
|----------|--------|-------------|
| **Action verbs** | 20% | Must contain: analyze, detect, forecast, transform, generate, validate, compare, or optimize |
| **"Use when"** | 25% | Must include "Use when" phrase |
| **"Trigger with"** | 25% | Must include "Trigger with" phrase |
| **Length** | 15% | Description must be 100-300 characters |
| **Domain keywords** | 15% | Must contain: timegpt, forecast, time series, nixtla, or statsforecast |

**Test command**: `python tests/skills/test_all_skills.py`

**Example perfect description**:
```yaml
description: "Analyze and forecast Polymarket contracts using TimeGPT with confidence intervals. Use when predicting contract prices. Trigger with 'Polymarket analysis' or 'forecast prediction market'."
```
Score: 100/100 ✓ (has action verb, "use when", "trigger with", 172 chars, domain keyword "forecast")

## Quick Commands

### Testing & CI

```bash
# Run all tests from repo root (default target: tests/)
pytest -v

# Run with coverage (outputs to 001-htmlcov/)
pytest --cov=005-plugins --cov-report=term -v

# Run specific plugin tests
pytest 005-plugins/nixtla-baseline-lab/tests -v

# Run by marker (see pytest.ini for all markers)
pytest -m "unit"              # Only unit tests
pytest -m "not integration"   # Skip integration tests
pytest -m "not slow"          # Skip slow tests
pytest -m "not cloud"         # Skip tests requiring cloud access
pytest -m "not api"           # Skip tests calling external APIs

# Run single test file
pytest tests/skills/test_all_skills.py -v

# Run single test function
pytest tests/skills/test_all_skills.py::test_l4_quality -v

# Run tests matching pattern
pytest -k "test_baseline" -v

# Lint/format checks (must pass CI)
black --check .
isort --check-only .
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

# Auto-fix formatting
black .
isort .
```

**Pytest Markers** (defined in `pytest.ini`):
- `unit` - Unit tests (fast, no external dependencies)
- `integration` - Integration tests (require external services)
- `slow` - Tests taking >5 seconds
- `cloud` - Tests requiring cloud provider access (AWS/GCP/Azure)
- `api` - Tests calling external APIs (TimeGPT, etc.)

### Plugin Development (Baseline Lab)

```bash
cd 005-plugins/nixtla-baseline-lab
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
pip install -e 006-packages/nixtla-claude-skills-installer
cd /path/to/your/project
nixtla-skills init    # Install all 26 skills
nixtla-skills update  # Update to latest
```

### Testing Individual Components

```bash
# Skills installer E2E test
python 007-tests/test_skills_installer_e2e.py

# Baseline lab smoke test
python 005-plugins/nixtla-baseline-lab/tests/run_baseline_m4_smoke.py

# Skills compliance validator (strict mode)
python 004-scripts/validate_skills_v2.py

# Skills test suite (L1/L2/L4 quality checks)
python tests/skills/test_all_skills.py                        # All 23 skills
python tests/skills/test_all_skills.py --skill nixtla-*       # Single skill
python tests/skills/test_all_skills.py --level 4              # L4 quality only
```

### Validation Commands (Pre-Commit/Pre-PR)

```bash
# Validate all skills (strict mode, fail on warnings)
python 004-scripts/validate_skills_v2.py --fail-on-warn

# Validate all skills (verbose output)
python 004-scripts/validate_skills_v2.py --verbose

# Validate all plugins (canonical schema)
bash 004-scripts/validate-all-plugins.sh .

# Universal validator (evidence bundle output)
python 003-skills/.claude/skills/nixtla-universal-validator/scripts/run_validator_suite.py \
  --target . \
  --project pr-1234 \
  --out reports/pr-1234 \
  --profile default

# List available validator profiles
python 003-skills/.claude/skills/nixtla-universal-validator/scripts/run_validator_suite.py \
  --list-profiles \
  --target . \
  --project test \
  --out reports/test
```

**Evidence Bundle Output**:
- `reports/<project>/<timestamp>/summary.json` - Machine-readable results
- `reports/<project>/<timestamp>/report.md` - Human-readable report
- `reports/<project>/<timestamp>/checks/*.log` - Individual check logs

### Automation Scripts

```bash
# Generate new skills using Vertex AI Gemini (overnight batch)
python 004-scripts/overnight_skill_generator.py --dry-run  # Preview only
python 004-scripts/overnight_skill_generator.py            # Actually generate

# Extract embedded code from skills to scripts/ folders
python 004-scripts/add_scripts_to_skills.py
```

## Architecture

### Three-Layer Plugin/Skill System

1. **Claude Skills** (`003-skills/.claude/skills/nixtla-*/`)
   - AI prompts that transform Claude's behavior
   - Auto-activate when Claude detects relevant context
   - **26 production skills** (all at 100% L4 quality):
     - 8 original: timegpt-lab, experiment-architect, schema-mapper, usage-optimizer, etc.
     - 5 core-forecasting: anomaly-detector, cross-validator, exogenous-integrator, timegpt2-migrator, uncertainty-quantifier
     - 10 prediction-markets: polymarket-analyst, market-risk-analyzer, contract-schema-mapper, correlation-mapper, arbitrage-detector, event-impact-modeler, liquidity-forecaster, batch-forecaster, forecast-validator, model-selector
     - **3 development-acceleration (NEW - Epic 2)**:
       - **plugin-scaffolder**: Scaffold production plugins from PRD documents (519 LOC)
       - **prd-to-code**: Transform PRDs into implementation task lists with TodoWrite (306 LOC)
       - **demo-generator**: Generate Jupyter notebooks for statsforecast/mlforecast/timegpt (442 LOC)

2. **Plugins** (`005-plugins/*/`)
   - Complete applications with MCP servers, tests, Python backends
   - Working: nixtla-baseline-lab, nixtla-bigquery-forecaster, nixtla-search-to-slack

3. **Slash Commands** (`005-plugins/*/commands/*.md`)
   - User-invoked commands like `/nixtla-baseline-m4`

### Key Source Files

| File | Purpose |
|------|---------|
| `005-plugins/nixtla-baseline-lab/scripts/nixtla_baseline_mcp.py` | MCP server exposing forecasting tools |
| `005-plugins/nixtla-baseline-lab/tests/run_baseline_m4_smoke.py` | Golden task test harness |
| `006-packages/nixtla-claude-skills-installer/nixtla_skills_installer/core.py` | Skills installation logic |
| `003-skills/.claude/skills/*/SKILL.md` | Individual skill definitions |

### MCP Server Pattern

The baseline lab MCP server (`nixtla_baseline_mcp.py`) exposes 4 tools:
- `run_baselines` - Run statsforecast models on M4/custom data
- `get_nixtla_compatibility_info` - Library version info
- `generate_benchmark_report` - Markdown report from metrics CSV
- `generate_github_issue_draft` - GitHub issue template with reproducibility info

## Enterprise Compliance & Quality Standards

### Validator v2 (Enterprise + Strict Quality Mode)

**Location**: `004-scripts/validate_skills_v2.py`

**Purpose**: Combines Anthropic 2025 spec + Intent Solutions enterprise standard + Nixtla strict quality mode.

**Enterprise Required Fields**:
```yaml
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
version: "1.0.0"
```

**Nixtla Strict Quality Requirements**:
1. **Description Must Include**: "Use when..." and "Trigger with..." phrases
2. **Unscoped Bash Forbidden**: All Bash must be scoped (e.g., `Bash(python:*)`)
3. **Required Body Sections** (8 sections):
   - Overview, Prerequisites, Instructions, Output, Error Handling, Examples, Resources
4. **Reserved Words Forbidden**: No "anthropic" or "claude" in name/description
5. **L4 Quality Scoring**: 100% maintained across all 26 skills

**Run Validator**:
```bash
# Check all skills
python 004-scripts/validate_skills_v2.py

# Verbose mode (show all errors)
python 004-scripts/validate_skills_v2.py --verbose

# Auto-fix enterprise fields (bulk operation)
python 004-scripts/bulk_add_enterprise_fields.py --dry-run  # Preview
python 004-scripts/bulk_add_enterprise_fields.py            # Apply
```

**CI/CD Integration**: `.github/workflows/skills-validation.yml` blocks merges if validation fails.

**Current Status**:
- ✅ 26/26 production skills compliant (100%)
- ✅ 5/5 plugin-bundled skills compliant (100%)
- ✅ 2/2 root-level skills compliant (100%)
- ✅ Total: 33/33 skills enterprise-ready

### Bulk Enterprise Fields Updater

**Script**: `004-scripts/bulk_add_enterprise_fields.py`

Automatically adds/updates `author` and `license` fields across all SKILL.md files while preserving YAML formatting.

**Features**:
- Dry-run mode for safe previewing
- Automatic field ordering (name → description → allowed-tools → version → author → license)
- Excludes backup directories
- YAML-preserving (no formatting damage)

**Usage**:
```bash
# Preview changes
python 004-scripts/bulk_add_enterprise_fields.py --dry-run

# Apply to production skills
python 004-scripts/bulk_add_enterprise_fields.py

# Apply to plugin-bundled skills
python 004-scripts/bulk_add_enterprise_fields.py --path 005-plugins
```

## Development Workflow

### Commit Message Convention

Follow **Conventional Commits** format for all commits:

```bash
# Format: <type>(<scope>): <description>

# Examples:
feat(skills): add nixtla-timegpt-lab skill
fix(baseline-lab): correct M4 data loading bug
docs(readme): update installation instructions
chore(ci): upgrade pytest to 7.4.0
test(skills): add L4 quality validation tests
refactor(plugins): extract common MCP server logic
style(scripts): format with black
perf(baseline-lab): optimize forecast computation
```

**Types**: `feat`, `fix`, `docs`, `chore`, `test`, `refactor`, `style`, `perf`, `ci`, `build`

**Scopes**: `skills`, `plugins`, `scripts`, `docs`, `ci`, `tests`, `packages`

**Reference Doc IDs** when applicable:
```bash
git commit -m "082-AA-AUDT: complete phase 1 audit"
git commit -m "feat(skills): 075-PP-PLAN implement polymarket-analyst"
```

**Breaking Changes**:
```bash
feat(skills)!: change skill frontmatter schema to v2.0

BREAKING CHANGE: All skills must update to new schema format
```

### Code Style & Formatting

**Indentation**: 4 spaces for Python (see `.editorconfig`)
**Line Length**: ≤100 characters (Black/Flake8 enforced)
**Format**: `black .` (auto-fix)
**Imports**: `isort .` (auto-fix)
**Lint**: `flake8 .` (check only)
**Type Hints**: `mypy <path>` (optional, not enforced)

**Naming Conventions**:
- Plugin folders: `kebab-case` (e.g., `nixtla-forecast-explainer`)
- Python modules/functions: `snake_case`
- Python classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`

### Pull Request Workflow

**Before Opening PR**:
```bash
# 1. Run validation
python 004-scripts/validate_skills_v2.py --fail-on-warn
bash 004-scripts/validate-all-plugins.sh .

# 2. Run tests
pytest -v -m "not integration"

# 3. Check formatting
black --check .
isort --check-only .
flake8 .

# 4. Update docs if needed
# Add entry to CHANGELOG.md if user-facing change
# Update 000-docs/ if behavior/architecture changed
```

**PR Description Must Include**:
- **What**: Summary of changes (link to doc ID if applicable)
- **Why**: Problem being solved or feature being added
- **How to Test**: Commands to verify the change works
- **Linked Issues**: Reference GitHub issues or Beads IDs
- **Required Env Vars**: Any new environment variables (never include actual secrets)

**PR Checks (CI/CD)**:
- `.github/workflows/ci.yml` - Main validation (MUST PASS to merge)
- `.github/workflows/skills-validation.yml` - Skills compliance
- `.github/workflows/plugin-validator.yml` - Plugin schema validation
- Additional checks may run based on changed files

**After Merge**:
- Update AAR docs in `000-docs/` if significant work
- Run `bd sync` if using Beads for issue tracking

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
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: "MIT"
```

**Forbidden fields**: priority, audience, when_to_use

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

## Skills Testing Framework

**Location**: `tests/skills/`

### Test Levels

| Level | Name | Description | Required |
|-------|------|-------------|----------|
| **L1** | Structural | SKILL.md exists, frontmatter valid, scripts exist, syntax valid | CRITICAL |
| **L2** | Functional | Scripts importable, CLI interface works (--help) | CRITICAL |
| **L4** | Quality | Description quality scoring (100% required) | CRITICAL |

### Success Criteria

**L1/L2/L4 must pass** - All are critical requirements
- L1/L2: Skills are broken without these
- L4: Required for optimal auto-activation and discoverability (100% mandatory)

**Current status**: `tests/skills/TEST_RESULTS_2025-12-10.md`
- 23/23 skills pass L1/L2 (CRITICAL)
- 23/23 skills at 100% L4 quality

### Run Tests

```bash
python tests/skills/test_all_skills.py                 # All tests, all skills
python tests/skills/test_all_skills.py --skill NAME    # Single skill
python tests/skills/test_all_skills.py --level 4       # L4 quality only
python tests/skills/test_all_skills.py --output DIR    # Custom output dir
python tests/skills/test_all_skills.py --json          # JSON output
```

### Test Files

- `tests/skills/test_all_skills.py` - Main test runner (569 lines)
- `tests/skills/SUCCESS_CRITERIA.md` - Per-skill success definitions from PRD/ARD
- `tests/skills/TEST_RESULTS_*.md` - Timestamped test results
- `tests/skills/results/*.json` - Individual skill test outputs

## Python Environments

| Component | Python | Location |
|-----------|--------|----------|
| Skills installer | 3.8+ | `006-packages/nixtla-claude-skills-installer/` |
| Baseline lab | 3.10+ | `005-plugins/nixtla-baseline-lab/.venv-nixtla-baseline/` |
| BigQuery forecaster | 3.10+ | `005-plugins/nixtla-bigquery-forecaster/.venv/` |

## CI/CD Workflows

All in `.github/workflows/`:
- `ci.yml` - Main validation pipeline (required to merge)
- `skills-validation.yml` - Claude Skills strict compliance validator
- `nixtla-baseline-lab-ci.yml` - Baseline lab plugin tests
- `skills-installer-ci.yml` - Skills installer tests
- `plugin-validator.yml` - Plugin schema validation
- `gemini-code-assist-trigger.yml` - Gemini Code Assist PR review trigger
- `gemini-daily-audit.yml` - Daily automated audit
- `timegpt-real-smoke.yml` - TimeGPT API integration smoke tests
- `deploy-bigquery-forecaster.yml` - BigQuery Cloud Functions deployment

## Critical Messaging

**This is experimental/prototype work** for business development:
- Use: "experimental", "prototype", "showcase", "demonstrates value"
- Avoid: "production-ready", "enterprise-grade", "guaranteed"

## Version & Release

**Current**: 1.8.1 (source of truth: `VERSION`)

See `CHANGELOG.md` for full history. Release process:
1. Update `VERSION` file
2. Update `CHANGELOG.md` with release highlights, contributors, features
3. Create release AAR in `000-docs/` (After Action Review)
4. Tag: `git tag -a v1.X.Y -m "Release v1.X.Y"`
5. Push tag: `git push origin v1.X.Y`

## Skill Extraction Standard

**New in 1.6+**: Skills must extract embedded Python/shell code to separate files.

- **Scripts location**: `003-skills/.claude/skills/{skill-name}/scripts/`
- **Templates location**: `003-skills/.claude/skills/{skill-name}/assets/templates/`
- **Why**: Prevents SKILL.md from becoming unwieldy, enables code reuse
- **Validator**: `python 004-scripts/validate_skills_v2.py` checks compliance

Recent extractions (Dec 2025):
- nixtla-experiment-architect, nixtla-prod-pipeline-generator, nixtla-schema-mapper
- nixtla-timegpt-lab, nixtla-timegpt-finetune-lab, nixtla-usage-optimizer
- nixtla-arbitrage-detector, nixtla-batch-forecaster

See git log for extraction commit pattern: `fix(skills): extract {skill} embedded code to scripts`

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: statsforecast` | `pip install -r scripts/requirements.txt` (in plugin dir) |
| `ModuleNotFoundError` (general) | `pip install -e . && pip install -r requirements-dev.txt` |
| Tests fail with import error | `export PYTHONPATH=$PWD` or activate venv |
| Permission denied on script | `chmod +x scripts/*.sh` or `chmod +x 004-scripts/*.sh` |
| Plugin not found after install | Restart Claude Code to reload plugin registry |
| Smoke test timeout | First run downloads M4 data (~30MB), subsequent runs are fast |
| `NIXTLA_TIMEGPT_API_KEY not set` | Only needed for TimeGPT features, not baseline lab (statsforecast) |
| Python version error | Need Python 3.9+ (`python3 --version`) |
| Coverage report missing | Check `001-htmlcov/` directory after running `pytest --cov` |
| Black/isort conflicts | Run `black .` first, then `isort .` |
| Pytest markers not working | Ensure `pytest.ini` is in repo root |
| Validation failures | Run `python 004-scripts/validate_skills_v2.py --verbose` for details |
| Git hooks not running | `bd hooks install` (if using Beads) |
| Virtual environment issues | Delete `venv/` and re-run `./004-scripts/setup-dev-environment.sh` |

**Still stuck?**
1. Check recent AAR docs in `000-docs/` for context
2. Run health check: See "First 5 Minutes - Health Check" section above
3. Open GitHub issue with error logs

## Post-Compact Context Restoration

**After every context compaction, immediately read these files:**

1. `000-docs/000a-skills-schema/SKILLS-STANDARD-COMPLETE.md` - Skills schema standard
2. Last two AAR docs in `000-docs/` (highest numbered `*-AA-AAR-*.md` or `*-AA-AACR-*.md` files)

This ensures continuity of project standards and recent work context.

<!-- bv-agent-instructions-v1 -->

---

## Beads Workflow Integration

This project uses [beads_viewer](https://github.com/Dicklesworthstone/beads_viewer) for issue tracking. Issues are stored in `.beads/` and tracked in git.

### Essential Commands

```bash
# View issues (launches TUI - avoid in automated sessions)
bv

# CLI commands for agents (use these instead)
bd ready              # Show issues ready to work (no blockers)
bd list --status=open # All open issues
bd show <id>          # Full issue details with dependencies
bd create --title="..." --type=task --priority=2
bd update <id> --status=in_progress
bd close <id> --reason="Completed"
bd close <id1> <id2>  # Close multiple issues at once
bd sync               # Commit and push changes
```

### Workflow Pattern

1. **Start**: Run `bd ready` to find actionable work
2. **Claim**: Use `bd update <id> --status=in_progress`
3. **Work**: Implement the task
4. **Complete**: Use `bd close <id>`
5. **Sync**: Always run `bd sync` at session end

### Key Concepts

- **Dependencies**: Issues can block other issues. `bd ready` shows only unblocked work.
- **Priority**: P0=critical, P1=high, P2=medium, P3=low, P4=backlog (use numbers, not words)
- **Types**: task, bug, feature, epic, question, docs
- **Blocking**: `bd dep add <issue> <depends-on>` to add dependencies

### Session Protocol

**Before ending any session, run this checklist:**

```bash
git status              # Check what changed
git add <files>         # Stage code changes
bd sync                 # Commit beads changes
git commit -m "..."     # Commit code
bd sync                 # Commit any new beads changes
git push                # Push to remote
```

### Best Practices

- Check `bd ready` at session start to find available work
- Update status as you work (in_progress → closed)
- Create new issues with `bd create` when you discover tasks
- Use descriptive titles and set appropriate priority/type
- Always `bd sync` before ending session

<!-- end-bv-agent-instructions -->
