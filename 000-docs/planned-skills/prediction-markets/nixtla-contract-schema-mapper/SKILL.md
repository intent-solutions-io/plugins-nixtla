---
name: nixtla-contract-schema-mapper
description: |
  Transforms prediction market data to Nixtla format (unique_id, ds, y).
  Use when preparing prediction market datasets for Nixtla's forecasting tools.
  Trigger with "convert to Nixtla format", "Nixtla schema", "transform data".
allowed-tools: "Read,Write,Edit,Glob,Grep"
version: "1.0.0"
---

# Nixtla Contract Schema Mapper

Transforms prediction market data into the Nixtla-compatible format (unique_id, ds, y).

## Overview

Converts prediction market datasets with varying schemas into a standardized Nixtla format. This enables the data to be ingested by Nixtla's forecasting models. Analyzes the input schema, maps relevant fields to 'unique_id', 'ds', and 'y', and outputs a CSV file in the Nixtla format. Useful for preparing datasets with time series information associated with unique entities.

## Prerequisites

**Tools**: Read, Write, Edit, Glob, Grep

**Packages**:
```bash
pip install pandas matplotlib statsforecast
```

**Environment Variables**:
For using TimeGPT, you need to set the `NIXTLA_TIMEGPT_API_KEY` environment variable.

## Instructions

### Step 1: Load Data

Read the prediction market data from a CSV file.

### Step 2: Analyze Schema and Transform Data

Run the following script to analyze the schema, transform the data, and save it in Nixtla format.

```python
import pandas as pd
import argparse
import os
from typing import Optional
import matplotlib.pyplot as plt
from statsforecast import StatsForecast
from statsforecast.models import AutoETS, AutoARIMA, SeasonalNaive, AutoTheta

def transform_data(
    input_file: str,
    id_col: str,
    date_col: str,
    target_col: str,
    output_file: str = "nixtla_data.csv",
    timegpt: bool = False
) -> None:
    """
    Transforms prediction market data to Nixtla format (unique_id, ds, y).

    Args:
        input_file: Path to the input CSV file.
        id_col: Name of the column containing the unique ID.
        date_col: Name of the column containing the date.
        target_col: Name of the column containing the target variable.
        output_file: Name of the output CSV file. Defaults to "nixtla_data.csv".
        timegpt: Whether to use TimeGPT for forecasting. Defaults to False.
    """
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file not found: {input_file}")
    except Exception as e:
        raise Exception(f"Error reading input file: {e}")

    # Check if columns exist
    if id_col not in df.columns:
        raise ValueError(f"Column not found: {id_col}")
    if date_col not in df.columns:
        raise ValueError(f"Column not found: {date_col}")
    if target_col not in df.columns:
        raise ValueError(f"Column not found: {target_col}")

    # Rename columns
    df = df.rename(
        columns={id_col: "unique_id", date_col: "ds", target_col: "y"}
    )

    # Convert 'ds' column to datetime
    try:
        df["ds"] = pd.to_datetime(df["ds"])
    except ValueError:
        raise ValueError(
            "Invalid date format in date_column.  Please ensure dates are in a standard format (e.g., YYYY-MM-DD)."
        )

    # Ensure 'y' column is numeric
    try:
        df["y"] = pd.to_numeric(df["y"])
    except ValueError:
        raise ValueError(
            "Non-numeric data in target_column. Please ensure the target column contains only numeric data."
        )

    # Save the transformed data
    try:
        df.to_csv(output_file, index=False)
        print(f"Transformed data saved to {output_file}")
    except Exception as e:
        raise Exception(f"Error saving output file: {e}")

    # Basic EDA and Visualization
    print("\nBasic EDA:")
    print(df.head())
    print(df.describe())

    # Plotting the time series for the first unique_id
    first_id = df['unique_id'].iloc[0]
    df_plot = df[df['unique_id'] == first_id].set_index('ds')
    plt.figure(figsize=(12, 6))
    plt.plot(df_plot['y'])
    plt.title(f'Time Series for {first_id}')
    plt.xlabel('Date')
    plt.ylabel('Target Variable (y)')
    plt.grid(True)
    plt.savefig('time_series_plot.png')
    print("Time series plot saved to time_series_plot.png")

    # Example Forecasting with StatsForecast
    try:
        sf = StatsForecast(models=[AutoETS(), AutoARIMA()], freq='D', n_jobs=-1)
        forecasts = sf.forecast(df=df, h=14)
        print("\nStatsForecast Forecasts:")
        print(forecasts.head())
    except Exception as e:
        print(f"Error during StatsForecast forecasting: {e}")

    # Example Forecasting with TimeGPT (if timegpt is True and API key is set)
    if timegpt:
        try:
            from nixtla import NixtlaClient
            api_key = os.getenv('NIXTLA_TIMEGPT_API_KEY')
            if not api_key:
                raise ValueError("NIXTLA_TIMEGPT_API_KEY environment variable not set.")
            client = NixtlaClient(api_key=api_key)
            forecast = client.forecast(df=df, h=24, freq='D')
            print("\nTimeGPT Forecasts:")
            print(forecast.head())
        except ImportError:
            print("NixtlaClient not installed. Please install it to use TimeGPT.")
        except ValueError as e:
            print(f"Error during TimeGPT forecasting: {e}")
        except Exception as e:
            print(f"Error during TimeGPT forecasting: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Transforms prediction market data to Nixtla format (unique_id, ds, y)."
    )
    parser.add_argument("--input", required=True, help="Path to the input CSV file")
    parser.add_argument(
        "--id_col", required=True, help="Name of the column containing the unique ID"
    )
    parser.add_argument(
        "--date_col", required=True, help="Name of the column containing the date"
    )
    parser.add_argument(
        "--target_col", required=True, help="Name of the column containing the target variable"
    )
    parser.add_argument(
        "--output", default="nixtla_data.csv", help="Name of the output CSV file"
    )
    parser.add_argument(
        "--timegpt", action="store_true", help="Use TimeGPT for forecasting"
    )

    args = parser.parse_args()

    try:
        transform_data(args.input, args.id_col, args.date_col, args.target_col, args.output, args.timegpt)
    except Exception as e:
        print(f"Error: {e}")
```

