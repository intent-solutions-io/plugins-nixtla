#!/usr/bin/env python3
"""
Forecast Validation Script

Validates time series forecast quality metrics by comparing current performance
against historical benchmarks. Detects significant deviations in MASE and sMAPE.

Usage:
    python validate_forecast.py --historical historical_metrics.csv --current current_metrics.csv
    python validate_forecast.py --historical hist.csv --current curr.csv --mase_threshold 0.3 --smape_threshold 0.25

Output:
    - validation_report.txt: Summary of validation results
    - metrics_comparison.csv: Side-by-side comparison of metrics
    - alert.log: Alerts for significant degradation
    - metrics_visualization.png: Bar charts comparing metrics
"""

import argparse
import logging
import os
from typing import Dict, Tuple

import matplotlib.pyplot as plt
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def load_metrics_data(file_path: str) -> pd.DataFrame:
    """
    Loads forecast metrics data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: A DataFrame containing the metrics data.

    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If the file cannot be parsed.
    """
    try:
        df = pd.read_csv(file_path)
        if df.empty:
            raise pd.errors.EmptyDataError(f"The file {file_path} is empty.")
        logging.info(f"Successfully loaded metrics data from {file_path}")
        return df
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        raise
    except pd.errors.EmptyDataError as e:
        logging.error(str(e))
        raise
    except pd.errors.ParserError as e:
        logging.error(f"Error parsing file {file_path}: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def configure_validation_parameters(
    mase_threshold: float = 0.2, smape_threshold: float = 0.2
) -> Tuple[float, float]:
    """
    Configures the validation parameters for MASE and sMAPE thresholds.

    Args:
        mase_threshold (float): The threshold for acceptable MASE deviation (default: 0.2).
        smape_threshold (float): The threshold for acceptable sMAPE deviation (default: 0.2).

    Returns:
        Tuple[float, float]: A tuple containing the MASE and sMAPE thresholds.

    Raises:
        ValueError: If either threshold is not a positive number.
    """
    if not isinstance(mase_threshold, (int, float)) or mase_threshold <= 0:
        raise ValueError("MASE threshold must be a positive number.")
    if not isinstance(smape_threshold, (int, float)) or smape_threshold <= 0:
        raise ValueError("sMAPE threshold must be a positive number.")

    logging.info(
        f"Validation parameters configured: MASE threshold = {mase_threshold}, sMAPE threshold = {smape_threshold}"
    )
    return mase_threshold, smape_threshold


def validate_forecast_metrics(
    historical_metrics: pd.DataFrame,
    current_metrics: pd.DataFrame,
    mase_threshold: float,
    smape_threshold: float,
) -> Dict[str, Dict[str, float]]:
    """
    Validates forecast metrics by comparing current metrics against historical benchmarks.

    Args:
        historical_metrics (pd.DataFrame): DataFrame containing historical metrics.
        current_metrics (pd.DataFrame): DataFrame containing current metrics.
        mase_threshold (float): Threshold for acceptable MASE deviation.
        smape_threshold (float): Threshold for acceptable sMAPE deviation.

    Returns:
        Dict[str, Dict[str, float]]: A dictionary containing validation results for each model.
            The keys are model names, and the values are dictionaries containing 'MASE_increase' and 'sMAPE_increase' flags.

    Raises:
        ValueError: If required columns are missing from the input data.
    """
    validation_results = {}

    # Ensure 'model' column exists in both DataFrames
    if "model" not in historical_metrics.columns or "model" not in current_metrics.columns:
        raise ValueError("Missing required 'model' column in metrics data.")

    # Ensure 'MASE' and 'sMAPE' columns exist in both DataFrames
    required_metrics = ["MASE", "sMAPE"]
    for metric in required_metrics:
        if metric not in historical_metrics.columns or metric not in current_metrics.columns:
            raise ValueError(f"Missing required metrics column: {metric}")

    # Merge historical and current metrics on the 'model' column
    merged_metrics = pd.merge(
        historical_metrics, current_metrics, on="model", suffixes=("_historical", "_current")
    )

    for index, row in merged_metrics.iterrows():
        model_name = row["model"]
        historical_mase = row["MASE_historical"]
        current_mase = row["MASE_current"]
        historical_smape = row["sMAPE_historical"]
        current_smape = row["sMAPE_current"]

        # Calculate percentage increase
        mase_increase = (
            (current_mase - historical_mase) / historical_mase
            if historical_mase != 0
            else float("inf")
        )
        smape_increase = (
            (current_smape - historical_smape) / historical_smape
            if historical_smape != 0
            else float("inf")
        )

        # Check if the increase exceeds the threshold
        mase_exceeds_threshold = mase_increase > mase_threshold
        smape_exceeds_threshold = smape_increase > smape_threshold

        validation_results[model_name] = {
            "MASE_increase": mase_increase,
            "sMAPE_increase": smape_increase,
            "MASE_exceeds_threshold": mase_exceeds_threshold,
            "sMAPE_exceeds_threshold": smape_exceeds_threshold,
        }

        logging.info(
            f"Validation results for model {model_name}: MASE increase = {mase_increase:.2f}, sMAPE increase = {smape_increase:.2f}"
        )

    return validation_results


