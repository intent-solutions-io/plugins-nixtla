# Claude Skill ARD: [Skill Name]

**Template Version**: 1.0.0
**Based On**: [Global Standard Skill Schema](../GLOBAL-STANDARD-SKILL-SCHEMA.md)
**Purpose**: Architecture & Requirements Document for Claude Skills
**Status**: Template

---

## Document Control

| Field | Value |
|-------|-------|
| **Skill Name** | nixtla-[short-name] |
| **Architectural Pattern** | [ ] Script Automation [ ] Read-Process-Write [ ] Search-Analyze-Report [ ] Command Chain [ ] Wizard [ ] Template-Based [ ] Iterative Refinement [ ] Context Aggregation |
| **Complexity Level** | [ ] Simple (3 steps) [ ] Medium (4-5 steps) [ ] Complex (6+ steps) |
| **API Integrations** | [Number of external APIs] |
| **Token Budget** | [Estimated tokens] / 5,000 max |
| **Status** | [ ] Planned [ ] In Development [ ] Complete |
| **Owner** | [Name/Team] |
| **Last Updated** | YYYY-MM-DD |

---

## 1. Architectural Overview

### 1.1 Skill Purpose

**One-Sentence Summary**: [What this skill orchestrates in one clear sentence]

**Architectural Pattern**: [Primary pattern from the 8 standard patterns]

**Why This Pattern**: [Justification for pattern selection]

### 1.2 High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     SKILL ORCHESTRATION                      │
│                  [Skill Name] Workflow                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
         ┌────────────────────────────────────────┐
         │  Step 1: [Action Name]                 │
         │  ├─ API Call: [Service Name]           │
         │  ├─ Code: scripts/[filename.py]        │
         │  └─ Output: data/[file.format]         │
         └────────────────────────────────────────┘
                              │
                              ▼
         ┌────────────────────────────────────────┐
         │  Step 2: [Action Name]                 │
         │  ├─ Code: scripts/[filename.py]        │
         │  ├─ Transform: [format A → format B]   │
         │  └─ Output: data/[file.format]         │
         └────────────────────────────────────────┘
                              │
                              ▼
         ┌────────────────────────────────────────┐
         │  Step 3: [Action Name]                 │
         │  ├─ API Call: [Service Name]           │
         │  ├─ Code: scripts/[filename.py]        │
         │  └─ Output: data/[file.format]         │
         └────────────────────────────────────────┘
                              │
                              ▼
         ┌────────────────────────────────────────┐
         │  Step 4: [Action Name]                 │
         │  ├─ API Call: [Service Name] (optional)│
         │  ├─ Code: scripts/[filename.py]        │
         │  └─ Output: data/[file.format]         │
         └────────────────────────────────────────┘
                              │
                              ▼
         ┌────────────────────────────────────────┐
         │  Step 5: [Action Name]                 │
         │  ├─ Code: scripts/[filename.py]        │
         │  ├─ Template: assets/[template.md]     │
         │  └─ Output: reports/[final-report.md]  │
         └────────────────────────────────────────┘
