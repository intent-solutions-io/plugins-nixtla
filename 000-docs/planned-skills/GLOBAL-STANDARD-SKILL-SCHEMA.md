# Global Standard Skill Schema

**Version**: 1.0.0
**Created**: 2025-12-05
**Authority**: Intent Solutions × Nixtla
**Purpose**: Authoritative specification for Claude Skills as multi-step workflow orchestrators

---

## Core Principle

**Skills are NOT simple prompt templates. Skills are WORKFLOW ORCHESTRATORS.**

Each skill must:
1. Execute **3-5+ workflow steps minimum**
2. Utilize **executable code** (Python, Bash, scripts)
3. Call **multiple APIs** across services (stackable integrations)
4. Be **composable** (skills can call other skills)
5. Think **outside the box** (ultra-creative problem solving)

---

## Schema Definition

### 1. Frontmatter (Metadata Layer)

**Official Anthropic Standard**: ONLY `name` and `description` fields allowed.

```yaml
---
name: nixtla-[short-name]
description: "[Action verb] [what it does]. [Key capabilities]. Use when [scenarios]. Trigger with '[phrases]'."
---
```

#### Description Formula (80%+ Quality Target)

**Structure**: `[Action]. [Capabilities]. Use when [scenarios]. Trigger with "[phrases]".`

**Example (95/100 score)**:
```yaml
description: "Orchestrates multi-step Polymarket analysis workflows. Fetches contract odds via API, transforms to time series format, forecasts prices using TimeGPT, analyzes arbitrage vs Kalshi, and generates trading recommendations. Use when analyzing prediction markets, forecasting contract prices, identifying mispriced opportunities, or comparing cross-platform odds. Trigger with 'analyze Polymarket contract', 'forecast prediction market', 'find arbitrage opportunities'."
```

**Scoring Criteria**:
- Action-oriented language (20%): "Orchestrates", "Fetches", "Transforms", "Forecasts"
- Clear trigger phrases (25%): Explicit examples in quotes
- Comprehensive coverage (15%): All 5 workflow steps mentioned
- Natural language matching (20%): How users actually talk
- Specificity without verbosity (10%): Concrete, not generic
- Technical domain terms (10%): "TimeGPT", "arbitrage", "time series"

**Character Limit**: <250 characters (fits in 15k token discovery budget)

---

### 2. SKILL.md (Core Orchestration Layer)

**Token Budget**: <500 lines (~2,500 tokens)
**Purpose**: Define the multi-step workflow orchestration logic

#### Required Sections

##### 2.1 Purpose
```markdown
# [Skill Name]

**Purpose**: [1-2 sentences explaining the multi-step orchestration]

**Workflow**: [High-level 3-5 step summary]
1. Step 1 (API/Code)
2. Step 2 (API/Code)
3. Step 3 (API/Code)
4. Step 4 (API/Code)
5. Step 5 (Output)
```

##### 2.2 Overview
```markdown
## Overview

**What This Skill Orchestrates**:
- API Integration 1: [Service name, purpose]
- API Integration 2: [Service name, purpose]
- Code Execution: [Python/Bash scripts]
- Data Transformation: [Format conversions]
- Output Generation: [What artifacts produced]

**When to Use**:
- Scenario 1
- Scenario 2
- Scenario 3

**Composability**: Can be stacked with [other skills] for [combined workflow]
```

##### 2.3 Prerequisites
```markdown
## Prerequisites

**API Access**:
- [ ] API 1: [Name] (set `API_KEY_1` environment variable)
- [ ] API 2: [Name] (set `API_KEY_2` environment variable)
- [ ] API 3: [Name] (optional for enhanced features)

**Environment Variables**:
```bash
export POLYMARKET_API_KEY="your_key_here"
export NIXTLA_API_KEY="your_timegpt_key"
export KALSHI_API_KEY="your_key_here"  # Optional
```

**Required Libraries**:
```bash
pip install nixtla statsforecast pandas requests
```

**File Structure**:
```
{baseDir}/
├── SKILL.md              # This file
├── scripts/
│   ├── fetch_polymarket.py      # Step 1: API data fetcher
│   ├── transform_to_timeseries.py  # Step 2: Format converter
│   ├── forecast_timegpt.py       # Step 3: TimeGPT forecaster
│   ├── analyze_arbitrage.py     # Step 4: Cross-platform analyzer
│   └── generate_report.py       # Step 5: Report generator
├── references/
│   ├── POLYMARKET_API.md        # API documentation
│   ├── TIMEGPT_GUIDE.md         # TimeGPT integration guide
│   └── EXAMPLES.md              # Extended examples
└── assets/
    └── report_template.md       # Output template
