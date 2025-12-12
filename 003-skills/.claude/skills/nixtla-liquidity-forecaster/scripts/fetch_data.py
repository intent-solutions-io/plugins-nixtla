"""Fetch orderbook data from Polymarket API.

This module fetches historical orderbook data from the Polymarket API
and saves it to a CSV file for further processing.
"""

import argparse
import logging
import os
from typing import Dict, List

import pandas as pd
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def fetch_polymarket_data(market_id: str) -> pd.DataFrame:
    """Fetch historical orderbook data from the Polymarket API.

    Args:
        market_id: The ID of the Polymarket market.

    Returns:
        A Pandas DataFrame containing the orderbook data.

    Raises:
        requests.exceptions.RequestException: If the API request fails.
        ValueError: If no orderbook data is found for the specified market ID.
    """
    try:
        url = f"https://api.polymarket.com/v3/markets/{market_id}/orderbook"
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        # Extract relevant data (adjust based on actual API response structure)
        bids = data.get("bids", [])
        asks = data.get("asks", [])

        # Convert bids and asks to DataFrames
        bids_df = pd.DataFrame(bids)
        asks_df = pd.DataFrame(asks)

        # Add a 'side' column to distinguish between bids and asks
        bids_df["side"] = "bid"
        asks_df["side"] = "ask"

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


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Fetch orderbook data from Polymarket API.")
    parser.add_argument("--market_id", required=True, help="The Polymarket market ID.")
    parser.add_argument(
        "--output",
        default="orderbook_data.csv",
        help="Output CSV file path (default: orderbook_data.csv)",
    )
    args = parser.parse_args()

    try:
        orderbook_data = fetch_polymarket_data(args.market_id)
        print(orderbook_data.head())  # Print the first few rows of the DataFrame
        orderbook_data.to_csv(args.output, index=False)
        logging.info(f"Orderbook data saved to {args.output}")

    except Exception as e:
        logging.error(f"Failed to fetch and save orderbook data: {e}")
        raise


if __name__ == "__main__":
    main()
