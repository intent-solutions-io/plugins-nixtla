#!/usr/bin/env python3
"""
Submit TimeGPT Fine-Tuning Job

This script submits a fine-tuning job to the TimeGPT API:
1. Loads configuration and training data
2. Validates API credentials
3. Submits fine-tuning job
4. Saves job ID and metadata
"""

import argparse
import logging
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
import yaml

# Security logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from nixtla import NixtlaClient
except ImportError:
    print("ERROR: nixtla package not installed")
    print("Run: pip install nixtla")
    sys.exit(1)


def validate_api_key(key: Optional[str]) -> bool:
    """
    Validate API key format and structure.

    Args:
        key: API key string to validate

    Returns:
        True if key appears valid, False otherwise

    Security:
        - Minimum length check prevents empty/trivial keys
        - Pattern check validates expected format
        - Does not log key value to prevent credential leakage
        - OWASP A07:2021 - Identification and Authentication Failures
    """
    if not key:
        logger.error("API key is missing or empty")
        return False

    key = key.strip()

    # Minimum length check (Nixtla keys are typically 32+ characters)
    if len(key) < 20:
        logger.error("API key is too short (minimum 20 characters required)")
        return False

    # Check for common placeholder values
    placeholder_patterns = [
        r"^your[-_]?api[-_]?key",
        r"^xxx+$",
        r"^test[-_]?key",
        r"^placeholder",
        r"^demo[-_]?key",
    ]
    for pattern in placeholder_patterns:
        if re.match(pattern, key, re.IGNORECASE):
            logger.error("API key appears to be a placeholder value")
            return False

    # Basic alphanumeric pattern check (allow alphanumeric, hyphens, underscores)
    if not re.match(r"^[a-zA-Z0-9_-]+$", key):
        logger.error("API key contains invalid characters")
        return False

    return True


def load_config(config_path: str) -> dict:
    """
    Load fine-tuning configuration from YAML file.

    Args:
        config_path: Path to configuration file

    Returns:
        Configuration dictionary
    """
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"Configuration not found: {config_path}")

    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    return config


def load_training_data(config: dict) -> pd.DataFrame:
    """
    Load training data based on configuration.

    Args:
        config: Fine-tuning configuration

    Returns:
        Training dataframe in Nixtla format
    """
    train_path = config["fine_tune"]["data"]["train_path"]
    train_df = pd.read_csv(train_path)

    # Validate required columns
    required_cols = ["unique_id", "ds", "y"]
    missing_cols = [col for col in required_cols if col not in train_df.columns]

    if missing_cols:
        raise ValueError(f"Training data missing columns: {missing_cols}")

    print(f"Loaded training data: {len(train_df)} rows")
    print(f"  - {train_df['unique_id'].nunique()} unique series")
    print(f"  - Date range: {train_df['ds'].min()} to {train_df['ds'].max()}")

    return train_df


def submit_finetune_job(client: NixtlaClient, config: dict, train_df: pd.DataFrame) -> dict:
    """
    Submit fine-tuning job to TimeGPT API.

    Args:
        client: NixtlaClient instance
        config: Fine-tuning configuration
        train_df: Training data

    Returns:
        Job response dictionary
    """
    fine_tune_config = config["fine_tune"]
    params = fine_tune_config["parameters"]

    print("\n" + "=" * 60)
    print("SUBMITTING FINE-TUNING JOB")
    print("=" * 60)
    print(f"Model name:    {fine_tune_config['model_name']}")
    print(f"Horizon:       {params['horizon']}")
    print(f"Frequency:     {params['freq']}")
    print(f"Training rows: {len(train_df)}")
    print(f"Finetune steps: {params.get('finetune_steps', 100)}")
    print(f"Loss function:  {params.get('finetune_loss', 'mae')}")
    print("=" * 60 + "\n")

    # Submit job
    try:
        job_response = client.finetune(
            df=train_df,
            h=params["horizon"],
            freq=params["freq"],
            model_name=fine_tune_config["model_name"],
            finetune_steps=params.get("finetune_steps", 100),
            finetune_loss=params.get("finetune_loss", "mae"),
        )

        print("Fine-tuning job submitted successfully!")
        return job_response

    except Exception as e:
        print(f"ERROR: Failed to submit job - {e}")
        raise


