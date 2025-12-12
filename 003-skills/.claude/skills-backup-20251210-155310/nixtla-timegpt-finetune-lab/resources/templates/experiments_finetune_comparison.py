#!/usr/bin/env python3
"""
TimeGPT Fine-Tuning Comparison Experiments

Compare performance of:
- TimeGPT zero-shot (baseline)
- TimeGPT fine-tuned (custom model)
- StatsForecast baselines (AutoETS, AutoARIMA, etc.)
"""

import os
from pathlib import Path

import pandas as pd
import yaml
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA, AutoETS, AutoTheta
from utilsforecast.evaluation import evaluate
from utilsforecast.losses import mae, mase, smape

from nixtla import NixtlaClient


def load_finetuned_model_id():
    """Load fine-tuned model ID from artifacts"""
    model_id_file = Path("forecasting/artifacts/timegpt_finetune/finetune_model_id.txt")

    if not model_id_file.exists():
        print("WARNING: No fine-tuned model ID found")
        print("Run timegpt_finetune_job.py first")
        return None

    return model_id_file.read_text().strip()


def run_timegpt_zeroshot(client, df, horizon, freq):
    """Run TimeGPT zero-shot forecast"""
    print("Running TimeGPT zero-shot...")
    forecast = client.forecast(df=df, h=horizon, freq=freq)
    return forecast


def run_timegpt_finetuned(client, df, horizon, freq, finetune_id):
    """Run TimeGPT fine-tuned forecast"""
    if not finetune_id:
        print("Skipping fine-tuned forecast (no model ID)")
        return None

    print(f"Running TimeGPT fine-tuned (model: {finetune_id})...")
    forecast = client.forecast(df=df, h=horizon, freq=freq, finetune_id=finetune_id)
    return forecast


def run_statsforecast_baselines(df, horizon, freq):
    """Run StatsForecast baseline models"""
    print("Running StatsForecast baselines...")

    models = [
        AutoETS(season_length=7 if freq == "D" else 1),
        AutoARIMA(season_length=7 if freq == "D" else 1),
        AutoTheta(season_length=7 if freq == "D" else 1),
    ]

    sf = StatsForecast(models=models, freq=freq, n_jobs=-1)
    forecasts = sf.forecast(df=df, h=horizon)

    return forecasts


def calculate_metrics(y_true, y_pred, y_train=None):
    """Calculate evaluation metrics"""
    metrics = {"mae": mae(y_true, y_pred), "smape": smape(y_true, y_pred)}

    if y_train is not None:
        metrics["mase"] = mase(y_true, y_pred, y_train)

    return metrics


def compare_models(test_df, forecasts_dict):
    """
    Compare multiple model forecasts

    Args:
        test_df: Test data with actual values (unique_id, ds, y)
        forecasts_dict: Dictionary of {model_name: forecast_df}

    Returns:
        pd.DataFrame: Comparison results
    """
    results = []

    for model_name, forecast_df in forecasts_dict.items():
        if forecast_df is None:
            continue

        # Merge forecast with actual values
        merged = test_df.merge(forecast_df, on=["unique_id", "ds"], how="inner")

        # Calculate metrics per series
        for unique_id in merged["unique_id"].unique():
            series_data = merged[merged["unique_id"] == unique_id]
            y_true = series_data["y"].values

            # Handle different forecast column names
            if "TimeGPT" in forecast_df.columns:
                y_pred = series_data["TimeGPT"].values
            elif model_name in forecast_df.columns:
                y_pred = series_data[model_name].values
            else:
                continue

            metrics = calculate_metrics(y_true, y_pred)

            results.append({"model": model_name, "unique_id": unique_id, **metrics})

    return pd.DataFrame(results)


def main():
    """Run comparison experiments"""
    # Load config
    with open("forecasting/config.yml", "r") as f:
        config = yaml.safe_load(f)

    fine_tune_config = config["fine_tune"]

    # Initialize TimeGPT client
    api_key = os.getenv("NIXTLA_API_KEY")
    if not api_key:
        print("ERROR: NIXTLA_API_KEY not set")
        exit(1)

    client = NixtlaClient(api_key=api_key)

    # Load data
    train_df = pd.read_csv(fine_tune_config["data"]["train_path"])
    test_df = pd.read_csv(fine_tune_config["data"]["val_path"])

    horizon = fine_tune_config["parameters"]["horizon"]
    freq = fine_tune_config["parameters"]["freq"]

    # Load fine-tuned model ID
    finetune_id = load_finetuned_model_id()

    # Run all forecasts
    forecasts = {}

    # TimeGPT zero-shot
    forecasts["TimeGPT Zero-Shot"] = run_timegpt_zeroshot(client, train_df, horizon, freq)

    # TimeGPT fine-tuned
    if finetune_id:
        forecasts["TimeGPT Fine-Tuned"] = run_timegpt_finetuned(
            client, train_df, horizon, freq, finetune_id
        )

    # StatsForecast baselines
    sf_forecasts = run_statsforecast_baselines(train_df, horizon, freq)
    forecasts["AutoETS"] = sf_forecasts[["unique_id", "ds", "AutoETS"]].rename(
        columns={"AutoETS": "TimeGPT"}  # Normalize column name
    )
    forecasts["AutoARIMA"] = sf_forecasts[["unique_id", "ds", "AutoARIMA"]].rename(
        columns={"AutoARIMA": "TimeGPT"}
    )

    # Compare models
    results = compare_models(test_df, forecasts)

    # Aggregate results
    summary = (
        results.groupby("model").agg({"mae": "mean", "smape": "mean", "mase": "mean"}).round(4)
    )

    print("\n" + "=" * 60)
    print("COMPARISON RESULTS")
    print("=" * 60)
    print(summary.to_string())

    # Save results
    output_dir = Path(config["comparison"]["output"]["results_path"]).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    results_file = config["comparison"]["output"]["results_path"]
    results.to_csv(results_file, index=False)
    print(f"\nDetailed results saved to: {results_file}")

    summary_file = output_dir / "comparison_summary.csv"
    summary.to_csv(summary_file)
    print(f"Summary saved to: {summary_file}")


if __name__ == "__main__":
    main()
