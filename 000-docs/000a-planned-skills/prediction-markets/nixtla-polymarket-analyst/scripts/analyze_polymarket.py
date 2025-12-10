#!/usr/bin/env python3
"""
Complete Polymarket Analysis Pipeline

End-to-end workflow that fetches contract data, transforms it to Nixtla format,
generates TimeGPT forecasts, and produces analysis reports with visualizations.
"""

import argparse
import json
import sys
from datetime import datetime

import pandas as pd

from fetch_contract import get_contract_data
from transform_data import transform_to_nixtla
from forecast_contract import (
    forecast_with_timegpt,
    create_forecast_plot,
    analyze_forecast
)


def run_polymarket_analysis(
    condition_id: str,
    horizon: int = 24,
    days_history: int = 30,
    output_dir: str = "."
) -> dict:
    """
    Run complete Polymarket analysis pipeline.

    Args:
        condition_id: Polymarket contract ID
        horizon: Forecast horizon in periods
        days_history: Days of historical data to fetch
        output_dir: Directory for output files

    Returns:
        Dict with analysis results and file paths

    Raises:
        Exception: If any step fails
    """
    print(f"\n{'='*60}")
    print("POLYMARKET CONTRACT ANALYSIS")
    print(f"Contract: {condition_id}")
    print(f"{'='*60}\n")

    # Step 1: Fetch data
    print("Step 1: Fetching contract data...")
    contract_data = get_contract_data(condition_id, days_history)
    print(f"  Fetched {len(contract_data['prices'])} price points")

    # Step 2: Transform data
    print("\nStep 2: Transforming to Nixtla format...")
    df = transform_to_nixtla(contract_data)
    print(f"  Transformed to {len(df)} time series points")

    # Infer frequency
    if len(df) > 1:
        time_diff = (df["ds"].iloc[1] - df["ds"].iloc[0]).total_seconds()
        freq = "H" if time_diff <= 3600 else "D"
    else:
        freq = "H"

    # Step 3: Forecast
    print(f"\nStep 3: Forecasting {horizon} periods ahead...")
    forecast_df, metadata = forecast_with_timegpt(df, horizon=horizon, freq=freq)
    print("  Generated forecast with confidence intervals")

    # Step 4: Analyze and save
    print("\nStep 4: Generating outputs...")

    # Save files
    prefix = f"{output_dir}/polymarket_{condition_id[:8]}"

    df.to_csv(f"{prefix}_historical.csv", index=False)
    forecast_df.to_csv(f"{prefix}_forecast.csv", index=False)

    create_forecast_plot(
        historical=df,
        forecast=forecast_df,
        title=f"Polymarket: {contract_data['question'][:50]}...",
        output_path=f"{prefix}_plot.png"
    )

    # Analyze
    current_price = df["y"].iloc[-1]
    analysis = analyze_forecast(forecast_df, current_price)

    # Complete output
    output = {
        "contract_id": condition_id,
        "question": contract_data["question"],
        "analysis": analysis,
        "metadata": metadata,
        "files": {
            "historical": f"{prefix}_historical.csv",
            "forecast": f"{prefix}_forecast.csv",
            "plot": f"{prefix}_plot.png"
        }
    }

    with open(f"{prefix}_analysis.json", "w") as f:
        json.dump(output, f, indent=2, default=str)

    # Print summary
    print(f"\n{'='*60}")
    print("ANALYSIS COMPLETE")
    print(f"{'='*60}")
    print(f"\nContract: {contract_data['question'][:60]}...")
    print(f"\nCurrent Price: ${analysis['current_price']:.4f}")
    print(f"Forecast Price: ${analysis['forecast_price']:.4f}")
    print(f"Expected Change: {analysis['pct_change']:+.2f}%")
    print(f"\nSIGNAL: {analysis['signal']} ({analysis['trend']})")
    print("\nOutput files:")
    for name, path in output["files"].items():
        print(f"  - {name}: {path}")
    print(f"\n{analysis['disclaimer']}")

    return output


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Complete Polymarket contract analysis with TimeGPT forecasting"
    )
    parser.add_argument(
        "contract_id",
        help="Polymarket contract/condition ID"
    )
    parser.add_argument(
        "--horizon",
        type=int,
        default=24,
        help="Forecast horizon in periods (default: 24)"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="Days of historical data (default: 30)"
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Output directory (default: current directory)"
    )

    args = parser.parse_args()

    try:
        run_polymarket_analysis(
            condition_id=args.contract_id,
            horizon=args.horizon,
            days_history=args.days,
            output_dir=args.output_dir
        )
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
