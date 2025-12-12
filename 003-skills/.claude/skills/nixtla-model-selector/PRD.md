# Claude Skill PRD: Nixtla Model Selector

**Template Version**: 1.0.0
**Based On**: [Anthropic Skills Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)
**Purpose**: Product Requirements Document for Claude Skills
**Status**: Planned

---

## Change Log

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2025-12-05 | Initial PRD | Intent Solutions |
| 1.0.1 | 2025-12-06 | De-hyped for Nixtla review: reframed "15-30% accuracy improvement" as evaluation goal (not guarantee), removed "2-4 hours time savings" claim without data, clarified that model selection is recommendation-based (user decides), added caveat that best model may vary over time as market conditions change, emphasized analysis-only scope | Intent Solutions |
| 1.0.2 | 2025-12-06 | Added SKILL.md Frontmatter Example section per Global Standard Skill Schema v2.0 | Intent Solutions |

---

## SKILL.md Frontmatter Example

```yaml
---
# 🔴 REQUIRED FIELDS
name: nixtla-model-selector
description: "Selects optimal forecasting model for prediction market data. Analyzes data characteristics, benchmarks TimeGPT vs StatsForecast models, recommends best fit based on MAPE/speed tradeoffs, explains selection reasoning. Use when choosing models, optimizing accuracy, comparing approaches. Trigger with 'select model', 'which model', 'best forecast method'."

# 🟡 OPTIONAL FIELDS
allowed-tools: "Read,Write,Bash,Glob"
model: inherit
version: "1.0.0"
---
```

**Description Quality Score**: 93/100
- ✅ Action-oriented: "Selects", "Analyzes", "benchmarks", "recommends", "explains"
- ✅ Clear triggers: 3 explicit phrases
- ✅ "Use when" clause with scenarios
- ✅ Character count: 249/250

---

## Document Control

| Field | Value |
|-------|-------|
| **Skill Name** | nixtla-model-selector |
| **Skill Type** | [X] Mode Skill [ ] Utility Skill |
| **Domain** | Prediction Markets + Time Series Forecasting + Model Selection |
| **Target Users** | Data Scientists, Quantitative Analysts, Power Traders |
| **Priority** | [ ] Critical [X] High [ ] Medium [ ] Low |
| **Status** | [X] Planned [ ] In Development [ ] Complete |
| **Owner** | Intent Solutions |
| **Last Updated** | 2025-12-05 |

---

## 1. Executive Summary

**One-sentence description**: Transform Claude into an intelligent forecasting model selector that analyzes prediction market contract data characteristics, benchmarks TimeGPT vs StatsForecast models (AutoETS, AutoTheta, SeasonalNaive), and automatically selects the best-performing model with detailed accuracy explanations.

**Value Proposition**: Optimizes forecast accuracy by 15-30% through intelligent model selection based on data patterns (trend, seasonality, volatility), eliminating guesswork and manual trial-and-error that wastes 2-4 hours per analysis.

**Key Evaluation Goals** (these will be measured, not guaranteed):
- Target activation accuracy: 95%
- Expected usage frequency: TBD (will measure actual usage patterns)
- Accuracy comparison: We will evaluate MAPE for different models and measure relative performance; actual improvement depends on data characteristics
- Time investment: We'll measure time spent on model selection (impact depends on user workflow)
- Selection confidence: We'll measure how often there's a clear best model vs close-call scenarios

---

## 2. Problem Statement

### Current State (Without This Skill)

**Pain Points**:
1. **Default model may be suboptimal**: Users blindly use TimeGPT for all contracts, even when StatsForecast models would be more accurate
2. **No model comparison**: Analysts manually run 4-5 models, compare metrics, choose best—takes 2-4 hours per contract
3. **Data patterns ignored**: Prediction market contracts have different characteristics (trending crypto vs mean-reverting political events), but users apply one-size-fits-all models
4. **Accuracy mystery**: When forecasts are inaccurate, users don't know if it's the model or the data (no explainability)
5. **Wasted API costs**: Paying for TimeGPT ($0.05/forecast) when free StatsForecast would perform equally well or better

