# Nixtla Schema Contract

**Generated**: [DATE_PLACEHOLDER]
**Source**: [SOURCE_PLACEHOLDER]
**Transformation**: [TRANSFORM_PATH_PLACEHOLDER]

---

## Schema Mapping

| Nixtla Column | Source Column | Type | Description |
|---------------|---------------|------|-------------|
| `unique_id` | [PLACEHOLDER] | string | Series identifier ([N] unique series) |
| `ds` | [PLACEHOLDER] | datetime | Timestamp ([FREQUENCY] frequency) |
| `y` | [PLACEHOLDER] | float | Target: [DESCRIPTION] |

## Exogenous Variables

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| [PLACEHOLDER] | [TYPE] | [DESCRIPTION] | [EXAMPLE] |

---

## Assumptions

1. **Frequency**: [FREQUENCY_PLACEHOLDER] (e.g., Daily D, Hourly H)
   - Inferred from median time delta between observations
   - Each series should have consecutive observations at this frequency

2. **Timezone**: UTC (default)
   - Original timestamp column has no timezone info
   - Converted to UTC for consistency

3. **Missing Values**:
   - Rows with null `y` (target) are dropped
   - Exogenous variables retain nulls (filled downstream if needed)

4. **Series Count**: [COUNT_PLACEHOLDER]
   - Each unique_id represents a separate time series
   - Forecast generated independently per series

---

## Data Quality Checks

Before using transformed data, verify:

- [ ] All series have sufficient history (>= 2 * seasonal period)
- [ ] No gaps in timestamp sequence (or filled with appropriate method)
- [ ] Target (`y`) has no remaining nulls
- [ ] Exogenous variables aligned with forecast horizon

---

## Usage Examples

### Load Transformed Data

```python
from data.transform.to_nixtla_schema import to_nixtla_schema

# Transform source data
df = to_nixtla_schema("[SOURCE_PATH]")

# Inspect
print(df.head())
print(df.info())
```

### Use with StatsForecast

```python
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA, AutoETS

sf = StatsForecast(
    models=[AutoARIMA(), AutoETS(season_length=[SEASON_LENGTH])],
    freq='[FREQUENCY]'
)
sf.fit(df)
forecasts = sf.forecast(h=[HORIZON])
```

### Use with TimeGPT

```python
from nixtla import NixtlaClient

client = NixtlaClient(api_key='YOUR_KEY')
forecast_df = client.forecast(
    df=df,
    h=[HORIZON],
    freq='[FREQUENCY]',
    level=[80, 90]
)
```

---

## Troubleshooting

### Issue: "Frequency cannot be inferred"

**Solution**: Explicitly pass `freq='[FREQUENCY]'` to StatsForecast or TimeGPT.

### Issue: "Duplicate timestamps for same unique_id"

**Solution**: Aggregate duplicates before transformation:
```python
df = df.groupby(['unique_id_col', 'date_col']).agg({'target_col': 'sum'}).reset_index()
```

### Issue: "Too few observations"

**Solution**: Filter series with insufficient history:
```python
# Keep only series with >= 60 observations
counts = df.groupby('unique_id').size()
valid_series = counts[counts >= 60].index
df = df[df['unique_id'].isin(valid_series)]
```

---

## Schema Validation

Run this script to validate Nixtla schema compliance:

```python
import pandas as pd

def validate_nixtla_schema(df: pd.DataFrame) -> bool:
    """Validate that DataFrame matches Nixtla schema."""

    # Check required columns
    required = ['unique_id', 'ds', 'y']
    if not all(col in df.columns for col in required):
        print(f"❌ Missing required columns: {set(required) - set(df.columns)}")
        return False

    # Check types
    if not pd.api.types.is_datetime64_any_dtype(df['ds']):
        print("❌ 'ds' must be datetime type")
        return False

    if not pd.api.types.is_numeric_dtype(df['y']):
        print("❌ 'y' must be numeric type")
        return False

    # Check for nulls in target
    if df['y'].isnull().any():
        print(f"⚠️  {df['y'].isnull().sum()} null values in 'y'")
        return False

    # Check chronological order
    if not df.groupby('unique_id')['ds'].is_monotonic_increasing.all():
        print("⚠️  Data not sorted chronologically within series")
        return False

    print("✅ Nixtla schema validation passed")
    return True

# Run validation
df = to_nixtla_schema("[SOURCE_PATH]")
validate_nixtla_schema(df)
```

---

## Changelog

| Date | Change | Author |
|------|--------|--------|
| [DATE] | Initial schema mapping | nixtla-schema-mapper skill |

---

**Maintained by**: nixtla-schema-mapper (Claude Code skill)
**For questions**: See NIXTLA_SCHEMA_CONTRACT.md in your project
