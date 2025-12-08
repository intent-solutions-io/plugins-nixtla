#!/usr/bin/env python3
"""
Arbitrage Detector
Compares Polymarket and Kalshi prices to find arbitrage opportunities
"""

import json
import pandas as pd
from typing import Dict, List, Tuple
from difflib import SequenceMatcher

# Fee structures (approximate)
POLYMARKET_FEE = 0.02  # 2% trading fee
KALSHI_FEE = 0.01      # 1% trading fee

def load_market_data() -> Tuple[List[Dict], List[Dict]]:
    """Load market data from JSON files."""
    with open("polymarket_data.json", "r") as f:
        polymarket = json.load(f)
    with open("kalshi_data.json", "r") as f:
        kalshi = json.load(f)
    return polymarket, kalshi

def normalize_event_name(name: str) -> str:
    """Normalize event name for matching."""
    return name.lower().strip().replace("?", "").replace("!", "")

def find_matching_events(poly_markets: List[Dict], kalshi_markets: List[Dict]) -> List[Dict]:
    """
    Find matching events across platforms using fuzzy string matching.

    Returns:
        List of matched event pairs
    """
    matches = []

    for poly in poly_markets:
        poly_name = normalize_event_name(poly["event_name"])

        for kalshi in kalshi_markets:
            kalshi_name = normalize_event_name(kalshi["event_name"])

            # Calculate similarity score
            similarity = SequenceMatcher(None, poly_name, kalshi_name).ratio()

            if similarity > 0.7:  # 70% similarity threshold
                matches.append({
                    "polymarket": poly,
                    "kalshi": kalshi,
                    "similarity": similarity,
                    "event_name": poly["event_name"]
                })

    return matches

def calculate_arbitrage(poly_yes: float, poly_no: float,
                        kalshi_yes: float, kalshi_no: float) -> List[Dict]:
    """
    Calculate arbitrage opportunity between two platforms.

    Arbitrage exists when:
    - Buy YES on platform A + Buy NO on platform B < 1.0 (guaranteed profit)
    - Or price discrepancy allows profitable round-trip

    Returns:
        List of arbitrage opportunities
    """
    opportunities = []

    # Strategy 1: Buy Polymarket YES, Buy Kalshi NO
    cost_1 = poly_yes * (1 + POLYMARKET_FEE) + kalshi_no * (1 + KALSHI_FEE)
    if cost_1 < 1.0:
        profit_1 = 1.0 - cost_1
        opportunities.append({
            "strategy": "Buy Polymarket YES + Kalshi NO",
            "cost": cost_1,
            "guaranteed_return": 1.0,
            "profit": profit_1,
            "profit_pct": (profit_1 / cost_1) * 100
        })

    # Strategy 2: Buy Polymarket NO, Buy Kalshi YES
    cost_2 = poly_no * (1 + POLYMARKET_FEE) + kalshi_yes * (1 + KALSHI_FEE)
    if cost_2 < 1.0:
        profit_2 = 1.0 - cost_2
        opportunities.append({
            "strategy": "Buy Polymarket NO + Kalshi YES",
            "cost": cost_2,
            "guaranteed_return": 1.0,
            "profit": profit_2,
            "profit_pct": (profit_2 / cost_2) * 100
        })

    # Strategy 3: Price discrepancy (buy low, sell high same outcome)
    if poly_yes < kalshi_yes * (1 - KALSHI_FEE - POLYMARKET_FEE):
        profit_3 = kalshi_yes - poly_yes - (poly_yes * POLYMARKET_FEE) - (kalshi_yes * KALSHI_FEE)
        if profit_3 > 0:
            opportunities.append({
                "strategy": "Buy Polymarket YES, Sell Kalshi YES",
                "buy_price": poly_yes,
                "sell_price": kalshi_yes,
                "profit": profit_3,
                "profit_pct": (profit_3 / poly_yes) * 100
            })

    if kalshi_yes < poly_yes * (1 - KALSHI_FEE - POLYMARKET_FEE):
        profit_4 = poly_yes - kalshi_yes - (kalshi_yes * KALSHI_FEE) - (poly_yes * POLYMARKET_FEE)
        if profit_4 > 0:
            opportunities.append({
                "strategy": "Buy Kalshi YES, Sell Polymarket YES",
                "buy_price": kalshi_yes,
                "sell_price": poly_yes,
                "profit": profit_4,
                "profit_pct": (profit_4 / kalshi_yes) * 100
            })

    return opportunities

def detect_arbitrage() -> pd.DataFrame:
    """
    Main function to detect all arbitrage opportunities.

    Returns:
        DataFrame with arbitrage opportunities sorted by profit
    """
    polymarket, kalshi = load_market_data()
    matches = find_matching_events(polymarket, kalshi)

    all_opportunities = []

    for match in matches:
        poly = match["polymarket"]
        kal = match["kalshi"]

        opportunities = calculate_arbitrage(
            poly["yes_price"], poly["no_price"],
            kal["yes_price"], kal["no_price"]
        )

        for opp in opportunities:
            opp["event_name"] = match["event_name"]
            opp["match_similarity"] = match["similarity"]
            opp["polymarket_yes"] = poly["yes_price"]
            opp["polymarket_no"] = poly["no_price"]
            opp["kalshi_yes"] = kal["yes_price"]
            opp["kalshi_no"] = kal["no_price"]
            all_opportunities.append(opp)

    if not all_opportunities:
        print("No arbitrage opportunities found.")
        return pd.DataFrame()

    df = pd.DataFrame(all_opportunities)
    df = df.sort_values("profit_pct", ascending=False)

    return df

if __name__ == "__main__":
    print("Analyzing arbitrage opportunities...")

    opportunities = detect_arbitrage()

    if not opportunities.empty:
        # Save to CSV
        opportunities.to_csv("arbitrage_opportunities.csv", index=False)
        print(f"\nFound {len(opportunities)} opportunities!")
        print(f"Saved to arbitrage_opportunities.csv")

        # Display top opportunities
        print("\n=== TOP ARBITRAGE OPPORTUNITIES ===\n")
        for _, row in opportunities.head(5).iterrows():
            print(f"Event: {row['event_name'][:50]}...")
            print(f"Strategy: {row['strategy']}")
            print(f"Profit: ${row['profit']:.4f} ({row['profit_pct']:.2f}%)")
            print(f"Polymarket: YES={row['polymarket_yes']:.2f}, NO={row['polymarket_no']:.2f}")
            print(f"Kalshi: YES={row['kalshi_yes']:.2f}, NO={row['kalshi_no']:.2f}")
            print("-" * 50)
    else:
        print("No profitable arbitrage opportunities found at this time.")
