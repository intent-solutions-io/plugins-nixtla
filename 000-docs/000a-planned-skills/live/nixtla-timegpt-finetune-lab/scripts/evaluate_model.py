#!/usr/bin/env python3
"""
Model evaluation script for fine-tuned TimeGPT.
"""
import pandas as pd
import pickle
import json
from nixtla import NixtlaClient
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
from typing import Dict
import logging
import argparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def load_model(file_path: str) -> NixtlaClient:
    """
    Loads the fine-tuned TimeGPT model from a pickle file.

    Args:
        file_path (str): The path to the saved model.

    Returns:
        NixtlaClient: The loaded TimeGPT model.

    Raises:
        FileNotFoundError: If the specified file path does not exist.
        Exception: If the model loading fails.
    """
    try:
        with open(file_path, 'rb') as f:
            model = pickle.load(f)
        logging.info(f"Model loaded from {file_path}")
        return model
    except FileNotFoundError:
        raise FileNotFoundError(f"Model file not found at path: {file_path}")
    except Exception as e:
        logging.error(f"Failed to load model: {e}")
        raise Exception(f"Failed to load model: {e}")


def evaluate_model(model: NixtlaClient, val_df: pd.DataFrame, config: Dict) -> Dict:
    """
    Evaluates the fine-tuned TimeGPT model on the provided validation data.

    Args:
        model (NixtlaClient): The fine-tuned TimeGPT model.
        val_df (pd.DataFrame): The validation data in Nixtla format (unique_id, ds, y).
        config (Dict): The training configuration dictionary (to get the forecast frequency).

    Returns:
        Dict: A dictionary containing the evaluation metrics (MAE, RMSE).
    """
    try:
        logging.info("Generating forecasts...")
        forecast = model.forecast(df=val_df, h=24, freq=config['freq'])

        merged_df = pd.merge(val_df, forecast, on=['unique_id', 'ds'], how='inner', suffixes=('_actual', '_forecast'))

        mae = mean_absolute_error(merged_df['y_actual'], merged_df['y_forecast'])
        rmse = np.sqrt(mean_squared_error(merged_df['y_actual'], merged_df['y_forecast']))

        metrics = {'MAE': mae, 'RMSE': rmse}
        logging.info(f"Evaluation metrics: {metrics}")
        return metrics

    except Exception as e:
        logging.error(f"Model evaluation failed: {e}")
        raise Exception(f"Model evaluation failed: {e}")


def save_metrics(metrics: Dict, file_path: str) -> None:
    """
    Saves the evaluation metrics to a JSON file.

    Args:
        metrics (Dict): The evaluation metrics dictionary.
        file_path (str): The path to save the metrics.
    """
    try:
        with open(file_path, 'w') as f:
            json.dump(metrics, f, indent=4)
        logging.info(f"Metrics saved to {file_path}")
    except Exception as e:
        logging.error(f"Failed to save metrics: {e}")
        raise Exception(f"Failed to save metrics: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate fine-tuned TimeGPT model.")
    parser.add_argument("--val_data", required=True, help="Path to validation data CSV.")
    parser.add_argument("--model", required=True, help="Path to fine-tuned model pickle file.")
    parser.add_argument("--config", required=True, help="Path to training config JSON.")
    parser.add_argument("--output", default="metrics.json", help="Path to save evaluation metrics.")

    args = parser.parse_args()

    try:
        val_df = pd.read_csv(args.val_data)
        val_df['ds'] = pd.to_datetime(val_df['ds'])
        model = load_model(args.model)
        config = json.load(open(args.config, 'r'))

        metrics = evaluate_model(model, val_df, config)
        save_metrics(metrics, args.output)

    except (FileNotFoundError, ValueError, Exception) as e:
        logging.error(f"Error: {e}")
        exit(1)
