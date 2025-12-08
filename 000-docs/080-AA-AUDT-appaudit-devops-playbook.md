# Nixtla Plugin Showcase: Operator-Grade System Analysis & Operations Guide

*For: DevOps Engineer*
*Generated: 2025-12-07*
*System Version: v1.4.1-9-g03d5ff7*

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

This repository is a **business showcase for the Nixtla CEO** demonstrating Claude Code plugins and AI skills for time-series forecasting workflows. The project showcases Intent Solutions' capabilities in building production-style AI integrations, specifically targeting the Nixtla ecosystem (StatsForecast, TimeGPT, MLForecast, NeuralForecast).

The system operates as an **experimental/prototype platform** with 3 working plugins, 8 Claude Skills, and comprehensive documentation. It demonstrates how Claude Code can be extended to provide specialized AI assistance for data scientists working with time-series forecasting.

**Current Operational Status**: The repository is actively maintained with recent commits focused on CI/CD optimization and marketplace compliance. All CI pipelines are passing. No production deployments are live; this is a demo/showcase repository.

**Technology Foundation**: Python 3.9+ with Nixtla's open-source forecasting libraries, Google Cloud Platform (BigQuery, Cloud Functions), Claude Code plugin architecture (MCP servers, skills, slash commands). The choice of Python aligns with Nixtla's native ecosystem, and GCP provides cost-effective serverless options for demonstration purposes.

**Immediate Assessment**:
- **Strengths**: Comprehensive documentation, clean plugin architecture, tiered CI/CD strategy
- **Risks**: Experimental status means no SLA guarantees; GCP credentials required for BigQuery plugin
- **Strategic Value**: Positions Intent Solutions as a Claude Code plugin development partner for Nixtla

### Operational Status Matrix

| Environment | Status | Uptime Target | Current Uptime | Release Cadence | Active Users |
|-------------|--------|---------------|----------------|-----------------|--------------|
| Production  | N/A | N/A | N/A | N/A | N/A |
| Staging     | N/A | N/A | N/A | N/A | N/A |
| Development | Active | N/A | N/A | Per-commit | 1 (demo) |
| GitHub CI   | Active | 99% | ~99% | Per-push | Automated |

### Technology Stack Summary

| Category | Technology | Version | Purpose |
|----------|------------|---------|---------|
| Language | Python | 3.9-3.12 | Core development language |
| Framework | Flask/functions-framework | N/A | Cloud Functions runtime |
| Database | BigQuery | N/A | Time-series data storage (plugin) |
| Cloud Platform | Google Cloud | N/A | Functions, BigQuery, Vertex AI |
| CI/CD | GitHub Actions | N/A | Testing, validation, deployment |
| AI Integration | Claude Code Plugins | N/A | Primary platform |
| Forecasting | Nixtla (statsforecast, nixtla) | 0.5.0+ | Time-series forecasting |

---

## 2. Operator & Customer Journey

### Primary Personas

- **Operators**: DevOps engineers managing the showcase, Intent Solutions team
- **External Customers**: Nixtla CEO/leadership, prospective enterprise clients
- **Reseller Partners**: N/A (prototype stage)
- **Automation Bots**: GitHub Actions CI/CD, Gemini code review

### End-to-End Journey Map

```
Awareness (GitHub/Demo) → Installation (plugin/skills) → Usage (Claude Code) → Feedback → Iteration
```

**Critical Touchpoints**:
1. **Discovery**: README.md, marketplace.json listing
2. **Installation**: `pip install` for skills, `/plugin install` for plugins
3. **First Use**: `/nixtla-baseline-m4` slash command (90-second smoke test)
4. **Value Realization**: Benchmark report generation, BigQuery forecasting
5. **Feedback**: GitHub issues, direct communication

### SLA Commitments

| Metric | Target | Current | Owner |
|--------|--------|---------|-------|
| Uptime | N/A (demo) | N/A | N/A |
| CI Pipeline | <10 min | ~2-5 min | GitHub Actions |
| Smoke Test | <90 sec | ~90 sec | Baseline Lab |
| Documentation | Current | Up-to-date | Jeremy |

---

## 3. System Architecture Overview

### Technology Stack (Detailed)

