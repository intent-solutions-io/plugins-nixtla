---
name: nixtla-prod-pipeline-generator
description: |
  Transforms experiments into production pipelines with Airflow/Prefect.
  Use when deploying time series models or managing complex data workflows.
  Trigger with "productionize model", "create pipeline", "deploy forecasting".
allowed-tools: "Read,Write,Edit,Glob,Grep"
version: "1.0.0"
---

# Nixtla Production Pipeline Generator

Transforms forecasting experiments into robust production pipelines.

## Purpose

Automates the creation of Airflow or Prefect workflows to deploy time series models.

## Overview

Analyzes experiment configurations and generates production-ready pipeline code. Supports integration with TimeGPT API for seamless model deployment. Facilitates scheduling, monitoring, and version control of forecasting pipelines. Outputs Python code for Airflow/Prefect DAGs and associated configuration files.

## Prerequisites

**Tools**: Read, Write, Edit, Glob, Grep

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install airflow prefect nixtla statsforecast matplotlib pandas
```

## Instructions

### Step 1: Create experiment configuration

Generate a sample configuration file or use an existing one.

```bash
python {baseDir}/scripts/create_sample_config.py --output experiment.yaml
```

**Configuration format**:
```yaml
pipeline_name: my_forecasting_pipeline
model_type: TimeGPT  # or StatsForecast
data_location: data.csv
frequency: D
horizon: 14
```

### Step 2: Validate configuration

Load and validate the experiment configuration.

```bash
python {baseDir}/scripts/load_config.py experiment.yaml
```

**Validates**:
- Required keys: model_type, data_location, frequency, horizon, pipeline_name
- Model type: TimeGPT or StatsForecast
- Horizon: positive integer
- Frequency: valid pandas frequency string

### Step 3: Generate pipeline code

Select target framework (Airflow or Prefect) and generate pipeline code.

```bash
# For Airflow
python {baseDir}/scripts/generate_pipeline.py \
  --config experiment.yaml \
  --framework airflow

# For Prefect
python {baseDir}/scripts/generate_pipeline.py \
  --config experiment.yaml \
  --framework prefect
```

**Airflow output**: `dags/{pipeline_name}_dag.py`
**Prefect output**: `flows/{pipeline_name}_flow.py`

## Output

- **dags/**: Airflow DAG Python files
- **flows/**: Prefect flow Python files
- **experiment.yaml**: Pipeline configuration file

## Error Handling

1. **Error**: `Invalid framework specified`
   **Solution**: Choose either 'airflow' or 'prefect'

2. **Error**: `Experiment config not found`
   **Solution**: Ensure the config file exists and path is correct

3. **Error**: `Missing TimeGPT API key`
   **Solution**: Set `NIXTLA_TIMEGPT_API_KEY` environment variable

4. **Error**: `Invalid experiment configuration`
   **Solution**: Check the experiment config file for missing or invalid fields

5. **Error**: `Missing required key`
   **Solution**: Ensure config has: model_type, data_location, frequency, horizon, pipeline_name

## Examples

### Example 1: Airflow deployment

**Input**:
```bash
python {baseDir}/scripts/generate_pipeline.py \
  --config experiment.yaml \
  --framework airflow
```

**Output**:
Airflow DAG Python file in `dags/` folder ready for deployment to Airflow environment.

### Example 2: Prefect deployment

**Input**:
```bash
python {baseDir}/scripts/generate_pipeline.py \
  --config experiment.yaml \
  --framework prefect
```

**Output**:
Prefect flow Python file in `flows/` folder ready for deployment to Prefect environment.

## Resources

- Configuration loader: `{baseDir}/scripts/load_config.py`
- Pipeline generator: `{baseDir}/scripts/generate_pipeline.py`
- Sample config creator: `{baseDir}/scripts/create_sample_config.py`