```

### 1.3 Workflow Summary

**Total Steps**: [3-5+]

| Step | Action | Type | Dependencies | Output |
|------|--------|------|--------------|--------|
| 1 | [Action name] | API Call + Code | None | [file.format] |
| 2 | [Action name] | Code | Step 1 output | [file.format] |
| 3 | [Action name] | API Call + Code | Step 2 output | [file.format] |
| 4 | [Action name] | Code/API (optional) | Step 3 output | [file.format] |
| 5 | [Action name] | Code + Template | Steps 3-4 output | [final-report.md] |

---

## 2. Progressive Disclosure Strategy

### 2.1 Level 1: Frontmatter (Metadata)

**What Goes Here**: ONLY `name` and `description` (Anthropic official standard)

```yaml
---
name: nixtla-[short-name]
description: "[Perfect description formula: Action. Capabilities. Use when [scenarios]. Trigger with '[phrases]'.]"
---
```

**Description Quality Target**: 80%+ on 6-criterion formula

**Character Limit**: <250 characters

**Example**:
```yaml
---
name: nixtla-polymarket-analyst
description: "Orchestrates multi-step Polymarket analysis workflows. Fetches contract odds via API, transforms to time series, forecasts prices using TimeGPT, analyzes arbitrage vs Kalshi, generates trading recommendations. Use when analyzing prediction markets, forecasting contract prices, identifying mispriced opportunities. Trigger with 'analyze Polymarket contract', 'forecast prediction market', 'find arbitrage'."
---
```

### 2.2 Level 2: SKILL.md (Core Instructions)

**Token Budget**: <2,500 tokens (500 lines max)

**Required Sections**:
1. Purpose (1-2 sentences + workflow summary)
2. Overview (what, when, capabilities, composability)
3. Prerequisites (APIs, env vars, libraries, file structure)
4. Workflow Instructions (3-5+ steps with code)
5. Output Artifacts (what files produced)
6. Error Handling (common errors + solutions)
7. Composability & Stacking (how to combine with other skills)
8. Examples (2-3 concrete walkthroughs)

**What Goes Here**:
- Core orchestration logic
- Step-by-step instructions (imperative voice)
- Code execution commands
- Expected outputs for each step
- Error handling strategies
- Composability patterns

**What Does NOT Go Here**:
- Detailed API documentation (goes in references/)
- Extended examples (goes in references/EXAMPLES.md)
- Script source code (goes in scripts/)
- Templates (goes in assets/)

### 2.3 Level 3: Resources (Extended Context)

#### scripts/ Directory
**Purpose**: Executable Python/Bash scripts for each workflow step

**Naming Convention**: `[action]_[service/purpose].py`

**Required Scripts**:
- `scripts/fetch_[service].py` - API data fetcher (Step 1)
- `scripts/transform_[purpose].py` - Data transformer (Step 2)
- `scripts/forecast_[method].py` - Forecasting engine (Step 3)
- `scripts/analyze_[purpose].py` - Analysis/comparison (Step 4)
- `scripts/generate_report.py` - Report generator (Step 5)

**Script Requirements**:
- Self-contained (can run independently)
- Command-line arguments (no hardcoded values)
- Error handling with exit codes
- Logging to stdout/stderr
- API keys from environment variables

#### references/ Directory
**Purpose**: Documentation loaded into Claude's context

**Token Budget**: Each file <1,000 tokens

**Required Files**:
- `API_REFERENCE.md` - API documentation extracts
- `EXAMPLES.md` - Extended use cases and walkthroughs
- `ADVANCED_PATTERNS.md` - Power user techniques (optional)
- `TROUBLESHOOTING.md` - Common issues and solutions (optional)

#### assets/ Directory
**Purpose**: Templates and static resources (NOT loaded into context)

**Required Files**:
- `report_template.md` - Markdown template for final output
- `config.example.json` - Example configuration
- `sample_data.csv` - Test data for development (optional)

---

## 3. Tool Permission Strategy

### 3.1 Required Tools

**Minimal Necessary Set**: [List only tools this skill actually needs]

**Examples**:
- `Read` - Reading API responses, loading data files
- `Write` - Writing intermediate data files, final reports
- `Bash` - Executing Python scripts, running commands
- `Glob` - Finding existing data files (optional)
- `Edit` - Modifying configuration files (optional)

### 3.2 Tool Usage Justification

| Tool | Why Needed | Usage Pattern |
|------|------------|---------------|
| Read | Load API responses, read CSV/JSON data | Step 2, 4, 5 |
| Write | Save intermediate outputs, final report | Step 1-5 |
| Bash | Execute Python scripts for each step | Step 1-5 |
| Glob | Find existing forecast files (optional) | Step 4 (optional) |

### 3.3 Tools Explicitly NOT Needed

**Excluded Tools**: [List tools NOT required and why]

**Examples**:
- `Edit` - Not needed (scripts generate fresh files, no editing)
- `WebFetch` - Not needed (Python scripts handle API calls directly)
- `Grep` - Not needed (no code search required)

---

## 4. Directory Structure & File Organization

### 4.1 Complete Skill Structure

```
nixtla-[skill-name]/
├── SKILL.md                          # Core instructions (<500 lines)
│
├── scripts/                          # Executable code (NOT loaded into context)
│   ├── fetch_[service].py            # Step 1: API data fetcher
│   ├── transform_[purpose].py        # Step 2: Data transformer
│   ├── forecast_[method].py          # Step 3: Forecasting engine
│   ├── analyze_[purpose].py          # Step 4: Analysis/comparison
│   ├── generate_report.py            # Step 5: Report generator
│   └── utils/                        # Shared utilities (optional)
│       ├── api_client.py             # Reusable API client
│       └── validators.py             # Data validation functions
│
├── references/                       # Documentation (loaded into context)
│   ├── API_REFERENCE.md              # API docs extract (<1,000 tokens)
│   ├── EXAMPLES.md                   # Extended examples (<1,000 tokens)
│   ├── ADVANCED_PATTERNS.md          # Power user patterns (optional)
│   └── TROUBLESHOOTING.md            # Common issues (optional)
│
└── assets/                           # Templates (NOT loaded into context)
    ├── report_template.md            # Markdown report template
    ├── config.example.json           # Example configuration
    └── sample_data.csv               # Test data (optional)
