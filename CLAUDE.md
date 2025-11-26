# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Private agentic engineering workspace for Nixtla time series forecasting. Built on Bob's Brain architecture (Vertex AI Agent Engine), this project wraps Nixtla's stack (TimeGPT, StatsForecast, MLForecast, NeuralForecast) with "junior engineer" agents that automate repetitive workflows.

**Status**: Experimental private collaboration between Intent Solutions and Nixtla.

## Quick Start Commands

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install project in editable mode
pip install -e .

# Run all validation checks
./scripts/validate-all-plugins.sh
./scripts/validate-marketplace.sh
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage (must meet 60% threshold)
pytest --cov=plugins --cov=examples --cov-report=term-missing

# Run specific test categories
pytest -m unit              # Unit tests only
pytest -m integration       # Integration tests only
pytest -m "not slow"        # Exclude slow tests

# Run plugin-specific tests
pytest plugins/nixtla-baseline-lab/tests/
```

### Code Quality
```bash
# Format code with Black (line length: 100)
black .

# Sort imports with isort
isort .

# Type checking with mypy
mypy plugins/ examples/

# Linting
flake8 plugins/ examples/
```

## Nixtla Baseline Lab Plugin

The primary working component in this repository. This plugin demonstrates all Claude Code plugin capabilities.

### Installation & Setup
```bash
# Navigate to plugin directory
cd plugins/nixtla-baseline-lab

# Run automated setup (creates virtualenv and installs dependencies)
/nixtla-baseline-setup

# Or use the setup script directly
./scripts/setup_nixtla_env.sh --venv
```

### Running Baseline Forecasts
```bash
# M4 Daily benchmark with default settings (14-day horizon, 50 series)
/nixtla-baseline-m4

# Custom parameters
/nixtla-baseline-m4 horizon=7 series_limit=25

# Custom CSV dataset
/nixtla-baseline-m4 --dataset-type csv --csv-path /path/to/data.csv

# With visualization plots
/nixtla-baseline-m4 --enable-plots

# Include TimeGPT comparison (requires NIXTLA_TIMEGPT_API_KEY)
/nixtla-baseline-m4 --include-timegpt
```

### Understanding Results

After running baselines, ask the AI Skill to interpret results:
```
Which baseline model performed best overall and why?
```

The Skill (`nixtla-baseline-review`) reads the generated CSV metrics and provides AI-powered interpretation of sMAPE and MASE scores.

## High-Level Architecture

The system follows an **orchestrator + specialist agents** pattern:

```
User → Orchestrator Agent → Specialist Agents → Nixtla Tools/GitHub
```

**Implemented Components**:
- `plugins/nixtla-baseline-lab/` - Production-ready forecasting plugin (v0.6.0)
  - Commands: `/nixtla-baseline-m4`, `/nixtla-baseline-setup`
  - Agents: `nixtla-baseline-analyst` for result interpretation
  - Skills: `nixtla-baseline-review` for AI-powered metric analysis
  - MCP Server: `nixtla-baseline-mcp` with `run_baselines` tool
- `claude-code-plugins-plus/` - Plugin marketplace with 200+ Claude Code plugins

**Planned Specialist Agents**:
- **Backtest QA** - Run backtests on benchmark datasets, compare models
- **TimeGPT Runner** - Manage TimeGPT experiments with different configs
- **CI Triage** - Parse CI failures, propose fixes
- **Doc Sync** - Detect drift between code and documentation
- **Anomaly Monitor** - Detect anomalies using TimeGPT methods

## Project Structure

```
nixtla/
├── plugins/
│   └── nixtla-baseline-lab/     # ✅ Production plugin (v0.6.0)
│       ├── scripts/
│       │   ├── nixtla_baseline_mcp.py    # MCP server implementation
│       │   ├── timegpt_client.py         # TimeGPT integration
│       │   └── setup_nixtla_env.sh       # Automated setup
│       ├── commands/
│       │   ├── nixtla-baseline-m4.md     # M4 baseline command
│       │   └── nixtla-baseline-setup.md  # Setup command
│       ├── agents/                        # Subagent definitions
│       ├── skills/                        # AI skills for interpretation
│       ├── tests/                         # Golden task harness
│       └── data/                          # Benchmark datasets
├── claude-code-plugins-plus/              # Plugin marketplace
├── 000-docs/                              # Technical documentation
├── scripts/                               # Automation scripts
│   ├── setup-dev-environment.sh
│   ├── validate-all-plugins.sh
│   └── validate-marketplace.sh
├── tests/                                 # Repository-level tests
├── examples/                              # Usage examples
├── pyproject.toml                         # Python package config
├── pytest.ini                             # Test configuration
└── requirements.txt / requirements-dev.txt
```

## Nixtla Integration Patterns

Reference code patterns for Nixtla API usage:

```python
# TimeGPT
from nixtla import NixtlaClient
client = NixtlaClient(api_key='YOUR_API_KEY')
forecast = client.forecast(df=data, h=24, freq='H', level=[80, 90, 95])

