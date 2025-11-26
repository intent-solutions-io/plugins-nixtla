# Nixtla Baseline Lab Plugin

**Maintained by**: Intent Solutions (Jeremy Longshore)
**Sponsored by**: Nixtla (Max Mergenthaler – early/enterprise supporter)

> Experimental Claude Code plugin for reproducible statsforecast baseline experiments with optional TimeGPT comparison.

---

## Overview

The **Nixtla Baseline Lab** plugin is a Claude Code integration that enables reproducible time series baseline experiments using Nixtla's open-source statsforecast library. It runs classical forecasting models (SeasonalNaive, AutoETS, AutoTheta) on M4 benchmark data or custom CSV files, calculates standard metrics (sMAPE, MASE), and generates structured reproducibility bundles.

**In terms a Nixtla engineer would immediately recognize**:

- Runs **statsforecast models** (SeasonalNaive, AutoETS, AutoTheta) on **M4 Daily** subset or **custom CSV** (`unique_id`, `ds`, `y` columns).
- Calculates **sMAPE and MASE** metrics per series/model using train/test splits.
- Generates **benchmark reports** (Markdown format suitable for GitHub issues).
- Captures **repro bundles** (`run_manifest.json`, `compat_info.json`) with library versions (statsforecast, datasetsforecast, pandas, numpy).
- Includes **GitHub issue draft generator** to create pre-filled issue templates for `nixtla/statsforecast` (community helper, not official template).
- Offers **optional TimeGPT showdown** (opt-in only) to compare baselines against TimeGPT on a small, controlled sample.

**What this enables**:

- Automated baseline experiments inside Claude Code with reproducible outputs.
- Easy sharing of metrics, library versions, and run configurations with Nixtla maintainers or collaborators.
- Reference implementation for integrating Nixtla OSS libraries into Claude Code plugins.

---

## Core Capabilities

The plugin has been developed through 6 phases of implementation:

### Phase 1-3: Offline Statsforecast Baselines

**Supported Models** (from `statsforecast`):

- **SeasonalNaive** – Repeats seasonal pattern from training data.
- **AutoETS** – Exponential smoothing with automatic parameter selection.
- **AutoTheta** – Theta method with optimization (often wins on M4 benchmarks).

**Datasets**:

- **M4 Daily** – Subset of M4 benchmark dataset via `datasetsforecast` library.
  - Auto-downloads and caches to `plugins/nixtla-baseline-lab/data/`.
  - Configurable series limit (e.g., 5 for quick demos, 50+ for full benchmarks).
- **Custom CSV** – User-provided files with required columns:
  - `unique_id` – Series identifier (string).
  - `ds` – Timestamp (datetime).
  - `y` – Target value (numeric).

**Metrics**:

- **sMAPE** (Symmetric Mean Absolute Percentage Error) – Range: 0% (perfect) to 200% (worst).
  - Interpretation: < 10% (good), 10-20% (acceptable), > 20% (poor).
- **MASE** (Mean Absolute Scaled Error) – Scaled against seasonal naive baseline.
  - Interpretation: < 1.0 (better than naive), 1.0 (same as naive), > 1.0 (worse than naive).

**Outputs**:

- `results_M4_Daily_h7.csv` – Per-series, per-model metrics table.
- `summary_M4_Daily_h7.txt` – Human-readable summary with average metrics.

**Key Features**:

- Configurable parameters: `horizon`, `series_limit`, `models`, `freq`, `season_length`.
- Demo presets for quick testing (e.g., `demo_preset=m4_daily_small` loads 5 series with horizon=7).
- No API keys required – **offline-only by default**.

### Phase 4: Benchmark Reports & Compatibility Info

**Benchmark Reports**:

- Markdown-formatted reports (`benchmark_report_M4_Daily_h7.md`) suitable for GitHub issues or documentation.
- Includes:
  - Dataset and horizon details.
  - statsforecast version (for reproducibility).
  - Average metrics table (sorted by performance).
  - Highlights section with key insights.
  - Timestamp.

**Compatibility Info**:

- `compat_info.json` – Captures library versions:
  - `statsforecast`, `datasetsforecast`, `pandas`, `numpy`, `python`.
- Auto-detects installed versions for debugging and repro.

**Version Introspection**:

- Plugin automatically captures environment details at runtime.
- Helps Nixtla maintainers reproduce exact behavior when debugging issues.

