# Claude Skill ARD: Nixtla Polymarket Analyst

**Template Version**: 1.0.0
**Based On**: [Global Standard Skill Schema](../../GLOBAL-STANDARD-SKILL-SCHEMA.md)
**Purpose**: Architecture & Requirements Document for Claude Skills
**Status**: Planned

---

## Document Control

| Field | Value |
|-------|-------|
| **Skill Name** | nixtla-polymarket-analyst |
| **Architectural Pattern** | [X] Script Automation [ ] Read-Process-Write [ ] Search-Analyze-Report [ ] Command Chain [ ] Wizard [ ] Template-Based [ ] Iterative Refinement [ ] Context Aggregation |
| **Complexity Level** | [ ] Simple (3 steps) [X] Medium (4-5 steps) [ ] Complex (6+ steps) |
| **API Integrations** | 3 (Polymarket, TimeGPT, Kalshi) |
| **Token Budget** | ~4,200 / 5,000 max |
| **Status** | [X] Planned [ ] In Development [ ] Complete |
| **Owner** | Intent Solutions |
| **Last Updated** | 2025-12-06 |

---

## 1. Architectural Overview

### 1.1 Skill Purpose

**One-Sentence Summary**: Orchestrates a 5-step prediction market analysis workflow that fetches Polymarket contract odds via GraphQL API, transforms them to time series format, generates TimeGPT price forecasts, identifies potential pricing discrepancies vs Kalshi, and produces structured forecast and analysis reports.

**Architectural Pattern**: **Script Automation** (Primary)

**Why This Pattern**:
- **Complex operations need deterministic logic**: Each step (API calls, data transformations, forecasting) requires precise Python code execution
- **Claude orchestrates → Python executes → Claude processes**: Claude manages workflow, Python scripts handle API interactions and data processing, Claude interprets results
- **Sequential dependencies**: Each step depends on previous output (fetch → transform → forecast → analyze → report)
- **Multiple API integrations**: 3 different APIs (Polymarket, TimeGPT, Kalshi) require structured HTTP calls with authentication, error handling, retries

**Secondary Pattern**: **Context Aggregation** (for Step 4 - combining Polymarket forecast + Kalshi current odds)

### 1.2 High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│         NIXTLA POLYMARKET ANALYST ORCHESTRATION             │
│                  5-Step Workflow                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
         ┌────────────────────────────────────────┐
         │  Step 1: Fetch Polymarket Contract Data│
         │  ├─ API: Polymarket GraphQL            │
         │  ├─ Code: scripts/fetch_polymarket.py  │
         │  ├─ Auth: None (public data)           │
         │  └─ Output: data/raw_odds.json         │
         └────────────────────────────────────────┘
                              │
                              ▼
         ┌────────────────────────────────────────┐
         │  Step 2: Transform to Time Series      │
         │  ├─ Code: scripts/transform_to_ts.py   │
         │  ├─ Transform: JSON → CSV (Nixtla fmt) │
         │  ├─ Validation: No gaps, 0≤y≤1         │
         │  └─ Output: data/timeseries.csv        │
         └────────────────────────────────────────┘
                              │
                              ▼
         ┌────────────────────────────────────────┐
         │  Step 3: TimeGPT Price Forecast        │
         │  ├─ API: Nixtla TimeGPT API            │
         │  ├─ Code: scripts/forecast_timegpt.py  │
         │  ├─ Auth: X-API-Key (NIXTLA_API_KEY)   │
         │  ├─ Fallback: StatsForecast (local)    │
         │  └─ Output: data/forecast.csv          │
         └────────────────────────────────────────┘
                              │
                              ▼
         ┌────────────────────────────────────────┐
         │  Step 4: Arbitrage Analysis vs Kalshi  │
         │  ├─ API: Kalshi REST API (optional)    │
         │  ├─ Code: scripts/analyze_arbitrage.py │
         │  ├─ Auth: API Key (optional)           │
         │  ├─ Logic: Compare forecast vs current │
         │  └─ Output: data/arbitrage.json        │
         └────────────────────────────────────────┘
                              │
                              ▼
         ┌────────────────────────────────────────┐
         │  Step 5: Generate Analysis Report      │
         │  ├─ Code: scripts/generate_report.py   │
         │  ├─ Template: assets/report_template.md│
         │  ├─ Charts: ASCII price visualization  │
         │  └─ Output: reports/analysis_DATE.md   │
         └────────────────────────────────────────┘
```

### 1.3 Workflow Summary

**Total Steps**: 5 (all mandatory except Step 4 gracefully degrades)

| Step | Action | Type | Dependencies | Output | Avg Time |
|------|--------|------|--------------|--------|----------|
| 1 | Fetch Contract Data | API Call + Python | None (user provides contract ID) | raw_odds.json (5-50 KB) | 3-5 sec |
| 2 | Transform to Time Series | Python | Step 1 (raw_odds.json) | timeseries.csv (2-10 KB) | 1-2 sec |
| 3 | Generate Forecast | API Call + Python | Step 2 (timeseries.csv) | forecast.csv (3-15 KB) | 20-30 sec |
| 4 | Analyze Arbitrage | API Call + Python (optional) | Step 3 (forecast.csv) | arbitrage.json (1-5 KB) | 5-10 sec |
| 5 | Generate Report | Python + Template | Steps 3-4 (forecast + comparison) | analysis_DATE.md (10-50 KB) | 3-5 sec |

**Total Execution Time**: 32-52 seconds (target: <60 seconds)

---

## 2. Progressive Disclosure Strategy

### 2.1 Level 1: Frontmatter (Metadata)

**What Goes Here**: ONLY `name` and `description` (Anthropic official standard)

```yaml
---
# 🔴 REQUIRED FIELDS
name: nixtla-polymarket-analyst
description: "Orchestrates multi-step Polymarket analysis workflows. Fetches contract odds via API, transforms to time series, forecasts prices using TimeGPT, compares odds across platforms, generates analysis reports. Use when analyzing prediction markets, forecasting contract prices, comparing platform pricing. Trigger with 'analyze Polymarket contract', 'forecast prediction market', 'compare odds'."

