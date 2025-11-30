# Nixtla Plugin Showcase - Decision Matrix

**For:** Max Mergenthaler, Nixtla
**From:** Jeremy Longshore, Intent Solutions
**Date:** 2025-11-30
**Version:** 1.0
**Purpose:** Help prioritize which plugins to build first

---

## How to Use This Matrix

This document scores all 9 specified plugins across 4 criteria to help you decide which to build first. Use this for:

- Selecting your Pilot plugin (Option 2)
- Choosing your Platform bundle (Option 3)
- Understanding trade-offs between plugins

---

## Scoring Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **Business Impact** | 40% | Revenue generation or cost reduction potential |
| **Development Effort** | 20% | Complexity, dependencies, unknowns |
| **Risk** | 20% | Technical risk, adoption risk, market risk |
| **Strategic Fit** | 20% | Alignment with Nixtla's vision and roadmap |

### Scoring Scale

- **5** = Excellent (high impact, low effort, low risk, perfect fit)
- **4** = Good (above average)
- **3** = Average (moderate across the board)
- **2** = Below Average (concerns exist)
- **1** = Poor (high risk, low impact, or misaligned)

---

## Plugin Scores

### Efficiency Plugins

#### 1. Cost Optimizer

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| Business Impact | 5 | Direct cost reduction (30-50%), measurable ROI |
| Development Effort | 4 | Moderate complexity (usage analysis + recommendations) |
| Risk | 5 | Low - similar tools exist, proven value |
| Strategic Fit | 4 | Aligns with enterprise cost management |
| **Weighted Total** | **4.6** | **HIGHEST SCORE** |

**Recommendation:** **Top choice for Pilot.** Delivers immediate, measurable value with low risk.

---

#### 2. Migration Assistant

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| Business Impact | 4 | Reduces onboarding friction, accelerates customer acquisition |
| Development Effort | 3 | Complex (code translation, accuracy comparison) |
| Risk | 3 | Medium - depends on Prophet API compatibility |
| Strategic Fit | 5 | Critical for market share growth against Prophet |
| **Weighted Total** | **3.8** | |

**Recommendation:** High strategic value, but higher complexity. Good for Platform bundle.

---

#### 3. Forecast Explainer

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| Business Impact | 4 | Reduces support load (40% fewer tickets) |
| Development Effort | 3 | Moderate (requires explainability algorithms) |
| Risk | 4 | Low-medium - well-understood domain |
| Strategic Fit | 4 | Improves customer experience and trust |
| **Weighted Total** | **3.8** | |

**Recommendation:** Strong ROI for support teams. Good second choice for Pilot.

---

### Growth Plugins

#### 4. Nixtla vs StatsForecast Benchmark

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| Business Impact | 4 | Increases TimeGPT adoption, provides upsell data |
| Development Effort | 4 | Moderate (builds on existing Baseline Lab) |
| Risk | 4 | Low - extends working plugin |
| Strategic Fit | 5 | Differentiates TimeGPT value proposition |
| **Weighted Total** | **4.2** | **2nd HIGHEST SCORE** |

**Recommendation:** Natural extension of Baseline Lab. Excellent for demonstrating TimeGPT value.

---

#### 5. ROI Calculator

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| Business Impact | 4 | Shortens enterprise sales cycles (2-3 months) |
| Development Effort | 5 | Low - mostly calculation logic and UI |
| Risk | 5 | Very low - no external dependencies |
| Strategic Fit | 4 | Enables enterprise sales team |
| **Weighted Total** | **4.4** | **3rd HIGHEST SCORE** |

**Recommendation:** Quick win for sales enablement. Low effort, high value.

---

#### 6. Airflow Operator

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| Business Impact | 5 | Opens enterprise data platform market |
| Development Effort | 3 | Moderate (Airflow integration, monitoring) |
| Risk | 3 | Medium - depends on Airflow API stability |
| Strategic Fit | 5 | Critical for enterprise market expansion |
| **Weighted Total** | **4.2** | **Tied 2nd HIGHEST** |

**Recommendation:** High strategic value for enterprise market. Good for Platform bundle.

---

#### 7. dbt Package

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| Business Impact | 4 | Expands into analytics engineering market |
| Development Effort | 3 | Moderate (dbt integration, SQL workflows) |
| Risk | 3 | Medium - requires dbt expertise |
| Strategic Fit | 4 | Reaches new customer segment |
| **Weighted Total** | **3.6** | |

**Recommendation:** Strategic market expansion. Consider for Platform bundle.

---

#### 8. Snowflake Adapter

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| Business Impact | 5 | 10x larger enterprise contracts (Fortune 500) |
| Development Effort | 2 | High complexity (UDF, Snowflake integration) |
| Risk | 2 | High - requires Snowflake expertise, testing |
| Strategic Fit | 5 | Critical for Fortune 500 market |
| **Weighted Total** | **3.8** | |

**Recommendation:** Highest revenue potential, but highest risk. Requires Snowflake expertise. Consider for later or with partner.

---

