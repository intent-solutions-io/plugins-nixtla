#!/usr/bin/env python3
"""
Run Nixtla Forecasts

Generates time series forecasts using StatsForecast baseline models
and optionally TimeGPT if NIXTLA_API_KEY is configured.

Usage:
    python run_forecast.py --data data.csv --horizon 14 --freq D
    python run_forecast.py --data data.csv --horizon 24 --freq H --output forecasts.csv
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional

try:
    import pandas as pd
except ImportError:
    print("Error: pandas not installed. Run: pip install pandas")
    sys.exit(1)


def check_dependencies() -> dict:
    """Check which forecasting libraries are available."""
    available = {}

    try:
        import statsforecast

        available["statsforecast"] = True
    except ImportError:
        available["statsforecast"] = False

    try:
        import nixtla

        available["nixtla"] = True
    except ImportError:
        available["nixtla"] = False

    return available


def validate_data(df: pd.DataFrame) -> None:
    """Validate that dataframe follows Nixtla schema."""
    required_cols = ["unique_id", "ds", "y"]
    missing = [c for c in required_cols if c not in df.columns]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}. " f"Nixtla schema requires: unique_id, ds, y"
        )

    # Convert ds to datetime if needed
    if not pd.api.types.is_datetime64_any_dtype(df["ds"]):
        df["ds"] = pd.to_datetime(df["ds"])


def run_statsforecast(df: pd.DataFrame, horizon: int, freq: str) -> pd.DataFrame:
    """Run StatsForecast baseline models."""
    from statsforecast import StatsForecast
    from statsforecast.models import AutoETS, SeasonalNaive

    # Determine seasonal period based on frequency
    season_map = {"D": 7, "W": 52, "M": 12, "H": 24, "Q": 4}
    season_length = season_map.get(freq, 1)

    models = [
        SeasonalNaive(season_length=season_length),
        AutoETS(season_length=season_length),
    ]

    # Try to add AutoARIMA if available (slower but more accurate)
    try:
        from statsforecast.models import AutoARIMA

        models.append(AutoARIMA(season_length=season_length))
    except ImportError:
        pass

    sf = StatsForecast(models=models, freq=freq, n_jobs=-1)
    forecasts = sf.forecast(df=df, h=horizon, level=[80, 90])

    return forecasts.reset_index()


def run_timegpt(df: pd.DataFrame, horizon: int, freq: str) -> Optional[pd.DataFrame]:
    """Run TimeGPT if API key is configured."""
    api_key = os.environ.get("NIXTLA_API_KEY")

    if not api_key:
        print("Note: NIXTLA_API_KEY not set, skipping TimeGPT")
        return None

    try:
        from nixtla import NixtlaClient

        client = NixtlaClient(api_key=api_key)
        forecasts = client.forecast(df=df, h=horizon, freq=freq, level=[80, 90])

        return forecasts
    except Exception as e:
        print(f"Warning: TimeGPT forecast failed: {e}")
        return None


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate time series forecasts using Nixtla libraries",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --data sales.csv --horizon 14 --freq D
  %(prog)s --data hourly.csv --horizon 24 --freq H --output predictions.csv

Input CSV must have columns: unique_id, ds, y
        """,
    )

    parser.add_argument("--data", "-d", required=True, help="Input CSV file with time series data")
    parser.add_argument(
        "--horizon", "-h", type=int, required=True, help="Forecast horizon (number of periods)"
    )
    parser.add_argument(
        "--freq",
        "-f",
        required=True,
        help="Frequency string (D=daily, H=hourly, W=weekly, M=monthly)",
    )
    parser.add_argument(
        "--output", "-o", default="forecasts.csv", help="Output CSV file (default: forecasts.csv)"
    )

    args = parser.parse_args()

    # Check dependencies
    deps = check_dependencies()
    if not deps["statsforecast"]:
        print("Error: statsforecast not installed. Run: pip install statsforecast")
        return 1

    # Load data
    data_path = Path(args.data)
    if not data_path.exists():
        print(f"Error: File not found: {data_path}")
        return 1

    print(f"Loading data from {data_path}...")
    df = pd.read_csv(data_path)

    try:
        validate_data(df)
    except ValueError as e:
        print(f"Error: {e}")
        return 1

    print(f"Data shape: {df.shape}")
    print(f"Series count: {df['unique_id'].nunique()}")
    print(f"Forecast horizon: {args.horizon} periods")
    print(f"Frequency: {args.freq}")
    print()

    # Run StatsForecast
    print("Running StatsForecast baseline models...")
    sf_forecasts = run_statsforecast(df, args.horizon, args.freq)
    print(f"  Generated {len(sf_forecasts)} forecast rows")

    # Optionally run TimeGPT
    if deps["nixtla"]:
        print("Running TimeGPT...")
        tgpt_forecasts = run_timegpt(df, args.horizon, args.freq)

        if tgpt_forecasts is not None:
            # Merge TimeGPT results
            sf_forecasts = sf_forecasts.merge(
                tgpt_forecasts[["unique_id", "ds", "TimeGPT"]], on=["unique_id", "ds"], how="left"
            )
            print(f"  Added TimeGPT column")

    # Save results
    output_path = Path(args.output)
    sf_forecasts.to_csv(output_path, index=False)
    print(f"\nForecasts saved to: {output_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
