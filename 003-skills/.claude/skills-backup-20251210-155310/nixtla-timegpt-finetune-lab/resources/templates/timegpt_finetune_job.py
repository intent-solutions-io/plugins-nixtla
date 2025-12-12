#!/usr/bin/env python3
"""
TimeGPT Fine-Tuning Job Script

This script handles the complete fine-tuning workflow:
1. Load and validate training data
2. Submit fine-tuning job to TimeGPT API
3. Monitor job status until completion
4. Save fine-tuned model ID for later use
"""

import os
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import yaml

# TODO: Install nixtla package if not available
# pip install nixtla

# TODO: Set your TimeGPT API key
# export NIXTLA_API_KEY='your-api-key-here'
# Get API key from: https://dashboard.nixtla.io

try:
    from nixtla import NixtlaClient
except ImportError:
    print("ERROR: nixtla package not installed")
    print("Run: pip install nixtla")
    exit(1)


def load_config():
    """Load fine-tuning configuration from config.yml"""
    with open("forecasting/config.yml", "r") as f:
        config = yaml.safe_load(f)
    return config["fine_tune"]


def load_training_data(config):
    """
    Load training and validation data based on split strategy

    Returns:
        tuple: (train_df, val_df) in Nixtla format (unique_id, ds, y)
    """
    split_strategy = config["data"].get("split_strategy", "time")

    if split_strategy == "time":
        # Time-based split
        train_df = pd.read_csv(config["data"]["train_path"])
        val_df = pd.read_csv(config["data"]["val_path"])
    else:
        # Percentage split
        full_df = pd.read_csv(config["data"]["train_path"])
        split_pct = config["data"].get("train_split_pct", 0.8)
        split_idx = int(len(full_df) * split_pct)
        train_df = full_df[:split_idx]
        val_df = full_df[split_idx:]

    # Validate Nixtla format
    required_cols = ["unique_id", "ds", "y"]
    for col in required_cols:
        if col not in train_df.columns:
            raise ValueError(f"Training data missing required column: {col}")

    return train_df, val_df


def submit_finetune_job(client, config, train_df):
    """
    Submit fine-tuning job to TimeGPT API

    Args:
        client: NixtlaClient instance
        config: Fine-tuning configuration
        train_df: Training data in Nixtla format

    Returns:
        dict: Fine-tuning job response
    """
    print(f"Submitting fine-tuning job: {config['model_name']}")
    print(f"Training data shape: {train_df.shape}")

    finetune_job = client.finetune(
        df=train_df,
        h=config["parameters"]["horizon"],
        freq=config["parameters"]["freq"],
        model_name=config["model_name"],
        finetune_steps=config["parameters"].get("finetune_steps", 100),
        finetune_loss=config["parameters"].get("finetune_loss", "mae"),
    )

    print(f"Fine-tuning job submitted successfully!")
    print(f"Job ID: {finetune_job.get('finetune_id', 'N/A')}")

    return finetune_job


def monitor_finetune_status(client, finetune_id, timeout_minutes=60):
    """
    Monitor fine-tuning job status until completion

    Args:
        client: NixtlaClient instance
        finetune_id: ID of the fine-tuning job
        timeout_minutes: Maximum time to wait (default: 60 minutes)

    Returns:
        str: Final status ('completed', 'failed', 'timeout')
    """
    start_time = time.time()
    timeout_seconds = timeout_minutes * 60

    print(f"Monitoring fine-tuning job: {finetune_id}")
    print("This may take 10-30 minutes depending on dataset size...")

    while True:
        elapsed = time.time() - start_time
        if elapsed > timeout_seconds:
            print(f"Timeout after {timeout_minutes} minutes")
            return "timeout"

        try:
            status = client.get_finetune_status(finetune_id)
            current_status = status.get("status", "unknown")

            print(f"[{int(elapsed/60)}m {int(elapsed%60)}s] Status: {current_status}")

            if current_status == "completed":
                print("Fine-tuning completed successfully!")
                return "completed"
            elif current_status == "failed":
                print(f"Fine-tuning failed: {status.get('error', 'Unknown error')}")
                return "failed"

            # Wait before next check (increase interval over time)
            if elapsed < 300:  # First 5 minutes: check every 30s
                time.sleep(30)
            else:  # After 5 minutes: check every 2 minutes
                time.sleep(120)

        except Exception as e:
            print(f"Error checking status: {e}")
            time.sleep(60)


def save_finetune_results(config, finetune_job, status):
    """
    Save fine-tuned model ID and metadata

    Args:
        config: Fine-tuning configuration
        finetune_job: Job response from API
        status: Final job status
    """
    output_dir = Path(config["artifacts"]["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save model ID
    model_id_file = output_dir / "finetune_model_id.txt"
    model_id = finetune_job.get("finetune_id", "")
    model_id_file.write_text(model_id)
    print(f"Saved model ID to: {model_id_file}")

    # Save metadata
    metadata = {
        "model_name": config["model_name"],
        "finetune_id": model_id,
        "status": status,
        "horizon": config["parameters"]["horizon"],
        "freq": config["parameters"]["freq"],
        "finetune_steps": config["parameters"].get("finetune_steps", 100),
        "finetune_loss": config["parameters"].get("finetune_loss", "mae"),
        "timestamp": datetime.now().isoformat(),
    }

    metadata_file = output_dir / "finetune_metadata.yml"
    with open(metadata_file, "w") as f:
        yaml.dump(metadata, f, default_flow_style=False)
    print(f"Saved metadata to: {metadata_file}")


def main():
    """Main fine-tuning workflow"""
    # Initialize client
    api_key = os.getenv("NIXTLA_API_KEY")
    if not api_key:
        print("ERROR: NIXTLA_API_KEY not set")
        print("Set it with: export NIXTLA_API_KEY='your-api-key-here'")
        exit(1)

    client = NixtlaClient(api_key=api_key)

    # Load configuration
    config = load_config()
    print(f"Loaded configuration for: {config['model_name']}")

    # Load training data
    train_df, val_df = load_training_data(config)
    print(f"Loaded training data: {len(train_df)} rows")
    print(f"Loaded validation data: {len(val_df)} rows")

    # Submit fine-tuning job
    finetune_job = submit_finetune_job(client, config, train_df)
    finetune_id = finetune_job.get("finetune_id")

    if not finetune_id:
        print("ERROR: No finetune_id returned from API")
        exit(1)

    # Monitor status
    status = monitor_finetune_status(client, finetune_id)

    # Save results
    save_finetune_results(config, finetune_job, status)

    print("\nFine-tuning workflow completed!")
    print(f"Final status: {status}")
    print(f"\nNext steps:")
    print(f"1. Review artifacts in: {config['artifacts']['output_dir']}")
    print(f"2. Run comparison experiments: python forecasting/experiments.py")
    print(f"3. Evaluate fine-tuned model performance")


if __name__ == "__main__":
    main()
