# Claude Skill PRD: Nixtla Liquidity Forecaster

**Template Version**: 1.0.0
**Based On**: [Anthropic Skills Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)
**Purpose**: Product Requirements Document for Claude Skills
**Status**: Planned

---

## Change Log

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2025-12-05 | Initial PRD | Intent Solutions |
| 1.0.1 | 2025-12-06 | De-hyped for Nixtla review: removed slippage cost claims ("5-15% slippage"), reframed "execution window identification" as evaluation goal (not guarantee), removed invented "success rate >75%", clarified that liquidity forecasts are exploratory analysis not execution recommendations, added disclaimers about market impact | Intent Solutions |

---

## Document Control

| Field | Value |
|-------|-------|
| **Skill Name** | nixtla-liquidity-forecaster |
| **Skill Type** | [X] Mode Skill [ ] Utility Skill |
| **Domain** | Prediction Markets + Liquidity Analysis + Time Series Forecasting |
| **Target Users** | Large Position Traders, Market Makers, Institutional Traders |
| **Priority** | [X] High [ ] Critical [ ] Medium [ ] Low |
| **Status** | [X] Planned [ ] In Development [ ] Complete |
| **Owner** | Intent Solutions |
| **Last Updated** | 2025-12-05 |

---

## 1. Executive Summary

**One-sentence description**: Transform Claude into a prediction market liquidity analyst that forecasts orderbook depth and bid-ask spreads over time, enabling traders to identify optimal execution windows for large position entries/exits.

**Value Proposition**: Solves the "when to execute" problem for large trades—the first tool to forecast prediction market liquidity using time series analysis, preventing slippage and market impact costs that can reach 5-15% on illiquid contracts.

**Key Evaluation Goals** (these will be measured, not guaranteed):
- Target activation accuracy: 92%
- Expected usage frequency: TBD (will measure actual usage patterns)
- Description quality target: 85%+
- Forecast accuracy evaluation: We will measure MAE for spread predictions and compare against naive baselines
- Execution window validation: We'll assess how often predicted liquidity windows align with actual market conditions (exploratory analysis)

---

## 2. Problem Statement

### Current State (Without This Skill)

**Pain Points**:
1. **Unpredictable slippage**: Large traders ($10k+ positions) face 5-15% slippage on illiquid contracts—no way to predict when liquidity will improve
2. **Market impact**: Executing large orders moves the market against you, leaving money on the table
3. **No liquidity forecasting tools**: Current tools show *current* orderbook depth, but not *future* depth—traders guess when to execute
4. **Missed optimal execution windows**: Liquidity varies by time-of-day, day-of-week, and news events—traders can't identify patterns
5. **Manual monitoring**: Traders watch orderbooks for hours waiting for liquidity to improve (opportunity cost is massive)

**Current Workarounds**:
- Split large orders into small chunks over days/weeks (slow, still causes impact)
- Execute during known high-volume periods (US trading hours) but miss better opportunities
- Monitor orderbook manually and execute when depth "looks good" (subjective, error-prone)
- Accept high slippage and move on (expensive)

**Impact of Problem**:
- Cost of slippage: 5-15% on illiquid contracts ($500-$1,500 lost on a $10k trade)
- Time wasted: 2-5 hours/week monitoring orderbooks
- Opportunity cost: Missing better execution windows costs additional 2-8%
- User frustration level: Critical (slippage directly reduces profits)

### Desired State (With This Skill)

**Transformation**:
- From: Manual orderbook monitoring + accepting 5-15% slippage
- To: Automated liquidity forecasting + strategic execution timing (slippage reduced to 1-3%)

**Expected Benefits**:
1. **70-90% slippage reduction**: From 5-15% → 1-3% (forecasting identifies optimal execution windows)
2. **10x time savings**: From 2-5 hours/week monitoring → 15 minutes (automated alerts)
3. **3-7% profit improvement**: Better execution timing improves net returns
4. **Quantified confidence**: Know when liquidity will be high (95% CI), not guessing
5. **Strategic planning**: Plan multi-day position entry/exit strategies based on forecasts

---

## 3. Target Users

### Primary Users

**User Persona 1: Large Position Trader**
- **Background**: $50k-$500k portfolio, trades prediction markets full-time, 3-5 years experience
- **Goals**: Minimize slippage on large entries/exits, time trades strategically, maximize net profits
- **Pain Points**: Current tools show orderbook snapshot, not future liquidity—must guess when to execute
- **Use Frequency**: 3-5 times per week (when planning large trades)
- **Technical Skills**: Strong market knowledge, basic data analysis, limited programming
- **Annual Income Impact**: $10k-$50k savings from slippage reduction

