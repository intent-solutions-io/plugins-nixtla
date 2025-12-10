#!/usr/bin/env python3
"""
Data preparation script for TimeGPT fine-tuning.
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from typing import Tuple
import matplotlib.pyplot as plt
import argparse


def load_and_preprocess_data(file_path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Loads time series data from a CSV file, preprocesses it, and splits it into training and validation sets.

    Args:
        file_path (str): The path to the CSV file containing the time series data.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: A tuple containing the training and validation DataFrames.

    Raises:
        FileNotFoundError: If the specified file path does not exist.
        ValueError: If the data format is invalid (missing columns, incorrect data types).
    """
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found at path: {file_path}")
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {e}")

    # Check for required columns
    required_columns = ['unique_id', 'ds', 'y']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Convert 'ds' column to datetime
    try:
        df['ds'] = pd.to_datetime(df['ds'])
    except ValueError:
        raise ValueError("Could not convert 'ds' column to datetime. Ensure it's in a recognizable format.")

    # Ensure 'y' column is numeric
    try:
        df['y'] = pd.to_numeric(df['y'])
    except ValueError:
        raise ValueError("Could not convert 'y' column to numeric.")

    # Basic data cleaning (remove rows with missing values)
    df = df.dropna()

    # Split data into training and validation sets (80/20 split)
    train_df, val_df = train_test_split(df, test_size=0.2, shuffle=False, random_state=42)

    # Visualize the data
    unique_ids = train_df['unique_id'].unique()
    num_series = len(unique_ids)
    num_plots = min(num_series, 3)

    fig, axes = plt.subplots(num_plots, 1, figsize=(12, 4 * num_plots))
    if num_plots == 1:
        axes = [axes]

    for i in range(num_plots):
        series_id = unique_ids[i]
        series_data = train_df[train_df['unique_id'] == series_id]
        axes[i].plot(series_data['ds'], series_data['y'])
        axes[i].set_title(f"Time Series: {series_id}")
        axes[i].set_xlabel("Date")
        axes[i].set_ylabel("Value")
        axes[i].tick_params(axis='x', rotation=45)
        axes[i].grid(True)

    plt.tight_layout()
    plt.savefig("time_series_visualization.png")
    print("Time series visualization saved to time_series_visualization.png")

    return train_df, val_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare data for TimeGPT fine-tuning.")
    parser.add_argument("--input", required=True, help="Path to input CSV file.")
    parser.add_argument("--train_output", default="train_data.csv", help="Path to save training data.")
    parser.add_argument("--val_output", default="val_data.csv", help="Path to save validation data.")

    args = parser.parse_args()

    try:
        train_data, val_data = load_and_preprocess_data(args.input)
        train_data.to_csv(args.train_output, index=False)
        val_data.to_csv(args.val_output, index=False)
        print(f"Data prepared successfully. Training data shape: {train_data.shape}, Validation data shape: {val_data.shape}")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        exit(1)
