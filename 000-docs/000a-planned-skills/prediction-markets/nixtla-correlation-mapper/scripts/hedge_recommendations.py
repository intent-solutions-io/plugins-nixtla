#!/usr/bin/env python3
"""
Correlation Mapper - Hedge Recommendations
Generates hedging strategies based on correlations
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
from scipy import stats


def calculate_hedge_ratio(
    returns: pd.DataFrame, target: str, hedge: str, method: str = "ols"
) -> Dict:
    """
    Calculate optimal hedge ratio between two contracts.

    Args:
        returns: Returns DataFrame
        target: Contract to hedge
        hedge: Contract used as hedge
        method: "ols" for regression, "min_variance" for minimum variance

    Returns:
        Dict with hedge ratio and statistics

    Raises:
        ValueError: If contracts not found or method invalid
    """
    if target not in returns.columns:
        raise ValueError(f"Target contract not found: {target}")
    if hedge not in returns.columns:
        raise ValueError(f"Hedge contract not found: {hedge}")

    target_returns = returns[target].dropna()
    hedge_returns = returns[hedge].dropna()

    # Align indices
    common_idx = target_returns.index.intersection(hedge_returns.index)
    target_returns = target_returns.loc[common_idx]
    hedge_returns = hedge_returns.loc[common_idx]

    if len(target_returns) < 3:
        raise ValueError("Insufficient data for hedge calculation")

    if method == "ols":
        # OLS regression: target = alpha + beta * hedge
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            hedge_returns, target_returns
        )
        hedge_ratio = -slope  # Negative for hedging

    elif method == "min_variance":
        # Minimum variance hedge ratio
        covariance = np.cov(target_returns, hedge_returns)[0, 1]
        variance = np.var(hedge_returns)
        if variance == 0:
            raise ValueError("Hedge contract has zero variance")
        hedge_ratio = -covariance / variance

    else:
        raise ValueError(f"Unknown method: {method}. Use 'ols' or 'min_variance'")

    # Calculate effectiveness
    correlation = np.corrcoef(target_returns, hedge_returns)[0, 1]
    variance_reduction = correlation ** 2

    return {
        "target": target,
        "hedge_instrument": hedge,
        "hedge_ratio": round(hedge_ratio, 4),
        "method": method,
        "correlation": round(correlation, 4),
        "r_squared": round(variance_reduction, 4),
        "variance_reduction_pct": round(variance_reduction * 100, 2),
        "interpretation": interpret_hedge_ratio(hedge_ratio, correlation),
    }


def interpret_hedge_ratio(ratio: float, correlation: float) -> str:
    """
    Generate human-readable interpretation of hedge ratio.

    Args:
        ratio: Hedge ratio value
        correlation: Correlation coefficient

    Returns:
        Interpretation string
    """
    if correlation > 0:
        direction = "SHORT"
        relationship = "positively correlated"
    else:
        direction = "LONG"
        relationship = "negatively correlated"

    return (
        f"For every 1 unit LONG in target, take {abs(ratio):.2f} units {direction} "
        f"in hedge instrument. Contracts are {relationship}."
    )


def generate_hedge_recommendations(
    returns: pd.DataFrame, corr_matrix: pd.DataFrame, top_n: int = 10
) -> List[Dict]:
    """
    Generate hedge recommendations for all significant pairs.

    Args:
        returns: Returns DataFrame
        corr_matrix: Correlation matrix
        top_n: Number of top recommendations

    Returns:
        List of hedge recommendations
    """
    recommendations = []
    contracts = corr_matrix.columns.tolist()

    # Find best hedge for each contract
    for target in contracts:
        best_hedge = None
        best_effectiveness = 0

        for hedge in contracts:
            if target == hedge:
                continue

            corr = abs(corr_matrix.loc[target, hedge])

            if corr > best_effectiveness:
                best_effectiveness = corr
                best_hedge = hedge

        if best_hedge and best_effectiveness > 0.3:
            try:
                rec = calculate_hedge_ratio(returns, target, best_hedge)
                recommendations.append(rec)
            except (ValueError, Exception) as e:
                print(f"Warning: Failed to calculate hedge for {target}: {e}")
                continue

    # Sort by variance reduction
    recommendations.sort(key=lambda x: x["variance_reduction_pct"], reverse=True)

    return recommendations[:top_n]


def create_hedge_portfolio(
    recommendations: List[Dict], portfolio_value: float = 100000
) -> pd.DataFrame:
    """
    Create a hedged portfolio based on recommendations.

    Args:
        recommendations: List of hedge recommendations
        portfolio_value: Total portfolio value

    Returns:
        DataFrame with portfolio allocations
    """
    if not recommendations:
        return pd.DataFrame(
            columns=["contract", "position_type", "position_value", "purpose"]
        )

    allocations = []
    equal_weight = portfolio_value / len(recommendations)

    for rec in recommendations:
        target_position = equal_weight
        hedge_position = target_position * abs(rec["hedge_ratio"])

        allocations.append(
            {
                "contract": rec["target"],
                "position_type": "LONG",
                "position_value": round(target_position, 2),
                "purpose": "Target",
            }
        )

        position_type = "SHORT" if rec["hedge_ratio"] < 0 else "LONG"
        allocations.append(
            {
                "contract": rec["hedge_instrument"],
                "position_type": position_type,
                "position_value": round(hedge_position, 2),
                "purpose": f"Hedge for {rec['target']}",
            }
        )

    return pd.DataFrame(allocations)


def main():
    """Main entry point for hedge recommendations."""
    parser = argparse.ArgumentParser(
        description="Generate hedge recommendations from correlation analysis"
    )
    parser.add_argument(
        "--returns",
        type=str,
        default="returns.csv",
        help="Input returns CSV file (default: returns.csv)",
    )
    parser.add_argument(
        "--correlation",
        type=str,
        default="correlation_matrix.csv",
        help="Input correlation matrix CSV (default: correlation_matrix.csv)",
    )
    parser.add_argument(
        "--method",
        type=str,
        default="ols",
        choices=["ols", "min_variance"],
        help="Hedge ratio method (default: ols)",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=10,
        help="Number of top recommendations to generate (default: 10)",
    )
    parser.add_argument(
        "--portfolio-value",
        type=float,
        default=100000,
        help="Total portfolio value for allocation (default: 100000)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=".",
        help="Output directory (default: current dir)",
    )

    args = parser.parse_args()

    try:
        # Load data
        returns_path = Path(args.returns)
        corr_path = Path(args.correlation)

        if not returns_path.exists():
            raise FileNotFoundError(f"Returns file not found: {returns_path}")
        if not corr_path.exists():
            raise FileNotFoundError(f"Correlation file not found: {corr_path}")

        returns = pd.read_csv(returns_path, index_col=0, parse_dates=True)
        corr_matrix = pd.read_csv(corr_path, index_col=0)

        print(f"Loaded returns: {len(returns)} rows x {len(returns.columns)} contracts")
        print(f"Loaded correlation matrix: {len(corr_matrix)} x {len(corr_matrix.columns)}")

        # Create output directory
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate recommendations
        print(f"\nGenerating top {args.top_n} hedge recommendations...")
        recommendations = generate_hedge_recommendations(
            returns, corr_matrix, top_n=args.top_n
        )

        if not recommendations:
            print("WARNING: No hedge recommendations could be generated")
            return 1

        # Save recommendations
        rec_df = pd.DataFrame(recommendations)
        rec_csv = output_dir / "hedge_recommendations.csv"
        rec_df.to_csv(rec_csv, index=False)
        print(f"Saved: {rec_csv}")

        rec_json = output_dir / "hedge_recommendations.json"
        with open(rec_json, "w") as f:
            json.dump(recommendations, f, indent=2)
        print(f"Saved: {rec_json}")

        # Create portfolio allocation
        print(f"\nCreating portfolio allocation (${args.portfolio_value:,.0f})...")
        portfolio = create_hedge_portfolio(recommendations, args.portfolio_value)
        portfolio_path = output_dir / "hedged_portfolio.csv"
        portfolio.to_csv(portfolio_path, index=False)
        print(f"Saved: {portfolio_path}")

        # Display top recommendations
        print(f"\nTop {min(3, len(recommendations))} hedge recommendations:")
        for i, rec in enumerate(recommendations[:3], 1):
            print(f"\n{i}. {rec['target']} hedged with {rec['hedge_instrument']}")
            print(f"   Ratio: {rec['hedge_ratio']:.2f}")
            print(f"   Variance Reduction: {rec['variance_reduction_pct']:.1f}%")
            print(f"   {rec['interpretation']}")

        print("\nNext: Run visualize.py to create charts")
        return 0

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
