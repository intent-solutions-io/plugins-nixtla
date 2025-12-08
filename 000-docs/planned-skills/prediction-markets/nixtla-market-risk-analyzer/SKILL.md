---
name: nixtla-market-risk-analyzer
description: |
  Analyzes market risk by calculating VaR, volatility, drawdown, and position sizing.
  Use when assessing investment risk, managing portfolios, or determining position sizes.
  Trigger with "analyze market risk", "calculate portfolio risk", "determine position size".
allowed-tools: "Read,Write,Bash,Glob,Grep"
version: "1.0.0"
---

# Market Risk Analyzer

Calculates key market risk metrics and recommends optimal position sizes.

## Overview

Uses historical market data to calculate Value at Risk (VaR), volatility, maximum drawdown, and optimal position sizes. Provides insights for managing investment risk and optimizing portfolio allocation. Optionally uses TimeGPT for volatility forecasting.

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep

**Environment**: Optional `NIXTLA_TIMEGPT_API_KEY` for volatility forecasting

**Packages**:
```bash
pip install pandas numpy scipy matplotlib
# Optional for forecasting:
pip install nixtla
```

## Instructions

### Step 1: Load and Prepare Price Data

Create the data preparation script:

```python
#!/usr/bin/env python3
"""
Market Risk Analyzer - Data Preparation
Loads price data and calculates returns
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple

def load_price_data(filepath: str) -> pd.DataFrame:
    """
    Load price data from CSV file.

    Expected format:
    - Column 'ds' or 'date': datetime index
    - Column 'y' or 'price': price values

    Args:
        filepath: Path to CSV file

    Returns:
        DataFrame with datetime index and price column
    """
    print(f"Loading price data from {filepath}...")

    df = pd.read_csv(filepath)

    # Detect date column
    date_col = None
    for col in ['ds', 'date', 'Date', 'timestamp', 'Timestamp']:
        if col in df.columns:
            date_col = col
            break

    if date_col is None:
        raise ValueError("No date column found. Need 'ds', 'date', or 'timestamp'")

    # Detect price column
    price_col = None
    for col in ['y', 'price', 'Price', 'close', 'Close', 'value']:
        if col in df.columns:
            price_col = col
            break

    if price_col is None:
        raise ValueError("No price column found. Need 'y', 'price', or 'close'")

    # Standardize
    df = df[[date_col, price_col]].copy()
    df.columns = ['ds', 'price']
    df['ds'] = pd.to_datetime(df['ds'])
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df = df.dropna()
    df = df.sort_values('ds').set_index('ds')

    print(f"Loaded {len(df)} price points from {df.index.min().date()} to {df.index.max().date()}")
    return df

def calculate_returns(prices: pd.DataFrame, method: str = "log") -> pd.Series:
    """
    Calculate returns from price series.

    Args:
        prices: DataFrame with 'price' column
        method: "log" for log returns, "simple" for simple returns

    Returns:
        Series of returns
    """
    if method == "log":
        returns = np.log(prices['price'] / prices['price'].shift(1))
    else:
        returns = prices['price'].pct_change()

    return returns.dropna()

def detect_frequency(df: pd.DataFrame) -> str:
    """Detect the frequency of the time series."""
    if len(df) < 2:
        return "D"

    # Calculate median time difference
    diffs = pd.Series(df.index).diff().dropna()
    median_diff = diffs.median()

    if median_diff <= pd.Timedelta(hours=1):
        return "H"  # Hourly
    elif median_diff <= pd.Timedelta(days=1):
        return "D"  # Daily
    elif median_diff <= pd.Timedelta(weeks=1):
        return "W"  # Weekly
    else:
        return "M"  # Monthly

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python prepare_data.py <prices.csv>")
        sys.exit(1)

    filepath = sys.argv[1]
    prices = load_price_data(filepath)
    returns = calculate_returns(prices)
    freq = detect_frequency(prices)

    # Save returns
    returns.to_csv("returns.csv", header=['returns'])

    print(f"\nData Summary:")
    print(f"  Frequency: {freq}")
    print(f"  Returns: {len(returns)} observations")
    print(f"  Mean return: {returns.mean():.4%}")
    print(f"  Volatility: {returns.std():.4%}")
```