# StatsForecast
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA, AutoETS, SeasonalNaive
sf = StatsForecast(models=[AutoARIMA(season_length=12)], freq='M')
sf.fit(df)
forecasts = sf.predict(h=12)

# MLForecast
from mlforecast import MLForecast
from sklearn.ensemble import RandomForestRegressor
mlf = MLForecast(models=[RandomForestRegressor()], freq='D', lags=[1,7,14])
mlf.fit(df)
predictions = mlf.predict(h=30)
```

## CI/CD and Validation

### GitHub Actions Workflows
```bash
# Check workflow status
cat .github/workflows/nixtla-baseline-lab-ci.yml

# Workflows run on:
# - Every push to main
# - All pull requests
# - Manual workflow_dispatch
```

### CI Guarantees (when green ✅)
- Baseline runs produce valid CSV outputs with expected metric ranges
- Golden task harness passes (5-step validation)
- Setup script succeeds on Ubuntu/Linux
- TimeGPT integration is opt-in (graceful degradation)
- Test artifacts preserved for 7 days
- Coverage meets 60% minimum threshold

### Golden Task Validation
The plugin includes a comprehensive test harness that validates:
1. CSV schema correctness (columns: series_id, model, sMAPE, MASE)
2. Metric ranges (sMAPE: 0-200%, MASE: >0)
3. Summary content validation
4. Model coverage (SeasonalNaive, AutoETS, AutoTheta)
5. Error handling and graceful failures

## Document Organization

Documentation in `000-docs/` follows the Document Filing System v3.0:

**Format**: `NNN-CC-ABCD-description.md`

**Key Documents**:
- **6767-OD-OVRV-nixtla-baseline-lab-product-overview.md** - Product overview, user journey
- **6767-OD-ARCH-nixtla-claude-plugin-poc-baseline-lab.md** - Technical architecture
- **6767-PP-PLAN-nixtla-claude-plugin-poc-baseline-lab.md** - Implementation roadmap
- **015-022-AA-AACR-phase-NN-*.md** - Phase-by-phase After-Action Reports (AARs)
- **023-QA-TEST-nixtla-baseline-lab-test-coverage.md** - Test coverage report

**Category Codes**:
- **PP** - Planning & Product requirements
- **AA** - Audits & After-Action Reports
- **AT** - Architecture & Technical design
- **OD** - Overview & Documentation
- **QA** - Quality Assurance & Testing

## Environment Variables

**Required for TimeGPT Integration** (optional feature):
```bash
NIXTLA_TIMEGPT_API_KEY=your_api_key_here
```

**Plugin Development**:
```bash
# No environment variables required for baseline models
# Baselines use public M4 data and open-source libraries
```

## Key Dependencies

**Baseline Lab Plugin**:
- `statsforecast>=1.5.0` - Classical forecasting methods
- `datasetsforecast>=0.0.8` - M4 benchmark datasets
- `nixtla>=0.5.1` - TimeGPT client (optional)
- `pandas>=2.0.0` - Data manipulation
- `matplotlib>=3.7.0` - Visualization (optional)

**Development**:
- `pytest>=7.4.0` - Testing framework
- `pytest-cov>=4.1.0` - Coverage reporting
- `black>=23.0.0` - Code formatting
- `mypy>=1.4.0` - Type checking
- `flake8>=6.0.0` - Linting

## Reference Architecture

This project adapts patterns from **Bob's Brain** (https://github.com/jeremylongshore/bobs-brain):

**Core Patterns**:
- **Vertex AI Agent Engine** for orchestration
- **A2A protocol** for agent communication
- **Golden tasks** for validation
- **CI-only deployments** with guardrails
- **Human-in-the-loop** review for all changes
- **ARV-style validation** before deployment

**Specialist Agent Architecture**:
- Orchestrator delegates to domain-specific agents
- Each specialist has deep knowledge of one workflow
- Agents communicate through structured interfaces
- Comprehensive test coverage and telemetry

## Common Development Workflows

### Adding a New Plugin Command
1. Create `commands/command-name.md` with YAML frontmatter
2. Define parameters and usage examples
3. Implement MCP tool in `scripts/` if needed
4. Add tests in `tests/`
5. Update plugin README

### Running the Full Test Suite
```bash
# Run validation scripts first
./scripts/validate-all-plugins.sh
./scripts/validate-marketplace.sh

