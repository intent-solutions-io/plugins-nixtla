#!/usr/bin/env python3
"""
Market Risk Analyzer - Risk Metrics
Calculates VaR, volatility, drawdown, and other risk metrics
"""

import argparse
import json
import sys
import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict


def calculate_var(
    returns: pd.Series,
    confidence: float = 0.95,
    method: str = "historical"
) -> Dict:
    """
    Calculate Value at Risk (VaR).

    Args:
        returns: Series of returns
        confidence: Confidence level (e.g., 0.95 for 95%)
        method: "historical", "parametric", or "monte_carlo"

    Returns:
        Dict with VaR values and metadata
    """
    alpha = 1 - confidence

    if method == "historical":
        var = np.percentile(returns, alpha * 100)
    elif method == "parametric":
        mu = returns.mean()
        sigma = returns.std()
        var = stats.norm.ppf(alpha, mu, sigma)
    elif method == "monte_carlo":
        mu = returns.mean()
        sigma = returns.std()
        simulations = np.random.normal(mu, sigma, 10000)
        var = np.percentile(simulations, alpha * 100)
    else:
        raise ValueError(f"Unknown method: {method}")

    # Calculate CVaR (Expected Shortfall)
    cvar = returns[returns <= var].mean()

    return {
        "var": round(var, 6),
        "var_pct": round(var * 100, 4),
        "cvar": round(cvar, 6) if not np.isnan(cvar) else None,
        "confidence": confidence,
        "method": method,
        "interpretation": f"At {confidence*100:.0f}% confidence, maximum daily loss is {abs(var)*100:.2f}%"
    }


def calculate_volatility(
    returns: pd.Series,
    window: int = 20,
    annualize: bool = True,
    trading_days: int = 252
) -> Dict:
    """Calculate historical and rolling volatility."""
    hist_vol = returns.std()
    hist_vol_annual = hist_vol * np.sqrt(trading_days) if annualize else None

    rolling_vol = returns.rolling(window=window).std()
    if annualize:
        rolling_vol = rolling_vol * np.sqrt(trading_days)

    current_vol = rolling_vol.iloc[-1]
    avg_vol = rolling_vol.mean()
    vol_percentile = stats.percentileofscore(rolling_vol.dropna(), current_vol)

    return {
        "daily_volatility": round(hist_vol, 6),
        "annualized_volatility": round(hist_vol_annual, 4) if hist_vol_annual else None,
        "current_rolling_vol": round(current_vol, 4),
        "average_rolling_vol": round(avg_vol, 4),
        "volatility_percentile": round(vol_percentile, 1),
        "window": window,
        "regime": "HIGH" if vol_percentile > 75 else "LOW" if vol_percentile < 25 else "NORMAL"
    }


def calculate_drawdown(prices: pd.DataFrame) -> Dict:
    """Calculate maximum drawdown and drawdown statistics."""
    price_series = prices['price']
    running_max = price_series.expanding().max()
    drawdown = (price_series - running_max) / running_max

    max_drawdown = drawdown.min()
    max_dd_date = drawdown.idxmin()

    # Find recovery
    post_dd = drawdown[max_dd_date:]
    recovery_dates = post_dd[post_dd >= 0].index

    if len(recovery_dates) > 0:
        recovery_date = recovery_dates[0]
        recovery_days = (recovery_date - max_dd_date).days
    else:
        recovery_date = None
        recovery_days = None

    current_dd = drawdown.iloc[-1]
    avg_dd = drawdown.mean()

    return {
        "max_drawdown": round(max_drawdown, 4),
        "max_drawdown_pct": round(max_drawdown * 100, 2),
        "max_drawdown_date": max_dd_date.strftime("%Y-%m-%d"),
        "recovery_date": recovery_date.strftime("%Y-%m-%d") if recovery_date else "Not recovered",
        "recovery_days": recovery_days,
        "current_drawdown": round(current_dd, 4),
        "current_drawdown_pct": round(current_dd * 100, 2),
        "average_drawdown": round(avg_dd, 4)
    }


