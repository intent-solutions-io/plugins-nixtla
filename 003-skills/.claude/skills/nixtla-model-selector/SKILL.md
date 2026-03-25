---
name: nixtla-model-selector
description: "Automatically selects the best forecasting model between StatsForecast and TimeGPT based on time series data characteristics. Use when unsure which model performs best for a dataset. Trigger with 'auto-select model', 'choose best model', 'model selection'."
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
compatible-with: claude-code
tags: [nixtla, time-series, forecasting, model-selection, statsforecast, timegpt]
allowed-tools: "Read,Write,Bash(python:*),Glob,Grep"
---

# Nixtla Model Selector

Automatically selects and executes the optimal forecasting model for time series data.

## Overview

This skill analyzes time series data characteristics to determine whether StatsForecast or TimeGPT will yield more accurate forecasts. It evaluates data length, frequency, seasonality, missing values, and series count to make an intelligent selection. The skill then executes the chosen model and returns forecasts with selection rationale, eliminating manual model selection and experimentation cycles.

**When to use**: Deciding between StatsForecast and TimeGPT for a forecasting task, or when the optimal model for a dataset is unknown.

**Trigger phrases**: "auto-select model", "choose best model", "model selection", "which forecasting model", "compare models".

**Decision Logic**:
- **StatsForecast**: Selected for missing values, short data (<30 points), seasonal patterns, or many series (>100)
- **TimeGPT**: Selected for long, non-seasonal data with complete observations

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep

**Environment**: `NIXTLA_TIMEGPT_API_KEY` (required if TimeGPT is selected)

**Packages**:
```bash
pip install statsforecast nixtla pandas matplotlib statsmodels
```

**Input Format**: CSV file with columns `unique_id`, `ds` (datetime), `y` (target values)

## Instructions

### Step 1: Prepare and Validate Data

Read the input CSV file and validate the required schema. The data must contain `unique_id` (series identifier), `ds` (timestamp), and `y` (observations). The script converts timestamps to datetime format and infers the frequency (daily, hourly, etc.).

Execute: `python {baseDir}/scripts/model_selector.py --input data.csv --visualize`

### Step 2: Analyze Data Characteristics

The script analyzes the time series to extract decision criteria:
- **Data length**: Number of observations per series
- **Missing values**: Presence of null values in target variable
- **Seasonality**: Detects seasonal patterns using statistical decomposition
- **Series count**: Number of unique time series in the dataset

The analysis uses seasonal decomposition to identify seasonal components and compares seasonal variance against total variance using a heuristic threshold.

### Step 3: Select and Execute Model

Based on the analysis, the script applies decision rules:

1. **Missing values detected** -> StatsForecast (handles missing data robustly)
2. **Data length < 30** -> StatsForecast (insufficient data for TimeGPT)
3. **Seasonality present** -> StatsForecast (specialized seasonal models)
4. **Series count > 100** -> StatsForecast (efficient batch processing)
5. **Otherwise** -> TimeGPT (optimal for long, complex patterns)

**StatsForecast execution**: Uses AutoETS and AutoARIMA with parallel processing. **TimeGPT execution**: Requires API key, calls cloud API with inferred frequency.

Default horizon: 14 periods (customizable via `--horizon` flag).

### Step 4: Generate Output

The script saves two output files:

1. **forecast.csv**: Predictions with columns `unique_id`, `ds`, `model`, `yhat` in long format
2. **model_selection.txt**: Selection report with model name, reason, and record count

Complete workflow:
```bash
python {baseDir}/scripts/model_selector.py --input data.csv --output forecast.csv --horizon 30
```

## Output

- **forecast.csv**: Time series predictions in long format (one row per forecast point)
- **model_selection.txt**: Model selection report with rationale and data characteristics
- **time_series_plot.png** (optional): Input data visualization when `--visualize` flag is used

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Input file not found | Invalid file path | Verify file path and check permissions |
| Invalid data format | Missing required columns | Ensure CSV contains `unique_id`, `ds`, `y` |
| NIXTLA_TIMEGPT_API_KEY not set | API key missing | `export NIXTLA_TIMEGPT_API_KEY="your_key"` |
| Could not infer frequency | Irregular timestamps | Ensure `ds` column has consistent intervals |
| Seasonality check failed | Insufficient data | Provide 24+ observations; falls back to non-seasonal |

## Examples

See [examples](references/examples.md) for detailed usage patterns including short seasonal data, long non-seasonal data, and multi-series datasets with missing values.

## Resources

- **Script**: `{baseDir}/scripts/model_selector.py`
- **StatsForecast Documentation**: https://nixtla.github.io/statsforecast/
- **TimeGPT API Reference**: https://docs.nixtla.io/
- **Related skills**: `nixtla-cross-validator`, `nixtla-benchmark-reporter`
