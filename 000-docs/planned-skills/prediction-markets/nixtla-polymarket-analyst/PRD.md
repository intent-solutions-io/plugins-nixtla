# Claude Skill PRD: Nixtla Polymarket Analyst

**Template Version**: 1.0.0
**Based On**: [Anthropic Skills Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)
**Purpose**: Product Requirements Document for Claude Skills
**Status**: Planned

---

## Change Log

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2025-12-05 | Initial PRD | Intent Solutions |
| 1.0.1 | 2025-12-06 | PRD de-hyped for Nixtla review: metrics reframed as evaluation goals (not guarantees), P&L and income claims removed, adoption targets made realistic, error rates replaced with engineering validation goals, explicit "analysis only / not financial advice" framing added throughout, risk section expanded with realistic assessment that models may not outperform markets | Intent Solutions |

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
| **Last Updated** | 2025-12-06 |

---

## 1. Executive Summary

**One-sentence description**: Transform Claude into a prediction market analyst that fetches Polymarket contract odds, forecasts prices using TimeGPT, analyzes potential arbitrage opportunities vs Kalshi, and generates structured analytical reports.

**Value Proposition**: Combines Polymarket's real-time prediction market data with Nixtla's TimeGPT forecasting to analyze contract pricing and identify potential cross-platform discrepancies—providing a structured workflow for prediction market analysis that doesn't currently exist in consolidated form.

**Key Evaluation Goals** (these will be measured, not guaranteed):
- Target activation accuracy: 95% (skill triggers correctly)
- Expected usage frequency: We'll track actual usage to validate demand
- Description quality target: 90%+ (measured against Nixtla standard)
- Forecast accuracy evaluation: Compare MAPE against naive baselines; goal is to be competitive or better
- Arbitrage detection validation: Measure what percentage of detected opportunities represent actual pricing discrepancies

---

## 2. Problem Statement

### Current State (Without This Skill)

**Pain Points**:
1. **Manual data fetching**: Traders manually navigate Polymarket APIs and copy data into analysis tools
2. **No integrated forecasting tools**: No readily available tools combine prediction market data fetching with time-series forecasting in a single workflow
3. **Cross-platform comparison is manual**: Identifying pricing discrepancies between Polymarket and Kalshi requires monitoring both platforms separately
4. **Time series expertise required**: Converting prediction market odds to standardized time series format requires understanding of both domains
5. **No standardized analysis**: Each analyst builds their own ad-hoc tools with inconsistent methodologies

**Current Workarounds**:
- Export Polymarket data → Import to analysis tools → Write custom forecasting code
- Monitor Polymarket and Kalshi simultaneously in separate browser tabs
- Use generic time series tools not designed specifically for prediction market workflows

**Impact of Problem**:
- Time investment: Manual analysis workflows are time-consuming
- Error-prone: Manual data handling introduces potential for mistakes
- User frustration: Complex, fragmented workflow with no standardization
- Delayed analysis: By the time manual analysis completes, market conditions may have shifted

### Desired State (With This Skill)

**Transformation**:
- From: Fragmented manual workflow requiring multiple tools and manual data transformation
- To: Integrated automated workflow with standardized methodology and structured output

**Expected Benefits**:
1. **Faster analysis**: Significantly reduced time from data fetching to forecast generation
2. **Reduced manual errors**: Automated data transformation with schema validation reduces data-handling mistakes
3. **Cross-platform analysis**: Streamlined comparison of pricing across platforms
4. **Standardized methodology**: Consistent workflow following Nixtla time-series best practices
5. **Lower barrier to entry**: Simplified workflow makes analysis accessible to users without deep time-series expertise

**Important**: This is an analysis and decision-support tool, not a trading bot or guaranteed profit generator. Users remain responsible for their own trading decisions.

---

## 3. Target Users

### Primary Users

**User Persona 1: Prediction Market Trader**
- **Background**: 2-5 years trading experience, familiar with Polymarket/Kalshi, varying technical skills
- **Goals**: Make more informed trading decisions through structured price analysis
- **Pain Points**: Manual analysis is slow, can't scale to monitor multiple contracts efficiently
- **Use Frequency**: Likely daily for active traders (actual usage TBD)
- **Technical Skills**: Understands prediction markets, basic spreadsheet skills, varying coding proficiency
- **Value**: Faster, more structured analysis workflow; access to time-series forecasting techniques