| Layer | Technology | Version | Source of Truth | Purpose | Owner |
|-------|------------|---------|-----------------|---------|-------|
| Plugin Runtime | Claude Code | Latest | N/A | Plugin execution environment | Anthropic |
| MCP Server | Python/stdio | 1.1.0 | `nixtla_baseline_mcp.py:30` | Tool exposure via MCP | Intent Solutions |
| Backend/API | Cloud Functions | Gen2 | `deploy-bigquery-forecaster.yml` | BigQuery forecasting | Intent Solutions |
| Data Access | BigQuery Client | 3.10.0+ | `requirements.txt` | Time-series data | GCP |
| Forecasting | statsforecast | 1.7.0+ | `requirements.txt` | Baseline models | Nixtla |
| Forecasting | nixtla SDK | 0.5.0+ | `requirements.txt` | TimeGPT access | Nixtla |
| AI Review | Gemini 3 Pro | Preview | `gemini-pr-review.yml` | PR code review | GCP Vertex AI |
| Skills CLI | Python package | 0.4.0 | `pyproject.toml` | Skills installation | Intent Solutions |

### Environment Matrix

| Environment | Purpose | Hosting | Data Source | Release Cadence | IaC Source | Notes |
|-------------|---------|---------|-------------|-----------------|------------|-------|
| local | Development | Developer machine | M4 sample data | N/A | N/A | Virtual env per plugin |
| ci | Validation | GitHub Actions | Mock/synthetic | Per-push | `.github/workflows/` | Tiered: Tier1 fast, Tier2 full |
| demo | Showcase | GCP (manual) | Public BigQuery | On-demand | `deploy-*.yml` | BigQuery forecaster only |

### Cloud & Platform Services

| Service | Purpose | Environment(s) | Key Config | Cost/Limits | Owner | Vendor Risk |
|---------|---------|----------------|------------|-------------|-------|-------------|
| GitHub Actions | CI/CD | All | Free tier | 2000 min/mo | Intent Solutions | Low |
| GCP Cloud Functions | Forecaster API | Demo | Gen2, us-central1 | Pay-per-use | Intent Solutions | Medium |
| GCP BigQuery | Data storage | Demo | Public datasets OK | Pay-per-query | Intent Solutions | Low |
| Vertex AI (Gemini) | PR Review | CI | Gemini 3 Pro Preview | Token-based | Intent Solutions | Low |
| Claude Code | Plugin runtime | User machines | N/A | Free tier | Anthropic | Low |

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CLAUDE CODE RUNTIME                               │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  NIXTLA PLUGINS (3 working)                                          │  │
│  │                                                                       │  │
│  │  ┌──────────────────────┐  ┌──────────────────────┐                  │  │
│  │  │ nixtla-baseline-lab  │  │ nixtla-bigquery-     │                  │  │
│  │  │ ├── MCP Server      │  │ forecaster           │                  │  │
│  │  │ │   (stdio/python)   │  │ ├── Cloud Function  │                  │  │
│  │  │ ├── Commands (/m4)   │  │ └── BigQuery Client │                  │  │
│  │  │ ├── Agents           │  └──────────────────────┘                  │  │
│  │  │ └── Skills           │  ┌──────────────────────┐                  │  │
│  │  └──────────────────────┘  │ nixtla-search-to-    │                  │  │
│  │                             │ slack (MVP)          │                  │  │
│  │  ┌────────────────────────┐└──────────────────────┘                  │  │
│  │  │ SKILLS PACK (8 skills) │                                          │  │
│  │  │ timegpt-lab, experiment-architect, schema-mapper...              │  │
│  │  └────────────────────────┘                                          │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    ▼                 ▼                 ▼
            ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
            │   M4 Data    │  │   BigQuery   │  │  Slack API   │
            │  (bundled)   │  │  (external)  │  │  (external)  │
            └──────────────┘  └──────────────┘  └──────────────┘
