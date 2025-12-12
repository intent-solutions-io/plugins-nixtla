#!/usr/bin/env python3
"""
TimeGPT API Smoke Test

This script performs a minimal, controlled TimeGPT forecast to validate the lab environment.

Design decisions:
- Dataset: 2 time series (series_1, series_2) with 90 daily timestamps each
- Forecast horizon: 14 days (2 weeks)
- API calls: Exactly ONE forecast call with the full dataset
- Output: Forecast results saved to reports/timegpt_smoke_forecast.csv
- Cost control: Tiny dataset, single call, daily frequency

Modes:
    --dry-run: Exercises all code paths without API calls. Uses synthetic forecasts
               (last observed value). No API key required. Safe for CI/CD.
    (default): Makes real TimeGPT API call. Requires NIXTLA_TIMEGPT_API_KEY.

Exit codes:
    0: Smoke test successful, forecast saved
    1: Environment error (missing API key, packages, or dataset)
    2: TimeGPT API error (network, authentication, or validation) - real mode only
"""

import argparse
import os
import sys
from pathlib import Path

# Robust path handling
SCRIPT_DIR = Path(__file__).resolve().parent
LAB_ROOT = SCRIPT_DIR.parent
DATA_DIR = LAB_ROOT / "data"
REPORTS_DIR = LAB_ROOT / "reports"

# Ensure reports directory exists
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def validate_environment():
    """Validate environment before attempting API call"""
    api_key = os.getenv("NIXTLA_TIMEGPT_API_KEY")

    if not api_key:
        print("=" * 60)
        print("ERROR: Missing API Key")
        print("=" * 60)
        print()
        print("The NIXTLA_TIMEGPT_API_KEY environment variable is not set.")
        print()
        print("To fix this:")
        print("  1. Obtain your API key from https://dashboard.nixtla.io/")
        print("  2. Set the environment variable:")
        print("     export NIXTLA_TIMEGPT_API_KEY='your_key_here'")
        print()
        print("  Or create a .env file in the lab root:")
        print("     NIXTLA_TIMEGPT_API_KEY=your_key_here")
        print()
        print("See docs/timegpt-env-setup.md for detailed instructions.")
        print("=" * 60)
        return None

    # Mask API key when displaying (show only first 4 chars)
    masked_key = api_key[:4] + "..." if len(api_key) > 4 else "***"
    print(f"✓ API key present ({masked_key})")

    return api_key


def load_dataset():
    """Load the smoke test sample dataset"""
    dataset_path = DATA_DIR / "timegpt_smoke_sample.csv"

    if not dataset_path.exists():
        print("=" * 60)
        print("ERROR: Dataset Not Found")
        print("=" * 60)
        print()
        print(f"Expected dataset at: {dataset_path}")
        print()
        print("The smoke test requires the sample dataset to be present.")
        print("Please ensure the file exists and try again.")
        print("=" * 60)
        return None

    try:
        import pandas as pd
    except ImportError:
        print("=" * 60)
        print("ERROR: Missing pandas Package")
        print("=" * 60)
        print()
        print("The pandas package is required but not installed.")
        print()
        print("To fix this:")
        print("  pip install pandas")
        print()
        print("See docs/timegpt-env-setup.md for full setup instructions.")
        print("=" * 60)
        return None

    try:
        df = pd.read_csv(dataset_path)
    except Exception as e:
        print("=" * 60)
        print("ERROR: Failed to Load Dataset")
        print("=" * 60)
        print()
        print(f"Could not read {dataset_path}")
        print(f"Error: {e}")
        print("=" * 60)
        return None

    # Validate required columns
    required_cols = {"unique_id", "ds", "y"}
    if not required_cols.issubset(df.columns):
        missing = required_cols - set(df.columns)
        print("=" * 60)
        print("ERROR: Invalid Dataset Schema")
        print("=" * 60)
        print()
        print(f"Dataset is missing required columns: {missing}")
        print(f"Found columns: {list(df.columns)}")
        print()
        print("Expected columns: unique_id, ds, y")
        print("=" * 60)
        return None

    unique_series = df["unique_id"].nunique()
    total_rows = len(df)
    print(f"✓ Dataset loaded: {unique_series} series, {total_rows} rows")

    return df


def call_timegpt(df, api_key):
    """Make a single TimeGPT forecast call"""

    try:
        from nixtla import NixtlaClient
    except ImportError:
        print("=" * 60)
        print("ERROR: Missing nixtla Package")
        print("=" * 60)
        print()
        print("The nixtla package is required but not installed.")
        print()
        print("To fix this:")
        print("  pip install nixtla>=0.5.0")
        print()
        print("See docs/timegpt-env-setup.md for full setup instructions.")
        print("=" * 60)
        return None

    try:
        # Initialize TimeGPT client
        client = NixtlaClient(api_key=api_key)

        # Make forecast call (horizon: 14 days)
        print("Calling TimeGPT API (horizon=14)...")
        forecast_df = client.forecast(df=df, h=14, freq="D", time_col="ds", target_col="y")

        print("✓ TimeGPT API call successful")
        return forecast_df

    except Exception as e:
        error_msg = str(e)
        print("=" * 60)
        print("ERROR: TimeGPT API Call Failed")
        print("=" * 60)
        print()
        print(f"Error: {error_msg}")
        print()

        # Provide context-specific guidance
        if "401" in error_msg or "authentication" in error_msg.lower():
            print("This appears to be an authentication error.")
            print("Please verify your API key is valid:")
            print("  1. Check https://dashboard.nixtla.io/")
            print("  2. Ensure NIXTLA_TIMEGPT_API_KEY is set correctly")
        elif "network" in error_msg.lower() or "connection" in error_msg.lower():
            print("This appears to be a network connectivity error.")
            print("Please check your internet connection and try again.")
        elif "validation" in error_msg.lower() or "schema" in error_msg.lower():
            print("This appears to be a data validation error.")
            print("The dataset may not match TimeGPT's expected format.")

        print("=" * 60)
        return None


