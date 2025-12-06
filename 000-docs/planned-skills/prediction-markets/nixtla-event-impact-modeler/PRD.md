# Claude Skill PRD: Nixtla Event Impact Modeler

**Template Version**: 1.0.0
**Based On**: [Anthropic Skills Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)
**Purpose**: Product Requirements Document for Claude Skills
**Status**: Planned

---

## Document Control

| Field | Value |
|-------|-------|
| **Skill Name** | nixtla-event-impact-modeler |
| **Skill Type** | [X] Mode Skill [ ] Utility Skill |
| **Domain** | Time Series Forecasting + Event Analysis |
| **Target Users** | Traders, Risk Analysts, Data Scientists, Economists |
| **Priority** | [X] Critical [ ] High [ ] Medium [ ] Low |
| **Status** | [X] Planned [ ] In Development [ ] Complete |
| **Owner** | Intent Solutions |
| **Last Updated** | 2025-12-05 |

---

## 1. Executive Summary

**One-sentence description**: Transform Claude into an event impact analyst that models how external events (Fed meetings, earnings reports, elections, economic data releases) impact prediction market contract prices using TimeGPT's exogenous variables feature to quantify event-driven price changes.

**Value Proposition**: Answers the critical question "What if X happens?" by comparing baseline forecasts vs event-adjusted forecasts, quantifying event impact (e.g., "+15% odds if Fed cuts rates")—a capability unique to TimeGPT's exogenous variables feature not available in traditional forecasting tools.

**Key Metrics**:
- Target activation accuracy: 95%
- Expected usage frequency: 3-5 times per day (active traders/analysts)
- Description quality target: 90%+
- Event impact accuracy target: MAPE <20% on historical event impacts
- Scenario analysis completeness: 95% (all major events captured)

---

## 2. Problem Statement

### Current State (Without This Skill)

**Pain Points**:
1. **No quantification of event impact**: Traders know "Fed meeting matters" but can't quantify how much (gut feeling vs data-driven)
2. **Manual scenario analysis is time-consuming**: Building "what-if" models requires data science expertise (2-4 hours per scenario)
3. **Missed event dependencies**: Events interact (Fed cuts + strong jobs report = different impact than Fed cuts alone)
4. **No standardized event calendars**: Traders manually track Fed schedules, earnings dates, political events across multiple sources
5. **Baseline vs event-adjusted comparison is manual**: No tools to visualize "forecast with event" vs "forecast without event"

**Current Workarounds**:
- Monitor economic calendars manually → Guess impact magnitude based on "market feel" (highly subjective)
- Build custom Python scripts with regression models (requires PhD-level time series knowledge)
- Use simple rule-based adjustments: "Fed cut = +10% to crypto odds" (oversimplified, often wrong)

**Impact of Problem**:
- Time wasted: 2-4 hours per event analysis
- Error rate: 40-60% (subjective estimates, no validation)
- User frustration level: Very High (complex, requires expert knowledge, unreliable)
- Missed opportunities: Can't pre-position before major events (too slow to analyze)

### Desired State (With This Skill)

**Transformation**:
- From: Manual 2-4 hour scenario analysis with 40-60% error rate
- To: Automated 90-second event impact modeling with <20% error rate and standardized methodology

**Expected Benefits**:
1. **20x faster analysis**: 2-4 hours → 90 seconds (98% time reduction)
2. **Higher accuracy**: 40-60% error rate → <20% error rate (67% improvement)
3. **Event calendar integration**: Automatic fetching of Fed schedules, earnings calendars, political events
4. **Scenario comparison**: Visual side-by-side: baseline vs event-adjusted forecasts
5. **Multi-event modeling**: Capture interactions between events (Fed + jobs + CPI = combined impact)

---

## 3. Target Users

### Primary Users

**User Persona 1: Prediction Market Trader**
- **Background**: 3-7 years trading experience, understands macro events impact markets, limited data science skills
- **Goals**: Pre-position ahead of major events (Fed meetings, elections, earnings) with quantified impact estimates
- **Pain Points**: Can't quantify event magnitude, missed opportunities due to slow manual analysis, wrong positions due to gut-feel estimates
- **Use Frequency**: Daily during event-heavy periods (FOMC weeks, earnings season, election cycles)
- **Technical Skills**: Deep market knowledge, basic spreadsheet skills, no coding background
- **Annual Income Impact**: $100k-$500k potential (better event-driven positioning)

