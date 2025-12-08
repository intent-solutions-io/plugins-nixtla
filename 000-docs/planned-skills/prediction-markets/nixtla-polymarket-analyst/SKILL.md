---
name: nixtla-polymarket-analyst
description: |
  Analyzes Polymarket contracts and forecasts price movements using TimeGPT.
  Use when needing to understand market sentiment and predict contract outcomes.
  Trigger with "Polymarket analysis", "predict contract odds", "forecast Polymarket".
allowed-tools: "Read,Write,Bash,Glob,Grep,WebFetch"
version: "1.0.0"
---

# Polymarket Analyst

Analyzes and forecasts Polymarket contract prices using historical data and TimeGPT.

## Overview

Fetches Polymarket contract data, transforms it into Nixtla time series format, and generates forecasts using TimeGPT. Provides insights into potential contract outcomes and market trends. Useful for traders and analysts who want data-driven insights on prediction markets. Outputs include price forecasts, confidence intervals, and visualizations.

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep, WebFetch

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install nixtla pandas requests matplotlib
```

## Instructions

### Step 1: Fetch Contract Data

Create and run the Polymarket data fetcher:

```python
#!/usr/bin/env python3
"""
Polymarket Contract Data Fetcher
Fetches historical price data for a specific contract
"""

import requests
import json
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional

POLYMARKET_CLOB_API = "https://clob.polymarket.com"
POLYMARKET_GAMMA_API = "https://gamma-api.polymarket.com"

