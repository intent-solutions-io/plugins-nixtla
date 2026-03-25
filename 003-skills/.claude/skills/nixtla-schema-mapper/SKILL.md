---
name: nixtla-schema-mapper
description: "Transform data sources to Nixtla schema (unique_id, ds, y) with column inference. Use when preparing data for forecasting. Trigger with 'map to Nixtla schema' or 'transform data'."
allowed-tools: "Read,Write,Glob,Grep,Edit"
version: "1.1.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
compatible-with: claude-code
tags: [nixtla, time-series, data-transformation, schema, etl]
---

# Nixtla Schema Mapper

Transform data sources to Nixtla-compatible schema (`unique_id`, `ds`, `y`).

## Overview

This skill automates data transformation for Nixtla forecasting workflows:

- **Column inference**: Detects timestamp, target, and ID columns from data types and naming conventions
- **Code generation**: Produces reusable Python modules for CSV, SQL, Parquet, and dbt sources
- **Schema contracts**: Generates documentation with validation rules to enforce data quality
- **Quality checks**: Validates transformed data for missing values, type mismatches, and frequency gaps

## Prerequisites

**Required**: Python 3.8+, `pandas`

**Optional**: `pyarrow` (Parquet), `sqlalchemy` (SQL), `dbt-core` (dbt models)

```bash
pip install pandas pyarrow sqlalchemy
```

## Instructions

### Step 1: Identify Data Source

Determine the input format and location. Supported formats include CSV files, Parquet files, SQL tables or queries, and dbt models.

### Step 2: Analyze Schema

Run the schema analyzer to detect column types and recommend mappings:
```bash
python {baseDir}/scripts/analyze_schema.py --input data/sales.csv
```

**Output**:
```
Detected columns:
  Timestamp: 'date' (datetime64)
  Target: 'sales' (float64)
  Series ID: 'store_id' (object)
  Exogenous: price, promotion
```

### Step 3: Generate Transformation

```bash
python {baseDir}/scripts/generate_transform.py \
    --input data/sales.csv \
    --id_col store_id \
    --date_col date \
    --target_col sales \
    --output data/transform/to_nixtla_schema.py
```

### Step 4: Create Schema Contract

Generate a markdown contract documenting mapping rules and validation criteria:
```bash
python {baseDir}/scripts/create_contract.py \
    --mapping mapping.json \
    --output NIXTLA_SCHEMA_CONTRACT.md
```

### Step 5: Validate Transformation

Execute the generated module and verify output conforms to Nixtla schema:
```bash
python data/transform/to_nixtla_schema.py
```

## Output

- **data/transform/to_nixtla_schema.py**: Transformation module with column renaming and type casting
- **NIXTLA_SCHEMA_CONTRACT.md**: Schema documentation with validation rules
- **nixtla_data.csv**: Transformed data in Nixtla format (optional)

## Error Handling

1. **Error**: `No timestamp column detected` -- Specify manually with `--date_col`
2. **Error**: `Multiple target candidates` -- Specify manually with `--target_col`
3. **Error**: `Date parsing failed` -- Specify format with `--date_format "%Y-%m-%d"`
4. **Error**: `Non-numeric target column` -- Use `pd.to_numeric(errors='coerce')`

## Examples

See [examples](references/examples.md) for detailed usage scenarios.

## Resources

- Scripts: `{baseDir}/scripts/`
- Templates: `{baseDir}/assets/templates/`
- Nixtla Schema Docs: https://nixtla.github.io/statsforecast/

**Related Skills**:
- `nixtla-timegpt-lab`: Use transformed data for forecasting
- `nixtla-experiment-architect`: Reference in experiments