**User Persona 2: Risk Analyst (Financial Institution)**
- **Background**: Quantitative finance background, tasked with stress-testing portfolios under event scenarios
- **Goals**: Model portfolio sensitivity to major events (Fed policy changes, geopolitical risks, economic shocks)
- **Pain Points**: Building event scenario models is time-consuming, requires custom code for each event type
- **Use Frequency**: Weekly (stress testing, risk reporting)
- **Technical Skills**: Expert in finance, proficient in R/Python, limited time for custom tool-building
- **Value**: Faster risk reports, more comprehensive scenario coverage, regulatory compliance

### Secondary Users

**Economists**: Research how events propagate through markets
**Policy Analysts**: Track market-implied policy expectations (e.g., Fed rate cut probabilities)
**Journalists**: Quantify event impact for news stories ("Fed cut would boost BTC odds 15%")

---

## 4. User Stories

**Format**: "As a [user type], I want [capability], so that [benefit]"

### Critical User Stories (Must Have)

1. **As a** prediction market trader,
   **I want** to model the impact of an upcoming Fed rate cut on a BTC prediction market contract,
   **So that** I can pre-position before the FOMC meeting and profit from the event-driven price move.

   **Acceptance Criteria**:
   - [ ] Accepts event definition: type (Fed meeting), date, parameters (cut 25bps, hold, raise)
   - [ ] Generates baseline forecast (no event) + event-adjusted forecast (with event)
   - [ ] Quantifies impact: "+15% odds if cut, -5% odds if hold, -20% odds if raise"
   - [ ] Visual chart shows baseline vs 3 event scenarios side-by-side
   - [ ] Workflow completes in <90 seconds

2. **As a** trader,
   **I want** to automatically fetch upcoming event calendars (Fed, earnings, elections) for the next 30 days,
   **So that** I can identify high-impact events ahead of time without manual calendar tracking.

   **Acceptance Criteria**:
   - [ ] Fetches Fed meeting schedule (FOMC dates, minutes releases)
   - [ ] Fetches earnings calendars for major companies (TSLA, AAPL, NVDA, etc.)
   - [ ] Fetches political event calendars (election dates, debates, key votes)
   - [ ] Fetches economic data release calendars (CPI, jobs, GDP)
   - [ ] Outputs structured JSON: event type, date, expected impact magnitude

3. **As a** data scientist,
   **I want** the skill to format exogenous variables for TimeGPT automatically,
   **So that** I can focus on analysis instead of learning TimeGPT's exogenous variable schema.

   **Acceptance Criteria**:
   - [ ] Converts event calendar → TimeGPT-compatible exogenous variable format
   - [ ] Validates exogenous variable alignment with forecast dates
   - [ ] Handles multiple events (creates multi-column exogenous dataframe)
   - [ ] Outputs standard format: ds (date), event_1 (binary), event_2 (continuous), etc.
   - [ ] Logs validation warnings (event dates outside forecast horizon)

### High-Priority User Stories (Should Have)

4. **As a** trader,
   **I want** to compare multiple event scenarios simultaneously (Fed cut vs hold vs raise),
   **So that** I can see the full range of possible outcomes and position accordingly.

   **Acceptance Criteria**:
   - [ ] Accepts multi-scenario input: List[Event] with different outcomes
   - [ ] Generates separate forecast for each scenario
   - [ ] Creates comparison table: Scenario | Final Price | % Change | Confidence
   - [ ] Ranks scenarios by probability-weighted expected value

5. **As a** risk analyst,
   **I want** to model multi-event interactions (Fed cut + strong jobs report),
   **So that** I can capture compound effects not visible in single-event analysis.

   **Acceptance Criteria**:
   - [ ] Accepts compound events: Event A AND Event B
   - [ ] Models interaction effects using TimeGPT exogenous variables
   - [ ] Compares: Event A alone, Event B alone, A+B together
   - [ ] Quantifies interaction: "A+B = X%, which is Y% more than A+B separately"

### Nice-to-Have User Stories (Could Have)

6. **As a** power user,
   **I want** to import custom event calendars from CSV/JSON,
   **So that** I can model proprietary events (internal product launches, conference dates).

7. **As a** researcher,
   **I want** to backtest event impact accuracy on historical events,
   **So that** I can validate model performance before trusting live predictions.

---

## 5. Functional Requirements

### Core Capabilities (Must Have)

