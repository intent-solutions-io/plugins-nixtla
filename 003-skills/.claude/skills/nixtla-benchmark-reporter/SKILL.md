---
name: nixtla-benchmark-reporter
description: Generate comprehensive markdown benchmark reports from forecast accuracy metrics with model comparisons, statistical analysis, and regression detection. Use when analyzing baseline performance, comparing forecast models, or validating model quality. Trigger with 'generate benchmark report', 'analyze forecast metrics', or 'create performance summary'.
allowed-tools: "Read,Write,Glob,Bash(python:*)"
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
compatible-with: claude-code
tags: [nixtla, time-series, forecasting, benchmarking, metrics]
---

# Nixtla Benchmark Reporter

## Purpose

Generate production-ready benchmark reports from forecasting accuracy metrics. This skill enables systematic model comparison and regression detection for Nixtla forecasting workflows, automating analysis that typically takes 2-3 hours into a 2-minute process.

## Overview

Transform raw forecast metrics (sMAPE, MASE, MAE, RMSE) into actionable insights:
- Parse benchmark results CSV files from statsforecast/TimeGPT experiments
- Calculate summary statistics (mean, median, std dev, percentiles)
- Generate model comparison tables with winners highlighted
- Create regression detection reports comparing current vs. baseline results
- Produce GitHub issue templates for performance degradations

## Prerequisites

- Benchmark results CSV with columns: `series_id`, `model`, `sMAPE`, `MASE` (minimum). Additional columns `MAE` and `RMSE` are supported but optional.
- Optional: Baseline results CSV for regression comparison
- Python 3.8+ with pandas, numpy installed

**Expected CSV Structure**:
```csv
series_id,model,sMAPE,MASE,MAE,RMSE
D1,SeasonalNaive,15.23,1.05,12.5,18.3
D1,AutoETS,13.45,0.92,10.2,15.1
D1,AutoTheta,12.34,0.87,9.8,14.5
```

## Instructions

### Step 1: Parse Benchmark Results

Run the report generator against a benchmark CSV. The script validates CSV structure, extracts unique models and series, and groups metrics by model automatically.

```bash
python {baseDir}/scripts/generate_benchmark_report.py \
    --results /path/to/benchmark_results.csv \
    --output /path/to/report.md
```

### Step 2: Calculate Summary Statistics

For each model, the script computes: mean, median, standard deviation, min/max, percentiles (25th/50th/75th/95th), and win rate (percentage of series where the model performed best). These statistics appear in the generated comparison table.

### Step 3: Identify Winner and Recommendations

The winner is determined by three criteria in priority order: lowest mean sMAPE/MASE, lowest standard deviation (consistency), and highest win rate. The report generates actionable recommendations including production baseline selection, alternative model guidance, and failure case analysis.

### Step 4: Regression Detection (Optional)

Compare current results against a baseline to detect performance degradation. Specify a threshold percentage to control alert sensitivity.

```bash
python {baseDir}/scripts/generate_benchmark_report.py \
    --results current_results.csv \
    --baseline baseline_results.csv \
    --output regression_report.md \
    --threshold 5.0
```

The regression report includes models with degradation, severity percentages, affected series, and a GitHub issue template for tracking regressions.

## Output

- **Standard Report**: Executive summary, comparison table, statistical analysis, winner declaration, recommendations, failure case analysis. See [output-formats.md](references/output-formats.md) for all format options.
- **Regression Report**: Generated when `--baseline` is provided. Includes severity analysis and GitHub issue templates.
- **Executive Summary**: Use `--format executive` for a condensed 1-page report.
- **GitHub Issue Template**: Use `--format github` to produce issue templates for regression tracking.

## Error Handling

See [error-handling.md](references/error-handling.md) for detailed error messages, solutions, and best practices for report automation.

Common issues: missing metrics file, invalid CSV structure (missing required columns), empty results, and regression threshold violations.

## Examples

See [examples.md](references/examples.md) for complete usage examples including standard reports, regression detection, executive summaries, and custom metric focus.

Quick start:
```bash
python {baseDir}/scripts/generate_benchmark_report.py \
    --results nixtla_baseline_m4/results_M4_Daily_h14.csv \
    --output reports/m4_daily_baseline.md --verbose
```

## Resources

- **Script**: `{baseDir}/scripts/generate_benchmark_report.py`
- **Template**: `{baseDir}/assets/templates/report_template.md`
- **Example Report**: [EXAMPLE_REPORT.md](references/EXAMPLE_REPORT.md)
- **M4 Benchmark**: https://github.com/Mcompetitions/M4-methods
- **Forecast Metrics**: https://otexts.com/fpp3/accuracy.html