**User Persona 2: Data Scientist (Quantitative Analyst)**
- **Background**: Strong Python/stats background, exploring prediction markets as a forecasting domain
- **Goals**: Apply time series forecasting techniques to prediction markets, validate TimeGPT performance on this data type
- **Pain Points**: Unfamiliar with prediction market APIs and data formats, need standardized workflows
- **Use Frequency**: Likely weekly for research and experimentation
- **Technical Skills**: Expert in ML/stats, proficient in Python, learning prediction markets domain
- **Value**: Research insights, benchmarking platform, methodology exploration

### Secondary Users

**Market Researchers**: Track prediction market sentiment on political/economic events
**Journalists**: Analyze prediction market trends for data-driven stories
**Academic Researchers**: Study prediction market dynamics and forecasting model performance

---

## 4. User Stories

**Format**: "As a [user type], I want [capability], so that [benefit]"

### Critical User Stories (Must Have)

1. **As a** prediction market trader,
   **I want** to analyze a Polymarket contract and get a structured price forecast,
   **So that** I can make more informed trading decisions based on time-series analysis.

   **Acceptance Criteria**:
   - [ ] Workflow completes in reasonable time (<120 seconds target, <60 seconds stretch goal)
   - [ ] Forecast includes point predictions + confidence intervals
   - [ ] Visual representation shows historical data + forecast
   - [ ] Output provides structured analysis: data summary, forecast, and interpretation
   - [ ] Works with any valid Polymarket contract ID

2. **As a** prediction market trader,
   **I want** to compare Polymarket forecasts vs Kalshi current odds,
   **So that** I can identify potential pricing discrepancies across platforms.

   **Acceptance Criteria**:
   - [ ] Compares Polymarket forecast vs Kalshi current price (when available)
   - [ ] Calculates spread and displays comparison
   - [ ] Filters by configurable minimum spread threshold (default 5%)
   - [ ] Presents findings in structured format
   - [ ] Includes disclaimer that identified discrepancies are informational only

3. **As a** data scientist,
   **I want** the skill to transform Polymarket odds into Nixtla-compatible time series format automatically,
   **So that** I can focus on analysis instead of data wrangling.

   **Acceptance Criteria**:
   - [ ] Automatically converts JSON odds → CSV time series
   - [ ] Validates data quality (schema checks, completeness)
   - [ ] Handles binary contracts (YES/NO odds)
   - [ ] Outputs standard 3-column format: unique_id, ds, y
   - [ ] Logs data quality warnings and validation results

### High-Priority User Stories (Should Have)

4. **As a** trader,
   **I want** to specify custom forecast horizons,
   **So that** I can align forecasts with my analysis timeframe.

   **Acceptance Criteria**:
   - [ ] Accepts `--horizon` parameter (default: 14 days)
   - [ ] Supports reasonable horizon ranges
   - [ ] Adjusts confidence intervals based on horizon length
   - [ ] Warns if horizon exceeds contract expiration date

5. **As a** trader,
   **I want** fallback to StatsForecast when TimeGPT quota is exceeded,
   **So that** I can continue analysis even when API limits are reached.

   **Acceptance Criteria**:
   - [ ] Detects TimeGPT quota errors automatically
   - [ ] Switches to StatsForecast (AutoETS, AutoTheta, SeasonalNaive)
   - [ ] Logs which model was used (TimeGPT or StatsForecast)
   - [ ] Produces consistent output format regardless of engine

### Nice-to-Have User Stories (Could Have)

6. **As a** power user,
   **I want** to batch-process multiple contracts,
   **So that** I can analyze my watchlist more efficiently.

7. **As a** researcher,
   **I want** to export forecast data to CSV for further analysis,
   **So that** I can perform custom validation and experimentation.

---

## 5. Functional Requirements

### Core Capabilities (Must Have)

**REQ-1: Polymarket Data Fetching**
- **Description**: Fetch historical contract odds from Polymarket GraphQL API for specified contract ID
- **Rationale**: Foundation of the workflow—need historical data to perform time-series analysis
- **Acceptance Criteria**:
  - [ ] Accepts contract ID as input (hex format validation)
  - [ ] Fetches historical odds data (minimum viable history: 14 days; default: 30 days)
  - [ ] Retrieves: timestamp, yes_price, no_price, volume, liquidity
  - [ ] Handles API errors gracefully (retries with exponential backoff)
  - [ ] Saves raw data to structured format
- **Dependencies**: Polymarket API access (public, no authentication required)

