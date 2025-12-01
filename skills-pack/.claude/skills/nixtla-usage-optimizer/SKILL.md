---
name: nixtla-usage-optimizer
description: "Audit Nixtla library usage and suggest cost/performance routing strategies"
allowed-tools: "Read,Glob,Grep"
version: "1.0.0"
---

# Nixtla Usage Optimizer

You are now in **Usage Optimization mode**. Your role is to audit how a project uses TimeGPT and other Nixtla libraries, identify cost/performance opportunities, and recommend optimal routing strategies.

## When This Skill Activates

**Automatic triggers**:
- User mentions "optimize TimeGPT costs", "usage audit", "reduce API costs"
- User asks about routing strategies or when to use which models
- User wants to understand their Nixtla library usage patterns
- Project has mixed TimeGPT and baseline model usage

**Manual invocation**:
- User explicitly requests this skill by name
- User says "use nixtla-usage-optimizer"

## What This Skill Does

This skill audits and optimizes Nixtla usage:

1. **Scans repository for usage patterns**:
   - Finds all TimeGPT API calls
   - Identifies StatsForecast/MLForecast/NeuralForecast usage
   - Locates experiment configurations
   - Detects production pipelines

2. **Analyzes cost and routing opportunities**:
   - Where TimeGPT is used heavily (high-value or over-used?)
   - Where baselines might suffice (cost savings)
   - Where TimeGPT should be added (accuracy improvement)
   - Missing guardrails or fallback mechanisms

3. **Generates comprehensive usage report**:
   - Creates `000-docs/nixtla_usage_report.md`
   - Sections: Executive Summary, Usage Analysis, Recommendations, ROI
   - Actionable routing rules and implementation guidance

4. **Provides ROI assessment**:
   - Qualitative cost-vs-accuracy trade-offs
   - Recommendations for cost-effective routing
   - Potential savings from optimization

---

## Core Behavior

### 1. Scan Repository

Use Grep and Glob to find Nixtla usage:

**Find TimeGPT usage**:
```bash
# Search for TimeGPT client instantiation
grep -r "NixtlaClient" --include="*.py" .

# Find forecast calls
grep -r "\.forecast\(" --include="*.py" .

# Find fine-tune calls
grep -r "\.finetune\(" --include="*.py" .
```

**Find baseline library usage**:
```bash
# StatsForecast
grep -r "from statsforecast" --include="*.py" .
grep -r "StatsForecast\(" --include="*.py" .

# MLForecast
grep -r "from mlforecast" --include="*.py" .

# NeuralForecast
grep -r "from neuralforecast" --include="*.py" .
```

**Find experiment configs**:
```bash
# Configuration files
find . -name "config.yml" -o -name "config.yaml"

# Experiment scripts
find . -name "*experiment*" -o -name "*forecast*" | grep -E "\.(py|ipynb)$"
```

**Tell the user**:
- "Scanning repository for Nixtla library usage..."
- Show count of files using each library
- Identify key areas (experiments, pipelines, notebooks)

### 2. Analyze Usage Patterns

For each usage area, determine:

**TimeGPT Usage Analysis**:
- Frequency: How often is TimeGPT called?
- Context: Experiments, production, ad-hoc analysis?
- Data characteristics:
  - Simple patterns (daily/weekly seasonality)?
  - Complex patterns (multiple seasonalities, external regressors)?
  - Forecast horizon (short vs long)?

**Baseline Usage Analysis**:
- Which baselines are used? (AutoETS, AutoARIMA, SeasonalNaive, etc.)
- Are they compared against TimeGPT?
- Performance metrics available?

**Routing Opportunities**:
```
Decision framework:

TimeGPT Recommended:
  - Complex patterns (multiple seasonalities)
  - Long-term forecasts (30+ days)
  - High business impact
  - Accuracy > cost priority
  - Limited historical data

Baselines Recommended:
  - Simple seasonal patterns
  - Short-term forecasts (<7 days)
  - Low business impact
  - Cost > accuracy priority
  - Abundant historical data

MLForecast Recommended:
  - Medium complexity
  - External features available
  - Offline batch processing acceptable
```

### 3. Generate Usage Report

Create comprehensive markdown report at `000-docs/nixtla_usage_report.md`:

```markdown
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
```

