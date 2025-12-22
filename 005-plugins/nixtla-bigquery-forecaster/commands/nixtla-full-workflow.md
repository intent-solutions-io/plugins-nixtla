---
name: nixtla-full-workflow
description: Run the complete baseline-to-production forecasting pipeline
---

# Nixtla Full Forecasting Workflow

Run the complete baseline-to-production forecasting pipeline:

1. **Extract sample** from BigQuery (representative subset)
2. **Test baseline models** (AutoETS, AutoTheta, SeasonalNaive) on sample
3. **Find winner** (lowest sMAPE)
4. **Run winner** on full BigQuery dataset

## Usage

```
/nixtla-full-workflow project=<PROJECT> dataset=<DATASET> table=<TABLE> \
    timestamp_col=<TIMESTAMP_COL> value_col=<VALUE_COL> \
    [group_by=<GROUP_COL>] [sample_size=100] [horizon=30] \
    [output_dataset=<OUT_DATASET>] [output_table=<OUT_TABLE>]
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `project` | Yes | - | GCP project ID |
| `dataset` | Yes | - | BigQuery dataset name |
| `table` | Yes | - | BigQuery table name |
| `timestamp_col` | Yes | - | Column containing timestamps |
| `value_col` | Yes | - | Column containing values to forecast |
| `group_by` | No | - | Column to group by (creates unique time series) |
| `sample_size` | No | 100 | Number of series to sample for baseline testing |
| `horizon` | No | 30 | Forecast horizon (days) |
| `output_dataset` | No | - | Output dataset for forecasts |
| `output_table` | No | - | Output table for forecasts |

## Example

```
/nixtla-full-workflow project=myproject dataset=sales table=daily_transactions \
    timestamp_col=date value_col=revenue group_by=store_id \
    sample_size=50 horizon=14 \
    output_dataset=forecasts output_table=revenue_forecast_20250110
```

## Workflow Output

```
nixtla_workflow_output/
├── sample.csv                    # Extracted sample from BigQuery
├── baseline_results/
│   ├── results_Custom_h14.csv    # Per-model metrics
│   └── summary_Custom_h14.txt    # Model comparison
├── winning_model_config.json     # Winner for production use
├── forecast_request.json         # Ready-to-use API request
└── workflow_results.json         # Complete workflow summary
```

## What It Does

### Step 1: Sample Extraction
Pulls a statistically representative sample from your BigQuery table.
Only series with 30+ data points are included.

### Step 2: Baseline Testing
Runs 3 forecasting models on **the same sample data**:
- SeasonalNaive (simple baseline)
- AutoETS (exponential smoothing)
- AutoTheta (theta method)

### Step 3: Model Selection
Compares models using sMAPE (Symmetric Mean Absolute Percentage Error).
Winner = lowest average sMAPE across all sampled series.

### Step 4: Production Forecast
Prepares a forecast request using only the winning model.
Run at scale on your full BigQuery dataset.

## Integration

This command integrates two plugins:
- **nixtla-baseline-lab**: Model testing and selection
- **nixtla-bigquery-forecaster**: Production-scale forecasting

The winning model config (`winning_model_config.json`) can be used directly
with the bigquery-forecaster Cloud Function.