```

### 4.2 File Naming Conventions

**Scripts**: `[verb]_[noun].py`
- ✅ `fetch_polymarket.py` - Clear action + target
- ✅ `transform_to_timeseries.py` - Clear transformation
- ❌ `script1.py` - Not descriptive
- ❌ `polymarket.py` - Missing action verb

**References**: `[NOUN]_[TYPE].md` (uppercase)
- ✅ `API_REFERENCE.md` - Clear purpose
- ✅ `EXAMPLES.md` - Clear content type
- ❌ `docs.md` - Too vague
- ❌ `readme.md` - Wrong case

**Assets**: `[noun]_[type].[ext]` (lowercase)
- ✅ `report_template.md` - Clear purpose
- ✅ `config.example.json` - Clear intent
- ❌ `template.md` - Not specific enough
- ❌ `test.csv` - Too generic

### 4.3 Path Referencing Standard

**Always Use**: `{baseDir}` for all file paths in SKILL.md

**Correct**:
```python
python {baseDir}/scripts/fetch_polymarket.py --output data/odds.json
```

**Incorrect**:
```python
python scripts/fetch_polymarket.py  # Missing {baseDir}
python ./scripts/fetch_polymarket.py  # Relative path
python /absolute/path/scripts/fetch_polymarket.py  # Hardcoded
```

---

## 5. API Integration Architecture

### 5.1 External API Integrations

**API 1: [Primary Service Name - e.g., Polymarket API]**

**Purpose**: [What data/functionality this provides]

**Integration Details**:
- **Endpoint**: `https://api.service.com/v1/endpoint`
- **Method**: GET/POST/etc.
- **Authentication**: API Key (header: `Authorization: Bearer $API_KEY`)
- **Rate Limits**: [X requests per Y timeframe]
- **Response Format**: JSON
- **Key Fields**:
  - `field1`: [description]
  - `field2`: [description]

**Example Request**:
```python
import requests
import os

api_key = os.getenv("SERVICE_API_KEY")
response = requests.get(
    "https://api.service.com/v1/endpoint",
    headers={"Authorization": f"Bearer {api_key}"},
    params={"param1": "value1"}
)
data = response.json()
```

**Example Response**:
```json
{
  "status": "success",
  "data": {
    "field1": "value1",
    "field2": 123.45
  }
}
```

**Error Handling**:
- `401 Unauthorized`: Invalid API key → Check `SERVICE_API_KEY` env var
- `429 Rate Limit`: Too many requests → Implement exponential backoff
- `500 Server Error`: Service down → Retry with backoff, fallback to cached data

---

**API 2: [Secondary Service Name - e.g., Nixtla TimeGPT]**

**Purpose**: [What data/functionality this provides]