def generate_report(
    validation_results: Dict[str, Dict[str, float]], output_path: str = "validation_report.txt"
) -> None:
    """
    Generates a report summarizing the validation results.

    Args:
        validation_results (Dict[str, Dict[str, float]]): A dictionary containing validation results for each model.
        output_path (str): The path to save the report (default: 'validation_report.txt').
    """
    with open(output_path, "w") as f:
        report_lines = []
        for model_name, results in validation_results.items():
            if results["MASE_exceeds_threshold"]:
                report_lines.append(
                    f"WARNING: Significant increase in MASE detected for model {model_name}."
                )
            if results["sMAPE_exceeds_threshold"]:
                report_lines.append(
                    f"WARNING: Significant increase in sMAPE detected for model {model_name}."
                )

        if not report_lines:
            report_lines.append("Forecast validation passed. No significant degradation detected.")

        for line in report_lines:
            f.write(line + "\n")
            logging.warning(line)

    logging.info(f"Validation report generated at {output_path}")


def create_metrics_comparison_csv(
    historical_metrics: pd.DataFrame,
    current_metrics: pd.DataFrame,
    output_path: str = "metrics_comparison.csv",
) -> None:
    """
    Creates a CSV file containing a comparison of historical and current metrics.

    Args:
        historical_metrics (pd.DataFrame): DataFrame containing historical metrics.
        current_metrics (pd.DataFrame): DataFrame containing current metrics.
        output_path (str): The path to save the CSV file (default: 'metrics_comparison.csv').

    Raises:
        Exception: If an error occurs during CSV creation.
    """
    try:
        merged_metrics = pd.merge(
            historical_metrics, current_metrics, on="model", suffixes=("_historical", "_current")
        )
        merged_metrics.to_csv(output_path, index=False)
        logging.info(f"Metrics comparison CSV generated at {output_path}")
    except Exception as e:
        logging.error(f"Error creating metrics comparison CSV: {e}")
        raise


def create_alert_log(
    validation_results: Dict[str, Dict[str, float]], output_path: str = "alert.log"
) -> None:
    """
    Creates a log file containing alerts if significant degradation is detected.

    Args:
        validation_results (Dict[str, Dict[str, float]]): A dictionary containing validation results for each model.
        output_path (str): The path to save the alert log (default: 'alert.log').
    """
    with open(output_path, "w") as f:
        alert_lines = []
        for model_name, results in validation_results.items():
            if results["MASE_exceeds_threshold"]:
                alert_lines.append(
                    f"ALERT: Significant increase in MASE detected for model {model_name}."
                )
            if results["sMAPE_exceeds_threshold"]:
                alert_lines.append(
                    f"ALERT: Significant increase in sMAPE detected for model {model_name}."
                )

        for line in alert_lines:
            f.write(line + "\n")
            logging.warning(line)

    logging.info(f"Alert log generated at {output_path}")


