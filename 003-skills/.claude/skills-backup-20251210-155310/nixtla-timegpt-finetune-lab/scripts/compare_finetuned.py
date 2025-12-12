#!/usr/bin/env python3
"""
Compare TimeGPT Zero-Shot vs Fine-Tuned Models

This script compares forecasting performance:
1. Generates forecasts from TimeGPT zero-shot (baseline)
2. Generates forecasts from fine-tuned TimeGPT model
3. Calculates evaluation metrics (SMAPE, MASE, MAE)
4. Produces comparison report showing improvement
"""

import argparse
import logging
import os
import re
import sys
from pathlib import Path
from typing import Optional

import pandas as pd
import yaml

# Security logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from nixtla import NixtlaClient
except ImportError:
    print("ERROR: nixtla package not installed")
    print("Run: pip install nixtla")
    sys.exit(1)


def validate_api_key(key: Optional[str]) -> bool:
    """
    Validate API key format and structure.

    Args:
        key: API key string to validate

    Returns:
        True if key appears valid, False otherwise

    Security:
        - Minimum length check prevents empty/trivial keys
        - Pattern check validates expected format
        - Does not log key value to prevent credential leakage
        - OWASP A07:2021 - Identification and Authentication Failures
    """
    if not key:
        logger.error("API key is missing or empty")
        return False

    key = key.strip()

    # Minimum length check (Nixtla keys are typically 32+ characters)
    if len(key) < 20:
        logger.error("API key is too short (minimum 20 characters required)")
        return False

    # Check for common placeholder values
    placeholder_patterns = [
        r"^your[-_]?api[-_]?key",
        r"^xxx+$",
        r"^test[-_]?key",
        r"^placeholder",
        r"^demo[-_]?key",
    ]
    for pattern in placeholder_patterns:
        if re.match(pattern, key, re.IGNORECASE):
            logger.error("API key appears to be a placeholder value")
            return False

    # Basic alphanumeric pattern check (allow alphanumeric, hyphens, underscores)
    if not re.match(r"^[a-zA-Z0-9_-]+$", key):
        logger.error("API key contains invalid characters")
        return False

    return True


def load_finetuned_model_id(artifacts_dir: str) -> str:
    """
    Load fine-tuned model ID from artifacts.

    Args:
        artifacts_dir: Path to artifacts directory

    Returns:
        Model ID string or None
    """
    model_id_file = Path(artifacts_dir) / "finetune_model_id.txt"

    if not model_id_file.exists():
        print(f"WARNING: Model ID file not found: {model_id_file}")
        return None

    return model_id_file.read_text().strip()


def run_zeroshot_forecast(
    client: NixtlaClient, df: pd.DataFrame, horizon: int, freq: str
) -> pd.DataFrame:
    """
    Generate TimeGPT zero-shot forecast.

    Args:
        client: NixtlaClient instance
        df: Training data
        horizon: Forecast horizon
        freq: Data frequency

    Returns:
        Forecast dataframe
    """
    print("Running TimeGPT zero-shot forecast...")
    forecast = client.forecast(df=df, h=horizon, freq=freq)
    print(f"  Generated {len(forecast)} forecast points")
    return forecast


def run_finetuned_forecast(
    client: NixtlaClient, df: pd.DataFrame, horizon: int, freq: str, finetune_id: str
) -> pd.DataFrame:
    """
    Generate fine-tuned TimeGPT forecast.

    Args:
        client: NixtlaClient instance
        df: Training data
        horizon: Forecast horizon
        freq: Data frequency
        finetune_id: Fine-tuned model ID

    Returns:
        Forecast dataframe
    """
    print(f"Running TimeGPT fine-tuned forecast (model: {finetune_id})...")
    forecast = client.forecast(df=df, h=horizon, freq=freq, finetune_id=finetune_id)
    print(f"  Generated {len(forecast)} forecast points")
    return forecast


def calculate_metrics(
    test_df: pd.DataFrame, forecast_df: pd.DataFrame, model_name: str
) -> pd.DataFrame:
    """
    Calculate evaluation metrics for forecast.

    Args:
        test_df: Test data with actual values
        forecast_df: Forecast predictions
        model_name: Name for this model

    Returns:
        DataFrame with metrics per series
    """
    # Merge actual and predicted
    merged = test_df.merge(forecast_df, on=["unique_id", "ds"], how="inner")

    results = []

    for unique_id in merged["unique_id"].unique():
        series_data = merged[merged["unique_id"] == unique_id]

        y_true = series_data["y"].values
        y_pred = series_data["TimeGPT"].values

        # Calculate metrics
        mae = abs(y_true - y_pred).mean()
        mse = ((y_true - y_pred) ** 2).mean()
        rmse = mse**0.5

        # SMAPE (Symmetric Mean Absolute Percentage Error)
        smape = 100 * (abs(y_true - y_pred) / (abs(y_true) + abs(y_pred))).mean()

        results.append(
            {"model": model_name, "unique_id": unique_id, "mae": mae, "rmse": rmse, "smape": smape}
        )

    return pd.DataFrame(results)