```

---

## 4. Directory Deep-Dive

### Project Structure Analysis

```
nixtla/
├── .claude/                    # Claude Code project skills
│   └── skills/                 # Skills local to this repo
├── .claude-plugin/             # Root marketplace config
│   └── marketplace.json        # Plugin registry (3 plugins)
├── .github/
│   └── workflows/              # CI/CD pipelines (7 workflows)
├── 000-docs/                   # Documentation hub (Doc-Filing v3.0)
│   ├── global/                 # Cross-cutting guides
│   └── planned-plugins/        # Per-plugin documentation sets
├── plugins/                    # Working plugins (3)
│   ├── nixtla-baseline-lab/    # Benchmarking plugin
│   ├── nixtla-bigquery-forecaster/  # Cloud Functions plugin
│   └── nixtla-search-to-slack/ # Content curation (MVP)
├── skills-pack/                # Distributable skills
│   └── .claude/skills/         # 8 skill definitions
├── packages/                   # Python packages
│   └── nixtla-claude-skills-installer/  # CLI tool (v0.4.0)
├── tests/                      # Root-level tests
├── CLAUDE.md                   # Claude Code instructions
├── README.md                   # Repository overview
├── CHANGELOG.md                # Version history
├── VERSION                     # Current version (1.4.1)
├── pyproject.toml              # Python package config
├── requirements.txt            # Core dependencies
└── requirements-dev.txt        # Development dependencies
```

### Detailed Directory Analysis

#### plugins/nixtla-baseline-lab/

**Purpose**: Primary working plugin for running statsforecast baseline models on M4 benchmark data

**Key Files**:
- `scripts/nixtla_baseline_mcp.py:26` - MCP server class (NixtlaBaselineMCP)
- `tests/run_baseline_m4_smoke.py` - Golden task smoke test (90 seconds)
- `.claude-plugin/plugin.json` - Plugin metadata (v1.4.1)
- `.mcp.json` - MCP server configuration

**Patterns**:
- MCP server pattern: Python class exposing 4 tools via JSON-RPC over stdio
- Golden task pattern: Pre-defined smoke tests for validation

**Entry Points**:
- MCP Server: `python scripts/nixtla_baseline_mcp.py`
- Slash Command: `/nixtla-baseline-m4`

**Data Layer**:
- M4 Daily benchmark data (bundled in `data/`)
- Custom CSV support for user data
- Output: CSV files + markdown reports

#### plugins/nixtla-bigquery-forecaster/

**Purpose**: Cloud Function that forecasts BigQuery time-series data

**Key Files**:
- `src/main.py:23` - Cloud Function entry point (`forecast_handler`)
- `src/bigquery_connector.py` - BigQuery client wrapper
- `src/forecaster.py` - Nixtla model orchestration

**Patterns**:
- Cloud Function pattern: HTTP trigger, JSON request/response
- ETL pattern: Read from BigQuery → Forecast → Write back

**Deployment**:
- Workflow: `.github/workflows/deploy-bigquery-forecaster.yml`
- Region: us-central1
- Memory: 2Gi, Timeout: 540s

**Authentication**:
- Workload Identity Federation (keyless GCP auth)
- Required secrets: `GCP_WORKLOAD_IDENTITY_PROVIDER`, `GCP_SA_EMAIL`, `GCP_PROJECT_ID`

#### packages/nixtla-claude-skills-installer/

**Purpose**: CLI tool for installing Nixtla skills into projects

**Key Files**:
- `nixtla_skills_installer/cli.py` - CLI entry point (`nixtla-skills` command)
- `nixtla_skills_installer/core.py` - Installation logic

**Commands**:
- `nixtla-skills init` - Install all 8 skills
- `nixtla-skills update` - Update to latest versions

**Python Version**: 3.8+ (widest compatibility)

#### tests/

**Framework**: pytest 7.4.0+

**Test Files**:
- `test_skills_installer_e2e.py` - End-to-end skills installation test
- `basic_validator.py` - Skills compliance checker
- `test_placeholder.py` - Placeholder for root tests

**Coverage**: Not enforced (fail-under disabled in CI)

**Gaps**: Limited unit tests; focus is on E2E validation

---

## 5. Automation & Agent Surfaces

### CI/CD Workflows (7 total)

| Workflow | Purpose | Trigger | Cost Tier | Approx Runtime |
|----------|---------|---------|-----------|----------------|
| `ci.yml` | Main validation pipeline | push/PR | Tier1: ~2min, Tier2: ~15min | Varies |
| `nixtla-baseline-lab-ci.yml` | Baseline lab specific tests | push to plugin | Low | ~3min |
| `skills-installer-ci.yml` | Skills installer tests | push to package | Low | ~2min |
| `deploy-bigquery-forecaster.yml` | GCP Cloud Function deploy | push to main | Medium | ~5min |
| `gemini-pr-review.yml` | AI code review | PR opened/sync | Low | ~2min |
| `gemini-daily-audit.yml` | Weekly code audit | Sunday 6am CST | Low | ~5min |
| `plugin-validator.yml` | Marketplace compliance | push | Low | ~2min |

### MCP Servers

| Server | Plugin | Tools Exposed | Transport | Timeout |
|--------|--------|---------------|-----------|---------|
| `nixtla-baseline-mcp` | baseline-lab | 4 tools | stdio | 300s |

**Tools**:
1. `run_baselines` - Run forecasting models
2. `get_nixtla_compatibility_info` - Library versions
3. `generate_benchmark_report` - Markdown report
4. `generate_github_issue_draft` - Issue template

### Claude Skills (8)

| Skill | Purpose | Location |
|-------|---------|----------|
| `nixtla-timegpt-lab` | TimeGPT API experimentation | `skills-pack/.claude/skills/` |
| `nixtla-experiment-architect` | Experiment design | `skills-pack/.claude/skills/` |
| `nixtla-schema-mapper` | Data schema transformation | `skills-pack/.claude/skills/` |
| `nixtla-timegpt-finetune-lab` | Model fine-tuning | `skills-pack/.claude/skills/` |
| `nixtla-prod-pipeline-generator` | Production pipeline code | `skills-pack/.claude/skills/` |
| `nixtla-usage-optimizer` | API usage optimization | `skills-pack/.claude/skills/` |
| `nixtla-skills-bootstrap` | Skills installation helper | `skills-pack/.claude/skills/` |
| `nixtla-skills-index` | Skills discovery | `skills-pack/.claude/skills/` |

### Gemini AI Integration

**PR Review** (`gemini-pr-review.yml`):
- Triggered on PR open/sync
- Uses Gemini 3 Pro Preview via Vertex AI
- Checks: security, Python quality, Nixtla patterns
- Outputs: APPROVE or CHANGES_REQUESTED with explanation

**Weekly Audit** (`gemini-daily-audit.yml`):
- Scheduled: Sundays 12:00 UTC (6am CST)
- Reviews last 24 hours of commits
- Creates GitHub issues for findings

---

## 6. Operational Reference

### Deployment Workflows

#### Local Development

**Prerequisites**:
- Python 3.10+ (3.12 recommended)
- Git
- Claude Code CLI (for testing plugins)
- virtualenv or venv

**Environment Setup**:
```bash
# Clone repository
git clone https://github.com/intent-solutions-io/plugins-nixtla.git
cd plugins-nixtla

