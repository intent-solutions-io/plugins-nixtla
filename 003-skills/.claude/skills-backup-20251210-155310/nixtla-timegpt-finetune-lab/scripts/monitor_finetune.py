#!/usr/bin/env python3
"""
Monitor TimeGPT Fine-Tuning Job Status

This script monitors a fine-tuning job until completion:
1. Checks job status via TimeGPT API
2. Displays progress updates
3. Handles completion, failure, and timeout scenarios
4. Updates job metadata with final status
"""

import argparse
import logging
import os
import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

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


def load_job_metadata(artifacts_dir: str = "forecasting/artifacts/timegpt_finetune") -> dict:
    """
    Load job metadata from artifacts directory.

    Args:
        artifacts_dir: Path to artifacts directory

    Returns:
        Metadata dictionary
    """
    metadata_file = Path(artifacts_dir) / "finetune_metadata.yml"

    if not metadata_file.exists():
        return None

    with open(metadata_file, "r") as f:
        metadata = yaml.safe_load(f)

    return metadata


def save_job_metadata(metadata: dict, artifacts_dir: str):
    """
    Save updated job metadata.

    Args:
        metadata: Metadata dictionary
        artifacts_dir: Path to artifacts directory
    """
    artifacts_path = Path(artifacts_dir)
    artifacts_path.mkdir(parents=True, exist_ok=True)

    metadata_file = artifacts_path / "finetune_metadata.yml"

    with open(metadata_file, "w") as f:
        yaml.dump(metadata, f, default_flow_style=False, sort_keys=False)


def check_job_status(client: NixtlaClient, finetune_id: str) -> dict:
    """
    Check fine-tuning job status.

    Args:
        client: NixtlaClient instance
        finetune_id: Job ID

    Returns:
        Status dictionary
    """
    try:
        status = client.get_finetune_status(finetune_id)
        return status
    except Exception as e:
        print(f"ERROR: Failed to check status - {e}")
        return {"status": "error", "error": str(e)}


def format_elapsed_time(seconds: float) -> str:
    """Format elapsed time as human-readable string"""
    delta = timedelta(seconds=int(seconds))
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"


def monitor_job(
    client: NixtlaClient, finetune_id: str, timeout_minutes: int = 60, check_interval: int = 30
) -> tuple[str, dict]:
    """
    Monitor job until completion, failure, or timeout.

    Args:
        client: NixtlaClient instance
        finetune_id: Job ID
        timeout_minutes: Maximum wait time in minutes
        check_interval: Seconds between status checks

    Returns:
        Tuple of (final_status, status_dict)
    """
    start_time = time.time()
    timeout_seconds = timeout_minutes * 60
    check_count = 0

    print("\n" + "=" * 60)
    print("MONITORING FINE-TUNING JOB")
    print("=" * 60)
    print(f"Job ID: {finetune_id}")
    print(f"Timeout: {timeout_minutes} minutes")
    print(f"Check interval: {check_interval} seconds")
    print("=" * 60 + "\n")

    while True:
        check_count += 1
        elapsed = time.time() - start_time

        # Check timeout
        if elapsed > timeout_seconds:
            print(f"\nTimeout reached after {format_elapsed_time(elapsed)}")
            return "timeout", {"status": "timeout", "elapsed": elapsed}

        # Check status
        status = check_job_status(client, finetune_id)
        current_status = status.get("status", "unknown")

        # Display update
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(
            f"[{timestamp}] Check #{check_count} ({format_elapsed_time(elapsed)}): {current_status}"
        )

        # Handle terminal states
        if current_status == "completed":
            print(f"\nFine-tuning completed successfully!")
            print(f"Total time: {format_elapsed_time(elapsed)}")
            return "completed", status

        elif current_status == "failed":
            error_msg = status.get("error", "Unknown error")
            print(f"\nFine-tuning failed: {error_msg}")
            print(f"Total time: {format_elapsed_time(elapsed)}")
            return "failed", status

        elif current_status == "error":
            print(f"\nError checking status")
            return "error", status

        # Adaptive interval: longer waits after initial checks
        if elapsed < 300:  # First 5 minutes
            sleep_time = check_interval
        elif elapsed < 900:  # 5-15 minutes
            sleep_time = 60
        else:  # After 15 minutes
            sleep_time = 120

        time.sleep(sleep_time)


