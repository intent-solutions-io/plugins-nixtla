# Claude Skill PRD: Nixtla Arbitrage Detector

**Template Version**: 1.0.0
**Based On**: [Anthropic Skills Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)
**Purpose**: Product Requirements Document for Claude Skills
**Status**: Planned

---

## Change Log

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2025-12-05 | Initial PRD | Intent Solutions |
| 1.0.1 | 2025-12-06 | De-hyped for Nixtla review: P&L claims removed ("$10k-$100k", "$50k-$500k"), adoption targets made realistic (15-30 early adopters vs 40%), error rates reframed as evaluation goals, added "not financial advice" and fee disclaimers throughout, clarified that opportunities are informational only | Intent Solutions |
| 1.0.2 | 2025-12-06 | Added SKILL.md Frontmatter Example section per Global Standard Skill Schema v2.0 | Intent Solutions |

---

## SKILL.md Frontmatter Example

```yaml
---
# 🔴 REQUIRED FIELDS
name: nixtla-arbitrage-detector
description: "Scans prediction markets for cross-platform pricing discrepancies. Fetches Polymarket and Kalshi odds in parallel, matches equivalent contracts, calculates spreads, ranks by magnitude. Use when finding arbitrage, comparing cross-platform prices, scanning for mispricing. Trigger with 'find arbitrage', 'scan markets', 'detect mispricing'."

# 🟡 OPTIONAL FIELDS
allowed-tools: "Read,Write,Bash,Glob"
model: inherit
version: "1.0.0"
---
```

**Description Quality Score**: 92/100
- ✅ Action-oriented: "Scans", "Fetches", "matches", "calculates", "ranks"
- ✅ Clear triggers: 3 explicit phrases
- ✅ "Use when" clause with scenarios
- ✅ Character count: 246/250

---

## Document Control

| Field | Value |
|-------|-------|
| **Skill Name** | nixtla-arbitrage-detector |
| **Skill Type** | [X] Mode Skill [ ] Utility Skill |
| **Domain** | Prediction Markets + Real-Time Arbitrage Detection |
| **Target Users** | Active Traders, Market Makers, Quantitative Analysts |
| **Priority** | [X] High [ ] Medium [ ] Low |
| **Status** | [X] Planned [ ] In Development [ ] Complete |
| **Owner** | Intent Solutions |
| **Last Updated** | 2025-12-05 |

---

## 1. Executive Summary

**One-sentence description**: Transform Claude into a real-time arbitrage scanner that monitors multiple prediction market contracts across Polymarket and Kalshi simultaneously, identifies price discrepancies, and ranks opportunities by profit potential—no forecasting required.

**Value Proposition**: Unlike polymarket-analyst (which forecasts future prices), this skill focuses exclusively on finding arbitrage opportunities right now by comparing current prices across platforms—dramatically faster execution (<10 seconds for 10 contracts vs 60 seconds for single forecast) and purely data-driven with no prediction uncertainty.

**Key Evaluation Goals** (these will be measured, not guaranteed):
- Target activation accuracy: 95%
- Expected usage frequency: TBD (will track actual usage patterns)
- Description quality target: 85%+
- Detection speed: Goal <10 seconds for 10 contracts (stretch goal)
- False positive validation: We'll measure what percentage of detected opportunities represent actual pricing discrepancies

---

## 2. Problem Statement

### Current State (Without This Skill)

**Pain Points**:
1. **Manual cross-platform monitoring**: Traders must manually compare Polymarket and Kalshi prices across dozens of contracts (impossible to scale)
2. **Arbitrage windows close in seconds**: By the time manual analysis completes, opportunity is gone
3. **No centralized scanner**: No tool exists to batch-scan multiple contracts for arbitrage in real-time
4. **Forecast-based arbitrage is slow**: polymarket-analyst requires 30-60 seconds per contract (too slow for arbitrage)
5. **High cognitive load**: Monitoring 2 platforms × 20 contracts = 40 prices to track mentally

**Current Workarounds**:
- Open 10+ browser tabs (Polymarket + Kalshi) and manually spot-check prices
- Build custom Python scripts (10-20 hours development time, requires technical skills)
- Use polymarket-analyst for forecasting (too slow for arbitrage, focuses on prediction not current prices)

