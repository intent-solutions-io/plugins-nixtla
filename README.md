# Nixtla Plugin Showcase

> Open playground for Claude Code plugins and AI skills that accelerate Nixtla's internal operations, enhance open-source tools, serve current customers, and unlock new markets

**Sponsor:** Nixtla (Max Mergenthaler)
**Prepared by:** Intent Solutions (jeremy@intentsolutions.io)
**Version:** 1.2.0 | **Last Updated:** 2025-12-01
**Status:** 3 plugins working · 9 specified · 8 skills (95%+ compliant)

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
git clone https://github.com/jeremylongshore/claude-code-plugins-nixtla.git
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
| **Category** | Efficiency |
| **Impact** | 95% time reduction in customer issue reproduction |

**What It Does**

Runs statsforecast baseline models (AutoETS, AutoTheta, SeasonalNaive) on M4 benchmark data, generates human-readable metric summaries (sMAPE, MASE), creates complete reproducibility bundles (library versions, configs, data), and produces GitHub-ready issue drafts with full context. Optionally compares against TimeGPT for benchmarking.

**Business Value**

- **95% time reduction**: Customer issue reproduction from 2-4 hours → 5 minutes
- **20% productivity gain**: Engineers save 7-9 hours per week
- **50% faster resolution**: Issue cycle time from 2-3 days → 1 day
- **Improved standardization**: Consistent benchmark workflow eliminates back-and-forth

**Try It Now**