**REQ-2: Time Series Transformation**
- **Description**: Convert Polymarket odds JSON to Nixtla-compatible CSV time series format
- **Rationale**: TimeGPT requires specific 3-column format (unique_id, ds, y); transformation ensures data quality
- **Acceptance Criteria**:
  - [ ] Parses JSON, extracts yes_price as target variable
  - [ ] Converts timestamps to ISO 8601 format
  - [ ] Generates unique_id from contract metadata
  - [ ] Validates: no critical data gaps, prices within valid range [0, 1], chronological order
  - [ ] Saves to CSV with standard 3-column schema
- **Dependencies**: REQ-1 (raw data)

**REQ-3: TimeGPT Forecasting**
- **Description**: Generate price forecast using Nixtla TimeGPT API with confidence intervals
- **Rationale**: Apply time-series forecasting to prediction market prices
- **Acceptance Criteria**:
  - [ ] Calls TimeGPT API with time series data + horizon
  - [ ] Retrieves point forecasts + 80%/95% confidence intervals
  - [ ] Performs basic forecast validation (checks for anomalies)
  - [ ] Handles API quota errors → fallback to StatsForecast
  - [ ] Saves forecast to structured format
- **Dependencies**: REQ-2 (time series data), NIXTLA_API_KEY environment variable

**REQ-4: Cross-Platform Pricing Analysis**
- **Description**: Compare Polymarket forecast vs Kalshi current odds to identify potential pricing discrepancies
- **Rationale**: Provide cross-platform analysis capability
- **Acceptance Criteria**:
  - [ ] Fetches equivalent Kalshi contract odds (if contract mapping exists)
  - [ ] Calculates spread: abs(polymarket_forecast - kalshi_current)
  - [ ] Filters by configurable minimum spread threshold (default 5%)
  - [ ] Ranks by spread magnitude
  - [ ] Saves comparison to structured format
- **Dependencies**: REQ-3 (forecast), Kalshi API access (optional)

**REQ-5: Analysis Report Generation**
- **Description**: Generate markdown report with forecast visualization, cross-platform comparison, and structured analysis
- **Rationale**: Deliverable output that users can review and use for decision support
- **Acceptance Criteria**:
  - [ ] Loads forecast + comparison data
  - [ ] Generates ASCII or text-based chart of price predictions
  - [ ] Formats analysis findings with clear structure
  - [ ] Includes confidence intervals and uncertainty quantification
  - [ ] Saves to timestamped markdown file
  - [ ] **Includes prominent disclaimer**: "This tool provides informational analysis only. It is not financial advice, does not guarantee profitable trades, and users remain responsible for their own trading decisions."
- **Dependencies**: REQ-3 (forecast), REQ-4 (comparison data)

### Integration Requirements

**REQ-API-1: Polymarket GraphQL API**
- **Purpose**: Fetch historical contract odds and metadata
- **Endpoints**: `https://gamma-api.polymarket.com/` (GraphQL)
- **Authentication**: None required (public data)
- **Rate Limits**: 100 requests/minute (sufficient for typical single-contract analysis)
- **Error Handling**: Retry 3x with exponential backoff on 5xx errors, fail gracefully on 4xx with informative message

**REQ-API-2: Nixtla TimeGPT API**
- **Purpose**: Generate price forecasts with confidence intervals
- **Endpoints**: `https://api.nixtla.io/timegpt/forecast`
- **Authentication**: API key (header: `X-API-Key`)
- **Rate Limits**: Quota-based (1,000 requests/month typical for standard tier)
- **Cost Considerations**: Usage-based pricing; estimated $0.01-$0.10 per forecast depending on series length
- **Error Handling**: 402 Payment Required → automatic fallback to StatsForecast (local, free)

**REQ-API-3: Kalshi API** (Optional)
- **Purpose**: Fetch current odds for cross-platform comparison
- **Endpoints**: `https://trading-api.kalshi.com/v1/markets`
- **Authentication**: API key (optional feature)
- **Rate Limits**: 60 requests/minute
- **Error Handling**: Graceful degradation—if Kalshi API unavailable or contract unmapped, skip comparison step (Step 4)

### Data Requirements

**REQ-DATA-1: Input Data Format**
- **Format**: Contract ID (string)
- **Required Fields**: Hex address (40 characters, 0x prefix)
- **Optional Fields**: Date range (ISO 8601), forecast horizon (integer)
- **Validation Rules**: Regex match `^0x[a-f0-9]{40}$`, horizon: reasonable range (e.g., 1-90 days)

