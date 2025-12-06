# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

**Business Showcase Repository for Nixtla CEO (Max Mergenthaler)**

This repository demonstrates how Claude Code plugins deliver measurable business value to Nixtla through:
1. **Internal efficiency** - Make Nixtla's team 2-3x more productive
2. **Business growth** - Expand market reach to Airflow, dbt, and Snowflake customers

**Current Version**: 1.3.0 (Prediction Markets Vertical Launch)
**Status**: 3 working plugins + 8 production-ready Claude Skills (95%+ compliant) + 9 plugin specifications

**Key Documents**:
- `README.md` - Business pitch for Max (start here)
- `000-docs/035-PP-PROD-nixtla-plugin-business-case.md` - Detailed ROI analysis
- `CHANGELOG.md` - Complete version history and release notes

## Quick Commands

### Skills Pack (Recommended Entry Point)

```bash
# Install skills in your project
pip install -e packages/nixtla-claude-skills-installer
cd /path/to/your/forecasting-project
nixtla-skills init

# Update skills to latest
nixtla-skills update
```

### Plugin Development

```bash
# Try the baseline lab plugin
cd plugins/nixtla-baseline-lab
./scripts/setup_nixtla_env.sh --venv
source .venv-nixtla-baseline/bin/activate
pip install -r scripts/requirements.txt

# Run golden task harness (90 seconds, fully offline)
cd tests
python run_baseline_m4_smoke.py

# In Claude Code, run the slash command:
/nixtla-baseline-m4 demo_preset=m4_daily_small
```

### Testing & Validation

```bash
# Run skills installer E2E test
python tests/test_skills_installer_e2e.py

# Run baseline lab smoke test
python plugins/nixtla-baseline-lab/tests/run_baseline_m4_smoke.py

# Validate skills compliance
python tests/basic_validator.py
```

### Documentation Management

```bash
# Browse plugin documentation
ls -la 000-docs/plugins/*/         # Per-plugin docs (6 files each)

# Read executive materials
cat 000-docs/global/000-EXECUTIVE-SUMMARY.md
cat 000-docs/global/001-ENGAGEMENT-OPTIONS.md

# Check skills compliance
cat 000-docs/085-QA-AUDT-claude-skills-compliance-audit.md
```

## Architecture

### Working Plugins (3 Total)

#### 1. Nixtla Baseline Lab (v0.8.0) - Production-Ready
- **Location**: `plugins/nixtla-baseline-lab/`
- **Purpose**: Run statsforecast baselines on M4 benchmark data, generate reproducibility bundles
- **Business Impact**: Faster customer issue debugging, easier issue reporting
- **Status**: Production-ready with CI/CD, comprehensive tests, full documentation
- **Git**: Multiple commits from v0.1.0 → v0.8.0 over 8 development phases

**Key Components**:
```
plugins/nixtla-baseline-lab/
├── scripts/
│   └── mcp_server.py           # MCP server exposing baseline forecasting
├── commands/
│   └── nixtla-baseline-m4.md   # Slash command definition
├── skills/
│   └── nixtla-baseline-review/ # AI skill for metric interpretation
└── tests/
    └── run_baseline_m4_smoke.py # Golden task validation
```

#### 2. Nixtla BigQuery Forecaster - Working Demo
- **Location**: `plugins/nixtla-bigquery-forecaster/`
- **Purpose**: Run Nixtla statsforecast on BigQuery data via serverless Cloud Functions
- **Business Impact**: Demonstrates Google Cloud + Nixtla integration, tested with 200M+ row datasets
- **Status**: Working demo with deployment automation
- **Git**: `4d4f679` - feat: Nixtla BigQuery Forecaster

**Key Components**:
```
plugins/nixtla-bigquery-forecaster/
├── src/
│   ├── main.py                  # Cloud Function entry point
│   ├── forecaster.py            # Nixtla statsforecast wrapper
│   └── bigquery_connector.py    # BigQuery data reader/writer
├── test_local.py                # Local testing script
└── requirements.txt             # statsforecast, google-cloud-bigquery
```

#### 3. Nixtla Search-to-Slack (v0.1.0) - MVP
- **Location**: `plugins/nixtla-search-to-slack/`
- **Purpose**: Automated content discovery & curation (Search → AI Summary → Slack)
- **Business Impact**: Demonstrates content automation for time-series/forecasting topics
- **Status**: MVP / Construction kit with comprehensive tests
- **Git**: `0c27c23` - feat: add FREE web search providers