```bash
git clone https://github.com/jeremylongshore/claude-code-plugins-nixtla.git
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
| [Business Case](000-docs/plugins/nixtla-baseline-lab/01-BUSINESS-CASE.md) | ROI and market opportunity |
| [PRD](000-docs/plugins/nixtla-baseline-lab/02-PRD.md) | Requirements and success metrics |
| [Architecture](000-docs/plugins/nixtla-baseline-lab/03-ARCHITECTURE.md) | System design and integrations |
| [User Journey](000-docs/plugins/nixtla-baseline-lab/04-USER-JOURNEY.md) | Step-by-step usage guide |
| [Technical Spec](000-docs/plugins/nixtla-baseline-lab/05-TECHNICAL-SPEC.md) | Implementation details |
| [Status](000-docs/plugins/nixtla-baseline-lab/06-STATUS.md) | Current state and roadmap |

---

#### BigQuery Forecaster

| | |
|---|---|
| **Status** | ✅ Working Demo |
| **Category** | Integration |
| **Impact** | Demonstrates Nixtla + Google Cloud at 200M+ row scale |

**What It Does**

Runs Nixtla statsforecast models (AutoETS, AutoTheta, SeasonalNaive) on BigQuery data via serverless Cloud Functions. Tested with Chicago taxi public dataset (200M+ rows). Supports optional TimeGPT comparison when API key provided.

**Business Value**

- **Demonstrates scalability**: Nixtla OSS handles 100K+ rows easily
- **Serverless deployment**: Cloud Functions auto-scale with zero server management
- **Real-world proof point**: Not toy examples - real data, real use case
- **Partnership potential**: Template for Nixtla + Google Cloud integrations

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
| **Impact** | Automated content discovery for time-series/forecasting |

**What It Does**

Automated content discovery and curation pipeline: searches web (SerpAPI) and GitHub for Nixtla/time-series content, uses AI (OpenAI/Anthropic) to summarize and curate, posts formatted digests to Slack with Block Kit formatting. Construction kit / reference implementation.

**Business Value**

- **Automated monitoring**: Stay on top of Nixtla mentions, time-series discussions
- **Content curation**: AI-filtered, AI-summarized content saves reading time
- **Reference implementation**: Patterns for search → AI → Slack workflows
- **Educational**: Comprehensive setup guide (24KB) and 6 test files

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

**Internal Efficiency** (Make Your Team Faster)

---

#### Cost Optimizer

| | |
|---|---|
| **Status** | 📋 Specified |
| **Category** | Efficiency |
| **Impact** | 30-50% reduction in TimeGPT API costs |
| **Build Time** | 4-6 weeks |
| **Priority** | 🥇 Recommended Quick Win (Score: 4.6/5) |

**What It Does**

Analyzes Nixtla API usage patterns, detects redundant forecasts, implements intelligent caching, and provides actionable cost-saving recommendations. Prevents bill shock scenarios where misconfigured cron jobs or inefficient batching cause massive unexpected API costs.

**Business Value**

- **30-50% direct cost reduction** through redundancy detection and caching
- **Prevents customer churn** from bill shock (massive unexpected costs)
- **Clear ROI metric** with before/after API spend comparison
- **Enterprise risk management** with cost projection and alerts

**Documentation**

| Doc | Description |
|-----|-------------|
| [Business Case](000-docs/plugins/nixtla-cost-optimizer/01-BUSINESS-CASE.md) | ROI and market opportunity |
| [PRD](000-docs/plugins/nixtla-cost-optimizer/02-PRD.md) | Product requirements and success metrics |
| [Architecture](000-docs/plugins/nixtla-cost-optimizer/03-ARCHITECTURE.md) | System design and integrations |
| [User Journey](000-docs/plugins/nixtla-cost-optimizer/04-USER-JOURNEY.md) | Step-by-step usage guide |
| [Technical Spec](000-docs/plugins/nixtla-cost-optimizer/05-TECHNICAL-SPEC.md) | Implementation details |
| [Status](000-docs/plugins/nixtla-cost-optimizer/06-STATUS.md) | Current state and roadmap |

💡 **Comprehensive Spec**: [All-in-one document](000-docs/009-AT-ARCH-plugin-01-nixtla-cost-optimizer.md) (59KB)

---

#### Migration Assistant

| | |
|---|---|
| **Status** | 📋 Specified |
| **Category** | Efficiency |
| **Impact** | Customer onboarding from weeks to hours |
| **Build Time** | 4-6 weeks |
| **Priority** | 🥈 High Value (Score: 3.8/5) |

**What It Does**

Automated migration tool that analyzes existing StatsForecast/MLForecast code and generates equivalent TimeGPT API calls, with side-by-side A/B testing, rollback safety, and accuracy validation. Reduces the "switching cost" friction that prevents TimeGPT adoption.

**Business Value**

- **Dramatically faster onboarding** (weeks → hours for customer migrations)
- **Reduces technical barrier** to switching from OSS to TimeGPT
- **Competitive displacement** against Prophet/ARIMA/StatsForecast
- **Risk mitigation** with automatic validation and rollback

**Documentation**

| Doc | Description |
|-----|-------------|
| [Business Case](000-docs/plugins/nixtla-migration-assistant/01-BUSINESS-CASE.md) | ROI and market opportunity |
| [PRD](000-docs/plugins/nixtla-migration-assistant/02-PRD.md) | Product requirements and success metrics |
| [Architecture](000-docs/plugins/nixtla-migration-assistant/03-ARCHITECTURE.md) | System design and integrations |
| [User Journey](000-docs/plugins/nixtla-migration-assistant/04-USER-JOURNEY.md) | Step-by-step usage guide |
| [Technical Spec](000-docs/plugins/nixtla-migration-assistant/05-TECHNICAL-SPEC.md) | Implementation details |
| [Status](000-docs/plugins/nixtla-migration-assistant/06-STATUS.md) | Current state and roadmap |

💡 **Comprehensive Spec**: [All-in-one document](000-docs/016-AT-ARCH-plugin-08-nixtla-migration-assistant.md) (37KB)

---

#### Forecast Explainer

| | |
|---|---|
| **Status** | 📋 Specified |
| **Category** | Efficiency |
| **Impact** | 40% reduction in support tickets |
| **Build Time** | 4-6 weeks |
| **Priority** | 🥈 High Value (Score: 3.8/5) |

**What It Does**

Post-hoc explainability tool that transforms TimeGPT's "black box" forecasts into transparent, stakeholder-friendly narratives with visual decomposition, SHAP values, confidence bounds, and plain-English explanations.

**Business Value**

- **40% fewer support tickets** through self-serve explanations
- **Enterprise sales enabler** (overcomes "black box" objections)
- **Builds trust** in forecasts with stakeholders
- **Risk committee approval** for regulated industries

**Documentation**

| Doc | Description |
|-----|-------------|
| [Business Case](000-docs/plugins/nixtla-forecast-explainer/01-BUSINESS-CASE.md) | ROI and market opportunity |
| [PRD](000-docs/plugins/nixtla-forecast-explainer/02-PRD.md) | Product requirements and success metrics |
| [Architecture](000-docs/plugins/nixtla-forecast-explainer/03-ARCHITECTURE.md) | System design and integrations |
| [User Journey](000-docs/plugins/nixtla-forecast-explainer/04-USER-JOURNEY.md) | Step-by-step usage guide |
| [Technical Spec](000-docs/plugins/nixtla-forecast-explainer/05-TECHNICAL-SPEC.md) | Implementation details |
| [Status](000-docs/plugins/nixtla-forecast-explainer/06-STATUS.md) | Current state and roadmap |

💡 **Comprehensive Spec**: [All-in-one document](000-docs/017-AT-ARCH-plugin-09-nixtla-forecast-explainer.md) (40KB)

---

**Business Growth** (Expand Your Market)

---

#### VS StatsForecast Benchmark

| | |
|---|---|
| **Status** | 📋 Specified |
| **Category** | Growth |
| **Impact** | Increase TimeGPT adoption through demonstrated superiority |
| **Build Time** | 3-4 weeks |
| **Priority** | 🥈 High Value (Score: 4.2/5) |

**What It Does**

Side-by-side comparison tool that benchmarks TimeGPT API against local StatsForecast OSS models, providing accuracy metrics (MAPE, RMSE, sMAPE) and comprehensive ROI calculations to justify the upgrade from free to paid forecasting.

**Business Value**

- **Data-driven sales conversations** with concrete accuracy comparisons
- **Demonstrates TimeGPT value** beyond "it's more accurate"
- **Content for marketing** (case studies, benchmarks, blog posts)
- **Natural extension** of existing Baseline Lab plugin

**Documentation**

| Doc | Description |
|-----|-------------|
| [Business Case](000-docs/plugins/nixtla-vs-statsforecast-benchmark/01-BUSINESS-CASE.md) | ROI and market opportunity |
| [PRD](000-docs/plugins/nixtla-vs-statsforecast-benchmark/02-PRD.md) | Product requirements and success metrics |
| [Architecture](000-docs/plugins/nixtla-vs-statsforecast-benchmark/03-ARCHITECTURE.md) | System design and integrations |
| [User Journey](000-docs/plugins/nixtla-vs-statsforecast-benchmark/04-USER-JOURNEY.md) | Step-by-step usage guide |
| [Technical Spec](000-docs/plugins/nixtla-vs-statsforecast-benchmark/05-TECHNICAL-SPEC.md) | Implementation details |
| [Status](000-docs/plugins/nixtla-vs-statsforecast-benchmark/06-STATUS.md) | Current state and roadmap |

💡 **Comprehensive Spec**: [All-in-one document](000-docs/010-AT-ARCH-plugin-02-nixtla-vs-statsforecast-benchmark.md) (23KB)

---

#### ROI Calculator

| | |
|---|---|
| **Status** | 📋 Specified |
| **Category** | Growth |
| **Impact** | Shorten sales cycles by 2-3 months |
| **Build Time** | 3-4 weeks |
| **Priority** | 🥇 Quick Win (Score: 4.4/5) |

**What It Does**

Interactive ROI calculator that compares total cost of ownership (TCO) for internal forecasting builds vs Nixtla TimeGPT API, generating executive-ready business cases for procurement approval.

**Business Value**

- **Accelerates sales** with concrete cost justification
- **Enables customer self-service** business case creation
- **Differentiates** from competitors who can't quantify value
- **Easiest to build** (low complexity, high impact)

**Documentation**

| Doc | Description |
|-----|-------------|
| [Business Case](000-docs/plugins/nixtla-roi-calculator/01-BUSINESS-CASE.md) | ROI and market opportunity |
| [PRD](000-docs/plugins/nixtla-roi-calculator/02-PRD.md) | Product requirements and success metrics |
| [Architecture](000-docs/plugins/nixtla-roi-calculator/03-ARCHITECTURE.md) | System design and integrations |
| [User Journey](000-docs/plugins/nixtla-roi-calculator/04-USER-JOURNEY.md) | Step-by-step usage guide |
| [Technical Spec](000-docs/plugins/nixtla-roi-calculator/05-TECHNICAL-SPEC.md) | Implementation details |
| [Status](000-docs/plugins/nixtla-roi-calculator/06-STATUS.md) | Current state and roadmap |

💡 **Comprehensive Spec**: [All-in-one document](000-docs/011-AT-ARCH-plugin-03-nixtla-roi-calculator.md) (22KB)

---

#### Airflow Operator

| | |
|---|---|
| **Status** | 📋 Specified |
| **Category** | Growth |
| **Impact** | Opens enterprise data platform market |
| **Build Time** | 6-8 weeks |
| **Priority** | 🥈 Strategic (Score: 4.2/5) |

**What It Does**

Production-grade Apache Airflow operator (`NixtlaForecastOperator`) that natively integrates Nixtla TimeGPT forecasting into DAGs with automatic retry logic, authentication handling, and dependency management.

**Business Value**

- **Reaches enterprise data teams** (huge addressable market)
- **Fits existing workflows** (no rip-and-replace)
- **Reduces integration friction** (eliminates "glue code tax")
- **Production-grade reliability** with Airflow's retry/monitoring

**Documentation**

| Doc | Description |
|-----|-------------|
| [Business Case](000-docs/plugins/nixtla-airflow-operator/01-BUSINESS-CASE.md) | ROI and market opportunity |
| [PRD](000-docs/plugins/nixtla-airflow-operator/02-PRD.md) | Product requirements and success metrics |
| [Architecture](000-docs/plugins/nixtla-airflow-operator/03-ARCHITECTURE.md) | System design and integrations |
| [User Journey](000-docs/plugins/nixtla-airflow-operator/04-USER-JOURNEY.md) | Step-by-step usage guide |
| [Technical Spec](000-docs/plugins/nixtla-airflow-operator/05-TECHNICAL-SPEC.md) | Implementation details |
| [Status](000-docs/plugins/nixtla-airflow-operator/06-STATUS.md) | Current state and roadmap |

💡 **Comprehensive Spec**: [All-in-one document](000-docs/012-AT-ARCH-plugin-04-nixtla-airflow-operator.md) (19KB)

---

#### dbt Package

| | |
|---|---|
| **Status** | 📋 Specified |
| **Category** | Growth |
| **Impact** | Expand into analytics engineering market |
| **Build Time** | 6-8 weeks |
| **Priority** | 🥉 Strategic (Score: 3.6/5) |

**What It Does**

Native dbt package that treats forecasting as a data transformation step, allowing SQL analysts to generate Nixtla forecasts using `{{ nixtla_forecast(...) }}` macros directly in dbt models.

**Business Value**

- **Reaches analytics engineers** (large, underserved market)
- **SQL-native interface** (no Python required)
- **Forecasting in transformation layer** (fits modern data stack)
- **Self-serve enablement** for analysts

**Documentation**

| Doc | Description |
|-----|-------------|
| [Business Case](000-docs/plugins/nixtla-dbt-package/01-BUSINESS-CASE.md) | ROI and market opportunity |
| [PRD](000-docs/plugins/nixtla-dbt-package/02-PRD.md) | Product requirements and success metrics |
| [Architecture](000-docs/plugins/nixtla-dbt-package/03-ARCHITECTURE.md) | System design and integrations |
| [User Journey](000-docs/plugins/nixtla-dbt-package/04-USER-JOURNEY.md) | Step-by-step usage guide |
| [Technical Spec](000-docs/plugins/nixtla-dbt-package/05-TECHNICAL-SPEC.md) | Implementation details |
| [Status](000-docs/plugins/nixtla-dbt-package/06-STATUS.md) | Current state and roadmap |

💡 **Comprehensive Spec**: [All-in-one document](000-docs/013-AT-ARCH-plugin-05-nixtla-dbt-package.md) (12KB)

---

#### Snowflake Adapter

| | |
|---|---|
| **Status** | 📋 Specified |
| **Category** | Growth |
| **Impact** | 10x larger enterprise contracts (Fortune 500) |
| **Build Time** | 8-10 weeks |
| **Priority** | 🥉 Strategic (Score: 3.8/5) |

**What It Does**

Claude Code plugin that wraps Nixtla's existing Snowflake Native App integration, providing one-command SQL-native forecasting with automatic setup and error handling directly in Snowflake.

**Business Value**

- **Unlocks Fortune 500** with Snowflake-first strategies
- **Data never leaves customer's Snowflake** (compliance win)
- **Premium pricing justified** by enterprise features
- **Makes existing integration discoverable** and easy

**Documentation**

| Doc | Description |
|-----|-------------|
| [Business Case](000-docs/plugins/nixtla-snowflake-adapter/01-BUSINESS-CASE.md) | ROI and market opportunity |
| [PRD](000-docs/plugins/nixtla-snowflake-adapter/02-PRD.md) | Product requirements and success metrics |
| [Architecture](000-docs/plugins/nixtla-snowflake-adapter/03-ARCHITECTURE.md) | System design and integrations |
| [User Journey](000-docs/plugins/nixtla-snowflake-adapter/04-USER-JOURNEY.md) | Step-by-step usage guide |
| [Technical Spec](000-docs/plugins/nixtla-snowflake-adapter/05-TECHNICAL-SPEC.md) | Implementation details |
| [Status](000-docs/plugins/nixtla-snowflake-adapter/06-STATUS.md) | Current state and roadmap |

💡 **Comprehensive Spec**: [All-in-one document](000-docs/014-AT-ARCH-plugin-06-nixtla-snowflake-adapter.md) (12KB)

---

#### Anomaly Streaming Monitor

| | |
|---|---|
| **Status** | 📋 Specified |
| **Category** | Growth |
| **Impact** | Opens real-time monitoring market |
| **Build Time** | 8-10 weeks |
| **Priority** | 🥉 Strategic (Score: 3.5/5) |

**What It Does**

Real-time streaming anomaly detection plugin that processes Kafka/Kinesis streams with sub-second latency, using Nixtla's TimeGPT for anomaly detection with automatic alerting and dashboard visualization.

**Business Value**

- **Opens real-time use cases** (fraud, IoT, operations)
- **Differentiation from batch-only** competitors
- **Premium pricing** for streaming capabilities
- **Builds production trust** in TimeGPT

**Documentation**

| Doc | Description |
|-----|-------------|
| [Business Case](000-docs/plugins/nixtla-anomaly-streaming-monitor/01-BUSINESS-CASE.md) | ROI and market opportunity |
| [PRD](000-docs/plugins/nixtla-anomaly-streaming-monitor/02-PRD.md) | Product requirements and success metrics |
| [Architecture](000-docs/plugins/nixtla-anomaly-streaming-monitor/03-ARCHITECTURE.md) | System design and integrations |
| [User Journey](000-docs/plugins/nixtla-anomaly-streaming-monitor/04-USER-JOURNEY.md) | Step-by-step usage guide |
| [Technical Spec](000-docs/plugins/nixtla-anomaly-streaming-monitor/05-TECHNICAL-SPEC.md) | Implementation details |
| [Status](000-docs/plugins/nixtla-anomaly-streaming-monitor/06-STATUS.md) | Current state and roadmap |

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
git clone https://github.com/jeremylongshore/claude-code-plugins-nixtla.git
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

**Detailed architecture**: See [individual plugin docs](000-docs/plugins/)

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

| Option | Scope | Timeline | Risk |
|--------|-------|----------|------|
| 🧪 **Evaluate** | Use working demos for 30 days | No commitment | None |
| 🎯 **Pilot** | 1 plugin to production | 4-6 weeks | Low |
| 🚀 **Platform** | 3+ plugins | 12-16 weeks | Medium |

### Recommended Quick Wins

**For Pilot** (Choose 1):
- **Cost Optimizer** (Score: 4.6/5) - Immediate ROI, low risk
- **ROI Calculator** (Score: 4.4/5) - Easiest to build, enables sales

**For Platform** (Choose 3):
- **Bundle A**: Cost Optimizer + ROI Calculator + Airflow Operator (quick wins + market expansion)
- **Bundle B**: Cost Optimizer + Nixtla vs Benchmark + Migration Assistant (strategic differentiation)

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
- `000-docs/plugins/<slug>/` with all 6 doc templates
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

## What Intent Solutions Brings

- **Speed**: 1 working plugin in 8 weeks (Baseline Lab)
- **Quality**: 70+ technical documents, full CI/CD, test coverage
- **Business Thinking**: Plugins designed for ROI, not just tech demos
- **Claude Code Expertise**: Deep integration with Claude ecosystem (253+ plugins in marketplace)

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
