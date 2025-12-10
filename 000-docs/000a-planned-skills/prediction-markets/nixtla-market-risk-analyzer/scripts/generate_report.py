#!/usr/bin/env python3
"""
Market Risk Analyzer - Report Generator
Creates comprehensive risk analysis report with visualizations
"""

import argparse
import json
import sys
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from typing import Dict


def create_risk_plots(
    prices: pd.DataFrame,
    returns: pd.Series,
    output_dir: str = "."
) -> Dict[str, str]:
    """Create risk visualization plots."""
    plots = {}

    # Calculate rolling volatility for plotting
    rolling_vol = returns.rolling(window=20).std() * (252 ** 0.5)

    # Calculate drawdown for plotting
    running_max = prices['price'].expanding().max()
    drawdown = (prices['price'] - running_max) / running_max

    # Price and Drawdown Plot
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    axes[0].plot(prices.index, prices['price'], color='blue')
    axes[0].set_ylabel('Price')
    axes[0].set_title('Price History')
    axes[0].grid(True, alpha=0.3)

    axes[1].fill_between(drawdown.index, drawdown * 100, 0, color='red', alpha=0.5)
    axes[1].set_ylabel('Drawdown (%)')
    axes[1].set_xlabel('Date')
    axes[1].set_title('Drawdown')
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{output_dir}/drawdown.png", dpi=150)
    plt.close()
    plots['drawdown'] = f"{output_dir}/drawdown.png"

    # Volatility Plot
    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(rolling_vol.index, rolling_vol * 100, color='orange')
    ax.axhline(y=rolling_vol.mean() * 100, color='green', linestyle='--', label='Average')
    ax.set_ylabel('Rolling Volatility (%)')
    ax.set_xlabel('Date')
    ax.set_title('Rolling 20-Day Volatility (Annualized)')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{output_dir}/volatility.png", dpi=150)
    plt.close()
    plots['volatility'] = f"{output_dir}/volatility.png"

    # Returns Distribution
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.hist(returns * 100, bins=50, density=True, alpha=0.7, color='blue')
    ax.axvline(x=returns.mean() * 100, color='green', linestyle='--', label='Mean')
    ax.axvline(x=returns.quantile(0.05) * 100, color='red', linestyle='--', label='5th Percentile (VaR)')
    ax.set_xlabel('Daily Return (%)')
    ax.set_ylabel('Density')
    ax.set_title('Return Distribution')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{output_dir}/var.png", dpi=150)
    plt.close()
    plots['var'] = f"{output_dir}/var.png"

    return plots


