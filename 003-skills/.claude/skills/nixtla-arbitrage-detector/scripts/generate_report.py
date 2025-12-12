#!/usr/bin/env python3
"""
Arbitrage Report Generator
Creates a formatted report of arbitrage opportunities
"""

from datetime import datetime

import pandas as pd


def generate_report():
    """Generate a markdown report of arbitrage opportunities."""

    try:
        df = pd.read_csv("arbitrage_opportunities.csv")
    except FileNotFoundError:
        print("No arbitrage_opportunities.csv found. Run detection first.")
        return

    report = f"""# Arbitrage Opportunities Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Markets Compared**: Polymarket vs Kalshi

## Summary

- **Total Opportunities Found**: {len(df)}
- **Best Profit %**: {df['profit_pct'].max():.2f}%
- **Average Profit %**: {df['profit_pct'].mean():.2f}%

## Top Opportunities

| Event | Strategy | Profit | Profit % |
|-------|----------|--------|----------|
"""

    for _, row in df.head(10).iterrows():
        event = row["event_name"][:40] + "..." if len(row["event_name"]) > 40 else row["event_name"]
        report += (
            f"| {event} | {row['strategy']} | ${row['profit']:.4f} | {row['profit_pct']:.2f}% |\n"
        )

    report += """
## Risk Warnings

1. **Execution Risk**: Prices may change before trades execute
2. **Liquidity Risk**: May not be able to fill orders at quoted prices
3. **Platform Risk**: Different settlement rules between platforms
4. **Fee Changes**: Trading fees may change without notice

## Recommended Actions

1. Verify prices manually before trading
2. Start with small position sizes
3. Monitor for price convergence
4. Consider slippage in calculations

---
*This report is for informational purposes only. Not financial advice.*
"""

    with open("arbitrage_report.md", "w") as f:
        f.write(report)

    print("Report saved to arbitrage_report.md")
    return report


if __name__ == "__main__":
    generate_report()
