#!/usr/bin/env python3
"""
Nixtla Anomaly Detector - TimeGPT-based anomaly detection.

Detects outliers, level shifts, and trend breaks in time series data
using the Nixtla TimeGPT API.

Usage:
    python detect_anomalies.py --input data.csv [--output-csv anomalies.csv]
                               [--output-plot plot.png] [--output-summary summary.txt]

Requirements:
    pip install nixtla pandas matplotlib

Environment:
    NIXTLA_TIMEGPT_API_KEY - Your TimeGPT API key

Author: Nixtla Skills Pack
Version: 1.0.0
"""

import argparse
import os
import sys
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd


def load_data(input_file: str) -> pd.DataFrame:
    """
    Load time series data from a CSV file.

    Args:
        input_file: Path to the CSV file.

    Returns:
        DataFrame containing the time series data.

    Raises:
        FileNotFoundError: If the input file does not exist.
        ValueError: If CSV doesn't contain required columns.
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {e}")

    required_columns = ["unique_id", "ds", "y"]
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"CSV file missing required columns: {missing}")

    df["ds"] = pd.to_datetime(df["ds"])
    return df


def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect anomalies in time series data using TimeGPT.

    Args:
        df: DataFrame containing the time series data.

    Returns:
        DataFrame containing detected anomalies with timestamps and type.
        Returns empty DataFrame if no anomalies detected.

    Raises:
        ValueError: If API key is not set.
    """
    api_key = os.getenv("NIXTLA_TIMEGPT_API_KEY")
    if not api_key:
        raise ValueError(
            "NIXTLA_TIMEGPT_API_KEY not set. " "Run: export NIXTLA_TIMEGPT_API_KEY=your_key"
        )

    try:
        from nixtla import NixtlaClient

        client = NixtlaClient(api_key=api_key)
        anomalies_df = client.detect_anomalies(df)

        if anomalies_df.empty:
            print("No anomalies detected.")
            return pd.DataFrame()

        return anomalies_df

    except ImportError:
        raise ImportError("nixtla package not installed. Run: pip install nixtla")
    except Exception as e:
        print(f"Error during anomaly detection: {e}")
        return pd.DataFrame()


def generate_summary(anomalies_df: pd.DataFrame) -> str:
    """
    Generate a summary of detected anomalies.

    Args:
        anomalies_df: DataFrame containing the detected anomalies.

    Returns:
        Summary string with counts by anomaly type.
    """
    if anomalies_df.empty:
        return "No anomalies detected."

    total = len(anomalies_df)
    summary_lines = [
        f"Anomaly Detection Summary",
        f"=" * 40,
        f"Total anomalies detected: {total}",
        "",
    ]

    if "anomaly_type" in anomalies_df.columns:
        counts = anomalies_df["anomaly_type"].value_counts()
        summary_lines.append("By type:")
        for anomaly_type, count in counts.items():
            summary_lines.append(f"  - {anomaly_type}: {count}")

    if "unique_id" in anomalies_df.columns:
        series_counts = anomalies_df["unique_id"].value_counts()
        summary_lines.append("")
        summary_lines.append("By series:")
        for series_id, count in series_counts.head(10).items():
            summary_lines.append(f"  - {series_id}: {count}")

    return "\n".join(summary_lines)


def plot_anomalies(df: pd.DataFrame, anomalies_df: pd.DataFrame, output_plot: str) -> None:
    """
    Visualize time series data with anomalies highlighted.

    Args:
        df: DataFrame containing the time series data.
        anomalies_df: DataFrame containing the detected anomalies.
        output_plot: Path to save the visualization plot.
    """
    if df.empty:
        print("No data to plot.")
        return

    unique_ids = df["unique_id"].unique()

    # For multiple series, create subplots
    n_series = min(len(unique_ids), 4)  # Max 4 subplots
    fig, axes = plt.subplots(n_series, 1, figsize=(12, 4 * n_series))

    if n_series == 1:
        axes = [axes]

    for idx, uid in enumerate(unique_ids[:n_series]):
        ax = axes[idx]
        series_data = df[df["unique_id"] == uid]
        ax.plot(series_data["ds"], series_data["y"], label="Time Series", alpha=0.7)

        if not anomalies_df.empty and "unique_id" in anomalies_df.columns:
            series_anomalies = anomalies_df[anomalies_df["unique_id"] == uid]
            if not series_anomalies.empty:
                ax.scatter(
                    series_anomalies["ds"],
                    series_anomalies["y"],
                    color="red",
                    s=100,
                    label="Anomaly",
                    zorder=5,
                )

        ax.set_xlabel("Date")
        ax.set_ylabel("Value")
        ax.set_title(f"Time Series: {uid}")
        ax.legend()
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_plot, dpi=150)
    plt.close()
    print(f"Anomaly plot saved to: {output_plot}")


def save_results(
    anomalies_df: pd.DataFrame, summary: str, output_csv: str, output_summary: str
) -> None:
    """
    Save anomaly detection results to files.

    Args:
        anomalies_df: DataFrame containing detected anomalies.
        summary: Summary text.
        output_csv: Path for CSV output.
        output_summary: Path for summary text file.
    """
    if not anomalies_df.empty:
        anomalies_df.to_csv(output_csv, index=False)
        print(f"Anomalies saved to: {output_csv}")

    with open(output_summary, "w") as f:
        f.write(summary)
    print(f"Summary saved to: {output_summary}")


def main():
    """Main entry point for anomaly detection."""
    parser = argparse.ArgumentParser(
        description="Detect anomalies in time series data using TimeGPT."
    )
    parser.add_argument(
        "--input",
        "-i",
        type=str,
        required=True,
        help="Path to input CSV file (columns: unique_id, ds, y)",
    )
    parser.add_argument(
        "--output-csv",
        "-o",
        type=str,
        default="anomalies.csv",
        help="Path for anomaly output CSV (default: anomalies.csv)",
    )
    parser.add_argument(
        "--output-plot",
        "-p",
        type=str,
        default="anomalies_plot.png",
        help="Path for visualization plot (default: anomalies_plot.png)",
    )
    parser.add_argument(
        "--output-summary",
        "-s",
        type=str,
        default="anomaly_summary.txt",
        help="Path for summary text file (default: anomaly_summary.txt)",
    )

    args = parser.parse_args()

    try:
        print(f"Loading data from: {args.input}")
        df = load_data(args.input)
        print(f"Loaded {len(df)} records across {df['unique_id'].nunique()} series")

        print("Running anomaly detection...")
        anomalies_df = detect_anomalies(df)

        summary = generate_summary(anomalies_df)
        print("\n" + summary)

        save_results(anomalies_df, summary, args.output_csv, args.output_summary)

        if not anomalies_df.empty:
            plot_anomalies(df, anomalies_df, args.output_plot)

        print("\nAnomaly detection complete!")
        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
