#!/usr/bin/env python3
"""
TimeGPT vs StatsForecast Comparison Aggregator

Aggregates results from TimeGPT lab and StatsForecast lab to produce
a CEO-friendly comparison report.

Design:
- Loads existing CSV results from both labs (no re-running experiments)
- Normalizes metrics (smape, mae) for comparison
- Generates combined CSV + executive Markdown report
- Handles missing StatsForecast baseline gracefully (TimeGPT-only mode)

Exit codes:
    0: Success (full comparison or TimeGPT-only report with warning)
    1: TimeGPT results missing (hard error)
    2: Parse/processing error
"""

import sys
from pathlib import Path

# Robust path handling - detect repo root
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent

# Input paths
TIMEGPT_RESULTS_CSV = (
    REPO_ROOT / "002-workspaces/timegpt-lab/reports/timegpt_experiments_results.csv"
)
STATSFORECAST_RESULTS_CSV = (
    REPO_ROOT / "002-workspaces/statsforecast-lab/reports/statsforecast_baseline_results.csv"
)

# Output paths
OUTPUT_DIR = SCRIPT_DIR / "compare_outputs"
OUTPUT_CSV = OUTPUT_DIR / "timegpt_vs_statsforecast_metrics.csv"
OUTPUT_REPORT_MD = REPO_ROOT / "000-docs/091-RA-REPT-timegpt-vs-statsforecast-baseline.md"


def check_timegpt_results():
    """
    Check if TimeGPT results exist (REQUIRED)

    Returns: True if exists, False otherwise
    """
    if not TIMEGPT_RESULTS_CSV.exists():
        print("=" * 70)
        print("ERROR: TimeGPT Experiments Results Not Found")
        print("=" * 70)
        print()
        print(f"Expected file: {TIMEGPT_RESULTS_CSV}")
        print()
        print("The comparison aggregator requires TimeGPT experiment results.")
        print()
        print("To generate TimeGPT results:")
        print("  1. cd 002-workspaces/timegpt-lab")
        print("  2. Set NIXTLA_TIMEGPT_API_KEY environment variable")
        print("  3. python scripts/run_experiment.py")
        print()
        print("See 002-workspaces/timegpt-lab/README.md for detailed instructions.")
        print("=" * 70)
        return False

    return True


def check_statsforecast_results():
    """
    Check if StatsForecast baseline results exist (OPTIONAL)

    Returns: True if exists, False otherwise
    """
    if not STATSFORECAST_RESULTS_CSV.exists():
        print("=" * 70)
        print("WARNING: StatsForecast Baseline Results Not Found")
        print("=" * 70)
        print()
        print(f"Expected file: {STATSFORECAST_RESULTS_CSV}")
        print()
        print("StatsForecast baseline results are not yet available.")
        print("Proceeding with TimeGPT-only report.")
        print()
        print("To generate StatsForecast baselines:")
        print("  1. cd 002-workspaces/statsforecast-lab")
        print("  2. python scripts/run_statsforecast_baseline.py")
        print()
        print("Once baseline results exist, re-run this script for full comparison.")
        print("=" * 70)
        print()
        return False

    return True


def load_timegpt_results():
    """Load and normalize TimeGPT experiment results"""
    try:
        import pandas as pd
    except ImportError:
        print("ERROR: pandas package required but not installed.")
        print("Install with: pip install pandas")
        return None

    try:
        df = pd.read_csv(TIMEGPT_RESULTS_CSV)
    except Exception as e:
        print(f"ERROR: Failed to load TimeGPT results: {e}")
        return None

    # Normalize columns
    # Expected: experiment_name, unique_id, horizon, eval_window, mae, smape, runtime_seconds
    df = df.rename(columns={"experiment_name": "model", "unique_id": "series_id"})

    # Add source column
    df["source"] = "timegpt"

    # Select relevant columns for comparison
    df = df[["source", "model", "series_id", "horizon", "mae", "smape"]]

    print(f"✓ Loaded TimeGPT results: {len(df)} rows")
    return df


def load_statsforecast_results():
    """Load and normalize StatsForecast baseline results"""
    try:
        import pandas as pd
    except ImportError:
        print("ERROR: pandas package required but not installed.")
        return None

    try:
        df = pd.read_csv(STATSFORECAST_RESULTS_CSV)
    except Exception as e:
        print(f"ERROR: Failed to load StatsForecast results: {e}")
        return None

    # Normalize columns
    # Expected: unique_id, model, horizon, smape, mae
    df = df.rename(columns={"unique_id": "series_id"})

    # Add source column
    df["source"] = "statsforecast"

    # Select relevant columns for comparison
    df = df[["source", "model", "series_id", "horizon", "mae", "smape"]]

    print(f"✓ Loaded StatsForecast results: {len(df)} rows")
    return df