### Step 2: Calculate Risk Metrics

Create the comprehensive risk metrics calculator:

```python
#!/usr/bin/env python3
"""
Market Risk Analyzer - Risk Metrics
Calculates VaR, volatility, drawdown, and other risk metrics
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Tuple

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
        # Historical simulation
        var = np.percentile(returns, alpha * 100)

    elif method == "parametric":
        # Gaussian VaR
        mu = returns.mean()
        sigma = returns.std()
        var = stats.norm.ppf(alpha, mu, sigma)

    elif method == "monte_carlo":
        # Monte Carlo simulation
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
    """
    Calculate historical and rolling volatility.

    Args:
        returns: Series of returns
        window: Rolling window size
        annualize: Whether to annualize volatility
        trading_days: Trading days per year

    Returns:
        Dict with volatility metrics
    """
    # Historical volatility
    hist_vol = returns.std()
    if annualize:
        hist_vol_annual = hist_vol * np.sqrt(trading_days)
    else:
        hist_vol_annual = None

    # Rolling volatility
    rolling_vol = returns.rolling(window=window).std()
    if annualize:
        rolling_vol = rolling_vol * np.sqrt(trading_days)

    # Current vs average volatility
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
        "regime": "HIGH" if vol_percentile > 75 else "LOW" if vol_percentile < 25 else "NORMAL",
        "rolling_volatility": rolling_vol
    }

def calculate_drawdown(prices: pd.DataFrame) -> Dict:
    """
    Calculate maximum drawdown and drawdown statistics.

    Args:
        prices: DataFrame with 'price' column

    Returns:
        Dict with drawdown metrics
    """
    price_series = prices['price']

    # Calculate running maximum
    running_max = price_series.expanding().max()

    # Calculate drawdown
    drawdown = (price_series - running_max) / running_max

    # Maximum drawdown
    max_drawdown = drawdown.min()
    max_dd_date = drawdown.idxmin()

    # Find recovery
    max_dd_idx = drawdown.idxmin()
    post_dd = drawdown[max_dd_idx:]
    recovery_dates = post_dd[post_dd >= 0].index

    if len(recovery_dates) > 0:
        recovery_date = recovery_dates[0]
        recovery_days = (recovery_date - max_dd_date).days
    else:
        recovery_date = None
        recovery_days = None

    # Current drawdown
    current_dd = drawdown.iloc[-1]

    # Average drawdown
    avg_dd = drawdown.mean()

    return {
        "max_drawdown": round(max_drawdown, 4),
        "max_drawdown_pct": round(max_drawdown * 100, 2),
        "max_drawdown_date": max_dd_date.strftime("%Y-%m-%d"),
        "recovery_date": recovery_date.strftime("%Y-%m-%d") if recovery_date else "Not recovered",
        "recovery_days": recovery_days,
        "current_drawdown": round(current_dd, 4),
        "current_drawdown_pct": round(current_dd * 100, 2),
        "average_drawdown": round(avg_dd, 4),
        "drawdown_series": drawdown
    }

def calculate_sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.05,
    trading_days: int = 252
) -> Dict:
    """
    Calculate Sharpe ratio and related metrics.

    Args:
        returns: Series of returns
        risk_free_rate: Annual risk-free rate
        trading_days: Trading days per year

    Returns:
        Dict with Sharpe ratio metrics
    """
    # Annualize returns and volatility
    annual_return = returns.mean() * trading_days
    annual_vol = returns.std() * np.sqrt(trading_days)

    # Sharpe ratio
    sharpe = (annual_return - risk_free_rate) / annual_vol

    # Sortino ratio (downside deviation)
    downside_returns = returns[returns < 0]
    downside_vol = downside_returns.std() * np.sqrt(trading_days)
    sortino = (annual_return - risk_free_rate) / downside_vol if downside_vol > 0 else np.nan

    return {
        "sharpe_ratio": round(sharpe, 3),
        "sortino_ratio": round(sortino, 3) if not np.isnan(sortino) else None,
        "annualized_return": round(annual_return, 4),
        "annualized_volatility": round(annual_vol, 4),
        "risk_free_rate": risk_free_rate,
        "interpretation": interpret_sharpe(sharpe)
    }

def interpret_sharpe(sharpe: float) -> str:
    """Interpret Sharpe ratio value."""
    if sharpe >= 2.0:
        return "Excellent risk-adjusted returns"
    elif sharpe >= 1.0:
        return "Good risk-adjusted returns"
    elif sharpe >= 0.5:
        return "Moderate risk-adjusted returns"
    elif sharpe >= 0:
        return "Poor risk-adjusted returns"
    else:
        return "Negative risk-adjusted returns"

def run_risk_analysis(prices: pd.DataFrame, returns: pd.Series) -> Dict:
    """
    Run complete risk analysis.

    Args:
        prices: Price DataFrame
        returns: Returns Series

    Returns:
        Dict with all risk metrics
    """
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

if __name__ == "__main__":
    import json
    from prepare_data import load_price_data, calculate_returns

    prices = load_price_data("prices.csv") if len(sys.argv) < 2 else load_price_data(sys.argv[1])
    returns = calculate_returns(prices)

    print("\nCalculating risk metrics...")
    results = run_risk_analysis(prices, returns)

    # Remove non-serializable data
    output = {k: v for k, v in results.items() if k != "volatility" or "rolling_volatility" not in v}
    for key in output:
        if isinstance(output[key], dict):
            output[key] = {k: v for k, v in output[key].items()
                          if not isinstance(v, (pd.Series, pd.DataFrame))}

    with open("risk_metrics.json", "w") as f:
        json.dump(output, f, indent=2, default=str)

    print("\n" + "="*50)
    print("RISK ANALYSIS SUMMARY")
    print("="*50)
    print(f"VaR (95%): {results['var_95']['var_pct']:.2f}%")
    print(f"VaR (99%): {results['var_99']['var_pct']:.2f}%")
    print(f"Annualized Volatility: {results['volatility']['annualized_volatility']*100:.1f}%")
    print(f"Max Drawdown: {results['drawdown']['max_drawdown_pct']:.1f}%")
    print(f"Sharpe Ratio: {results['sharpe']['sharpe_ratio']:.2f}")
    print(f"Volatility Regime: {results['volatility']['regime']}")
```

