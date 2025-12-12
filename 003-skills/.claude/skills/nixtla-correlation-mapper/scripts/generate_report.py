#!/usr/bin/env python3
"""
Correlation Mapper - Report Generator
Creates comprehensive correlation analysis report
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd


def generate_correlation_report(
    corr_matrix: pd.DataFrame,
    high_corr: list,
    recommendations: list,
    output_path: str = "correlation_report.md",
) -> str:
    """
    Generate markdown report of correlation analysis.

    Args:
        corr_matrix: Correlation matrix DataFrame
        high_corr: List of high correlation pairs
        recommendations: List of hedge recommendations
        output_path: Path to save the report

    Returns:
        Report content as string
    """
    n_contracts = len(corr_matrix)
    n_pairs = n_contracts * (n_contracts - 1) // 2

    # Calculate statistics (excluding diagonal)
    mask = ~np.eye(n_contracts, dtype=bool)
    corr_values = corr_matrix.values[mask]
    avg_corr = corr_values.mean()
    max_pos_corr = corr_values.max()
    max_neg_corr = corr_values.min()

    report = f"""# Portfolio Correlation Analysis Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary

| Metric | Value |
|--------|-------|
| Contracts Analyzed | {n_contracts} |
| Total Pairs | {n_pairs} |
| High Correlation Pairs (abs > 0.5) | {len(high_corr)} |
| Hedge Recommendations | {len(recommendations)} |

## Correlation Matrix

See `correlation_matrix.csv` and `correlation_heatmap.png` for full matrix.

### Key Statistics

| Statistic | Value |
|-----------|-------|
| Average Correlation | {avg_corr:.3f} |
| Max Positive Correlation | {max_pos_corr:.3f} |
| Max Negative Correlation | {max_neg_corr:.3f} |
| Standard Deviation | {corr_values.std():.3f} |

## High Correlation Pairs

"""

    if high_corr:
        report += """| Contract 1 | Contract 2 | Correlation | Relationship | Hedge Potential |
|------------|------------|-------------|--------------|-----------------|
"""
        for pair in high_corr[:10]:
            report += (
                f"| {pair['contract_1']} | {pair['contract_2']} | "
                f"{pair['correlation']:.3f} | {pair['relationship']} | "
                f"{pair['hedge_potential']} |\n"
            )

        if len(high_corr) > 10:
            report += f"\n*...and {len(high_corr) - 10} more pairs*\n"
    else:
        report += "*No high correlation pairs found with current threshold.*\n"

    report += """
## Hedge Recommendations

"""

    if recommendations:
        report += """| Target | Hedge Instrument | Ratio | Correlation | Var Reduction |
|--------|------------------|-------|-------------|---------------|
"""
        for rec in recommendations[:10]:
            report += (
                f"| {rec['target']} | {rec['hedge_instrument']} | "
                f"{rec['hedge_ratio']:.2f} | {rec['correlation']:.3f} | "
                f"{rec['variance_reduction_pct']:.1f}% |\n"
            )

        if len(recommendations) > 10:
            report += f"\n*...and {len(recommendations) - 10} more recommendations*\n"
    else:
        report += "*No hedge recommendations generated.*\n"

    report += """
## Interpretation Guide

### Correlation Values

- **+0.7 to +1.0**: Strong positive - assets move together
- **+0.3 to +0.7**: Moderate positive - some co-movement
- **-0.3 to +0.3**: Weak/No correlation - independent movement
- **-0.7 to -0.3**: Moderate negative - partial hedge potential
- **-1.0 to -0.7**: Strong negative - excellent hedge opportunity

### Hedge Ratio Interpretation

- **Negative ratio**: Take opposite direction position (typical hedge)
- **Positive ratio**: Take same direction position (unusual for hedging)
- **Ratio magnitude**: Units of hedge instrument per unit of target

**Example**: Ratio of -0.75 means "for every 1 unit LONG in target, take 0.75 units SHORT in hedge instrument"

### Variance Reduction

- **>50%**: Highly effective hedge
- **25-50%**: Moderately effective hedge
- **<25%**: Low effectiveness, consider alternatives

## Output Files

- `correlation_matrix.csv` - Full correlation matrix
- `correlation_pvalues.csv` - Statistical significance p-values
- `correlation_heatmap.png` - Visual heatmap
- `high_correlations.json` - Significant correlation pairs
- `hedge_recommendations.csv` - Detailed hedge recommendations
- `hedge_recommendations.json` - Recommendations in JSON format
- `hedged_portfolio.csv` - Sample portfolio allocation
- `rolling_correlations.csv` - Time-series correlation stability
- `rolling_correlation.png` - Rolling correlation plot
- `hedge_effectiveness.png` - Hedge effectiveness chart

## Risk Disclaimer

**Important**: Correlations are based on historical data and may not persist in the future. Past relationships do not guarantee future behavior. Market conditions, regime changes, and external events can alter correlations significantly.

**Recommendations**:
- Monitor correlations regularly and adjust hedges
- Use stop-losses and position limits
- Consider transaction costs and slippage
- Validate strategies with out-of-sample testing
- Consult with financial professionals before implementation

---

*Report generated by Nixtla Correlation Mapper*
"""

    # Save report
    with open(output_path, "w") as f:
        f.write(report)

    print(f"Report saved to {output_path}")
    return report


def main():
    """Main entry point for report generation."""
    parser = argparse.ArgumentParser(
        description="Generate comprehensive correlation analysis report"
    )
    parser.add_argument(
        "--correlation",
        type=str,
        default="correlation_matrix.csv",
        help="Input correlation matrix CSV (default: correlation_matrix.csv)",
    )
    parser.add_argument(
        "--high-correlations",
        type=str,
        default="high_correlations.json",
        help="Input high correlations JSON (default: high_correlations.json)",
    )
    parser.add_argument(
        "--recommendations",
        type=str,
        default="hedge_recommendations.json",
        help="Input recommendations JSON (default: hedge_recommendations.json)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="correlation_report.md",
        help="Output report filename (default: correlation_report.md)",
    )

    args = parser.parse_args()

    try:
        # Load correlation matrix
        corr_path = Path(args.correlation)
        if not corr_path.exists():
            raise FileNotFoundError(f"Correlation matrix not found: {corr_path}")

        corr_matrix = pd.read_csv(corr_path, index_col=0)
        print(f"Loaded correlation matrix: {len(corr_matrix)} contracts")

        # Load high correlations
        high_corr_path = Path(args.high_correlations)
        if high_corr_path.exists():
            with open(high_corr_path) as f:
                high_corr = json.load(f)
            print(f"Loaded {len(high_corr)} high correlation pairs")
        else:
            print(f"Warning: High correlations not found: {high_corr_path}")
            high_corr = []

        # Load recommendations
        rec_path = Path(args.recommendations)
        if rec_path.exists():
            with open(rec_path) as f:
                recommendations = json.load(f)
            print(f"Loaded {len(recommendations)} hedge recommendations")
        else:
            print(f"Warning: Recommendations not found: {rec_path}")
            recommendations = []

        # Generate report
        print("\nGenerating report...")
        report = generate_correlation_report(corr_matrix, high_corr, recommendations, args.output)

        print("\nReport generation complete!")
        print(f"Review the report: {args.output}")
        return 0

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
