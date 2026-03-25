---
name: nixtla-correlation-mapper
description: "Analyze multi-contract correlations for forecast-based hedge recommendations. Use when managing correlated assets. Trigger with 'analyze correlations' or 'suggest hedge'."
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
compatible-with: claude-code
tags: [nixtla, time-series, forecasting, correlation, hedging]
allowed-tools: "Read,Write,Bash(python:*),Glob,Grep"
---

# Nixtla Correlation Mapper

Identifies correlations between multiple contracts and generates hedging strategies for portfolio risk management.

## Overview

Analyzes relationships between assets in a portfolio to suggest hedging strategies. Takes CSV data with multiple time series, calculates correlation matrix, identifies significant relationships, and outputs hedge recommendations with visualizations. Generates correlation heatmap, rolling correlation plots, and hedge effectiveness charts.

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep

**Environment**: None required (optional: `NIXTLA_TIMEGPT_API_KEY` for forecasted correlations)

**Packages**:
```bash
pip install pandas numpy scipy matplotlib seaborn
```

**Input Format**: CSV with columns: `unique_id` (contract identifier), `ds` (date), `y` (price/value)

## Instructions

### Step 1: Prepare Data

Load multi-series contract data and calculate returns. Uses `{baseDir}/scripts/prepare_data.py`.

```bash
python scripts/prepare_data.py contracts.csv --method log --output-dir results/
```

**Output**: `prices_wide.csv`, `returns.csv`

### Step 2: Calculate Correlations

Calculate correlation matrix and identify significant pairs. Uses `{baseDir}/scripts/correlation_analysis.py`.

```bash
python scripts/correlation_analysis.py \
  --returns results/returns.csv \
  --method pearson \
  --threshold 0.5 \
  --rolling-window 30 \
  --output-dir results/
```

**Output**: `correlation_matrix.csv`, `correlation_pvalues.csv`, `high_correlations.json`, `rolling_correlations.csv`

### Step 3: Generate Hedge Recommendations

Calculate optimal hedge ratios using regression or minimum variance methods. Uses `{baseDir}/scripts/hedge_recommendations.py`.

```bash
python scripts/hedge_recommendations.py \
  --returns results/returns.csv \
  --correlation results/correlation_matrix.csv \
  --method ols \
  --top-n 10 \
  --portfolio-value 100000 \
  --output-dir results/
```

**Output**: `hedge_recommendations.csv`, `hedge_recommendations.json`, `hedged_portfolio.csv`

### Step 4: Create Visualizations

Generate correlation heatmap, rolling correlation plot, and hedge effectiveness chart. Uses `{baseDir}/scripts/visualize.py`.

```bash
python scripts/visualize.py \
  --correlation results/correlation_matrix.csv \
  --rolling results/rolling_correlations.csv \
  --recommendations results/hedge_recommendations.json \
  --output-dir results/ \
  --top-n 5
```

**Output**: `correlation_heatmap.png`, `rolling_correlation.png`, `hedge_effectiveness.png`

### Step 5: Generate Report

Create comprehensive markdown report with all analysis results. Uses `{baseDir}/scripts/generate_report.py`.

```bash
python scripts/generate_report.py \
  --correlation results/correlation_matrix.csv \
  --high-correlations results/high_correlations.json \
  --recommendations results/hedge_recommendations.json \
  --output results/correlation_report.md
```

**Output**: `correlation_report.md`

## Output

See [output reference](references/outputs.md) for the complete list of generated files.

## Error Handling

See [error handling](references/error-handling.md) for common errors and solutions.

## Examples

See [examples](references/examples.md) for detailed usage patterns.

## Resources

**Scripts**: All analysis scripts located in `{baseDir}/scripts/`
- `prepare_data.py`: Data loading, pivoting, returns calculation
- `correlation_analysis.py`: Correlation matrix, p-values, rolling correlations
- `hedge_recommendations.py`: Hedge ratios, portfolio allocation
- `visualize.py`: Heatmaps, rolling plots, effectiveness charts
- `generate_report.py`: Comprehensive markdown report

**Correlation Methods**: Pearson (linear), Spearman (rank-based), Kendall (concordance)

**Hedge Methods**: OLS regression (standard), Minimum variance (risk-minimizing)

**Interpretation**:
- Strong correlation: |r| > 0.7 (high co-movement)
- Moderate: 0.3 < |r| < 0.7 (partial relationship)
- Weak: |r| < 0.3 (minimal relationship)
- Negative correlation: r < -0.5 (good hedge potential)
