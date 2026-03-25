---
name: nixtla-contract-schema-mapper
description: "Transform prediction market data to Nixtla format (unique_id, ds, y). Use when preparing datasets for forecasting. Trigger with 'convert to Nixtla format' or 'schema mapping'."
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
compatible-with: claude-code
tags: [nixtla, time-series, forecasting, data-transformation, schema-mapping]
allowed-tools: "Read,Write,Bash(python:*),Glob,Grep"
---

# Nixtla Contract Schema Mapper

Transforms prediction market data into Nixtla-compatible format (unique_id, ds, y).

## Overview

Converts prediction market datasets with varying schemas into standardized Nixtla format. Maps arbitrary column names to required schema, validates date parsing and numeric types, produces clean CSV output ready for forecasting. Optional visualization and sample forecast generation.

## Prerequisites

**Required**:
- Python 3.8+
- `pandas`, `matplotlib` packages

**Optional** (for forecasting):
- `statsforecast` for open-source models
- `nixtla` for TimeGPT (requires API key)

**Environment Variables**:
- `NIXTLA_TIMEGPT_API_KEY`: Required only if using `--timegpt` flag

**Installation**:
```bash
pip install pandas matplotlib statsforecast nixtla
```

## Instructions

### Step 1: Identify Column Mappings

Examine your input CSV to identify:
- **ID column**: Unique identifier for each contract/series
- **Date column**: Timestamp or date values
- **Target column**: Numeric value to forecast (price, volume, probability)

### Step 2: Run Transformation

Execute the transformation script:
```bash
python {baseDir}/scripts/transform_data.py --input data.csv \
    --id_col contract_id --date_col date --target_col price
```

**Available options**:
- `--input`: Input CSV file path (required)
- `--id_col`: Column name for unique ID (required)
- `--date_col`: Column name for date (required)
- `--target_col`: Column name for target variable (required)
- `--output`: Output file path (default: nixtla_data.csv)
- `--plot`: Generate time series visualization
- `--forecast`: Run sample forecast after transform
- `--timegpt`: Use TimeGPT instead of StatsForecast

### Step 3: Verify Output

Check the transformed data:
```bash
head -5 nixtla_data.csv
```

Expected format:
```
unique_id,ds,y
contract_1,2024-01-01,0.75
contract_1,2024-01-02,0.78
```

## Output

- **nixtla_data.csv**: Transformed data with columns (unique_id, ds, y)
- **time_series_plot.png**: Visualization of first series (if `--plot`)
- **Console output**: Transformation summary with series count, date range, value statistics

## Error Handling

1. **Error**: `Input file not found: data.csv`
   **Solution**: Verify file path exists and is readable

2. **Error**: `Column 'contract_id' not found. Available: [...]`
   **Solution**: Use exact column name from the available list

3. **Error**: `Invalid date format in date column`
   **Solution**: Ensure dates use YYYY-MM-DD or standard parseable format

4. **Error**: `Non-numeric data in target column`
   **Solution**: Clean non-numeric values from target column

5. **Error**: `NIXTLA_TIMEGPT_API_KEY not set`
   **Solution**: `export NIXTLA_TIMEGPT_API_KEY=your_key` or omit `--timegpt`

## Examples

See [examples](references/examples.md) for detailed usage scenarios.

## Resources

- Script: `{baseDir}/scripts/transform_data.py`
- Nixtla Docs: https://nixtla.github.io/
- Nixtla Schema: unique_id (string), ds (datetime), y (numeric)
