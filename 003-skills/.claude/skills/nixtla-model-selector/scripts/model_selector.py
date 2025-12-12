#!/usr/bin/env python3
"""
Nixtla Model Selector - Automated forecasting model selection and execution.

This script automatically selects the best forecasting model (StatsForecast or TimeGPT)
based on time series data characteristics and executes the selected model.

Usage:
    python model_selector.py --input input.csv --output forecast.csv
    python model_selector.py --input input.csv --horizon 30 --visualize
"""

import argparse
import os
import sys
from typing import Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def load_and_analyze_data(file_path: str, visualize: bool = False) -> Tuple[pd.DataFrame, str]:
    """
    Loads time series data from a CSV file, analyzes its characteristics,
    and returns the DataFrame and inferred frequency.

    Args:
        file_path: Path to the CSV file containing time series data
        visualize: If True, generates and saves a visualization plot

    Returns:
        Tuple containing the DataFrame and inferred frequency string

    Raises:
        FileNotFoundError: If the input file does not exist
        ValueError: If data format is invalid or frequency cannot be inferred
    """
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file not found: {file_path}")
    except Exception as e:
        raise ValueError(f"Error reading CSV: {e}")

    # Validate required columns
    required_columns = ["unique_id", "ds", "y"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(
                f"Input CSV must contain columns: {required_columns}. "
                f"Found: {df.columns.tolist()}"
            )

    # Convert 'ds' to datetime
    try:
        df["ds"] = pd.to_datetime(df["ds"])
    except Exception as e:
        raise ValueError(f"Error converting 'ds' column to datetime: {e}")

    # Infer frequency
    try:
        inferred_freq = pd.infer_freq(df["ds"])
        if inferred_freq is None:
            raise ValueError("Could not infer frequency from the time series data.")
    except Exception as e:
        raise ValueError(f"Error inferring frequency: {e}")

    # Basic data analysis
    print(f"Data loaded successfully from {file_path}")
    print(f"Data shape: {df.shape}")
    print(f"Inferred frequency: {inferred_freq}")
    print(f"Unique series: {df['unique_id'].nunique()}")
    print(f"Date range: {df['ds'].min()} to {df['ds'].max()}")
    print(f"First few rows:\n{df.head()}\n")

    # Optionally plot the time series data
    if visualize:
        unique_ids = df["unique_id"].unique()
        num_series = len(unique_ids)
        fig, axes = plt.subplots(
            num_series, 1, figsize=(12, 3 * num_series), sharex=True, squeeze=False
        )

        for i, unique_id in enumerate(unique_ids):
            series_data = df[df["unique_id"] == unique_id]
            ax = axes[i, 0]
            ax.plot(series_data["ds"], series_data["y"])
            ax.set_title(f"Time Series for {unique_id}")
            ax.set_xlabel("Date")
            ax.set_ylabel("Value")
            ax.grid(True)

        plt.tight_layout()
        plot_path = "time_series_plot.png"
        plt.savefig(plot_path)
        print(f"Time series plot saved to {plot_path}\n")
        plt.close()

    return df, inferred_freq


def select_model(df: pd.DataFrame, inferred_freq: str) -> Tuple[str, str]:
    """
    Selects the appropriate forecasting model based on data characteristics.

    Decision logic:
    - StatsForecast: Missing values, short data (<30 points), seasonality, many series (>100)
    - TimeGPT: Long data without clear seasonality

    Args:
        df: DataFrame containing time series data
        inferred_freq: Inferred frequency of the time series

    Returns:
        Tuple containing the selected model name and selection reason
    """
    data_length = len(df)
    unique_ids = df["unique_id"].nunique()

    print("=== Model Selection Analysis ===")
    print(f"Data length: {data_length}")
    print(f"Number of series: {unique_ids}")
    print(f"Missing values: {df['y'].isnull().sum()}")

    # Check for missing values
    if df["y"].isnull().any():
        reason = "StatsForecast selected due to missing values in the target variable."
        print(f"Decision: {reason}\n")
        return "StatsForecast", reason

    # Check for short time series
    if data_length < 30:
        reason = "StatsForecast selected due to short data length (<30 observations)."
        print(f"Decision: {reason}\n")
        return "StatsForecast", reason

    # Check for seasonality using seasonal decomposition
    seasonality_present = False
    try:
        from statsmodels.tsa.seasonal import seasonal_decompose

        # Decompose the first time series
        first_series = df[df["unique_id"] == df["unique_id"].iloc[0]]["y"].values

        # Need sufficient data for seasonal decomposition
        if len(first_series) >= 24:  # At least 2 periods for decomposition
            period = 12 if len(first_series) >= 24 else 7
            decomposition = seasonal_decompose(
                first_series, model="additive", period=period, extrapolate_trend="freq"
            )
            seasonal_component = decomposition.seasonal

            # Check if seasonal component has significant variation
            seasonality_present = seasonal_component.std() > 0.1 * first_series.std()
            print(
                f"Seasonality check (period={period}): {'Present' if seasonality_present else 'Not detected'}"
            )
    except Exception as e:
        print(f"Warning: Could not perform seasonality check: {e}")
        seasonality_present = False

    if seasonality_present:
        reason = "StatsForecast selected due to presence of seasonality."
        print(f"Decision: {reason}\n")
        return "StatsForecast", reason

    # Check for number of series
    if unique_ids > 100:
        reason = "StatsForecast selected due to large number of time series (>100)."
        print(f"Decision: {reason}\n")
        return "StatsForecast", reason

    # Default to TimeGPT for longer, non-seasonal data
    reason = "TimeGPT selected due to long data length and lack of clear seasonality."
    print(f"Decision: {reason}\n")
    return "TimeGPT", reason


def execute_forecast(
    df: pd.DataFrame, model_name: str, inferred_freq: str, horizon: int = 14
) -> pd.DataFrame:
    """
    Executes the selected forecasting model on the input data.

    Args:
        df: DataFrame containing time series data
        model_name: Name of selected model ("StatsForecast" or "TimeGPT")
        inferred_freq: Inferred frequency of the time series
        horizon: Number of periods to forecast

    Returns:
        DataFrame containing the forecasts

    Raises:
        ValueError: If model name is invalid or TimeGPT API key is missing
        Exception: If any error occurs during forecasting
    """
    print(f"=== Executing {model_name} ===")
    print(f"Forecast horizon: {horizon} periods\n")

    try:
        if model_name == "StatsForecast":
            from statsforecast import StatsForecast
            from statsforecast.models import AutoARIMA, AutoETS

            # Initialize StatsForecast with appropriate models
            sf = StatsForecast(models=[AutoETS(), AutoARIMA()], freq=inferred_freq, n_jobs=-1)

            # Generate forecasts
            print("Fitting models...")
            forecasts = sf.forecast(df=df, h=horizon)

            # Convert to desired output format
            forecasts = forecasts.reset_index()
            forecasts["timestamp"] = pd.Timestamp.now()

            # Melt to long format for consistency
            id_vars = ["unique_id", "ds"] if "ds" in forecasts.columns else ["unique_id"]
            forecasts_long = forecasts.melt(
                id_vars=id_vars,
                value_vars=["AutoETS", "AutoARIMA"],
                var_name="model",
                value_name="yhat",
            )

            print(f"Forecast complete. Generated {len(forecasts)} predictions.\n")
            return forecasts_long

        elif model_name == "TimeGPT":
            from nixtla import NixtlaClient

            api_key = os.getenv("NIXTLA_TIMEGPT_API_KEY")
            if not api_key:
                raise ValueError(
                    "NIXTLA_TIMEGPT_API_KEY not set. "
                    "Please set the environment variable before running."
                )

            client = NixtlaClient(api_key=api_key)

            # Generate forecasts
            print("Calling TimeGPT API...")
            forecast = client.forecast(df=df, h=horizon, freq=inferred_freq)

            # Convert to desired output format
            forecast = forecast.reset_index()
            forecast = forecast.rename(columns={"TimeGPT": "yhat"})
            forecast["ds"] = pd.to_datetime(forecast["ds"])
            forecast["model"] = "TimeGPT"
            forecast = forecast[["unique_id", "ds", "model", "yhat"]]

            print(f"Forecast complete. Generated {len(forecast)} predictions.\n")
            return forecast

        else:
            raise ValueError(
                f"Invalid model name: {model_name}. " f"Must be 'StatsForecast' or 'TimeGPT'."
            )

    except Exception as e:
        raise Exception(f"Error during forecasting with {model_name}: {e}")


def generate_output(
    forecasts: pd.DataFrame,
    model_name: str,
    reason: str,
    output_file_path: str = "forecast.csv",
    model_selection_file_path: str = "model_selection.txt",
) -> None:
    """
    Saves forecasts and model selection information to files.

    Args:
        forecasts: DataFrame containing the forecasts
        model_name: Name of the selected model
        reason: Reason for model selection
        output_file_path: Path to save forecasts CSV file
        model_selection_file_path: Path to save model selection text file

    Returns:
        None
    """
    try:
        # Save forecasts to CSV
        forecasts.to_csv(output_file_path, index=False)
        print(f"Forecasts saved to {output_file_path}")
        print(f"Forecast summary:\n{forecasts.head()}\n")

        # Write model selection information to text file
        with open(model_selection_file_path, "w") as f:
            f.write(f"Selected model: {model_name}\n")
            f.write(f"Reason: {reason}\n")
            f.write(f"Forecast records: {len(forecasts)}\n")
        print(f"Model selection information saved to {model_selection_file_path}\n")

    except Exception as e:
        print(f"Error generating output: {e}")
        raise


def main():
    """Main entry point for the model selector script."""
    parser = argparse.ArgumentParser(
        description="Automatically select and execute the best forecasting model",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python model_selector.py --input data.csv

  # Custom output path and horizon
  python model_selector.py --input data.csv --output results.csv --horizon 30

  # With visualization
  python model_selector.py --input data.csv --visualize
        """,
    )

    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to input CSV file with columns: unique_id, ds, y",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="forecast.csv",
        help="Path to output forecast CSV file (default: forecast.csv)",
    )
    parser.add_argument(
        "--selection-output",
        type=str,
        default="model_selection.txt",
        help="Path to model selection text file (default: model_selection.txt)",
    )
    parser.add_argument(
        "--horizon", type=int, default=14, help="Forecast horizon in periods (default: 14)"
    )
    parser.add_argument(
        "--visualize", action="store_true", help="Generate visualization plot of input data"
    )

    args = parser.parse_args()

    try:
        # Step 1: Load and analyze data
        print("Step 1: Loading and analyzing data...\n")
        df, inferred_freq = load_and_analyze_data(args.input, args.visualize)

        # Step 2: Select model
        print("Step 2: Selecting forecasting model...\n")
        model_name, reason = select_model(df, inferred_freq)

        # Step 3: Execute forecast
        print("Step 3: Executing forecast...\n")
        forecasts = execute_forecast(df, model_name, inferred_freq, args.horizon)

        # Step 4: Generate output
        print("Step 4: Generating output...\n")
        generate_output(forecasts, model_name, reason, args.output, args.selection_output)

        print("=== Model Selection Complete ===")
        print(f"Model: {model_name}")
        print(f"Reason: {reason}")
        print(f"Output: {args.output}")

    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"ERROR: Unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    main()
