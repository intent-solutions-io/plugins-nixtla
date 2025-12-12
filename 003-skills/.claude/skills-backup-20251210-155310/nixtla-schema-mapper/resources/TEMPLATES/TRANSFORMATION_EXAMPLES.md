# Schema Transformation Examples

Complete code examples for transforming data to Nixtla schema format.

## Python Transform Module

Create `data/transform/to_nixtla_schema.py`:

```python
"""
Nixtla Schema Transformation
Source: data/sales.csv
Target: Nixtla schema (unique_id, ds, y + exogenous)
"""

import pandas as pd
from typing import List, Optional

def to_nixtla_schema(
    source_path: str = "data/sales.csv",
    unique_id_col: str = "store_id",
    ds_col: str = "date",
    y_col: str = "sales",
    exog_cols: Optional[List[str]] = None
) -> pd.DataFrame:
    """Transform source data to Nixtla-compatible schema.

    Args:
        source_path: Path to CSV or Parquet file
        unique_id_col: Column name for series identifier
        ds_col: Column name for timestamp
        y_col: Column name for target variable
        exog_cols: Optional list of exogenous variable columns

    Returns:
        DataFrame with Nixtla schema (unique_id, ds, y, [exogenous])
    """

    # Load data
    if source_path.endswith('.csv'):
        df = pd.read_csv(source_path)
    elif source_path.endswith('.parquet'):
        df = pd.read_parquet(source_path)
    else:
        raise ValueError(f"Unsupported format: {source_path}")

    # Validate required columns exist
    required = [unique_id_col, ds_col, y_col]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    # Apply transformations
    df_nixtla = df.copy()
    df_nixtla['unique_id'] = df[unique_id_col].astype(str)
    df_nixtla['ds'] = pd.to_datetime(df[ds_col])
    df_nixtla['y'] = pd.to_numeric(df[y_col], errors='coerce')

    # Include exogenous variables
    if exog_cols is None:
        exog_cols = ['price', 'promotion', 'day_of_week', 'holiday']

    final_cols = ['unique_id', 'ds', 'y'] + [
        col for col in exog_cols if col in df.columns
    ]
    df_nixtla = df_nixtla[final_cols]

    # Data quality cleanup
    df_nixtla = df_nixtla.dropna(subset=['y'])
    df_nixtla = df_nixtla.sort_values(['unique_id', 'ds']).reset_index(drop=True)

    # Validation
    assert df_nixtla['unique_id'].notna().all(), "unique_id contains NaN"
    assert df_nixtla['ds'].notna().all(), "ds contains NaN"
    assert df_nixtla['y'].notna().all(), "y contains NaN after cleanup"

    return df_nixtla

# Test/validation script
if __name__ == "__main__":
    df = to_nixtla_schema("data/sales.csv")

    print(f"✓ Transformed {len(df)} rows")
    print(f"✓ Series count: {df['unique_id'].nunique()}")
    print(f"✓ Date range: {df['ds'].min()} to {df['ds'].max()}")
    print(f"✓ Columns: {list(df.columns)}")
    print(f"\nFirst 5 rows:\n{df.head()}")
    print(f"\nData types:\n{df.dtypes}")
```

## dbt SQL Model

Create `dbt/models/nixtla_schema.sql`:

```sql
{{ config(
    materialized='table',
    tags=['nixtla', 'forecasting'],
    post_hook=[
        "CREATE INDEX IF NOT EXISTS idx_nixtla_unique_id ON {{ this }} (unique_id)",
        "CREATE INDEX IF NOT EXISTS idx_nixtla_ds ON {{ this }} (ds)"
    ]
) }}

/*
  Nixtla Schema Transformation
  Source: fct_sales (dbt model)
  Target: Nixtla schema (unique_id, ds, y + exogenous)
*/

WITH source_data AS (
  SELECT * FROM {{ ref('fct_sales') }}
  WHERE sales IS NOT NULL  -- Filter nulls early
),

nixtla_schema AS (
  SELECT
    -- Required Nixtla columns
    CAST(store_id AS VARCHAR) AS unique_id,
    CAST(date AS TIMESTAMP) AS ds,
    CAST(sales AS DOUBLE PRECISION) AS y,

    -- Exogenous variables (optional)
    CAST(price AS DOUBLE PRECISION) AS price,
    CAST(promotion AS INTEGER) AS promotion,
    CAST(day_of_week AS INTEGER) AS day_of_week,
    CAST(holiday AS INTEGER) AS holiday

  FROM source_data
),

-- Data quality checks
validated_data AS (
  SELECT *
  FROM nixtla_schema
  WHERE unique_id IS NOT NULL
    AND ds IS NOT NULL
    AND y IS NOT NULL
    AND y >= 0  -- Business rule: sales cannot be negative
)

SELECT *
FROM validated_data
ORDER BY unique_id, ds
```