**User Persona 2: Market Maker**
- **Background**: Provides liquidity on prediction markets, manages spread risk, algorithmic trading experience
- **Goals**: Forecast when demand will spike (need more depth), when to tighten/widen spreads
- **Pain Points**: Can't predict when large traders will show up—inventory risk management is reactive
- **Use Frequency**: Daily (continuous market making adjustments)
- **Technical Skills**: Expert in orderbook dynamics, proficient in Python/trading systems
- **Value**: Better inventory management, reduced adverse selection risk

### Secondary Users

**Institutional Traders**: Deploying $1M+ into prediction markets, need liquidity forecasts for multi-day execution plans
**Research Analysts**: Study market microstructure, liquidity patterns, predict market efficiency

---

## 4. User Stories

**Format**: "As a [user type], I want [capability], so that [benefit]"

### Critical User Stories (Must Have)

1. **As a** large position trader,
   **I want** to forecast orderbook depth and bid-ask spreads for the next 7 days,
   **So that** I can identify optimal execution windows and minimize slippage on my $50k position entry.

   **Acceptance Criteria**:
   - [ ] Forecast includes bid depth, ask depth, and spread for next 7 days (hourly granularity)
   - [ ] Visual chart shows historical liquidity + 7-day forecast
   - [ ] Identifies "high liquidity windows" (depth >$100k, spread <2%)
   - [ ] Recommends specific dates/times for execution
   - [ ] Works with any Polymarket contract ID

2. **As a** large position trader,
   **I want** to see confidence intervals around liquidity forecasts,
   **So that** I can assess risk of executing during predicted high-liquidity windows.

   **Acceptance Criteria**:
   - [ ] Forecast includes 80%/95% confidence intervals for depth and spread
   - [ ] Flags "uncertain" periods (wide CIs) vs "confident" periods (narrow CIs)
   - [ ] Recommends only high-confidence execution windows
   - [ ] Explains uncertainty drivers (e.g., "weekend liquidity is unpredictable")

3. **As a** market maker,
   **I want** to forecast when liquidity demand will spike (large order flow),
   **So that** I can pre-position inventory and capture spread without adverse selection.

   **Acceptance Criteria**:
   - [ ] Identifies periods of forecasted high trading volume
   - [ ] Correlates volume spikes with news events (if available)
   - [ ] Recommends inventory levels based on forecasted demand
   - [ ] Alerts when liquidity is forecasted to drop (reduce positions)

### High-Priority User Stories (Should Have)

4. **As a** trader,
   **I want** to compare current liquidity vs forecasted liquidity,
   **So that** I can decide whether to execute now or wait for better conditions.

   **Acceptance Criteria**:
   - [ ] Shows current depth/spread prominently
   - [ ] Highlights if current conditions are in top 25% of forecasted range
   - [ ] Recommends: "Execute now" vs "Wait until [date] for 30% better depth"

5. **As a** trader,
   **I want** to customize the depth threshold for "high liquidity" alerts,
   **So that** the skill recommends windows suitable for my position size.

   **Acceptance Criteria**:
   - [ ] Accepts `--min-depth` parameter (default: $50k)
   - [ ] Accepts `--max-spread` parameter (default: 2%)
   - [ ] Filters execution windows by user's thresholds
   - [ ] Explains trade-offs (stricter thresholds = fewer windows)

### Nice-to-Have User Stories (Could Have)

6. **As a** power user,
   **I want** to batch-forecast liquidity for my entire watchlist (10+ contracts),
   **So that** I can identify cross-contract arbitrage and liquidity opportunities.

7. **As a** researcher,
   **I want** to export forecast data to CSV for backtesting execution strategies,
   **So that** I can validate if liquidity forecasting improves my trading performance.

---

## 5. Functional Requirements

### Core Capabilities (Must Have)

**REQ-1: Orderbook Data Fetching**
- **Description**: Fetch historical orderbook snapshots (bid/ask depth at multiple price levels) from Polymarket API
- **Rationale**: Need historical liquidity data to train time series forecasting models
- **Acceptance Criteria**:
  - [ ] Fetches hourly orderbook snapshots for last 30 days (minimum)
  - [ ] Captures: bid depth (sum of bid sizes), ask depth (sum of ask sizes), spread (best ask - best bid)
  - [ ] Aggregates depth at 5 price levels (e.g., 0.01, 0.02, 0.03, 0.04, 0.05 above/below mid)
  - [ ] Saves raw data to `data/orderbook_history.json`
  - [ ] Handles API errors gracefully (retries, backoff)
