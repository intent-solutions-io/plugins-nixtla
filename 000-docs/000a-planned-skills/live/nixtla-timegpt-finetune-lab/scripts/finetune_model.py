#!/usr/bin/env python3
"""
TimeGPT fine-tuning execution script.
"""
import pandas as pd
import os
import pickle
import json
from nixtla import NixtlaClient
from typing import Dict
import logging
import argparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def finetune_timegpt(train_df: pd.DataFrame, config: Dict) -> NixtlaClient:
    """
    Fine-tunes the TimeGPT model on the provided training data.

    Args:
        train_df (pd.DataFrame): The training data in Nixtla format (unique_id, ds, y).
        config (Dict): The training configuration dictionary.

    Returns:
        NixtlaClient: The fine-tuned TimeGPT model.

    Raises:
        ValueError: If the training data is empty or if the API key is not set.
        Exception: If the fine-tuning process fails.
    """
    logging.info("Starting TimeGPT fine-tuning process...")

    if train_df.empty:
        raise ValueError("Training data is empty. Please provide a valid training dataset.")

    api_key = os.getenv('NIXTLA_TIMEGPT_API_KEY')
    if not api_key:
        raise ValueError("NIXTLA_TIMEGPT_API_KEY not set. Please set the environment variable.")

    try:
        client = NixtlaClient(api_key=api_key)

        logging.info(f"Using the following configuration: {config}")

        # Fine-tuning parameters
        finetune_options = {
            'learning_rate': config['learning_rate'],
            'epochs': config['epochs'],
            'batch_size': config['batch_size'],
            'num_workers': config['num_workers']
        }

        # Execute fine-tuning
        logging.info("Initiating fine-tuning...")
        client.finetune(df=train_df, model_name=config['model_name'], finetune_options=finetune_options)
        logging.info("Fine-tuning completed successfully.")

        return client

    except Exception as e:
        logging.error(f"Fine-tuning failed: {e}")
        raise Exception(f"Fine-tuning failed: {e}")


def save_model(model: NixtlaClient, file_path: str) -> None:
    """
    Saves the fine-tuned TimeGPT model to a pickle file.

    Args:
        model (NixtlaClient): The fine-tuned TimeGPT model.
        file_path (str): The path to save the model.
    """
    try:
        with open(file_path, 'wb') as f:
            pickle.dump(model, f)
        logging.info(f"Model saved to {file_path}")
    except Exception as e:
        logging.error(f"Failed to save model: {e}")
        raise Exception(f"Failed to save model: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fine-tune TimeGPT model.")
    parser.add_argument("--train_data", required=True, help="Path to training data CSV.")
    parser.add_argument("--config", required=True, help="Path to training config JSON.")
    parser.add_argument("--output", default="finetuned_model.pkl", help="Path to save fine-tuned model.")

    args = parser.parse_args()

    try:
        train_df = pd.read_csv(args.train_data)
        train_df['ds'] = pd.to_datetime(train_df['ds'])
        config = json.load(open(args.config, 'r'))

        finetuned_model = finetune_timegpt(train_df, config)
        save_model(finetuned_model, args.output)

    except (FileNotFoundError, ValueError, Exception) as e:
        logging.error(f"Error: {e}")
        exit(1)
