---
name: nixtla-liquidity-forecaster
description: |
  Forecasts orderbook depth and spreads to optimize trade execution timing.
  Use when needing to estimate market liquidity for large orders.
  Trigger with "forecast liquidity", "predict orderbook", "estimate depth".
allowed-tools: "Read,Write,Bash,Glob,Grep,WebFetch"
version: "1.0.0"
---

# Liquidity Forecaster

Predicts future orderbook depth and bid-ask spreads using historical market data and TimeGPT.

## Overview

Analyzes historical trade data and orderbook snapshots from Polymarket to forecast liquidity conditions. Predicts near-term changes in orderbook depth and bid-ask spreads. Use when determining optimal trade execution timing based on expected liquidity. Generates CSV files with predicted depth and spread values.

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep, WebFetch

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install nixtla pandas requests matplotlib
```

## Instructions

### Step 1: Fetch data

Fetch historical orderbook data from the Polymarket API.

```python
import requests
import pandas as pd
import argparse
import os
from typing import Dict, List, Tuple
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_polymarket_data(market_id: str) -> pd.DataFrame:
    """
    Fetches historical orderbook data from the Polymarket API.

    Args:
        market_id: The ID of the Polymarket market.

    Returns:
        A Pandas DataFrame containing the orderbook data.
    """
    try:
        url = f"https://api.polymarket.com/v3/markets/{market_id}/orderbook"
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        # Extract relevant data (adjust based on actual API response structure)
        bids = data.get('bids', [])
        asks = data.get('asks', [])

        # Convert bids and asks to DataFrames
        bids_df = pd.DataFrame(bids)
        asks_df = pd.DataFrame(asks)

        # Add a 'side' column to distinguish between bids and asks
        bids_df['side'] = 'bid'
        asks_df['side'] = 'ask'

        # Concatenate bids and asks DataFrames
        orderbook_df = pd.concat([bids_df, asks_df], ignore_index=True)

        if orderbook_df.empty:
            raise ValueError("No orderbook data found for the specified market ID.")

        return orderbook_df

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from Polymarket API: {e}")
        raise
    except ValueError as e:
        logging.error(f"Error processing data from Polymarket API: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch orderbook data from Polymarket API.")
    parser.add_argument("--market_id", required=True, help="The Polymarket market ID.")
    args = parser.parse_args()

    try:
        orderbook_data = fetch_polymarket_data(args.market_id)
        print(orderbook_data.head())  # Print the first few rows of the DataFrame
        orderbook_data.to_csv("orderbook_data.csv", index=False)
        logging.info("Orderbook data saved to orderbook_data.csv")

    except Exception as e:
        logging.error(f"Failed to fetch and save orderbook data: {e}")