**REQ-1: Event Calendar Integration**
- **Description**: Fetch upcoming events from multiple sources (Fed, economic data, earnings, political)
- **Rationale**: Foundation of workflow—need accurate event dates and metadata
- **Acceptance Criteria**:
  - [ ] Fetches Fed FOMC schedule (meetings, minutes, press conferences)
  - [ ] Fetches economic calendar (CPI, jobs, GDP, retail sales, etc.) via API
  - [ ] Fetches earnings calendars for S&P 500 companies
  - [ ] Fetches political event calendar (elections, debates, key votes)
  - [ ] Saves to `data/event_calendar.json` (structured format)
  - [ ] Updates calendar daily (caching with 24-hour TTL)
- **Dependencies**: Economic calendar API (free tier available: tradingeconomics.com, fxstreet.com)

**REQ-2: Event-to-Exogenous Variable Transformation**
- **Description**: Convert event calendar to TimeGPT-compatible exogenous variables dataframe
- **Rationale**: TimeGPT requires specific schema for exogenous variables (aligned dates, numeric encoding)
- **Acceptance Criteria**:
  - [ ] Creates binary variables for discrete events (Fed meeting yes/no = 1/0)
  - [ ] Creates continuous variables for magnitude events (Fed cut magnitude = -0.25, -0.50, etc.)
  - [ ] Aligns event dates with forecast horizon (ds column matches)
  - [ ] Validates: no missing dates, all events within forecast range
  - [ ] Saves to `data/exogenous_vars.csv` (TimeGPT format)
- **Dependencies**: REQ-1 (event calendar data)

**REQ-3: Baseline Forecast (No Events)**
- **Description**: Generate baseline forecast assuming no major events (business-as-usual scenario)
- **Rationale**: Need baseline to compare against event-adjusted forecasts (delta = event impact)
- **Acceptance Criteria**:
  - [ ] Calls TimeGPT API with historical time series only (no exogenous variables)
  - [ ] Generates 14-day forecast with confidence intervals
  - [ ] Validates forecast quality (MAPE, coverage)
  - [ ] Saves to `data/forecast_baseline.csv`
- **Dependencies**: Historical time series data (user-provided or from prior skill)

**REQ-4: Event-Adjusted Forecast (With Events)**
- **Description**: Generate forecast incorporating event impact using TimeGPT exogenous variables
- **Rationale**: Core value proposition—shows how events change the forecast
- **Acceptance Criteria**:
  - [ ] Calls TimeGPT API with time series + exogenous variables
  - [ ] Generates 14-day forecast adjusted for events
  - [ ] Compares to baseline: calculates delta for each date
  - [ ] Handles multi-scenario analysis (multiple forecasts with different event outcomes)
  - [ ] Saves to `data/forecast_with_events.csv`
- **Dependencies**: REQ-2 (exogenous variables), REQ-3 (baseline forecast)

**REQ-5: Event Impact Quantification Report**
- **Description**: Generate markdown report comparing baseline vs event-adjusted forecasts with impact metrics
- **Rationale**: Final deliverable that analysts use to make decisions
- **Acceptance Criteria**:
  - [ ] Loads baseline + event-adjusted forecasts
  - [ ] Calculates impact metrics: absolute change, % change, confidence intervals
  - [ ] Generates side-by-side ASCII charts (baseline vs event scenarios)
  - [ ] Creates event impact table: Event | Date | Impact | Confidence
  - [ ] Provides actionable recommendations: "Position for X if event Y happens"
  - [ ] Saves to `reports/event_impact_YYYY-MM-DD.md`
- **Dependencies**: REQ-3 (baseline), REQ-4 (event-adjusted)

### Integration Requirements

**REQ-API-1: Economic Calendar API**
- **Purpose**: Fetch upcoming Fed meetings, economic data releases, political events
- **Endpoints**:
  - TradingEconomics API: `https://api.tradingeconomics.com/calendar`
  - FXStreet API: `https://www.fxstreet.com/economic-calendar` (scraping fallback)
- **Authentication**: API key (free tier: 500 requests/month)
- **Rate Limits**: 100 requests/day (sufficient for daily updates)
- **Error Handling**: Retry 3x on 5xx errors, graceful degradation (use cached calendar if API fails)

**REQ-API-2: Nixtla TimeGPT API** (with exogenous variables)
- **Purpose**: Generate forecasts with event impact modeling
- **Endpoints**: `https://api.nixtla.io/timegpt/forecast`
- **Authentication**: API key (header: `X-API-Key`)
- **Key Feature**: Exogenous variables support (not available in StatsForecast—TimeGPT only)
- **Rate Limits**: 1,000 requests/month
- **Cost**: ~$0.08 per forecast with exogenous variables (higher than baseline-only forecasts)
- **Error Handling**: 402 Payment Required → Warn user (no fallback—exogenous vars require TimeGPT)