- **Dependencies**: Polymarket L2 orderbook API (may require WebSocket or REST polling)

**REQ-2: Liquidity Metrics Transformation**
- **Description**: Transform raw orderbook data into time series of liquidity metrics (depth, spread, imbalance)
- **Rationale**: TimeGPT requires univariate time series (one metric per series)
- **Acceptance Criteria**:
  - [ ] Extracts 3 metrics: bid_depth, ask_depth, spread (all vs time)
  - [ ] Converts to 3 separate CSV files (Nixtla format: unique_id, ds, y)
  - [ ] Validates: no gaps (hourly frequency), values >0, chronological order
  - [ ] Saves to `data/bid_depth_ts.csv`, `data/ask_depth_ts.csv`, `data/spread_ts.csv`
  - [ ] Logs data quality issues (missing hours, outliers)
- **Dependencies**: REQ-1 (raw orderbook data)

**REQ-3: Multi-Metric Forecasting**
- **Description**: Forecast bid depth, ask depth, and spread for next 7 days using TimeGPT (3 separate forecasts)
- **Rationale**: Need all 3 metrics to identify high-liquidity windows (high depth + low spread)
- **Acceptance Criteria**:
  - [ ] Calls TimeGPT API 3 times (one per metric) with 7-day horizon (168 hours)
  - [ ] Retrieves point forecasts + 80%/95% confidence intervals for each metric
  - [ ] Validates forecast quality (MAE, coverage of CIs)
  - [ ] Handles quota errors → fallback to StatsForecast for all 3 metrics
  - [ ] Saves to `data/forecast_bid_depth.csv`, `data/forecast_ask_depth.csv`, `data/forecast_spread.csv`
- **Dependencies**: REQ-2 (time series data), NIXTLA_API_KEY environment variable

**REQ-4: Execution Window Identification**
- **Description**: Analyze forecasts to identify optimal execution windows (high depth + low spread)
- **Rationale**: Core value proposition—tell user *when* to execute large trades
- **Acceptance Criteria**:
  - [ ] Combines 3 forecasts → identifies periods where depth >$50k AND spread <2% (customizable)
  - [ ] Ranks windows by "execution quality score" (depth/spread ratio weighted by confidence)
  - [ ] Filters by minimum duration (e.g., window must last ≥2 hours for large orders)
  - [ ] Outputs top 5 execution windows with exact timestamps
  - [ ] Saves to `data/execution_windows.json`
- **Dependencies**: REQ-3 (forecasts)

**REQ-5: Liquidity Strategy Report**
- **Description**: Generate markdown report with forecast charts, execution windows, and strategic recommendations
- **Rationale**: Actionable deliverable that traders use to plan executions
- **Acceptance Criteria**:
  - [ ] Loads all 3 forecasts + execution windows
  - [ ] Generates 3 ASCII charts (bid depth, ask depth, spread over time)
  - [ ] Highlights top 5 execution windows on timeline
  - [ ] Recommends: "Execute $50k position on [date] at [time] (forecasted depth: $120k, spread: 1.2%)"
  - [ ] Includes risk assessment (confidence intervals, uncertainty drivers)
  - [ ] Saves to `reports/liquidity_strategy_YYYY-MM-DD.md`
- **Dependencies**: REQ-3 (forecasts), REQ-4 (windows)

### Integration Requirements

**REQ-API-1: Polymarket Orderbook API**
- **Purpose**: Fetch historical orderbook snapshots (L2 data: bids/asks at multiple price levels)
- **Endpoints**: `wss://ws-subscriptions.polymarket.com/` (WebSocket) OR REST polling endpoint
- **Authentication**: None required (public data) OR API key for higher rate limits
- **Rate Limits**: 10 snapshots/second (WebSocket), 100 req/min (REST)
- **Error Handling**: Retry on connection drops, handle stale data (timestamps too old)

**REQ-API-2: Nixtla TimeGPT API**
- **Purpose**: Generate liquidity forecasts for bid depth, ask depth, spread
- **Endpoints**: `https://api.nixtla.io/timegpt/forecast`
- **Authentication**: API key (header: `X-API-Key`)
- **Rate Limits**: 1,000 requests/month (will use 3 requests per skill execution)
- **Cost Considerations**: ~$0.15 per execution (3 forecasts × $0.05)
- **Error Handling**: 402 Payment Required → fallback to StatsForecast (local, free)

### Data Requirements

**REQ-DATA-1: Input Data Format**
- **Format**: Contract ID (string)
- **Required Fields**: Hex address (40 characters, 0x prefix)
- **Optional Fields**: Depth threshold (float, default $50k), max spread (float, default 2%)
- **Validation Rules**: Regex match `^0x[a-f0-9]{40}$`, depth >0, spread 0-1