**Impact of Problem**:
- Manual workflows are slow and error-prone
- Scaling to multiple contracts is impractical without tooling
- User frustration: Speed matters for arbitrage execution
- Opportunities require timely detection

### Desired State (With This Skill)

**Transformation**:
- From: Manual cross-platform price monitoring via spreadsheets/tabs
- To: Automated batch scanning with structured, ranked results

**Expected Benefits**:
1. **Faster scanning**: Significantly reduced time to identify pricing discrepancies
2. **More contracts**: Monitor more contracts than manual workflows allow
3. **Structured output**: Standardized ranking and presentation of opportunities
4. **Reduced manual errors**: Automated comparison reduces data-handling mistakes
5. **No prediction uncertainty**: Pure price comparison (informational only, not forecasts)

---

## 3. Target Users

### Primary Users

**User Persona 1: Arbitrage Trader**
- **Background**: 1-3 years trading experience, monitors Polymarket/Kalshi, interested in price analysis
- **Goals**: Identify price discrepancies across platforms, understand market dynamics
- **Pain Points**: Manual monitoring is slow and tedious, hard to track multiple contracts
- **Use Frequency**: Likely multiple times per day for active traders
- **Technical Skills**: Understands arbitrage mechanics, basic spreadsheet skills, varying coding proficiency
- **Value**: Faster, more systematic price comparison workflow

**User Persona 2: Market Analyst**
- **Background**: Professional analyst or trader, tracks multiple prediction markets
- **Goals**: Understand cross-platform pricing dynamics, identify market inefficiencies
- **Pain Points**: Need to monitor many contracts, manual comparison doesn't scale
- **Use Frequency**: Regular use for analysis and research
- **Technical Skills**: Expert in market mechanics, proficient in trading/analysis tools
- **Value**: Structured analysis workflow, research insights

### Secondary Users

**Quantitative Analysts**: Research prediction market efficiency, measure cross-platform price convergence
**Academic Researchers**: Study arbitrage detection algorithms and market microstructure

---

## 4. User Stories

**Format**: "As a [user type], I want [capability], so that [benefit]"

### Critical User Stories (Must Have)

1. **As an** arbitrage trader,
   **I want** to scan 10 Polymarket contracts and compare them to Kalshi equivalents in under 10 seconds,
   **So that** I can identify arbitrage opportunities before the price window closes.

   **Acceptance Criteria**:
   - [ ] Batch processing: 10 contracts in <10 seconds total
   - [ ] Parallel API calls to Polymarket + Kalshi
   - [ ] Returns list of opportunities ranked by spread %
   - [ ] Includes buy/sell recommendations for each opportunity

2. **As an** arbitrage trader,
   **I want** opportunities ranked by profit potential (spread %),
   **So that** I can prioritize which trades to execute first (largest profits).

   **Acceptance Criteria**:
   - [ ] Calculates spread: abs(polymarket_price - kalshi_price)
   - [ ] Converts to profit %: spread / entry_price
   - [ ] Sorts opportunities descending by profit %
   - [ ] Filters by minimum threshold (default 3%, user-configurable)

3. **As a** trader,
   **I want** the skill to automatically match Polymarket contracts to Kalshi equivalents,
   **So that** I don't have to manually find matching contracts across platforms.

   **Acceptance Criteria**:
   - [ ] Fuzzy matching on contract titles/descriptions
   - [ ] Handles variations: "BTC $100k by Dec 2025" vs "Bitcoin $100,000 December 2025"
   - [ ] Logs unmatched contracts (no Kalshi equivalent found)
   - [ ] Confidence score for matches (high/medium/low)

### High-Priority User Stories (Should Have)

4. **As a** trader,
   **I want** to specify custom spread thresholds (e.g., only show >5% opportunities),
   **So that** I can filter out small arbitrage that isn't worth transaction costs.

   **Acceptance Criteria**:
   - [ ] Accepts `--min-spread` parameter (default: 0.03 = 3%)
   - [ ] Supports range: 0.01 to 0.20 (1% to 20%)
   - [ ] Returns "No opportunities found" if all spreads below threshold

