# Nixtla Usage Optimization Report

**Generated**: {date}
**Repository**: {repo_name}
**Audited By**: nixtla-usage-optimizer skill

---

## Executive Summary

**Current State**:
- TimeGPT usage: {count} locations found
- StatsForecast usage: {count} locations found
- MLForecast usage: {count} locations found
- Total files analyzed: {count}

**Key Findings**:
1. {finding_1}
2. {finding_2}
3. {finding_3}

**Estimated Savings Potential**: {qualitative_estimate}

---

## Usage Analysis

### 1. TimeGPT Usage Patterns

#### High-Volume Areas:
- `{file_path}`: {context} ({frequency})
- `{file_path}`: {context} ({frequency})

**Observations**:
- {observation_1}
- {observation_2}

#### Appropriate Use Cases:
✅ `experiments/timegpt_vs_baselines.py`:
   - Complex multi-seasonal retail data
   - Long-term forecasts (30 days)
   - High business impact (demand planning)
   - **Recommendation**: Keep using TimeGPT

#### Over-Use Candidates:
⚠️  `scripts/daily_simple_forecast.py`:
   - Simple weekly seasonality
   - Short-term forecasts (7 days)
   - Low business impact (internal reporting)
   - **Recommendation**: Consider StatsForecast AutoETS

### 2. Baseline Library Usage

#### Current Baselines:
- AutoETS: {count} usages
- AutoARIMA: {count} usages
- SeasonalNaive: {count} usages

**Observations**:
- {observation_1}
- {observation_2}

#### Missed Opportunities:
🔍 `pipelines/production_forecast.py`:
   - Currently uses basic seasonal naive
   - Could benefit from AutoETS or TimeGPT
   - **Recommendation**: Upgrade to TimeGPT if accuracy critical, else AutoETS

### 3. Routing and Guardrails

#### Current Routing Logic:
{code_block_showing_existing_routing_if_any}

**Gaps Identified**:
- {gap_1}
- {gap_2}

---

## Recommendations

### 1. Implement Routing Strategy

**Proposed Decision Tree**:

```python
def choose_forecasting_model(
    data_complexity: str,
    horizon_days: int,
    business_impact: str,
    budget_priority: str
):
    """
    Smart routing based on characteristics

    data_complexity: "simple" | "medium" | "complex"
    horizon_days: int (forecast horizon)
    business_impact: "low" | "medium" | "high"
    budget_priority: "cost" | "balanced" | "accuracy"
    """

    # High-value cases: Use TimeGPT
    if business_impact == "high" and budget_priority == "accuracy":
        return "TimeGPT"

    # Complex patterns: Use TimeGPT or MLForecast
    if data_complexity == "complex":
        if horizon_days > 30:
            return "TimeGPT"
        else:
            return "MLForecast"

    # Simple patterns, cost-sensitive: Use StatsForecast
    if data_complexity == "simple" and budget_priority == "cost":
        return "StatsForecast-AutoETS"

    # Default balanced option
    if budget_priority == "balanced":
        return "MLForecast"

    return "StatsForecast-AutoETS"
```

**Implementation Steps**:
1. Add routing function to `forecasting/routing.py`
2. Update pipelines to call routing function
3. Log routing decisions for audit
4. Monitor accuracy by routing tier

### 2. Add Fallback Mechanisms

**Current Gap**: No fallback when TimeGPT fails

**Recommended Fallback Chain**:
```
TimeGPT → MLForecast → StatsForecast AutoETS → SeasonalNaive
```

**Implementation**:
```python
def forecast_with_fallback(df, horizon, freq):
    """Robust forecasting with fallback chain"""

    try:
        # Try TimeGPT first
        if NIXTLA_API_KEY:
            from nixtla import NixtlaClient
            client = NixtlaClient(api_key=NIXTLA_API_KEY)
            return client.forecast(df=df, h=horizon, freq=freq)
    except Exception as e:
        logging.warning(f"TimeGPT failed: {e}, falling back")

    try:
        # Fallback to MLForecast
        from mlforecast import MLForecast
        from sklearn.ensemble import RandomForestRegressor
        mlf = MLForecast(models=[RandomForestRegressor()], freq=freq)
        mlf.fit(df)
        return mlf.predict(h=horizon)
    except Exception as e:
        logging.warning(f"MLForecast failed: {e}, falling back")

    # Final fallback to StatsForecast
    from statsforecast import StatsForecast
    from statsforecast.models import AutoETS
    sf = StatsForecast(models=[AutoETS()], freq=freq)
    sf.fit(df)
    return sf.predict(h=horizon)
```

### 3. Cost Optimization Opportunities

#### Opportunity 1: Batch TimeGPT Calls
**Location**: `{file_path}`
**Current**: Individual forecast calls per series
**Recommended**: Batch multiple series in single API call
**Estimated Savings**: ~40% API cost reduction

```python
# Before (inefficient)
for series_id in unique_ids:
    series_df = df[df['unique_id'] == series_id]
    forecast = client.forecast(df=series_df, h=horizon)

# After (batched)
forecast = client.forecast(df=df, h=horizon)  # All series at once
```

#### Opportunity 2: Replace TimeGPT in Low-Impact Areas
**Locations**: {list_of_files}
**Current**: TimeGPT for simple daily forecasts
**Recommended**: StatsForecast AutoETS
**Estimated Savings**: ~100% on these calls (free baseline)

#### Opportunity 3: Add TimeGPT Where Missing
**Location**: `{file_path}`
**Current**: Basic SeasonalNaive
**Impact**: High-value revenue forecasts
**Recommended**: Upgrade to TimeGPT
**Estimated Value**: Improved accuracy could justify costs

---

## ROI Assessment

### Cost-Accuracy Trade-offs

**Current Approach**: {description}

**Optimized Approach**:
- High-value forecasts: TimeGPT (~{percentage}% of calls)
- Medium complexity: MLForecast (~{percentage}% of calls)
- Low-value/simple: StatsForecast (~{percentage}% of calls)

### Estimated Impact

**Cost Savings** (qualitative):
- Batching improvements: Moderate savings
- Routing to baselines: High savings on low-impact forecasts
- Total estimated reduction: 30-50% API costs

**Accuracy Impact**:
- Critical forecasts: Maintained or improved (TimeGPT)
- Medium forecasts: Comparable (MLForecast)
- Low-impact forecasts: Acceptable degradation (if any)

**Net Value**: Significant cost reduction while protecting critical forecast quality

---

## Implementation Checklist

- [ ] Review routing decision tree with stakeholders
- [ ] Implement routing function in `forecasting/routing.py`
- [ ] Add fallback chain to all production pipelines
- [ ] Batch TimeGPT calls where possible
- [ ] Replace TimeGPT in identified low-impact areas
- [ ] Add TimeGPT to identified high-impact areas
- [ ] Add routing decision logging
- [ ] Monitor accuracy by routing tier (monthly)
- [ ] Track cost savings (compare pre/post optimization)

---

## Appendix: Detailed Usage Inventory

### TimeGPT Calls Inventory
{detailed_list_of_all_timegpt_usage_with_context}

### Baseline Library Inventory
{detailed_list_of_all_baseline_usage_with_context}

### Configuration Files Analyzed
{list_of_config_files_with_key_parameters}

---

**Next Steps**:
1. Review this report with team
2. Prioritize recommendations
3. Implement routing strategy
4. Monitor results over 30 days
5. Re-run audit to verify improvements

---

**Generated by**: nixtla-usage-optimizer skill
**Contact**: For questions about this audit, consult Nixtla documentation or team