**REQ-DATA-2: Output Data Format**
- **Format**: Markdown report + CSV forecast data
- **Fields**:
  - Report: Data summary, forecast visualization, comparison table, structured analysis, risk disclaimers
  - CSV: unique_id, ds, TimeGPT (or model name), TimeGPT-lo-80, TimeGPT-hi-80, TimeGPT-lo-95, TimeGPT-hi-95
- **Quality Standards**: Validation checks throughout pipeline; clear logging of data quality warnings

### Performance Requirements

**REQ-PERF-1: Response Time**
- **Goal**: Complete analysis in <60 seconds for standard single-contract analysis
- **Acceptable**: <120 seconds
- **Breakdown estimates**:
  - Step 1 (Fetch): <10 seconds
  - Step 2 (Transform): <5 seconds
  - Step 3 (Forecast): <40 seconds (TimeGPT API call)
  - Step 4 (Comparison): <15 seconds
  - Step 5 (Report): <10 seconds

**REQ-PERF-2: Token Budget**
- **Description Size**: <250 characters (fits within 15k token budget)
- **SKILL.md Size**: <500 lines (~2,500 tokens target)
- **Total Skill Size**: <5,000 tokens including all references

### Quality Requirements

**REQ-QUAL-1: Description Quality**
- **Target Score**: 90%+ on Nixtla quality formula (exceeds 80% minimum)
- **Must Include**:
  - [X] Action-oriented verbs: "Orchestrates", "Fetches", "Transforms", "Forecasts", "Analyzes", "Generates"
  - [X] "Use when [scenarios]" clause: "analyzing prediction markets, forecasting contract prices, exploring cross-platform pricing"
  - [X] "Trigger with '[phrases]'" examples: "analyze Polymarket contract", "forecast prediction market", "compare platforms"
  - [X] Domain keywords: "Polymarket", "Kalshi", "TimeGPT", "time series", "forecasting"

**REQ-QUAL-2: Engineering Validation Goals**
- **Forecast Quality Evaluation**: We will measure MAPE and compare against naive baselines (e.g., last-value-carried-forward, simple moving average)
  - **Initial Goal**: Match or beat naive baselines in majority of test cases
  - **Stretch Goal**: 10-20% relative improvement where data permits
  - **Reality Check**: Prediction market data is noisy and may not be highly forecastable; primary value may be in structured analysis workflow, not superior predictive accuracy
- **Data Transformation Accuracy**: Schema validation, unit tests for transformation logic, integration tests for end-to-end pipeline
- **Workflow Reliability**: Comprehensive error handling, graceful degradation, detailed logging
- **Comparison Validation**: For cross-platform analysis, validate that detected discrepancies represent actual pricing differences (not data artifacts)

---

## 6. Non-Goals (Out of Scope)

**What This Skill Does NOT Do**:

1. **Automated Trading Execution**
   - **Rationale**: This is strictly an analysis and decision-support tool. It does NOT execute trades automatically due to regulatory concerns, safety considerations, and the fact that it cannot guarantee profitable outcomes.
   - **Alternative**: Users review analysis and manually execute trades on their chosen platforms based on their own judgment
   - **Explicit Stance**: This tool provides informational forecasts and structured analysis—not trading signals or financial advice

2. **Guaranteed Profits or Performance**
   - **Rationale**: Prediction markets are influenced by many factors beyond historical price patterns. Forecasts are probabilistic estimates, not guarantees.
   - **Reality**: Models may not consistently outperform market prices. The tool's primary value is in providing faster, more structured analysis—not guaranteed alpha generation.

3. **Real-Time Streaming Analysis**
   - **Rationale**: Skill runs on-demand analysis, not continuous monitoring
   - **Alternative**: Users can schedule periodic runs (e.g., cron job) for quasi-real-time updates

4. **Portfolio Optimization**
   - **Rationale**: Single-contract focus initially, not multi-contract portfolio allocation
   - **Alternative**: Stack with other analysis tools for portfolio-level work
   - **May be added in**: Future version after validating single-contract value

5. **Historical Backtesting**
   - **Rationale**: Focus is on forward-looking forecasts, not historical strategy validation
   - **Alternative**: Export forecast data to CSV, use external backtesting tools
   - **Depends on**: User demand for this feature

---

## 7. Success Metrics

### Skill Activation Metrics

