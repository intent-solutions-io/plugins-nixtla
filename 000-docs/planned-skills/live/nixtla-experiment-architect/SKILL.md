---
name: nixtla-experiment-architect
description: |
  Scaffolds production-ready forecasting experiments with configuration files.
  Use when designing a new forecasting project, comparing models, or automating pipelines.
  Trigger with "design experiment", "setup forecasting project", "create forecasting configs".
allowed-tools: "Read,Write,Edit,Glob,Grep"
version: "1.0.0"
---

# Nixtla Experiment Architect

Automates the creation of forecasting experiment configurations.

## Overview

Creates standardized configuration files for forecasting experiments, including dataset definitions, model selections (TimeGPT, StatsForecast), evaluation metrics, and pipeline settings. This simplifies experiment design, promotes reproducibility, and facilitates model comparison. Outputs a directory structure with pre-configured YAML files and Python scripts.

## Prerequisites

**Tools**: Read, Write, Edit, Glob, Grep

**Environment**: `NIXTLA_TIMEGPT_API_KEY` (for TimeGPT experiments)

**Packages**:
```bash
pip install nixtla statsforecast matplotlib pandas scikit-learn pyyaml
```

## Instructions

### Step 1: Define experiment parameters

Parse and validate user inputs (dataset path, model types, horizon).

```bash
python {baseDir}/scripts/parse_arguments.py \
  --dataset_path data.csv \
  --model_type TimeGPT \
  --horizon 30 \
  --experiment_name my_experiment
```

**Parameters**:
- `--dataset_path`: Path to CSV with time series data
- `--model_type`: TimeGPT, AutoARIMA, AutoETS, SeasonalNaive, or AutoTheta
- `--horizon`: Number of periods to forecast
- `--experiment_name`: Directory name for outputs
- `--metrics`: Evaluation metrics (default: MASE, sMAPE)
- `--freq`: Data frequency (D=daily, H=hourly, etc.)
- `--train_fraction`: Train/test split ratio (default: 0.8)

### Step 2: Generate configuration files

Create YAML configs for data loading, model training, and evaluation.

```bash
python {baseDir}/scripts/generate_configs.py \
  --dataset_path data.csv \
  --model_type TimeGPT \
  --horizon 30 \
  --experiment_name my_experiment \
  --metrics MASE sMAPE RMSE
```

**Outputs**:
- `my_experiment/data.yaml`: Data loading configuration
- `my_experiment/models.yaml`: Model selection configuration
- `my_experiment/config.yaml`: Experiment configuration

### Step 3: Run experiment pipeline

Execute the forecasting experiment using generated configs.

```bash
python {baseDir}/scripts/run_pipeline.py --experiment_name my_experiment
```

**Workflow**:
1. Loads configurations from YAML files
2. Loads and splits data into train/test sets
3. Trains selected forecasting model
4. Evaluates on test set using specified metrics
5. Generates visualization comparing actual vs predicted values

## Output

- **data.yaml**: Data loading configuration
- **models.yaml**: Model selection configuration
- **config.yaml**: Experiment configuration
- **forecast_visualization.png**: Visualization of forecast vs actual values
- **Evaluation metrics**: Printed to console (MASE, sMAPE, RMSE, MAE)

## Error Handling

1. **Error**: `Invalid model type`
   **Solution**: Use valid model names: TimeGPT, AutoARIMA, AutoETS, SeasonalNaive, AutoTheta

2. **Error**: `Dataset path not found`
   **Solution**: Verify the dataset file path exists and is accessible

3. **Error**: `Missing horizon`
   **Solution**: Specify the forecasting horizon using --horizon parameter

4. **Error**: `Invalid metric`
   **Solution**: Use valid evaluation metrics: MASE, sMAPE, RMSE, MAE

5. **Error**: `NIXTLA_TIMEGPT_API_KEY not set` (TimeGPT only)
   **Solution**: Set environment variable: `export NIXTLA_TIMEGPT_API_KEY=your_api_key`

## Examples

### Example 1: TimeGPT experiment

**Input**:
```bash
python {baseDir}/scripts/generate_configs.py \
  --dataset_path sales.csv \
  --model_type TimeGPT \
  --horizon 30 \
  --experiment_name sales_forecast
```

**Output**:
A directory `sales_forecast/` with config files and scripts for a TimeGPT forecasting experiment on sales.csv with a 30-day horizon.

### Example 2: StatsForecast experiment

**Input**:
```bash
python {baseDir}/scripts/generate_configs.py \
  --dataset_path demand.csv \
  --model_type AutoARIMA \
  --horizon 7 \
  --experiment_name demand_forecast
```

**Output**:
A directory `demand_forecast/` with config files and scripts for an AutoARIMA forecasting experiment on demand.csv with a 7-day horizon.

## Resources

- Configuration generator: `{baseDir}/scripts/generate_configs.py`
- Argument parser: `{baseDir}/scripts/parse_arguments.py`
- Pipeline runner: `{baseDir}/scripts/run_pipeline.py`