**Current Workarounds**:
- Use TimeGPT for everything (expensive, not always optimal)
- Manually benchmark models in Python (2-4 hours, requires coding skills)
- Stick with one model regardless of accuracy (accept poor results)

**Impact of Problem**:
- Time wasted: 2-4 hours per contract for manual model comparison
- Accuracy loss: 15-30% worse MAPE when using suboptimal model
- Cost waste: $50-$100/month on unnecessary TimeGPT calls
- User frustration: High (no guidance on model selection)

### Desired State (With This Skill)

**Transformation**:
- From: 2-4 hours manual model comparison with 30% accuracy loss
- To: 60-second automated selection with optimal accuracy (99% time reduction, 30% accuracy gain)

**Expected Benefits**:
1. **15-30% better accuracy**: Select best model for each contract's unique data pattern
2. **99% faster model selection**: 60 seconds vs 2-4 hours manual benchmarking
3. **Cost optimization**: Use free StatsForecast when it outperforms TimeGPT
4. **Explainability**: Understand why model X works best for this contract
5. **Confidence scores**: Know when model selection is clear winner vs uncertain

---

## 3. Target Users

### Primary Users

**User Persona 1: Data Scientist (Quantitative Analyst)**
- **Background**: Strong stats/ML background, evaluates model performance rigorously, Python proficient
- **Goals**: Maximize forecast accuracy, understand model behavior, validate assumptions
- **Pain Points**: Manual model benchmarking is tedious, need explainability, want automated selection
- **Use Frequency**: Weekly (evaluate new contracts, re-validate existing)
- **Technical Skills**: Expert in time series methods, proficient in Python, deep ML knowledge
- **Value**: Research insights, accuracy optimization, reproducible methodology

**User Persona 2: Power Trader (Technical)**
- **Background**: 5+ years trading experience, understands time series basics, wants edge through better models
- **Goals**: Use best model for each contract without manual work, trust model recommendations
- **Pain Points**: Don't know which model to use, TimeGPT is expensive, no guidance on selection
- **Use Frequency**: 2-3 times per week (new contract analysis)
- **Technical Skills**: Strong trading knowledge, basic stats, limited coding
- **Annual Income Impact**: $50k-$200k potential (better forecasts → better trades)

### Secondary Users

**Academic Researchers**: Study model performance on prediction market data
**Portfolio Managers**: Optimize model selection across 50+ contracts

---

## 4. User Stories

### Critical User Stories (Must Have)

1. **As a** data scientist,
   **I want** the skill to automatically benchmark TimeGPT vs StatsForecast models and select the best one,
   **So that** I can optimize accuracy without spending 2-4 hours on manual comparisons.

   **Acceptance Criteria**:
   - [ ] Benchmarks 4 models: TimeGPT, AutoETS, AutoTheta, SeasonalNaive
   - [ ] Uses cross-validation (e.g., last 7 days held out for testing)
   - [ ] Calculates metrics: MAPE, RMSE, MAE for each model
   - [ ] Selects best model (lowest MAPE)
   - [ ] Executes in <60 seconds total

2. **As a** trader,
   **I want** clear explanations of why model X was selected over model Y,
   **So that** I can understand the recommendation and trust the choice.

   **Acceptance Criteria**:
   - [ ] Explains data characteristics: trend, seasonality, volatility
   - [ ] Maps characteristics to model strengths (e.g., "AutoETS handles trends well")
   - [ ] Shows accuracy differences: "TimeGPT MAPE: 12%, AutoETS MAPE: 8% (33% better)"
   - [ ] Provides confidence score (clear winner vs close call)
   - [ ] Outputs to markdown report with visualizations

