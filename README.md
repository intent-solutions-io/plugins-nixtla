# Claude Code Plugins – Nixtla Ecosystem

> Private, community-built Claude Code integrations around Nixtla's statsforecast and TimeGPT. **2 Plugins**: Baseline Lab (benchmarking) + BigQuery Forecaster (production forecasts on cloud data).

[![Private Repository](https://img.shields.io/badge/Repository-Private-red)](https://github.com/jeremylongshore/claude-code-plugins-nixtla)
[![Experimental](https://img.shields.io/badge/Status-Experimental-orange)](https://github.com/jeremylongshore/claude-code-plugins-nixtla)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

> **Maintained by**: Intent Solutions (Jeremy Longshore)
> **Sponsored by**: Nixtla (Max Mergenthaler – early/enterprise supporter)
> **Status**: Experimental prototype | Private collaboration workspace

---

## What This Repo Is

This repository is a **developer sandbox** for building and testing Claude Code plugins on top of Nixtla's open-source time series stack.

**Key components**:

- **Nixtla Baseline Lab Plugin** – A Claude Code plugin that runs statsforecast baseline models (SeasonalNaive, AutoETS, AutoTheta) on M4 benchmark data or custom CSV files.
- **Metrics & Benchmarking** – Calculates sMAPE and MASE metrics, generates reproducible benchmark reports in Markdown format.
- **Repro Bundles** – Captures run configuration, library versions, and results for exact reproducibility.
- **GitHub Issue Draft Generator** – Unique productivity tool that auto-generates pre-filled issue drafts with your complete experimental context (metrics, config, library versions) ready to share with Nixtla maintainers on `nixtla/statsforecast`.
- **Optional TimeGPT Showdown** – Opt-in comparison path for users with valid `NIXTLA_TIMEGPT_API_KEY` who want to compare baselines against Nixtla's TimeGPT foundation model on a small, controlled sample.

### Where to Start in the Code

- **Plugin entrypoint**: `plugins/nixtla-baseline-lab/scripts/mcp_server.py` (Claude Code MCP server exposing `/nixtla-baseline-m4`).
- **Task orchestration**: `plugins/nixtla-baseline-lab/scripts/m4_baseline.py` (loads datasets, runs models, writes repro bundles).
- **Skill for result interpretation**: `plugins/nixtla-baseline-lab/skills/interpret_results.py` (turns metrics into natural-language summaries).
- **Demo harnesses**: `scripts/run_nixtla_review_baseline.sh` and `scripts/run_nixtla_review_timegpt.sh` (quick validation flows).
- **Docs**: Full plugin guide in `plugins/nixtla-baseline-lab/README.md`.

**What this enables**:

- CI-backed, reproducible statsforecast baseline experiments inside Claude Code.
- One-command capture of metrics, library versions, and run configurations for sharing with Nixtla maintainers or collaborators.
- A reference implementation showing how to integrate Nixtla OSS libraries into Claude Code plugins.

---

## 🔌 Plugins in This Repo

### Plugin 1: Nixtla Baseline Lab
**Purpose**: Run statsforecast baselines (AutoETS, AutoTheta) on M4 benchmark data. Perfect for research and model evaluation.

**Quick Demo**:
```bash
/nixtla-baseline-m4 demo_preset=m4_daily_small
```

**Output**: Metrics (sMAPE, MASE), repro bundles, GitHub issue drafts

---

### Plugin 2: Nixtla BigQuery Forecaster ⭐ NEW

> **What it is**: Run Nixtla statsforecast models on BigQuery data via Cloud Functions
> **Why it exists**: Showcase what's possible with Claude Code plugins + Nixtla + Google Cloud
> **Who it's for**: Anyone who wants to forecast BigQuery time series data

#### 2-Minute Demo

Uses **PUBLIC** Chicago taxi data (200M+ rows). Zero setup on your end.

**Step 1: Deploy** (GitHub Actions handles everything)

**Step 2: Test**
```bash
curl -X POST "FUNCTION_URL" -d '{
  "project_id": "bigquery-public-data",
  "dataset": "chicago_taxi_trips",
  "table": "taxi_trips",
  "timestamp_col": "trip_start_timestamp",
  "value_col": "trip_total",
  "group_by": "payment_type",
  "horizon": 7,
  "source_project": "bigquery-public-data"
}'
```

**Step 3: Get Results**
- Forecasts for next 7 days
- AutoETS + AutoTheta models (official Nixtla statsforecast)
- Payment types: Cash, Credit Card, Mobile, etc.

#### What This Shows

✅ **Nixtla OSS works great on massive datasets** (we tested with 100K+ rows)
✅ **Serverless deployment is easy** (Cloud Functions auto-scale)
✅ **Real-world data, real-world use case** (not toy examples)

#### Ideas for Max

Could this become:
- Customer demo for "Nixtla + BigQuery"?
- Internal tool for testing statsforecast at scale?
- Template for building Nixtla integrations?
- Proof point for Google Cloud partnerships?

**We don't know. Just sharing what we built.**

**Setup**: See `plugins/nixtla-bigquery-forecaster/` and `000-docs/070-OD-GUID-gcp-setup-complete.md`

**Built with**: Nixtla statsforecast, Google Cloud, Claude Code | **Time to build**: 48 hours | **Status**: Working demo, tested with real data

---

## Quickstart: Run Your First Baseline (2 Minutes)

**Safe default flow** (no API keys, no network calls, offline-only):

```bash
# 1. Clone and navigate to plugin
git clone https://github.com/jeremylongshore/claude-code-plugins-nixtla.git
cd claude-code-plugins-nixtla/plugins/nixtla-baseline-lab

# 2. Setup Python environment (creates .venv-nixtla-baseline)
./scripts/setup_nixtla_env.sh --venv

# 3. Activate virtualenv
source .venv-nixtla-baseline/bin/activate

# 4. Install plugin dependencies
pip install -r scripts/requirements.txt

# 5. Trust the workspace in Claude Code (follow prompts)
```

### Run Your First Experiment

From Claude Code (after trusting the repo and installing the plugin):

```
/nixtla-baseline-m4 demo_preset=m4_daily_small
```

**What this does**:

- Loads M4 Daily dataset (subset of 5 series for quick demo).
- Runs SeasonalNaive, AutoETS, AutoTheta models with horizon=7.
- Calculates sMAPE and MASE metrics.
- Generates complete reproducibility bundle:
  - `results_M4_Daily_h7.csv` – Metrics table.
  - `summary_M4_Daily_h7.txt` – Human-readable summary.
  - `benchmark_report_M4_Daily_h7.md` – Markdown report.
  - `run_manifest.json` – Run configuration (for exact reproduction).
  - `compat_info.json` – Library versions (statsforecast, pandas, numpy).

**No API keys required. No network calls. Offline-only by default.**

### Review Your Results

```bash
# View human-readable summary
cat nixtla_baseline_m4_demo/summary_M4_Daily_h7.txt

# View detailed metrics
cat nixtla_baseline_m4_demo/results_M4_Daily_h7.csv

# View benchmark report (GitHub-ready)
cat nixtla_baseline_m4_demo/benchmark_report_M4_Daily_h7.md
```

---

## Local Development & Testing

Want to extend the plugin? Here's the fastest way to get a green test run:

1. **Create a virtualenv (repo root)**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. **Install dev dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```
3. **Run the test suite** (offline-safe; uses golden task harness)
   ```bash
   pytest plugins/nixtla-baseline-lab/tests/
   ```
4. **Run full coverage + lint** (optional but recommended before PRs)
   ```bash
   pytest --cov=plugins --cov=examples --cov-report=term-missing
   black . && isort . && flake8 plugins examples tests
   ```

All commands are offline by default; TimeGPT calls remain opt-in only when you pass `include_timegpt=true` in plugin runs.

---

## 📱 For Max: Quick Phone Checklist

> **Mobile-friendly guide**: Follow these steps from your phone while working on your desktop.

### Prerequisites
- ✅ Claude Code installed
- ✅ Python 3.10+ on your machine
- ✅ Git installed

### Step 1: Clone the Repo
```bash
git clone https://github.com/jeremylongshore/claude-code-plugins-nixtla.git
cd claude-code-plugins-nixtla
```

### Step 2: Open in Claude Code
1. Open the `claude-code-plugins-nixtla` folder in Claude Code
2. Trust the workspace when prompted
3. Plugin will auto-install from local marketplace

### Step 3: Setup Python Environment
```bash
cd plugins/nixtla-baseline-lab
./scripts/setup_nixtla_env.sh --venv
```

This installs: statsforecast, datasetsforecast, pandas, numpy

### Step 4: Run Offline Baseline Demo
In Claude Code:
```
/nixtla-baseline-m4 demo_preset=m4_daily_small
```

**What happens**:
- Loads M4 Daily subset (5 series)
- Runs SeasonalNaive, AutoETS, AutoTheta
- Computes sMAPE and MASE
- Creates output in `nixtla_baseline_m4_test/`

**Ask Claude**: "Which statsforecast model performed best and why?"

### Step 5 (Optional): TimeGPT Showdown
Only if you want to test TimeGPT comparison:

```bash
# Set API key
export NIXTLA_TIMEGPT_API_KEY="your-key-here"
```

In Claude Code:
```
/nixtla-baseline-m4 demo_preset=m4_daily_small include_timegpt=true timegpt_max_series=2
```

Creates additional `timegpt_showdown_*.txt` file comparing TimeGPT vs baselines.

### Step 6: Review Results
```bash
# View summary
cat nixtla_baseline_m4_test/summary_M4_Daily_h7.txt

# View metrics CSV
cat nixtla_baseline_m4_test/results_M4_Daily_h7.csv

# View benchmark report
cat nixtla_baseline_m4_test/benchmark_report_M4_Daily_h7.md
```

### What This Shows
- Offline statsforecast baselines work inside Claude Code
- Metrics and reports are auto-generated
- Repro bundles capture complete experimental context
- Optional TimeGPT comparison (strictly opt-in)

**Questions?** jeremy@intentsolutions.io | 251.213.1115

---

## Core Capabilities

Now that you've run your first baseline, here's what the plugin offers:

### 1. Offline Statsforecast Baselines

- **Models**: SeasonalNaive, AutoETS, AutoTheta from Nixtla's `statsforecast` library.
- **Datasets**:
  - **M4 Daily** subset (benchmark dataset via `datasetsforecast`).
  - **Custom CSV** files with columns `unique_id`, `ds`, `y`.
- **Metrics**: sMAPE (Symmetric Mean Absolute Percentage Error) and MASE (Mean Absolute Scaled Error).
- **Power-User Controls**:
  - Select specific models: `models=["AutoETS", "AutoTheta"]`
  - Configure frequency: `freq="D"` (Daily), `"H"` (Hourly), `"W"` (Weekly), `"M"` (Monthly)
  - Set seasonal period: `season_length=7` (for weekly patterns)
  - Quick demos: `demo_preset=m4_daily_small` (5 series, horizon=7)

### 2. Reproducibility Bundles

**Problem**: Sharing time series experiments with incomplete context wastes maintainer time.

**Solution**: Automatic repro bundle generation captures everything needed to reproduce your exact run:

- **`run_manifest.json`** – Dataset, horizon, models, frequency, seasonal period
- **`compat_info.json`** – Library versions (statsforecast, datasetsforecast, pandas, numpy, python)
- **Metrics CSV + Summary** – Complete results in multiple formats

**Use case**: When asking Nixtla maintainers about unexpected behavior, share your repro bundle for instant context.

### 3. GitHub Issue Draft Generator

**Problem**: Reporting statsforecast issues requires manually gathering metrics, versions, configurations.

**Solution**: One command generates a complete, pre-filled GitHub issue draft:

```
/nixtla-generate-issue-draft issue_type=question
```

**What this generates** (`github_issue_draft.md`):

- Issue template (question/bug/benchmark) with proper formatting
- Your complete benchmark results (metrics table)
- Run configuration (horizon, models, freq, season_length)
- Library versions (for reproducibility)
- Clear instructions for posting to `nixtla/statsforecast`

**Workflow**:
1. Run your baseline experiment
2. Generate issue draft
3. Review and customize the draft
4. Post manually to [nixtla/statsforecast](https://github.com/Nixtla/statsforecast/issues)

**Note**: This is a **community helper tool** (not an official Nixtla template) that respects maintainer time by providing complete context upfront.

### 4. Benchmark Reports

- **Markdown-formatted reports** suitable for GitHub issues, documentation, or internal sharing.
- **Compatibility info**: Auto-detects installed library versions for debugging and repro.
- **Version introspection**: Helps Nixtla maintainers identify version-specific behavior.

---

## Advanced: TimeGPT Comparison (Optional)

**When to use this**: Useful for checking if the Foundation Model approach (zero-shot, complex patterns) outperforms traditional statistics on your specific data signature. For example, if your data has complex seasonality or trend patterns that classical models might miss, TimeGPT's learned representations could provide lift.

**Requirements**:

1. Valid `NIXTLA_TIMEGPT_API_KEY` in your environment.
2. Explicit `include_timegpt=true` flag.
3. Understanding that this will make network calls to Nixtla's TimeGPT API and may incur costs.

**Example**:

```bash
# Set API key (never commit this!)
export NIXTLA_TIMEGPT_API_KEY="your-api-key-here"

# Run with TimeGPT showdown
/nixtla-baseline-m4 demo_preset=m4_daily_small include_timegpt=true timegpt_max_series=3
```

**What this does**:

- Runs statsforecast baselines as usual (offline).
- **Additionally**: Sends first 3 series to TimeGPT API for forecasts.
- Computes sMAPE and MASE for TimeGPT forecasts.
- Compares TimeGPT to best statsforecast baseline.
- Generates `timegpt_showdown_M4_Daily_h7.txt` with comparison summary.
- **Emphasis**: Results based on small sample (3 series) are **indicative, not conclusive**.

**Cost control**:
- **Strictly opt-in** (disabled by default)
- **Series limit** (default 5, configurable via `timegpt_max_series`)
- **Graceful degradation** (TimeGPT failure doesn't break baseline run)

**Important notes**:

- You are responsible for monitoring your TimeGPT API usage and costs.
- This repo makes no guarantees about TimeGPT availability, latency, or pricing.
- For official TimeGPT documentation, visit [docs.nixtla.io](https://docs.nixtla.io/).

---

## Context & Expectations

Now that you understand what this plugin does, here's what to expect:

### What This Repo Is

- **A developer sandbox** for prototyping reproducible baseline workflows inside Claude Code.
- **A community helper** that makes it easier to share experimental context with Nixtla maintainers.
- **A reference implementation** showing how Nixtla OSS libraries can integrate with Claude Code plugins.

### What This Repo Is NOT

Set expectations clearly:

- **Not an official Nixtla product** – This is a community integration maintained by Intent Solutions, not by Nixtla. Nixtla is an early sponsor and collaborator, but this repo is not part of Nixtla's official tooling.
- **Not a production SLA or support commitment** – This is an experimental prototype intended for development, benchmarking, and reproducibility workflows. No guarantees about uptime, support, or maintenance timelines.
- **Not a guarantee of optimal performance** – The plugin runs statsforecast models with sensible defaults. It does not claim that any particular model or configuration will be optimal for all workloads. For production forecasting, consult Nixtla's official documentation and best practices.

### Development Principles

**1. Respectful Integration**
- We build on top of Nixtla's OSS tools, not parallel to them.
- We focus on automation and reproducibility helpers, not replacement tooling.

**2. Modest Framing**
- We avoid over-promising ("production-ready", "enterprise-grade", "guaranteed").
- We prefer "experimental", "prototype", "developer sandbox", "intended to help".

**3. Technical Accuracy**
- We document what the plugin actually does, not what we hope it might do someday.
- We provide clear reproducibility information (library versions, run configurations).

**4. Human-Centered**
- We help developers reproduce experiments and share context with Nixtla maintainers.
- We require human review for all generated content (issue drafts, reports).

---

## Repository Structure & Documentation

```
claude-code-plugins-nixtla/
├── plugins/
│   ├── nixtla-baseline-lab/        # Main plugin directory
│   │   ├── scripts/                # MCP server, setup
│   │   ├── skills/                 # AI skill for result interpretation
│   │   ├── tests/                  # Golden task harness (CI validation)
│   │   ├── data/                   # M4 dataset cache (auto-downloaded)
│   │   └── README.md               # Complete plugin manual
│   ├── nixtla-bigquery-forecaster/ # BigQuery Cloud Functions plugin
│   └── nixtla-search-to-slack/     # Content discovery plugin
├── scripts/
│   ├── run_nixtla_review_baseline.sh    # 2-minute offline review demo
│   ├── run_nixtla_review_timegpt.sh     # Optional TimeGPT review
│   └── cleanup-doc-filing-v3.sh         # Doc-Filing v3.0 cleanup script
├── 000-docs/                       # Technical documentation (69 files)
│   ├── 6767-OD-*.md               # Overview, architecture, planning (4 canonical docs)
│   ├── 015-022-AA-AACR-*.md       # Phase implementation AARs (Phases 1-8)
│   ├── 050-060-*.md               # Plugin specification series (9 plugin specs)
│   ├── 061-076-*.md               # Migrated documentation (guides, memos)
│   ├── 077-OD-RELS-v0-8-0-doc-filing-compliance.md   # Latest release AAR
│   └── README.md                  # Documentation index
├── docs/                           # User-facing documentation
│   ├── index.md                   # Docs home page
│   ├── nixtla-baseline-lab.md     # Complete plugin documentation
│   └── architecture.md            # Architecture overview
├── archive/                        # Historical backups
│   └── backups-20251108/          # Archived plugin backups (6,517 files)
├── examples/                       # Integration examples
├── CHANGELOG.md                    # Release history (0.1.0 → 0.8.0)
├── CLAUDE.md                       # Claude Code agent guidance
├── VERSION                         # Current version: 0.8.0
└── README.md                       # This file
```

### Documentation Links

**User-Facing**:
- **[Plugin Manual](./plugins/nixtla-baseline-lab/README.md)** – Complete setup, usage examples, parameter reference
- **[Docs Site](./docs/index.md)** – Docs home page
- **[Plugin Documentation](./docs/nixtla-baseline-lab.md)** – Comprehensive plugin guide

**Technical**:
- **[Nixtla Review Kit](./000-docs/035-OD-RELS-v0-7-0-nixtla-review-kit.md)** – For Nixtla engineers reviewing this integration
- **[Architecture Overview](./000-docs/6767-OD-OVRV-nixtla-baseline-lab-overview.md)** – High-level system design
- **[Implementation Plan](./000-docs/6767-PP-PLAN-nixtla-claude-plugin-poc-baseline-lab.md)** – Development roadmap
- **[Test Coverage](./000-docs/023-QA-TEST-nixtla-baseline-lab-test-coverage.md)** – Comprehensive test report
- **[CHANGELOG.md](./CHANGELOG.md)** – Complete version history

### Roadmap & Next Steps

- **High-level roadmap**: [000-docs/068-PP-RMAP-project-roadmap.md](./000-docs/068-PP-RMAP-project-roadmap.md)
- **Release audit trail**: [000-docs/077-OD-RELS-v0-8-0-doc-filing-compliance.md](./000-docs/077-OD-RELS-v0-8-0-doc-filing-compliance.md)
- **Planning artifacts**: [000-docs/6767-PP-PLAN-nixtla-claude-plugin-poc-baseline-lab.md](./000-docs/6767-PP-PLAN-nixtla-claude-plugin-poc-baseline-lab.md)

---

## Nixtla & Sponsorship Context

**Nixtla** is an early and enterprise supporter of this experimental work.

- **Maintained by**: Intent Solutions (Jeremy Longshore) – not by Nixtla.
- **Sponsored by**: Nixtla (Max Mergenthaler) – provides guidance, feedback, and collaboration.
- **Purpose**: Make it easier for Nixtla users and maintainers to reproduce baseline behavior, share experiments, and collaborate on time series workflows inside Claude Code.

**This integration exists to**:

- Help developers run reproducible statsforecast experiments.
- Capture metrics, library versions, and run configurations for sharing with Nixtla maintainers.
- Demonstrate how Nixtla's OSS stack can integrate with Claude Code plugins.

**What this is NOT**:

- Not an official Nixtla product or endorsement.
- Not a replacement for Nixtla's official tooling or documentation.
- Not a production support commitment from Nixtla.

**For official Nixtla resources**:

- [Nixtla Documentation](https://docs.nixtla.io/)
- [statsforecast GitHub](https://github.com/Nixtla/statsforecast)
- [TimeGPT Documentation](https://docs.nixtla.io/docs/getting-started-timegpt)
- [Nixtla Community Slack](https://join.slack.com/t/nixtlaworkspace/shared_invite/zt-135dssye9-fWTzMpv2WBthq8NK0Yvu6A)

---

## CI Status & Validation

The plugin includes GitHub Actions CI that runs on every push/PR:

- ✅ Validates plugin manifest
- ✅ Runs golden task harness (5-step validation)
- ✅ Uploads test artifacts (7-day retention)

**CI remains offline-only** – No TimeGPT calls, no network dependencies.

**Golden task validation checks**:
1. CSV schema (columns: unique_id, model, sMAPE, MASE)
2. Metrics ranges (sMAPE: 0-200%, MASE > 0)
3. Summary file content (baseline names, horizon, dataset)
4. Repro bundle completeness (manifest, compat info)
5. Exit code (0 = success, 1 = failure)

---

## Collaboration

This is a **private workspace** for experimentation between Intent Solutions and Nixtla. We are:

- Prototyping reproducible baseline workflows before wider release.
- Validating integration patterns with real Nixtla codebases.
- Building community helpers that respect Nixtla's existing tooling.

**For questions or collaboration inquiries**:

- **Jeremy Longshore** (Intent Solutions): jeremy@intentsolutions.io | 251.213.1115
- **Max Mergenthaler** (Nixtla): max@nixtla.io

---

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

---

## Acknowledgments

- **Nixtla Team**: For building world-class open-source time series forecasting tools and sponsoring this experimental integration work.
- **Max Mergenthaler**: For partnership, vision, and early/enterprise support.
- **Anthropic**: For Claude and the agent infrastructure that makes this possible.

---

**Maintained by**: Jeremy Longshore (Intent Solutions)
**Sponsored by**: Nixtla (Max Mergenthaler)
**Status**: Experimental Prototype | Private Collaboration
**Version**: 0.7.0