**REQ-API-3: Earnings Calendar API** (Optional)
- **Purpose**: Fetch upcoming earnings dates for specific companies
- **Endpoints**: Polygon.io API, Alpha Vantage API
- **Authentication**: API key (optional feature)
- **Rate Limits**: 60 requests/minute
- **Error Handling**: Graceful degradation—if API fails, skip earnings events (focus on macro events)

### Data Requirements

**REQ-DATA-1: Input Data Format**
- **Format**: Time series CSV + Event specification JSON
- **Required Fields**:
  - Time series: unique_id, ds, y (standard Nixtla format)
  - Event spec: event_type, event_date, event_magnitude, event_probability
- **Optional Fields**: Multiple events (array), custom event names
- **Validation Rules**: Event dates within forecast horizon, event magnitudes normalized 0-1

**REQ-DATA-2: Output Data Format**
- **Format**: Markdown report + CSV forecasts (baseline + event scenarios)
- **Fields**:
  - Report: Executive summary, event calendar, baseline chart, event-adjusted charts, impact table, recommendations
  - CSV: ds, TimeGPT_baseline, TimeGPT_event_1, TimeGPT_event_2, delta_event_1, delta_event_2
- **Quality Standards**: Event impact MAPE <20%, confidence intervals cover 90%+ of realized outcomes

### Performance Requirements

**REQ-PERF-1: Response Time**
- **Target**: <90 seconds for standard single-event analysis
- **Max Acceptable**: <180 seconds
- **Breakdown**:
  - Step 1 (Event Calendar Fetch): <10 seconds
  - Step 2 (Transform to Exogenous Vars): <5 seconds
  - Step 3 (Baseline Forecast): <30 seconds
  - Step 4 (Event-Adjusted Forecast): <35 seconds (heavier computation with exogenous vars)
  - Step 5 (Impact Report): <10 seconds

**REQ-PERF-2: Token Budget**
- **Description Size**: 250 characters (fits in 15k token budget) ✓
- **SKILL.md Size**: <500 lines (~2,500 tokens)
- **Total Skill Size**: <5,000 tokens including all references

### Quality Requirements

**REQ-QUAL-1: Description Quality**
- **Target Score**: 90%+ on quality formula (exceeds 80% minimum)
- **Must Include**:
  - [X] Action-oriented verbs: "Models", "Quantifies", "Compares", "Integrates", "Forecasts"
  - [X] "Use when [scenarios]" clause: "modeling event impact, scenario analysis, what-if forecasting"
  - [X] "Trigger with '[phrases]'" examples: "model event impact", "what if Fed cuts rates", "scenario analysis"
  - [X] Domain keywords: "TimeGPT", "exogenous variables", "event impact", "scenario analysis"

**REQ-QUAL-2: Accuracy**
- **Event Impact Accuracy**: MAPE <20% on historical event impacts (backtested)
- **Scenario Coverage**: 95%+ of major events captured in default calendar
- **Error Rate**: <5% (workflow failures due to bugs)
- **Event Detection**: 99%+ accuracy (no missed events in calendar fetch)

---

## 6. Non-Goals (Out of Scope)

**What This Skill Does NOT Do**:

1. **Real-Time Event Detection**
   - **Rationale**: Skill works with scheduled events (Fed meetings, earnings), not breaking news
   - **Alternative**: User manually adds breaking news events via custom JSON
   - **May be added in**: v2.0 (sentiment analysis + news API integration)

2. **Automated Event Trading**
   - **Rationale**: Provides analysis only, does NOT execute trades
   - **Alternative**: User manually trades based on recommendations
   - **Depends on**: Regulatory/safety concerns

3. **Multi-Asset Portfolio Event Impact**
   - **Rationale**: Single-contract focus, not portfolio-level stress testing
   - **Alternative**: Run skill multiple times for different contracts, aggregate manually
   - **May be added in**: v1.5 (portfolio mode)

4. **Historical Event Backtesting**
   - **Rationale**: Forward-looking scenario analysis only
   - **Alternative**: Export forecast data, use external backtesting tools
   - **May be added in**: v1.2 (historical validation mode)

---

## 7. Success Metrics

### Skill Activation Metrics

**Metric 1: Activation Accuracy**
- **Definition**: % of times skill activates when it should (based on trigger phrases)
- **Target**: 95%+
- **Measurement**: Manual testing with 20 trigger phrase variations
- **Test Phrases**: "model event impact", "what if Fed cuts rates", "scenario analysis for election", "quantify event impact on BTC"

