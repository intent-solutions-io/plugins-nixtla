# Claude Skill PRD: Nixtla Polymarket Analyst

**Template Version**: 1.0.0
**Based On**: [Anthropic Skills Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)
**Purpose**: Product Requirements Document for Claude Skills
**Status**: Planned

---

## Document Control

| Field | Value |
|-------|-------|
| **Skill Name** | nixtla-polymarket-analyst |
| **Skill Type** | [X] Mode Skill [ ] Utility Skill |
| **Domain** | Prediction Markets + Time Series Forecasting |
| **Target Users** | Traders, Data Scientists, Market Analysts |
| **Priority** | [X] Critical [ ] High [ ] Medium [ ] Low |
| **Status** | [X] Planned [ ] In Development [ ] Complete |
| **Owner** | Intent Solutions |
| **Last Updated** | 2025-12-05 |

---

## 1. Executive Summary

**One-sentence description**: Transform Claude into a prediction market analyst that fetches Polymarket contract odds, forecasts prices using TimeGPT, analyzes arbitrage opportunities vs Kalshi, and generates actionable trading recommendations.

**Value Proposition**: Combines Polymarket's real-time prediction market data with Nixtla's TimeGPT forecasting to identify mispriced contracts and arbitrage opportunities across platforms—a capability not available in any existing tool.

**Key Metrics**:
- Target activation accuracy: 95%
- Expected usage frequency: 5-10 times per day (active traders)
- Description quality target: 90%+
- Forecast accuracy target: MAPE <15%
- Arbitrage detection success rate: >70%

---

## 2. Problem Statement

### Current State (Without This Skill)

**Pain Points**:
1. **Manual data fetching**: Traders manually copy/paste Polymarket odds into spreadsheets (15-30 min per contract)
2. **No forecasting tools**: No tools exist to forecast prediction market contract prices—traders rely on gut feeling
3. **Cross-platform arbitrage is invisible**: Identifying mispricing between Polymarket and Kalshi requires monitoring both platforms manually (impossible at scale)
4. **Time series expertise required**: Converting prediction market odds to time series format requires understanding of both domains (rare skillset)
5. **No standardized analysis**: Each analyst builds their own ad-hoc tools with inconsistent methodologies

**Current Workarounds**:
- Export Polymarket data to CSV → Import to Python → Write custom forecasting code (2-4 hours)
- Monitor Polymarket and Kalshi simultaneously in browser tabs (mentally calculate spreads)
- Use generic time series tools not designed for prediction markets (poor fit)

**Impact of Problem**:
- Time wasted: 2-4 hours per analysis
- Error rate: 30-40% (manual data entry errors, incorrect transformations)
- User frustration level: High (complex, error-prone, no standardization)
- Missed opportunities: Arbitrage opportunities expire before manual analysis completes

### Desired State (With This Skill)

**Transformation**:
- From: Manual 2-4 hour analysis per contract with 30-40% error rate
- To: Automated 60-second analysis with <5% error rate and standardized methodology

**Expected Benefits**:
1. **10x faster analysis**: 2-4 hours → 60 seconds (99% time reduction)
2. **Higher accuracy**: 30-40% error rate → <5% error rate (86% improvement)
3. **Arbitrage detection**: Identify cross-platform opportunities automatically (impossible manually at scale)
4. **Standardized methodology**: Every analysis follows the same proven workflow
5. **Accessible to non-experts**: No time series or forecasting expertise required

---

## 3. Target Users

### Primary Users

**User Persona 1: Prediction Market Trader**
- **Background**: 2-5 years trading experience, familiar with Polymarket/Kalshi, limited Python skills
- **Goals**: Maximize profit through accurate price predictions and arbitrage opportunities
- **Pain Points**: Manual analysis is too slow, can't scale to monitor 10+ contracts, missing profitable trades
- **Use Frequency**: Daily (5-10 analyses per day)
- **Technical Skills**: Understands prediction markets deeply, basic spreadsheet skills, limited coding
- **Annual Income Impact**: $50k-$200k potential (improved trade timing + arbitrage)

