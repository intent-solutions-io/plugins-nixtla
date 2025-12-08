#!/usr/bin/env python3
"""
Configuration loader and validator for Nixtla production pipelines.
"""
import yaml
import json
import os
from typing import Dict, Any
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Loads experiment configuration from a YAML or JSON file.

    Args:
        config_path: Path to the configuration file.

    Returns:
        A dictionary containing the configuration.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        ValueError: If the configuration file is not valid YAML or JSON.
    """
    try:
        with open(config_path, 'r') as f:
            if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                config = yaml.safe_load(f)
            elif config_path.endswith('.json'):
                config = json.load(f)
            else:
                raise ValueError("Unsupported configuration file format. Use YAML or JSON.")
        logging.info(f"Configuration loaded from {config_path}")
        return config
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {config_path}")
        raise
    except yaml.YAMLError as e:
        logging.error(f"Error parsing YAML configuration: {e}")
        raise ValueError(f"Invalid YAML configuration: {e}")
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing JSON configuration: {e}")
        raise ValueError(f"Invalid JSON configuration: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def validate_config(config: Dict[str, Any]) -> None:
    """
    Validates the experiment configuration.

    Args:
        config: The configuration dictionary.

    Raises:
        ValueError: If the configuration is invalid.
    """
    required_keys = ['model_type', 'data_location', 'frequency', 'horizon', 'pipeline_name']
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required key in configuration: {key}")

    if config['model_type'] not in ['TimeGPT', 'StatsForecast']:
        raise ValueError("Invalid model_type. Must be 'TimeGPT' or 'StatsForecast'.")

    if not isinstance(config['horizon'], int) or config['horizon'] <= 0:
        raise ValueError("Horizon must be a positive integer.")

    logging.info("Configuration validation successful.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python load_config.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        config = load_config(config_file)
        validate_config(config)
        logging.info(f"Successfully loaded and validated configuration: {config}")
    except (FileNotFoundError, ValueError) as e:
        logging.error(f"Error loading configuration: {e}")
        sys.exit(1)