**Metric 2: False Positive Rate**
- **Definition**: % of times skill activates incorrectly
- **Target**: <3%
- **Measurement**: User feedback + monitoring logs

### Quality Metrics

**Metric 3: Description Quality Score**
- **Formula**: 6-criterion weighted scoring (see ARD)
- **Target**: 90%+ (exceeds 80% minimum)
- **Components**: Action-oriented (20%), Clear triggers (25%), Comprehensive (15%), Natural language (20%), Specificity (10%), Technical terms (10%)

**Metric 4: Event Impact Accuracy**
- **Domain-Specific**: MAPE (Mean Absolute Percentage Error) <20% on historical events
- **Target**: Beat naive baseline (no event impact) by 50%+
- **Measurement**: Backtest on historical Fed meetings, elections, earnings surprises

### Usage Metrics

**Metric 5: Adoption Rate**
- **Target**: 50% of active prediction market traders try skill within first month
- **Measurement**: Skill invocation logs, community feedback

**Metric 6: User Satisfaction**
- **Target**: 4.7/5 rating
- **Measurement**: Post-analysis survey (optional prompt after skill completes)

### Performance Metrics

**Metric 7: Scenario Completeness**
- **Target**: 95%+ of major events captured in default calendar
- **Measurement**: Compare skill's event calendar vs Bloomberg/Reuters event calendars

**Metric 8: Multi-Event Modeling Accuracy**
- **Target**: 80%+ accuracy when modeling 2-3 simultaneous events
- **Measurement**: Backtest on historical compound events (e.g., Fed cut + strong jobs report)

---

## 8. User Experience Flow

### Typical Usage Flow

1. **User Intent**: Trader wants to know "What happens to BTC $100k contract odds if Fed cuts rates next week?"
2. **Trigger**: User says "Model the impact of a Fed rate cut on BTC $100k contract"
3. **Skill Activation**: Claude recognizes need for `nixtla-event-impact-modeler` skill
4. **Skill Execution**:
   - Step 1: Fetch Fed meeting calendar, identify next FOMC meeting (Dec 18, 2025)
   - Step 2: Transform event → Exogenous variable (Fed cut = -0.25 on Dec 18)
   - Step 3: Generate baseline forecast (no event)
   - Step 4: Generate event-adjusted forecast (with Fed cut)
   - Step 5: Compare forecasts, quantify impact: "+18% odds if Fed cuts 25bps"
5. **Output Delivered**: Markdown report with baseline chart, event chart, impact table, recommendations
6. **User Action**: Reviews report, decides to BUY BTC contract at 0.52 (forecast: 0.70 post-cut, 35% profit potential)

### Example Scenario

**Scenario**: Trader preparing for upcoming Fed FOMC meeting

**Input**:
```
Model the impact of three Fed scenarios on the Polymarket BTC $100k by Dec 2025 contract:
1. Cut 25bps
2. Hold rates
3. Raise 25bps

Show me which scenario is most likely and how it affects the forecast.
```

**Claude's Response**:
```
I'll model these three Fed rate scenarios using the nixtla-event-impact-modeler skill.
This will generate baseline forecast + three event-adjusted forecasts, then compare
the impact of each scenario.

[Skill executes 5-step workflow in ~90 seconds]

✓ Analysis complete! I've generated a comprehensive event impact report comparing
  all three Fed scenarios.
```

**Output** (`reports/event_impact_fed_2025-12-05.md`):
```markdown
# Event Impact Analysis: Fed Rate Decision on BTC $100k Contract

**Contract**: Will Bitcoin Reach $100k by December 2025?
**Analysis Date**: 2025-12-05
**Event**: Fed FOMC Meeting (December 18, 2025)
**Scenarios Analyzed**: 3 (Cut 25bps, Hold, Raise 25bps)

## Executive Summary
Fed rate decision significantly impacts BTC contract odds. Our model predicts:
- **Cut 25bps**: +18% odds (0.52 → 0.70) - BULLISH
- **Hold rates**: +5% odds (0.52 → 0.57) - NEUTRAL
- **Raise 25bps**: -15% odds (0.52 → 0.37) - BEARISH

Market-implied probability: 60% cut, 30% hold, 10% raise.
**Recommended Position**: BUY ahead of expected cut (60% probability × 18% impact = +10.8% expected value).

## Event Calendar

| Event | Date | Type | Parameters |
|-------|------|------|------------|
| Fed FOMC Meeting | 2025-12-18 | Monetary Policy | Cut 25bps / Hold / Raise 25bps |
| FOMC Press Conference | 2025-12-18 14:30 EST | Announcement | Powell remarks |
| CPI Release | 2025-12-13 | Economic Data | Influences Fed decision |

## Baseline Forecast (No Event Impact)

Assuming business-as-usual (no major events):

```
BTC $100k YES Odds
0.60│
0.58│         ╱─────────
0.56│     ╱───
0.54│ ╱───
0.52│─
0.50│
    └──────────────────────────> Time
    Now  +3d  +7d  +10d  +14d

