#!/usr/bin/env python3
"""
ERCOT Grid Forecasting Prototype
================================
Pulls ERCOT load data, runs TimeGPT + statsforecast baselines,
and generates forecast visualization.

Part of: 121-AA-REPT Energy Grid Forecasting Opportunity Research
"""

import warnings
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# ============================================================================
# 1. DATA LOADING
# ============================================================================


def load_ercot_data():
    """Load clean ERCOT dataset from Nixtla's S3 bucket."""
    print("Loading ERCOT data from Nixtla S3...")
    url = "https://datasets-nixtla.s3.amazonaws.com/ERCOT-clean.csv"
    df = pd.read_csv(url, parse_dates=["ds"])
    print(f"  Loaded {len(df):,} rows")
    print(f"  Date range: {df['ds'].min()} to {df['ds'].max()}")
    print(f"  Unique series: {df['unique_id'].nunique()}")
    return df


def prepare_train_test(df, horizon=48):
    """Split data into train/test sets."""
    # Use last `horizon` hours as test set
    cutoff = df["ds"].max() - timedelta(hours=horizon)
    train = df[df["ds"] <= cutoff].copy()
    test = df[df["ds"] > cutoff].copy()
    print(f"\nTrain/Test Split:")
    print(f"  Train: {len(train):,} rows (up to {cutoff})")
    print(f"  Test:  {len(test):,} rows ({horizon}h holdout)")
    return train, test


# ============================================================================
# 2. STATSFORECAST BASELINES
# ============================================================================


def run_statsforecast_baselines(train_df, horizon=48):
    """Run statsforecast models (no API key needed)."""
    from statsforecast import StatsForecast
    from statsforecast.models import (
        MSTL,
        AutoARIMA,
        AutoETS,
        SeasonalNaive,
    )

    print("\nRunning statsforecast baselines...")

    # MSTL with multiple seasonalities (hourly + daily)
    # 24 = hourly seasonality, 24*7 = weekly seasonality
    models = [
        SeasonalNaive(season_length=24),  # Simple baseline
        MSTL(season_length=[24, 24 * 7], trend_forecaster=AutoARIMA()),
        AutoETS(season_length=24),
    ]

    sf = StatsForecast(
        models=models,
        freq="H",
        n_jobs=-1,  # Use all cores
    )

    # Fit and predict
    forecasts = sf.forecast(df=train_df, h=horizon)
    forecasts = forecasts.reset_index()

    print(f"  Generated {len(forecasts):,} forecast rows")
    print(f"  Models: {[m.__class__.__name__ for m in models]}")

    return forecasts


# ============================================================================
# 3. TIMEGPT FORECAST (requires API key)
# ============================================================================


def run_timegpt_forecast(train_df, horizon=48):
    """Run TimeGPT forecast (requires NIXTLA_TIMEGPT_API_KEY)."""
    import os

    api_key = os.getenv("NIXTLA_TIMEGPT_API_KEY")
    if not api_key:
        print("\nTimeGPT: Skipped (NIXTLA_TIMEGPT_API_KEY not set)")
        return None

    from nixtla import NixtlaClient

    print("\nRunning TimeGPT forecast...")
    client = NixtlaClient(api_key=api_key)

    # Use long-horizon model for 48h forecast
    forecasts = client.forecast(
        df=train_df,
        h=horizon,
        freq="H",
        model="timegpt-1-long-horizon",
        level=[90],  # 90% confidence interval
    )

    print(f"  Generated {len(forecasts):,} forecast rows")
    return forecasts


# ============================================================================
# 4. EVALUATION
# ============================================================================


def evaluate_forecasts(test_df, sf_forecasts, tgpt_forecasts=None):
    """Calculate error metrics for all models."""
    from sklearn.metrics import mean_absolute_error, mean_squared_error

    print("\n" + "=" * 60)
    print("FORECAST EVALUATION")
    print("=" * 60)

    results = []

    # Merge test with statsforecast predictions
    merged = test_df.merge(sf_forecasts, on=["unique_id", "ds"], how="inner")

    for model_col in ["SeasonalNaive", "MSTL", "AutoETS"]:
        if model_col in merged.columns:
            mae = mean_absolute_error(merged["y"], merged[model_col])
            rmse = np.sqrt(mean_squared_error(merged["y"], merged[model_col]))
            mape = np.mean(np.abs((merged["y"] - merged[model_col]) / merged["y"])) * 100
            results.append({"Model": model_col, "MAE": mae, "RMSE": rmse, "MAPE": f"{mape:.2f}%"})

    # TimeGPT evaluation
    if tgpt_forecasts is not None:
        tgpt_merged = test_df.merge(tgpt_forecasts, on=["unique_id", "ds"], how="inner")
        if "TimeGPT" in tgpt_merged.columns:
            mae = mean_absolute_error(tgpt_merged["y"], tgpt_merged["TimeGPT"])
            rmse = np.sqrt(mean_squared_error(tgpt_merged["y"], tgpt_merged["TimeGPT"]))
            mape = (
                np.mean(np.abs((tgpt_merged["y"] - tgpt_merged["TimeGPT"]) / tgpt_merged["y"]))
                * 100
            )
            results.append({"Model": "TimeGPT", "MAE": mae, "RMSE": rmse, "MAPE": f"{mape:.2f}%"})

    results_df = pd.DataFrame(results)
    print(results_df.to_string(index=False))

    return results_df


