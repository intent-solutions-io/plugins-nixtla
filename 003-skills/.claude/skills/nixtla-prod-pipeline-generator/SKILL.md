---
name: nixtla-prod-pipeline-generator
description: "Transform forecasting experiments into Airflow/Prefect pipelines with monitoring. Use when deploying forecasts to production. Trigger with 'generate pipeline' or 'create Airflow DAG'."
allowed-tools: "Read,Write,Glob,Grep,Edit"
version: "1.0.0"
license: MIT
---

# Nixtla Production Pipeline Generator

Transform validated forecasting experiments into production-ready inference pipelines with proper orchestration, monitoring, and error handling.

## Overview

This skill productionizes Nixtla forecasting workflows by generating complete deployment artifacts:

- **Airflow DAGs**: Enterprise orchestration with dependencies and monitoring
- **Prefect Flows**: Modern Python-native pipelines with better local testing
- **Cron Scripts**: Simple single-machine batch processing

All pipelines implement: Extract -> Transform -> Forecast -> Load -> Monitor

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

Load experiment from `forecasting/config.yml`:
```bash
python {baseDir}/scripts/read_experiment.py --config forecasting/config.yml
```

### Step 2: Select Orchestration Platform

Choose based on requirements:
- **Airflow**: Enterprise, complex dependencies, extensive monitoring
- **Prefect**: Python-native, better local testing, modern error handling
- **Cron**: Simple single-machine, no dependencies, quick setup

### Step 3: Generate Pipeline

```bash
python {baseDir}/scripts/generate_pipeline.py \
    --config forecasting/config.yml \
    --platform airflow \
    --output pipelines/
```

### Step 4: Add Monitoring

```bash
python {baseDir}/scripts/add_monitoring.py \
    --pipeline pipelines/forecast_dag.py \
    --metrics smape,mase
```

### Step 5: Deploy

Follow generated `pipelines/README.md` for deployment instructions.

## Output

- **pipelines/forecast_dag.py**: Main pipeline file (Airflow/Prefect/Cron)
- **pipelines/monitoring.py**: Quality checks and fallback logic
- **pipelines/README.md**: Deployment instructions
- **pipelines/requirements.txt**: Dependencies

## Error Handling

1. **Error**: `Config file not found`
   **Solution**: Run `nixtla-experiment-architect` first to create config

2. **Error**: `NIXTLA_API_KEY not set`
   **Solution**: Export your TimeGPT API key or use StatsForecast baselines

3. **Error**: `Database connection failed`
   **Solution**: Verify `FORECAST_DATA_SOURCE` connection string

4. **Error**: `Forecast quality check failed`
   **Solution**: Pipeline auto-falls back to baseline models

## Examples

### Example 1: Airflow DAG

```bash
python {baseDir}/scripts/generate_pipeline.py \
    --config forecasting/config.yml \
    --platform airflow \
    --schedule "0 6 * * *" \
    --output pipelines/
```

**Output**:
```
Generated: pipelines/forecast_dag.py
Schedule: Daily at 6am
Tasks: extract -> transform -> forecast -> load -> monitor
```

### Example 2: Simple Cron Script

```bash
python {baseDir}/scripts/generate_pipeline.py \
    --config forecasting/config.yml \
    --platform cron \
    --output pipelines/
```

## Resources

- Scripts: `{baseDir}/scripts/`
- Templates: `{baseDir}/assets/templates/`
- Nixtla Docs: https://nixtla.github.io/

**Related Skills**:
- `nixtla-experiment-architect`: Creates experiments to productionize
- `nixtla-timegpt-finetune-lab`: Fine-tuned models for pipelines
- `nixtla-usage-optimizer`: Cost-effective routing strategies
