# Nixtla TimeGPT Lab - Complete Examples

This document contains complete working examples for common forecasting scenarios using Nixtla libraries.

## Example 1: Basic Forecasting Workflow

Complete end-to-end forecasting example:

```python
import pandas as pd
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA, AutoETS, SeasonalNaive

# Step 1: Load and prepare data
df_raw = pd.read_csv('sales_data.csv')

# Step 2: Transform to Nixtla schema (unique_id, ds, y)
df = df_raw.rename(columns={
    'store_id': 'unique_id',
    'date': 'ds',
    'sales': 'y'
})

# Convert date to datetime
df['ds'] = pd.to_datetime(df['ds'])

# Step 3: Define baseline models
models = [
    SeasonalNaive(season_length=7),  # Weekly seasonality baseline
    AutoARIMA(),                     # Auto ARIMA
    AutoETS(season_length=7)         # Exponential smoothing
]

# Step 4: Initialize StatsForecast
sf = StatsForecast(
    models=models,
    freq='D',      # Daily frequency
    n_jobs=-1      # Use all CPU cores
)

# Step 5: Fit models
sf.fit(df)

# Step 6: Generate forecasts with prediction intervals
forecasts = sf.forecast(h=30, level=[80, 90])

# Step 7: Inspect results
print(forecasts.head())
# Columns: ds, unique_id, SeasonalNaive, AutoARIMA, AutoETS,
#          AutoARIMA-lo-80, AutoARIMA-hi-80, AutoARIMA-lo-90, AutoARIMA-hi-90
```

## Example 2: Model Comparison with Cross-Validation

Systematically compare models to select the best one:

```python
from statsforecast import StatsForecast
from statsforecast.models import (
    Naive, SeasonalNaive,
    AutoARIMA, AutoETS, AutoTheta
)
from utilsforecast.evaluation import evaluate
from utilsforecast.losses import mae, smape, mase

# Define model suite
models = [
    Naive(),                         # Simple baseline
    SeasonalNaive(season_length=7),  # Seasonal baseline
    AutoARIMA(),                     # ARIMA
    AutoETS(season_length=7),        # ETS
    AutoTheta(season_length=7)       # Theta method
]

# Initialize StatsForecast
sf = StatsForecast(models=models, freq='D')
sf.fit(df)

# Cross-validation with 8 windows
cv_df = sf.cross_validation(
    df=df,
    h=14,          # Forecast 2 weeks ahead
    step_size=7,   # Move window by 1 week
    n_windows=8    # 8 validation folds
)

# Calculate metrics
metrics_df = evaluate(
    cv_df,
    metrics=[mae, smape, mase],
    models=['Naive', 'SeasonalNaive', 'AutoARIMA', 'AutoETS', 'AutoTheta']
)

# Aggregate by model
summary = metrics_df.groupby('model')[['mae', 'smape', 'mase']].mean()
print(summary.sort_values('smape'))

# Select best model (lowest SMAPE)
best_model = summary.sort_values('smape').index[0]
print(f"\nBest model: {best_model}")
```

## Example 3: TimeGPT vs Baseline Comparison

Compare TimeGPT against statistical baselines:

```python
import os
import pandas as pd
from nixtla import NixtlaClient
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA, AutoETS, SeasonalNaive
from utilsforecast.losses import mae, smape

# Check for API key
if not os.getenv('NIXTLA_API_KEY'):
    raise ValueError("Set NIXTLA_API_KEY environment variable")

# Initialize clients
nixtla_client = NixtlaClient()
sf = StatsForecast(
    models=[SeasonalNaive(season_length=7), AutoARIMA(), AutoETS()],
    freq='D'
)

# Split data (train/test)
train_df = df[df['ds'] < '2024-03-01']
test_df = df[df['ds'] >= '2024-03-01']

# Generate TimeGPT forecasts
timegpt_fcst = nixtla_client.forecast(
    df=train_df,
    h=30,
    level=[80, 90]
)

# Generate StatsForecast baselines
sf.fit(train_df)
baseline_fcst = sf.forecast(h=30, level=[80, 90])

# Merge with actuals
timegpt_eval = test_df.merge(timegpt_fcst, on=['unique_id', 'ds'])
baseline_eval = test_df.merge(baseline_fcst, on=['unique_id', 'ds'])

# Calculate errors
timegpt_mae = mae(timegpt_eval['y'], timegpt_eval['TimeGPT'])
baseline_mae = {
    'SeasonalNaive': mae(baseline_eval['y'], baseline_eval['SeasonalNaive']),
    'AutoARIMA': mae(baseline_eval['y'], baseline_eval['AutoARIMA']),
    'AutoETS': mae(baseline_eval['y'], baseline_eval['AutoETS'])
}

print(f"TimeGPT MAE: {timegpt_mae:.2f}")
for model, error in baseline_mae.items():
    print(f"{model} MAE: {error:.2f}")
```