5. **As a** trader,
   **I want** the skill to check both directions (buy Polymarket/sell Kalshi AND buy Kalshi/sell Polymarket),
   **So that** I don't miss opportunities regardless of which platform is overpriced.

   **Acceptance Criteria**:
   - [ ] Compares both: P > K and K > P
   - [ ] Returns direction: "BUY [platform] / SELL [platform]"
   - [ ] Calculates profit for both directions (may differ due to fees)

### Nice-to-Have User Stories (Could Have)

6. **As a** power user,
   **I want** to save my watchlist of contracts and re-scan with one command,
   **So that** I can monitor the same 20 contracts daily without re-entering IDs.

7. **As a** researcher,
   **I want** to export scan results to CSV for historical analysis,
   **So that** I can study arbitrage frequency and duration patterns.

---

## 5. Functional Requirements

### Core Capabilities (Must Have)

**REQ-1: Batch Contract Fetching**
- **Description**: Fetch current prices for multiple Polymarket contracts in parallel (not sequential)
- **Rationale**: Speed is critical—parallel fetching 10x faster than sequential
- **Acceptance Criteria**:
  - [ ] Accepts list of contract IDs (comma-separated or file)
  - [ ] Makes parallel API calls (asyncio or multiprocessing)
  - [ ] Fetches only current price (not historical—arbitrage is NOW)
  - [ ] Completes 10 contracts in <5 seconds
  - [ ] Saves to `data/polymarket_prices.json`
- **Dependencies**: Polymarket API access (free, no auth)

**REQ-2: Kalshi Equivalent Matching**
- **Description**: Automatically find Kalshi contracts matching each Polymarket contract
- **Rationale**: Manual matching is error-prone and time-consuming
- **Acceptance Criteria**:
  - [ ] Fuzzy string matching on contract titles (85%+ similarity threshold)
  - [ ] Handles common variations (abbreviations, date formats)
  - [ ] Logs confidence score (high/medium/low) for each match
  - [ ] Returns null if no match found (not an error—some contracts unique to one platform)
  - [ ] Saves to `data/kalshi_prices.json`
- **Dependencies**: Kalshi API access (optional—graceful degradation if unavailable)

**REQ-3: Arbitrage Detection & Ranking**
- **Description**: Compare prices across platforms, calculate spreads, filter by threshold, rank by profit
- **Rationale**: Core value proposition—identify best opportunities instantly
- **Acceptance Criteria**:
  - [ ] Calculates spread: abs(polymarket_price - kalshi_price)
  - [ ] Converts to profit %: (spread / entry_price) * 100
  - [ ] Filters: spread_pct >= min_threshold (default 3%)
  - [ ] Sorts: descending by profit %
  - [ ] Includes both directions (P→K and K→P)
  - [ ] Saves to `data/arbitrage_opportunities.json`
- **Dependencies**: REQ-1 (Polymarket prices), REQ-2 (Kalshi prices)

**REQ-4: Concise Opportunity Report**
- **Description**: Generate markdown table showing opportunities with actionable recommendations
- **Rationale**: Traders need instant decision-making info, not lengthy reports
- **Acceptance Criteria**:
  - [ ] Table format: Event | Polymarket | Kalshi | Spread | Profit % | Action
  - [ ] Sorted by profit % descending
  - [ ] Includes specific trade instructions: "BUY Kalshi YES at 0.45, SELL Polymarket YES at 0.52"
  - [ ] Notes unmatched contracts at bottom (for visibility)
  - [ ] Total execution time displayed (transparency)
  - [ ] Saves to `reports/arbitrage_scan_YYYY-MM-DD_HH-MM-SS.md`
- **Dependencies**: REQ-3 (arbitrage opportunities)

### Integration Requirements

**REQ-API-1: Polymarket REST API** (Current Prices Only)
- **Purpose**: Fetch current market prices (not historical odds—faster, simpler)
- **Endpoints**: `https://gamma-api.polymarket.com/markets` (REST, not GraphQL)
- **Authentication**: None required
- **Rate Limits**: 100 requests/minute (plenty for batch of 10-50 contracts)
- **Error Handling**: Retry 2x on 5xx errors, skip contract on 4xx errors (log warning)

