#!/usr/bin/env python3
"""
API usage pattern analysis for Nixtla usage optimization.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, Any
import logging
import argparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def analyze_usage_patterns(api_logs_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyzes API usage patterns from the API logs DataFrame.

    Args:
        api_logs_df: Pandas DataFrame containing API log data.

    Returns:
        A dictionary containing usage statistics and patterns.
    """
    if api_logs_df.empty:
        logging.warning("API logs DataFrame is empty. Cannot analyze usage patterns.")
        return {}

    try:
        # Convert timestamp column to datetime objects
        if 'timestamp' in api_logs_df.columns:
            api_logs_df['timestamp'] = pd.to_datetime(api_logs_df['timestamp'])
            api_logs_df.set_index('timestamp', inplace=True)

        # Frequency of API calls
        frequency = api_logs_df.resample('H').size()

        # Region analysis (assuming 'region' column exists)
        if 'region' in api_logs_df.columns:
            region_usage = api_logs_df['region'].value_counts()
        else:
            region_usage = {}
            logging.warning("No 'region' column found in API logs. Skipping region analysis.")

        # API endpoint analysis (assuming 'endpoint' column exists)
        if 'endpoint' in api_logs_df.columns:
            endpoint_usage = api_logs_df['endpoint'].value_counts()
        else:
            endpoint_usage = {}
            logging.warning("No 'endpoint' column found in API logs. Skipping endpoint analysis.")

        # Create visualizations
        plt.figure(figsize=(12, 6))
        frequency.plot(title='API Call Frequency (Hourly)')
        plt.xlabel('Time')
        plt.ylabel('Number of Calls')
        plt.savefig('api_call_frequency.png')

        if region_usage:
            plt.figure(figsize=(10, 6))
            region_usage.plot(kind='bar', title='API Usage by Region')
            plt.xlabel('Region')
            plt.ylabel('Number of Calls')
            plt.savefig('api_usage_by_region.png')

        if endpoint_usage:
            plt.figure(figsize=(10, 6))
            endpoint_usage.plot(kind='bar', title='API Usage by Endpoint')
            plt.xlabel('Endpoint')
            plt.ylabel('Number of Calls')
            plt.savefig('api_usage_by_endpoint.png')

        usage_patterns = {
            'frequency': frequency.to_dict(),
            'region_usage': region_usage.to_dict() if isinstance(region_usage, pd.Series) else {},
            'endpoint_usage': endpoint_usage.to_dict() if isinstance(endpoint_usage, pd.Series) else {}
        }

        logging.info("Successfully analyzed API usage patterns.")
        return usage_patterns

    except Exception as e:
        logging.error(f"An error occurred during usage pattern analysis: {e}")
        return {}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze API usage patterns.")
    parser.add_argument("--log_path", required=True, help="Path to API log file (CSV or JSON).")
    args = parser.parse_args()

    try:
        api_logs_df = pd.read_csv(args.log_path)
        usage_patterns = analyze_usage_patterns(api_logs_df)

        if usage_patterns:
            print("Usage Patterns Analysis:")
            print(usage_patterns)
        else:
            print("Failed to analyze usage patterns.")

    except FileNotFoundError:
        print(f"Error: API log file not found at {args.log_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