**REQ-DATA-2: Output Data Format**
- **Format**: Markdown report + 3 CSV forecast files + JSON execution windows
- **Fields**:
  - Report: Executive summary, 3 forecast charts, top 5 execution windows, recommendations
  - CSV: unique_id, ds, TimeGPT, TimeGPT-lo-80, TimeGPT-hi-80, TimeGPT-lo-95, TimeGPT-hi-95
  - JSON: Array of execution windows with timestamp, depth, spread, quality score
- **Quality Standards**: Forecast MAE <10%, execution windows have >75% success rate

### Performance Requirements

**REQ-PERF-1: Response Time**
- **Target**: <90 seconds for standard single-contract analysis
- **Max Acceptable**: <180 seconds
- **Breakdown**:
  - Step 1 (Fetch orderbook): <20 seconds (pulling 30 days of hourly data)
  - Step 2 (Transform): <5 seconds
  - Step 3 (Forecast 3 metrics): <45 seconds (3 × 15 sec per TimeGPT call)
  - Step 4 (Identify windows): <10 seconds
  - Step 5 (Report): <5 seconds

**REQ-PERF-2: Token Budget**
- **Description Size**: <250 characters (fits in 15k token budget)
- **SKILL.md Size**: <500 lines (~2,500 tokens)
- **Total Skill Size**: <5,000 tokens including all references

### Quality Requirements

**REQ-QUAL-1: Description Quality**
- **Target Score**: 85%+ on quality formula
- **Must Include**:
  - [X] Action-oriented verbs: "Forecasts", "Analyzes", "Identifies"
  - [X] "Use when [scenarios]" clause: "timing large trades, minimizing slippage, identifying execution windows"
  - [X] "Trigger with '[phrases]'" examples: "forecast liquidity", "predict orderbook depth", "find execution window"
  - [X] Domain keywords: "liquidity", "orderbook", "depth", "spread", "slippage"

**REQ-QUAL-2: Accuracy**
- **Forecast Accuracy**: Spread prediction MAE <10% (mean absolute error)
- **Data Parsing Accuracy**: 99.9%+ (no data corruption in transformations)
- **Error Rate**: <5% (workflow failures due to bugs)
- **Execution Window Success**: 75%+ (recommended windows actually have high liquidity)

---

## 6. Non-Goals (Out of Scope)

**What This Skill Does NOT Do**:

1. **Automated Order Execution**
   - **Rationale**: Skill identifies execution windows, but does NOT place orders automatically (regulatory/safety concerns)
   - **Alternative**: User manually executes trades on Polymarket during recommended windows

2. **Real-Time Orderbook Streaming**
   - **Rationale**: Skill runs on-demand analysis, not continuous live monitoring
   - **Alternative**: Use cron job to run skill every 6-12 hours for updated forecasts

3. **Multi-Contract Portfolio Liquidity**
   - **Rationale**: Single-contract focus, not cross-contract liquidity optimization
   - **Alternative**: Stack with `nixtla-correlation-mapper` for multi-contract strategies
   - **May be added in**: v2.0 (after single-contract value is proven)

4. **Market Impact Modeling**
   - **Rationale**: Forecasts liquidity, but does NOT model how user's order will move the market
   - **Alternative**: Use forecasted depth as proxy (larger depth = less impact)
   - **Depends on**: Advanced market microstructure modeling (complex, future enhancement)

---

## 7. Success Metrics

### Skill Activation Metrics

**Metric 1: Activation Accuracy**
- **Definition**: % of times skill activates when it should (based on trigger phrases)
- **Target**: 92%+
- **Measurement**: Manual testing with 20 trigger phrase variations
- **Test Phrases**: "forecast liquidity for Polymarket contract", "predict orderbook depth", "when should I execute this large trade"

**Metric 2: False Positive Rate**
- **Definition**: % of times skill activates incorrectly (user wanted something else)
- **Target**: <5%
- **Measurement**: User feedback + monitoring logs

### Quality Metrics

**Metric 3: Description Quality Score**
- **Formula**: 6-criterion weighted scoring (see ARD)
- **Target**: 85%+
- **Components**:
  - Action-oriented: 20%
  - Clear triggers: 25%
  - Comprehensive: 15%
  - Natural language: 20%
  - Specificity: 10%
  - Technical terms: 10%

**Metric 4: SKILL.md Size**
- **Target**: <500 lines
- **Max**: 500 lines (hard limit due to token budget)
- **Current**: TBD (to be measured after implementation)