**Metric 1: Activation Accuracy**
- **Definition**: % of times skill activates correctly when user intent matches skill purpose
- **Target**: 95%+
- **Measurement**: Manual testing with representative trigger phrase variations
- **Test Phrases**: "analyze Polymarket contract", "forecast prediction market", "compare Polymarket vs Kalshi"

**Metric 2: False Positive Rate**
- **Definition**: % of times skill activates when user wanted something different
- **Target**: <3%
- **Measurement**: User feedback + monitoring logs

### Quality Metrics

**Metric 3: Description Quality Score**
- **Formula**: 6-criterion weighted scoring (see Nixtla standard)
- **Target**: 90%+ (exceeds 80% minimum)
- **Components**: Action-oriented, clear triggers, comprehensive, natural language, specificity, technical terms

**Metric 4: SKILL.md Size**
- **Target**: <500 lines
- **Max**: 500 lines (hard limit for token budget)

### Usage Metrics

**Metric 5: Adoption & Usage Validation**
- **Goal**: Achieve 20-50 active users running ≥10 analyses each in first 60 days to validate practical usefulness
- **Rationale**: Need real-world usage data to validate that the tool provides value in practice
- **Measurement**: Skill invocation logs, community feedback
- **Reality Check**: Actual adoption will depend on market interest, tool quality, and whether it solves real user problems

**Metric 6: User Satisfaction**
- **Target**: 4.0/5 rating (realistic for v1.0)
- **Measurement**: Optional post-analysis feedback (non-intrusive)

### Performance & Accuracy Evaluation

**Metric 7: Forecast Accuracy Evaluation**
- **Approach**: Compare MAPE (Mean Absolute Percentage Error) against naive baselines on historical contracts
- **Baseline Comparisons**: Last-value-carried-forward, simple moving average, seasonal naive
- **Initial Goal**: Be competitive with (at least as good as) naive baselines
- **Stretch Goal**: 10-20% relative improvement in MAPE where data permits
- **Important Caveat**: Prediction market prices may not be highly forecastable; if models don't consistently outperform baselines, primary value lies in workflow automation and structured analysis, not predictive superiority

**Metric 8: Cross-Platform Comparison Validation**
- **Approach**: For detected pricing discrepancies, validate that opportunities reflect actual pricing differences (not data artifacts or timing issues)
- **Goal**: ≥70% of detected discrepancies (above threshold) represent genuine cross-platform pricing gaps when manually validated
- **Measurement**: Sample-based manual validation of identified opportunities

---

## 8. User Experience Flow

### Typical Usage Flow

1. **User Intent**: Trader wants to analyze "Will Bitcoin reach $100k by Dec 2025?" contract on Polymarket
2. **Trigger**: User says "Analyze Polymarket contract 0xABC123456 and forecast the next 14 days"
3. **Skill Activation**: Claude recognizes need for `nixtla-polymarket-analyst` skill
4. **Skill Execution**:
   - Step 1: Fetch historical odds from Polymarket API
   - Step 2: Transform JSON → CSV time series format
   - Step 3: Call TimeGPT API for forecast (or StatsForecast fallback)
   - Step 4: Check Kalshi for comparable contract, calculate pricing comparison
   - Step 5: Generate markdown report with forecast, comparison, and structured analysis
5. **Output Delivered**: Markdown report with forecast visualization, cross-platform comparison, and analysis
6. **User Action**: Reviews report and decides on next steps based on their own judgment and risk tolerance

### Example Scenario

**Scenario**: Active trader exploring crypto prediction market contract

**Input**:
```
Analyze the Polymarket contract 0x1234567890abcdef1234567890abcdef12345678
(Will Bitcoin reach $100k by December 2025?) and forecast the next 14 days.
Also check if there are potential pricing discrepancies vs Kalshi.
```

**Claude's Response**:
```
I'll analyze this Polymarket contract using the nixtla-polymarket-analyst skill.
This will fetch historical odds, generate a forecast using TimeGPT, and check for
cross-platform pricing comparison vs Kalshi.

[Skill executes 5-step workflow]

✓ Analysis complete! I've generated a structured report.
```

