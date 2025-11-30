# Plugin #5: Nixtla dbt Package
**Technical Architecture & Implementation Specification**

**Created**: 2025-11-30
**Status**: Design Phase
**Priority**: Tier 2 (INTEGRATION WIN)
**Addresses**: Integration Tax (Friction #4)

---

## Executive Summary

### What It Is
A native dbt package that treats forecasting as a data transformation step, allowing SQL analysts to generate Nixtla forecasts using `{{ nixtla_forecast(...) }}` macros directly in dbt models.

### Why It Exists
Nixtla's CRO identifies friction:
> "There isn't a widely touted, one-click dbt package that abstracts API calls. Users wire pieces together manually."

**This plugin brings TimeGPT forecasting into the dbt transformation layer.**

### Who It's For
- **Analytics engineers** using dbt for transformations
- **SQL analysts** without Python skills
- **Data teams** standardizing on dbt-centric workflows
- **BI teams** needing forecasts in dashboards

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  DBT MODEL (SQL + Jinja)                                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  {{                                                   │  │
│  │    config(materialized='incremental')                │  │
│  │  }}                                                   │  │
│  │                                                       │  │
│  │  {{ nixtla_forecast(                                 │  │
│  │      source_ref=ref('staging_sales'),               │  │
│  │      timestamp_col='date',                           │  │
│  │      value_col='revenue',                            │  │
│  │      horizon=90                                      │  │
│  │  ) }}                                                 │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  DBT PACKAGE: dbt_nixtla                                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  macros/                                              │  │
│  │  ├─ nixtla_forecast.sql        (core macro)         │  │
│  │  ├─ nixtla_anomaly.sql         (anomaly detection)  │  │
│  │  └─ nixtla_cross_validate.sql  (backtesting)        │  │
│  │                                                       │  │
│  │  models/                                             │  │
│  │  └─ staging/                   (helpers)            │  │
│  │                                                       │  │
│  │  python/                                             │  │
│  │  └─ nixtla_runner.py           (Python UDF)         │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  EXECUTION                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐   │
│  │  dbt run    │  │  Python UDF │  │  Nixtla API      │   │
│  │  (compile)  │→ │  (execute)  │→ │  (forecast)      │   │
│  └─────────────┘  └─────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Plugin Type
**dbt Package** (SQL Jinja macros + Python UDFs)

### Components

1. **dbt Macros** (3)
   - `nixtla_forecast()` - Generate forecasts
   - `nixtla_anomaly()` - Detect anomalies
   - `nixtla_cross_validate()` - Backtest models

2. **Python UDFs** (1)
   - `nixtla_runner.py` - Execute API calls from SQL

3. **Helper Models** (2)
   - `staging/prepare_timeseries.sql` - Format data for Nixtla
   - `utils/nixtla_config.sql` - Centralized configuration

---

## API Keys & User Requirements

### Required
```yaml
# dbt_project.yml
vars:
  nixtla_api_key: "{{ env_var('NIXTLA_API_KEY') }}"
```

### User Requirements

#### Minimum
- dbt Core 1.5.0+ or dbt Cloud
- Python 3.10+ (for UDFs)
- Data warehouse supporting Python UDFs (Snowflake, BigQuery, Databricks)

#### Recommended
- dbt Cloud for scheduling
- Version control (Git) for dbt project
- Separate dev/prod environments

---

## Installation Process

### Installation via dbt packages.yml

```yaml
# packages.yml
packages:
  - git: "https://github.com/nixtla/dbt-nixtla"
    revision: v1.0.0
```

```bash
# Install dependencies
dbt deps

# Configure API key
export NIXTLA_API_KEY=nixak-...

# Run models
dbt run --select tag:nixtla
```

---

## Code Implementation

### Directory Structure

```
dbt-nixtla/
├── dbt_project.yml
├── README.md
├── LICENSE
├── macros/
│   ├── nixtla_forecast.sql           # Core forecasting macro
│   ├── nixtla_anomaly.sql            # Anomaly detection
│   ├── nixtla_cross_validate.sql     # Backtesting
│   └── utils/
│       ├── get_api_key.sql
│       └── format_timeseries.sql
├── models/
│   ├── staging/
│   │   └── prepare_timeseries.sql
│   └── examples/
│       ├── sales_forecast.sql
│       └── anomaly_detection.sql
├── python/
│   └── nixtla_runner.py              # Python UDF
├── tests/
│   └── forecast_schema_test.sql
└── integration_tests/
    └── test_forecast_output.sql
```

### Core Macro: nixtla_forecast.sql

```sql
{#
Nixtla Forecast Macro for dbt

Usage:
  {{ nixtla_forecast(
      source_ref=ref('staging_sales'),
      timestamp_col='date',
      value_col='revenue',
      group_by='product_id',
      horizon=30
  ) }}
#}

{% macro nixtla_forecast(
    source_ref,
    timestamp_col,
    value_col,
    group_by=none,
    horizon=30,
    freq='D',
    models=['TimeGPT'],
    level=[80, 90, 95]
) %}

  {%- set api_key = var('nixtla_api_key', env_var('NIXTLA_API_KEY', '')) -%}

  {%- if api_key == '' -%}
    {{ exceptions.raise_compiler_error("NIXTLA_API_KEY not configured") }}
  {%- endif -%}

  {# Prepare input data in Nixtla format (unique_id, ds, y) #}
  WITH prepared_data AS (
    SELECT
      {% if group_by %}
        {{ group_by }} AS unique_id,
      {% else %}
        'series_1' AS unique_id,
      {% endif %}
      {{ timestamp_col }} AS ds,
      {{ value_col }} AS y
    FROM {{ source_ref }}
    WHERE {{ value_col }} IS NOT NULL
      AND {{ timestamp_col }} IS NOT NULL
  )

  {# Call Python UDF to execute Nixtla API #}
  {% if target.type == 'snowflake' %}
    {# Snowflake Python UDF #}
    , forecast_results AS (
      SELECT
        unique_id,
        ds,
        y,
        nixtla_forecast_udf(
          unique_id,
          ds,
          y,
          {{ horizon }},
          '{{ freq }}',
          '{{ api_key }}'
        ) AS forecast_value
      FROM prepared_data
    )

  {% elif target.type == 'bigquery' %}
    {# BigQuery Remote Function #}
    , forecast_results AS (
      SELECT
        unique_id,
        ds,
        `{{ target.project }}.{{ target.dataset }}.nixtla_forecast`(
          ARRAY_AGG(STRUCT(unique_id, ds, y)),
          {{ horizon }},
          '{{ freq }}'
        ) AS forecast_value
      FROM prepared_data
      GROUP BY unique_id
    )

  {% else %}
    {{ exceptions.raise_compiler_error("Unsupported warehouse: " ~ target.type) }}
  {% endif %}

  SELECT * FROM forecast_results

{% endmacro %}
```

### Python UDF: nixtla_runner.py

```python
"""
Python UDF for Snowflake/BigQuery to call Nixtla API from SQL
"""
from nixtla import NixtlaClient
import pandas as pd


def nixtla_forecast_udf(
    unique_ids: list,
    dates: list,
    values: list,
    horizon: int,
    freq: str,
    api_key: str
) -> list:
    """
    Snowflake Python UDF to forecast with Nixtla

    Returns list of forecast values
    """
    # Create DataFrame in Nixtla format
    df = pd.DataFrame({
        'unique_id': unique_ids,
        'ds': pd.to_datetime(dates),
        'y': values
    })

    # Initialize client
    client = NixtlaClient(api_key=api_key)

    # Run forecast
    forecasts = client.forecast(
        df=df,
        h=horizon,
        freq=freq
    )

    # Return forecast values as list
    return forecasts['TimeGPT'].tolist()
```

---

## Example dbt Model

```sql
-- models/forecasts/sales_forecast.sql
{{
  config(
    materialized='incremental',
    unique_key='unique_id',
    tags=['nixtla', 'forecasting', 'daily']
  )
}}

-- Generate 90-day sales forecast by product
{{ nixtla_forecast(
    source_ref=ref('staging_sales_history'),
    timestamp_col='sale_date',
    value_col='revenue_usd',
    group_by='product_id',
    horizon=90,
    freq='D',
    models=['TimeGPT'],
    level=[80, 90, 95]
) }}
```

---

## User Journey

### Journey 1: SQL Analyst Adds Forecasting

**Persona**: Maria, Analytics Engineer
**Goal**: Add sales forecasting to daily dbt runs
**Context**: Only knows SQL, no Python experience

**Before**:
```
Maria: "I need forecasts but can't write Python"
Team: "Ask the data science team, they're backlogged 3 months"
```

**After (with dbt_nixtla)**:

1. **Install Package**
   ```yaml
   # packages.yml
   packages:
     - git: "https://github.com/nixtla/dbt-nixtla"
       revision: v1.0.0
   ```

   ```bash
   dbt deps
   ```

2. **Create Forecast Model**
   ```sql
   -- models/forecasts/daily_sales.sql
   {{ nixtla_forecast(
       source_ref=ref('staging_sales'),
       timestamp_col='date',
       value_col='revenue',
       group_by='region',
       horizon=30
   ) }}
   ```

3. **Run dbt**
   ```bash
   export NIXTLA_API_KEY=nixak-...
   dbt run --select daily_sales
   ```

4. **Results in Data Warehouse**
   ```sql
   -- Forecasts now available in warehouse
   SELECT * FROM analytics.daily_sales
   WHERE forecast_date > CURRENT_DATE

   -- Use in dashboards
   SELECT
     region,
     forecast_date,
     forecast_value,
     lower_bound_80,
     upper_bound_80
   FROM analytics.daily_sales
   ```

**Outcome**: Maria adds forecasting in 10 minutes using only SQL, no data science team needed.

---

## Dependencies

```txt
# requirements.txt (for Python UDFs)
nixtla>=0.7.1
pandas>=2.0.0
```

```yaml
# dbt_project.yml
require-dbt-version: [">=1.5.0", "<2.0.0"]

config-version: 2

vars:
  nixtla_api_key: "{{ env_var('NIXTLA_API_KEY') }}"
  nixtla_default_horizon: 30
  nixtla_default_freq: 'D'
```

---

**Document Version**: 1.0.0
**Last Updated**: 2025-11-30
**Language**: SQL (Jinja macros) + Python (UDFs)
