"""
Perform time series cross-validation with TimeGPT or StatsForecast models.

Usage:
    python cross_validate.py --input data.csv --model arima --window 20 --folds 3 --freq D
"""

import argparse
import json
import os
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import pandas as pd
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA, AutoETS, AutoTheta, SeasonalNaive

from nixtla import NixtlaClient


def cross_validate(
    df: pd.DataFrame, model_name: str, window_size: int, folds: int, freq: str
) -> Tuple[pd.DataFrame, Dict[str, float]]:
    """
    Performs time series cross-validation using expanding window.

    Args:
        df: The input DataFrame with 'unique_id', 'ds', and 'y' columns.
        model_name: The name of the model to use ('timegpt', 'arima', 'ets').
        window_size: The size of the validation window.
        folds: The number of folds to create.
        freq: The frequency of the time series data (e.g., 'D', 'M').

    Returns:
        A tuple containing:
            - A DataFrame with cross-validation results (fold, unique_id, ds, y, y_hat).
            - A dictionary with overall performance metrics (MAE, RMSE).

    Raises:
        ValueError: If model_name is invalid.
        ValueError: If window_size or folds are invalid.
        ValueError: If the DataFrame is too small for the specified window_size and folds.
        Exception: If an error occurs during model training or forecasting.
    """

    if model_name not in ["timegpt", "arima", "ets", "theta", "naive"]:
        raise ValueError(
            f"Invalid model name: {model_name}. Supported models are 'timegpt', 'arima', 'ets', 'theta', 'naive'."
        )

    if window_size <= 0:
        raise ValueError("Window size must be a positive integer.")
    if folds <= 0:
        raise ValueError("Number of folds must be a positive integer.")

    total_length = len(df)
    if total_length <= window_size * folds:
        raise ValueError(
            "DataFrame is too small for the specified window size and number of folds."
        )

    cv_results = []
    all_mae = []
    all_rmse = []

    for i in range(folds):
        train_end = total_length - (folds - i) * window_size
        val_start = train_end
        val_end = train_end + window_size

        train_df = df.iloc[:train_end].copy()
        val_df = df.iloc[val_start:val_end].copy()

        try:
            if model_name == "timegpt":
                api_key = os.getenv("NIXTLA_TIMEGPT_API_KEY")
                if not api_key:
                    raise ValueError("NIXTLA_TIMEGPT_API_KEY environment variable not set.")
                client = NixtlaClient(api_key=api_key)
                forecast = client.forecast(df=train_df, h=window_size, freq=freq)
                forecast = forecast.rename(
                    columns={"unique_id": "unique_id", "ds": "ds", "TimeGPT": "y_hat"}
                )

            elif model_name == "arima":
                sf = StatsForecast(models=[AutoARIMA()], freq=freq, n_jobs=-1)
                forecast = sf.forecast(df=train_df, h=window_size)
                forecast = forecast.reset_index().rename(
                    columns={"unique_id": "unique_id", "ds": "ds", "AutoARIMA": "y_hat"}
                )

            elif model_name == "ets":
                sf = StatsForecast(models=[AutoETS()], freq=freq, n_jobs=-1)
                forecast = sf.forecast(df=train_df, h=window_size)
                forecast = forecast.reset_index().rename(
                    columns={"unique_id": "unique_id", "ds": "ds", "AutoETS": "y_hat"}
                )

            elif model_name == "theta":
                sf = StatsForecast(models=[AutoTheta()], freq=freq, n_jobs=-1)
                forecast = sf.forecast(df=train_df, h=window_size)
                forecast = forecast.reset_index().rename(
                    columns={"unique_id": "unique_id", "ds": "ds", "AutoTheta": "y_hat"}
                )

            elif model_name == "naive":
                sf = StatsForecast(models=[SeasonalNaive()], freq=freq, n_jobs=-1)
                forecast = sf.forecast(df=train_df, h=window_size)
                forecast = forecast.reset_index().rename(
                    columns={"unique_id": "unique_id", "ds": "ds", "SeasonalNaive": "y_hat"}
                )

            else:
                raise ValueError(f"Unsupported model: {model_name}")

            # Merge actual and predicted values
            fold_results = val_df.merge(forecast, on=["unique_id", "ds"], how="left")
            fold_results["fold"] = i + 1
            cv_results.append(fold_results)

            # Calculate metrics for this fold
            mae = abs(fold_results["y"] - fold_results["y_hat"]).mean()
            rmse = ((fold_results["y"] - fold_results["y_hat"]) ** 2).mean() ** 0.5
            all_mae.append(mae)
            all_rmse.append(rmse)

            # Create a plot for each fold
            plt.figure(figsize=(10, 6))
            plt.plot(fold_results["ds"], fold_results["y"], label="Actual")
            plt.plot(fold_results["ds"], fold_results["y_hat"], label="Predicted")
            plt.xlabel("Date")
            plt.ylabel("Value")
            plt.title(f"Fold {i+1}: Actual vs Predicted")
            plt.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()
            os.makedirs("plots", exist_ok=True)
            plt.savefig(f"plots/fold_{i+1}.png")
            plt.close()

        except Exception as e:
            raise Exception(f"Error during cross-validation fold {i+1}: {e}")

    # Combine results from all folds
    cv_results_df = pd.concat(cv_results)

    # Calculate overall metrics
    overall_mae = sum(all_mae) / len(all_mae)
    overall_rmse = sum(all_rmse) / len(all_rmse)
    metrics = {"MAE": overall_mae, "RMSE": overall_rmse}

    return cv_results_df, metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perform time series cross-validation.")
    parser.add_argument("--input", required=True, help="Path to input CSV file")
    parser.add_argument(
        "--model",
        required=True,
        choices=["timegpt", "arima", "ets", "theta", "naive"],
        help="Model to use for forecasting",
    )
    parser.add_argument("--window", type=int, required=True, help="Validation window size")
    parser.add_argument("--folds", type=int, required=True, help="Number of cross-validation folds")
    parser.add_argument("--freq", required=True, help="Time series frequency (e.g., D, M, H)")

    args = parser.parse_args()

    try:
        # Load data
        df = pd.read_csv(args.input)

        # Perform cross-validation
        cv_results_df, metrics = cross_validate(df, args.model, args.window, args.folds, args.freq)

        # Save results to CSV
        cv_results_df.to_csv("cv_results.csv", index=False)
        print("Cross-validation results saved to cv_results.csv")

        # Save metrics to JSON
        with open("metrics.json", "w") as f:
            json.dump(metrics, f, indent=4)
        print("Metrics saved to metrics.json")
        print(f"Overall MAE: {metrics['MAE']:.2f}")
        print(f"Overall RMSE: {metrics['RMSE']:.2f}")

    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)
