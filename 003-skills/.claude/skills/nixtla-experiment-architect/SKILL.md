---
name: nixtla-experiment-architect
description: "Generate production-ready forecasting experiments with StatsForecast and TimeGPT. Use when setting up model benchmarking or cross-validation. Trigger with 'scaffold experiment' or 'compare models'."
allowed-tools: "Read,Write,Glob,Grep,Edit"
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
compatible-with: claude-code
tags: [nixtla, time-series, forecasting, experiment-design, cross-validation]
---

# Nixtla Experiment Architect

Design and scaffold complete forecasting experiments using Nixtla's libraries.

## Overview

This skill creates production-ready experiment harnesses:

- **Configuration management**: YAML-based experiment config with data source, models, and evaluation settings
- **Multi-model comparison**: StatsForecast + MLForecast + TimeGPT side-by-side evaluation
- **Cross-validation**: Rolling-origin or expanding-window strategies for robust evaluation
- **Metrics evaluation**: SMAPE, MASE, MAE, RMSE computed per model and per series

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

Collect experiment parameters from the user or project context:
- Data source path and format (CSV, Parquet, SQL)
- Target column name (the value to forecast)
- Forecast horizon (e.g., 14 days, 24 hours)
- Frequency (D, H, W, M)
- Unique ID column for multi-series data (optional, defaults to single series)

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

Examine the metrics summary to identify the best-performing model and assess cross-validation consistency:
```bash
cat forecasting/results/metrics_summary.csv
```

## Output

- **forecasting/config.yml**: Experiment configuration defining data, models, and evaluation parameters
- **forecasting/experiments.py**: Runnable experiment harness with cross-validation and metrics collection
- **forecasting/results/**: Metrics CSVs and forecast outputs (generated after running the experiment)

## Error Handling

1. **Error**: `Data file not found`
   **Solution**: Verify data source path in config

2. **Error**: `Column not found`
   **Solution**: Check column names match your data schema

3. **Error**: `Missing required package`
   **Solution**: Install missing dependencies with pip

4. **Error**: `Cross-validation failed`
   **Solution**: Ensure enough data points for n_windows (each window needs at least horizon + history)

## Examples

See [examples](references/examples.md) for detailed usage scenarios.

## Resources

- Scripts: `{baseDir}/scripts/`
- Templates: `{baseDir}/assets/templates/`
- Nixtla Docs: https://nixtla.github.io/

**Related Skills**:
- `nixtla-timegpt-lab`: Core forecasting guidance
- `nixtla-schema-mapper`: Data transformation
- `nixtla-prod-pipeline-generator`: Production deployment
