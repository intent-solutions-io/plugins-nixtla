#!/usr/bin/env python3
"""
Prepare and Validate Data for TimeGPT Fine-Tuning

This script prepares datasets for TimeGPT fine-tuning by:
1. Validating data format (unique_id, ds, y columns)
2. Checking data quality (no NaN, sufficient observations)
3. Converting to Nixtla schema if needed
4. Splitting into train/validation sets
"""

import argparse
import sys
from pathlib import Path
from typing import Optional, Tuple

import pandas as pd


def validate_nixtla_schema(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate that dataframe matches Nixtla schema requirements.

    Args:
        df: DataFrame to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    required_cols = ["unique_id", "ds", "y"]

    # Check required columns
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        return False, f"Missing required columns: {missing_cols}"

    # Check for NaN values
    nan_counts = df[required_cols].isna().sum()
    if nan_counts.any():
        return False, f"Found NaN values: {nan_counts.to_dict()}"

    # Check data types
    if not pd.api.types.is_numeric_dtype(df["y"]):
        return False, "Column 'y' must be numeric"

    # Check minimum observations per series
    min_obs = 100
    series_counts = df.groupby("unique_id").size()
    insufficient_series = series_counts[series_counts < min_obs]

    if len(insufficient_series) > 0:
        return False, f"Series with < {min_obs} observations: {list(insufficient_series.index)}"

    return True, "Valid"


def convert_to_nixtla_schema(
    df: pd.DataFrame,
    id_col: Optional[str] = None,
    time_col: Optional[str] = None,
    target_col: Optional[str] = None,
) -> pd.DataFrame:
    """
    Convert dataframe to Nixtla schema (unique_id, ds, y).

    Args:
        df: Input dataframe
        id_col: Name of the ID column (default: auto-detect)
        time_col: Name of the timestamp column (default: auto-detect)
        target_col: Name of the target value column (default: auto-detect)

    Returns:
        DataFrame in Nixtla schema
    """
    result = df.copy()

    # Auto-detect or rename columns
    if "unique_id" not in result.columns:
        if id_col:
            result = result.rename(columns={id_col: "unique_id"})
        else:
            # Try common names
            for candidate in ["id", "series_id", "item_id", "store_id"]:
                if candidate in result.columns:
                    result = result.rename(columns={candidate: "unique_id"})
                    break

    if "ds" not in result.columns:
        if time_col:
            result = result.rename(columns={time_col: "ds"})
        else:
            # Try common names
            for candidate in ["date", "timestamp", "time", "datetime"]:
                if candidate in result.columns:
                    result = result.rename(columns={candidate: "ds"})
                    break

    if "y" not in result.columns:
        if target_col:
            result = result.rename(columns={target_col: "y"})
        else:
            # Try common names
            for candidate in ["value", "target", "sales", "demand"]:
                if candidate in result.columns:
                    result = result.rename(columns={candidate: "y"})
                    break

    # Keep only required columns (and optional exogenous variables)
    base_cols = ["unique_id", "ds", "y"]
    exog_cols = [col for col in result.columns if col not in base_cols]

    if exog_cols:
        print(f"Found {len(exog_cols)} exogenous variables: {exog_cols}")
        result = result[base_cols + exog_cols]
    else:
        result = result[base_cols]

    # Convert timestamp to datetime
    result["ds"] = pd.to_datetime(result["ds"])

    return result


def split_train_val(
    df: pd.DataFrame, val_size: int = 14, method: str = "time"
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split data into training and validation sets.

    Args:
        df: Input dataframe
        val_size: Number of periods for validation (default: 14)
        method: Split method ('time' or 'percentage')

    Returns:
        Tuple of (train_df, val_df)
    """
    if method == "time":
        # Hold out last val_size periods per series
        train_list = []
        val_list = []

        for unique_id in df["unique_id"].unique():
            series = df[df["unique_id"] == unique_id].sort_values("ds")
            train_list.append(series.iloc[:-val_size])
            val_list.append(series.iloc[-val_size:])

        train_df = pd.concat(train_list, ignore_index=True)
        val_df = pd.concat(val_list, ignore_index=True)

    else:  # percentage
        split_pct = 0.8
        n_train = int(len(df) * split_pct)
        train_df = df.iloc[:n_train]
        val_df = df.iloc[n_train:]

    return train_df, val_df


def main():
    """Main data preparation workflow"""
    parser = argparse.ArgumentParser(
        description="Prepare and validate data for TimeGPT fine-tuning",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python prepare_finetune_data.py --input data/sales.csv --output data/train.csv

  # With custom column names
  python prepare_finetune_data.py --input data.csv --output train.csv \\
      --id-col store_id --time-col date --target-col sales

  # With train/validation split
  python prepare_finetune_data.py --input data.csv \\
      --output-train data/train.csv --output-val data/val.csv --val-size 14
        """,
    )

    parser.add_argument("--input", required=True, help="Input CSV file path")
    parser.add_argument("--output", help="Output CSV file path (single file)")
    parser.add_argument("--output-train", help="Training set output path")
    parser.add_argument("--output-val", help="Validation set output path")
    parser.add_argument("--id-col", help="Name of ID column")
    parser.add_argument("--time-col", help="Name of timestamp column")
    parser.add_argument("--target-col", help="Name of target value column")
    parser.add_argument(
        "--val-size", type=int, default=14, help="Validation set size (default: 14)"
    )
    parser.add_argument(
        "--split-method",
        choices=["time", "percentage"],
        default="time",
        help="Train/val split method",
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.output and not (args.output_train and args.output_val):
        parser.error("Must specify either --output or both --output-train and --output-val")

    # Load data
    print(f"Loading data from: {args.input}")
    df = pd.read_csv(args.input)
    print(f"Loaded {len(df)} rows, {len(df.columns)} columns")

    # Convert to Nixtla schema
    print("Converting to Nixtla schema...")
    df_nixtla = convert_to_nixtla_schema(
        df, id_col=args.id_col, time_col=args.time_col, target_col=args.target_col
    )

    # Validate
    print("Validating data...")
    is_valid, msg = validate_nixtla_schema(df_nixtla)

    if not is_valid:
        print(f"ERROR: Validation failed - {msg}")
        sys.exit(1)

    print(f"Validation passed: {msg}")
    print(f"  - {df_nixtla['unique_id'].nunique()} unique series")
    print(f"  - {len(df_nixtla)} total observations")

    # Split or save single file
    if args.output_train and args.output_val:
        print(f"\nSplitting data (method: {args.split_method})...")
        train_df, val_df = split_train_val(
            df_nixtla, val_size=args.val_size, method=args.split_method
        )

        # Save splits
        Path(args.output_train).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output_val).parent.mkdir(parents=True, exist_ok=True)

        train_df.to_csv(args.output_train, index=False)
        val_df.to_csv(args.output_val, index=False)

        print(f"Saved training set: {args.output_train} ({len(train_df)} rows)")
        print(f"Saved validation set: {args.output_val} ({len(val_df)} rows)")

    else:
        # Save single file
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        df_nixtla.to_csv(args.output, index=False)
        print(f"\nSaved prepared data: {args.output}")

    print("\nData preparation complete!")


if __name__ == "__main__":
    main()
