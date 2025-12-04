# Advanced Features

Advanced schema mapping patterns for Nixtla data transformation.

## Multi-Source Mapping

If user has multiple data sources to combine:

```python
def to_nixtla_schema_combined(
    sales_path: str,
    weather_path: str
) -> pd.DataFrame:
    """
    Combine sales + weather data into Nixtla schema.
    """
    # Load sources
    sales = pd.read_csv(sales_path)
    weather = pd.read_csv(weather_path)

    # Transform sales to Nixtla schema
    df_sales = sales.rename(columns={
        'store_id': 'unique_id',
        'date': 'ds',
        'sales': 'y'
    })
    df_sales['ds'] = pd.to_datetime(df_sales['ds'])

    # Transform weather
    df_weather = weather.rename(columns={'date': 'ds'})
    df_weather['ds'] = pd.to_datetime(df_weather['ds'])

    # Join (left join to preserve all sales observations)
    df_combined = df_sales.merge(
        df_weather[['ds', 'temperature', 'precipitation']],
        on='ds',
        how='left'
    )

    return df_combined
```

## Type Casting and Cleaning

Add robust data quality fixes:

```python
def to_nixtla_schema(source_path: str) -> pd.DataFrame:
    # ... load data ...

    # Robust timestamp parsing
    df_nixtla['ds'] = pd.to_datetime(
        df['date'],
        errors='coerce',  # Invalid dates → NaT
        infer_datetime_format=True
    )

    # Drop invalid timestamps
    df_nixtla = df_nixtla.dropna(subset=['ds'])

    # Robust numeric conversion
    df_nixtla['y'] = pd.to_numeric(
        df['sales'],
        errors='coerce'  # Invalid numbers → NaN
    )

    # Handle negative sales (if invalid)
    df_nixtla.loc[df_nixtla['y'] < 0, 'y'] = pd.NA

    # Drop nulls in target
    df_nixtla = df_nixtla.dropna(subset=['y'])

    return df_nixtla
```

## Frequency Detection

Auto-detect frequency from timestamp deltas:

```python
def infer_frequency(df: pd.DataFrame) -> str:
    """Infer pandas frequency string from timestamp deltas."""
    time_deltas = df.groupby('unique_id')['ds'].diff()
    median_delta = time_deltas.median()

    # Map to pandas freq strings
    if median_delta <= pd.Timedelta(hours=1):
        return 'H'  # Hourly
    elif median_delta <= pd.Timedelta(days=1):
        return 'D'  # Daily
    elif median_delta <= pd.Timedelta(weeks=1):
        return 'W'  # Weekly
    elif median_delta <= pd.Timedelta(days=31):
        return 'M'  # Monthly
    else:
        return 'Y'  # Yearly

freq = infer_frequency(df_nixtla)
print(f"Detected frequency: {freq}")
```
