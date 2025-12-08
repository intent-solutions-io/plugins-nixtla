#!/usr/bin/env python3
"""
Configuration file generator for Nixtla forecasting experiments.
"""
import yaml
import os
import argparse


def create_config_files(args: argparse.Namespace) -> None:
    """Creates YAML configuration files for the forecasting experiment."""

    experiment_dir = args.experiment_name
    os.makedirs(experiment_dir, exist_ok=True)

    # Data configuration
    data_config = {
        "dataset_path": args.dataset_path,
        "freq": args.freq,
        "target_col": args.target_col,
        "date_col": args.date_col,
        "id_col": args.id_col,
        "train_fraction": args.train_fraction
    }
    with open(os.path.join(experiment_dir, "data.yaml"), "w") as f:
        yaml.dump(data_config, f, indent=4)

    # Model configuration
    model_config = {
        "model_type": args.model_type,
        "horizon": args.horizon
    }
    with open(os.path.join(experiment_dir, "models.yaml"), "w") as f:
        yaml.dump(model_config, f, indent=4)

    # Experiment configuration
    experiment_config = {
        "experiment_name": args.experiment_name,
        "metrics": args.metrics
    }
    with open(os.path.join(experiment_dir, "config.yaml"), "w") as f:
        yaml.dump(experiment_config, f, indent=4)

    print(f"Configuration files created in directory: {experiment_dir}")


if __name__ == "__main__":
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

    try:
        args = parser.parse_args()
        create_config_files(args)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
