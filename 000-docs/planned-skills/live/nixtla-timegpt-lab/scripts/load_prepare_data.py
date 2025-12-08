#!/usr/bin/env python3
"""
Data loading and preparation for time series forecasting.
"""
import pandas as pd
import numpy as np
import argparse
from typing import Optional


def load_and_prepare_data(input_csv: str, freq: Optional[str] = None) -> pd.DataFrame:
    """
    Loads time series data from a CSV file, preprocesses it, and infers frequency if not provided.

    Args:
        input_csv (str): Path to the input CSV file.
        freq (Optional[str]): Frequency of the time series data (e.g., 'D', 'W', 'M', 'H'). If None, it will be inferred.

    Returns:
        pd.DataFrame: A DataFrame with columns 'unique_id', 'ds', and 'y', ready for forecasting.

    Raises:
        FileNotFoundError: If the input CSV file does not exist.
        ValueError: If the input CSV does not contain the required columns or if the inferred frequency is invalid.
    """
    try:
        df = pd.read_csv(input_csv)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The file {input_csv} was not found.")

    required_columns = ['unique_id', 'ds', 'y']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"Error: The input CSV must contain columns named {required_columns}")

    df['ds'] = pd.to_datetime(df['ds'])

    # Handle missing values using linear interpolation
    df['y'] = df['y'].interpolate(method='linear')

    # Ensure 'unique_id' is a string
    df['unique_id'] = df['unique_id'].astype(str)

    # Infer frequency if not provided
    if freq is None:
        inferred_freq = pd.infer_freq(df['ds'])
        if inferred_freq is None:
            raise ValueError("Error: Could not infer the frequency of the time series. Please provide it using the --freq parameter.")
        freq = inferred_freq
        print(f"Inferred frequency: {freq}")

    # Validate frequency
    try:
        pd.date_range(df['ds'].min(), df['ds'].max(), freq=freq)
    except ValueError:
        raise ValueError(f"Error: Invalid frequency '{freq}'. Please provide a valid frequency (e.g., 'D', 'W', 'M', 'H').")

    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load and prepare time series data.")
    parser.add_argument("--input", required=True, help="Path to the input CSV file.")
    parser.add_argument("--freq", help="Frequency of the time series data (e.g., 'D', 'W', 'M', 'H'). If not provided, it will be inferred.")
    parser.add_argument("--output", default="prepared_data.csv", help="Path to save prepared data.")

    args = parser.parse_args()

    try:
        df = load_and_prepare_data(args.input, args.freq)
        df.to_csv(args.output, index=False)
        print(f"Data loaded and prepared successfully. Saved to {args.output}")
        print(df.head())
    except (FileNotFoundError, ValueError) as e:
        print(e)
        exit(1)
