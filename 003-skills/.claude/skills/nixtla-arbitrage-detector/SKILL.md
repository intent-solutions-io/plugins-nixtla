---
name: nixtla-arbitrage-detector
description: "Detect arbitrage opportunities between Polymarket and Kalshi using forecast analysis. Use when finding price discrepancies across platforms. Trigger with 'find arbitrage' or 'compare market prices'."
version: "1.0.0"
license: MIT
allowed-tools: "Read,Write,Bash(python:*),Glob,Grep,WebFetch"
---

# Arbitrage Detector

Identifies potential arbitrage opportunities across Polymarket and Kalshi prediction markets.

## Purpose

Finds discrepancies in contract prices for the same event across Polymarket and Kalshi prediction markets, calculating potential profit after fees.

## Overview

Scans Polymarket and Kalshi for matching events. Fetches current prices for each event. Calculates the potential profit from buying on one platform and selling on the other, factoring in fees. Outputs a list of arbitrage opportunities ranked by potential profit.

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep, WebFetch

**Environment**: None required

**Packages**:
```bash
pip install requests pandas
```

## Instructions

### Step 1: Fetch Polymarket Data

Run the Polymarket data fetcher:
```bash
python {baseDir}/scripts/fetch_polymarket.py
```

This fetches active markets and current prices from Polymarket CLOB API, saving results to `polymarket_data.json`.

### Step 2: Fetch Kalshi Data

Run the Kalshi data fetcher:
```bash
python {baseDir}/scripts/fetch_kalshi.py
```

This fetches open markets from Kalshi API, saving results to `kalshi_data.json`.

### Step 3: Detect Arbitrage Opportunities

Run the arbitrage analyzer:
```bash
python {baseDir}/scripts/detect_arbitrage.py
```

This compares prices across platforms using fuzzy string matching (70% similarity threshold), calculates arbitrage strategies, and outputs opportunities sorted by profit percentage.

### Step 4: Generate Report

Create the summary report:
```bash
python {baseDir}/scripts/generate_report.py
```

Generates a formatted markdown report with top opportunities and risk warnings.

## Output

- **polymarket_data.json**: Raw market data from Polymarket
- **kalshi_data.json**: Raw market data from Kalshi
- **arbitrage_opportunities.csv**: All detected opportunities with profit calculations
- **arbitrage_report.md**: Formatted summary report

## Error Handling

1. **Error**: `Polymarket API Error`
   **Solution**: Check Polymarket API status at status.polymarket.com. Retry after 30 seconds.

2. **Error**: `Kalshi API Error`
   **Solution**: Check Kalshi API status. May need API authentication for some endpoints.

3. **Error**: `No matching events found`
   **Solution**: Lower the similarity threshold (default 0.7) or manually map event names.

4. **Error**: `Insufficient data to calculate arbitrage`
   **Solution**: Ensure both platforms have YES and NO prices > 0.

## Examples

### Example 1: Profitable Arbitrage Found

**Scenario**: Same election event on both platforms

```
Event: "Will candidate X win the 2024 election?"
Polymarket: YES = 0.45, NO = 0.55
Kalshi: YES = 0.52, NO = 0.48

Strategy: Buy Polymarket YES + Kalshi NO
Cost: 0.45 * 1.02 + 0.48 * 1.01 = 0.459 + 0.485 = 0.944
Guaranteed Return: $1.00
Profit: $0.056 (5.9%)
```

### Example 2: No Arbitrage

**Scenario**: Prices are efficiently aligned

```
Event: "Will it rain tomorrow in NYC?"
Polymarket: YES = 0.50, NO = 0.50
Kalshi: YES = 0.50, NO = 0.50

Cost of any strategy > $1.00 after fees
Result: No profitable arbitrage
```

## Resources

- Polymarket data fetcher: `{baseDir}/scripts/fetch_polymarket.py`
- Kalshi data fetcher: `{baseDir}/scripts/fetch_kalshi.py`
- Arbitrage analyzer: `{baseDir}/scripts/detect_arbitrage.py`
- Report generator: `{baseDir}/scripts/generate_report.py`

## Usage

Run the complete workflow:

```bash
# 1. Fetch data from both platforms
python {baseDir}/scripts/fetch_polymarket.py
python {baseDir}/scripts/fetch_kalshi.py

# 2. Detect arbitrage opportunities
python {baseDir}/scripts/detect_arbitrage.py

# 3. Generate report
python {baseDir}/scripts/generate_report.py
```

Or invoke this skill to generate and execute all scripts automatically.