**Output** (`reports/polymarket_BTC_100k_2025-12-05.md`):
```markdown
# Polymarket Analysis: Will Bitcoin Reach $100k by Dec 2025?

**Contract**: 0x1234567890abcdef1234567890abcdef12345678
**Analysis Date**: 2025-12-05
**Forecast Horizon**: 14 days (through 2025-12-19)

**⚠️ DISCLAIMER**: This analysis is provided for informational purposes only and is not financial advice. Forecasts are probabilistic estimates with significant uncertainty. This tool does not guarantee profitable trades. Users remain responsible for their own trading decisions and risk management.

## Data Summary

- **Historical Data**: 30 days (2025-11-05 to 2025-12-05)
- **Current YES Price**: 0.52
- **Model Used**: TimeGPT
- **Validation**: Data quality checks passed

## Forecast Overview

**14-Day Point Forecast**: 0.52 → 0.56 (+7.7%)

**Confidence Intervals**:
- 80% CI: [0.50, 0.62]
- 95% CI: [0.46, 0.66]

**Interpretation**: Moderate upward trend with wide confidence intervals indicating substantial uncertainty.

## Forecast Visualization

```
YES Price
0.70│
0.65│             ╭──────
0.60│         ╭───╯
0.55│     ╭───╯
0.50│─────╯
0.45│
    └──────────────────────> Time
    Now  +3d  +7d  +10d  +14d

Shaded area represents 80% confidence interval
```

## Cross-Platform Comparison

| Platform | Current Price | 14d Forecast | Spread | Notes |
|----------|---------------|--------------|--------|-------|
| Polymarket | 0.52 | 0.56 | - | Forecasted |
| Kalshi | 0.54 | - | 0.02 | Below 5% threshold |

**Analysis**: Current cross-platform spread is 2% (below 5% threshold). No significant pricing discrepancy detected at this time.

## Structured Analysis

**Trend**: Moderate upward price movement suggested by forecast

**Uncertainty**: Wide confidence intervals reflect market volatility and forecast uncertainty

**Cross-Platform**: Polymarket and Kalshi prices are currently well-aligned

**Risk Factors**:
- Bitcoin is highly volatile; external news and market conditions can rapidly change dynamics
- Confidence intervals are wide, indicating forecast uncertainty
- Prediction market odds incorporate collective market intelligence; forecasts may not outperform market consensus

## Data Quality Notes

- No data gaps detected
- All prices within valid range [0, 1]
- Chronological order validated
- Series length: 30 days (adequate for forecasting)

---

*Generated by nixtla-polymarket-analyst | Powered by TimeGPT*
*This is an analytical tool, not a trading system. Not financial advice.*
```

**User Benefit**: Trader receives structured analysis in ~60 seconds instead of manual multi-hour workflow, can review forecast and make informed decisions based on their own judgment

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
- **Cost**: Usage-based (~$0.05 per forecast; reasonable for value provided)

**System 3: Kalshi REST API** (Optional)
- **Purpose**: Fetch current contract odds for cross-platform comparison
- **Integration Type**: REST API (HTTP GET)
- **Authentication**: API key (optional—skill works without it via graceful degradation)
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
   - Polymarket: 100 req/min (not a constraint for typical single-contract analysis)
   - TimeGPT: Quota-based (1,000 req/month typical; may limit heavy users—fallback to StatsForecast available)
   - Kalshi: 60 req/min (not a constraint)
3. **Processing Time**: Target <60 seconds, acceptable <120 seconds
4. **Dependencies**: Requires Python 3.9+, internet connection, API keys (TimeGPT key for full functionality)

### Business Constraints

1. **API Costs**: TimeGPT usage costs ~$0.05/forecast (users should budget accordingly; StatsForecast fallback available)
2. **Timeline**: Aligned with prediction markets vertical exploration timeline
3. **Resources**: Realistic development and testing effort

### Assumptions

1. **Assumption 1: Users have basic Polymarket familiarity**
   - **Risk if false**: Users may not understand contract IDs, odds interpretation
   - **Mitigation**: Provide examples in documentation, link to Polymarket resources

2. **Assumption 2: TimeGPT forecasts are reasonably applicable to prediction market data**
   - **Risk if false**: Poor forecast quality → user distrust → skill abandoned
   - **Mitigation**: Validate on historical data before launch, provide StatsForecast fallback, set realistic expectations that forecasts are exploratory tools not guaranteed alpha generators

3. **Assumption 3: Cross-platform pricing discrepancies occur with sufficient frequency to be valuable**
   - **Risk if false**: Users frequently get "No discrepancy found" → feature perceived as low-value
   - **Mitigation**: Set realistic expectations that significant discrepancies are opportunistic, not guaranteed; emphasize forecast value as primary feature