**Key Components**:
```
plugins/nixtla-search-to-slack/
├── src/nixtla_search_to_slack/  # Core search & curation logic
├── tests/                       # 6 comprehensive test files
├── skills/                      # Agent skills for content analysis
├── SETUP_GUIDE.md              # 24KB comprehensive setup guide
└── requirements.txt             # serpapi, slack-sdk, openai/anthropic
```

### Plugin Specifications (Ready to Build)

**9 Complete Specifications** (`000-docs/009-017-*.md`):

**Internal Efficiency (33%)**:
1. Cost Optimizer - 30-50% API cost reduction
2. Migration Assistant - Onboarding: weeks → hours
3. Forecast Explainer - 40% fewer support tickets

**Business Growth (67%)**:
4. VS StatsForecast Benchmark - Increase TimeGPT adoption
5. ROI Calculator - Shorten sales cycles 2-3 months
6. Airflow Operator - Enterprise data platform teams
7. dbt Package - Analytics engineering market
8. Snowflake Adapter - Fortune 500 contracts
9. Anomaly Streaming Monitor - Real-time monitoring market

## Repository Structure

```
nixtla/
├── skills-pack/                         # ✅ Claude Skills Pack (8 skills, 95%+ compliant)
│   └── .claude/skills/
│       ├── nixtla-timegpt-lab/          # Mode skill (transforms Claude behavior)
│       ├── nixtla-experiment-architect/ # Scaffold forecasting experiments
│       ├── nixtla-schema-mapper/        # Data schema mapping
│       ├── nixtla-timegpt-finetune-lab/ # Fine-tuning guide
│       ├── nixtla-prod-pipeline-generator/ # Production pipelines
│       ├── nixtla-usage-optimizer/      # Cost optimization
│       ├── nixtla-skills-bootstrap/     # CLI installer skill
│       └── nixtla-skills-index/         # Skill discovery
│
├── packages/                            # Distributable packages
│   └── nixtla-claude-skills-installer/  # CLI: nixtla-skills init/update
│       ├── nixtla_skills_installer/
│       └── pyproject.toml
│
├── plugins/                             # Working plugin code
│   ├── nixtla-baseline-lab/             # ✅ Benchmarking plugin (v1.1.0)
│   │   ├── scripts/                     # MCP server, benchmarking
│   │   ├── commands/                    # /nixtla-baseline-m4 slash command
│   │   ├── skills/                      # AI skill for result interpretation
│   │   └── tests/                       # Golden task harness
│   ├── nixtla-bigquery-forecaster/      # ✅ BigQuery + Cloud Functions demo
│   └── nixtla-search-to-slack/          # ✅ Content automation MVP
│
├── 000-docs/                            # 80+ technical documents
│   ├── global/                          # Executive decision materials
│   │   ├── 000-EXECUTIVE-SUMMARY.md     # For Max (Nixtla CEO)
│   │   ├── 001-ENGAGEMENT-OPTIONS.md    # Pricing/timelines
│   │   └── 002-DECISION-MATRIX.md       # Plugin prioritization
│   ├── planned-plugins/                 # 11 plugin specs (6 docs each)
│   │   ├── nixtla-baseline-lab/         # Complete documentation (working)
│   │   ├── nixtla-cost-optimizer/       # Specification (planned)
│   │   ├── nixtla-defi-sentinel/        # Exploration (prediction markets)
│   │   └── [8 more plugins]/
│   ├── planned-skills/                  # Future skill specifications
│   ├── 040-047-AA-REPT-*.md             # After-Action Reports (Skills phases)
│   ├── 041-SPEC-nixtla-skill-standard.md # Skill compliance standard
│   ├── 048-050-AA-AUDIT-*.md            # Compliance audits
│   └── 081-095-AA-*.md                  # Individual skill audits/postmortems
│
├── demo-project/                        # End-to-end demo walkthrough
│   ├── data/m4_daily_sample.csv
│   └── forecasting/
│
├── tests/                               # Repository-level tests
│   ├── test_skills_installer_e2e.py     # Skills installer E2E
│   └── basic_validator.py               # Skills compliance validator
│
├── .github/workflows/
│   ├── skills-installer-ci.yml          # Skills installer CI
│   └── ci.yml                           # Main CI pipeline
│
├── CHANGELOG.md                         # Release history (v0.1.0 → v1.2.0)
├── VERSION                              # Current: 1.2.0
└── README.md                            # Business showcase (for Max)
```