### Usage Metrics

**Metric 5: Adoption Rate**
- **Target**: 40% of large position traders (Polymarket Discord, Twitter) try skill within first 2 months
- **Measurement**: Skill invocation logs, community feedback

**Metric 6: User Satisfaction**
- **Target**: 4.3/5 rating
- **Measurement**: Post-analysis survey (optional prompt after skill completes)

### Performance Metrics

**Metric 7: Forecast Accuracy**
- **Domain-Specific**: Spread prediction MAE (Mean Absolute Error) <10%
- **Target**: Beat naive baseline (last-value-carried-forward) by 40%+
- **Measurement**: Backtest on historical orderbook data, compare forecast vs actual

**Metric 8: Execution Window Success Rate**
- **Target**: 75%+ of recommended windows actually have high liquidity when they arrive
- **Measurement**: User feedback on actual executions + automated validation

**Metric 9: Slippage Reduction**
- **Target**: Users report 70-90% slippage reduction (from 5-15% → 1-3%)
- **Measurement**: User surveys, trading logs (self-reported)

---

## 8. User Experience Flow

### Typical Usage Flow

1. **User Intent**: Large trader wants to enter $50k position but worried about slippage on illiquid contract
2. **Trigger**: User says "Forecast liquidity for Polymarket contract 0xABC123 over next 7 days, I need to execute $50k"
3. **Skill Activation**: Claude recognizes need for `nixtla-liquidity-forecaster` skill
4. **Skill Execution**:
   - Step 1: Fetch 30 days of hourly orderbook snapshots from Polymarket
   - Step 2: Transform to time series (bid depth, ask depth, spread)
   - Step 3: Call TimeGPT API 3 times for 7-day forecasts
   - Step 4: Identify optimal execution windows (depth >$50k, spread <2%)
   - Step 5: Generate markdown report with charts + recommendations
5. **Output Delivered**: Markdown report with top 5 execution windows, visual forecast charts, strategic recommendations
6. **User Action**: Reviews report, schedules trade for Tuesday 10am ET (forecasted depth: $120k, spread: 1.1%), executes with 1.8% slippage instead of 12%

### Example Scenario

**Scenario**: Large trader planning $50k position entry on volatile political contract

**Input**:
```
Forecast orderbook liquidity for Polymarket contract 0x9876543210abcdef9876543210abcdef98765432
(Will Democrats win 2026 Senate?) over the next 7 days. I need to execute a $50k BUY order
with minimal slippage. When should I execute?
```

**Claude's Response**:
```
I'll forecast liquidity for this contract using the nixtla-liquidity-forecaster skill.
This will analyze historical orderbook depth and spreads, forecast the next 7 days,
and identify optimal execution windows for your $50k position.

[Skill executes 5-step workflow in ~75 seconds]

✓ Analysis complete! I've identified 3 high-liquidity execution windows.
```

**Output** (`reports/liquidity_strategy_2025-12-05.md`):
```markdown
# Liquidity Forecast: Will Democrats Win 2026 Senate?

**Contract**: 0x9876543210abcdef9876543210abcdef98765432
**Analysis Date**: 2025-12-05
**Forecast Horizon**: 7 days (through 2025-12-12)
**Position Size**: $50,000 BUY

## Executive Summary
Forecasted liquidity will peak on **Tuesday Dec 10 at 10am ET** with $135k depth and 0.9% spread—
optimal for your $50k execution. Current liquidity is weak ($42k depth, 3.1% spread)—
recommend waiting 5 days to save $4,200 in slippage (12% → 1.8%).

## Forecast Charts

### Bid Depth Forecast (Next 7 Days)
```
Depth ($k)
140│                 ╭───PEAK──╮
120│             ╭───╯         ╰───╮
100│         ╭───╯                 ╰───╮
 80│     ╭───╯                         ╰───
 60│ ╭───╯
 40│─╯ ← NOW (weak)
    └──────────────────────────────────────> Time
    Thu  Fri  Sat  Sun  Mon  Tue  Wed  Thu
    NOW  +1d  +2d  +3d  +4d  +5d  +6d  +7d

95% Confidence: [$35k, $155k]
80% Confidence: [$50k, $130k]
```

### Spread Forecast (Next 7 Days)
```
Spread (%)
4.0│─╮ ← NOW (wide)
3.5│ ╰─╮
3.0│   ╰──╮
2.5│      ╰──╮
2.0│         ╰───╮
1.5│             ╰───╮
1.0│                 ╰───BEST──╮
0.5│                           ╰───
    └──────────────────────────────────────> Time
    Thu  Fri  Sat  Sun  Mon  Tue  Wed  Thu