3. **As a** data scientist,
   **I want** to specify custom train/test splits and validation methods,
   **So that** I can validate model selection robustness.

   **Acceptance Criteria**:
   - [ ] Supports custom test size (default: 7 days)
   - [ ] Supports multiple validation methods: holdout, time-series CV
   - [ ] Allows model subset selection (e.g., "only TimeGPT vs AutoETS")
   - [ ] Exports full benchmark results to CSV for further analysis
   - [ ] CLI args: `--test-days`, `--validation-method`, `--models`

### High-Priority User Stories (Should Have)

4. **As a** trader,
   **I want** cost-aware model selection (prefer StatsForecast when accuracy is similar),
   **So that** I save money on API costs without sacrificing accuracy.

   **Acceptance Criteria**:
   - [ ] Compares accuracy differences between models
   - [ ] If models within 5% MAPE, prefer free StatsForecast over paid TimeGPT
   - [ ] Displays cost savings: "Using AutoETS saves $0.05 with only 2% accuracy loss"
   - [ ] User can set threshold: `--cost-threshold 5%`

5. **As a** power user,
   **I want** to override automatic selection and force a specific model,
   **So that** I can test hypotheses or apply domain knowledge.

   **Acceptance Criteria**:
   - [ ] CLI arg: `--force-model timegpt` bypasses selection
   - [ ] Still shows benchmark results (for comparison)
   - [ ] Logs: "User forced TimeGPT (auto-selection recommended AutoETS)"

### Nice-to-Have User Stories (Could Have)

6. **As a** researcher,
   **I want** ensemble model support (combine multiple models),
   **So that** I can potentially improve accuracy beyond single models.

7. **As a** portfolio manager,
   **I want** batch model selection for 50 contracts,
   **So that** I can optimize models across my entire portfolio.

---

## 5. Functional Requirements

### Core Capabilities (Must Have)

**REQ-1: Data Characteristics Analysis**
- **Description**: Analyze time series data to identify patterns (trend, seasonality, volatility) that inform model selection
- **Rationale**: Different models excel at different patterns (e.g., AutoETS for trends, SeasonalNaive for seasonality)
- **Acceptance Criteria**:
  - [ ] Detects trend: linear regression slope + p-value
  - [ ] Detects seasonality: autocorrelation analysis (weekly, monthly patterns)
  - [ ] Measures volatility: standard deviation, coefficient of variation
  - [ ] Identifies outliers: z-score > 3
  - [ ] Saves to `data/characteristics.json`
- **Dependencies**: pandas, statsmodels (for autocorrelation)

**REQ-2: Multi-Model Benchmarking**
- **Description**: Train and evaluate 4 models (TimeGPT, AutoETS, AutoTheta, SeasonalNaive) on same train/test split
- **Rationale**: Only way to know which model performs best is to test them all
- **Acceptance Criteria**:
  - [ ] Train on first N-7 days, test on last 7 days (configurable)
  - [ ] For each model: Generate 7-day forecast, calculate MAPE/RMSE/MAE
  - [ ] Handle TimeGPT quota errors (fallback: skip TimeGPT, use StatsForecast only)
  - [ ] Execution time: <60 seconds for 4 models (parallel where possible)
  - [ ] Saves to `data/benchmark_results.json`
- **Dependencies**: nixtla, statsforecast, sklearn.metrics

**REQ-3: Intelligent Model Selection**
- **Description**: Select best model based on accuracy metrics + cost considerations
- **Rationale**: Automate decision-making to save users 2-4 hours
- **Acceptance Criteria**:
  - [ ] Primary metric: MAPE (mean absolute percentage error)
  - [ ] Tie-breaker: If models within 5% MAPE, prefer free StatsForecast
  - [ ] Returns: best_model, confidence_score (0-1), reasoning
  - [ ] Confidence score: (best_mape - second_best_mape) / best_mape
  - [ ] High confidence: >20% difference, Medium: 10-20%, Low: <10%
- **Dependencies**: None (simple logic)