def calculate_sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.05,
    trading_days: int = 252
) -> Dict:
    """Calculate Sharpe ratio and related metrics."""
    annual_return = returns.mean() * trading_days
    annual_vol = returns.std() * np.sqrt(trading_days)
    sharpe = (annual_return - risk_free_rate) / annual_vol

    downside_returns = returns[returns < 0]
    downside_vol = downside_returns.std() * np.sqrt(trading_days)
    sortino = (annual_return - risk_free_rate) / downside_vol if downside_vol > 0 else np.nan

    def interpret_sharpe(sharpe_val):
        if sharpe_val >= 2.0:
            return "Excellent risk-adjusted returns"
        elif sharpe_val >= 1.0:
            return "Good risk-adjusted returns"
        elif sharpe_val >= 0.5:
            return "Moderate risk-adjusted returns"
        elif sharpe_val >= 0:
            return "Poor risk-adjusted returns"
        else:
            return "Negative risk-adjusted returns"

    return {
        "sharpe_ratio": round(sharpe, 3),
        "sortino_ratio": round(sortino, 3) if not np.isnan(sortino) else None,
        "annualized_return": round(annual_return, 4),
        "annualized_volatility": round(annual_vol, 4),
        "risk_free_rate": risk_free_rate,
        "interpretation": interpret_sharpe(sharpe)
    }


def run_risk_analysis(prices: pd.DataFrame, returns: pd.Series) -> Dict:
    """Run complete risk analysis."""
    var_95 = calculate_var(returns, confidence=0.95, method="historical")
    var_99 = calculate_var(returns, confidence=0.99, method="historical")
    volatility = calculate_volatility(returns)
    drawdown = calculate_drawdown(prices)
    sharpe = calculate_sharpe_ratio(returns)

    return {
        "var_95": var_95,
        "var_99": var_99,
        "volatility": volatility,
        "drawdown": drawdown,
        "sharpe": sharpe,
        "summary": {
            "daily_var_95": var_95["var_pct"],
            "annualized_volatility": volatility["annualized_volatility"],
            "max_drawdown_pct": drawdown["max_drawdown_pct"],
            "sharpe_ratio": sharpe["sharpe_ratio"],
            "volatility_regime": volatility["regime"]
        }
    }


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Calculate risk metrics from price data'
    )
    parser.add_argument(
        'input_file',
        help='Path to CSV file with price data'
    )
    parser.add_argument(
        '--output',
        default='risk_metrics.json',
        help='Output file for risk metrics (default: risk_metrics.json)'
    )
    parser.add_argument(
        '--risk-free-rate',
        type=float,
        default=0.05,
        help='Annual risk-free rate for Sharpe calculation (default: 0.05)'
    )

    args = parser.parse_args()

    try:
        # Load data
        from prepare_data import load_price_data, calculate_returns

        prices = load_price_data(args.input_file)
        returns = calculate_returns(prices)

        print("\nCalculating risk metrics...")
        results = run_risk_analysis(prices, returns)

        # Save results
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2, default=str)

        print("\n" + "="*50)
        print("RISK ANALYSIS SUMMARY")
        print("="*50)
        print(f"VaR (95%): {results['var_95']['var_pct']:.2f}%")
        print(f"VaR (99%): {results['var_99']['var_pct']:.2f}%")
        print(f"Annualized Volatility: {results['volatility']['annualized_volatility']*100:.1f}%")
        print(f"Max Drawdown: {results['drawdown']['max_drawdown_pct']:.1f}%")
        print(f"Sharpe Ratio: {results['sharpe']['sharpe_ratio']:.2f}")
        print(f"Volatility Regime: {results['volatility']['regime']}")
        print(f"\nMetrics saved to {args.output}")

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