# Then run pytest
pytest --cov=plugins --cov=examples --cov-report=term-missing

# Check coverage threshold (must be ≥60%)
```

### Debugging Plugin Issues
```bash
# Check MCP server logs
cat plugins/nixtla-baseline-lab/.mcp.json

# Run baseline script directly
cd plugins/nixtla-baseline-lab
python scripts/nixtla_baseline_mcp.py

# Validate virtualenv setup
ls -la .venv-nixtla-baseline/

# Test with dry-run
/nixtla-baseline-m4 series_limit=1 horizon=1
```

### Updating Documentation
```bash
# Follow Document Filing System v3.0 format
# See: 000-docs/003-DR-META-document-standards.md

# Create new doc
# Format: NNN-CC-ABCD-description.md
# Example: 024-AA-AUDT-new-audit-report.md
```

## Testing Philosophy

**Golden Task Harness**:
- Every plugin has a golden task that validates core functionality
- Tests run on every CI build
- Metrics must fall within expected ranges
- Exit code 0 required for CI success

**Test Organization**:
- `tests/` - Repository-level tests
- `plugins/*/tests/` - Plugin-specific tests
- Use pytest markers: `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.slow`

**Coverage Requirements**:
- Minimum 60% coverage enforced by pytest
- Focus on critical paths and error handling
- Use `pytest --cov-report=html` for detailed coverage reports

---

## Current State Snapshot (Phase 7 – v0.7.0)

**Last Updated**: 2025-11-26

This section helps future AI agents working in this repository understand the current state after Phases 1-6 implementation.

### What Exists Now

**Primary Component**:
- **Nixtla Baseline Lab Plugin** – The ONLY fully implemented and working component in this repository.
  - Location: `plugins/nixtla-baseline-lab/`
  - Status: Experimental prototype (v0.7.0)
  - Purpose: Reproducible statsforecast baseline experiments inside Claude Code.

**Core Capabilities** (Phases 1-6):
1. **Offline Statsforecast Baselines** – SeasonalNaive, AutoETS, AutoTheta models on M4/custom CSV.
2. **Metrics & Benchmarking** – sMAPE, MASE calculation + Markdown benchmark reports.
3. **Repro Bundles** – `run_manifest.json`, `compat_info.json` for reproducibility.
4. **GitHub Issue Draft Generator** – Pre-filled Markdown drafts for `nixtla/statsforecast`.
5. **Optional TimeGPT Showdown** – Opt-in comparison (disabled by default, requires API key).
6. **CI Validation** – GitHub Actions golden task harness (offline-only).

**Key Files That Must Stay Accurate**:
- **Root README.md** – Repository overview with modest, technically accurate framing.
- **docs/index.md** – Docs site home page aligned with plugin capabilities.
- **docs/nixtla-baseline-lab.md** – Plugin-level documentation page.
- **000-docs/6767-OD-OVRV-nixtla-baseline-lab-overview.md** – Compact canonical overview.
- **plugins/nixtla-baseline-lab/README.md** – Complete plugin manual.
- **Phase AARs (015-AA-AACR-* through 033-AA-AACR-*)** – Implementation history.

### Critical Messaging Guidelines

**Always maintain this framing**:
- This is a **community integration**, not an official Nixtla product.
- **Maintained by**: Intent Solutions (Jeremy Longshore).
- **Sponsored by**: Nixtla (Max Mergenthaler – early/enterprise supporter).
- Status: **Experimental prototype** / **developer sandbox**.

**Language to AVOID**:
- ❌ "production-ready", "enterprise-grade", "guaranteed", "always", "will", "promises"
- ❌ Any implication that Nixtla has formally adopted or endorsed this as an official product
- ❌ SLAs, support commitments, or performance guarantees

**Language to PREFER**:
- ✅ "experimental", "prototype", "developer sandbox", "integration", "helper"
- ✅ "intended to help developers...", "designed to make it easier to..."
- ✅ "reproducible experiments", "sharing context", "reference implementation"

### What Must Not Be Broken

**Offline-Only Default Behavior**:
- Plugin must work without ANY API keys or network calls by default.
- TimeGPT is strictly opt-in (requires `include_timegpt=true` AND `NIXTLA_TIMEGPT_API_KEY`).
- CI remains offline-only (no network dependencies).

**Backward Compatibility**:
- Existing commands, parameters, and tool schemas must not break.
- Golden task harness must continue to pass on every CI run.
- File outputs (CSV, summary, benchmark report) must maintain current structure.

**Documentation Accuracy**:
- Any changes to plugin behavior must be reflected in:
  - Root README.md
  - Plugin README.md  
  - Docs site pages (index.md, nixtla-baseline-lab.md)
  - Relevant phase AARs

### Future Work Reminders

**What Phases 1-6 Did NOT Implement**:
- ❌ Multi-agent orchestration system (mentioned in old README, never built)
- ❌ Bob's Brain-style specialist agents (conceptual only, not implemented)
- ❌ Automated PR posting or issue posting (only draft generators exist)
- ❌ Production-grade TimeGPT integration (only experimental opt-in showdown)

**If Adding New Features**:
1. Maintain offline-only default (opt-in for network calls).
2. Update ALL relevant docs (README, plugin README, docs site, overview).
3. Add golden task validation if core functionality changes.
4. Create phase AAR documenting changes.
5. Use modest framing (experimental, prototype, helper).

### Contact & Escalation

**For questions about plugin architecture or implementation**:
- Review phase AARs (000-docs/015-AA-AACR-* through 033-AA-AACR-*).
- Check overview doc (000-docs/6767-OD-OVRV-nixtla-baseline-lab-overview.md).
- Reference plugin README (plugins/nixtla-baseline-lab/README.md).

**For questions about Nixtla collaboration or messaging**:
- **Jeremy Longshore** (Intent Solutions): jeremy@intentsolutions.io
- **Max Mergenthaler** (Nixtla): max@nixtla.io

---

**End of Current State Snapshot**

This snapshot reflects the state as of Phase 7 (Docs Refresh). Future agents should treat this as the baseline understanding of what exists and what must be preserved.