def generate_risk_report(
    risk_metrics: Dict,
    position_sizing: Dict,
    output_path: str = "risk_report.md"
) -> str:
    """Generate comprehensive markdown risk report."""

    var_95 = risk_metrics['var_95']
    var_99 = risk_metrics['var_99']
    vol = risk_metrics['volatility']
    dd = risk_metrics['drawdown']
    sharpe = risk_metrics['sharpe']

    report = f"""# Market Risk Analysis Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

| Metric | Value | Interpretation |
|--------|-------|----------------|
| VaR (95%) | {var_95['var_pct']:.2f}% | {var_95['interpretation']} |
| Volatility | {vol['annualized_volatility']*100:.1f}% | {vol['regime']} regime |
| Max Drawdown | {dd['max_drawdown_pct']:.1f}% | Occurred {dd['max_drawdown_date']} |
| Sharpe Ratio | {sharpe['sharpe_ratio']:.2f} | {sharpe['interpretation']} |

## Value at Risk (VaR)

### 95% Confidence Level

| Metric | Value |
|--------|-------|
| Daily VaR | {var_95['var_pct']:.2f}% |
| CVaR | {var_95['cvar']*100:.2f}% if var_95['cvar'] else "N/A" |

### 99% Confidence Level

| Metric | Value |
|--------|-------|
| Daily VaR | {var_99['var_pct']:.2f}% |
| CVaR | {var_99['cvar']*100:.2f}% if var_99['cvar'] else "N/A" |

## Volatility Analysis

| Metric | Value |
|--------|-------|
| Daily Volatility | {vol['daily_volatility']*100:.2f}% |
| Annualized Volatility | {vol['annualized_volatility']*100:.1f}% |
| Current Rolling Vol | {vol['current_rolling_vol']*100:.1f}% |
| Volatility Regime | **{vol['regime']}** |

## Drawdown Analysis

| Metric | Value |
|--------|-------|
| Maximum Drawdown | {dd['max_drawdown_pct']:.1f}% |
| Max Drawdown Date | {dd['max_drawdown_date']} |
| Recovery Date | {dd['recovery_date']} |
| Current Drawdown | {dd['current_drawdown_pct']:.1f}% |

## Risk-Adjusted Returns

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Sharpe Ratio | {sharpe['sharpe_ratio']:.2f} | {sharpe['interpretation']} |
| Sortino Ratio | {sharpe['sortino_ratio']:.2f if sharpe['sortino_ratio'] else "N/A"} | Downside-adjusted |
| Annualized Return | {sharpe['annualized_return']*100:.1f}% | |

## Position Sizing Recommendations

| Method | Position Size | % of Account |
|--------|---------------|--------------|
| Fixed Fractional | ${position_sizing['fixed_fractional']['max_position_value']:,.0f} | {position_sizing['fixed_fractional']['position_pct_of_account']:.1f}% |
| Volatility Adjusted | ${position_sizing['volatility_adjusted']['position_value']:,.0f} | {position_sizing['volatility_adjusted']['position_pct_of_account']:.1f}% |
| VaR-Based | ${position_sizing['var_based']['position_value']:,.0f} | {position_sizing['var_based']['position_pct_of_account']:.1f}% |

### Kelly Criterion

| Variant | Position % |
|---------|------------|
| Full Kelly | {position_sizing['kelly']['kelly_full']*100:.1f}% |
| Half Kelly | {position_sizing['kelly']['kelly_half']*100:.1f}% |

### Recommended Position

**${position_sizing['recommendation']['conservative_position']:,.0f}** ({position_sizing['recommendation']['conservative_pct']:.1f}% of account)

## Visualizations

- `drawdown.png` - Price history and drawdown chart
- `volatility.png` - Rolling volatility over time
- `var.png` - Return distribution with VaR levels

## Disclaimer

This analysis is for informational purposes only. Not financial advice.
"""

    with open(output_path, "w") as f:
        f.write(report)

    print(f"Report saved to {output_path}")
    return report


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Generate risk analysis report'
    )
    parser.add_argument(
        'price_file',
        help='Path to CSV file with price data'
    )
    parser.add_argument(
        '--risk-metrics',
        default='risk_metrics.json',
        help='Risk metrics JSON file (default: risk_metrics.json)'
    )
    parser.add_argument(
        '--position-sizing',
        default='position_sizing.json',
        help='Position sizing JSON file (default: position_sizing.json)'
    )
    parser.add_argument(
        '--output',
        default='risk_report.md',
        help='Output report file (default: risk_report.md)'
    )
    parser.add_argument(
        '--output-dir',
        default='.',
        help='Output directory for plots (default: current directory)'
    )

    args = parser.parse_args()

    try:
        # Load metrics
        with open(args.risk_metrics) as f:
            risk_metrics = json.load(f)

        with open(args.position_sizing) as f:
            position_sizing = json.load(f)

        # Load price data for plots
        from prepare_data import load_price_data, calculate_returns

        prices = load_price_data(args.price_file)
        returns = calculate_returns(prices)

        print("Creating visualizations...")
        plots = create_risk_plots(prices, returns, args.output_dir)

        print("Generating report...")
        generate_risk_report(risk_metrics, position_sizing, args.output)

        print("\nGenerated files:")
        print(f"  - {args.output}")
        for name, path in plots.items():
            print(f"  - {path}")

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
