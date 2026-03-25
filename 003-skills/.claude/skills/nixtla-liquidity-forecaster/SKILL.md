---
name: nixtla-liquidity-forecaster
description: "Forecasts orderbook depth and spreads to optimize trade execution timing. Use when needing to estimate market liquidity for large orders or predicting bid-ask spread evolution. Trigger with 'forecast liquidity', 'predict orderbook', 'estimate depth'."
allowed-tools: "Read,Write,Bash(python:*),Glob,Grep,WebFetch"
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
compatible-with: claude-code
tags: [nixtla, time-series, forecasting, liquidity, polymarket, orderbook]
---

# Liquidity Forecaster

Predicts future orderbook depth and bid-ask spreads using historical market data and TimeGPT.

## Overview

This skill analyzes historical trade data and orderbook snapshots from Polymarket to forecast liquidity conditions. It predicts near-term changes in orderbook depth and bid-ask spreads, helping determine optimal trade execution timing. The workflow fetches data via Polymarket API, preprocesses it for TimeGPT compatibility, and generates forecasts with visualizations and reports.

**When to use**: Determining optimal trade execution timing based on expected liquidity conditions, predicting orderbook depth changes, estimating bid-ask spread evolution.

**Trigger phrases**: "forecast liquidity", "predict orderbook depth", "estimate spread changes", "analyze market liquidity", "forecast trading conditions".

## Prerequisites

**Required environment variables**:
- `NIXTLA_TIMEGPT_API_KEY` - Your Nixtla TimeGPT API key

**Python packages**:
```bash
pip install nixtla pandas requests matplotlib
```

**Required tools**: Read, Write, Bash, Glob, Grep, WebFetch

**Minimum Python version**: 3.8+

## Instructions

### Step 1: Fetch orderbook data

Fetch historical orderbook data from Polymarket API using the market ID. The script retrieves bids and asks, combines them into a single dataset, and saves to CSV format.

**Script**: `{baseDir}/scripts/fetch_data.py`

```bash
python {baseDir}/scripts/fetch_data.py --market_id <MARKET_ID> [--output orderbook_data.csv]
```

**Parameters**:
- `--market_id` (required): Polymarket market identifier
- `--output` (optional): Output CSV file path (default: orderbook_data.csv)

### Step 2: Preprocess data

Clean and format orderbook data for TimeGPT input. The script calculates mid-price, spread, and depth metrics, then formats the data according to Nixtla's schema requirements (unique_id, ds, y columns).

**Script**: `{baseDir}/scripts/preprocess_data.py`

```bash
python {baseDir}/scripts/preprocess_data.py --input_file orderbook_data.csv [--output preprocessed_data.csv]
```

### Step 3: Execute forecast

Run TimeGPT forecast on preprocessed data. The script generates predictions for the specified horizon, creates visualizations, and produces a summary report.

**Script**: `{baseDir}/scripts/forecast_liquidity.py`

```bash
python {baseDir}/scripts/forecast_liquidity.py --input_file preprocessed_data.csv --horizon <PERIODS> [--output depth_forecast.csv] [--plot_prefix depth]
```

### Step 4: Interpret results

Review the generated outputs to understand predicted liquidity conditions. The forecast CSV contains time-indexed predictions, the plot visualizes historical data overlaid with forecast values, and the report provides metadata about the forecasting run including market ID and horizon settings.

## Output

**Generated files**:
- `depth_forecast.csv` - Time-series predictions for orderbook depth and mid-price
- `depth_forecast.png` - Visualization showing historical data and forecast overlay
- `report.txt` - Summary report with market ID, horizon, and output file paths

**CSV format**: Columns include unique_id, ds (timestamp), y (predicted mid-price), and optional spread/depth metrics.

## Error Handling

See [error handling reference](references/error-handling.md) for detailed troubleshooting of common issues including invalid market IDs, missing API keys, and data format problems.

## Examples

See [examples](references/examples.md) for detailed usage patterns including election markets, cryptocurrency contracts, and sports prediction markets.

## Resources

**Nixtla documentation**:
- TimeGPT API reference: https://docs.nixtla.io/
- Data format requirements: https://docs.nixtla.io/docs/tutorials-forecasting_with_timegpt

**Polymarket API**:
- API documentation: https://docs.polymarket.com/
- Market explorer: https://polymarket.com/markets

**Related skills**:
- `nixtla-timegpt-lab` - General TimeGPT forecasting workflows
- `nixtla-schema-mapper` - Data format transformation utilities
