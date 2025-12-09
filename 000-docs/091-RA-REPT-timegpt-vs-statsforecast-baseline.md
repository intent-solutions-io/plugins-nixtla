# TimeGPT vs StatsForecast Baseline Comparison

**Generated**: 2025-12-08 21:56:29 CST
**Aggregator**: `004-scripts/compare_timegpt_vs_statsforecast.py`

## Executive Summary

**Current Status**: TimeGPT-only report (2 experiments). StatsForecast baseline results are not yet available. This report will be updated with a full comparison once baseline metrics are generated.

## StatsForecast Baseline Status

**Status**: PENDING

No StatsForecast baseline CSV found at:
```
002-workspaces/statsforecast-lab/reports/statsforecast_baseline_results.csv
```

**To generate baseline metrics**:
```bash
cd 002-workspaces/statsforecast-lab
python scripts/run_statsforecast_baseline.py
```

Once baseline results exist, re-run:
```bash
python 004-scripts/compare_timegpt_vs_statsforecast.py
```

## TimeGPT Results

| Model | Horizon | Avg sMAPE | Avg MAE |
|-------|---------|-----------|---------|
| timegpt_baseline_14d | 14d | 3.11% | 6.2179 |
| timegpt_baseline_28d | 28d | 5.83% | 11.1607 |

## Dataset

- **Series**: 2 time series
- **Source**: M4-style daily data
- **Evaluation**: Train/test split with holdout period

## How to Reproduce

### 1. Run TimeGPT Experiments
```bash
cd 002-workspaces/timegpt-lab
export NIXTLA_TIMEGPT_API_KEY='your_key_here'
python scripts/run_experiment.py
```

### 2. Run StatsForecast Baselines
```bash
cd 002-workspaces/statsforecast-lab
python scripts/run_statsforecast_baseline.py
```

### 3. Generate Comparison
```bash
python 004-scripts/compare_timegpt_vs_statsforecast.py
```

---

**Report Type**: Research Analysis (RA-REPT)
**Phase**: 08 - Cross-Lab Benchmark
**Owner**: intent solutions io
**Contact**: jeremy@intentsolutions.io