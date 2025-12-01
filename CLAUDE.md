# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

**Business Showcase Repository for Nixtla CEO (Max Mergenthaler)**

This repository demonstrates how Claude Code plugins deliver measurable business value to Nixtla through:
1. **Internal efficiency** - Make Nixtla's team 2-3x more productive
2. **Business growth** - Expand market reach to Airflow, dbt, and Snowflake customers

**Status**: 3 working plugins (Baseline Lab v0.8.0 + 2 demos) + 9 complete specifications ready to build

**Key Documents**:
- `README.md` - Business pitch for Max (start here)
- `000-docs/035-PP-PROD-nixtla-plugin-business-case.md` - Detailed ROI analysis

## Quick Commands

### Plugin Development
```bash
# Try the working plugin
cd plugins/nixtla-baseline-lab
./scripts/setup_nixtla_env.sh --venv
# Then in Claude Code: /nixtla-baseline-m4 demo_preset=m4_daily_small

# Run tests
pytest plugins/nixtla-baseline-lab/tests/

# Validate all plugins
./scripts/validate-all-plugins.sh
```

### Documentation Management
```bash
# View plugin specifications
ls -la 000-docs/009-017-*.md  # 9 complete plugin specs

# Read business case
cat 000-docs/035-PP-PROD-nixtla-plugin-business-case.md

# Check release history
cat CHANGELOG.md
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
├── plugins/
│   └── nixtla-baseline-lab/     # ✅ Working plugin (v0.8.0)
│       ├── scripts/             # MCP server, benchmarking logic
│       ├── skills/              # AI skills for result interpretation
│       ├── tests/               # Golden task harness
│       └── README.md            # Plugin user manual
│
├── 000-docs/                    # 70 technical documents
│   ├── 009-017-*.md            # 9 plugin specifications (COMPLETE)
│   ├── 035-PP-PROD-nixtla-plugin-business-case.md  # Business case
│   ├── 6767-OD-*.md            # Architecture & planning (4 canonical)
│   └── aar/                    # Phase 1-4 implementation AARs
│
├── scripts/
│   ├── run_nixtla_review_baseline.sh    # 2-minute demo
│   └── cleanup-doc-filing-v3.sh         # Doc-Filing v3.0 compliance
│
├── CHANGELOG.md                 # Release history (v0.1.0 → v0.8.0)
├── VERSION                      # Current: 0.8.0
└── README.md                    # Business showcase (for Max)
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

## Testing

```bash
# Run full test suite
pytest

# Run with coverage (minimum 65%)
pytest --cov=plugins --cov-report=term-missing

# Run specific plugin tests
pytest plugins/nixtla-baseline-lab/tests/

# Golden task validation (CI uses this)
cd plugins/nixtla-baseline-lab/tests
python run_baseline_m4_smoke.py
```

## Nixtla Integration Patterns

```python
# StatsForecast (currently implemented)
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

## Version Management

**Current Version**: 1.1.0 (3 Working Plugins + Doc Renumbering)

**Release Process**:
1. Update `VERSION` file
2. Update `CHANGELOG.md` with release notes
3. Create release AAR in `000-docs/0NN-OD-RELS-*.md`
4. Update README version references
5. Tag: `git tag -a v0.X.Y -m "Release vX.Y.Z"`
6. Push: `git push origin main --tags`

**Semantic Versioning**:
- **MAJOR**: Breaking changes, major architectural shifts
- **MINOR**: New plugins, additive features, significant improvements
- **PATCH**: Bug fixes, documentation, CI tweaks

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