**Integration Details**:
- **Endpoint**: `https://api.nixtla.io/timegpt/forecast`
- **Method**: POST
- **Authentication**: API Key (header: `X-API-Key: $NIXTLA_API_KEY`)
- **Rate Limits**: [X requests per month (quota-based)]
- **Request Format**: JSON with time series data
- **Response Format**: JSON with forecast + confidence intervals

**Example Request**:
```python
import requests
import os
import pandas as pd

api_key = os.getenv("NIXTLA_API_KEY")
df = pd.read_csv("data/timeseries.csv")

response = requests.post(
    "https://api.nixtla.io/timegpt/forecast",
    headers={"X-API-Key": api_key},
    json={
        "data": df.to_dict(orient="records"),
        "horizon": 14,
        "freq": "D"
    }
)
forecast = response.json()
```

**Error Handling**:
- `402 Payment Required`: Quota exceeded → Fallback to StatsForecast (local, free)
- `400 Bad Request`: Invalid data format → Validate schema before sending

---

### 5.2 API Call Sequencing

**Sequential vs Parallel**:

```
Step 1 (API Call 1)
    ↓
Step 2 (Local Processing) ← No API, transform only
    ↓
Step 3 (API Call 2) ← Depends on Step 2 output
    ↓
Step 4 (API Call 3) ← Optional, can run in parallel with Step 3
    ↓
Step 5 (Local Processing) ← No API, report generation
```

**Parallel Opportunities**: [Identify steps that can run concurrently]
- Example: Steps 3 and 4 can run in parallel if they don't depend on each other

**Fallback Strategy**: [What happens if an API is down]
- Primary: TimeGPT API → Fallback: StatsForecast (local)
- Primary: Live Kalshi API → Fallback: Skip arbitrage analysis (optional step)

---

## 6. Data Flow Architecture

### 6.1 Input → Processing → Output Pipeline

```
INPUT (User Request)
    ↓
Step 1: Fetch Raw Data
    │   Input: Contract ID (from user)
    │   API Call: Polymarket GraphQL
    │   Output: data/raw_odds.json (5-50 KB)
    ↓
Step 2: Transform to Time Series
    │   Input: data/raw_odds.json
    │   Processing: Parse JSON → Convert to CSV
    │   Output: data/timeseries.csv (2-10 KB)
    ↓
Step 3: Generate Forecast
    │   Input: data/timeseries.csv
    │   API Call: TimeGPT forecast API
    │   Output: data/forecast.csv (3-15 KB)
    ↓
Step 4: Analyze Arbitrage (Optional)
    │   Input: data/forecast.csv
    │   API Call: Kalshi API (optional)
    │   Processing: Compare prices, calculate spreads
    │   Output: data/arbitrage.json (1-5 KB)
    ↓
Step 5: Generate Report
    │   Input: data/forecast.csv + data/arbitrage.json
    │   Processing: Fill markdown template
    │   Output: reports/analysis_YYYY-MM-DD.md (10-50 KB)
    ↓
FINAL OUTPUT (Markdown Report)
```

### 6.2 Data Format Specifications

**Format 1: Raw API Data** (`data/raw_odds.json`)
```json
{
  "contract_id": "0x1234567890abcdef",
  "contract_name": "Will Bitcoin reach $100k by Dec 2025?",
  "odds_history": [
    {
      "timestamp": "2025-11-01T00:00:00Z",
      "yes_price": 0.65,
      "no_price": 0.35,
      "volume": 125000.50,
      "liquidity": 450000.00
    }
  ]
}
```

**Format 2: Time Series Data** (`data/timeseries.csv`)
```csv
unique_id,ds,y
BTC_100k_Dec2025,2025-11-01,0.65
BTC_100k_Dec2025,2025-11-02,0.67
BTC_100k_Dec2025,2025-11-03,0.66
```

**Format 3: Forecast Output** (`data/forecast.csv`)
```csv
unique_id,ds,TimeGPT,TimeGPT-lo-80,TimeGPT-hi-80,TimeGPT-lo-95,TimeGPT-hi-95
BTC_100k_Dec2025,2025-12-06,0.68,0.65,0.71,0.63,0.73
BTC_100k_Dec2025,2025-12-07,0.69,0.66,0.72,0.64,0.74
```