```
```

##### 2.4 Workflow Instructions (3-5+ Steps)

**CRITICAL**: Each step must be concrete, executable, and utilize code or API calls.

```markdown
## Workflow Instructions

### Step 1: Fetch Contract Data from Polymarket API

**Action**: Execute Python script to fetch live contract odds.

**Code**:
```python
# Run this command
python {baseDir}/scripts/fetch_polymarket.py --contract-id "0x1234" --output data/raw_odds.json
```

**What This Does**:
1. Connects to Polymarket GraphQL API
2. Fetches historical odds data (last 30 days)
3. Extracts orderbook depth and liquidity
4. Saves to `data/raw_odds.json`

**Expected Output**:
```json
{
  "contract_id": "0x1234",
  "contract_name": "Will Bitcoin reach $100k by Dec 2025?",
  "odds_history": [
    {"timestamp": "2025-11-01T00:00:00Z", "yes_price": 0.65, "no_price": 0.35},
    ...
  ],
  "liquidity": 125000.50
}
```

---

### Step 2: Transform Odds to Time Series Format

**Action**: Convert prediction market odds to Nixtla-compatible time series.

**Code**:
```python
python {baseDir}/scripts/transform_to_timeseries.py \
  --input data/raw_odds.json \
  --output data/timeseries.csv \
  --freq D
```

**What This Does**:
1. Parses JSON odds data
2. Converts to 3-column format: `unique_id`, `ds` (timestamp), `y` (yes price)
3. Validates data quality (no gaps, proper frequency)
4. Saves CSV for TimeGPT

**Expected Output**:
```csv
unique_id,ds,y
BTC_100k_Dec2025,2025-11-01,0.65
BTC_100k_Dec2025,2025-11-02,0.67
BTC_100k_Dec2025,2025-11-03,0.66
...
```

---

### Step 3: Forecast Prices Using TimeGPT API

**Action**: Call Nixtla TimeGPT API to forecast next 14 days of contract prices.

**Code**:
```python
python {baseDir}/scripts/forecast_timegpt.py \
  --input data/timeseries.csv \
  --horizon 14 \
  --freq D \
  --output data/forecast.csv
```

**What This Does**:
1. Loads time series data
2. Calls TimeGPT API with 14-day horizon
3. Retrieves point forecasts + 80%/95% confidence intervals
4. Validates forecast quality (MAPE, coverage)
5. Saves forecast with metadata

**Expected Output**:
```csv
unique_id,ds,TimeGPT,TimeGPT-lo-80,TimeGPT-hi-80,TimeGPT-lo-95,TimeGPT-hi-95
BTC_100k_Dec2025,2025-12-06,0.68,0.65,0.71,0.63,0.73
BTC_100k_Dec2025,2025-12-07,0.69,0.66,0.72,0.64,0.74
...
```

---

### Step 4: Analyze Arbitrage Opportunities vs Kalshi

**Action**: Compare Polymarket forecast vs Kalshi current odds to identify mispricing.

**Code**:
```python
python {baseDir}/scripts/analyze_arbitrage.py \
  --polymarket-forecast data/forecast.csv \
  --kalshi-api-key $KALSHI_API_KEY \
  --min-spread 0.05 \
  --output data/arbitrage.json
