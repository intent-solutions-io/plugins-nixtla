#!/usr/bin/env python3
"""
Nixtla Schema Contract Generator

Creates comprehensive schema contract documentation with validation rules,
data quality checks, and usage examples.

Usage:
    python create_contract.py --mapping mapping.json --output NIXTLA_SCHEMA_CONTRACT.md
    python create_contract.py --input data/sales.csv --id_col store_id --date_col date --target_col sales
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd


def sanitize_path(user_path: str, allowed_dirs: list = None, purpose: str = "file") -> Path:
    """
    Sanitize user-provided path to prevent path traversal attacks.

    Args:
        user_path: User-provided path string
        allowed_dirs: List of allowed parent directories (None = cwd only)
        purpose: Description for error messages

    Returns:
        Resolved, validated Path object

    Raises:
        ValueError: If path attempts traversal outside allowed directories

    OWASP Reference: A01:2021 - Broken Access Control
    """
    if allowed_dirs is None:
        allowed_dirs = [Path.cwd()]

    # Resolve to absolute path
    resolved = Path(user_path).resolve()

    # Check for path traversal attempts
    if ".." in str(user_path):
        raise ValueError(
            f"Security: Path traversal detected in {purpose} path. "
            f"Relative parent references (..) are not allowed."
        )

    # Verify path is within allowed directories
    is_allowed = any(
        resolved == allowed_dir or str(resolved).startswith(str(allowed_dir.resolve()) + "/")
        for allowed_dir in allowed_dirs
    )

    if not is_allowed:
        raise ValueError(
            f"Security: {purpose.capitalize()} path must be within allowed directories. "
            f"Path '{resolved}' is outside permitted locations."
        )

    return resolved


CONTRACT_TEMPLATE = '''# Nixtla Schema Contract

**Source**: `{source_path}`
**Transformation Module**: `{transform_module}`
**Generated**: `{generated_date}`
**Version**: `1.0.0`

## Overview

{overview}

## Schema Mapping

| Nixtla Column | Source Column | Type | Description | Transformation |
|---------------|---------------|------|-------------|----------------|
| `unique_id` | `{id_col}` | {id_type} | Series identifier | `astype(str)` |
| `ds` | `{date_col}` | {date_type} | Timestamp | `pd.to_datetime()` |
| `y` | `{target_col}` | {target_type} | Target variable | `pd.to_numeric()` |

### Series Metadata

- **Number of series**: {series_count:,}
- **Series granularity**: {series_granularity}
- **Example series IDs**: {example_series_ids}

### Temporal Characteristics

- **Frequency**: {frequency}
- **Date range**: `{date_min}` to `{date_max}`
- **Total observations**: {total_observations:,}
- **Observations per series**: {obs_avg:.1f} (avg), {obs_min} (min), {obs_max} (max)

## Exogenous Variables

{exogenous_table}

## Data Quality Rules

**Filters applied**:
- Remove rows where `y IS NULL`
- Remove rows where `ds IS NULL`
- Remove duplicate `(unique_id, ds)` pairs (keep first)
{additional_filters}

**Type conversions**:
- `unique_id`: String casting with `astype(str)`
- `ds`: Datetime parsing with `pd.to_datetime()`
- `y`: Numeric conversion with `pd.to_numeric(errors='coerce')`

**Constraints**:
- No duplicate `(unique_id, ds)` pairs
- Sorted by `unique_id`, `ds` ascending
- All required columns non-null

## Validation Script

```python
import pandas as pd


def validate_nixtla_schema(df: pd.DataFrame) -> bool:
    """
    Validate DataFrame meets Nixtla schema requirements.

    Args:
        df: DataFrame to validate

    Returns:
        True if all checks pass

    Raises:
        AssertionError: If validation fails
    """
    # Check required columns exist
    required_cols = ['unique_id', 'ds', 'y']
    assert all(col in df.columns for col in required_cols), \\
        f"Missing required columns: {{set(required_cols) - set(df.columns)}}"

    # Check types
    assert df['unique_id'].dtype == 'object', \\
        f"unique_id must be string/object, got {{df['unique_id'].dtype}}"
    assert pd.api.types.is_datetime64_any_dtype(df['ds']), \\
        f"ds must be datetime, got {{df['ds'].dtype}}"
    assert pd.api.types.is_numeric_dtype(df['y']), \\
        f"y must be numeric, got {{df['y'].dtype}}"

    # Check no nulls in required columns
    assert df['unique_id'].notna().all(), "unique_id contains NaN"
    assert df['ds'].notna().all(), "ds contains NaN"
    assert df['y'].notna().all(), "y contains NaN"

    # Check sorting
    df_sorted = df.sort_values(['unique_id', 'ds']).reset_index(drop=True)
    assert df.equals(df_sorted), "Data not sorted by unique_id, ds"

    # Check for duplicates
    duplicates = df.duplicated(subset=['unique_id', 'ds']).sum()
    assert duplicates == 0, f"Found {{duplicates}} duplicate (unique_id, ds) pairs"

    print("✓ All validation checks passed")
    return True


# Run validation
if __name__ == "__main__":
    df = pd.read_csv("{output_file}")
    validate_nixtla_schema(df)
```

## Usage Examples

### Basic Forecasting with StatsForecast

```python
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA, AutoETS, SeasonalNaive
from {transform_import} import to_nixtla_schema

# Transform data
df = to_nixtla_schema("{source_path}")

# Initialize forecasting models
sf = StatsForecast(
    models=[
        AutoARIMA(season_length={season_length}),
        AutoETS(season_length={season_length}),
        SeasonalNaive(season_length={season_length})
    ],
    freq='{frequency_code}'
)

# Generate forecasts
forecasts = sf.forecast(df=df, h={forecast_horizon})
print(forecasts.head())
```

### TimeGPT API Forecasting

```python
from nixtla import NixtlaClient
from {transform_import} import to_nixtla_schema

# Transform data
df = to_nixtla_schema("{source_path}")

# Initialize TimeGPT client
client = NixtlaClient(api_key='your-api-key-here')

# Generate forecasts
forecasts = client.forecast(
    df=df,
    h={forecast_horizon},
    freq='{frequency_code}',
    level=[80, 95]  # Prediction intervals
)

print(forecasts.head())
```

### Cross-Validation

```python
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA
from {transform_import} import to_nixtla_schema

# Transform data
df = to_nixtla_schema("{source_path}")

# Initialize model
sf = StatsForecast(
    models=[AutoARIMA(season_length={season_length})],
    freq='{frequency_code}'
)

# Run cross-validation
cv_results = sf.cross_validation(
    df=df,
    h={forecast_horizon},
    step_size={cv_step_size},
    n_windows={cv_windows}
)

# Calculate metrics
from statsforecast.utils import evaluate

metrics = evaluate(cv_results)
print(metrics)
```

## Known Issues & Assumptions

**Assumptions**:
- All series have consistent temporal frequency
- Missing dates represent actual data gaps (not system errors)
{additional_assumptions}

**Known data quality issues**:
{known_issues}

**Handling missing values**:
- Target variable (`y`): Rows with missing `y` are dropped
- Timestamps (`ds`): Rows with unparseable dates are dropped
- Exogenous variables: Missing values preserved (model-dependent handling)

## Troubleshooting

### Error: "Missing required columns"

**Cause**: Source data doesn't contain expected columns.

**Solution**:
1. Verify source file column names
2. Update transformation parameters in `to_nixtla_schema()` call
3. Check for typos in column specifications

### Error: "y contains NaN after cleanup"

**Cause**: All target values are null or failed numeric conversion.

**Solution**:
1. Inspect source data for data type issues
2. Check for string values in numeric column
3. Add data cleaning step before transformation

### Warning: "Duplicate (unique_id, ds) pairs found"

**Cause**: Multiple records exist for same series at same timestamp.

**Solution**:
1. Investigate data source for duplicate records
2. Aggregate duplicates (sum, mean, etc.) before transformation
3. Add explicit deduplication logic in transformation

### Error: "Failed to parse date column"

**Cause**: Date format not recognized by pandas.

**Solution**:
1. Specify explicit format: `to_nixtla_schema(date_format="%Y-%m-%d")`
2. Check for mixed date formats in source data
3. Preprocess dates before transformation

## Maintenance

**Update frequency**: {update_frequency}
**Owner**: {owner}
**Last validated**: {generated_date}

## References

- [Nixtla Documentation](https://docs.nixtla.io/)
- [StatsForecast Input Format](https://nixtla.github.io/statsforecast/docs/getting-started/input-format.html)
- [TimeGPT API Reference](https://docs.nixtla.io/docs/api-reference)

---

*Generated by nixtla-schema-mapper skill v1.1.0*
'''


def infer_frequency(date_series: pd.Series) -> tuple:
    """
    Infer temporal frequency from date series.

    Args:
        date_series: Pandas datetime series

    Returns:
        Tuple of (frequency_description, frequency_code, season_length)
    """
    if len(date_series) < 2:
        return ("Unknown", "D", 1)

    time_deltas = date_series.diff().dt.total_seconds().median()

    if not time_deltas or pd.isna(time_deltas):
        return ("Unknown", "D", 1)

    # Convert to appropriate frequency
    if time_deltas < 3600:  # Less than 1 hour
        minutes = int(time_deltas / 60)
        return (f"{minutes}-minute", f"{minutes}min", 60 // minutes)
    elif time_deltas < 86400:  # Less than 1 day
        hours = int(time_deltas / 3600)
        return (f"{hours}-hour", f"{hours}H", 24 // hours)
    elif time_deltas < 604800:  # Less than 1 week
        days = int(time_deltas / 86400)
        return (f"{days}-day", f"{days}D", 7 // days)
    elif time_deltas < 2592000:  # Less than ~30 days
        weeks = int(time_deltas / 604800)
        return (f"{weeks}-week", f"{weeks}W", 52 // weeks)
    else:
        months = int(time_deltas / 2592000)
        return (f"{months}-month", f"{months}M", 12 // months)


def create_contract(
    mapping_file: Optional[str] = None,
    source_path: Optional[str] = None,
    id_col: Optional[str] = None,
    date_col: Optional[str] = None,
    target_col: Optional[str] = None,
    transform_module: str = "data.transform.to_nixtla_schema",
    output_path: str = "NIXTLA_SCHEMA_CONTRACT.md",
) -> str:
    """
    Generate schema contract documentation.

    Args:
        mapping_file: Optional JSON mapping file from analyze_schema.py
        source_path: Path to source data file
        id_col: Column name for unique_id
        date_col: Column name for ds
        target_col: Column name for y
        transform_module: Import path for transformation module
        output_path: Output path for contract markdown

    Returns:
        Generated contract markdown
    """
    # Load configuration
    if mapping_file:
        with open(mapping_file, "r") as f:
            mapping = json.load(f)

        source_path = mapping.get("source_path", "data/source.csv")
        id_col = mapping["mapping"].get("unique_id", "id")
        date_col = mapping["mapping"]["ds"]
        target_col = mapping["mapping"]["y"]

        id_type = mapping["column_types"].get("unique_id", "object")
        date_type = mapping["column_types"]["ds"]
        target_type = mapping["column_types"]["y"]

        series_count = mapping["statistics"].get("series_count", 0)
        date_min = mapping["statistics"]["date_range"]["min"]
        date_max = mapping["statistics"]["date_range"]["max"]
        total_obs = mapping.get("total_rows", 0)

        exog_vars = mapping.get("exogenous_variables", [])
    else:
        # Load data to infer statistics
        if not source_path or not Path(source_path).exists():
            raise ValueError(f"Source file not found: {source_path}")

        if source_path.endswith(".csv"):
            df = pd.read_csv(source_path, nrows=10000)
        elif source_path.endswith(".parquet"):
            df = pd.read_parquet(source_path)
            if len(df) > 10000:
                df = df.head(10000)
        else:
            raise ValueError(f"Unsupported file format: {source_path}")

        id_type = str(df[id_col].dtype) if id_col and id_col in df.columns else "object"
        date_type = str(df[date_col].dtype)
        target_type = str(df[target_col].dtype)

        series_count = df[id_col].nunique() if id_col and id_col in df.columns else 1
        date_series = pd.to_datetime(df[date_col])
        date_min = str(date_series.min())
        date_max = str(date_series.max())
        total_obs = len(df)

        exog_vars = []
        excluded = [id_col, date_col, target_col] if id_col else [date_col, target_col]
        for col in df.columns:
            if col not in excluded:
                exog_vars.append({"name": col, "dtype": str(df[col].dtype)})

    # Calculate statistics
    if source_path and Path(source_path).exists():
        if source_path.endswith(".csv"):
            df_sample = pd.read_csv(source_path, nrows=10000)
        else:
            df_sample = pd.read_parquet(source_path)
            if len(df_sample) > 10000:
                df_sample = df_sample.head(10000)

        date_series = pd.to_datetime(df_sample[date_col])
        freq_desc, freq_code, season_len = infer_frequency(date_series)

        if id_col and id_col in df_sample.columns:
            series_lens = df_sample.groupby(id_col).size()
            obs_avg = series_lens.mean()
            obs_min = series_lens.min()
            obs_max = series_lens.max()

            example_ids = df_sample[id_col].unique()[:3].tolist()
            example_series_ids = ", ".join(str(x) for x in example_ids)
            series_granularity = f"One series per unique {id_col}"
        else:
            obs_avg = len(df_sample)
            obs_min = len(df_sample)
            obs_max = len(df_sample)
            example_series_ids = "N/A (single series)"
            series_granularity = "Single time series"
    else:
        freq_desc = "Daily"
        freq_code = "D"
        season_len = 7
        obs_avg = total_obs / max(series_count, 1)
        obs_min = 0
        obs_max = total_obs
        example_series_ids = "N/A"
        series_granularity = "Unknown"

    # Format exogenous variables table
    if exog_vars:
        exog_rows = []
        for var in exog_vars:
            exog_rows.append(
                f"| `{var['name']}` | {var['dtype']} | [Description] | [Range/Values] |"
            )
        exogenous_table = "| Column | Type | Description | Range/Values |\n"
        exogenous_table += "|--------|------|-------------|--------------|\\n"
        exogenous_table += "\\n".join(exog_rows)
    else:
        exogenous_table = "*No exogenous variables included*"

    # Generate contract
    contract = CONTRACT_TEMPLATE.format(
        source_path=source_path,
        transform_module=transform_module,
        generated_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        overview=f"Transform {Path(source_path).name} to Nixtla-compatible schema for time series forecasting.",
        id_col=id_col or "N/A",
        date_col=date_col,
        target_col=target_col,
        id_type=id_type,
        date_type=date_type,
        target_type=target_type,
        series_count=series_count,
        series_granularity=series_granularity,
        example_series_ids=example_series_ids,
        frequency=freq_desc,
        frequency_code=freq_code,
        date_min=date_min,
        date_max=date_max,
        total_observations=total_obs,
        obs_avg=obs_avg,
        obs_min=obs_min,
        obs_max=obs_max,
        exogenous_table=exogenous_table,
        additional_filters="",
        additional_assumptions="",
        known_issues="- *None identified during analysis*",
        update_frequency="As needed (triggered by source data changes)",
        owner="Data Engineering Team",
        output_file=Path(source_path).stem + "_nixtla.csv",
        transform_import=transform_module.replace("/", ".").replace(".py", ""),
        season_length=season_len,
        forecast_horizon=season_len * 2,
        cv_step_size=season_len,
        cv_windows=3,
    )

    return contract


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate Nixtla schema contract documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate from mapping file
  python create_contract.py --mapping mapping.json --output NIXTLA_SCHEMA_CONTRACT.md

  # Generate from explicit parameters
  python create_contract.py --input data/sales.csv --id_col store_id --date_col date --target_col revenue
        """,
    )

    parser.add_argument("--mapping", help="Path to JSON mapping file from analyze_schema.py")
    parser.add_argument("--input", help="Path to input CSV or Parquet file")
    parser.add_argument("--id_col", help="Column name for series identifier")
    parser.add_argument("--date_col", help="Column name for timestamp")
    parser.add_argument("--target_col", help="Column name for target variable")
    parser.add_argument(
        "--transform_module",
        default="data.transform.to_nixtla_schema",
        help="Import path for transformation module",
    )
    parser.add_argument(
        "--output",
        default="NIXTLA_SCHEMA_CONTRACT.md",
        help="Output path for contract markdown (default: NIXTLA_SCHEMA_CONTRACT.md)",
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.mapping and not (args.input and args.date_col and args.target_col):
        print(
            "Error: Must provide either --mapping or (--input --date_col --target_col)",
            file=sys.stderr,
        )
        parser.print_help()
        sys.exit(1)

    try:
        # Security: Sanitize all file paths
        mapping_path = None
        input_path = None

        if args.mapping:
            try:
                mapping_path = str(sanitize_path(args.mapping, purpose="mapping"))
            except ValueError as e:
                print(f"Security Error: {e}", file=sys.stderr)
                sys.exit(1)

        if args.input:
            try:
                input_path = str(sanitize_path(args.input, purpose="input"))
            except ValueError as e:
                print(f"Security Error: {e}", file=sys.stderr)
                sys.exit(1)

        try:
            output_file = sanitize_path(args.output, purpose="output")
        except ValueError as e:
            print(f"Security Error: {e}", file=sys.stderr)
            sys.exit(1)

        # Generate contract
        contract = create_contract(
            mapping_file=mapping_path,
            source_path=input_path,
            id_col=args.id_col,
            date_col=args.date_col,
            target_col=args.target_col,
            transform_module=args.transform_module,
            output_path=str(output_file),
        )

        # Write to file
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w") as f:
            f.write(contract)

        print(f"✓ Schema contract generated: {output_file}")
        print(f"\nContract includes:")
        print("  - Schema mapping table")
        print("  - Data quality rules")
        print("  - Validation script")
        print("  - Usage examples")
        print("  - Troubleshooting guide")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
