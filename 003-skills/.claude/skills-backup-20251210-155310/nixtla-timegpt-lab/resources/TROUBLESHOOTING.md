# Nixtla TimeGPT Lab - Troubleshooting Guide

This document contains error handling patterns and solutions for common issues when working with Nixtla libraries.

## Common Error Patterns

### 1. Schema Validation Errors

**Error**: `KeyError: 'unique_id'` or `KeyError: 'ds'` or `KeyError: 'y'`

**Cause**: Data not in Nixtla schema format

**Solution**:
```python
# Check current columns
print(df.columns.tolist())

# Rename to Nixtla schema
df_nixtla = df.rename(columns={
    'product_id': 'unique_id',  # Series identifier
    'date': 'ds',               # Timestamp
    'sales': 'y'                # Target value
})

# Verify schema
assert 'unique_id' in df_nixtla.columns
assert 'ds' in df_nixtla.columns
assert 'y' in df_nixtla.columns
```

### 2. Frequency Detection Failures

**Error**: `ValueError: Could not infer frequency` or `freq must be specified`

**Cause**: Irregular timestamps or missing data

**Solution**:
```python
# Convert to datetime if needed
df['ds'] = pd.to_datetime(df['ds'])

# Sort by time
df = df.sort_values(['unique_id', 'ds'])

# Fill missing dates (if needed)
from statsforecast.utils import generate_series_with_missing_dates

# Or explicitly specify frequency
sf = StatsForecast(models=models, freq='D')  # Daily
sf = StatsForecast(models=models, freq='H')  # Hourly
sf = StatsForecast(models=models, freq='M')  # Monthly

# Common pandas frequency codes:
# 'D' - Daily
# 'H' - Hourly
# 'W' - Weekly
# 'M' - Monthly (end of month)
# 'MS' - Monthly (start of month)
# 'Q' - Quarterly
# 'Y' - Yearly
```

### 3. Missing Library Errors

**Error**: `ModuleNotFoundError: No module named 'statsforecast'`

**Solution**:
```bash
# Install core Nixtla libraries
pip install statsforecast mlforecast utilsforecast

# For TimeGPT
pip install nixtla

# For deep learning models
pip install neuralforecast

# Check installed versions
pip list | grep forecast
```

### 4. TimeGPT API Key Issues

**Error**: `NixtlaAPIKeyError: API key not found`

**Solution**:
```python
import os

# Set API key in environment
os.environ['NIXTLA_API_KEY'] = 'your-api-key-here'

# Or pass directly
from nixtla import NixtlaClient
client = NixtlaClient(api_key='your-api-key-here')

# Verify connection
try:
    client.validate_api_key()
    print("✓ TimeGPT API key valid")
except Exception as e:
    print(f"✗ API key invalid: {e}")
```

### 5. Memory Errors with Large Datasets

**Error**: `MemoryError` or `Out of memory`

**Solution**:
```python
# Use parallel processing with limited workers
sf = StatsForecast(
    models=models,
    freq='D',
    n_jobs=4  # Limit workers (default is -1 = all cores)
)

# Process series in batches
unique_ids = df['unique_id'].unique()
batch_size = 100

for i in range(0, len(unique_ids), batch_size):
    batch_ids = unique_ids[i:i+batch_size]
    df_batch = df[df['unique_id'].isin(batch_ids)]

    sf.fit(df_batch)
    forecasts_batch = sf.predict(h=30)
    # Save batch results
```

### 6. Cross-Validation Window Errors

**Error**: `ValueError: Not enough data points for cross-validation`

**Cause**: Series too short for requested validation windows

**Solution**:
```python
# Check series length
series_lengths = df.groupby('unique_id').size()
min_length = series_lengths.min()
print(f"Shortest series: {min_length} points")

# Adjust CV parameters
h = 14  # Horizon
n_windows = 3  # Number of windows
step_size = 7

# Minimum required length: (n_windows * step_size) + h
min_required = (n_windows * step_size) + h
print(f"Required length: {min_required} points")

# Either reduce n_windows/h or filter short series
df_filtered = df.groupby('unique_id').filter(
    lambda x: len(x) >= min_required
)
```

### 7. Model Fitting Failures

**Error**: `ValueError: Model failed to fit` or convergence warnings