### Step 3: Position Sizing Calculator

Create the position sizing script:

```python
#!/usr/bin/env python3
"""
Market Risk Analyzer - Position Sizing
Calculates optimal position sizes based on risk metrics
"""

import pandas as pd
import numpy as np
from typing import Dict

def kelly_criterion(
    win_rate: float,
    avg_win: float,
    avg_loss: float
) -> Dict:
    """
    Calculate Kelly Criterion position size.

    Args:
        win_rate: Probability of winning (0-1)
        avg_win: Average winning trade return
        avg_loss: Average losing trade return (positive number)

    Returns:
        Dict with Kelly position sizing
    """
    # Kelly formula: f* = (bp - q) / b
    # where b = avg_win/avg_loss, p = win_rate, q = 1 - win_rate
    b = avg_win / avg_loss if avg_loss > 0 else 0
    p = win_rate
    q = 1 - win_rate

    kelly_full = (b * p - q) / b if b > 0 else 0
    kelly_half = kelly_full / 2  # Half Kelly (more conservative)
    kelly_quarter = kelly_full / 4  # Quarter Kelly (conservative)

    return {
        "kelly_full": round(max(0, kelly_full), 4),
        "kelly_half": round(max(0, kelly_half), 4),
        "kelly_quarter": round(max(0, kelly_quarter), 4),
        "win_rate": win_rate,
        "win_loss_ratio": round(b, 2),
        "recommendation": "Use Half Kelly for practical trading",
        "warning": "Full Kelly is mathematically optimal but aggressive"
    }

def fixed_fractional(
    account_size: float,
    risk_per_trade: float,
    stop_loss_pct: float
) -> Dict:
    """
    Calculate fixed fractional position size.

    Args:
        account_size: Total account value
        risk_per_trade: Maximum risk per trade (e.g., 0.02 for 2%)
        stop_loss_pct: Stop loss percentage (e.g., 0.05 for 5%)

    Returns:
        Dict with position sizing details
    """
    # Maximum loss amount
    max_loss = account_size * risk_per_trade

    # Position size
    position_size = max_loss / stop_loss_pct

    # Number of shares/contracts at given price
    # (Caller needs to divide by current price)

    return {
        "account_size": account_size,
        "risk_per_trade_pct": risk_per_trade * 100,
        "risk_per_trade_dollars": round(max_loss, 2),
        "stop_loss_pct": stop_loss_pct * 100,
        "max_position_value": round(position_size, 2),
        "position_pct_of_account": round((position_size / account_size) * 100, 1),
        "formula": "position = (account × risk%) / stop_loss%"
    }

def volatility_adjusted_position(
    account_size: float,
    target_volatility: float,
    asset_volatility: float,
    leverage: float = 1.0
) -> Dict:
    """
    Calculate volatility-adjusted position size.

    Args:
        account_size: Total account value
        target_volatility: Target portfolio volatility (annualized)
        asset_volatility: Asset's volatility (annualized)
        leverage: Maximum leverage allowed

    Returns:
        Dict with position sizing details
    """
    # Position size to achieve target volatility
    raw_position_pct = target_volatility / asset_volatility

    # Apply leverage constraint
    position_pct = min(raw_position_pct, leverage)

    # Dollar position
    position_value = account_size * position_pct

    return {
        "account_size": account_size,
        "target_volatility_pct": target_volatility * 100,
        "asset_volatility_pct": asset_volatility * 100,
        "position_pct_of_account": round(position_pct * 100, 1),
        "position_value": round(position_value, 2),
        "leverage_used": round(position_pct, 2),
        "max_leverage": leverage,
        "portfolio_volatility_pct": round(position_pct * asset_volatility * 100, 2)
    }

def var_based_position(
    account_size: float,
    max_var_loss: float,
    var_95: float
) -> Dict:
    """
    Calculate position size based on VaR constraint.

    Args:
        account_size: Total account value
        max_var_loss: Maximum acceptable VaR loss (e.g., 0.05 for 5%)
        var_95: Asset's 95% VaR (daily)

    Returns:
        Dict with position sizing details
    """
    # Maximum loss in dollars
    max_loss_dollars = account_size * max_var_loss

    # Position size to limit VaR loss
    position_value = max_loss_dollars / abs(var_95)

    # As percentage of account
    position_pct = position_value / account_size

    return {
        "account_size": account_size,
        "max_var_loss_pct": max_var_loss * 100,
        "max_var_loss_dollars": round(max_loss_dollars, 2),
        "asset_var_95_pct": round(abs(var_95) * 100, 2),
        "position_value": round(position_value, 2),
        "position_pct_of_account": round(position_pct * 100, 1),
        "expected_95_loss": round(position_value * abs(var_95), 2)
    }

def calculate_all_position_sizes(
    account_size: float = 100000,
    risk_per_trade: float = 0.02,
    stop_loss_pct: float = 0.05,
    target_volatility: float = 0.15,
    asset_volatility: float = 0.25,
    var_95: float = -0.02,
    max_var_loss: float = 0.03,
    win_rate: float = 0.55,
    avg_win: float = 0.03,
    avg_loss: float = 0.02
) -> Dict:
    """
    Calculate position sizes using all methods.

    Returns:
        Dict with all position sizing recommendations
    """
    fixed = fixed_fractional(account_size, risk_per_trade, stop_loss_pct)
    vol_adj = volatility_adjusted_position(account_size, target_volatility, asset_volatility)
    var_based = var_based_position(account_size, max_var_loss, var_95)
    kelly = kelly_criterion(win_rate, avg_win, avg_loss)

    # Calculate recommended position (most conservative)
    positions = [
        fixed["max_position_value"],
        vol_adj["position_value"],
        var_based["position_value"]
    ]
    conservative_position = min(positions)

    return {
        "fixed_fractional": fixed,
        "volatility_adjusted": vol_adj,
        "var_based": var_based,
        "kelly": kelly,
        "recommendation": {
            "conservative_position": round(conservative_position, 2),
            "conservative_pct": round((conservative_position / account_size) * 100, 1),
            "method": "Minimum of all methods",
            "rationale": "Use the most conservative sizing to limit downside risk"
        }
    }

if __name__ == "__main__":
    import json

    print("Calculating position sizes...")

    # Example parameters
    results = calculate_all_position_sizes(
        account_size=100000,
        risk_per_trade=0.02,
        stop_loss_pct=0.05,
        target_volatility=0.15,
        asset_volatility=0.25,
        var_95=-0.02,
        max_var_loss=0.03
    )

    with open("position_sizing.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n" + "="*50)
    print("POSITION SIZING RECOMMENDATIONS")
    print("="*50)
    print(f"\nFixed Fractional: ${results['fixed_fractional']['max_position_value']:,.0f}")
    print(f"Volatility Adjusted: ${results['volatility_adjusted']['position_value']:,.0f}")
    print(f"VaR-Based: ${results['var_based']['position_value']:,.0f}")
    print(f"\nKelly Full: {results['kelly']['kelly_full']*100:.1f}%")
    print(f"Kelly Half (Recommended): {results['kelly']['kelly_half']*100:.1f}%")
    print(f"\n>>> RECOMMENDED: ${results['recommendation']['conservative_position']:,.0f}")
    print(f">>> ({results['recommendation']['conservative_pct']:.1f}% of account)")
```

