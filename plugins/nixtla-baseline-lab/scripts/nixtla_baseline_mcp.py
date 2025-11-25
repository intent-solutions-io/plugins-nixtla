#!/usr/bin/env python3
"""
Nixtla Baseline Lab MCP Server

Exposes baseline forecasting tools via Model Context Protocol.
Uses Nixtla's open-source libraries to run classical forecasting baselines
on the M4 Daily benchmark dataset.
"""

import json
import sys
import logging
from pathlib import Path
from typing import Dict, Any, List
import csv

# Configure logging to stderr
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)


class NixtlaBaselineMCP:
    """MCP server for Nixtla baseline forecasting."""

    def __init__(self):
        self.version = "0.1.0"
        logger.info(f"Nixtla Baseline MCP Server v{self.version} initializing")

    def get_tools(self) -> List[Dict[str, Any]]:
        """Return list of available tools."""
        return [
            {
                "name": "run_baselines",
                "description": "Run baseline forecasting models (SeasonalNaive, AutoETS, AutoTheta) on M4 Daily dataset or custom CSV",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "horizon": {
                            "type": "integer",
                            "description": "Forecast horizon in days",
                            "default": 14,
                            "minimum": 1,
                            "maximum": 60
                        },
                        "series_limit": {
                            "type": "integer",
                            "description": "Maximum number of series to process",
                            "default": 50,
                            "minimum": 1,
                            "maximum": 500
                        },
                        "output_dir": {
                            "type": "string",
                            "description": "Directory for output files",
                            "default": "nixtla_baseline_m4"
                        },
                        "enable_plots": {
                            "type": "boolean",
                            "description": "Generate PNG forecast plots for a sample of series",
                            "default": False
                        },
                        "dataset_type": {
                            "type": "string",
                            "description": "Dataset type: 'm4' for M4 Daily dataset or 'csv' for custom CSV file",
                            "default": "m4",
                            "enum": ["m4", "csv"]
                        },
                        "csv_path": {
                            "type": "string",
                            "description": "Path to custom CSV file (required when dataset_type='csv'). Must have columns: unique_id, ds, y"
                        }
                    },
                    "required": []
                }
            }
        ]

    def run_baselines(
        self,
        horizon: int = 14,
        series_limit: int = 50,
        output_dir: str = "nixtla_baseline_m4",
        enable_plots: bool = False,
        dataset_type: str = "m4",
        csv_path: str = None
    ) -> Dict[str, Any]:
        """
        Execute baseline forecasting workflow using real Nixtla libraries.

        Args:
            horizon: Forecast horizon in days
            series_limit: Maximum number of series to process
            output_dir: Directory for output files
            enable_plots: Generate PNG forecast plots
            dataset_type: 'm4' for M4 Daily dataset or 'csv' for custom CSV
            csv_path: Path to custom CSV file (required when dataset_type='csv')

        Returns:
            Dict with success status, message, files, and summary
        """
        logger.info(f"Running baselines: horizon={horizon}, series_limit={series_limit}, dataset_type={dataset_type}")

        try:
            # Import Nixtla libraries
            logger.debug("Importing Nixtla libraries...")
            from datasetsforecast.m4 import M4
            from statsforecast import StatsForecast
            from statsforecast.models import SeasonalNaive, AutoETS, AutoTheta
            import pandas as pd
            import numpy as np

            # Create output directory
            out_path = Path(output_dir)
            out_path.mkdir(exist_ok=True)
            logger.debug(f"Output directory: {out_path.absolute()}")

            # Load dataset based on type
            if dataset_type == "csv":
                # Validate CSV path provided
                if not csv_path:
                    return {
                        "success": False,
                        "message": "csv_path is required when dataset_type='csv'"
                    }

                # Load custom CSV
                logger.info(f"Loading custom CSV dataset from: {csv_path}")
                csv_file = Path(csv_path)
                if not csv_file.exists():
                    return {
                        "success": False,
                        "message": f"CSV file not found: {csv_path}"
                    }

                df = pd.read_csv(csv_file)
                logger.info(f"Loaded CSV with {len(df)} rows")

                # Validate required columns
                required_cols = {'unique_id', 'ds', 'y'}
                missing_cols = required_cols - set(df.columns)
                if missing_cols:
                    return {
                        "success": False,
                        "message": f"CSV missing required columns: {missing_cols}. Must have: unique_id, ds, y"
                    }

                logger.info(f"Loaded {len(df['unique_id'].unique())} total series from CSV")
                dataset_name = "Custom CSV"

            else:  # dataset_type == "m4"
                # Determine data directory (store M4 data under plugin root)
                plugin_root = Path(__file__).parent.parent
                data_root = plugin_root / "data"
                data_root.mkdir(exist_ok=True)
                logger.info(f"Data directory: {data_root}")

                # Load M4 Daily dataset
                logger.info("Loading M4 Daily dataset...")
                df, *_ = M4.load(directory=str(data_root), group='Daily')
                logger.info(f"Loaded {len(df['unique_id'].unique())} total series from M4 Daily")
                dataset_name = "M4 Daily"

            # Sample series to limit runtime
            unique_ids = df['unique_id'].unique()[:series_limit]
            df_sample = df[df['unique_id'].isin(unique_ids)].copy()
            logger.info(f"Sampled {len(unique_ids)} series for processing")

            # Define models
            models = [
                SeasonalNaive(season_length=7),  # Weekly seasonality for Daily data
                AutoETS(season_length=7),
                AutoTheta(season_length=7)
            ]
            logger.info(f"Models: SeasonalNaive, AutoETS, AutoTheta (season_length=7)")

            # Create StatsForecast instance
            sf = StatsForecast(
                models=models,
                freq='D',
                n_jobs=-1  # Use all available cores
            )
            logger.info("StatsForecast instance created")

            # Split data into train/test for metric calculation
            # Use last 'horizon' points as test set
            logger.info(f"Splitting data: test set = last {horizon} points")
            df_train = []
            df_test = []

            for uid in unique_ids:
                series_data = df_sample[df_sample['unique_id'] == uid].copy()
                series_data = series_data.sort_values('ds')

                if len(series_data) <= horizon:
                    logger.warning(f"Series {uid} too short ({len(series_data)} points), skipping")
                    continue

                train = series_data.iloc[:-horizon].copy()
                test = series_data.iloc[-horizon:].copy()

                df_train.append(train)
                df_test.append(test)

            df_train = pd.concat(df_train, ignore_index=True)
            df_test = pd.concat(df_test, ignore_index=True)

            logger.info(f"Train set: {len(df_train)} points across {len(df_train['unique_id'].unique())} series")
            logger.info(f"Test set: {len(df_test)} points")

            # Fit models and generate forecasts
            logger.info("Fitting models and generating forecasts...")
            forecasts_df = sf.forecast(df=df_train, h=horizon)
            logger.info(f"Forecasts generated: {len(forecasts_df)} points")

            # Calculate metrics (sMAPE and MASE)
            logger.info("Calculating metrics...")
            metrics_data = []

            for uid in df_train['unique_id'].unique():
                # Get actual test values
                test_values = df_test[df_test['unique_id'] == uid]['y'].values

                if len(test_values) == 0:
                    logger.warning(f"No test values for series {uid}, skipping metrics")
                    continue

                # Get forecasts for this series
                forecast_row = forecasts_df[forecasts_df['unique_id'] == uid]

                if len(forecast_row) == 0:
                    logger.warning(f"No forecasts for series {uid}, skipping metrics")
                    continue

                # Calculate metrics for each model
                for model in ['SeasonalNaive', 'AutoETS', 'AutoTheta']:
                    if model not in forecast_row.columns:
                        continue

                    pred_values = forecast_row[model].values[0] if isinstance(forecast_row[model].values[0], np.ndarray) else forecast_row[model].values

                    # Ensure same length
                    min_len = min(len(test_values), len(pred_values))
                    actual = test_values[:min_len]
                    predicted = pred_values[:min_len]

                    # sMAPE calculation
                    smape = self._calculate_smape(actual, predicted)

                    # MASE calculation (using naive seasonal forecast as baseline)
                    train_values = df_train[df_train['unique_id'] == uid]['y'].values
                    mase = self._calculate_mase(actual, predicted, train_values, season_length=7)

                    metrics_data.append({
                        "series_id": uid,
                        "model": model,
                        "sMAPE": round(smape, 2),
                        "MASE": round(mase, 3)
                    })

            logger.info(f"Calculated metrics for {len(metrics_data)} model/series combinations")

            # Write metrics CSV (use dataset-specific filename)
            dataset_label = "M4_Daily" if dataset_type == "m4" else "Custom"
            metrics_file = out_path / f"results_{dataset_label}_h{horizon}.csv"
            with open(metrics_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=["series_id", "model", "sMAPE", "MASE"])
                writer.writeheader()
                writer.writerows(metrics_data)

            logger.info(f"Wrote metrics to {metrics_file}")

            # Calculate summary statistics
            model_summaries = {}
            models_list = ["SeasonalNaive", "AutoETS", "AutoTheta"]

            for model in models_list:
                model_metrics = [m for m in metrics_data if m["model"] == model]

                if model_metrics:
                    avg_smape = sum(m["sMAPE"] for m in model_metrics) / len(model_metrics)
                    avg_mase = sum(m["MASE"] for m in model_metrics) / len(model_metrics)

                    model_summaries[model] = {
                        "avg_smape": round(avg_smape, 2),
                        "avg_mase": round(avg_mase, 3),
                        "series_count": len(model_metrics)
                    }

            # Write summary text
            summary_file = out_path / f"summary_{dataset_label}_h{horizon}.txt"
            with open(summary_file, 'w') as f:
                f.write(f"Baseline Results Summary\n")
                f.write(f"========================\n\n")
                f.write(f"Dataset: {dataset_name}\n")
                f.write(f"Series: {len(df_train['unique_id'].unique())}\n")
                f.write(f"Horizon: {horizon} days\n\n")
                f.write(f"Average Metrics by Model:\n")
                f.write(f"-" * 60 + "\n")

                for model, stats in sorted(model_summaries.items(), key=lambda x: x[1]["avg_smape"]):
                    f.write(f"  {model:20s} - sMAPE: {stats['avg_smape']:6.2f}%  MASE: {stats['avg_mase']:.3f}\n")

                f.write(f"\n")
                f.write(f"Files generated:\n")
                f.write(f"  - {metrics_file.name}\n")
                f.write(f"  - {summary_file.name}\n")

            logger.info(f"Wrote summary to {summary_file}")

            # Generate plots if requested
            plot_files = []
            if enable_plots:
                plot_files = self._generate_forecast_plots(
                    df_train=df_train,
                    df_test=df_test,
                    forecasts_df=forecasts_df,
                    metrics_data=metrics_data,
                    output_dir=out_path,
                    horizon=horizon,
                    max_series=2
                )

            return {
                "success": True,
                "message": f"Baseline models completed on {dataset_name} ({len(df_train['unique_id'].unique())} series, horizon={horizon})",
                "files": [str(metrics_file), str(summary_file)] + plot_files,
                "summary": model_summaries,
                "plots_generated": len(plot_files)
            }

        except ImportError as e:
            error_msg = f"Missing required library: {e}. Please install with: pip install -r requirements.txt"
            logger.error(error_msg)
            return {
                "success": False,
                "message": error_msg,
                "files": [],
                "summary": {}
            }

        except Exception as e:
            error_msg = f"Error running baselines: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                "success": False,
                "message": error_msg,
                "files": [],
                "summary": {}
            }

    def _calculate_smape(self, actual: List[float], predicted: List[float]) -> float:
        """
        Calculate Symmetric Mean Absolute Percentage Error (sMAPE).

        sMAPE = (100 / n) * Σ(|actual - predicted| / ((|actual| + |predicted|) / 2))

        Args:
            actual: Actual values
            predicted: Predicted values

        Returns:
            sMAPE as percentage (0-200)
        """
        import numpy as np

        actual = np.array(actual)
        predicted = np.array(predicted)

        numerator = np.abs(actual - predicted)
        denominator = (np.abs(actual) + np.abs(predicted)) / 2.0

        # Avoid division by zero
        denominator = np.where(denominator == 0, 1e-10, denominator)

        smape = 100.0 * np.mean(numerator / denominator)
        return smape

    def _calculate_mase(
        self,
        actual: List[float],
        predicted: List[float],
        train_series: List[float],
        season_length: int = 7
    ) -> float:
        """
        Calculate Mean Absolute Scaled Error (MASE).

        MASE = MAE / MAE_naive_seasonal

        Where MAE_naive_seasonal is the MAE of a naive seasonal forecast on the training set.

        Args:
            actual: Actual test values
            predicted: Predicted test values
            train_series: Historical training values
            season_length: Seasonal period length

        Returns:
            MASE value (< 1.0 is better than naive seasonal)
        """
        import numpy as np

        actual = np.array(actual)
        predicted = np.array(predicted)
        train_series = np.array(train_series)

        # MAE of the forecast
        mae_forecast = np.mean(np.abs(actual - predicted))

        # Calculate MAE of naive seasonal forecast on training data
        if len(train_series) <= season_length:
            # Not enough data for seasonal naive, use simple naive
            naive_errors = np.abs(np.diff(train_series))
        else:
            # Seasonal naive: y_t = y_{t-season_length}
            naive_errors = np.abs(train_series[season_length:] - train_series[:-season_length])

        mae_naive = np.mean(naive_errors)

        # Avoid division by zero
        if mae_naive == 0:
            mae_naive = 1e-10

        mase = mae_forecast / mae_naive
        return mase

    def _generate_forecast_plots(
        self,
        df_train,
        df_test,
        forecasts_df,
        metrics_data: List[Dict[str, Any]],
        output_dir: Path,
        horizon: int,
        max_series: int = 2
    ) -> List[str]:
        """
        Generate PNG forecast plots for a sample of series.

        Args:
            df_train: Training data DataFrame
            df_test: Test data DataFrame
            forecasts_df: Forecasts DataFrame
            metrics_data: List of metrics for all series/models
            output_dir: Directory for output files
            horizon: Forecast horizon
            max_series: Maximum number of series to plot

        Returns:
            List of generated plot file paths
        """
        try:
            import matplotlib
            matplotlib.use('Agg')  # Use non-interactive backend
            import matplotlib.pyplot as plt
            import numpy as np
            import pandas as pd

            logger.info(f"Generating forecast plots for up to {max_series} series...")

            plot_files = []
            unique_series = df_train['unique_id'].unique()[:max_series]

            for uid in unique_series:
                try:
                    # Get train and test data
                    train_data = df_train[df_train['unique_id'] == uid]
                    test_data = df_test[df_test['unique_id'] == uid]

                    if len(test_data) == 0:
                        logger.warning(f"No test data for series {uid}, skipping plot")
                        continue

                    # Get forecasts
                    forecast_row = forecasts_df[forecasts_df['unique_id'] == uid]
                    if len(forecast_row) == 0:
                        logger.warning(f"No forecasts for series {uid}, skipping plot")
                        continue

                    # Find best model for this series (lowest sMAPE)
                    series_metrics = [m for m in metrics_data if m['series_id'] == uid]
                    if not series_metrics:
                        continue

                    best_metric = min(series_metrics, key=lambda x: x['sMAPE'])
                    best_model = best_metric['model']

                    # Create plot
                    fig, ax = plt.subplots(figsize=(12, 6))

                    # Plot historical data (train + test)
                    all_historical = pd.concat([train_data, test_data])
                    ax.plot(
                        range(len(all_historical)),
                        all_historical['y'].values,
                        'o-',
                        label='Actual',
                        color='#2E86AB',
                        linewidth=2,
                        markersize=4
                    )

                    # Mark the train/test split
                    train_end_idx = len(train_data)
                    ax.axvline(
                        x=train_end_idx - 0.5,
                        color='gray',
                        linestyle='--',
                        alpha=0.5,
                        label='Train/Test Split'
                    )

                    # Plot forecast
                    forecast_values = forecast_row[best_model].values[0]
                    if isinstance(forecast_values, np.ndarray):
                        forecast_indices = range(train_end_idx, train_end_idx + len(forecast_values))
                        ax.plot(
                            forecast_indices,
                            forecast_values,
                            's-',
                            label=f'Forecast ({best_model})',
                            color='#A23B72',
                            linewidth=2,
                            markersize=6
                        )

                    # Styling
                    ax.set_xlabel('Time Index', fontsize=12)
                    ax.set_ylabel('Value', fontsize=12)
                    ax.set_title(
                        f'Series {uid} - Forecast vs Actual (h={horizon})\n'
                        f'Best Model: {best_model} (sMAPE: {best_metric["sMAPE"]:.2f}%, MASE: {best_metric["MASE"]:.3f})',
                        fontsize=14,
                        fontweight='bold'
                    )
                    ax.legend(loc='best', fontsize=10)
                    ax.grid(True, alpha=0.3)

                    # Save plot
                    plot_file = output_dir / f"plot_series_{uid}.png"
                    plt.tight_layout()
                    plt.savefig(plot_file, dpi=100, bbox_inches='tight')
                    plt.close(fig)

                    plot_files.append(str(plot_file))
                    logger.info(f"Generated plot: {plot_file.name}")

                except Exception as e:
                    logger.warning(f"Failed to generate plot for series {uid}: {e}")
                    continue

            logger.info(f"Generated {len(plot_files)} plots")
            return plot_files

        except ImportError:
            logger.warning("matplotlib not available, skipping plot generation")
            return []
        except Exception as e:
            logger.warning(f"Error generating plots: {e}")
            return []

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP request."""
        method = request.get("method")
        params = request.get("params", {})

        logger.debug(f"Handling request: {method}")

        if method == "tools/list":
            return {"tools": self.get_tools()}

        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})

            if tool_name == "run_baselines":
                result = self.run_baselines(**arguments)
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ]
                }
            else:
                return {"error": f"Unknown tool: {tool_name}"}

        else:
            return {"error": f"Unknown method: {method}"}

    def run(self):
        """Main server loop."""
        logger.info("MCP server started, waiting for requests...")

        for line in sys.stdin:
            try:
                request = json.loads(line)
                response = self.handle_request(request)
                print(json.dumps(response), flush=True)
            except Exception as e:
                logger.error(f"Error handling request: {e}", exc_info=True)
                print(json.dumps({"error": str(e)}), flush=True)


if __name__ == "__main__":
    # Simple test mode for debugging
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        logger.info("Running in test mode...")
        server = NixtlaBaselineMCP()
        # Check if --enable-plots flag is present
        enable_plots = "--enable-plots" in sys.argv
        result = server.run_baselines(
            horizon=7,
            series_limit=5,
            output_dir="nixtla_baseline_m4_test",
            enable_plots=enable_plots
        )
        print(json.dumps(result, indent=2))
    else:
        # Normal MCP server mode
        server = NixtlaBaselineMCP()
        server.run()
