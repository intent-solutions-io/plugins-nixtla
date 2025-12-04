# Advanced Features

Advanced configuration patterns for Nixtla experiment architecture. Reference from main SKILL.md when users need complex experiment setups.

## Multiple Data Sources

If user has multiple datasets to compare:

```yaml
# config.yml with multiple experiments
experiments:
  - name: "daily_sales"
    data:
      source: "data/daily_sales.csv"
    forecast:
      horizon: 30
      freq: "D"

  - name: "hourly_traffic"
    data:
      source: "data/traffic.parquet"
    forecast:
      horizon: 168  # 1 week in hours
      freq: "H"
```

Generate loop in experiments.py to run both.

## Custom Model Configuration

Allow users to specify hyperparameters:

```yaml
models:
  statsforecast:
    - name: AutoARIMA
      seasonal: true
      approximation: false

    - name: AutoETS
      model: ["Z", "Z", "Z"]  # error, trend, seasonal
      damped: true

  mlforecast:
    - name: RandomForest
      n_estimators: 200
      max_depth: 10
```

## Hierarchical Forecasting

If user mentions hierarchy (e.g., national → regional → store):

```yaml
hierarchy:
  enabled: true
  levels:
    - national
    - region
    - store
  reconciliation: "bottom_up"  # or "top_down", "optimal_combination"
```

Add `hierarchicalforecast` to experiment harness.

## Ensemble Models

Combine multiple models:

```yaml
ensemble:
  enabled: true
  method: "mean"  # or "median", "weighted"
  models:
    - StatsForecast/AutoARIMA
    - MLForecast/LGBMRegressor
    - TimeGPT
  weights: [0.3, 0.3, 0.4]  # For weighted ensemble
```
