#!/usr/bin/env python3
"""
Read and validate forecasting experiment configuration.

This script parses the YAML config file created by nixtla-experiment-architect
and validates all required fields for production pipeline generation.

Usage:
    python read_experiment.py --config forecasting/config.yml
    python read_experiment.py --config forecasting/config.yml --validate-data
    python read_experiment.py --config forecasting/config.yml --output json

Author: nixtla-prod-pipeline-generator skill
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


class ExperimentConfigReader:
    """Parse and validate Nixtla experiment configuration files."""

    REQUIRED_FIELDS = {"data": ["source", "ds", "y"], "forecast": ["horizon", "freq"]}

    VALID_FREQUENCIES = ["D", "H", "W", "M", "Y", "Q", "T", "S", "MS", "QS", "YS"]

    def __init__(self, config_path: str):
        """
        Initialize config reader.

        Args:
            config_path: Path to config.yml file
        """
        self.config_path = Path(config_path)
        self.config: Optional[Dict[str, Any]] = None
        self.errors: list = []
        self.warnings: list = []

    def read(self) -> Dict[str, Any]:
        """
        Read YAML config file.

        Returns:
            Parsed configuration dictionary

        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If YAML is invalid
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, "r") as f:
            self.config = yaml.safe_load(f)

        if not self.config:
            raise ValueError(f"Config file is empty: {self.config_path}")

        return self.config

    def validate(self) -> bool:
        """
        Validate configuration structure and values.

        Returns:
            True if valid, False otherwise
        """
        if not self.config:
            self.errors.append("No configuration loaded. Call read() first.")
            return False

        # Check required sections
        for section, fields in self.REQUIRED_FIELDS.items():
            if section not in self.config:
                self.errors.append(f"Missing required section: {section}")
                continue

            # Check required fields in section
            for field in fields:
                if field not in self.config[section]:
                    self.errors.append(f"Missing required field: {section}.{field}")

        # Validate frequency
        if "forecast" in self.config:
            freq = self.config["forecast"].get("freq")
            if freq and freq not in self.VALID_FREQUENCIES:
                self.errors.append(
                    f"Invalid frequency: {freq}. Must be one of {self.VALID_FREQUENCIES}"
                )

        # Check horizon is positive
        if "forecast" in self.config:
            horizon = self.config["forecast"].get("horizon")
            if horizon is not None and (not isinstance(horizon, int) or horizon <= 0):
                self.errors.append(f"Horizon must be positive integer, got: {horizon}")

        # Validate models section
        if "models" in self.config:
            self._validate_models()

        # Check for common issues (warnings)
        self._check_warnings()

        return len(self.errors) == 0

    def _validate_models(self):
        """Validate models configuration."""
        models = self.config["models"]

        # Check if at least one model type is enabled
        has_models = False

        if "statsforecast" in models and models["statsforecast"]:
            has_models = True

        if "mlforecast" in models and models["mlforecast"].get("enabled"):
            has_models = True

        if "timegpt" in models and models["timegpt"].get("enabled"):
            has_models = True

        if not has_models:
            self.warnings.append("No models enabled. Pipeline will use default baselines.")

    def _check_warnings(self):
        """Check for common configuration issues."""
        # Check if data source exists (if it's a file path)
        data_source = self.config.get("data", {}).get("source", "")
        if data_source and not data_source.startswith(("sql://", "postgresql://", "bigquery://")):
            source_path = Path(data_source)
            if not source_path.exists():
                self.warnings.append(f"Data source file not found: {data_source}")

        # Check for TimeGPT without API key
        if self.config.get("models", {}).get("timegpt", {}).get("enabled"):
            import os

            if not os.getenv("NIXTLA_API_KEY"):
                self.warnings.append(
                    "TimeGPT enabled but NIXTLA_API_KEY not set. "
                    "Pipeline will fallback to baselines."
                )

    def get_summary(self) -> Dict[str, Any]:
        """
        Get configuration summary.

        Returns:
            Dictionary with key config parameters
        """
        if not self.config:
            return {}

        summary = {
            "data_source": self.config.get("data", {}).get("source"),
            "target_column": self.config.get("data", {}).get("y"),
            "forecast_horizon": self.config.get("forecast", {}).get("horizon"),
            "frequency": self.config.get("forecast", {}).get("freq"),
            "models": self._get_enabled_models(),
            "has_cross_validation": "cv" in self.config,
            "valid": len(self.errors) == 0,
        }

        return summary

    def _get_enabled_models(self) -> list:
        """Get list of enabled model types."""
        enabled = []

        if not self.config or "models" not in self.config:
            return enabled

        models = self.config["models"]

        if "statsforecast" in models and models["statsforecast"]:
            enabled.append("statsforecast")

        if "mlforecast" in models and models["mlforecast"].get("enabled"):
            enabled.append("mlforecast")

        if "timegpt" in models and models["timegpt"].get("enabled"):
            enabled.append("timegpt")

        return enabled


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Read and validate Nixtla experiment configuration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic validation
  python read_experiment.py --config forecasting/config.yml

  # Show detailed summary
  python read_experiment.py --config forecasting/config.yml --verbose

  # Output as JSON
  python read_experiment.py --config forecasting/config.yml --output json
        """,
    )

    parser.add_argument("--config", required=True, help="Path to config.yml file")

    parser.add_argument(
        "--output", choices=["text", "json"], default="text", help="Output format (default: text)"
    )

    parser.add_argument(
        "--verbose", action="store_true", help="Show detailed configuration summary"
    )

    args = parser.parse_args()

    # Read and validate config
    reader = ExperimentConfigReader(args.config)

    try:
        config = reader.read()
        print(f"✓ Config file loaded: {args.config}")

        is_valid = reader.validate()

        if args.output == "json":
            # Output JSON format
            output = {
                "config": config,
                "summary": reader.get_summary(),
                "valid": is_valid,
                "errors": reader.errors,
                "warnings": reader.warnings,
            }
            print(json.dumps(output, indent=2))
            return 0 if is_valid else 1

        # Text output
        if reader.errors:
            print("\n❌ Configuration Errors:")
            for error in reader.errors:
                print(f"  - {error}")

        if reader.warnings:
            print("\n⚠️  Warnings:")
            for warning in reader.warnings:
                print(f"  - {warning}")

        if is_valid:
            print("\n✓ Configuration is valid")

            if args.verbose:
                print("\nConfiguration Summary:")
                summary = reader.get_summary()
                for key, value in summary.items():
                    if key != "valid":
                        print(f"  {key}: {value}")

            return 0
        else:
            print("\n❌ Configuration validation failed")
            return 1

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return 1
    except yaml.YAMLError as e:
        print(f"❌ Invalid YAML: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
