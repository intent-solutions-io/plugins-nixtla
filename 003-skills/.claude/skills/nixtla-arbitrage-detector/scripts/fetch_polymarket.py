#!/usr/bin/env python3
"""
Polymarket Data Fetcher
Fetches current market prices from Polymarket CLOB API
"""

import json
from datetime import datetime
from typing import Dict, List, Optional

import requests

POLYMARKET_API = "https://clob.polymarket.com"


def fetch_polymarket_markets() -> List[Dict]:
    """Fetch all active markets from Polymarket."""
    try:
        response = requests.get(f"{POLYMARKET_API}/markets", params={"active": "true"}, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching Polymarket data: {e}")
        return []


def fetch_polymarket_prices(condition_id: str) -> Optional[Dict]:
    """Fetch current prices for a specific market."""
    try:
        response = requests.get(
            f"{POLYMARKET_API}/prices", params={"market": condition_id}, timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching prices for {condition_id}: {e}")
        return None


def get_polymarket_data() -> List[Dict]:
    """
    Fetch and structure Polymarket data for arbitrage analysis.

    Returns:
        List of dicts with: event_name, yes_price, no_price, condition_id
    """
    markets = fetch_polymarket_markets()
    results = []

    for market in markets[:50]:  # Limit to avoid rate limits
        condition_id = market.get("condition_id")
        if not condition_id:
            continue

        prices = fetch_polymarket_prices(condition_id)
        if not prices:
            continue

        results.append(
            {
                "platform": "Polymarket",
                "event_name": market.get("question", "Unknown"),
                "condition_id": condition_id,
                "yes_price": float(prices.get("yes", 0)),
                "no_price": float(prices.get("no", 0)),
                "volume": market.get("volume", 0),
                "fetched_at": datetime.now().isoformat(),
            }
        )

    return results


if __name__ == "__main__":
    print("Fetching Polymarket data...")
    data = get_polymarket_data()

    with open("polymarket_data.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved {len(data)} markets to polymarket_data.json")
