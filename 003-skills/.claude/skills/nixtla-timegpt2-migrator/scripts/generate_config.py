"""
Generate TimeGPT-2 configuration file.

Usage:
    python generate_config.py
"""

import os
from typing import Any, Dict

import yaml


def generate_timegpt2_config(
    config_data: Dict[str, Any], output_file: str = "timegpt2_config.yaml"
) -> None:
    """
    Generates a TimeGPT-2 configuration file in YAML format.

    Args:
        config_data: A dictionary containing the configuration parameters.
        output_file: The path to the output configuration file.
    """
    try:
        with open(output_file, "w") as f:
            yaml.dump(config_data, f, indent=2)
        print(f"Successfully generated TimeGPT-2 configuration file: {output_file}")
    except Exception as e:
        print(f"Error generating TimeGPT-2 configuration file: {e}")


if __name__ == "__main__":
    # Example configuration data
    config_data = {
        "api_key": os.getenv("NIXTLA_TIMEGPT_API_KEY", "YOUR_API_KEY_HERE"),
        "model_name": "TimeGPT-2",
        "frequency": "H",
        "forecast_horizon": 24,
        "data_format": "Nixtla",
        "feature_engineering": {"enabled": True, "seasonal_decomposition": True},
        "advanced_settings": {"uncertainty_level": 90, "optimization_method": "L-BFGS-B"},
    }

    generate_timegpt2_config(config_data)
    print("TimeGPT-2 configuration file generated successfully.")