# Install dev dependencies
pip install -r requirements-dev.txt

# For baseline-lab plugin
cd plugins/nixtla-baseline-lab
./scripts/setup_nixtla_env.sh --venv
source .venv-nixtla-baseline/bin/activate
pip install -r scripts/requirements.txt
```

**Verification**:
```bash
# Run root tests
pytest -v

# Run baseline lab smoke test
python plugins/nixtla-baseline-lab/tests/run_baseline_m4_smoke.py
```

#### CI Pipeline Deployment (Automated)

**Tier 1 (Every Push)**:
- Runs: `lint-and-format`, `test-primary`, `validate-plugins`
- Duration: ~2 minutes
- Runner: ubuntu-latest only

**Tier 2 (PRs to main)**:
- Runs: Full OS matrix (Linux/Windows/macOS)
- Python versions: 3.9, 3.10, 3.11, 3.12
- Duration: ~15-20 minutes

**BigQuery Forecaster Deployment**:
```bash
# Automatic on push to main affecting plugin
# Manual: gh workflow run deploy-bigquery-forecaster.yml
```

### Monitoring & Alerting

**Dashboards**: None (prototype status)

**Logging**:
- CI logs: GitHub Actions tab
- Cloud Function logs: `firebase functions:log` / GCP Console

**Alerts**: None configured

### Incident Response

Not applicable for prototype. For demo failures:
1. Check GitHub Actions for pipeline failures
2. Review Gemini audit issues
3. Contact Jeremy (jeremy@intentsolutions.io)

### Backup & Recovery

**Backups**: Git repository only
**Recovery**: Clone from GitHub, re-run setup scripts

---

## 7. Security, Compliance & Access

### Identity & Access Management

| Account/Role | Purpose | Permissions | Provisioning | MFA | Used By |
|--------------|---------|-------------|--------------|-----|---------|
| `nixtla-github-deployer` | GCP Service Account | Cloud Functions deploy, BigQuery access | WIF | N/A | GitHub Actions |
| GitHub PAT | Repo access | push/PR | Manual | Yes | Jeremy |

### Secrets Management

**Location**: GitHub Actions Secrets

| Secret | Purpose | Rotation | Used In |
|--------|---------|----------|---------|
| `GCP_WORKLOAD_IDENTITY_PROVIDER` | WIF configuration | N/A | deploy-bigquery-forecaster.yml |
| `GCP_SA_EMAIL` | Service account email | N/A | deploy-bigquery-forecaster.yml |
| `GCP_PROJECT_ID` | GCP project | N/A | deploy-bigquery-forecaster.yml |
| `NIXTLA_TIMEGPT_API_KEY` | TimeGPT API access | As needed | Cloud Function env |

### Security Posture

**Authentication**:
- WIF for GCP (keyless, secure)
- No long-lived service account keys

**Authorization**:
- Least privilege for service accounts
- Public read for public BigQuery datasets

**Encryption**:
- HTTPS enforced for all API calls
- GCP at-rest encryption by default

**Scanning**:
- Trivy security scanner (CI)
- Secrets detection in CI (excludes archive/, .md files)
- Gemini code review checks for hardcoded secrets

**Known Issues**: None

**Security Contact**: security@intentsolutions.io

---

## 8. Cost & Performance

### Current Costs

**Monthly Cloud Spend**: ~$0-10 (prototype, minimal usage)

- GitHub Actions: Free tier (2000 min/mo)
- GCP Cloud Functions: Pay-per-invocation (~$0 for demo)
- BigQuery: Public datasets free, minimal query costs
- Vertex AI (Gemini): Token-based, ~$0-5/mo for PR reviews

### Performance Baseline

**CI Pipeline**:
- Tier 1: ~2 minutes (Linux, Python 3.11)
- Tier 2: ~15-20 minutes (full matrix)

**Baseline Lab Smoke Test**:
- Target: 90 seconds
- Actual: ~90 seconds (offline, no API calls)

**BigQuery Forecaster**:
- Cold start: ~5-10 seconds
- Forecast execution: Depends on data size

### Cost Optimization (Implemented)

Per CTO directive (December 2025):
- macOS = 10x multiplier → Restricted to Tier 2 only
- Windows = 2x multiplier → Restricted to Tier 2 only
- Gemini audit: Changed from daily to weekly (saves ~30 min/week)

---

## 9. Development Workflow

### Local Development

**Standard Environment**:
- OS: Linux, macOS, or Windows
- Python: 3.10+ recommended
- Tools: pytest, black, isort, flake8

**Bootstrap**:
```bash
pip install -r requirements-dev.txt
# For plugins, use plugin-specific setup scripts
```

### CI/CD Pipeline

**Platform**: GitHub Actions

**Stages**:
1. `lint-and-format` - black, isort, flake8
2. `test-primary` - pytest with coverage
3. `validate-plugins` - plugin.json validation
4. `security-scan` - Trivy, secrets detection
5. `all-checks-passed` - Gate for merge

### Code Quality

**Linting**:
- `black --check .` - Formatting
- `isort --check-only .` - Import ordering
- `flake8 . --select=E9,F63,F7,F82` - Critical errors only

**Auto-fix**:
```bash
black .
isort .
```

**Commit Convention**: Conventional commits
- Format: `<type>(<scope>): <subject>`
- Types: feat, fix, docs, style, refactor, test, chore, perf

---

## 10. Dependencies & Supply Chain

### Core Dependencies

| Package | Version | Purpose | Security Notes |
|---------|---------|---------|----------------|
| nixtla | >=0.5.0 | TimeGPT client | Maintained by Nixtla |
| statsforecast | >=1.7.0 | Open-source forecasting | Maintained by Nixtla |
| pandas | >=2.0.0 | Data manipulation | High-trust, well-maintained |
| numpy | >=1.24.0 | Numerical computing | High-trust, well-maintained |
| pydantic | >=2.0.0 | Data validation | High-trust |
| google-cloud-bigquery | >=3.10.0 | BigQuery access | Google-maintained |

### Development Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pytest | >=7.4.0 | Testing framework |
| pytest-cov | >=4.1.0 | Coverage reporting |
| black | >=23.0.0 | Code formatter |
| flake8 | >=6.0.0 | Linter |
| isort | >=5.12.0 | Import sorter |
| mypy | >=1.4.0 | Type checking |

### Third-Party Services

| Service | Purpose | Data Shared | Auth | SLA | Renewal | Owner |
|---------|---------|-------------|------|-----|---------|-------|
| Nixtla API | TimeGPT forecasting | Time-series data | API key | Commercial | N/A | Nixtla |
| BigQuery | Data storage | Query data | GCP IAM | 99.99% | N/A | GCP |
| Slack | Notifications (search-to-slack) | Messages | OAuth | 99.99% | N/A | Slack |
| Vertex AI | Code review | Code diffs | WIF | 99.9% | N/A | GCP |

---

## 11. Integration with Existing Documentation

### Documentation Inventory

| Document | Status | Last Updated | Purpose |
|----------|--------|--------------|---------|
| `README.md` | Current | Dec 2025 | Repository overview |
| `CLAUDE.md` | Current | Dec 2025 | Claude Code instructions |
| `CHANGELOG.md` | Current | Dec 2025 | Version history |
| `SECURITY.md` | Current | Nov 2025 | Security policy |
| `CONTRIBUTING.md` | Current | Nov 2025 | Contribution guidelines |
| `000-docs/global/003-GUIDE-devops-nixtla-skills-operations.md` | Current | Nov 2025 | DevOps operations guide |
| `000-docs/078-SPEC-MASTER-claude-code-plugins-standard.md` | Current | Dec 2025 | Plugin specification |

### Documentation Standards

**Doc-Filing v3.0**:
- Pattern: `NNN-CC-ABCD-description.md`
- Category Codes: PP (Planning), AT (Architecture), AA (Audits), OD (Overview), QA (Quality)

**Per-Plugin Documentation**:
Each plugin requires 6 docs in `000-docs/planned-plugins/{plugin}/`:
- 01-BUSINESS-CASE.md
- 02-PRD.md
- 03-ARCHITECTURE.md
- 04-USER-JOURNEY.md
- 05-TECHNICAL-SPEC.md
- 06-STATUS.md

### Discrepancies

None identified. Documentation is well-maintained and consistent with code.

### Recommended Reading Order

1. `README.md` - 5 minutes - Repository overview
2. `CLAUDE.md` - 10 minutes - How Claude Code interacts with repo
3. `000-docs/global/003-GUIDE-devops-nixtla-skills-operations.md` - 20 minutes - Skills lifecycle
4. `000-docs/078-SPEC-MASTER-claude-code-plugins-standard.md` - 30 minutes - Plugin architecture
5. Plugin-specific READMEs - 15 minutes each

---

## 12. Current State Assessment

### What's Working Well

| Item | Evidence |
|------|----------|
| CI/CD Pipeline | All workflows passing, tiered cost optimization |
| Plugin Structure | 100% marketplace compliance (3/3 plugins) |
| Documentation | Comprehensive, follows Doc-Filing v3.0 |
| Security | WIF authentication, secret scanning, Gemini review |
| Code Quality | black/isort/flake8 enforced, consistent formatting |
| Skills Architecture | 8 skills with proper frontmatter, installer CLI |
| MCP Server | 4 tools exposed, 300s timeout, robust error handling |

### Areas Needing Attention

| Item | Priority | Issue |
|------|----------|-------|
| Test Coverage | Medium | No coverage thresholds enforced |
| Production Deployment | Low | BigQuery forecaster is demo-only |
| Monitoring | Low | No dashboards or alerting (acceptable for prototype) |
| Skills Installer | Medium | Not yet published to PyPI |

### Immediate Priorities

1. **[Low]** – Test coverage thresholds • Impact: Code quality • Action: Enable pytest-cov fail-under • Owner: Jeremy
2. **[Low]** – PyPI publication • Impact: Easier installation • Action: Publish nixtla-claude-skills-installer • Owner: Jeremy
3. **[Info]** – Weekly Gemini audit • Impact: Proactive issue detection • Action: Review issues created • Owner: DevOps

---

## 13. Quick Reference

### Operational Command Map

| Capability | Command/Tool | Source | Notes |
|------------|--------------|--------|-------|
| Local env setup | `pip install -r requirements-dev.txt` | Root | All tests |
| Plugin env | `./scripts/setup_nixtla_env.sh --venv` | baseline-lab | Per-plugin |
| Run all tests | `pytest -v` | Root | Uses pytest.ini_options |
| Run single test | `pytest tests/test_file.py::test_name -v` | Root | Standard pytest |
| Smoke test | `python plugins/nixtla-baseline-lab/tests/run_baseline_m4_smoke.py` | baseline-lab | 90 seconds |
| Format code | `black . && isort .` | Root | Auto-fix |
| Lint check | `flake8 . --select=E9,F63,F7,F82` | Root | CI-matching |
| Install skills | `nixtla-skills init` | CLI | Requires pip install |
| View CI logs | GitHub Actions tab | Browser | Per-workflow |

### Critical Endpoints & Resources

- **Repository**: https://github.com/intent-solutions-io/plugins-nixtla
- **Marketplace Config**: `.claude-plugin/marketplace.json`
- **Plugin Manifest**: `plugins/{name}/.claude-plugin/plugin.json`
- **Skills Location**: `skills-pack/.claude/skills/{skill-name}/SKILL.md`
- **CI Workflows**: `.github/workflows/`
- **Documentation Hub**: `000-docs/`

### First-Week Checklist

- [ ] Clone repository and run `pip install -r requirements-dev.txt`
- [ ] Run `pytest -v` to verify test environment
- [ ] Run baseline-lab smoke test (90 seconds)
- [ ] Read CLAUDE.md and README.md
- [ ] Review `000-docs/global/003-GUIDE-devops-nixtla-skills-operations.md`
- [ ] Understand plugin structure via `000-docs/078-SPEC-MASTER-claude-code-plugins-standard.md`
- [ ] Check GitHub Actions for recent CI runs
- [ ] Review Gemini audit issues (if any)

---

## 14. Recommendations Roadmap

### Week 1 – Familiarization

**Goals**:
- Complete first-week checklist
- Understand plugin/skill architecture
- Run all smoke tests successfully

**Stakeholders**: DevOps engineer, Jeremy

**Dependencies**: Access to repository

### Month 1 – Operational Stability

**Goals**:
- Set up local development environment for all plugins
- Understand CI/CD tiering strategy
- Document any gaps found in operational guides

**Stakeholders**: DevOps engineer, Jeremy

**Dependencies**: None

### Quarter 1 – Enhancement & Automation

**Goals**:
- Evaluate test coverage improvements
- Consider skills installer PyPI publication
- Monitor Gemini audit for recurring issues

**Stakeholders**: DevOps engineer, Jeremy, Nixtla (feedback)

**Dependencies**: Nixtla engagement progress

---

## Appendices

### Appendix A. Glossary

| Term | Definition |
|------|------------|
| MCP | Model Context Protocol - standard for tool integration with Claude |
| StatsForecast | Nixtla's open-source statistical forecasting library |
| TimeGPT | Nixtla's commercial foundation model for time-series |
| WIF | Workload Identity Federation - keyless GCP authentication |
| M4 | Makridakis 4 - standard forecasting benchmark dataset |
| SMAPE/MASE | Symmetric Mean Absolute Percentage Error / Mean Absolute Scaled Error |

### Appendix B. Reference Links

| Resource | URL |
|----------|-----|
| Nixtla Documentation | https://docs.nixtla.io |
| Claude Code Plugins | https://code.claude.com/docs/en/plugins-reference |
| StatsForecast | https://github.com/Nixtla/statsforecast |
| Repository | https://github.com/intent-solutions-io/plugins-nixtla |

### Appendix C. Troubleshooting Playbooks

**Problem**: `ModuleNotFoundError: statsforecast`
**Solution**: Run `pip install -r scripts/requirements.txt` in plugin directory

**Problem**: Plugin not found after install
**Solution**: Restart Claude Code

**Problem**: Permission denied on setup script
**Solution**: Run `chmod +x scripts/setup_nixtla_env.sh`

**Problem**: CI fails on formatting
**Solution**: Run `black . && isort .` and commit

### Appendix D. Change Management

**Release Process**:
1. Update `VERSION` file
2. Update `CHANGELOG.md`
3. Create release AAR in `000-docs/`
4. Tag: `git tag -a v1.X.Y -m "Release v1.X.Y"`

**Branch Strategy**:
- `main` - Production-ready
- `develop` - Integration
- `feature/*` - Features
- `fix/*` - Bug fixes

### Appendix E. Open Questions

1. Timeline for Nixtla CEO demo?
2. Should BigQuery forecaster be promoted to production?
3. PyPI publication timeline for skills installer?

---

*Document Generated: 2025-12-07*
*System Version: v1.4.1-9-g03d5ff7*
*Next Review: Q1 2026 or on major release*