### Phase 5: Repro Bundles & GitHub Issue Drafts

**Repro Bundle Structure**:

After running a baseline experiment, the output directory contains:

```
nixtla_baseline_m4_demo/
├── results_M4_Daily_h7.csv          # Metrics (sMAPE, MASE per series/model)
├── summary_M4_Daily_h7.txt          # Human-readable summary
├── benchmark_report_M4_Daily_h7.md  # Markdown benchmark report
├── run_manifest.json                # Run configuration
├── compat_info.json                 # Library versions
└── timegpt_showdown_*.txt           # Optional TimeGPT comparison (if enabled)
```

**run_manifest.json Example**:

```json
{
  "dataset_label": "M4_Daily",
  "horizon": 7,
  "series_limit": 5,
  "models": ["SeasonalNaive", "AutoETS", "AutoTheta"],
  "freq": "D",
  "season_length": 7,
  "demo_preset": "m4_daily_small",
  "generated_at": "2025-11-26T16:14:19Z"
}
```

**compat_info.json Example**:

```json
{
  "statsforecast": "2.0.3",
  "datasetsforecast": "1.0.0",
  "pandas": "2.3.3",
  "numpy": "2.3.5",
  "python": "3.12.3"
}
```

**GitHub Issue Draft Generator**:

MCP tool to create pre-filled Markdown issue drafts for `nixtla/statsforecast`:

```
/nixtla-generate-issue-draft issue_type=question
```

**Generated draft includes**:

- Issue template (question/bug/benchmark).
- Complete benchmark results.
- Run configuration and library versions.
- Reproducibility information.

**Important note**: This is a **community helper tool**, not an official Nixtla issue template. Users should review the draft and manually post to GitHub.

### Phase 6: Optional TimeGPT Showdown

**Strictly Opt-In** (disabled by default):

- Requires explicit `include_timegpt=true` flag.
- Requires valid `NIXTLA_TIMEGPT_API_KEY` environment variable.
- **No network calls made unless explicitly opted in**.

**Cost Control**:

- Limited to small number of series (default 5, configurable via `timegpt_max_series`).
- Prevents unexpected API charges.

**Graceful Degradation**:

- TimeGPT failure (missing key, SDK, API error) doesn't break baseline run.
- Baseline CSV and summary files still generated.
- Clear failure reasons in response (`missing_api_key`, `sdk_not_installed`, `api_error`).

**Showdown Report**:

Text summary comparing TimeGPT forecasts to best statsforecast baseline:

```
timegpt_showdown_M4_Daily_h7.txt

TimeGPT Showdown Summary
========================
Dataset: M4 Daily
Horizon: 7
Series Evaluated: 3 (limited for cost control)

TimeGPT Performance:
- Average sMAPE: 1.23%
- Average MASE: 0.654

Best Baseline (AutoETS):
- Average sMAPE: 0.77%
- Average MASE: 0.422

Comparison:
- TimeGPT vs Best Baseline sMAPE: +0.46 pp (TimeGPT worse)
- TimeGPT vs Best Baseline MASE: +0.232 (TimeGPT worse)

WINNER: AutoETS (baseline)
```

**Important Disclaimers**:

