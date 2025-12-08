# Comprehensive Learning Guide: Nixtla Plugins & Skills

**Document ID**: 063-OD-GUID-comprehensive-plugins-skills-learning-guide
**Version**: 2.0.0
**Created**: 2025-12-08
**Updated**: 2025-12-08
**Audience**: Developers, DevOps, Technical Stakeholders

---

## Table of Contents

1. [Understanding the Architecture](#understanding-the-architecture)
2. [Plugins Deep Dive](#plugins-deep-dive)
   - [Plugin 1: Nixtla Baseline Lab](#plugin-1-nixtla-baseline-lab)
   - [Plugin 2: Nixtla BigQuery Forecaster](#plugin-2-nixtla-bigquery-forecaster)
   - [Plugin 3: Nixtla Search-to-Slack](#plugin-3-nixtla-search-to-slack)
3. [Production Skills (8)](#production-skills-8)
4. [Generated Skills - Core Forecasting (5)](#generated-skills---core-forecasting-5)
5. [Generated Skills - Prediction Markets (10)](#generated-skills---prediction-markets-10)
6. [Generated Skills - Live/Retroactive (6)](#generated-skills---liveretroactive-6)
7. [MCP Server Pattern](#mcp-server-pattern)
8. [How Skills Activate](#how-skills-activate)
9. [Integration Patterns](#integration-patterns)
10. [Reference Documentation](#reference-documentation)

---

## Understanding the Architecture

### What's the Difference Between Plugins and Skills?

| Aspect | Plugins | Skills |
|--------|---------|--------|
| **What they are** | Complete applications with backends, servers, and tools | AI behavior modifiers (prompts that teach Claude) |
| **Where they live** | `plugins/plugin-name/` | `.claude/skills/skill-name/SKILL.md` |
| **How they work** | Run actual code via MCP servers | Inject instructions into Claude's system prompt |
| **Persistence** | Installed per-project, runs server processes | Markdown files that persist across sessions |
| **Complexity** | High (Python backends, tests, configs) | Low (just markdown with YAML frontmatter) |
| **API Key needed** | Depends on plugin functionality | Only if skill generates code that uses APIs |

### The Three-Layer System

```
┌─────────────────────────────────────────────────────────────────┐
│                       USER INTERFACE                             │
│   • Slash commands: /nixtla-baseline-m4                         │
│   • Natural language: "Forecast my sales data"                   │
└─────────────────────────┬───────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────────┐
│                     LAYER 1: SKILLS                              │
│   • Transform Claude's behavior                                  │
│   • Auto-activate on context detection                          │
│   • 8 production + 21 generated skills                          │
│   • Location: .claude/skills/nixtla-*/SKILL.md                  │
└─────────────────────────┬───────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────────┐
│                     LAYER 2: PLUGINS                             │
│   • Full applications with MCP servers                          │
│   • Expose tools: run_baselines, generate_report, etc.          │
│   • 3 working plugins                                           │
│   • Location: plugins/*/                                        │
└─────────────────────────┬───────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────────┐
│                 LAYER 3: SLASH COMMANDS                          │
│   • User-invoked commands                                        │
│   • Trigger specific workflows                                   │
│   • Location: plugins/*/commands/*.md                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Plugins Deep Dive

We have **3 working plugins**, each demonstrating different patterns.

---

### Plugin 1: Nixtla Baseline Lab

**Location**: `plugins/nixtla-baseline-lab/`
**Status**: Production-ready flagship plugin

#### Purpose

Runs Nixtla's statsforecast baseline models (SeasonalNaive, AutoETS, AutoTheta) on benchmark datasets directly inside Claude Code conversations. This is the **flagship plugin** demonstrating the full Claude Code plugin architecture.

#### Why It Exists

1. **Proves Claude can execute forecasting workflows** - Not just generate code, but actually run models
2. **Reference implementation** - Shows all plugin components working together
3. **Reproducible benchmarks** - Same code runs locally and in CI
4. **Zero API cost** - Uses open-source statsforecast, no TimeGPT required

#### Directory Structure

```
plugins/nixtla-baseline-lab/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest (version, author, entry points)
├── .mcp.json                 # MCP server configuration
├── commands/
│   ├── nixtla-baseline-m4.md      # /nixtla-baseline-m4 command
│   └── nixtla-baseline-setup.md   # /nixtla-baseline-setup command
├── agents/
│   └── nixtla-baseline-analyst/   # AI analyst subagent
├── skills/
│   └── nixtla-baseline-review/    # Result interpretation skill
├── scripts/
│   ├── nixtla_baseline_mcp.py     # MCP server (THE CORE - 1777 lines)
│   ├── setup_nixtla_env.sh        # Environment setup
│   └── requirements.txt           # Python dependencies
├── tests/
│   └── run_baseline_m4_smoke.py   # Golden task test harness
└── README.md                       # 1200 lines of documentation
```

#### MCP Server Tools (4 Tools)

The MCP server (`scripts/nixtla_baseline_mcp.py`) exposes these tools:

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `run_baselines` | Execute statsforecast models on M4/CSV data | `horizon`, `series_limit`, `models`, `demo_preset` |
| `get_nixtla_compatibility_info` | Return library versions for reproducibility | None |
| `generate_benchmark_report` | Create markdown report from metrics CSV | `metrics_csv_path`, `dataset_label` |
| `generate_github_issue_draft` | Create GitHub issue with repro info | `issue_type`, `metrics_csv_path` |

#### run_baselines Tool Parameters

```python
{
    "horizon": 14,              # Forecast horizon in days (1-60)
    "series_limit": 50,         # Max series to process (1-500)
    "output_dir": "nixtla_baseline_m4",  # Output directory
    "enable_plots": False,      # Generate PNG visualizations
    "dataset_type": "m4",       # 'm4' or 'csv'
    "csv_path": None,           # Path to custom CSV (if dataset_type='csv')
    "models": ["SeasonalNaive", "AutoETS", "AutoTheta"],
    "freq": "D",                # Frequency: D, M, H, W
    "season_length": 7,         # Seasonal period
    "demo_preset": None,        # 'm4_daily_small' for quick demo
    "generate_repro_bundle": True,  # Write compat_info.json
    "include_timegpt": False,   # Enable TimeGPT comparison
    "timegpt_max_series": 5     # Limit TimeGPT series (cost control)
}
```

#### Demo Preset (90-second demo)

```bash
# Run this command in Claude Code:
/nixtla-baseline-m4 demo_preset=m4_daily_small

# What happens:
# - dataset_type = "m4"
# - models = ["SeasonalNaive", "AutoETS", "AutoTheta"]
# - series_limit = 5
# - horizon = 7
# - Runs in ~90 seconds, fully offline
```

#### Output Files Generated

| File | Purpose |
|------|---------|
| `results_M4_Daily_h7.csv` | Per-series metrics (sMAPE, MASE) |
| `summary_M4_Daily_h7.txt` | Human-readable summary |
| `compat_info.json` | Library versions for reproducibility |
| `run_manifest.json` | Run parameters for reproducibility |
| `benchmark_report_*.md` | Nixtla-style benchmark report |

#### Metrics Explained

| Metric | Formula | Good Value |
|--------|---------|------------|
| **sMAPE** | 100 × mean(\|actual - pred\| / ((actual + pred)/2)) | < 10% (excellent), < 20% (good) |
| **MASE** | MAE / MAE_naive_seasonal | < 1.0 (beats naive), < 0.5 (excellent) |

#### Example Results

From actual M4 Daily run:

| Model | Avg sMAPE | Avg MASE | Notes |
|-------|-----------|----------|-------|
| AutoETS | **0.77%** | **0.422** | Winner |
| AutoTheta | 0.85% | 0.454 | Close second |
| SeasonalNaive | 1.49% | 0.898 | Baseline |

**Reference**: `plugins/nixtla-baseline-lab/README.md` (1200 lines)

---

### Plugin 2: Nixtla BigQuery Forecaster

**Location**: `plugins/nixtla-bigquery-forecaster/`
**Status**: Working (requires GCP)

#### Purpose

Run Nixtla statsforecast models on BigQuery data via Google Cloud Functions. Demonstrates **enterprise cloud integration**.

#### Why It Exists

1. **Shows Nixtla + GCP integration** - Production-ready pattern
2. **Handles massive datasets** - Tested with 100K+ rows
3. **Serverless deployment** - Cloud Functions auto-scale
4. **Real-world demo** - Uses public Chicago taxi data (200M+ rows)

#### Directory Structure

```
plugins/nixtla-bigquery-forecaster/
├── src/
│   ├── main.py                  # Cloud Function entry point
│   ├── bigquery_connector.py    # BigQuery data reader/writer
│   └── forecaster.py            # Nixtla statsforecast wrapper
├── scripts/                     # Deployment scripts
├── 000-docs/
│   └── 003-AT-ARCH-plugin-architecture.md
├── requirements.txt             # Python dependencies
└── README.md
```

#### How It Works

**Step 1: Deploy Cloud Function**
```bash
gcloud functions deploy nixtla-bigquery-forecaster \
  --runtime python310 \
  --trigger-http \
  --entry-point forecast_handler
```

**Step 2: Send HTTP request**
```bash
curl -X POST "https://YOUR-FUNCTION-URL" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "bigquery-public-data",
    "dataset": "chicago_taxi_trips",
    "table": "taxi_trips",
    "timestamp_col": "trip_start_timestamp",
    "value_col": "trip_total",
    "group_by": "payment_type",
    "horizon": 7
  }'
```

**Step 3: Get results**
```json
{
  "status": "success",
  "metadata": {
    "rows_read": 210,
    "unique_series": 7,
    "forecast_points_generated": 49
  },
  "forecasts": [
    {"unique_id": "Cash", "ds": "2023-02-01", "AutoETS": 69918.06}
  ]
}
```

#### Environment Variables Required

| Variable | Purpose |
|----------|---------|
| `PROJECT_ID` | GCP project ID |
| `LOCATION` | GCP region (default: us-central1) |

#### Key Learnings

- statsforecast handles 100K+ rows efficiently
- BigQuery public datasets are excellent for demos
- Cost: ~$0.01 per forecast run

**Reference**: `plugins/nixtla-bigquery-forecaster/README.md`

---

### Plugin 3: Nixtla Search-to-Slack

**Location**: `plugins/nixtla-search-to-slack/`
**Status**: MVP

#### Purpose

Find Nixtla-related content across web/GitHub, create AI summaries, post to Slack. Demonstrates **content curation workflow**.

#### Why It Exists

1. **Construction kit** - Example for learning/adaptation
2. **Reference implementation** - Search → AI → Slack pattern
3. **Community tool** - Keeps team updated on Nixtla ecosystem
4. **MVP demonstration** - Minimal features, maximum learning

#### Directory Structure

```
plugins/nixtla-search-to-slack/
├── src/nixtla_search_to_slack/
│   ├── main.py                 # Entry point
│   ├── search_orchestrator.py  # Search coordination
│   ├── content_aggregator.py   # Deduplication
│   ├── ai_curator.py           # AI summaries
│   └── slack_publisher.py      # Slack posting
├── config/
│   ├── sources.yaml            # Search source config
│   └── topics.yaml             # Topic definitions
├── tests/                      # Unit tests
└── README.md
```

#### Workflow Pipeline

```
1. Define topics (config/topics.yaml)
   │
   ▼
2. Search sources (SerpAPI, GitHub)
   │
   ▼
3. Aggregate (deduplicate by URL)
   │
   ▼
4. Curate (AI summaries)
   │
   ▼
5. Publish (Slack channel)
```

#### Configuration Example

```yaml
# config/topics.yaml
topics:
  nixtla-core:
    name: "Nixtla Core Updates"
    keywords: [TimeGPT, StatsForecast, MLForecast]
    sources: [web, github]
    slack_channel: "#nixtla-updates"
```

#### Environment Variables Required

| Variable | Purpose |
|----------|---------|
| `SERPAPI_API_KEY` | Web search API |
| `SLACK_BOT_TOKEN` | Slack posting |
| `OPENAI_API_KEY` | AI summaries (optional) |

#### Current Limitations (MVP)

- Limited to 2 search sources (web + GitHub)
- Basic string matching deduplication
- No persistence (may re-send duplicates)
- Single-threaded, no queue system

**Reference**: `plugins/nixtla-search-to-slack/README.md`, `SETUP_GUIDE.md`

---

## Production Skills (8)

Located in `skills-pack/.claude/skills/`:

### 1. nixtla-timegpt-lab

**Purpose**: Expert forecasting using TimeGPT/StatsForecast

**Triggers**: "forecast my data", "predict sales", "time series forecast"

**What It Does**:
- Detects Nixtla libraries in the repo
- Biases all suggestions toward Nixtla stacks
- Generates Nixtla-compatible code
- References official documentation

**Model Hierarchy** (always suggests in this order):
```python
# 1. Baseline models (StatsForecast) - Always first
from statsforecast.models import SeasonalNaive, AutoARIMA, AutoETS, AutoTheta

# 2. ML models (MLForecast) - For feature engineering
from mlforecast import MLForecast

# 3. TimeGPT - Foundation model (if API key configured)
from nixtla import NixtlaClient
```

**Location**: `skills-pack/.claude/skills/nixtla-timegpt-lab/SKILL.md`

---

### 2. nixtla-experiment-architect

**Purpose**: Scaffold production-ready forecasting experiments

**Triggers**: "design experiment", "setup forecasting project", "create forecasting configs"

**What It Does**:
- Creates standardized config files (YAML)
- Generates experiment directory structure
- Defines dataset, model selections, metrics
- Outputs ready-to-run pipeline scripts

**Output Structure**:
```
experiment/
├── config.yaml       # Main experiment config
├── data.yaml        # Data loading config
├── models.yaml      # Model selection config
├── pipeline.py      # Python script to run
└── README.md        # Instructions
```

**Location**: `skills-pack/.claude/skills/nixtla-experiment-architect/SKILL.md`

---

### 3. nixtla-schema-mapper

**Purpose**: Transform data to Nixtla format (unique_id, ds, y)

**Triggers**: "convert to Nixtla format", "Nixtla data schema", "prepare time series data"

**What It Does**:
- Analyzes input data (first 100 rows)
- Infers column mappings automatically
- Generates transformation code
- Documents schema contract

**Example Transformation**:
```
Input:                      Output:
store_id,date,sales   →    unique_id,ds,y
A1,2023-01-01,100     →    A1,2023-01-01,100
```

**Location**: `skills-pack/.claude/skills/nixtla-schema-mapper/SKILL.md`

---

### 4. nixtla-timegpt-finetune-lab

**Purpose**: Fine-tune TimeGPT on custom datasets

**Triggers**: "finetune TimeGPT", "train TimeGPT", "adapt TimeGPT"

**What It Does**:
- Guides through data preprocessing
- Configures fine-tuning parameters
- Executes fine-tuning workflow
- Evaluates and saves model

**Location**: `skills-pack/.claude/skills/nixtla-timegpt-finetune-lab/SKILL.md`

---

### 5. nixtla-prod-pipeline-generator

**Purpose**: Generate Airflow/Prefect production pipelines

**Triggers**: "productionize model", "create pipeline", "deploy forecasting"

**What It Does**:
- Reads experiment configuration
- Generates Airflow DAGs or Prefect flows
- Creates deployment configuration
- Outputs ready-to-deploy code

**Location**: `skills-pack/.claude/skills/nixtla-prod-pipeline-generator/SKILL.md`

---

### 6. nixtla-usage-optimizer

**Purpose**: Audit and optimize TimeGPT API costs

**Triggers**: "optimize Nixtla costs", "analyze TimeGPT usage", "reduce API expenses"

**What It Does**:
- Reads API logs
- Identifies usage patterns
- Recommends cost optimizations
- Estimates potential savings

**Location**: `skills-pack/.claude/skills/nixtla-usage-optimizer/SKILL.md`

---

### 7. nixtla-skills-index

**Purpose**: Directory of all installed Nixtla skills

**Triggers**: "list skills", "what skills available"

**What It Does**:
- Scans `.claude/skills/nixtla-*/`
- Reads skill frontmatter
- Outputs formatted index
- Guides skill selection

**Location**: `skills-pack/.claude/skills/nixtla-skills-index/SKILL.md`

---

### 8. nixtla-skills-bootstrap

**Purpose**: Install/update skills in projects

**Triggers**: "install Nixtla skills", "update skills", "setup Nixtla"

**What It Does**:
- Guides init vs update decision
- Checks CLI availability
- Runs nixtla-skills command
- Lists installed skills

**Location**: `skills-pack/.claude/skills/nixtla-skills-bootstrap/SKILL.md`

---

## Generated Skills - Core Forecasting (5)

Located in `000-docs/planned-skills/core-forecasting/`:

---

### 1. nixtla-anomaly-detector

**Purpose**: Detect outliers, level shifts, and trend breaks in time series

**Triggers**: "detect anomalies", "find outliers", "anomaly detection"

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install nixtla pandas
```

**Workflow**:
```
Step 1: Load data (CSV with unique_id, ds, y)
Step 2: Configure detection sensitivity
Step 3: Execute: python scripts/detect_anomalies.py --input data.csv
Step 4: Save anomaly CSV and visualization
```

**Output Files**:
- `anomalies.csv` - Detected anomalies with timestamps and type
- `plot.png` - Visualization with anomalies highlighted
- `summary.txt` - Count and types summary

**Example**:
```
Input:
unique_id,ds,y
website_1,2024-01-01,1000
website_1,2024-01-02,1050
website_1,2024-01-03,300   # Outlier!

Output:
unique_id,ds,anomaly_type
website_1,2024-01-03,outlier
```

**Error Handling**:
| Error | Solution |
|-------|----------|
| `NIXTLA_TIMEGPT_API_KEY not set` | `export NIXTLA_TIMEGPT_API_KEY=your_key` |
| `Invalid input data format` | Ensure CSV has unique_id, ds, y columns |
| `No anomalies detected` | Lower sensitivity parameter |

**Location**: `000-docs/planned-skills/core-forecasting/nixtla-anomaly-detector/SKILL.md`

---

### 2. nixtla-exogenous-integrator

**Purpose**: Add external variables (holidays, weather, events) to forecasts

**Triggers**: "include holidays", "add weather data", "integrate events"

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install nixtla pandas
```

**Workflow**:
```
Step 1: Read historical CSV and exogenous CSVs
Step 2: Merge on 'ds' column
Step 3: Configure TimeGPT API call
Step 4: Execute: python scripts/integrate_exogenous.py --input data.csv --exogenous holidays.csv --horizon 14
```

**Example**:
```
Input (data.csv):
unique_id,ds,y
store_1,2024-01-01,100
store_1,2024-01-02,120

Input (holidays.csv):
ds,holiday
2024-01-01,New Year's Day
2024-02-14,Valentine's Day

Output:
unique_id,ds,TimeGPT,TimeGPT-lo-90,TimeGPT-hi-90
store_1,2024-01-03,130,115,145
```

**Error Handling**:
| Error | Solution |
|-------|----------|
| `Exogenous data missing 'ds' column` | Rename date column to 'ds' |
| `Mismatch in date range` | Ensure exogenous covers full period |
| `NaN values in forecast horizon` | Provide future values for exogenous |

**Location**: `000-docs/planned-skills/core-forecasting/nixtla-exogenous-integrator/SKILL.md`

---

### 3. nixtla-uncertainty-quantifier

**Purpose**: Generate prediction intervals and confidence bands

**Triggers**: "quantify uncertainty", "generate prediction intervals", "confidence bands"

**Environment**: `NIXTLA_TIMEGPT_API_KEY` (optional)

**Packages**:
```bash
pip install nixtla pandas statsforecast
```

**Workflow**:
```
Step 1: Load data and generate point forecasts
Step 2: Configure confidence level (90%, 95%)
Step 3: Execute: python scripts/uncertainty.py --input forecast.csv --confidence 0.90 --method quantile
Step 4: Save forecast with intervals
```

**Methods**:
- `quantile` - Quantile regression
- `jackknife+` - Jackknife+ conformal prediction

**Output**:
```
unique_id,ds,TimeGPT,lower_bound_90,upper_bound_90
store_1,2024-01-01,100,80,120
store_1,2024-01-02,120,100,140
```

**Location**: `000-docs/planned-skills/core-forecasting/nixtla-uncertainty-quantifier/SKILL.md`

---

### 4. nixtla-cross-validator

**Purpose**: Backtest models using time series cross-validation

**Triggers**: "cross validate time series", "evaluate forecasting model", "time series backtesting"

**Environment**: `NIXTLA_TIMEGPT_API_KEY` (if using TimeGPT)

**Packages**:
```bash
pip install nixtla pandas statsforecast
```

**Workflow**:
```
Step 1: Read time series CSV
Step 2: Configure: window size, step size, folds
Step 3: Execute: python scripts/cross_validate.py --input data.csv --model timegpt --window 30 --folds 3
Step 4: Calculate MAE, RMSE across folds
```

**Output**:
- `cv_results.csv` - Per-fold results
- `metrics.json` - Overall metrics
- `plots/` - Actual vs predicted per fold

**Example Metrics Output**:
```json
{
  "MAE": 5.2,
  "RMSE": 7.1
}
```

**Location**: `000-docs/planned-skills/core-forecasting/nixtla-cross-validator/SKILL.md`

---

### 5. nixtla-timegpt2-migrator

**Purpose**: Migrate from TimeGPT-1 to TimeGPT-2

**Triggers**: "migrate to TimeGPT-2", "upgrade TimeGPT", "TimeGPT compatibility"

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install nixtla pandas
```

**Workflow**:
```
Step 1: Analyze codebase with Glob and Grep
Step 2: Run compatibility checker: python scripts/compatibility_check.py
Step 3: Generate migration plan
Step 4: Update configuration files
```

**Output**:
- `migration_report.txt` - Required changes summary
- `updated_codebase/` - Modified source files
- `timegpt2_config.yaml` - New configuration

**Location**: `000-docs/planned-skills/core-forecasting/nixtla-timegpt2-migrator/SKILL.md`

---

## Generated Skills - Prediction Markets (10)

Located in `000-docs/planned-skills/prediction-markets/`:

---

### 1. nixtla-polymarket-analyst

**Purpose**: Forecast Polymarket contract prices

**Triggers**: "Polymarket analysis", "predict contract odds", "forecast Polymarket"

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install nixtla pandas requests
```

**Workflow**:
```
Step 1: Fetch contract data from Polymarket API
Step 2: Transform to time series (ds, y)
Step 3: Execute: python scripts/polymarket_forecast.py --contract_id <id> --horizon 14
Step 4: Generate forecast CSV and visualization
```

**Output**:
- `forecast.csv` - Predictions with confidence intervals
- `plot.png` - Actual vs predicted visualization
- `metadata.json` - Contract metadata

**Location**: `000-docs/planned-skills/prediction-markets/nixtla-polymarket-analyst/SKILL.md`

---

### 2. nixtla-arbitrage-detector

**Purpose**: Find pricing inefficiencies between Polymarket and Kalshi

**Triggers**: "find arbitrage", "detect market inefficiencies", "compare Polymarket and Kalshi"

**Environment**: None required

**Packages**:
```bash
pip install requests
```

**Workflow**:
```
Step 1: Fetch data from both platforms
Step 2: Analyze matching events
Step 3: Generate report
Step 4: Output arbitrage opportunities
```

**Output**:
```
Event,Platform Buy,Platform Sell,Profit
Event A,Polymarket Yes,Kalshi Yes,0.09
```

**Location**: `000-docs/planned-skills/prediction-markets/nixtla-arbitrage-detector/SKILL.md`

---

### 3. nixtla-contract-schema-mapper

**Purpose**: Transform prediction market data to Nixtla format

**Triggers**: "convert to Nixtla format", "Nixtla schema", "transform data"

**Packages**:
```bash
pip install pandas
```

**Workflow**:
```
Step 1: Load prediction market CSV
Step 2: Identify ID, date, target columns
Step 3: Execute: python scripts/transform.py --input input.csv --id_col id_column --date_col date_column --target_col target_column
Step 4: Output nixtla_data.csv
```

**Example**:
```
Input:                          Output:
contract_id,date,volume   →    unique_id,ds,y
contract_1,2024-01-01,100 →    contract_1,2024-01-01,100
```

**Location**: `000-docs/planned-skills/prediction-markets/nixtla-contract-schema-mapper/SKILL.md`

---

### 4. nixtla-batch-forecaster

**Purpose**: Forecast multiple contracts in parallel batches

**Triggers**: "batch forecast", "portfolio forecast", "parallel forecasting"

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install nixtla pandas
```

**Workflow**:
```
Step 1: Read input CSV with multiple series
Step 2: Configure horizon and batch size
Step 3: Execute: python scripts/batch_forecast.py --input data.csv --horizon 30 --batch_size 20
Step 4: Generate individual + aggregated forecasts
```

**Output**:
- `forecasts/{unique_id}.csv` - Individual forecasts
- `aggregated_forecast.csv` - Portfolio-level forecast
- `summary.json` - Batch processing summary

**Location**: `000-docs/planned-skills/prediction-markets/nixtla-batch-forecaster/SKILL.md`

---

### 5. nixtla-event-impact-modeler

**Purpose**: Model how events affect contract prices

**Triggers**: "event impact analysis", "model event effects", "quantify event impact"

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install nixtla pandas causalimpact
```

**Workflow**:
```
Step 1: Read price data and event details
Step 2: Define event periods and causal model
Step 3: Execute: python scripts/event_impact.py --prices prices.csv --events events.csv
Step 4: Generate impact results and visualization
```

**Output**:
- `impact_results.csv` - Quantified impact per event
- `adjusted_forecast.csv` - Forecast with events removed
- `impact_plot.png` - Visualization of impact

**Location**: `000-docs/planned-skills/prediction-markets/nixtla-event-impact-modeler/SKILL.md`

---

### 6. nixtla-forecast-validator

**Purpose**: Validate forecast quality metrics

**Triggers**: "validate forecast", "check forecast quality", "assess forecast metrics"

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install pandas
```

**Workflow**:
```
Step 1: Load historical and current metrics (MASE, sMAPE)
Step 2: Configure validation thresholds
Step 3: Execute: python scripts/validate_forecast.py --historical historical_metrics.csv --current current_metrics.csv
Step 4: Generate validation report and alerts
```

**Output**:
- `validation_report.txt` - Summary of validation results
- `metrics_comparison.csv` - Historical vs current comparison
- `alert.log` - Alerts if degradation detected

**Example Alert**:
```
WARNING: Significant increase in MASE detected for model_A.
```

**Location**: `000-docs/planned-skills/prediction-markets/nixtla-forecast-validator/SKILL.md`

---

### 7. nixtla-model-selector

**Purpose**: Auto-select best model (StatsForecast vs TimeGPT)

**Triggers**: "auto-select model", "choose best model", "model selection"

**Environment**: `NIXTLA_TIMEGPT_API_KEY` (if TimeGPT selected)

**Packages**:
```bash
pip install statsforecast nixtla pandas
```

**Workflow**:
```
Step 1: Load and analyze data characteristics
Step 2: Determine best model based on length, frequency, seasonality, outliers
Step 3: Execute selected model
Step 4: Generate forecast and selection explanation
```

**Selection Logic**:
- Short, seasonal data → StatsForecast
- Long, non-seasonal data → TimeGPT

**Output**:
- `forecast.csv` - Predictions from selected model
- `model_selection.txt` - Explanation of why model was chosen

**Location**: `000-docs/planned-skills/prediction-markets/nixtla-model-selector/SKILL.md`

---

### 8. nixtla-liquidity-forecaster

**Purpose**: Forecast orderbook depth and spreads

**Triggers**: "forecast liquidity", "predict orderbook", "estimate depth"

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install nixtla pandas requests
```

**Workflow**:
```
Step 1: Fetch historical orderbook data from Polymarket API
Step 2: Preprocess for TimeGPT input
Step 3: Execute: python scripts/liquidity_forecast.py --market_id polymarket_market_id --horizon 12
Step 4: Generate depth and spread forecasts
```

**Output**:
- `depth_forecast.csv` - Predicted orderbook depth
- `spread_forecast.csv` - Predicted bid-ask spread
- `report.txt` - Forecasting summary

**Location**: `000-docs/planned-skills/prediction-markets/nixtla-liquidity-forecaster/SKILL.md`

---

### 9. nixtla-correlation-mapper

**Purpose**: Analyze multi-contract correlations for hedging

**Triggers**: "analyze correlations", "suggest hedge", "portfolio risk assessment"

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install pandas numpy scipy
```

**Workflow**:
```
Step 1: Load contract data (multiple series)
Step 2: Execute: python scripts/correlation_analysis.py --input contracts.csv
Step 3: Calculate correlation matrix
Step 4: Generate hedge recommendations
```

**Output**:
- `correlation_matrix.csv` - Correlations between contracts
- `hedge_recommendations.csv` - Suggested hedge ratios
- `report.txt` - Analysis summary

**Example**:
```
Gold-Silver correlation: 0.85
Recommended hedge ratio: 0.73
```

**Location**: `000-docs/planned-skills/prediction-markets/nixtla-correlation-mapper/SKILL.md`

---

### 10. nixtla-market-risk-analyzer

**Purpose**: Calculate VaR, volatility, drawdown, position sizing

**Triggers**: "analyze market risk", "calculate portfolio risk", "determine position size"

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install nixtla pandas numpy
```

**Workflow**:
```
Step 1: Load historical price data (date, price columns)
Step 2: Calculate VaR, volatility, drawdown
Step 3: Use TimeGPT for volatility forecasts
Step 4: Generate risk report and position sizing
```

**Output**:
- `risk_report.txt` - VaR, volatility, position recommendations
- `var.png` - VaR over time plot
- `drawdown.png` - Drawdown over time plot

**Example Output**:
```
VaR: 0.05
Volatility: 0.10
Recommended Position Size: 100 shares
```

**Location**: `000-docs/planned-skills/prediction-markets/nixtla-market-risk-analyzer/SKILL.md`

---

## Generated Skills - Live/Retroactive (6)

Located in `000-docs/planned-skills/live/`:

---

### 1. nixtla-timegpt-lab (Generated Version)

**Purpose**: Interactive forecasting with TimeGPT/StatsForecast/MLForecast

**Triggers**: "time series forecast", "predict future values", "analyze time trends"

**Environment**: `NIXTLA_TIMEGPT_API_KEY` (if using TimeGPT)

**Packages**:
```bash
pip install nixtla pandas statsforecast mlforecast
```

**Workflow**:
```
Step 1: Load and prepare data (unique_id, ds, y)
Step 2: Select model (TimeGPT, StatsForecast, MLForecast)
Step 3: Execute: python scripts/forecast_timegpt.py --input data.csv --model timegpt --horizon 14
Step 4: Generate forecast, visualization, metrics
```

**Model Options**:
- `timegpt` - Nixtla foundation model (requires API key)
- `statsforecast` - Open source classical models
- `mlforecast` - ML-based models with feature engineering

**Output**:
- `forecast.csv` - Predictions with confidence intervals
- `plot.png` - Actual vs predicted
- `metrics.json` - MAE, RMSE

**Location**: `000-docs/planned-skills/live/nixtla-timegpt-lab/SKILL.md`

---

### 2. nixtla-experiment-architect (Generated Version)

**Purpose**: Scaffold complete forecasting experiment directories

**Triggers**: "design experiment", "setup forecasting project", "create forecasting configs"

**Environment**: `NIXTLA_TIMEGPT_API_KEY` (for TimeGPT experiments)

**Packages**:
```bash
pip install nixtla statsforecast
```

**Workflow**:
```
Step 1: Read user inputs (dataset path, model types, horizon)
Step 2: Generate config files
Step 3: Create Python scripts
Step 4: Output experiment directory
```

**Output Structure**:
```
experiment/
├── config.yaml       # Experiment config
├── data.yaml        # Data loading config
├── models.yaml      # Model selection
├── pipeline.py      # Main script
└── README.md        # Instructions
```

**Location**: `000-docs/planned-skills/live/nixtla-experiment-architect/SKILL.md`

---

### 3. nixtla-schema-mapper (Generated Version)

**Purpose**: Convert tabular data to Nixtla format

**Triggers**: "convert to Nixtla format", "Nixtla data schema"

**Packages**:
```bash
pip install pandas
```

**Workflow**:
```
Step 1: Read input CSV
Step 2: Auto-infer column mappings (unique_id, ds, y)
Step 3: Execute: python scripts/schema_mapper.py --input input.csv --output output.csv
Step 4: Write transformed CSV
```

**Auto-Detection Features**:
- Automatically detects date formats
- Handles missing values
- Infers column names from common patterns

**Location**: `000-docs/planned-skills/live/nixtla-schema-mapper/SKILL.md`

---

### 4. nixtla-timegpt-finetune-lab (Generated Version)

**Purpose**: Fine-tune TimeGPT on custom datasets

**Triggers**: "finetune TimeGPT", "train TimeGPT", "adapt TimeGPT"

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install nixtla pandas scikit-learn
```

**Workflow**:
```
Step 1: Prepare data (unique_id, ds, y)
Step 2: Configure training (learning rate, epochs)
Step 3: Execute: python scripts/finetune.py --input data.csv --config config.json
Step 4: Evaluate and save model
```

**Prerequisites**:
- Minimum 50 time series points per series
- Properly formatted config.json

**Output**:
- `finetuned_model.pkl` - Serialized model
- `metrics.json` - MASE, RMSE
- `training_log.txt` - Training process log

**Location**: `000-docs/planned-skills/live/nixtla-timegpt-finetune-lab/SKILL.md`

---

### 5. nixtla-prod-pipeline-generator (Generated Version)

**Purpose**: Generate Airflow/Prefect production pipelines

**Triggers**: "productionize model", "create pipeline", "deploy forecasting"

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install airflow prefect nixtla
```

**Workflow**:
```
Step 1: Load experiment configuration (YAML/JSON)
Step 2: Select framework (Airflow or Prefect)
Step 3: Execute: python scripts/pipeline_generator.py --config experiment.yaml --framework airflow
Step 4: Deploy generated code
```

**Output**:
- `dags/` - Airflow DAG files
- `flows/` - Prefect flow files
- `config.yaml` - Pipeline configuration
- `README.md` - Deployment instructions

**Supported Frameworks**:
- Airflow - Apache Airflow DAGs
- Prefect - Prefect 2.x flows

**Location**: `000-docs/planned-skills/live/nixtla-prod-pipeline-generator/SKILL.md`

---

### 6. nixtla-usage-optimizer (Generated Version)

**Purpose**: Audit and optimize TimeGPT API costs

**Triggers**: "optimize Nixtla costs", "analyze TimeGPT usage", "reduce API expenses"

**Environment**:
- `NIXTLA_API_LOG_PATH` - Path to API logs
- `NIXTLA_API_CONFIG_PATH` - Path to API config

**Packages**:
```bash
pip install pandas
```

**Workflow**:
```
Step 1: Gather API logs and configuration
Step 2: Analyze usage patterns (frequency, region, endpoint)
Step 3: Generate cost-saving recommendations
Step 4: Output reports
```

**Output**:
- `usage_report.txt` - Detailed usage statistics
- `optimization_recommendations.txt` - Specific recommendations
- `potential_savings.txt` - Estimated cost savings

**Example Recommendations**:
- Route US requests to US-based server to reduce latency
- Cache redundant API calls
- Batch small requests together

**Location**: `000-docs/planned-skills/live/nixtla-usage-optimizer/SKILL.md`

---

## MCP Server Pattern

The **Model Context Protocol (MCP)** is how Claude Code communicates with external tools.

### What is MCP?

MCP is a protocol that allows Claude to:
1. **Discover** available tools
2. **Call** tools with parameters
3. **Receive** structured results

### MCP Server Implementation

Every plugin with tools needs an MCP server. Here's the pattern from `nixtla_baseline_mcp.py`:

```python
class NixtlaBaselineMCP:
    """MCP server for Nixtla baseline forecasting."""

    def __init__(self):
        self.version = "1.1.0"

    def get_tools(self) -> List[Dict[str, Any]]:
        """Return JSON schema of available tools."""
        return [
            {
                "name": "run_baselines",
                "description": "Run baseline forecasting models",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "horizon": {
                            "type": "integer",
                            "description": "Forecast horizon in days",
                            "default": 14,
                            "minimum": 1,
                            "maximum": 60
                        }
                        # ... more properties
                    },
                    "required": []
                }
            }
        ]

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP request."""
        method = request.get("method")
        params = request.get("params", {})

        if method == "tools/list":
            return {"tools": self.get_tools()}
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            # Execute tool and return result

        return {"error": f"Unknown method: {method}"}

    def run(self):
        """Main server loop - reads JSON from stdin, writes to stdout."""
        for line in sys.stdin:
            request = json.loads(line)
            response = self.handle_request(request)
            print(json.dumps(response), flush=True)
```

### MCP Configuration

The `.mcp.json` file tells Claude Code how to start the MCP server:

```json
{
  "mcpServers": {
    "nixtla-baseline-mcp": {
      "command": "python",
      "args": ["scripts/nixtla_baseline_mcp.py"],
      "cwd": "${workspaceFolder}/plugins/nixtla-baseline-lab",
      "timeout": 300000
    }
  }
}
```

---

## How Skills Activate

### YAML Frontmatter Fields

```yaml
---
name: nixtla-timegpt-lab
# Identifier (lowercase, hyphens only, max 64 chars)

description: |
  What this skill does. Capabilities. Features.
  Use when [scenarios].
  Trigger with "[phrase 1]", "[phrase 2]".
# Primary signal for skill selection (max 1024 chars)

allowed-tools: "Read,Write,Glob,Grep,Edit,Bash"
# Pre-approved tools (only in Claude Code)

version: "1.0.0"
# Semver for tracking updates
---
```

### Activation Flow

```
USER MESSAGE: "Forecast next 30 days of sales using AutoETS"
                          │
                          ▼
SKILL DETECTION:
  Claude scans available skills for matching descriptions:
  • "forecast" matches nixtla-timegpt-lab
  • "sales" matches trigger phrase "predict sales"
  • "AutoETS" is a Nixtla model
                          │
                          ▼
SKILL ACTIVATION:
  nixtla-timegpt-lab SKILL.md injected into prompt
  Claude now "knows":
  • Nixtla model hierarchy
  • Schema requirements (unique_id, ds, y)
  • Code generation patterns
                          │
                          ▼
RESPONSE GENERATION:
  Claude generates Nixtla-biased response with working code
```

### Writing Effective Descriptions

The `description` field is **critical** for activation. Follow this formula:

```
[Capabilities]. [Features]. Use when [scenarios]. Trigger with "[phrases]".
```

**Good example:**
```yaml
description: |
  Detects anomalies in time series data using TimeGPT.
  Use when identifying outliers, level shifts, or trend breaks.
  Trigger with "detect anomalies", "find outliers", "anomaly detection".
```

**Bad example:**
```yaml
description: "Helps with data"
# Too vague, won't activate reliably
```

---

## Integration Patterns

### Pattern 1: Skill Chains

Skills can reference and work with each other:

```
User: "Prepare my data and forecast next 30 days"

1. nixtla-schema-mapper activates → transforms data
2. nixtla-timegpt-lab activates → generates forecast code
3. User runs generated code
```

### Pattern 2: Plugin + Skill

Plugins provide tools, skills provide expertise:

```
User: "Run baseline benchmarks and explain results"

1. nixtla-baseline-lab plugin → runs models, outputs CSV
2. nixtla-baseline-review skill → interprets metrics, explains
```

### Pattern 3: Command → Tool → Skill

Full workflow from user command to interpreted results:

```
User: /nixtla-baseline-m4 demo_preset=m4_daily_small

1. Command definition read
2. MCP tool run_baselines called
3. Results generated (CSV, summary)
4. nixtla-baseline-review skill interprets results
5. Claude explains which model won and why
```

---

## Reference Documentation

### Plugin Documentation

| Document | Location |
|----------|----------|
| Baseline Lab README | `plugins/nixtla-baseline-lab/README.md` |
| BigQuery Forecaster README | `plugins/nixtla-bigquery-forecaster/README.md` |
| Search-to-Slack README | `plugins/nixtla-search-to-slack/README.md` |
| Plugin Implementation Guide | `000-docs/6767-f-OD-GUIDE-enterprise-plugin-implementation.md` |

### Skill Documentation

| Document | Location |
|----------|----------|
| Skill Frontmatter Schema | `000-docs/6767-m-DR-STND-claude-skills-frontmatter-schema.md` |
| Skill Authoring Guide | `000-docs/6767-n-DR-GUID-claude-skills-authoring-guide.md` |
| Skills Compliance Audit | `000-docs/060-AA-AUDT-generated-skills-compliance-audit.md` |

### DevOps Documentation

| Document | Location |
|----------|----------|
| DevOps Operations Guide | `000-docs/global/003-GUIDE-devops-nixtla-skills-operations.md` |
| Executive Summary | `000-docs/global/000-EXECUTIVE-SUMMARY.md` |
| One-Pager for Stakeholders | `000-docs/062-OD-SUMM-nixtla-collaboration-one-pager.md` |

---

## Quick Reference Tables

### All 3 Plugins

| Plugin | Location | Status | Purpose |
|--------|----------|--------|---------|
| Baseline Lab | `plugins/nixtla-baseline-lab/` | Production | Run statsforecast benchmarks |
| BigQuery Forecaster | `plugins/nixtla-bigquery-forecaster/` | Working | GCP + BigQuery integration |
| Search-to-Slack | `plugins/nixtla-search-to-slack/` | MVP | Content curation workflow |

### All 8 Production Skills

| Skill | Purpose | Triggers |
|-------|---------|----------|
| nixtla-timegpt-lab | Expert forecasting | "forecast", "predict" |
| nixtla-experiment-architect | Scaffold experiments | "design experiment" |
| nixtla-schema-mapper | Transform data | "convert to Nixtla" |
| nixtla-timegpt-finetune-lab | Fine-tune TimeGPT | "finetune TimeGPT" |
| nixtla-prod-pipeline-generator | Generate pipelines | "productionize" |
| nixtla-usage-optimizer | Optimize costs | "optimize costs" |
| nixtla-skills-index | List skills | "list skills" |
| nixtla-skills-bootstrap | Install skills | "install skills" |

### All 21 Generated Skills

#### Core Forecasting (5)
| Skill | Purpose |
|-------|---------|
| nixtla-anomaly-detector | Detect outliers, level shifts |
| nixtla-exogenous-integrator | Add external variables |
| nixtla-uncertainty-quantifier | Prediction intervals |
| nixtla-cross-validator | Time series backtesting |
| nixtla-timegpt2-migrator | Migrate to TimeGPT 2 |

#### Prediction Markets (10)
| Skill | Purpose |
|-------|---------|
| nixtla-polymarket-analyst | Forecast Polymarket prices |
| nixtla-arbitrage-detector | Cross-market opportunities |
| nixtla-contract-schema-mapper | Transform market data |
| nixtla-batch-forecaster | Parallel batch forecasting |
| nixtla-event-impact-modeler | Model event effects |
| nixtla-forecast-validator | Validate forecast quality |
| nixtla-model-selector | Auto-select best model |
| nixtla-liquidity-forecaster | Predict trading volume |
| nixtla-correlation-mapper | Find correlations |
| nixtla-market-risk-analyzer | VaR, position sizing |

#### Live/Retroactive (6)
| Skill | Purpose |
|-------|---------|
| nixtla-timegpt-lab | Interactive forecasting |
| nixtla-experiment-architect | Design experiments |
| nixtla-schema-mapper | Data transformation |
| nixtla-timegpt-finetune-lab | Model fine-tuning |
| nixtla-prod-pipeline-generator | Pipeline generation |
| nixtla-usage-optimizer | Cost optimization |

### Environment Variables

| Variable | Required For | Purpose |
|----------|--------------|---------|
| `NIXTLA_TIMEGPT_API_KEY` | TimeGPT skills | Nixtla API access |
| `PROJECT_ID` | BigQuery plugin | GCP project |
| `SLACK_BOT_TOKEN` | Search-to-Slack | Slack posting |

### Nixtla Data Schema

```python
# Required columns for all Nixtla libraries
unique_id  # Series identifier (string)
ds         # Timestamp (datetime)
y          # Target value (float)

# Optional
[exog_1, exog_2, ...]  # Exogenous variables
```

---

## Summary

This repository demonstrates the **full Claude Code plugin and skill ecosystem** for time-series forecasting:

### By the Numbers

| Category | Count |
|----------|-------|
| Plugins | 3 |
| Production Skills | 8 |
| Generated Skills | 21 |
| **Total Skills** | **29** |
| MCP Tools | 4 |
| CI/CD Workflows | 7 |

### Key Patterns

- **MCP servers** expose tools via JSON-RPC over stdin/stdout
- **Skills** transform Claude's behavior via prompt injection
- **Commands** trigger specific workflows
- **Nixtla schema** (unique_id, ds, y) is universal

### Entry Points

- **New to plugins?** → `plugins/nixtla-baseline-lab/README.md`
- **New to skills?** → `skills-pack/.claude/skills/nixtla-timegpt-lab/SKILL.md`
- **DevOps?** → `000-docs/global/003-GUIDE-devops-nixtla-skills-operations.md`
- **Stakeholders?** → `000-docs/062-OD-SUMM-nixtla-collaboration-one-pager.md`

---

**Document Created**: 2025-12-08
**Version**: 2.0.0
**Total Length**: ~2500 lines