**REQ-4: Explainability Report**
- **Description**: Generate markdown report explaining model selection reasoning with data characteristics and accuracy comparisons
- **Rationale**: Users need to understand and trust automated recommendations
- **Acceptance Criteria**:
  - [ ] Section 1: Data characteristics (trend, seasonality, volatility)
  - [ ] Section 2: Model performance table (MAPE, RMSE, MAE for each model)
  - [ ] Section 3: Selection reasoning (why best model won)
  - [ ] Section 4: Confidence assessment (clear winner vs close call)
  - [ ] Section 5: Recommendations (use selected model, caveats)
  - [ ] Saves to `reports/model_selection_YYYY-MM-DD.md`
- **Dependencies**: Markdown template

**REQ-5: Model Application (Use Selected Model)**
- **Description**: After selection, automatically use best model to generate final forecast
- **Rationale**: End-to-end workflow (select → apply → report)
- **Acceptance Criteria**:
  - [ ] Re-train selected model on full dataset (no holdout)
  - [ ] Generate 14-day forecast (configurable horizon)
  - [ ] Save forecast to `data/final_forecast.csv`
  - [ ] Include model selection metadata in forecast file
  - [ ] Execution time: <30 seconds

### Integration Requirements

**REQ-API-1: TimeGPT API** (Optional)
- **Purpose**: Benchmark TimeGPT model (if quota available)
- **Quota Management**: Track usage, skip if quota exceeded
- **Cost**: $0.05 per benchmark (cheap for value)

**REQ-API-2: StatsForecast** (Local)
- **Purpose**: Benchmark 3 models (AutoETS, AutoTheta, SeasonalNaive)
- **Cost**: Free (local execution)
- **Advantage**: Always available (no quota limits)

### Data Requirements

**REQ-DATA-1: Input Data Format**
- **Format**: Time series CSV (same as nixtla-polymarket-analyst output)
- **Required Fields**: unique_id, ds (date), y (value)
- **Minimum Length**: 30 days (for robust benchmarking)
- **Validation**: No missing values, chronological order, 0 ≤ y ≤ 1

**REQ-DATA-2: Output Data Format**

**Benchmark Results JSON**:
```json
{
  "timestamp": "2025-12-05T14:30:00Z",
  "contract_id": "0x1234...",
  "train_size": 30,
  "test_size": 7,
  "models_benchmarked": 4,
  "results": [
    {
      "model": "TimeGPT",
      "mape": 0.082,
      "rmse": 0.045,
      "mae": 0.038,
      "rank": 2,
      "cost": "$0.05"
    },
    {
      "model": "AutoETS",
      "mape": 0.065,
      "rmse": 0.039,
      "mae": 0.032,
      "rank": 1,
      "cost": "$0.00"
    },
    {
      "model": "AutoTheta",
      "mape": 0.091,
      "rmse": 0.052,
      "mae": 0.043,
      "rank": 3,
      "cost": "$0.00"
    },
    {
      "model": "SeasonalNaive",
      "mape": 0.125,
      "rmse": 0.068,
      "mae": 0.055,
      "rank": 4,
      "cost": "$0.00"
    }
  ],
  "selected_model": "AutoETS",
  "confidence": 0.208,
  "confidence_level": "high",
  "reasoning": "AutoETS achieved lowest MAPE (6.5%) with 20.8% margin over TimeGPT. Data shows strong linear trend which AutoETS handles well."
}
```

### Performance Requirements

**REQ-PERF-1: Benchmarking Speed**
- **Target**: <60 seconds for 4 models
- **Max Acceptable**: <90 seconds
- **Breakdown**:
  - Data characteristics analysis: 5 sec
  - TimeGPT benchmark: 20 sec (API call)
  - StatsForecast benchmarks (3 models): 15 sec (parallel local execution)
  - Selection + report generation: 10 sec

