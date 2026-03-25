---
name: nixtla-timegpt-finetune-lab
description: "Configure TimeGPT fine-tuning on custom datasets with Nixtla SDK. Use when training domain-specific forecast models. Trigger with 'fine-tune TimeGPT' or 'train custom model'."
allowed-tools: "Read,Write,Glob,Grep,Edit"
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
compatible-with: claude-code
tags: [nixtla, time-series, forecasting, fine-tuning, timegpt]
---

# Nixtla TimeGPT Fine-Tuning Lab

Guide production-ready TimeGPT fine-tuning workflows from data preparation through model comparison.

## Overview

This skill manages the full TimeGPT fine-tuning lifecycle:

- **Dataset preparation**: Validate format, check minimum observation counts, and handle missing values
- **Job submission**: Submit fine-tuning jobs to the TimeGPT API with configurable parameters
- **Status monitoring**: Track job progress and retrieve completion status
- **Model comparison**: Compare zero-shot vs fine-tuned performance with accuracy metrics

## Prerequisites

**Required**:
- Python 3.8+
- `nixtla` package
- `NIXTLA_API_KEY` environment variable

**Installation**:
```bash
pip install nixtla pandas utilsforecast
export NIXTLA_API_KEY='your-api-key'
```

**Get API Key**: https://dashboard.nixtla.io

## Instructions

### Step 1: Prepare Dataset

Ensure data conforms to Nixtla schema (`unique_id`, `ds`, `y`). Run the preparation script to validate format, check for NaN values, and enforce minimum observation counts.
```bash
python {baseDir}/scripts/prepare_finetune_data.py \
    --input data/sales.csv \
    --output data/finetune_train.csv
```

### Step 2: Configure Fine-Tuning

Set model name, forecast horizon, and frequency. The configuration file captures all parameters needed for reproducible fine-tuning.
```bash
python {baseDir}/scripts/configure_finetune.py \
    --train data/finetune_train.csv \
    --model_name "sales-model-v1" \
    --horizon 14 \
    --freq D
```

### Step 3: Submit Job

```bash
python {baseDir}/scripts/submit_finetune.py \
    --config forecasting/finetune_config.yml
```

### Step 4: Monitor Progress

Poll the API for job status until completion. The script reports training progress and alerts on failures.
```bash
python {baseDir}/scripts/monitor_finetune.py \
    --job_id <job_id>
```

### Step 5: Compare Models

Evaluate fine-tuned model against zero-shot baseline on held-out test data:
```bash
python {baseDir}/scripts/compare_finetuned.py \
    --test data/test.csv \
    --finetune_id <model_id>
```

## Output

- **forecasting/finetune_config.yml**: Fine-tuning configuration with all parameters
- **forecasting/artifacts/finetune_model_id.txt**: Saved model ID for inference
- **forecasting/results/comparison_metrics.csv**: Side-by-side performance comparison

## Error Handling

1. **Error**: `NIXTLA_API_KEY not set`
   **Solution**: Export your API key: `export NIXTLA_API_KEY='...'`

2. **Error**: `Insufficient training data`
   **Solution**: Need 100+ observations per series for effective fine-tuning

3. **Error**: `Fine-tuning job failed`
   **Solution**: Check data format, ensure no NaN values, verify schema compliance

4. **Error**: `Model ID not found`
   **Solution**: Verify job completed successfully, check artifacts directory

## Examples

See [examples](references/examples.md) for detailed usage scenarios.

## Resources

- Scripts: `{baseDir}/scripts/`
- TimeGPT Docs: https://docs.nixtla.io/
- [Fine-Tuning Guide](https://docs.nixtla.io/docs/finetuning)

**Related Skills**: `nixtla-schema-mapper` (data prep), `nixtla-experiment-architect` (baselines), `nixtla-usage-optimizer` (cost)
