# Claude Skill PRD: Nixtla Batch Forecaster

**Template Version**: 1.0.0
**Based On**: [Anthropic Skills Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)
**Purpose**: Product Requirements Document for Claude Skills
**Status**: Planned

---

## Document Control

| Field | Value |
|-------|-------|
| **Skill Name** | nixtla-batch-forecaster |
| **Skill Type** | [X] Mode Skill [ ] Utility Skill |
| **Domain** | Prediction Markets + Time Series Forecasting |
| **Target Users** | Active Traders, Portfolio Managers, Market Analysts |
| **Priority** | [X] Critical [ ] High [ ] Medium [ ] Low |
| **Status** | [X] Planned [ ] In Development [ ] Complete |
| **Owner** | Intent Solutions |
| **Last Updated** | 2025-12-05 |

---

## 1. Executive Summary

**One-sentence description**: Transform Claude into a parallel batch processor that analyzes 10-100 prediction market contracts simultaneously, generating individual forecasts and aggregated portfolio reports with watchlist tracking and automated alerts.

**Value Proposition**: Processes entire prediction market portfolios 10x faster than sequential analysis, enabling traders to monitor large watchlists (50+ contracts) and identify opportunities across multiple markets in minutes instead of hours.

**Key Metrics**:
- Target activation accuracy: 95%
- Expected usage frequency: 2-5 times per day (portfolio managers)
- Parallel speedup: 10x faster than sequential (10 contracts in 2 min vs 20 min)
- Batch size support: 10-100 contracts per run
- Success rate target: >90% (at least 9/10 contracts forecast successfully)

---

## 2. Problem Statement

### Current State (Without This Skill)

**Pain Points**:
1. **Sequential bottleneck**: Analyzing 50 contracts one-by-one takes 50+ hours using manual methods
2. **Watchlist management impossible**: No way to monitor entire portfolio efficiently—traders miss opportunities
3. **No aggregated insights**: Even with individual forecasts, no portfolio-level view (correlations, risk, diversification)
4. **Timing critical**: Prediction markets move fast—by the time sequential analysis completes, opportunities have expired
5. **Manual tracking overhead**: Traders maintain spreadsheets of contract IDs, manually check each one, copy/paste results

**Current Workarounds**:
- Analyze only 5-10 "top priority" contracts manually (miss 80% of opportunities)
- Use generic portfolio tools not designed for prediction markets (poor fit)
- Hire analysts to monitor markets 24/7 (expensive, $50k-$100k/year)

**Impact of Problem**:
- Time wasted: 10-20 hours/week on manual portfolio monitoring
- Missed opportunities: 70-80% of profitable trades never identified (analysis too slow)
- User frustration level: Critical (portfolio management is impossible without batch processing)
- Financial cost: $50k-$100k/year for manual monitoring or missed profits

### Desired State (With This Skill)

**Transformation**:
- From: 10-20 hours/week manual monitoring with 80% missed opportunities
- To: 5 minutes automated batch analysis with <5% missed opportunities (10x time reduction, 15x opportunity increase)

**Expected Benefits**:
1. **10x faster portfolio analysis**: 50 contracts in 5 minutes vs 50+ hours manual
2. **Comprehensive coverage**: Monitor entire watchlist, not just top 10 contracts
3. **Aggregated insights**: Portfolio-level metrics (diversification, correlation, risk)
4. **Automated alerts**: Notify when any contract meets criteria (forecast change >10%, arbitrage detected, etc.)
5. **Watchlist management**: Import/export contract lists, track performance over time

---

## 3. Target Users

### Primary Users

**User Persona 1: Active Portfolio Trader**
- **Background**: Manages 20-50 prediction market positions, trades daily, experienced with Polymarket/Kalshi
- **Goals**: Monitor entire portfolio efficiently, identify new opportunities, rebalance positions based on forecast changes
- **Pain Points**: Sequential analysis is too slow, can't scale monitoring to 50+ contracts, missing profitable trades
- **Use Frequency**: Daily (2-5 batch analyses per day: morning scan, mid-day check, evening review)
- **Technical Skills**: Strong trading knowledge, basic CLI skills, limited coding experience
- **Annual Income Impact**: $100k-$500k potential (better portfolio management + faster opportunity detection)