**User Persona 2: Data Scientist (Quantitative Analyst)**
- **Background**: Strong Python/stats background, new to prediction markets, exploring forecasting techniques
- **Goals**: Apply time series forecasting to prediction markets, validate TimeGPT vs traditional methods
- **Pain Points**: Unfamiliar with prediction market APIs and data formats, need standardized workflows
- **Use Frequency**: Weekly (research and backtesting)
- **Technical Skills**: Expert in ML/stats, proficient in Python, learning prediction markets domain
- **Value**: Research insights, portfolio optimization, methodology validation

### Secondary Users

**Market Researchers**: Track prediction market sentiment on political/economic events
**Journalists**: Analyze prediction market trends for news stories
**Academic Researchers**: Study prediction market efficiency and forecasting accuracy

---

## 4. User Stories

**Format**: "As a [user type], I want [capability], so that [benefit]"

### Critical User Stories (Must Have)

1. **As a** prediction market trader,
   **I want** to analyze a Polymarket contract and get a 14-day price forecast in under 60 seconds,
   **So that** I can make timely trading decisions before market conditions change.

   **Acceptance Criteria**:
   - [ ] Total workflow execution <60 seconds for standard contract
   - [ ] Forecast includes point predictions + 80%/95% confidence intervals
   - [ ] Visual chart shows historical data + forecast
   - [ ] Recommendation is clear: BUY/SELL/HOLD with reasoning
   - [ ] Works with any Polymarket contract ID

2. **As a** prediction market trader,
   **I want** to automatically identify arbitrage opportunities between Polymarket and Kalshi,
   **So that** I can profit from price discrepancies across platforms.

   **Acceptance Criteria**:
   - [ ] Compares Polymarket forecast vs Kalshi current price
   - [ ] Calculates spread and potential profit %
   - [ ] Filters opportunities by minimum spread threshold (default 5%)
   - [ ] Ranks opportunities by profit potential
   - [ ] Provides specific trade instructions (buy on X, sell on Y)

3. **As a** data scientist,
   **I want** the skill to transform Polymarket odds into Nixtla-compatible time series format automatically,
   **So that** I can focus on analysis instead of data wrangling.

   **Acceptance Criteria**:
   - [ ] Automatically converts JSON odds → CSV time series
   - [ ] Validates data quality (no gaps, proper frequency)
   - [ ] Handles multiple contract types (binary, categorical)
   - [ ] Outputs standard 3-column format: unique_id, ds, y
   - [ ] Logs data quality warnings (missing dates, outliers)

### High-Priority User Stories (Should Have)

4. **As a** trader,
   **I want** to specify custom forecast horizons (7, 14, 30 days),
   **So that** I can align forecasts with my trading timeframe.

   **Acceptance Criteria**:
   - [ ] Accepts `--horizon` parameter (default: 14 days)
   - [ ] Supports horizons from 1 to 90 days
   - [ ] Adjusts confidence intervals based on horizon length
   - [ ] Warns if horizon exceeds contract expiration date

5. **As a** trader,
   **I want** fallback to StatsForecast when TimeGPT quota is exceeded,
   **So that** I can continue analysis even when API limits are reached.

   **Acceptance Criteria**:
   - [ ] Detects TimeGPT quota errors automatically
   - [ ] Switches to StatsForecast (AutoETS, AutoTheta, SeasonalNaive)
   - [ ] Logs which model was used (TimeGPT or StatsForecast)
   - [ ] Produces same output format regardless of engine

### Nice-to-Have User Stories (Could Have)

6. **As a** power user,
   **I want** to batch-process 10+ contracts in parallel,
   **So that** I can analyze my entire watchlist in one command.

7. **As a** researcher,
   **I want** to export forecast data to CSV for further analysis,
   **So that** I can perform custom backtesting and validation.

---

## 5. Functional Requirements

### Core Capabilities (Must Have)

