#!/usr/bin/env python3
"""
Generate YAML configuration file for Nixtla forecasting experiments.

This script creates a forecasting experiment configuration file from command-line
arguments, using sensible defaults for optional parameters. The generated config
can be used with scaffold_experiment.py to create runnable experiment code.

Usage:
    python generate_config.py --data data/sales.csv --target sales --horizon 14 --freq D
    python generate_config.py --data data/energy.csv --target consumption \\
        --horizon 24 --freq H --id_col meter_id --output config.yml
"""

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate Nixtla forecasting experiment configuration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Daily sales forecast
  python generate_config.py --data data/sales.csv --target revenue --horizon 30 --freq D

  # Hourly energy forecast with multiple series
  python generate_config.py --data data/energy.csv --target consumption \\
      --horizon 24 --freq H --id_col meter_id

  # Monthly forecast with custom output location
  python generate_config.py --data data/monthly.csv --target value \\
      --horizon 12 --freq M --output forecasting/config.yml

Frequency codes:
  D  - Daily
  H  - Hourly
  W  - Weekly
  M  - Monthly (month end)
  MS - Monthly (month start)
  Q  - Quarterly
  Y  - Yearly
        """,
    )

    # Required arguments
    parser.add_argument(
        "--data",
        required=True,
        help="Path to data file (CSV or Parquet)",
    )
    parser.add_argument(
        "--target",
        required=True,
        help="Target column name for forecasting",
    )
    parser.add_argument(
        "--horizon",
        type=int,
        required=True,
        help="Forecast horizon (number of periods ahead)",
    )
    parser.add_argument(
        "--freq",
        required=True,
        choices=["D", "H", "W", "M", "MS", "Q", "Y"],
        help="Frequency of the time series",
    )

    # Optional arguments
    parser.add_argument(
        "--id_col",
        default=None,
        help="Column name for series identifier (use for multiple series)",
    )
    parser.add_argument(
        "--ds_col",
        default="date",
        help="Timestamp column name (default: 'date')",
    )
    parser.add_argument(
        "--exog_vars",
        nargs="+",
        default=[],
        help="Exogenous variables to include in forecasting",
    )
    parser.add_argument(
        "--cv_windows",
        type=int,
        default=4,
        help="Number of cross-validation windows (default: 4)",
    )
    parser.add_argument(
        "--cv_method",
        choices=["rolling", "expanding"],
        default="rolling",
        help="Cross-validation method (default: rolling)",
    )
    parser.add_argument(
        "--enable_mlforecast",
        action="store_true",
        help="Enable MLForecast models (requires mlforecast package)",
    )
    parser.add_argument(
        "--enable_timegpt",
        action="store_true",
        help="Enable TimeGPT (requires NIXTLA_API_KEY)",
    )
    parser.add_argument(
        "--output",
        default="forecasting/config.yml",
        help="Output path for config file (default: forecasting/config.yml)",
    )

    return parser.parse_args()


def detect_season_length(freq: str) -> int:
    """
    Determine appropriate season length based on frequency.

    Args:
        freq: Pandas frequency string

    Returns:
        Season length for seasonal models
    """
    season_map = {
        "H": 24,  # Hourly: 24 hours in a day
        "D": 7,  # Daily: 7 days in a week
        "W": 52,  # Weekly: 52 weeks in a year
        "M": 12,  # Monthly: 12 months in a year
        "MS": 12,
        "Q": 4,  # Quarterly: 4 quarters in a year
        "Y": 1,  # Yearly: no seasonality
    }
    return season_map.get(freq, 1)


def calculate_cv_horizon(horizon: int) -> int:
    """
    Calculate appropriate cross-validation horizon.

    Args:
        horizon: Forecast horizon

    Returns:
        Cross-validation horizon (typically 50% of forecast horizon)
    """
    return max(1, horizon // 2)


def calculate_cv_step_size(cv_horizon: int) -> int:
    """
    Calculate step size for cross-validation windows.

    Args:
        cv_horizon: Cross-validation horizon

    Returns:
        Step size for moving windows
    """
    return max(1, cv_horizon // 2)


def validate_inputs(args: argparse.Namespace) -> None:
    """
    Validate input arguments and raise errors for invalid configurations.

    Args:
        args: Parsed command-line arguments

    Raises:
        ValueError: If validation fails
    """
    # Check data file exists
    data_path = Path(args.data)
    if not data_path.exists():
        raise ValueError(f"Data file not found: {args.data}")

    # Check file extension
    if data_path.suffix not in [".csv", ".parquet"]:
        raise ValueError(f"Unsupported file format: {data_path.suffix}. Use .csv or .parquet")

    # Validate horizon
    if args.horizon < 1:
        raise ValueError(f"Horizon must be positive, got: {args.horizon}")

    # Validate cv_windows
    if args.cv_windows < 1:
        raise ValueError(f"CV windows must be positive, got: {args.cv_windows}")


def generate_config(args: argparse.Namespace) -> Dict[str, Any]:
    """
    Generate configuration dictionary from arguments.

    Args:
        args: Parsed command-line arguments

    Returns:
        Configuration dictionary
    """
    season_length = detect_season_length(args.freq)
    cv_horizon = calculate_cv_horizon(args.horizon)
    cv_step_size = calculate_cv_step_size(cv_horizon)

    config = {
        "data": {
            "source": args.data,
            "unique_id": args.id_col,
            "ds": args.ds_col,
            "y": args.target,
            "exog_vars": args.exog_vars,
        },
        "forecast": {
            "horizon": args.horizon,
            "freq": args.freq,
            "season_length": season_length,
        },
        "cv": {
            "method": args.cv_method,
            "h": cv_horizon,
            "step_size": cv_step_size,
            "n_windows": args.cv_windows,
        },
        "models": {
            "statsforecast": ["SeasonalNaive", "AutoARIMA", "AutoETS", "AutoTheta"],
            "mlforecast": {
                "enabled": args.enable_mlforecast,
                "base_models": ["RandomForestRegressor", "LGBMRegressor"],
                "lags": [1, season_length, season_length * 2, season_length * 4],
                "lag_transforms": True,
            },
            "timegpt": {
                "enabled": args.enable_timegpt,
                "finetune_steps": 0,
                "level": [80, 90],
            },
        },
        "metrics": ["smape", "mase", "rmse"],
        "output": {
            "save_forecasts": True,
            "save_cv_results": True,
            "results_dir": "forecasting/results",
            "plot_forecasts": False,
        },
    }

    return config


def save_config(config: Dict[str, Any], output_path: str) -> None:
    """
    Save configuration to YAML file.

    Args:
        config: Configuration dictionary
        output_path: Path to save config file
    """
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    with open(output, "w") as f:
        f.write("# Forecasting Experiment Configuration\n")
        f.write("# Generated by nixtla-experiment-architect skill\n\n")
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    print(f"✅ Configuration saved to: {output}")


def print_summary(config: Dict[str, Any]) -> None:
    """
    Print configuration summary.

    Args:
        config: Configuration dictionary
    """
    print("\n" + "=" * 60)
    print("Configuration Summary")
    print("=" * 60)
    print(f"Data source:      {config['data']['source']}")
    print(f"Target column:    {config['data']['y']}")
    print(f"Forecast horizon: {config['forecast']['horizon']} ({config['forecast']['freq']})")
    print(f"Season length:    {config['forecast']['season_length']}")
    print(f"CV windows:       {config['cv']['n_windows']}")
    print(f"CV method:        {config['cv']['method']}")

    print("\nModels enabled:")
    print(f"  StatsForecast:  {len(config['models']['statsforecast'])} models")
    print(f"  MLForecast:     {'Yes' if config['models']['mlforecast']['enabled'] else 'No'}")
    print(f"  TimeGPT:        {'Yes' if config['models']['timegpt']['enabled'] else 'No'}")

    print("\nNext steps:")
    print(f"  1. Review config: {config.get('output_path', 'forecasting/config.yml')}")
    print("  2. Run: python scripts/scaffold_experiment.py --config forecasting/config.yml")
    print("  3. Execute: python forecasting/experiments.py")
    print()


def main() -> int:
    """Main entry point."""
    try:
        args = parse_args()
        validate_inputs(args)
        config = generate_config(args)
        config["output_path"] = args.output
        save_config(config, args.output)
        print_summary(config)
        return 0
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
