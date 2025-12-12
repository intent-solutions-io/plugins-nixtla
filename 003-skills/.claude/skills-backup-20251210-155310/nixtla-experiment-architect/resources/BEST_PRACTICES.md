# Best Practices

Production-grade forecasting experiment best practices using Nixtla libraries.

## 1. Always Include Naive Baselines

```yaml
models:
  statsforecast:
    - SeasonalNaive  # Critical baseline (never skip!)
    - AutoARIMA
    - AutoETS
```

**Why**: MASE metric requires naive baseline for normalization.

## 2. Match Seasonality to Frequency

```yaml
# Daily data → weekly seasonality
forecast:
  freq: "D"
  season_length: 7

# Hourly data → daily seasonality
forecast:
  freq: "H"
  season_length: 24

# Monthly data → yearly seasonality
forecast:
  freq: "M"
  season_length: 12
```

## 3. Cross-Validation Window Sizing

```yaml
cv:
  h: 14              # Should match production forecast horizon
  step_size: 7       # Smaller = more validation folds (slower but more robust)
  n_windows: 4       # More windows = better error estimates
```

**Rule of thumb**: Use at least 4 windows for stable metric estimates.

## 4. Progressive Model Addition

Start simple, add complexity:

1. **Phase 1**: StatsForecast baselines only
2. **Phase 2**: Add MLForecast (if helpful)
3. **Phase 3**: Add TimeGPT (if budget allows)

This allows comparing cost vs accuracy tradeoffs.