## Document Filing System v3.0

All documentation follows: `NNN-CC-ABCD-description.md`

**Category Codes**:
- **PP** - Planning & Product requirements
- **AT** - Architecture & Technical design
- **AA** - Audits & After-Action Reports
- **OD** - Overview & Documentation
- **QA** - Quality Assurance & Testing

**Key Documents**:
- `035-PP-PROD-nixtla-plugin-business-case.md` - ROI analysis for Max
- `009-017-AT-ARCH-plugin-*.md` - 9 plugin specifications
- `6767-OD-OVRV-nixtla-baseline-lab-overview.md` - Product overview
- `034-OD-RELS-v0-8-0-doc-filing-compliance.md` - Latest release AAR

## Testing & CI/CD

### Running Tests

```bash
# Skills installer E2E test (validates all 8 skills install correctly)
python tests/test_skills_installer_e2e.py

# Baseline lab smoke test (90 seconds, fully offline, no API costs)
cd plugins/nixtla-baseline-lab
python tests/run_baseline_m4_smoke.py

# Skills compliance validator
python tests/basic_validator.py

# BigQuery forecaster local test
cd plugins/nixtla-bigquery-forecaster
source .venv/bin/activate
python test_local.py

# Search-to-Slack tests (requires API keys in .env)
cd plugins/nixtla-search-to-slack
pytest tests/
```

### CI/CD Workflows

All workflows are in `.github/workflows/`:
- `skills-installer-ci.yml` - Tests skills installer on every push/PR
- `nixtla-baseline-lab-ci.yml` - Tests baseline lab plugin
- `deploy-bigquery-forecaster.yml` - Deploys BigQuery forecaster to GCP
- `ci.yml` - Main validation pipeline
- `plugin-validator.yml` - Validates plugin structure

## Claude Skills Architecture

### Progressive Disclosure Design

Skills follow a 3-level token budget hierarchy:

**Level 1: Metadata** (~100 tokens)
- YAML frontmatter in `SKILL.md`
- Loaded by Claude for skill discovery
- Critical: `description` field drives skill selection via LLM reasoning

**Level 2: Core Prompt** (~2,500 tokens average)
- Main `SKILL.md` body (Purpose, Overview, Instructions, Output)
- Target: <500 lines per skill (avg: 375 lines in v1.2.0)
- Loaded when skill activates

**Level 3: Reference Materials** (loaded on-demand)
- Files in `resources/` directory
- Examples: API docs, code templates, troubleshooting guides
- Referenced by SKILL.md but not loaded upfront

### Skill Standard Compliance

All Nixtla skills MUST comply with `041-SPEC-nixtla-skill-standard.md`:

**Required frontmatter fields**:
- `name: nixtla-<short-name>` (matches folder name)
- `description: >` (action-oriented with when-to-use context)
- `version: X.Y.Z` (semantic versioning)
- `allowed-tools: "Read,Write,Glob,Grep,Edit"` (minimal set)

**Forbidden fields** (not in Anthropic 6767 standard):
- ❌ `author`, `priority`, `audience`, `when_to_use`, `license`

**Quality targets** (v1.2.0 achievements):
- Description quality: 80%+ (all 8 skills achieved)
- Skill size: <500 lines (avg: 375, best: 216)
- Compliance: 95%+ with Anthropic Agent Skills standard

### Skills vs Plugins vs Slash Commands

**Claude Skills** (`skills-pack/.claude/skills/nixtla-*/`)
- AI agent prompts that transform Claude's behavior
- Auto-activate when Claude detects relevant context
- Install per-project: `nixtla-skills init`
- Example: `nixtla-timegpt-lab` (mode skill)

**Plugins** (`plugins/*/`)
- Complete applications with MCP servers, tests, docs
- Include slash commands, skills, Python backends
- Example: `nixtla-baseline-lab` (benchmarking plugin)

**Slash Commands** (`plugins/*/commands/*.md`)
- User-invoked commands like `/nixtla-baseline-m4`
- Execute specific plugin workflows
- Defined in markdown files processed by Claude Code

### Installing Skills in Your Project