**Format 4: Final Report** (`reports/analysis_YYYY-MM-DD.md`)
- Markdown format with sections: Executive Summary, Forecast Chart, Recommendations, Risk Assessment

### 6.3 Data Validation Rules

**Validation Checkpoints**:

1. **After Step 1** (Raw API Data):
   - ✅ JSON is valid and parseable
   - ✅ Required fields present: `contract_id`, `odds_history`
   - ✅ At least 14 days of historical data
   - ✅ Prices are between 0 and 1

2. **After Step 2** (Time Series):
   - ✅ CSV has exactly 3 columns: `unique_id`, `ds`, `y`
   - ✅ No missing dates (frequency is consistent)
   - ✅ All `y` values are numeric and 0 ≤ y ≤ 1
   - ✅ Dates are in chronological order

3. **After Step 3** (Forecast):
   - ✅ Forecast horizon matches request (e.g., 14 days)
   - ✅ Confidence intervals are valid: lo-95 < lo-80 < forecast < hi-80 < hi-95
   - ✅ All forecasts are between 0 and 1

---

## 7. Error Handling Strategy

### 7.1 Error Categories & Responses

**Category 1: Missing Prerequisites**

| Error | Cause | Detection | Solution |
|-------|-------|-----------|----------|
| `API_KEY not found` | Environment variable not set | Script startup | Display setup instructions with export command |
| `Library not installed` | Missing Python package | Import statement | Display `pip install` command |
| `Invalid config` | Missing/malformed config file | File read | Generate example config, show expected format |

**Category 2: API Failures**

| Error | Cause | Detection | Solution |
|-------|-------|-----------|----------|
| `401 Unauthorized` | Invalid API key | API response code | Verify key format, check account status |
| `429 Rate Limit` | Too many requests | API response code | Exponential backoff, queue requests |
| `500 Server Error` | API service down | API response code | Retry 3x with backoff, then fallback |
| `Quota Exceeded` | Monthly limit reached | API response | Switch to free alternative (StatsForecast) |

**Category 3: Data Quality Issues**

| Error | Cause | Detection | Solution |
|-------|-------|-----------|----------|
| `Insufficient data` | <14 days of history | Data validation | Request longer time range or skip forecast |
| `Missing values` | Gaps in time series | Data validation | Interpolate missing points, log warning |
| `Invalid format` | Wrong data structure | Schema validation | Show expected vs actual format, fix script |

**Category 4: Execution Failures**

| Error | Cause | Detection | Solution |
|-------|-------|-----------|----------|
| `Script not found` | Missing Python file | File system check | Verify skill installation, re-download |
| `Permission denied` | File/directory permissions | OS error | Display chmod command to fix |
| `Disk full` | No space for output | Write operation | Clean up old files, check disk space |

### 7.2 Graceful Degradation

**Fallback Hierarchy**:

```
Primary Path:
  Step 1 → Step 2 → Step 3 (TimeGPT) → Step 4 (Kalshi) → Step 5
                              ↓ (if API fails)
Fallback Path 1:
  Step 1 → Step 2 → Step 3 (StatsForecast local) → Step 5
                                                      ↓ (skip Step 4)
Fallback Path 2:
  Step 1 → Step 2 → Step 3 (cached forecast) → Step 5
```

**Optional Steps**: [Which steps can be skipped without breaking the workflow]
- Step 4 (Arbitrage Analysis) is optional - skill still produces valuable forecast without it

### 7.3 Logging & Debugging

**Log Levels**:
- `INFO`: Normal progress ("Fetching data...", "Forecast complete")
- `WARNING`: Recoverable issues ("Missing data interpolated", "Using fallback API")
- `ERROR`: Failures that stop execution ("API key invalid", "Data validation failed")

