#!/usr/bin/env python3
"""
Correlation Mapper - Data Preparation
Loads multi-series data and pivots for correlation analysis
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import pandas as pd


def load_contract_data(filepath: str) -> pd.DataFrame:
    """
    Load multi-series contract data.

    Expected format: CSV with columns (unique_id, ds, y)
    where unique_id identifies different contracts.

    Args:
        filepath: Path to CSV file

    Returns:
        DataFrame in Nixtla format

    Raises:
        ValueError: If required columns are missing
        FileNotFoundError: If filepath does not exist
    """
    print(f"Loading data from {filepath}...")

    if not Path(filepath).exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    df = pd.read_csv(filepath)

    # Validate columns
    required = ["unique_id", "ds", "y"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Convert types
    df["ds"] = pd.to_datetime(df["ds"])
    df["y"] = pd.to_numeric(df["y"], errors="coerce")
    df["unique_id"] = df["unique_id"].astype(str)

    # Remove NaN values
    initial_len = len(df)
    df = df.dropna(subset=["y"])
    if len(df) < initial_len:
        print(f"Warning: Dropped {initial_len - len(df)} rows with NaN values")

    # Sort
    df = df.sort_values(["unique_id", "ds"]).reset_index(drop=True)

    n_contracts = df["unique_id"].nunique()
    print(f"Loaded {len(df)} rows, {n_contracts} contracts")

    if n_contracts < 2:
        raise ValueError("Need at least 2 contracts for correlation analysis")

    return df


def pivot_for_correlation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pivot long-format data to wide format for correlation.

    Args:
        df: Long format with unique_id, ds, y

    Returns:
        Wide format with ds as index, contracts as columns

    Raises:
        ValueError: If insufficient data after pivoting
    """
    # Pivot: rows=dates, columns=contracts, values=prices
    pivoted = df.pivot(index="ds", columns="unique_id", values="y")

    # Forward fill missing values (for misaligned dates)
    pivoted = pivoted.ffill()

    # Drop any remaining NaN rows
    initial_len = len(pivoted)
    pivoted = pivoted.dropna()

    if len(pivoted) < 30:
        raise ValueError(
            f"Insufficient data: {len(pivoted)} rows after pivot. Need at least 30."
        )

    if len(pivoted) < initial_len:
        print(f"Dropped {initial_len - len(pivoted)} rows with missing values")

    print(f"Pivoted to {len(pivoted)} dates x {len(pivoted.columns)} contracts")
    return pivoted


def calculate_returns(prices: pd.DataFrame, method: str = "log") -> pd.DataFrame:
    """
    Calculate returns from price data.

    Args:
        prices: Wide-format price DataFrame
        method: "log" for log returns, "simple" for simple returns

    Returns:
        Returns DataFrame

    Raises:
        ValueError: If invalid method specified
    """
    if method not in ["log", "simple"]:
        raise ValueError(f"Invalid method: {method}. Use 'log' or 'simple'")

    if method == "log":
        returns = np.log(prices / prices.shift(1))
    else:
        returns = prices.pct_change()

    # Drop first row (NaN)
    returns = returns.iloc[1:]

    print(f"Calculated {method} returns: {len(returns)} rows")
    return returns


def main():
    """Main entry point for data preparation."""
    parser = argparse.ArgumentParser(
        description="Prepare contract data for correlation analysis"
    )
    parser.add_argument(
        "input_file",
        type=str,
        help="Input CSV file with columns: unique_id, ds, y"
    )
    parser.add_argument(
        "--method",
        type=str,
        default="log",
        choices=["log", "simple"],
        help="Return calculation method (default: log)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=".",
        help="Output directory for generated files (default: current dir)"
    )

    args = parser.parse_args()

    try:
        # Load and prepare data
        df = load_contract_data(args.input_file)
        pivoted = pivot_for_correlation(df)
        returns = calculate_returns(pivoted, method=args.method)

        # Create output directory
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save intermediate files
        prices_path = output_dir / "prices_wide.csv"
        returns_path = output_dir / "returns.csv"

        pivoted.to_csv(prices_path)
        returns.to_csv(returns_path)

        print("\nData preparation complete:")
        print(f"  - {prices_path} ({len(pivoted)} x {len(pivoted.columns)})")
        print(f"  - {returns_path} ({len(returns)} x {len(returns.columns)})")
        print("\nNext: Run correlation_analysis.py")

        return 0

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