```bash
# One-time setup
pip install -e packages/nixtla-claude-skills-installer

# In your forecasting project
cd /path/to/your/project
nixtla-skills init  # Installs all 8 skills to .claude/skills/

# Skills activate automatically when Claude detects:
# - Forecasting discussions
# - Time series analysis
# - Nixtla API usage
# - Data schema mapping needs
```

## Nixtla Integration Patterns

```python
# StatsForecast (currently implemented in plugins)
from statsforecast import StatsForecast
from statsforecast.models import AutoETS, AutoTheta, SeasonalNaive
sf = StatsForecast(models=[AutoETS(), AutoTheta()], freq='D')
sf.fit(df)
forecasts = sf.predict(h=14)

# TimeGPT (opt-in, requires API key)
from nixtla import NixtlaClient
client = NixtlaClient(api_key='NIXTLA_TIMEGPT_API_KEY')
forecast = client.forecast(df=data, h=24, freq='H')

# MLForecast (future plugin)
from mlforecast import MLForecast
from sklearn.ensemble import RandomForestRegressor
mlf = MLForecast(models=[RandomForestRegressor()], freq='D', lags=[1,7])
mlf.fit(df)
predictions = mlf.predict(h=30)
```

## Critical Messaging

**This is a business development tool**, not a technical sandbox. Maintain this framing:

**What This Is**:
- Business showcase for Nixtla CEO
- Proof of execution (1 working plugin + 9 specs)
- ROI-focused plugin roadmap
- Market expansion strategy

**What This Is NOT**:
- Not a production SLA (experimental prototype)
- Not official Nixtla product (community integration)
- Not over-promising ("guaranteed ROI", "enterprise-ready")

**Language to Use**:
- ✅ "experimental", "prototype", "showcase", "demonstrates value"
- ✅ "10x-100x ROI potential", "2-3x team productivity"
- ✅ "market expansion", "business growth", "internal efficiency"

**Language to Avoid**:
- ❌ "production-ready", "enterprise-grade", "guaranteed"
- ❌ Any implication this is official Nixtla product
- ❌ SLAs, support commitments, performance guarantees

## Development Workflows

### Adding a New Plugin

```bash
# Use the plugin scaffold script
./scripts/new-plugin.sh <slug> "<Name>" <category>

# Example:
./scripts/new-plugin.sh cost-optimizer "Cost Optimizer" efficiency

# This creates:
# - plugins/<slug>/ directory structure
# - 000-docs/planned-plugins/<slug>/ with 6 doc templates
# - Plugin README with quick start guide
```

### Working with Skills

```bash
# Install skills package in development mode
pip install -e packages/nixtla-claude-skills-installer

# Install skills to a project
cd /path/to/your/project
nixtla-skills init

# Update skills
nixtla-skills update

# Validate skills compliance
python tests/basic_validator.py
```

### Working with Baseline Lab Plugin

```bash
cd plugins/nixtla-baseline-lab

# Setup environment (creates .venv-nixtla-baseline)
./scripts/setup_nixtla_env.sh --venv
source .venv-nixtla-baseline/bin/activate
pip install -r scripts/requirements.txt

# Run the MCP server
python scripts/nixtla_baseline_mcp.py

# Run tests
python tests/run_baseline_m4_smoke.py

# In Claude Code, run slash command:
/nixtla-baseline-m4 demo_preset=m4_daily_small
```

### Documentation Standards

This repository follows **Doc-Filing v3.0** with strict naming conventions:

**Format**: `NNN-CC-ABCD-description.md`

**Category Codes**:
- `PP` - Planning & Product requirements
- `AT` - Architecture & Technical design
- `AA` - Audits & After-Action Reports
- `OD` - Overview & Documentation
- `QA` - Quality Assurance & Testing

**Per-Plugin Documentation**: Each plugin requires 6 standardized documents:
1. `01-BUSINESS-CASE.md` - ROI and market opportunity
2. `02-PRD.md` - Product requirements
3. `03-ARCHITECTURE.md` - System design
4. `04-USER-JOURNEY.md` - User experience
5. `05-TECHNICAL-SPEC.md` - Implementation details
6. `06-STATUS.md` - Current state tracking

### Python Environment Setup