def fetch_contract_metadata(condition_id: str) -> Optional[Dict]:
    """Fetch contract metadata from Polymarket."""
    try:
        response = requests.get(
            f"{POLYMARKET_CLOB_API}/markets/{condition_id}",
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching metadata: {e}")
        return None

def fetch_price_history(condition_id: str, days: int = 30) -> List[Dict]:
    """
    Fetch historical price data for a contract.

    Args:
        condition_id: Polymarket contract/condition ID
        days: Number of days of history to fetch

    Returns:
        List of price points with timestamps
    """
    try:
        # Calculate time range
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)

        response = requests.get(
            f"{POLYMARKET_GAMMA_API}/markets/{condition_id}/prices",
            params={
                "start": int(start_time.timestamp()),
                "end": int(end_time.timestamp()),
                "interval": "1h"  # Hourly data
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json().get("prices", [])
    except requests.RequestException as e:
        print(f"Error fetching price history: {e}")
        return []

def get_contract_data(condition_id: str, days: int = 30) -> Dict:
    """
    Fetch complete contract data including metadata and price history.

    Args:
        condition_id: Polymarket contract ID
        days: Days of history

    Returns:
        Dict with metadata and price history
    """
    print(f"Fetching data for contract: {condition_id}")

    metadata = fetch_contract_metadata(condition_id)
    if not metadata:
        raise ValueError(f"Could not fetch metadata for {condition_id}")

    prices = fetch_price_history(condition_id, days)
    if not prices:
        raise ValueError(f"No price history available for {condition_id}")

    return {
        "condition_id": condition_id,
        "question": metadata.get("question", "Unknown"),
        "description": metadata.get("description", ""),
        "end_date": metadata.get("end_date_iso"),
        "volume": metadata.get("volume", 0),
        "liquidity": metadata.get("liquidity", 0),
        "prices": prices,
        "fetched_at": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python fetch_contract.py <condition_id> [days]")
        sys.exit(1)

    condition_id = sys.argv[1]
    days = int(sys.argv[2]) if len(sys.argv) > 2 else 30

    data = get_contract_data(condition_id, days)

    with open(f"contract_{condition_id[:8]}_data.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"Contract: {data['question'][:60]}...")
    print(f"Price points: {len(data['prices'])}")
    print(f"Saved to contract_{condition_id[:8]}_data.json")
```

### Step 2: Transform to Nixtla Time Series Format

Create the data transformation script:

```python
#!/usr/bin/env python3
"""
Transform Polymarket Data to Nixtla Format
Converts raw price data to unique_id, ds, y format
"""

import json
import pandas as pd
from datetime import datetime
from typing import Dict

def load_contract_data(filepath: str) -> Dict:
    """Load contract data from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)

def transform_to_nixtla(contract_data: Dict) -> pd.DataFrame:
    """
    Transform Polymarket price data to Nixtla format.

    Args:
        contract_data: Dict with prices list

    Returns:
        DataFrame with unique_id, ds, y columns
    """
    prices = contract_data.get("prices", [])

    if not prices:
        raise ValueError("No price data available")

    records = []
    for price_point in prices:
        # Handle different API response formats
        timestamp = price_point.get("t") or price_point.get("timestamp")
        price = price_point.get("p") or price_point.get("yes_price") or price_point.get("price")

        if timestamp and price is not None:
            # Convert timestamp (may be unix or ISO)
            if isinstance(timestamp, (int, float)):
                ds = datetime.fromtimestamp(timestamp)
            else:
                ds = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))

            records.append({
                "unique_id": contract_data.get("condition_id", "contract_1"),
                "ds": ds,
                "y": float(price)
            })

    df = pd.DataFrame(records)
    df = df.sort_values("ds").reset_index(drop=True)

    # Remove duplicates (keep last price for each timestamp)
    df = df.drop_duplicates(subset=["unique_id", "ds"], keep="last")

    return df

def validate_nixtla_data(df: pd.DataFrame) -> bool:
    """Validate the transformed data meets Nixtla requirements."""
    required_cols = ["unique_id", "ds", "y"]

    for col in required_cols:
        if col not in df.columns:
            print(f"Missing required column: {col}")
            return False

    if df["y"].isna().any():
        print(f"Warning: {df['y'].isna().sum()} null values in y column")

    if len(df) < 10:
        print(f"Warning: Only {len(df)} data points - may be insufficient for forecasting")

    return True

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python transform_data.py <contract_data.json>")
        sys.exit(1)

    filepath = sys.argv[1]
    contract_data = load_contract_data(filepath)

    df = transform_to_nixtla(contract_data)

    if validate_nixtla_data(df):
        output_file = filepath.replace("_data.json", "_nixtla.csv")
        df.to_csv(output_file, index=False)

        print(f"Transformed {len(df)} price points to Nixtla format")
        print(f"Date range: {df['ds'].min()} to {df['ds'].max()}")
        print(f"Price range: {df['y'].min():.4f} to {df['y'].max():.4f}")
        print(f"Saved to {output_file}")
```

### Step 3: Forecast with TimeGPT

Create the forecasting script:

```python
#!/usr/bin/env python3
"""
Polymarket Contract Forecaster
Uses TimeGPT to forecast contract prices
"""

import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from typing import Dict, Optional, Tuple

def check_api_key() -> str:
    """Verify TimeGPT API key is set."""
    api_key = os.getenv("NIXTLA_TIMEGPT_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "NIXTLA_TIMEGPT_API_KEY not set. "
            "Get your key at https://dashboard.nixtla.io"
        )
    return api_key

def load_nixtla_data(filepath: str) -> pd.DataFrame:
    """Load Nixtla-formatted data."""
    df = pd.read_csv(filepath, parse_dates=["ds"])
    return df

def forecast_with_timegpt(
    df: pd.DataFrame,
    horizon: int = 24,
    freq: str = "H",
    levels: list = [80, 90, 95]
) -> Tuple[pd.DataFrame, Dict]:
    """
    Generate forecasts using TimeGPT.

    Args:
        df: DataFrame in Nixtla format (unique_id, ds, y)
        horizon: Number of periods to forecast
        freq: Frequency string (H=hourly, D=daily)
        levels: Confidence interval levels

    Returns:
        Tuple of (forecast DataFrame, metadata dict)
    """
    from nixtla import NixtlaClient

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

if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Forecast Polymarket contract prices")
    parser.add_argument("data_file", help="Path to Nixtla-formatted CSV")
    parser.add_argument("--horizon", type=int, default=24, help="Forecast horizon")
    parser.add_argument("--freq", default="H", help="Frequency (H=hourly, D=daily)")
    parser.add_argument("--output", default="forecast", help="Output file prefix")

    args = parser.parse_args()

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
    print("\n⚠️  " + analysis['disclaimer'])
```

### Step 4: Complete Workflow Script

Create a single script to run the entire pipeline:

```python
#!/usr/bin/env python3
"""
Complete Polymarket Analysis Pipeline
Fetches, transforms, and forecasts contract prices
"""

import os
import sys
import json
import pandas as pd
from datetime import datetime

def run_polymarket_analysis(
    condition_id: str,
    horizon: int = 24,
    days_history: int = 30,
    output_dir: str = "."
) -> Dict:
    """
    Run complete Polymarket analysis pipeline.

    Args:
        condition_id: Polymarket contract ID
        horizon: Forecast horizon in periods
        days_history: Days of historical data to fetch
        output_dir: Directory for output files

    Returns:
        Dict with analysis results and file paths
    """
    from fetch_contract import get_contract_data
    from transform_data import transform_to_nixtla
    from forecast_contract import (
        forecast_with_timegpt,
        create_forecast_plot,
        analyze_forecast
    )

    print(f"\n{'='*60}")
    print(f"POLYMARKET CONTRACT ANALYSIS")
    print(f"Contract: {condition_id}")
    print(f"{'='*60}\n")

    # Step 1: Fetch data
    print("Step 1: Fetching contract data...")
    contract_data = get_contract_data(condition_id, days_history)
    print(f"  ✓ Fetched {len(contract_data['prices'])} price points")

    # Step 2: Transform data
    print("\nStep 2: Transforming to Nixtla format...")
    df = transform_to_nixtla(contract_data)
    print(f"  ✓ Transformed to {len(df)} time series points")

    # Infer frequency
    if len(df) > 1:
        time_diff = (df["ds"].iloc[1] - df["ds"].iloc[0]).total_seconds()
        freq = "H" if time_diff <= 3600 else "D"
    else:
        freq = "H"

    # Step 3: Forecast
    print(f"\nStep 3: Forecasting {horizon} periods ahead...")
    forecast_df, metadata = forecast_with_timegpt(df, horizon=horizon, freq=freq)
    print(f"  ✓ Generated forecast with confidence intervals")

    # Step 4: Analyze and save
    print("\nStep 4: Generating outputs...")

    # Save files
    prefix = f"{output_dir}/polymarket_{condition_id[:8]}"

    df.to_csv(f"{prefix}_historical.csv", index=False)
    forecast_df.to_csv(f"{prefix}_forecast.csv", index=False)

    create_forecast_plot(
        historical=df,
        forecast=forecast_df,
        title=f"Polymarket: {contract_data['question'][:50]}...",
        output_path=f"{prefix}_plot.png"
    )

    # Analyze
    current_price = df["y"].iloc[-1]
    analysis = analyze_forecast(forecast_df, current_price)

    # Complete output
    output = {
        "contract_id": condition_id,
        "question": contract_data["question"],
        "analysis": analysis,
        "metadata": metadata,
        "files": {
            "historical": f"{prefix}_historical.csv",
            "forecast": f"{prefix}_forecast.csv",
            "plot": f"{prefix}_plot.png"
        }
    }

    with open(f"{prefix}_analysis.json", "w") as f:
        json.dump(output, f, indent=2, default=str)

    # Print summary
    print(f"\n{'='*60}")
    print("ANALYSIS COMPLETE")
    print(f"{'='*60}")
    print(f"\nContract: {contract_data['question'][:60]}...")
    print(f"\nCurrent Price: ${analysis['current_price']:.4f}")
    print(f"Forecast Price: ${analysis['forecast_price']:.4f}")
    print(f"Expected Change: {analysis['pct_change']:+.2f}%")
    print(f"\n📊 SIGNAL: {analysis['signal']} ({analysis['trend']})")
    print(f"\nOutput files:")
    for name, path in output["files"].items():
        print(f"  - {name}: {path}")
    print(f"\n⚠️  {analysis['disclaimer']}")

    return output

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Analyze Polymarket contract")
    parser.add_argument("contract_id", help="Polymarket condition ID")
    parser.add_argument("--horizon", type=int, default=24, help="Forecast horizon")
    parser.add_argument("--days", type=int, default=30, help="Days of history")
    parser.add_argument("--output-dir", default=".", help="Output directory")

    args = parser.parse_args()

    run_polymarket_analysis(
        condition_id=args.contract_id,
        horizon=args.horizon,
        days_history=args.days,
        output_dir=args.output_dir
    )
```

## Output

- **polymarket_{id}_historical.csv**: Historical price data in Nixtla format
- **polymarket_{id}_forecast.csv**: Price forecasts with confidence intervals
- **polymarket_{id}_plot.png**: Visualization of historical vs forecast
- **polymarket_{id}_analysis.json**: Complete analysis with metadata

## Error Handling

1. **Error**: `Invalid contract ID`
   **Solution**: Verify the condition_id from Polymarket URL or API. Format is typically a hex string.

2. **Error**: `NIXTLA_TIMEGPT_API_KEY not set`
   **Solution**:
   ```bash
   export NIXTLA_TIMEGPT_API_KEY='your-api-key'
   # Get key at https://dashboard.nixtla.io
   ```

3. **Error**: `Insufficient data`
   **Solution**: Contract may be new. Try increasing `--days` or wait for more trading activity.

4. **Error**: `API rate limit exceeded`
   **Solution**: Wait 60 seconds and retry. Consider caching fetched data.

## Examples

### Example 1: Election Contract Analysis

**Input**:
```bash
python analyze_polymarket.py 0x1234abcd --horizon 48 --days 60
```

**Output**:
```
ANALYSIS COMPLETE
Contract: "Will candidate X win the 2024 election?"

Current Price: $0.4500
Forecast Price: $0.5200
Expected Change: +15.56%

📊 SIGNAL: BUY (BULLISH)

Output files:
  - historical: polymarket_1234abcd_historical.csv
  - forecast: polymarket_1234abcd_forecast.csv
  - plot: polymarket_1234abcd_plot.png
```

### Example 2: Crypto Price Contract

**Input**:
```bash
python analyze_polymarket.py 0xdef456 --horizon 24 --days 14
```

**Output**:
```
ANALYSIS COMPLETE
Contract: "Will ETH be above $3000 on Dec 31?"

Current Price: $0.6800
Forecast Price: $0.6500
Expected Change: -4.41%

📊 SIGNAL: HOLD (NEUTRAL)
```

## Usage

Complete workflow:

```bash
# Set API key
export NIXTLA_TIMEGPT_API_KEY='your-key'

# Run analysis
python analyze_polymarket.py <contract_id> --horizon 48 --days 30

# Or run individual steps:
python fetch_contract.py <contract_id> 30
python transform_data.py contract_<id>_data.json
python forecast_contract.py contract_<id>_nixtla.csv --horizon 48
```

## Risk Disclaimer

- Forecasts are probabilistic estimates, not guarantees
- Past performance does not indicate future results
- Always verify data before making trading decisions
- Consider market liquidity and execution costs
- This is not financial advice