**Log Format**:
```
[YYYY-MM-DD HH:MM:SS] [LEVEL] [Step N] Message
[2025-12-05 14:32:10] [INFO] [Step 1] Fetching Polymarket contract 0x1234...
[2025-12-05 14:32:12] [INFO] [Step 1] ✓ Saved 30 days of data to data/raw_odds.json
[2025-12-05 14:32:13] [WARNING] [Step 2] Missing data on 2025-11-15, interpolating...
[2025-12-05 14:32:14] [INFO] [Step 3] Calling TimeGPT API (horizon=14)...
[2025-12-05 14:32:45] [ERROR] [Step 3] TimeGPT API quota exceeded, switching to StatsForecast
```

---

## 8. Composability & Stacking Architecture

### 8.1 Standalone Execution

**This skill can run independently**:
```bash
# User provides contract ID, skill handles everything
python {baseDir}/scripts/fetch_polymarket.py --contract-id "0x1234"
# ... Steps 2-5 execute automatically
```

**Output**: Self-contained report with all analysis

### 8.2 Skill Stacking Patterns

**Stack Pattern 1: Sequential Chaining**

```
nixtla-polymarket-analyst (this skill)
    → Produces: forecast.csv
        ↓
nixtla-market-risk-analyzer (next skill)
    → Consumes: forecast.csv
    → Produces: risk_analysis.json (VaR, volatility, drawdown)
```

**Usage**:
```bash
# Step 1: Run this skill
./run_polymarket_analyst.sh --contract "0x1234"

# Step 2: Feed output to risk analyzer
./run_market_risk_analyzer.sh --input reports/forecast.csv
```

---

**Stack Pattern 2: Parallel Multi-Contract**

```
nixtla-polymarket-analyst (contract A)  ┐
nixtla-polymarket-analyst (contract B)  ├─→ nixtla-correlation-mapper
nixtla-polymarket-analyst (contract C)  ┘
    → Produces: correlation_matrix.csv + hedge_recommendations.md
```

**Usage**:
```bash
# Run this skill on 3 contracts in parallel
for contract in "0xAAA" "0xBBB" "0xCCC"; do
  ./run_polymarket_analyst.sh --contract $contract &
done
wait

# Stack with correlation mapper
./run_correlation_mapper.sh --inputs reports/forecast_*.csv
```

---

**Stack Pattern 3: Cross-Platform Aggregation**

```
nixtla-polymarket-analyst ─┐
                           ├─→ nixtla-context-aggregator
External Data (Twitter)   ─┘
    → Produces: multi_source_forecast.md
```

### 8.3 Skill Input/Output Contracts

**Input Contract** (what this skill expects):
- Contract ID (string, hex format: `0x[a-f0-9]{40}`)
- Optional: Date range (ISO 8601 format)
- Optional: Configuration overrides (JSON)

**Output Contract** (what this skill guarantees):
- `data/forecast.csv` - Always produced (even on API failure via fallback)
- `reports/analysis_YYYY-MM-DD.md` - Always produced
- `data/arbitrage.json` - Conditionally produced (only if Step 4 succeeds)

**Versioning**: Output format is stable within major version (v1.x.x)

---

## 9. Performance & Scalability

### 9.1 Performance Targets

| Metric | Target | Max Acceptable | Measurement |
|--------|--------|----------------|-------------|
| Total execution time | <60 seconds | <120 seconds | End-to-end workflow |
| Step 1 (API fetch) | <5 seconds | <15 seconds | API response time |
| Step 2 (transform) | <2 seconds | <5 seconds | Processing time |
| Step 3 (forecast) | <30 seconds | <60 seconds | API response time |
| Step 4 (arbitrage) | <10 seconds | <20 seconds | API + analysis |
| Step 5 (report) | <5 seconds | <10 seconds | Template rendering |

### 9.2 Scalability Considerations

**Single Contract**: Optimized for 1 contract analysis (<60 sec)

**Batch Processing** (10 contracts):
- Sequential: ~10 minutes (10 × 60 sec)
- Parallel (recommended): ~2 minutes (max API latency + overhead)

**Batch Pattern**:
```bash
# Process 10 contracts in parallel
for contract in $(cat contracts.txt); do
  ./run_full_workflow.sh --contract $contract &
done
wait
```