### Step 3: Generate Output

The transformed data is saved in Nixtla format (unique_id, ds, y) to a new CSV file.

## Output

- **nixtla_data.csv**: Transformed data in Nixtla format (unique_id, ds, y).
- **time_series_plot.png**: A plot of the time series data for the first unique ID.

## Error Handling

1. **Error**: `Missing required argument: --input`
   **Solution**: Provide the input CSV file path using `--input input.csv`.

2. **Error**: `Column not found: id_column`
   **Solution**: Ensure the specified ID column exists in the input CSV file.

3. **Error**: `Invalid date format in date_column`
   **Solution**: Correct the date format in the specified column or use a custom date parser.

4. **Error**: `Non-numeric data in target_column`
   **Solution**: Ensure the target column contains only numeric data.

5. **Error**: `NIXTLA_TIMEGPT_API_KEY environment variable not set.`
   **Solution**: Set the `NIXTLA_TIMEGPT_API_KEY` environment variable before running the script with the `--timegpt` flag.

## Examples

### Example 1: Basic Conversion

**Input**:
```
contract_id,date,volume
contract_1,2024-01-01,100
contract_1,2024-01-02,120
```

**Output**:
```
unique_id,ds,y
contract_1,2024-01-01,100
contract_1,2024-01-02,120
```

### Example 2: Renaming Columns

**Input**:
```
id,timestamp,price
market_1,2024-01-01,0.75
market_1,2024-01-02,0.80
```

**Output**:
```
unique_id,ds,y
market_1,2024-01-01,0.75
market_1,2024-01-02,0.80
```

## Usage

To run the script, use the following command:

```bash
python transform.py --input input.csv --id_col id_column --date_col date_column --target_col target_column
```

To use TimeGPT for forecasting (requires `NIXTLA_TIMEGPT_API_KEY` environment variable):

```bash
python transform.py --input input.csv --id_col id_column --date_col date_column --target_col target_column --timegpt
```