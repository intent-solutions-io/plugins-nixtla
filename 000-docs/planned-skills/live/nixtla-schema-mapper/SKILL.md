---
name: nixtla-schema-mapper
description: |
  Transforms tabular data into the Nixtla format (unique_id, ds, y).
  Use when needing to prepare time series data for Nixtla forecasting models.
  Trigger with "convert to Nixtla format", "Nixtla data schema", "prepare time series data".
allowed-tools: "Read,Write,Edit,Glob,Grep"
version: "1.0.0"
---

# Nixtla Schema Mapper

Converts data into the Nixtla-compatible (unique_id, ds, y) format.

## Overview

Analyzes input data, infers the mapping between columns and the `unique_id`, `ds` (datetime), and `y` (target) fields, and transforms the data accordingly. Useful when needing to process data for use with Nixtla's time series models or tools. Automatically detects date formats and handles missing values. Outputs a CSV file in the Nixtla format.

## Prerequisites

**Tools**: Read, Write, Edit, Glob, Grep

**Packages**:
```bash
pip install pandas matplotlib statsforecast
```

## Instructions

### Step 1: Transform data to Nixtla format

Read input CSV and transform to (unique_id, ds, y) format.

```bash
# Auto-detect column mappings
python {baseDir}/scripts/transform_data.py \
  --input input.csv \
  --output output.csv

# Or specify column mappings explicitly
python {baseDir}/scripts/transform_data.py \
  --input input.csv \
  --output output.csv \
  --id_col store_id \
  --date_col date \
  --target_col sales
```

**Parameters**:
- `--input`: Path to input CSV file
- `--output`: Path to output CSV file
- `--id_col`: (Optional) Name of unique ID column
- `--date_col`: (Optional) Name of date column
- `--target_col`: (Optional) Name of target variable column
- `--date_format`: (Optional) Date format string (e.g., '%Y-%m-%d')

**Output**: CSV file in Nixtla format with columns: unique_id, ds, y

### Step 2: Visualize transformed data

The transformation script automatically generates visualizations for up to 5 time series.

**Output**: `{output_file}_{unique_id}.png` for each series

### Step 3: Forecast with StatsForecast (optional)

Run forecasting on the transformed data.

```bash
python {baseDir}/scripts/forecast_with_statsforecast.py \
  --input output.csv \
  --horizon 24
```

**Parameters**:
- `--input`: Path to Nixtla-formatted CSV
- `--horizon`: Number of periods to forecast (default: 14)

**Output**: `statsforecast_forecasts.csv` with predictions

## Output

- **output.csv**: Transformed data in Nixtla format (unique_id, ds, y)
- **{output_file}_{unique_id}.png**: Visualizations of time series data
- **statsforecast_forecasts.csv**: Forecasts (if Step 3 executed)

## Error Handling

1. **Error**: `Could not infer mapping`
   **Solution**: Specify column mappings using `--id_col`, `--date_col`, `--target_col` arguments

2. **Error**: `Date parsing failed`
   **Solution**: Specify the date format using the `--date_format` argument (e.g., '%Y-%m-%d')

3. **Error**: `Missing values in target column`
   **Solution**: Handle missing values by removing rows or using imputation before running the script

4. **Error**: `Input file not found`
   **Solution**: Ensure the input file exists at the specified path

5. **Error**: `Input file must have columns: ['unique_id', 'ds', 'y']` (in StatsForecast step)
   **Solution**: Ensure the input file is in the correct Nixtla format from Step 1

## Examples

### Example 1: Sales Data

**Input**:
```csv
store_id,date,sales
A1,2023-01-01,100
A1,2023-01-02,110
```

**Command**:
```bash
python {baseDir}/scripts/transform_data.py --input sales.csv --output sales_nixtla.csv
```

**Output**:
```csv
unique_id,ds,y
A1,2023-01-01,100
A1,2023-01-02,110
```

### Example 2: Energy Consumption

**Input**:
```csv
id,timestamp,consumption
X1,2023-01-01 00:00:00,50
X1,2023-01-01 01:00:00,55
```

**Command**:
```bash
python {baseDir}/scripts/transform_data.py --input energy.csv --output energy_nixtla.csv
```

**Output**:
```csv
unique_id,ds,y
X1,2023-01-01 00:00:00,50
X1,2023-01-01 01:00:00,55
```

## Resources

- Data transformer: `{baseDir}/scripts/transform_data.py`
- StatsForecast forecaster: `{baseDir}/scripts/forecast_with_statsforecast.py`
