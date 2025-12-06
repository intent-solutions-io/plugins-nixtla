# Claude Skill PRD: Nixtla Forecast Validator

**Template Version**: 1.0.0
**Based On**: [Anthropic Skills Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)
**Purpose**: Product Requirements Document for Claude Skills
**Status**: Planned

---

## Document Control

| Field | Value |
|-------|-------|
| **Skill Name** | nixtla-forecast-validator |
| **Skill Type** | [X] Mode Skill [ ] Utility Skill |
| **Domain** | Prediction Markets + Time Series Forecasting + Quality Assurance |
| **Target Users** | Data Scientists, Portfolio Managers, Quality Engineers |
| **Priority** | [ ] Critical [X] High [ ] Medium [ ] Low |
| **Status** | [X] Planned [ ] In Development [ ] Complete |
| **Owner** | Intent Solutions |
| **Last Updated** | 2025-12-05 |

---

## 1. Executive Summary

**One-sentence description**: Transform Claude into a forecast quality monitor that compares predictions against actual outcomes, calculates accuracy metrics (MAPE, RMSE, coverage), detects degradation over time, triggers retraining alerts, and generates validation reports with actionable recommendations.

**Value Proposition**: Prevents costly trading decisions based on degraded forecasts by detecting accuracy decay early (20-30% MAPE increase = warning), automating quality monitoring that would otherwise require 5-10 hours/week of manual validation, and providing clear retraining triggers.

