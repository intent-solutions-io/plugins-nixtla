#!/usr/bin/env python3
"""
Market Risk Analyzer - Position Sizing
Calculates optimal position sizes based on risk metrics
"""

import argparse
import json
import sys
from typing import Dict


def kelly_criterion(win_rate: float, avg_win: float, avg_loss: float) -> Dict:
    """
    Calculate Kelly Criterion position size.

    Args:
        win_rate: Probability of winning (0-1)
        avg_win: Average winning trade return
        avg_loss: Average losing trade return (positive number)

    Returns:
        Dict with Kelly position sizing
    """
    b = avg_win / avg_loss if avg_loss > 0 else 0
    p = win_rate
    q = 1 - win_rate

    kelly_full = (b * p - q) / b if b > 0 else 0
    kelly_half = kelly_full / 2
    kelly_quarter = kelly_full / 4

    return {
        "kelly_full": round(max(0, kelly_full), 4),
        "kelly_half": round(max(0, kelly_half), 4),
        "kelly_quarter": round(max(0, kelly_quarter), 4),
        "win_rate": win_rate,
        "win_loss_ratio": round(b, 2),
        "recommendation": "Use Half Kelly for practical trading",
        "warning": "Full Kelly is mathematically optimal but aggressive",
    }


def fixed_fractional(account_size: float, risk_per_trade: float, stop_loss_pct: float) -> Dict:
    """
    Calculate fixed fractional position size.

    Args:
        account_size: Total account value
        risk_per_trade: Maximum risk per trade (e.g., 0.02 for 2%)
        stop_loss_pct: Stop loss percentage (e.g., 0.05 for 5%)

    Returns:
        Dict with position sizing details
    """
    max_loss = account_size * risk_per_trade
    position_size = max_loss / stop_loss_pct

    return {
        "account_size": account_size,
        "risk_per_trade_pct": risk_per_trade * 100,
        "risk_per_trade_dollars": round(max_loss, 2),
        "stop_loss_pct": stop_loss_pct * 100,
        "max_position_value": round(position_size, 2),
        "position_pct_of_account": round((position_size / account_size) * 100, 1),
        "formula": "position = (account × risk%) / stop_loss%",
    }


def volatility_adjusted_position(
    account_size: float, target_volatility: float, asset_volatility: float, leverage: float = 1.0
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
    raw_position_pct = target_volatility / asset_volatility
    position_pct = min(raw_position_pct, leverage)
    position_value = account_size * position_pct

    return {
        "account_size": account_size,
        "target_volatility_pct": target_volatility * 100,
        "asset_volatility_pct": asset_volatility * 100,
        "position_pct_of_account": round(position_pct * 100, 1),
        "position_value": round(position_value, 2),
        "leverage_used": round(position_pct, 2),
        "max_leverage": leverage,
        "portfolio_volatility_pct": round(position_pct * asset_volatility * 100, 2),
    }


def var_based_position(account_size: float, max_var_loss: float, var_95: float) -> Dict:
    """
    Calculate position size based on VaR constraint.

    Args:
        account_size: Total account value
        max_var_loss: Maximum acceptable VaR loss (e.g., 0.05 for 5%)
        var_95: Asset's 95% VaR (daily)

    Returns:
        Dict with position sizing details
    """
    max_loss_dollars = account_size * max_var_loss
    position_value = max_loss_dollars / abs(var_95)
    position_pct = position_value / account_size

    return {
        "account_size": account_size,
        "max_var_loss_pct": max_var_loss * 100,
        "max_var_loss_dollars": round(max_loss_dollars, 2),
        "asset_var_95_pct": round(abs(var_95) * 100, 2),
        "position_value": round(position_value, 2),
        "position_pct_of_account": round(position_pct * 100, 1),
        "expected_95_loss": round(position_value * abs(var_95), 2),
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
    avg_loss: float = 0.02,
) -> Dict:
    """Calculate position sizes using all methods."""
    fixed = fixed_fractional(account_size, risk_per_trade, stop_loss_pct)
    vol_adj = volatility_adjusted_position(account_size, target_volatility, asset_volatility)
    var_based = var_based_position(account_size, max_var_loss, var_95)
    kelly = kelly_criterion(win_rate, avg_win, avg_loss)

    positions = [
        fixed["max_position_value"],
        vol_adj["position_value"],
        var_based["position_value"],
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
            "rationale": "Use the most conservative sizing to limit downside risk",
        },
    }


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Calculate optimal position sizes")
    parser.add_argument(
        "--account-size",
        type=float,
        default=100000,
        help="Account size in dollars (default: 100000)",
    )
    parser.add_argument(
        "--risk-per-trade",
        type=float,
        default=0.02,
        help="Risk per trade as decimal (default: 0.02 = 2%%)",
    )
    parser.add_argument(
        "--stop-loss",
        type=float,
        default=0.05,
        help="Stop loss percentage as decimal (default: 0.05 = 5%%)",
    )
    parser.add_argument(
        "--target-volatility",
        type=float,
        default=0.15,
        help="Target portfolio volatility (default: 0.15 = 15%%)",
    )
    parser.add_argument(
        "--asset-volatility",
        type=float,
        default=0.25,
        help="Asset volatility (default: 0.25 = 25%%)",
    )
    parser.add_argument(
        "--var-95",
        type=float,
        default=-0.02,
        help="Asset 95%% VaR as decimal (default: -0.02 = -2%%)",
    )
    parser.add_argument(
        "--max-var-loss",
        type=float,
        default=0.03,
        help="Maximum acceptable VaR loss (default: 0.03 = 3%%)",
    )
    parser.add_argument(
        "--output",
        default="position_sizing.json",
        help="Output file (default: position_sizing.json)",
    )

    args = parser.parse_args()

    try:
        print("Calculating position sizes...")

        results = calculate_all_position_sizes(
            account_size=args.account_size,
            risk_per_trade=args.risk_per_trade,
            stop_loss_pct=args.stop_loss,
            target_volatility=args.target_volatility,
            asset_volatility=args.asset_volatility,
            var_95=args.var_95,
            max_var_loss=args.max_var_loss,
        )

        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)

        print("\n" + "=" * 50)
        print("POSITION SIZING RECOMMENDATIONS")
        print("=" * 50)
        print(f"\nFixed Fractional: ${results['fixed_fractional']['max_position_value']:,.0f}")
        print(f"Volatility Adjusted: ${results['volatility_adjusted']['position_value']:,.0f}")
        print(f"VaR-Based: ${results['var_based']['position_value']:,.0f}")
        print(f"\nKelly Full: {results['kelly']['kelly_full']*100:.1f}%")
        print(f"Kelly Half (Recommended): {results['kelly']['kelly_half']*100:.1f}%")
        print(f"\n>>> RECOMMENDED: ${results['recommendation']['conservative_position']:,.0f}")
        print(f">>> ({results['recommendation']['conservative_pct']:.1f}% of account)")
        print(f"\nResults saved to {args.output}")

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