4. **Assumption 4: Users will execute trades manually based on their own analysis of the reports**
   - **Risk if false**: Users expect automated trading (out of scope and potentially problematic)
   - **Mitigation**: Crystal-clear documentation that skill is analysis-only, not a trading bot; prominent disclaimers in every report

---

## 11. Risk Assessment

### Technical Risks

**Risk 1: TimeGPT API Rate Limiting**
- **Probability**: Medium-High (quota-based, 1,000 req/month for typical tier)
- **Impact**: Medium (skill stops working mid-month for heavy users)
- **Mitigation**:
  - Implement StatsForecast fallback (free, local)
  - Log which model was used
  - Warn users about quota usage
  - Document cost expectations upfront

**Risk 2: Forecast Accuracy Below Expectations**
- **Probability**: Medium-High (prediction markets are noisy, may not be highly forecastable)
- **Impact**: Medium-High (poor forecasts could lead to user distrust)
- **Mitigation**:
  - **Set realistic expectations upfront**: Clearly communicate that this is an experimental analysis tool, not a proven alpha generator
  - Validate against naive baselines on historical contracts before launch
  - If models don't consistently outperform baselines, pivot messaging to emphasize workflow automation and structured analysis as primary value
  - Wide confidence intervals communicate uncertainty
  - Provide risk disclaimers in every report
  - Make StatsForecast fallback visible so users can compare approaches

