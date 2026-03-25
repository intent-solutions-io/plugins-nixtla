---
name: nixtla-uncertainty-quantifier
description: "Analyze forecast uncertainty using conformal prediction. Use when risk assessment, scenario planning, or prediction interval generation is required. Trigger with 'quantify uncertainty', 'prediction intervals', or 'confidence bands'."
allowed-tools: "Read,Write,Bash(python:*),Glob,Grep"
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
compatible-with: claude-code
tags: [nixtla, time-series, forecasting, uncertainty, conformal-prediction, risk-assessment]
---

# Uncertainty Quantifier

Generates prediction intervals and confidence bands for time series forecasts using conformal prediction.

## Overview

This skill calculates prediction intervals and confidence bands around point forecasts, leveraging conformal prediction techniques. It requires a trained forecasting model (e.g., TimeGPT, StatsForecast) and historical data. The skill produces calibrated uncertainty estimates that enable risk-aware decision-making by quantifying how much trust to place in point forecast values.

**When to use**: Point forecasts alone are insufficient and an understanding of forecast uncertainty is needed. Applicable to risk assessment, capacity planning, inventory management, and any domain where knowing the forecast range matters as much as the forecast itself.

**Trigger phrases**: "quantify uncertainty", "prediction intervals", "confidence bands", "forecast uncertainty", "conformal prediction".

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep

**Environment**:
- Requires access to a trained forecasting model (e.g., TimeGPT API Key or StatsForecast model).
- `NIXTLA_TIMEGPT_API_KEY` (if using TimeGPT for the underlying forecast).

**Packages**:
```bash
pip install nixtla pandas statsforecast matplotlib scikit-learn
```

## Instructions

### Step 1: Generate Forecasts

Load historical data and generate point forecasts using StatsForecast.

**Script**: `{baseDir}/scripts/generate_forecasts.py`

```bash
python {baseDir}/scripts/generate_forecasts.py \
  --input data.csv \
  --output forecast.csv
```

The script loads CSV data with `unique_id`, `ds`, `y` columns, splits data into training (80%) and validation (20%), trains AutoETS model with weekly seasonality, generates forecasts for the validation period, and saves results with columns: unique_id, ds, y, StatsForecast.

### Step 2: Quantify Uncertainty

Execute the uncertainty quantification script with the chosen confidence level and method.

**Script**: `{baseDir}/scripts/quantify_uncertainty.py`

```bash
python {baseDir}/scripts/quantify_uncertainty.py \
  --input forecast.csv \
  --confidence 0.95 \
  --method quantile \
  --forecast_col StatsForecast
```

**Parameters**:
- `--input`: Path to forecast CSV file from Step 1
- `--confidence`: Confidence level (0.90 for 90%, 0.95 for 95%, etc.)
- `--method`: Conformal prediction method (`quantile` or `jackknife+`)
- `--forecast_col`: Name of the forecast column (default: StatsForecast)

**Methods**:
- **quantile**: Uses calibration set residuals to compute prediction intervals. Faster and suitable for most use cases.
- **jackknife+**: Uses leave-one-out cross-validation for uncertainty estimation. More robust but computationally expensive.

The script automatically calculates conformal prediction intervals, evaluates calibration (coverage, interval width), generates visualization with confidence bands, and saves all outputs.

## Output

- **forecast_with_uncertainty.csv**: Predictions with lower and upper bounds of the prediction interval at the specified confidence level.
- **uncertainty_plot.png**: Visualization of the forecast with shaded confidence bands showing the prediction interval.
- **calibration_metrics.json**: Metrics evaluating the calibration of the prediction intervals including empirical coverage and average interval width.

## Error Handling

| Error | Solution |
|-------|----------|
| Input file not found | Verify the file path specified in the `--input` argument |
| Invalid confidence level | Specify a value between 0 and 1 (e.g., 0.95 for 95%) |
| Unsupported conformal method | Choose `quantile` or `jackknife+` |
| Missing required columns | Ensure CSV has `unique_id`, `ds`, `y`, and forecast columns |
| Empty calibration set | Provide at least 10-20 observations for calibration |

## Examples

See [examples](references/examples.md) for detailed usage patterns including sales forecasting with 90% confidence, energy demand with 95% confidence using jackknife+, and complete end-to-end workflows.

## Resources

- Conformal prediction overview: https://en.wikipedia.org/wiki/Conformal_prediction
- StatsForecast documentation: https://nixtlaverse.nixtla.io/statsforecast/
- Uncertainty quantification guide: https://otexts.com/fpp3/prediction-intervals.html
- Scripts: `{baseDir}/scripts/` directory contains all executable code

**Related Skills**:
- `nixtla-forecast-validator` - Validate forecast accuracy and calibration
- `nixtla-market-risk-analyzer` - Risk metrics and position sizing