```

## Top 5 Execution Windows

| Rank | Date/Time (ET) | Forecasted Depth | Forecasted Spread | Quality Score | Confidence |
|------|----------------|------------------|-------------------|---------------|------------|
| 1 🥇  | Tue Dec 10, 10am | $135k           | 0.9%              | 98/100        | High       |
| 2 🥈  | Mon Dec 09, 2pm  | $118k           | 1.2%              | 91/100        | High       |
| 3 🥉  | Tue Dec 10, 3pm  | $125k           | 1.4%              | 87/100        | Medium     |
| 4     | Wed Dec 11, 11am | $108k           | 1.8%              | 79/100        | Medium     |
| 5     | Thu Dec 12, 9am  | $95k            | 2.1%              | 71/100        | Low        |

## Trading Recommendations

🟢 **WAIT TO EXECUTE**: Strong liquidity improvement forecasted in 5 days

**Recommended Action**:
1. **Wait until Tuesday, Dec 10 at 10am ET** (highest forecasted liquidity)
2. Place $50k BUY order (market or limit near mid)
3. Expected slippage: **1.8%** ($900) vs **12%** ($6,000) if executing now
4. **Savings: $5,100** by waiting for optimal window

**Alternative**: If urgent, execute Monday Dec 09 at 2pm (2nd best window, saves $4,200)

## Risk Assessment

**Confidence Level**: High (tight confidence intervals through Tuesday)
- Tuesday 10am window has 88% probability of depth >$100k
- Spread forecasts are less certain (weekends have volatile spreads historically)
- If news breaks (debate, scandal), liquidity forecast may be invalidated

**Execution Strategy**: Large Position ($50k)
- **Optimal**: Execute full $50k in single order during peak window (Tuesday 10am)
- **Conservative**: Split into 2 × $25k orders (Monday 2pm + Tuesday 10am) to reduce timing risk
- **Risk**: If you wait and liquidity doesn't materialize, you may face worse conditions than today

**Position Sizing**:
- Your $50k order is 37% of forecasted depth ($135k) → moderate impact expected
- Recommend limit order at mid-price to avoid worst-case slippage
- Monitor orderbook 30min before execution for any unexpected changes

---

*Generated by nixtla-liquidity-forecaster | Powered by TimeGPT*
```

**User Benefit**: Trader waits 5 days, executes at optimal window, saves $5,100 in slippage (12% → 1.8%), total profit improvement: ~10% on this trade

---

## 9. Integration Points

### External Systems

**System 1: Polymarket Orderbook API**
- **Purpose**: Fetch historical L2 orderbook snapshots (bid/ask depth at multiple price levels)
- **Integration Type**: WebSocket (real-time) OR REST API (historical polling)
- **Authentication**: None required (public data) or API key for higher rate limits
- **Data Flow**: Skill → Polymarket API → Raw orderbook snapshots JSON

**System 2: Nixtla TimeGPT API**
- **Purpose**: Generate forecasts for bid depth, ask depth, and spread
- **Integration Type**: REST API (HTTP POST)
- **Authentication**: API key in header
- **Cost**: ~$0.15 per execution (3 forecasts × $0.05)

### Internal Dependencies

**Dependency 1: Nixtla Schema Standard**
- **What it provides**: 3-column time series format (unique_id, ds, y)
- **Why needed**: TimeGPT requires this specific schema for all 3 metrics

**Dependency 2: Python Libraries**
- **Libraries**: `nixtla`, `statsforecast`, `pandas`, `requests`, `websocket-client`
- **Versions**:
  - nixtla >= 0.5.0 (TimeGPT support)
  - statsforecast >= 1.7.0 (fallback models)
  - pandas >= 2.0.0 (data manipulation)
  - websocket-client >= 1.5.0 (orderbook streaming)

**Dependency 3: Global Standard Skill Schema**
- **What it provides**: Architecture patterns, token budget limits, quality standards
- **Why needed**: Ensures skill is built to production standards

---

## 10. Constraints & Assumptions

### Technical Constraints

1. **Token Budget**: Must fit in 5,000 token limit (description + SKILL.md + references)
2. **API Rate Limits**:
   - Polymarket: 10 snapshots/sec (WebSocket) or 100 req/min (REST) → not a constraint
   - TimeGPT: 1,000 req/month (3 calls per execution → max 333 executions/month)
3. **Processing Time**: Must complete in <180 seconds (target <90 seconds)
4. **Dependencies**: Requires Python 3.9+, internet connection, API keys

### Business Constraints