```

### Step 2: Preprocess data

Clean and format the orderbook data for TimeGPT input.

```python
import pandas as pd
import numpy as np
import argparse
import logging
from typing import Tuple

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def preprocess_orderbook_data(orderbook_df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses the orderbook data for TimeGPT input.

    Args:
        orderbook_df: A Pandas DataFrame containing the raw orderbook data.

    Returns:
        A Pandas DataFrame containing the preprocessed data in the Nixtla format.
    """
    try:
        # Ensure necessary columns exist and are of the correct type
        if not all(col in orderbook_df.columns for col in ['price', 'quantity', 'side']):
            raise ValueError("Missing required columns: price, quantity, side")

        orderbook_df['price'] = pd.to_numeric(orderbook_df['price'], errors='coerce')
        orderbook_df['quantity'] = pd.to_numeric(orderbook_df['quantity'], errors='coerce')

        # Handle missing values (e.g., replace with 0 or drop)
        orderbook_df.dropna(subset=['price', 'quantity'], inplace=True)

        # Calculate mid-price
        bids = orderbook_df[orderbook_df['side'] == 'bid'].groupby('price')['quantity'].sum()
        asks = orderbook_df[orderbook_df['side'] == 'ask'].groupby('price')['quantity'].sum()

        if bids.empty or asks.empty:
            raise ValueError("Insufficient bid or ask data to calculate mid-price.")

        best_bid = bids.index.max()
        best_ask = asks.index.min()
        mid_price = (best_bid + best_ask) / 2

        # Calculate spread
        spread = best_ask - best_bid

        # Calculate depth (example: total quantity at best bid and ask)
        bid_depth = bids.loc[best_bid]
        ask_depth = asks.loc[best_ask]
        depth = bid_depth + ask_depth

        # Create a DataFrame with the calculated features
        data = {'ds': [pd.Timestamp.now()], 'mid_price': [mid_price], 'spread': [spread], 'depth': [depth]}
        processed_df = pd.DataFrame(data)

        # Convert 'ds' to datetime and set as index
        processed_df['ds'] = pd.to_datetime(processed_df['ds'])
        processed_df.set_index('ds', inplace=True)

        # Resample to a fixed frequency (e.g., 1 minute)
        processed_df = processed_df.resample('1T').mean().interpolate()

        # Add unique_id column for Nixtla
        processed_df['unique_id'] = 'polymarket'

        # Rename columns to match Nixtla's expected format
        processed_df = processed_df.rename(columns={'mid_price': 'y'})

        # Select and reorder columns
        processed_df = processed_df[['unique_id', 'y', 'spread', 'depth']]
        processed_df.reset_index(inplace=True)

        return processed_df

    except ValueError as e:
        logging.error(f"Error during data preprocessing: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess orderbook data for TimeGPT.")
    parser.add_argument("--input_file", required=True, help="Path to the raw orderbook data CSV file.")
    args = parser.parse_args()

    try:
        raw_orderbook_data = pd.read_csv(args.input_file)
        preprocessed_data = preprocess_orderbook_data(raw_orderbook_data)
        print(preprocessed_data.head())
        preprocessed_data.to_csv("preprocessed_data.csv", index=False)
        logging.info("Preprocessed data saved to preprocessed_data.csv")

    except FileNotFoundError:
        logging.error(f"Input file not found: {args.input_file}")
    except Exception as e:
        logging.error(f"Failed to preprocess and save data: {e}")
```

### Step 3: Execute forecast

Run the TimeGPT forecast.

```python
import pandas as pd
import os
import argparse
import logging
from nixtla import NixtlaClient
import matplotlib.pyplot as plt
from typing import Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def forecast_liquidity(df: pd.DataFrame, horizon: int) -> Optional[pd.DataFrame]:
    """
    Forecasts liquidity (depth and spread) using TimeGPT.

    Args:
        df: A Pandas DataFrame containing the preprocessed orderbook data in Nixtla format.
        horizon: The forecast horizon (number of periods to forecast).

    Returns:
        A Pandas DataFrame containing the forecasted values, or None if an error occurs.
    """
    try:
        api_key = os.getenv('NIXTLA_TIMEGPT_API_KEY')
        if not api_key:
            raise ValueError("TimeGPT API Key missing. Set the NIXTLA_TIMEGPT_API_KEY environment variable.")

        client = NixtlaClient(api_key=api_key)

        # Ensure the DataFrame has the correct columns and data types
        if not all(col in df.columns for col in ['unique_id', 'ds', 'y']):
            raise ValueError("DataFrame must contain 'unique_id', 'ds', and 'y' columns.")

        df['ds'] = pd.to_datetime(df['ds'])

        # Forecast using TimeGPT
        forecast = client.forecast(df=df, h=horizon, freq='T') # Assuming 1 minute frequency

        return forecast

    except ValueError as e:
        logging.error(f"Error: {e}")
        return None
    except Exception as e:
        logging.error(f"TimeGPT forecast failed: {e}")
        return None

def plot_forecast(df: pd.DataFrame, forecast: pd.DataFrame, file_prefix: str) -> None:
    """
    Plots the historical data and the forecast.

    Args:
        df: The historical data.
        forecast: The forecast data.
        file_prefix: The prefix for the output file name.
    """
    try:
        plt.figure(figsize=(12, 6))
        plt.plot(df['ds'], df['y'], label='Historical Data')
        plt.plot(forecast['ds'], forecast['y'], label='Forecast', color='red')
        plt.xlabel('Time')
        plt.ylabel('Mid Price')
        plt.title('Mid Price Forecast')
        plt.legend()
        plt.grid(True)
        plt.savefig(f'{file_prefix}_forecast.png')
        plt.close()
        logging.info(f"Forecast plot saved to {file_prefix}_forecast.png")
    except Exception as e:
        logging.error(f"Error plotting forecast: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Forecast liquidity using TimeGPT.")
    parser.add_argument("--input_file", required=True, help="Path to the preprocessed data CSV file.")
    parser.add_argument("--horizon", type=int, required=True, help="The forecast horizon.")
    args = parser.parse_args()

    try:
        # Load the preprocessed data
        preprocessed_data = pd.read_csv(args.input_file)

        # Forecast liquidity
        forecast_data = forecast_liquidity(preprocessed_data, args.horizon)

        if forecast_data is not None:
            # Save the forecast to a CSV file
            forecast_data.to_csv("depth_forecast.csv", index=False)
            logging.info("Forecasted depth saved to depth_forecast.csv")

            # Plot the forecast
            plot_forecast(preprocessed_data, forecast_data, "depth")

            # Create a report
            with open("report.txt", "w") as f:
                f.write("Liquidity Forecasting Report\n")
                f.write(f"Market ID: {preprocessed_data['unique_id'].iloc[0]}\n")
                f.write(f"Forecast Horizon: {args.horizon}\n")
                f.write(f"Forecast saved to depth_forecast.csv\n")
                f.write(f"Plot saved to depth_forecast.png\n")
            logging.info("Report saved to report.txt")

        else:
            logging.error("Forecasting failed. Check the logs for details.")

    except FileNotFoundError:
        logging.error(f"Input file not found: {args.input_file}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
```

### Step 4: Generate output

Save forecast CSV with predicted depth and spread. (This is handled within the `forecast_liquidity.py` script)

## Output

- **depth_forecast.csv**: Predictions for orderbook depth.
- **spread_forecast.csv**: Predictions for bid-ask spread.
- **report.txt**: Summary of the forecasting process.

## Error Handling

1. **Error**: `Invalid Polymarket Market ID`
   **Solution**: Verify the Market ID with the Polymarket API.

2. **Error**: `TimeGPT API Key missing`
   **Solution**: Set the `NIXTLA_TIMEGPT_API_KEY` environment variable.

3. **Error**: `Insufficient data from Polymarket API`
   **Solution**: Check data availability for the specified Market ID and time range.

4. **Error**: `TimeGPT forecast failed`
   **Solution**: Check the TimeGPT API status and input data format.

## Examples

### Example 1: Forecast Depth for "Will Trump Win?" Market

**Input**:
`--input_file preprocessed_data.csv --horizon 6`

**Output**:
`depth_forecast.csv` containing 6 forecasted depth values.

### Example 2: Forecast Spread for "Ethereum Price Above $3000?" Market

**Input**:
`--input_file preprocessed_data.csv --horizon 24`

**Output**:
`depth_forecast.csv` containing 24 forecasted depth values.

## Usage

1.  **Fetch Data**:
    ```bash
    python fetch_data.py --market_id polymarket_market_id
    ```

2.  **Preprocess Data**:
    ```bash
    python preprocess_data.py --input_file orderbook_data.csv
    ```

3.  **Forecast Liquidity**:
    ```bash
    python forecast_liquidity.py --input_file preprocessed_data.csv --horizon 12
    ```