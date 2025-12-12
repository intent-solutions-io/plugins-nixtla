# Nixtla Schema Contract Template

Use this template to document your data transformation to Nixtla format.

---

# Nixtla Schema Contract

**Source**: `{source_path or description}`
**Transformation**: `{transformation_module_path}`
**Generated**: `{date}`
**Version**: `1.0.0`

## Overview

Brief description of data source, business context, and forecasting objective.

## Schema Mapping

| Nixtla Column | Source Column | Type | Description | Transformation |
|---------------|---------------|------|-------------|----------------|
| `unique_id` | `{source_col}` | string | Series identifier | `CAST AS VARCHAR` |
| `ds` | `{source_col}` | datetime | Timestamp | `pd.to_datetime()` or `CAST AS TIMESTAMP` |
| `y` | `{source_col}` | float | Target variable | `CAST AS FLOAT64` |

### Series Metadata

- **Number of series**: `{count}`
- **Series granularity**: `{description, e.g., "one per store"}`
- **Example series IDs**: `{example_1, example_2, example_3}`

### Temporal Characteristics

- **Frequency**: `{daily, hourly, monthly, etc.}`
- **Date range**: `{min_date}` to `{max_date}`
- **Total observations**: `{row_count}`
- **Observations per series**: `{avg}` (avg), `{min}` (min), `{max}` (max)

## Exogenous Variables (Optional)

| Column | Type | Description | Range/Values |
|--------|------|-------------|--------------|
| `{col_name}` | `{type}` | `{description}` | `{range or categorical values}` |

## Data Quality Rules

**Filters applied**:
- Removed rows where `y IS NULL`
- Removed rows where `{custom_condition}`

**Type conversions**:
- `unique_id`: String casting with `str()` or `CAST AS VARCHAR`
- `ds`: Datetime parsing with format `{format_string}`
- `y`: Numeric conversion with `pd.to_numeric(errors='coerce')`

**Constraints**:
- No duplicate `(unique_id, ds)` pairs
- Sorted by `unique_id`, `ds` ascending
- All required columns non-null

## Validation Script

```python
import pandas as pd

def validate_nixtla_schema(df: pd.DataFrame) -> bool:
    """Validate DataFrame meets Nixtla schema requirements."""

    # Check required columns exist
    required_cols = ['unique_id', 'ds', 'y']
    assert all(col in df.columns for col in required_cols), "Missing required columns"

    # Check types
    assert df['unique_id'].dtype == 'object', "unique_id must be string/object"
    assert pd.api.types.is_datetime64_any_dtype(df['ds']), "ds must be datetime"
    assert pd.api.types.is_numeric_dtype(df['y']), "y must be numeric"

    # Check no nulls in required columns
    assert df['unique_id'].notna().all(), "unique_id contains NaN"
    assert df['ds'].notna().all(), "ds contains NaN"
    assert df['y'].notna().all(), "y contains NaN"

    # Check sorting
    df_sorted = df.sort_values(['unique_id', 'ds']).reset_index(drop=True)
    assert df.equals(df_sorted), "Data not sorted by unique_id, ds"

    # Check for duplicates
    duplicates = df.duplicated(subset=['unique_id', 'ds']).sum()
    assert duplicates == 0, f"Found {duplicates} duplicate (unique_id, ds) pairs"

    print("✓ All validation checks passed")
    return True

# Run validation
df = pd.read_csv("data/sales_nixtla.csv")
validate_nixtla_schema(df)
```

## Usage Examples

### Basic Forecasting

```python
from data.transform.to_nixtla_schema import to_nixtla_schema
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA, AutoETS

# Transform data
df = to_nixtla_schema("{source_path}")

# Forecast
sf = StatsForecast(models=[AutoARIMA(), AutoETS()], freq='{frequency}')
sf.fit(df)
forecasts = sf.forecast(h={horizon})
```

### With TimeGPT (API)

```python
from nixtla import NixtlaClient

# Transform data
df = to_nixtla_schema("{source_path}")

# Forecast with TimeGPT
client = NixtlaClient(api_key='your-api-key')
forecasts = client.forecast(df=df, h={horizon}, freq='{frequency}')
```

### Cross-Validation

```python
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA

df = to_nixtla_schema("{source_path}")

sf = StatsForecast(models=[AutoARIMA()], freq='{frequency}')
cv_results = sf.cross_validation(df=df, h={horizon}, step_size={step}, n_windows={n_windows})
```

## Known Issues & Assumptions

**Assumptions**:
- `{Assumption 1, e.g., "All stores have daily observations"}`
- `{Assumption 2, e.g., "Missing dates indicate closed days, not data gaps"}`

**Known data quality issues**:
- `{Issue 1, e.g., "Store #42 has 10 outliers in Jan 2023"}`
- `{Issue 2, e.g., "Holiday column has 5% missing values"}`

**Handling missing values**:
- `{Strategy, e.g., "Forward fill up to 3 days, drop series with >10% missing"}`

## Troubleshooting

### Error: "Missing columns: ['store_id']"

**Solution**: Verify source data has all required columns. Update `to_nixtla_schema()` parameters to match your column names.

### Error: "y contains NaN after cleanup"

**Solution**: Check source data for null values. Add imputation or filtering logic before transformation.

### Warning: "Duplicate (unique_id, ds) pairs found"

**Solution**: Aggregate duplicates or investigate data quality issue in source system.

## Maintenance

**Update frequency**: `{e.g., "Re-run transformation daily via cron job"}`
**Owner**: `{team or individual}`
**Last validated**: `{date}`

---

## References

- [Nixtla Schema Documentation](https://nixtla.github.io/statsforecast/docs/getting-started/input-format.html)
- [Source data documentation]: `{link}`
- [Forecasting pipeline repo]: `{link}`