**User Persona 2: Quantitative Portfolio Manager**
- **Background**: Manages 100+ prediction market positions, algorithmic trading background, Python proficient
- **Goals**: Automate daily portfolio monitoring, backtest strategies on historical batches, optimize position sizing
- **Pain Points**: Existing tools don't support prediction markets, need batch API access, want customizable alerts
- **Use Frequency**: Multiple times daily (automated cron jobs + manual reviews)
- **Technical Skills**: Expert in Python/stats, proficient in CLI, experienced with batch processing
- **Value**: Automated portfolio management, research insights, strategy optimization

### Secondary Users

**Market Researchers**: Analyze trends across many contracts simultaneously
**Hedge Funds**: Monitor large prediction market allocations
**Academic Researchers**: Study market efficiency at scale

---

## 4. User Stories

### Critical User Stories (Must Have)

1. **As a** portfolio trader,
   **I want** to analyze my entire 50-contract watchlist in under 5 minutes,
   **So that** I can make timely portfolio decisions before market conditions change.

   **Acceptance Criteria**:
   - [ ] Accepts CSV file with 10-100 contract IDs
   - [ ] Processes contracts in parallel (not sequential)
   - [ ] Completes 50 contracts in <5 minutes (avg 6 sec per contract)
   - [ ] Produces individual forecast files for each contract
   - [ ] Generates aggregated portfolio report with summary statistics

2. **As a** portfolio trader,
   **I want** to receive alerts when any contract in my watchlist meets specific criteria (forecast change >10%, arbitrage >5%, etc.),
   **So that** I can act quickly on opportunities without manually checking every contract.

   **Acceptance Criteria**:
   - [ ] Supports custom alert rules (forecast change, arbitrage threshold, confidence level)
   - [ ] Filters batch results by alert criteria
   - [ ] Highlights flagged contracts in portfolio report
   - [ ] Saves flagged contracts to separate alerts file (JSON)
   - [ ] Provides actionable recommendations for each alert

3. **As a** quantitative manager,
   **I want** the batch processor to handle failures gracefully (skip failed contracts, continue processing others),
   **So that** one bad contract doesn't block my entire portfolio analysis.

   **Acceptance Criteria**:
   - [ ] Continues processing if individual contract fails (API error, missing data, etc.)
   - [ ] Logs failures with helpful error messages
   - [ ] Produces partial portfolio report (excludes failed contracts)
   - [ ] Reports success rate (X/Y contracts processed successfully)
   - [ ] Saves failure details to errors.json for debugging

### High-Priority User Stories (Should Have)

