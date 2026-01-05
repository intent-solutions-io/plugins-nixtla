#!/usr/bin/env python3
"""
Generate comprehensive benchmark reports from forecast accuracy metrics.

This script transforms raw forecast metrics into actionable insights with:
- Model comparison tables
- Statistical analysis
- Regression detection
- GitHub issue templates

Usage:
    python generate_benchmark_report.py --results metrics.csv
    python generate_benchmark_report.py --results current.csv --baseline old.csv
    python generate_benchmark_report.py --results metrics.csv --format executive
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import numpy as np
    import pandas as pd
except ImportError:
    print("Error: pandas and numpy required. Install with: pip install pandas numpy")
    sys.exit(1)


class BenchmarkAnalyzer:
    """Analyze forecast benchmark results and generate reports."""

    def __init__(self, results_path: Path, baseline_path: Optional[Path] = None):
        self.results_path = results_path
        self.baseline_path = baseline_path
        self.results_df = None
        self.baseline_df = None
        self.summary_stats = {}
        self.regressions = []

    def load_results(self) -> bool:
        """Load benchmark results CSV file."""
        try:
            self.results_df = pd.read_csv(self.results_path)

            # Validate required columns
            required_cols = ["series_id", "model"]
            metric_cols = ["sMAPE", "MASE", "MAE", "RMSE"]

            missing_required = [col for col in required_cols if col not in self.results_df.columns]
            if missing_required:
                print(f"Error: Required columns missing: {missing_required}")
                return False

            # Check for at least one metric column
            available_metrics = [col for col in metric_cols if col in self.results_df.columns]
            if not available_metrics:
                print(f"Error: No metric columns found. Expected one of: {metric_cols}")
                return False

            return True
        except FileNotFoundError:
            print(f"Error: Results file not found: {self.results_path}")
            return False
        except Exception as e:
            print(f"Error loading results: {e}")
            return False

    def load_baseline(self) -> bool:
        """Load baseline results for regression detection."""
        if not self.baseline_path:
            return True

        try:
            self.baseline_df = pd.read_csv(self.baseline_path)
            return True
        except FileNotFoundError:
            print(f"Error: Baseline file not found: {self.baseline_path}")
            return False
        except Exception as e:
            print(f"Error loading baseline: {e}")
            return False

    def calculate_summary_stats(self, metric: str = "sMAPE") -> Dict:
        """Calculate summary statistics for each model."""
        if metric not in self.results_df.columns:
            available = [
                col for col in ["sMAPE", "MASE", "MAE", "RMSE"] if col in self.results_df.columns
            ]
            if available:
                metric = available[0]
            else:
                return {}

        stats = {}
        models = self.results_df["model"].unique()

        for model in models:
            model_data = self.results_df[self.results_df["model"] == model][metric]

            # Calculate win rate (how many series did this model win on)
            series_ids = self.results_df["series_id"].unique()
            wins = 0
            for series_id in series_ids:
                series_data = self.results_df[self.results_df["series_id"] == series_id]
                if len(series_data) > 0:
                    best_model = series_data.loc[series_data[metric].idxmin(), "model"]
                    if best_model == model:
                        wins += 1

            stats[model] = {
                "mean": model_data.mean(),
                "median": model_data.median(),
                "std": model_data.std(),
                "min": model_data.min(),
                "max": model_data.max(),
                "p25": model_data.quantile(0.25),
                "p75": model_data.quantile(0.75),
                "p95": model_data.quantile(0.95),
                "wins": wins,
                "total_series": len(series_ids),
                "win_rate": wins / len(series_ids) if len(series_ids) > 0 else 0,
            }

        self.summary_stats[metric] = stats
        return stats

    def detect_regressions(self, threshold: float = 5.0, metric: str = "sMAPE") -> List[Dict]:
        """Detect performance regressions vs. baseline."""
        if not self.baseline_df or metric not in self.results_df.columns:
            return []

        regressions = []
        models = self.results_df["model"].unique()

        for model in models:
            # Calculate current mean
            current_mean = self.results_df[self.results_df["model"] == model][metric].mean()

            # Calculate baseline mean
            if model in self.baseline_df["model"].values:
                baseline_mean = self.baseline_df[self.baseline_df["model"] == model][metric].mean()

                # Calculate % change
                pct_change = ((current_mean - baseline_mean) / baseline_mean) * 100

                # Check if regression exceeds threshold
                if pct_change > threshold:
                    regressions.append(
                        {
                            "model": model,
                            "metric": metric,
                            "baseline": baseline_mean,
                            "current": current_mean,
                            "pct_change": pct_change,
                        }
                    )

        self.regressions = regressions
        return regressions

    def identify_winner(self, metric: str = "sMAPE") -> Tuple[str, Dict]:
        """Identify overall best model based on metrics."""
        if metric not in self.summary_stats:
            self.calculate_summary_stats(metric)

        stats = self.summary_stats[metric]
        if not stats:
            return None, {}

        # Score models by: mean (60%), std dev (20%), win rate (20%)
        scores = {}
        for model, model_stats in stats.items():
            mean_score = 100 - model_stats["mean"]  # Lower is better
            std_score = 100 - model_stats["std"]  # Lower is better
            win_score = model_stats["win_rate"] * 100

            scores[model] = (0.6 * mean_score) + (0.2 * std_score) + (0.2 * win_score)

        winner = max(scores, key=scores.get)
        return winner, stats[winner]


class ReportGenerator:
    """Generate markdown benchmark reports."""

    def __init__(self, analyzer: BenchmarkAnalyzer):
        self.analyzer = analyzer

    def generate_standard_report(self, metric: str = "sMAPE") -> str:
        """Generate standard benchmark report."""
        lines = []

        # Header
        lines.append(f"# Forecast Benchmark Report")
        lines.append(f"")
        lines.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**Metric**: {metric}")
        lines.append(f"**Results File**: {self.analyzer.results_path.name}")
        lines.append(f"")
        lines.append("---")
        lines.append("")

        # Executive Summary
        winner, winner_stats = self.analyzer.identify_winner(metric)
        if winner:
            lines.append(f"## Executive Summary")
            lines.append(f"")
            lines.append(f"**Winner**: {winner}")
            lines.append(f"- Mean {metric}: {winner_stats['mean']:.2f}%")
            lines.append(
                f"- Win Rate: {winner_stats['wins']}/{winner_stats['total_series']} ({winner_stats['win_rate']*100:.1f}%)"
            )
            lines.append(f"- Consistency: σ = {winner_stats['std']:.2f}%")
            lines.append(f"")

        # Model Comparison Table
        stats = self.analyzer.summary_stats[metric]
        if stats:
            lines.append(f"## Model Comparison ({metric})")
            lines.append(f"")
            lines.append(f"| Model | Mean | Median | Std Dev | Min | Max | Wins | Win Rate |")
            lines.append(f"|-------|------|--------|---------|-----|-----|------|----------|")

            # Sort by mean (ascending for error metrics)
            sorted_models = sorted(stats.items(), key=lambda x: x[1]["mean"])

            for model, model_stats in sorted_models:
                lines.append(
                    f"| {model} | "
                    f"{model_stats['mean']:.2f}% | "
                    f"{model_stats['median']:.2f}% | "
                    f"{model_stats['std']:.2f}% | "
                    f"{model_stats['min']:.2f}% | "
                    f"{model_stats['max']:.2f}% | "
                    f"{model_stats['wins']}/{model_stats['total_series']} | "
                    f"{model_stats['win_rate']*100:.1f}% |"
                )
            lines.append("")

        # Regression Detection (if baseline provided)
        if self.analyzer.regressions:
            lines.append(f"## 🚨 Regressions Detected")
            lines.append(f"")
            for regression in self.analyzer.regressions:
                lines.append(f"**{regression['model']}**:")
                lines.append(f"- Baseline: {regression['baseline']:.2f}%")
                lines.append(f"- Current: {regression['current']:.2f}%")
                lines.append(f"- Change: +{regression['pct_change']:.1f}%")
                lines.append(f"")

        # Recommendations
        if winner:
            lines.append(f"## Recommendations")
            lines.append(f"")
            lines.append(f"1. **Production Baseline**: Use {winner} as default forecasting model")
            lines.append(
                f"2. **Consistency**: {winner} has low variance (σ = {winner_stats['std']:.2f}%)"
            )
            lines.append(
                f"3. **Win Rate**: {winner} performed best on {winner_stats['win_rate']*100:.1f}% of series"
            )
            lines.append(f"")

        # Footer
        lines.append("---")
        lines.append("")
        lines.append("*Generated by nixtla-benchmark-reporter*")
        lines.append("")

        return "\n".join(lines)

    def generate_executive_summary(self, metric: str = "sMAPE") -> str:
        """Generate 1-page executive summary."""
        lines = []

        lines.append(f"# Forecast Benchmark - Executive Summary")
        lines.append(f"")
        lines.append(f"**Date**: {datetime.now().strftime('%Y-%m-%d')}")
        lines.append(f"")

        winner, winner_stats = self.analyzer.identify_winner(metric)
        if winner:
            lines.append(f"## Winner: {winner}")
            lines.append(f"")
            lines.append(f"**Mean {metric}**: {winner_stats['mean']:.2f}%")
            lines.append(
                f"**Win Rate**: {winner_stats['wins']}/{winner_stats['total_series']} series ({winner_stats['win_rate']*100:.1f}%)"
            )
            lines.append(f"")

        # Quick comparison
        stats = self.analyzer.summary_stats[metric]
        if stats:
            sorted_models = sorted(stats.items(), key=lambda x: x[1]["mean"])
            lines.append(f"## Model Ranking")
            lines.append(f"")
            for i, (model, model_stats) in enumerate(sorted_models, 1):
                lines.append(f"{i}. **{model}**: {model_stats['mean']:.2f}% sMAPE")
            lines.append(f"")

        return "\n".join(lines)

    def generate_github_issue(self, threshold: float = 5.0, metric: str = "sMAPE") -> str:
        """Generate GitHub issue template for regressions."""
        regressions = self.analyzer.detect_regressions(threshold, metric)
        if not regressions:
            return ""

        lines = []
        lines.append("---")
        lines.append('title: "Performance Regression Detected"')
        lines.append('labels: ["regression", "performance"]')
        lines.append("---")
        lines.append("")
        lines.append("## Regression Summary")
        lines.append("")

        for regression in regressions:
            lines.append(f"**Model**: {regression['model']}")
            lines.append(f"**Metric**: {metric} degraded by {regression['pct_change']:.1f}%")
            lines.append(f"**Baseline**: {regression['baseline']:.2f}%")
            lines.append(f"**Current**: {regression['current']:.2f}%")
            lines.append("")

        lines.append("## Acceptance Criteria")
        lines.append("")
        lines.append("- [ ] Investigate root cause")
        lines.append("- [ ] Restore performance to within 2% of baseline")
        lines.append("- [ ] Add regression test to CI/CD")
        lines.append("")

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate benchmark reports from forecast accuracy metrics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Standard report
  python generate_benchmark_report.py --results metrics.csv

  # With regression detection
  python generate_benchmark_report.py --results current.csv --baseline old.csv --threshold 5.0

  # Executive summary
  python generate_benchmark_report.py --results metrics.csv --format executive
        """,
    )

    parser.add_argument(
        "--results", type=Path, required=True, help="Path to benchmark results CSV file"
    )

    parser.add_argument(
        "--baseline", type=Path, help="Path to baseline results CSV for regression detection"
    )

    parser.add_argument(
        "--output",
        type=Path,
        help="Output path for generated report (default: benchmark_report.md)",
    )

    parser.add_argument(
        "--format",
        choices=["standard", "executive", "github"],
        default="standard",
        help="Report format (default: standard)",
    )

    parser.add_argument(
        "--primary-metric", default="sMAPE", help="Primary metric for comparison (default: sMAPE)"
    )

    parser.add_argument(
        "--threshold",
        type=float,
        default=5.0,
        help="Regression threshold percentage (default: 5.0)",
    )

    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    # Default output path
    if not args.output:
        args.output = Path(f'benchmark_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md')

    # Initialize analyzer
    analyzer = BenchmarkAnalyzer(args.results, args.baseline)

    # Load results
    print(f"Loading results from {args.results}...")
    if not analyzer.load_results():
        return 1

    if args.baseline:
        print(f"Loading baseline from {args.baseline}...")
        if not analyzer.load_baseline():
            return 1

    # Calculate statistics
    print(f"Calculating summary statistics for {args.primary_metric}...")
    stats = analyzer.calculate_summary_stats(args.primary_metric)

    if args.verbose:
        print(f"\nFound {len(stats)} models:")
        for model in stats.keys():
            print(f"  - {model}")

    # Detect regressions
    if args.baseline:
        print(f"Detecting regressions (threshold: {args.threshold}%)...")
        regressions = analyzer.detect_regressions(args.threshold, args.primary_metric)
        if regressions:
            print(f"⚠️  REGRESSION DETECTED in {len(regressions)} model(s):")
            for reg in regressions:
                print(
                    f"  - {reg['model']}: {reg['baseline']:.2f}% → {reg['current']:.2f}% (+{reg['pct_change']:.1f}%)"
                )

    # Generate report
    print(f"\nGenerating {args.format} report...")
    generator = ReportGenerator(analyzer)

    if args.format == "standard":
        report_content = generator.generate_standard_report(args.primary_metric)
    elif args.format == "executive":
        report_content = generator.generate_executive_summary(args.primary_metric)
    elif args.format == "github":
        report_content = generator.generate_github_issue(args.threshold, args.primary_metric)

    # Write report
    args.output.write_text(report_content)
    print(f"✓ Report generated: {args.output} ({len(report_content.split())} words)")

    # Identify winner
    winner, winner_stats = analyzer.identify_winner(args.primary_metric)
    if winner:
        print(f"\n🏆 Winner: {winner} (mean {args.primary_metric}: {winner_stats['mean']:.2f}%)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
