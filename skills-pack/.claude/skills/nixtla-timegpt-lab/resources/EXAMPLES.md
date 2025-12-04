# Nixtla Forecasting Examples

Complete working examples for common Nixtla forecasting scenarios. Reference from main SKILL.md.

## Example 1: Basic Forecasting

**User**: "I have daily sales data, need to forecast next 30 days"

**Your response**:
```python
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA, AutoETS, SeasonalNaive

# Ensure data is in Nixtla format: unique_id, ds, y
# If not, transform it first

models = [
    SeasonalNaive(season_length=7),  # Weekly baseline
    AutoARIMA(),
    AutoETS(season_length=7)
]

sf = StatsForecast(models=models, freq='D', n_jobs=-1)
sf.fit(df)

# Forecast next 30 days
forecasts = sf.forecast(h=30, level=[80, 90])
print(forecasts)
```

## Example 2: Model Comparison with CV

**User**: "Which model is best for my data?"

**Your response**:
```python
# Cross-validation to compare models
cv_df = sf.cross_validation(
    df=df,
    h=14,          # 2-week horizon
    step_size=7,   # Weekly validation
    n_windows=8    # 8 validation folds
)

# Evaluate metrics
from utilsforecast.evaluation import evaluate
from utilsforecast.losses import smape, mase

metrics_df = evaluate(
    cv_df,
    metrics=[smape, mase],
    models=['SeasonalNaive', 'AutoARIMA', 'AutoETS']
)

# Show results
print(metrics_df.groupby('model')[['smape', 'mase']].mean())
# Pick model with lowest SMAPE or MASE
```

## Example 3: TimeGPT Integration

**User**: "Can I use TimeGPT here?"

**Your response**:
```python
import os
from nixtla import NixtlaClient

if not os.getenv('NIXTLA_API_KEY'):
    print("Set NIXTLA_API_KEY environment variable first:")
    print("export NIXTLA_API_KEY='your-key-here'")
else:
    client = NixtlaClient()

    # Forecast with TimeGPT
    timegpt_fcst = client.forecast(
        df=df,
        h=30,
        freq='D',
        level=[80, 90]  # Conformal intervals
    )

    # Compare to StatsForecast baselines
    # [Show comparison code]
```