Baseline: 0.52 → 0.59 (+13.5%) over 14 days
95% CI: [0.45, 0.73]
```

## Event-Adjusted Forecasts

### Scenario 1: Fed Cuts 25bps (60% probability)

```
BTC $100k YES Odds
0.75│                     ╱─────
0.70│                 ╱───
0.65│             ╱───
0.60│         ╱───
0.55│     ╱───
0.52│─────           ← Event (Dec 18)
0.50│
    └──────────────────────────> Time
    Now  +3d  +7d  +10d  +14d

With Cut: 0.52 → 0.70 (+34.6%) over 14 days
Event Impact: +18% (0.70 vs 0.59 baseline)
95% CI: [0.62, 0.78]
```

### Scenario 2: Fed Holds Rates (30% probability)

```
With Hold: 0.52 → 0.57 (+9.6%)
Event Impact: +5% vs baseline
95% CI: [0.50, 0.64]
```

### Scenario 3: Fed Raises 25bps (10% probability)

```
With Raise: 0.52 → 0.37 (-28.8%)
Event Impact: -15% vs baseline
95% CI: [0.30, 0.44]
```

## Event Impact Table

| Scenario | Probability | Current | Forecast (14d) | Absolute Impact | % Impact | Confidence |
|----------|-------------|---------|----------------|-----------------|----------|------------|
| Baseline | - | 0.52 | 0.59 | - | - | High |
| Cut 25bps | 60% | 0.52 | 0.70 | +0.11 | +18% | High |
| Hold | 30% | 0.52 | 0.57 | +0.05 | +5% | Medium |
| Raise 25bps | 10% | 0.52 | 0.37 | -0.11 | -15% | Medium |

**Expected Value Calculation**:
- (60% × +18%) + (30% × +5%) + (10% × -15%) = **+10.8% expected impact**

## Trading Recommendations

🟢 **BUY SIGNAL**: Strong positive expected value ahead of Fed decision

**Recommended Action**:
1. **BUY** BTC YES at current price 0.52
2. **Target** SELL at 0.70 (post-cut scenario)
3. **Stop Loss** at 0.48 (if Fed surprises with raise)
4. **Expected Profit**: 10.8% (probability-weighted across scenarios)
5. **Optimal Position Size**: 5-8% of portfolio (high-conviction trade)

**Risk Assessment**: Medium-High
- Upside scenario (Cut 25bps): 60% probability, +35% profit
- Downside scenario (Raise 25bps): 10% probability, -29% loss
- Risk/Reward Ratio: 3.5:1 (favorable)
- Key Risk: Fed could surprise with 50bps cut (even more bullish) or hold (neutral)

**Timing**:
- Enter position: Now (before market fully prices in cut)
- Exit position: Within 24 hours post-FOMC (Dec 18 2pm EST)
- Monitor CPI release (Dec 13) for early signal

**Position Monitoring**:
- If CPI comes in hot (>3.5%): Fed less likely to cut → reduce position 50%
- If CPI comes in cool (<3.0%): Fed more likely to cut → increase position 25%

---

*Generated by nixtla-event-impact-modeler | Powered by TimeGPT Exogenous Variables*
*Analysis includes: 3 scenarios, 1 major event, 14-day forecast horizon*
```

**User Benefit**: Trader identifies high-conviction trade with quantified risk/reward in 90 seconds (vs 2-4 hours manual analysis), executes BUY, realizes 35% profit when Fed cuts rates as expected

---

## 9. Integration Points

### External Systems

**System 1: Economic Calendar API**
- **Purpose**: Fetch upcoming Fed meetings, economic data releases, political events
- **Integration Type**: REST API (HTTP GET)
- **Authentication**: API key (free tier available)
- **Data Flow**: Skill → Economic Calendar API → Event JSON

**System 2: Nixtla TimeGPT API** (with Exogenous Variables)
- **Purpose**: Generate baseline + event-adjusted forecasts
- **Integration Type**: REST API (HTTP POST)
- **Authentication**: API key in header
- **Key Feature**: Exogenous variables support (unique to TimeGPT)
- **Cost**: ~$0.08 per forecast with exogenous variables

