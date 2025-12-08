#!/usr/bin/env python3
"""
Forecasting experiment pipeline runner for Nixtla.
"""
import pandas as pd
import yaml
import os
import argparse
from typing import Dict, Any, Tuple, List
from statsforecast import StatsForecast
from statsforecast.models import AutoETS, AutoARIMA, SeasonalNaive, AutoTheta
from nixtla import NixtlaClient
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt


def load_config(config_path: str) -> Dict[str, Any]:
    """Loads a YAML configuration file."""
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def load_data(data_config: Dict[str, Any]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Loads and preprocesses the time series data."""
    try:
        df = pd.read_csv(data_config["dataset_path"])
        df = df[[data_config["id_col"], data_config["date_col"], data_config["target_col"]]]
        df.rename(columns={
            data_config["id_col"]: "unique_id",
            data_config["date_col"]: "ds",
            data_config["target_col"]: "y"
        }, inplace=True)
        df['ds'] = pd.to_datetime(df['ds'])

        # Split into train and test sets
        train_size = int(len(df) * data_config["train_fraction"])
        train_df = df[:train_size]
        test_df = df[train_size:]

        return train_df, test_df

    except Exception as e:
        raise ValueError(f"Error loading data: {e}")


def train_model(model_config: Dict[str, Any], train_df: pd.DataFrame, freq: str) -> Any:
    """Trains the specified forecasting model."""
    model_type = model_config["model_type"]
    horizon = model_config["horizon"]

    try:
        if model_type == "TimeGPT":
            api_key = os.getenv('NIXTLA_TIMEGPT_API_KEY')
            if not api_key:
                raise ValueError("NIXTLA_TIMEGPT_API_KEY environment variable not set.")
            client = NixtlaClient(api_key=api_key)
            forecast = client.forecast(df=train_df, h=horizon, freq=freq)
            return forecast

        elif model_type in ["AutoARIMA", "AutoETS", "SeasonalNaive", "AutoTheta"]:
            models = []
            if model_type == "AutoARIMA":
                models.append(AutoARIMA())
            elif model_type == "AutoETS":
                models.append(AutoETS())
            elif model_type == "SeasonalNaive":
                models.append(SeasonalNaive())
            elif model_type == "AutoTheta":
                models.append(AutoTheta())

            sf = StatsForecast(models=models, freq=freq, n_jobs=-1)
            forecasts = sf.forecast(df=train_df, h=horizon)
            return forecasts
        else:
            raise ValueError(f"Unsupported model type: {model_type}")

    except Exception as e:
        raise ValueError(f"Error training model: {e}")


def evaluate_model(forecasts: pd.DataFrame, test_df: pd.DataFrame, metrics: List[str], data_config: Dict[str, Any]) -> Dict[str, float]:
    """Evaluates the forecasting performance."""
    results = {}

    # Merge forecasts with test data
    test_df = test_df.rename(columns={data_config.get("target_col", "y"): "y"})
    merged_df = pd.merge(test_df, forecasts, on=['unique_id', 'ds'], how='inner')

    if merged_df.empty:
        print("Warning: No common dates between forecast and test data. Evaluation might be inaccurate.")
        return results

    y_true = merged_df['y'].values
    model_col = next((col for col in forecasts.columns if col not in ['unique_id', 'ds']), None)
    if not model_col:
        print("Warning: Could not identify forecast column")
        return results

    y_pred = merged_df[model_col].values

    if len(y_true) != len(y_pred):
        print("Warning: Length mismatch between true and predicted values. Evaluation might be inaccurate.")
        return results

    for metric in metrics:
        try:
            if metric == "MASE":
                train_data = pd.read_csv(data_config["dataset_path"])
                train_data = train_data[train_data[data_config["id_col"]] == merged_df['unique_id'].iloc[0]]
                train_data = train_data[data_config["target_col"]].values

                if len(train_data) == 0:
                    print(f"Warning: No training data found for series {merged_df['unique_id'].iloc[0]}. MASE cannot be calculated.")
                    results[metric] = float('nan')
                    continue

                mae_naive = mean_absolute_error(train_data[1:], train_data[:-1])
                mae = mean_absolute_error(y_true, y_pred)
                results[metric] = mae / mae_naive if mae_naive != 0 else float('inf')

            elif metric == "sMAPE":
                numerator = abs(y_true - y_pred)
                denominator = (abs(y_true) + abs(y_pred)) / 2
                results[metric] = (numerator / denominator).mean() * 100

            elif metric == "RMSE":
                results[metric] = ((y_true - y_pred) ** 2).mean() ** 0.5
            elif metric == "MAE":
                results[metric] = mean_absolute_error(y_true, y_pred)
            else:
                raise ValueError(f"Unsupported metric: {metric}")
        except Exception as e:
            print(f"Error calculating metric {metric}: {e}")
            results[metric] = float('nan')

    return results


def visualize_forecast(forecasts: pd.DataFrame, test_df: pd.DataFrame, data_config: Dict[str, Any], experiment_name: str) -> None:
    """Visualizes the forecast against the actual values."""
    plt.figure(figsize=(12, 6))

    # Plot actual values
    plt.plot(test_df['ds'], test_df[data_config.get("target_col", "y")], label='Actual', marker='o')

    # Plot forecasted values
    model_col = next((col for col in forecasts.columns if col not in ['unique_id', 'ds']), 'forecast')
    plt.plot(forecasts['ds'], forecasts[model_col], label='Forecast', marker='x')

    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title('Forecast vs Actual')
    plt.legend()
    plt.grid(True)

    # Save the plot
    plot_path = os.path.join(experiment_name, "forecast_visualization.png")
    plt.savefig(plot_path)
    plt.close()

    print(f"Forecast visualization saved to: {plot_path}")


def main(args: argparse.Namespace) -> None:
    """Main function to run the forecasting experiment."""
    experiment_name = args.experiment_name

    # Load configurations
    data_config = load_config(os.path.join(experiment_name, "data.yaml"))
    model_config = load_config(os.path.join(experiment_name, "models.yaml"))
    experiment_config = load_config(os.path.join(experiment_name, "config.yaml"))

    # Load data
    try:
        train_df, test_df = load_data(data_config)
    except ValueError as e:
        print(f"Error loading data: {e}")
        return

    # Train model
    try:
        forecasts = train_model(model_config, train_df, data_config["freq"])
    except ValueError as e:
        print(f"Error training model: {e}")
        return

    # Evaluate model
    try:
        metrics = experiment_config["metrics"]
        evaluation_results = evaluate_model(forecasts, test_df, metrics, data_config)
        print("Evaluation Results:")
        for metric, value in evaluation_results.items():
            print(f"{metric}: {value:.4f}")
    except ValueError as e:
        print(f"Error evaluating model: {e}")

    # Visualize forecast
    try:
        visualize_forecast(forecasts, test_df, data_config, experiment_name)
    except Exception as e:
        print(f"Error visualizing forecast: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nixtla Forecasting Experiment Pipeline")
    parser.add_argument("--experiment_name", type=str, default="forecasting_experiment", help="Name of the experiment directory.")
    args = parser.parse_args()

    main(args)