**Solution**:
```python
# Add fallback models
from statsforecast.models import Naive, SeasonalNaive

# Always include simple baselines that never fail
models = [
    Naive(),                    # Fallback: last value
    SeasonalNaive(season_length=7),  # Fallback: seasonal
    AutoARIMA(),                # May fail on some series
    AutoETS(season_length=7)    # May fail on some series
]

# Handle failures gracefully
sf = StatsForecast(models=models, freq='D')
try:
    sf.fit(df)
    forecasts = sf.predict(h=30)
except Exception as e:
    print(f"Some models failed: {e}")
    # Forecasts will still be generated for models that succeeded
```

### 8. Exogenous Variable Issues

**Error**: `ValueError: Future exogenous variables required for prediction`

**Cause**: Model trained with exogenous vars, but not provided for forecast

**Solution**:
```python
# Training with exogenous variables
df_train = pd.DataFrame({
    'unique_id': ['A', 'A', 'A'],
    'ds': pd.date_range('2024-01-01', periods=3),
    'y': [100, 110, 105],
    'temperature': [20, 22, 21],  # Exogenous variable
    'promotion': [0, 1, 0]         # Exogenous variable
})

sf.fit(df_train)

# Must provide future exogenous values for prediction
df_future = pd.DataFrame({
    'unique_id': ['A', 'A'],
    'ds': pd.date_range('2024-01-04', periods=2),
    'temperature': [23, 24],  # Future values required
    'promotion': [0, 0]       # Future values required
})

forecasts = sf.predict(h=2, X_df=df_future)
```

### 9. Seasonal Length Errors

**Error**: `ValueError: season_length must be specified` or poor seasonal model performance

**Solution**:
```python
# Determine appropriate season_length based on frequency
frequency_to_season = {
    'H': 24,      # Hourly: 24 hours in a day
    'D': 7,       # Daily: 7 days in a week
    'W': 52,      # Weekly: 52 weeks in a year
    'M': 12,      # Monthly: 12 months in a year
}

# Or detect from data
from statsforecast.utils import detect_seasonality
season_length = detect_seasonality(df['y'].values, freq='D')

# Use in models
models = [
    SeasonalNaive(season_length=season_length),
    AutoETS(season_length=season_length)
]
```

### 10. TimeGPT Rate Limiting

**Error**: `RateLimitError: Too many requests`

**Solution**:
```python
import time

# Add retry logic with exponential backoff
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def forecast_with_retry(client, df, h):
    return client.forecast(df=df, h=h)

# Use the wrapper
try:
    forecast_df = forecast_with_retry(client, data, h=24)
except Exception as e:
    print(f"Failed after retries: {e}")
    print("Falling back to StatsForecast baselines...")
    # Use baselines instead
```

## Debugging Checklist

When encountering errors, check these in order:

1. **Data Schema**:
   - Do columns include `unique_id`, `ds`, `y`?
   - Is `ds` a datetime type?
   - Is `y` numeric (float or int)?

2. **Frequency**:
   - Is frequency explicitly specified?
   - Are timestamps regular (no gaps)?
   - Are timestamps sorted?

3. **Series Length**:
   - Minimum 2 * season_length observations?
   - Enough data for cross-validation windows?

4. **Library Versions**:
   - statsforecast >= 1.0.0?
   - nixtla >= 0.5.0 (for TimeGPT)?
   - Compatible Python version (3.8+)?

5. **Environment**:
   - NIXTLA_API_KEY set (if using TimeGPT)?
   - Sufficient memory for dataset size?
   - Network connectivity (for TimeGPT)?

## Getting Help

When an error persists:

1. **Check Nixtla docs**:
   - https://nixtla.github.io/statsforecast/
   - https://nixtla.github.io/mlforecast/
   - https://docs.nixtla.io/ (TimeGPT)

2. **Minimal reproducible example**:
   ```python
   import pandas as pd
   from statsforecast import StatsForecast
   from statsforecast.models import AutoETS

   # Minimal data
   df = pd.DataFrame({
       'unique_id': ['A'] * 10,
       'ds': pd.date_range('2024-01-01', periods=10),
       'y': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
   })

   # Minimal model
   sf = StatsForecast(models=[AutoETS()], freq='D')
   sf.fit(df)
   forecasts = sf.predict(h=3)
   print(forecasts)
   ```

3. **Community support**:
   - GitHub issues: https://github.com/Nixtla/statsforecast/issues
   - Slack community: Join via Nixtla website
