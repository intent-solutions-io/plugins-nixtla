#!/usr/bin/env python3
"""
StatsForecast Baseline Runner

This script runs classical statistical baseline models (Naive, SeasonalNaive, AutoETS)
on M4-style daily time series data and generates performance metrics.

Design:
- Dataset: M4-style daily series from data/statsforecast_baseline_sample.csv
- Models: Naive, SeasonalNaive (period=7), AutoETS
- Forecast horizon: 14 days
- Metrics: sMAPE (Symmetric MAPE), MAE (Mean Absolute Error)
- Outputs: CSV results + Markdown summary in reports/

Exit codes:
    0: Baseline run successful, reports generated
    1: Environment error (missing dataset, packages, or validation failure)
    2: Model fitting or forecasting error
"""

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


def load_dataset():
    """Load the M4-style baseline sample dataset"""
    dataset_path = DATA_DIR / "statsforecast_baseline_sample.csv"

    if not dataset_path.exists():
        print("=" * 60)
        print("ERROR: Dataset Not Found")
        print("=" * 60)
        print()
        print(f"Expected dataset at: {dataset_path}")
        print()
        print("The baseline runner requires the sample dataset to be present.")
        print("Please ensure data/statsforecast_baseline_sample.csv exists.")
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
        print("See README.md for full setup instructions.")
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
        print("Expected columns: unique_id, ds, y (M4-style format)")
        print("=" * 60)
        return None

    # Ensure ds is datetime
    df["ds"] = pd.to_datetime(df["ds"])

    unique_series = df["unique_id"].nunique()
    total_rows = len(df)
    print(f"✓ Dataset loaded: {unique_series} series, {total_rows} rows")

    return df


def smape(y_true, y_pred):
    """
    Symmetric Mean Absolute Percentage Error

    sMAPE = 100 * mean(|y_true - y_pred| / ((|y_true| + |y_pred|) / 2))

    Notes:
    - Returns percentage (0-200 scale)
    - Handles zero values more gracefully than MAPE
    - Symmetric: treats over/under-prediction equally
    """
    import numpy as np

    numerator = np.abs(y_true - y_pred)
    denominator = (np.abs(y_true) + np.abs(y_pred)) / 2

    # Avoid division by zero
    mask = denominator != 0
    smape_values = np.zeros_like(y_true, dtype=float)
    smape_values[mask] = numerator[mask] / denominator[mask]

    return 100 * np.mean(smape_values)


def mae(y_true, y_pred):
    """
    Mean Absolute Error

    MAE = mean(|y_true - y_pred|)
    """
    import numpy as np

    return np.mean(np.abs(y_true - y_pred))