```bash
# Skills installer uses Python 3.8+
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e packages/nixtla-claude-skills-installer

# Baseline lab uses Python 3.10+
cd plugins/nixtla-baseline-lab
./scripts/setup_nixtla_env.sh --venv
source .venv-nixtla-baseline/bin/activate

# BigQuery forecaster uses Python 3.10+
cd plugins/nixtla-bigquery-forecaster
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Version Management

**Current Version**: 1.3.0 (Prediction Markets Vertical Launch - 2025-12-06)

**What's in v1.3.0**:
- **New Vertical**: Prediction Markets (10 skills planned, 7 production-ready at 25/25 audit score)
- **Global Standard Skill Schema**: 26KB specification with 8 architectural patterns
- **Flagship Skill**: `nixtla-polymarket-analyst` (97/100 quality, 32-52s workflow)
- **Documentation**: 186 pages of skill specs (8 PRDs, 7 ARDs)
- **Repository**: Reorganized with planned-plugins/ and planned-skills/ directories
- See `CHANGELOG.md` for complete v1.3.0 release notes

**Version History** (see `CHANGELOG.md` for full details):
- v1.3.0 (2025-12-06): Prediction Markets Vertical Launch
- v1.2.0 (2025-12-04): Claude Skills Pack (8 skills, 95%+ compliant)
- v1.1.0 (2025-11-30): Documentation accuracy (3 working plugins verified)
- v1.0.0 (2025-11-30): Enterprise README Standard
- v0.8.0 (2025-11-30): Doc-Filing v3.0 compliance
- v0.1.0-v0.7.0: Initial implementation phases

**Release Process** (for maintainers):
1. Update `VERSION` file
2. Update `CHANGELOG.md` with detailed notes
3. Create release AAR in `000-docs/`
4. Tag: `git tag -a v1.X.Y -m "Release v1.X.Y"`
5. Push: `git push origin main --tags`

## Technology Stack

### Core Dependencies

**Python Requirements**:
- Python 3.8+ (Skills installer)
- Python 3.10+ (Baseline lab, BigQuery forecaster)
- Python 3.12 (Development environment)

**Nixtla Libraries**:
- `statsforecast` - Statistical forecasting models (AutoETS, AutoTheta, SeasonalNaive)
- `datasetsforecast` - M4 and other benchmark datasets
- `nixtla` - TimeGPT SDK (optional, requires API key)

**Cloud & Infrastructure**:
- Google Cloud Platform (BigQuery, Cloud Functions)
- Firebase (for potential hosting)
- GitHub Actions (CI/CD)

**Development Tools**:
- pytest - Testing framework
- pandas, numpy - Data manipulation
- PyYAML - Configuration files

### Key Integration Points

**Nixtla API Usage**:
```python
# StatsForecast (open source, no API key needed)
from statsforecast import StatsForecast
from statsforecast.models import AutoETS, AutoTheta, SeasonalNaive

# TimeGPT (requires NIXTLA_TIMEGPT_API_KEY)
from nixtla import NixtlaClient
client = NixtlaClient(api_key='NIXTLA_TIMEGPT_API_KEY')
```

**MCP Server Pattern** (plugins/nixtla-baseline-lab/scripts/nixtla_baseline_mcp.py):
- Exposes forecasting operations to Claude Code
- Handles tool registration and execution
- Returns structured results

**Claude Skills Pattern** (skills-pack/.claude/skills/*/):
- YAML frontmatter with `name`, `description`, `version`, `allowed-tools`
- Progressive disclosure: SKILL.md (core) + resources/ (reference)
- Auto-activation based on context detection

## Contact & Collaboration

**Maintained by**: Intent Solutions (Jeremy Longshore)
- Email: jeremy@intentsolutions.io
- Phone: 251.213.1115

**Sponsored by**: Nixtla (Max Mergenthaler)
- Email: max@nixtla.io

**Purpose**: Demonstrate plugin value to Nixtla, drive plugin investment decision for Q1 2026

## Next Steps for Max

When Max reviews this repo, guide him through:

1. **Try the plugin** (5 min): `/nixtla-baseline-m4 demo_preset=m4_daily_small`
2. **Read business case** (10 min): `000-docs/035-PP-PROD-nixtla-plugin-business-case.md`
3. **Pick top 3 plugins** (15 min): Review `000-docs/009-017-AT-ARCH-*.md`
4. **Schedule call**: Discuss priorities, timeline, ROI

**The Ask**: "Which 3 plugins deliver the most value in Q1 2026?"
