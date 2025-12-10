#!/usr/bin/env python3
"""
Polymarket Contract Forecaster

Uses TimeGPT to forecast contract prices with confidence intervals.
Generates forecasts, plots, and analysis reports.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Dict, Tuple

import matplotlib.pyplot as plt
import pandas as pd


def check_api_key() -> str:
    """
    Verify TimeGPT API key is set.

    Returns:
        API key string

    Raises:
        EnvironmentError: If API key not found
    """
    api_key = os.getenv("NIXTLA_TIMEGPT_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "NIXTLA_TIMEGPT_API_KEY not set. "
            "Get your key at https://dashboard.nixtla.io"
        )
    return api_key


def load_nixtla_data(filepath: str) -> pd.DataFrame:
    """
    Load Nixtla-formatted data.

    Args:
        filepath: Path to CSV file with unique_id, ds, y columns

    Returns:
        DataFrame with parsed datetime column
    """
    df = pd.read_csv(filepath, parse_dates=["ds"])
    return df


def forecast_with_timegpt(
    df: pd.DataFrame,
    horizon: int = 24,
    freq: str = "H",
    levels: list = None
) -> Tuple[pd.DataFrame, Dict]:
    """
    Generate forecasts using TimeGPT.

    Args:
        df: DataFrame in Nixtla format (unique_id, ds, y)
        horizon: Number of periods to forecast
        freq: Frequency string (H=hourly, D=daily)
        levels: Confidence interval levels (default: [80, 90, 95])

    Returns:
        Tuple of (forecast DataFrame, metadata dict)
    """
    from nixtla import NixtlaClient

    if levels is None:
        levels = [80, 90, 95]

    api_key = check_api_key()
    client = NixtlaClient(api_key=api_key)

    print(f"Forecasting {horizon} periods ahead...")

    # Generate forecast with prediction intervals
    forecast_df = client.forecast(
        df=df,
        h=horizon,
        freq=freq,
        level=levels,
        time_col="ds",
        target_col="y"
    )

    metadata = {
        "horizon": horizon,
        "freq": freq,
        "levels": levels,
        "forecast_generated_at": datetime.now().isoformat(),
        "input_rows": len(df),
        "last_observed": df["ds"].max().isoformat(),
        "model": "TimeGPT"
    }

    return forecast_df, metadata


def create_forecast_plot(
    historical: pd.DataFrame,
    forecast: pd.DataFrame,
    title: str = "Polymarket Contract Forecast",
    output_path: str = "forecast_plot.png"
) -> None:
    """
    Create visualization of historical data and forecast.

    Args:
        historical: Historical price data
        forecast: Forecast data with prediction intervals
        title: Plot title
        output_path: Where to save the plot
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot historical data
    ax.plot(
        historical["ds"],
        historical["y"],
        label="Historical",
        color="blue",
        linewidth=1.5
    )

    # Plot forecast
    ax.plot(
        forecast["ds"],
        forecast["TimeGPT"],
        label="Forecast",
        color="red",
        linewidth=2
    )

    # Plot confidence intervals if available
    if "TimeGPT-lo-95" in forecast.columns:
        ax.fill_between(
            forecast["ds"],
            forecast["TimeGPT-lo-95"],
            forecast["TimeGPT-hi-95"],
            alpha=0.2,
            color="red",
            label="95% CI"
        )

    if "TimeGPT-lo-80" in forecast.columns:
        ax.fill_between(
            forecast["ds"],
            forecast["TimeGPT-lo-80"],
            forecast["TimeGPT-hi-80"],
            alpha=0.3,
            color="red",
            label="80% CI"
        )

    ax.set_xlabel("Date")
    ax.set_ylabel("Contract Price")
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Add horizontal lines for key levels
    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5, label="50% odds")
    ax.axhline(y=1.0, color="green", linestyle="--", alpha=0.3)
    ax.axhline(y=0.0, color="red", linestyle="--", alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

    print(f"Plot saved to {output_path}")


def analyze_forecast(forecast: pd.DataFrame, current_price: float) -> Dict:
    """
    Analyze forecast results and generate insights.

    Args:
        forecast: Forecast DataFrame
        current_price: Current contract price

    Returns:
        Dict with analysis results
    """
    final_forecast = forecast["TimeGPT"].iloc[-1]

    # Calculate expected change
    price_change = final_forecast - current_price
    pct_change = (price_change / current_price) * 100

    # Determine trend
    if pct_change > 5:
        trend = "BULLISH"
        signal = "BUY"
    elif pct_change < -5:
        trend = "BEARISH"
        signal = "SELL"
    else:
        trend = "NEUTRAL"
        signal = "HOLD"

    # Calculate confidence bounds
    lo_95 = forecast["TimeGPT-lo-95"].iloc[-1] if "TimeGPT-lo-95" in forecast.columns else None
    hi_95 = forecast["TimeGPT-hi-95"].iloc[-1] if "TimeGPT-hi-95" in forecast.columns else None

    return {
        "current_price": current_price,
        "forecast_price": final_forecast,
        "price_change": price_change,
        "pct_change": pct_change,
        "trend": trend,
        "signal": signal,
        "confidence_low_95": lo_95,
        "confidence_high_95": hi_95,
        "forecast_horizon": len(forecast),
        "disclaimer": "This is not financial advice. Predictions are probabilistic estimates."
    }


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Forecast Polymarket contract prices with TimeGPT"
    )
    parser.add_argument(
        "data_file",
        help="Path to Nixtla-formatted CSV"
    )
    parser.add_argument(
        "--horizon",
        type=int,
        default=24,
        help="Forecast horizon (default: 24)"
    )
    parser.add_argument(
        "--freq",
        default="H",
        help="Frequency (H=hourly, D=daily, default: H)"
    )
    parser.add_argument(
        "--output",
        default="forecast",
        help="Output file prefix (default: forecast)"
    )

    args = parser.parse_args()

    try:
        # Load data
        df = load_nixtla_data(args.data_file)
        print(f"Loaded {len(df)} historical price points")

        # Generate forecast
        forecast_df, metadata = forecast_with_timegpt(
            df,
            horizon=args.horizon,
            freq=args.freq
        )

        # Save forecast
        forecast_df.to_csv(f"{args.output}_forecast.csv", index=False)
        print(f"Forecast saved to {args.output}_forecast.csv")

        # Create plot
        create_forecast_plot(
            historical=df,
            forecast=forecast_df,
            output_path=f"{args.output}_plot.png"
        )

        # Analyze results
        current_price = df["y"].iloc[-1]
        analysis = analyze_forecast(forecast_df, current_price)

        # Save metadata and analysis
        output_meta = {**metadata, "analysis": analysis}
        with open(f"{args.output}_metadata.json", "w") as f:
            json.dump(output_meta, f, indent=2, default=str)

        # Print summary
        print("\n" + "="*50)
        print("FORECAST SUMMARY")
        print("="*50)
        print(f"Current Price: {analysis['current_price']:.4f}")
        print(f"Forecast Price: {analysis['forecast_price']:.4f}")
        print(f"Expected Change: {analysis['pct_change']:+.2f}%")
        print(f"Trend: {analysis['trend']}")
        print(f"Signal: {analysis['signal']}")
        if analysis['confidence_low_95'] and analysis['confidence_high_95']:
            print(f"95% CI: [{analysis['confidence_low_95']:.4f}, {analysis['confidence_high_95']:.4f}]")
        print(f"\n{analysis['disclaimer']}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
