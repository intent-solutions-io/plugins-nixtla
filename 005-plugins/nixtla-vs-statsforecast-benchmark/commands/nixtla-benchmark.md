---
name: nixtla-benchmark
description: Run TimeGPT vs StatsForecast head-to-head comparison
---

# /nixtla-benchmark

Run TimeGPT vs StatsForecast head-to-head comparison.

## Usage

```
/nixtla-benchmark [data_path] [--horizon=14] [--freq=D]
```

## Workflow

1. Load user's time series data
2. Split into train/test
3. Run TimeGPT forecast
4. Run StatsForecast models (AutoETS, AutoTheta, etc.)
5. Calculate accuracy metrics (sMAPE, MASE, RMSE)
6. Generate comparison report

## Parameters

- `data_path`: Path to CSV with columns (unique_id, ds, y)
- `--horizon`: Forecast horizon (default: 14)
- `--freq`: Frequency (D, H, W, M)
- `--models`: StatsForecast models to compare

## Output

- Accuracy comparison table
- Speed benchmark
- Cost analysis
- Recommendation report
