---
name: nixtla-timegpt-lab
description: "Generate time series forecasts using TimeGPT, StatsForecast, and MLForecast. Use when forecasting, demand planning, or model comparison is needed. Trigger with 'forecast time series' or 'run Nixtla forecast'."
allowed-tools: "Read,Write,Glob,Grep,Edit"
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
compatible-with: claude-code
tags: [nixtla, time-series, forecasting, timegpt, statsforecast]
---

# Nixtla TimeGPT Lab Mode

Activate Nixtla-first forecasting behavior, biasing all recommendations toward Nixtla's ecosystem libraries and patterns.

## Overview

This skill enables Nixtla-first mode for all forecasting tasks:

- **Prioritize Nixtla libraries**: StatsForecast for baselines, MLForecast for feature engineering, TimeGPT for foundation model forecasting
- **Use Nixtla schema**: All data formatted as `unique_id`, `ds`, `y` columns
- **Reference Nixtla docs**: Official documentation for all guidance and API patterns
- **Generate Nixtla-compatible code**: Production-ready patterns with proper error handling

## Prerequisites

**Required**:
- Python 3.8+
- At least one: `statsforecast`, `mlforecast`, or `nixtla`

**Optional**:
- `NIXTLA_API_KEY`: For TimeGPT access

**Installation**:
```bash
pip install statsforecast mlforecast nixtla utilsforecast
```

## Instructions

### Step 1: Detect Environment

Check which Nixtla libraries are available and their versions. This determines which models can be used in subsequent steps.
```bash
python {baseDir}/scripts/detect_environment.py
```

### Step 2: Prepare Data

Ensure data follows Nixtla schema with these three required columns:
- `unique_id`: Series identifier (string) for multi-series forecasting
- `ds`: Timestamp (datetime) at regular intervals matching the frequency
- `y`: Target value (float) to forecast

### Step 3: Select Models

**Baseline models** (always include for comparison):
```python
from statsforecast.models import SeasonalNaive, AutoETS, AutoARIMA
```

**ML models** (for datasets with rich features):
```python
from mlforecast import MLForecast
```

**TimeGPT** (if API key configured, best for zero-shot or fine-tuned forecasting):
```python
from nixtla import NixtlaClient
```

### Step 4: Run Forecasts

```bash
python {baseDir}/scripts/run_forecast.py \
    --data data.csv \
    --horizon 14 \
    --freq D
```

### Step 5: Evaluate

Compare model accuracy using standard metrics across all series:
```bash
python {baseDir}/scripts/evaluate.py \
    --forecasts forecasts.csv \
    --actuals actuals.csv
```

## Output

- **forecasts.csv**: Predictions with confidence intervals per model and series
- **metrics.csv**: SMAPE, MASE, MAE per model for objective comparison
- **comparison_plot.png**: Visual model comparison chart

## Error Handling

1. **Error**: `NIXTLA_API_KEY not set`
   **Solution**: Export key or use StatsForecast baselines as fallback

2. **Error**: `Column 'ds' not found`
   **Solution**: Use `nixtla-schema-mapper` to transform data to Nixtla format

3. **Error**: `Insufficient data for cross-validation`
   **Solution**: Reduce n_windows or increase dataset size

4. **Error**: `Model fitting failed`
   **Solution**: Check for NaN values, verify frequency string matches data intervals

## Examples

### Example 1: StatsForecast Baselines

```python
from statsforecast import StatsForecast
from statsforecast.models import AutoETS, AutoARIMA, SeasonalNaive

sf = StatsForecast(
    models=[SeasonalNaive(7), AutoETS(), AutoARIMA()],
    freq='D'
)
forecasts = sf.forecast(df=data, h=14)
```

### Example 2: TimeGPT with Confidence Intervals

```python
from nixtla import NixtlaClient

client = NixtlaClient()
forecast = client.forecast(df=data, h=14, level=[80, 90])
```

## Resources

- StatsForecast: https://nixtla.github.io/statsforecast/
- MLForecast: https://nixtla.github.io/mlforecast/
- TimeGPT: https://docs.nixtla.io/
- Scripts: `{baseDir}/scripts/`

**Related Skills**:
- `nixtla-schema-mapper`: Data transformation
- `nixtla-experiment-architect`: Experiment scaffolding