**REQ-1: Polymarket Data Fetching**
- **Description**: Fetch historical contract odds from Polymarket GraphQL API for any contract ID
- **Rationale**: Foundation of the workflow—need real historical data to forecast
- **Acceptance Criteria**:
  - [ ] Accepts contract ID as input (hex format: 0x[a-f0-9]{40})
  - [ ] Fetches minimum 14 days of historical odds (30 days default)
  - [ ] Retrieves: timestamp, yes_price, no_price, volume, liquidity
  - [ ] Handles API errors gracefully (retries with exponential backoff)
  - [ ] Saves raw data to `data/raw_odds.json`
- **Dependencies**: Polymarket API access (free, no authentication required)

**REQ-2: Time Series Transformation**
- **Description**: Convert Polymarket odds JSON to Nixtla-compatible CSV time series format
- **Rationale**: TimeGPT requires specific 3-column format (unique_id, ds, y)
- **Acceptance Criteria**:
  - [ ] Parses JSON, extracts yes_price as target variable
  - [ ] Converts timestamps to ISO 8601 format
  - [ ] Generates unique_id from contract metadata
  - [ ] Validates: no missing dates, prices 0 ≤ y ≤ 1, chronological order
  - [ ] Saves to `data/timeseries.csv` (3 columns)
- **Dependencies**: REQ-1 (raw data)

**REQ-3: TimeGPT Forecasting**
- **Description**: Generate 14-day forecast using Nixtla TimeGPT API with confidence intervals
- **Rationale**: Core value proposition—accurate price predictions
- **Acceptance Criteria**:
  - [ ] Calls TimeGPT API with time series data + horizon
  - [ ] Retrieves point forecasts + 80%/95% confidence intervals
  - [ ] Validates forecast quality (MAPE, coverage)
  - [ ] Handles API quota errors → fallback to StatsForecast
  - [ ] Saves forecast to `data/forecast.csv`
- **Dependencies**: REQ-2 (time series data), NIXTLA_API_KEY environment variable

**REQ-4: Cross-Platform Arbitrage Analysis**
- **Description**: Compare Polymarket forecast vs Kalshi current odds to identify mispricing
- **Rationale**: Key differentiator—automated arbitrage detection
- **Acceptance Criteria**:
  - [ ] Fetches equivalent Kalshi contract odds (if exists)
  - [ ] Calculates spread: abs(polymarket_forecast - kalshi_current)
  - [ ] Filters opportunities by minimum spread (default 5%)
  - [ ] Ranks by potential profit percentage
  - [ ] Saves to `data/arbitrage.json`
- **Dependencies**: REQ-3 (forecast), Kalshi API access (optional)

**REQ-5: Trading Recommendations Report**
- **Description**: Generate markdown report with forecast chart, arbitrage opportunities, and actionable recommendations
- **Rationale**: Final deliverable that traders use to make decisions
- **Acceptance Criteria**:
  - [ ] Loads forecast + arbitrage data
  - [ ] Generates ASCII chart of price predictions
  - [ ] Formats trading recommendations: BUY/SELL/HOLD with reasoning
  - [ ] Includes risk assessment (confidence intervals)
  - [ ] Saves to `reports/analysis_YYYY-MM-DD.md`
- **Dependencies**: REQ-3 (forecast), REQ-4 (arbitrage)

### Integration Requirements

**REQ-API-1: Polymarket GraphQL API**
- **Purpose**: Fetch historical contract odds and metadata
- **Endpoints**: `https://gamma-api.polymarket.com/` (GraphQL)
- **Authentication**: None required (public data)
- **Rate Limits**: 100 requests/minute (generous for single-contract analysis)
- **Error Handling**: Retry 3x with exponential backoff on 5xx errors, fail gracefully on 4xx

