#!/usr/bin/env python3
"""
analyze_impact.py - Run causal impact analysis with TimeGPT.

This script performs causal impact analysis to quantify the effect of events on
contract prices using CausalImpact and TimeGPT forecasting.
"""

import argparse
import logging
import os
import sys
from typing import List, Tuple

import pandas as pd
from causalimpact import CausalImpact

from nixtla import NixtlaClient

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def analyze_event_impact(
    prices_df: pd.DataFrame,
    event_periods: List[Tuple[pd.Timestamp, pd.Timestamp]],
    niter: int = 1000,
) -> Tuple[pd.DataFrame, pd.DataFrame, str]:
    """
    Analyze the impact of events on contract prices using CausalImpact and TimeGPT.

    Args:
        prices_df: DataFrame with 'ds', 'y', and 'unique_id' columns.
        event_periods: List of (start_date, end_date) tuples for events.
        niter: Number of MCMC iterations for CausalImpact (default: 1000).

    Returns:
        Tuple of (impact_results_df, adjusted_forecast_df, causal_impact_summary).

    Raises:
        ValueError: If NIXTLA_TIMEGPT_API_KEY is not set.
        RuntimeError: If analysis fails.
    """
    try:
        # Validate API key
        api_key = os.getenv("NIXTLA_TIMEGPT_API_KEY")
        if not api_key:
            raise ValueError("NIXTLA_TIMEGPT_API_KEY environment variable not set")

        # Sort and prepare data
        prices_df = prices_df.sort_values(by="ds")
        prices_indexed = prices_df.set_index("ds")

        # Define intervention dates
        intervention_dates = []
        for start_date, end_date in event_periods:
            intervention_dates.extend(pd.date_range(start_date, end_date))

        # Define pre and post periods
        pre_period = [prices_indexed.index.min(), intervention_dates[0] - pd.Timedelta(days=1)]
        post_period = [intervention_dates[0], prices_indexed.index.max()]

        logger.info(f"Pre-intervention period: {pre_period[0]} to {pre_period[1]}")
        logger.info(f"Post-intervention period: {post_period[0]} to {post_period[1]}")

        # Run CausalImpact analysis
        logger.info(f"Running CausalImpact with {niter} iterations")
        causal_impact = CausalImpact(prices_indexed["y"], pre_period, post_period, niter=niter)

        # Extract results
        summary = causal_impact.summary(output="report")
        results = causal_impact.inferences

        # Calculate impact metrics
        absolute_effect = results["point_effects"].sum()
        relative_effect = absolute_effect / prices_indexed["y"].mean()

        impact_results = pd.DataFrame(
            {
                "event": [f"Event_{i+1}" for i in range(len(event_periods))],
                "absolute_effect": [absolute_effect],
                "relative_effect": [relative_effect],
                "avg_price": [prices_indexed["y"].mean()],
            }
        )

        logger.info(f"Absolute effect: {absolute_effect:.2f}")
        logger.info(f"Relative effect: {relative_effect:.2%}")

        # Generate TimeGPT forecast
        logger.info("Generating TimeGPT adjusted forecast")
        client = NixtlaClient(api_key=api_key)

        prices_df_reset = prices_indexed.reset_index()
        forecast = client.forecast(
            df=prices_df_reset[["unique_id", "ds", "y"]], h=len(prices_df_reset), freq="D"
        )

        # Merge forecast with original data
        adjusted_forecast = pd.merge(prices_df_reset, forecast, on=["unique_id", "ds"], how="left")

        logger.info("Analysis completed successfully")
        return impact_results, adjusted_forecast, summary

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise


def main():
    """CLI entry point for causal impact analysis."""
    parser = argparse.ArgumentParser(
        description="Run causal impact analysis on contract prices with TimeGPT."
    )
    parser.add_argument("--prices", type=str, required=True, help="Path to configured prices CSV")
    parser.add_argument("--events", type=str, required=True, help="Path to events CSV")
    parser.add_argument(
        "--niter", type=int, default=1000, help="MCMC iterations for CausalImpact (default: 1000)"
    )
    parser.add_argument(
        "--window-days", type=int, default=3, help="Event window size in days (default: 3)"
    )
    parser.add_argument(
        "--output-impact",
        type=str,
        default="impact_results.csv",
        help="Path to save impact results (default: impact_results.csv)",
    )
    parser.add_argument(
        "--output-forecast",
        type=str,
        default="adjusted_forecast.csv",
        help="Path to save adjusted forecast (default: adjusted_forecast.csv)",
    )
    parser.add_argument(
        "--output-summary",
        type=str,
        default="causal_summary.txt",
        help="Path to save CausalImpact summary (default: causal_summary.txt)",
    )

    args = parser.parse_args()

    try:
        logger.info(f"Loading data from {args.prices} and {args.events}")
        prices_df = pd.read_csv(args.prices, parse_dates=["ds"])
        events_df = pd.read_csv(args.events, parse_dates=["ds"])

        # Configure event periods
        event_periods = []
        for _, row in events_df.iterrows():
            event_date = row["ds"]
            start_date = event_date - pd.Timedelta(days=args.window_days)
            end_date = event_date + pd.Timedelta(days=args.window_days)
            event_periods.append((start_date, end_date))

        # Run analysis
        impact_results, adjusted_forecast, summary = analyze_event_impact(
            prices_df, event_periods, args.niter
        )

        # Save outputs
        impact_results.to_csv(args.output_impact, index=False)
        adjusted_forecast.to_csv(args.output_forecast, index=False)

        with open(args.output_summary, "w") as f:
            f.write(summary)

        logger.info(f"Impact results saved to {args.output_impact}")
        logger.info(f"Adjusted forecast saved to {args.output_forecast}")
        logger.info(f"CausalImpact summary saved to {args.output_summary}")

        print("\nImpact Results:")
        print(impact_results)
        print("\nAdjusted Forecast (first 10 rows):")
        print(adjusted_forecast.head(10))

        return 0

    except Exception as e:
        logger.error(f"Error in analysis: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
