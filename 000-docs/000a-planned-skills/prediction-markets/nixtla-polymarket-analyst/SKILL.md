---
name: nixtla-polymarket-analyst
description: >
  Analyzes Polymarket prediction market contracts and forecasts price movements using TimeGPT.
  Activates when analyzing prediction markets, forecasting contract outcomes, or evaluating market sentiment.
  Triggers on: "Polymarket analysis", "predict contract odds", "forecast prediction market".
allowed-tools: "Read,Write,Bash,Glob,Grep,WebFetch"
version: "1.0.0"
---

# Polymarket Analyst

Analyzes and forecasts Polymarket prediction market contract prices using historical data and TimeGPT forecasting models.

## Overview

This skill fetches Polymarket contract data via API, transforms it into Nixtla time series format, and generates probabilistic forecasts using TimeGPT. The agent produces price forecasts with confidence intervals, trend analysis, and trading signals. Useful for traders and analysts seeking data-driven insights on prediction markets. Outputs include CSV forecasts, visualizations, and analysis reports with risk disclaimers.

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

The agent should follow this workflow when analyzing Polymarket contracts:

### Step 1: Verify Environment

Check that the TimeGPT API key is configured:
```bash
echo $NIXTLA_TIMEGPT_API_KEY
```

If not set, instruct the user to export their API key.

### Step 2: Fetch Contract Data

Use the fetch script to retrieve contract metadata and historical prices:
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
  --horizon 48 \
  --freq H \
  --output forecast_results
```

Generates:
- `forecast_results_forecast.csv` - Predicted prices with confidence intervals (80%, 90%, 95%)
- `forecast_results_plot.png` - Visualization of historical vs forecast
- `forecast_results_metadata.json` - Analysis with trend, signal, and metadata

### Step 5: Complete Pipeline (Alternative)

For end-to-end analysis in one command:
```bash
python {baseDir}/scripts/analyze_polymarket.py <condition_id> \
  --horizon 48 \
  --days 30 \
  --output-dir ./results
```

This runs all steps automatically and produces complete analysis outputs.

### Interpretation Guidelines

The agent should interpret forecast results as follows:

**Trend Classification**:
- BULLISH: Expected price increase > 5% (Signal: BUY)
- BEARISH: Expected price decrease > 5% (Signal: SELL)
- NEUTRAL: Expected change between -5% and +5% (Signal: HOLD)

**Confidence Intervals**: 95% CI shows the range where the true price is likely to fall. Wide intervals indicate higher uncertainty.

**Risk Factors**: Consider market liquidity, trading volume, time until contract resolution, and external events that may affect outcomes.

## Output

The agent generates these artifacts:

1. **Historical Data CSV** (`polymarket_{id}_historical.csv`) - Nixtla-formatted time series
2. **Forecast CSV** (`polymarket_{id}_forecast.csv`) - Predictions with confidence intervals
3. **Visualization PNG** (`polymarket_{id}_plot.png`) - Chart showing historical prices, forecast, and confidence bands
4. **Analysis JSON** (`polymarket_{id}_analysis.json`) - Complete metadata including:
   - Current price and forecast price
   - Expected change percentage
   - Trend classification and signal
   - Confidence bounds
   - Contract metadata (question, volume, liquidity)

## Error Handling

**Error: Invalid contract ID**
- **Cause**: Incorrect or malformed condition_id
- **Solution**: Verify the ID from the Polymarket URL or API. Format is typically a hexadecimal string.

**Error: NIXTLA_TIMEGPT_API_KEY not set**
- **Cause**: Environment variable not configured
- **Solution**: `export NIXTLA_TIMEGPT_API_KEY='your-key-here'`

**Error: Insufficient data**
- **Cause**: Contract is too new or has low trading activity
- **Solution**: Increase `--days` parameter or wait for more trading history. Minimum 10-20 data points recommended.

**Error: API rate limit exceeded**
- **Cause**: Too many requests to Polymarket or Nixtla APIs
- **Solution**: Wait 60 seconds and retry. Consider caching fetched data for repeated analyses.

**Error: Connection timeout**
- **Cause**: Network issues or API downtime
- **Solution**: Verify internet connectivity. Check Polymarket API status. Increase timeout in fetch_contract.py if needed.

## Examples

### Example 1: Election Contract

**User Request**: "Analyze the 2024 election contract 0x1234abcd with 48-hour forecast"

**Agent Actions**:
```bash
python {baseDir}/scripts/analyze_polymarket.py 0x1234abcd --horizon 48 --days 60
```

**Expected Output**:
```
Contract: "Will candidate X win the 2024 election?"
Current Price: $0.4500
Forecast Price: $0.5200
Expected Change: +15.56%
Signal: BUY (BULLISH)
95% CI: [0.4800, 0.5600]
```

**Interpretation**: The model predicts a 15.56% increase in the "yes" price, suggesting growing confidence in the outcome. The tight confidence interval indicates reasonable certainty.

### Example 2: Crypto Price Contract

**User Request**: "What's the forecast for the ETH price contract?"

**Agent Actions**:
```bash
python {baseDir}/scripts/analyze_polymarket.py 0xdef456 --horizon 24 --days 14
```

**Expected Output**:
```
Contract: "Will ETH be above $3000 on Dec 31?"
Current Price: $0.6800
Forecast Price: $0.6500
Expected Change: -4.41%
Signal: HOLD (NEUTRAL)
95% CI: [0.6000, 0.7000]
```

**Interpretation**: The model predicts a slight decrease, but within the neutral range. Wide confidence interval suggests uncertainty. No strong trading signal.

## Resources

- **Polymarket API Docs**: https://docs.polymarket.com/
- **TimeGPT Documentation**: https://docs.nixtla.io/
- **Nixtla Format Specification**: https://docs.nixtla.io/docs/tutorials/nixtla_format
- **Prediction Market Background**: https://en.wikipedia.org/wiki/Prediction_market

**Risk Disclaimer**: Forecasts are probabilistic estimates, not guarantees. Past performance does not indicate future results. This is not financial advice. Always verify data before making trading decisions.