```

**What This Does**:
1. Fetches current Kalshi odds for same event
2. Compares Polymarket forecast vs Kalshi current price
3. Calculates spread: `abs(polymarket_forecast - kalshi_current)`
4. Filters opportunities where spread > 5%
5. Ranks by profit potential

**Expected Output**:
```json
{
  "opportunities": [
    {
      "event": "BTC $100k by Dec 2025",
      "polymarket_forecast": 0.68,
      "kalshi_current": 0.60,
      "spread": 0.08,
      "potential_profit_pct": 13.3,
      "confidence": "high",
      "recommendation": "Buy Kalshi YES at 0.60, hedge on Polymarket"
    }
  ],
  "analysis_timestamp": "2025-12-05T12:00:00Z"
}
```

---

### Step 5: Generate Trading Recommendations Report

**Action**: Create markdown report with visualizations and actionable recommendations.

**Code**:
```python
python {baseDir}/scripts/generate_report.py \
  --forecast data/forecast.csv \
  --arbitrage data/arbitrage.json \
  --template {baseDir}/assets/report_template.md \
  --output reports/polymarket_analysis_2025-12-05.md
```

**What This Does**:
1. Loads forecast and arbitrage data
2. Generates ASCII charts of price predictions
3. Formats trading recommendations with risk levels
4. Fills markdown template with data
5. Saves final report

**Expected Output**: `reports/polymarket_analysis_2025-12-05.md`
```

##### 2.5 Output Artifacts
```markdown
## Output Artifacts

This skill produces:

1. **Raw Data**: `data/raw_odds.json` (Polymarket API response)
2. **Time Series**: `data/timeseries.csv` (Nixtla format)
3. **Forecast**: `data/forecast.csv` (TimeGPT predictions with confidence intervals)
4. **Arbitrage Analysis**: `data/arbitrage.json` (Trading opportunities)
5. **Final Report**: `reports/polymarket_analysis_YYYY-MM-DD.md` (Markdown with recommendations)

**Report Format**:
- Executive summary (1-2 sentences)
- Forecast chart (ASCII visualization)
- Arbitrage opportunities table (ranked by profit potential)
- Risk assessment (high/medium/low)
- Specific trading recommendations
- Confidence levels and disclaimers
```

##### 2.6 Error Handling
```markdown
## Error Handling

### Common Errors & Solutions

**Error 1**: `POLYMARKET_API_KEY not found`
- **Cause**: Environment variable not set
- **Solution**: `export POLYMARKET_API_KEY="your_key"`

**Error 2**: `TimeGPT API quota exceeded`
- **Cause**: Monthly API limit reached
- **Solution**: Use StatsForecast fallback: `python scripts/forecast_statsforecast.py` (local, free)

**Error 3**: `No arbitrage opportunities found`
- **Cause**: Markets are efficient, spreads < 5%
- **Solution**: Lower threshold with `--min-spread 0.02` or check back later

**Error 4**: `Kalshi API authentication failed`
- **Cause**: Invalid API key or missing
- **Solution**: Step 4 is optional; skill still produces forecast without arbitrage analysis

**Error 5**: `Invalid time series format`
- **Cause**: Data gaps or wrong frequency
- **Solution**: Script auto-fills missing dates with interpolation, logs warnings
```

##### 2.7 Composability & Stacking
```markdown
## Composability & Stacking

This skill can be **stacked** with other skills for advanced workflows:

### Stack 1: Multi-Contract Batch Analysis
```bash
# Analyze 10 Polymarket contracts in parallel
for contract_id in $(cat contracts.txt); do
  # This skill handles each contract
  python {baseDir}/scripts/fetch_polymarket.py --contract-id $contract_id &
done
wait
# Then run Steps 2-5 on all contracts
```

### Stack 2: Event Impact Modeling
```bash
# Combine with nixtla-event-impact-modeler skill
# 1. Run this skill for baseline forecast
# 2. Feed forecast into event-impact-modeler
# 3. Model how news events affect contract prices
```

### Stack 3: Portfolio Risk Analysis
```bash
# Combine with nixtla-market-risk-analyzer skill
# 1. Run this skill on multiple correlated contracts
# 2. Feed forecasts into risk-analyzer
# 3. Calculate portfolio VaR and position sizing
```

**Cross-Skill API Calls**:
Skills can invoke other skills via:
```python
# In a Python script
from claude_skills import invoke_skill

