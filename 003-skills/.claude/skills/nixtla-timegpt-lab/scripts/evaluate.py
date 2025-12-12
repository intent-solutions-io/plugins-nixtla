#!/usr/bin/env python3
"""
Evaluate Forecast Accuracy

Computes standard forecasting metrics (SMAPE, MASE, MAE, RMSE)
comparing forecasts against actual values.

Usage:
    python evaluate.py --forecasts forecasts.csv --actuals actuals.csv
    python evaluate.py --forecasts forecasts.csv --actuals actuals.csv --output metrics.csv
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List

try:
    import numpy as np
    import pandas as pd
except ImportError:
    print("Error: pandas and numpy required. Run: pip install pandas numpy")
    sys.exit(1)


def smape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Symmetric Mean Absolute Percentage Error.

    SMAPE = 100 * mean(2 * |y - yhat| / (|y| + |yhat|))
    """
    numerator = 2 * np.abs(y_true - y_pred)
    denominator = np.abs(y_true) + np.abs(y_pred)

    # Avoid division by zero
    mask = denominator != 0
    if not mask.any():
        return 0.0

    return 100 * np.mean(numerator[mask] / denominator[mask])


def mase(y_true: np.ndarray, y_pred: np.ndarray, y_train: np.ndarray, season: int = 1) -> float:
    """
    Mean Absolute Scaled Error.

    MASE = MAE / naive_MAE
    where naive_MAE is the MAE of the seasonal naive forecast on training data.
    """
    mae = np.mean(np.abs(y_true - y_pred))

    # Compute naive MAE from training data
    if len(y_train) <= season:
        return np.nan

    naive_errors = np.abs(y_train[season:] - y_train[:-season])
    naive_mae = np.mean(naive_errors)

    if naive_mae == 0:
        return np.nan

    return mae / naive_mae


def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Mean Absolute Error."""
    return np.mean(np.abs(y_true - y_pred))


def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Root Mean Squared Error."""
    return np.sqrt(np.mean((y_true - y_pred) ** 2))


def compute_metrics(
    actuals: pd.DataFrame,
    forecasts: pd.DataFrame,
    model_cols: List[str],
    train_data: pd.DataFrame = None,
) -> pd.DataFrame:
    """
    Compute metrics for each model and series.

    Args:
        actuals: DataFrame with unique_id, ds, y columns
        forecasts: DataFrame with unique_id, ds, and model prediction columns
        model_cols: List of column names containing model predictions
        train_data: Optional training data for MASE calculation

    Returns:
        DataFrame with metrics per model
    """
    # Merge actuals with forecasts
    merged = actuals.merge(
        forecasts, on=["unique_id", "ds"], how="inner", suffixes=("_actual", "_forecast")
    )

    if len(merged) == 0:
        raise ValueError("No matching rows between actuals and forecasts")

    results = []

    for model in model_cols:
        if model not in merged.columns:
            continue

        y_true = merged["y"].values
        y_pred = merged[model].values

        # Skip if all predictions are NaN
        valid_mask = ~np.isnan(y_pred)
        if not valid_mask.any():
            continue

        y_true_valid = y_true[valid_mask]
        y_pred_valid = y_pred[valid_mask]

        metrics = {
            "model": model,
            "SMAPE": smape(y_true_valid, y_pred_valid),
            "MAE": mae(y_true_valid, y_pred_valid),
            "RMSE": rmse(y_true_valid, y_pred_valid),
            "n_samples": len(y_true_valid),
        }

        # Compute MASE if training data provided
        if train_data is not None and len(train_data) > 0:
            y_train = train_data["y"].values
            metrics["MASE"] = mase(y_true_valid, y_pred_valid, y_train, season=1)

        results.append(metrics)

    return pd.DataFrame(results)


def detect_model_columns(df: pd.DataFrame) -> List[str]:
    """Detect which columns contain model predictions."""
    exclude = {"unique_id", "ds", "y", "cutoff"}
    # Also exclude confidence interval columns
    model_cols = [
        c
        for c in df.columns
        if c not in exclude
        and not c.endswith("-lo-80")
        and not c.endswith("-lo-90")
        and not c.endswith("-hi-80")
        and not c.endswith("-hi-90")
    ]
    return model_cols


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Evaluate forecast accuracy with standard metrics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --forecasts forecasts.csv --actuals actuals.csv
  %(prog)s --forecasts forecasts.csv --actuals actuals.csv --output metrics.csv

Both CSVs must have columns: unique_id, ds
Actuals must have column: y
Forecasts must have model prediction columns (auto-detected)

Metrics computed:
  SMAPE: Symmetric Mean Absolute Percentage Error (0-200, lower is better)
  MAE:   Mean Absolute Error (lower is better)
  RMSE:  Root Mean Squared Error (lower is better)
  MASE:  Mean Absolute Scaled Error (if training data provided)
        """,
    )

    parser.add_argument(
        "--forecasts", "-f", required=True, help="CSV file with forecast predictions"
    )
    parser.add_argument("--actuals", "-a", required=True, help="CSV file with actual values")
    parser.add_argument(
        "--output",
        "-o",
        default="metrics.csv",
        help="Output CSV file for metrics (default: metrics.csv)",
    )
    parser.add_argument("--train", "-t", help="Optional training data CSV for MASE calculation")

    args = parser.parse_args()

    # Load forecasts
    forecasts_path = Path(args.forecasts)
    if not forecasts_path.exists():
        print(f"Error: Forecasts file not found: {forecasts_path}")
        return 1

    print(f"Loading forecasts from {forecasts_path}...")
    forecasts = pd.read_csv(forecasts_path)
    forecasts["ds"] = pd.to_datetime(forecasts["ds"])

    # Load actuals
    actuals_path = Path(args.actuals)
    if not actuals_path.exists():
        print(f"Error: Actuals file not found: {actuals_path}")
        return 1

    print(f"Loading actuals from {actuals_path}...")
    actuals = pd.read_csv(actuals_path)
    actuals["ds"] = pd.to_datetime(actuals["ds"])

    if "y" not in actuals.columns:
        print("Error: Actuals file must have 'y' column")
        return 1

    # Load training data if provided
    train_data = None
    if args.train:
        train_path = Path(args.train)
        if train_path.exists():
            print(f"Loading training data from {train_path}...")
            train_data = pd.read_csv(train_path)

    # Detect model columns
    model_cols = detect_model_columns(forecasts)
    if not model_cols:
        print("Error: No model prediction columns found in forecasts")
        return 1

    print(f"Found {len(model_cols)} models: {model_cols}")
    print()

    # Compute metrics
    try:
        metrics = compute_metrics(actuals, forecasts, model_cols, train_data)
    except ValueError as e:
        print(f"Error: {e}")
        return 1

    # Display results
    print("Evaluation Results")
    print("=" * 60)
    print(metrics.to_string(index=False))
    print()

    # Find best model by SMAPE
    if len(metrics) > 0:
        best = metrics.loc[metrics["SMAPE"].idxmin()]
        print(f"Best model by SMAPE: {best['model']} ({best['SMAPE']:.2f})")

    # Save metrics
    output_path = Path(args.output)
    metrics.to_csv(output_path, index=False)
    print(f"\nMetrics saved to: {output_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
