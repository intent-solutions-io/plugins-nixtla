#!/usr/bin/env python3
"""
Training configuration management for TimeGPT fine-tuning.
"""
import argparse
import json
from typing import Dict


def create_default_config() -> Dict:
    """
    Creates a default training configuration dictionary.

    Returns:
        Dict: A dictionary containing the default training configuration.
    """
    default_config = {
        "learning_rate": 0.001,
        "epochs": 10,
        "batch_size": 32,
        "num_workers": 4,
        "model_name": "TimeGPT",
        "freq": "D",
    }
    return default_config


def load_config(config_path: str) -> Dict:
    """
    Loads the training configuration from a JSON file.

    Args:
        config_path (str): The path to the JSON configuration file.

    Returns:
        Dict: A dictionary containing the training configuration.

    Raises:
        FileNotFoundError: If the specified file path does not exist.
        json.JSONDecodeError: If the JSON file is invalid.
    """
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found at path: {config_path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON format in config file: {e.msg}", e.doc, e.pos)


def validate_config(config: Dict) -> None:
    """
    Validates the training configuration to ensure required parameters are present and of the correct type.

    Args:
        config (Dict): The training configuration dictionary.

    Raises:
        ValueError: If any required parameters are missing or of the incorrect type.
    """
    required_params = {
        "learning_rate": float,
        "epochs": int,
        "batch_size": int,
        "num_workers": int,
        "model_name": str,
        "freq": str,
    }

    for param, expected_type in required_params.items():
        if param not in config:
            raise ValueError(f"Missing required parameter in config: {param}")
        if not isinstance(config[param], expected_type):
            raise ValueError(
                f"Parameter '{param}' must be of type {expected_type}, but is of type {type(config[param])}"
            )

    # Additional checks for specific values
    if config["epochs"] <= 0:
        raise ValueError("Number of epochs must be a positive integer.")
    if config["batch_size"] <= 0:
        raise ValueError("Batch size must be a positive integer.")
    if config["learning_rate"] <= 0:
        raise ValueError("Learning rate must be a positive float.")


def save_config(config: Dict, output_path: str) -> None:
    """
    Saves configuration to a JSON file.

    Args:
        config (Dict): Configuration dictionary to save.
        output_path (str): Path to save the configuration file.
    """
    with open(output_path, "w") as f:
        json.dump(config, f, indent=4)
    print(f"Configuration saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Configure TimeGPT fine-tuning.")
    parser.add_argument(
        "--create_default", action="store_true", help="Create a default config file."
    )
    parser.add_argument("--config", help="Path to config file to validate.")
    parser.add_argument("--output", default="config.json", help="Output path for config file.")

    args = parser.parse_args()

    try:
        if args.create_default:
            config = create_default_config()
            save_config(config, args.output)
        elif args.config:
            config = load_config(args.config)
            validate_config(config)
            print("Config loaded and validated successfully.")
            print(f"Config: {config}")
        else:
            print("Please specify --create_default or --config <path>")
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"Error: {e}")
        exit(1)