**Rate Limiting**: Respect API limits
- Polymarket: 100 req/min → Max 100 contracts/min
- TimeGPT: 1000 req/month → Budget accordingly

### 9.3 Resource Usage

**Disk Space**:
- Per contract: ~100 KB (all intermediate + final files)
- 100 contracts: ~10 MB
- Cleanup strategy: Delete intermediate files after Step 5

**Memory**:
- Per contract: <50 MB RAM
- Batch processing: <500 MB RAM (10 contracts parallel)

**Network**:
- Polymarket API: ~10 KB/request
- TimeGPT API: ~50 KB/request
- Total per contract: ~100 KB bandwidth

---

## 10. Testing Strategy

### 10.1 Unit Testing (Per-Step Validation)

**Test Step 1** (API Fetch):
```bash
# Test with known contract ID
python scripts/fetch_polymarket.py \
  --contract-id "0xTEST_CONTRACT_ID" \
  --output /tmp/test_odds.json

# Validate output
assert_file_exists /tmp/test_odds.json
assert_json_valid /tmp/test_odds.json
assert_field_exists "contract_id" /tmp/test_odds.json
```

**Test Step 2** (Transform):
```bash
# Use sample data
python scripts/transform_to_timeseries.py \
  --input assets/sample_data.json \
  --output /tmp/test_ts.csv

# Validate output
assert_csv_columns "unique_id,ds,y" /tmp/test_ts.csv
assert_no_missing_values /tmp/test_ts.csv
```

**Test Step 3-5**: Similar per-step validation

### 10.2 Integration Testing (Full Workflow)

**Happy Path Test**:
```bash
# Run full workflow with test contract
./run_full_workflow.sh \
  --contract-id "0xTEST_CONTRACT" \
  --output /tmp/test_report.md

# Validate final output
assert_file_exists /tmp/test_report.md
assert_contains "Forecast Chart" /tmp/test_report.md
assert_contains "Recommendations" /tmp/test_report.md
```

**Failure Path Tests**:
1. **Missing API Key**: Verify helpful error message
2. **Invalid Contract ID**: Verify graceful failure
3. **API Rate Limit**: Verify exponential backoff
4. **TimeGPT Quota Exceeded**: Verify StatsForecast fallback

### 10.3 Acceptance Criteria

**This skill is production-ready when**:

- [ ] All 5 workflow steps execute successfully
- [ ] Description scores 80%+ on quality formula
- [ ] Total token budget <5,000 tokens
- [ ] SKILL.md is <500 lines
- [ ] All scripts have error handling
- [ ] Fallback paths work (StatsForecast, skip optional steps)
- [ ] At least 2 stacking patterns demonstrated
- [ ] Documentation is complete (references/, examples)
- [ ] Happy path test passes in <60 seconds
- [ ] Failure path tests show helpful errors

---

## 11. Deployment & Maintenance

### 11.1 Installation Requirements

**System Requirements**:
- Python 3.9+
- 500 MB disk space
- Internet connection for API calls

**Dependencies**:
```bash
pip install nixtla statsforecast pandas requests
```

**Environment Setup**:
```bash
export POLYMARKET_API_KEY="your_key_here"
export NIXTLA_API_KEY="your_timegpt_key"
export KALSHI_API_KEY="optional_key"  # For Step 4
```

### 11.2 Versioning Strategy

**Semantic Versioning**: `MAJOR.MINOR.PATCH`

**Version Increments**:
- **MAJOR**: Breaking changes to output format or API contracts
- **MINOR**: New features (e.g., additional API integrations, new stacking patterns)
- **PATCH**: Bug fixes, performance improvements, documentation updates

**Example**:
- v1.0.0 - Initial release
- v1.1.0 - Added Kalshi arbitrage analysis (Step 4)
- v1.1.1 - Fixed time zone handling in Step 2
- v2.0.0 - Changed output format from markdown to JSON (breaking)

### 11.3 Monitoring & Observability

