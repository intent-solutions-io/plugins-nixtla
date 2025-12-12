# Nixtla Experiment Architect Scripts

Production-ready Python scripts for scaffolding forecasting experiments with Nixtla libraries.

## Scripts Overview

### 1. generate_config.py
Generate YAML configuration files from command-line arguments.

**Features**:
- Auto-detect appropriate season length based on frequency
- Calculate optimal CV horizon and step size
- Support for single or multi-series forecasting
- Configurable model families (StatsForecast, MLForecast, TimeGPT)

**Usage**:
```bash
python generate_config.py \
    --data data/sales.csv \
    --target revenue \
    --horizon 30 \
    --freq D \
    --output forecasting/config.yml
```

**Arguments**:
- `--data`: Path to CSV or Parquet file (required)
- `--target`: Target column name (required)
- `--horizon`: Forecast horizon in periods (required)
- `--freq`: Frequency (D/H/W/M/MS/Q/Y) (required)
- `--id_col`: Unique ID column for multi-series (optional)
- `--ds_col`: Timestamp column name (default: "date")
- `--exog_vars`: Exogenous variables (optional)
- `--cv_windows`: Number of CV windows (default: 4)
- `--cv_method`: rolling or expanding (default: rolling)
- `--enable_mlforecast`: Enable MLForecast models
- `--enable_timegpt`: Enable TimeGPT
- `--output`: Output path (default: forecasting/config.yml)

### 2. scaffold_experiment.py
Generate runnable experiment scripts from configuration files.

**Features**:
- Process experiments_template.py with config values
- Add configuration summary to generated script
- Validate config structure before generation
- Create output directories automatically

**Usage**:
```bash
python scaffold_experiment.py \
    --config forecasting/config.yml \
    --output forecasting/experiments.py
```

**Arguments**:
- `--config`: Path to YAML config file (required)
- `--output`: Output path for experiment script (default: forecasting/experiments.py)
- `--template`: Custom template path (optional)

### 3. validate_experiment.py
Comprehensive validation of experiment configuration and data readiness.

**Features**:
- Configuration structure validation
- Data file accessibility and format checks
- Required columns presence verification
- Data quality checks (nulls, types, date parsing)
- Package dependency verification
- Cross-validation settings validation

**Usage**:
```bash
# Basic validation
python validate_experiment.py --config forecasting/config.yml

# Include package checks
python validate_experiment.py --config config.yml --check-packages

# Verbose diagnostics
python validate_experiment.py --config config.yml --verbose
```

**Arguments**:
- `--config`: Path to YAML config file (required)
- `--check-packages`: Verify required packages are installed
- `--verbose`: Print detailed diagnostics

**Exit Codes**:
- 0: All validations passed
- 1: Validation errors found
- 2: Configuration file issues

## Workflow

Complete experiment setup workflow:

```bash
# Step 1: Generate configuration
python scripts/generate_config.py \
    --data data/sales.csv \
    --target revenue \
    --horizon 30 \
    --freq D

# Step 2: Validate configuration and data
python scripts/validate_experiment.py \
    --config forecasting/config.yml \
    --check-packages

# Step 3: Scaffold experiment
python scripts/scaffold_experiment.py \
    --config forecasting/config.yml

# Step 4: Run experiment
python forecasting/experiments.py

# Step 5: Review results
cat forecasting/results/metrics_summary.csv
```

## Dependencies

### Core (required for scripts):
```bash
pip install pyyaml pandas
```

### Forecasting (required for generated experiments):
```bash
pip install statsforecast utilsforecast
```

### Optional (for specific model families):
```bash
# MLForecast
pip install mlforecast scikit-learn lightgbm

# TimeGPT
pip install nixtla
export NIXTLA_API_KEY='your-api-key'
```

## Examples

### Example 1: Daily Sales Forecast
```bash
python generate_config.py \
    --data data/daily_sales.csv \
    --target revenue \
    --horizon 30 \
    --freq D \
    --id_col store_id \
    --enable_mlforecast
```

**Generated config**:
- Forecast: 30 days ahead
- Season length: 7 (weekly seasonality)
- CV: 4 windows, 15-day horizon
- Models: StatsForecast + MLForecast

### Example 2: Hourly Energy Forecast
```bash
python generate_config.py \
    --data data/energy.csv \
    --target consumption \
    --horizon 24 \
    --freq H \
    --id_col meter_id
```

**Generated config**:
- Forecast: 24 hours ahead
- Season length: 24 (daily seasonality)
- CV: 4 windows, 12-hour horizon
- Models: StatsForecast only

### Example 3: Monthly Financial Forecast with TimeGPT
```bash
python generate_config.py \
    --data data/financials.csv \
    --target revenue \
    --horizon 12 \
    --freq M \
    --enable_timegpt \
    --cv_windows 6
```

**Generated config**:
- Forecast: 12 months ahead
- Season length: 12 (yearly seasonality)
- CV: 6 windows, 6-month horizon
- Models: StatsForecast + TimeGPT

## Error Handling

All scripts include comprehensive error handling:

- **generate_config.py**: Validates file paths, frequency codes, horizon values
- **scaffold_experiment.py**: Validates config structure, template availability
- **validate_experiment.py**: Provides detailed diagnostics for all validation failures

## Integration with Skill

These scripts are used by the `nixtla-experiment-architect` skill:

```bash
# Skill workflow references these scripts
python {baseDir}/scripts/generate_config.py ...
python {baseDir}/scripts/scaffold_experiment.py ...
python {baseDir}/scripts/validate_experiment.py ...
```

## Development Notes

- All scripts use argparse with comprehensive --help output
- Exit codes: 0 (success), 1 (validation error), 2 (file error)
- Scripts are executable: `chmod +x *.py`
- Type hints used throughout for clarity
- Docstrings follow Google style
- Error messages are user-friendly and actionable

## File Locations

```
nixtla-experiment-architect/
├── SKILL.md
├── assets/
│   └── templates/
│       ├── config_template.yml
│       └── experiments_template.py
└── scripts/
    ├── README.md (this file)
    ├── generate_config.py
    ├── scaffold_experiment.py
    ├── validate_experiment.py
    └── requirements.txt
```

## Version

Scripts version: 1.0.0
Compatible with: nixtla-experiment-architect skill v1.0.0