def generate_synthetic_forecast(df):
    """Generate a synthetic forecast for dry-run mode (no API call)

    Strategy: Repeat the last observed value for each series.
    This exercises the same code paths (data loading, saving, reporting)
    without making real API calls.
    """
    try:
        import pandas as pd
    except ImportError:
        # Already checked in load_dataset, but be defensive
        print("ERROR: pandas not available")
        return None

    # Get the last observed value for each series
    last_values = df.groupby("unique_id").tail(1)[["unique_id", "y"]].copy()

    # Create 14 forecast rows per series (matching real horizon)
    forecasts = []
    for _, row in last_values.iterrows():
        unique_id = row["unique_id"]
        last_y = row["y"]

        # Get the last timestamp for this series
        series_df = df[df["unique_id"] == unique_id]
        last_ds = pd.to_datetime(series_df["ds"].iloc[-1])

        # Generate 14 future dates
        future_dates = pd.date_range(start=last_ds + pd.Timedelta(days=1), periods=14, freq="D")

        for ds in future_dates:
            forecasts.append(
                {
                    "unique_id": unique_id,
                    "ds": ds,
                    "TimeGPT": last_y,  # Naive forecast: repeat last value
                }
            )

    forecast_df = pd.DataFrame(forecasts)
    print("✓ Synthetic forecast generated (last-value baseline)")
    return forecast_df


def save_forecast(forecast_df):
    """Save forecast results to CSV"""
    output_path = REPORTS_DIR / "timegpt_smoke_forecast.csv"

    try:
        forecast_df.to_csv(output_path, index=False)
        print(f"✓ Forecast saved to: {output_path.relative_to(LAB_ROOT)}")
        return True
    except Exception as e:
        print("=" * 60)
        print("ERROR: Failed to Save Forecast")
        print("=" * 60)
        print()
        print(f"Could not write to {output_path}")
        print(f"Error: {e}")
        print("=" * 60)
        return False


def main():
    """Main smoke test workflow"""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="TimeGPT API smoke test with optional dry-run mode"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Run in dry-run mode (no API calls, synthetic forecasts)",
    )
    args = parser.parse_args()

    # Display mode clearly
    mode = "DRY RUN" if args.dry_run else "REAL"
    print("=" * 60)
    print(f"TimeGPT Smoke Test - {mode} MODE")
    print("=" * 60)
    print()

    if args.dry_run:
        print("⚠️  DRY-RUN MODE: No API calls will be made.")
        print("    Synthetic forecasts will be generated for testing.")
        print()

    # Step 1: Validate environment (skip API key check in dry-run mode)
    if args.dry_run:
        print("Step 1: Validating environment (dry-run mode)...")
        print("✓ Skipping API key validation (dry-run mode)")
        api_key = None
    else:
        print("Step 1: Validating environment...")
        api_key = validate_environment()
        if api_key is None:
            return 1
    print()

    # Step 2: Load dataset (same for both modes)
    print("Step 2: Loading dataset...")
    df = load_dataset()
    if df is None:
        return 1
    print()

    # Step 3: Generate forecast (real or synthetic)
    if args.dry_run:
        print("Step 3: Generating synthetic forecast...")
        forecast_df = generate_synthetic_forecast(df)
        if forecast_df is None:
            return 1
    else:
        print("Step 3: Calling TimeGPT API...")
        forecast_df = call_timegpt(df, api_key)
        if forecast_df is None:
            return 2
    print()

    # Step 4: Save results (same for both modes)
    print("Step 4: Saving forecast results...")
    if not save_forecast(forecast_df):
        return 1
    print()

    # Success summary
    print("=" * 60)
    print(f"✓ TimeGPT Smoke Test ({mode}): PASSED")
    print("=" * 60)
    print()
    print("Summary:")
    print(f"  Mode: {mode}")
    print(f"  Input series: {df['unique_id'].nunique()}")
    print(f"  Forecast horizon: 14 days")
    print(f"  Output: reports/timegpt_smoke_forecast.csv")
    if args.dry_run:
        print(f"  Forecast method: Last-value baseline (synthetic)")
    else:
        print(f"  Forecast method: TimeGPT API")
    print()

    if not args.dry_run:
        print("Next steps:")
        print("  - Review the forecast results in reports/")
        print("  - Explore TimeGPT features in the lab")
        print("  - See docs/timegpt-env-setup.md for guidance")
        print()

    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