**Risk 3: Models May Not Outperform Market Prices**
- **Probability**: High (markets are often efficient; forecasting edge is difficult to achieve)
- **Impact**: High (if users expect guaranteed profits and don't get them)
- **Mitigation**:
  - **Primary mitigation**: Frame tool as analysis and exploration platform, NOT profit guarantee
  - **Secondary value**: Even if forecasts don't outperform markets, the tool provides:
    - Faster data aggregation and transformation
    - Structured analytical workflow
    - Confidence interval quantification
    - Documentation of assumptions
    - Learning platform for time-series techniques
  - **Explicit messaging**: "This tool helps you analyze prediction markets more systematically. It does not guarantee that forecasts will outperform market prices or lead to profitable trades."

**Risk 4: Polymarket API Changes**
- **Probability**: Medium (APIs evolve over time)
- **Impact**: High (skill could break)
- **Mitigation**:
  - Version pin API endpoints
  - Monitor Polymarket developer communications
  - Graceful error handling with informative messages
  - Plan for maintenance updates

### User Experience Risks

**Risk 1: Skill Over-Triggering (False Positives)**
- **Probability**: Low (well-crafted description with specific domain terminology)
- **Impact**: Medium (user annoyance, but not harmful)
- **Mitigation**:
  - Precise description with prediction market specific terms
  - Test with diverse trigger phrase variations
  - Iterate based on user feedback

**Risk 2: Skill Under-Triggering (False Negatives)**
- **Probability**: Medium (users may use non-standard phrasing)
- **Impact**: Medium (skill not activated when it should be)
- **Mitigation**:
  - Comprehensive trigger phrases in description
  - Document example phrases clearly
  - Gather user feedback on missed activations

**Risk 3: Users Misinterpret Analysis as Trading Advice or Guaranteed Profits**
- **Probability**: High (overconfidence in AI predictions is common)
- **Impact**: Critical (financial losses → reputational damage, potential liability concerns)
- **Mitigation**:
  - **Explicit, prominent disclaimers in every report**: "This is informational analysis only, not financial advice"
  - **Risk assessment sections** with confidence intervals and uncertainty quantification
  - **Conservative language**: Avoid "BUY/SELL" signals; use "suggests", "indicates", "exploratory analysis"
  - **Documentation**: Clear user guide emphasizing tool limitations and user responsibility
  - **No position sizing recommendations**: Remove specific portfolio allocation suggestions (e.g., "2-5% of portfolio")—users must make their own risk management decisions

---

## 12. Open Questions

**Questions Requiring Decisions**:

1. **Question**: Should we support categorical markets (>2 outcomes) or only binary markets initially?
   - **Options**:
     - Option A: Binary only (simpler, faster to validate)
     - Option B: Binary + categorical (more versatile, more complex)
   - **Decision Needed By**: Before development starts
   - **Owner**: Product Lead (Intent Solutions)

2. **Question**: What should default forecast horizon be (7, 14, or 30 days)?
   - **Options**:
     - 7 days: Faster, lower API cost, suitable for short-term analysis
     - 14 days: Balanced (recommended)
     - 30 days: More context, higher API cost, potentially less accurate for volatile markets
   - **Decision Needed By**: Before v1.0 release
   - **Owner**: Product Lead + validation testing

3. **Question**: Should cross-platform comparison be mandatory or optional?
   - **Options**:
     - Mandatory: Always run (requires Kalshi API key or public endpoint access)
     - Optional: Skip if Kalshi API unavailable (graceful degradation)
   - **Decision Needed By**: Before development
   - **Owner**: Technical Lead

**Recommended Decisions**:
1. Binary only for v1.0 (categorical in future version if demand exists)
2. Default 14-day horizon (user can override via parameter)
3. Optional cross-platform comparison with graceful degradation

---

## 13. Appendix: Examples

### Example 1: Standard Polymarket Analysis

**User Request**:
```
Analyze Polymarket contract 0xABC123 (Trump wins 2024) and forecast next 14 days
```

**Expected Skill Behavior**:
1. Fetch historical YES/NO price data from Polymarket
2. Transform JSON → CSV time series (YES price as target)
3. Call TimeGPT API with 14-day horizon (or StatsForecast fallback)
4. Check Kalshi for comparable contract (if available/configured)
5. Generate report with forecast visualization, comparison, and structured analysis

**Expected Output Highlights**:
```markdown
# Polymarket Analysis: Trump Wins 2024

**⚠️ DISCLAIMER**: Informational analysis only. Not financial advice.

**Forecast**: YES price 0.52 → 0.54 (+3.8%) over next 14 days
**Confidence**: 80% CI [0.48, 0.60], 95% CI [0.44, 0.64]
**Cross-Platform**: Kalshi price 0.53 (within 2% of forecast; no significant discrepancy)
**Analysis**: Mild upward trend with moderate uncertainty. Wide confidence intervals reflect market volatility.

**Risk Factors**: Political events can rapidly shift market dynamics; forecast reflects historical patterns but cannot predict external shocks.
```

### Example 2: Hypothetical Cross-Platform Comparison (Example Only)

**User Request**:
```
Compare Bitcoin price forecasts between Polymarket and Kalshi
```

**Expected Skill Behavior**:
1. Fetch Polymarket "BTC $100k by Dec 2025" contract
2. Transform → forecast (14-day horizon)
3. Fetch Kalshi equivalent contract
4. Calculate spread: abs(polymarket_forecast - kalshi_current)
5. Generate comparison report

**Expected Output (Hypothetical Example)**:
```markdown
# Cross-Platform Pricing Comparison (Hypothetical Example)

**Contract**: BTC reaches $100k by Dec 2025

| Platform | Current/Forecast | Type | Spread | Notes |
|----------|------------------|------|--------|-------|
| Polymarket | 0.68 | 14d Forecast | - | TimeGPT projection |
| Kalshi | 0.60 | Current Price | 8% | As of analysis time |

**Analysis**: This is a hypothetical scenario showing how cross-platform comparison would be presented. An 8% spread would exceed the 5% threshold and be flagged for user attention.

**Important**: This is informational only. Pricing discrepancies can close rapidly, may reflect different market liquidity or participant bases, and do not guarantee profitable arbitrage opportunities. Users should verify current prices before taking action.
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
5. Generate report with note about model used

**Expected Output**:
```markdown
# Polymarket Analysis: [Contract Name]

**Model Used**: StatsForecast (AutoETS)
*Note: TimeGPT quota exceeded. Forecast generated using local StatsForecast models (no API cost).*

**Forecast**: YES price 0.45 → 0.47 (+4.4%) over next 14 days
**Confidence**: 80% CI [0.43, 0.51]
**Analysis**: Mild upward trend. StatsForecast models provide solid baseline forecasts.

**Interpretation**: StatsForecast provides classical time-series forecasting as an alternative to TimeGPT. Results may differ in accuracy depending on data characteristics.
```

---

## 14. Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2025-12-05 | Initial PRD | Intent Solutions |
| 1.0.1 | 2025-12-06 | De-hyped for Nixtla review (see Change Log at top) | Intent Solutions |

---

## 15. Approval

| Role | Name | Approval Date | Signature |
|------|------|---------------|-----------|
| Product Owner | Jeremy Longshore | 2025-12-06 | [Pending] |
| Tech Lead | Jeremy Longshore | 2025-12-06 | [Pending] |
| User Representative | Prediction Markets Community | TBD | [Pending] |

---

**Template maintained by**: Intent Solutions
**For**: Nixtla Skills Pack + Global Standard
**Last Updated**: 2025-12-06