#### 9. Anomaly Streaming Monitor

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| Business Impact | 4 | Opens real-time monitoring market (DevOps/SRE) |
| Development Effort | 2 | High complexity (Kafka/Kinesis, alerting) |
| Risk | 3 | Medium - streaming infrastructure complexity |
| Strategic Fit | 3 | Moderate - new market segment |
| **Weighted Total** | **3.2** | |

**Recommendation:** Interesting market, but high complexity. Consider for future.

---

## Summary Rankings

| Rank | Plugin | Score | Category | Recommendation |
|------|--------|-------|----------|----------------|
| **1** | **Cost Optimizer** | **4.6** | Efficiency | **Best Pilot choice** |
| **2** | ROI Calculator | 4.4 | Growth | Quick win for sales |
| **3** | Nixtla vs Benchmark | 4.2 | Growth | Extends working plugin |
| **3** | Airflow Operator | 4.2 | Growth | Enterprise market expansion |
| **5** | Migration Assistant | 3.8 | Efficiency | High strategic value |
| **5** | Forecast Explainer | 3.8 | Efficiency | Support load reduction |
| **5** | Snowflake Adapter | 3.8 | Growth | Highest revenue, highest risk |
| **8** | dbt Package | 3.6 | Growth | New market segment |
| **9** | Streaming Monitor | 3.2 | Growth | Future consideration |

---

## Recommended Combinations

### Pilot Option (Choose 1)

**Best Choice:** **Cost Optimizer** (Score: 4.6)
- Highest overall score
- Immediate, measurable ROI
- Low risk, moderate effort
- Aligns with enterprise cost management

**Alternative:** **ROI Calculator** (Score: 4.4)
- Easiest to build (5/5 development effort)
- Enables sales team immediately
- Very low risk

---

### Platform Bundles (Choose 3+)

#### Bundle A: Quick Wins + Market Expansion
1. **Cost Optimizer** (4.6) - Immediate ROI
2. **ROI Calculator** (4.4) - Sales enablement
3. **Airflow Operator** (4.2) - Enterprise market

**Why:** Balance of quick wins and strategic market expansion. All have manageable risk.

---

#### Bundle B: Strategic Differentiation
1. **Cost Optimizer** (4.6) - Immediate value
2. **Nixtla vs Benchmark** (4.2) - Differentiate TimeGPT
3. **Migration Assistant** (3.8) - Competitive advantage vs Prophet

**Why:** Positions Nixtla as the modern, AI-native alternative to legacy tools.

---

#### Bundle C: Enterprise Focus
1. **ROI Calculator** (4.4) - Sales tool
2. **Airflow Operator** (4.2) - Enterprise data teams
3. **Snowflake Adapter** (3.8) - Fortune 500 contracts

**Why:** Comprehensive enterprise play. Requires Snowflake expertise or partner.

---

## Decision Framework

### If your priority is...

**Immediate ROI:**
→ Choose **Cost Optimizer** (Pilot)
→ Measurable within 30 days

**Sales Acceleration:**
→ Choose **ROI Calculator** + **Nixtla vs Benchmark** (Platform)
→ Equip sales team with proof points

**Enterprise Market:**
→ Choose **Airflow Operator** + **Snowflake Adapter** (Platform)
→ Reach data platform buyers

**Competitive Positioning:**
→ Choose **Migration Assistant** + **Nixtla vs Benchmark** (Platform)
→ Differentiate from Prophet/ARIMA

**Support Reduction:**
→ Choose **Forecast Explainer** (Pilot)
→ Reduce ticket volume 40%

---

## Risk Mitigation

### High-Risk Plugins (Score < 3.5)

| Plugin | Primary Risk | Mitigation Strategy |
|--------|--------------|---------------------|
| **Snowflake Adapter** | Complexity, requires expertise | Partner with Snowflake expert or hire consultant |
| **Streaming Monitor** | Infrastructure complexity | Start with POC, validate market demand first |
| **dbt Package** | Requires dbt expertise | Validate customer interest before building |

---

## Next Steps

1. **Review scores and rationale** with your team
2. **Identify your top priority** (ROI, sales, enterprise, competitive)
3. **Choose 1 plugin (Pilot) or 3+ plugins (Platform)** using recommendations above
4. **Schedule call** to finalize selection and discuss implementation

---

## Questions to Ask Yourself

Before deciding, consider:

- [ ] What's our biggest pain point right now? (Cost, support, onboarding, sales?)
- [ ] What market segment do we want to expand into? (Enterprise, analytics, real-time?)
- [ ] What's our risk tolerance? (Low = Cost Optimizer, High = Snowflake)
- [ ] What's our timeline? (4-6 weeks = Pilot, 12-16 weeks = Platform)
- [ ] What do we want to achieve in Q1 2026? (Quick win vs strategic positioning)

---

## Contact

**Jeremy Longshore**
Intent Solutions
📧 jeremy@intentsolutions.io
📞 251.213.1115
📅 [Schedule Call](https://calendly.com/intentconsulting)

---

*Scores are estimates based on current information. Final scores may change after discovery phase.*
