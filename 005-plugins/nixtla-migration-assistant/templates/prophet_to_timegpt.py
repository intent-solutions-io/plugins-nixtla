"""
Template: Prophet to TimeGPT Migration

This template shows the equivalent TimeGPT code for common Prophet patterns.
"""

# =============================================================================
# BEFORE: Prophet Code
# =============================================================================
"""
from prophet import Prophet
import pandas as pd

# Load data
df = pd.read_csv('data.csv')

# Initialize and fit model
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False
)
model.fit(df)

# Create future dataframe
future = model.make_future_dataframe(periods=30)

# Generate forecast
forecast = model.predict(future)
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])
"""

# =============================================================================
# AFTER: TimeGPT Code
# =============================================================================

import pandas as pd
from nixtla import NixtlaClient

# Load data (same format as Prophet: ds, y columns)
df = pd.read_csv('data.csv')

# Add unique_id if not present (required for Nixtla)
if 'unique_id' not in df.columns:
    df['unique_id'] = 'series_1'

# Initialize client
client = NixtlaClient()  # Uses NIXTLA_TIMEGPT_API_KEY env var

# Generate forecast (replaces fit + predict)
forecast = client.forecast(
    df=df,
    h=30,  # horizon (same as periods in Prophet)
    freq='D',  # frequency
    level=[80, 95]  # confidence intervals (similar to Prophet's interval_width)
)

# Results columns: unique_id, ds, TimeGPT, TimeGPT-lo-80, TimeGPT-hi-80, etc.
print(forecast)

# =============================================================================
# Key Differences:
# =============================================================================
# 1. No model fitting required - TimeGPT is a foundation model
# 2. Single API call replaces fit() + make_future_dataframe() + predict()
# 3. Requires unique_id column for time series identification
# 4. Confidence intervals specified via 'level' parameter
# 5. Results are returned immediately (no training time)
