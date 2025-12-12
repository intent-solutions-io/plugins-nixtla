#!/usr/bin/env python3
"""
Market Risk Analyzer - Data Preparation
Loads price data and calculates returns
"""

import argparse
import sys
from typing import Tuple

import numpy as np
import pandas as pd


def load_price_data(filepath: str) -> pd.DataFrame:
    """
    Load price data from CSV file.

    Expected format:
    - Column 'ds' or 'date': datetime index
    - Column 'y' or 'price': price values

    Args:
        filepath: Path to CSV file

    Returns:
        DataFrame with datetime index and price column
    """
    print(f"Loading price data from {filepath}...")

    df = pd.read_csv(filepath)

    # Detect date column
    date_col = None
    for col in ["ds", "date", "Date", "timestamp", "Timestamp"]:
        if col in df.columns:
            date_col = col
            break

    if date_col is None:
        raise ValueError("No date column found. Need 'ds', 'date', or 'timestamp'")

    # Detect price column
    price_col = None
    for col in ["y", "price", "Price", "close", "Close", "value"]:
        if col in df.columns:
            price_col = col
            break

    if price_col is None:
        raise ValueError("No price column found. Need 'y', 'price', or 'close'")

    # Standardize
    df = df[[date_col, price_col]].copy()
    df.columns = ["ds", "price"]
    df["ds"] = pd.to_datetime(df["ds"])
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df.dropna()
    df = df.sort_values("ds").set_index("ds")

    print(f"Loaded {len(df)} price points from {df.index.min().date()} to {df.index.max().date()}")
    return df


def calculate_returns(prices: pd.DataFrame, method: str = "log") -> pd.Series:
    """
    Calculate returns from price series.

    Args:
        prices: DataFrame with 'price' column
        method: "log" for log returns, "simple" for simple returns

    Returns:
        Series of returns
    """
    if method == "log":
        returns = np.log(prices["price"] / prices["price"].shift(1))
    else:
        returns = prices["price"].pct_change()

    return returns.dropna()


def detect_frequency(df: pd.DataFrame) -> str:
    """Detect the frequency of the time series."""
    if len(df) < 2:
        return "D"

    # Calculate median time difference
    diffs = pd.Series(df.index).diff().dropna()
    median_diff = diffs.median()

    if median_diff <= pd.Timedelta(hours=1):
        return "H"  # Hourly
    elif median_diff <= pd.Timedelta(days=1):
        return "D"  # Daily
    elif median_diff <= pd.Timedelta(weeks=1):
        return "W"  # Weekly
    else:
        return "M"  # Monthly


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Prepare price data for risk analysis")
    parser.add_argument("input_file", help="Path to CSV file with price data")
    parser.add_argument(
        "--method",
        choices=["log", "simple"],
        default="log",
        help="Return calculation method (default: log)",
    )
    parser.add_argument(
        "--output", default="returns.csv", help="Output file for returns (default: returns.csv)"
    )

    args = parser.parse_args()

    try:
        # Load and process data
        prices = load_price_data(args.input_file)
        returns = calculate_returns(prices, method=args.method)
        freq = detect_frequency(prices)

        # Save returns
        returns.to_csv(args.output, header=["returns"])

        print(f"\nData Summary:")
        print(f"  Frequency: {freq}")
        print(f"  Returns: {len(returns)} observations")
        print(f"  Mean return: {returns.mean():.4%}")
        print(f"  Volatility: {returns.std():.4%}")
        print(f"\nReturns saved to {args.output}")

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