**System 3: Earnings Calendar API** (Optional)
- **Purpose**: Fetch company earnings dates
- **Integration Type**: REST API
- **Authentication**: API key (optional feature)
- **Data Flow**: Skill → Earnings API → Earnings events JSON

### Internal Dependencies

**Dependency 1: Time Series Data**
- **What it provides**: Historical price/odds data for forecasting
- **Why needed**: TimeGPT requires historical data to generate forecasts
- **Source**: User-provided CSV or output from `nixtla-polymarket-analyst` skill

**Dependency 2: Nixtla Schema Standard**
- **What it provides**: 3-column time series format (unique_id, ds, y)
- **Why needed**: TimeGPT requires this specific schema

**Dependency 3: Global Standard Skill Schema**
- **What it provides**: Architecture patterns, token budget limits, quality standards
- **Why needed**: Ensures skill is built to production standards

---

## 10. Constraints & Assumptions

### Technical Constraints

1. **Token Budget**: Must fit in 5,000 token limit (description + SKILL.md + references)
2. **API Rate Limits**:
   - Economic Calendar API: 100 req/day (sufficient for daily updates)
   - TimeGPT: 1,000 req/month (may limit heavy users—plan accordingly)
3. **Processing Time**: Must complete in <180 seconds (target <90 seconds)
4. **Dependencies**: Requires Python 3.9+, internet connection, TimeGPT API key (NO StatsForecast fallback—exogenous vars require TimeGPT)

### Business Constraints

1. **API Costs**: TimeGPT with exogenous variables costs ~$0.08/forecast (budget: <$80/month for heavy users)
2. **Timeline**: Skill must be ready for prediction markets vertical launch (Q1 2026)
3. **Resources**: 1 developer, 60 hours development + testing (more complex than baseline-only forecasting)

### Assumptions

1. **Assumption 1: Users understand event-driven trading concepts**
   - **Risk if false**: Users may not understand "exogenous variables", "scenario analysis"
   - **Mitigation**: Provide simple examples in documentation, avoid jargon in outputs

2. **Assumption 2: TimeGPT exogenous variables improve forecast accuracy vs baseline**
   - **Risk if false**: Event-adjusted forecasts no better than baseline → skill has no value
   - **Mitigation**: Validate on historical events before launch, provide accuracy metrics in reports

3. **Assumption 3: Economic calendar API provides accurate, timely event data**
   - **Risk if false**: Missed events or wrong dates → bad forecasts
   - **Mitigation**: Use multiple API sources (primary + fallback), validate against official Fed/BLS calendars

4. **Assumption 4: Users willing to pay higher API costs for exogenous variable forecasts**
   - **Risk if false**: Users abandon skill due to cost (2x baseline-only forecasts)
   - **Mitigation**: Clearly communicate value (event impact quantification worth the cost), offer batch discounts

---

## 11. Risk Assessment

### Technical Risks

**Risk 1: TimeGPT Exogenous Variables Quota Exhaustion**
- **Probability**: High (quota-based, 1,000 req/month, no fallback)
- **Impact**: Critical (skill stops working mid-month—NO StatsForecast fallback for exogenous vars)
- **Mitigation**:
  - Track usage aggressively, warn users at 80% quota
  - Provide cost calculator: "X scenarios = Y API calls = $Z cost"
  - Encourage batch analysis to reduce API calls

