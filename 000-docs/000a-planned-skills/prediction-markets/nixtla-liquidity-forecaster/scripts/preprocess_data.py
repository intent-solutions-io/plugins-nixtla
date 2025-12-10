"""Preprocess orderbook data for TimeGPT input.

This module cleans and formats raw orderbook data into the format
required by Nixtla's TimeGPT API.
"""

import argparse
import logging
from typing import Tuple

import numpy as np
import pandas as pd

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def preprocess_orderbook_data(orderbook_df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess the orderbook data for TimeGPT input.

    Calculates mid-price, spread, and depth from raw orderbook data.
    Formats the data according to Nixtla's expected schema with columns:
    unique_id, ds, y, spread, depth.

    Args:
        orderbook_df: A Pandas DataFrame containing the raw orderbook data
            with columns: price, quantity, side.

    Returns:
        A Pandas DataFrame containing the preprocessed data in the Nixtla format.

    Raises:
        ValueError: If required columns are missing or insufficient data.
    """
    try:
        # Ensure necessary columns exist and are of the correct type
        if not all(col in orderbook_df.columns for col in ["price", "quantity", "side"]):
            raise ValueError("Missing required columns: price, quantity, side")

        orderbook_df["price"] = pd.to_numeric(orderbook_df["price"], errors="coerce")
        orderbook_df["quantity"] = pd.to_numeric(
            orderbook_df["quantity"], errors="coerce"
        )

        # Handle missing values (e.g., replace with 0 or drop)
        orderbook_df.dropna(subset=["price", "quantity"], inplace=True)

        # Calculate mid-price
        bids = (
            orderbook_df[orderbook_df["side"] == "bid"]
            .groupby("price")["quantity"]
            .sum()
        )
        asks = (
            orderbook_df[orderbook_df["side"] == "ask"]
            .groupby("price")["quantity"]
            .sum()
        )

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
        data = {
            "ds": [pd.Timestamp.now()],
            "mid_price": [mid_price],
            "spread": [spread],
            "depth": [depth],
        }
        processed_df = pd.DataFrame(data)

        # Convert 'ds' to datetime and set as index
        processed_df["ds"] = pd.to_datetime(processed_df["ds"])
        processed_df.set_index("ds", inplace=True)

        # Resample to a fixed frequency (e.g., 1 minute)
        processed_df = processed_df.resample("1T").mean().interpolate()

        # Add unique_id column for Nixtla
        processed_df["unique_id"] = "polymarket"

        # Rename columns to match Nixtla's expected format
        processed_df = processed_df.rename(columns={"mid_price": "y"})

        # Select and reorder columns
        processed_df = processed_df[["unique_id", "y", "spread", "depth"]]
        processed_df.reset_index(inplace=True)

        return processed_df

    except ValueError as e:
        logging.error(f"Error during data preprocessing: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Preprocess orderbook data for TimeGPT."
    )
    parser.add_argument(
        "--input_file",
        required=True,
        help="Path to the raw orderbook data CSV file.",
    )
    parser.add_argument(
        "--output",
        default="preprocessed_data.csv",
        help="Output CSV file path (default: preprocessed_data.csv)",
    )
    args = parser.parse_args()

    try:
        raw_orderbook_data = pd.read_csv(args.input_file)
        preprocessed_data = preprocess_orderbook_data(raw_orderbook_data)
        print(preprocessed_data.head())
        preprocessed_data.to_csv(args.output, index=False)
        logging.info(f"Preprocessed data saved to {args.output}")

    except FileNotFoundError:
        logging.error(f"Input file not found: {args.input_file}")
        raise
    except Exception as e:
        logging.error(f"Failed to preprocess and save data: {e}")
        raise


if __name__ == "__main__":
    main()