**REQ-API-2: Nixtla TimeGPT API**
- **Purpose**: Generate price forecasts with confidence intervals
- **Endpoints**: `https://api.nixtla.io/timegpt/forecast`
- **Authentication**: API key (header: `X-API-Key`)
- **Rate Limits**: 1,000 requests/month (quota-based, not rate-limited)
- **Cost Considerations**: $0.01-$0.10 per forecast (depending on series length)
- **Error Handling**: 402 Payment Required → fallback to StatsForecast (local, free)

**REQ-API-3: Kalshi API** (Optional)
- **Purpose**: Fetch current odds for arbitrage comparison
- **Endpoints**: `https://trading-api.kalshi.com/v1/markets`
- **Authentication**: API key (optional feature)
- **Rate Limits**: 60 requests/minute
- **Error Handling**: Graceful degradation—if Kalshi API fails, skip arbitrage analysis (Step 4)

### Data Requirements

**REQ-DATA-1: Input Data Format**
- **Format**: Contract ID (string)
- **Required Fields**: Hex address (40 characters, 0x prefix)
- **Optional Fields**: Date range (ISO 8601), forecast horizon (integer)
- **Validation Rules**: Regex match `^0x[a-f0-9]{40}$`, horizon 1-90 days

**REQ-DATA-2: Output Data Format**
- **Format**: Markdown report + CSV forecast data
- **Fields**:
  - Report: Executive summary, forecast chart, arbitrage table, recommendations
  - CSV: unique_id, ds, TimeGPT, TimeGPT-lo-80, TimeGPT-hi-80, TimeGPT-lo-95, TimeGPT-hi-95
- **Quality Standards**: Forecast MAPE <15%, arbitrage opportunities have >5% spread

### Performance Requirements

**REQ-PERF-1: Response Time**
- **Target**: <60 seconds for standard single-contract analysis
- **Max Acceptable**: <120 seconds
- **Breakdown**:
  - Step 1 (Fetch): <5 seconds
  - Step 2 (Transform): <2 seconds
  - Step 3 (Forecast): <30 seconds
  - Step 4 (Arbitrage): <10 seconds
  - Step 5 (Report): <5 seconds

**REQ-PERF-2: Token Budget**
- **Description Size**: 248 characters (fits in 15k token budget) ✓
- **SKILL.md Size**: <500 lines (~2,500 tokens)
- **Total Skill Size**: <5,000 tokens including all references

### Quality Requirements

**REQ-QUAL-1: Description Quality**
- **Target Score**: 90%+ on quality formula (exceeds 80% minimum)
- **Must Include**:
  - [X] Action-oriented verbs: "Orchestrates", "Fetches", "Transforms", "Forecasts", "Analyzes", "Generates"
  - [X] "Use when [scenarios]" clause: "analyzing prediction markets, forecasting contract prices, identifying mispriced opportunities"
  - [X] "Trigger with '[phrases]'" examples: "analyze Polymarket contract", "forecast prediction market", "find arbitrage"
  - [X] Domain keywords: "Polymarket", "Kalshi", "TimeGPT", "arbitrage", "time series"

**REQ-QUAL-2: Accuracy**
- **Forecast Accuracy**: MAPE <15% (mean absolute percentage error)
- **Data Parsing Accuracy**: 99.9%+ (no data corruption in transformations)
- **Error Rate**: <5% (workflow failures due to bugs)
- **Arbitrage Detection**: 70%+ success rate (opportunities actually exist and are profitable)

---

## 6. Non-Goals (Out of Scope)

**What This Skill Does NOT Do**:

1. **Automated Trading Execution**
   - **Rationale**: Skill provides analysis and recommendations, but does NOT execute trades automatically (regulatory/safety concerns)
   - **Alternative**: User manually executes trades on Polymarket/Kalshi based on recommendations

2. **Real-Time Streaming Analysis**
   - **Rationale**: Skill runs on-demand analysis, not continuous monitoring
   - **Alternative**: Use cron job to run skill every N hours for quasi-real-time updates

3. **Portfolio Optimization**
   - **Rationale**: Single-contract focus, not multi-contract portfolio allocation
   - **Alternative**: Stack with `nixtla-correlation-mapper` skill for portfolio analysis
   - **May be added in**: v2.0 (after initial release proves single-contract value)

