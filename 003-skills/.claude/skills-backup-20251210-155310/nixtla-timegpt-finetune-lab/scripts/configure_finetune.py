#!/usr/bin/env python3
"""
Configure TimeGPT Fine-Tuning Job

This script creates a fine-tuning configuration file with:
1. Model settings (name, horizon, frequency)
2. Hyperparameters (finetune_steps, loss function)
3. Data paths (train, validation)
4. Output directories (artifacts, results)
"""

import argparse
import sys
from pathlib import Path

import yaml

DEFAULT_CONFIG = {
    "fine_tune": {
        "model_name": None,  # Set by user
        "parameters": {"horizon": 14, "freq": "D", "finetune_steps": 100, "finetune_loss": "mae"},
        "data": {
            "train_path": None,  # Set by user
            "val_path": None,  # Set by user
            "split_strategy": "time",
            "train_split_pct": 0.8,
        },
        "artifacts": {"output_dir": "forecasting/artifacts/timegpt_finetune"},
    },
    "comparison": {"output": {"results_path": "forecasting/results/comparison_metrics.csv"}},
}


def create_config(args) -> dict:
    """
    Create fine-tuning configuration from arguments.

    Args:
        args: Parsed command-line arguments

    Returns:
        Configuration dictionary
    """
    config = DEFAULT_CONFIG.copy()

    # Set model settings
    config["fine_tune"]["model_name"] = args.model_name
    config["fine_tune"]["parameters"]["horizon"] = args.horizon
    config["fine_tune"]["parameters"]["freq"] = args.freq

    # Set hyperparameters
    if args.finetune_steps:
        config["fine_tune"]["parameters"]["finetune_steps"] = args.finetune_steps

    if args.finetune_loss:
        config["fine_tune"]["parameters"]["finetune_loss"] = args.finetune_loss

    # Set data paths
    config["fine_tune"]["data"]["train_path"] = args.train
    if args.val:
        config["fine_tune"]["data"]["val_path"] = args.val
        config["fine_tune"]["data"]["split_strategy"] = "time"
    else:
        # Use percentage split if no validation set provided
        config["fine_tune"]["data"]["val_path"] = args.train
        config["fine_tune"]["data"]["split_strategy"] = "percentage"

    # Set output directories
    if args.artifacts_dir:
        config["fine_tune"]["artifacts"]["output_dir"] = args.artifacts_dir

    return config


def validate_config(config: dict) -> tuple[bool, str]:
    """
    Validate configuration settings.

    Args:
        config: Configuration dictionary

    Returns:
        Tuple of (is_valid, error_message)
    """
    fine_tune = config["fine_tune"]

    # Check required fields
    if not fine_tune["model_name"]:
        return False, "model_name is required"

    if not fine_tune["data"]["train_path"]:
        return False, "train_path is required"

    # Validate data paths exist
    train_path = Path(fine_tune["data"]["train_path"])
    if not train_path.exists():
        return False, f"Training data not found: {train_path}"

    val_path = fine_tune["data"].get("val_path")
    if val_path and val_path != fine_tune["data"]["train_path"]:
        if not Path(val_path).exists():
            return False, f"Validation data not found: {val_path}"

    # Validate parameters
    params = fine_tune["parameters"]

    if params["horizon"] <= 0:
        return False, "horizon must be > 0"

    if params["freq"] not in ["H", "D", "W", "M", "Q", "Y"]:
        return False, f"Invalid frequency: {params['freq']}"

    if params["finetune_steps"] <= 0:
        return False, "finetune_steps must be > 0"

    if params["finetune_loss"] not in ["mae", "mse", "rmse", "mape"]:
        return False, f"Invalid loss function: {params['finetune_loss']}"

    return True, "Valid"


def print_config_summary(config: dict):
    """Print human-readable configuration summary"""
    fine_tune = config["fine_tune"]
    params = fine_tune["parameters"]

    print("\n" + "=" * 60)
    print("FINE-TUNING CONFIGURATION")
    print("=" * 60)
    print(f"\nModel Settings:")
    print(f"  Name:     {fine_tune['model_name']}")
    print(f"  Horizon:  {params['horizon']}")
    print(f"  Frequency: {params['freq']}")

    print(f"\nHyperparameters:")
    print(f"  Fine-tune steps: {params['finetune_steps']}")
    print(f"  Loss function:   {params['finetune_loss']}")

    print(f"\nData:")
    print(f"  Training:   {fine_tune['data']['train_path']}")
    print(f"  Validation: {fine_tune['data']['val_path']}")
    print(f"  Split:      {fine_tune['data']['split_strategy']}")

    print(f"\nOutput:")
    print(f"  Artifacts:  {fine_tune['artifacts']['output_dir']}")
    print(f"  Results:    {config['comparison']['output']['results_path']}")
    print("=" * 60 + "\n")


def main():
    """Main configuration workflow"""
    parser = argparse.ArgumentParser(
        description="Configure TimeGPT fine-tuning job",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic configuration
  python configure_finetune.py \\
      --train data/train.csv \\
      --model-name "sales-forecast-v1" \\
      --horizon 14 \\
      --freq D

  # With validation set
  python configure_finetune.py \\
      --train data/train.csv \\
      --val data/val.csv \\
      --model-name "demand-forecast" \\
      --horizon 24 \\
      --freq H

  # With custom hyperparameters
  python configure_finetune.py \\
      --train data/train.csv \\
      --model-name "my-model" \\
      --horizon 7 \\
      --freq D \\
      --finetune-steps 200 \\
      --finetune-loss mse

Frequency codes:
  H = Hourly, D = Daily, W = Weekly, M = Monthly, Q = Quarterly, Y = Yearly
        """,
    )

    # Required arguments
    parser.add_argument("--train", required=True, help="Training data CSV path")
    parser.add_argument("--model-name", required=True, help="Fine-tuned model name")
    parser.add_argument("--horizon", type=int, required=True, help="Forecast horizon")
    parser.add_argument("--freq", required=True, help="Data frequency (H, D, W, M, Q, Y)")

    # Optional arguments
    parser.add_argument("--val", help="Validation data CSV path")
    parser.add_argument(
        "--finetune-steps", type=int, help="Number of fine-tuning steps (default: 100)"
    )
    parser.add_argument(
        "--finetune-loss",
        choices=["mae", "mse", "rmse", "mape"],
        help="Loss function (default: mae)",
    )
    parser.add_argument("--artifacts-dir", help="Artifacts output directory")
    parser.add_argument(
        "--output",
        default="forecasting/finetune_config.yml",
        help="Configuration output path (default: forecasting/finetune_config.yml)",
    )

    args = parser.parse_args()

    # Create configuration
    print("Creating fine-tuning configuration...")
    config = create_config(args)

    # Validate configuration
    print("Validating configuration...")
    is_valid, msg = validate_config(config)

    if not is_valid:
        print(f"ERROR: Configuration invalid - {msg}")
        sys.exit(1)

    print(f"Configuration valid: {msg}")

    # Print summary
    print_config_summary(config)

    # Save configuration
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    print(f"Configuration saved to: {output_path}")
    print("\nNext steps:")
    print(f"  1. Review configuration: cat {output_path}")
    print(f"  2. Submit fine-tuning job: python scripts/submit_finetune.py --config {output_path}")


if __name__ == "__main__":
    main()
