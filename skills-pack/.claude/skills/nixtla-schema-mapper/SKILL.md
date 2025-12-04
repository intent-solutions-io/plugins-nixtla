---
name: nixtla-schema-mapper
description: "Analyzes data sources and generates Nixtla-compatible schema transformations. Infers column mappings, creates transformation modules for CSV/SQL/Parquet/dbt sources, generates schema contracts, and validates data quality. Use when user needs data transformation, schema mapping, column inference, or Nixtla format conversion. Trigger with 'map data to Nixtla schema', 'transform CSV for forecasting', 'convert to Nixtla format', 'infer schema'."
---

# Nixtla Schema Mapper

This skill **analyzes user data sources** and **generates transformation code** to convert them into Nixtla-compatible schema (`unique_id`, `ds`, `y`). It creates both the transformation logic and comprehensive documentation.

## When This Skill Activates

**Trigger phrases**:
- "Map my data to Nixtla schema"
- "Transform this CSV for forecasting"
- "Convert my data to Nixtla format"
- "Infer my time series schema"
- "Prepare data for TimeGPT"

**File patterns**:
- User has data file but doesn't match Nixtla schema
- Mentions column mapping or data transformation
- Asks about unique_id, ds, y columns

## What This Skill Does

1. **Samples and analyzes data** (first 100 rows)
2. **Infers schema mapping** (unique_id, ds, y, exogenous variables)
3. **Generates transformation artifact**:
   - Python module (`data/transform/to_nixtla_schema.py`), OR
   - dbt SQL model (`dbt/models/nixtla_schema.sql`)
4. **Creates schema contract** (`NIXTLA_SCHEMA_CONTRACT.md`)
5. **Provides usage instructions** (one-liner to call transform)

---

## Skill Behavior

### Step 1: Gather Data Source

Ask user for data source if not obvious:

```
I'll help map your data to Nixtla schema. Where is your data?

Options:
1. CSV file (e.g., data/sales.csv)
2. Parquet file (e.g., data/sales.parquet)
3. SQL table (e.g., "public.sales" or full SELECT query)
4. dbt model (e.g., {{ ref('fct_sales') }})
5. Already loaded in DataFrame (provide variable name)

Please specify:
```

**If user provides path/query**, proceed to sampling.

**If user says "it's already loaded"**, ask for variable name and inspect directly.

### Step 2: Sample and Analyze Data

Load or read first ~100 rows to infer schema:

```python
# For CSV
import pandas as pd
df_sample = pd.read_csv(source, nrows=100)

# For Parquet
df_sample = pd.read_parquet(source).head(100)
```

**Analyze columns**:
- **Timestamp candidates**: datetime types or names: `date`, `timestamp`, `ds`, `time`, `datetime`, `created_at`
- **Target candidates**: numeric types with names: `sales`, `revenue`, `demand`, `y`, `value`, `target`, `metric`
- **Series ID candidates**: categorical types with names: `id`, `store`, `product`, `unique_id`, `series`
- **Exogenous variables**: Remaining numeric or categorical columns

**Print analysis summary**:
```
📊 Data Analysis (first 100 rows):

Columns found: 15
Rows sampled: 100

Detected schema:
  ✓ Timestamp column: 'date' (datetime64[ns])
  ✓ Target column: 'sales' (float64)
  ✓ Series ID: 'store_id' (object, 5 unique values)

Potential exogenous variables:
  - 'price' (float64)
  - 'promotion' (int64, binary 0/1)
  - 'day_of_week' (int64)
  - 'holiday' (bool)
```

### Step 3: Propose Mapping

Based on analysis, propose Nixtla schema mapping:

```
Proposed mapping to Nixtla schema:

unique_id ← 'store_id' (identifies 5 different series)
ds        ← 'date' (timestamp, daily frequency detected)
y         ← 'sales' (target variable)

Exogenous variables (optional, will be included):
- 'price'
- 'promotion'
- 'day_of_week'
- 'holiday'

Does this mapping look correct? (yes/no/adjust)
```

**If user confirms**, proceed to generating transformation code.

**If user says "adjust"**, ask which columns to change.

**If ambiguous** (e.g., multiple timestamp columns), ask user to clarify.

### Step 4: Generate Transformation Artifact

Based on data source type, generate appropriate transformation:

#### Option A: Python Transform Module

For CSV/Parquet sources, create `data/transform/to_nixtla_schema.py`:

```python
"""
Nixtla Schema Transformation
Source: data/sales.csv
Target: Nixtla schema (unique_id, ds, y + exogenous)
"""

import pandas as pd

def to_nixtla_schema(source_path: str = "data/sales.csv") -> pd.DataFrame:
    """Transform source data to Nixtla-compatible schema."""

    # Load data
    if source_path.endswith('.csv'):
        df = pd.read_csv(source_path)
    elif source_path.endswith('.parquet'):
        df = pd.read_parquet(source_path)
    else:
        raise ValueError(f"Unsupported format: {source_path}")

    # Apply transformations
    df_nixtla = df.copy()
    df_nixtla['unique_id'] = df['store_id'].astype(str)
    df_nixtla['ds'] = pd.to_datetime(df['date'])
    df_nixtla['y'] = pd.to_numeric(df['sales'], errors='coerce')

    # Include exogenous variables
    exog_vars = ['price', 'promotion', 'day_of_week', 'holiday']
    final_cols = ['unique_id', 'ds', 'y'] + exog_vars
    df_nixtla = df_nixtla[final_cols]

    # Data quality
    df_nixtla = df_nixtla.dropna(subset=['y'])
    df_nixtla = df_nixtla.sort_values(['unique_id', 'ds']).reset_index(drop=True)

    return df_nixtla

# Test
if __name__ == "__main__":
    df = to_nixtla_schema("data/sales.csv")
    print(f"✓ Transformed {len(df)} rows, {df['unique_id'].nunique()} series")
    print(df.head())
```