## BigQuery SQL

For BigQuery data warehouse:

```sql
-- nixtla_schema.sql
CREATE OR REPLACE TABLE `project.dataset.nixtla_schema` AS

WITH source_data AS (
  SELECT * FROM `project.dataset.fct_sales`
  WHERE sales IS NOT NULL
),

nixtla_schema AS (
  SELECT
    CAST(store_id AS STRING) AS unique_id,
    CAST(date AS TIMESTAMP) AS ds,
    CAST(sales AS FLOAT64) AS y,
    CAST(price AS FLOAT64) AS price,
    CAST(promotion AS INT64) AS promotion,
    EXTRACT(DAYOFWEEK FROM date) AS day_of_week,
    CAST(holiday AS INT64) AS holiday
  FROM source_data
)

SELECT *
FROM nixtla_schema
WHERE unique_id IS NOT NULL
  AND ds IS NOT NULL
  AND y IS NOT NULL
ORDER BY unique_id, ds;
```

## Spark/PySpark

For big data processing:

```python
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, to_timestamp, lit
from pyspark.sql.types import StringType, TimestampType, DoubleType

def to_nixtla_schema_spark(
    df: DataFrame,
    unique_id_col: str = "store_id",
    ds_col: str = "date",
    y_col: str = "sales",
    exog_cols: list = None
) -> DataFrame:
    """Transform Spark DataFrame to Nixtla schema."""

    if exog_cols is None:
        exog_cols = ['price', 'promotion', 'day_of_week', 'holiday']

    # Apply transformations
    df_nixtla = (
        df
        .withColumn('unique_id', col(unique_id_col).cast(StringType()))
        .withColumn('ds', to_timestamp(col(ds_col)))
        .withColumn('y', col(y_col).cast(DoubleType()))
        .select(['unique_id', 'ds', 'y'] + exog_cols)
        .filter(col('y').isNotNull())
        .orderBy('unique_id', 'ds')
    )

    return df_nixtla

# Example usage
spark = SparkSession.builder.appName("NixtlaTransform").getOrCreate()
df_raw = spark.read.csv("data/sales.csv", header=True, inferSchema=True)
df_nixtla = to_nixtla_schema_spark(df_raw)
df_nixtla.write.parquet("data/nixtla_schema.parquet", mode="overwrite")
```

## Polars (High-Performance)

For faster DataFrame operations:

```python
import polars as pl
from datetime import datetime

def to_nixtla_schema_polars(
    source_path: str,
    unique_id_col: str = "store_id",
    ds_col: str = "date",
    y_col: str = "sales"
) -> pl.DataFrame:
    """Transform data to Nixtla schema using Polars."""

    # Load data (Polars is ~10x faster than pandas)
    df = pl.read_csv(source_path) if source_path.endswith('.csv') else pl.read_parquet(source_path)

    # Transform
    df_nixtla = (
        df
        .select([
            pl.col(unique_id_col).cast(pl.Utf8).alias('unique_id'),
            pl.col(ds_col).str.strptime(pl.Datetime, "%Y-%m-%d").alias('ds'),
            pl.col(y_col).cast(pl.Float64).alias('y'),
            pl.col('price'), pl.col('promotion'),
            pl.col('day_of_week'), pl.col('holiday')
        ])
        .filter(pl.col('y').is_not_null())
        .sort(['unique_id', 'ds'])
    )

    return df_nixtla
```

## Usage Patterns

### Pattern 1: Simple CSV Transform

```python
from data.transform.to_nixtla_schema import to_nixtla_schema

# Transform and save
df = to_nixtla_schema("data/sales.csv")
df.to_csv("data/sales_nixtla.csv", index=False)
```

### Pattern 2: Custom Column Mapping

```python
df = to_nixtla_schema(
    source_path="data/custom_data.csv",
    unique_id_col="product_sku",
    ds_col="transaction_date",
    y_col="revenue",
    exog_cols=['temperature', 'competitor_price']
)
```

### Pattern 3: Pipeline Integration

```python
# In your forecasting pipeline
from data.transform.to_nixtla_schema import to_nixtla_schema
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA

# Step 1: Transform
df = to_nixtla_schema("data/raw_sales.csv")

# Step 2: Forecast
sf = StatsForecast(models=[AutoARIMA()], freq='D')
sf.fit(df)
forecasts = sf.forecast(h=30)
```