def save_job_metadata(config: dict, job_response: dict):
    """
    Save job ID and metadata to artifacts directory.

    Args:
        config: Fine-tuning configuration
        job_response: Job response from API
    """
    artifacts_dir = Path(config["fine_tune"]["artifacts"]["output_dir"])
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    # Extract job information
    finetune_id = job_response.get("finetune_id")
    if not finetune_id:
        print("WARNING: No finetune_id in response")
        print(f"Response: {job_response}")
        return

    # Save model ID
    model_id_file = artifacts_dir / "finetune_model_id.txt"
    model_id_file.write_text(finetune_id)
    print(f"\nSaved model ID to: {model_id_file}")

    # Save metadata
    params = config["fine_tune"]["parameters"]
    metadata = {
        "finetune_id": finetune_id,
        "model_name": config["fine_tune"]["model_name"],
        "status": "submitted",
        "horizon": params["horizon"],
        "freq": params["freq"],
        "finetune_steps": params.get("finetune_steps", 100),
        "finetune_loss": params.get("finetune_loss", "mae"),
        "train_path": config["fine_tune"]["data"]["train_path"],
        "submission_time": datetime.now().isoformat(),
        "response": job_response,
    }

    metadata_file = artifacts_dir / "finetune_metadata.yml"
    with open(metadata_file, "w") as f:
        yaml.dump(metadata, f, default_flow_style=False, sort_keys=False)

    print(f"Saved metadata to: {metadata_file}")


def main():
    """Main job submission workflow"""
    parser = argparse.ArgumentParser(
        description="Submit TimeGPT fine-tuning job",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Submit job from configuration
  python submit_finetune.py --config forecasting/finetune_config.yml

  # Submit with custom timeout for monitoring
  python submit_finetune.py --config config.yml --no-wait

Environment Variables:
  NIXTLA_API_KEY: Required. Get from https://dashboard.nixtla.io
        """,
    )

    parser.add_argument("--config", required=True, help="Fine-tuning configuration YAML file")
    parser.add_argument(
        "--no-wait", action="store_true", help="Submit job and exit (do not monitor)"
    )

    args = parser.parse_args()

    # Security: Validate API key before use
    api_key = os.getenv("NIXTLA_API_KEY", "").strip()

    if not validate_api_key(api_key):
        print("ERROR: Invalid or missing NIXTLA_API_KEY")
        print("Export your API key: export NIXTLA_API_KEY='your-key'")
        print("Get API key from: https://dashboard.nixtla.io")
        print("\nSecurity requirements:")
        print("  - Minimum 20 characters")
        print("  - Cannot be a placeholder value")
        print("  - Alphanumeric characters, hyphens, and underscores only")
        sys.exit(1)

    # Initialize client
    logger.info("Initializing TimeGPT client...")
    client = NixtlaClient(api_key=api_key)

    # Load configuration
    print(f"Loading configuration: {args.config}")
    config = load_config(args.config)

    # Load training data
    train_df = load_training_data(config)

    # Submit job
    job_response = submit_finetune_job(client, config, train_df)

    # Save metadata
    save_job_metadata(config, job_response)

    # Print next steps
    finetune_id = job_response.get("finetune_id")

    print("\n" + "=" * 60)
    print("SUBMISSION COMPLETE")
    print("=" * 60)
    print(f"Job ID: {finetune_id}")
    print(f"\nNext steps:")

    if args.no_wait:
        print(f"  1. Monitor progress: python scripts/monitor_finetune.py --job-id {finetune_id}")
        print(f"  2. Check status in dashboard: https://dashboard.nixtla.io")
    else:
        print(f"  1. Wait for completion (may take 10-30 minutes)")
        print(f"  2. Monitor with: python scripts/monitor_finetune.py --job-id {finetune_id}")

    print(f"  3. Compare models: python scripts/compare_finetuned.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