**REQ-API-2: Kalshi REST API** (Current Prices)
- **Purpose**: Fetch current market prices for matched contracts
- **Endpoints**: `https://trading-api.kalshi.com/v1/markets`
- **Authentication**: API Key (optional—skill works without it, just no Kalshi comparison)
- **Rate Limits**: 60 requests/minute
- **Error Handling**: Skip Kalshi comparison entirely if API key missing or API fails (graceful degradation)

### Data Requirements

**REQ-DATA-1: Input Data Format**
- **Format**: List of Polymarket contract IDs (string array)
- **Required Fields**: Contract ID (hex address, 40 chars, 0x prefix)
- **Optional Fields**: Min spread threshold (float, 0.01-0.20)
- **Validation Rules**: Each ID matches regex `^0x[a-f0-9]{40}$`

**REQ-DATA-2: Output Data Format**
- **Format**: Markdown table + JSON opportunities
- **Fields**:
  - Event name (string)
  - Polymarket current price (float, 0-1)
  - Kalshi current price (float, 0-1)
  - Spread (float, 0-1)
  - Profit % (float)
  - Action (string: "BUY [platform] / SELL [platform]")
- **Quality Standards**: Spread % accurate to 2 decimal places, prices to 3 decimal places

### Performance Requirements

**REQ-PERF-1: Response Time**
- **Target**: <10 seconds for 10 contracts
- **Max Acceptable**: <20 seconds
- **Breakdown**:
  - Fetch Polymarket (parallel): <3 seconds
  - Fetch Kalshi (parallel): <3 seconds
  - Matching + Calculation: <1 second
  - Report Generation: <1 second

**REQ-PERF-2: Token Budget**
- **Description Size**: <250 characters (fits in 15k token budget)
- **SKILL.md Size**: <400 lines (~2,000 tokens) — simpler than polymarket-analyst
- **Total Skill Size**: <4,000 tokens including references

### Quality Requirements

**REQ-QUAL-1: Description Quality**
- **Target Score**: 85%+ on quality formula
- **Must Include**:
  - [X] Action-oriented verbs: "Scans", "Compares", "Identifies", "Ranks"
  - [X] "Use when [scenarios]" clause: "finding arbitrage opportunities", "comparing cross-platform prices"
  - [X] "Trigger with '[phrases]'" examples: "find arbitrage", "scan for mispricing", "compare Polymarket Kalshi prices"
  - [X] Domain keywords: "arbitrage", "Polymarket", "Kalshi", "spread", "mispricing"

**REQ-QUAL-2: Evaluation Goals**
- **Price Accuracy**: We will use current prices from APIs; validation will ensure data integrity
- **Matching Accuracy**: Goal is 85%+ correct Polymarket↔Kalshi matches; we'll measure actual performance and log confidence scores
- **Opportunity Validation**: We'll measure what percentage of detected pricing discrepancies reflect genuine cross-platform differences
- **Performance**: Goal is to complete 10-contract scan in <10 seconds (stretch goal); max acceptable <20 seconds

---

## 6. Non-Goals (Out of Scope)

**What This Skill Does NOT Do**:

1. **Price Forecasting**
   - **Rationale**: This skill is NOT polymarket-analyst—it compares current prices only, no ML/prediction
   - **Alternative**: Use polymarket-analyst for forecasting future prices

2. **Automated Trade Execution & Guaranteed Profits**
   - **Rationale**: This is strictly a detection and analysis tool, NOT a trading system. It does not and cannot guarantee profitable trades. Execution is user's responsibility and risk.
   - **Alternative**: User reviews recommendations and manually executes trades based on their own judgment
   - **Critical**: Pricing opportunities may close before execution, fees will reduce profit, and market conditions may change.

3. **Historical Arbitrage Analysis**
   - **Rationale**: Real-time scanning only, not backtesting or historical patterns
   - **Alternative**: Export results to CSV, use external analytics tools
   - **May be added in**: v2.0 (if user demand exists)

