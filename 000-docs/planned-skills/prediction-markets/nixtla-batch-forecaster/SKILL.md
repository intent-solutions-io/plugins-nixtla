---
name: nixtla-batch-forecaster
description: |
  Forecasts multiple time series in parallel batches using TimeGPT API.
  Use when processing 10-100 contracts, performing portfolio aggregation, or needing efficient forecasting.
  Trigger with "batch forecast", "portfolio forecast", "parallel forecasting".
allowed-tools: "Read,Write,Bash,Glob,Grep"
version: "1.0.0"
---

# Batch Forecaster

Processes multiple time series forecasts in parallel, optimizing throughput with TimeGPT.

## Purpose

Generate forecasts for many time series efficiently, handling portfolio aggregation where needed.

## Overview

Leverages TimeGPT API to produce forecasts for multiple time series concurrently. Optimizes performance by processing in parallel batches with rate limiting. Supports portfolio-level aggregation. Outputs individual forecasts and optional aggregated view.

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install nixtla pandas numpy tqdm
```

## Instructions

### Step 1: Prepare Input Data

Create data loading and validation script:

```python
#!/usr/bin/env python3
"""
Batch Forecaster - Data Preparation
Validates and prepares multi-series data for batch forecasting
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple

def load_multi_series_data(filepath: str) -> pd.DataFrame:
    """
    Load and validate multi-series time series data.

    Args:
        filepath: Path to CSV with columns (unique_id, ds, y)

    Returns:
        Validated DataFrame in Nixtla format
    """
    print(f"Loading data from {filepath}...")

    df = pd.read_csv(filepath)

    # Validate required columns
    required_cols = ["unique_id", "ds", "y"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Convert types
    df["ds"] = pd.to_datetime(df["ds"])
    df["y"] = pd.to_numeric(df["y"], errors="coerce")
    df["unique_id"] = df["unique_id"].astype(str)

    # Remove nulls
    null_count = df["y"].isna().sum()
    if null_count > 0:
        print(f"Warning: Dropping {null_count} rows with null y values")
        df = df.dropna(subset=["y"])

    # Sort by series and time
    df = df.sort_values(["unique_id", "ds"]).reset_index(drop=True)

    return df

def analyze_series(df: pd.DataFrame) -> Dict:
    """
    Analyze the multi-series dataset.

    Returns:
        Dict with series statistics
    """
    series_counts = df.groupby("unique_id").size()

    stats = {
        "total_rows": len(df),
        "num_series": df["unique_id"].nunique(),
        "series_list": df["unique_id"].unique().tolist(),
        "min_length": series_counts.min(),
        "max_length": series_counts.max(),
        "avg_length": series_counts.mean(),
        "date_range": {
            "min": df["ds"].min().isoformat(),
            "max": df["ds"].max().isoformat()
        },
        "value_range": {
            "min": df["y"].min(),
            "max": df["y"].max(),
            "mean": df["y"].mean()
        }
    }

    return stats

def split_into_batches(
    df: pd.DataFrame,
    batch_size: int = 10
) -> List[pd.DataFrame]:
    """
    Split multi-series data into batches by unique_id.

    Args:
        df: Full dataset
        batch_size: Number of series per batch

    Returns:
        List of DataFrames, each containing batch_size series
    """
    series_ids = df["unique_id"].unique()
    batches = []

    for i in range(0, len(series_ids), batch_size):
        batch_ids = series_ids[i:i + batch_size]
        batch_df = df[df["unique_id"].isin(batch_ids)]
        batches.append(batch_df)

    print(f"Split {len(series_ids)} series into {len(batches)} batches")
    return batches

if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python prepare_data.py <input.csv>")
        sys.exit(1)

    filepath = sys.argv[1]
    df = load_multi_series_data(filepath)
    stats = analyze_series(df)

    print("\n" + "="*50)
    print("DATASET ANALYSIS")
    print("="*50)
    print(f"Total rows: {stats['total_rows']:,}")
    print(f"Number of series: {stats['num_series']}")
    print(f"Series length: {stats['min_length']} - {stats['max_length']} (avg: {stats['avg_length']:.0f})")
    print(f"Date range: {stats['date_range']['min']} to {stats['date_range']['max']}")
    print(f"Value range: {stats['value_range']['min']:.4f} to {stats['value_range']['max']:.4f}")

    # Save stats
    with open("data_stats.json", "w") as f:
        json.dump(stats, f, indent=2, default=str)
    print("\nSaved analysis to data_stats.json")
```

### Step 2: Batch Forecasting Engine

Create the main batch forecasting script:

```python
#!/usr/bin/env python3
"""
Batch Forecaster - Main Engine
Forecasts multiple time series in parallel with rate limiting
"""

import os
import json
import time
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def check_api_key() -> str:
    """Verify TimeGPT API key."""
    api_key = os.getenv("NIXTLA_TIMEGPT_API_KEY")
    if not api_key:
        raise EnvironmentError("NIXTLA_TIMEGPT_API_KEY not set")
    return api_key

def forecast_single_series(
    client,
    df: pd.DataFrame,
    horizon: int,
    freq: str,
    levels: List[int] = [80, 90]
) -> Tuple[str, pd.DataFrame, Optional[str]]:
    """
    Forecast a single time series.

    Returns:
        Tuple of (unique_id, forecast_df, error_message)
    """
    unique_id = df["unique_id"].iloc[0]

    try:
        forecast = client.forecast(
            df=df,
            h=horizon,
            freq=freq,
            level=levels
        )
        return (unique_id, forecast, None)

    except Exception as e:
        return (unique_id, None, str(e))

def forecast_batch(
    client,
    batch_df: pd.DataFrame,
    horizon: int,
    freq: str,
    levels: List[int] = [80, 90]
) -> Tuple[pd.DataFrame, List[Dict]]:
    """
    Forecast an entire batch of series at once.

    TimeGPT API supports multi-series forecasting natively,
    which is more efficient than individual calls.

    Returns:
        Tuple of (combined_forecasts, errors)
    """
    errors = []

    try:
        # TimeGPT handles multiple unique_ids in one call
        forecasts = client.forecast(
            df=batch_df,
            h=horizon,
            freq=freq,
            level=levels
        )
        return (forecasts, errors)

    except Exception as e:
        # If batch fails, try individual series
        print(f"Batch failed, falling back to individual: {e}")

        all_forecasts = []
        for uid in batch_df["unique_id"].unique():
            series_df = batch_df[batch_df["unique_id"] == uid]
            uid, forecast, error = forecast_single_series(
                client, series_df, horizon, freq, levels
            )
            if error:
                errors.append({"unique_id": uid, "error": error})
            elif forecast is not None:
                all_forecasts.append(forecast)

        if all_forecasts:
            return (pd.concat(all_forecasts, ignore_index=True), errors)
        return (pd.DataFrame(), errors)

def run_batch_forecast(
    input_path: str,
    horizon: int = 14,
    freq: str = "D",
    batch_size: int = 20,
    output_dir: str = "forecasts",
    aggregate: bool = False,
    rate_limit_delay: float = 1.0
) -> Dict:
    """
    Run batch forecasting on multi-series data.

    Args:
        input_path: Path to input CSV
        horizon: Forecast horizon
        freq: Frequency string (D, H, W, M)
        batch_size: Number of series per batch
        output_dir: Directory for output files
        aggregate: Whether to create aggregated forecast
        rate_limit_delay: Seconds between batches

    Returns:
        Dict with results summary
    """
    from nixtla import NixtlaClient
    from prepare_data import load_multi_series_data, split_into_batches, analyze_series

    # Initialize
    check_api_key()
    client = NixtlaClient()

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Load and prepare data
    print("Loading data...")
    df = load_multi_series_data(input_path)
    stats = analyze_series(df)

    print(f"\nForecasting {stats['num_series']} series, horizon={horizon}, freq={freq}")

    # Split into batches
    batches = split_into_batches(df, batch_size)

    # Process batches
    all_forecasts = []
    all_errors = []

    print(f"\nProcessing {len(batches)} batches...")
    for i, batch_df in enumerate(tqdm(batches, desc="Batches")):
        forecasts, errors = forecast_batch(
            client, batch_df, horizon, freq
        )

        if not forecasts.empty:
            all_forecasts.append(forecasts)
        all_errors.extend(errors)

        # Rate limiting
        if i < len(batches) - 1:
            time.sleep(rate_limit_delay)

    # Combine results
    if not all_forecasts:
        raise RuntimeError("No forecasts generated!")

    combined = pd.concat(all_forecasts, ignore_index=True)

    # Save individual forecasts
    for uid in combined["unique_id"].unique():
        uid_df = combined[combined["unique_id"] == uid]
        uid_safe = uid.replace("/", "_").replace("\\", "_")
        uid_df.to_csv(f"{output_dir}/{uid_safe}_forecast.csv", index=False)

    # Save combined
    combined.to_csv(f"{output_dir}/all_forecasts.csv", index=False)

    # Aggregation
    aggregated = None
    if aggregate:
        print("\nAggregating forecasts...")
        aggregated = combined.groupby("ds").agg({
            "TimeGPT": "sum",
            "TimeGPT-lo-80": "sum",
            "TimeGPT-hi-80": "sum",
            "TimeGPT-lo-90": "sum",
            "TimeGPT-hi-90": "sum"
        }).reset_index()
        aggregated["unique_id"] = "AGGREGATED"
        aggregated.to_csv(f"{output_dir}/aggregated_forecast.csv", index=False)

    # Summary
    summary = {
        "input_file": input_path,
        "total_series": stats["num_series"],
        "series_forecasted": combined["unique_id"].nunique(),
        "horizon": horizon,
        "freq": freq,
        "batch_size": batch_size,
        "num_batches": len(batches),
        "errors": all_errors,
        "error_count": len(all_errors),
        "success_rate": (stats["num_series"] - len(all_errors)) / stats["num_series"] * 100,
        "output_dir": output_dir,
        "aggregated": aggregate,
        "timestamp": datetime.now().isoformat()
    }

    with open(f"{output_dir}/summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    return summary

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Batch forecast multiple time series")
    parser.add_argument("input", help="Input CSV path")
    parser.add_argument("--horizon", type=int, default=14, help="Forecast horizon")
    parser.add_argument("--freq", default="D", help="Frequency (D, H, W, M)")
    parser.add_argument("--batch-size", type=int, default=20, help="Series per batch")
    parser.add_argument("--output-dir", default="forecasts", help="Output directory")
    parser.add_argument("--aggregate", action="store_true", help="Create aggregated forecast")
    parser.add_argument("--delay", type=float, default=1.0, help="Rate limit delay (seconds)")

    args = parser.parse_args()

    summary = run_batch_forecast(
        input_path=args.input,
        horizon=args.horizon,
        freq=args.freq,
        batch_size=args.batch_size,
        output_dir=args.output_dir,
        aggregate=args.aggregate,
        rate_limit_delay=args.delay
    )

    print("\n" + "="*50)
    print("BATCH FORECAST COMPLETE")
    print("="*50)
    print(f"Series forecasted: {summary['series_forecasted']}/{summary['total_series']}")
    print(f"Success rate: {summary['success_rate']:.1f}%")
    print(f"Errors: {summary['error_count']}")
    print(f"Output: {summary['output_dir']}/")
    if summary['aggregated']:
        print(f"Aggregated: {summary['output_dir']}/aggregated_forecast.csv")
```

### Step 3: Report Generator

Create summary report generator:

```python
#!/usr/bin/env python3
"""
Batch Forecaster - Report Generator
Creates summary reports from batch forecasting results
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime

def generate_batch_report(output_dir: str = "forecasts") -> str:
    """Generate markdown report from batch forecast results."""

    # Load summary
    summary_path = Path(output_dir) / "summary.json"
    if not summary_path.exists():
        raise FileNotFoundError(f"No summary.json in {output_dir}")

    with open(summary_path) as f:
        summary = json.load(f)

    # Load combined forecasts
    combined_path = Path(output_dir) / "all_forecasts.csv"
    forecasts = pd.read_csv(combined_path, parse_dates=["ds"])

    # Generate report
    report = f"""# Batch Forecast Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Input File**: {summary['input_file']}

## Summary

| Metric | Value |
|--------|-------|
| Total Series | {summary['total_series']} |
| Successfully Forecasted | {summary['series_forecasted']} |
| Success Rate | {summary['success_rate']:.1f}% |
| Forecast Horizon | {summary['horizon']} periods |
| Frequency | {summary['freq']} |
| Batch Size | {summary['batch_size']} |
| Total Batches | {summary['num_batches']} |

## Forecast Statistics

| Statistic | Value |
|-----------|-------|
| Total Forecast Points | {len(forecasts):,} |
| Date Range | {forecasts['ds'].min().date()} to {forecasts['ds'].max().date()} |
| Mean Forecast | {forecasts['TimeGPT'].mean():.4f} |
| Min Forecast | {forecasts['TimeGPT'].min():.4f} |
| Max Forecast | {forecasts['TimeGPT'].max():.4f} |

## Series Summary

| Series | Forecast Mean | Forecast Std |
|--------|---------------|--------------|
"""

    # Add per-series stats
    series_stats = forecasts.groupby("unique_id")["TimeGPT"].agg(["mean", "std"])
    for uid, row in series_stats.head(20).iterrows():
        uid_display = uid[:30] + "..." if len(uid) > 30 else uid
        report += f"| {uid_display} | {row['mean']:.4f} | {row['std']:.4f} |\n"

    if len(series_stats) > 20:
        report += f"\n*...and {len(series_stats) - 20} more series*\n"

    # Errors section
    if summary['errors']:
        report += f"""
## Errors ({summary['error_count']})

| Series | Error |
|--------|-------|
"""
        for error in summary['errors'][:10]:
            report += f"| {error['unique_id']} | {error['error'][:50]}... |\n"

    # Aggregation section
    if summary.get('aggregated'):
        agg_path = Path(output_dir) / "aggregated_forecast.csv"
        agg_df = pd.read_csv(agg_path)
        report += f"""
## Aggregated Forecast

Total forecasted value across all series:
- Sum at horizon end: {agg_df['TimeGPT'].iloc[-1]:.4f}
- Average across horizon: {agg_df['TimeGPT'].mean():.4f}

"""

    report += """
## Output Files

- `all_forecasts.csv` - Combined forecasts for all series
- `forecasts/{series}_forecast.csv` - Individual series forecasts
- `summary.json` - Processing metadata
"""

    if summary.get('aggregated'):
        report += "- `aggregated_forecast.csv` - Portfolio-level aggregated forecast\n"

    # Save report
    report_path = Path(output_dir) / "batch_report.md"
    with open(report_path, "w") as f:
        f.write(report)

    print(f"Report saved to {report_path}")
    return report

