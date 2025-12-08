#!/usr/bin/env python3
"""
Kalshi Data Fetcher
Fetches current market prices from Kalshi API
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Optional

KALSHI_API = "https://trading-api.kalshi.com/trade-api/v2"

def fetch_kalshi_markets() -> List[Dict]:
    """Fetch all active markets from Kalshi."""
    try:
        response = requests.get(
            f"{KALSHI_API}/markets",
            params={"status": "open"},
            timeout=30
        )
        response.raise_for_status()
        return response.json().get("markets", [])
    except requests.RequestException as e:
        print(f"Error fetching Kalshi data: {e}")
        return []

def get_kalshi_data() -> List[Dict]:
    """
    Fetch and structure Kalshi data for arbitrage analysis.

    Returns:
        List of dicts with: event_name, yes_price, no_price, ticker
    """
    markets = fetch_kalshi_markets()
    results = []

    for market in markets[:50]:  # Limit to avoid rate limits
        ticker = market.get("ticker")
        if not ticker:
            continue

        # Kalshi prices are in cents (0-100)
        yes_bid = market.get("yes_bid", 0) / 100
        yes_ask = market.get("yes_ask", 0) / 100
        no_bid = market.get("no_bid", 0) / 100
        no_ask = market.get("no_ask", 0) / 100

        results.append({
            "platform": "Kalshi",
            "event_name": market.get("title", "Unknown"),
            "ticker": ticker,
            "yes_price": (yes_bid + yes_ask) / 2 if yes_bid and yes_ask else 0,
            "no_price": (no_bid + no_ask) / 2 if no_bid and no_ask else 0,
            "yes_bid": yes_bid,
            "yes_ask": yes_ask,
            "no_bid": no_bid,
            "no_ask": no_ask,
            "volume": market.get("volume", 0),
            "fetched_at": datetime.now().isoformat()
        })

    return results

if __name__ == "__main__":
    print("Fetching Kalshi data...")
    data = get_kalshi_data()

    with open("kalshi_data.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved {len(data)} markets to kalshi_data.json")