4. **As a** trader,
   **I want** to import watchlists from CSV or JSON files,
   **So that** I can easily manage and update my contract lists.

   **Acceptance Criteria**:
   - [ ] Accepts CSV format: contract_id, contract_name (optional), notes (optional)
   - [ ] Accepts JSON format: array of {id, name, metadata}
   - [ ] Validates contract IDs before processing (regex check)
   - [ ] Warns about duplicates, invalid IDs
   - [ ] Supports comments in CSV (lines starting with #)

5. **As a** portfolio manager,
   **I want** aggregated portfolio metrics (avg forecast change, portfolio risk, top opportunities),
   **So that** I can understand my overall position without reading 50 individual reports.

   **Acceptance Criteria**:
   - [ ] Calculates portfolio-level statistics (mean, median, std dev of forecasts)
   - [ ] Identifies top 10 opportunities (highest forecast change, arbitrage, etc.)
   - [ ] Provides risk assessment (concentration, volatility, correlation estimates)
   - [ ] Generates ASCII charts of portfolio distribution
   - [ ] Exports to portfolio_summary.json for further analysis

### Nice-to-Have User Stories (Could Have)

6. **As a** power user,
   **I want** to customize forecast horizons and confidence levels per contract,
   **So that** I can optimize analysis for different contract types (short-term vs long-term).

7. **As a** researcher,
   **I want** to export batch results to CSV for historical tracking,
   **So that** I can analyze portfolio performance over time.

---

## 5. Functional Requirements

### Core Capabilities (Must Have)

**REQ-1: Parallel Batch Processing**
- **Description**: Process 10-100 contracts in parallel, not sequentially, to achieve 10x speedup
- **Rationale**: Core value proposition—speed is critical for portfolio monitoring
- **Acceptance Criteria**:
  - [ ] Accepts input file (CSV/JSON) with contract IDs
  - [ ] Launches N parallel processes (configurable, default: 10 workers)
  - [ ] Distributes contracts across workers evenly
  - [ ] Aggregates results when all workers complete
  - [ ] Total time: <5 min for 50 contracts (target: 2-3 min)
- **Dependencies**: Python multiprocessing or concurrent.futures library

**REQ-2: Watchlist Input Management**
- **Description**: Import contract lists from CSV or JSON, validate IDs, handle duplicates
- **Rationale**: Users need easy way to maintain watchlists without manual CLI entry
- **Acceptance Criteria**:
  - [ ] CSV format: contract_id, name (optional), notes (optional)
  - [ ] JSON format: [{id, name, metadata}]
  - [ ] Validates contract ID format (0x + 40 hex chars)
  - [ ] Removes duplicates automatically
  - [ ] Logs warnings for invalid IDs (skips, doesn't fail)
- **Dependencies**: pandas for CSV parsing, json library for JSON

**REQ-3: Individual Contract Forecasting**
- **Description**: For each contract, run full forecast workflow (fetch → transform → forecast → arbitrage → report)
- **Rationale**: Each contract needs complete analysis (same quality as single-contract skill)
- **Acceptance Criteria**:
  - [ ] Reuses nixtla-polymarket-analyst workflow for each contract
  - [ ] Saves individual forecast files: reports/contract_<ID>_forecast.csv
  - [ ] Saves individual reports: reports/contract_<ID>_analysis.md
  - [ ] Handles failures gracefully (log error, continue to next contract)
  - [ ] Reports per-contract execution time
- **Dependencies**: nixtla-polymarket-analyst skill (reusable components)

**REQ-4: Aggregated Portfolio Report**
- **Description**: Combine all individual forecasts into portfolio-level summary with statistics and top opportunities
- **Rationale**: Traders need high-level view without reading 50 individual reports
- **Acceptance Criteria**:
  - [ ] Calculates portfolio metrics: avg forecast change, success rate, total opportunities
  - [ ] Identifies top 10 contracts by forecast change (ascending/descending)
  - [ ] Identifies top 10 arbitrage opportunities (highest spread)
  - [ ] Generates portfolio distribution chart (ASCII histogram)
  - [ ] Saves to reports/portfolio_summary_YYYY-MM-DD.md
- **Dependencies**: pandas for aggregation, numpy for statistics

**REQ-5: Automated Alerts System**
- **Description**: Filter batch results by user-defined criteria, flag high-priority contracts
- **Rationale**: Traders can't manually review 50 reports—need automated flagging
- **Acceptance Criteria**:
  - [ ] Supports alert rules: forecast_change_pct, arbitrage_spread_min, confidence_level_min
  - [ ] Filters contracts matching any alert rule
  - [ ] Saves flagged contracts to data/alerts.json with recommendations
  - [ ] Highlights alerts in portfolio summary report
  - [ ] Provides alert counts (X contracts flagged out of Y total)
- **Dependencies**: Alert rule engine (simple if/else filtering)

### Integration Requirements

**REQ-API-1: Polymarket Bulk Fetching**
- **Purpose**: Fetch multiple contracts in parallel without hitting rate limits
- **Rate Limits**: 100 req/min → Max 100 contracts in first minute, then throttle
- **Error Handling**: Implement request queueing with rate limiting (e.g., 80 req/min to stay safe)

**REQ-API-2: TimeGPT Quota Management**
- **Purpose**: Avoid exhausting monthly quota (1,000 req/month) with large batches
- **Strategy**: Track usage, warn if batch would exceed quota, fallback to StatsForecast for overflow
- **Cost Considerations**: 50 contracts = $2.50 cost (50 × $0.05/forecast)

**REQ-API-3: Kalshi Bulk Queries** (Optional)
- **Purpose**: Check arbitrage for multiple contracts efficiently
- **Rate Limits**: 60 req/min → Throttle to match
- **Error Handling**: Graceful degradation (skip arbitrage for failed lookups)

### Data Requirements

**REQ-DATA-1: Input Watchlist Format**

**CSV Example**:
```csv
contract_id,name,notes
0x1234567890abcdef1234567890abcdef12345678,BTC $100k by Dec 2025,High confidence
0xabcdef1234567890abcdef1234567890abcdef12,ETH $10k by Dec 2025,Watch closely
0x9876543210fedcba9876543210fedcba98765432,Trump wins 2024,Political event
```

**JSON Example**:
```json
[
  {
    "id": "0x1234567890abcdef1234567890abcdef12345678",
    "name": "BTC $100k by Dec 2025",
    "metadata": {"priority": "high", "added": "2025-12-01"}
  },
  {
    "id": "0xabcdef1234567890abcdef1234567890abcdef12",
    "name": "ETH $10k by Dec 2025",
    "metadata": {"priority": "medium", "added": "2025-11-15"}
  }
]
```

**REQ-DATA-2: Output Portfolio Report Format**

```markdown
# Portfolio Analysis: 50 Contracts (2025-12-05)

## Executive Summary
- **Contracts Analyzed**: 50 / 50 (100% success rate)
- **Avg Forecast Change**: +8.2% (bullish)
- **Top Opportunities**: 12 contracts with >10% upside
- **Arbitrage Detected**: 3 contracts with >5% spread
- **Portfolio Risk**: Medium (moderate concentration)

## Top 10 Opportunities (by forecast change)
| Rank | Contract | Current | Forecast (14d) | Change | Confidence |
|------|----------|---------|----------------|--------|------------|
| 1 | BTC $100k Dec 2025 | 0.52 | 0.68 | +30.8% | High |
| 2 | ETH $10k Dec 2025 | 0.45 | 0.58 | +28.9% | High |
| 3 | ... | ... | ... | ... | ... |

## Arbitrage Opportunities
| Contract | Polymarket Forecast | Kalshi Current | Spread | Profit % |
|----------|---------------------|----------------|--------|----------|
| BTC $100k Dec 2025 | 0.68 | 0.60 | 0.08 | 13.3% |
| ... | ... | ... | ... | ... |

## Alerts (5 contracts flagged)
- **High Forecast Change** (3 contracts): >15% upside detected
- **Arbitrage Opportunity** (2 contracts): >8% spread vs Kalshi

## Portfolio Distribution
[ASCII histogram of forecast changes]

## Risk Assessment
- **Concentration**: 40% of portfolio in crypto contracts (diversify)
- **Volatility**: High confidence intervals on 20% of contracts
- **Recommendations**: Reduce crypto exposure, add political/economic contracts
```

### Performance Requirements

**REQ-PERF-1: Batch Processing Speed**
- **Target**: 50 contracts in <5 minutes (avg 6 sec per contract)
- **Max Acceptable**: 50 contracts in <10 minutes
- **Breakdown**:
  - Parallel workers: 10 (configurable)
  - Avg time per contract: 30-40 sec (same as single-contract skill)
  - Parallelization speedup: 10x (10 contracts run simultaneously)
  - Total for 50 contracts: 50 / 10 workers × 40 sec = 200 sec (~3.5 min)

**REQ-PERF-2: Resource Usage**
- **Memory**: <2 GB RAM for 50 contracts (10 workers × 50 MB each + aggregation)
- **Disk**: <50 MB for 50 contracts (50 × 1 MB per contract)
- **Network**: <10 MB for 50 contracts (50 × 200 KB API calls)

### Quality Requirements

**REQ-QUAL-1: Description Quality**
- **Target Score**: 90%+ on quality formula
- **Must Include**:
  - [X] Action verbs: "Processes", "Analyzes", "Monitors", "Aggregates", "Alerts"
  - [X] "Use when [scenarios]": "monitoring portfolios, analyzing watchlists, tracking multiple contracts"
  - [X] Trigger phrases: "analyze my watchlist", "batch forecast 50 contracts", "monitor portfolio"
  - [X] Domain keywords: "batch", "parallel", "portfolio", "watchlist", "alerts"

**REQ-QUAL-2: Success Rate**
- **Target**: 90%+ contracts processed successfully (at most 5/50 failures acceptable)
- **Failure Handling**: Graceful degradation (skip failed contracts, continue batch)
- **Error Reporting**: Clear error logs with actionable solutions

---

## 6. Non-Goals (Out of Scope)

**What This Skill Does NOT Do**:

1. **Real-Time Streaming Updates**
   - **Rationale**: Batch processing is on-demand, not continuous monitoring
   - **Alternative**: Use cron job to run batches every N hours
   - **May be added in**: v2.0 (websocket streaming support)

2. **Historical Backtesting**
   - **Rationale**: Forward-looking portfolio analysis only
   - **Alternative**: Export batch results to CSV, use external backtesting tools
   - **Depends on**: User demand

3. **Portfolio Optimization (Position Sizing)**
   - **Rationale**: Provides analysis, not trade execution or allocation recommendations
   - **Alternative**: Stack with nixtla-market-risk-analyzer for position sizing
   - **May be added in**: v2.0

4. **Cross-Platform Portfolio Aggregation**
   - **Rationale**: Single platform (Polymarket) only in v1.0
   - **Alternative**: Manually combine watchlists from multiple platforms
   - **Depends on**: API availability (Kalshi, Manifold, etc.)

---

## 7. Success Metrics

### Skill Activation Metrics

**Metric 1: Activation Accuracy**
- **Target**: 95%+
- **Test Phrases**: "analyze my watchlist", "batch forecast 50 contracts", "monitor my portfolio"

**Metric 2: False Positive Rate**
- **Target**: <3%
- **Measurement**: User feedback

### Quality Metrics

**Metric 3: Batch Success Rate**
- **Target**: 90%+ contracts processed successfully
- **Measurement**: (Successful contracts / Total contracts) × 100

**Metric 4: Processing Speed**
- **Target**: <5 min for 50 contracts
- **Measurement**: End-to-end batch execution time

### Usage Metrics

**Metric 5: Adoption Rate**
- **Target**: 50% of active portfolio traders use batch processing within first month
- **Measurement**: Skill invocation logs

**Metric 6: Average Batch Size**
- **Target**: 20-50 contracts per batch (indicates serious portfolio management use)
- **Measurement**: Median watchlist size across all invocations

### Performance Metrics

**Metric 7: Time Savings**
- **Target**: 10x faster than sequential analysis
- **Measurement**: 50 contracts in 5 min (batch) vs 50+ hours (manual sequential)

**Metric 8: Alert Precision**
- **Target**: 70%+ of flagged contracts are acted upon by users
- **Measurement**: User feedback on alert usefulness

---

## 8. User Experience Flow

### Typical Usage Flow

1. **User Intent**: Portfolio trader wants to analyze their 50-contract watchlist
2. **Trigger**: User says "Analyze my prediction market watchlist" (uploads watchlist.csv)
3. **Skill Activation**: Claude recognizes need for `nixtla-batch-forecaster` skill
4. **Skill Execution**:
   - Load watchlist (50 contracts from CSV)
   - Validate contract IDs (all valid)
   - Launch 10 parallel workers
   - Each worker processes 5 contracts (fetch → transform → forecast → arbitrage → report)
   - Aggregate results from all workers
   - Generate portfolio summary report
   - Filter by alert rules (flag 5 high-priority contracts)
5. **Output Delivered**: Portfolio summary report + 50 individual forecasts + alerts.json
6. **User Action**: Reviews top 10 opportunities, investigates 5 alerts, executes 3 trades

### Example Scenario

**Input (watchlist.csv)**:
```csv
contract_id,name
0x1234567890abcdef1234567890abcdef12345678,BTC $100k Dec 2025
0xabcdef1234567890abcdef1234567890abcdef12,ETH $10k Dec 2025
0x9876543210fedcba9876543210fedcba98765432,Trump wins 2024
... (47 more contracts)
```

**Claude's Response**:
```
I'll analyze your 50-contract watchlist using the nixtla-batch-forecaster skill.
This will process all contracts in parallel and generate a portfolio summary.

[Skill executes batch workflow in ~3.5 minutes]

✓ Batch complete! Processed 50/50 contracts successfully (100% success rate)
✓ Generated portfolio summary report
✓ Identified 12 high-opportunity contracts
✓ Detected 3 arbitrage opportunities
✓ Flagged 5 contracts for immediate review

Top 3 Opportunities:
1. BTC $100k Dec 2025: +30.8% forecast change (STRONG BUY)
2. ETH $10k Dec 2025: +28.9% forecast change (BUY)
3. Inflation CPI >5% Jan 2026: +22.5% forecast change (BUY)

See full report: reports/portfolio_summary_2025-12-05.md
See alerts: data/alerts.json
```

**User Benefit**: Analyzed entire portfolio in 3.5 minutes (vs 50+ hours manually), identified 12 opportunities (vs missing 80% with manual spot-checks)

---

## 9. Integration Points

### External Systems

**System 1: Polymarket GraphQL API** (Batch Fetching)
- **Purpose**: Fetch multiple contracts efficiently
- **Integration Type**: Parallel HTTP requests with rate limiting
- **Rate Limit Strategy**: Queue requests at 80 req/min (below 100 req/min limit)

**System 2: Nixtla TimeGPT API** (Batch Forecasting)
- **Purpose**: Generate forecasts for all contracts
- **Quota Management**: Track usage, warn if batch exceeds monthly limit, fallback to StatsForecast
- **Cost**: 50 contracts × $0.05 = $2.50 per batch

**System 3: Kalshi REST API** (Optional Batch Arbitrage)
- **Purpose**: Check arbitrage for multiple contracts
- **Integration Type**: Parallel HTTP requests with rate limiting
- **Rate Limit Strategy**: Queue requests at 50 req/min (below 60 req/min limit)

### Internal Dependencies

**Dependency 1: nixtla-polymarket-analyst**
- **What it provides**: Single-contract forecast workflow (reusable)
- **Why needed**: Each contract in batch uses same analysis logic

**Dependency 2: Python multiprocessing**
- **What it provides**: Parallel execution across multiple CPU cores
- **Why needed**: Achieve 10x speedup

---

## 10. Constraints & Assumptions

### Technical Constraints

1. **API Rate Limits**: Polymarket (100 req/min), TimeGPT (1,000 req/month), Kalshi (60 req/min)
2. **Memory**: 10 parallel workers × 50 MB = 500 MB minimum (2 GB recommended for large batches)
3. **Processing Time**: Must complete in <10 min (user patience threshold)

### Business Constraints

1. **API Costs**: $0.05/contract (TimeGPT) → $5 for 100-contract batch (budget: <$50/month for heavy users)
2. **Timeline**: Must be ready for prediction markets vertical launch (Q1 2026)

### Assumptions

1. **Assumption 1: Users maintain watchlists in CSV/JSON**
   - **Risk if false**: Users expect direct Polymarket integration (watchlist sync)
   - **Mitigation**: Document CSV export from Polymarket UI

2. **Assumption 2: 10 parallel workers is optimal for most systems**
   - **Risk if false**: Slower systems (4 cores) may struggle with 10 workers
   - **Mitigation**: Make worker count configurable (default: min(10, CPU cores))

3. **Assumption 3: Users accept 90% success rate (some failures OK)**
   - **Risk if false**: Users expect 100% success (any failure = broken)
   - **Mitigation**: Clear documentation that failures are expected (API errors, missing data)

---

## 11. Risk Assessment

### Technical Risks

**Risk 1: TimeGPT Quota Exhaustion**
- **Probability**: High (100-contract batch = 10% of monthly quota)
- **Impact**: Critical (batch processing blocked)
- **Mitigation**: Track quota, warn users, fallback to StatsForecast

**Risk 2: Parallel Workers Overload System**
- **Probability**: Medium (users on low-end hardware)
- **Impact**: Medium (slow performance, system unresponsive)
- **Mitigation**: Auto-detect CPU cores, limit workers to min(10, CPU cores)

**Risk 3: API Rate Limit Violations**
- **Probability**: Medium (batch spikes hit rate limits)
- **Impact**: High (API blocks requests, batch fails)
- **Mitigation**: Implement request queue with conservative rate limiting (80% of max)

### User Experience Risks

**Risk 1: Users Expect Real-Time Updates**
- **Probability**: Medium (confusion between batch and streaming)
- **Impact**: Medium (user frustration)
- **Mitigation**: Clear documentation that batch is on-demand, not real-time

**Risk 2: Portfolio Report Overwhelming (Too Much Data)**
- **Probability**: Medium (50+ contracts = hundreds of metrics)
- **Impact**: Medium (users ignore report)
- **Mitigation**: Focus on top 10 opportunities, hide details in separate files

---

## 12. Open Questions

1. **Question**: Should we support watchlist auto-sync from Polymarket user accounts?
   - **Options**: A) Manual CSV import (v1.0), B) API integration (v2.0)
   - **Recommendation**: A (manual CSV for v1.0, auto-sync in v2.0 if demand exists)

