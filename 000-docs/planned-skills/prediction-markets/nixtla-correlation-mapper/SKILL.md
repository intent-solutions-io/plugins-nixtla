---
name: nixtla-correlation-mapper
description: |
  Analyzes multi-contract correlations and generates hedge recommendations.
  Use when managing a portfolio of correlated assets and needing to mitigate risk.
  Trigger with "analyze correlations", "suggest hedge", "portfolio risk assessment".
allowed-tools: "Read,Write,Bash,Glob,Grep"
version: "1.0.0"
---

# Nixtla Correlation Mapper

Identifies correlations between multiple contracts and generates hedging strategies.

## Purpose

Analyzes relationships between assets in a portfolio to suggest hedging strategies for risk mitigation.

## Overview

Takes CSV data with multiple time series of contract values. Calculates correlation matrix between contracts. Using correlation coefficients, suggests optimal hedging strategies to reduce portfolio risk. Outputs correlation matrix, heatmap visualization, and hedging recommendations.

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep

**Environment**: None required (optional: `NIXTLA_TIMEGPT_API_KEY` for forecasted correlations)

**Packages**:
```bash
pip install pandas numpy scipy matplotlib seaborn
```

## Instructions

### Step 1: Load and Prepare Data

Create the data preparation script:

```python
#!/usr/bin/env python3
"""
Correlation Mapper - Data Preparation
Loads multi-series data and pivots for correlation analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple

def load_contract_data(filepath: str) -> pd.DataFrame:
    """
    Load multi-series contract data.

    Expected format: CSV with columns (unique_id, ds, y)
    where unique_id identifies different contracts.

    Args:
        filepath: Path to CSV file

    Returns:
        DataFrame in Nixtla format
    """
    print(f"Loading data from {filepath}...")

    df = pd.read_csv(filepath)

    # Validate columns
    required = ["unique_id", "ds", "y"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    # Convert types
    df["ds"] = pd.to_datetime(df["ds"])
    df["y"] = pd.to_numeric(df["y"], errors="coerce")
    df["unique_id"] = df["unique_id"].astype(str)

    # Sort
    df = df.sort_values(["unique_id", "ds"]).reset_index(drop=True)

    print(f"Loaded {len(df)} rows, {df['unique_id'].nunique()} contracts")
    return df

def pivot_for_correlation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pivot long-format data to wide format for correlation.

    Args:
        df: Long format with unique_id, ds, y

    Returns:
        Wide format with ds as index, contracts as columns
    """
    # Pivot: rows=dates, columns=contracts, values=prices
    pivoted = df.pivot(index="ds", columns="unique_id", values="y")

    # Forward fill missing values (for misaligned dates)
    pivoted = pivoted.ffill()

    # Drop any remaining NaN rows
    pivoted = pivoted.dropna()

    print(f"Pivoted to {len(pivoted)} dates x {len(pivoted.columns)} contracts")
    return pivoted

def calculate_returns(prices: pd.DataFrame, method: str = "log") -> pd.DataFrame:
    """
    Calculate returns from price data.

    Args:
        prices: Wide-format price DataFrame
        method: "log" for log returns, "simple" for simple returns

    Returns:
        Returns DataFrame
    """
    if method == "log":
        returns = np.log(prices / prices.shift(1))
    else:
        returns = prices.pct_change()

    # Drop first row (NaN)
    returns = returns.iloc[1:]

    return returns

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python prepare_data.py <contracts.csv>")
        sys.exit(1)

    filepath = sys.argv[1]
    df = load_contract_data(filepath)
    pivoted = pivot_for_correlation(df)
    returns = calculate_returns(pivoted)

    # Save intermediate files
    pivoted.to_csv("prices_wide.csv")
    returns.to_csv("returns.csv")

    print("\nData prepared:")
    print(f"  - prices_wide.csv ({len(pivoted)} x {len(pivoted.columns)})")
    print(f"  - returns.csv ({len(returns)} x {len(returns.columns)})")
```

### Step 2: Calculate Correlation Matrix

Create the correlation analysis script:

```python
#!/usr/bin/env python3
"""
Correlation Mapper - Correlation Analysis
Calculates correlation matrix and statistics
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, Tuple, List

def calculate_correlation_matrix(
    returns: pd.DataFrame,
    method: str = "pearson"
) -> pd.DataFrame:
    """
    Calculate correlation matrix from returns.

    Args:
        returns: Returns DataFrame (dates x contracts)
        method: "pearson", "spearman", or "kendall"

    Returns:
        Correlation matrix DataFrame
    """
    if method == "pearson":
        corr = returns.corr(method="pearson")
    elif method == "spearman":
        corr = returns.corr(method="spearman")
    elif method == "kendall":
        corr = returns.corr(method="kendall")
    else:
        raise ValueError(f"Unknown method: {method}")

    return corr

def calculate_rolling_correlation(
    returns: pd.DataFrame,
    window: int = 30,
    pair: Tuple[str, str] = None
) -> pd.DataFrame:
    """
    Calculate rolling correlation for analysis of stability.

    Args:
        returns: Returns DataFrame
        window: Rolling window size
        pair: Specific pair to calculate, or None for all pairs

    Returns:
        Rolling correlation DataFrame
    """
    if pair:
        col1, col2 = pair
        rolling = returns[col1].rolling(window).corr(returns[col2])
        return pd.DataFrame({f"{col1}_vs_{col2}": rolling})

    # Calculate for all pairs
    contracts = returns.columns.tolist()
    rolling_corrs = {}

    for i, c1 in enumerate(contracts):
        for c2 in contracts[i+1:]:
            key = f"{c1}_vs_{c2}"
            rolling_corrs[key] = returns[c1].rolling(window).corr(returns[c2])

    return pd.DataFrame(rolling_corrs)

def identify_high_correlations(
    corr_matrix: pd.DataFrame,
    threshold: float = 0.7
) -> List[Dict]:
    """
    Identify highly correlated pairs (potential hedges).

    Args:
        corr_matrix: Correlation matrix
        threshold: Correlation threshold (absolute value)

    Returns:
        List of high correlation pairs with details
    """
    pairs = []
    contracts = corr_matrix.columns.tolist()

    for i, c1 in enumerate(contracts):
        for j, c2 in enumerate(contracts):
            if i >= j:  # Skip diagonal and duplicates
                continue

            corr = corr_matrix.loc[c1, c2]

            if abs(corr) >= threshold:
                pairs.append({
                    "contract_1": c1,
                    "contract_2": c2,
                    "correlation": round(corr, 4),
                    "relationship": "positive" if corr > 0 else "negative",
                    "hedge_potential": "high" if corr < -0.5 else "medium" if abs(corr) > 0.8 else "low"
                })

    # Sort by absolute correlation
    pairs.sort(key=lambda x: abs(x["correlation"]), reverse=True)

    return pairs

def calculate_p_values(
    returns: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate statistical significance of correlations.

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
                corr, p = stats.pearsonr(returns[c1].dropna(), returns[c2].dropna())
                p_values.loc[c1, c2] = p

    return p_values

if __name__ == "__main__":
    import json

    # Load returns
    returns = pd.read_csv("returns.csv", index_col=0, parse_dates=True)

    print("Calculating correlations...")

    # Calculate correlation matrix
    corr_matrix = calculate_correlation_matrix(returns, method="pearson")
    corr_matrix.to_csv("correlation_matrix.csv")
    print(f"Saved correlation_matrix.csv")

    # Calculate p-values
    p_values = calculate_p_values(returns)
    p_values.to_csv("correlation_pvalues.csv")

    # Identify high correlations
    high_corr = identify_high_correlations(corr_matrix, threshold=0.5)

    print(f"\nFound {len(high_corr)} pairs with |correlation| > 0.5")
    for pair in high_corr[:5]:
        print(f"  {pair['contract_1']} <-> {pair['contract_2']}: {pair['correlation']:.3f}")

    # Save high correlations
    with open("high_correlations.json", "w") as f:
        json.dump(high_corr, f, indent=2)
```

### Step 3: Generate Hedge Recommendations

Create the hedging strategy script:

```python
#!/usr/bin/env python3
"""
Correlation Mapper - Hedge Recommendations
Generates hedging strategies based on correlations
"""

import pandas as pd
import numpy as np
from typing import Dict, List

def calculate_hedge_ratio(
    returns: pd.DataFrame,
    target: str,
    hedge: str,
    method: str = "ols"
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
    """
    from scipy import stats

    target_returns = returns[target].dropna()
    hedge_returns = returns[hedge].dropna()

    # Align indices
    common_idx = target_returns.index.intersection(hedge_returns.index)
    target_returns = target_returns.loc[common_idx]
    hedge_returns = hedge_returns.loc[common_idx]

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
        hedge_ratio = -covariance / variance

    else:
        raise ValueError(f"Unknown method: {method}")

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
        "interpretation": interpret_hedge_ratio(hedge_ratio, correlation)
    }

def interpret_hedge_ratio(ratio: float, correlation: float) -> str:
    """Generate human-readable interpretation of hedge ratio."""
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
    returns: pd.DataFrame,
    corr_matrix: pd.DataFrame,
    top_n: int = 10
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

    # Find all pairs with significant correlation
    for i, target in enumerate(contracts):
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
            rec = calculate_hedge_ratio(returns, target, best_hedge)
            recommendations.append(rec)

    # Sort by variance reduction
    recommendations.sort(key=lambda x: x["variance_reduction_pct"], reverse=True)

    return recommendations[:top_n]

def create_hedge_portfolio(
    recommendations: List[Dict],
    portfolio_value: float = 100000
) -> pd.DataFrame:
    """
    Create a hedged portfolio based on recommendations.

    Args:
        recommendations: List of hedge recommendations
        portfolio_value: Total portfolio value

    Returns:
        DataFrame with portfolio allocations
    """
    allocations = []

    equal_weight = portfolio_value / len(recommendations)

    for rec in recommendations:
        target_position = equal_weight
        hedge_position = target_position * rec["hedge_ratio"]

        allocations.append({
            "contract": rec["target"],
            "position_type": "LONG",
            "position_value": target_position,
            "purpose": "Target"
        })

        allocations.append({
            "contract": rec["hedge_instrument"],
            "position_type": "SHORT" if rec["hedge_ratio"] < 0 else "LONG",
            "position_value": abs(hedge_position),
            "purpose": f"Hedge for {rec['target']}"
        })

    return pd.DataFrame(allocations)

if __name__ == "__main__":
    import json

    # Load data
    returns = pd.read_csv("returns.csv", index_col=0, parse_dates=True)
    corr_matrix = pd.read_csv("correlation_matrix.csv", index_col=0)

    print("Generating hedge recommendations...")

    # Generate recommendations
    recommendations = generate_hedge_recommendations(returns, corr_matrix, top_n=10)

    # Save recommendations
    recommendations_df = pd.DataFrame(recommendations)
    recommendations_df.to_csv("hedge_recommendations.csv", index=False)

    with open("hedge_recommendations.json", "w") as f:
        json.dump(recommendations, f, indent=2)

    # Create portfolio allocation
    portfolio = create_hedge_portfolio(recommendations)
    portfolio.to_csv("hedged_portfolio.csv", index=False)

    print(f"\nGenerated {len(recommendations)} hedge recommendations")
    print("\nTop recommendations:")
    for rec in recommendations[:3]:
        print(f"  {rec['target']} hedged with {rec['hedge_instrument']}")
        print(f"    Ratio: {rec['hedge_ratio']:.2f}, Var Reduction: {rec['variance_reduction_pct']:.1f}%")
```

### Step 4: Create Visualization

Create the visualization script:

```python
#!/usr/bin/env python3
"""
Correlation Mapper - Visualization
Creates correlation heatmap and analysis plots
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional

def create_correlation_heatmap(
    corr_matrix: pd.DataFrame,
    output_path: str = "correlation_heatmap.png",
    title: str = "Contract Correlation Matrix"
) -> None:
    """
    Create a correlation heatmap visualization.

    Args:
        corr_matrix: Correlation matrix DataFrame
        output_path: Path to save the plot
        title: Plot title
    """
    # Set up the figure
    n_contracts = len(corr_matrix)
    fig_size = max(10, n_contracts * 0.5)

    fig, ax = plt.subplots(figsize=(fig_size, fig_size * 0.8))

    # Create heatmap
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)

    cmap = sns.diverging_palette(250, 10, as_cmap=True)

    sns.heatmap(
        corr_matrix,
        mask=mask,
        cmap=cmap,
        vmin=-1,
        vmax=1,
        center=0,
        square=True,
        linewidths=0.5,
        annot=True if n_contracts <= 10 else False,
        fmt=".2f",
        ax=ax
    )

    ax.set_title(title, fontsize=14, fontweight="bold")

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"Saved heatmap to {output_path}")

def create_rolling_correlation_plot(
    rolling_corr: pd.DataFrame,
    output_path: str = "rolling_correlation.png",
    top_n: int = 5
) -> None:
    """
    Plot rolling correlations over time.

    Args:
        rolling_corr: Rolling correlation DataFrame
        output_path: Path to save the plot
        top_n: Number of pairs to plot
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot top N pairs by volatility (most interesting)
    volatility = rolling_corr.std().sort_values(ascending=False)
    top_pairs = volatility.head(top_n).index.tolist()

    for pair in top_pairs:
        ax.plot(rolling_corr.index, rolling_corr[pair], label=pair, alpha=0.7)

    ax.axhline(y=0, color="black", linestyle="--", alpha=0.3)
    ax.axhline(y=0.5, color="green", linestyle=":", alpha=0.3)
    ax.axhline(y=-0.5, color="red", linestyle=":", alpha=0.3)

    ax.set_xlabel("Date")
    ax.set_ylabel("Rolling Correlation")
    ax.set_title("Rolling 30-Day Correlation Between Contracts")
    ax.legend(loc="upper left", bbox_to_anchor=(1, 1))
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"Saved rolling correlation plot to {output_path}")

def create_hedge_effectiveness_chart(
    recommendations: list,
    output_path: str = "hedge_effectiveness.png"
) -> None:
    """
    Create bar chart of hedge effectiveness.

    Args:
        recommendations: List of hedge recommendation dicts
        output_path: Path to save the plot
    """
    if not recommendations:
        print("No recommendations to plot")
        return

    fig, ax = plt.subplots(figsize=(10, 6))

    labels = [f"{r['target']}\n→{r['hedge_instrument']}" for r in recommendations]
    effectiveness = [r["variance_reduction_pct"] for r in recommendations]
    colors = ["green" if e > 50 else "orange" if e > 25 else "red" for e in effectiveness]

    bars = ax.barh(labels, effectiveness, color=colors, alpha=0.7)

    # Add value labels
    for bar, val in zip(bars, effectiveness):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                f"{val:.1f}%", va="center", fontsize=9)

    ax.set_xlabel("Variance Reduction (%)")
    ax.set_title("Hedge Effectiveness by Contract Pair")
    ax.axvline(x=50, color="green", linestyle="--", alpha=0.5, label="Good (>50%)")
    ax.axvline(x=25, color="orange", linestyle="--", alpha=0.5, label="Moderate (>25%)")

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"Saved hedge effectiveness chart to {output_path}")

if __name__ == "__main__":
    import json

    # Load data
    corr_matrix = pd.read_csv("correlation_matrix.csv", index_col=0)

    # Create heatmap
    create_correlation_heatmap(corr_matrix)

    # Load and plot rolling correlations if available
    try:
        rolling = pd.read_csv("rolling_correlations.csv", index_col=0, parse_dates=True)
        create_rolling_correlation_plot(rolling)
    except FileNotFoundError:
        print("No rolling correlations file found, skipping plot")

    # Load and plot hedge effectiveness
    try:
        with open("hedge_recommendations.json") as f:
            recommendations = json.load(f)
        create_hedge_effectiveness_chart(recommendations)
    except FileNotFoundError:
        print("No recommendations file found, skipping chart")
```

### Step 5: Generate Report

Create the comprehensive report:

```python
#!/usr/bin/env python3
"""
Correlation Mapper - Report Generator
Creates comprehensive correlation analysis report
"""

import json
import pandas as pd
from datetime import datetime

def generate_correlation_report() -> str:
    """Generate markdown report of correlation analysis."""

    # Load all data
    corr_matrix = pd.read_csv("correlation_matrix.csv", index_col=0)

    with open("high_correlations.json") as f:
        high_corr = json.load(f)

    with open("hedge_recommendations.json") as f:
        recommendations = json.load(f)

    n_contracts = len(corr_matrix)

    report = f"""# Portfolio Correlation Analysis Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary

| Metric | Value |
|--------|-------|
| Contracts Analyzed | {n_contracts} |
| Total Pairs | {n_contracts * (n_contracts - 1) // 2} |
| High Correlation Pairs (|r| > 0.5) | {len(high_corr)} |
| Hedge Recommendations | {len(recommendations)} |

## Correlation Matrix

See `correlation_matrix.csv` and `correlation_heatmap.png` for full matrix.

### Key Statistics

| Statistic | Value |
|-----------|-------|
| Average Correlation | {corr_matrix.values[~np.eye(n_contracts, dtype=bool)].mean():.3f} |
| Max Positive Correlation | {corr_matrix.values[~np.eye(n_contracts, dtype=bool)].max():.3f} |
| Max Negative Correlation | {corr_matrix.values[~np.eye(n_contracts, dtype=bool)].min():.3f} |

## High Correlation Pairs

| Contract 1 | Contract 2 | Correlation | Relationship | Hedge Potential |
|------------|------------|-------------|--------------|-----------------|
"""

    for pair in high_corr[:10]:
        report += f"| {pair['contract_1']} | {pair['contract_2']} | {pair['correlation']:.3f} | {pair['relationship']} | {pair['hedge_potential']} |\n"

    if len(high_corr) > 10:
        report += f"\n*...and {len(high_corr) - 10} more pairs*\n"

    report += """
## Hedge Recommendations

| Target | Hedge Instrument | Ratio | Var Reduction |
|--------|------------------|-------|---------------|
"""

    for rec in recommendations[:10]:
        report += f"| {rec['target']} | {rec['hedge_instrument']} | {rec['hedge_ratio']:.2f} | {rec['variance_reduction_pct']:.1f}% |\n"

    report += """
## Interpretation Guide

### Correlation Values
- **+0.7 to +1.0**: Strong positive - move together
- **+0.3 to +0.7**: Moderate positive - some co-movement
- **-0.3 to +0.3**: Weak/No correlation - independent
- **-0.7 to -0.3**: Moderate negative - partial hedge potential
- **-1.0 to -0.7**: Strong negative - excellent hedge

### Hedge Ratio Interpretation
- **Positive ratio**: Same direction position (unusual for hedging)
- **Negative ratio**: Opposite direction (typical hedge)
- **Ratio magnitude**: Units of hedge per unit of target

## Output Files

- `correlation_matrix.csv` - Full correlation matrix
- `correlation_heatmap.png` - Visual heatmap
- `hedge_recommendations.csv` - Detailed recommendations
- `hedged_portfolio.csv` - Sample portfolio allocation

## Risk Disclaimer

Correlations are historical and may not persist. Past relationships do not guarantee future behavior. Always validate hedging strategies before implementation.
"""

    # Save report
    with open("correlation_report.md", "w") as f:
        f.write(report)

    print("Report saved to correlation_report.md")
    return report

if __name__ == "__main__":
    import numpy as np
    generate_correlation_report()
```

## Output

- **correlation_matrix.csv**: Full correlation matrix
- **correlation_heatmap.png**: Visual heatmap
- **hedge_recommendations.csv**: Detailed hedging suggestions
- **hedged_portfolio.csv**: Sample portfolio allocation
- **correlation_report.md**: Comprehensive analysis report

## Error Handling

1. **Error**: `Input file not found`
   **Solution**: Verify file path exists with `ls -la`

2. **Error**: `Missing required columns`
   **Solution**: Ensure CSV has unique_id, ds, y columns

3. **Error**: `Insufficient data points`
   **Solution**: Need at least 30 data points per contract for reliable correlations

4. **Error**: `Invalid data format`
   **Solution**: Check that y values are numeric

## Examples

### Example 1: Analyze Crypto Portfolio

**Input** (portfolio.csv):
```csv
unique_id,ds,y
BTC,2024-01-01,42000
ETH,2024-01-01,2200
BTC,2024-01-02,42500
ETH,2024-01-02,2250
```

**Output**:
```
Correlation: BTC <-> ETH: 0.85
Hedge Ratio: -0.95
Interpretation: Strong positive correlation,
hedge by shorting 0.95 ETH per 1 BTC long
```

### Example 2: Prediction Market Contracts

**Input**: 5 related election contracts

**Output**:
```
Found 3 pairs with |correlation| > 0.7
Top hedge: Contract A hedged with Contract B
Variance Reduction: 62%
```

## Usage

```bash
# Complete workflow
python prepare_data.py contracts.csv
python correlation_analysis.py
python hedge_recommendations.py
python visualize.py
python generate_report.py

# Or run all at once (if combined script)
python correlation_mapper.py contracts.csv --output-dir results/
```
