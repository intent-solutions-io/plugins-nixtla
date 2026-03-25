---
name: nixtla-prod-pipeline-generator
description: "Transform forecasting experiments into Airflow/Prefect pipelines with monitoring. Use when deploying forecasts to production. Trigger with 'generate pipeline' or 'create Airflow DAG'."
allowed-tools: "Read,Write,Glob,Grep,Edit"
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
compatible-with: claude-code
tags: [nixtla, time-series, forecasting, production, pipelines, airflow]
---

# Nixtla Production Pipeline Generator

Transform validated forecasting experiments into production-ready inference pipelines with proper orchestration, monitoring, and error handling.

## Overview

This skill productionizes Nixtla forecasting workflows by generating complete deployment artifacts:

- **Airflow DAGs**: Enterprise orchestration with task dependencies, SLAs, and alerting
- **Prefect Flows**: Modern Python-native pipelines with better local testing and retry logic
- **Cron Scripts**: Simple single-machine batch processing for quick deployments

All pipelines implement the ETL-F pattern: Extract -> Transform -> Forecast -> Load -> Monitor

## Prerequisites

**Required**:
- Python 3.8+
- Completed experiment in `forecasting/config.yml`
- One of: Airflow, Prefect, or cron access

**Environment Variables**:
- `NIXTLA_API_KEY`: TimeGPT API key (if using TimeGPT)
- `FORECAST_DATA_SOURCE`: Production data connection string
- `FORECAST_DESTINATION`: Output destination for forecasts

**Installation**:
```bash
pip install nixtla pandas statsforecast  # Core
pip install apache-airflow  # For Airflow
pip install prefect  # For Prefect
```

## Instructions

### Step 1: Read Experiment Config

Load the validated experiment configuration. This step verifies the config exists and contains all required fields for pipeline generation.
```bash
python {baseDir}/scripts/read_experiment.py --config forecasting/config.yml
```

### Step 2: Select Orchestration Platform

Choose based on infrastructure and team requirements:
- **Airflow**: Best for enterprise environments with complex dependencies and extensive monitoring needs
- **Prefect**: Best for Python-native teams wanting better local testing and modern error handling
- **Cron**: Best for simple single-machine deployments with no external dependencies

### Step 3: Generate Pipeline

```bash
python {baseDir}/scripts/generate_pipeline.py \
    --config forecasting/config.yml \
    --platform airflow \
    --output pipelines/
```

### Step 4: Add Monitoring

Attach quality checks and fallback logic to the generated pipeline. Monitoring validates forecast accuracy against historical baselines and triggers alerts on degradation.
```bash
python {baseDir}/scripts/add_monitoring.py \
    --pipeline pipelines/forecast_dag.py \
    --metrics smape,mase
```

### Step 5: Deploy

Follow generated `pipelines/README.md` for platform-specific deployment instructions including environment setup, dependency installation, and scheduling configuration.

## Output

- **pipelines/forecast_dag.py**: Main pipeline file (Airflow DAG, Prefect Flow, or Cron script)
- **pipelines/monitoring.py**: Quality checks, accuracy validation, and fallback logic
- **pipelines/README.md**: Platform-specific deployment instructions
- **pipelines/requirements.txt**: Python dependencies for the generated pipeline

## Error Handling

1. **Error**: `Config file not found`
   **Solution**: Run `nixtla-experiment-architect` first to create config

2. **Error**: `NIXTLA_API_KEY not set`
   **Solution**: Export your TimeGPT API key or use StatsForecast baselines

3. **Error**: `Database connection failed`
   **Solution**: Verify `FORECAST_DATA_SOURCE` connection string and network access

4. **Error**: `Forecast quality check failed`
   **Solution**: Pipeline auto-falls back to baseline models; check monitoring logs for root cause

## Examples

See [examples](references/examples.md) for detailed usage scenarios.

## Resources

- Scripts: `{baseDir}/scripts/`
- Templates: `{baseDir}/assets/templates/`
- Nixtla Docs: https://nixtla.github.io/

**Related Skills**:
- `nixtla-experiment-architect`: Creates experiments to productionize
- `nixtla-timegpt-finetune-lab`: Fine-tuned models for pipelines
- `nixtla-usage-optimizer`: Cost-effective routing strategies
