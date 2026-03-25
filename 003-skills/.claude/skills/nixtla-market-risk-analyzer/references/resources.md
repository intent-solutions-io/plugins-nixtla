# Market Risk Analyzer Resources

## Statistical Methods

- **VaR**: Historical simulation, parametric (Gaussian), and Monte Carlo methods are supported. Historical simulation is the default as it makes no distributional assumptions.
- **Volatility**: EWMA (Exponentially Weighted Moving Average) for responsive estimates, GARCH models available in extension for modeling volatility clustering.
- **Drawdown**: Peak-to-trough analysis with automatic recovery period tracking and regime detection.

## Position Sizing Theory

- **Kelly Criterion**: Optimal bet sizing for known edge. Maximizes long-term geometric growth rate but can be aggressive in practice.
- **Fixed Fractional**: Fixed percentage of account risked per trade. Simple and widely used. Default risk-per-trade is 2%.
- **Volatility Targeting**: Normalize risk across assets by targeting specific portfolio volatility. Adjusts position size inversely to asset volatility.
- **VaR-Based**: Limits maximum Value at Risk loss per position. Conservative approach suitable for institutional portfolios.

## Best Practices

- Use Half Kelly for practical trading since Full Kelly is too aggressive for real-world applications with estimation error.
- Combine multiple sizing methods and choose the most conservative recommendation.
- Adjust for liquidity constraints and execution costs that reduce effective returns.
- Monitor regime changes (HIGH/NORMAL/LOW volatility) and reduce position sizes during high volatility periods.
- Rebalance positions when volatility regime shifts to maintain target risk exposure.

## Academic References

- VaR methodology: RiskMetrics Technical Document (J.P. Morgan)
- Kelly Criterion: Fortune's Formula (Poundstone)
- Sharpe Ratio: "The Sharpe Ratio" (Sharpe, 1994)
- Position Sizing: "Trade Your Way to Financial Freedom" (Tharp)
