# Benchmark Reporter Examples

## Example 1: Generate Standard Benchmark Report

```bash
python {baseDir}/scripts/generate_benchmark_report.py \
    --results nixtla_baseline_m4/results_M4_Daily_h14.csv \
    --output reports/m4_daily_baseline.md \
    --verbose
```

**Output**:
```
Loaded 150 results (50 series x 3 models)
Calculated summary statistics
Identified winner: AutoTheta (mean sMAPE: 12.3%)
Generated report: reports/m4_daily_baseline.md (1,245 words)
```

## Example 2: Detect Regressions vs. Baseline

```bash
python {baseDir}/scripts/generate_benchmark_report.py \
    --results current_run/results.csv \
    --baseline baseline/v1.0_results.csv \
    --output regression_report.md \
    --threshold 3.0
```

**Output**:
```
REGRESSION DETECTED in 2/3 models:
  - AutoETS: sMAPE 13.5% -> 14.8% (+9.6%)
  - AutoTheta: sMAPE 12.3% -> 12.7% (+3.3%)
Generated regression report with GitHub issue template
```

## Example 3: Generate Executive Summary

```bash
python {baseDir}/scripts/generate_benchmark_report.py \
    --results quarterly_benchmark.csv \
    --format executive \
    --output Q1_summary.md
```

**Output**:
```markdown
# Q1 2025 Forecast Baseline Report

**Winner**: AutoTheta with 12.3% sMAPE (vs. 13.5% AutoETS, 15.2% Naive)

**Key Findings**:
- AutoTheta won 64% of series (32/50)
- Most consistent performance (std dev 4.2%)
- Recommended for production baseline

**Action Items**:
- Deploy AutoTheta as default model
- Use AutoETS for highly seasonal data (criteria: seasonal_strength > 0.8)
- Investigate 3 failure cases (sMAPE > 30%)
```

## Example 4: Custom Metric Focus

```bash
python {baseDir}/scripts/generate_benchmark_report.py \
    --results results.csv \
    --primary-metric MASE \
    --output mase_focused_report.md
```
