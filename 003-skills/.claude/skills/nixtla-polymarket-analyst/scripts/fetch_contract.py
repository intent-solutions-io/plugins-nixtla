#!/usr/bin/env python3
"""
Polymarket Contract Data Fetcher

Fetches historical price data for a specific Polymarket contract.
Outputs JSON file with contract metadata and price history.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import requests

POLYMARKET_CLOB_API = "https://clob.polymarket.com"
POLYMARKET_GAMMA_API = "https://gamma-api.polymarket.com"


def fetch_contract_metadata(condition_id: str) -> Optional[Dict]:
    """
    Fetch contract metadata from Polymarket.

    Args:
        condition_id: Polymarket contract/condition ID

    Returns:
        Dict with contract metadata or None if error
    """
    try:
        response = requests.get(f"{POLYMARKET_CLOB_API}/markets/{condition_id}", timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching metadata: {e}", file=sys.stderr)
        return None


def fetch_price_history(condition_id: str, days: int = 30) -> List[Dict]:
    """
    Fetch historical price data for a contract.

    Args:
        condition_id: Polymarket contract/condition ID
        days: Number of days of history to fetch

    Returns:
        List of price points with timestamps
    """
    try:
        # Calculate time range
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)

        response = requests.get(
            f"{POLYMARKET_GAMMA_API}/markets/{condition_id}/prices",
            params={
                "start": int(start_time.timestamp()),
                "end": int(end_time.timestamp()),
                "interval": "1h",  # Hourly data
            },
            timeout=30,
        )
        response.raise_for_status()
        return response.json().get("prices", [])
    except requests.RequestException as e:
        print(f"Error fetching price history: {e}", file=sys.stderr)
        return []


def get_contract_data(condition_id: str, days: int = 30) -> Dict:
    """
    Fetch complete contract data including metadata and price history.

    Args:
        condition_id: Polymarket contract ID
        days: Days of history to fetch

    Returns:
        Dict with metadata and price history

    Raises:
        ValueError: If data cannot be fetched
    """
    print(f"Fetching data for contract: {condition_id}")

    metadata = fetch_contract_metadata(condition_id)
    if not metadata:
        raise ValueError(f"Could not fetch metadata for {condition_id}")

    prices = fetch_price_history(condition_id, days)
    if not prices:
        raise ValueError(f"No price history available for {condition_id}")

    return {
        "condition_id": condition_id,
        "question": metadata.get("question", "Unknown"),
        "description": metadata.get("description", ""),
        "end_date": metadata.get("end_date_iso"),
        "volume": metadata.get("volume", 0),
        "liquidity": metadata.get("liquidity", 0),
        "prices": prices,
        "fetched_at": datetime.now().isoformat(),
    }


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Fetch Polymarket contract data")
    parser.add_argument("condition_id", help="Polymarket contract/condition ID")
    parser.add_argument(
        "--days", type=int, default=30, help="Days of historical data to fetch (default: 30)"
    )
    parser.add_argument("--output", help="Output file path (default: contract_{id}_data.json)")

    args = parser.parse_args()

    try:
        data = get_contract_data(args.condition_id, args.days)

        output_file = args.output or f"contract_{args.condition_id[:8]}_data.json"
        with open(output_file, "w") as f:
            json.dump(data, f, indent=2)

        print(f"Contract: {data['question'][:60]}...")
        print(f"Price points: {len(data['prices'])}")
        print(f"Saved to {output_file}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