**Key Metrics to Track**:
1. **Activation Rate**: How often skill is triggered vs false positives
2. **Success Rate**: % of executions that complete successfully
3. **Average Execution Time**: Per step and total
4. **API Failure Rate**: % of API calls that fail
5. **Fallback Usage**: How often StatsForecast is used vs TimeGPT

**Logging Strategy**:
- All executions logged to `logs/skill_execution_YYYY-MM-DD.log`
- Errors logged with full stack traces
- Performance metrics logged per step

---

## 12. Security & Compliance

### 12.1 API Key Management

**Storage**: Environment variables ONLY (never hardcoded)

**Validation**:
```python
import os
import sys

def validate_api_keys():
    required_keys = ["POLYMARKET_API_KEY", "NIXTLA_API_KEY"]
    missing = [k for k in required_keys if not os.getenv(k)]

    if missing:
        print(f"ERROR: Missing API keys: {', '.join(missing)}", file=sys.stderr)
        print("Set with: export KEY_NAME='your_key'", file=sys.stderr)
        sys.exit(1)
```

**Rotation**: Document how to update keys without breaking skill

### 12.2 Data Privacy

**User Data**: No PII collected or stored

**API Data**: Cached locally in `data/` directory
- Retention: 7 days (auto-cleanup)
- Access: Local filesystem only (not shared)

**Logs**: No sensitive data in logs (API keys masked)

### 12.3 Rate Limiting & Abuse Prevention

**API Quotas**: Track usage to prevent quota exhaustion

**Backoff Strategy**: Exponential backoff on rate limit errors
```python
import time

def call_api_with_backoff(url, max_retries=3):
    for attempt in range(max_retries):
        response = requests.get(url)
        if response.status_code == 429:
            wait_time = 2 ** attempt  # 1s, 2s, 4s
            time.sleep(wait_time)
            continue
        return response
    raise Exception("Max retries exceeded")
```

---

## 13. Documentation Requirements

### 13.1 SKILL.md Sections Checklist

- [ ] Purpose (1-2 sentences + workflow summary)
- [ ] Overview (what, when, capabilities, composability)
- [ ] Prerequisites (APIs, env vars, libraries, file structure)
- [ ] Workflow Instructions (3-5+ steps with code)
- [ ] Output Artifacts (what files produced)
- [ ] Error Handling (common errors + solutions)
- [ ] Composability & Stacking (at least 2 patterns)
- [ ] Examples (2-3 concrete walkthroughs)

### 13.2 references/ Files Checklist

- [ ] `API_REFERENCE.md` - API documentation extracts (<1,000 tokens)
- [ ] `EXAMPLES.md` - Extended examples (<1,000 tokens)
- [ ] `ADVANCED_PATTERNS.md` - Power user techniques (optional)
- [ ] `TROUBLESHOOTING.md` - Common issues (optional)

### 13.3 Code Documentation Checklist

- [ ] All scripts have docstrings (module, function, class)
- [ ] All scripts have usage examples in `--help`
- [ ] All functions have type hints (Python 3.9+)
- [ ] Complex logic has inline comments

---

## 14. Open Questions & Decisions

**Questions Requiring Decisions**:

1. **Question**: [Open architectural question]
   - **Options**: [Option A, Option B, Option C]
   - **Trade-offs**: [Pros/cons of each]
   - **Recommendation**: [Preferred option]
   - **Decision Needed By**: [Date]
   - **Owner**: [Who decides]

2. **Question**: [Another open question]
   - **Options**: [Options]
   - **Trade-offs**: [Analysis]
   - **Recommendation**: [Suggestion]
   - **Decision Needed By**: [Date]
   - **Owner**: [Who decides]

---

## 15. Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | YYYY-MM-DD | Initial ARD | [Name] |

---

## 16. Approval

| Role | Name | Approval Date | Signature |
|------|------|---------------|--------------|
| Tech Lead | [Name] | [Date] | [Signature] |
| Security Review | [Name] | [Date] | [Signature] |
| Product Owner | [Name] | [Date] | [Signature] |

---

**Template maintained by**: Intent Solutions
**For**: Nixtla Skills Pack + Global Standard
**Last Updated**: 2025-12-05
