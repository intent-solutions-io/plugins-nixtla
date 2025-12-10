#!/usr/bin/env python3
"""
Transform Polymarket Data to Nixtla Format

Converts raw Polymarket price data to Nixtla time series format
with columns: unique_id, ds, y.
"""

import argparse
import json
import sys
from datetime import datetime

import pandas as pd


def load_contract_data(filepath: str) -> dict:
    """
    Load contract data from JSON file.

    Args:
        filepath: Path to contract data JSON

    Returns:
        Dict with contract data
    """
    with open(filepath, 'r') as f:
        return json.load(f)


def transform_to_nixtla(contract_data: dict) -> pd.DataFrame:
    """
    Transform Polymarket price data to Nixtla format.

    Args:
        contract_data: Dict with prices list

    Returns:
        DataFrame with unique_id, ds, y columns

    Raises:
        ValueError: If no price data available
    """
    prices = contract_data.get("prices", [])

    if not prices:
        raise ValueError("No price data available")

    records = []
    for price_point in prices:
        # Handle different API response formats
        timestamp = price_point.get("t") or price_point.get("timestamp")
        price = (
            price_point.get("p") or
            price_point.get("yes_price") or
            price_point.get("price")
        )

        if timestamp and price is not None:
            # Convert timestamp (may be unix or ISO)
            if isinstance(timestamp, (int, float)):
                ds = datetime.fromtimestamp(timestamp)
            else:
                ds = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))

            records.append({
                "unique_id": contract_data.get("condition_id", "contract_1"),
                "ds": ds,
                "y": float(price)
            })

    df = pd.DataFrame(records)
    df = df.sort_values("ds").reset_index(drop=True)

    # Remove duplicates (keep last price for each timestamp)
    df = df.drop_duplicates(subset=["unique_id", "ds"], keep="last")

    return df


def validate_nixtla_data(df: pd.DataFrame) -> bool:
    """
    Validate the transformed data meets Nixtla requirements.

    Args:
        df: DataFrame to validate

    Returns:
        True if valid, False otherwise
    """
    required_cols = ["unique_id", "ds", "y"]

    for col in required_cols:
        if col not in df.columns:
            print(f"Missing required column: {col}", file=sys.stderr)
            return False

    if df["y"].isna().any():
        null_count = df["y"].isna().sum()
        print(f"Warning: {null_count} null values in y column", file=sys.stderr)

    if len(df) < 10:
        print(
            f"Warning: Only {len(df)} data points - may be insufficient for forecasting",
            file=sys.stderr
        )

    return True


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Transform Polymarket data to Nixtla format"
    )
    parser.add_argument(
        "input_file",
        help="Path to contract data JSON file"
    )
    parser.add_argument(
        "--output",
        help="Output CSV file path (default: input_nixtla.csv)"
    )

    args = parser.parse_args()

    try:
        contract_data = load_contract_data(args.input_file)
        df = transform_to_nixtla(contract_data)

        if not validate_nixtla_data(df):
            sys.exit(1)

        output_file = args.output or args.input_file.replace("_data.json", "_nixtla.csv")
        df.to_csv(output_file, index=False)

        print(f"Transformed {len(df)} price points to Nixtla format")
        print(f"Date range: {df['ds'].min()} to {df['ds'].max()}")
        print(f"Price range: {df['y'].min():.4f} to {df['y'].max():.4f}")
        print(f"Saved to {output_file}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
