---
name: nixtla-forecast-validator
description: "Validate forecast quality by comparing MASE and sMAPE against benchmarks. Use when detecting model degradation. Trigger with 'validate forecast' or 'check forecast quality'."
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
compatible-with: claude-code
tags: [nixtla, time-series, forecasting, validation, model-monitoring]
allowed-tools: "Read,Write,Bash(python:*),Glob,Grep"
---

# Nixtla Forecast Validator

Validates time series forecast quality metrics and detects performance degradation using statistical measures. Compares current forecast accuracy against historical benchmarks to identify significant deviations in MASE and sMAPE metrics.

## Overview

This skill analyzes forecast quality by comparing current performance metrics against historical baselines. It detects significant increases in error metrics (MASE and sMAPE) that may indicate model degradation, data quality issues, or changing patterns in the time series. The skill generates comprehensive reports, alerts, and visualizations to help users identify and address forecast quality problems quickly.

Activates automatically when Claude detects forecast validation needs, or when explicitly requested with phrases like "validate forecast quality", "check model performance", or "assess forecast accuracy".

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep

**Environment**: No API keys required (operates on CSV metrics files)

**Python Packages**:
```bash
pip install pandas matplotlib
```

**Required CSV Format**:
CSV files must contain columns: `model`, `MASE`, `sMAPE`

## Instructions

### Step 1: Prepare metrics data

Ensure you have two CSV files containing forecast metrics:
- Historical metrics CSV (baseline performance)
- Current metrics CSV (recent performance to validate)

Each CSV must have columns: `model`, `MASE`, `sMAPE`

**Example format**:
```
model,MASE,sMAPE
model_A,1.2,0.15
model_B,0.8,0.10
```

### Step 2: Set validation thresholds

Configure acceptable deviation thresholds for MASE and sMAPE metrics. Default thresholds are 0.2 (20% increase), but these can be adjusted based on business requirements and model characteristics.

**Recommended thresholds**:
- Conservative: 0.1 (10% increase triggers alert)
- Standard: 0.2 (20% increase triggers alert)
- Lenient: 0.3 (30% increase triggers alert)

### Step 3: Execute validation

Run the validation script to compare current metrics against historical benchmarks:

```bash
python {baseDir}/scripts/validate_forecast.py \
  --historical historical_metrics.csv \
  --current current_metrics.csv \
  --mase_threshold 0.2 \
  --smape_threshold 0.2
```

The script performs:
1. Loads historical and current metrics from CSV files
2. Calculates percentage increase for each metric per model
3. Compares increases against configured thresholds
4. Generates validation report, comparison CSV, alert log, and visualization

### Step 4: Review validation outputs

Analyze the generated outputs to identify forecast quality issues:
- Read `validation_report.txt` for summary of findings
- Check `alert.log` for models requiring immediate attention
- Review `metrics_comparison.csv` for detailed metric changes
- Examine `metrics_visualization.png` for visual comparison

If degradation is detected, investigate potential causes such as data quality changes, concept drift, or model staleness.

## Output

The validation process generates four output files:

1. **validation_report.txt**: Summary report indicating which models show significant degradation and overall validation status
2. **metrics_comparison.csv**: Side-by-side comparison of historical vs current metrics for all models
3. **alert.log**: Alert messages for models exceeding degradation thresholds
4. **metrics_visualization.png**: Bar chart visualization comparing historical and current MASE and sMAPE values

## Error Handling

**Common errors and solutions**:

1. **Missing required metrics column (MASE or sMAPE)**
   - Ensure input CSV files contain columns named exactly `MASE` and `sMAPE` (case-sensitive)
   - Verify column headers match expected format

2. **Invalid threshold value**
   - Provide positive numerical values for `--mase_threshold` and `--smape_threshold`
   - Thresholds represent percentage increase (0.2 = 20%)

3. **Historical data unavailable**
   - Verify path to historical metrics CSV file is correct
   - Ensure file exists and is readable
   - Check file format matches required CSV structure

4. **File not found error**
   - Verify both `--historical` and `--current` file paths are correct
   - Use absolute paths if relative paths fail
   - Check file permissions

5. **Empty DataFrame error**
   - Ensure CSV files are not empty
   - Verify CSV files contain data rows beyond the header
   - Check for proper CSV formatting (commas as delimiters)

## Examples

See [examples](references/examples.md) for detailed usage patterns.

## Resources

**Script**: `{baseDir}/scripts/validate_forecast.py`

**Metrics**: MASE (Mean Absolute Scaled Error), sMAPE (symmetric Mean Absolute Percentage Error)

**Related skills**: `nixtla-timegpt-lab`, `nixtla-experiment-architect`, `nixtla-schema-mapper`