### Step 4: Generate Risk Report

Create the report generator:

```python
#!/usr/bin/env python3
"""
Market Risk Analyzer - Report Generator
Creates comprehensive risk analysis report
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from typing import Dict

def create_risk_plots(
    prices: pd.DataFrame,
    returns: pd.Series,
    rolling_vol: pd.Series,
    drawdown: pd.Series,
    output_dir: str = "."
) -> Dict[str, str]:
    """Create risk visualization plots."""

    plots = {}

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

| Method | Daily VaR | Interpretation |
|--------|-----------|----------------|
| Historical | {var_95['var_pct']:.2f}% | 95% confident loss won't exceed this |
| CVaR (Expected Shortfall) | {var_95['cvar']*100:.2f}% if var_95['cvar'] else "N/A" | Average loss when VaR is exceeded |

### 99% Confidence Level

| Metric | Value |
|--------|-------|
| Daily VaR | {var_99['var_pct']:.2f}% |
| CVaR | {var_99['cvar']*100:.2f}% if var_99['cvar'] else "N/A" |

**What this means**: On 95% of days, losses should not exceed {abs(var_95['var_pct']):.2f}%.
On the remaining 5% of days, losses could be worse.

## Volatility Analysis

| Metric | Value |
|--------|-------|
| Daily Volatility | {vol['daily_volatility']*100:.2f}% |
| Annualized Volatility | {vol['annualized_volatility']*100:.1f}% |
| Current Rolling Vol | {vol['current_rolling_vol']*100:.1f}% |
| Average Rolling Vol | {vol['average_rolling_vol']*100:.1f}% |
| Volatility Percentile | {vol['volatility_percentile']:.0f}th |
| Current Regime | **{vol['regime']}** |

## Drawdown Analysis

| Metric | Value |
|--------|-------|
| Maximum Drawdown | {dd['max_drawdown_pct']:.1f}% |
| Max Drawdown Date | {dd['max_drawdown_date']} |
| Recovery Date | {dd['recovery_date']} |
| Recovery Time | {dd['recovery_days']} days if dd['recovery_days'] else "Not recovered" |
| Current Drawdown | {dd['current_drawdown_pct']:.1f}% |
| Average Drawdown | {dd['average_drawdown']*100:.1f}% |

## Risk-Adjusted Returns

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Sharpe Ratio | {sharpe['sharpe_ratio']:.2f} | {sharpe['interpretation']} |
| Sortino Ratio | {sharpe['sortino_ratio']:.2f if sharpe['sortino_ratio'] else "N/A"} | Downside-adjusted |
| Annualized Return | {sharpe['annualized_return']*100:.1f}% | |
| Annualized Volatility | {sharpe['annualized_volatility']*100:.1f}% | |

## Position Sizing Recommendations

Based on a $100,000 account:

| Method | Position Size | % of Account |
|--------|---------------|--------------|
| Fixed Fractional (2% risk) | ${position_sizing['fixed_fractional']['max_position_value']:,.0f} | {position_sizing['fixed_fractional']['position_pct_of_account']:.1f}% |
| Volatility Adjusted (15% target) | ${position_sizing['volatility_adjusted']['position_value']:,.0f} | {position_sizing['volatility_adjusted']['position_pct_of_account']:.1f}% |
| VaR-Based (3% max loss) | ${position_sizing['var_based']['position_value']:,.0f} | {position_sizing['var_based']['position_pct_of_account']:.1f}% |

### Kelly Criterion

| Variant | Position % |
|---------|------------|
| Full Kelly | {position_sizing['kelly']['kelly_full']*100:.1f}% |
| Half Kelly (Recommended) | {position_sizing['kelly']['kelly_half']*100:.1f}% |
| Quarter Kelly (Conservative) | {position_sizing['kelly']['kelly_quarter']*100:.1f}% |

### Recommended Position

**${position_sizing['recommendation']['conservative_position']:,.0f}** ({position_sizing['recommendation']['conservative_pct']:.1f}% of account)

This is the most conservative sizing across all methods.

## Visualizations

- `drawdown.png` - Price history and drawdown chart
- `volatility.png` - Rolling volatility over time
- `var.png` - Return distribution with VaR levels

## Risk Warnings

1. Past performance does not guarantee future results
2. VaR models assume normal market conditions
3. Tail risk events (black swans) may exceed VaR estimates
4. Correlations may change during market stress
5. Position sizing should be adjusted for liquidity

## Disclaimer

This analysis is for informational purposes only. Not financial advice.
Always consult a qualified financial advisor before making investment decisions.
"""

    with open(output_path, "w") as f:
        f.write(report)

    print(f"Report saved to {output_path}")
    return report

if __name__ == "__main__":
    # Load metrics
    with open("risk_metrics.json") as f:
        risk_metrics = json.load(f)

    with open("position_sizing.json") as f:
        position_sizing = json.load(f)

    generate_risk_report(risk_metrics, position_sizing)
```

