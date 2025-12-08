#!/usr/bin/env python3
"""
Argument parser for Nixtla forecasting experiments.
"""
import argparse
import os
from typing import Optional


def parse_arguments() -> argparse.Namespace:
    """Parses command-line arguments for the forecasting experiment."""
    parser = argparse.ArgumentParser(description="Nixtla Forecasting Experiment Architect")
    parser.add_argument("--dataset_path", type=str, required=True, help="Path to the dataset CSV file.")
    parser.add_argument("--model_type", type=str, required=True, help="Type of forecasting model (e.g., TimeGPT, AutoARIMA).")
    parser.add_argument("--horizon", type=int, required=True, help="Forecasting horizon.")
    parser.add_argument("--experiment_name", type=str, default="forecasting_experiment", help="Name of the experiment directory.")
    parser.add_argument("--metrics", type=str, nargs='+', default=["MASE", "sMAPE"], help="Evaluation metrics to use.")
    parser.add_argument("--freq", type=str, default="D", help="Frequency of the time series data (e.g., D for daily, H for hourly).")
    parser.add_argument("--target_col", type=str, default="y", help="Name of the target variable column.")
    parser.add_argument("--date_col", type=str, default="ds", help="Name of the date column.")
    parser.add_argument("--id_col", type=str, default="unique_id", help="Name of the unique ID column.")
    parser.add_argument("--train_fraction", type=float, default=0.8, help="Fraction of data to use for training.")
    return parser.parse_args()


def validate_arguments(args: argparse.Namespace) -> None:
    """Validates the command-line arguments."""
    if not os.path.exists(args.dataset_path):
        raise FileNotFoundError(f"Dataset path not found: {args.dataset_path}")

    valid_model_types = ["TimeGPT", "AutoARIMA", "AutoETS", "SeasonalNaive", "AutoTheta"]
    if args.model_type not in valid_model_types:
        raise ValueError(f"Invalid model type: {args.model_type}. Must be one of {valid_model_types}")

    if args.horizon <= 0:
        raise ValueError("Horizon must be a positive integer.")

    valid_metrics = ["MASE", "sMAPE", "RMSE", "MAE"]
    for metric in args.metrics:
        if metric not in valid_metrics:
            raise ValueError(f"Invalid metric: {metric}. Must be one of {valid_metrics}")

    if not 0 < args.train_fraction < 1:
        raise ValueError("Train fraction must be between 0 and 1.")


if __name__ == "__main__":
    try:
        args = parse_arguments()
        validate_arguments(args)
        print("Experiment parameters are valid.")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