def print_comparison(zeroshot_metrics: pd.DataFrame, finetuned_metrics: pd.DataFrame):
    """
    Print comparison summary.

    Args:
        zeroshot_metrics: Zero-shot model metrics
        finetuned_metrics: Fine-tuned model metrics
    """
    # Aggregate metrics
    zs_agg = zeroshot_metrics[["mae", "rmse", "smape"]].mean()
    ft_agg = finetuned_metrics[["mae", "rmse", "smape"]].mean()

    # Calculate improvement
    mae_improve = ((zs_agg["mae"] - ft_agg["mae"]) / zs_agg["mae"]) * 100
    rmse_improve = ((zs_agg["rmse"] - ft_agg["rmse"]) / zs_agg["rmse"]) * 100
    smape_improve = ((zs_agg["smape"] - ft_agg["smape"]) / zs_agg["smape"]) * 100

    print("\n" + "=" * 60)
    print("MODEL COMPARISON")
    print("=" * 60)
    print(f"\nTimeGPT Zero-Shot:")
    print(f"  MAE:   {zs_agg['mae']:.4f}")
    print(f"  RMSE:  {zs_agg['rmse']:.4f}")
    print(f"  SMAPE: {zs_agg['smape']:.2f}%")

    print(f"\nTimeGPT Fine-Tuned:")
    print(f"  MAE:   {ft_agg['mae']:.4f}")
    print(f"  RMSE:  {ft_agg['rmse']:.4f}")
    print(f"  SMAPE: {ft_agg['smape']:.2f}%")

    print(f"\nImprovement:")
    print(f"  MAE:   {mae_improve:+.1f}%")
    print(f"  RMSE:  {rmse_improve:+.1f}%")
    print(f"  SMAPE: {smape_improve:+.1f}%")
    print("=" * 60 + "\n")


def main():
    """Main comparison workflow"""
    parser = argparse.ArgumentParser(
        description="Compare TimeGPT zero-shot vs fine-tuned models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Compare using test data
  python compare_finetuned.py --test data/test.csv

  # Specify custom model ID
  python compare_finetuned.py --test data/test.csv --finetune-id my-model-v1

  # Custom forecast parameters
  python compare_finetuned.py --test data/test.csv --horizon 14 --freq D

Environment Variables:
  NIXTLA_API_KEY: Required. Get from https://dashboard.nixtla.io
        """,
    )

    parser.add_argument("--test", required=True, help="Test data CSV path (with actual values)")
    parser.add_argument("--finetune-id", help="Fine-tuned model ID (or load from artifacts)")
    parser.add_argument(
        "--artifacts-dir",
        default="forecasting/artifacts/timegpt_finetune",
        help="Artifacts directory",
    )
    parser.add_argument("--horizon", type=int, default=14, help="Forecast horizon (default: 14)")
    parser.add_argument("--freq", default="D", help="Data frequency (default: D)")
    parser.add_argument(
        "--output", default="forecasting/results/comparison_metrics.csv", help="Output CSV path"
    )

    args = parser.parse_args()

    # Security: Validate API key before use
    api_key = os.getenv("NIXTLA_API_KEY", "").strip()

    if not validate_api_key(api_key):
        print("ERROR: Invalid or missing NIXTLA_API_KEY")
        print("Export your API key: export NIXTLA_API_KEY='your-key'")
        print("\nSecurity requirements:")
        print("  - Minimum 20 characters")
        print("  - Cannot be a placeholder value")
        print("  - Alphanumeric characters, hyphens, and underscores only")
        sys.exit(1)

    # Load test data
    print(f"Loading test data: {args.test}")
    test_df = pd.read_csv(args.test)

    # Validate test data
    required_cols = ["unique_id", "ds", "y"]
    missing_cols = [col for col in required_cols if col not in test_df.columns]
    if missing_cols:
        print(f"ERROR: Test data missing columns: {missing_cols}")
        sys.exit(1)

    print(f"  {len(test_df)} test observations")
    print(f"  {test_df['unique_id'].nunique()} unique series")

    # Prepare training data (use test data without target for forecasting)
    train_df = test_df[["unique_id", "ds"]].copy()

    # Get fine-tuned model ID
    finetune_id = args.finetune_id
    if not finetune_id:
        finetune_id = load_finetuned_model_id(args.artifacts_dir)

    if not finetune_id:
        print("ERROR: No fine-tuned model ID found")
        print("Specify --finetune-id or ensure artifacts directory contains model ID")
        sys.exit(1)

    # Initialize client
    print("\nInitializing TimeGPT client...")
    client = NixtlaClient(api_key=api_key)

    # Generate forecasts
    print("\nGenerating forecasts...")
    zeroshot_forecast = run_zeroshot_forecast(client, train_df, args.horizon, args.freq)
    finetuned_forecast = run_finetuned_forecast(
        client, train_df, args.horizon, args.freq, finetune_id
    )

    # Calculate metrics
    print("\nCalculating metrics...")
    zeroshot_metrics = calculate_metrics(test_df, zeroshot_forecast, "TimeGPT Zero-Shot")
    finetuned_metrics = calculate_metrics(test_df, finetuned_forecast, "TimeGPT Fine-Tuned")

    # Combine results
    all_metrics = pd.concat([zeroshot_metrics, finetuned_metrics], ignore_index=True)

    # Print comparison
    print_comparison(zeroshot_metrics, finetuned_metrics)

    # Save results
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    all_metrics.to_csv(output_path, index=False)

    print(f"Results saved to: {output_path}")
    print("\nNext steps:")
    print("  1. Review detailed metrics CSV")
    print("  2. Visualize forecasts and errors")
    print("  3. Evaluate if improvement justifies fine-tuning cost")


if __name__ == "__main__":
    main()
