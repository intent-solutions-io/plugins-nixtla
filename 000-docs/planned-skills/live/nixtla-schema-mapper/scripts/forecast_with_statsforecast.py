#!/usr/bin/env python3
"""
Forecasting script using StatsForecast on Nixtla-formatted data.
"""
import pandas as pd
from statsforecast import StatsForecast
from statsforecast.models import AutoETS, AutoARIMA, SeasonalNaive, AutoTheta
import logging
import argparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def forecast_with_statsforecast(input_file: str, h: int = 14) -> pd.DataFrame:
    """
    Forecasts time series data using StatsForecast.

    Args:
        input_file (str): Path to the input CSV file in Nixtla format (unique_id, ds, y).
        h (int): Forecast horizon (number of periods to forecast).

    Returns:
        pd.DataFrame: Forecasts in a Pandas DataFrame.

    Raises:
        FileNotFoundError: If the input file does not exist.
        ValueError: If the input file is not in the correct Nixtla format.
        Exception: For any other errors during forecasting.
    """
    try:
        df = pd.read_csv(input_file)

        # Validate Nixtla format
        required_columns = ['unique_id', 'ds', 'y']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Input file must have columns: {required_columns}")

        # Convert 'ds' to datetime
        df['ds'] = pd.to_datetime(df['ds'])

        # Determine frequency (most common difference between datetimes)
        df['time_diff'] = df.groupby('unique_id')['ds'].diff().dt.total_seconds()
        most_common_diff = df['time_diff'].mode()[0] if not df['time_diff'].dropna().empty else None
        if most_common_diff is None:
            freq = 'D'  # Default to daily if no time difference can be determined
            logging.warning("Could not automatically determine frequency. Defaulting to daily ('D').")
        else:
            if most_common_diff == 86400:
                freq = 'D'
            elif most_common_diff == 3600:
                freq = 'H'
            elif most_common_diff == 60:
                freq = 'T'
            else:
                freq = 'D'  # Default if frequency is unusual
                logging.warning("Could not automatically determine frequency. Defaulting to daily ('D').")

        # Initialize StatsForecast with models
        sf = StatsForecast(
            models=[AutoETS(), AutoARIMA(), SeasonalNaive(), AutoTheta()],
            freq=freq,
            n_jobs=-1  # Use all available cores
        )

        # Forecast
        forecasts = sf.forecast(df=df, h=h)
        logging.info(f"Successfully generated forecasts using StatsForecast with horizon {h}")
        return forecasts

    except FileNotFoundError:
        logging.error(f"Input file not found: {input_file}")
        raise
    except ValueError as e:
        logging.error(f"Error in input data format: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def main():
    parser = argparse.ArgumentParser(description="Forecast time series data using StatsForecast.")
    parser.add_argument("--input", required=True, help="Path to the input CSV file in Nixtla format.")
    parser.add_argument("--horizon", type=int, default=14, help="Forecast horizon (number of periods to forecast).")

    args = parser.parse_args()

    try:
        forecasts = forecast_with_statsforecast(args.input, args.horizon)
        print(forecasts.head())  # Display the first few rows of the forecasts
        forecasts.to_csv("statsforecast_forecasts.csv")
        logging.info("Forecasts saved to statsforecast_forecasts.csv")

    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
