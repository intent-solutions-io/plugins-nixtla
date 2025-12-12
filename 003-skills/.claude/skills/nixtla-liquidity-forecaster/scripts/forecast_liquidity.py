"""Forecast liquidity using TimeGPT.

This module generates forecasts for orderbook depth and spread using
Nixtla's TimeGPT API. It also produces visualizations and reports.
"""

import argparse
import logging
import os
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd

from nixtla import NixtlaClient

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def forecast_liquidity(df: pd.DataFrame, horizon: int) -> Optional[pd.DataFrame]:
    """Forecast liquidity (depth and spread) using TimeGPT.

    Args:
        df: A Pandas DataFrame containing the preprocessed orderbook data
            in Nixtla format with columns: unique_id, ds, y, spread, depth.
        horizon: The forecast horizon (number of periods to forecast).

    Returns:
        A Pandas DataFrame containing the forecasted values, or None if an error occurs.

    Raises:
        ValueError: If the API key is missing or required columns are absent.
    """
    try:
        api_key = os.getenv("NIXTLA_TIMEGPT_API_KEY")
        if not api_key:
            raise ValueError(
                "TimeGPT API Key missing. Set the NIXTLA_TIMEGPT_API_KEY environment variable."
            )

        client = NixtlaClient(api_key=api_key)

        # Ensure the DataFrame has the correct columns and data types
        if not all(col in df.columns for col in ["unique_id", "ds", "y"]):
            raise ValueError("DataFrame must contain 'unique_id', 'ds', and 'y' columns.")

        df["ds"] = pd.to_datetime(df["ds"])

        # Forecast using TimeGPT
        forecast = client.forecast(df=df, h=horizon, freq="T")  # Assuming 1 minute frequency

        return forecast

    except ValueError as e:
        logging.error(f"Error: {e}")
        return None
    except Exception as e:
        logging.error(f"TimeGPT forecast failed: {e}")
        return None


def plot_forecast(df: pd.DataFrame, forecast: pd.DataFrame, file_prefix: str) -> None:
    """Plot the historical data and the forecast.

    Args:
        df: The historical data with columns: ds, y.
        forecast: The forecast data with columns: ds, y.
        file_prefix: The prefix for the output file name.
    """
    try:
        plt.figure(figsize=(12, 6))
        plt.plot(df["ds"], df["y"], label="Historical Data")
        plt.plot(forecast["ds"], forecast["y"], label="Forecast", color="red")
        plt.xlabel("Time")
        plt.ylabel("Mid Price")
        plt.title("Mid Price Forecast")
        plt.legend()
        plt.grid(True)
        plt.savefig(f"{file_prefix}_forecast.png")
        plt.close()
        logging.info(f"Forecast plot saved to {file_prefix}_forecast.png")
    except Exception as e:
        logging.error(f"Error plotting forecast: {e}")


def generate_report(preprocessed_data: pd.DataFrame, horizon: int, output_files: dict) -> None:
    """Generate a text report summarizing the forecasting process.

    Args:
        preprocessed_data: The preprocessed input data.
        horizon: The forecast horizon used.
        output_files: Dictionary mapping output types to file paths.
    """
    try:
        with open("report.txt", "w") as f:
            f.write("Liquidity Forecasting Report\n")
            f.write("=" * 50 + "\n")
            f.write(f"Market ID: {preprocessed_data['unique_id'].iloc[0]}\n")
            f.write(f"Forecast Horizon: {horizon}\n")
            f.write(f"Forecast saved to: {output_files.get('forecast', 'N/A')}\n")
            f.write(f"Plot saved to: {output_files.get('plot', 'N/A')}\n")
        logging.info("Report saved to report.txt")
    except Exception as e:
        logging.error(f"Error generating report: {e}")


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Forecast liquidity using TimeGPT.")
    parser.add_argument(
        "--input_file",
        required=True,
        help="Path to the preprocessed data CSV file.",
    )
    parser.add_argument("--horizon", type=int, required=True, help="The forecast horizon.")
    parser.add_argument(
        "--output",
        default="depth_forecast.csv",
        help="Output forecast CSV file path (default: depth_forecast.csv)",
    )
    parser.add_argument(
        "--plot_prefix",
        default="depth",
        help="Prefix for plot file (default: depth)",
    )
    args = parser.parse_args()

    try:
        # Load the preprocessed data
        preprocessed_data = pd.read_csv(args.input_file)

        # Forecast liquidity
        forecast_data = forecast_liquidity(preprocessed_data, args.horizon)

        if forecast_data is not None:
            # Save the forecast to a CSV file
            forecast_data.to_csv(args.output, index=False)
            logging.info(f"Forecasted depth saved to {args.output}")

            # Plot the forecast
            plot_prefix = args.plot_prefix
            plot_forecast(preprocessed_data, forecast_data, plot_prefix)

            # Create a report
            output_files = {
                "forecast": args.output,
                "plot": f"{plot_prefix}_forecast.png",
            }
            generate_report(preprocessed_data, args.horizon, output_files)

        else:
            logging.error("Forecasting failed. Check the logs for details.")
            raise RuntimeError("Forecasting failed")

    except FileNotFoundError:
        logging.error(f"Input file not found: {args.input_file}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


if __name__ == "__main__":
    main()
