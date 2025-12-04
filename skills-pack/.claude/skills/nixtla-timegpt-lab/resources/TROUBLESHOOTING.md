# Nixtla Forecasting Troubleshooting Guide

Common issues and solutions for Nixtla library usage. Reference from main SKILL.md when errors occur.

## Missing Libraries

If Nixtla libraries aren't installed:

```python
# Generate code with clear installation instructions
"""
# Install required Nixtla libraries:
pip install statsforecast mlforecast nixtla

# Or with specific versions:
pip install statsforecast==1.7.0 mlforecast==0.10.0
"""
```

## Schema Mismatches

If user data doesn't match Nixtla schema:

```python
# Detect and fix common issues
# Issue: No 'unique_id' column
if 'unique_id' not in df.columns:
    # Ask: "Is this a single series or multiple series?"
    # If single: df['unique_id'] = 'series_1'
    # If multiple: df['unique_id'] = df['store'] + '_' + df['product']

# Issue: 'ds' is string, not datetime
df['ds'] = pd.to_datetime(df['ds'])

# Issue: Missing values in 'y'
# Recommend: Fill forward, interpolate, or drop
df = df.dropna(subset=['y'])  # Or ffill() or interpolate()
```

## Frequency Detection Failures

```python
# If StatsForecast can't infer frequency
# Solution: Explicitly pass freq parameter
sf = StatsForecast(
    models=models,
    freq='D'  # Daily, or 'H' hourly, 'M' monthly, etc.
)
```