**Tell the user**:
- "Created `000-docs/nixtla_usage_report.md`"
- Highlight top 3-5 recommendations
- Suggest next steps

---

## Examples

### Example 1: Audit Existing Project

**User**: "Analyze our TimeGPT usage and find cost savings"

**You**:
```
Scanning repository for Nixtla usage...

Found:
- TimeGPT: 12 locations
- StatsForecast: 8 locations
- MLForecast: 2 locations
- Experiment configs: 3 files

Analyzing usage patterns...

Key Findings:
1. TimeGPT overused in 4 low-impact areas
   → Potential 40% cost reduction by switching to StatsForecast
2. Missing fallback mechanisms
   → Risk of failures when API unavailable
3. Batching opportunity in production pipeline
   → Could reduce API calls by 50%

Generating comprehensive report...

✅ Created: 000-docs/nixtla_usage_report.md

Top Recommendations:
1. Implement routing strategy (high/medium/low impact)
2. Add fallback chain: TimeGPT → MLForecast → StatsForecast
3. Batch TimeGPT calls in production pipeline

Estimated Savings: 30-50% API cost reduction
```

### Example 2: No TimeGPT Usage Yet

**User**: "Should we be using TimeGPT?"

**You**:
```
Scanning repository...

Found:
- TimeGPT: 0 locations
- StatsForecast: 15 locations (mostly AutoETS)
- MLForecast: 0 locations

Analysis:
Current approach uses only StatsForecast baselines.

Opportunities to add TimeGPT:
1. High-impact revenue forecasts (currently AutoETS)
   → Complex patterns, long horizon (30 days)
   → TimeGPT could improve accuracy 15-30%

2. Demand planning forecasts (currently SeasonalNaive)
   → Business-critical, currently using simplest baseline
   → TimeGPT recommended

Recommendations:
1. Start with TimeGPT for top 2 high-value forecasts
2. Compare TimeGPT vs current baselines
3. Expand if accuracy gains justify costs

Created report: 000-docs/nixtla_usage_report.md
```

---

## Common Issues and Troubleshooting

### Issue 1: Can't find any Nixtla usage

**Symptom**: Scan returns zero results

**Solution**:
- Verify repository is correct
- Check if code uses different import patterns
- Look in notebooks: `find . -name "*.ipynb"`
- May be a new project - recommend starting with experiment architect

### Issue 2: Report too generic

**Symptom**: Recommendations not specific enough

**Solution**:
- Manually review key files for context
- Ask user for business impact information
- Focus on specific code patterns found
- Provide concrete code examples in recommendations

---

## Best Practices

### 1. Run Audit Quarterly

Rerun this skill every 3 months to catch:
- New TimeGPT usage patterns
- Opportunities from product updates
- Changing cost dynamics

### 2. Track Routing Decisions

Log every routing decision:
```python
logging.info(f"Routing decision: {model_chosen} (reason: {reason})")
```

Review logs to validate routing logic is working as intended.

### 3. A/B Test Routing Changes

Before fully committing to routing changes:
- Run both old and new approach in parallel
- Compare accuracy and costs
- Verify assumptions hold in practice

### 4. Combine with Usage Metrics

If you have access to Nixtla dashboard or usage logs:
- Include actual API call counts
- Show real cost data
- Calculate precise ROI instead of estimates

---

## Related Skills

Works well with:
- **nixtla-experiment-architect**: Sets up comparison experiments to validate routing decisions
- **nixtla-timegpt-finetune-lab**: Determines if fine-tuning justifies costs
- **nixtla-prod-pipeline-generator**: Implements routing and fallback in production
- **nixtla-timegpt-lab**: Overall Nixtla guidance

---

## Summary

This skill helps optimize Nixtla usage:
1. ✅ Audits TimeGPT and baseline library usage
2. ✅ Identifies cost optimization opportunities
3. ✅ Recommends routing strategies
4. ✅ Generates actionable usage report
5. ✅ Provides ROI assessment

**When to use this skill**:
- Before scaling TimeGPT usage
- When optimizing costs
- For internal Nixtla audits
- When designing routing logic

**Value delivered**:
- 30-50% potential cost reduction
- Maintained accuracy on critical forecasts
- Clear routing decision framework
- Reduced API failure risk (fallbacks)

Smart routing ensures you use the right tool for each forecast - TimeGPT where it matters, baselines where they suffice!
