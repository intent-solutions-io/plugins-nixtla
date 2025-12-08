#!/usr/bin/env python3
"""
API logs and configuration gathering for Nixtla usage analysis.
"""
import os
import json
import pandas as pd
from typing import Dict, Any, List
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def read_api_logs(log_path: str) -> pd.DataFrame:
    """
    Reads API logs from a JSON file and returns a Pandas DataFrame.

    Args:
        log_path: Path to the API log file.

    Returns:
        A Pandas DataFrame containing the API log data.
        Returns an empty DataFrame if an error occurs.
    """
    try:
        with open(log_path, 'r') as f:
            logs: List[Dict[str, Any]] = [json.loads(line) for line in f]
        df = pd.DataFrame(logs)
        logging.info(f"Successfully read API logs from {log_path}")
        return df
    except FileNotFoundError:
        logging.error(f"API log file not found: {log_path}")
        return pd.DataFrame()
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON format in API log file: {log_path}")
        return pd.DataFrame()
    except Exception as e:
        logging.error(f"An unexpected error occurred while reading API logs: {e}")
        return pd.DataFrame()


def read_api_config(config_path: str) -> Dict[str, Any]:
    """
    Reads API configuration from a JSON file and returns a dictionary.

    Args:
        config_path: Path to the API configuration file.

    Returns:
        A dictionary containing the API configuration data.
        Returns an empty dictionary if an error occurs.
    """
    try:
        with open(config_path, 'r') as f:
            config: Dict[str, Any] = json.load(f)
        logging.info(f"Successfully read API configuration from {config_path}")
        return config
    except FileNotFoundError:
        logging.error(f"API configuration file not found: {config_path}")
        return {}
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON format in API configuration file: {config_path}")
        return {}
    except Exception as e:
        logging.error(f"An unexpected error occurred while reading API configuration: {e}")
        return {}


if __name__ == "__main__":
    log_path = os.getenv('NIXTLA_API_LOG_PATH')
    config_path = os.getenv('NIXTLA_API_CONFIG_PATH')

    if not log_path:
        logging.error("NIXTLA_API_LOG_PATH not set. Please set the environment variable.")
    if not config_path:
        logging.error("NIXTLA_API_CONFIG_PATH not set. Please set the environment variable.")

    if log_path and config_path:
        api_logs_df = read_api_logs(log_path)
        api_config = read_api_config(config_path)

        if not api_logs_df.empty and api_config:
            print("API logs and configuration loaded successfully.")
        else:
            print("Failed to load API logs or configuration.")