# ============================================================================
# 5. VISUALIZATION
# ============================================================================


def plot_forecasts(
    train_df, test_df, sf_forecasts, tgpt_forecasts=None, series_id=None, output_path=None
):
    """Generate forecast visualization."""
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt

    # Pick first series if not specified
    if series_id is None:
        series_id = train_df["unique_id"].iloc[0]

    print(f"\nPlotting forecasts for series: {series_id}")

    # Filter to single series
    train_s = train_df[train_df["unique_id"] == series_id].tail(24 * 7)  # Last week
    test_s = test_df[test_df["unique_id"] == series_id]
    sf_s = sf_forecasts[sf_forecasts["unique_id"] == series_id]

    fig, ax = plt.subplots(figsize=(14, 6))

    # Historical
    ax.plot(train_s["ds"], train_s["y"], "b-", label="Historical", linewidth=1.5)

    # Actual (test)
    ax.plot(test_s["ds"], test_s["y"], "k-", label="Actual", linewidth=2)

    # Statsforecast models
    colors = {"SeasonalNaive": "gray", "MSTL": "green", "AutoETS": "orange"}
    for model, color in colors.items():
        if model in sf_s.columns:
            ax.plot(
                sf_s["ds"], sf_s[model], "--", color=color, label=model, linewidth=1.5, alpha=0.8
            )

    # TimeGPT
    if tgpt_forecasts is not None:
        tgpt_s = tgpt_forecasts[tgpt_forecasts["unique_id"] == series_id]
        if len(tgpt_s) > 0:
            ax.plot(tgpt_s["ds"], tgpt_s["TimeGPT"], "r-", label="TimeGPT", linewidth=2)
            # Confidence interval
            if "TimeGPT-lo-90" in tgpt_s.columns:
                ax.fill_between(
                    tgpt_s["ds"],
                    tgpt_s["TimeGPT-lo-90"],
                    tgpt_s["TimeGPT-hi-90"],
                    color="red",
                    alpha=0.2,
                    label="90% CI",
                )

    # Formatting
    ax.set_xlabel("Date")
    ax.set_ylabel("Load (MW)")
    ax.set_title(f"ERCOT Load Forecast - {series_id}\n48-Hour Horizon")
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M"))
    plt.xticks(rotation=45)
    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        print(f"  Saved to {output_path}")

    plt.show()
    return fig


# ============================================================================
# 6. MAIN
# ============================================================================


def main():
    """Run the complete prototype pipeline."""
    print("=" * 60)
    print("ERCOT GRID FORECASTING PROTOTYPE")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}")

    # Load data
    df = load_ercot_data()

    # Prepare train/test
    horizon = 48  # 48-hour forecast
    train_df, test_df = prepare_train_test(df, horizon=horizon)

    # Run statsforecast (always works - no API key)
    sf_forecasts = run_statsforecast_baselines(train_df, horizon=horizon)

    # Run TimeGPT (optional - needs API key)
    tgpt_forecasts = run_timegpt_forecast(train_df, horizon=horizon)

    # Evaluate
    results = evaluate_forecasts(test_df, sf_forecasts, tgpt_forecasts)

    # Save results
    output_dir = "."
    sf_forecasts.to_csv(f"{output_dir}/sf_forecasts.csv", index=False)
    results.to_csv(f"{output_dir}/evaluation_results.csv", index=False)

    # Plot
    plot_forecasts(
        train_df,
        test_df,
        sf_forecasts,
        tgpt_forecasts,
        output_path=f"{output_dir}/forecast_plot.png",
    )

    print("\n" + "=" * 60)
    print("PROTOTYPE COMPLETE")
    print("=" * 60)
    print(f"Outputs saved to {output_dir}/")
    print("  - sf_forecasts.csv")
    print("  - evaluation_results.csv")
    print("  - forecast_plot.png")

    return df, sf_forecasts, tgpt_forecasts, results


if __name__ == "__main__":
    df, sf_forecasts, tgpt_forecasts, results = main()