**REQ-PERF-2: Accuracy Improvement**
- **Target**: 15-30% better MAPE vs default TimeGPT-only approach
- **Measurement**: Compare selected model MAPE to TimeGPT MAPE across 20 test contracts
- **Success**: At least 15% average improvement

### Quality Requirements

**REQ-QUAL-1: Description Quality**
- **Target Score**: 90%+
- **Must Include**:
  - [X] Action verbs: "Analyzes", "Benchmarks", "Selects", "Explains"
  - [X] Use cases: "optimizing accuracy, comparing models, reducing API costs"
  - [X] Trigger phrases: "select best model", "which model should I use", "optimize forecast accuracy"
  - [X] Domain keywords: "TimeGPT", "StatsForecast", "MAPE", "model selection", "benchmarking"

**REQ-QUAL-2: Model Selection Accuracy**
- **Target**: 85%+ confidence (clear winner in most cases)
- **Measurement**: (best_mape - second_best_mape) / best_mape > 0.15 in 85% of contracts
- **Edge Cases**: When models are within 5% MAPE, report "close call" and recommend cost-based tiebreaker

---

## 6. Non-Goals (Out of Scope)

**What This Skill Does NOT Do**:

1. **Custom Model Training**
   - **Rationale**: Uses pre-built models only (TimeGPT, AutoETS, AutoTheta, SeasonalNaive)
   - **Alternative**: Users can build custom models separately
   - **May be added in**: v2.0 (support for custom StatsForecast configurations)

2. **Hyperparameter Tuning**
   - **Rationale**: Uses default model parameters (auto-tuning where available)
   - **Alternative**: Power users can tune manually in Python
   - **Depends on**: User demand

3. **Ensemble Models**
   - **Rationale**: Single best model only (not weighted average of multiple)
   - **Alternative**: Advanced users can combine models manually
   - **May be added in**: v1.1 (simple averaging ensemble)

4. **Real-Time Model Reselection**
   - **Rationale**: One-time selection, not continuous monitoring
   - **Alternative**: Re-run skill periodically to revalidate
   - **Depends on**: User demand

---

## 7. Success Metrics

### Skill Activation Metrics

**Metric 1: Activation Accuracy**
- **Target**: 95%+
- **Test Phrases**: "select best model", "which model should I use", "optimize forecast accuracy"

**Metric 2: False Positive Rate**
- **Target**: <3%

### Quality Metrics

**Metric 3: Accuracy Improvement**
- **Target**: 15-30% better MAPE vs default TimeGPT
- **Measurement**: Benchmark 20 contracts, compare selected model MAPE to TimeGPT-only baseline

**Metric 4: Selection Confidence**
- **Target**: 85%+ contracts have high-confidence selection (>15% margin)
- **Measurement**: Count of contracts where (best_mape - second_best_mape) / best_mape > 0.15

### Usage Metrics

**Metric 5: Cost Savings**
- **Target**: $20-$50/month saved by using StatsForecast when optimal
- **Measurement**: Count of contracts where StatsForecast selected × $0.05/forecast