# This skill's forecast can trigger another skill
risk_analysis = invoke_skill(
    name="nixtla-market-risk-analyzer",
    input_data=forecast_results
)
```
```

##### 2.8 Examples
```markdown
## Examples

### Example 1: Basic Polymarket Forecast

**User Request**:
> "Analyze the 'Trump wins 2024' contract on Polymarket and forecast the next 2 weeks"

**Skill Execution**:
```bash
# Step 1: Fetch
python {baseDir}/scripts/fetch_polymarket.py --contract-id "0xABC123" --output data/trump_2024.json

# Step 2: Transform
python {baseDir}/scripts/transform_to_timeseries.py --input data/trump_2024.json --output data/trump_ts.csv

# Step 3: Forecast
python {baseDir}/scripts/forecast_timegpt.py --input data/trump_ts.csv --horizon 14 --output data/trump_forecast.csv

# Step 4: Arbitrage (skip if no Kalshi equivalent)
# (Skipped - no matching Kalshi contract)

# Step 5: Report
python {baseDir}/scripts/generate_report.py --forecast data/trump_forecast.csv --output reports/trump_2024_analysis.md
```

**Output Report** (`reports/trump_2024_analysis.md`):
```markdown
# Polymarket Analysis: Trump Wins 2024

**Contract**: 0xABC123
**Analysis Date**: 2025-12-05
**Forecast Horizon**: 14 days

## Executive Summary
Forecasted YES price to rise from 0.52 → 0.56 (+7.7%) over next 2 weeks with high confidence.

## Forecast Chart
```
Price
0.58│           ╭────
0.56│       ╭───╯
0.54│   ╭───╯
0.52│───╯
    └────────────────> Time
    Now  +7d  +14d
```

## Recommendation
HOLD current position. Forecast shows steady upward trend with 80% confidence interval [0.54, 0.58].

**Risk**: Medium (wide confidence intervals indicate market uncertainty)
```

### Example 2: Cross-Platform Arbitrage Detection

**User Request**:
> "Find arbitrage opportunities between Polymarket and Kalshi for crypto markets"

**Skill Execution**:
```bash
# Run full 5-step workflow with Kalshi integration
./run_full_workflow.sh --category crypto --platforms polymarket,kalshi --min-spread 0.05
```

**Output**: 3 arbitrage opportunities identified with 8-13% profit potential

### Example 3: Stacked Multi-Contract Portfolio Analysis

**User Request**:
> "Analyze correlation between BTC price contracts, ETH price contracts, and election contracts"

**Skill Execution**:
```bash
# Step 1: Fetch all 3 contract types
python scripts/fetch_polymarket.py --contracts btc_contracts.txt
python scripts/fetch_polymarket.py --contracts eth_contracts.txt
python scripts/fetch_polymarket.py --contracts election_contracts.txt

# Step 2-3: Transform + Forecast all
for file in data/raw_*.json; do
  python scripts/transform_to_timeseries.py --input $file
  python scripts/forecast_timegpt.py --input data/$(basename $file .json)_ts.csv
done

# Step 4: Stack with correlation-mapper skill
invoke_skill("nixtla-correlation-mapper", inputs=all_forecasts)

# Step 5: Generate portfolio report
python scripts/generate_report.py --mode portfolio --output reports/portfolio_correlation.md
```

**Output**: Correlation matrix showing BTC/ETH 0.82 correlation, BTC/Election 0.23 correlation (weak)
```

---

### 3. scripts/ Directory (Code Execution Layer)

**Purpose**: Executable Python/Bash scripts for each workflow step

**Requirements**:
- Each script is **self-contained** (can run independently)
- Accepts **command-line arguments** (no hardcoded values)
- Includes **error handling** and logging
- Returns **exit codes** (0 = success, 1+ = error)
- Outputs to **stdout** or specified file