def aggregate_metrics(df_timegpt, df_statsforecast=None):
    """
    Aggregate metrics across series for each model

    Returns: DataFrame with aggregated metrics
    """
    import pandas as pd

    # Combine dataframes
    if df_statsforecast is not None:
        df_combined = pd.concat([df_timegpt, df_statsforecast], ignore_index=True)
    else:
        df_combined = df_timegpt.copy()

    # Compute mean metrics per (source, model, horizon)
    agg_metrics = (
        df_combined.groupby(["source", "model", "horizon"])
        .agg({"mae": "mean", "smape": "mean"})
        .reset_index()
    )

    # Rename for clarity
    agg_metrics = agg_metrics.rename(columns={"mae": "mean_mae", "smape": "mean_smape"})

    return df_combined, agg_metrics


def write_csv_output(df_combined, agg_metrics):
    """Write combined metrics CSV"""
    import pandas as pd

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    try:
        # Write combined raw metrics
        df_combined.to_csv(OUTPUT_CSV, index=False)
        print(f"✓ CSV output: {OUTPUT_CSV.relative_to(REPO_ROOT)}")
        return True
    except Exception as e:
        print(f"ERROR: Failed to write CSV: {e}")
        return False


def write_markdown_report(df_combined, agg_metrics, has_statsforecast):
    """Write executive Markdown comparison report"""
    from datetime import datetime

    import pandas as pd

    lines = []

    # Header
    lines.append("# TimeGPT vs StatsForecast Baseline Comparison")
    lines.append("")
    lines.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S CST')}")
    lines.append(f"**Aggregator**: `004-scripts/compare_timegpt_vs_statsforecast.py`")
    lines.append("")

    # Executive Summary
    lines.append("## Executive Summary")
    lines.append("")

    if has_statsforecast:
        # Full comparison
        timegpt_count = len(df_combined[df_combined["source"] == "timegpt"]["model"].unique())
        statsforecast_count = len(
            df_combined[df_combined["source"] == "statsforecast"]["model"].unique()
        )

        lines.append(
            f"Comparison of TimeGPT forecasts ({timegpt_count} experiments) against classical StatsForecast baselines ({statsforecast_count} models) on identical M4-style daily time series. Metrics: sMAPE (Symmetric Mean Absolute Percentage Error) and MAE (Mean Absolute Error). Lower values indicate better forecast accuracy."
        )
    else:
        # TimeGPT-only mode
        timegpt_count = len(df_combined["model"].unique())

        lines.append(
            f"**Current Status**: TimeGPT-only report ({timegpt_count} experiments). StatsForecast baseline results are not yet available. This report will be updated with a full comparison once baseline metrics are generated."
        )

    lines.append("")

    # StatsForecast Status (if missing)
    if not has_statsforecast:
        lines.append("## StatsForecast Baseline Status")
        lines.append("")
        lines.append("**Status**: PENDING")
        lines.append("")
        lines.append(f"No StatsForecast baseline CSV found at:")
        lines.append(f"```")
        lines.append(f"{STATSFORECAST_RESULTS_CSV.relative_to(REPO_ROOT)}")
        lines.append(f"```")
        lines.append("")
        lines.append("**To generate baseline metrics**:")
        lines.append("```bash")
        lines.append("cd 002-workspaces/statsforecast-lab")
        lines.append("python scripts/run_statsforecast_baseline.py")
        lines.append("```")
        lines.append("")
        lines.append("Once baseline results exist, re-run:")
        lines.append("```bash")
        lines.append("python 004-scripts/compare_timegpt_vs_statsforecast.py")
        lines.append("```")
        lines.append("")

    # TimeGPT Results
    lines.append("## TimeGPT Results")
    lines.append("")

    timegpt_metrics = agg_metrics[agg_metrics["source"] == "timegpt"]

    if not timegpt_metrics.empty:
        lines.append("| Model | Horizon | Avg sMAPE | Avg MAE |")
        lines.append("|-------|---------|-----------|---------|")
        for _, row in timegpt_metrics.iterrows():
            lines.append(
                f"| {row['model']} | {row['horizon']}d | {row['mean_smape']:.2f}% | {row['mean_mae']:.4f} |"
            )
        lines.append("")
    else:
        lines.append("*No TimeGPT results available.*")
        lines.append("")

    # StatsForecast Results (if available)
    if has_statsforecast:
        lines.append("## StatsForecast Baseline Results")
        lines.append("")

        statsforecast_metrics = agg_metrics[agg_metrics["source"] == "statsforecast"]

        if not statsforecast_metrics.empty:
            lines.append("| Model | Horizon | Avg sMAPE | Avg MAE |")
            lines.append("|-------|---------|-----------|---------|")
            for _, row in statsforecast_metrics.iterrows():
                lines.append(
                    f"| {row['model']} | {row['horizon']}d | {row['mean_smape']:.2f}% | {row['mean_mae']:.4f} |"
                )
            lines.append("")
        else:
            lines.append("*No StatsForecast results available.*")
            lines.append("")

        # Comparative Analysis
        lines.append("## Comparative Analysis")
        lines.append("")

        # Find best models by metric
        best_smape = agg_metrics.loc[agg_metrics["mean_smape"].idxmin()]
        best_mae = agg_metrics.loc[agg_metrics["mean_mae"].idxmin()]

        lines.append("**Best Models by Metric**:")
        lines.append(
            f"- **Lowest sMAPE**: {best_smape['model']} ({best_smape['source']}) - {best_smape['mean_smape']:.2f}%"
        )
        lines.append(
            f"- **Lowest MAE**: {best_mae['model']} ({best_mae['source']}) - {best_mae['mean_mae']:.4f}"
        )
        lines.append("")

    # Dataset Info
    lines.append("## Dataset")
    lines.append("")
    series_count = df_combined["series_id"].nunique()
    lines.append(f"- **Series**: {series_count} time series")
    lines.append(f"- **Source**: M4-style daily data")
    lines.append(f"- **Evaluation**: Train/test split with holdout period")
    lines.append("")

    # How to Reproduce
    lines.append("## How to Reproduce")
    lines.append("")
    lines.append("### 1. Run TimeGPT Experiments")
    lines.append("```bash")
    lines.append("cd 002-workspaces/timegpt-lab")
    lines.append("export NIXTLA_TIMEGPT_API_KEY='your_key_here'")
    lines.append("python scripts/run_experiment.py")
    lines.append("```")
    lines.append("")
    lines.append("### 2. Run StatsForecast Baselines")
    lines.append("```bash")
    lines.append("cd 002-workspaces/statsforecast-lab")
    lines.append("python scripts/run_statsforecast_baseline.py")
    lines.append("```")
    lines.append("")
    lines.append("### 3. Generate Comparison")
    lines.append("```bash")
    lines.append("python 004-scripts/compare_timegpt_vs_statsforecast.py")
    lines.append("```")
    lines.append("")

    # Footer
    lines.append("---")
    lines.append("")
    lines.append("**Report Type**: Research Analysis (RA-REPT)")
    lines.append("**Phase**: 08 - Cross-Lab Benchmark")
    lines.append("**Owner**: intent solutions io")
    lines.append("**Contact**: jeremy@intentsolutions.io")

    # Write markdown
    md_content = "\n".join(lines)
    try:
        with open(OUTPUT_REPORT_MD, "w") as f:
            f.write(md_content)
        print(f"✓ Markdown report: {OUTPUT_REPORT_MD.relative_to(REPO_ROOT)}")
        return True
    except Exception as e:
        print(f"ERROR: Failed to write Markdown report: {e}")
        return False


