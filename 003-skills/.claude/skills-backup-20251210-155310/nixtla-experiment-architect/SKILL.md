---
name: nixtla-experiment-architect
description: Scaffolds production-ready forecasting experiments with Nixtla libraries. Creates configuration files, experiment harnesses, multi-model comparisons, and cross-validation workflows for StatsForecast, MLForecast, and TimeGPT. Activates when user needs experiment setup, forecasting pipeline creation, model benchmarking, or multi-model comparison framework.
allowed-tools: "Read,Write,Glob,Grep,Edit"
version: "1.0.0"
license: MIT
---

# Nixtla Experiment Architect

Design and scaffold complete forecasting experiments using Nixtla's libraries.

## Overview

This skill creates production-ready experiment harnesses:

- **Configuration management**: YAML-based experiment config
- **Multi-model comparison**: StatsForecast + MLForecast + TimeGPT
- **Cross-validation**: Rolling-origin or expanding-window
- **Metrics evaluation**: SMAPE, MASE, MAE, RMSE

## Prerequisites

**Required**:
- Python 3.8+
- `statsforecast`, `utilsforecast`

**Optional**:
- `mlforecast`: For ML models
- `nixtla`: For TimeGPT
- `NIXTLA_API_KEY`: TimeGPT access

**Installation**:
```bash
pip install statsforecast mlforecast nixtla utilsforecast pyyaml
```

## Instructions

### Step 1: Gather Requirements

Collect experiment parameters:
- Data source path
- Target column name
- Forecast horizon (e.g., 14 days)
- Frequency (D, H, W, M)
- Unique ID column (optional)

### Step 2: Generate Configuration

```bash
python {baseDir}/scripts/generate_config.py \
    --data data/sales.csv \
    --target sales \
    --horizon 14 \
    --freq D \
    --output forecasting/config.yml
```

### Step 3: Scaffold Experiment

```bash
python {baseDir}/scripts/scaffold_experiment.py \
    --config forecasting/config.yml \
    --output forecasting/experiments.py
```

### Step 4: Run Experiment

```bash
python forecasting/experiments.py
```

### Step 5: Review Results

```bash
cat forecasting/results/metrics_summary.csv
```

## Output

- **forecasting/config.yml**: Experiment configuration
- **forecasting/experiments.py**: Runnable experiment harness
- **forecasting/results/**: Metrics and forecasts (after running)

## Error Handling

1. **Error**: `Data file not found`
   **Solution**: Verify data source path in config

2. **Error**: `Column not found`
   **Solution**: Check column names match your data

3. **Error**: `Missing required package`
   **Solution**: Install missing dependencies with pip

4. **Error**: `Cross-validation failed`
   **Solution**: Ensure enough data for n_windows

## Examples

### Example 1: Daily Sales Forecast

```bash
python {baseDir}/scripts/generate_config.py \
    --data data/sales.csv \
    --target revenue \
    --horizon 30 \
    --freq D \
    --id_col store_id
```

**Output config.yml**:
```yaml
data:
  source: data/sales.csv
  target: revenue
  unique_id: store_id
forecasting:
  horizon: 30
  freq: D
models:
  - SeasonalNaive
  - AutoETS
  - AutoARIMA
```

### Example 2: Hourly Energy Forecast

```bash
python {baseDir}/scripts/generate_config.py \
    --data data/energy.csv \
    --target consumption \
    --horizon 24 \
    --freq H
```

## Resources

- Scripts: `{baseDir}/scripts/`
- Templates: `{baseDir}/assets/templates/`
- Nixtla Docs: https://nixtla.github.io/

**Related Skills**:
- `nixtla-timegpt-lab`: Core forecasting guidance
- `nixtla-schema-mapper`: Data transformation
- `nixtla-prod-pipeline-generator`: Production deployment
