---
name: nixtla-market-risk-analyzer
description: "Analyze market risk with VaR, volatility, and position sizing using forecast data. Use when assessing investment risk, calculating portfolio metrics, or determining position sizes. Trigger with 'analyze market risk', 'calculate VaR', or 'position sizing'."
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
compatible-with: claude-code
tags: [nixtla, time-series, risk-analysis, VaR, portfolio, position-sizing]
allowed-tools: "Read,Write,Bash(python:*),Glob,Grep"
---

# Market Risk Analyzer

Calculates key market risk metrics and recommends optimal position sizes using historical data analysis.

## Overview

This skill analyzes market risk using historical price data to calculate Value at Risk (VaR), volatility metrics, maximum drawdown, Sharpe ratios, and optimal position sizing. It provides actionable insights for managing investment risk and optimizing portfolio allocation. The workflow uses four specialized Python scripts for data preparation, risk analysis, position sizing, and report generation.

**When to use**: Assessing portfolio risk exposure, determining trade position sizes, evaluating risk-adjusted returns, or generating comprehensive risk reports with visualizations.

**Trigger phrases**: "analyze market risk", "calculate VaR", "position sizing", "volatility analysis", "drawdown report", "Sharpe ratio".

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep

**Environment**: Optional `NIXTLA_TIMEGPT_API_KEY` for volatility forecasting (not required for core analysis)

**Packages**:
```bash
pip install pandas numpy scipy matplotlib
# Optional for forecasting:
pip install nixtla
```

**Input Data Format**: CSV file with columns:
- Date column: `ds`, `date`, or `timestamp`
- Price column: `y`, `price`, or `close`

## Instructions

### Step 1: Prepare Price Data

Execute the data preparation script to load prices and calculate returns:

```bash
python {baseDir}/scripts/prepare_data.py prices.csv --method log --output returns.csv
```

**Script**: `{baseDir}/scripts/prepare_data.py` - Loads price data from CSV, calculates log or simple returns, detects time series frequency, and outputs `returns.csv`.

### Step 2: Calculate Risk Metrics

Run comprehensive risk analysis on the price data:

```bash
python {baseDir}/scripts/risk_metrics.py prices.csv --output risk_metrics.json --risk-free-rate 0.05
```

**Script**: `{baseDir}/scripts/risk_metrics.py` - Calculates VaR at 95% and 99% confidence levels, computes historical and rolling volatility, analyzes maximum drawdown and recovery periods, and calculates Sharpe and Sortino ratios.

**Key Metrics**:
- **VaR**: Maximum expected loss at confidence level
- **CVaR**: Expected loss when VaR is exceeded
- **Volatility**: Daily and annualized, with regime classification (HIGH/NORMAL/LOW)
- **Drawdown**: Maximum loss from peak, recovery analysis
- **Sharpe Ratio**: Risk-adjusted return metric

### Step 3: Calculate Position Sizing

Determine optimal position sizes using multiple methodologies:

```bash
python {baseDir}/scripts/position_sizing.py \
  --account-size 100000 \
  --risk-per-trade 0.02 \
  --stop-loss 0.05 \
  --target-volatility 0.15 \
  --asset-volatility 0.25 \
  --var-95 -0.02 \
  --max-var-loss 0.03 \
  --output position_sizing.json
```

**Script**: `{baseDir}/scripts/position_sizing.py` - Computes Fixed Fractional, Volatility Adjusted, VaR-Based, and Kelly Criterion sizing methods. Outputs `position_sizing.json` with the most conservative recommended position.

### Step 4: Generate Risk Report

Create a comprehensive markdown report with visualizations:

```bash
python {baseDir}/scripts/generate_report.py prices.csv \
  --risk-metrics risk_metrics.json \
  --position-sizing position_sizing.json \
  --output risk_report.md \
  --output-dir .
```

**Script**: `{baseDir}/scripts/generate_report.py` - Generates markdown report with all metrics, plus three visualizations: `drawdown.png`, `volatility.png`, and `var.png`.

## Output

**Generated Files**:
- `returns.csv`: Calculated returns series
- `risk_metrics.json`: Complete risk metrics (VaR, volatility, drawdown, ratios)
- `position_sizing.json`: Position sizing recommendations across all methods
- `risk_report.md`: Comprehensive markdown report with 7 sections
- `drawdown.png`, `volatility.png`, `var.png`: Risk visualizations

## Error Handling

See [error handling reference](references/error-handling.md) for detailed troubleshooting of common issues including column detection, data sufficiency, and dependency errors.

## Examples

See [examples](references/examples.md) for detailed usage patterns including stock analysis, prediction market contracts, and custom risk parameter comparisons.

## Resources

See [resources reference](references/resources.md) for statistical method descriptions, position sizing theory, best practices, and academic references.

**Related skills**:
- `nixtla-liquidity-forecaster` - Orderbook depth and spread forecasting
- `nixtla-uncertainty-quantifier` - Conformal prediction intervals