## Example 4: MLForecast with Feature Engineering

Use machine learning with engineered features:

```python
import pandas as pd
from mlforecast import MLForecast
from mlforecast.lag_transforms import rolling_mean, expanding_std
from sklearn.ensemble import LGBMRegressor, RandomForestRegressor

# Prepare data in Nixtla format
df = pd.DataFrame({
    'unique_id': ['A'] * 100 + ['B'] * 100,
    'ds': pd.date_range('2023-01-01', periods=100).tolist() * 2,
    'y': [100 + i + (i % 7) * 5 for i in range(100)] * 2
})

# Initialize MLForecast with lag features
mlf = MLForecast(
    models=[
        LGBMRegressor(verbosity=-1),
        RandomForestRegressor(n_estimators=100)
    ],
    freq='D',
    lags=[1, 7, 14, 28],  # Lag features: 1 day, 1 week, 2 weeks, 4 weeks
    lag_transforms={
        7: [rolling_mean],    # 7-day rolling mean
        28: [expanding_std]   # Expanding standard deviation
    },
    date_features=['dayofweek', 'month', 'quarter']  # Calendar features
)

# Fit and forecast
mlf.fit(df)
forecasts = mlf.predict(h=30)

print(forecasts.head())
# Includes predictions from both LGBMRegressor and RandomForestRegressor
```

## Example 5: Multiple Series Forecasting

Forecast many series at scale:

```python
import pandas as pd
import numpy as np
from statsforecast import StatsForecast
from statsforecast.models import AutoETS, AutoARIMA

# Generate sample data with 100 series
np.random.seed(42)
n_series = 100
n_periods = 200

data = []
for i in range(n_series):
    dates = pd.date_range('2023-01-01', periods=n_periods, freq='D')
    values = 100 + np.cumsum(np.random.randn(n_periods)) + \
             10 * np.sin(np.arange(n_periods) * 2 * np.pi / 7)  # Weekly pattern

    for date, value in zip(dates, values):
        data.append({
            'unique_id': f'series_{i:03d}',
            'ds': date,
            'y': value
        })

df = pd.DataFrame(data)

# Forecast all series in parallel
sf = StatsForecast(
    models=[AutoETS(), AutoARIMA()],
    freq='D',
    n_jobs=-1  # Parallel processing
)

sf.fit(df)
forecasts = sf.forecast(h=30, level=[90])

# Analyze results by series
print(f"Total series: {forecasts['unique_id'].nunique()}")
print(f"Forecast shape: {forecasts.shape}")
print(forecasts.groupby('unique_id').head(3))
```

## Example 6: Data Transformation and Validation

Transform raw data to Nixtla schema with validation:

