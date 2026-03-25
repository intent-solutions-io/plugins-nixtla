---
name: nixtla-event-impact-modeler
description: "Analyze causal impact of events on time series forecasts using TimeGPT. Use when quantifying promotion or disaster effects. Trigger with 'event impact analysis' or 'causal analysis'."
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
compatible-with: claude-code
tags: [nixtla, time-series, forecasting, causal-impact, event-analysis]
allowed-tools: "Read,Write,Bash(python:*),Glob,Grep,WebSearch"
---

# Nixtla Event Impact Modeler

Quantifies the causal impact of exogenous events on contract prices using TimeGPT forecasting and CausalImpact analysis.

## Overview

This skill analyzes how external events (promotions, natural disasters, policy changes) affect contract prices over time. It combines historical price data with event details to quantify causal impacts using MCMC-based counterfactual modeling and TimeGPT forecasting. The skill produces impact estimates, adjusted forecasts, and visualizations for event-driven price changes.

**Use cases**: Promotion effectiveness analysis, disaster impact quantification, policy change assessment, pricing anomaly investigation, event-aware forecasting.

## Prerequisites

**Environment**:
- `NIXTLA_TIMEGPT_API_KEY` (required for TimeGPT forecasting)

**Dependencies**:
```bash
pip install nixtla pandas causalimpact matplotlib
```

**Input requirements**:
- `prices.csv`: Contract prices with columns `ds` (datetime), `price` (numeric)
- `events.csv`: Event data with columns `ds` (datetime), `event` (string description)

## Instructions

### Step 1: Prepare data

Load and validate contract price and event data using the data preparation script.

```bash
python {baseDir}/scripts/prepare_data.py \
  --prices prices.csv \
  --events events.csv \
  --output-prices prepared_prices.csv \
  --output-events prepared_events.csv
```

**To create sample data for testing**:
```bash
python {baseDir}/scripts/prepare_data.py --create-sample
```

**Script actions**:
- Loads CSV files with datetime parsing
- Validates required columns (`ds`, `price`/`event`)
- Renames columns to Nixtla standard (`y` for price)
- Adds default `unique_id` if missing
- Outputs prepared CSVs for analysis

### Step 2: Configure model

Define event windows and mark treatment/control periods in the price data.

```bash
python {baseDir}/scripts/configure_model.py \
  --prices prepared_prices.csv \
  --events prepared_events.csv \
  --window-days 3 \
  --output configured_prices.csv
```

**Script actions**:
- Defines event periods with configurable window (default: 3 days before/after)
- Validates event dates fall within price data range
- Creates `treatment` column (1=treatment period, 0=control period)
- Outputs configured DataFrame with treatment markers

**Parameters**:
- `--window-days`: Event window size in days (default: 3)

### Step 3: Execute analysis

Run CausalImpact analysis with TimeGPT forecasting to quantify event effects.

```bash
python {baseDir}/scripts/analyze_impact.py \
  --prices configured_prices.csv \
  --events prepared_events.csv \
  --niter 1000 \
  --window-days 3 \
  --output-impact impact_results.csv \
  --output-forecast adjusted_forecast.csv \
  --output-summary causal_summary.txt
```

**Script actions**:
- Defines pre-intervention and post-intervention periods
- Runs CausalImpact MCMC analysis (configurable iterations)
- Calculates absolute and relative event effects
- Generates TimeGPT adjusted forecasts
- Outputs impact metrics, forecasts, and summary report

**Parameters**:
- `--niter`: MCMC iterations for CausalImpact (default: 1000)
- `--window-days`: Event window size (must match Step 2)

### Step 4: Generate report

Create visualization and markdown report summarizing the analysis.

```bash
python {baseDir}/scripts/generate_report.py \
  --impact-results impact_results.csv \
  --adjusted-forecast adjusted_forecast.csv \
  --causal-summary causal_summary.txt \
  --output-plot impact_plot.png \
  --output-report impact_report.md \
  --title "Event Impact on Contract Prices"
```

**Script actions**:
- Generates time series plot with actual prices, forecasts, and treatment periods
- Creates markdown report with impact metrics, CausalImpact summary, and methodology
- Outputs high-resolution PNG and structured markdown report

## Output

- `impact_results.csv`: Absolute and relative event effects with confidence intervals
- `adjusted_forecast.csv`: TimeGPT forecasts adjusted for identified event impacts
- `impact_report.md`: Structured markdown report with methodology and findings
- `impact_plot.png`: Time series visualization with treatment periods highlighted

See [output files](references/outputs.md) for full schema and metric definitions.

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Missing NIXTLA_TIMEGPT_API_KEY | API key not set | Export key: `export NIXTLA_TIMEGPT_API_KEY=your_key` |
| Event dates outside price range | Events fall outside time series bounds | Ensure events overlap with price data |
| CausalImpact convergence failure | Insufficient data or iterations | Increase `--niter` or extend price history |

See [error handling](references/error-handling.md) for additional troubleshooting.

## Examples

See [examples](references/examples.md) for detailed usage scenarios including promotion analysis and disaster impact quantification.

## Resources

**Scripts** (all in `{baseDir}/scripts/`):
- `prepare_data.py`: Data loading and validation with argparse CLI
- `configure_model.py`: Event period configuration and treatment/control marking
- `analyze_impact.py`: CausalImpact + TimeGPT analysis engine
- `generate_report.py`: Visualization and markdown report generation

**Documentation**:
- [Nixtla TimeGPT API](https://docs.nixtla.io/)
- [CausalImpact Python](https://github.com/jamalsenouci/causalimpact)
- [StatsForecast Documentation](https://nixtla.github.io/statsforecast/)