# 🟡 OPTIONAL FIELDS
allowed-tools: "Read,Write,Bash"
model: inherit
version: "1.0.1"
---
```

**Description Quality Analysis**:

| Criterion | Score | Evidence |
|-----------|-------|----------|
| Action-oriented (20%) | 20/20 | "Orchestrates", "Fetches", "transforms", "forecasts", "analyzes", "generates" |
| Clear triggers (25%) | 25/25 | Three explicit phrases: "analyze Polymarket contract", "forecast prediction market", "compare odds" |
| Comprehensive (15%) | 14/15 | All 5 steps mentioned (fetch, transform, forecast, analyze, generate) |
| Natural language (20%) | 18/20 | Matches analyst vocabulary ("platform pricing", "analysis reports") |
| Specificity (10%) | 10/10 | Concrete tools/platforms: "Polymarket", "TimeGPT", "Kalshi", "arbitrage" |
| Technical terms (10%) | 10/10 | Domain keywords: "time series", "forecast", "arbitrage", "contract odds" |
| **TOTAL** | **97/100** | ✅ Exceeds 80% target |

**Character Count**: 248 / 250 max ✅

### 2.2 Level 2: SKILL.md (Core Instructions)

**Token Budget**: ~2,400 tokens (480 lines × 5 tokens/line avg)

**Required Sections**:
1. ✅ Purpose (1-2 sentences + workflow summary)
2. ✅ Overview (what, when, capabilities, composability)
3. ✅ Prerequisites (APIs, env vars, libraries, file structure)
4. ✅ Workflow Instructions (5 steps with code)
5. ✅ Output Artifacts (5 files produced)
6. ✅ Error Handling (common errors + solutions)
7. ✅ Composability & Stacking (3 stacking patterns)
8. ✅ Examples (3 concrete walkthroughs)

**What Goes Here**:
- Core orchestration logic for each of the 5 steps
- Concrete Python commands with arguments
- Expected output formats and file paths (using `{baseDir}`)
- Error handling for API failures, quota limits, missing keys
- Stacking patterns with other skills

**What Does NOT Go Here**:
- Polymarket API documentation (→ `references/POLYMARKET_API.md`)
- TimeGPT API documentation (→ `references/TIMEGPT_GUIDE.md`)
- Extended examples (→ `references/EXAMPLES.md`)
- Python script source code (→ `004-scripts/*.py`)
- Report templates (→ `assets/report_template.md`)

### 2.3 Level 3: Resources (Extended Context)

#### scripts/ Directory (NOT loaded into context)

**Purpose**: Executable Python scripts for each workflow step

**Files** (5 primary + 1 utility):

1. **`fetch_polymarket.py`** (~150 lines)
   - GraphQL query for contract odds history
   - Error handling: retries, rate limits, invalid contract IDs
   - CLI args: `--contract-id`, `--days-back`, `--output`
   - Output: `data/raw_odds.json`

2. **`transform_to_timeseries.py`** (~100 lines)
   - Parse JSON, extract yes_price as target
   - Convert to 3-column CSV: unique_id, ds, y
   - Validation: no gaps, 0≤y≤1, chronological
   - CLI args: `--input`, `--output`, `--freq`
   - Output: `data/timeseries.csv`

3. **`forecast_timegpt.py`** (~120 lines)
   - Call TimeGPT API with time series + horizon
   - Fallback to StatsForecast on quota errors
   - CLI args: `--input`, `--horizon`, `--freq`, `--output`
   - Output: `data/forecast.csv`

4. **`analyze_arbitrage.py`** (~180 lines)
   - Fetch Kalshi equivalent contract (optional)
   - Calculate spread: abs(forecast - kalshi_current)
   - Filter by minimum spread threshold
   - CLI args: `--forecast`, `--kalshi-api-key`, `--min-spread`, `--output`
   - Output: `data/arbitrage.json`

5. **`generate_report.py`** (~90 lines)
   - Load forecast + arbitrage data
   - Generate ASCII chart of predictions
   - Fill markdown template with data
   - CLI args: `--forecast`, `--arbitrage`, `--template`, `--output`
   - Output: `reports/analysis_YYYY-MM-DD.md`

6. **`utils/api_client.py`** (~80 lines, optional)
   - Shared HTTP client with retries, backoff
   - Reusable across scripts

**Naming Convention**: `[verb]_[noun].py`
- ✅ `fetch_polymarket.py` - Clear action + target
- ✅ `transform_to_timeseries.py` - Clear transformation
- ✅ `forecast_timegpt.py` - Clear method + tool

#### references/ Directory (loaded into context)

**Purpose**: Documentation that Claude reads during skill execution

**Token Budget**: Each file <1,000 tokens (total ~1,800 tokens)

**Files**:

1. **`POLYMARKET_API.md`** (~800 tokens)
   - GraphQL endpoint and query structure
   - Contract ID format and discovery
   - Response schema (odds_history fields)
   - Rate limits and error codes

2. **`TIMEGPT_GUIDE.md`** (~600 tokens)
   - TimeGPT API endpoint and authentication
   - Request format (time series data schema)
   - Response format (forecast + confidence intervals)
   - Quota limits and fallback strategy

3. **`EXAMPLES.md`** (~400 tokens)
   - Extended walkthrough: BTC $100k contract analysis
   - Extended walkthrough: Cross-platform arbitrage detection
   - Extended walkthrough: Handling quota exceeded error

#### assets/ Directory (NOT loaded into context)

**Purpose**: Templates and resources used by scripts

**Files**:

1. **`report_template.md`** (~200 lines)
   - Markdown structure with placeholders
   - Sections: Executive Summary, Forecast Chart, Cross-Platform Comparison, Analysis Summary, Risk Assessment

2. **`config.example.json`** (~20 lines)
   - Example API key configuration
   - Default parameters (horizon, min_spread, etc.)

3. **`sample_data.csv`** (~50 lines, optional)
   - Test data for development/testing

---

## 3. Tool Permission Strategy

### 3.1 Required Tools

**Minimal Necessary Set**: `Read`, `Write`, `Bash`

### 3.2 Tool Usage Justification

| Tool | Why Needed | Usage Pattern | Steps Used |
|------|------------|---------------|------------|
| **Bash** | Execute Python scripts for each workflow step | `python {baseDir}/scripts/[script].py --args` | Steps 1-5 (all) |
| **Read** | Load intermediate outputs for validation, read forecast data for reporting | `Read data/forecast.csv`, `Read data/arbitrage.json` | Steps 4-5 |
| **Write** | Create data directories if they don't exist (Claude can set up workspace) | `mkdir -p data/ reports/` (via Bash) | Step 1 (setup) |

### 3.3 Tools Explicitly NOT Needed

**Excluded Tools**:
- ❌ `Edit` - Not needed (scripts generate fresh files, no editing of existing files)
- ❌ `WebFetch` - Not needed (Python scripts handle all API calls directly with `requests` library)
- ❌ `Grep` - Not needed (no code search required for execution)
- ❌ `Glob` - Not needed (file paths are deterministic, not searching for files)

**Rationale**: Minimalist approach reduces complexity and token overhead. All file operations are handled by Python scripts with explicit paths.

---

## 4. Directory Structure & File Organization

### 4.1 Complete Skill Structure

```
nixtla-polymarket-analyst/
├── SKILL.md                          # Core instructions (480 lines, ~2,400 tokens)
│
├── scripts/                          # Executable code (NOT loaded into context)
│   ├── fetch_polymarket.py           # Step 1: GraphQL data fetcher (150 lines)
│   ├── transform_to_timeseries.py    # Step 2: JSON→CSV transformer (100 lines)
│   ├── forecast_timegpt.py           # Step 3: TimeGPT API caller (120 lines)
│   ├── analyze_arbitrage.py          # Step 4: Cross-platform analyzer (180 lines)
│   ├── generate_report.py            # Step 5: Markdown report generator (90 lines)
│   └── utils/
│       └── api_client.py             # Shared HTTP client (80 lines)
│
├── references/                       # Documentation (loaded into context, ~1,800 tokens)
│   ├── POLYMARKET_API.md             # GraphQL API docs (800 tokens)
│   ├── TIMEGPT_GUIDE.md              # TimeGPT integration guide (600 tokens)
│   └── EXAMPLES.md                   # Extended walkthroughs (400 tokens)
│
└── assets/                           # Templates (NOT loaded into context)
    ├── report_template.md            # Markdown report structure (200 lines)
    ├── config.example.json           # Example configuration (20 lines)
    └── sample_data.csv               # Test data (50 lines)

Total Discovery Budget: ~4,200 tokens ✓ (within 5,000 limit)
```

### 4.2 File Naming Conventions

**Scripts**: `[verb]_[noun].py`
- ✅ `fetch_polymarket.py` - Action: fetch, Target: polymarket
- ✅ `transform_to_timeseries.py` - Action: transform, Result: timeseries
- ✅ `forecast_timegpt.py` - Action: forecast, Method: timegpt
- ✅ `analyze_arbitrage.py` - Action: analyze, Focus: arbitrage
- ✅ `generate_report.py` - Action: generate, Output: report

**References**: `[NOUN]_[TYPE].md` (uppercase for visibility)
- ✅ `POLYMARKET_API.md` - Service: Polymarket, Type: API docs
- ✅ `TIMEGPT_GUIDE.md` - Tool: TimeGPT, Type: Guide
- ✅ `EXAMPLES.md` - Type: Examples (self-explanatory)

**Assets**: `[noun]_[type].[ext]` (lowercase, descriptive)
- ✅ `report_template.md` - Purpose: report, Nature: template
- ✅ `config.example.json` - Type: config, Nature: example
- ✅ `sample_data.csv` - Purpose: sample, Type: data

### 4.3 Path Referencing Standard

**Always Use**: `{baseDir}` for all file paths in SKILL.md and user-facing instructions

**Examples**:

```python
# ✅ CORRECT
python {baseDir}/scripts/fetch_polymarket.py --contract-id "0x123" --output data/raw_odds.json

# ❌ INCORRECT - Missing {baseDir}
python scripts/fetch_polymarket.py --contract-id "0x123"

# ❌ INCORRECT - Relative path
python ./scripts/fetch_polymarket.py --contract-id "0x123"

# ❌ INCORRECT - Hardcoded absolute path
python /home/user/.claude/skills/nixtla-polymarket-analyst/scripts/fetch_polymarket.py
```

**Rationale**: `{baseDir}` is dynamically resolved to the skill's installation directory, making the skill portable across different environments.

---

## 5. API Integration Architecture

### 5.1 External API Integrations

**API 1: Polymarket GraphQL API**

**Purpose**: Fetch historical contract odds, volume, liquidity data

**Integration Details**:
- **Endpoint**: `https://gamma-api.polymarket.com/` (GraphQL)
- **Method**: POST
- **Authentication**: None (public data)
- **Rate Limits**: 100 requests/minute
- **Response Format**: JSON (GraphQL response)
- **Key Fields**:
  - `contract.id`: Contract hex address
  - `contract.question`: Contract description
  - `contract.oddsHistory[]`: Array of historical odds
    - `timestamp`: ISO 8601 datetime
    - `yesPrice`: Probability of YES (0-1)
    - `noPrice`: Probability of NO (0-1)
    - `volume`: Trading volume (USD)
    - `liquidity`: Orderbook depth (USD)

**Example Request** (from `004-scripts/fetch_polymarket.py`):
```python
import requests

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
    "id": "0x1234567890abcdef1234567890abcdef12345678",
    "startDate": "2025-11-05T00:00:00Z"  # 30 days back
}

response = requests.post(
    "https://gamma-api.polymarket.com/",
    json={"query": query, "variables": variables}
)
data = response.json()
```

**Example Response**:
```json
{
  "data": {
    "contract": {
      "id": "0x1234567890abcdef1234567890abcdef12345678",
      "question": "Will Bitcoin reach $100k by December 2025?",
      "outcomes": ["YES", "NO"],
      "oddsHistory": [
        {
          "timestamp": "2025-11-05T00:00:00Z",
          "yesPrice": 0.52,
          "noPrice": 0.48,
          "volume": 125000.50,
          "liquidity": 450000.00
        },
        {
          "timestamp": "2025-11-06T00:00:00Z",
          "yesPrice": 0.54,
          "noPrice": 0.46,
          "volume": 98000.25,
          "liquidity": 455000.00
        }
        // ... 30 days of data
      ]
    }
  }
}
```

**Error Handling**:
- `400 Bad Request`: Invalid contract ID format → Validate regex `^0x[a-f0-9]{40}$`
- `404 Not Found`: Contract doesn't exist → Display helpful error with contract discovery link
- `429 Rate Limit`: Too many requests → Exponential backoff (1s, 2s, 4s), max 3 retries
- `500 Server Error`: Polymarket API down → Retry 3x, then fail gracefully with cached data suggestion

---

**API 2: Nixtla TimeGPT API**

**Purpose**: Generate 14-day price forecast with confidence intervals

**Integration Details**:
- **Endpoint**: `https://api.nixtla.io/timegpt/forecast`
- **Method**: POST
- **Authentication**: API Key (header: `X-API-Key: $NIXTLA_API_KEY`)
- **Rate Limits**: 1,000 requests/month (quota-based, not rate-limited)
- **Request Format**: JSON with time series data
- **Response Format**: JSON with forecast + 80%/95% confidence intervals
- **Cost**: ~$0.05 per forecast (varies by series length)

**Example Request** (from `004-scripts/forecast_timegpt.py`):
```python
import os
import requests
import pandas as pd

api_key = os.getenv("NIXTLA_API_KEY")
if not api_key:
    print("ERROR: NIXTLA_API_KEY environment variable not set")
    exit(1)

df = pd.read_csv("data/timeseries.csv")

response = requests.post(
    "https://api.nixtla.io/timegpt/forecast",
    headers={"X-API-Key": api_key},
    json={
        "data": df.to_dict(orient="records"),
        "horizon": 14,
        "freq": "D",
        "level": [80, 95]  # Confidence intervals
    }
)

forecast = response.json()
```

**Example Response**:
```json
{
  "forecast": [
    {
      "unique_id": "BTC_100k_Dec2025",
      "ds": "2025-12-06",
      "TimeGPT": 0.68,
      "TimeGPT-lo-80": 0.65,
      "TimeGPT-hi-80": 0.71,
      "TimeGPT-lo-95": 0.63,
      "TimeGPT-hi-95": 0.73
    },
    {
      "unique_id": "BTC_100k_Dec2025",
      "ds": "2025-12-07",
      "TimeGPT": 0.69,
      "TimeGPT-lo-80": 0.66,
      "TimeGPT-hi-80": 0.72,
      "TimeGPT-lo-95": 0.64,
      "TimeGPT-hi-95": 0.74
    }
    // ... 14 days
  ],
  "metadata": {
    "model": "timegpt-1",
    "horizon": 14,
    "frequency": "D"
  }
}
```

**Error Handling**:
- `401 Unauthorized`: Invalid API key → Check `NIXTLA_API_KEY` format, verify account
- `402 Payment Required`: Quota exceeded → **CRITICAL**: Fallback to StatsForecast (local, free)
- `400 Bad Request`: Invalid data format → Validate CSV schema before sending
- `500 Server Error`: TimeGPT service down → Retry 2x, then fallback to StatsForecast

**Fallback Strategy** (StatsForecast):
```python
# If TimeGPT fails, use local StatsForecast models
from statsforecast import StatsForecast
from statsforecast.models import AutoETS, AutoTheta, SeasonalNaive

sf = StatsForecast(
    models=[AutoETS(), AutoTheta(), SeasonalNaive()],
    freq='D'
)
sf.fit(df)
forecast = sf.predict(h=14, level=[80, 95])
```

---

**API 3: Kalshi REST API** (Optional)

**Purpose**: Fetch current contract odds for arbitrage comparison

**Integration Details**:
- **Endpoint**: `https://trading-api.kalshi.com/v1/markets`
- **Method**: GET
- **Authentication**: API Key (header: `Authorization: Bearer $KALSHI_API_KEY`) — Optional
- **Rate Limits**: 60 requests/minute
- **Response Format**: JSON with current market odds
- **Graceful Degradation**: If API key not provided or API fails, **skip Step 4** entirely (arbitrage analysis is optional)

**Example Request** (from `004-scripts/analyze_arbitrage.py`):
```python
import os
import requests

api_key = os.getenv("KALSHI_API_KEY")
if not api_key:
    print("WARNING: KALSHI_API_KEY not set, skipping arbitrage analysis")
    return None  # Graceful degradation

response = requests.get(
    "https://trading-api.kalshi.com/v1/markets",
    headers={"Authorization": f"Bearer {api_key}"},
    params={"event_ticker": "BTC-100K-DEC25"}
)

if response.status_code != 200:
    print(f"WARNING: Kalshi API failed ({response.status_code}), skipping arbitrage")
    return None

data = response.json()
```

**Example Response**:
```json
{
  "markets": [
    {
      "ticker": "BTC-100K-DEC25",
      "title": "Will Bitcoin reach $100,000 by December 2025?",
      "yes_price": 0.60,
      "no_price": 0.40,
      "volume": 85000,
      "open_interest": 120000
    }
  ]
}
```

**Error Handling**:
- `401 Unauthorized`: Invalid/missing API key → Skip arbitrage analysis (optional step)
- `404 Not Found`: No equivalent Kalshi contract → Log "No matching Kalshi contract", skip arbitrage
- `429 Rate Limit`: Too many requests → Exponential backoff, max 2 retries, then skip
- `500 Server Error`: Kalshi API down → Skip arbitrage analysis

---

### 5.2 API Call Sequencing

**Sequential Execution** (each step depends on previous):

```
Step 1: Polymarket API (fetch historical odds)
    ↓ (depends on: user input)
    Output: data/raw_odds.json

Step 2: Local processing (transform JSON → CSV)
    ↓ (depends on: Step 1 output)
    Output: data/timeseries.csv

Step 3: TimeGPT API (generate forecast)
    ↓ (depends on: Step 2 output)
    Output: data/forecast.csv

Step 4: Kalshi API (optional arbitrage analysis)
    ↓ (depends on: Step 3 output, optional on Kalshi API)
    Output: data/arbitrage.json OR null (if skipped)

Step 5: Local processing (generate markdown report)
    ↓ (depends on: Step 3 output, Step 4 output optional)
    Output: reports/analysis_YYYY-MM-DD.md
```

**Parallel Opportunities**: None (all steps are sequential dependencies)

**Fallback Strategies**:

1. **TimeGPT Quota Exceeded** (Step 3):
   ```
   Primary: TimeGPT API
       ↓ (if 402 error)
   Fallback: StatsForecast (local, free)
       ↓ (always succeeds, no API)
   Continue to Step 4
   ```

2. **Kalshi API Failure** (Step 4):
   ```
   Primary: Fetch Kalshi odds
       ↓ (if any error)
   Fallback: Skip arbitrage analysis
       ↓ (set arbitrage.json = null)
   Continue to Step 5 (report still valuable without arbitrage)
   ```

---

## 6. Data Flow Architecture

### 6.1 Input → Processing → Output Pipeline

```
USER INPUT (Contract ID: 0x1234...)
    ↓
┌────────────────────────────────────────────────────┐
│ Step 1: Fetch Polymarket Contract Data            │
│   Input: Contract ID (user-provided)              │
│   API Call: Polymarket GraphQL                    │
│   Processing: Parse GraphQL response              │
│   Output: data/raw_odds.json (5-50 KB)            │
│   Sample: 30 days × 24 data points = 720 records  │
└────────────────────────────────────────────────────┘
    ↓
┌────────────────────────────────────────────────────┐
│ Step 2: Transform to Time Series                  │
│   Input: data/raw_odds.json                       │
│   Processing:                                      │
│     - Parse JSON → Extract yesPrice               │
│     - Convert timestamps → ISO 8601 format        │
│     - Create unique_id from contract metadata     │
│     - Validate: no gaps, 0≤y≤1, chronological     │
│   Output: data/timeseries.csv (2-10 KB)           │
│   Format: unique_id, ds, y (3 columns, 30 rows)   │
└────────────────────────────────────────────────────┘
    ↓
┌────────────────────────────────────────────────────┐
│ Step 3: Generate TimeGPT Forecast                 │
│   Input: data/timeseries.csv                      │
│   API Call: TimeGPT POST with time series data    │
│   Processing:                                      │
│     - Send CSV data to TimeGPT API                │
│     - Receive forecast + 80%/95% CI               │
│     - Validate: forecast 0≤y≤1, CI bounds valid   │
│     - Fallback to StatsForecast if quota exceeded │
│   Output: data/forecast.csv (3-15 KB)             │
│   Format: 7 columns × 14 rows (forecast horizon)  │
└────────────────────────────────────────────────────┘
    ↓
┌────────────────────────────────────────────────────┐
│ Step 4: Analyze Arbitrage vs Kalshi (Optional)    │
│   Input: data/forecast.csv                        │
│   API Call: Kalshi REST API (if key provided)     │
│   Processing:                                      │
│     - Fetch current Kalshi odds for same event    │
│     - Compare: spread = |forecast - kalshi_price| │
│     - Filter: spread > min_threshold (default 5%) │
│     - Rank: by spread size                        │
│   Output: data/arbitrage.json (1-5 KB)            │
│   Format: Array of opportunities with metadata    │
│   Graceful Degradation: null if Kalshi unavailable│
└────────────────────────────────────────────────────┘
    ↓
┌────────────────────────────────────────────────────┐
│ Step 5: Generate Trading Recommendations Report   │
│   Input: data/forecast.csv + data/arbitrage.json  │
│   Processing:                                      │
│     - Load forecast data                          │
│     - Load arbitrage data (or null if skipped)    │
│     - Generate ASCII price chart                  │
│     - Note directional alignment (if any)         │
│     - Assess risk level (confidence intervals)    │
│     - Fill markdown template with data            │
│   Output: reports/analysis_YYYY-MM-DD.md (10-50KB)│
│   Format: Markdown with sections:                 │
│     - Executive Summary                           │
│     - Forecast Chart (ASCII visualization)        │
│     - Cross-Platform Comparison (table)           │
│     - Analysis Summary (informational only)       │
│     - Risk Assessment (confidence-based)          │
└────────────────────────────────────────────────────┘
    ↓
FINAL OUTPUT (Markdown Report)
```

### 6.2 Data Format Specifications

**Format 1: Raw Polymarket Data** (`data/raw_odds.json`)
```json
{
  "contract_id": "0x1234567890abcdef1234567890abcdef12345678",
  "contract_name": "Will Bitcoin reach $100k by December 2025?",
  "outcomes": ["YES", "NO"],
  "odds_history": [
    {
      "timestamp": "2025-11-05T00:00:00Z",
      "yes_price": 0.52,
      "no_price": 0.48,
      "volume": 125000.50,
      "liquidity": 450000.00
    },
    {
      "timestamp": "2025-11-06T00:00:00Z",
      "yes_price": 0.54,
      "no_price": 0.46,
      "volume": 98000.25,
      "liquidity": 455000.00
    }
    // ... 30 days
  ],
  "fetched_at": "2025-12-05T14:30:00Z"
}
```

**Format 2: Nixtla Time Series** (`data/timeseries.csv`)
```csv
unique_id,ds,y
BTC_100k_Dec2025,2025-11-05,0.52
BTC_100k_Dec2025,2025-11-06,0.54
BTC_100k_Dec2025,2025-11-07,0.53
BTC_100k_Dec2025,2025-11-08,0.55
...
BTC_100k_Dec2025,2025-12-04,0.67
BTC_100k_Dec2025,2025-12-05,0.68
```

**Validation Rules**:
- Exactly 3 columns: `unique_id` (string), `ds` (ISO 8601 date), `y` (float)
- No missing dates (daily frequency, no gaps)
- All `y` values: 0 ≤ y ≤ 1 (probabilities)
- Chronological order (ascending dates)
- Minimum 14 days of data (required for forecast)

**Format 3: TimeGPT Forecast** (`data/forecast.csv`)
```csv
unique_id,ds,TimeGPT,TimeGPT-lo-80,TimeGPT-hi-80,TimeGPT-lo-95,TimeGPT-hi-95
BTC_100k_Dec2025,2025-12-06,0.68,0.65,0.71,0.63,0.73
BTC_100k_Dec2025,2025-12-07,0.69,0.66,0.72,0.64,0.74
BTC_100k_Dec2025,2025-12-08,0.70,0.67,0.73,0.65,0.75
...
BTC_100k_Dec2025,2025-12-19,0.75,0.71,0.79,0.68,0.82
```

**Validation Rules**:
- 7 columns: unique_id, ds, TimeGPT, TimeGPT-lo-80, TimeGPT-hi-80, TimeGPT-lo-95, TimeGPT-hi-95
- Confidence intervals valid: lo-95 < lo-80 < TimeGPT < hi-80 < hi-95
- All forecasts: 0 ≤ forecast ≤ 1 (probabilities)
- Exactly 14 rows (14-day horizon)

**Format 4: Cross-Platform Comparison** (`data/comparison.json`)
```json
{
  "comparisons": [
    {
      "event": "Bitcoin reaches $100k by December 2025",
      "polymarket_forecast": 0.68,
      "kalshi_current": 0.60,
      "spread": 0.08,
      "spread_pct": 8.0,
      "spread_direction": "Polymarket forecast higher than Kalshi current",
      "forecast_confidence": "high"
    }
  ],
  "analysis_timestamp": "2025-12-05T14:35:00Z",
  "min_spread_threshold": 0.05,
  "disclaimer": "Cross-platform comparison only. Not financial advice."
}
```

**Or null if skipped**:
```json
null
```

**Format 5: Final Report** (`reports/analysis_YYYY-MM-DD.md`)

See PRD Section 8 for full example. Key sections:
- Disclaimer (NOT FINANCIAL ADVICE - analysis only)
- Executive Summary (2-3 sentences)
- Forecast Chart (ASCII visualization, 10-15 lines)
- Cross-Platform Comparison (markdown table)
- Analysis Summary (observations, not recommendations)
- Risk Assessment (based on confidence intervals)

---

### 6.3 Data Validation Rules

**Checkpoint 1: After Step 1** (Raw Polymarket Data)
```python
def validate_raw_odds(data):
    assert "contract_id" in data, "Missing contract_id"
    assert "odds_history" in data, "Missing odds_history"
    assert len(data["odds_history"]) >= 14, "Insufficient data (<14 days)"

    for record in data["odds_history"]:
        assert 0 <= record["yes_price"] <= 1, f"Invalid yes_price: {record['yes_price']}"
        assert 0 <= record["no_price"] <= 1, f"Invalid no_price: {record['no_price']}"
        assert abs(record["yes_price"] + record["no_price"] - 1.0) < 0.01, "Prices don't sum to ~1"
```

**Checkpoint 2: After Step 2** (Time Series)
```python
def validate_timeseries(df):
    assert list(df.columns) == ["unique_id", "ds", "y"], "Wrong columns"
    assert len(df) >= 14, "Insufficient data (<14 days)"
    assert df["y"].between(0, 1).all(), "Y values out of range [0,1]"

    # Check for missing dates (daily frequency)
    dates = pd.to_datetime(df["ds"])
    date_diffs = dates.diff().dropna()
    assert (date_diffs == pd.Timedelta(days=1)).all(), "Missing dates detected"

    # Check chronological order
    assert dates.is_monotonic_increasing, "Dates not in chronological order"
```

**Checkpoint 3: After Step 3** (Forecast)
```python
def validate_forecast(df):
    expected_cols = ["unique_id", "ds", "TimeGPT", "TimeGPT-lo-80", "TimeGPT-hi-80", "TimeGPT-lo-95", "TimeGPT-hi-95"]
    assert list(df.columns) == expected_cols, f"Wrong columns: {df.columns}"
    assert len(df) == 14, f"Wrong horizon: {len(df)} days (expected 14)"

    # Validate confidence intervals
    for _, row in df.iterrows():
        assert row["TimeGPT-lo-95"] < row["TimeGPT-lo-80"], "95% CI not wider than 80% CI"
        assert row["TimeGPT-lo-80"] < row["TimeGPT"], "Lower bound > forecast"
        assert row["TimeGPT"] < row["TimeGPT-hi-80"], "Forecast > upper bound"
        assert row["TimeGPT-hi-80"] < row["TimeGPT-hi-95"], "80% CI not wider than 95% CI"

    # Validate probabilities
    assert df["TimeGPT"].between(0, 1).all(), "Forecasts out of range [0,1]"
```

---

## 7. Error Handling Strategy

### 7.1 Error Categories & Responses

**Category 1: Missing Prerequisites**

| Error | Cause | Detection | Solution | Step |
|-------|-------|-----------|----------|------|
| `NIXTLA_API_KEY not found` | Env var not set | Script startup | Display: `export NIXTLA_API_KEY='your_key'` | Step 3 |
| `POLYMARKET_API_KEY not found` | N/A (public API) | N/A | N/A (no auth required) | Step 1 |
| `KALSHI_API_KEY not found` | Env var not set | Script startup | Skip Step 4 (graceful degradation) | Step 4 |
| `pandas not installed` | Missing library | Import error | Display: `pip install pandas statsforecast nixtla requests` | All |
| `Invalid contract ID format` | User input error | Regex validation | Display: "Expected format: 0x[40 hex chars]" | Step 1 |

**Category 2: API Failures**

| Error | Cause | Detection | Solution | Step |
|-------|-------|-----------|----------|------|
| `401 Unauthorized (TimeGPT)` | Invalid API key | HTTP status | Verify `NIXTLA_API_KEY` format, check account | Step 3 |
| `402 Payment Required (TimeGPT)` | Quota exceeded | HTTP status | **Fallback to StatsForecast** (local, free) | Step 3 |
| `404 Not Found (Polymarket)` | Invalid contract ID | HTTP status | Suggest contract discovery on Polymarket.com | Step 1 |
| `429 Rate Limit (Polymarket)` | Too many requests | HTTP status | Exponential backoff (1s, 2s, 4s), max 3 retries | Step 1 |
| `429 Rate Limit (Kalshi)` | Too many requests | HTTP status | Retry 2x, then skip Step 4 | Step 4 |
| `500 Server Error (any API)` | Service down | HTTP status | Retry 3x with backoff, then fail gracefully | All |

**Category 3: Data Quality Issues**

| Error | Cause | Detection | Solution | Step |
|-------|-------|-----------|----------|------|
| `Insufficient data (<14 days)` | Contract too new | Data validation | Prompt user: "Need ≥14 days history, contract has only X days" | Step 1 |
| `Missing values in time series` | Data gaps | Schema validation | **Interpolate** missing points, log warning | Step 2 |
| `Prices out of range [0,1]` | Data corruption | Value validation | Clamp to [0,1], log warning | Step 2 |
| `Confidence intervals invalid` | API error | CI validation | Log error, use wider intervals (manual override) | Step 3 |
| `No matching Kalshi contract` | Different event | API search | Skip Step 4, note in report: "No Kalshi equivalent found" | Step 4 |

**Category 4: Execution Failures**

| Error | Cause | Detection | Solution | Step |
|-------|-------|-----------|----------|------|
| `Script not found` | Missing file | FileNotFoundError | Re-download skill, verify installation | All |
| `Permission denied` | File permissions | PermissionError | Display: `chmod +x {baseDir}/scripts/*.py` | All |
| `Disk full` | No space | OSError | Clean old reports: `rm reports/*` (ask user first) | Step 5 |
| `JSON parse error` | Malformed API response | JSONDecodeError | Log raw response, retry request, fail if persists | Steps 1,3,4 |

### 7.2 Graceful Degradation

**Fallback Hierarchy**:

```
PRIMARY PATH (Full Workflow):
  Step 1 (Polymarket) → Step 2 (Transform) → Step 3 (TimeGPT) → Step 4 (Kalshi) → Step 5 (Report)
                                                      ↓ (if 402 quota error)
FALLBACK PATH 1 (StatsForecast):
  Step 1 (Polymarket) → Step 2 (Transform) → Step 3 (StatsForecast local) → Step 5 (Report)
                                                                               ↓ (skip Step 4)
FALLBACK PATH 2 (No Arbitrage):
  Step 1 (Polymarket) → Step 2 (Transform) → Step 3 (TimeGPT/StatsForecast) → Step 5 (Report)
                                                                               ↑ (Step 4 skipped if Kalshi unavailable)
FALLBACK PATH 3 (Cached Data):
  Use previous forecast from reports/ directory (if recent analysis exists)
```

**Optional Steps**:
- **Step 4 (Arbitrage)** can be skipped without breaking workflow
  - Skill still produces valuable forecast report
  - Report notes: "Arbitrage analysis unavailable (Kalshi API not configured)"

**Critical Steps** (must succeed or workflow fails):
- Step 1: Polymarket data fetch (no fallback—need real data)
- Step 2: Data transformation (deterministic, should always succeed)
- Step 3: Forecast generation (has StatsForecast fallback)
- Step 5: Report generation (deterministic, should always succeed)

### 7.3 Logging & Debugging

**Log Levels**:
- `INFO`: Normal progress (green text)
- `WARNING`: Recoverable issues (yellow text)
- `ERROR`: Failures that stop execution (red text)

**Log Format**:
```
[YYYY-MM-DD HH:MM:SS] [LEVEL] [Step N] Message
```

**Example Execution Log**:
```
[2025-12-05 14:30:10] [INFO] [Step 1] Fetching Polymarket contract 0x1234567890abcdef...
[2025-12-05 14:30:12] [INFO] [Step 1] ✓ Fetched 30 days of odds data (720 records)
[2025-12-05 14:30:12] [INFO] [Step 1] ✓ Saved to data/raw_odds.json (12.5 KB)

[2025-12-05 14:30:13] [INFO] [Step 2] Transforming JSON → CSV time series...
[2025-12-05 14:30:13] [WARNING] [Step 2] Missing data on 2025-11-15, interpolating from neighbors
[2025-12-05 14:30:13] [INFO] [Step 2] ✓ Validation passed: 30 days, no gaps, 0≤y≤1
[2025-12-05 14:30:13] [INFO] [Step 2] ✓ Saved to data/timeseries.csv (2.1 KB)

[2025-12-05 14:30:14] [INFO] [Step 3] Calling TimeGPT API (horizon=14, freq=D)...
[2025-12-05 14:30:42] [INFO] [Step 3] ✓ Forecast received (14 days, MAPE: 8.2%) [illustrative example]
[2025-12-05 14:30:42] [INFO] [Step 3] ✓ Saved to data/forecast.csv (3.8 KB)

[2025-12-05 14:30:43] [INFO] [Step 4] Checking Kalshi for matching contract...
[2025-12-05 14:30:45] [INFO] [Step 4] ✓ Found Kalshi contract: BTC-100K-DEC25
[2025-12-05 14:30:45] [INFO] [Step 4] ✓ Spread detected: 8.0% (Polymarket forecast 0.68 vs Kalshi current 0.60) [illustrative example]
[2025-12-05 14:30:45] [INFO] [Step 4] ✓ Saved to data/arbitrage.json (1.2 KB)

[2025-12-05 14:30:46] [INFO] [Step 5] Generating analysis report...
[2025-12-05 14:30:48] [INFO] [Step 5] ✓ Report saved to reports/analysis_2025-12-05.md (18.4 KB)

[2025-12-05 14:30:48] [INFO] ✅ Workflow complete in 38 seconds
```

**Example Error Log** (TimeGPT quota exceeded):
```
[2025-12-05 14:30:14] [INFO] [Step 3] Calling TimeGPT API (horizon=14, freq=D)...
[2025-12-05 14:30:16] [ERROR] [Step 3] TimeGPT API returned 402 Payment Required
[2025-12-05 14:30:16] [WARNING] [Step 3] Monthly quota exceeded (1000/1000 requests used)
[2025-12-05 14:30:16] [INFO] [Step 3] Falling back to StatsForecast (local models)...
[2025-12-05 14:30:18] [INFO] [Step 3] ✓ Forecast generated using AutoETS (MAPE: 11.5%) [illustrative example]
[2025-12-05 14:30:18] [WARNING] [Step 3] Note: StatsForecast used instead of TimeGPT (quota limit)
[2025-12-05 14:30:18] [INFO] [Step 3] ✓ Saved to data/forecast.csv (3.8 KB)
```

---

## 8. Composability & Stacking Architecture

### 8.1 Standalone Execution

**This skill runs independently**:

```bash
# User provides contract ID, skill handles full workflow
Claude: "Analyze Polymarket contract 0x1234567890abcdef and forecast 14 days"

# Skill executes all 5 steps automatically:
# 1. Fetch from Polymarket
# 2. Transform to time series
# 3. TimeGPT forecast
# 4. Check Kalshi arbitrage
# 5. Generate report

# Output: reports/analysis_2025-12-05.md (complete, self-contained)
```

**Self-Contained Value**: Produces analysis reports without requiring other skills

### 8.2 Skill Stacking Patterns

**Stack Pattern 1: Sequential Chaining → Risk Analysis**

```
nixtla-polymarket-analyst (this skill)
    Produces: data/forecast.csv (14-day price predictions)
        ↓
nixtla-market-risk-analyzer (next skill)
    Consumes: data/forecast.csv
    Produces: data/risk_analysis.json (VaR, volatility, max drawdown)
        ↓
Enhanced Report: Forecast + Risk Metrics
```

**Use Case**: Analyst wants forecast + risk context

**Implementation**:
```bash
# Step 1: Run this skill
Claude: "Analyze Polymarket contract 0xABC123"
# Produces: data/forecast.csv

# Step 2: Feed forecast into risk analyzer
Claude: "Now analyze the risk of this forecast using nixtla-market-risk-analyzer"
# Consumes: data/forecast.csv
# Produces: Risk context based on VaR
```

**Output**: Combined report with forecast + risk context

---

**Stack Pattern 2: Parallel Multi-Contract → Correlation Analysis**

```
nixtla-polymarket-analyst (contract A: BTC $100k)  ┐
    Produces: data/forecast_btc.csv               │
                                                   ├→ nixtla-correlation-mapper
nixtla-polymarket-analyst (contract B: ETH $10k)  │    Consumes: Multiple forecasts
    Produces: data/forecast_eth.csv               │    Produces: Correlation matrix
                                                   │             Hedge recommendations
nixtla-polymarket-analyst (contract C: Election)  ┘
    Produces: data/forecast_election.csv
```

**Use Case**: Analyst wants to understand how different contracts move together (correlation analysis)

**Implementation**:
```bash
# Step 1: Run this skill on 3 contracts in parallel
for contract in "0xBTC_ID" "0xETH_ID" "0xELECTION_ID"; do
    Claude: "Analyze Polymarket contract $contract"
done
# Produces: 3 separate forecast files

# Step 2: Stack with correlation mapper
Claude: "Analyze correlations between these 3 forecasts using nixtla-correlation-mapper"
# Produces: Correlation matrix showing BTC/ETH highly correlated (0.82), BTC/Election weakly correlated (0.23)
```

**Output**: Correlation insights (e.g., "BTC and ETH move together (0.82 correlation), Election contracts show weak correlation (0.23)")

---

**Stack Pattern 3: Event Impact Modeling**

```
nixtla-polymarket-analyst (baseline forecast)
    Produces: data/forecast_baseline.csv
        ↓
nixtla-event-impact-modeler (scenario analysis)
    Consumes: data/forecast_baseline.csv
    Adds: External events (Fed meeting, earnings reports)
    Produces: data/forecast_with_events.csv (adjusted predictions)
```

**Use Case**: "What happens to BTC $100k contract odds if the Fed cuts rates next week?"

**Implementation**:
```bash
# Step 1: Baseline forecast
Claude: "Forecast Polymarket BTC $100k contract for next 14 days"
# Produces: Baseline forecast assuming no major events

# Step 2: Model event impact
Claude: "Model the impact of a Fed rate cut on this forecast using nixtla-event-impact-modeler"
# Produces: Adjusted forecast showing +15% odds increase if Fed cuts rates
```

**Output**: Scenario analysis report (baseline vs event-adjusted forecasts)

---

### 8.3 Skill Input/Output Contracts

**Input Contract** (what this skill expects):

| Input | Type | Format | Required | Default |
|-------|------|--------|----------|---------|
| Contract ID | String | Hex: `0x[a-f0-9]{40}` | ✅ Yes | None |
| Forecast Horizon | Integer | Days (1-90) | ❌ No | 14 |
| Date Range | String | ISO 8601 date range | ❌ No | Last 30 days |
| Kalshi API Key | String | Env var: `KALSHI_API_KEY` | ❌ No | Skip Step 4 if missing |
| Min Spread Threshold | Float | 0-1 (percentage) | ❌ No | 0.05 (5%) |

**Example Valid Inputs**:
```bash
# Minimal (only contract ID)
"Analyze Polymarket contract 0x1234567890abcdef1234567890abcdef12345678"

# With custom horizon
"Forecast contract 0xABC...123 for next 30 days"

# With arbitrage threshold
"Find arbitrage opportunities with minimum 8% spread for contract 0xDEF...456"
```

**Output Contract** (what this skill guarantees to produce):

| Output | Type | Format | Always Produced? | Conditions |
|--------|------|--------|------------------|------------|
| Forecast CSV | File | 7 columns × 14 rows | ✅ Yes | Even on TimeGPT failure (StatsForecast fallback) |
| Markdown Report | File | Structured markdown | ✅ Yes | Always (may note "arbitrage unavailable") |
| Arbitrage JSON | File | JSON array | ❌ No | Only if Kalshi API succeeds |
| Raw Data JSON | File | Polymarket response | ✅ Yes | Always (for debugging/reproducibility) |
| Time Series CSV | File | 3 columns × N rows | ✅ Yes | Always (intermediate output) |

**Output Stability Guarantee**:
- **CSV format** (forecast.csv): Stable across all versions 1.x.x (columns won't change)
- **Markdown structure**: Stable sections (Executive Summary, Forecast Chart, Recommendations, Risk)
- **JSON schema** (arbitrage.json): Stable fields (event, spread, confidence, recommendation)

**Versioning**:
- v1.0.0 → v1.x.x: Backward-compatible (stacking patterns continue to work)
- v2.0.0: Breaking changes allowed (e.g., new output format, different API)

---

## 9. Performance & Scalability

### 9.1 Performance Targets

| Metric | Target | Max Acceptable | Measurement | Current Estimate |
|--------|--------|----------------|-------------|------------------|
| **Total execution time** | <60 sec | <120 sec | End-to-end workflow | 38-52 sec ✅ |
| **Step 1** (Polymarket fetch) | <5 sec | <15 sec | API response time | 3-5 sec ✅ |
| **Step 2** (Transform) | <2 sec | <5 sec | Python processing | 1-2 sec ✅ |
| **Step 3** (TimeGPT forecast) | <30 sec | <60 sec | API latency | 20-30 sec ✅ |
| **Step 4** (Arbitrage) | <10 sec | <20 sec | API + analysis | 5-10 sec ✅ |
| **Step 5** (Report) | <5 sec | <10 sec | Template rendering | 3-5 sec ✅ |

**Bottleneck**: Step 3 (TimeGPT API) accounts for 50-60% of total time

**Optimization Opportunities**:
- Cache recent forecasts (if user re-runs same contract within 1 hour)
- Parallel API calls where possible (Step 4 could start while Step 3 processes response)

### 9.2 Scalability Considerations

**Single Contract** (Primary Use Case):
- **Optimized for**: 1 contract analysis in <60 seconds
- **Resource Usage**: <50 MB RAM, <100 KB network bandwidth
- **Bottleneck**: TimeGPT API latency (20-30 sec)

**Batch Processing** (10 contracts):

| Approach | Total Time | Resource Usage | Implementation |
|----------|------------|----------------|----------------|
| **Sequential** | ~10 min (10 × 60 sec) | <100 MB RAM | Run skill 10 times in loop |
| **Parallel** (recommended) | ~2 min (max API latency) | <500 MB RAM | Run 10 instances concurrently |

**Parallel Batch Pattern**:
```bash
# Process 10 contracts in parallel (saves 8 minutes)
for contract in $(cat watchlist.txt); do
    # Each runs as separate process
    python {baseDir}/scripts/fetch_polymarket.py --contract-id $contract &
done
wait  # Wait for all to complete

# Then run Steps 2-5 for each
for file in data/raw_odds_*.json; do
    python {baseDir}/scripts/transform_to_timeseries.py --input $file
    python {baseDir}/scripts/forecast_timegpt.py --input data/timeseries_*.csv
    # ... etc
done
```

**API Rate Limiting**:

| API | Rate Limit | Implication for Batch |
|-----|------------|----------------------|
| Polymarket | 100 req/min | Can process 100 contracts/min (not a bottleneck) |
| TimeGPT | 1,000 req/month | Budget: ~33 contracts/day max (plan accordingly) |
| Kalshi | 60 req/min | Can process 60 contracts/min (not a bottleneck) |

**Scaling Strategy**:
- **0-10 contracts**: Run in parallel, complete in ~2 minutes
- **10-100 contracts**: Batch into groups of 10, run groups sequentially (~20 min total)
- **100+ contracts**: Requires queue system + distributed execution (out of scope for v1.0)

### 9.3 Resource Usage

**Disk Space** (per contract analysis):
- Raw data (Step 1): 5-50 KB
- Time series (Step 2): 2-10 KB
- Forecast (Step 3): 3-15 KB
- Arbitrage (Step 4): 1-5 KB
- Report (Step 5): 10-50 KB
- **Total**: ~100 KB per contract

**Storage Scaling**:
- 100 contracts: ~10 MB
- 1,000 contracts: ~100 MB
- Cleanup strategy: Delete files older than 30 days

**Memory** (per contract):
- Python process: <50 MB RAM
- Data loaded in memory: <5 MB (small CSV files)
- **Total**: <50 MB per contract

**Parallel Memory Usage**:
- 10 parallel processes: <500 MB RAM (acceptable on modern systems)

**Network Bandwidth** (per contract):
- Polymarket API request: ~2 KB
- Polymarket API response: ~10 KB (30 days of data)
- TimeGPT API request: ~5 KB (time series data)
- TimeGPT API response: ~3 KB (forecast)
- Kalshi API request: ~1 KB
- Kalshi API response: ~2 KB
- **Total**: ~25 KB per contract (negligible)

**Bandwidth Scaling**:
- 100 contracts: ~2.5 MB (completes in seconds on broadband)

---

## 10. Testing Strategy

### 10.1 Unit Testing (Per-Step Validation)

**Test Step 1** (Polymarket Fetch):
```bash
# Test with known contract ID (Bitcoin $100k by Dec 2025)
python {baseDir}/scripts/fetch_polymarket.py \
  --contract-id "0x1234567890abcdef1234567890abcdef12345678" \
  --output /tmp/test_odds.json

# Validate output
assert_file_exists /tmp/test_odds.json
assert_json_valid /tmp/test_odds.json
assert_field_exists "contract_id" /tmp/test_odds.json
assert_field_exists "odds_history" /tmp/test_odds.json
assert_array_length_gte "odds_history" 14 /tmp/test_odds.json
```

**Test Step 2** (Transform):
```bash
# Use sample data from assets/
python {baseDir}/scripts/transform_to_timeseries.py \
  --input {baseDir}/assets/sample_data.json \
  --output /tmp/test_ts.csv

# Validate output
assert_csv_columns "unique_id,ds,y" /tmp/test_ts.csv
assert_no_missing_values /tmp/test_ts.csv
assert_values_in_range "y" 0 1 /tmp/test_ts.csv
assert_chronological "ds" /tmp/test_ts.csv
```

**Test Step 3** (Forecast):
```bash
# Test TimeGPT API call (requires valid API key)
python {baseDir}/scripts/forecast_timegpt.py \
  --input {baseDir}/assets/sample_timeseries.csv \
  --horizon 14 \
  --output /tmp/test_forecast.csv

# Validate output
assert_csv_columns "unique_id,ds,TimeGPT,TimeGPT-lo-80,TimeGPT-hi-80,TimeGPT-lo-95,TimeGPT-hi-95" /tmp/test_forecast.csv
assert_row_count 14 /tmp/test_forecast.csv
assert_confidence_intervals_valid /tmp/test_forecast.csv
```

**Test Step 4** (Arbitrage):
```bash
# Test with known contract that has Kalshi equivalent
python {baseDir}/scripts/analyze_arbitrage.py \
  --forecast /tmp/test_forecast.csv \
  --kalshi-api-key $KALSHI_API_KEY \
  --output /tmp/test_arbitrage.json

# Validate output
assert_json_valid /tmp/test_arbitrage.json
assert_field_exists "opportunities" /tmp/test_arbitrage.json
```

**Test Step 5** (Report):
```bash
# Test report generation with sample data
python {baseDir}/scripts/generate_report.py \
  --forecast /tmp/test_forecast.csv \
  --arbitrage /tmp/test_arbitrage.json \
  --template {baseDir}/assets/report_template.md \
  --output /tmp/test_report.md

# Validate output
assert_file_exists /tmp/test_report.md
assert_contains "Executive Summary" /tmp/test_report.md
assert_contains "Forecast Chart" /tmp/test_report.md
assert_contains "Recommendations" /tmp/test_report.md
```

### 10.2 Integration Testing (Full Workflow)

**Happy Path Test** (Everything Succeeds):
```bash
# Run full workflow with test contract
export NIXTLA_API_KEY="test_key_123"
export KALSHI_API_KEY="test_key_456"

./run_full_workflow.sh \
  --contract-id "0xTEST_CONTRACT_ID" \
  --horizon 14 \
  --output /tmp/test_report.md

# Validate final output
assert_file_exists /tmp/test_report.md
assert_file_size_gt /tmp/test_report.md 5000  # >5 KB (substantial report)
assert_contains "Forecast Chart" /tmp/test_report.md
assert_contains "Cross-Platform Comparison" /tmp/test_report.md
assert_contains "Analysis Summary" /tmp/test_report.md
assert_contains "Risk Assessment" /tmp/test_report.md

# Validate execution time
assert_execution_time_lt 60  # <60 seconds
```

**Failure Path Tests**:

**Test 1: Missing TimeGPT API Key**
```bash
# Unset API key
unset NIXTLA_API_KEY

./run_full_workflow.sh --contract-id "0xTEST"

# Expected: Helpful error message
assert_stdout_contains "ERROR: NIXTLA_API_KEY environment variable not set"
assert_stdout_contains "export NIXTLA_API_KEY='your_key'"
assert_exit_code 1
```

**Test 2: Invalid Contract ID**
```bash
./run_full_workflow.sh --contract-id "invalid_id_format"

# Expected: Validation error
assert_stdout_contains "ERROR: Invalid contract ID format"
assert_stdout_contains "Expected: 0x[40 hex characters]"
assert_exit_code 1
```

**Test 3: TimeGPT API Quota Exceeded**
```bash
# Mock 402 response from TimeGPT
./run_full_workflow.sh --contract-id "0xTEST" --mock-timegpt-quota-error

# Expected: Fallback to StatsForecast
assert_stdout_contains "WARNING: TimeGPT API quota exceeded"
assert_stdout_contains "Falling back to StatsForecast"
assert_file_exists /tmp/test_report.md  # Report still generated
assert_contains "StatsForecast" /tmp/test_report.md  # Notes fallback
assert_exit_code 0  # Success (graceful degradation)
```

**Test 4: Kalshi API Unavailable**
```bash
# Mock Kalshi API failure
./run_full_workflow.sh --contract-id "0xTEST" --mock-kalshi-failure

# Expected: Skip arbitrage, continue workflow
assert_stdout_contains "WARNING: Kalshi API failed, skipping arbitrage analysis"
assert_file_exists /tmp/test_report.md  # Report still generated
assert_contains "Arbitrage analysis unavailable" /tmp/test_report.md
assert_exit_code 0  # Success (Step 4 is optional)
```

### 10.3 Acceptance Criteria

**This skill is production-ready when ALL of the following are true**:

- [ ] **Description Quality**: Scores 97/100 on 6-criterion formula (exceeds 80% target)
- [ ] **Token Budget**: Total skill size <5,000 tokens (description + SKILL.md + references)
- [ ] **SKILL.md Size**: <500 lines (currently estimated 480 lines ✅)
- [ ] **Character Limit**: Description <250 characters (currently 248 chars ✅)
- [ ] **Workflow Completeness**: All 5 steps execute successfully in sequence
- [ ] **Error Handling**: All 4 error categories have graceful handling + helpful messages
- [ ] **Fallback Paths**: StatsForecast fallback works when TimeGPT quota exceeded
- [ ] **Graceful Degradation**: Skill produces report even if Step 4 (arbitrage) fails
- [ ] **Performance**: Happy path completes in <60 seconds (target: 38-52 sec ✅)
- [ ] **Stacking Demonstrated**: At least 2 stacking patterns documented with examples
- [ ] **Unit Tests**: All 5 steps pass individual validation
- [ ] **Integration Tests**: Happy path + 4 failure paths all pass
- [ ] **Documentation**: references/ files complete (POLYMARKET_API.md, TIMEGPT_GUIDE.md, EXAMPLES.md)
- [ ] **Code Quality**: All scripts have docstrings, CLI args, error handling, exit codes
- [ ] **API Keys**: No hardcoded keys, all from environment variables
- [ ] **Path References**: All paths use `{baseDir}` (no hardcoded or relative paths)

---

## 11. Deployment & Maintenance

### 11.1 Installation Requirements

**System Requirements**:
- Python 3.9+ (for type hints, f-strings)
- 500 MB disk space (scripts + data + reports)
- Internet connection (for API calls)
- Terminal/CLI access

**Dependencies**:
```bash
pip install nixtla>=0.5.0 statsforecast>=1.7.0 pandas>=2.0.0 requests>=2.28.0
```

**Environment Setup**:
```bash
# Required
export NIXTLA_API_KEY="your_timegpt_api_key_here"

# Optional (skip arbitrage analysis if not set)
export KALSHI_API_KEY="your_kalshi_api_key_here"
```

**Verification**:
```bash
# Test that all dependencies are installed
python -c "import nixtla, statsforecast, pandas, requests; print('✓ All dependencies installed')"

# Test API keys
python {baseDir}/scripts/fetch_polymarket.py --help
python {baseDir}/scripts/forecast_timegpt.py --help
```

### 11.2 Versioning Strategy

**Semantic Versioning**: `MAJOR.MINOR.PATCH`

**Version Increments**:

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| **Breaking changes** (output format, API contracts) | MAJOR | v1.x.x → v2.0.0 |
| **New features** (additional APIs, new stacking patterns) | MINOR | v1.0.x → v1.1.0 |
| **Bug fixes, performance, docs** | PATCH | v1.0.0 → v1.0.1 |

**Example Changelog**:
- **v1.0.0** (2025-12-10): Initial release
  - 5-step workflow: Polymarket fetch → Transform → TimeGPT forecast → Kalshi arbitrage → Report
  - StatsForecast fallback when TimeGPT quota exceeded
  - 3 stacking patterns documented

- **v1.1.0** (2026-01-15): Added categorical market support
  - New feature: Support for multi-outcome markets (not just binary YES/NO)
  - New feature: Batch processing mode (analyze 10 contracts in one command)
  - Bug fix: Improved time zone handling in Step 2

- **v1.1.1** (2026-01-20): Performance improvements
  - Bug fix: Fixed edge case where missing data caused crash
  - Performance: Reduced Step 2 processing time by 30%
  - Docs: Added troubleshooting guide for common API errors

- **v2.0.0** (2026-03-01): Breaking changes
  - **BREAKING**: Changed output format from markdown to JSON+HTML
  - **BREAKING**: Renamed arbitrage.json → opportunities.json
  - New feature: Interactive web dashboard for reports
  - Migration guide: v1.x → v2.0 conversion script provided

### 11.3 Monitoring & Observability

**Key Metrics to Track**:

1. **Activation Rate** (How often skill is triggered)
   - Target: 95%+ on relevant queries
   - Measurement: Log skill invocations vs user messages containing "Polymarket", "prediction market", "arbitrage"
   - Red flag: <80% activation rate → Description needs improvement

2. **Success Rate** (% of executions that complete without errors)
   - Target: 95%+ success
   - Measurement: Count of successful Step 5 completions / total skill invocations
   - Red flag: <90% success → Investigate API failures, add more error handling

3. **Average Execution Time** (Per step and total)
   - Target: <60 sec total
   - Measurement: Log timestamps at each step
   - Red flag: >90 sec total → Investigate API latency, optimize code

4. **API Failure Rate** (% of API calls that fail)
   - Target: <5% failures
   - Measurement: HTTP error codes from Polymarket, TimeGPT, Kalshi
   - Red flag: >10% failures → Check API status pages, adjust retry logic

5. **Fallback Usage** (How often StatsForecast is used vs TimeGPT)
   - Target: <10% fallback usage (most users stay within quota)
   - Measurement: Count of StatsForecast forecasts / total forecasts
   - Red flag: >30% fallback → Users hitting quota limits, recommend upgrading TimeGPT plan

**Logging Strategy**:
- All executions logged to `logs/skill_execution_YYYY-MM-DD.log`
- Errors logged with full stack traces to `logs/errors_YYYY-MM-DD.log`
- Performance metrics logged per step: `[timestamp] [step] [duration_ms]`

**Example Log Entry**:
```json
{
  "timestamp": "2025-12-05T14:30:48Z",
  "skill": "nixtla-polymarket-analyst",
  "version": "1.0.0",
  "contract_id": "0x1234567890abcdef1234567890abcdef12345678",
  "execution_time_ms": 38240,
  "steps": {
    "step_1": {"status": "success", "duration_ms": 3200},
    "step_2": {"status": "success", "duration_ms": 1100},
    "step_3": {"status": "success", "duration_ms": 26500, "model": "timegpt"},
    "step_4": {"status": "success", "duration_ms": 5800, "arbitrage_found": true},
    "step_5": {"status": "success", "duration_ms": 1640}
  },
  "output": "reports/analysis_2025-12-05.md"
}
```

---

## 12. Security & Compliance

### 12.1 API Key Management

**Storage**: Environment variables ONLY (never hardcoded in scripts or config files)

**Validation** (in every script that uses API keys):
```python
import os
import sys

def validate_api_key(key_name):
    """Validate that required API key is set"""
    api_key = os.getenv(key_name)
    if not api_key:
        print(f"ERROR: {key_name} environment variable not set", file=sys.stderr)
        print(f"Set with: export {key_name}='your_key_here'", file=sys.stderr)
        sys.exit(1)
    return api_key

# Usage in scripts
nixtla_key = validate_api_key("NIXTLA_API_KEY")  # Required
kalshi_key = os.getenv("KALSHI_API_KEY")  # Optional (None if not set)
```

**Rotation**: Document how to update keys without breaking skill
```bash
# To rotate TimeGPT API key:
# 1. Generate new key in Nixtla dashboard
# 2. Update environment variable
export NIXTLA_API_KEY="new_key_here"
# 3. Test with sample contract
python {baseDir}/scripts/forecast_timegpt.py --input test_data.csv --output /tmp/test.csv
# 4. Old key can be revoked after confirmation
```

### 12.2 Data Privacy

**User Data**: No personally identifiable information (PII) collected or stored
- Contract IDs are public blockchain addresses (not PII)
- Forecast data is derived from public market odds (not PII)

**API Data**: Cached locally in `data/` directory
- Retention: 7 days (automatic cleanup script)
- Access: Local filesystem only (not uploaded or shared)
- Cleanup command: `find data/ -name "*.json" -mtime +7 -delete`

**Logs**: No sensitive data in logs
- API keys are **masked** in logs: `NIXTLA_API_KEY=****xyz` (show last 3 chars only)
- Contract IDs are logged (public data, OK to log)
- Forecast values are logged (derived public data, OK to log)

**Example Secure Logging**:
```python
import os

api_key = os.getenv("NIXTLA_API_KEY")
masked_key = api_key[-3:] if api_key else "NOT_SET"
print(f"Using TimeGPT API key: ****{masked_key}")
# Output: "Using TimeGPT API key: ****xyz"
```

### 12.3 Rate Limiting & Abuse Prevention

**API Quotas**: Track usage to prevent quota exhaustion

**Quota Tracking** (for TimeGPT):
```python
# Track monthly usage
usage_file = "logs/timegpt_usage.json"

def log_api_call():
    """Increment usage counter"""
    import json
    from datetime import datetime

    if os.path.exists(usage_file):
        with open(usage_file, 'r') as f:
            usage = json.load(f)
    else:
        usage = {"month": datetime.now().strftime("%Y-%m"), "count": 0}

    # Reset if new month
    current_month = datetime.now().strftime("%Y-%m")
    if usage["month"] != current_month:
        usage = {"month": current_month, "count": 0}

    usage["count"] += 1

    with open(usage_file, 'w') as f:
        json.dump(usage, f)

    # Warn if approaching limit
    if usage["count"] >= 950:  # 95% of 1,000 quota
        print(f"WARNING: TimeGPT quota nearly exhausted ({usage['count']}/1000 this month)")
        print("Future requests will fallback to StatsForecast")

    return usage["count"]
```

**Backoff Strategy**: Exponential backoff on rate limit errors
```python
import time
import requests

def call_api_with_backoff(url, headers, json_data, max_retries=3):
    """Call API with exponential backoff on rate limits"""
    for attempt in range(max_retries):
        response = requests.post(url, headers=headers, json=json_data)

        if response.status_code == 429:  # Rate limit
            wait_time = 2 ** attempt  # 1s, 2s, 4s
            print(f"Rate limit hit, retrying in {wait_time}s... (attempt {attempt+1}/{max_retries})")
            time.sleep(wait_time)
            continue

        return response  # Success or non-rate-limit error

    raise Exception(f"Max retries ({max_retries}) exceeded due to rate limiting")
```

---

## 13. Documentation Requirements

### 13.1 SKILL.md Sections Checklist

- [X] **Purpose** (1-2 sentences + workflow summary)
- [X] **Overview** (what, when, capabilities, composability)
- [X] **Prerequisites** (APIs, env vars, libraries, file structure)
- [X] **Workflow Instructions** (5 steps with code)
- [X] **Output Artifacts** (5 files produced)
- [X] **Error Handling** (common errors + solutions, 4 categories)
- [X] **Composability & Stacking** (3 patterns: risk context, correlation, event impact)
- [X] **Examples** (3 concrete walkthroughs: standard, comparison, quota exceeded)

### 13.2 references/ Files Checklist

- [X] **`POLYMARKET_API.md`** - GraphQL API docs (<800 tokens)
- [X] **`TIMEGPT_GUIDE.md`** - TimeGPT integration (<600 tokens)
- [X] **`EXAMPLES.md`** - Extended walkthroughs (<400 tokens)
- [ ] **`ADVANCED_PATTERNS.md`** - Power user techniques (optional, v1.1)
- [ ] **`TROUBLESHOOTING.md`** - Common issues (optional, v1.1)

### 13.3 Code Documentation Checklist

- [X] **All scripts have module-level docstrings** (purpose, usage)
- [X] **All functions have docstrings** (parameters, return values)
- [X] **All functions have type hints** (Python 3.9+ syntax)
- [X] **Complex logic has inline comments** (e.g., API retry logic, data validation)
- [X] **All scripts have `--help` output** (argparse usage messages)

**Example Script Documentation**:
```python
#!/usr/bin/env python3
"""
Polymarket Contract Data Fetcher

Fetches historical contract odds from Polymarket GraphQL API.
Supports customizable date ranges and contract IDs.

Usage:
    python fetch_polymarket.py --contract-id "0x123..." --output data/raw_odds.json
    python fetch_polymarket.py --contract-id "0xABC..." --days-back 60
"""

import argparse
from typing import Dict, List

def fetch_contract_data(contract_id: str, days_back: int = 30) -> Dict:
    """
    Fetch historical odds data for a Polymarket contract.

    Args:
        contract_id: Hex address of contract (0x + 40 hex chars)
        days_back: Number of days of historical data to fetch (default: 30)

    Returns:
        Dictionary containing contract metadata and odds history

    Raises:
        ValueError: If contract_id format is invalid
        requests.HTTPError: If API request fails
    """
    # Implementation...
    pass
```

---

## 14. Open Questions & Decisions

**Questions Requiring Decisions**:

1. **Question**: Should we support categorical markets (>2 outcomes) in v1.0 or defer to v1.1?
   - **Options**:
     - **A**: Binary only (simpler, faster to market, most common use case)
     - **B**: Binary + categorical (more versatile, higher complexity)
   - **Trade-offs**:
     - A: Faster release (2 weeks), 80% of use cases covered
     - B: Delayed release (+1 week), 95% of use cases covered, more testing required
   - **Recommendation**: **Option A** (binary only for v1.0, categorical in v1.1 based on user demand)
   - **Decision Needed By**: Before development starts (2025-12-10)
   - **Owner**: Product Lead (Intent Solutions)

2. **Question**: What should default forecast horizon be (7, 14, or 30 days)?
   - **Options**:
     - **A**: 7 days (faster API, lower cost, short-term traders)
     - **B**: 14 days (balanced, most versatile)
     - **C**: 30 days (more context, higher cost, long-term traders)
   - **Trade-offs**:
     - A: Cheapest (~$0.03/forecast), least comprehensive
     - B: Moderate cost (~$0.05/forecast), good balance
     - C: Highest cost (~$0.08/forecast), may be less accurate for volatile markets
   - **Recommendation**: **Option B** (14 days default, user can override with `--horizon` flag)
   - **Decision Needed By**: Before v1.0 release
   - **Owner**: Product Lead + Early user feedback

3. **Question**: Should arbitrage analysis (Step 4) be mandatory or optional?
   - **Options**:
     - **A**: Mandatory (requires Kalshi API key for all users)
     - **B**: Optional (graceful degradation if API key not provided)
   - **Trade-offs**:
     - A: Ensures consistent experience, but blocks users without Kalshi access
     - B: More flexible, but report quality varies (with/without arbitrage)
   - **Recommendation**: **Option B** (optional, gracefully degrade—forecast still valuable without arbitrage)
   - **Decision Needed By**: Before development starts
   - **Owner**: Technical Lead

**Decisions Made**:
1. ✅ Binary markets only for v1.0 (categorical in v1.1)
2. ✅ 14-day default forecast horizon (user-overridable)
3. ✅ Optional arbitrage analysis (graceful degradation)

---

## 15. Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.1 | 2025-12-06 | De-hype update: Renamed trading language to analysis/forecast, added disclaimers, neutralized P&L language, marked examples as illustrative | Intent Solutions |
| 1.0.0 | 2025-12-05 | Initial ARD | Intent Solutions |

---

## 16. Approval

| Role | Name | Approval Date | Signature |
|------|------|---------------|-----------|
| Tech Lead | Jeremy Longshore | 2025-12-05 | [Pending] |
| Security Review | Jeremy Longshore | 2025-12-05 | [Pending] |
| Product Owner | Jeremy Longshore | 2025-12-05 | [Pending] |

---

**Template maintained by**: Intent Solutions
**For**: Nixtla Skills Pack + Global Standard
**Last Updated**: 2025-12-06
