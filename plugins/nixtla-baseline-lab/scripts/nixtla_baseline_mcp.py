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

    def _get_library_versions(self) -> Dict[str, str]:
        """Get versions of Nixtla OSS and related libraries.

        Returns:
            Dict mapping library names to version strings.
            Uses "unknown" or "not_installed" for missing/unavailable versions.
        """
        versions = {}

        # Try to get statsforecast version
        try:
            import statsforecast
            versions["statsforecast"] = getattr(statsforecast, "__version__", "unknown")
        except ImportError:
            versions["statsforecast"] = "not_installed"

        # Try to get datasetsforecast version
        try:
            import datasetsforecast
            versions["datasetsforecast"] = getattr(datasetsforecast, "__version__", "unknown")
        except ImportError:
            versions["datasetsforecast"] = "not_installed"

        # Try to get pandas version
        try:
            import pandas
            versions["pandas"] = getattr(pandas, "__version__", "unknown")
        except ImportError:
            versions["pandas"] = "not_installed"

        # Try to get numpy version
        try:
            import numpy
            versions["numpy"] = getattr(numpy, "__version__", "unknown")
        except ImportError:
            versions["numpy"] = "not_installed"

        return versions

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
                        },
                        "include_timegpt": {
                            "type": "boolean",
                            "description": "Include TimeGPT comparison (requires NIXTLA_TIMEGPT_API_KEY)",
                            "default": False
                        },
                        "timegpt_max_series": {
                            "type": "integer",
                            "description": "Maximum series for TimeGPT (cost/time cap)",
                            "default": 5,
                            "minimum": 1,
                            "maximum": 20
                        },
                        "models": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": ["SeasonalNaive", "AutoETS", "AutoTheta"]
                            },
                            "description": "List of statsforecast models to run. Available: SeasonalNaive, AutoETS, AutoTheta",
                            "default": ["SeasonalNaive", "AutoETS", "AutoTheta"]
                        },
                        "freq": {
                            "type": "string",
                            "description": "Frequency string for time series (D=daily, M=monthly, H=hourly, etc.)",
                            "default": "D"
                        },
                        "season_length": {
                            "type": "integer",
                            "description": "Seasonal period length for models and MASE calculation (e.g., 7 for weekly pattern in daily data)",
                            "default": 7,
                            "minimum": 1
                        },
                        "demo_preset": {
                            "type": ["string", "null"],
                            "description": "Demo preset configuration for quick GitHub-style demos. 'm4_daily_small' runs a fast demo on M4 Daily subset",
                            "enum": ["m4_daily_small", null],
                            "default": null
                        }
                    },
                    "required": []
                }
            },
            {
                "name": "get_nixtla_compatibility_info",
                "description": "Get version information for Nixtla OSS libraries (statsforecast, datasetsforecast) and dependencies (pandas, numpy) used by this plugin",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "generate_benchmark_report",
                "description": "Generate a Nixtla-style benchmark report in Markdown format from metrics CSV",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "metrics_csv_path": {
                            "type": "string",
                            "description": "Path to metrics CSV file (e.g., 'nixtla_baseline_m4_test/results_M4_Daily_h7.csv'). If not provided, attempts to use most recent run."
                        },
                        "dataset_label": {
                            "type": "string",
                            "description": "Dataset name for the report (e.g., 'M4 Daily'). If not provided, inferred from file name.",
                            "default": ""
                        },
                        "horizon": {
                            "type": "integer",
                            "description": "Forecast horizon. If not provided, inferred from file name.",
                            "default": 0
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
        csv_path: str = None,
        include_timegpt: bool = False,
        timegpt_max_series: int = 5,
        models: List[str] = None,
        freq: str = "D",
        season_length: int = 7,
        demo_preset: str = None
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
            include_timegpt: Include TimeGPT comparison (requires API key)
            timegpt_max_series: Max series for TimeGPT (cost/time cap)
            models: List of model names to run (SeasonalNaive, AutoETS, AutoTheta)
            freq: Frequency string for time series (D, M, H, etc.)
            season_length: Seasonal period for models and MASE calculation
            demo_preset: Demo preset ('m4_daily_small' for GitHub-style demo)

        Returns:
            Dict with success status, message, files, summary, and resolved parameters
        """
        # Apply demo preset if specified
        if demo_preset == "m4_daily_small":
            logger.info("🎬 Running Nixtla statsforecast GitHub-style demo: M4 Daily subset")
            dataset_type = "m4"
            models = ["SeasonalNaive", "AutoETS", "AutoTheta"]
            freq = "D"
            season_length = 7
            series_limit = 5
            horizon = 7
            logger.info("Demo preset applied: 5 series, 7-day horizon, all models")

        # Set default models if not provided
        if models is None:
            models = ["SeasonalNaive", "AutoETS", "AutoTheta"]

        # Validate models
        ALLOWED_MODELS = {"SeasonalNaive", "AutoETS", "AutoTheta"}
        invalid_models = [m for m in models if m not in ALLOWED_MODELS]
        if invalid_models:
            return {
                "success": False,
                "message": f"Invalid model names: {invalid_models}. Allowed: {sorted(ALLOWED_MODELS)}"
            }

        logger.info(f"Running baselines: horizon={horizon}, series_limit={series_limit}, dataset_type={dataset_type}, include_timegpt={include_timegpt}")
        logger.info(f"Power-user params: models={models}, freq={freq}, season_length={season_length}")

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

            # Define models dynamically based on user input
            # Map model names to model classes
            MODEL_MAP = {
                "SeasonalNaive": SeasonalNaive,
                "AutoETS": AutoETS,
                "AutoTheta": AutoTheta
            }

            # Instantiate requested models with user-specified season_length
            model_instances = [
                MODEL_MAP[model_name](season_length=season_length)
                for model_name in models
            ]
            logger.info(f"Models: {', '.join(models)} (season_length={season_length})")

            # Create StatsForecast instance with user-specified frequency
            sf = StatsForecast(
                models=model_instances,
                freq=freq,
                n_jobs=-1  # Use all available cores
            )
            logger.info(f"StatsForecast instance created (freq={freq})")

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

            # TimeGPT comparison if requested
            timegpt_result = self._run_timegpt_comparison(
                include_timegpt=include_timegpt,
                df_train=df_train,
                df_test=df_test,
                metrics_data=metrics_data,
                model_summaries=model_summaries,
                horizon=horizon,
                timegpt_max_series=timegpt_max_series,
                output_dir=out_path,
                dataset_label=dataset_label,
                dataset_name=dataset_name
            )

            # Build response
            response = {
                "success": True,
                "message": f"Baseline models completed on {dataset_name} ({len(df_train['unique_id'].unique())} series, horizon={horizon})",
                "files": [str(metrics_file), str(summary_file)] + plot_files,
                "summary": model_summaries,
                "plots_generated": len(plot_files),
                "resolved_models": models,
                "resolved_freq": freq,
                "resolved_season_length": season_length,
                "demo_preset": demo_preset,
                "compatibility_hint": "Run get_nixtla_compatibility_info tool for detailed version info."
            }

            # Add TimeGPT fields if comparison was attempted
            if timegpt_result:
                response.update(timegpt_result)

            return response

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

    def get_nixtla_compatibility_info(self) -> Dict[str, Any]:
        """
        Get version information for Nixtla OSS libraries and dependencies.

        Returns:
            Dict with success status, engine name, library versions, and notes.
        """
        logger.info("Getting Nixtla compatibility info...")

        try:
            library_versions = self._get_library_versions()

            return {
                "success": True,
                "engine": "nixtla.statsforecast",
                "library_versions": library_versions,
                "notes": "These are the versions currently importable by the Nixtla Baseline Lab MCP server."
            }
        except Exception as e:
            error_msg = f"Error getting compatibility info: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                "success": False,
                "message": error_msg,
                "library_versions": {}
            }

    def generate_benchmark_report(
        self,
        metrics_csv_path: str = "",
        dataset_label: str = "",
        horizon: int = 0
    ) -> Dict[str, Any]:
        """
        Generate a Nixtla-style benchmark report in Markdown format.

        Args:
            metrics_csv_path: Path to metrics CSV file. If empty, uses most recent.
            dataset_label: Dataset name for report. If empty, inferred from file name.
            horizon: Forecast horizon. If 0, inferred from file name.

        Returns:
            Dict with success status, report_path, and message.
        """
        logger.info("Generating benchmark report...")

        try:
            import pandas as pd
            from datetime import datetime, timezone

            # Find metrics CSV if not provided
            if not metrics_csv_path:
                # Look for most recent results CSV in common output directories
                possible_dirs = ["nixtla_baseline_m4", "nixtla_baseline_m4_test"]
                csv_files = []
                for dir_name in possible_dirs:
                    dir_path = Path(dir_name)
                    if dir_path.exists():
                        csv_files.extend(dir_path.glob("results_*.csv"))

                if not csv_files:
                    return {
                        "success": False,
                        "message": "No metrics CSV found. Please provide metrics_csv_path or run baselines first."
                    }

                # Use most recent
                metrics_csv_path = str(max(csv_files, key=lambda p: p.stat().st_mtime))
                logger.info(f"Using most recent metrics CSV: {metrics_csv_path}")

            # Validate CSV exists
            csv_path = Path(metrics_csv_path)
            if not csv_path.exists():
                return {
                    "success": False,
                    "message": f"Metrics CSV not found: {metrics_csv_path}"
                }

            # Infer parameters from filename if not provided
            # Expected format: results_M4_Daily_h7.csv or results_Custom_h14.csv
            filename = csv_path.stem  # e.g., "results_M4_Daily_h7"
            if not dataset_label and "_h" in filename:
                # Extract dataset name (everything between "results_" and "_h")
                parts = filename.split("_h")[0].replace("results_", "")
                dataset_label = parts.replace("_", " ")

            if horizon == 0 and "_h" in filename:
                # Extract horizon (number after "_h")
                try:
                    horizon = int(filename.split("_h")[1])
                except (IndexError, ValueError):
                    horizon = 0

            # Read metrics CSV
            df = pd.read_csv(csv_path)
            logger.info(f"Loaded {len(df)} rows from metrics CSV")

            # Calculate average metrics per model
            model_stats = {}
            for model in df['model'].unique():
                model_data = df[df['model'] == model]
                model_stats[model] = {
                    'smape_avg': model_data['sMAPE'].mean(),
                    'mase_avg': model_data['MASE'].mean(),
                    'series_count': len(model_data)
                }

            # Sort models by sMAPE (best first)
            sorted_models = sorted(model_stats.keys(), key=lambda m: model_stats[m]['smape_avg'])

            # Get library versions
            versions = self._get_library_versions()
            statsforecast_version = versions.get("statsforecast", "unknown")

            # Generate timestamp
            timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

            # Build Markdown report
            report_lines = [
                "# Nixtla Baseline Lab – StatsForecast Benchmark Report",
                "",
                f"- **Dataset**: {dataset_label or 'Unknown'}",
                f"- **Horizon**: {horizon if horizon > 0 else 'Unknown'}",
                f"- **Series**: {df['series_id'].nunique()}",
                f"- **StatsForecast Version**: {statsforecast_version}",
                f"- **Generated At**: {timestamp}",
                "",
                "## Average Metrics by Model",
                "",
                "| Model | sMAPE (%) | MASE | Series |",
                "|-------|-----------|------|--------|"
            ]

            # Add model rows (sorted by performance)
            for model in sorted_models:
                stats = model_stats[model]
                report_lines.append(
                    f"| {model:<13} | {stats['smape_avg']:>9.2f} | {stats['mase_avg']:>4.3f} | {stats['series_count']:>6} |"
                )

            # Add highlights section
            best_model = sorted_models[0]
            best_smape = model_stats[best_model]['smape_avg']
            best_mase = model_stats[best_model]['mase_avg']

            report_lines.extend([
                "",
                "## Highlights",
                "",
                f"- **{best_model}** performed best on average sMAPE ({best_smape:.2f}%)",
                f"- All models achieved sMAPE < {df['sMAPE'].max():.1f}%"
            ])

            # Check which models beat naive seasonal (MASE < 1.0)
            models_beat_naive = [m for m in model_stats if model_stats[m]['mase_avg'] < 1.0]
            if models_beat_naive:
                report_lines.append(f"- {', '.join(models_beat_naive)} beat SeasonalNaive baseline (MASE < 1.0)")

            report_lines.extend([
                "",
                "## Notes",
                "",
                "- Generated by Nixtla Baseline Lab (Claude Code plugin)",
                "- Uses Nixtla's statsforecast and datasetsforecast libraries",
                ""
            ])

            # Write report to file
            output_dir = csv_path.parent
            # Create deterministic filename based on dataset and horizon
            if horizon > 0:
                report_filename = f"benchmark_report_{dataset_label.replace(' ', '_')}_h{horizon}.md"
            else:
                report_filename = f"benchmark_report_{dataset_label.replace(' ', '_')}.md"

            report_path = output_dir / report_filename
            report_path.write_text("\n".join(report_lines))

            logger.info(f"Wrote benchmark report to {report_path}")

            return {
                "success": True,
                "report_path": str(report_path),
                "message": f"Benchmark report generated: {report_path.name}",
                "dataset": dataset_label,
                "horizon": horizon,
                "series_count": df['series_id'].nunique(),
                "models_evaluated": len(model_stats)
            }

        except ImportError as e:
            error_msg = f"Missing required library: {e}. Please install with: pip install -r requirements.txt"
            logger.error(error_msg)
            return {
                "success": False,
                "message": error_msg
            }
        except Exception as e:
            error_msg = f"Error generating benchmark report: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                "success": False,
                "message": error_msg
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

    def _run_timegpt_comparison(
        self,
        include_timegpt: bool,
        df_train,
        df_test,
        metrics_data: List[Dict[str, Any]],
        model_summaries: Dict[str, Any],
        horizon: int,
        timegpt_max_series: int,
        output_dir: Path,
        dataset_label: str,
        dataset_name: str
    ) -> Dict[str, Any]:
        """
        Run TimeGPT comparison if requested and generate showdown report.

        Returns dict with timegpt_status, timegpt_summary, timegpt_per_series, or None.
        """
        if not include_timegpt:
            return None

        try:
            # Import TimeGPT client
            from timegpt_client import create_timegpt_client
            import pandas as pd
            import numpy as np

            client = create_timegpt_client()

            # Check if API is available
            if not client.is_available():
                logger.warning("TimeGPT comparison requested but API key not found")
                return {
                    "timegpt_status": "skipped_no_api_key",
                    "timegpt_message": "NIXTLA_TIMEGPT_API_KEY environment variable not set"
                }

            logger.info(f"Starting TimeGPT comparison (max {timegpt_max_series} series)")

            # Select series for TimeGPT (limited by timegpt_max_series)
            unique_series = df_train['unique_id'].unique()
            timegpt_series = unique_series[:min(len(unique_series), timegpt_max_series)]
            logger.info(f"Selected {len(timegpt_series)} series for TimeGPT: {list(timegpt_series)}")

            # Prepare data for TimeGPT (train data only)
            df_timegpt_input = df_train[df_train['unique_id'].isin(timegpt_series)].copy()

            # Call TimeGPT API
            timegpt_response = client.forecast(
                df=df_timegpt_input,
                horizon=horizon,
                freq='D'
            )

            if not timegpt_response["success"]:
                logger.error(f"TimeGPT API error: {timegpt_response.get('error', 'Unknown error')}")
                return {
                    "timegpt_status": "error",
                    "timegpt_error": timegpt_response.get("error", "Unknown error")
                }

            forecast_df = timegpt_response["forecast"]
            logger.info(f"TimeGPT forecast received: {len(forecast_df)} predictions")

            # Compute TimeGPT metrics for each series
            timegpt_per_series = []
            timegpt_smapes = []
            timegpt_mases = []

            for uid in timegpt_series:
                # Get test data
                test_data = df_test[df_test['unique_id'] == uid]
                if len(test_data) == 0:
                    continue

                actual = test_data['y'].values

                # Get TimeGPT forecast
                timegpt_forecast = forecast_df[forecast_df['unique_id'] == uid]
                if len(timegpt_forecast) == 0:
                    logger.warning(f"No TimeGPT forecast for series {uid}")
                    continue

                predicted = timegpt_forecast['TimeGPT'].values[:len(actual)]

                # Calculate metrics
                smape = self._calculate_smape(actual, predicted)
                train_values = df_train[df_train['unique_id'] == uid]['y'].values
                mase = self._calculate_mase(actual, predicted, train_values, season_length=7)

                timegpt_smapes.append(smape)
                timegpt_mases.append(mase)

                # Get baseline metrics for this series
                baseline_metrics = [m for m in metrics_data if m["series_id"] == uid]
                baseline_best = min(baseline_metrics, key=lambda x: x["sMAPE"]) if baseline_metrics else None

                # Determine winner
                if baseline_best:
                    winner = "timegpt" if smape < baseline_best["sMAPE"] else "baseline"
                    if abs(smape - baseline_best["sMAPE"]) < 0.1:  # Close call
                        winner = "tie"
                else:
                    winner = "unknown"

                timegpt_per_series.append({
                    "series_id": uid,
                    "baseline_model": baseline_best["model"] if baseline_best else "unknown",
                    "baseline_sMAPE": round(baseline_best["sMAPE"], 2) if baseline_best else None,
                    "baseline_MASE": round(baseline_best["MASE"], 3) if baseline_best else None,
                    "timegpt_sMAPE": round(smape, 2),
                    "timegpt_MASE": round(mase, 3),
                    "winner": winner
                })

            # Calculate TimeGPT averages
            avg_timegpt_smape = round(sum(timegpt_smapes) / len(timegpt_smapes), 2) if timegpt_smapes else 0
            avg_timegpt_mase = round(sum(timegpt_mases) / len(timegpt_mases), 3) if timegpt_mases else 0

            # Get baseline best average (from model_summaries)
            baseline_best_model = min(model_summaries.items(), key=lambda x: x[1]["avg_smape"])
            baseline_best_smape = baseline_best_model[1]["avg_smape"]

            # Determine overall winner
            overall_winner = "timegpt" if avg_timegpt_smape < baseline_best_smape else "baseline"
            if abs(avg_timegpt_smape - baseline_best_smape) < 0.1:
                overall_winner = "tie"

            timegpt_summary = {
                "num_series": len(timegpt_series),
                "avg_sMAPE": avg_timegpt_smape,
                "avg_MASE": avg_timegpt_mase,
                "winner": overall_winner
            }

            logger.info(f"TimeGPT comparison complete: winner={overall_winner}, avg_sMAPE={avg_timegpt_smape}")

            # Generate showdown text report
            showdown_file = output_dir / f"timegpt_showdown_{dataset_label}_h{horizon}.txt"
            with open(showdown_file, 'w') as f:
                f.write(f"TimeGPT Showdown Report\n")
                f.write(f"======================\n\n")
                f.write(f"Dataset: {dataset_name}\n")
                f.write(f"Horizon: {horizon} days\n")
                f.write(f"Series Compared: {len(timegpt_series)} (subset)\n\n")

                f.write(f"Baseline Best Model: {baseline_best_model[0]}\n")
                f.write(f"  Avg sMAPE: {baseline_best_smape:.2f}%\n")
                f.write(f"  Avg MASE: {baseline_best_model[1]['avg_mase']:.3f}\n\n")

                f.write(f"TimeGPT:\n")
                f.write(f"  Avg sMAPE: {avg_timegpt_smape:.2f}%\n")
                f.write(f"  Avg MASE: {avg_timegpt_mase:.3f}\n\n")

                f.write(f"Winner: {overall_winner.upper()}\n\n")

                f.write(f"Per-Series Breakdown:\n")
                f.write(f"-" * 60 + "\n")
                for item in timegpt_per_series:
                    f.write(f"  {item['series_id']}: {item['winner']} ")
                    f.write(f"(Baseline: {item['baseline_sMAPE']:.2f}%, TimeGPT: {item['timegpt_sMAPE']:.2f}%)\n")

                f.write(f"\n")
                f.write(f"Note: This is a limited comparison on {len(timegpt_series)} series.\n")
                f.write(f"Not a comprehensive benchmark. Results may vary on full dataset.\n")

            logger.info(f"Wrote TimeGPT showdown to {showdown_file}")

            return {
                "timegpt_status": "ok",
                "timegpt_summary": timegpt_summary,
                "timegpt_per_series": timegpt_per_series,
                "timegpt_showdown_file": str(showdown_file)
            }

        except ImportError as e:
            logger.error(f"TimeGPT import error: {e}")
            return {
                "timegpt_status": "error",
                "timegpt_error": f"Missing TimeGPT dependencies: {e}"
            }
        except Exception as e:
            logger.error(f"TimeGPT comparison failed: {e}", exc_info=True)
            return {
                "timegpt_status": "error",
                "timegpt_error": str(e)
            }

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
        # Check for optional flags
        enable_plots = "--enable-plots" in sys.argv
        include_timegpt = "--include-timegpt" in sys.argv
        result = server.run_baselines(
            horizon=7,
            series_limit=5,
            output_dir="nixtla_baseline_m4_test",
            enable_plots=enable_plots,
            include_timegpt=include_timegpt,
            timegpt_max_series=3  # Limit for testing
        )
        print(json.dumps(result, indent=2))
    else:
        # Normal MCP server mode
        server = NixtlaBaselineMCP()
        server.run()