**Risk 2: Event Calendar API Outages**
- **Probability**: Medium (third-party API dependency)
- **Impact**: High (no events → skill can't run scenario analysis)
- **Mitigation**:
  - Cache last 7 days of event calendar locally
  - Implement fallback: TradingEconomics (primary) → FXStreet (secondary) → Manual user input (tertiary)
  - Log warnings when using cached data

**Risk 3: Exogenous Variable Forecast Accuracy Below Threshold**
- **Probability**: Medium (new feature, limited validation data)
- **Impact**: High (inaccurate event impact → bad trades → user distrust)
- **Mitigation**:
  - Backtest on 50+ historical events before launch
  - Provide confidence intervals for all event scenarios
  - Include disclaimer: "Historical event impact analysis is probabilistic, not guaranteed"

### User Experience Risks

**Risk 1: Users Misinterpret Scenario Probabilities**
- **Probability**: High (users may treat scenarios as certainties)
- **Impact**: Critical (financial losses → reputational damage)
- **Mitigation**:
  - Explicit disclaimers in every report
  - Use probability-weighted expected value (not single-scenario focus)
  - Provide risk assessment with downside scenarios

**Risk 2: Event Calendar Overload (Too Many Events)**
- **Probability**: Medium (default calendar may include 100+ events per month)
- **Impact**: Medium (user overwhelmed, can't focus on high-impact events)
- **Mitigation**:
  - Filter to "high-impact" events by default (Fed, elections, major earnings)
  - Allow user to customize event types: `--events fed,cpi,elections`
  - Rank events by historical impact magnitude

---

## 12. Open Questions

**Questions Requiring Decisions**:

1. **Question**: Should we support continuous event variables (e.g., Fed cut magnitude: -0.25, -0.50) or binary only (cut yes/no)?
   - **Options**:
     - Option A: Binary only (simpler, faster to market)
     - Option B: Binary + continuous (more accurate, higher complexity)
   - **Decision Needed By**: Before development starts
   - **Owner**: Product Lead (Intent Solutions)
   - **Recommendation**: Option B (continuous variables—more accurate event modeling, worth the complexity)

2. **Question**: What default forecast horizon for event impact analysis (7, 14, or 30 days)?
   - **Options**:
     - 7 days: Covers immediate event impact only
     - 14 days: Balanced (recommended)
     - 30 days: Captures long-term event propagation
   - **Decision Needed By**: Before v1.0 release
   - **Owner**: Product Lead + User feedback
   - **Recommendation**: 14 days (most events impact markets within 2 weeks)

3. **Question**: Should event calendar auto-update daily or on-demand only?
   - **Options**:
     - Auto-update: More convenient, uses API quota
     - On-demand: User control, conserves API quota
   - **Decision Needed By**: Before development
   - **Owner**: Technical Lead
   - **Recommendation**: Auto-update with 24-hour cache (balance convenience vs API cost)

---

## 13. Appendix: Examples

### Example 1: Single Event (Fed Rate Cut)

**User Request**:
```
Model the impact of a Fed rate cut on BTC $100k contract
```

**Expected Skill Behavior**:
1. Fetch Fed meeting calendar → Next FOMC meeting Dec 18, 2025
2. Create exogenous variable: Fed cut = 1 on Dec 18, 0 otherwise
3. Generate baseline forecast (no event)
4. Generate event-adjusted forecast (with Fed cut)
5. Compare forecasts, quantify impact: "+18% odds if Fed cuts"

**Expected Output**:
```markdown
# Event Impact: Fed Rate Cut on BTC $100k Contract

**Event**: Fed FOMC Meeting (Dec 18, 2025) - Cut 25bps
**Impact**: +18% odds (0.52 → 0.70)
**Confidence**: High
**Recommendation**: BUY ahead of expected cut
```

### Example 2: Multi-Scenario Analysis (Fed Cut vs Hold vs Raise)

**User Request**:
```
Compare three Fed scenarios: cut 25bps, hold, raise 25bps. Show me expected value.
```

**Expected Skill Behavior**:
1. Create 3 exogenous variables (cut, hold, raise)
2. Generate 4 forecasts: baseline + 3 scenarios
3. Calculate probability-weighted expected value
4. Rank scenarios by impact magnitude

**Expected Output**:
```markdown
| Scenario | Probability | Impact | Expected Value |
|----------|-------------|--------|----------------|
| Cut 25bps | 60% | +18% | +10.8% |
| Hold | 30% | +5% | +1.5% |
| Raise 25bps | 10% | -15% | -1.5% |

**Expected Value**: +10.8% (bullish, BUY signal)
```

### Example 3: Multi-Event Compound Analysis (Fed + Jobs Report)

**User Request**:
```
Model the combined impact of a Fed cut AND a strong jobs report next week
```

**Expected Skill Behavior**:
1. Fetch 2 events: Fed FOMC (Dec 18), Jobs Report (Dec 6)
2. Create 2 exogenous variables (Fed cut, jobs beat expectations)
3. Generate forecasts: baseline, Fed only, Jobs only, Fed+Jobs
4. Quantify interaction effect: "Fed+Jobs = +25%, which is +7% more than sum of individual effects"

**Expected Output**:
```markdown
# Compound Event Analysis: Fed Cut + Strong Jobs Report

**Individual Effects**:
- Fed cut alone: +18%
- Strong jobs alone: +8%
- Expected sum: +26%

**Actual Compound Effect**: +25%
**Interaction**: -1% (slight offset—strong jobs may reduce Fed cut probability)

**Recommendation**: Position for Fed cut scenario (primary driver), monitor jobs data for early signal
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
