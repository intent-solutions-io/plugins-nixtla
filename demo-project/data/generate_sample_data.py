"""
Generate Sample Time Series Data for Nixtla Skills Demo

This script creates synthetic time series data in Nixtla format (unique_id, ds, y)
with realistic patterns for demonstrating forecasting skills.

Generated data includes:
- 3 different series (product_A, product_B, product_C)
- Daily frequency
- 365 days of historical data (1 year)
- Trend, weekly seasonality, and noise
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Date range: 1 year of daily data
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)
dates = pd.date_range(start=start_date, end=end_date, freq='D')

def generate_series(unique_id, base_level, trend_slope, seasonality_amplitude, noise_level):
    """
    Generate a single time series with trend, weekly seasonality, and noise

    Parameters:
    - unique_id: Series identifier
    - base_level: Starting value
    - trend_slope: Linear trend per day
    - seasonality_amplitude: Weekly seasonality amplitude
    - noise_level: Random noise standard deviation
    """
    n = len(dates)

    # Linear trend
    trend = base_level + trend_slope * np.arange(n)

    # Weekly seasonality (7-day cycle)
    # Peak on weekends (days 5-6), lower on weekdays
    seasonality = seasonality_amplitude * np.sin(2 * np.pi * np.arange(n) / 7)

    # Random noise
    noise = np.random.normal(0, noise_level, n)

    # Combine components (ensure no negative values)
    values = np.maximum(trend + seasonality + noise, 0)

    # Create dataframe
    df = pd.DataFrame({
        'unique_id': unique_id,
        'ds': dates,
        'y': values
    })

    return df

# Generate 3 different series with different characteristics

# Product A: Strong upward trend, moderate seasonality
product_a = generate_series(
    unique_id='product_A',
    base_level=100,
    trend_slope=0.5,  # Growing ~0.5 units/day
    seasonality_amplitude=15,
    noise_level=8
)

# Product B: Slight downward trend, strong seasonality
product_b = generate_series(
    unique_id='product_B',
    base_level=200,
    trend_slope=-0.2,  # Declining ~0.2 units/day
    seasonality_amplitude=30,
    noise_level=12
)

# Product C: Flat trend, weak seasonality (harder to forecast)
product_c = generate_series(
    unique_id='product_C',
    base_level=150,
    trend_slope=0.05,
    seasonality_amplitude=10,
    noise_level=20  # High noise makes this challenging
)

# Combine all series
all_series = pd.concat([product_a, product_b, product_c], ignore_index=True)

# Save to CSV
output_path = 'demo-project/data/sample_series.csv'
all_series.to_csv(output_path, index=False)

print(f"✅ Generated sample data: {output_path}")
print(f"   - 3 series (product_A, product_B, product_C)")
print(f"   - {len(dates)} days per series (365 days)")
print(f"   - Total rows: {len(all_series)}")
print(f"\nData preview:")
print(all_series.head(10))
print("\nSummary statistics:")
print(all_series.groupby('unique_id')['y'].describe())