def run_baseline_models(df, horizon=14):
    """
    Run StatsForecast baseline models and compute metrics

    Args:
        df: DataFrame with columns [unique_id, ds, y]
        horizon: Forecast horizon (days)

    Returns:
        list of dicts with results or None on error
    """
    import numpy as np
    import pandas as pd

    # Import StatsForecast
    try:
        from statsforecast import StatsForecast
        from statsforecast.models import AutoETS, Naive, SeasonalNaive
    except ImportError:
        print("=" * 60)
        print("ERROR: Missing statsforecast Package")
        print("=" * 60)
        print()
        print("The statsforecast package is required but not installed.")
        print()
        print("To fix this:")
        print("  pip install statsforecast")
        print()
        print("See README.md for full setup instructions.")
        print("=" * 60)
        return None

    print()
    print("=" * 60)
    print("Running Baseline Models")
    print("=" * 60)
    print(f"Horizon: {horizon} days")
    print(f"Models: Naive, SeasonalNaive(7), AutoETS")
    print()

    results = []

    # Process each series
    for series_id in df["unique_id"].unique():
        series_df = df[df["unique_id"] == series_id].copy()
        series_df = series_df.sort_values("ds").reset_index(drop=True)

        total_points = len(series_df)

        # Validate enough data (need > horizon for train/test split)
        if total_points <= horizon:
            print(
                f"  WARNING: {series_id} has only {total_points} points, need >{horizon}. Skipping."
            )
            continue

        # Split train/test (last 'horizon' points for evaluation)
        train_df = series_df.iloc[:-horizon].copy()
        test_df = series_df.iloc[-horizon:].copy()

        print(f"  Series {series_id}: {len(train_df)} train, {len(test_df)} test")

        # StatsForecast requires specific column names
        train_df = train_df.rename(columns={"unique_id": "unique_id", "ds": "ds", "y": "y"})

        # Initialize models
        models = [
            Naive(),
            SeasonalNaive(season_length=7),  # Weekly seasonality for daily data
            AutoETS(season_length=7),
        ]

        try:
            # Fit and forecast with StatsForecast
            sf = StatsForecast(models=models, freq="D", n_jobs=1)  # Daily frequency

            # Fit models and generate forecasts
            forecasts_df = sf.forecast(df=train_df, h=horizon)

            # Compute metrics for each model
            y_true = test_df["y"].values

            for model in models:
                model_name = model.__class__.__name__

                # Extract forecast column (StatsForecast uses model class name)
                if model_name in forecasts_df.columns:
                    y_pred = forecasts_df[model_name].values
                else:
                    print(f"    WARNING: {model_name} forecast not found in results. Skipping.")
                    continue

                # Compute metrics
                smape_val = smape(y_true, y_pred)
                mae_val = mae(y_true, y_pred)

                print(f"    {model_name}: sMAPE={smape_val:.2f}%, MAE={mae_val:.4f}")

                results.append(
                    {
                        "unique_id": series_id,
                        "model": model_name,
                        "horizon": horizon,
                        "smape": smape_val,
                        "mae": mae_val,
                    }
                )

        except Exception as e:
            print("=" * 60)
            print("ERROR: Model Fitting/Forecasting Failed")
            print("=" * 60)
            print()
            print(f"Error for series {series_id}: {e}")
            print()
            print("This may indicate:")
            print("  - Incompatible data format")
            print("  - Insufficient data for model fitting")
            print("  - StatsForecast version mismatch")
            print("=" * 60)
            return None

    print()
    print(f"✓ Baseline models completed: {len(results)} total results")

    return results


def write_csv_report(results):
    """Write detailed CSV report with per-series, per-model metrics"""
    import pandas as pd

    csv_path = REPORTS_DIR / "statsforecast_baseline_results.csv"

    if not results:
        print(f"  No results to write to CSV")
        return False

    df = pd.DataFrame(results)
    df.to_csv(csv_path, index=False)

    print(f"✓ CSV report: {csv_path.relative_to(LAB_ROOT)}")
    return True