def visualize_metrics(
    historical_metrics: pd.DataFrame,
    current_metrics: pd.DataFrame,
    output_path: str = "metrics_visualization.png",
) -> None:
    """
    Visualizes historical and current metrics using bar plots.

    Args:
        historical_metrics (pd.DataFrame): DataFrame containing historical metrics.
        current_metrics (pd.DataFrame): DataFrame containing current metrics.
        output_path (str): The path to save the visualization (default: 'metrics_visualization.png').

    Raises:
        ValueError: If required columns are missing from the input data.
        Exception: If an error occurs during visualization creation.
    """
    try:
        # Ensure 'model' column exists in both DataFrames
        if "model" not in historical_metrics.columns or "model" not in current_metrics.columns:
            raise ValueError("Missing required 'model' column in metrics data.")

        # Ensure 'MASE' and 'sMAPE' columns exist in both DataFrames
        required_metrics = ["MASE", "sMAPE"]
        for metric in required_metrics:
            if metric not in historical_metrics.columns or metric not in current_metrics.columns:
                raise ValueError(f"Missing required metrics column: {metric}")

        # Set up the figure and axes
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

        # Plot MASE
        axes[0].bar(
            historical_metrics["model"], historical_metrics["MASE"], label="Historical", alpha=0.7
        )
        axes[0].bar(current_metrics["model"], current_metrics["MASE"], label="Current", alpha=0.7)
        axes[0].set_xlabel("Model")
        axes[0].set_ylabel("MASE")
        axes[0].set_title("MASE Comparison")
        axes[0].legend()

        # Plot sMAPE
        axes[1].bar(
            historical_metrics["model"], historical_metrics["sMAPE"], label="Historical", alpha=0.7
        )
        axes[1].bar(current_metrics["model"], current_metrics["sMAPE"], label="Current", alpha=0.7)
        axes[1].set_xlabel("Model")
        axes[1].set_ylabel("sMAPE")
        axes[1].set_title("sMAPE Comparison")
        axes[1].legend()

        # Adjust layout and save the figure
        plt.tight_layout()
        plt.savefig(output_path)
        logging.info(f"Metrics visualization saved to {output_path}")

    except Exception as e:
        logging.error(f"Error creating metrics visualization: {e}")
        raise


def main(
    historical_file: str,
    current_file: str,
    mase_threshold: float = 0.2,
    smape_threshold: float = 0.2,
) -> None:
    """
    Main function to execute the forecast validation process.

    Args:
        historical_file (str): Path to the historical metrics CSV file.
        current_file (str): Path to the current metrics CSV file.
        mase_threshold (float): Threshold for acceptable MASE deviation (default: 0.2).
        smape_threshold (float): Threshold for acceptable sMAPE deviation (default: 0.2).
    """
    try:
        # Load data
        historical_metrics = load_metrics_data(historical_file)
        current_metrics = load_metrics_data(current_file)

        # Configure validation parameters
        mase_threshold, smape_threshold = configure_validation_parameters(
            mase_threshold, smape_threshold
        )

        # Validate forecast metrics
        validation_results = validate_forecast_metrics(
            historical_metrics, current_metrics, mase_threshold, smape_threshold
        )

        # Generate report
        generate_report(validation_results)

        # Create metrics comparison CSV
        create_metrics_comparison_csv(historical_metrics, current_metrics)

        # Create alert log
        create_alert_log(validation_results)

        # Visualize metrics
        visualize_metrics(historical_metrics, current_metrics)

        logging.info("Forecast validation process completed successfully.")

    except Exception as e:
        logging.error(f"An error occurred during the validation process: {e}")
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate time series forecast quality metrics.")
    parser.add_argument(
        "--historical", type=str, required=True, help="Path to the historical metrics CSV file."
    )
    parser.add_argument(
        "--current", type=str, required=True, help="Path to the current metrics CSV file."
    )
    parser.add_argument(
        "--mase_threshold",
        type=float,
        default=0.2,
        help="Threshold for acceptable MASE deviation (default: 0.2).",
    )
    parser.add_argument(
        "--smape_threshold",
        type=float,
        default=0.2,
        help="Threshold for acceptable sMAPE deviation (default: 0.2).",
    )

    args = parser.parse_args()

    main(args.historical, args.current, args.mase_threshold, args.smape_threshold)