```python
import pandas as pd

# Raw data (not in Nixtla format)
df_raw = pd.DataFrame({
    'transaction_date': ['2024-01-01', '2024-01-02', '2024-01-03'] * 2,
    'product_code': ['SKU_A', 'SKU_A', 'SKU_A', 'SKU_B', 'SKU_B', 'SKU_B'],
    'store': ['NYC', 'NYC', 'NYC', 'LA', 'LA', 'LA'],
    'revenue': [1000, 1100, 1050, 2000, 2100, 2050]
})

# Step 1: Transform to Nixtla schema
df_nixtla = df_raw.copy()

# Create unique_id from product + store
df_nixtla['unique_id'] = df_nixtla['product_code'] + '_' + df_nixtla['store']

# Rename columns
df_nixtla = df_nixtla.rename(columns={
    'transaction_date': 'ds',
    'revenue': 'y'
})

# Convert ds to datetime
df_nixtla['ds'] = pd.to_datetime(df_nixtla['ds'])

# Keep only required columns
df_nixtla = df_nixtla[['unique_id', 'ds', 'y']]

# Step 2: Validate schema
required_cols = ['unique_id', 'ds', 'y']
assert all(col in df_nixtla.columns for col in required_cols), \
    f"Missing required columns. Need: {required_cols}"

# Check data types
assert pd.api.types.is_datetime64_any_dtype(df_nixtla['ds']), \
    "Column 'ds' must be datetime"
assert pd.api.types.is_numeric_dtype(df_nixtla['y']), \
    "Column 'y' must be numeric"

# Check for missing values
assert not df_nixtla['y'].isna().any(), \
    "Column 'y' contains missing values"

# Step 3: Sort by time
df_nixtla = df_nixtla.sort_values(['unique_id', 'ds']).reset_index(drop=True)

print("Schema validation passed!")
print(df_nixtla.head(10))
```

## Example 7: Forecast with Exogenous Variables

Incorporate external factors:

```python
import pandas as pd
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA

# Historical data with exogenous variables
df_train = pd.DataFrame({
    'unique_id': ['store_1'] * 90,
    'ds': pd.date_range('2024-01-01', periods=90),
    'y': [100 + i * 0.5 + (i % 7) * 10 for i in range(90)],  # Sales
    'promotion': [1 if i % 7 in [5, 6] else 0 for i in range(90)],  # Weekend promos
    'temperature': [20 + (i % 30) - 15 for i in range(90)]  # Temp cycles
})

# Future exogenous values (known for forecast period)
df_future = pd.DataFrame({
    'unique_id': ['store_1'] * 30,
    'ds': pd.date_range('2024-04-01', periods=30),
    'promotion': [1 if i % 7 in [5, 6] else 0 for i in range(30)],  # Planned promos
    'temperature': [25] * 30  # Weather forecast
})

# Forecast with exogenous variables
sf = StatsForecast(models=[AutoARIMA()], freq='D')
sf.fit(df_train)

# Must provide X_df with future exogenous values
forecasts = sf.predict(h=30, X_df=df_future)

print(forecasts.head())
```

## Example 8: Cross-Validation with Custom Metrics

Detailed cross-validation with multiple metrics:

```python
from statsforecast import StatsForecast
from statsforecast.models import AutoETS, AutoTheta, SeasonalNaive
from utilsforecast.evaluation import evaluate
from utilsforecast.losses import mae, mape, smape, rmse, mase

# Define models
models = [
    SeasonalNaive(season_length=7),
    AutoETS(season_length=7),
    AutoTheta(season_length=7)
]

# Cross-validation setup
sf = StatsForecast(models=models, freq='D')

cv_results = sf.cross_validation(
    df=df,
    h=14,           # 2-week forecast horizon
    step_size=7,    # Slide window by 1 week
    n_windows=12,   # 12 validation windows (~3 months)
    refit=True      # Refit model each window
)

# Evaluate with multiple metrics
metrics_df = evaluate(
    cv_results,
    metrics=[mae, mape, smape, rmse, mase],
    models=['SeasonalNaive', 'AutoETS', 'AutoTheta']
)

# Aggregate results
summary = metrics_df.groupby('model').agg({
    'mae': ['mean', 'std'],
    'smape': ['mean', 'std'],
    'mase': ['mean', 'std']
})

print("Cross-Validation Results:")
print(summary)

# Find best model for each metric
for metric in ['mae', 'smape', 'mase']:
    best_model = metrics_df.groupby('model')[metric].mean().idxmin()
    best_value = metrics_df.groupby('model')[metric].mean().min()
    print(f"\nBest model for {metric.upper()}: {best_model} ({best_value:.2f})")
```

## Reference Documentation

For more details, see:
- **StatsForecast**: https://nixtla.github.io/statsforecast/
- **MLForecast**: https://nixtla.github.io/mlforecast/
- **TimeGPT**: https://docs.nixtla.io/
- **Troubleshooting**: See `resources/TROUBLESHOOTING.md`
- **Advanced Patterns**: See `resources/ADVANCED_PATTERNS.md`
