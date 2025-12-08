#!/usr/bin/env python3
"""
Batch Forecaster - Data Preparation
Validates and prepares multi-series data for batch forecasting
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List

def load_multi_series_data(filepath: str) -> pd.DataFrame:
    """
    Load and validate multi-series time series data.

    Args:
        filepath: Path to CSV with columns (unique_id, ds, y)

    Returns:
        Validated DataFrame in Nixtla format
    """
    print(f"Loading data from {filepath}...")

    df = pd.read_csv(filepath)

    # Validate required columns
    required_cols = ["unique_id", "ds", "y"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Convert types
    df["ds"] = pd.to_datetime(df["ds"])
    df["y"] = pd.to_numeric(df["y"], errors="coerce")
    df["unique_id"] = df["unique_id"].astype(str)

    # Remove nulls
    null_count = df["y"].isna().sum()
    if null_count > 0:
        print(f"Warning: Dropping {null_count} rows with null y values")
        df = df.dropna(subset=["y"])

    # Sort by series and time
    df = df.sort_values(["unique_id", "ds"]).reset_index(drop=True)

    return df

def analyze_series(df: pd.DataFrame) -> Dict:
    """
    Analyze the multi-series dataset.

    Returns:
        Dict with series statistics
    """
    series_counts = df.groupby("unique_id").size()

    stats = {
        "total_rows": len(df),
        "num_series": df["unique_id"].nunique(),
        "series_list": df["unique_id"].unique().tolist(),
        "min_length": series_counts.min(),
        "max_length": series_counts.max(),
        "avg_length": series_counts.mean(),
        "date_range": {
            "min": df["ds"].min().isoformat(),
            "max": df["ds"].max().isoformat()
        },
        "value_range": {
            "min": df["y"].min(),
            "max": df["y"].max(),
            "mean": df["y"].mean()
        }
    }

    return stats

def split_into_batches(
    df: pd.DataFrame,
    batch_size: int = 10
) -> List[pd.DataFrame]:
    """
    Split multi-series data into batches by unique_id.

    Args:
        df: Full dataset
        batch_size: Number of series per batch

    Returns:
        List of DataFrames, each containing batch_size series
    """
    series_ids = df["unique_id"].unique()
    batches = []

    for i in range(0, len(series_ids), batch_size):
        batch_ids = series_ids[i:i + batch_size]
        batch_df = df[df["unique_id"].isin(batch_ids)]
        batches.append(batch_df)

    print(f"Split {len(series_ids)} series into {len(batches)} batches")
    return batches

if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python prepare_data.py <input.csv>")
        sys.exit(1)

    filepath = sys.argv[1]
    df = load_multi_series_data(filepath)
    stats = analyze_series(df)

    print("\n" + "="*50)
    print("DATASET ANALYSIS")
    print("="*50)
    print(f"Total rows: {stats['total_rows']:,}")
    print(f"Number of series: {stats['num_series']}")
    print(f"Series length: {stats['min_length']} - {stats['max_length']} (avg: {stats['avg_length']:.0f})")
    print(f"Date range: {stats['date_range']['min']} to {stats['date_range']['max']}")
    print(f"Value range: {stats['value_range']['min']:.4f} to {stats['value_range']['max']:.4f}")

    # Save stats
    with open("data_stats.json", "w") as f:
        json.dump(stats, f, indent=2, default=str)
    print("\nSaved analysis to data_stats.json")