**Key Metrics**:
- Target activation accuracy: 95%
- Expected usage frequency: Daily (automated monitoring) or on-demand (manual validation)
- Degradation detection: Alert when MAPE increases >15% from baseline
- Time savings: 5-10 hours/week vs manual validation
- False alarm rate: <10% (don't cry wolf on normal variance)

---

## 2. Problem Statement

### Current State (Without This Skill)

**Pain Points**:
1. **No validation feedback loop**: Forecasts are generated, used for trading, but never validated against actual outcomes
2. **Accuracy decay invisible**: Models degrade over time (market regime changes, new patterns), but users don't notice until major losses occur
3. **Manual validation tedious**: Collecting actuals, calculating metrics, comparing to baseline takes 5-10 hours/week
4. **No retraining triggers**: Users don't know when to retrain models—rely on gut feeling or fixed schedules (quarterly, annually)
5. **Trust erosion**: After repeated inaccurate forecasts, users lose confidence but have no systematic way to diagnose issues

**Current Workarounds**:
- Manually compare forecasts to actuals in spreadsheets (5-10 hours/week)
- Retrain models on fixed schedule (every 3-6 months) regardless of actual performance
- Ignore accuracy decay until catastrophic failure (major losing trade)

**Impact of Problem**:
- Time wasted: 5-10 hours/week on manual validation
- Financial losses: $10k-$50k per degraded forecast (user trades on inaccurate predictions)
- User frustration: Critical (forecasts feel like "black boxes" with no accountability)
- Model staleness: 3-6 month lags between retraining (even when earlier retraining needed)

### Desired State (With This Skill)

**Transformation**:
- From: 5-10 hours/week manual validation with 3-6 month retraining lags
- To: 60-second automated validation with real-time degradation alerts (99% time reduction, 10x faster retraining triggers)

**Expected Benefits**:
1. **Early degradation detection**: Alert when MAPE increases >15% (before major losses)
2. **99% faster validation**: 60 seconds vs 5-10 hours/week manual work
3. **Automated retraining triggers**: Know exactly when to retrain (data-driven, not guesswork)
4. **Trust restoration**: Transparent accuracy tracking builds confidence in forecasts
5. **Continuous improvement**: Monthly validation → model refinement cycle

---

## 3. Target Users

### Primary Users

**User Persona 1: Data Scientist (Model Owner)**
- **Background**: Builds and maintains forecasting models, responsible for accuracy, experienced with validation metrics
- **Goals**: Monitor model health, detect degradation early, know when to retrain, maintain >90% accuracy
- **Pain Points**: Manual validation is tedious, hard to detect gradual decay, no systematic retraining triggers
- **Use Frequency**: Daily (automated monitoring) + on-demand (after major market events)
- **Technical Skills**: Expert in ML metrics (MAPE, RMSE, coverage), proficient in Python, understands statistical testing
- **Value**: Model performance insights, early warning system, reproducible validation methodology

**User Persona 2: Portfolio Manager (Model Consumer)**
- **Background**: Uses forecasts for trading decisions, needs confidence in predictions, less technical but data-savvy
- **Goals**: Trust forecasts are accurate, know when to stop using degraded models, understand validation results
- **Pain Points**: Don't know if forecasts are reliable, rely on data scientists for validation, no visibility into accuracy
- **Use Frequency**: Weekly (review validation reports)
- **Technical Skills**: Strong trading knowledge, basic stats understanding, limited coding
- **Annual Income Impact**: $50k-$200k potential (avoid losses from degraded forecasts)

### Secondary Users

**Quality Engineers**: Systematically test model performance across contracts
**Academic Researchers**: Study forecast accuracy evolution over time

---

## 4. User Stories

### Critical User Stories (Must Have)

1. **As a** data scientist,
   **I want** to automatically validate forecasts against actual outcomes and calculate accuracy metrics (MAPE, RMSE, MAE),
   **So that** I can monitor model health without spending 5-10 hours/week on manual validation.

   **Acceptance Criteria**:
   - [ ] Accepts forecast file (CSV) + actuals file (CSV)
   - [ ] Aligns forecasts with actuals by date
   - [ ] Calculates 4 metrics: MAPE, RMSE, MAE, coverage (% within confidence intervals)
   - [ ] Compares to baseline (initial model performance)
   - [ ] Saves to `data/validation_results.json`
   - [ ] Executes in <60 seconds

2. **As a** data scientist,
   **I want** to detect forecast degradation automatically (MAPE increase >15% from baseline),
   **So that** I can retrain models early before major losses occur.

   **Acceptance Criteria**:
   - [ ] Loads baseline metrics (from initial validation or config)
   - [ ] Compares current MAPE to baseline MAPE
   - [ ] Degradation threshold: >15% increase (configurable)
   - [ ] Alert levels: Warning (15-30% increase), Critical (>30% increase)
   - [ ] Triggers: "RETRAIN RECOMMENDED" when threshold exceeded
   - [ ] Saves alerts to `data/degradation_alerts.json`

3. **As a** portfolio manager,
   **I want** clear validation reports explaining accuracy status and recommendations,
   **So that** I can decide whether to trust forecasts or wait for retraining.

   **Acceptance Criteria**:
   - [ ] Executive summary: Current MAPE, baseline MAPE, degradation status
   - [ ] Metrics table: MAPE, RMSE, MAE, coverage (current vs baseline)
   - [ ] Degradation analysis: Trend over time (if historical data available)
   - [ ] Recommendations: "PASS" (use forecast), "RETRAIN" (degraded), "INVESTIGATE" (borderline)
   - [ ] Saves to `reports/validation_report_YYYY-MM-DD.md`

### High-Priority User Stories (Should Have)

4. **As a** data scientist,
   **I want** to validate confidence interval coverage (% of actuals within 80%/95% CI),
   **So that** I can assess calibration (not just point forecast accuracy).

   **Acceptance Criteria**:
   - [ ] For each actual value, check if it falls within 80%/95% CI
   - [ ] Calculate coverage: (count in CI) / (total actuals)
   - [ ] Target: 80% CI should contain ~80% of actuals, 95% CI should contain ~95%
   - [ ] Alert if coverage <70% or >90% (miscalibrated intervals)
   - [ ] Display in validation report

5. **As a** power user,
   **I want** to track validation metrics over time (monthly trend),
   **So that** I can see gradual degradation patterns.

   **Acceptance Criteria**:
   - [ ] Store validation results in historical log (append-only)
   - [ ] Load last 6 months of validations
   - [ ] Generate trend chart (ASCII or data for plotting)
   - [ ] Detect trends: improving, stable, degrading
   - [ ] Saves to `data/validation_history.json`

### Nice-to-Have User Stories (Could Have)

6. **As a** researcher,
   **I want** to compare multiple models' validation results side-by-side,
   **So that** I can identify which model degrades fastest.

7. **As a** automation engineer,
   **I want** to integrate validation into CI/CD pipeline (automated nightly runs),
   **So that** model health is continuously monitored.

---

## 5. Functional Requirements

### Core Capabilities (Must Have)

**REQ-1: Forecast-Actual Alignment**
- **Description**: Match forecast dates with actual outcome dates, handle missing data gracefully
- **Rationale**: Forecasts and actuals may have different date ranges—need robust alignment
- **Acceptance Criteria**:
  - [ ] Accepts forecast.csv (unique_id, ds, forecast, CI_lo, CI_hi)
  - [ ] Accepts actuals.csv (unique_id, ds, actual)
  - [ ] Inner join on (unique_id, ds) to align
  - [ ] Logs: "X forecasts aligned with actuals (Y forecasts unmatched)"
  - [ ] Validates: aligned_count >= 7 (minimum for robust metrics)
  - [ ] Saves to `data/aligned_data.csv`
- **Dependencies**: pandas for join operations

**REQ-2: Accuracy Metrics Calculation**
- **Description**: Calculate MAPE, RMSE, MAE on aligned forecast-actual pairs
- **Rationale**: Standard forecasting metrics for quantitative validation
- **Acceptance Criteria**:
  - [ ] MAPE = mean(abs((actual - forecast) / actual)) × 100
  - [ ] RMSE = sqrt(mean((actual - forecast)²))
  - [ ] MAE = mean(abs(actual - forecast))
  - [ ] Handle edge cases: actual = 0 (skip MAPE, use RMSE/MAE)
  - [ ] Saves to `data/validation_results.json`
- **Dependencies**: numpy, sklearn.metrics

**REQ-3: Confidence Interval Coverage Validation**
- **Description**: Check if actuals fall within 80%/95% confidence intervals, calculate coverage %
- **Rationale**: Confidence intervals should be calibrated (80% CI → 80% coverage)
- **Acceptance Criteria**:
  - [ ] For each actual: check if CI_lo_80 ≤ actual ≤ CI_hi_80
  - [ ] Coverage_80 = (count in 80% CI) / (total actuals)
  - [ ] Coverage_95 = (count in 95% CI) / (total actuals)
  - [ ] Target: Coverage_80 ≈ 0.80 ± 0.10, Coverage_95 ≈ 0.95 ± 0.05
  - [ ] Alert if outside target ranges (miscalibration)
  - [ ] Saves to `data/validation_results.json`

**REQ-4: Degradation Detection**
- **Description**: Compare current MAPE to baseline, detect significant increases, trigger alerts
- **Rationale**: Core value proposition—know when model has degraded
- **Acceptance Criteria**:
  - [ ] Load baseline MAPE (from initial validation or config file)
  - [ ] Calculate degradation: (current_MAPE - baseline_MAPE) / baseline_MAPE
  - [ ] Thresholds:
    - [ ] OK: degradation ≤ 15% (green)
    - [ ] WARNING: degradation 15-30% (yellow)
    - [ ] CRITICAL: degradation > 30% (red)
  - [ ] Generate alert: "RETRAIN RECOMMENDED" if WARNING/CRITICAL
  - [ ] Saves to `data/degradation_alerts.json`
- **Dependencies**: Baseline metrics (from initial validation)

**REQ-5: Validation Report Generation**
- **Description**: Generate markdown report with metrics, degradation status, recommendations
- **Rationale**: Users need human-readable summary, not just JSON metrics
- **Acceptance Criteria**:
  - [ ] Section 1: Executive summary (current MAPE, degradation status)
  - [ ] Section 2: Metrics table (MAPE, RMSE, MAE, coverage)
  - [ ] Section 3: Degradation analysis (trend, alert level)
  - [ ] Section 4: Recommendations (PASS/RETRAIN/INVESTIGATE)
  - [ ] Section 5: Historical trend (if data available)
  - [ ] Saves to `reports/validation_report_YYYY-MM-DD.md`
- **Dependencies**: Markdown template

### Integration Requirements

**REQ-API-1: No External APIs**
- **Purpose**: Validation is fully local (no API calls)
- **Dependencies**: Python libraries only (pandas, numpy, sklearn)
- **Cost**: $0.00 (free)

### Data Requirements

**REQ-DATA-1: Input Data Formats**

**Forecast File (CSV)**:
```csv
unique_id,ds,forecast,forecast_lo_80,forecast_hi_80,forecast_lo_95,forecast_hi_95
BTC_100k,2025-12-06,0.68,0.65,0.71,0.63,0.73
BTC_100k,2025-12-07,0.69,0.66,0.72,0.64,0.74
...
```

**Actuals File (CSV)**:
```csv
unique_id,ds,actual
BTC_100k,2025-12-06,0.67
BTC_100k,2025-12-07,0.70
...
```

**Baseline Config (JSON)**:
```json
{
  "baseline_mape": 0.082,
  "baseline_rmse": 0.045,
  "baseline_mae": 0.038,
  "baseline_coverage_80": 0.78,
  "baseline_coverage_95": 0.94,
  "baseline_date": "2025-11-01",
  "baseline_description": "Initial model validation on M4 benchmark"
}
```

**REQ-DATA-2: Output Data Formats**

**Validation Results (JSON)**:
```json
{
  "timestamp": "2025-12-05T14:30:00Z",
  "contract_id": "0x1234...",
  "aligned_count": 14,
  "unmatched_forecasts": 0,
  "metrics": {
    "mape": 0.095,
    "rmse": 0.052,
    "mae": 0.043,
    "coverage_80": 0.71,
    "coverage_95": 0.93
  },
  "baseline": {
    "mape": 0.082,
    "rmse": 0.045,
    "mae": 0.038,
    "coverage_80": 0.78,
    "coverage_95": 0.94
  },
  "degradation": {
    "mape_pct_increase": 15.9,
    "rmse_pct_increase": 15.6,
    "mae_pct_increase": 13.2,
    "alert_level": "WARNING",
    "recommendation": "RETRAIN RECOMMENDED"
  }
}
```

**Degradation Alerts (JSON)**:
```json
{
  "timestamp": "2025-12-05T14:30:00Z",
  "contract_id": "0x1234...",
  "alerts": [
    {
      "metric": "MAPE",
      "current": 0.095,
      "baseline": 0.082,
      "degradation_pct": 15.9,
      "alert_level": "WARNING",
      "message": "MAPE increased 15.9% from baseline (8.2% → 9.5%). RETRAIN RECOMMENDED."
    },
    {
      "metric": "coverage_80",
      "current": 0.71,
      "baseline": 0.78,
      "degradation_pct": -9.0,
      "alert_level": "WARNING",
      "message": "80% CI coverage decreased to 71% (target: 80%). Confidence intervals may be miscalibrated."
    }
  ]
}
```

### Performance Requirements

**REQ-PERF-1: Validation Speed**
- **Target**: <60 seconds for 14-day forecast validation
- **Max Acceptable**: <90 seconds
- **Breakdown**:
  - Forecast-actual alignment: 2 sec
  - Metrics calculation: 5 sec
  - Degradation detection: 3 sec
  - Report generation: 10 sec

**REQ-PERF-2: Accuracy Detection Sensitivity**
- **Target**: Detect degradation with 90%+ sensitivity (true positive rate)
- **False Alarm Rate**: <10% (don't trigger on normal variance)

### Quality Requirements

**REQ-QUAL-1: Description Quality**
- **Target Score**: 90%+
- **Must Include**:
  - [X] Action verbs: "Validates", "Compares", "Detects", "Calculates", "Alerts"
  - [X] Use cases: "monitoring forecast quality, detecting degradation, triggering retraining"
  - [X] Trigger phrases: "validate forecast", "check accuracy", "has model degraded"
  - [X] Domain keywords: "MAPE", "RMSE", "coverage", "degradation", "retraining"

**REQ-QUAL-2: Alert Precision**
- **Target**: 90%+ of alerts are actionable (true degradation, not noise)
- **Measurement**: Manual review of alerts over 1 month

---

## 6. Non-Goals (Out of Scope)

**What This Skill Does NOT Do**:

1. **Automatic Model Retraining**
   - **Rationale**: Detects need for retraining, but doesn't execute it (user decides)
   - **Alternative**: Stack with model retraining workflow
   - **May be added in**: v2.0 (auto-retrain option)

2. **Real-Time Validation**
   - **Rationale**: On-demand or scheduled (daily), not streaming
   - **Alternative**: Run via cron job for quasi-real-time monitoring
   - **Depends on**: User demand

3. **Multi-Model Comparison**
   - **Rationale**: Validates single forecast at a time
   - **Alternative**: Run skill multiple times for different models
   - **May be added in**: v1.1 (batch validation)

4. **Root Cause Analysis**
   - **Rationale**: Detects degradation, doesn't diagnose why (data shift, model drift, etc.)
   - **Alternative**: Manual investigation by data scientists
   - **Depends on**: Advanced diagnostics (v2.0)

---

## 7. Success Metrics

### Skill Activation Metrics

**Metric 1: Activation Accuracy**
- **Target**: 95%+
- **Test Phrases**: "validate forecast", "check forecast accuracy", "has model degraded"

**Metric 2: False Positive Rate**
- **Target**: <3%

### Quality Metrics

**Metric 3: Degradation Detection Sensitivity**
- **Target**: 90%+ (detect 9/10 true degradations)
- **Measurement**: Simulate degraded forecasts (add 20% error), verify alerts triggered

**Metric 4: False Alarm Rate**
- **Target**: <10% (at most 1/10 alerts are false positives)
- **Measurement**: Manual review of alerts on stable models

### Usage Metrics

**Metric 5: Adoption Rate**
- **Target**: 70% of data scientists use validation within first month
- **Measurement**: Skill invocation logs

**Metric 6: Retraining Trigger Accuracy**
- **Target**: 80%+ of triggered retrainings improve accuracy
- **Measurement**: Compare post-retrain MAPE to pre-retrain MAPE

### Performance Metrics

**Metric 7: Time Savings**
- **Target**: 99% faster than manual validation (60 sec vs 5-10 hours/week)
- **Measurement**: User feedback surveys

---

## 8. User Experience Flow

### Typical Usage Flow

1. **User Intent**: Data scientist wants to validate last week's forecasts
2. **Trigger**: User says "Validate my BTC $100k forecast from last week"
3. **Skill Activation**: Claude recognizes need for `nixtla-forecast-validator` skill
4. **Skill Execution**:
   - Step 1: Load forecast file (14-day predictions from Dec 6-19)
   - Step 2: Load actuals file (actual outcomes Dec 6-19)
   - Step 3: Align forecasts with actuals (14 dates matched)
   - Step 4: Calculate metrics (MAPE: 9.5% vs baseline 8.2%)
   - Step 5: Detect degradation (15.9% increase → WARNING)
   - Step 6: Generate validation report
5. **Output Delivered**: Validation report + degradation alert
6. **User Action**: Reviews report, schedules model retraining for next week

### Example Scenario

**Input (forecast.csv + actuals.csv)**:
- Forecast: 14-day predictions (Dec 6-19, MAPE expected: 8%)
- Actuals: Real outcomes (Dec 6-19, actual MAPE: 9.5%)

**Claude's Response**:
```
I'll validate your BTC $100k forecast using nixtla-forecast-validator.

[Skill executes 6-step workflow in ~45 seconds]

⚠️ DEGRADATION DETECTED

**Current Performance**: MAPE 9.5%
**Baseline Performance**: MAPE 8.2%
**Degradation**: +15.9% (WARNING level)

**Recommendation**: RETRAIN RECOMMENDED
Your model's accuracy has decreased by 15.9%. This exceeds the 15% degradation threshold.
Suggest retraining on latest data within next week.

**Detailed Metrics**:
- MAPE: 9.5% (baseline: 8.2%, +15.9%)
- RMSE: 0.052 (baseline: 0.045, +15.6%)
- MAE: 0.043 (baseline: 0.038, +13.2%)
- 80% CI Coverage: 71% (baseline: 78%, -9.0%) ⚠️ Miscalibrated

**Actuals Alignment**: 14/14 forecasts matched with actuals (100%)

See full report: reports/validation_report_2025-12-05.md
See alerts: data/degradation_alerts.json
```

**User Benefit**: Detected degradation early (15.9% increase) before major losses, in 45 seconds vs 5-10 hours manual validation

---

## 9. Integration Points

### External Systems

**System 1: No External APIs**
- **Purpose**: Fully local validation
- **Cost**: $0.00

### Internal Dependencies

**Dependency 1: Forecast Output**
- **What it provides**: forecast.csv from nixtla-polymarket-analyst or nixtla-model-selector
- **Why needed**: Validation requires forecasts to compare against actuals

**Dependency 2: Actual Outcomes**
- **What it provides**: User-provided actuals.csv (from Polymarket contract resolution)
- **Why needed**: Ground truth for validation

**Dependency 3: Baseline Metrics**
- **What it provides**: Initial model performance (baseline_config.json)
- **Why needed**: Degradation detection requires baseline for comparison

---

## 10. Constraints & Assumptions

### Technical Constraints

1. **Minimum Data**: 7 forecast-actual pairs required for robust metrics
2. **Baseline Required**: Must have baseline metrics (from initial validation)
3. **Manual Actuals Collection**: Users must provide actuals (not auto-fetched from Polymarket)

### Business Constraints

1. **No API Costs**: Free skill (local execution only)
2. **Timeline**: Ready for prediction markets vertical launch (Q1 2026)

### Assumptions

1. **Assumption 1: Users can collect actuals easily**
   - **Risk if false**: Manual actuals collection is bottleneck
   - **Mitigation**: Document Polymarket API for actuals fetching (future automation)

2. **Assumption 2: 15% degradation threshold is appropriate**
   - **Risk if false**: Too sensitive (many false alarms) or too insensitive (miss degradations)
   - **Mitigation**: Make threshold configurable (--degradation-threshold)

3. **Assumption 3: Users understand MAPE/RMSE/MAE metrics**
   - **Risk if false**: Reports are confusing
   - **Mitigation**: Include metric explanations in report template

---

## 11. Risk Assessment

### Technical Risks

**Risk 1: Insufficient Actual Data**
- **Probability**: High (contracts may not resolve yet)
- **Impact**: Medium (can't validate if no actuals)
- **Mitigation**: Check aligned_count >= 7, warn if insufficient

**Risk 2: Baseline Metrics Unavailable**
- **Probability**: Medium (first-time users have no baseline)
- **Impact**: High (degradation detection impossible)
- **Mitigation**: Allow validation without baseline (report metrics only, skip degradation detection)

**Risk 3: False Alarms (Normal Variance Misinterpreted as Degradation)**
- **Probability**: Medium (MAPE fluctuates naturally)
- **Impact**: Medium (user fatigue, ignored alerts)
- **Mitigation**: Use statistical tests (t-test), require sustained degradation (2+ consecutive validations)

### User Experience Risks

**Risk 1: Users Ignore Degradation Alerts**
- **Probability**: Medium (alert fatigue)
- **Impact**: High (defeats purpose of skill)
- **Mitigation**: Clear recommendations, show impact ($X potential losses), make retraining easy

**Risk 2: Manual Actuals Collection is Tedious**
- **Probability**: High (no automation in v1.0)
- **Impact**: Medium (users skip validation)
- **Mitigation**: Provide Polymarket API guide for actuals fetching (v2.0: auto-fetch)

---

## 12. Open Questions

1. **Question**: Should we auto-fetch actuals from Polymarket API?
   - **Options**: A) Manual user-provided CSV (v1.0), B) Auto-fetch (v2.0)
   - **Recommendation**: A (manual for v1.0, auto-fetch in v2.0 to reduce friction)

2. **Question**: What should degradation threshold default be (10%, 15%, 20%)?
   - **Options**: 10% (sensitive), 15% (balanced), 20% (conservative)
   - **Recommendation**: 15% default (user-overridable)

3. **Question**: Should we support batch validation (multiple forecasts at once)?
   - **Options**: A) Single forecast (v1.0), B) Batch (v1.1)
   - **Recommendation**: A (single for v1.0, batch in v1.1)