def main():
    """Main aggregator workflow"""
    print("=" * 70)
    print("TimeGPT vs StatsForecast Comparison Aggregator")
    print("=" * 70)
    print()

    # Step 1: Check TimeGPT results (REQUIRED)
    print("Step 1: Checking TimeGPT results...")
    if not check_timegpt_results():
        return 1
    print()

    # Step 2: Check StatsForecast results (OPTIONAL)
    print("Step 2: Checking StatsForecast baseline results...")
    has_statsforecast = check_statsforecast_results()
    print()

    # Step 3: Load TimeGPT results
    print("Step 3: Loading TimeGPT results...")
    df_timegpt = load_timegpt_results()
    if df_timegpt is None:
        return 2
    print()

    # Step 4: Load StatsForecast results (if available)
    df_statsforecast = None
    if has_statsforecast:
        print("Step 4: Loading StatsForecast baseline results...")
        df_statsforecast = load_statsforecast_results()
        if df_statsforecast is None:
            print("WARNING: Failed to load StatsForecast results despite file existing.")
            print("Proceeding with TimeGPT-only mode.")
            has_statsforecast = False
        print()
    else:
        print("Step 4: Skipping StatsForecast load (results not available)...")
        print()

    # Step 5: Aggregate metrics
    print("Step 5: Aggregating metrics...")
    df_combined, agg_metrics = aggregate_metrics(df_timegpt, df_statsforecast)
    print(f"✓ Aggregated {len(df_combined)} total result rows")
    print()

    # Step 6: Write outputs
    print("Step 6: Writing outputs...")
    csv_ok = write_csv_output(df_combined, agg_metrics)
    md_ok = write_markdown_report(df_combined, agg_metrics, has_statsforecast)

    if not (csv_ok and md_ok):
        print()
        print("Failed to generate one or more output files.")
        return 2
    print()

    # Success summary
    print("=" * 70)
    if has_statsforecast:
        print("✓ Comparison Complete: FULL (TimeGPT + StatsForecast)")
    else:
        print("✓ Comparison Complete: PARTIAL (TimeGPT only)")
    print("=" * 70)
    print()
    print("Outputs:")
    print(f"  - CSV: {OUTPUT_CSV.relative_to(REPO_ROOT)}")
    print(f"  - Report: {OUTPUT_REPORT_MD.relative_to(REPO_ROOT)}")
    print()

    if not has_statsforecast:
        print("Next steps:")
        print(
            "  1. Run StatsForecast baseline: cd 002-workspaces/statsforecast-lab && python scripts/run_statsforecast_baseline.py"
        )
        print("  2. Re-run this script for full comparison")
        print()

    print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