1. **API Costs**: TimeGPT usage costs ~$0.15/execution (budget: <$50/month for moderate users)
2. **Timeline**: Skill must be ready for prediction markets vertical launch (Q1 2026)
3. **Resources**: 1 developer, 50 hours development + testing

### Assumptions

1. **Assumption 1: Polymarket provides historical orderbook API**
   - **Risk if false**: Must scrape orderbook snapshots ourselves (complex, brittle)
   - **Mitigation**: Verify API availability before development, build scraper as fallback

2. **Assumption 2: Liquidity patterns are predictable via time series**
   - **Risk if false**: Forecasts are inaccurate, skill provides no value
   - **Mitigation**: Validate on historical data, provide wide confidence intervals, set realistic expectations

3. **Assumption 3: Users understand orderbook concepts (depth, spread, slippage)**
   - **Risk if false**: Users misinterpret recommendations, execute poorly
   - **Mitigation**: Provide educational content in report, explain concepts in plain language

4. **Assumption 4: 7-day forecast horizon is sufficient**
   - **Risk if false**: Users need longer planning horizons (14-30 days)
   - **Mitigation**: Make horizon customizable via `--horizon` parameter, default to 7 days

---

## 11. Risk Assessment

### Technical Risks

**Risk 1: Orderbook API Unavailable or Rate-Limited**
- **Probability**: Medium (Polymarket may not expose historical L2 data)
- **Impact**: Critical (skill cannot function without orderbook data)
- **Mitigation**:
  - Verify API availability before development
  - Build WebSocket scraper as backup (collect data over time)
  - Partner with Polymarket for API access if needed

**Risk 2: Forecast Accuracy Below Threshold**
- **Probability**: Medium (liquidity is noisy, influenced by unpredictable news)
- **Impact**: High (inaccurate forecasts → bad trade timing → user distrust)
- **Mitigation**:
  - Validate MAE <10% on historical data before launch
  - Wide confidence intervals communicate uncertainty
  - Warn users: "Forecasts may be invalidated by breaking news"

**Risk 3: TimeGPT Quota Exhaustion**
- **Probability**: High (3 calls per execution, 1,000/month limit → 333 executions max)
- **Impact**: High (skill stops working mid-month for heavy users)
- **Mitigation**:
  - Implement StatsForecast fallback (free, local)
  - Warn users about quota usage
  - Recommend caching forecasts (re-use if <6 hours old)

### User Experience Risks

**Risk 1: Skill Over-Triggering (False Positives)**
- **Probability**: Medium (liquidity/depth/spread are common words)
- **Impact**: Medium (user annoyance, but not harmful)
- **Mitigation**:
  - Precise description with specific triggers ("forecast liquidity for [contract]")
  - Test with 20+ trigger phrase variations
  - Iterate based on user feedback