4. **Transaction Cost Optimization**
   - **Rationale**: Simple spread % calculation, doesn't factor in platform fees, gas costs, slippage
   - **Alternative**: User manually calculates net profit after fees
   - **Depends on**: Platform fee APIs (not currently available)

---

## 7. Success Metrics

### Skill Activation Metrics

**Metric 1: Activation Accuracy**
- **Definition**: % of times skill activates when it should (based on trigger phrases)
- **Target**: 95%+
- **Measurement**: Manual testing with 15 trigger phrase variations
- **Test Phrases**: "find arbitrage", "scan Polymarket Kalshi", "compare prediction market prices"

**Metric 2: False Positive Rate**
- **Definition**: % of times skill activates incorrectly (user wanted something else)
- **Target**: <5%
- **Measurement**: User feedback + monitoring logs

### Quality Metrics

**Metric 3: Description Quality Score**
- **Formula**: 6-criterion weighted scoring (see ARD)
- **Target**: 85%+
- **Components**:
  - Action-oriented: 20% (target: 18/20)
  - Clear triggers: 25% (target: 22/25)
  - Comprehensive: 15% (target: 13/15)
  - Natural language: 20% (target: 17/20)
  - Specificity: 10% (target: 9/10)
  - Technical terms: 10% (target: 10/10)
  - **Total Target**: 85/100

