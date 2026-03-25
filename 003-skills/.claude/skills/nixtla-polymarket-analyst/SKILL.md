---
name: nixtla-polymarket-analyst
description: "Analyze and forecast Polymarket contracts using TimeGPT with confidence intervals. Use when predicting contract prices or evaluating prediction market trends. Trigger with 'Polymarket analysis', 'forecast prediction market', or 'analyze contract'."
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
compatible-with: claude-code
tags: [nixtla, time-series, forecasting, polymarket, prediction-markets, trading]
allowed-tools: "Read,Write,Bash(python:*),Glob,Grep,WebFetch"
---

# Polymarket Analyst

Analyzes and forecasts Polymarket prediction market contract prices using historical data and TimeGPT forecasting models.

## Overview

This skill fetches Polymarket contract data via API, transforms it into Nixtla time series format, and generates probabilistic forecasts using TimeGPT. The agent produces price forecasts with confidence intervals, trend analysis, and trading signals. Outputs include CSV forecasts, visualizations, and analysis reports with risk disclaimers.

**When to use**: Seeking data-driven insights on prediction market contracts, forecasting contract price movements, or generating buy/sell/hold signals with confidence intervals.

**Trigger phrases**: "Polymarket analysis", "forecast prediction market", "analyze contract", "prediction market forecast", "contract price forecast".

## Prerequisites

**Required Tools**: Read, Write, Bash, Glob, Grep, WebFetch

**Environment Variables**:
- `NIXTLA_TIMEGPT_API_KEY` - Required for TimeGPT forecasting (get at https://dashboard.nixtla.io)

**Python Packages**:
```bash
pip install nixtla pandas requests matplotlib
```

**Script Files**: All Python scripts are located in `{baseDir}/scripts/`:
- `fetch_contract.py` - Fetches contract data from Polymarket API
- `transform_data.py` - Transforms data to Nixtla format (unique_id, ds, y)
- `forecast_contract.py` - Generates TimeGPT forecasts with confidence intervals
- `analyze_polymarket.py` - Complete end-to-end analysis pipeline

## Instructions

### Step 1: Verify Environment

Check that the TimeGPT API key is configured:
```bash
echo $NIXTLA_TIMEGPT_API_KEY
```

If not set, instruct the user to export their API key before proceeding.

### Step 2: Fetch Contract Data

Retrieve contract metadata and historical prices using the fetch script:
```bash
python {baseDir}/scripts/fetch_contract.py <condition_id> --days 30
```

This creates `contract_{id}_data.json` with the contract question, description, volume, liquidity, and hourly price history.

### Step 3: Transform to Time Series Format

Convert raw Polymarket data to Nixtla format (unique_id, ds, y columns):
```bash
python {baseDir}/scripts/transform_data.py contract_{id}_data.json
```

Output: `contract_{id}_nixtla.csv` ready for forecasting. The script validates data quality and warns about insufficient data points.

### Step 4: Generate Forecasts

Run TimeGPT forecasting with specified horizon and frequency:
```bash
python {baseDir}/scripts/forecast_contract.py contract_{id}_nixtla.csv \
  --horizon 48 --freq H --output forecast_results
```

Generates forecast CSV with confidence intervals (80%, 90%, 95%), visualization plot, and metadata JSON with trend/signal analysis.

### Step 5: Complete Pipeline (Alternative)

For end-to-end analysis in one command:
```bash
python {baseDir}/scripts/analyze_polymarket.py <condition_id> \
  --horizon 48 --days 30 --output-dir ./results
```

### Interpretation Guidelines

**Trend Classification**:
- BULLISH: Expected price increase > 5% (Signal: BUY)
- BEARISH: Expected price decrease > 5% (Signal: SELL)
- NEUTRAL: Expected change between -5% and +5% (Signal: HOLD)

**Confidence Intervals**: 95% CI shows the range where the true price is likely to fall. Wide intervals indicate higher uncertainty and lower signal reliability.

**Risk Factors**: Consider market liquidity, trading volume, time until contract resolution, and external events that may affect outcomes before acting on signals.

## Output

1. **Historical Data CSV** - Nixtla-formatted time series
2. **Forecast CSV** - Predictions with confidence intervals at 80%, 90%, and 95% levels
3. **Visualization PNG** - Chart showing historical prices, forecast, and confidence bands
4. **Analysis JSON** - Complete metadata including current price, forecast price, expected change, trend classification, signal, and contract metadata

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Invalid contract ID | Incorrect condition_id | Verify ID from Polymarket URL (hexadecimal string) |
| API key not set | Missing env variable | `export NIXTLA_TIMEGPT_API_KEY='your-key'` |
| Insufficient data | New or low-activity contract | Increase `--days` parameter; minimum 10-20 data points |
| API rate limit | Too many requests | Wait 60 seconds and retry; cache fetched data |
| Connection timeout | Network or API issues | Verify connectivity; check API status |

## Examples

See [examples](references/examples.md) for detailed usage patterns including election contracts, crypto price contracts, and step-by-step pipeline analysis.

## Resources

- **Polymarket API Docs**: https://docs.polymarket.com/
- **TimeGPT Documentation**: https://docs.nixtla.io/
- **Nixtla Format Specification**: https://docs.nixtla.io/docs/tutorials/nixtla_format

**Risk Disclaimer**: Forecasts are probabilistic estimates, not guarantees. Past performance does not indicate future results. This is not financial advice. Always verify data before making trading decisions.
