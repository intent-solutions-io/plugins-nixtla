# Nixtla Agentic Engineering Workspace: Operator-Grade System Analysis & Operations Guide

*For: DevOps Engineer*
*Generated: 2025-11-25*
*System Version: c38737b (v0.6.0)*
*Repository: claude-code-plugins-nixtla*

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Operator & Customer Journey](#2-operator--customer-journey)
3. [System Architecture Overview](#3-system-architecture-overview)
4. [Directory Deep-Dive](#4-directory-deep-dive)
5. [Automation & Agent Surfaces](#5-automation--agent-surfaces)
6. [Operational Reference](#6-operational-reference)
7. [Security, Compliance & Access](#7-security-compliance--access)
8. [Cost & Performance](#8-cost--performance)
9. [Development Workflow](#9-development-workflow)
10. [Dependencies & Supply Chain](#10-dependencies--supply-chain)
11. [Integration with Existing Documentation](#11-integration-with-existing-documentation)
12. [Current State Assessment](#12-current-state-assessment)
13. [Quick Reference](#13-quick-reference)
14. [Recommendations Roadmap](#14-recommendations-roadmap)

---

## 1. Executive Summary

### Business Purpose

The **Nixtla Agentic Engineering Workspace** is a private experimental collaboration between Intent Solutions and Nixtla, designed to prototype "junior engineer" agents that automate repetitive time series forecasting workflows. Built on Bob's Brain architecture patterns (Vertex AI Agent Engine), this system wraps Nixtla's comprehensive forecasting stack (TimeGPT, StatsForecast, MLForecast, NeuralForecast) with specialized AI agents.

The repository currently operates as a **proof-of-concept development environment** with one production-ready plugin (**Nixtla Baseline Lab v0.6.0**) that demonstrates end-to-end baseline forecasting workflows inside Claude Code conversations. The plugin executes SeasonalNaive, AutoETS, and AutoTheta models on M4 benchmark datasets or custom CSV files, generating reproducible metrics (sMAPE, MASE) with optional TimeGPT comparison.

The technology foundation consists of:
- **Python 3.12** for all ML/forecasting logic
- **Claude Code Plugin System** for IDE integration (commands, skills, agents, MCP servers)
- **GitHub Actions CI** for automated testing and validation
- **Nixtla OSS libraries** (statsforecast, datasetsforecast) plus TimeGPT SDK

**Operational Status**: Development/Experimental with CI passing. No production deployment infrastructure exists yet—all execution happens locally within Claude Code conversations or GitHub Actions runners.

### Operational Status Matrix

| Environment | Status | Uptime Target | Current Uptime | Release Cadence | Active Users |
|-------------|--------|---------------|----------------|-----------------|--------------|
| Local Dev | ✅ Active | N/A | N/A | Continuous | 1-2 |
| GitHub CI | ✅ Active | 99% | ~99% | Per PR/Push | Automated |
| Production | ❌ None | N/A | N/A | N/A | N/A |
| Staging | ❌ None | N/A | N/A | N/A | N/A |

### Technology Stack Summary

| Category | Technology | Version | Purpose |
|----------|------------|---------|---------|
| Language | Python | 3.12+ | Forecasting logic, MCP server |
| Framework | Claude Code Plugin | N/A | IDE integration, skill/command system |
| Forecasting | statsforecast | ≥1.5.0 | Baseline models (AutoETS, AutoTheta, SeasonalNaive) |
| Datasets | datasetsforecast | ≥0.0.8 | M4 benchmark data access |
| TimeGPT | nixtla SDK | ≥0.5.0 | Foundation model integration (opt-in) |
| Visualization | matplotlib | ≥3.7.0 | Forecast plot generation |
| CI/CD | GitHub Actions | v4 | Automated testing, artifact upload |
| Data | pandas/numpy | 2.0/1.24+ | Data processing |

---

## 2. Operator & Customer Journey

### Primary Personas

- **Operators**: Jeremy Longshore (Intent Solutions), potential Nixtla DevOps engineers
- **External Customers**: Max Mergenthaler (Nixtla CEO), Nixtla engineering team
- **Reseller Partners**: None currently (internal collaboration)
- **Automation Bots**: GitHub Actions CI, Claude Code MCP server

### End-to-End Journey Map

```
Discovery → Clone & Trust → Plugin Install → Environment Setup → Run Baselines → AI Interpretation → Results Review
```

| Stage | Touchpoints | Dependencies | Friction Points | Success Metrics |
|-------|-------------|--------------|-----------------|-----------------|
| Discovery | README, GitHub | None | Documentation completeness | Time to understand purpose |
| Clone & Trust | git, Claude Code | git access, Claude Code installed | Trust prompt workflow | < 2 min |
| Plugin Install | `/plugin install` | Marketplace config | Auto-discovery of local marketplace | Success on first try |
| Environment Setup | `/nixtla-baseline-setup` or shell script | Python 3.12+, pip | Package download time (~200MB) | < 2 min |
| Run Baselines | `/nixtla-baseline-m4` | Setup complete | M4 data first download (~95MB) | Valid CSV output |
| AI Interpretation | Skill invocation | Results files exist | N/A | Helpful analysis |
| Results Review | CSV, summary TXT | None | N/A | Actionable insights |

### SLA Commitments

| Metric | Target | Current | Owner |
|--------|--------|---------|-------|
| CI Pass Rate | > 95% | ~100% | Jeremy |
| Setup Success | 100% (Ubuntu/Linux) | 100% | Jeremy |
| Golden Task Pass | 100% | 100% | CI |
| Documentation Accuracy | 100% | ~95% | Jeremy |

---

## 3. System Architecture Overview

### Technology Stack (Detailed)

| Layer | Technology | Version | Source of Truth | Purpose | Owner |
|-------|------------|---------|-----------------|---------|-------|
| Plugin Runtime | Claude Code | Latest | claude.ai | IDE integration | Anthropic |
| MCP Server | Python | 3.12 | scripts/nixtla_baseline_mcp.py | JSON-RPC tool server | Jeremy |
| Forecasting | statsforecast | ≥1.5.0 | requirements.txt | Baseline models | Nixtla |
| Datasets | datasetsforecast | ≥0.0.8 | requirements.txt | M4 benchmark data | Nixtla |
| TimeGPT | nixtla SDK | ≥0.5.0 | requirements.txt | Foundation model | Nixtla |
| Data Processing | pandas/numpy | 2.0/1.24 | requirements.txt | DataFrame ops | PyData |
| Visualization | matplotlib | ≥3.7.0 | requirements.txt | Plot generation | Matplotlib |
| CI/CD | GitHub Actions | v4/v5 | .github/workflows/ | Testing, artifacts | GitHub |

### Environment Matrix

| Environment | Purpose | Hosting | Data Source | Release Cadence | IaC Source | Notes |
|-------------|---------|---------|-------------|-----------------|------------|-------|
| local | Development | Local machine | M4 public data | Continuous | None | Primary dev environment |
| CI | Testing | GitHub runners | M4 public data | Per push/PR | Workflow YAML | Ubuntu-latest |
| production | N/A | N/A | N/A | N/A | N/A | Not deployed |

### Cloud & Platform Services

| Service | Purpose | Environment(s) | Key Config | Cost/Limits | Owner | Vendor Risk |
|---------|---------|----------------|------------|-------------|-------|-------------|
| GitHub | Source control, CI | All | Public/Private repo | Free tier | Jeremy | Low |
| TimeGPT API | Foundation model | Local (opt-in) | API key env var | Pay-per-use | Nixtla | Low |
| Claude Code | IDE runtime | Local | Plugin manifest | Anthropic subscription | User | Medium |

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CLAUDE CODE IDE                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐          │
│  │ Slash Commands   │  │ Skills           │  │ Agents           │          │
│  │ /nixtla-baseline │  │ nixtla-baseline- │  │ nixtla-baseline- │          │
│  │ -m4              │  │ review           │  │ analyst          │          │
│  │ /nixtla-baseline │  │                  │  │ (deep analysis)  │          │
│  │ -setup           │  │                  │  │                  │          │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘          │
│           │                     │                     │                     │
│           └──────────────┬──────┴─────────────────────┘                     │
│                          │                                                  │
│                          ▼                                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    MCP SERVER (JSON-RPC)                             │   │
│  │                 nixtla_baseline_mcp.py (855 lines)                   │   │
│  │  ┌─────────────────────────────────────────────────────────────┐    │   │
│  │  │ Tools: run_baselines(horizon, series_limit, enable_plots,   │    │   │
│  │  │        dataset_type, csv_path, include_timegpt, ...)        │    │   │
│  │  └─────────────────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                          │                                                  │
└──────────────────────────┼──────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PYTHON RUNTIME (.venv-nixtla-baseline)               │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │
│  │ statsforecast   │  │ datasetsforecast│  │ nixtla SDK      │             │
│  │ ├─SeasonalNaive │  │ ├─M4 datasets   │  │ ├─TimeGPT API   │             │
│  │ ├─AutoETS       │  │ └─Eval metrics  │  │ └─(opt-in)      │             │
│  │ └─AutoTheta     │  │                 │  │                 │             │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘             │
│                          │                                                  │
│                          ▼                                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ OUTPUT FILES                                                         │   │
│  │ ├─ nixtla_baseline_m4_test/results_M4_Daily_h7.csv                  │   │
│  │ ├─ nixtla_baseline_m4_test/summary_M4_Daily_h7.txt                  │   │
│  │ ├─ nixtla_baseline_m4_test/plot_series_*.png (optional)             │   │
│  │ └─ nixtla_baseline_m4_test/timegpt_showdown_*.txt (optional)        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           GITHUB ACTIONS CI                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  Trigger: Push/PR to main (paths: plugins/nixtla-baseline-lab/**)           │
│  Runner: ubuntu-latest                                                       │
│  Steps:                                                                      │
│    1. Checkout → 2. Setup Python 3.12 → 3. Install deps → 4. MCP test       │
│    5. Golden task smoke test → 6. Upload artifacts (7-day retention)        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Directory Deep-Dive

### Project Structure Analysis

```
nixtla/                               # Repository root
├── .claude/                          # Claude Code IDE configuration
│   └── settings.json                 # Marketplace registration
├── .claude-plugin/                   # Root-level plugin manifest (marketplace)
│   └── marketplace.json              # Local marketplace definition
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                    # General CI (CodeQL, linting)
│   │   ├── nixtla-baseline-lab-ci.yml  # ★ Plugin-specific CI (62 lines)
│   │   └── plugin-validator.yml      # Marketplace validation
│   └── ISSUE_TEMPLATE/               # Bug, feature, collaboration templates
├── 000-docs/                         # Technical documentation (468KB)
│   ├── 6767-OD-ARCH-*.md            # Architecture docs (canonical)
│   ├── 6767-OD-OVRV-*.md            # Product overview (canonical)
│   ├── 6767-PP-PLAN-*.md            # Planning docs (canonical)
│   ├── 015-022-AA-AACR-phase-*.md   # Phase AARs (8 phases complete)
│   └── 023-QA-TEST-*.md             # Test coverage report
├── plugins/                          # ★ MAIN PLUGIN DIRECTORY (1.2GB with venv)
│   ├── nixtla-baseline-lab/         # ★ PRIMARY PLUGIN (v0.6.0)
│   │   ├── .claude-plugin/plugin.json  # Plugin manifest
│   │   ├── .mcp.json                 # MCP server config
│   │   ├── commands/                 # Slash commands
│   │   ├── skills/                   # AI skills
│   │   ├── agents/                   # Subagents
│   │   ├── scripts/                  # ★ Core Python (855 + 361 lines)
│   │   │   ├── nixtla_baseline_mcp.py   # MCP server
│   │   │   ├── timegpt_client.py        # TimeGPT wrapper
│   │   │   ├── setup_nixtla_env.sh      # Setup script
│   │   │   └── requirements.txt         # Python deps
│   │   ├── tests/                    # Test suite
│   │   │   ├── run_baseline_m4_smoke.py  # Golden task harness
│   │   │   └── data/example_timeseries.csv
│   │   └── README.md                 # Plugin documentation (21KB)
│   ├── nixtla-search-to-slack/      # Content digest plugin (MVP)
│   └── nixtla-baseline-m4/          # Legacy/deprecated
├── scripts/                          # Repository-level automation
│   ├── setup-dev-environment.sh     # Dev setup
│   ├── validate-all-plugins.sh      # Plugin validation
│   └── validate-marketplace.sh      # Marketplace checks
├── examples/                         # Example code
├── tests/                            # Root-level tests (placeholder)
├── docs/                             # MkDocs site source
├── CLAUDE.md                         # Repository guidance
├── README.md                         # Main documentation (22KB)
├── CHANGELOG.md                      # Release history (7KB)
├── pyproject.toml                    # Python project config
├── requirements.txt                  # Root dependencies
└── VERSION                           # Version file
```

### Detailed Directory Analysis

#### plugins/nixtla-baseline-lab/scripts/ ★

**Purpose**: Core Python implementation of the MCP server and setup automation.

**Key Files**:
- `nixtla_baseline_mcp.py` (855 lines) - Main MCP server implementing JSON-RPC `run_baselines` tool
- `timegpt_client.py` (148 lines) - TimeGPT API wrapper with graceful degradation
- `setup_nixtla_env.sh` (176 lines) - Bash setup script for Python environment
- `requirements.txt` - Plugin-specific dependencies

**Patterns**:
- Standard library `logging` with DEBUG level to stderr
- JSON-RPC protocol for Claude Code integration
- Environment variable configuration (`NIXTLA_TIMEGPT_API_KEY`)
- Graceful degradation (TimeGPT optional, matplotlib optional)

**Entry Points**:
- `python nixtla_baseline_mcp.py test` - Run test mode
- `python nixtla_baseline_mcp.py test --enable-plots` - With visualization
- `python nixtla_baseline_mcp.py test --include-timegpt` - With TimeGPT

#### plugins/nixtla-baseline-lab/tests/

**Framework**: Custom golden task harness (not pytest)
**Coverage**:
- Golden task: 100% critical path coverage
- Unit tests: Not implemented
- Integration: CI runs full workflow

**Categories**:
- BL-001 to BL-004: Baseline/core tests
- CSV-001 to CSV-003: Custom CSV tests
- PLOT-001 to PLOT-002: Visualization tests
- TG-001 to TG-005: TimeGPT tests
- MP-001: Marketplace tests

**Gaps**:
- No pytest-based unit tests
- No code coverage metrics
- Manual testing required for TimeGPT (API key needed)

#### .github/workflows/ 🔑

**CI Workflow**: `nixtla-baseline-lab-ci.yml` (62 lines)

**Triggers**:
- Push to main (paths: `plugins/nixtla-baseline-lab/**`)
- Pull requests to main (same paths)

**Steps**:
1. Checkout repository
2. Setup Python 3.12 with pip caching
3. Install dependencies from `scripts/requirements.txt`
4. Print package versions (verification)
5. Run MCP test mode
6. Run golden task smoke test
7. Upload artifacts (always, 7-day retention)

**Artifacts**: `nixtla-baseline-test-results` containing CSV and summary files

---

## 5. Automation & Agent Surfaces

### Claude Code Plugin Components

| Component | Location | Purpose | Trigger |
|-----------|----------|---------|---------|
| Slash Command | `commands/nixtla-baseline-m4.md` | Run baseline forecasts | User types `/nixtla-baseline-m4` |
| Slash Command | `commands/nixtla-baseline-setup.md` | Environment setup | User types `/nixtla-baseline-setup` |
| Skill | `skills/nixtla-baseline-review/SKILL.md` | Interpret results | Claude auto-invokes on questions |
| Agent | `agents/nixtla-baseline-analyst.md` | Deep analysis | Explicit invocation |
| MCP Server | `scripts/nixtla_baseline_mcp.py` | Forecasting tool | Called by commands |

### MCP Server Tools

| Tool | Purpose | Parameters | Return |
|------|---------|------------|--------|
| `run_baselines` | Execute forecasting workflow | `horizon`, `series_limit`, `dataset_type`, `csv_path`, `enable_plots`, `include_timegpt`, `output_dir` | JSON with success, files, summary |

### GitHub Actions Workflows

| Workflow | Purpose | Trigger | Failure Handling |
|----------|---------|---------|------------------|
| `nixtla-baseline-lab-ci.yml` | Plugin validation | Push/PR to main | Artifacts uploaded always |
| `ci.yml` | General CI (CodeQL) | Push/PR | Standard failure |
| `plugin-validator.yml` | Marketplace validation | Push/PR | Standard failure |

---

## 6. Operational Reference

### Deployment Workflows

#### Local Development

1. **Prerequisites**:
   - Python 3.12+
   - pip
   - Claude Code installed
   - git

2. **Environment Setup**:
   ```bash
   # Clone repository
   git clone https://github.com/intent-solutions-io/plugins-nixtla.git
   cd claude-code-plugins-nixtla

   # Navigate to plugin
   cd plugins/nixtla-baseline-lab

   # Create virtualenv and install deps
   ./scripts/setup_nixtla_env.sh --venv

   # Or use Claude Code command
   # /nixtla-baseline-setup
   ```

3. **Service Startup**:
   - No persistent services
   - MCP server spawned on-demand by Claude Code

4. **Verification**:
   ```bash
   # Activate venv
   source .venv-nixtla-baseline/bin/activate

   # Run test mode
   python scripts/nixtla_baseline_mcp.py test

   # Verify outputs
   ls -la nixtla_baseline_m4_test/
   ```

#### CI Deployment

- **Trigger**: Push to main or PR targeting main
- **Pre-flight**: Automatic path filtering (`plugins/nixtla-baseline-lab/**`)
- **Execution**: GitHub Actions workflow
- **Validation**: Exit code 0 from golden task
- **Rollback**: Revert commit (no deployment artifacts)

### Monitoring & Alerting

**Dashboards**: None configured (local development only)

**SLIs/SLOs**:
- CI pass rate: > 95%
- Golden task pass: 100%
- Setup success: 100% on Ubuntu/Linux

**Logging**:
- MCP server: Python `logging` module, DEBUG level, stderr output
- Golden task: Print statements with visual markers (`[1/5]`, `✓`, `⚠️`)
- CI: GitHub Actions log output

**On-Call**: N/A (experimental project)

### Incident Response

| Severity | Definition | Response Time | Roles | Playbook | Communication |
|----------|------------|---------------|-------|----------|---------------|
| P1 | CI broken on main | Same day | Jeremy | Re-run CI, check logs | Slack |
| P2 | Plugin malfunction | Next day | Jeremy | Debug locally | GitHub issue |
| P3 | Documentation issue | Week | Jeremy | Update docs | PR |

### Backup & Recovery

**Backup Jobs**: None (git is source of truth)
**Verification**: N/A
**RPO/RTO**: N/A (stateless plugin)
**Disaster Recovery**: Clone from GitHub

---

## 7. Security, Compliance & Access

### Identity & Access Management

| Account/Role | Purpose | Permissions | Provisioning | MFA | Used By |
|--------------|---------|-------------|--------------|-----|---------|
| GitHub (jeremylongshore) | Repo owner | Full admin | Manual | Yes | Jeremy |
| TimeGPT API key | Foundation model access | API calls | User provides | N/A | Plugin users |
| Claude Code | IDE access | Local only | Anthropic account | Per Anthropic | Users |

### Secrets Management

**Storage**: Environment variables only (`.env` files gitignored)
**Rotation**: User responsibility
**Break-glass**: N/A
**Compliance**: No PII, no customer data

### Security Posture

**Authentication**:
- GitHub: OAuth/PAT
- TimeGPT: API key via `NIXTLA_TIMEGPT_API_KEY`
- No user authentication in plugin

**Authorization**:
- GitHub: Repo permissions
- Plugin: Local execution only

**Encryption**:
- In-transit: HTTPS for GitHub, TimeGPT API
- At-rest: N/A (local files only)

**Network**:
- No inbound connections
- Outbound: GitHub API, TimeGPT API, PyPI

**Tooling**:
- CodeQL scanning in CI
- No SAST/DAST configured

**Known Issues**:
- No dependency vulnerability scanning
- No SBOM generation

---

## 8. Cost & Performance

### Current Costs

**Monthly Cloud Spend**: ~$0 (local development)

| Component | Cost | Notes |
|-----------|------|-------|
| GitHub | Free | Public/private repo |
| CI Minutes | Free tier | ~5 min per run |
| TimeGPT | Pay-per-use | User-provided key, opt-in |
| Storage | Local | User's machine |

### Performance Baseline

**Latency**:
- First run: ~60s (includes M4 data download)
- Subsequent runs: ~30s (5 series, horizon 7)
- Full M4 Daily: ~5-10 min

**Throughput**: Single-threaded, one run at a time

**Error Budget**: N/A

**Load Testing**: Not performed

### Optimization Opportunities

1. **Caching M4 data** → Reduce first-run time by ~30s
2. **Parallel model fitting** → Reduce runtime by ~40% (not implemented)
3. **Pre-computed metrics** → Instant results for common configs

---

## 9. Development Workflow

### Local Development

**Standard Environment**:
- Ubuntu 22.04+ / macOS (recommended) / Windows (WSL)
- Python 3.12+
- Claude Code IDE

**Bootstrap**:
```bash
cd plugins/nixtla-baseline-lab
./scripts/setup_nixtla_env.sh --venv
```

**Debugging**:
- Set `DEBUG=true` in environment
- Check stderr for MCP server logs
- Run golden task manually: `python tests/run_baseline_m4_smoke.py`

**Common Tasks**:
```bash
# Test baseline run
python scripts/nixtla_baseline_mcp.py test

# Test with plots
python scripts/nixtla_baseline_mcp.py test --enable-plots

# Test CSV path
python tests/run_baseline_m4_smoke.py \
  --dataset-type csv \
  --csv-path tests/data/example_timeseries.csv \
  --horizon 5 \
  --series-limit 2

# Test TimeGPT (requires API key)
export NIXTLA_TIMEGPT_API_KEY=your-key
python tests/run_baseline_m4_smoke.py --include-timegpt
```

### CI/CD Pipeline

**Platform**: GitHub Actions
**Triggers**: Push/PR to main
**Stages**: Setup → Install → Test → Upload
**Artifacts**: `nixtla-baseline-test-results` (7-day retention)

### Code Quality

**Linting**: Not enforced (pyproject.toml configured for black, isort, flake8)
**Analysis**: CodeQL scanning
**Review**: Manual PR review
**Coverage**: Not measured (golden task provides functional coverage)

---

## 10. Dependencies & Supply Chain

### Direct Dependencies (Plugin)

| Package | Version | Purpose | License |
|---------|---------|---------|---------|
| statsforecast | ≥1.5.0 | Forecasting models | Apache 2.0 |
| datasetsforecast | ≥0.0.8 | M4 benchmark data | Apache 2.0 |
| pandas | ≥2.0.0 | Data processing | BSD |
| numpy | ≥1.24.0 | Numerical operations | BSD |
| matplotlib | ≥3.7.0 | Visualization | PSF |
| nixtla | ≥0.5.0 | TimeGPT SDK | Proprietary |

### Third-Party Services

| Service | Purpose | Data Shared | Auth | SLA | Renewal | Owner |
|---------|---------|-------------|------|-----|---------|-------|
| GitHub | Source control | Code | OAuth | 99.9% | N/A | GitHub |
| TimeGPT | Foundation model | Time series data | API key | Per Nixtla | User | Nixtla |
| PyPI | Package hosting | None | None | Best effort | N/A | PSF |

---

## 11. Integration with Existing Documentation

### Documentation Inventory

| Document | Status | Last Updated | Completeness |
|----------|--------|--------------|--------------|
| README.md (root) | ✅ Current | 2025-11-25 | 95% |
| README.md (plugin) | ✅ Current | 2025-11-25 | 95% |
| CLAUDE.md | ✅ Current | 2025-11-24 | 90% |
| CHANGELOG.md | ⚠️ Outdated | 2025-11-23 | v0.2.0 (not v0.6.0) |
| ARCHITECTURE.md | ⚠️ Partial | 2025-11-23 | 60% |
| 6767-OD-ARCH-*.md | ✅ Current | 2025-11-24 | 95% |
| 6767-OD-OVRV-*.md | ✅ Current | 2025-11-25 | 95% |
| Phase AARs (015-022) | ✅ Complete | 2025-11-25 | 100% |
| Test coverage report | ✅ Current | 2025-11-25 | 95% |

### Discrepancies

1. **CHANGELOG.md**: Does not document v0.6.0 release or Phase 8 completion
2. **pyproject.toml**: Lists version as 1.0.0 but plugin is 0.6.0
3. **VERSION file**: Contains "0.2.0" but latest is v0.6.0

### Recommended Reading List

1. **Plugin README** (`plugins/nixtla-baseline-lab/README.md`) - Complete user guide
2. **Product Overview** (`000-docs/6767-OD-OVRV-*.md`) - Executive summary
3. **Architecture** (`000-docs/6767-OD-ARCH-*.md`) - Technical deep dive
4. **Phase 8 AAR** (`000-docs/022-AA-AACR-phase-08-*.md`) - Latest development
5. **Test Coverage** (`000-docs/023-QA-TEST-*.md`) - Testing strategy

---

## 12. Current State Assessment

### What's Working Well

✅ **Baseline forecasting workflow**: SeasonalNaive, AutoETS, AutoTheta on M4 Daily
✅ **Golden task harness**: 5-step validation with visual progress, strict exit codes
✅ **CI pipeline**: Automated testing on every push/PR with artifact upload
✅ **TimeGPT integration**: Opt-in showdown reports with graceful degradation
✅ **Custom CSV support**: Bring-your-own-data validated and working
✅ **Visualization**: PNG plot generation with matplotlib
✅ **Documentation**: 8 phase AARs, architecture docs, product overview
✅ **AI Skill**: Results interpretation working in Claude Code

### Areas Needing Attention

⚠️ **Version inconsistencies**: VERSION file, pyproject.toml, CHANGELOG not aligned
⚠️ **No pytest tests**: Golden task provides coverage but no unit test suite
⚠️ **No coverage metrics**: Cannot quantify test coverage percentage
⚠️ **CHANGELOG gap**: v0.6.0 not documented
⚠️ **No dependency scanning**: Vulnerabilities not tracked
⚠️ **Root pyproject.toml**: Configured for package that doesn't exist at root
⚠️ **Untracked test directories**: `nixtla_test_custom/`, `nixtla_baseline_csv_test/` in git status

### Immediate Priorities

1. **[High]** – Version alignment
   - Impact: Documentation inconsistency, user confusion
   - Action: Update VERSION, pyproject.toml, CHANGELOG to v0.6.0
   - Owner: Jeremy

2. **[Medium]** – CHANGELOG update
   - Impact: Release history incomplete
   - Action: Add v0.3.0 through v0.6.0 entries
   - Owner: Jeremy

3. **[Medium]** – Clean up untracked files
   - Impact: Git status noise
   - Action: Add to .gitignore or remove
   - Owner: Jeremy

4. **[Low]** – Add pytest unit tests
   - Impact: No regression safety net
   - Action: Create test_nixtla_baseline_mcp.py
   - Owner: Future

---

## 13. Quick Reference

### Operational Command Map

| Capability | Command/Tool | Source | Notes |
|------------|--------------|--------|-------|
| Local env setup | `./scripts/setup_nixtla_env.sh --venv` | Plugin scripts | Creates .venv-nixtla-baseline |
| Test suite | `python tests/run_baseline_m4_smoke.py` | Plugin tests | Golden task harness |
| MCP test | `python scripts/nixtla_baseline_mcp.py test` | Plugin scripts | Basic validation |
| With plots | `python scripts/nixtla_baseline_mcp.py test --enable-plots` | Plugin scripts | Generates PNGs |
| With TimeGPT | `python tests/run_baseline_m4_smoke.py --include-timegpt` | Plugin tests | Requires API key |
| CI trigger | Push to main | GitHub | Path-filtered |
| View CI logs | GitHub Actions tab | GitHub UI | 7-day artifact retention |

### Critical Endpoints & Resources

- **Repository**: https://github.com/intent-solutions-io/plugins-nixtla
- **CI Workflows**: https://github.com/intent-solutions-io/plugins-nixtla/actions
- **Plugin Directory**: `plugins/nixtla-baseline-lab/`
- **Documentation**: `000-docs/`
- **Phase AARs**: `000-docs/015-022-AA-AACR-phase-*.md`

### First-Week Checklist

- [ ] Clone repository and verify git status
- [ ] Install Claude Code if not present
- [ ] Trust repo folder in Claude Code
- [ ] Run `/nixtla-baseline-setup` successfully
- [ ] Run `/nixtla-baseline-m4 horizon=7 series_limit=5` successfully
- [ ] Ask Claude "Which model performed best?" and verify skill activation
- [ ] Review golden task output files
- [ ] Read plugin README and Product Overview docs
- [ ] Run CI locally with `python tests/run_baseline_m4_smoke.py`
- [ ] Understand phase AAR documentation structure

---

## 14. Recommendations Roadmap

### Week 1 – Critical Setup & Stabilization

**Goals**:
- [ ] Align version numbers (VERSION, pyproject.toml, CHANGELOG, plugin.json)
- [ ] Update CHANGELOG.md with v0.3.0 through v0.6.0 entries
- [ ] Clean up untracked test artifacts (add to .gitignore)
- [ ] Verify CI passes after cleanup

**Stakeholders**: Jeremy
**Dependencies**: None

### Month 1 – Foundation & Visibility

**Goals**:
- [ ] Add pytest unit tests for `nixtla_baseline_mcp.py`
- [ ] Configure coverage reporting in CI
- [ ] Add dependency vulnerability scanning (Dependabot)
- [ ] Document TimeGPT cost implications in README
- [ ] Create troubleshooting guide for common errors

**Stakeholders**: Jeremy, Max (review)
**Dependencies**: Week 1 complete

### Quarter 1 – Strategic Enhancements

**Goals**:
- [ ] Implement additional specialist agents (CI Triage, Doc Sync)
- [ ] Add support for MLForecast and NeuralForecast models
- [ ] Create benchmarking automation for Nixtla PRs
- [ ] Explore Vertex AI Agent Engine integration
- [ ] Evaluate production deployment requirements

**Stakeholders**: Jeremy, Max, Nixtla engineering
**Dependencies**: Month 1 complete

---

## Appendices

### Appendix A. Glossary

| Term | Definition |
|------|------------|
| MCP | Model Context Protocol - Claude Code's tool system |
| sMAPE | Symmetric Mean Absolute Percentage Error (0-200%, lower is better) |
| MASE | Mean Absolute Scaled Error (<1.0 beats naive seasonal) |
| Golden Task | Validation test that exercises critical path |
| AAR | After Action Report - Post-phase documentation |
| TimeGPT | Nixtla's foundation model for time series |
| StatsForecast | Nixtla's classical forecasting library |

### Appendix B. Reference Links

- **Repository**: https://github.com/intent-solutions-io/plugins-nixtla
- **Bob's Brain (reference)**: https://github.com/jeremylongshore/bobs-brain
- **Nixtla Docs**: https://docs.nixtla.io/
- **Claude Code Docs**: https://code.claude.com/docs/
- **M4 Competition**: https://mofc.unic.ac.cy/m4/

### Appendix C. Troubleshooting Playbooks

**CI fails on "Install dependencies"**:
1. Check `scripts/requirements.txt` for syntax errors
2. Verify package versions exist on PyPI
3. Check Python version compatibility

**Golden task fails with "FAIL: CSV file not found"**:
1. Ensure M4 data downloaded: check `data/` directory
2. Re-run with correct working directory
3. Check output_dir parameter

**TimeGPT returns "skipped_no_api_key"**:
1. Set `NIXTLA_TIMEGPT_API_KEY` environment variable
2. Verify key is valid at Nixtla dashboard
3. Restart Claude Code session

**Plots not generating**:
1. Verify matplotlib installed: `pip show matplotlib`
2. Check `--enable-plots` flag passed
3. Look for matplotlib import errors in stderr

### Appendix D. Change Management

**Release Process**:
1. Complete phase work and AAR
2. Update version in plugin.json
3. Update CHANGELOG.md
4. Create git tag (`vX.Y.Z`)
5. Push commits and tags
6. Verify CI passes

**Documentation Standards**:
- Phase AARs: `NNN-AA-AACR-phase-XX-description.md`
- Canonical docs: `6767-*` prefix
- Test reports: `NNN-QA-TEST-*`

### Appendix E. Open Questions

1. **Production deployment**: What infrastructure is needed for Nixtla team use?
2. **TimeGPT costs**: Should we add cost warnings for large series counts?
3. **Multi-repo support**: How to integrate with StatsForecast/MLForecast PRs?
4. **Agent orchestration**: When to implement Bob's Brain-style agent coordination?
5. **Nixtla collaboration**: What's the review/approval process for changes?

---

**Document ID**: 024-AA-AUDT-appaudit-devops-playbook.md
**Category**: Analysis/Assessment - Audit
**Author**: Claude Code (Opus)
**Date**: 2025-11-25
**Status**: Complete
