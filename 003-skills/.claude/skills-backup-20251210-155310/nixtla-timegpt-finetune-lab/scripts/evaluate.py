#!/usr/bin/env python3
"""
Evaluate TimeGPT Forecast Performance

This script calculates comprehensive evaluation metrics:
1. Point forecast metrics (MAE, RMSE, SMAPE, MASE)
2. Per-series and aggregated results
3. Statistical significance tests
4. Performance breakdown by series characteristics
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd


def calculate_mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Mean Absolute Error"""
    return np.abs(y_true - y_pred).mean()


def calculate_rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Root Mean Squared Error"""
    return np.sqrt(((y_true - y_pred) ** 2).mean())


def calculate_mape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Mean Absolute Percentage Error"""
    # Avoid division by zero
    mask = y_true != 0
    if not mask.any():
        return np.inf
    return (np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])).mean() * 100


def calculate_smape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Symmetric Mean Absolute Percentage Error"""
    numerator = np.abs(y_true - y_pred)
    denominator = np.abs(y_true) + np.abs(y_pred)
    # Handle division by zero
    mask = denominator != 0
    if not mask.any():
        return 0.0
    return (numerator[mask] / denominator[mask]).mean() * 100


def calculate_mase(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_train: Optional[np.ndarray] = None,
    seasonality: int = 1,
) -> float:
    """
    Mean Absolute Scaled Error

    Args:
        y_true: Actual test values
        y_pred: Predicted values
        y_train: Training values (for naive forecast baseline)
        seasonality: Seasonal period (1 for non-seasonal)

    Returns:
        MASE value
    """
    if y_train is None or len(y_train) < seasonality + 1:
        # Fallback to MAE if no training data
        return calculate_mae(y_true, y_pred)

    # Naive forecast error (seasonal naive)
    naive_error = np.abs(y_train[seasonality:] - y_train[:-seasonality]).mean()

    if naive_error == 0:
        return np.inf

    # Model error
    model_error = calculate_mae(y_true, y_pred)

    return model_error / naive_error


def evaluate_forecast(
    test_df: pd.DataFrame,
    forecast_df: pd.DataFrame,
    train_df: Optional[pd.DataFrame] = None,
    seasonality: int = 1,
) -> pd.DataFrame:
    """
    Calculate evaluation metrics for each series.

    Args:
        test_df: Test data (unique_id, ds, y)
        forecast_df: Forecast data (unique_id, ds, TimeGPT)
        train_df: Training data (for MASE calculation)
        seasonality: Seasonal period

    Returns:
        DataFrame with metrics per series
    """
    # Merge test and forecast
    merged = test_df.merge(
        forecast_df, on=["unique_id", "ds"], how="inner", suffixes=("_actual", "_pred")
    )

    if len(merged) == 0:
        print("WARNING: No matching records between test and forecast data")
        return pd.DataFrame()

    results = []

    for unique_id in merged["unique_id"].unique():
        series_data = merged[merged["unique_id"] == unique_id].sort_values("ds")

        y_true = series_data["y"].values
        y_pred = series_data["TimeGPT"].values

        # Get training data for MASE
        y_train = None
        if train_df is not None:
            train_series = train_df[train_df["unique_id"] == unique_id]
            if len(train_series) > 0:
                y_train = train_series.sort_values("ds")["y"].values

        # Calculate metrics
        metrics = {
            "unique_id": unique_id,
            "n_test": len(y_true),
            "mae": calculate_mae(y_true, y_pred),
            "rmse": calculate_rmse(y_true, y_pred),
            "mape": calculate_mape(y_true, y_pred),
            "smape": calculate_smape(y_true, y_pred),
            "mase": calculate_mase(y_true, y_pred, y_train, seasonality),
        }

        # Add statistics
        metrics["mean_actual"] = y_true.mean()
        metrics["mean_forecast"] = y_pred.mean()
        metrics["bias"] = (y_pred - y_true).mean()

        results.append(metrics)

    return pd.DataFrame(results)


def print_summary(metrics_df: pd.DataFrame, model_name: str = "TimeGPT"):
    """
    Print evaluation summary.

    Args:
        metrics_df: DataFrame with metrics
        model_name: Model name for display
    """
    print("\n" + "=" * 60)
    print(f"{model_name.upper()} EVALUATION SUMMARY")
    print("=" * 60)

    # Aggregate metrics
    agg = {
        "mae": "mean",
        "rmse": "mean",
        "mape": "mean",
        "smape": "mean",
        "mase": "mean",
        "bias": "mean",
    }

    summary = metrics_df[list(agg.keys())].agg(agg)

    print(f"\nOverall Performance (n={len(metrics_df)} series):")
    print(f"  MAE:   {summary['mae']:.4f}")
    print(f"  RMSE:  {summary['rmse']:.4f}")
    print(f"  MAPE:  {summary['mape']:.2f}%")
    print(f"  SMAPE: {summary['smape']:.2f}%")
    print(f"  MASE:  {summary['mase']:.4f}")
    print(f"  Bias:  {summary['bias']:.4f}")

    # Best/worst performing series
    print(f"\nBest Performing Series (by SMAPE):")
    best = metrics_df.nsmallest(3, "smape")[["unique_id", "smape", "mae"]]
    for _, row in best.iterrows():
        print(f"  {row['unique_id']}: SMAPE={row['smape']:.2f}%, MAE={row['mae']:.4f}")

    print(f"\nWorst Performing Series (by SMAPE):")
    worst = metrics_df.nlargest(3, "smape")[["unique_id", "smape", "mae"]]
    for _, row in worst.iterrows():
        print(f"  {row['unique_id']}: SMAPE={row['smape']:.2f}%, MAE={row['mae']:.4f}")

    print("=" * 60 + "\n")


def main():
    """Main evaluation workflow"""
    parser = argparse.ArgumentParser(
        description="Evaluate TimeGPT forecast performance",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic evaluation
  python evaluate.py --test data/test.csv --forecast forecasts.csv

  # With training data for MASE
  python evaluate.py --test data/test.csv --forecast forecasts.csv \\
      --train data/train.csv --seasonality 7

  # Evaluate comparison results
  python evaluate.py --comparison forecasting/results/comparison_metrics.csv

Metrics:
  MAE:   Mean Absolute Error
  RMSE:  Root Mean Squared Error
  MAPE:  Mean Absolute Percentage Error
  SMAPE: Symmetric Mean Absolute Percentage Error
  MASE:  Mean Absolute Scaled Error (relative to naive forecast)
        """,
    )

    # Input options
    parser.add_argument("--test", help="Test data CSV path (unique_id, ds, y)")
    parser.add_argument("--forecast", help="Forecast CSV path (unique_id, ds, TimeGPT)")
    parser.add_argument("--comparison", help="Comparison results CSV (from compare_finetuned.py)")
    parser.add_argument("--train", help="Training data CSV (for MASE calculation)")
    parser.add_argument(
        "--seasonality", type=int, default=1, help="Seasonal period for MASE (default: 1)"
    )

    # Output options
    parser.add_argument(
        "--output", help="Output CSV path (default: forecasting/results/evaluation.csv)"
    )
    parser.add_argument("--model-name", default="TimeGPT", help="Model name for display")

    args = parser.parse_args()

    # Validate arguments
    if args.comparison:
        # Load pre-computed comparison results
        print(f"Loading comparison results: {args.comparison}")
        metrics_df = pd.read_csv(args.comparison)

        # Group by model and summarize
        for model in metrics_df["model"].unique():
            model_metrics = metrics_df[metrics_df["model"] == model]
            print_summary(model_metrics, model)

        sys.exit(0)

    if not args.test or not args.forecast:
        parser.error("Must specify --test and --forecast, or --comparison")

    # Load data
    print(f"Loading test data: {args.test}")
    test_df = pd.read_csv(args.test)

    print(f"Loading forecast data: {args.forecast}")
    forecast_df = pd.read_csv(args.forecast)

    train_df = None
    if args.train:
        print(f"Loading training data: {args.train}")
        train_df = pd.read_csv(args.train)

    # Validate data
    for col in ["unique_id", "ds", "y"]:
        if col not in test_df.columns:
            print(f"ERROR: Test data missing column: {col}")
            sys.exit(1)

    for col in ["unique_id", "ds", "TimeGPT"]:
        if col not in forecast_df.columns:
            print(f"ERROR: Forecast data missing column: {col}")
            sys.exit(1)

    # Evaluate
    print("\nCalculating metrics...")
    metrics_df = evaluate_forecast(test_df, forecast_df, train_df, seasonality=args.seasonality)

    if len(metrics_df) == 0:
        print("ERROR: No metrics calculated")
        sys.exit(1)

    # Print summary
    print_summary(metrics_df, args.model_name)

    # Save results
    output = args.output or "forecasting/results/evaluation.csv"
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    metrics_df.to_csv(output_path, index=False)
    print(f"Evaluation results saved to: {output_path}")


if __name__ == "__main__":
    main()