**Recommended Decisions**:
1. Manual actuals CSV for v1.0
2. 15% default degradation threshold
3. Single forecast validation for v1.0

---

## 13. Appendix: Examples

### Example 1: PASS (No Degradation)

**Metrics**:
- Current MAPE: 8.5%
- Baseline MAPE: 8.2%
- Degradation: +3.7% (within 15% threshold)

**Output**:
```
✅ VALIDATION PASSED

Current MAPE (8.5%) is within 15% of baseline (8.2%).
Model performance is stable. Continue using forecasts.
```

### Example 2: WARNING (Moderate Degradation)

**Metrics**:
- Current MAPE: 9.5%
- Baseline MAPE: 8.2%
- Degradation: +15.9%

**Output**:
```
⚠️ DEGRADATION DETECTED (WARNING)

Current MAPE (9.5%) increased 15.9% from baseline (8.2%).
RECOMMENDATION: RETRAIN RECOMMENDED within next 1-2 weeks.
```

### Example 3: CRITICAL (Severe Degradation)

**Metrics**:
- Current MAPE: 11.2%
- Baseline MAPE: 8.2%
- Degradation: +36.6%

**Output**:
```
🚨 CRITICAL DEGRADATION

Current MAPE (11.2%) increased 36.6% from baseline (8.2%).
RECOMMENDATION: STOP USING FORECASTS. RETRAIN IMMEDIATELY.
Potential losses: $X per trade based on this degraded accuracy.
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