if __name__ == "__main__":
    import sys

    output_dir = sys.argv[1] if len(sys.argv) > 1 else "forecasts"
    generate_batch_report(output_dir)
```

## Output

- **forecasts/{unique_id}_forecast.csv**: Individual forecast per series
- **forecasts/all_forecasts.csv**: Combined forecasts
- **forecasts/aggregated_forecast.csv**: Portfolio aggregation (if enabled)
- **forecasts/summary.json**: Processing metadata
- **forecasts/batch_report.md**: Human-readable report

## Error Handling

1. **Error**: `NIXTLA_TIMEGPT_API_KEY not set`
   **Solution**: `export NIXTLA_TIMEGPT_API_KEY=your_key`

2. **Error**: `API Rate Limit Exceeded`
   **Solution**: Increase `--delay` parameter or reduce `--batch-size`

3. **Error**: `Input file not found`
   **Solution**: Verify file path with `ls -la`

4. **Error**: `Missing required columns`
   **Solution**: Ensure CSV has unique_id, ds, y columns

## Examples

### Example 1: Forecast 50 Daily Contracts

```bash
python batch_forecast.py contracts.csv \
    --horizon 14 \
    --freq D \
    --batch-size 10 \
    --output-dir forecasts/

# Output:
# Batch Forecast Complete
# Series forecasted: 50/50
# Success rate: 100.0%
```

### Example 2: Hourly Portfolio with Aggregation

```bash
python batch_forecast.py energy_demand.csv \
    --horizon 24 \
    --freq H \
    --batch-size 25 \
    --aggregate \
    --output-dir energy_forecasts/

# Output:
# Aggregated: energy_forecasts/aggregated_forecast.csv
```

## Usage

```bash
# Set API key
export NIXTLA_TIMEGPT_API_KEY='your-key'

# Basic batch forecast
python batch_forecast.py data.csv --horizon 14

# With aggregation and custom batch size
python batch_forecast.py portfolio.csv \
    --horizon 30 \
    --freq D \
    --batch-size 25 \
    --aggregate \
    --output-dir results/

# Generate report
python generate_report.py results/
```