2. **Question**: What should default worker count be (5, 10, 20)?
   - **Options**: 5 (conservative), 10 (balanced), 20 (aggressive)
   - **Recommendation**: 10 (min(10, CPU cores) for auto-scaling)

3. **Question**: Should batch processing support multi-platform (Polymarket + Kalshi)?
   - **Options**: A) Polymarket only (v1.0), B) Multi-platform (v2.0)
   - **Recommendation**: A (single platform for v1.0, multi-platform in v2.0)

**Recommended Decisions**:
1. Manual CSV watchlists for v1.0
2. Default 10 workers (auto-scale to CPU cores)
3. Polymarket only for v1.0

---

## 13. Appendix: Examples

### Example 1: Standard Portfolio Batch

**Input (watchlist.csv)**:
```csv
contract_id,name
0xABC123...,BTC $100k Dec 2025
0xDEF456...,ETH $10k Dec 2025
0xGHI789...,Trump wins 2024
... (47 more)
```

**Output (portfolio_summary_2025-12-05.md)**:
```markdown
# Portfolio Analysis: 50 Contracts

## Top 10 Opportunities
1. BTC $100k: +30.8% forecast change
2. ETH $10k: +28.9% forecast change
...

## Alerts (5 flagged)
- BTC $100k: Arbitrage 13.3% vs Kalshi
- ETH $10k: High forecast change (>15%)
...
```

### Example 2: Batch with Failures

**Input**: 50 contracts (5 invalid IDs)

**Output**:
```markdown
# Portfolio Analysis: 45 Contracts (90% success rate)

## Processing Summary
- **Success**: 45 contracts
- **Failed**: 5 contracts (see errors.json)
  - 0xINVALID1: Invalid contract ID format
  - 0xINVALID2: Contract not found on Polymarket
  - 0xTIMEOUT: API timeout after 3 retries
  - 0xQUOTA: TimeGPT quota exceeded (fallback to StatsForecast succeeded)
  - 0xERROR: Unknown error (logged for debugging)

## Portfolio Metrics (based on 45 successful contracts)
...
```

---

## 14. Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2025-12-05 | Initial PRD | Intent Solutions |

---

## 15. Approval

| Role | Name | Approval Date | Signature |
|------|------|---------------|-----------|
| Product Owner | Jeremy Longshore | 2025-12-05 | [Pending] |
| Tech Lead | Jeremy Longshore | 2025-12-05 | [Pending] |
| User Representative | Prediction Markets Community | TBD | [Pending] |

---

**Template maintained by**: Intent Solutions
**For**: Nixtla Skills Pack + Global Standard
**Last Updated**: 2025-12-05
