#!/usr/bin/env python3
"""
configure_model.py - Configure event periods and treatment/control groups.

This script defines event windows for causal impact analysis, marking treatment
and control periods in the price data.
"""

import argparse
import logging
import sys
from typing import List, Tuple

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def configure_event_periods(
    prices_df: pd.DataFrame, events_df: pd.DataFrame, window_days: int = 3
) -> List[Tuple[pd.Timestamp, pd.Timestamp]]:
    """
    Configure event periods for causal impact analysis.

    Args:
        prices_df: DataFrame containing price data with 'ds' column.
        events_df: DataFrame containing event data with 'ds' and 'event' columns.
        window_days: Number of days before/after event to include (default: 3).

    Returns:
        List of (start_date, end_date) tuples representing event periods.

    Raises:
        ValueError: If event dates fall outside the price data range.
    """
    try:
        event_periods: List[Tuple[pd.Timestamp, pd.Timestamp]] = []
        min_date = prices_df["ds"].min()
        max_date = prices_df["ds"].max()

        logger.info(f"Price data range: {min_date} to {max_date}")
        logger.info(f"Configuring events with {window_days}-day window")

        for _, row in events_df.iterrows():
            event_date = row["ds"]
            event_name = row["event"]

            # Define window around the event
            start_date = event_date - pd.Timedelta(days=window_days)
            end_date = event_date + pd.Timedelta(days=window_days)

            if start_date < min_date or end_date > max_date:
                raise ValueError(
                    f"Event '{event_name}' dates ({start_date} to {end_date}) "
                    f"fall outside price range ({min_date} to {max_date})"
                )

            event_periods.append((start_date, end_date))
            logger.info(f"Event '{event_name}': {start_date} to {end_date}")

        return event_periods

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise


def create_treatment_control_df(
    prices_df: pd.DataFrame, event_periods: List[Tuple[pd.Timestamp, pd.Timestamp]]
) -> pd.DataFrame:
    """
    Mark treatment and control periods in the price data.

    Args:
        prices_df: DataFrame containing price data with 'ds' column.
        event_periods: List of (start_date, end_date) tuples for treatment periods.

    Returns:
        DataFrame with added 'treatment' column (1=treatment, 0=control).
    """
    prices_df = prices_df.copy()
    prices_df["treatment"] = 0  # Initialize as control period

    for start_date, end_date in event_periods:
        mask = (prices_df["ds"] >= start_date) & (prices_df["ds"] <= end_date)
        prices_df.loc[mask, "treatment"] = 1

    treatment_count = (prices_df["treatment"] == 1).sum()
    control_count = (prices_df["treatment"] == 0).sum()

    logger.info(f"Treatment periods: {treatment_count} observations")
    logger.info(f"Control periods: {control_count} observations")

    return prices_df


def main():
    """CLI entry point for model configuration."""
    parser = argparse.ArgumentParser(
        description="Configure event periods and treatment/control groups for causal analysis."
    )
    parser.add_argument("--prices", type=str, required=True, help="Path to prepared prices CSV")
    parser.add_argument("--events", type=str, required=True, help="Path to prepared events CSV")
    parser.add_argument(
        "--window-days", type=int, default=3, help="Event window size in days (default: 3)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="configured_prices.csv",
        help="Path to save configured data (default: configured_prices.csv)",
    )

    args = parser.parse_args()

    try:
        logger.info(f"Loading data from {args.prices} and {args.events}")
        prices_df = pd.read_csv(args.prices, parse_dates=["ds"])
        events_df = pd.read_csv(args.events, parse_dates=["ds"])

        event_periods = configure_event_periods(prices_df, events_df, args.window_days)
        configured_df = create_treatment_control_df(prices_df, event_periods)

        # Save configured data
        configured_df.to_csv(args.output, index=False)
        logger.info(f"Configured data saved to {args.output}")

        print("\nConfigured DataFrame:")
        print(configured_df.head(10))
        print(f"\nShape: {configured_df.shape}")
        print(f"\nTreatment distribution:")
        print(configured_df["treatment"].value_counts())

        return 0

    except Exception as e:
        logger.error(f"Error in model configuration: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
