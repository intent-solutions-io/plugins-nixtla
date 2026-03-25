---
name: nixtla-exogenous-integrator
description: "Incorporates external variables (holidays, weather, events) into TimeGPT forecasts to improve accuracy. Use when forecasts require external data, holidays impact sales, or weather affects demand. Trigger with 'include holidays', 'add weather data', 'integrate events'."
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
compatible-with: claude-code
tags: [nixtla, time-series, forecasting, exogenous-variables]
allowed-tools: "Read,Write,Bash(python:*),Glob,Grep"
---

# Nixtla Exogenous Integrator

Augments TimeGPT forecasts with exogenous variables for increased accuracy.

## Purpose

Enhances time series predictions by integrating external data sources like holidays, weather, and events.

## Overview

This skill enriches TimeGPT forecasts by considering external factors influencing time series data. It reads exogenous data from CSV files, aligns it with the historical data, and passes both to the TimeGPT API. This integration improves forecast accuracy, especially when events or external conditions affect the time series. The skill outputs an augmented forecast incorporating the impact of these exogenous variables.

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install nixtla pandas matplotlib
```

## Instructions

### Step 1: Prepare data

Read historical time series CSV and exogenous variables CSVs. Ensure they have a common date ('ds') column.

Script: `{baseDir}/scripts/load_data.py`

**Usage**:
```bash
python {baseDir}/scripts/load_data.py data.csv holidays.csv
```

The loader expects:
- Historical data: `unique_id`, `ds`, `y` columns
- Exogenous data: `ds` column plus feature columns

### Step 2: Align data

Merge historical and exogenous dataframes based on the 'ds' column using the alignment script.

Script: `{baseDir}/scripts/align_data.py`

The script validates that both datasets share a 'ds' column and checks for column name conflicts. It performs a left join to preserve all historical timestamps.

### Step 3: Generate forecast

Run the integration script with your data files and forecast parameters.

Script: `{baseDir}/scripts/integrate_exogenous.py`

**Usage**:
```bash
python {baseDir}/scripts/integrate_exogenous.py \
  --input data.csv \
  --exogenous holidays.csv \
  --horizon 14 \
  --freq D
```

**Parameters**:
- `--input`: Historical time series CSV file
- `--exogenous`: Exogenous variables CSV file (optional)
- `--horizon`: Number of periods to forecast
- `--freq`: Time series frequency (D=daily, H=hourly, M=monthly, etc.)

The script automatically:
1. Loads and validates both datasets
2. Aligns data on the 'ds' column
3. Prepares exogenous variables (converts to numeric, fills missing values)
4. Calls TimeGPT API with exogenous features
5. Saves forecast and generates visualization

## Output

- **forecast_exogenous.csv**: Predictions with integrated exogenous variables.
- **forecast_plot.png**: Visualization of the forecast with historical data and exogenous variables.

## Error Handling

1. **Error**: `Exogenous data missing 'ds' column`
   **Solution**: Rename the date column in the exogenous data to 'ds'.

2. **Error**: `Mismatch in date range between historical and exogenous data`
   **Solution**: Ensure the exogenous data covers the entire historical and forecast period.

3. **Error**: `Exogenous variables have NaN values in the forecast horizon`
   **Solution**: Provide future values for exogenous variables for the entire forecast horizon.

4. **Error**: `TimeGPT API rejected exogenous variables`
   **Solution**: Ensure exogenous variables are numeric and compatible with the TimeGPT API schema.

5. **Error**: `NIXTLA_TIMEGPT_API_KEY environment variable not set`
   **Solution**: Set your TimeGPT API key as an environment variable before running the script.

## Examples

See [examples](references/examples.md) for detailed usage patterns.

## Resources

- TimeGPT exogenous variables guide: https://docs.nixtla.io/
- Holiday calendar generation: https://github.com/dr-prodigy/python-holidays
- Weather API integration: https://openweathermap.org/api
- Scripts: `{baseDir}/scripts/` directory contains all executable code
