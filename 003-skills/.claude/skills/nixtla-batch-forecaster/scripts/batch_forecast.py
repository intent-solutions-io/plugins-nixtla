#!/usr/bin/env python3
"""
Batch Forecaster - Main Engine
Forecasts multiple time series in parallel with rate limiting.

Usage:
    python batch_forecast.py <input.csv> [--horizon 14] [--freq D] [--batch-size 20]

Author: Nixtla Skills Pack
Version: 1.0.0
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd

try:
    from tqdm import tqdm

    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False


def check_api_key() -> str:
    """Verify TimeGPT API key."""
    api_key = os.getenv("NIXTLA_TIMEGPT_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "NIXTLA_TIMEGPT_API_KEY not set. " "Run: export NIXTLA_TIMEGPT_API_KEY=your_key"
        )
    return api_key


def forecast_batch(
    client, batch_df: pd.DataFrame, horizon: int, freq: str, levels: List[int] = [80, 90]
) -> Tuple[pd.DataFrame, List[Dict]]:
    """
    Forecast an entire batch of series at once.

    Returns:
        Tuple of (combined_forecasts, errors)
    """
    errors = []

    try:
        forecasts = client.forecast(df=batch_df, h=horizon, freq=freq, level=levels)
        return (forecasts, errors)

    except Exception as e:
        print(f"Batch failed: {e}")
        # Fall back to individual series
        all_forecasts = []
        for uid in batch_df["unique_id"].unique():
            series_df = batch_df[batch_df["unique_id"] == uid]
            try:
                forecast = client.forecast(df=series_df, h=horizon, freq=freq, level=levels)
                all_forecasts.append(forecast)
            except Exception as series_error:
                errors.append({"unique_id": uid, "error": str(series_error)})

        if all_forecasts:
            return (pd.concat(all_forecasts, ignore_index=True), errors)
        return (pd.DataFrame(), errors)


def run_batch_forecast(
    input_path: str,
    horizon: int = 14,
    freq: str = "D",
    batch_size: int = 20,
    output_dir: str = "forecasts",
    aggregate: bool = False,
    rate_limit_delay: float = 1.0,
) -> Dict:
    """
    Run batch forecasting on multi-series data.

    Args:
        input_path: Path to input CSV
        horizon: Forecast horizon
        freq: Frequency string (D, H, W, M)
        batch_size: Number of series per batch
        output_dir: Directory for output files
        aggregate: Whether to create aggregated forecast
        rate_limit_delay: Seconds between batches

    Returns:
        Dict with results summary
    """
    from prepare_data import analyze_series, load_multi_series_data, split_into_batches

    from nixtla import NixtlaClient

    check_api_key()
    client = NixtlaClient()

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    print("Loading data...")
    df = load_multi_series_data(input_path)
    stats = analyze_series(df)

    print(f"\nForecasting {stats['num_series']} series, horizon={horizon}, freq={freq}")

    batches = split_into_batches(df, batch_size)

    all_forecasts = []
    all_errors = []

    print(f"\nProcessing {len(batches)} batches...")
    iterator = tqdm(batches, desc="Batches") if HAS_TQDM else batches

    for i, batch_df in enumerate(iterator):
        forecasts, errors = forecast_batch(client, batch_df, horizon, freq)

        if not forecasts.empty:
            all_forecasts.append(forecasts)
        all_errors.extend(errors)

        if i < len(batches) - 1:
            time.sleep(rate_limit_delay)

    if not all_forecasts:
        raise RuntimeError("No forecasts generated!")

    combined = pd.concat(all_forecasts, ignore_index=True)

    # Save individual forecasts
    for uid in combined["unique_id"].unique():
        uid_df = combined[combined["unique_id"] == uid]
        uid_safe = uid.replace("/", "_").replace("\\", "_")
        uid_df.to_csv(f"{output_dir}/{uid_safe}_forecast.csv", index=False)

    combined.to_csv(f"{output_dir}/all_forecasts.csv", index=False)

    # Aggregation
    if aggregate and "TimeGPT" in combined.columns:
        print("\nAggregating forecasts...")
        agg_cols = [c for c in combined.columns if c.startswith("TimeGPT")]
        aggregated = combined.groupby("ds")[agg_cols].sum().reset_index()
        aggregated["unique_id"] = "AGGREGATED"
        aggregated.to_csv(f"{output_dir}/aggregated_forecast.csv", index=False)

    summary = {
        "input_file": input_path,
        "total_series": stats["num_series"],
        "series_forecasted": combined["unique_id"].nunique(),
        "horizon": horizon,
        "freq": freq,
        "batch_size": batch_size,
        "num_batches": len(batches),
        "errors": all_errors,
        "error_count": len(all_errors),
        "success_rate": (stats["num_series"] - len(all_errors)) / stats["num_series"] * 100,
        "output_dir": output_dir,
        "aggregated": aggregate,
        "timestamp": datetime.now().isoformat(),
    }

    with open(f"{output_dir}/summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    return summary


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Batch forecast multiple time series")
    parser.add_argument("input", help="Input CSV path")
    parser.add_argument("--horizon", type=int, default=14, help="Forecast horizon")
    parser.add_argument("--freq", default="D", help="Frequency (D, H, W, M)")
    parser.add_argument("--batch-size", type=int, default=20, help="Series per batch")
    parser.add_argument("--output-dir", default="forecasts", help="Output directory")
    parser.add_argument("--aggregate", action="store_true", help="Create aggregated forecast")
    parser.add_argument("--delay", type=float, default=1.0, help="Rate limit delay (seconds)")

    args = parser.parse_args()

    try:
        summary = run_batch_forecast(
            input_path=args.input,
            horizon=args.horizon,
            freq=args.freq,
            batch_size=args.batch_size,
            output_dir=args.output_dir,
            aggregate=args.aggregate,
            rate_limit_delay=args.delay,
        )

        print("\n" + "=" * 50)
        print("BATCH FORECAST COMPLETE")
        print("=" * 50)
        print(f"Series forecasted: {summary['series_forecasted']}/{summary['total_series']}")
        print(f"Success rate: {summary['success_rate']:.1f}%")
        print(f"Errors: {summary['error_count']}")
        print(f"Output: {summary['output_dir']}/")
        return 0

    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
