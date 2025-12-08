---
name: nixtla-timegpt-lab
description: |
  Provides expert time series forecasting capabilities by leveraging TimeGPT, StatsForecast, and MLForecast.
  Use when forecasting time series data, analyzing past trends, or generating predictions.
  Trigger with "time series forecast", "predict future values", "analyze time trends".
allowed-tools: "Read,Write,Bash,Glob,Grep"
version: "1.0.0"
---

# Nixtla TimeGPT Lab

Provides accurate time series forecasting using TimeGPT, StatsForecast, and MLForecast.

## Purpose

To generate forecasts from historical time series data.

## Overview

This skill allows users to perform time series forecasting using the Nixtla ecosystem. It encompasses data handling, model training/inference (TimeGPT/StatsForecast/MLForecast), and result visualization. Use it when predictions are required for various time series data. The skill outputs forecasts in CSV format, along with visualizations, and key metrics.

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep

**Environment**: `NIXTLA_TIMEGPT_API_KEY` (if using TimeGPT)

**Packages**:
```bash
pip install nixtla pandas statsforecast mlforecast matplotlib
```

## Instructions

### Step 1: Load and prepare data

Read input CSV and ensure correct format (unique_id, ds, y). Handle missing values.

```bash
python {baseDir}/scripts/load_prepare_data.py \
  --input data.csv \
  --output prepared_data.csv \
  --freq D
```

**Parameters**:
- `--input`: Path to input CSV file
- `--output`: Path to save prepared data (default: prepared_data.csv)
- `--freq`: (Optional) Frequency (D=daily, H=hourly, etc.) - auto-detected if omitted

**Requirements**:
- CSV with columns: unique_id, ds, y
- ds column in datetime format
- y column with numeric values

### Step 2: Execute forecasting

Run the selected forecasting model (TimeGPT, StatsForecast, or MLForecast).

```bash
# Using StatsForecast (no API key required)
python {baseDir}/scripts/forecast.py \
  --input prepared_data.csv \
  --model statsforecast \
  --horizon 14 \
  --freq D \
  --output_prefix forecast

# Using TimeGPT (requires API key)
export NIXTLA_TIMEGPT_API_KEY=your_api_key
python {baseDir}/scripts/forecast.py \
  --input prepared_data.csv \
  --model timegpt \
  --horizon 14 \
  --freq D \
  --output_prefix forecast
```

**Parameters**:
- `--input`: Path to prepared CSV file
- `--model`: timegpt, statsforecast, or mlforecast
- `--horizon`: Number of periods to forecast
- `--freq`: Data frequency (D, H, W, M, etc.)
- `--output_prefix`: Prefix for output files (default: forecast)

## Output

- **forecast.csv**: Predictions with confidence intervals
- **forecast.png**: Actual vs predicted visualization
- **forecast_metrics.json**: Accuracy metrics (MAE)

## Error Handling

1. **Error**: `NIXTLA_TIMEGPT_API_KEY not set`
   **Solution**: `export NIXTLA_TIMEGPT_API_KEY=your_key`

2. **Error**: `Invalid input format`
   **Solution**: Ensure CSV has columns named 'unique_id', 'ds', and 'y'

3. **Error**: `Unsupported frequency`
   **Solution**: Specify frequency using --freq parameter (e.g., 'D', 'W', 'M', 'H')

4. **Error**: `Model training failed`
   **Solution**: Check input data for errors, try different model parameters or a different model

5. **Error**: `Could not infer frequency`
   **Solution**: Provide frequency explicitly using --freq parameter

## Examples

### Example 1: Predicting daily sales

**Input**:
```csv
unique_id,ds,y
store_1,2024-01-01,100
store_1,2024-01-02,120
```

**Command**:
```bash
python {baseDir}/scripts/forecast.py \
  --input sales.csv \
  --model statsforecast \
  --horizon 7 \
  --freq D
```

**Output**:
```csv
unique_id,ds,AutoETS,AutoARIMA
store_1,2024-01-03,130,128
```

### Example 2: Forecasting hourly demand

**Input**:
```csv
unique_id,ds,y
grid_1,2024-01-01 00:00,5000
grid_1,2024-01-01 01:00,5100
```

**Command**:
```bash
python {baseDir}/scripts/forecast.py \
  --input demand.csv \
  --model timegpt \
  --horizon 24 \
  --freq H
```

**Output**:
```csv
unique_id,ds,TimeGPT
grid_1,2024-01-02 00:00,5200
```

## Resources

- Data loader: `{baseDir}/scripts/load_prepare_data.py`
- Forecasting engine: `{baseDir}/scripts/forecast.py`