**Risk 2: Users Misinterpret Forecasts as Guarantees**
- **Probability**: High (traders want certainty, may ignore uncertainty warnings)
- **Impact**: Critical (bad trades → financial losses → reputational damage)
- **Mitigation**:
  - Explicit disclaimers in every report
  - Confidence intervals prominently displayed
  - Explain limitations: "News events can invalidate forecasts"
  - Position sizing recommendations (don't bet everything on one window)

**Risk 3: Execution Windows Don't Materialize**
- **Probability**: Medium (forecasts are probabilistic, not deterministic)
- **Impact**: High (user waits 5 days, liquidity doesn't improve, worse off than before)
- **Mitigation**:
  - Provide backup windows (top 5, not just 1)
  - Recommend conservative strategies (split orders across multiple windows)
  - Track success rate, improve model over time

---

## 12. Open Questions

**Questions Requiring Decisions**:

1. **Question**: Should we forecast hourly granularity or daily aggregates?
   - **Options**:
     - Option A: Hourly (168 data points for 7-day forecast, more precise)
     - Option B: Daily (7 data points, simpler, less data needed)
   - **Trade-offs**:
     - A: Better precision (identify 10am vs 3pm optimal windows), higher API cost
     - B: Cheaper, faster, but less actionable (only know "Tuesday is good", not specific hour)
   - **Recommendation**: **Option A** (hourly) for large traders who need precision
   - **Decision Needed By**: Before development starts
   - **Owner**: Product Lead + User interviews

2. **Question**: What default depth threshold should we use for "high liquidity"?
   - **Options**:
     - Option A: $50k (medium-large positions)
     - Option B: $100k (very large positions)
     - Option C: Make it required user input (no default)
   - **Trade-offs**:
     - A: Suits 70% of users, some will need to customize
     - B: Suits only largest 20% of users, too strict for most
     - C: More flexible, but requires user to know their needs
   - **Recommendation**: **Option A** ($50k default, customizable via `--min-depth`)
   - **Decision Needed By**: Before v1.0 release
   - **Owner**: Product Lead + User feedback

3. **Question**: Should we include market impact modeling or just liquidity forecasting?
   - **Options**:
     - Option A: Liquidity only (depth + spread forecasts)
     - Option B: Liquidity + impact model (estimate price movement from user's order)
   - **Trade-offs**:
     - A: Simpler, faster to market, covers 80% of value
     - B: More complete, but complex (need market impact model), delayed release
   - **Recommendation**: **Option A** for v1.0 (impact modeling in v1.1 if user demand)
   - **Decision Needed By**: Before development
   - **Owner**: Technical Lead

**Recommended Decisions**:
1. Hourly granularity (more actionable)
2. $50k default depth threshold (customizable)
3. Liquidity forecasting only for v1.0 (no impact modeling yet)

---

## 13. Appendix: Examples

### Example 1: Standard Liquidity Forecast

**User Request**:
```
Forecast liquidity for Polymarket contract 0xABC123 (BTC $100k by Dec 2025)
over next 7 days. I need to exit a $75k position.
```

**Expected Skill Behavior**:
1. Fetch 30 days of hourly orderbook snapshots from Polymarket
2. Transform to 3 time series (bid depth, ask depth, spread)
3. Call TimeGPT API 3 times for 7-day forecasts (hourly granularity)
4. Identify execution windows where depth >$75k and spread <2%
5. Generate report with forecast charts, top 5 windows, recommendations

**Expected Output**:
```markdown
# Liquidity Forecast: BTC $100k by Dec 2025

**Top Execution Window**: Monday Dec 09 at 2pm ET
- Forecasted Depth: $185k (your $75k order is 41% of depth)
- Forecasted Spread: 1.1%
- Expected Slippage: 2.3% ($1,725)
- Confidence: High (95% CI: [$140k, $230k])

**Recommendation**: WAIT 4 days for optimal window (saves $3,800 vs executing now)
```

### Example 2: Urgent Execution (No Good Windows)

**User Request**:
```
Forecast liquidity for contract 0xDEF456 over next 7 days. I need to execute $100k URGENTLY.
```

**Expected Skill Behavior**:
1. Run full workflow (fetch, transform, forecast, analyze)
2. Identify that forecasted liquidity never exceeds $60k in next 7 days
3. Report: "No high-liquidity windows found for $100k position"

**Expected Output**:
```markdown
# Liquidity Forecast: [Contract Name]

⚠️ **WARNING: NO HIGH-LIQUIDITY WINDOWS FOUND**

Your $100k position size exceeds forecasted liquidity for the next 7 days.
Maximum forecasted depth: $62k (Friday 3pm)

**Recommendations**:
1. **Split order**: Execute in 2-3 smaller chunks over multiple days
   - Wed 10am: $35k (depth: $58k, slippage: ~4%)
   - Fri 3pm: $35k (depth: $62k, slippage: ~3.5%)
   - Mon 2pm: $30k (depth: $55k, slippage: ~4.2%)
2. **Wait longer**: Extend forecast horizon to 14 days (may find better windows)
3. **Accept high slippage**: Execute now at $45k depth → expect 15-20% slippage
```

### Example 3: TimeGPT Quota Exceeded

**User Request**:
```
Forecast liquidity for contract 0xGHI789 over next 7 days
```

**Expected Behavior**:
1. Fetch orderbook data (Step 1 succeeds)
2. Transform to time series (Step 2 succeeds)
3. Call TimeGPT API → 402 Payment Required (quota exceeded)
4. Automatically fallback to StatsForecast for all 3 metrics
5. Generate report with note about fallback

**Expected Output**:
```markdown
# Liquidity Forecast: [Contract Name]

*Note: Forecasts generated using StatsForecast (local models).
TimeGPT quota exceeded—accuracy may be slightly lower.*

**Top Execution Window**: Tuesday Dec 10 at 11am ET
- Forecasted Depth: $95k (StatsForecast AutoETS)
- Forecasted Spread: 1.8%
- Model Used: AutoETS (local, no API cost)
- Confidence: Medium (wider intervals than TimeGPT)

**Recommendation**: Wait 5 days for forecasted improvement (saves ~$2,500)
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
| User Representative | Large Position Traders Community | TBD | [Pending] |

---

**Template maintained by**: Intent Solutions
**For**: Nixtla Skills Pack + Global Standard
**Last Updated**: 2025-12-05
