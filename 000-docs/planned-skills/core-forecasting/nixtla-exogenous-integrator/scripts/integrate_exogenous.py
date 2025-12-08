"""
Generate TimeGPT forecasts with integrated exogenous variables.

Usage:
    python integrate_exogenous.py --input data.csv --exogenous holidays.csv --horizon 14 --freq D
"""
import pandas as pd
import os
import argparse
from typing import Optional, List
from nixtla import NixtlaClient
import matplotlib.pyplot as plt


def load_data(input_file: str, exogenous_file: Optional[str] = None) -> tuple[pd.DataFrame, Optional[pd.DataFrame]]:
    """Loads data from CSV files."""
    try:
        df = pd.read_csv(input_file)
        df['ds'] = pd.to_datetime(df['ds'])
    except FileNotFoundError:
        raise FileNotFoundError(f"Historical data file not found: {input_file}")
    except KeyError:
        raise ValueError("Historical data must contain 'unique_id', 'ds', and 'y' columns.")
    except Exception as e:
        raise ValueError(f"Error reading historical data: {e}")

    if exogenous_file:
        try:
            exog_df = pd.read_csv(exogenous_file)
            exog_df['ds'] = pd.to_datetime(exog_df['ds'])
        except FileNotFoundError:
            raise FileNotFoundError(f"Exogenous data file not found: {exogenous_file}")
        except KeyError:
            raise ValueError("Exogenous data must contain a 'ds' column.")
        except Exception as e:
            raise ValueError(f"Error reading exogenous data: {e}")
    else:
        exog_df = None

    return df, exog_df


def align_data(df: pd.DataFrame, exog_df: Optional[pd.DataFrame]) -> pd.DataFrame:
    """Merges historical and exogenous dataframes."""
    if exog_df is None:
        return df

    if 'ds' not in df.columns or 'ds' not in exog_df.columns:
        raise ValueError("Both historical and exogenous dataframes must have a 'ds' column.")

    common_columns = set(df.columns) & set(exog_df.columns)
    if len(common_columns - {'ds', 'unique_id', 'y'}) > 0:
        raise ValueError(f"Overlapping column names (excluding 'ds', 'unique_id', and 'y') found in both dataframes: {common_columns - {'ds', 'unique_id', 'y'}}")

    merged_df = pd.merge(df, exog_df, on='ds', how='left')
    return merged_df


def prepare_timegpt_data(df: pd.DataFrame, exog_cols: Optional[List[str]] = None) -> pd.DataFrame:
    """Prepares data for TimeGPT API call."""
    if df.empty:
        raise ValueError("Input DataFrame is empty.")

    required_columns = ['unique_id', 'ds', 'y']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"DataFrame must contain columns: {required_columns}")

    df['ds'] = pd.to_datetime(df['ds'])
    df['y'] = pd.to_numeric(df['y'], errors='raise')

    if exog_cols:
        for col in exog_cols:
            if col not in df.columns:
                raise ValueError(f"Exogenous variable column '{col}' not found in DataFrame.")
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].fillna(df[col].mean())
    return df


def generate_forecast(df: pd.DataFrame, h: int, freq: str, exog_cols: Optional[List[str]] = None) -> pd.DataFrame:
    """Generates forecast using TimeGPT API."""
    api_key = os.environ.get('NIXTLA_TIMEGPT_API_KEY')
    if not api_key:
        raise ValueError("NIXTLA_TIMEGPT_API_KEY environment variable not set.")

    client = NixtlaClient(api_key=api_key)

    try:
        if exog_cols:
            forecast = client.forecast(df=df, h=h, freq=freq, X_df=df[['ds'] + exog_cols])
        else:
            forecast = client.forecast(df=df, h=h, freq=freq)
        return forecast
    except Exception as e:
        raise RuntimeError(f"TimeGPT API call failed: {e}")


def plot_forecast(df: pd.DataFrame, forecast_df: pd.DataFrame, unique_id: str, exog_cols: Optional[List[str]] = None) -> None:
    """Plots the historical data and the forecast."""
    historical_data = df[df['unique_id'] == unique_id].set_index('ds')['y']
    forecast_data = forecast_df[forecast_df['unique_id'] == unique_id].set_index('ds')['TimeGPT']

    plt.figure(figsize=(12, 6))
    plt.plot(historical_data.index, historical_data.values, label='Historical Data')
    plt.plot(forecast_data.index, forecast_data.values, label='Forecast', color='red')

    if exog_cols:
        for exog_col in exog_cols:
            exog_data = df[df['unique_id'] == unique_id].set_index('ds')[exog_col]
            plt.plot(exog_data.index, exog_data.values, label=exog_col, linestyle='--')

    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title(f'Forecast for {unique_id}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig('forecast_plot.png')
    print("Forecast plot saved to forecast_plot.png")


def main(input_file: str, exogenous_file: Optional[str], horizon: int, freq: str) -> None:
    """Main function to orchestrate the forecasting process."""
    try:
        # Load data
        df, exog_df = load_data(input_file, exogenous_file)

        # Align data
        merged_df = align_data(df, exog_df)

        # Determine exogenous columns
        exog_cols = []
        if exog_df is not None:
            exog_cols = [col for col in exog_df.columns if col != 'ds']

        # Prepare data for TimeGPT
        prepared_df = prepare_timegpt_data(merged_df, exog_cols)

        # Generate forecast
        forecast_df = generate_forecast(prepared_df, horizon, freq, exog_cols)

        # Save forecast to CSV
        forecast_df.to_csv('forecast_exogenous.csv', index=False)
        print("Forecast saved to forecast_exogenous.csv")

        # Plot forecast
        unique_id = df['unique_id'].iloc[0]
        plot_forecast(prepared_df, forecast_df, unique_id, exog_cols)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
    except RuntimeError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate time series forecast with exogenous variables using TimeGPT.")
    parser.add_argument("--input", required=True, help="Path to the historical data CSV file.")
    parser.add_argument("--exogenous", required=False, help="Path to the exogenous variables CSV file.")
    parser.add_argument("--horizon", type=int, required=True, help="Forecast horizon.")
    parser.add_argument("--freq", type=str, required=True, help="Frequency of the time series (e.g., 'D' for daily, 'H' for hourly).")

    args = parser.parse_args()

    main(args.input, args.exogenous, args.horizon, args.freq)