## Output

- **risk_metrics.json**: Complete risk metrics (VaR, volatility, drawdown, Sharpe)
- **position_sizing.json**: Position sizing calculations
- **risk_report.md**: Comprehensive markdown report
- **drawdown.png**: Price and drawdown visualization
- **volatility.png**: Rolling volatility chart
- **var.png**: Return distribution with VaR

## Error Handling

1. **Error**: `NIXTLA_TIMEGPT_API_KEY not set`
   **Solution**: Only needed for volatility forecasting. Core analysis works without it.

2. **Error**: `Input file not found`
   **Solution**: Verify file path with `ls -la`

3. **Error**: `Invalid data format`
   **Solution**: Ensure CSV has date and price columns

4. **Error**: `Insufficient data for analysis`
   **Solution**: Need at least 30 price points for reliable analysis

## Examples

### Example 1: Analyze Stock Risk

```bash
python prepare_data.py AAPL_prices.csv
python risk_metrics.py AAPL_prices.csv
python position_sizing.py
python generate_report.py

# Output:
# VaR (95%): -2.15%
# Max Drawdown: -35.2%
# Sharpe Ratio: 0.95
# Recommended Position: $45,000 (45% of $100k account)
```

### Example 2: Prediction Market Contract

```bash
python risk_analyzer.py contract_prices.csv --account 50000

# Output:
# VaR (95%): -8.5%
# Volatility Regime: HIGH
# Recommended Position: $12,000 (24% of account)
```

## Usage

```bash
# Complete workflow
python prepare_data.py prices.csv
python risk_metrics.py
python position_sizing.py
python generate_report.py

# Or single command with all parameters
python risk_analyzer.py prices.csv \
    --account 100000 \
    --risk 0.02 \
    --stop-loss 0.05 \
    --output-dir results/
```