def write_markdown_summary(results, df_original):
    """Write human-readable Markdown summary"""
    from datetime import datetime

    import pandas as pd

    md_path = REPORTS_DIR / "statsforecast_baseline_summary.md"

    if not results:
        print(f"  No results to write to Markdown")
        return False

    df_results = pd.DataFrame(results)

    # Build markdown content
    lines = []
    lines.append("# StatsForecast Baseline Results")
    lines.append("")
    lines.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Dataset**: data/statsforecast_baseline_sample.csv")
    lines.append("")

    # Executive summary
    lines.append("## Executive Summary")
    lines.append("")
    unique_series = df_results["unique_id"].nunique()
    unique_models = df_results["model"].nunique()
    horizon = df_results["horizon"].iloc[0] if len(df_results) > 0 else "N/A"

    lines.append(
        f"Evaluated {unique_models} classical baseline models (Naive, SeasonalNaive, AutoETS) on {unique_series} daily time series. Forecast horizon: {horizon} days. Metrics computed: sMAPE (Symmetric MAPE) and MAE (Mean Absolute Error)."
    )
    lines.append("")

    # Dataset info
    lines.append("## Dataset")
    lines.append("")
    lines.append(f"- **Series**: {df_original['unique_id'].nunique()}")
    lines.append(f"- **Length**: {len(df_original)} total rows")
    lines.append(
        f"- **Date range**: {df_original['ds'].min().strftime('%Y-%m-%d')} to {df_original['ds'].max().strftime('%Y-%m-%d')}"
    )
    lines.append(f"- **Forecast horizon**: {horizon} days")
    lines.append("")

    # Results by model
    lines.append("## Results by Model")
    lines.append("")

    for model in df_results["model"].unique():
        model_results = df_results[df_results["model"] == model]

        lines.append(f"### {model}")
        lines.append("")

        # Per-series metrics table
        lines.append("| Series | sMAPE | MAE |")
        lines.append("|--------|-------|-----|")
        for _, row in model_results.iterrows():
            lines.append(f"| {row['unique_id']} | {row['smape']:.2f}% | {row['mae']:.4f} |")
        lines.append("")

        # Aggregate metrics
        avg_smape = model_results["smape"].mean()
        avg_mae = model_results["mae"].mean()

        lines.append(f"**Average Metrics**:")
        lines.append(f"- sMAPE: {avg_smape:.2f}%")
        lines.append(f"- MAE: {avg_mae:.4f}")
        lines.append("")

    # Comparative analysis
    if unique_models > 1:
        lines.append("## Comparative Analysis")
        lines.append("")

        # Group by model and compute averages
        model_summary = (
            df_results.groupby("model").agg({"smape": "mean", "mae": "mean"}).reset_index()
        )

        lines.append("| Model | Avg sMAPE | Avg MAE |")
        lines.append("|-------|-----------|---------|")
        for _, row in model_summary.iterrows():
            lines.append(f"| {row['model']} | {row['smape']:.2f}% | {row['mae']:.4f} |")
        lines.append("")

        # Best model
        best_smape_model = model_summary.loc[model_summary["smape"].idxmin(), "model"]
        best_mae_model = model_summary.loc[model_summary["mae"].idxmin(), "model"]

        lines.append("**Best Models**:")
        lines.append(f"- Lowest sMAPE: `{best_smape_model}`")
        lines.append(f"- Lowest MAE: `{best_mae_model}`")
        lines.append("")

    # Footer
    lines.append("---")
    lines.append("")
    lines.append("**Lab**: 002-workspaces/statsforecast-lab/")
    lines.append("**Phase**: 07 - StatsForecast Lab Bootstrap (M4 Daily)")

    # Write markdown
    md_content = "\n".join(lines)
    with open(md_path, "w") as f:
        f.write(md_content)

    print(f"✓ Markdown summary: {md_path.relative_to(LAB_ROOT)}")
    return True


def main():
    """Main baseline runner workflow"""
    print("=" * 60)
    print("StatsForecast Baseline Runner")
    print("=" * 60)
    print()

    # Step 1: Load dataset
    print("Step 1: Loading dataset...")
    df = load_dataset()
    if df is None:
        return 1
    print()

    # Step 2: Run baseline models
    print("Step 2: Running baseline models...")
    results = run_baseline_models(df, horizon=14)
    if results is None:
        return 2
    print()

    # Step 3: Generate reports
    print("Step 3: Generating reports...")
    csv_ok = write_csv_report(results)
    md_ok = write_markdown_summary(results, df)

    if not (csv_ok and md_ok):
        print()
        print("Failed to generate one or more reports.")
        return 1

    print()

    # Success summary
    print("=" * 60)
    print("✓ StatsForecast Baseline Run: COMPLETE")
    print("=" * 60)
    print()
    print("Summary:")
    print(f"  Models: Naive, SeasonalNaive, AutoETS")
    print(f"  Series: {df['unique_id'].nunique()}")
    print(f"  Horizon: 14 days")
    print(f"  Total results: {len(results)}")
    print()
    print("Reports:")
    print(f"  - reports/statsforecast_baseline_results.csv")
    print(f"  - reports/statsforecast_baseline_summary.md")
    print()
    print("Next steps:")
    print("  - Review metrics in reports/")
    print("  - Compare with TimeGPT lab results")
    print("  - Design baseline vs TimeGPT comparison experiments")
    print()
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
