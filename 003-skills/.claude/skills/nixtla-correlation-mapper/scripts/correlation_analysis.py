#!/usr/bin/env python3
"""
Correlation Mapper - Correlation Analysis
Calculates correlation matrix and identifies significant pairs
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from scipy import stats


def calculate_correlation_matrix(returns: pd.DataFrame, method: str = "pearson") -> pd.DataFrame:
    """
    Calculate correlation matrix from returns.

    Args:
        returns: Returns DataFrame (dates x contracts)
        method: "pearson", "spearman", or "kendall"

    Returns:
        Correlation matrix DataFrame

    Raises:
        ValueError: If invalid method specified
    """
    valid_methods = ["pearson", "spearman", "kendall"]
    if method not in valid_methods:
        raise ValueError(f"Invalid method: {method}. Use one of {valid_methods}")

    corr = returns.corr(method=method)
    return corr


def calculate_rolling_correlation(
    returns: pd.DataFrame, window: int = 30, pair: Tuple[str, str] = None
) -> pd.DataFrame:
    """
    Calculate rolling correlation for stability analysis.

    Args:
        returns: Returns DataFrame
        window: Rolling window size
        pair: Specific pair to calculate, or None for all pairs

    Returns:
        Rolling correlation DataFrame
    """
    if window < 2:
        raise ValueError(f"Window must be >= 2, got {window}")

    if pair:
        col1, col2 = pair
        if col1 not in returns.columns or col2 not in returns.columns:
            raise ValueError(f"Pair {pair} not found in returns columns")
        rolling = returns[col1].rolling(window).corr(returns[col2])
        return pd.DataFrame({f"{col1}_vs_{col2}": rolling})

    # Calculate for all pairs
    contracts = returns.columns.tolist()
    rolling_corrs = {}

    for i, c1 in enumerate(contracts):
        for c2 in contracts[i + 1 :]:
            key = f"{c1}_vs_{c2}"
            rolling_corrs[key] = returns[c1].rolling(window).corr(returns[c2])

    return pd.DataFrame(rolling_corrs)


def identify_high_correlations(corr_matrix: pd.DataFrame, threshold: float = 0.7) -> List[Dict]:
    """
    Identify highly correlated pairs.

    Args:
        corr_matrix: Correlation matrix
        threshold: Correlation threshold (absolute value)

    Returns:
        List of high correlation pairs with details
    """
    if not 0 <= threshold <= 1:
        raise ValueError(f"Threshold must be between 0 and 1, got {threshold}")

    pairs = []
    contracts = corr_matrix.columns.tolist()

    for i, c1 in enumerate(contracts):
        for j, c2 in enumerate(contracts):
            if i >= j:  # Skip diagonal and duplicates
                continue

            corr = corr_matrix.loc[c1, c2]

            if abs(corr) >= threshold:
                # Determine hedge potential
                if corr < -0.5:
                    hedge_potential = "high"
                elif abs(corr) > 0.8:
                    hedge_potential = "medium"
                else:
                    hedge_potential = "low"

                pairs.append(
                    {
                        "contract_1": c1,
                        "contract_2": c2,
                        "correlation": round(corr, 4),
                        "relationship": "positive" if corr > 0 else "negative",
                        "hedge_potential": hedge_potential,
                    }
                )

    # Sort by absolute correlation
    pairs.sort(key=lambda x: abs(x["correlation"]), reverse=True)

    return pairs


def calculate_p_values(returns: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate statistical significance of correlations.

    Args:
        returns: Returns DataFrame

    Returns:
        P-value matrix
    """
    n = len(returns)
    contracts = returns.columns.tolist()
    p_values = pd.DataFrame(index=contracts, columns=contracts, dtype=float)

    for c1 in contracts:
        for c2 in contracts:
            if c1 == c2:
                p_values.loc[c1, c2] = 0.0
            else:
                data1 = returns[c1].dropna()
                data2 = returns[c2].dropna()

                # Align indices
                common_idx = data1.index.intersection(data2.index)
                data1 = data1.loc[common_idx]
                data2 = data2.loc[common_idx]

                if len(data1) < 3:
                    p_values.loc[c1, c2] = 1.0
                else:
                    _, p = stats.pearsonr(data1, data2)
                    p_values.loc[c1, c2] = p

    return p_values


def main():
    """Main entry point for correlation analysis."""
    parser = argparse.ArgumentParser(
        description="Calculate correlation matrix and identify significant pairs"
    )
    parser.add_argument(
        "--returns",
        type=str,
        default="returns.csv",
        help="Input returns CSV file (default: returns.csv)",
    )
    parser.add_argument(
        "--method",
        type=str,
        default="pearson",
        choices=["pearson", "spearman", "kendall"],
        help="Correlation method (default: pearson)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="Correlation threshold for high correlations (default: 0.5)",
    )
    parser.add_argument(
        "--rolling-window",
        type=int,
        default=30,
        help="Rolling correlation window size (default: 30)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=".",
        help="Output directory (default: current dir)",
    )

    args = parser.parse_args()

    try:
        # Load returns
        returns_path = Path(args.returns)
        if not returns_path.exists():
            raise FileNotFoundError(f"Returns file not found: {returns_path}")

        returns = pd.read_csv(returns_path, index_col=0, parse_dates=True)
        print(f"Loaded returns: {len(returns)} rows x {len(returns.columns)} contracts")

        # Create output directory
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Calculate correlation matrix
        print(f"\nCalculating {args.method} correlations...")
        corr_matrix = calculate_correlation_matrix(returns, method=args.method)
        corr_path = output_dir / "correlation_matrix.csv"
        corr_matrix.to_csv(corr_path)
        print(f"Saved: {corr_path}")

        # Calculate p-values
        print("Calculating statistical significance...")
        p_values = calculate_p_values(returns)
        p_path = output_dir / "correlation_pvalues.csv"
        p_values.to_csv(p_path)
        print(f"Saved: {p_path}")

        # Identify high correlations
        print(f"\nIdentifying pairs with |correlation| > {args.threshold}...")
        high_corr = identify_high_correlations(corr_matrix, threshold=args.threshold)
        print(f"Found {len(high_corr)} significant pairs")

        if high_corr:
            print("\nTop correlations:")
            for pair in high_corr[:5]:
                print(
                    f"  {pair['contract_1']} <-> {pair['contract_2']}: "
                    f"{pair['correlation']:.3f} ({pair['relationship']})"
                )

        # Save high correlations
        high_corr_path = output_dir / "high_correlations.json"
        with open(high_corr_path, "w") as f:
            json.dump(high_corr, f, indent=2)
        print(f"\nSaved: {high_corr_path}")

        # Calculate rolling correlations
        if len(returns) >= args.rolling_window:
            print(f"\nCalculating rolling {args.rolling_window}-day correlations...")
            rolling_corr = calculate_rolling_correlation(returns, window=args.rolling_window)
            rolling_path = output_dir / "rolling_correlations.csv"
            rolling_corr.to_csv(rolling_path)
            print(f"Saved: {rolling_path}")
        else:
            print(
                f"\nSkipping rolling correlation: insufficient data "
                f"({len(returns)} < {args.rolling_window})"
            )

        print("\nNext: Run hedge_recommendations.py")
        return 0

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