4. **Historical Backtesting**
   - **Rationale**: Forward-looking forecasts only, not historical strategy validation
   - **Alternative**: Export forecast data to CSV, use external backtesting tools
   - **Depends on**: User demand for this feature

---

## 7. Success Metrics

### Skill Activation Metrics

**Metric 1: Activation Accuracy**
- **Definition**: % of times skill activates when it should (based on trigger phrases)
- **Target**: 95%+
- **Measurement**: Manual testing with 20 trigger phrase variations
- **Test Phrases**: "analyze Polymarket contract", "forecast prediction market", "find arbitrage on Polymarket"

**Metric 2: False Positive Rate**
- **Definition**: % of times skill activates incorrectly (user wanted something else)
- **Target**: <3%
- **Measurement**: User feedback + monitoring logs

### Quality Metrics

**Metric 3: Description Quality Score**
- **Formula**: 6-criterion weighted scoring (see ARD)
- **Target**: 90%+ (exceeds 80% minimum)
- **Components**:
  - Action-oriented: 20% (target: 20/20 = perfect)
  - Clear triggers: 25% (target: 25/25 = perfect)
  - Comprehensive: 15% (target: 14/15 = near-perfect)
  - Natural language: 20% (target: 18/20 = excellent)
  - Specificity: 10% (target: 9/10 = excellent)
  - Technical terms: 10% (target: 10/10 = perfect)
  - **Total Target**: 90/100

**Metric 4: SKILL.md Size**
- **Target**: <500 lines
- **Max**: 500 lines (hard limit due to token budget)
- **Current**: TBD (to be measured after implementation)

### Usage Metrics

**Metric 5: Adoption Rate**
- **Target**: 60% of active prediction market traders (Polymarket Discord community) try skill within first month
- **Measurement**: Skill invocation logs, community feedback

**Metric 6: User Satisfaction**
- **Target**: 4.5/5 rating
- **Measurement**: Post-analysis survey (optional prompt after skill completes)

### Performance Metrics

**Metric 7: Forecast Accuracy**
- **Domain-Specific**: MAPE (Mean Absolute Percentage Error) <15%
- **Target**: Beat naive baseline (last-value-carried-forward) by 30%+
- **Measurement**: Backtest on historical Polymarket contracts, compare forecast vs actual resolution

**Metric 8: Arbitrage Success Rate**
- **Target**: 70%+ of detected opportunities are profitable when executed
- **Measurement**: User feedback on actual trades executed

---

## 8. User Experience Flow

### Typical Usage Flow

1. **User Intent**: Trader wants to analyze "Will Bitcoin reach $100k by Dec 2025?" contract on Polymarket
2. **Trigger**: User says "Analyze Polymarket contract 0xABC123456 and forecast the next 14 days"
3. **Skill Activation**: Claude recognizes need for `nixtla-polymarket-analyst` skill
4. **Skill Execution**:
   - Step 1: Fetch 30 days of historical odds from Polymarket API
   - Step 2: Transform JSON → CSV time series format
   - Step 3: Call TimeGPT API for 14-day forecast
   - Step 4: Check Kalshi for same contract, calculate arbitrage spread
   - Step 5: Generate markdown report with chart + recommendations
5. **Output Delivered**: Markdown report with forecast, arbitrage opportunities, trade recommendations
6. **User Action**: Reviews report, decides to BUY on Kalshi at 0.60 (forecast: 0.68, 13% profit potential)

### Example Scenario

**Scenario**: Active trader analyzing crypto prediction market contract

**Input**:
```
Analyze the Polymarket contract 0x1234567890abcdef1234567890abcdef12345678
(Will Bitcoin reach $100k by December 2025?) and forecast the next 14 days.
Also check if there are arbitrage opportunities vs Kalshi.
```

