# Nixtla Plugin Showcase

> Experimental Claude Code plugins and AI skills for Nixtla time-series forecasting workflows

**Sponsor:** Nixtla (Max Mergenthaler)
**Prepared by:** Intent Solutions (jeremy@intentsolutions.io)
**Version:** 1.2.0 | **Last Updated:** 2025-12-04
**Status:** 3 plugins working · 9 specified · 8 skills (100% compliant)

---

## Quick Navigation

| I am a... | Start here |
|-----------|------------|
| 👔 Executive / Decision Maker | [Executive Summary](000-docs/global/000-EXECUTIVE-SUMMARY.md) |
| 💰 Evaluating Investment | [Engagement Options](000-docs/global/001-ENGAGEMENT-OPTIONS.md) |
| 🎯 Deciding Which Plugin | [Decision Matrix](000-docs/global/002-DECISION-MATRIX.md) |
| 🧠 Using Claude Skills | [Skills Pack](#-claude-skills-pack) |
| 🔧 Technical Evaluator | [Architecture Overview](#architecture-overview) |
| 👤 Potential User | [Demo](#demo) |

---

## Portfolio Overview

| Category | Count | Description |
|----------|-------|-------------|
| **Plugins** | | |
| ✅ Working | 3 | Ready to use now |
| 📋 Specified | 9 | Full docs, ready to build |
| 🔨 In Progress | 0 | Currently building |
| **Skills** | | |
| 🧠 Implemented | 8 | Claude Skills Pack (95%+ compliant) |
| **Total** | **20** | |

---

## 🧠 Claude Skills Pack

AI agent skills that transform Claude Code into a Nixtla forecasting expert. Skills activate automatically when Claude detects relevant context.

**Location:** `skills-pack/.claude/skills/nixtla-*/`
**Standard:** [Nixtla SKILL Standard](000-docs/041-SPEC-nixtla-skill-standard.md)
**Compliance:** 95%+ ([Audit Report](000-docs/085-QA-AUDT-claude-skills-compliance-audit.md))

### Skills Inventory

| Skill | Type | Description | Docs |
|-------|------|-------------|------|
| `nixtla-timegpt-lab` | Mode | Transforms Claude into Nixtla forecasting expert | [SKILL](skills-pack/.claude/skills/nixtla-timegpt-lab/SKILL.md) |
| `nixtla-experiment-architect` | Utility | Scaffold complete forecasting experiments | [SKILL](skills-pack/.claude/skills/nixtla-experiment-architect/SKILL.md) |
| `nixtla-schema-mapper` | Utility | Map data to Nixtla-compatible schema | [SKILL](skills-pack/.claude/skills/nixtla-schema-mapper/SKILL.md) |
| `nixtla-timegpt-finetune-lab` | Utility | Guide TimeGPT fine-tuning workflows | [SKILL](skills-pack/.claude/skills/nixtla-timegpt-finetune-lab/SKILL.md) |
| `nixtla-prod-pipeline-generator` | Utility | Generate production inference pipelines | [SKILL](skills-pack/.claude/skills/nixtla-prod-pipeline-generator/SKILL.md) |
| `nixtla-usage-optimizer` | Utility | Audit usage, suggest cost optimizations | [SKILL](skills-pack/.claude/skills/nixtla-usage-optimizer/SKILL.md) |
| `nixtla-skills-bootstrap` | Infra | Install/update skills via CLI | [SKILL](skills-pack/.claude/skills/nixtla-skills-bootstrap/SKILL.md) |
| `nixtla-skills-index` | Utility | List available skills and usage guidance | [SKILL](skills-pack/.claude/skills/nixtla-skills-index/SKILL.md) |

### Install Skills

```bash
# Clone repo and install CLI
git clone https://github.com/intent-solutions-io/plugins-nixtla.git
cd claude-code-plugins-nixtla
pip install -e packages/nixtla-claude-skills-installer

# Install skills in your project
cd /path/to/your/forecasting-project
nixtla-skills init
```

Skills are installed to `.claude/skills/nixtla-*/` in your project and activate automatically in Claude Code.

### Skills Architecture

```
skills-pack/.claude/skills/
├── nixtla-timegpt-lab/           # Mode skill (changes Claude behavior)
│   ├── SKILL.md                  # Core prompt (<5,000 words)
│   ├── scripts/                  # Executable code
│   ├── references/               # Long-form docs
│   └── assets/                   # Templates, configs
├── nixtla-experiment-architect/  # Utility skill
├── nixtla-schema-mapper/         # Utility skill
└── [5 more skills]/
```

**Detailed docs:** [Skills Architecture](000-docs/038-AT-ARCH-nixtla-claude-skills-pack.md) | [DevOps Guide](000-docs/global/003-GUIDE-devops-nixtla-skills-operations.md)

---

## ✅ Working Plugins

---

#### Baseline Lab

| | |
|---|---|
| **Status** | ✅ Working (v1.1.0) |
| **Category** | Benchmarking |

**What It Does**

Runs statsforecast baseline models (AutoETS, AutoTheta, SeasonalNaive) on M4 benchmark data, generates human-readable metric summaries (sMAPE, MASE), creates complete reproducibility bundles (library versions, configs, data), and produces GitHub-ready issue drafts with full context. Optionally compares against TimeGPT for benchmarking.

**Use Cases**

- Reproduce customer-reported forecasting issues with consistent baseline comparisons
- Generate standardized benchmark reports for GitHub issues
- Validate statsforecast model behavior on M4 datasets
- Compare baseline models against TimeGPT (optional)

**Try It Now**

```bash
git clone https://github.com/intent-solutions-io/plugins-nixtla.git
cd claude-code-plugins-nixtla/plugins/nixtla-baseline-lab

# Setup
./scripts/setup_nixtla_env.sh --venv
source .venv-nixtla-baseline/bin/activate
pip install -r scripts/requirements.txt

# In Claude Code:
/nixtla-baseline-m4 demo_preset=m4_daily_small
```

**Documentation**

| Doc | Description |
|-----|-------------|
| [Business Case](000-docs/planned-plugins/nixtla-baseline-lab/01-BUSINESS-CASE.md) | ROI and market opportunity |
| [PRD](000-docs/planned-plugins/nixtla-baseline-lab/02-PRD.md) | Requirements and success metrics |
| [Architecture](000-docs/planned-plugins/nixtla-baseline-lab/03-ARCHITECTURE.md) | System design and integrations |
| [User Journey](000-docs/planned-plugins/nixtla-baseline-lab/04-USER-JOURNEY.md) | Step-by-step usage guide |
| [Technical Spec](000-docs/planned-plugins/nixtla-baseline-lab/05-TECHNICAL-SPEC.md) | Implementation details |
| [Status](000-docs/planned-plugins/nixtla-baseline-lab/06-STATUS.md) | Current state and roadmap |

---

#### BigQuery Forecaster

| | |
|---|---|
| **Status** | ✅ Working Demo |
| **Category** | Integration |

**What It Does**

Runs Nixtla statsforecast models (AutoETS, AutoTheta, SeasonalNaive) on BigQuery data via serverless Cloud Functions. Tested with Chicago taxi public dataset (200M+ rows). Supports optional TimeGPT comparison when API key provided.

**Use Cases**

- Run forecasting models on BigQuery datasets without moving data
- Deploy serverless forecasting with Cloud Functions auto-scaling
- Test Nixtla models on large-scale public datasets
- Template for Google Cloud + Nixtla integrations

**Try It Now**

```bash
cd plugins/nixtla-bigquery-forecaster

# Local test
source .venv/bin/activate
python test_local.py

# Deploy via GitHub Actions (push to main)
# Then test with Chicago taxi data (PUBLIC - no setup needed)
curl -X POST "https://YOUR-FUNCTION-URL" \
  -H "Content-Type: application/json" \
  -d '{"project_id": "bigquery-public-data", "dataset": "chicago_taxi_trips", ...}'
```

**Git Reference**: `4d4f679` - feat: Nixtla BigQuery Forecaster - Cloud Functions demo

---

#### Search-to-Slack

| | |
|---|---|
| **Status** | ✅ Working MVP (v0.1.0) |
| **Category** | Content Automation |

**What It Does**

Automated content discovery and curation pipeline: searches web (SerpAPI) and GitHub for Nixtla/time-series content, uses AI (OpenAI/Anthropic) to summarize and curate, posts formatted digests to Slack with Block Kit formatting. Construction kit / reference implementation.

**Use Cases**

- Monitor web and GitHub for Nixtla mentions and time-series discussions
- Automate content curation with AI-powered summarization
- Reference patterns for search → AI → Slack workflows
- Learn integration patterns (comprehensive setup guide with 6 test files)

**Try It Now**

```bash
cd plugins/nixtla-search-to-slack

# Setup (see SETUP_GUIDE.md for detailed instructions)
pip install -r requirements.txt
cp .env.example .env  # Configure API keys

# Run tests
pytest tests/
```

**Git Reference**: `0c27c23` - feat: add FREE web search providers

**Note**: This is an MVP / construction kit. See README.md for what is and isn't implemented.

---

## 📋 Specified Plugins (Ready to Build)

**Internal Efficiency Plugins**

---

#### Cost Optimizer

| | |
|---|---|
| **Status** | 📋 Specified |
| **Category** | Efficiency |
| **Build Time** | 4-6 weeks |

**What It Does**

Analyzes Nixtla API usage patterns, detects redundant forecasts, implements intelligent caching, and provides actionable cost-saving recommendations. Detects scenarios where misconfigured cron jobs or inefficient batching cause unexpected API costs.

**Use Cases**

- Analyze TimeGPT API usage patterns and identify optimization opportunities
- Detect redundant forecast requests that could be cached
- Monitor API spend trends and provide cost projections
- Alert on usage anomalies that may indicate misconfiguration

**Documentation**

| Doc | Description |
|-----|-------------|
| [Business Case](000-docs/planned-plugins/nixtla-cost-optimizer/01-BUSINESS-CASE.md) | ROI and market opportunity |
| [PRD](000-docs/planned-plugins/nixtla-cost-optimizer/02-PRD.md) | Product requirements and success metrics |
| [Architecture](000-docs/planned-plugins/nixtla-cost-optimizer/03-ARCHITECTURE.md) | System design and integrations |
| [User Journey](000-docs/planned-plugins/nixtla-cost-optimizer/04-USER-JOURNEY.md) | Step-by-step usage guide |
| [Technical Spec](000-docs/planned-plugins/nixtla-cost-optimizer/05-TECHNICAL-SPEC.md) | Implementation details |
| [Status](000-docs/planned-plugins/nixtla-cost-optimizer/06-STATUS.md) | Current state and roadmap |

💡 **Comprehensive Spec**: [All-in-one document](000-docs/009-AT-ARCH-plugin-01-nixtla-cost-optimizer.md) (59KB)

---

#### Migration Assistant

| | |
|---|---|
| **Status** | 📋 Specified |
| **Category** | Efficiency |
| **Build Time** | 4-6 weeks |

**What It Does**

Automated migration tool that analyzes existing StatsForecast/MLForecast code and generates equivalent TimeGPT API calls, with side-by-side A/B testing, rollback safety, and accuracy validation.

**Use Cases**

- Convert existing StatsForecast/MLForecast code to TimeGPT API calls
- Run side-by-side comparisons between OSS models and TimeGPT
- Validate accuracy before switching to TimeGPT in production
- Generate migration reports with accuracy metrics and recommendations

**Documentation**

| Doc | Description |
|-----|-------------|
| [Business Case](000-docs/planned-plugins/nixtla-migration-assistant/01-BUSINESS-CASE.md) | ROI and market opportunity |
| [PRD](000-docs/planned-plugins/nixtla-migration-assistant/02-PRD.md) | Product requirements and success metrics |
| [Architecture](000-docs/planned-plugins/nixtla-migration-assistant/03-ARCHITECTURE.md) | System design and integrations |
| [User Journey](000-docs/planned-plugins/nixtla-migration-assistant/04-USER-JOURNEY.md) | Step-by-step usage guide |
| [Technical Spec](000-docs/planned-plugins/nixtla-migration-assistant/05-TECHNICAL-SPEC.md) | Implementation details |
| [Status](000-docs/planned-plugins/nixtla-migration-assistant/06-STATUS.md) | Current state and roadmap |

💡 **Comprehensive Spec**: [All-in-one document](000-docs/016-AT-ARCH-plugin-08-nixtla-migration-assistant.md) (37KB)

---

#### Forecast Explainer

| | |
|---|---|
| **Status** | 📋 Specified |
| **Category** | Efficiency |
| **Build Time** | 4-6 weeks |

**What It Does**

Post-hoc explainability tool that transforms TimeGPT forecasts into transparent explanations with visual decomposition, SHAP values, confidence bounds, and plain-English narratives.

**Use Cases**

- Generate explainability reports for TimeGPT forecasts
- Decompose forecasts into trend, seasonal, and residual components
- Calculate SHAP values to explain feature importance
- Create stakeholder-friendly narrative explanations

**Documentation**

| Doc | Description |
|-----|-------------|
| [Business Case](000-docs/planned-plugins/nixtla-forecast-explainer/01-BUSINESS-CASE.md) | ROI and market opportunity |
| [PRD](000-docs/planned-plugins/nixtla-forecast-explainer/02-PRD.md) | Product requirements and success metrics |
| [Architecture](000-docs/planned-plugins/nixtla-forecast-explainer/03-ARCHITECTURE.md) | System design and integrations |
| [User Journey](000-docs/planned-plugins/nixtla-forecast-explainer/04-USER-JOURNEY.md) | Step-by-step usage guide |
| [Technical Spec](000-docs/planned-plugins/nixtla-forecast-explainer/05-TECHNICAL-SPEC.md) | Implementation details |
| [Status](000-docs/planned-plugins/nixtla-forecast-explainer/06-STATUS.md) | Current state and roadmap |

💡 **Comprehensive Spec**: [All-in-one document](000-docs/017-AT-ARCH-plugin-09-nixtla-forecast-explainer.md) (40KB)

---

**Market Expansion Plugins**

---

#### VS StatsForecast Benchmark

| | |
|---|---|
| **Status** | 📋 Specified |
| **Category** | Growth |
| **Build Time** | 3-4 weeks |

**What It Does**

Side-by-side comparison tool that benchmarks TimeGPT API against local StatsForecast OSS models, providing accuracy metrics (MAPE, RMSE, sMAPE) and comparative analysis.

**Use Cases**

- Run head-to-head accuracy comparisons between TimeGPT and StatsForecast
- Generate benchmark reports with multiple accuracy metrics
- Test on standard datasets (M4, M5) or custom data
- Extension of existing Baseline Lab plugin

**Documentation**

| Doc | Description |
|-----|-------------|
| [Business Case](000-docs/planned-plugins/nixtla-vs-statsforecast-benchmark/01-BUSINESS-CASE.md) | ROI and market opportunity |
| [PRD](000-docs/planned-plugins/nixtla-vs-statsforecast-benchmark/02-PRD.md) | Product requirements and success metrics |
| [Architecture](000-docs/planned-plugins/nixtla-vs-statsforecast-benchmark/03-ARCHITECTURE.md) | System design and integrations |
| [User Journey](000-docs/planned-plugins/nixtla-vs-statsforecast-benchmark/04-USER-JOURNEY.md) | Step-by-step usage guide |
| [Technical Spec](000-docs/planned-plugins/nixtla-vs-statsforecast-benchmark/05-TECHNICAL-SPEC.md) | Implementation details |
| [Status](000-docs/planned-plugins/nixtla-vs-statsforecast-benchmark/06-STATUS.md) | Current state and roadmap |

💡 **Comprehensive Spec**: [All-in-one document](000-docs/010-AT-ARCH-plugin-02-nixtla-vs-statsforecast-benchmark.md) (23KB)

---

#### ROI Calculator

| | |
|---|---|
| **Status** | 📋 Specified |
| **Category** | Growth |
| **Build Time** | 3-4 weeks |

**What It Does**

Interactive ROI calculator that compares total cost of ownership (TCO) for internal forecasting builds vs Nixtla TimeGPT API, generating executive-ready business case reports.

**Use Cases**

- Calculate TCO for internal forecasting vs TimeGPT API
- Generate business case reports with cost breakdowns
- Compare build vs buy scenarios with customizable inputs
- Export executive summaries for procurement approval

**Documentation**

| Doc | Description |
|-----|-------------|
| [Business Case](000-docs/planned-plugins/nixtla-roi-calculator/01-BUSINESS-CASE.md) | ROI and market opportunity |
| [PRD](000-docs/planned-plugins/nixtla-roi-calculator/02-PRD.md) | Product requirements and success metrics |
| [Architecture](000-docs/planned-plugins/nixtla-roi-calculator/03-ARCHITECTURE.md) | System design and integrations |
| [User Journey](000-docs/planned-plugins/nixtla-roi-calculator/04-USER-JOURNEY.md) | Step-by-step usage guide |
| [Technical Spec](000-docs/planned-plugins/nixtla-roi-calculator/05-TECHNICAL-SPEC.md) | Implementation details |
| [Status](000-docs/planned-plugins/nixtla-roi-calculator/06-STATUS.md) | Current state and roadmap |

💡 **Comprehensive Spec**: [All-in-one document](000-docs/011-AT-ARCH-plugin-03-nixtla-roi-calculator.md) (22KB)

---

#### Airflow Operator

| | |
|---|---|
| **Status** | 📋 Specified |
| **Category** | Growth |
| **Build Time** | 6-8 weeks |

**What It Does**

Apache Airflow operator (`NixtlaForecastOperator`) that integrates Nixtla TimeGPT forecasting into DAGs with automatic retry logic, authentication handling, and dependency management.

**Use Cases**

- Integrate TimeGPT forecasting into existing Airflow DAGs
- Schedule forecasting jobs with Airflow's orchestration
- Leverage Airflow's retry logic and monitoring
- Deploy production forecasting pipelines with minimal glue code

**Documentation**

| Doc | Description |
|-----|-------------|
| [Business Case](000-docs/planned-plugins/nixtla-airflow-operator/01-BUSINESS-CASE.md) | ROI and market opportunity |
| [PRD](000-docs/planned-plugins/nixtla-airflow-operator/02-PRD.md) | Product requirements and success metrics |
| [Architecture](000-docs/planned-plugins/nixtla-airflow-operator/03-ARCHITECTURE.md) | System design and integrations |
| [User Journey](000-docs/planned-plugins/nixtla-airflow-operator/04-USER-JOURNEY.md) | Step-by-step usage guide |
| [Technical Spec](000-docs/planned-plugins/nixtla-airflow-operator/05-TECHNICAL-SPEC.md) | Implementation details |
| [Status](000-docs/planned-plugins/nixtla-airflow-operator/06-STATUS.md) | Current state and roadmap |

💡 **Comprehensive Spec**: [All-in-one document](000-docs/012-AT-ARCH-plugin-04-nixtla-airflow-operator.md) (19KB)

---

#### dbt Package

| | |
|---|---|
| **Status** | 📋 Specified |
| **Category** | Growth |
| **Build Time** | 6-8 weeks |

**What It Does**

Native dbt package that treats forecasting as a data transformation step, allowing SQL analysts to generate Nixtla forecasts using `{{ nixtla_forecast(...) }}` macros directly in dbt models.

**Use Cases**

- Generate forecasts within dbt transformation workflows
- SQL-native interface (no Python required)
- Integrate forecasting into existing dbt projects
- Enable self-serve forecasting for analytics engineers

**Documentation**

| Doc | Description |
|-----|-------------|
| [Business Case](000-docs/planned-plugins/nixtla-dbt-package/01-BUSINESS-CASE.md) | ROI and market opportunity |
| [PRD](000-docs/planned-plugins/nixtla-dbt-package/02-PRD.md) | Product requirements and success metrics |
| [Architecture](000-docs/planned-plugins/nixtla-dbt-package/03-ARCHITECTURE.md) | System design and integrations |
| [User Journey](000-docs/planned-plugins/nixtla-dbt-package/04-USER-JOURNEY.md) | Step-by-step usage guide |
| [Technical Spec](000-docs/planned-plugins/nixtla-dbt-package/05-TECHNICAL-SPEC.md) | Implementation details |
| [Status](000-docs/planned-plugins/nixtla-dbt-package/06-STATUS.md) | Current state and roadmap |

💡 **Comprehensive Spec**: [All-in-one document](000-docs/013-AT-ARCH-plugin-05-nixtla-dbt-package.md) (12KB)

---

#### Snowflake Adapter

| | |
|---|---|
| **Status** | 📋 Specified |
| **Category** | Growth |
| **Build Time** | 8-10 weeks |

**What It Does**

Claude Code plugin that wraps Nixtla's existing Snowflake Native App integration, providing one-command SQL-native forecasting with automatic setup and error handling directly in Snowflake.

**Use Cases**

- Run TimeGPT forecasts on data in Snowflake without moving it
- SQL-native interface for Snowflake users
- Leverage Snowflake's security and compliance features
- Simplify setup of Nixtla's Snowflake Native App

**Documentation**

| Doc | Description |
|-----|-------------|
| [Business Case](000-docs/planned-plugins/nixtla-snowflake-adapter/01-BUSINESS-CASE.md) | ROI and market opportunity |
| [PRD](000-docs/planned-plugins/nixtla-snowflake-adapter/02-PRD.md) | Product requirements and success metrics |
| [Architecture](000-docs/planned-plugins/nixtla-snowflake-adapter/03-ARCHITECTURE.md) | System design and integrations |
| [User Journey](000-docs/planned-plugins/nixtla-snowflake-adapter/04-USER-JOURNEY.md) | Step-by-step usage guide |
| [Technical Spec](000-docs/planned-plugins/nixtla-snowflake-adapter/05-TECHNICAL-SPEC.md) | Implementation details |
| [Status](000-docs/planned-plugins/nixtla-snowflake-adapter/06-STATUS.md) | Current state and roadmap |

💡 **Comprehensive Spec**: [All-in-one document](000-docs/014-AT-ARCH-plugin-06-nixtla-snowflake-adapter.md) (12KB)

---

#### Anomaly Streaming Monitor

| | |
|---|---|
| **Status** | 📋 Specified |
| **Category** | Growth |
| **Build Time** | 8-10 weeks |

**What It Does**

Real-time streaming anomaly detection plugin that processes Kafka/Kinesis streams with sub-second latency, using Nixtla's TimeGPT for anomaly detection with automatic alerting and dashboard visualization.

**Use Cases**

- Monitor streaming data for anomalies in real-time
- Process Kafka/Kinesis streams with TimeGPT anomaly detection
- Configure automatic alerts for detected anomalies
- Visualize anomalies in real-time dashboards

**Documentation**

| Doc | Description |
|-----|-------------|
| [Business Case](000-docs/planned-plugins/nixtla-anomaly-streaming-monitor/01-BUSINESS-CASE.md) | ROI and market opportunity |
| [PRD](000-docs/planned-plugins/nixtla-anomaly-streaming-monitor/02-PRD.md) | Product requirements and success metrics |
| [Architecture](000-docs/planned-plugins/nixtla-anomaly-streaming-monitor/03-ARCHITECTURE.md) | System design and integrations |
| [User Journey](000-docs/planned-plugins/nixtla-anomaly-streaming-monitor/04-USER-JOURNEY.md) | Step-by-step usage guide |
| [Technical Spec](000-docs/planned-plugins/nixtla-anomaly-streaming-monitor/05-TECHNICAL-SPEC.md) | Implementation details |
| [Status](000-docs/planned-plugins/nixtla-anomaly-streaming-monitor/06-STATUS.md) | Current state and roadmap |

💡 **Comprehensive Spec**: [All-in-one document](000-docs/015-AT-ARCH-plugin-07-nixtla-anomaly-streaming-monitor.md) (42KB)

---

## 💡 Ideas & Backlog

Concepts that need discovery before specification.

| Idea | Category | Potential Impact | What's Needed |
|------|----------|------------------|---------------|
| *No ideas yet* | | | |

**Have an idea?** Add it to this table or discuss with the Nixtla team. All current concepts have been fully specified and are ready to build.

---

## Demo

### Try the Working Plugin Now

**Nixtla Baseline Lab** runs statsforecast benchmarks on M4 data with complete reproducibility.

```bash
# Clone the repository
git clone https://github.com/intent-solutions-io/plugins-nixtla.git
cd claude-code-plugins-nixtla/plugins/nixtla-baseline-lab

# Setup Python environment
./scripts/setup_nixtla_env.sh --venv
source .venv-nixtla-baseline/bin/activate
pip install -r scripts/requirements.txt

# In Claude Code, run:
/nixtla-baseline-m4 demo_preset=m4_daily_small
```

### What You Get

- ✅ Metrics CSV (sMAPE, MASE per model)
- ✅ Human-readable summary with interpretation
- ✅ GitHub-ready issue draft with full context
- ✅ Complete reproducibility bundle (versions, configs, data)

**Demo runs in ~90 seconds** with zero API costs (fully offline baseline mode).

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      Claude Code CLI                         │
├─────────────────────────────────────────────────────────────┤
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐   │
│  │  Baseline Lab │  │ Cost Optimizer│  │ ROI Calculator│   │
│  │   (Working)   │  │  (Specified)  │  │  (Specified)  │   │
│  └───────┬───────┘  └───────┬───────┘  └───────┬───────┘   │
│          │                  │                  │            │
│          ▼                  ▼                  ▼            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │        Nixtla Ecosystem                             │   │
│  │  statsforecast · datasetsforecast · nixtla SDK      │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Plugin Architecture:**
- **MCP Servers**: Expose forecasting operations to Claude Code
- **Slash Commands**: `/nixtla-*` commands for direct invocation
- **Agent Skills**: Auto-triggered when Claude detects forecasting discussions
- **Python Backend**: statsforecast, datasetsforecast, nixtla SDK integration

**Detailed architecture**: See [individual plugin docs](000-docs/planned-plugins/)

---

## Documentation Index

### Per-Plugin Documentation

Every specified plugin includes standardized documentation:

| Doc | Audience | Purpose |
|-----|----------|---------|
| 01-BUSINESS-CASE.md | Executive | ROI, market opportunity, recommendation |
| 02-PRD.md | Product | Requirements, user stories, success metrics |
| 03-ARCHITECTURE.md | Tech Lead | System design, integrations, constraints |
| 04-USER-JOURNEY.md | End User | Step-by-step experience with examples |
| 05-TECHNICAL-SPEC.md | Engineer | APIs, dependencies, implementation |
| 06-STATUS.md | Everyone | Current state, blockers, next steps |

**Status**: Baseline Lab has full docs. Specified plugins have comprehensive architecture specs (051-059 series) + STATUS docs.

### Global Documentation

| Doc | Purpose |
|-----|---------|
| [000-EXECUTIVE-SUMMARY.md](000-docs/global/000-EXECUTIVE-SUMMARY.md) | 1-page overview for Max |
| [001-ENGAGEMENT-OPTIONS.md](000-docs/global/001-ENGAGEMENT-OPTIONS.md) | Pricing, timelines, decision framework |
| [002-DECISION-MATRIX.md](000-docs/global/002-DECISION-MATRIX.md) | Which plugin to build first |

---

## Engagement Options

| Option | Scope | Timeline |
|--------|-------|----------|
| 🧪 **Evaluate** | Use working demos for 30 days | No commitment |
| 🎯 **Pilot** | 1 plugin to production | 4-6 weeks |
| 🚀 **Platform** | 3+ plugins | 12-16 weeks |

**Details:** [Engagement Options](000-docs/global/001-ENGAGEMENT-OPTIONS.md) | [Decision Matrix](000-docs/global/002-DECISION-MATRIX.md)

---

## Quality Standards

| Metric | Target | Current (Baseline Lab) |
|--------|--------|------------------------|
| Test Coverage | 65%+ | 67% |
| Docs per Plugin | 6 (or comprehensive spec) | ✅ Complete |
| CI/CD | All plugins | ✅ Active (Baseline Lab) |
| Reproducibility | 100% | ✅ Full repro bundles |

**Baseline Lab** meets all quality standards with CI/CD validation via golden task harness.

---

## Adding Plugins

### Add an Idea

1. Add row to "Ideas & Backlog" section above (currently empty - all concepts are specified)

### Specify a Plugin

```bash
./scripts/new-plugin.sh <slug> "<Name>" <category>
# Example: ./scripts/new-plugin.sh cost-optimizer "Cost Optimizer" efficiency
```

This creates:
- `plugins/<slug>/` directory structure
- `000-docs/planned-plugins/<slug>/` with all 6 doc templates
- Plugin README with quick start guide

### Validate Documentation

```bash
./scripts/validate-docs.sh
```

Checks for:
- Global docs exist (Executive Summary, Engagement Options)
- Each plugin has required docs
- No unfilled placeholders
- README has required sections

---

## Repository Structure

```
nixtla-plugin-showcase/
├── README.md                              # This file
├── CHANGELOG.md                           # Release history
├── VERSION                                # Current: 1.2.0
│
├── 000-docs/                              # Documentation (Doc-Filing v3.0)
│   ├── global/                            # Repo-wide docs
│   │   ├── 000-EXECUTIVE-SUMMARY.md       # For Max
│   │   ├── 001-ENGAGEMENT-OPTIONS.md      # Pilot/Platform options
│   │   ├── 002-DECISION-MATRIX.md         # Plugin prioritization
│   │   └── 003-GUIDE-devops-*.md          # Skills DevOps guide
│   ├── plugins/                           # Per-plugin docs (10 plugins)
│   ├── aar/                               # After-Action Reports
│   ├── 041-SPEC-nixtla-skill-standard.md  # Skills standard
│   ├── 038-AT-ARCH-nixtla-claude-skills-pack.md  # Skills architecture
│   └── 085-QA-AUDT-claude-skills-*.md     # Skills compliance audit
│
├── skills-pack/                           # Claude Skills Pack (8 skills)
│   └── .claude/skills/
│       ├── nixtla-timegpt-lab/            # Mode skill
│       ├── nixtla-experiment-architect/   # Utility
│       ├── nixtla-schema-mapper/          # Utility
│       ├── nixtla-timegpt-finetune-lab/   # Utility
│       ├── nixtla-prod-pipeline-generator/# Utility
│       ├── nixtla-usage-optimizer/        # Utility
│       ├── nixtla-skills-bootstrap/       # Infra
│       └── nixtla-skills-index/           # Utility
│
├── packages/                              # Distributable packages
│   └── nixtla-claude-skills-installer/    # Skills CLI installer
│
├── plugins/                               # Working plugin code
│   ├── nixtla-baseline-lab/               # Benchmarking plugin
│   ├── nixtla-bigquery-forecaster/        # BigQuery demo
│   └── nixtla-search-to-slack/            # Content automation
│
├── demo-project/                          # End-to-end demo walkthrough
│
└── scripts/                               # Utility scripts
```

---

## Technology Stack

**Languages:** Python 3.10+
**Nixtla Libraries:** statsforecast, datasetsforecast, nixtla (TimeGPT SDK)
**Testing:** pytest with golden task harness
**CI/CD:** GitHub Actions with validation pipeline
**Documentation:** Doc-Filing v3.0 compliant markdown

---

## Development History

- **Timeline**: First working plugin (Baseline Lab) completed in 8 weeks
- **Documentation**: 70+ technical documents following Doc-Filing v3.0 standard
- **Infrastructure**: Full CI/CD pipeline with GitHub Actions validation
- **Testing**: Golden task harness with 67% test coverage

---

## Contact

**Jeremy Longshore** | Intent Solutions
📧 jeremy@intentsolutions.io
📞 251.213.1115
📅 [Schedule Call](https://calendly.com/intentconsulting)

**Next Steps for Max:**
1. ⏱️ **Try the demo** (5 min): `/nixtla-baseline-m4 demo_preset=m4_daily_small`
2. 📖 **Read business case** (10 min): [Executive Summary](000-docs/global/000-EXECUTIVE-SUMMARY.md)
3. 🎯 **Pick top 3 plugins** (15 min): [Decision Matrix](000-docs/global/002-DECISION-MATRIX.md)
4. 📞 **Schedule call**: Discuss priorities, timeline, ROI

---

## License & Disclaimer

**License:** MIT — You own what we build together.

**This is:**
- ✅ Experimental collaboration
- ✅ Business development prototype
- ✅ Proof of execution capability

**This is NOT:**
- ❌ Production SLA
- ❌ Official Nixtla product
- ❌ Guaranteed ROI

All plugins are prototypes demonstrating feasibility. Production deployment requires proper testing, security review, and maintenance agreements.

---

*Maintained by Intent Solutions | Sponsored by Nixtla*

**Version 1.2.0** | 3 working plugins, 9 specified plugins, 8 Claude Skills (95%+ compliant), 70+ technical documents.
