"""
Quantify forecast uncertainty using conformal prediction.

Usage:
    python quantify_uncertainty.py --input forecast.csv --confidence 0.95 --method quantile
"""
import pandas as pd
import numpy as np
import argparse
import json
from typing import Dict
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


def calculate_conformal_intervals(
    df: pd.DataFrame,
    forecast_col: str,
    confidence: float = 0.90,
    method: str = 'quantile'
) -> pd.DataFrame:
    """
    Calculates conformal prediction intervals for time series forecasts.

    Args:
        df (pd.DataFrame): DataFrame containing historical data and forecasts.
                           Must include 'unique_id', 'ds', 'y', and forecast_col.
        forecast_col (str): Name of the column containing the point forecasts.
        confidence (float): Desired confidence level (e.g., 0.90 for 90% confidence).
        method (str): Conformal prediction method ('quantile' or 'jackknife+').

    Returns:
        pd.DataFrame: DataFrame with added columns for lower and upper bounds of the prediction interval.
    """
    try:
        if not 0 < confidence < 1:
            raise ValueError("Confidence level must be between 0 and 1.")

        if method not in ['quantile', 'jackknife+']:
            raise ValueError("Unsupported conformal prediction method. Choose 'quantile' or 'jackknife+'.")

        required_columns = ['unique_id', 'ds', 'y', forecast_col]
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Input DataFrame must contain columns: {required_columns}")

        alpha = 1 - confidence

        if method == 'quantile':
            # Split data into calibration and evaluation sets
            train_df, cal_df = train_test_split(df, test_size=0.5, shuffle=False)

            # Calculate residuals on the calibration set
            cal_df['residual'] = cal_df['y'] - cal_df[forecast_col]

            # Calculate the quantile of the absolute residuals
            q = np.quantile(np.abs(cal_df['residual']), 1 - alpha)

            # Add lower and upper bounds to the original DataFrame
            df[f'lower_bound_{int(confidence*100)}'] = df[forecast_col] - q
            df[f'upper_bound_{int(confidence*100)}'] = df[forecast_col] + q

        elif method == 'jackknife+':
            n = len(df)
            residuals = []
            for i in range(n):
                # Leave-one-out
                train_df = df.drop(index=i)
                test_point = df.iloc[[i]]

                # Train a simple model (e.g., mean forecast)
                mean_forecast = train_df['y'].mean()

                # Calculate residual
                residual = abs(test_point['y'].values[0] - mean_forecast)
                residuals.append(residual)

            # Calculate the (1-alpha) quantile of the residuals
            q = np.quantile(residuals, 1 - alpha)

            # Add lower and upper bounds to the original DataFrame
            df[f'lower_bound_{int(confidence*100)}'] = df[forecast_col] - q
            df[f'upper_bound_{int(confidence*100)}'] = df[forecast_col] + q

        return df

    except ValueError as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def evaluate_calibration(df: pd.DataFrame, confidence: float, forecast_col: str) -> Dict[str, float]:
    """
    Evaluates the calibration of the prediction intervals.

    Args:
        df (pd.DataFrame): DataFrame with actual values and prediction intervals.
        confidence (float): Confidence level of the prediction intervals.
        forecast_col (str): Name of the forecast column.

    Returns:
        Dict[str, float]: Dictionary containing calibration metrics (coverage, interval width).
    """
    lower_bound_col = f'lower_bound_{int(confidence*100)}'
    upper_bound_col = f'upper_bound_{int(confidence*100)}'

    df['inside'] = (df['y'] >= df[lower_bound_col]) & (df['y'] <= df[upper_bound_col])
    coverage = df['inside'].mean()
    interval_width = (df[upper_bound_col] - df[lower_bound_col]).mean()

    return {'coverage': coverage, 'interval_width': interval_width}


def plot_uncertainty(df: pd.DataFrame, forecast_col: str, confidence: float, output_file: str) -> None:
    """
    Generates a plot of the forecast with confidence bands.

    Args:
        df (pd.DataFrame): DataFrame containing the forecast and uncertainty bounds.
        forecast_col (str): Name of the forecast column.
        confidence (float): Confidence level of the prediction intervals.
        output_file (str): Path to save the plot.
    """
    try:
        lower_bound_col = f'lower_bound_{int(confidence*100)}'
        upper_bound_col = f'upper_bound_{int(confidence*100)}'

        plt.figure(figsize=(12, 6))
        plt.plot(df['ds'], df['y'], label='Actual', marker='o')
        plt.plot(df['ds'], df[forecast_col], label='Forecast', marker='x')
        plt.fill_between(df['ds'], df[lower_bound_col], df[upper_bound_col],
                         alpha=0.3, color='gray', label=f'{confidence*100}% Confidence Interval')
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.title('Forecast with Confidence Bands')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(output_file)
        print(f"Uncertainty plot saved to {output_file}")

    except Exception as e:
        print(f"Error generating plot: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Quantify forecast uncertainty using conformal prediction.')
    parser.add_argument('--input', type=str, required=True, help='Path to the input CSV file containing forecasts.')
    parser.add_argument('--confidence', type=float, default=0.90, help='Confidence level (e.g., 0.90 for 90% confidence).')
    parser.add_argument('--method', type=str, default='quantile', choices=['quantile', 'jackknife+'], help='Conformal prediction method (quantile or jackknife+).')
    parser.add_argument('--forecast_col', type=str, default='StatsForecast', help='Name of the forecast column.')
    args = parser.parse_args()

    try:
        forecast_df = pd.read_csv(args.input)
        forecast_df['ds'] = pd.to_datetime(forecast_df['ds'])

        # Calculate conformal intervals
        forecast_with_uncertainty = calculate_conformal_intervals(
            df=forecast_df.copy(),
            forecast_col=args.forecast_col,
            confidence=args.confidence,
            method=args.method
        )

        if forecast_with_uncertainty is not None:
            # Save the forecast with uncertainty to a CSV file
            output_csv_file = 'forecast_with_uncertainty.csv'
            forecast_with_uncertainty.to_csv(output_csv_file, index=False)
            print(f"Forecast with uncertainty saved to {output_csv_file}")

            # Evaluate calibration
            calibration_metrics = evaluate_calibration(forecast_with_uncertainty, args.confidence, args.forecast_col)
            print(f"Calibration metrics: {calibration_metrics}")

            # Save calibration metrics to JSON
            with open('calibration_metrics.json', 'w') as f:
                json.dump(calibration_metrics, f)
            print("Calibration metrics saved to calibration_metrics.json")

            # Generate and save the uncertainty plot
            plot_uncertainty(forecast_with_uncertainty, args.forecast_col, args.confidence, 'uncertainty_plot.png')

    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found.")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