**Example Script Structure** (`scripts/fetch_polymarket.py`):
```python
#!/usr/bin/env python3
"""
Polymarket API Data Fetcher
Fetches historical contract odds from Polymarket GraphQL API

Usage:
    python fetch_polymarket.py --contract-id "0x1234" --output data/odds.json
"""
import os
import sys
import json
import argparse
import requests
from datetime import datetime, timedelta

def fetch_polymarket_contract(contract_id: str, days_back: int = 30) -> dict:
    """Fetch contract data from Polymarket API"""
    api_key = os.getenv("POLYMARKET_API_KEY")
    if not api_key:
        print("ERROR: POLYMARKET_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    # GraphQL query
    query = """
    query GetContract($id: String!, $startDate: DateTime!) {
      contract(id: $id) {
        id
        question
        outcomes
        oddsHistory(startDate: $startDate) {
          timestamp
          yesPrice
          noPrice
          volume
          liquidity
        }
      }
    }
    """

    variables = {
        "id": contract_id,
        "startDate": (datetime.now() - timedelta(days=days_back)).isoformat()
    }

    response = requests.post(
        "https://api.polymarket.com/graphql",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"query": query, "variables": variables}
    )

    if response.status_code != 200:
        print(f"ERROR: API request failed with status {response.status_code}", file=sys.stderr)
        sys.exit(1)

    return response.json()

def main():
    parser = argparse.ArgumentParser(description="Fetch Polymarket contract data")
    parser.add_argument("--contract-id", required=True, help="Contract ID (hex address)")
    parser.add_argument("--output", required=True, help="Output JSON file path")
    parser.add_argument("--days-back", type=int, default=30, help="Days of history (default: 30)")

    args = parser.parse_args()

    print(f"Fetching Polymarket contract {args.contract_id}...")
    data = fetch_polymarket_contract(args.contract_id, args.days_back)

    # Save to file
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"✓ Saved {len(data['data']['contract']['oddsHistory'])} records to {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

**Naming Convention**: `[action]_[service].py` or `[action]_[purpose].py`
- `fetch_polymarket.py` - Fetches from Polymarket
- `transform_to_timeseries.py` - Transforms data format
- `forecast_timegpt.py` - Runs TimeGPT forecast
- `analyze_arbitrage.py` - Analyzes cross-platform opportunities
- `generate_report.py` - Generates markdown report

---

### 4. references/ Directory (Context Documentation)

**Purpose**: Documentation loaded into Claude's context during skill execution

**What to Include**:
- API documentation extracts
- Code examples
- Advanced patterns
- Troubleshooting guides
- Domain knowledge

**Example Files**:
```
references/
├── POLYMARKET_API.md        # Polymarket GraphQL API docs
├── KALSHI_API.md            # Kalshi REST API docs
├── TIMEGPT_GUIDE.md         # TimeGPT integration patterns
├── ARBITRAGE_STRATEGIES.md  # Trading strategies explained
└── EXAMPLES.md              # Extended use cases
```

**Token Budget**: Keep each reference <1,000 tokens (Claude loads these into context)

---

### 5. assets/ Directory (Templates & Static Resources)

**Purpose**: Templates and resources NOT loaded into context (only used by scripts)

**What to Include**:
- Markdown report templates
- Configuration files
- Sample data for testing

**Example Files**:
```
assets/
├── report_template.md       # Markdown template for final report
├── config.example.json      # Example configuration
└── sample_data.csv          # Test data for development
```

**Note**: Scripts reference these with `{baseDir}/assets/[filename]`

---

## 6. Quality Checklist

Before finalizing a skill, validate against this checklist:

### Frontmatter Quality
- [ ] Description follows formula: `[Action]. [Capabilities]. Use when [scenarios]. Trigger with "[phrases]".`
- [ ] Description scores 80%+ on 6-criterion quality formula
- [ ] Description is <250 characters
- [ ] Only `name` and `description` fields (no extra metadata)
- [ ] Name follows convention: `nixtla-[short-kebab-case-name]`

### SKILL.md Quality
- [ ] Total lines <500 (hard limit)
- [ ] Defines 3-5+ concrete workflow steps
- [ ] Each step has executable code or API call
- [ ] Uses `{baseDir}` for all file paths
- [ ] Imperative voice ("Execute", "Run", "Fetch" not "You should")
- [ ] All prerequisites documented (APIs, env vars, libraries)
- [ ] Error handling section with common failures + solutions
- [ ] At least 2 concrete examples with input/output
- [ ] Composability section showing how to stack with other skills

### Code Quality (scripts/)
- [ ] Each script is independently executable
- [ ] Command-line arguments (no hardcoded values)
- [ ] Proper error handling with exit codes
- [ ] Logging to stdout/stderr
- [ ] Docstrings explaining purpose and usage
- [ ] All API keys from environment variables (never hardcoded)

### Integration Quality
- [ ] API calls use proper authentication
- [ ] Data transformations are reversible/auditable
- [ ] Output formats are documented and validated
- [ ] Multiple API integrations work together seamlessly

### Composability Quality
- [ ] Skill can run standalone
- [ ] Skill can be stacked with other skills
- [ ] Input/output formats allow chaining
- [ ] Examples show at least 1 stacking pattern

### Documentation Quality
- [ ] references/ files are <1,000 tokens each
- [ ] assets/ templates are well-commented
- [ ] Examples cover common use cases
- [ ] Prerequisites are complete and testable

---

## 7. Architectural Patterns Reference

Each skill should leverage one or more of these 8 patterns:

### Pattern 1: Script Automation ⭐ (Primary for prediction markets)
```markdown
**Use When**: Complex operations need deterministic logic
**Flow**: Claude orchestrates → Python/Bash executes → Claude processes results
**Example**: Fetch Polymarket data → Transform → TimeGPT → Analyze → Report
```

### Pattern 2: Read-Process-Write
```markdown
**Use When**: Simple transformations
**Flow**: Read input → Apply rules → Write output
**Example**: Read contract JSON → Map to Nixtla schema → Write CSV
```

### Pattern 3: Search-Analyze-Report
```markdown
**Use When**: Finding patterns in data
**Flow**: Search → Read matches → Analyze → Generate report
**Example**: Search for mispriced contracts → Analyze spreads → Report arbitrage
```

### Pattern 4: Command Chain Execution
```markdown
**Use When**: Sequential operations with dependencies
**Flow**: Step 1 && Step 2 && Step 3
**Example**: Fetch && Transform && Forecast && Report
```

### Pattern 5: Wizard-Style Workflows
```markdown
**Use When**: User needs to confirm between steps
**Flow**: Step 1 → [Confirm] → Step 2 → [Confirm] → Step 3
**Example**: Configure API → [Confirm] → Test → [Confirm] → Forecast
```

### Pattern 6: Template-Based Generation
```markdown
**Use When**: Structured output needed
**Flow**: Load template from assets/ → Fill placeholders → Write
**Example**: Load forecast report template → Fill predictions → Generate markdown
```

### Pattern 7: Iterative Refinement
```markdown
**Use When**: Progressive deepening needed
**Flow**: Pass 1 (broad) → Pass 2 (deep) → Pass 3 (recommendations)
**Example**: Scan all contracts → Deep dive top 10 → Specific trades
```

### Pattern 8: Context Aggregation
```markdown
**Use When**: Synthesizing from multiple sources
**Flow**: Gather source 1, 2, 3 → Synthesize
**Example**: Polymarket odds + Kalshi odds + Twitter sentiment → Combined forecast
```

---

## 8. Token Budget Management

**Global Limit**: 15,000 characters for skill discovery

**Breakdown**:
- Frontmatter (name + description): ~250 chars
- SKILL.md: ~2,500 tokens (500 lines × 5 tokens/line avg)
- references/ (loaded into context): ~2,000 tokens total
- **Total**: ~5,000 tokens (well within budget)

**What NOT to Load**:
- scripts/ code (only executed, not loaded)
- assets/ templates (only referenced, not loaded)
- Large data files

---

## 9. Example: Complete Skill Structure

```
nixtla-polymarket-analyst/
├── SKILL.md                          # 480 lines (2,400 tokens)
├── scripts/
│   ├── fetch_polymarket.py           # 150 lines (executable)
│   ├── transform_to_timeseries.py    # 100 lines (executable)
│   ├── forecast_timegpt.py           # 120 lines (executable)
│   ├── analyze_arbitrage.py          # 180 lines (executable)
│   └── generate_report.py            # 90 lines (executable)
├── references/
│   ├── POLYMARKET_API.md             # 800 tokens (loaded)
│   ├── TIMEGPT_GUIDE.md              # 600 tokens (loaded)
│   └── EXAMPLES.md                   # 400 tokens (loaded)
└── assets/
    ├── report_template.md            # Not loaded
    └── config.example.json           # Not loaded