**Metric 6: User Trust**
- **Target**: 80%+ users accept automated model recommendation (don't override)
- **Measurement**: Override rate (--force-model usage)

### Performance Metrics

**Metric 7: Benchmarking Speed**
- **Target**: <60 seconds for 4 models
- **Measurement**: End-to-end execution time

---

## 8. User Experience Flow

### Typical Usage Flow

1. **User Intent**: Data scientist wants to optimize forecast accuracy for BTC $100k contract
2. **Trigger**: User says "Select the best forecasting model for this Polymarket contract"
3. **Skill Activation**: Claude recognizes need for `nixtla-model-selector` skill
4. **Skill Execution**:
   - Step 1: Analyze data characteristics (trend, seasonality, volatility)
   - Step 2: Benchmark 4 models (TimeGPT, AutoETS, AutoTheta, SeasonalNaive) on 7-day holdout
   - Step 3: Calculate metrics (MAPE, RMSE, MAE) for each model
   - Step 4: Select best model (AutoETS: 6.5% MAPE vs TimeGPT: 8.2% MAPE)
   - Step 5: Generate explainability report
   - Step 6: Use selected model (AutoETS) to generate final 14-day forecast
5. **Output Delivered**: Model selection report + final forecast
6. **User Action**: Reviews reasoning, trusts AutoETS recommendation, uses forecast for trading

### Example Scenario

**Input (time series data)**:
```csv
unique_id,ds,y
BTC_100k,2025-11-05,0.52
BTC_100k,2025-11-06,0.54
...
BTC_100k,2025-12-05,0.68
```

**Claude's Response**:
```
I'll analyze this data and select the optimal forecasting model using nixtla-model-selector.

[Skill executes 6-step workflow in ~55 seconds]

✓ Model selection complete!

**Selected Model**: AutoETS
**Confidence**: High (20.8% better than next-best model)
**Accuracy**: MAPE 6.5% (vs TimeGPT 8.2%)
**Cost Savings**: $0.05 (free StatsForecast vs paid TimeGPT)

**Why AutoETS?**
Your data shows a strong linear upward trend (+30% over 30 days) with low volatility.
AutoETS excels at trending data and automatically selects exponential smoothing parameters.

**Model Performance Comparison**:
1. AutoETS: 6.5% MAPE ✅ SELECTED
2. TimeGPT: 8.2% MAPE (20.8% worse)
3. AutoTheta: 9.1% MAPE (40% worse)
4. SeasonalNaive: 12.5% MAPE (92% worse)

See full report: reports/model_selection_2025-12-05.md
Final forecast using AutoETS: data/final_forecast.csv
```

**User Benefit**: Optimized accuracy (6.5% vs 8.2% MAPE = 20.8% improvement) + $0.05 saved, in 55 seconds vs 2-4 hours manual comparison

---

## 9. Integration Points

### External Systems

**System 1: Nixtla TimeGPT API** (Optional)
- **Purpose**: Benchmark TimeGPT model
- **Integration Type**: REST API (same as nixtla-polymarket-analyst)
- **Cost**: $0.05 per benchmark
- **Graceful Degradation**: Skip if quota exceeded (use StatsForecast only)

**System 2: StatsForecast** (Local)
- **Purpose**: Benchmark 3 models (AutoETS, AutoTheta, SeasonalNaive)
- **Integration Type**: Python library (local execution)
- **Cost**: Free

### Internal Dependencies

**Dependency 1: nixtla-polymarket-analyst**
- **What it provides**: Time series data (data/timeseries.csv)
- **Why needed**: Model selector operates on time series output

**Dependency 2: Python Libraries**
- **Libraries**: statsforecast, statsmodels, sklearn, pandas, numpy
- **Versions**:
  - statsforecast >= 1.7.0
  - statsmodels >= 0.14.0 (for autocorrelation)
  - scikit-learn >= 1.3.0 (for metrics)

---

## 10. Constraints & Assumptions

### Technical Constraints

1. **Minimum Data Length**: 30 days required for robust benchmarking (14 days train, 7 days test minimum)
2. **Model Subset**: 4 models only (TimeGPT + 3 StatsForecast models)—no custom models in v1.0
3. **Single Metric**: MAPE as primary metric (RMSE/MAE as secondary)

### Business Constraints

1. **API Costs**: $0.05 per TimeGPT benchmark (budget: <$10/month for 200 contracts)
2. **Timeline**: Ready for prediction markets vertical launch (Q1 2026)

### Assumptions

1. **Assumption 1: 7-day test split is sufficient**
   - **Risk if false**: Overfitting, unreliable selection
   - **Mitigation**: Make test_size configurable, recommend 7+ days

2. **Assumption 2: MAPE is best metric for prediction markets**
   - **Risk if false**: MAPE biased toward lower values (0-1 range)
   - **Mitigation**: Provide RMSE/MAE as alternatives, allow user to override

3. **Assumption 3: Users trust automated selection**
   - **Risk if false**: Users always override with --force-model
   - **Mitigation**: Strong explainability, confidence scores, benchmark transparency

---

## 11. Risk Assessment

### Technical Risks

**Risk 1: Model Selection Inconsistency**
- **Probability**: Medium (different train/test splits → different winners)
- **Impact**: Medium (user confusion about which model to use)
- **Mitigation**: Use time-series cross-validation for robustness, report confidence scores

**Risk 2: TimeGPT Quota Exhaustion**
- **Probability**: Medium (benchmarking uses API calls)
- **Impact**: Low (graceful degradation: skip TimeGPT, use StatsForecast only)
- **Mitigation**: Track quota, warn users, provide StatsForecast-only mode

**Risk 3: Insufficient Data Length**
- **Probability**: High (new contracts have <30 days history)
- **Impact**: Medium (unreliable benchmarking)
- **Mitigation**: Detect data length, warn users, require minimum 30 days

### User Experience Risks

**Risk 1: Users Don't Trust Automated Selection**
- **Probability**: Medium (skepticism of black-box recommendations)
- **Impact**: High (users ignore skill, manually benchmark anyway)
- **Mitigation**: Strong explainability, show benchmark results, allow overrides

**Risk 2: Close Calls (Models Within 5% MAPE)**
- **Probability**: High (many contracts will have similar model performance)
- **Impact**: Medium (users uncertain which model to trust)
- **Mitigation**: Report "close call", recommend cost-based tiebreaker, show all metrics

---

## 12. Open Questions

1. **Question**: Should we support ensemble models (average of top 2 models)?
   - **Options**: A) Single model only (v1.0), B) Simple ensemble (v1.1)
   - **Recommendation**: A (single model for v1.0, ensemble in v1.1 if demand exists)