**Claude's Response**:
```
I'll analyze this Polymarket contract using the nixtla-polymarket-analyst skill.
This will fetch historical odds, forecast prices using TimeGPT, and check for
arbitrage opportunities vs Kalshi.

[Skill executes 5-step workflow in ~45 seconds]

✓ Analysis complete! I've generated a comprehensive report.
```

**Output** (`reports/polymarket_BTC_100k_2025-12-05.md`):
```markdown
# Polymarket Analysis: Will Bitcoin Reach $100k by Dec 2025?

**Contract**: 0x1234567890abcdef1234567890abcdef12345678
**Analysis Date**: 2025-12-05
**Forecast Horizon**: 14 days (through 2025-12-19)

## Executive Summary
Forecasted YES price to rise from 0.52 → 0.68 (+30.8%) over next 14 days with high
confidence. Strong arbitrage opportunity detected: Kalshi trading at 0.60 vs our
forecast of 0.68 (13.3% profit potential).

## Forecast Chart
```
YES Price
0.70│                 ╭─────
0.68│             ╭───╯
0.66│         ╭───╯
0.64│     ╭───╯
0.62│ ╭───╯
0.60│─╯
0.58│
    └──────────────────────────> Time
    Now  +3d  +7d  +10d  +14d

95% Confidence: [0.58, 0.78]
80% Confidence: [0.62, 0.74]
```

## Arbitrage Opportunities

| Platform | Current Price | Forecast (14d) | Spread | Profit % | Confidence |
|----------|---------------|----------------|--------|----------|------------|
| Kalshi    | 0.60         | 0.68           | 0.08   | 13.3%    | High       |

## Trading Recommendations

🟢 **BUY SIGNAL**: Strong upward trend with arbitrage opportunity

**Recommended Action**:
1. BUY Kalshi YES at 0.60 (current price)
2. Target SELL at 0.68 (14-day forecast)
3. Potential profit: 13.3% (before fees)

**Risk Assessment**: Medium
- Wide confidence intervals indicate market uncertainty
- Bitcoin is volatile—external news could invalidate forecast
- Arbitrage window may close quickly (monitor Kalshi price)

**Position Sizing**: Recommend 2-5% of portfolio (medium risk)

---

*Generated by nixtla-polymarket-analyst | Powered by TimeGPT*
```

**User Benefit**: Trader identifies profitable arbitrage opportunity in 45 seconds (vs 2-4 hours manual analysis), executes trade, realizes 13% profit

---

## 9. Integration Points

### External Systems

**System 1: Polymarket GraphQL API**
- **Purpose**: Fetch historical contract odds and market metadata
- **Integration Type**: GraphQL API (HTTP POST)
- **Authentication**: None required (public data)
- **Data Flow**: Skill → Polymarket API → Raw odds JSON

**System 2: Nixtla TimeGPT API**
- **Purpose**: Generate price forecasts with confidence intervals
- **Integration Type**: REST API (HTTP POST)
- **Authentication**: API key in header
- **Cost**: ~$0.05 per forecast (reasonable for value provided)

**System 3: Kalshi REST API** (Optional)
- **Purpose**: Fetch current contract odds for arbitrage comparison
- **Integration Type**: REST API (HTTP GET)
- **Authentication**: API key (optional—skill works without it)
- **Data Flow**: Skill → Kalshi API → Current odds JSON

### Internal Dependencies

**Dependency 1: Nixtla Schema Standard**
- **What it provides**: 3-column time series format (unique_id, ds, y)
- **Why needed**: TimeGPT requires this specific schema

**Dependency 2: Python Libraries**
- **Libraries**: `nixtla`, `statsforecast`, `pandas`, `requests`
- **Versions**:
  - nixtla >= 0.5.0 (TimeGPT support)
  - statsforecast >= 1.7.0 (fallback models)
  - pandas >= 2.0.0 (data manipulation)

**Dependency 3: Global Standard Skill Schema**
- **What it provides**: Architecture patterns, token budget limits, quality standards
- **Why needed**: Ensures skill is built to production standards