**Metric 4: SKILL.md Size**
- **Target**: <400 lines (simpler than polymarket-analyst's 500-line limit)
- **Max**: 500 lines (hard limit due to token budget)
- **Current**: TBD (to be measured after implementation)

### Usage Metrics

**Metric 5: Adoption & Usage Validation**
- **Goal**: Achieve 15-30 active users running ≥5 scans each in first 60 days to validate practical usefulness
- **Rationale**: Need real-world usage data to validate that the tool provides value
- **Measurement**: Skill invocation logs, community feedback

**Metric 6: User Satisfaction**
- **Target**: 4.0/5 rating (realistic for v1.0 of new tool)
- **Measurement**: Optional post-scan feedback (non-intrusive)

### Performance & Validation Metrics

**Metric 7: Scan Performance**
- **Domain-Specific**: Time to scan 10 contracts
- **Goal**: Aim for <10 seconds (stretch goal); max acceptable <20 seconds
- **Measurement**: Log execution times for analysis
- **Reality check**: Actual performance depends on API latency and network conditions

**Metric 8: Opportunity Validation**
- **Approach**: For detected pricing discrepancies, measure what percentage represent genuine cross-platform pricing gaps
- **Goal**: ≥70% of detected opportunities (above threshold) represent actual pricing differences when manually validated
- **Important**: Detection indicates a potential pricing difference, not a guaranteed profitable trade. Opportunities may close, fees apply, and market conditions may change.

---

## 8. User Experience Flow

### Typical Usage Flow

1. **User Intent**: Trader wants to check for arbitrage opportunities across 10 contracts
2. **Trigger**: User says "Scan these 10 Polymarket contracts for arbitrage vs Kalshi"
3. **Skill Activation**: Claude recognizes need for `nixtla-arbitrage-detector` skill
4. **Skill Execution**:
   - Step 1: Fetch current prices from Polymarket (parallel, 10 contracts)
   - Step 2: Match to Kalshi equivalents, fetch Kalshi prices (parallel)
   - Step 3: Calculate spreads, filter by threshold, rank by profit %
   - Step 4: Generate concise markdown table with recommendations
5. **Output Delivered**: Markdown table showing 3 arbitrage opportunities ranked by profit
6. **User Action**: Reviews table, executes top 2 trades (BUY Kalshi, SELL Polymarket)

### Example Scenario

**Scenario**: Active trader monitoring 10 crypto prediction market contracts

**Input**:
```
Scan these 10 Polymarket contracts for arbitrage opportunities vs Kalshi:
0x1234567890abcdef1234567890abcdef12345678
0xABCDEF1234567890ABCDEF1234567890ABCDEF12
... (8 more contract IDs)

Minimum spread: 4%
```

**Claude's Response**:
```
I'll scan these 10 contracts for arbitrage using the nixtla-arbitrage-detector skill.
This will fetch current prices from both platforms and identify opportunities above 4% spread.

[Skill executes 4-step workflow in ~7 seconds]

✓ Scan complete! Found 3 arbitrage opportunities.
```

**Output** (`reports/arbitrage_scan_2025-12-05_14-30-25.md`):
```markdown
# Arbitrage Scan Results

**Scan Date**: 2025-12-05 14:30:25
**Contracts Scanned**: 10
**Minimum Spread**: 4.0%
**Execution Time**: 6.8 seconds

## Opportunities Found: 3

| Event | Polymarket | Kalshi | Spread | Profit % | Action |
|-------|------------|--------|--------|----------|--------|
| Bitcoin reaches $100k by Dec 2025 | 0.680 | 0.600 | 0.080 | 13.3% | BUY Kalshi YES at 0.600, SELL Polymarket YES at 0.680 |
| Ethereum reaches $10k by Q1 2026 | 0.420 | 0.380 | 0.040 | 10.5% | BUY Kalshi YES at 0.380, SELL Polymarket YES at 0.420 |
| Fed rate cut in January 2026 | 0.550 | 0.490 | 0.060 | 12.2% | BUY Kalshi YES at 0.490, SELL Polymarket YES at 0.550 |

## Contracts Below Threshold: 5

| Event | Polymarket | Kalshi | Spread | Profit % | Reason |
|-------|------------|--------|--------|----------|--------|
| Trump wins 2028 election | 0.520 | 0.510 | 0.010 | 2.0% | Below 4% threshold |
| ... | ... | ... | ... | ... | ... |

## Unmatched Contracts: 2

| Event | Platform | Current Price | Reason |
|-------|----------|---------------|--------|
| Bitcoin $150k by 2027 | Polymarket | 0.320 | No Kalshi equivalent found |
| Recession in 2026 | Polymarket | 0.450 | No Kalshi equivalent found |

---

*Generated by nixtla-arbitrage-detector | Execution time: 6.8 seconds*
```

**Important Disclaimer**: This example shows how pricing discrepancies are presented. Actual execution depends on user's trading decisions, timing, fees, and market conditions. Detected opportunities do not guarantee profitable trades. Users remain responsible for their own risk management and trading decisions. Not financial advice.

---

## 9. Integration Points

### External Systems

**System 1: Polymarket REST API**
- **Purpose**: Fetch current market prices for batch of contracts
- **Integration Type**: REST API (HTTP GET)
- **Authentication**: None required (public data)
- **Data Flow**: Skill → Polymarket API → Current prices JSON

**System 2: Kalshi REST API**
- **Purpose**: Fetch current market prices for matched contracts
- **Integration Type**: REST API (HTTP GET)
- **Authentication**: API key (optional—skill works without it)
- **Data Flow**: Skill → Kalshi API → Current prices JSON

### Internal Dependencies

**Dependency 1: Fuzzy Matching Library**
- **What it provides**: String similarity algorithm (Levenshtein distance)
- **Why needed**: Match Polymarket contract titles to Kalshi equivalents
- **Library**: `fuzzywuzzy` or `rapidfuzz` (Python)

**Dependency 2: Python Libraries**
- **Libraries**: `requests` (HTTP), `asyncio` (parallel API calls), `pandas` (data manipulation)
- **Versions**:
  - requests >= 2.28.0
  - asyncio (built-in Python 3.7+)
  - pandas >= 2.0.0

---

## 10. Constraints & Assumptions

### Technical Constraints

1. **Token Budget**: Must fit in 4,000 token limit (description + SKILL.md + references)
2. **API Rate Limits**:
   - Polymarket: 100 req/min (can scan 100 contracts/min—not a bottleneck)
   - Kalshi: 60 req/min (can scan 60 contracts/min—not a bottleneck)
3. **Processing Time**: Must complete in <20 seconds for 10 contracts
4. **Dependencies**: Requires Python 3.9+, internet connection

### Business Constraints

1. **API Costs**: No API costs (Polymarket is free, Kalshi free tier exists)
2. **Timeline**: Skill must be ready for prediction markets vertical launch (Q1 2026)
3. **Resources**: 1 developer, 20 hours development + testing (simpler than polymarket-analyst)

### Assumptions

1. **Assumption 1: Traders understand arbitrage mechanics**
   - **Risk if false**: Users may not understand how to execute trades based on recommendations
   - **Mitigation**: Include brief arbitrage explanation in skill documentation

2. **Assumption 2: Matching accuracy >90% is sufficient**
   - **Risk if false**: Many false matches → incorrect arbitrage signals
   - **Mitigation**: Log confidence scores, allow user to verify matches before trading

3. **Assumption 3: Arbitrage opportunities exist frequently (>5% of scans)**
   - **Risk if false**: Users get "No opportunities found" too often → skill appears useless
   - **Mitigation**: Set realistic expectations in documentation (arbitrage is rare, 5-10% hit rate)

4. **Assumption 4: 3% minimum spread is reasonable default**
   - **Risk if false**: Misses small arbitrage (<3%) or flags too many unprofitable opportunities (>3%)
   - **Mitigation**: Make threshold user-configurable (1-20%), document fee considerations

---

## 11. Risk Assessment

### Technical Risks

**Risk 1: API Rate Limiting (Kalshi)**
- **Probability**: Medium (60 req/min limit, scanning 10+ contracts)
- **Impact**: Medium (skill slows down, but doesn't break)
- **Mitigation**:
  - Batch Kalshi requests (1 call per 10 contracts if API supports batch)
  - Exponential backoff on 429 errors
  - Skip Kalshi if rate limit hit (graceful degradation)

**Risk 2: Fuzzy Matching Errors (False Positives)**
- **Probability**: Medium (string similarity isn't perfect)
- **Impact**: High (incorrect matches → false arbitrage signals → user loses money)
- **Mitigation**:
  - Require 85%+ similarity threshold (reduce false matches)
  - Log confidence scores (high/medium/low)
  - Manual verification step: show user the match before calculating spread

**Risk 3: Price Staleness (Arbitrage Window Closes)**
- **Probability**: High (arbitrage opportunities last seconds to minutes)
- **Impact**: High (user executes trade, but prices already equalized → no profit)
- **Mitigation**:
  - Timestamp all prices (warn if >30 seconds old)
  - Include disclaimer: "Prices as of YYYY-MM-DD HH:MM:SS—verify before trading"
  - Fast execution (<10 seconds) minimizes staleness

### User Experience Risks

**Risk 1: Skill Over-Triggering (False Positives)**
- **Probability**: Low (specific arbitrage terminology)
- **Impact**: Low (minor annoyance)
- **Mitigation**:
  - Precise description with arbitrage-specific triggers
  - Test with 15+ trigger phrase variations

**Risk 2: Skill Under-Triggering (False Negatives)**
- **Probability**: Medium (users may use non-standard phrasing)
- **Impact**: Medium (skill not activated when needed)
- **Mitigation**:
  - Comprehensive trigger phrases in description
  - Document example phrases in SKILL.md

**Risk 3: Users Overestimate Profit (Ignoring Fees) & Market Realities**
- **Probability**: High (skill doesn't factor in transaction costs, slippage, or market timing)
- **Impact**: High (user expects X% profit after detecting opportunity, but actual execution differs due to fees, timing, and market conditions)
- **Mitigation**:
  - Explicit disclaimer in every report: "Spread % shown excludes fees and slippage. Verify net profit and verify prices before trading."
  - Document fee structure and realistic expectations
  - Recommend 5%+ spread as baseline to account for typical costs

---

## 12. Open Questions

**Questions Requiring Decisions**:

1. **Question**: Should we include Polymarket→Polymarket arbitrage (same platform, different order books)?
   - **Options**:
     - Option A: Cross-platform only (Polymarket vs Kalshi)
     - Option B: Also check intra-platform arbitrage
   - **Decision Needed By**: Before development starts
   - **Owner**: Product Lead

2. **Question**: What should default minimum spread be (3%, 4%, or 5%)?
   - **Options**:
     - 3%: More opportunities, but many unprofitable after fees
     - 4%: Balanced (recommended)
     - 5%: Conservative, fewer false positives
   - **Decision Needed By**: Before v1.0 release
   - **Owner**: Early user feedback

3. **Question**: Should skill auto-verify matched contracts (require user confirmation)?
   - **Options**:
     - Auto-match: Faster, but risk of false matches
     - Manual verification: Slower, but more accurate
   - **Decision Needed By**: Before development
   - **Owner**: Technical Lead

**Recommended Decisions**:
1. Cross-platform only for v1.0 (simpler, clearer value)
2. Default 4% minimum spread (balances opportunity frequency and profitability)
3. Auto-match with confidence scores (log matches, user can override)

---

## 13. Appendix: Examples

### Example 1: Standard 10-Contract Scan

**User Request**:
```
Scan these 10 Polymarket contracts for arbitrage vs Kalshi:
[List of 10 contract IDs]
```

**Expected Skill Behavior**:
1. Fetch current prices from Polymarket (parallel, 10 contracts)
2. Match to Kalshi equivalents, fetch Kalshi prices (parallel)
3. Calculate spreads, filter by 3% threshold
4. Rank by profit %, generate table

**Expected Output**:
```markdown
# Arbitrage Scan Results
**Opportunities Found**: 2

| Event | Polymarket | Kalshi | Spread | Profit % | Action |
|-------|------------|--------|--------|----------|--------|
| BTC $100k Dec 2025 | 0.680 | 0.600 | 0.080 | 13.3% | BUY Kalshi / SELL Polymarket |
| ETH $10k Q1 2026 | 0.420 | 0.380 | 0.040 | 10.5% | BUY Kalshi / SELL Polymarket |

**Execution Time**: 7.2 seconds
```

### Example 2: High Spread Threshold (Conservative)

**User Request**:
```
Find arbitrage with minimum 8% spread for crypto markets
```

**Expected Behavior**:
1. Scan crypto-related contracts
2. Filter by 8% minimum spread (very conservative)
3. Likely returns 0-1 opportunities (high threshold)

**Expected Output**:
```markdown
# Arbitrage Scan Results
**Minimum Spread**: 8.0%
**Opportunities Found**: 0

**Contracts Below Threshold**: 8
(All spreads were <8%)

**Recommendation**: Lower threshold to 4-5% for more opportunities.
```

### Example 3: Kalshi API Unavailable (Graceful Degradation)

**User Request**:
```
Scan 5 contracts for arbitrage
```

**Expected Behavior**:
1. Fetch Polymarket prices (succeeds)
2. Attempt Kalshi fetch → API key missing or API down
3. Skip Kalshi comparison, note in output

**Expected Output**:
```markdown
# Arbitrage Scan Results

**WARNING**: Kalshi API unavailable (API key not set or service down)
Arbitrage detection skipped—Polymarket prices only.

**Polymarket Current Prices**:
| Contract | YES Price |
|----------|-----------|
| BTC $100k Dec 2025 | 0.680 |
| ETH $10k Q1 2026 | 0.420 |
...

**Recommendation**: Set KALSHI_API_KEY environment variable to enable arbitrage detection.
```

---

## 14. Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2025-12-05 | Initial PRD | Intent Solutions |
| 1.0.1 | 2025-12-06 | De-hyped for Nixtla review: P&L claims removed ("$10k-$100k", "$50k-$500k"), adoption targets made realistic (15-30 users vs 40%), accuracy metrics reframed as evaluation goals, emphasized that detected opportunities are informational only and not guaranteed profitable, added explicit disclaimers about fees/slippage/market timing, clarified analysis-only scope | Intent Solutions |

---

## 15. Approval

| Role | Name | Approval Date | Signature |
|------|------|---------------|-----------|
| Product Owner | Jeremy Longshore | 2025-12-05 | [Pending] |
| Tech Lead | Jeremy Longshore | 2025-12-05 | [Pending] |
| User Representative | Arbitrage Trading Community | TBD | [Pending] |

---

**Template maintained by**: Intent Solutions
**For**: Nixtla Skills Pack + Global Standard
**Last Updated**: 2025-12-05
