#!/usr/bin/env python3
"""
Contract Schema Mapper - Data Transformation
Transforms prediction market data to Nixtla format (unique_id, ds, y).

Usage:
    python transform_data.py --input data.csv --id_col contract_id \
                             --date_col date --target_col price

Author: Nixtla Skills Pack
Version: 1.0.0
"""

import argparse
import os
import sys
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd


def transform_data(
    input_file: str,
    id_col: str,
    date_col: str,
    target_col: str,
    output_file: str = "nixtla_data.csv",
    run_forecast: bool = False,
    use_timegpt: bool = False,
) -> pd.DataFrame:
    """
    Transform prediction market data to Nixtla format.

    Args:
        input_file: Path to input CSV file
        id_col: Column name for unique ID
        date_col: Column name for date
        target_col: Column name for target variable
        output_file: Output CSV file path
        run_forecast: Run sample forecast after transform
        use_timegpt: Use TimeGPT instead of StatsForecast

    Returns:
        Transformed DataFrame
    """
    # Load data
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        raise ValueError(f"Error reading CSV: {e}")

    # Validate columns exist
    for col, name in [(id_col, "id_col"), (date_col, "date_col"), (target_col, "target_col")]:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found. Available: {list(df.columns)}")

    # Rename to Nixtla schema
    df = df.rename(columns={id_col: "unique_id", date_col: "ds", target_col: "y"})

    # Convert types
    try:
        df["ds"] = pd.to_datetime(df["ds"])
    except Exception:
        raise ValueError("Invalid date format in date column. Use YYYY-MM-DD format.")

    try:
        df["y"] = pd.to_numeric(df["y"])
    except Exception:
        raise ValueError("Non-numeric data in target column.")

    # Keep only required columns
    df = df[["unique_id", "ds", "y"]].copy()
    df = df.sort_values(["unique_id", "ds"]).reset_index(drop=True)

    # Save transformed data
    df.to_csv(output_file, index=False)
    print(f"Transformed data saved to: {output_file}")

    # Print summary
    print(f"\nTransformation Summary:")
    print(f"  Series count: {df['unique_id'].nunique()}")
    print(f"  Total rows: {len(df)}")
    print(f"  Date range: {df['ds'].min()} to {df['ds'].max()}")
    print(f"  Value range: {df['y'].min():.4f} to {df['y'].max():.4f}")

    return df


def create_visualization(df: pd.DataFrame, output_plot: str = "time_series_plot.png") -> None:
    """Create time series visualization for first series."""
    first_id = df["unique_id"].iloc[0]
    series_df = df[df["unique_id"] == first_id]

    plt.figure(figsize=(12, 6))
    plt.plot(series_df["ds"], series_df["y"], marker="o", markersize=3)
    plt.title(f"Time Series: {first_id}")
    plt.xlabel("Date")
    plt.ylabel("Value (y)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_plot, dpi=150)
    plt.close()
    print(f"Plot saved to: {output_plot}")


def run_sample_forecast(df: pd.DataFrame, use_timegpt: bool = False) -> None:
    """Run sample forecast on transformed data."""
    if use_timegpt:
        api_key = os.getenv("NIXTLA_TIMEGPT_API_KEY")
        if not api_key:
            print("Warning: NIXTLA_TIMEGPT_API_KEY not set, skipping TimeGPT forecast")
            return

        try:
            from nixtla import NixtlaClient

            client = NixtlaClient(api_key=api_key)
            forecast = client.forecast(df=df, h=14, freq="D")
            print("\nTimeGPT Sample Forecast:")
            print(forecast.head())
        except Exception as e:
            print(f"TimeGPT forecast error: {e}")
    else:
        try:
            from statsforecast import StatsForecast
            from statsforecast.models import AutoARIMA, AutoETS

            sf = StatsForecast(models=[AutoETS(), AutoARIMA()], freq="D", n_jobs=-1)
            forecast = sf.forecast(df=df, h=14)
            print("\nStatsForecast Sample Forecast:")
            print(forecast.head())
        except Exception as e:
            print(f"StatsForecast error: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Transform prediction market data to Nixtla format"
    )
    parser.add_argument("--input", "-i", required=True, help="Input CSV file")
    parser.add_argument("--id_col", required=True, help="Unique ID column name")
    parser.add_argument("--date_col", required=True, help="Date column name")
    parser.add_argument("--target_col", required=True, help="Target variable column name")
    parser.add_argument("--output", "-o", default="nixtla_data.csv", help="Output CSV file")
    parser.add_argument("--plot", action="store_true", help="Create visualization")
    parser.add_argument("--forecast", action="store_true", help="Run sample forecast")
    parser.add_argument("--timegpt", action="store_true", help="Use TimeGPT for forecast")

    args = parser.parse_args()

    try:
        df = transform_data(
            input_file=args.input,
            id_col=args.id_col,
            date_col=args.date_col,
            target_col=args.target_col,
            output_file=args.output,
        )

        if args.plot:
            create_visualization(df)

        if args.forecast:
            run_sample_forecast(df, use_timegpt=args.timegpt)

        print("\nTransformation complete!")
        return 0

    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