---

## 10. Constraints & Assumptions

### Technical Constraints

1. **Token Budget**: Must fit in 5,000 token limit (description + SKILL.md + references)
2. **API Rate Limits**:
   - Polymarket: 100 req/min (not a constraint for single-contract analysis)
   - TimeGPT: 1,000 req/month (may limit heavy users—fallback to StatsForecast)
   - Kalshi: 60 req/min (not a constraint)
3. **Processing Time**: Must complete in <120 seconds (target <60 seconds)
4. **Dependencies**: Requires Python 3.9+, internet connection, API keys

### Business Constraints

1. **API Costs**: TimeGPT usage costs ~$0.05/forecast (budget: <$50/month for heavy users)
2. **Timeline**: Skill must be ready for prediction markets vertical launch (Q1 2026)
3. **Resources**: 1 developer, 40 hours development + testing

### Assumptions

1. **Assumption 1: Users have Polymarket familiarity**
   - **Risk if false**: Users may not understand contract IDs, odds interpretation
   - **Mitigation**: Provide examples in documentation, link to Polymarket docs

2. **Assumption 2: TimeGPT forecasts are accurate for prediction market data**
   - **Risk if false**: Poor forecasts → user distrust → skill abandoned
   - **Mitigation**: Validate accuracy on historical data before launch, provide StatsForecast fallback

3. **Assumption 3: Arbitrage opportunities exist frequently enough to be valuable**
   - **Risk if false**: Users get "No arbitrage found" message too often
   - **Mitigation**: Set realistic expectations (arbitrage is rare), emphasize forecast value

4. **Assumption 4: Users will execute trades manually based on recommendations**
   - **Risk if false**: Users expect automated trading (out of scope)
   - **Mitigation**: Clear documentation that skill is analysis-only, not trading bot

---

## 11. Risk Assessment

### Technical Risks

**Risk 1: TimeGPT API Rate Limiting**
- **Probability**: High (quota-based, 1,000 req/month)
- **Impact**: High (skill stops working mid-month for heavy users)
- **Mitigation**:
  - Implement StatsForecast fallback (free, local)
  - Log which model was used
  - Warn users about quota usage

**Risk 2: Forecast Accuracy Below Threshold**
- **Probability**: Medium (prediction markets are noisy)
- **Impact**: High (inaccurate forecasts → bad trades → user distrust)
- **Mitigation**:
  - Validate MAPE <15% on historical contracts before launch
  - Wide confidence intervals communicate uncertainty
  - Provide risk assessment in every report

**Risk 3: Polymarket API Changes**
- **Probability**: Medium (APIs evolve)
- **Impact**: High (skill breaks completely)
- **Mitigation**:
  - Version pin API endpoints
  - Monitor Polymarket developer announcements
  - Graceful error handling with helpful messages

### User Experience Risks

**Risk 1: Skill Over-Triggering (False Positives)**
- **Probability**: Low (well-crafted description with specific triggers)
- **Impact**: Medium (user annoyance, but not harmful)
- **Mitigation**:
  - Precise description with prediction market terminology
  - Test with 20+ trigger phrase variations
  - Iterate based on user feedback

**Risk 2: Skill Under-Triggering (False Negatives)**
- **Probability**: Medium (users may use non-standard phrasing)
- **Impact**: Medium (skill not activated when it should be)
- **Mitigation**:
  - Comprehensive trigger phrases in description
  - Document example phrases in SKILL.md
  - Gather user feedback on missed activations

**Risk 3: Users Misinterpret Recommendations as Guaranteed Profits**
- **Probability**: High (overconfidence in AI predictions)
- **Impact**: Critical (financial losses → reputational damage)
- **Mitigation**:
  - Explicit disclaimers in every report
  - Risk assessment with confidence intervals
  - Position sizing recommendations (2-5% of portfolio)

---

## 12. Open Questions

**Questions Requiring Decisions**:

1. **Question**: Should we support categorical markets (>2 outcomes) or only binary markets initially?
   - **Options**:
     - Option A: Binary only (simpler, faster to market)
     - Option B: Binary + categorical (more versatile, more complex)
   - **Decision Needed By**: Before development starts
   - **Owner**: Product Lead (Intent Solutions)

2. **Question**: What should default forecast horizon be (7, 14, or 30 days)?
   - **Options**:
     - 7 days: Faster, less API cost, good for short-term traders
     - 14 days: Balanced (recommended)
     - 30 days: More context, higher API cost, less accurate for volatile markets
   - **Decision Needed By**: Before v1.0 release
   - **Owner**: Product Lead + User feedback

3. **Question**: Should arbitrage analysis be mandatory or optional?
   - **Options**:
     - Mandatory: Always run (requires Kalshi API key)
     - Optional: Skip if Kalshi API key not provided (graceful degradation)
   - **Decision Needed By**: Before development
   - **Owner**: Technical Lead

**Recommended Decisions**:
1. Binary only for v1.0 (categorical in v1.1)
2. Default 14-day horizon (user can override)
3. Optional arbitrage (graceful degradation)

---

## 13. Appendix: Examples

### Example 1: Standard Polymarket Analysis

**User Request**:
```
Analyze Polymarket contract 0xABC123 (Trump wins 2024) and forecast next 14 days
```

**Expected Skill Behavior**:
1. Fetch 30 days of historical YES/NO price data from Polymarket
2. Transform JSON → CSV time series (YES price as target)
3. Call TimeGPT API with 14-day horizon
4. Check Kalshi for "Trump wins 2024" contract (if API key provided)
5. Generate report with forecast chart, arbitrage opportunities, recommendations

**Expected Output**:
```markdown
# Polymarket Analysis: Trump Wins 2024

**Forecast**: YES price 0.52 → 0.56 (+7.7%) over next 14 days
**Arbitrage**: No opportunities found (Kalshi price within 2% of forecast)
**Recommendation**: HOLD current position
**Risk**: Medium (wide confidence intervals)
```

### Example 2: Arbitrage Opportunity Detection

**User Request**:
```
Find arbitrage opportunities for Bitcoin price contracts on Polymarket vs Kalshi
```

**Expected Skill Behavior**:
1. Fetch Polymarket "BTC $100k by Dec 2025" contract
2. Transform → forecast (14-day horizon)
3. Fetch Kalshi equivalent contract
4. Calculate spread: abs(0.68 forecast - 0.60 Kalshi current) = 0.08 (8%)
5. Generate report highlighting arbitrage

**Expected Output**:
```markdown
# Arbitrage Opportunity Detected

**Platform**: Polymarket vs Kalshi
**Contract**: BTC reaches $100k by Dec 2025
**Spread**: 8% (above 5% threshold)
**Recommendation**: BUY Kalshi YES at 0.60, target SELL at 0.68
**Profit Potential**: 13.3%
**Confidence**: High (tight confidence intervals)
```

### Example 3: Edge Case - TimeGPT Quota Exceeded

**User Request**:
```
Analyze Polymarket contract 0xDEF456 and forecast 14 days
```

**Expected Behavior**:
1. Fetch Polymarket data (Step 1 succeeds)
2. Transform to time series (Step 2 succeeds)
3. Call TimeGPT API → 402 Payment Required (quota exceeded)
4. Automatically fallback to StatsForecast (AutoETS, AutoTheta, SeasonalNaive)
5. Generate report with note: "Forecast generated using StatsForecast (TimeGPT quota exceeded)"

**Expected Output**:
```markdown
# Polymarket Analysis: [Contract Name]

*Note: Forecast generated using StatsForecast (local models).
TimeGPT quota exceeded—forecasts will resume next month.*

**Forecast**: YES price 0.45 → 0.48 (+6.7%) over next 14 days
**Model Used**: AutoETS (local, no API cost)
**Recommendation**: Weak BUY signal (moderate confidence)
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
