# TimeGPT Fine-Tuning Scripts

Production-ready Python scripts for TimeGPT fine-tuning workflows.

## Overview

This directory contains 6 scripts that guide you through the complete TimeGPT fine-tuning lifecycle:

1. **prepare_finetune_data.py** - Prepare and validate training data
2. **configure_finetune.py** - Create fine-tuning configuration
3. **submit_finetune.py** - Submit fine-tuning job to TimeGPT API
4. **monitor_finetune.py** - Monitor job status until completion
5. **compare_finetuned.py** - Compare zero-shot vs fine-tuned models
6. **evaluate.py** - Calculate comprehensive evaluation metrics

## Prerequisites

```bash
pip install nixtla pandas pyyaml
export NIXTLA_API_KEY='your-api-key'
```

Get API key: https://dashboard.nixtla.io

## Quick Start

### 1. Prepare Data

```bash
python prepare_finetune_data.py \
    --input data/sales.csv \
    --output-train data/train.csv \
    --output-val data/val.csv \
    --val-size 14
```

### 2. Configure Fine-Tuning

```bash
python configure_finetune.py \
    --train data/train.csv \
    --val data/val.csv \
    --model-name "sales-forecast-v1" \
    --horizon 14 \
    --freq D
```

### 3. Submit Job

```bash
python submit_finetune.py \
    --config forecasting/finetune_config.yml
```

### 4. Monitor Progress

```bash
python monitor_finetune.py \
    --artifacts-dir forecasting/artifacts/timegpt_finetune \
    --timeout 60
```

### 5. Compare Models

```bash
python compare_finetuned.py \
    --test data/test.csv \
    --artifacts-dir forecasting/artifacts/timegpt_finetune
```

### 6. Evaluate Performance

```bash
python evaluate.py \
    --comparison forecasting/results/comparison_metrics.csv
```

## Script Details

### prepare_finetune_data.py (255 lines)

Validates and prepares data in Nixtla schema (unique_id, ds, y).

**Features**:
- Auto-detects column names (id, date, value)
- Validates data quality (no NaN, sufficient observations)
- Splits into train/validation sets
- Supports time-based or percentage splits

**Example**:
```bash
python prepare_finetune_data.py \
    --input raw_data.csv \
    --output-train train.csv \
    --output-val val.csv \
    --id-col store_id \
    --time-col date \
    --target-col sales
```

### configure_finetune.py (252 lines)

Creates YAML configuration for fine-tuning job.

**Features**:
- Sets model parameters (horizon, frequency)
- Configures hyperparameters (steps, loss function)
- Validates data paths
- Generates readable YAML config

**Example**:
```bash
python configure_finetune.py \
    --train train.csv \
    --model-name "my-model" \
    --horizon 24 \
    --freq H \
    --finetune-steps 200 \
    --finetune-loss mae
```

### submit_finetune.py (241 lines)

Submits fine-tuning job to TimeGPT API.

**Features**:
- Loads configuration and validates
- Submits job with all parameters
- Saves job ID and metadata
- Error handling for API failures

**Example**:
```bash
python submit_finetune.py \
    --config forecasting/finetune_config.yml \
    --no-wait
```

### monitor_finetune.py (277 lines)

Monitors job status until completion.

**Features**:
- Polls API for status updates
- Adaptive check intervals (30s → 2min)
- Handles timeout scenarios
- Updates job metadata

**Example**:
```bash
python monitor_finetune.py \
    --job-id abc123 \
    --timeout 90 \
    --check-interval 30
```

### compare_finetuned.py (299 lines)

Compares zero-shot vs fine-tuned model performance.

**Features**:
- Generates forecasts from both models
- Calculates metrics (MAE, RMSE, SMAPE)
- Shows percentage improvement
- Saves detailed comparison CSV

**Example**:
```bash
python compare_finetuned.py \
    --test data/test.csv \
    --finetune-id my-model-v1 \
    --horizon 14 \
    --freq D
```

### evaluate.py (305 lines)

Calculates comprehensive evaluation metrics.

**Features**:
- Point forecast metrics (MAE, RMSE, MAPE, SMAPE, MASE)
- Per-series and aggregated results
- Best/worst performing series
- Bias analysis

**Example**:
```bash
python evaluate.py \
    --test data/test.csv \
    --forecast forecasts.csv \
    --train data/train.csv \
    --seasonality 7
```

## Output Structure

```
forecasting/
├── finetune_config.yml              # Configuration
├── artifacts/
│   └── timegpt_finetune/
│       ├── finetune_model_id.txt    # Model ID
│       └── finetune_metadata.yml    # Job metadata
└── results/
    ├── comparison_metrics.csv       # Model comparison
    └── evaluation.csv               # Evaluation results
```

## Error Handling

All scripts include:
- Input validation
- API error handling
- Graceful failure modes
- Helpful error messages

## Common Issues

### NIXTLA_API_KEY not set
```bash
export NIXTLA_API_KEY='your-key-from-dashboard'
```

### Insufficient training data
Need 100+ observations per series for fine-tuning.

### Fine-tuning job failed
Check data format, ensure no NaN values, validate frequency matches data.

## Help

All scripts support `--help`:
```bash
python <script>.py --help
```

## Related Resources

- SKILL.md: Skill definition and workflows
- resources/BEST_PRACTICES.md: Fine-tuning best practices
- resources/SCENARIOS.md: Common use cases
- resources/TROUBLESHOOTING.md: Debugging guide
