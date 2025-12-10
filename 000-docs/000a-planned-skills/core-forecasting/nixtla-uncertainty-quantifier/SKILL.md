---
name: nixtla-uncertainty-quantifier
description: |
  Quantifies prediction uncertainty using conformal prediction.
  Use when risk assessment, scenario planning, or decision-making under uncertainty is required.
  Trigger with "quantify uncertainty", "generate prediction intervals", "confidence bands".
allowed-tools: "Read,Write,Bash,Glob,Grep"
version: "1.0.0"
---

# Uncertainty Quantifier

Generates prediction intervals and confidence bands for time series forecasts using conformal prediction.

## Purpose

Provides a measure of the uncertainty associated with time series forecasts, enabling more informed decision-making.

## Overview

Calculates prediction intervals and confidence bands around point forecasts, leveraging conformal prediction techniques. Requires a trained forecasting model (e.g., TimeGPT, StatsForecast) and historical data. Use when point forecasts alone are insufficient and an understanding of forecast uncertainty is needed. Outputs CSV files containing the forecast with uncertainty bounds and visualizations.

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep

**Environment**:
- Requires access to a trained forecasting model (e.g., TimeGPT API Key or StatsForecast model).
- `NIXTLA_TIMEGPT_API_KEY` (if using TimeGPT).

**Packages**:
```bash
pip install nixtla pandas statsforecast matplotlib scikit-learn
```

## Instructions

### Step 1: Generate forecasts

Load historical data and generate point forecasts using StatsForecast.

Script: `{baseDir}/scripts/generate_forecasts.py`

**Usage**:
```bash
python {baseDir}/scripts/generate_forecasts.py \
  --input data.csv \
  --output forecast.csv
```

The script:
- Loads CSV data with `unique_id`, `ds`, `y` columns
- Splits data into training (80%) and validation (20%)
- Trains AutoETS model with weekly seasonality
- Generates forecasts for validation period
- Saves results with columns: unique_id, ds, y, StatsForecast

### Step 2: Quantify uncertainty

Execute the uncertainty quantification script with your chosen confidence level and method.

Script: `{baseDir}/scripts/quantify_uncertainty.py`

**Usage**:
```bash
python {baseDir}/scripts/quantify_uncertainty.py \
  --input forecast.csv \
  --confidence 0.95 \
  --method quantile \
  --forecast_col StatsForecast
```

**Parameters**:
- `--input`: Path to forecast CSV file
- `--confidence`: Confidence level (0.90 for 90%, 0.95 for 95%, etc.)
- `--method`: Conformal prediction method (`quantile` or `jackknife+`)
- `--forecast_col`: Name of the forecast column (default: StatsForecast)

**Methods**:
- **quantile**: Uses calibration set residuals to compute prediction intervals
- **jackknife+**: Uses leave-one-out cross-validation for uncertainty estimation

The script automatically:
1. Calculates conformal prediction intervals
2. Evaluates calibration (coverage, interval width)
3. Generates visualization with confidence bands
4. Saves all outputs

## Output

- **forecast_with_uncertainty.csv**: Predictions with lower and upper bounds of the prediction interval.
- **uncertainty_plot.png**: Visualization of the forecast with confidence bands.
- **calibration_metrics.json**: Metrics evaluating the calibration of the prediction intervals (coverage, interval width).

## Error Handling

1. **Error**: `Input file not found`
   **Solution**: Verify the file path specified in the `--input` argument is correct.

2. **Error**: `Invalid confidence level`
   **Solution**: Specify a confidence level between 0 and 1 (e.g., 0.95 for 95% confidence).

3. **Error**: `Unsupported conformal prediction method`
   **Solution**: Choose a valid conformal prediction method, such as 'quantile' or 'jackknife+'.

4. **Error**: `Forecast file does not contain required columns`
   **Solution**: Ensure the input CSV file contains `unique_id`, `ds`, `y`, and forecast columns (e.g., 'StatsForecast').

5. **Error**: `Data split results in empty calibration set`
   **Solution**: Ensure you have sufficient data for both calibration and evaluation (minimum 10-20 observations).

## Examples

### Example 1: Sales forecast with 90% confidence

**Input (forecast.csv)**:
```csv
unique_id,ds,y,StatsForecast
store_1,2024-01-01,100,95
store_1,2024-01-02,120,115
store_1,2024-01-03,110,112
```

**Command**:
```bash
python {baseDir}/scripts/quantify_uncertainty.py \
  --input forecast.csv \
  --confidence 0.90 \
  --method quantile
```

**Output (forecast_with_uncertainty.csv)**:
```csv
unique_id,ds,y,StatsForecast,lower_bound_90,upper_bound_90
store_1,2024-01-01,100,95.0,85.0,105.0
store_1,2024-01-02,120,115.0,105.0,125.0
store_1,2024-01-03,110,112.0,102.0,122.0
```

### Example 2: Energy demand forecast with 95% confidence

**Input (data.csv)**:
```csv
unique_id,ds,y
grid_1,2024-01-01 00:00,5000
grid_1,2024-01-01 01:00,5100
...
grid_1,2024-01-31 23:00,5200
```

**Commands**:
```bash
# Step 1: Generate forecasts
python {baseDir}/scripts/generate_forecasts.py \
  --input data.csv \
  --output forecast.csv

# Step 2: Quantify uncertainty
python {baseDir}/scripts/quantify_uncertainty.py \
  --input forecast.csv \
  --confidence 0.95 \
  --method jackknife+
```

**Output**: Forecast with 95% prediction intervals for risk-aware energy planning.

### Example 3: Complete workflow

```bash
# Generate forecasts from historical data
python {baseDir}/scripts/generate_forecasts.py \
  --input sales_history.csv \
  --output sales_forecast.csv

# Quantify uncertainty with 90% confidence using quantile method
python {baseDir}/scripts/quantify_uncertainty.py \
  --input sales_forecast.csv \
  --confidence 0.90 \
  --method quantile \
  --forecast_col StatsForecast

# Review outputs:
# - forecast_with_uncertainty.csv (data with intervals)
# - uncertainty_plot.png (visualization)
# - calibration_metrics.json (quality metrics)
```

## Resources

- Conformal prediction overview: https://en.wikipedia.org/wiki/Conformal_prediction
- StatsForecast documentation: https://nixtlaverse.nixtla.io/statsforecast/
- Uncertainty quantification guide: https://otexts.com/fpp3/prediction-intervals.html
- Scripts: `{baseDir}/scripts/` directory contains all executable code