**Note**: See **resources/TEMPLATES/to_nixtla_schema_template.py** for complete implementation with error handling and validation.

#### Option B: dbt SQL Model

For SQL/dbt sources, create `dbt/models/nixtla_schema.sql`:

```sql
{{ config(materialized='table', tags=['nixtla', 'forecasting']) }}

WITH source_data AS (
  SELECT * FROM {{ ref('fct_sales') }}
),

nixtla_schema AS (
  SELECT
    CAST(store_id AS VARCHAR) AS unique_id,
    CAST(date AS TIMESTAMP) AS ds,
    CAST(sales AS DOUBLE PRECISION) AS y,
    price, promotion, day_of_week,
    CAST(holiday AS INTEGER) AS holiday
  FROM source_data
  WHERE sales IS NOT NULL
)

SELECT * FROM nixtla_schema
ORDER BY unique_id, ds
```

**Note**: See **resources/TEMPLATES/nixtla_schema_dbt.sql** for complete dbt model template.

### Step 5: Create Schema Contract

Generate `NIXTLA_SCHEMA_CONTRACT.md`:

```markdown
# Nixtla Schema Contract

**Source**: data/sales.csv
**Transformation**: data/transform/to_nixtla_schema.py

## Schema Mapping

| Nixtla Column | Source Column | Type | Description |
|---------------|---------------|------|-------------|
| unique_id | store_id | string | Series identifier (5 stores) |
| ds | date | datetime | Timestamp (daily frequency) |
| y | sales | float | Target: daily sales volume |

## Exogenous Variables

| Column | Type | Description |
|--------|------|-------------|
| price | float | Product price |
| promotion | int | Promotional indicator (0/1) |
| day_of_week | int | Day of week (0-6) |
| holiday | bool | Holiday indicator |

## Usage

```python
from data.transform.to_nixtla_schema import to_nixtla_schema
df = to_nixtla_schema("data/sales.csv")

# Use with StatsForecast
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA
sf = StatsForecast(models=[AutoARIMA()], freq='D')
sf.fit(df)
forecasts = sf.forecast(h=30)
```

[Full contract template in resources/TEMPLATES/NIXTLA_SCHEMA_CONTRACT_TEMPLATE.md]
```

**Note**: See **resources/TEMPLATES/NIXTLA_SCHEMA_CONTRACT_TEMPLATE.md** for complete contract template with troubleshooting and validation scripts.

### Step 6: Provide Usage Summary

After generating files, print clear instructions:

```
✅ Nixtla schema transformation created!

Generated files:
  🐍 data/transform/to_nixtla_schema.py (transformation module)
  📄 NIXTLA_SCHEMA_CONTRACT.md (schema documentation)

Schema mapping:
  unique_id ← store_id
  ds        ← date
  y         ← sales

Next steps:

1. Test transformation:
   python data/transform/to_nixtla_schema.py

2. Use in forecasting code:
   from data.transform.to_nixtla_schema import to_nixtla_schema
   df = to_nixtla_schema("data/sales.csv")

3. Validate schema:
   See validation script in NIXTLA_SCHEMA_CONTRACT.md

4. Integrate with experiments:
   Update forecasting/config.yml to use transformed data
```

---

## Advanced Features

For advanced patterns, see:
- **resources/ADVANCED_FEATURES.md** - Multi-source mapping, type casting, frequency detection
- **resources/SCENARIOS.md** - Real-world examples (single series, multiple IDs, hierarchical data)
- **resources/TROUBLESHOOTING.md** - Common issues and solutions

Full code templates:
- **resources/TEMPLATES/to_nixtla_schema_template.py** - Complete Python transformation module
- **resources/TEMPLATES/nixtla_schema_dbt.sql** - Complete dbt SQL model
- **resources/TEMPLATES/NIXTLA_SCHEMA_CONTRACT_TEMPLATE.md** - Complete schema contract template

---

## Summary

This skill **maps raw data to Nixtla schema** by:

1. **Sampling and analyzing** user data
2. **Inferring column mappings** (unique_id, ds, y)
3. **Generating transformation code** (Python or SQL)
4. **Documenting schema contract** (assumptions, validation, usage)
5. **Providing clear usage instructions**

**Key outputs**:
- `data/transform/to_nixtla_schema.py` OR `dbt/models/nixtla_schema.sql`
- `NIXTLA_SCHEMA_CONTRACT.md`

**Installed location**: `.claude/skills/nixtla-schema-mapper/`
**Works with**: nixtla-timegpt-lab (mode skill), nixtla-experiment-architect (experiment setup)