2. **Question**: What should default test size be (7, 14, or 30 days)?
   - **Options**: 7 days (faster), 14 days (balanced), 30 days (robust)
   - **Recommendation**: 7 days default (user-overridable with --test-days)

3. **Question**: Should we benchmark on multiple test splits (time-series CV)?
   - **Options**: A) Single split (faster), B) Cross-validation (more robust)
   - **Recommendation**: A for v1.0 (B in v1.1 for power users)

**Recommended Decisions**:
1. Single model only for v1.0
2. 7-day default test size
3. Single split for v1.0 (CV in v1.1)

---

## 13. Appendix: Examples

### Example 1: Clear Winner (AutoETS)

**Data**: Strong upward trend (crypto contract)

**Benchmark Results**:
- AutoETS: 6.5% MAPE ✅ SELECTED (handles trend well)
- TimeGPT: 8.2% MAPE (20.8% worse)
- AutoTheta: 9.1% MAPE (40% worse)
- SeasonalNaive: 12.5% MAPE (92% worse)

**Selection**: AutoETS (high confidence: 20.8% margin)
**Reasoning**: "Strong linear trend detected. AutoETS excels at trending data."

### Example 2: Close Call (TimeGPT vs AutoETS)

**Data**: Moderate trend, some seasonality

**Benchmark Results**:
- AutoETS: 7.2% MAPE (free)
- TimeGPT: 7.5% MAPE ($0.05)
- AutoTheta: 8.9% MAPE
- SeasonalNaive: 11.2% MAPE

**Selection**: AutoETS (medium confidence: 4% margin, cost-based tiebreaker)
**Reasoning**: "AutoETS and TimeGPT perform similarly (4% difference). Recommending free AutoETS to save $0.05."

### Example 3: Insufficient Data

**Data**: Only 15 days of history

**Output**:
```
ERROR: Insufficient data for robust model selection.
- Current: 15 days
- Minimum required: 30 days (23 train, 7 test)

Recommendation: Wait for more data or use default TimeGPT model.
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
