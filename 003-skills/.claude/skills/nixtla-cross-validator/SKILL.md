---
name: nixtla-cross-validator
description: "Performs rigorous time series cross-validation using expanding and sliding windows. Use when needing to evaluate the performance of time series models on unseen data. Trigger with cross validate time series, evaluate forecasting model, time series backtesting."
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
compatible-with: claude-code
tags: [nixtla, time-series, forecasting, cross-validation, model-evaluation]
allowed-tools: "Read,Write,Bash(python:*),Glob,Grep"
---

# Cross-Validator Skill

Evaluates time series model performance using cross-validation.

## Purpose

Rigorously assesses how well a time series model generalizes to unseen data by simulating future predictions.

## Overview

This skill automates time series cross-validation by splitting historical data into multiple training and validation sets based on expanding or sliding window techniques. It integrates with TimeGPT and StatsForecast to evaluate model performance across various time periods. It reports key accuracy metrics, helping users select the best model.

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep

**Environment**: `NIXTLA_TIMEGPT_API_KEY` (if using TimeGPT)

**Packages**:
```bash
pip install nixtla pandas statsforecast matplotlib
```

## Instructions

### Step 1: Prepare data

Read time series data from CSV file into a pandas DataFrame using the data loader script.

Script: `{baseDir}/scripts/load_data.py`

The script expects a CSV file with columns: `unique_id`, `ds` (timestamp), and `y` (target value).

**Example usage**:
```bash
python {baseDir}/scripts/load_data.py data.csv
```

### Step 2: Configure cross-validation

Define parameters like window size, step size, and number of folds using the configuration script.

Script: `{baseDir}/scripts/configure_cv.py`

The script creates expanding window splits for cross-validation. It validates that the data is sufficient for the specified window size and number of folds.

### Step 3: Execute cross-validation

Run the cross-validation script with your chosen model and parameters.

Script: `{baseDir}/scripts/cross_validate.py`

**Usage**:
```bash
python {baseDir}/scripts/cross_validate.py \
  --input data.csv \
  --model arima \
  --window 20 \
  --folds 3 \
  --freq D
```

**Supported models**:
- `timegpt`: TimeGPT API (requires NIXTLA_TIMEGPT_API_KEY)
- `arima`: AutoARIMA from StatsForecast
- `ets`: AutoETS from StatsForecast
- `theta`: AutoTheta from StatsForecast
- `naive`: SeasonalNaive baseline

### Step 4: Analyze results

The script automatically calculates and outputs cross-validation metrics (MAE, RMSE) for all folds.

## Output

- **cv_results.csv**: CSV file containing the cross-validation results for each fold.
- **metrics.json**: JSON file containing overall performance metrics across all folds.
- **plots/**: Directory containing plots comparing actual vs. predicted values for each fold.

## Error Handling

1. **Error**: `Input file not found`
   **Solution**: Ensure the specified input CSV file exists at the given path.

2. **Error**: `Invalid model name`
   **Solution**: Use a supported model name: 'timegpt', 'arima', 'ets', 'theta', 'naive'.

3. **Error**: `Insufficient data for cross-validation`
   **Solution**: Increase the length of the input time series or reduce the window size.

4. **Error**: `Missing required parameter`
   **Solution**: Specify all required parameters: input, model, window, folds.

5. **Error**: `NIXTLA_TIMEGPT_API_KEY environment variable not set.`
   **Solution**: Set the `NIXTLA_TIMEGPT_API_KEY` environment variable before running the script when using TimeGPT.

## Examples

See [examples](references/examples.md) for detailed usage patterns.

## Resources

- StatsForecast documentation: https://nixtlaverse.nixtla.io/statsforecast/
- TimeGPT API documentation: https://docs.nixtla.io/
- Cross-validation best practices: https://otexts.com/fpp3/tscv.html
- Scripts: `{baseDir}/scripts/` directory contains all executable code
