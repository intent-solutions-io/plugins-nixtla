#!/usr/bin/env python3
"""
prepare_data.py - Load and validate contract price and event data from CSV files.

This script loads price and event data, validates columns, and prepares them for
causal impact analysis with TimeGPT.
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Tuple

import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_data(prices_path: str, events_path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load price and event data from CSV files.

    Args:
        prices_path: Path to the prices CSV file (requires 'ds' datetime and 'price' columns).
        events_path: Path to the events CSV file (requires 'ds' datetime and 'event' columns).

    Returns:
        Tuple containing (prices_df, events_df) with standardized column names.

    Raises:
        FileNotFoundError: If either CSV file is not found.
        ValueError: If CSV files do not contain required columns.
    """
    try:
        logger.info(f"Loading prices from {prices_path}")
        prices_df = pd.read_csv(prices_path, parse_dates=['ds'])

        logger.info(f"Loading events from {events_path}")
        events_df = pd.read_csv(events_path, parse_dates=['ds'])

        # Rename columns to Nixtla standard
        prices_df = prices_df.rename(columns={'price': 'y'})

        # Add unique_id if not present
        if 'unique_id' not in prices_df.columns:
            prices_df['unique_id'] = 'contract_1'
            logger.info("Added default unique_id='contract_1'")

        # Validate required columns
        if 'ds' not in prices_df.columns or 'y' not in prices_df.columns:
            raise ValueError("Prices CSV must contain 'ds' (datetime) and 'price' columns.")

        if 'ds' not in events_df.columns or 'event' not in events_df.columns:
            raise ValueError("Events CSV must contain 'ds' (datetime) and 'event' columns.")

        logger.info(f"Loaded {len(prices_df)} price records and {len(events_df)} events")
        return prices_df, events_df

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise
    except ValueError as e:
        logger.error(f"Data validation error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise


def create_sample_data(prices_output: str, events_output: str) -> None:
    """
    Create sample CSV files for testing.

    Args:
        prices_output: Path to write sample prices CSV.
        events_output: Path to write sample events CSV.
    """
    prices_data = {
        'ds': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03',
                              '2023-01-04', '2023-01-05', '2023-01-06', '2023-01-07']),
        'price': [10, 12, 13, 11, 14, 15, 16]
    }
    events_data = {
        'ds': pd.to_datetime(['2023-01-04']),
        'event': ['Promotion']
    }

    pd.DataFrame(prices_data).to_csv(prices_output, index=False)
    pd.DataFrame(events_data).to_csv(events_output, index=False)
    logger.info(f"Created sample data: {prices_output}, {events_output}")


def main():
    """CLI entry point for data preparation."""
    parser = argparse.ArgumentParser(
        description='Load and validate contract price and event data for causal impact analysis.'
    )
    parser.add_argument('--prices', type=str, default='prices.csv',
                        help='Path to prices CSV (default: prices.csv)')
    parser.add_argument('--events', type=str, default='events.csv',
                        help='Path to events CSV (default: events.csv)')
    parser.add_argument('--create-sample', action='store_true',
                        help='Create sample CSV files for testing')
    parser.add_argument('--output-prices', type=str, default='prepared_prices.csv',
                        help='Path to save prepared prices (default: prepared_prices.csv)')
    parser.add_argument('--output-events', type=str, default='prepared_events.csv',
                        help='Path to save prepared events (default: prepared_events.csv)')

    args = parser.parse_args()

    try:
        if args.create_sample:
            create_sample_data(args.prices, args.events)
            logger.info("Sample data created successfully")
            return 0

        prices_df, events_df = load_data(args.prices, args.events)

        # Save prepared data
        prices_df.to_csv(args.output_prices, index=False)
        events_df.to_csv(args.output_events, index=False)

        logger.info(f"Prepared data saved to {args.output_prices} and {args.output_events}")

        print("\nPrices DataFrame:")
        print(prices_df.head())
        print(f"\nShape: {prices_df.shape}")

        print("\nEvents DataFrame:")
        print(events_df.head())
        print(f"\nShape: {events_df.shape}")

        return 0

    except Exception as e:
        logger.error(f"Error in data preparation: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
