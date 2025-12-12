#!/usr/bin/env python3
"""
TimeGPT Experiment Harness

Config-driven experiment runner for TimeGPT forecasting workflows.
Runs multiple experiments defined in experiments/timegpt_experiments.json,
computes metrics (MAE, SMAPE), and generates CSV + Markdown reports.

Design:
- Load experiments from JSON config
- For each enabled experiment:
  - Split data into train/test using eval_window
  - Make ONE TimeGPT API call for forecasts (or use baseline in dry-run)
  - Compute MAE and SMAPE metrics
  - Track runtime
- Generate reports/timegpt_experiments_results.csv (per-series metrics)
- Generate reports/timegpt_experiments_summary.md (human-readable summary)

Modes:
    --dry-run: Uses naive baseline forecasts (last value) instead of TimeGPT.
               Computes metrics against baseline. No API key required. Safe for CI/CD.
    (default): Makes real TimeGPT API calls. Requires NIXTLA_TIMEGPT_API_KEY.

Exit codes:
    0: All experiments completed successfully
    1: Environment/config/data error
    2: TimeGPT API error (real mode only)
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

# Robust path handling
SCRIPT_DIR = Path(__file__).resolve().parent
LAB_ROOT = SCRIPT_DIR.parent
EXPERIMENTS_DIR = LAB_ROOT / "experiments"
DATA_DIR = LAB_ROOT / "data"
REPORTS_DIR = LAB_ROOT / "reports"

# Ensure reports directory exists
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def validate_environment():
    """Validate environment before experiments (reuses smoke test pattern)"""
    api_key = os.getenv("NIXTLA_TIMEGPT_API_KEY")

    if not api_key:
        print("=" * 60)
        print("ERROR: Missing API Key")
        print("=" * 60)
        print()
        print("The NIXTLA_TIMEGPT_API_KEY environment variable is not set.")
        print()
        print("To fix this:")
        print("  1. Obtain your API key from https://dashboard.nixtla.io/")
        print("  2. Set the environment variable:")
        print("     export NIXTLA_TIMEGPT_API_KEY='your_key_here'")
        print()
        print("  Or create a .env file in the lab root:")
        print("     NIXTLA_TIMEGPT_API_KEY=your_key_here")
        print()
        print("See docs/timegpt-env-setup.md for detailed instructions.")
        print("=" * 60)
        return None

    # Mask API key when displaying (show only first 4 chars)
    masked_key = api_key[:4] + "..." if len(api_key) > 4 else "***"
    print(f"✓ API key present ({masked_key})")

    return api_key


def load_experiments_config():
    """Load and validate experiments configuration"""
    config_path = EXPERIMENTS_DIR / "timegpt_experiments.json"

    if not config_path.exists():
        print("=" * 60)
        print("ERROR: Config Not Found")
        print("=" * 60)
        print()
        print(f"Expected config at: {config_path}")
        print()
        print("The experiment harness requires a configuration file.")
        print("Please ensure experiments/timegpt_experiments.json exists.")
        print("=" * 60)
        return None

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print("=" * 60)
        print("ERROR: Invalid JSON Config")
        print("=" * 60)
        print()
        print(f"Failed to parse {config_path}")
        print(f"Error: {e}")
        print("=" * 60)
        return None

    # Validate config structure
    if "experiments" not in config:
        print("=" * 60)
        print("ERROR: Invalid Config Structure")
        print("=" * 60)
        print()
        print("Config must have an 'experiments' array.")
        print("See experiments/timegpt_experiments.json for the expected format.")
        print("=" * 60)
        return None

    experiments = config["experiments"]
    if not isinstance(experiments, list):
        print("=" * 60)
        print("ERROR: Invalid Experiments Format")
        print("=" * 60)
        print()
        print("'experiments' must be a list/array.")
        print("=" * 60)
        return None

    # Validate each experiment
    required_fields = ["name", "horizon", "eval_window", "enabled"]
    for i, exp in enumerate(experiments):
        if not isinstance(exp, dict):
            print(f"ERROR: Experiment {i} is not a dict/object")
            return None

        missing = [f for f in required_fields if f not in exp]
        if missing:
            print(f"ERROR: Experiment '{exp.get('name', i)}' missing fields: {missing}")
            return None

    print(f"✓ Config loaded: {len(experiments)} experiments defined")
    return experiments


def load_dataset():
    """Load the smoke test sample dataset"""
    dataset_path = DATA_DIR / "timegpt_smoke_sample.csv"

    if not dataset_path.exists():
        print("=" * 60)
        print("ERROR: Dataset Not Found")
        print("=" * 60)
        print()
        print(f"Expected dataset at: {dataset_path}")
        print()
        print("The experiment harness requires the sample dataset.")
        print("Please ensure data/timegpt_smoke_sample.csv exists.")
        print("=" * 60)
        return None

    try:
        import pandas as pd
    except ImportError:
        print("=" * 60)
        print("ERROR: Missing pandas Package")
        print("=" * 60)
        print()
        print("The pandas package is required but not installed.")
        print()
        print("To fix this:")
        print("  pip install pandas")
        print()
        print("See docs/timegpt-env-setup.md for full setup instructions.")
        print("=" * 60)
        return None

    try:
        df = pd.read_csv(dataset_path)
    except Exception as e:
        print("=" * 60)
        print("ERROR: Failed to Load Dataset")
        print("=" * 60)
        print()
        print(f"Could not read {dataset_path}")
        print(f"Error: {e}")
        print("=" * 60)
        return None

    # Validate required columns
    required_cols = {"unique_id", "ds", "y"}
    if not required_cols.issubset(df.columns):
        missing = required_cols - set(df.columns)
        print("=" * 60)
        print("ERROR: Invalid Dataset Schema")
        print("=" * 60)
        print()
        print(f"Dataset is missing required columns: {missing}")
        print(f"Found columns: {list(df.columns)}")
        print()
        print("Expected columns: unique_id, ds, y")
        print("=" * 60)
        return None

    # Ensure ds is datetime
    df["ds"] = pd.to_datetime(df["ds"])

    unique_series = df["unique_id"].nunique()
    total_rows = len(df)
    print(f"✓ Dataset loaded: {unique_series} series, {total_rows} rows")

    return df


def mae(y_true, y_pred):
    """
    Mean Absolute Error

    MAE = mean(|y_true - y_pred|)
    """
    import numpy as np

    return np.mean(np.abs(y_true - y_pred))


def smape(y_true, y_pred):
    """
    Symmetric Mean Absolute Percentage Error

    SMAPE = 100 * mean(|y_true - y_pred| / ((|y_true| + |y_pred|) / 2))

    Notes:
    - Returns percentage (0-200 scale)
    - Handles zero values more gracefully than MAPE
    - Symmetric: treats over/under-prediction equally
    """
    import numpy as np

    numerator = np.abs(y_true - y_pred)
    denominator = (np.abs(y_true) + np.abs(y_pred)) / 2

    # Avoid division by zero
    mask = denominator != 0
    smape_values = np.zeros_like(y_true, dtype=float)
    smape_values[mask] = numerator[mask] / denominator[mask]

    return 100 * np.mean(smape_values)


def generate_baseline_forecast(train_df, horizon):
    """
    Generate baseline forecast for dry-run mode (no API call)

    Strategy: Repeat the last observed value for the forecast horizon.
    This is a naive baseline used in dry-run mode to test workflows without API calls.

    Note: In dry-run mode, metrics are computed against this baseline, not TimeGPT.
          This validates the experiment workflow but not TimeGPT accuracy.
    """
    import numpy as np
    import pandas as pd

    # Get the last value in the training data
    last_value = train_df["y"].iloc[-1]
    last_date = pd.to_datetime(train_df["ds"].iloc[-1])

    # Determine frequency (assume daily for now, can extend)
    freq = "D"

    # Generate future dates
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=horizon, freq=freq)

    # Create forecast dataframe
    forecast_df = pd.DataFrame(
        {
            "ds": future_dates,
            "TimeGPT": [last_value] * horizon,  # Use TimeGPT column name for compatibility
        }
    )

    return forecast_df


def run_experiment(experiment, df, api_key, dry_run=False):
    """
    Run a single experiment: split data, forecast, compute metrics

    Args:
        experiment: Experiment config dict
        df: Full dataset
        api_key: TimeGPT API key (can be None in dry-run mode)
        dry_run: If True, use baseline forecast instead of TimeGPT API

    Returns: dict with results or None on error
    """
    import numpy as np
    import pandas as pd

    exp_name = experiment["name"]
    horizon = experiment["horizon"]
    eval_window = experiment["eval_window"]
    freq = experiment.get("frequency", "D")

    print(f"\n{'='*60}")
    print(f"Running Experiment: {exp_name}")
    print(f"{'='*60}")
    print(f"Horizon: {horizon} steps")
    print(f"Eval window: {eval_window} steps")
    print(f"Frequency: {freq}")
    if dry_run:
        print(f"Mode: DRY RUN (baseline forecast)")

    results = []
    start_time = time.time()

    # Process each series
    for series_id in df["unique_id"].unique():
        series_df = df[df["unique_id"] == series_id].copy()
        series_df = series_df.sort_values("ds").reset_index(drop=True)

        total_points = len(series_df)

        # Validate enough data
        if total_points <= eval_window:
            print(
                f"  WARNING: {series_id} has only {total_points} points, need >{eval_window}. Skipping."
            )
            continue

        # Split train/test
        train_df = series_df.iloc[:-eval_window].copy()
        test_df = series_df.iloc[-eval_window:].copy()

        print(f"  Series {series_id}: {len(train_df)} train, {len(test_df)} test")

        # Generate forecast (dry-run or real)
        if dry_run:
            # Use baseline forecast (no API call)
            forecast_df = generate_baseline_forecast(train_df, horizon)
            y_pred = forecast_df["TimeGPT"].values[:eval_window]

        else:
            # Forecast using TimeGPT (real mode)
            try:
                from nixtla import NixtlaClient
            except ImportError:
                print("=" * 60)
                print("ERROR: Missing nixtla Package")
                print("=" * 60)
                print()
                print("The nixtla package is required but not installed.")
                print()
                print("To fix this:")
                print("  pip install nixtla>=0.5.0")
                print()
                print("See docs/timegpt-env-setup.md for full setup instructions.")
                print("=" * 60)
                return None

            try:
                client = NixtlaClient(api_key=api_key)

                forecast_df = client.forecast(
                    df=train_df, h=horizon, freq=freq, time_col="ds", target_col="y"
                )

                # Extract forecast values
                # TimeGPT returns different column names depending on version
                if "TimeGPT" in forecast_df.columns:
                    y_pred = forecast_df["TimeGPT"].values[:eval_window]
                elif "y_hat" in forecast_df.columns:
                    y_pred = forecast_df["y_hat"].values[:eval_window]
                else:
                    print(f"  ERROR: Cannot find forecast column in {forecast_df.columns}")
                    return None

            except Exception as e:
                error_msg = str(e)
                print("=" * 60)
                print("ERROR: TimeGPT API Call Failed")
                print("=" * 60)
                print()
                print(f"Error: {error_msg}")
                print()

                # Provide context-specific guidance
                if "401" in error_msg or "authentication" in error_msg.lower():
                    print("This appears to be an authentication error.")
                    print("Please verify your API key is valid.")
                elif "network" in error_msg.lower() or "connection" in error_msg.lower():
                    print("This appears to be a network connectivity error.")
                    print("Please check your internet connection.")

                print("=" * 60)
                return None

        # Compute metrics (same for both modes)
        y_true = test_df["y"].values[:eval_window]
        mae_val = mae(y_true, y_pred)
        smape_val = smape(y_true, y_pred)

        print(f"    MAE: {mae_val:.4f}")
        print(f"    SMAPE: {smape_val:.2f}%")

        results.append(
            {
                "experiment_name": exp_name,
                "unique_id": series_id,
                "horizon": horizon,
                "eval_window": eval_window,
                "mae": mae_val,
                "smape": smape_val,
            }
        )

    runtime = time.time() - start_time

    # Add runtime to all results
    for r in results:
        r["runtime_seconds"] = runtime

    print(f"\n✓ Experiment completed in {runtime:.2f}s")

    return results


def write_csv_report(all_results):
    """Write detailed CSV report with per-series metrics"""
    import pandas as pd

    csv_path = REPORTS_DIR / "timegpt_experiments_results.csv"

    if not all_results:
        print(f"  No results to write to CSV")
        return False

    df = pd.DataFrame(all_results)
    df.to_csv(csv_path, index=False)

    print(f"✓ CSV report: {csv_path.relative_to(LAB_ROOT)}")
    return True


def write_markdown_summary(all_results, experiments_config, dry_run=False):
    """Write human-readable Markdown summary"""
    from datetime import datetime

    import pandas as pd

    md_path = REPORTS_DIR / "timegpt_experiments_summary.md"

    if not all_results:
        print(f"  No results to write to Markdown")
        return False

    df = pd.DataFrame(all_results)

    # Build markdown content
    lines = []
    mode = "DRY RUN" if dry_run else "REAL"
    lines.append(f"# TimeGPT Experiments Summary - {mode} MODE")
    lines.append("")
    lines.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Mode**: {mode}")
    if dry_run:
        lines.append(
            f"**Note**: Metrics are against naive baseline (last-value), not TimeGPT. Validates workflow, not accuracy."
        )
    lines.append(f"**Config**: experiments/timegpt_experiments.json")
    lines.append("")

    # Config summary
    enabled_exps = [e for e in experiments_config if e.get("enabled", False)]
    disabled_exps = [e for e in experiments_config if not e.get("enabled", False)]

    lines.append("## Configuration")
    lines.append("")
    lines.append(f"- **Total experiments defined**: {len(experiments_config)}")
    lines.append(f"- **Enabled experiments**: {len(enabled_exps)}")
    lines.append(f"- **Disabled experiments**: {len(disabled_exps)}")
    lines.append("")

    # Per-experiment summary
    lines.append("## Results by Experiment")
    lines.append("")

    for exp in enabled_exps:
        exp_name = exp["name"]
        exp_results = df[df["experiment_name"] == exp_name]

        if exp_results.empty:
            lines.append(f"### {exp_name}")
            lines.append("")
            lines.append("*No results (experiment may have failed)*")
            lines.append("")
            continue

        lines.append(f"### {exp_name}")
        lines.append("")
        lines.append(f"**Description**: {exp.get('description', 'N/A')}")
        lines.append(f"**Horizon**: {exp['horizon']} steps")
        lines.append(f"**Eval Window**: {exp['eval_window']} steps")
        lines.append(f"**Runtime**: {exp_results['runtime_seconds'].iloc[0]:.2f}s")
        lines.append("")

        # Per-series metrics table
        lines.append("| Series | MAE | SMAPE |")
        lines.append("|--------|-----|-------|")
        for _, row in exp_results.iterrows():
            lines.append(f"| {row['unique_id']} | {row['mae']:.4f} | {row['smape']:.2f}% |")
        lines.append("")

        # Aggregate metrics
        avg_mae = exp_results["mae"].mean()
        avg_smape = exp_results["smape"].mean()

        lines.append(f"**Aggregate Metrics**:")
        lines.append(f"- Average MAE: {avg_mae:.4f}")
        lines.append(f"- Average SMAPE: {avg_smape:.2f}%")
        lines.append("")

    # Comparative analysis
    if len(enabled_exps) > 1:
        lines.append("## Comparative Analysis")
        lines.append("")

        # Group by experiment and compute averages
        exp_summary = (
            df.groupby("experiment_name")
            .agg({"mae": "mean", "smape": "mean", "runtime_seconds": "first"})
            .reset_index()
        )

        lines.append("| Experiment | Avg MAE | Avg SMAPE | Runtime |")
        lines.append("|------------|---------|-----------|---------|")
        for _, row in exp_summary.iterrows():
            lines.append(
                f"| {row['experiment_name']} | {row['mae']:.4f} | {row['smape']:.2f}% | {row['runtime_seconds']:.2f}s |"
            )
        lines.append("")

        # Brief insights
        best_mae_exp = exp_summary.loc[exp_summary["mae"].idxmin(), "experiment_name"]
        best_smape_exp = exp_summary.loc[exp_summary["smape"].idxmin(), "experiment_name"]

        lines.append("**Insights**:")
        lines.append(f"- Lowest MAE: `{best_mae_exp}`")
        lines.append(f"- Lowest SMAPE: `{best_smape_exp}`")

        # Note on longer horizons
        if len(enabled_exps) >= 2:
            horizons = sorted([e["horizon"] for e in enabled_exps])
            lines.append(f"- Horizon range: {horizons[0]}-{horizons[-1]} days")
            lines.append("- Longer horizons typically have higher error (expected behavior)")

        lines.append("")

    # Footer
    lines.append("---")
    lines.append("")
    lines.append("**Lab**: 002-workspaces/timegpt-lab/")
    lines.append("**Phase**: 05 - TimeGPT Experiment Workflows")

    # Write markdown
    md_content = "\n".join(lines)
    with open(md_path, "w") as f:
        f.write(md_content)

    print(f"✓ Markdown summary: {md_path.relative_to(LAB_ROOT)}")
    return True


def main():
    """Main experiment harness workflow"""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="TimeGPT experiment harness with optional dry-run mode"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Run in dry-run mode (baseline forecasts, no API calls)",
    )
    args = parser.parse_args()

    # Display mode clearly
    mode = "DRY RUN" if args.dry_run else "REAL"
    print("=" * 60)
    print(f"TimeGPT Experiment Harness - {mode} MODE")
    print("=" * 60)
    print()

    if args.dry_run:
        print("⚠️  DRY-RUN MODE: No API calls will be made.")
        print("    Using naive baseline forecasts for workflow validation.")
        print()

    # Step 1: Validate environment (skip API key check in dry-run mode)
    if args.dry_run:
        print("Step 1: Validating environment (dry-run mode)...")
        print("✓ Skipping API key validation (dry-run mode)")
        api_key = None
    else:
        print("Step 1: Validating environment...")
        api_key = validate_environment()
        if api_key is None:
            return 1
    print()

    # Step 2: Load config
    print("Step 2: Loading experiment configuration...")
    experiments = load_experiments_config()
    if experiments is None:
        return 1
    print()

    # Filter enabled experiments
    enabled_experiments = [e for e in experiments if e.get("enabled", False)]
    disabled_experiments = [e for e in experiments if not e.get("enabled", False)]

    print(f"Enabled experiments: {len(enabled_experiments)}")
    print(f"Disabled experiments: {len(disabled_experiments)}")

    if not enabled_experiments:
        print()
        print("No enabled experiments to run.")
        print("Enable experiments in experiments/timegpt_experiments.json")
        return 0
    print()

    # Step 3: Load dataset
    print("Step 3: Loading dataset...")
    df = load_dataset()
    if df is None:
        return 1
    print()

    # Step 4: Run experiments
    print("Step 4: Running experiments...")
    all_results = []

    for exp in enabled_experiments:
        results = run_experiment(exp, df, api_key, dry_run=args.dry_run)
        if results is None:
            print()
            print(f"Experiment '{exp['name']}' failed. Stopping.")
            return 2

        all_results.extend(results)

    print()

    # Step 5: Generate reports
    print("Step 5: Generating reports...")
    csv_ok = write_csv_report(all_results)
    md_ok = write_markdown_summary(all_results, experiments, dry_run=args.dry_run)

    if not (csv_ok and md_ok):
        print()
        print("Failed to generate one or more reports.")
        return 1

    print()

    # Success summary
    print("=" * 60)
    print(f"✓ Experiment Harness ({mode}): COMPLETE")
    print("=" * 60)
    print()
    print("Summary:")
    print(f"  Mode: {mode}")
    print(f"  Experiments run: {len(enabled_experiments)}")
    print(f"  Series processed: {len(df['unique_id'].unique())}")
    print(f"  Total results: {len(all_results)}")
    if args.dry_run:
        print(f"  Forecast method: Last-value baseline (synthetic)")
    else:
        print(f"  Forecast method: TimeGPT API")
    print()
    print("Reports:")
    print(f"  - reports/timegpt_experiments_results.csv")
    print(f"  - reports/timegpt_experiments_summary.md")
    print()

    if not args.dry_run:
        print("Next steps:")
        print("  - Review metrics in reports/")
        print("  - Adjust experiment configs in experiments/")
        print("  - Enable/disable experiments as needed")
        print()

    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