- Results based on small sample (3-5 series) are **indicative, not conclusive**.
- This repo makes **no guarantees** about TimeGPT availability, latency, or cost.
- Users are responsible for monitoring their TimeGPT API usage and costs.
- For official TimeGPT documentation, visit [docs.nixtla.io](https://docs.nixtla.io/).

---

## How To Run It (High-Level)

### 1. Setup Environment

From `plugins/nixtla-baseline-lab/`:

```bash
# Create virtualenv
./scripts/setup_nixtla_env.sh --venv

# Activate virtualenv
source .venv-nixtla-baseline/bin/activate

# Install dependencies
pip install -r scripts/requirements.txt
```

### 2. Run Baseline Experiment

**Quick demo** (offline, 5 series, horizon=7):

```
/nixtla-baseline-m4 demo_preset=m4_daily_small
```

**Custom configuration**:

```
/nixtla-baseline-m4 horizon=14 series_limit=50 freq=D season_length=7
```

**With custom CSV**:

```
/nixtla-baseline-m4 dataset_type=csv csv_path=/path/to/data.csv horizon=7
```

### 3. Review Results

```bash
# View metrics
cat nixtla_baseline_m4_demo/results_M4_Daily_h7.csv

# View summary
cat nixtla_baseline_m4_demo/summary_M4_Daily_h7.txt

# View benchmark report
cat nixtla_baseline_m4_demo/benchmark_report_M4_Daily_h7.md
```

### 4. Generate Repro Bundle (Optional)

Repro bundle is **generated by default**. To disable:

```
/nixtla-baseline-m4 demo_preset=m4_daily_small generate_repro_bundle=false
```

### 5. Generate GitHub Issue Draft (Optional)

```
/nixtla-generate-issue-draft issue_type=question
```

Review `github_issue_draft.md`, fill in your question, and manually post to [nixtla/statsforecast](https://github.com/Nixtla/statsforecast/issues).

### 6. Run TimeGPT Showdown (Optional)

**Requirements**:

```bash
# Set API key
export NIXTLA_TIMEGPT_API_KEY="your-api-key-here"

# Install nixtla SDK
pip install nixtla
```

**Run with TimeGPT**:

```
/nixtla-baseline-m4 demo_preset=m4_daily_small include_timegpt=true timegpt_max_series=3
```

**Review showdown**:

```bash
cat nixtla_baseline_m4_demo/timegpt_showdown_M4_Daily_h7.txt
```

---

## Safety & Scope Notes

### What This Is

- An **experimental workspace** for reproducible baseline experiments.
- A **developer sandbox** for integrating Nixtla OSS libraries with Claude Code.
- A **community helper** for capturing metrics, library versions, and run configurations.

### What This Is NOT

- **Not an official Nixtla product** – This is maintained by Intent Solutions, not by Nixtla.
- **Not a production SLA** – No guarantees about uptime, support, or maintenance timelines.
- **Not a guarantee of optimal performance** – The plugin runs models with sensible defaults. For production forecasting, consult Nixtla's official documentation and best practices.

### Nixtla Remains the Source of Truth

For official information about:

- **statsforecast behavior** – [statsforecast docs](https://nixtlaverse.nixtla.io/statsforecast/)
- **TimeGPT documentation and pricing** – [docs.nixtla.io](https://docs.nixtla.io/)
- **Model selection and best practices** – [Nixtla blog and tutorials](https://www.nixtla.io/blog)

This plugin is intended to **help developers reproduce baseline behavior**, not to replace Nixtla's official tooling or documentation.

---

## Technical Architecture

### MCP Server

The plugin exposes tools via **Model Context Protocol (MCP)** JSON-RPC server:

- **Tool**: `run_baselines` – Runs statsforecast baselines on M4 or custom CSV.
- **Tool**: `generate_benchmark_report` – Creates Markdown benchmark report.
- **Tool**: `generate_github_issue_draft` – Creates pre-filled issue draft.

### AI Skill

The plugin includes an **AI skill** (`nixtla-baseline-review`) that helps Claude interpret baseline results:

- Reads metrics CSV and summary files.
- Identifies best-performing models.
- Explains sMAPE and MASE values.
- Provides recommendations based on results.
- Handles TimeGPT showdown interpretation (when enabled).

### Golden Task Harness

The plugin includes a **golden task harness** for validation:

- `tests/run_baseline_m4_smoke.py` – 5-step validation test.
- Runs on every CI build (GitHub Actions).
- Validates CSV schema, metrics ranges, summary content.
- Exit code 0 on success, 1 on failure.

### CI Integration

GitHub Actions workflow (`.github/workflows/nixtla-baseline-lab-ci.yml`):

- Runs on every push/PR to main.
- Validates plugin manifest.
- Runs golden task harness (offline statsforecast baselines).
- Uploads test artifacts (7-day retention).
- **CI remains offline-only** – No TimeGPT calls, no network dependencies.

---

## Links & References

### Plugin Documentation

- **[Plugin Manual (README)](https://github.com/jeremylongshore/claude-code-plugins-nixtla/tree/main/plugins/nixtla-baseline-lab/README.md)** – Complete user guide with detailed setup, parameters, and examples.

### Repository Documentation

- **[Root README](https://github.com/jeremylongshore/claude-code-plugins-nixtla)** – Repository overview, quickstart, and collaboration context.
- **[Architecture Doc (6767-OD-ARCH)](https://github.com/jeremylongshore/claude-code-plugins-nixtla/blob/main/000-docs/6767-OD-ARCH-nixtla-claude-plugin-poc-baseline-lab.md)** – Technical architecture and design decisions.
- **[Planning Doc (6767-PP-PLAN)](https://github.com/jeremylongshore/claude-code-plugins-nixtla/blob/main/000-docs/6767-PP-PLAN-nixtla-claude-plugin-poc-baseline-lab.md)** – Implementation roadmap and phase breakdown.

### Phase After-Action Reports (AARs)

- **[Phase 1 AAR (015)](https://github.com/jeremylongshore/claude-code-plugins-nixtla/blob/main/000-docs/015-AA-AACR-phase-01-structure-and-skeleton.md)** – Plugin scaffolding, marketplace setup.
- **[Phase 2 AAR (016)](https://github.com/jeremylongshore/claude-code-plugins-nixtla/blob/main/000-docs/016-AA-AACR-phase-02-manifest-and-mcp.md)** – MCP server tools.
- **[Phase 3 AAR (017)](https://github.com/jeremylongshore/claude-code-plugins-nixtla/blob/main/000-docs/017-AA-AACR-phase-03-mcp-baselines-nixtla-oss.md)** – Statsforecast baselines + M4 integration.
- **[Phase 4 AAR (018)](https://github.com/jeremylongshore/claude-code-plugins-nixtla/blob/main/000-docs/018-AA-AACR-phase-04-testing-and-skills.md)** – Golden task harness + AI skill.
- **[Phase 5 AAR (019)](https://github.com/jeremylongshore/claude-code-plugins-nixtla/blob/main/000-docs/019-AA-AACR-phase-05-setup-and-validation.md)** – Setup script + dependency validation.
- **[Phase 6 AAR (020)](https://github.com/jeremylongshore/claude-code-plugins-nixtla/blob/main/000-docs/020-AA-AACR-phase-06-ci-and-marketplace-hardening.md)** – CI + marketplace finalization.
- **[Phase 7 AAR (021)](https://github.com/jeremylongshore/claude-code-plugins-nixtla/blob/main/000-docs/021-AA-AACR-phase-07-visualization-csv-parametrization.md)** – Plot generation + custom CSV support.
- **[Phase 8 AAR (022)](https://github.com/jeremylongshore/claude-code-plugins-nixtla/blob/main/000-docs/022-AA-AACR-phase-08-timegpt-showdown-and-evals.md)** – TimeGPT integration + showdown reports.
- **[Phase 6 TimeGPT Status (032)](https://github.com/jeremylongshore/claude-code-plugins-nixtla/blob/main/000-docs/032-AA-STAT-phase-06-timegpt-showdown-status.md)** – Phase 6 status verification.
- **[Phase 6 TimeGPT AAR (033)](https://github.com/jeremylongshore/claude-code-plugins-nixtla/blob/main/000-docs/033-AA-AACR-phase-06-timegpt-showdown.md)** – Phase 6 AAR (optional TimeGPT showdown).

### Testing Documentation

- **[Test Coverage Report (023)](https://github.com/jeremylongshore/claude-code-plugins-nixtla/blob/main/000-docs/023-QA-TEST-nixtla-baseline-lab-test-coverage.md)** – Comprehensive test coverage mapping.

---

## Collaboration & Contact

**Maintained by**: [Intent Solutions](https://intentsolutions.io) (Jeremy Longshore)
**Sponsored by**: [Nixtla](https://nixtla.io) (Max Mergenthaler – early/enterprise supporter)

**For questions or collaboration**:

- **Jeremy Longshore**: jeremy@intentsolutions.io | 251.213.1115
- **Max Mergenthaler**: max@nixtla.io

---

## Official Nixtla Resources

For official Nixtla documentation, support, and resources:

- [Nixtla Documentation](https://docs.nixtla.io/)
- [statsforecast GitHub](https://github.com/Nixtla/statsforecast)
- [TimeGPT Documentation](https://docs.nixtla.io/docs/getting-started-timegpt)
- [Nixtla Community Slack](https://join.slack.com/t/nixtlaworkspace/shared_invite/zt-135dssye9-fWTzMpv2WBthq8NK0Yvu6A)

---

*This is a community integration maintained by Intent Solutions. For official Nixtla products and support, visit [nixtla.io](https://nixtla.io).*
