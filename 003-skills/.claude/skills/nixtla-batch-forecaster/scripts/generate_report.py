#!/usr/bin/env python3
"""
Batch Forecaster - Report Generator
Creates summary reports from batch forecasting results.

Usage:
    python generate_report.py [output_dir]

Author: Nixtla Skills Pack
Version: 1.0.0
"""

import json
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd


def generate_batch_report(output_dir: str = "forecasts") -> str:
    """Generate markdown report from batch forecast results."""

    summary_path = Path(output_dir) / "summary.json"
    if not summary_path.exists():
        raise FileNotFoundError(f"No summary.json in {output_dir}")

    with open(summary_path) as f:
        summary = json.load(f)

    combined_path = Path(output_dir) / "all_forecasts.csv"
    forecasts = pd.read_csv(combined_path, parse_dates=["ds"])

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

    series_stats = forecasts.groupby("unique_id")["TimeGPT"].agg(["mean", "std"])
    for uid, row in series_stats.head(20).iterrows():
        uid_display = uid[:30] + "..." if len(uid) > 30 else uid
        report += f"| {uid_display} | {row['mean']:.4f} | {row['std']:.4f} |\n"

    if len(series_stats) > 20:
        report += f"\n*...and {len(series_stats) - 20} more series*\n"

    if summary["errors"]:
        report += f"""
## Errors ({summary['error_count']})

| Series | Error |
|--------|-------|
"""
        for error in summary["errors"][:10]:
            error_msg = error["error"][:50] + "..." if len(error["error"]) > 50 else error["error"]
            report += f"| {error['unique_id']} | {error_msg} |\n"

    if summary.get("aggregated"):
        agg_path = Path(output_dir) / "aggregated_forecast.csv"
        if agg_path.exists():
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
- `{series}_forecast.csv` - Individual series forecasts
- `summary.json` - Processing metadata
"""

    if summary.get("aggregated"):
        report += "- `aggregated_forecast.csv` - Portfolio-level aggregated forecast\n"

    report_path = Path(output_dir) / "batch_report.md"
    with open(report_path, "w") as f:
        f.write(report)

    print(f"Report saved to {report_path}")
    return report


def main():
    """Main entry point."""
    output_dir = sys.argv[1] if len(sys.argv) > 1 else "forecasts"

    try:
        report = generate_batch_report(output_dir)
        print("\nReport generated successfully!")
        return 0
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