Total Discovery Budget: ~4,450 tokens ✓ (within 5,000 limit)
```

---

## 10. Validation & Testing

### Pre-Flight Checklist
Before deploying a skill, test:

1. **Standalone Execution**: Each script runs independently
2. **Full Workflow**: All 5 steps execute in sequence
3. **Error Handling**: Scripts fail gracefully with helpful errors
4. **API Integration**: All API calls work with test keys
5. **Composability**: Skill can be stacked with another skill
6. **Token Budget**: Total skill size <5,000 tokens
7. **Description Quality**: Scores 80%+ on quality formula
8. **Documentation**: All prerequisites are accurate

### Testing Template
```bash
# Test 1: Individual script execution
python scripts/fetch_polymarket.py --contract-id TEST_ID --output /tmp/test.json
echo $?  # Should be 0

# Test 2: Full workflow
./run_full_workflow.sh --contract-id TEST_ID --output /tmp/report.md

# Test 3: Error handling (missing API key)
unset POLYMARKET_API_KEY
python scripts/fetch_polymarket.py --contract-id TEST_ID
# Should print helpful error message

# Test 4: Composability (stack with another skill)
# (Manual test - invoke skill, then invoke another skill with output)

# Test 5: Token budget
wc -l SKILL.md  # Should be <500 lines
```

---

## 11. Global Standard Enforcement

**This schema is MANDATORY for all Nixtla skills.**

**Compliance Requirements**:
1. Must follow frontmatter standard (name + description only)
2. Must define 3-5+ workflow steps with code/API calls
3. Must stay within token budget (<5,000 tokens)
4. Must score 80%+ on description quality
5. Must demonstrate composability with stacking examples
6. Must include error handling for all steps
7. Must use `{baseDir}` for all paths
8. Must validate against quality checklist

**Non-Compliance Consequences**:
- Skill will fail activation (poor description quality)
- Skill will exceed token budget (slow loading)
- Skill will break (hardcoded paths, missing error handling)
- Skill won't scale (can't be stacked or composed)

**Enforcement**: All skills must pass validation before release:
```bash
python validate_skill.py --skill-dir nixtla-polymarket-analyst/
# Checks all compliance requirements
# Returns 0 if compliant, 1+ if issues found
```

---

## 12. Future Extensions

This schema is version 1.0.0. Future enhancements may include:

1. **Skill Registry**: Central catalog of all skills with metadata
2. **Dependency Management**: Skills declare dependencies on other skills
3. **Versioning**: Semantic versioning for skills (v1.2.3)
4. **Testing Framework**: Automated testing harness for workflow validation
5. **Marketplace Integration**: Skills can be published to Claude Code marketplace
6. **Analytics**: Track skill usage, success rates, error patterns
7. **A/B Testing**: Test description variations for activation accuracy

---

**Version**: 1.0.0
**Last Updated**: 2025-12-05
**Maintained By**: Intent Solutions × Nixtla
**Status**: Global Standard (Active)

---

**This schema represents the cutting edge of Claude Skills architecture.**
**Think outside the box. Build workflows, not templates.**
**Stack, compose, orchestrate. 🚀**