def main():
    """Main monitoring workflow"""
    parser = argparse.ArgumentParser(
        description="Monitor TimeGPT fine-tuning job status",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Monitor specific job
  python monitor_finetune.py --job-id abc123def456

  # Monitor with custom timeout
  python monitor_finetune.py --job-id abc123 --timeout 90

  # Load job ID from artifacts
  python monitor_finetune.py --artifacts-dir forecasting/artifacts/timegpt_finetune

Environment Variables:
  NIXTLA_API_KEY: Required. Get from https://dashboard.nixtla.io
        """,
    )

    parser.add_argument("--job-id", help="Fine-tuning job ID")
    parser.add_argument(
        "--artifacts-dir",
        default="forecasting/artifacts/timegpt_finetune",
        help="Artifacts directory (to load job ID)",
    )
    parser.add_argument("--timeout", type=int, default=60, help="Timeout in minutes (default: 60)")
    parser.add_argument(
        "--check-interval",
        type=int,
        default=30,
        help="Status check interval in seconds (default: 30)",
    )
    parser.add_argument("--once", action="store_true", help="Check status once and exit")

    args = parser.parse_args()

    # Get job ID
    finetune_id = args.job_id

    if not finetune_id:
        # Try loading from metadata
        print(f"Loading job ID from: {args.artifacts_dir}")
        metadata = load_job_metadata(args.artifacts_dir)

        if metadata:
            finetune_id = metadata.get("finetune_id")
            print(f"Found job ID: {finetune_id}")
        else:
            print("ERROR: No job ID provided and no metadata found")
            print("Specify --job-id or ensure artifacts directory contains metadata")
            sys.exit(1)

    # Security: Validate API key before use
    api_key = os.getenv("NIXTLA_API_KEY", "").strip()

    if not validate_api_key(api_key):
        print("ERROR: Invalid or missing NIXTLA_API_KEY")
        print("Export your API key: export NIXTLA_API_KEY='your-key'")
        print("\nSecurity requirements:")
        print("  - Minimum 20 characters")
        print("  - Cannot be a placeholder value")
        print("  - Alphanumeric characters, hyphens, and underscores only")
        sys.exit(1)

    # Initialize client
    client = NixtlaClient(api_key=api_key)

    # Check once or monitor
    if args.once:
        print(f"Checking status for job: {finetune_id}")
        status = check_job_status(client, finetune_id)
        print(f"\nStatus: {status.get('status', 'unknown')}")

        if status.get("error"):
            print(f"Error: {status['error']}")

        sys.exit(0 if status.get("status") == "completed" else 1)

    # Monitor until completion
    final_status, status_dict = monitor_job(
        client, finetune_id, timeout_minutes=args.timeout, check_interval=args.check_interval
    )

    # Update metadata
    metadata = load_job_metadata(args.artifacts_dir)
    if metadata:
        metadata["status"] = final_status
        metadata["completion_time"] = datetime.now().isoformat()
        metadata["final_status"] = status_dict
        save_job_metadata(metadata, args.artifacts_dir)
        print(f"\nUpdated metadata: {args.artifacts_dir}/finetune_metadata.yml")

    # Print next steps
    print("\n" + "=" * 60)
    if final_status == "completed":
        print("Next steps:")
        print("  1. Compare models: python scripts/compare_finetuned.py")
        print("  2. Evaluate performance: python scripts/evaluate.py")
        print("  3. View dashboard: https://dashboard.nixtla.io")
        sys.exit(0)
    else:
        print("Job did not complete successfully")
        print("Check logs and troubleshoot: https://docs.nixtla.io/docs/finetuning")
        sys.exit(1)


if __name__ == "__main__":
    main()
