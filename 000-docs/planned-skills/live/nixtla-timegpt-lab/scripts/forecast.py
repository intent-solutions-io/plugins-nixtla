#!/usr/bin/env python3
"""
Time series forecasting using TimeGPT, StatsForecast, or MLForecast.
"""
import argparse
import os
import pandas as pd
from typing import Literal
from statsforecast import StatsForecast
from statsforecast.models import AutoETS, AutoARIMA
from nixtla import NixtlaClient
import json
import matplotlib.pyplot as plt


def execute_forecasting(input_csv: str, model_name: Literal['timegpt', 'statsforecast', 'mlforecast'], horizon: int, freq: str, output_prefix: str = "forecast") -> None:
    """
    Executes time series forecasting using the specified model (TimeGPT, StatsForecast, or MLForecast).

    Args:
        input_csv (str): Path to the input CSV file.
        model_name (Literal['timegpt', 'statsforecast', 'mlforecast']): The name of the forecasting model to use.
        horizon (int): The forecasting horizon (number of periods to predict).
        freq (str): The frequency of the time series data (e.g., 'D', 'W', 'M', 'H').
        output_prefix (str): Prefix for output files (forecast.csv, plot.png, metrics.json).
    """

    try:
        df = pd.read_csv(input_csv)
        df['ds'] = pd.to_datetime(df['ds'])
        df['unique_id'] = df['unique_id'].astype(str)
        df = df.sort_values(['unique_id', 'ds'])
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The file {input_csv} was not found.")
    except ValueError as e:
        raise ValueError(f"Error: Could not read the input data: {e}")

    try:
        if model_name == 'timegpt':
            api_key = os.getenv('NIXTLA_TIMEGPT_API_KEY')
            if not api_key:
                raise ValueError("Error: NIXTLA_TIMEGPT_API_KEY environment variable not set.")
            client = NixtlaClient(api_key=api_key)
            forecast = client.forecast(df=df, h=horizon, freq=freq)
            forecast_df = forecast
            model_used = "TimeGPT"

        elif model_name == 'statsforecast':
            sf = StatsForecast(models=[AutoETS(), AutoARIMA()], freq=freq, n_jobs=-1)
            forecasts = sf.forecast(df=df, h=horizon)
            forecast_df = forecasts.reset_index()
            forecast_df = forecast_df.rename(columns={'index': 'ds'})
            forecast_df['ds'] = pd.to_datetime(forecast_df['ds'])
            model_used = "StatsForecast"

        elif model_name == 'mlforecast':
            raise NotImplementedError("MLForecast is not yet implemented.")
        else:
            raise ValueError(f"Error: Invalid model name '{model_name}'. Choose from 'timegpt', 'statsforecast', or 'mlforecast'.")

        # Save forecast to CSV
        forecast_csv_path = f"{output_prefix}.csv"
        forecast_df.to_csv(forecast_csv_path, index=False)
        print(f"Forecast saved to {forecast_csv_path}")

        # Generate and save visualization
        plot_path = f"{output_prefix}.png"
        plt.figure(figsize=(12, 6))
        for unique_id in df['unique_id'].unique():
            df_subset = df[df['unique_id'] == unique_id]
            forecast_subset = forecast_df[forecast_df['unique_id'] == unique_id]

            plt.plot(df_subset['ds'], df_subset['y'], label=f'{unique_id} - Actual')
            if model_used in forecast_subset.columns:
                plt.plot(forecast_subset['ds'], forecast_subset[model_used], label=f'{unique_id} - Predicted')

        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.title('Actual vs Predicted')
        plt.legend()
        plt.savefig(plot_path)
        plt.close()
        print(f"Visualization saved to {plot_path}")

        # Calculate and save metrics (example: MAE)
        metrics = {}
        for unique_id in df['unique_id'].unique():
            df_subset = df[df['unique_id'] == unique_id].set_index('ds')
            forecast_subset = forecast_df[forecast_df['unique_id'] == unique_id].set_index('ds')

            common_index = df_subset.index.intersection(forecast_subset.index)
            df_subset = df_subset.loc[common_index]
            forecast_subset = forecast_subset.loc[common_index]

            if not df_subset.empty and not forecast_subset.empty and model_used in forecast_subset.columns:
                mae = abs(df_subset['y'] - forecast_subset[model_used]).mean()
                metrics[unique_id] = {'MAE': mae}
            else:
                metrics[unique_id] = {'MAE': None}

        metrics_json_path = f"{output_prefix}_metrics.json"
        with open(metrics_json_path, 'w') as f:
            json.dump(metrics, f, indent=4)
        print(f"Metrics saved to {metrics_json_path}")

    except Exception as e:
        print(f"An error occurred during forecasting: {e}")
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute time series forecasting.")
    parser.add_argument("--input", required=True, help="Path to the input CSV file.")
    parser.add_argument("--model", required=True, choices=['timegpt', 'statsforecast', 'mlforecast'], help="Forecasting model to use (timegpt, statsforecast, mlforecast).")
    parser.add_argument("--horizon", required=True, type=int, help="Forecasting horizon (number of periods to predict).")
    parser.add_argument("--freq", required=True, help="Frequency of the time series data (e.g., 'D', 'W', 'M', 'H').")
    parser.add_argument("--output_prefix", default="forecast", help="Prefix for output files (forecast.csv, plot.png, metrics.json).")

    args = parser.parse_args()

    try:
        execute_forecasting(args.input, args.model, args.horizon, args.freq, args.output_prefix)
        print("Forecasting completed successfully.")
    except (FileNotFoundError, ValueError, NotImplementedError) as e:
        print(e)
        exit(1)
