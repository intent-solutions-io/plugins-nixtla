---
name: nixtla-usage-optimizer
description: "Audits Nixtla library usage and recommends cost-effective routing strategies. Scans TimeGPT, StatsForecast, and MLForecast patterns, identifies cost optimization opportunities, generates comprehensive usage reports, and suggests smart routing between models. Use when user needs cost optimization, API usage audit, routing strategy design, or Nixtla cost reduction. Trigger with 'optimize TimeGPT costs', 'audit Nixtla usage', 'reduce API costs', 'routing strategy'."
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

Create comprehensive markdown report at `000-docs/nixtla_usage_report.md`.

**Report Structure** (see full template in `resources/TEMPLATES/NIXTLA_USAGE_REPORT_TEMPLATE.md`):

1. **Executive Summary**: Current state, key findings, savings potential
2. **Usage Analysis**: TimeGPT patterns, baseline usage, routing gaps
3. **Recommendations**: Routing strategy, fallback mechanisms, cost optimization
4. **ROI Assessment**: Cost-accuracy trade-offs, estimated impact
5. **Implementation Checklist**: Action items
6. **Appendix**: Detailed usage inventory

**Key recommendation types**:
- Implement smart routing (high/medium/low impact)
- Add fallback chain: TimeGPT → MLForecast → StatsForecast → SeasonalNaive
- Batch TimeGPT calls for cost savings
- Replace TimeGPT in low-impact areas
- Add TimeGPT to high-value forecasts

For the complete report template, see `resources/TEMPLATES/NIXTLA_USAGE_REPORT_TEMPLATE.md`

**Tell the user**:
- "Created `000-docs/nixtla_usage_report.md`"
- Highlight top 3-5 recommendations
- Suggest next steps

---

## Examples

**Example 1**: Audit existing project with TimeGPT usage
- Scans repository, finds 12 TimeGPT locations
- Identifies 4 low-impact overuse candidates (40% cost reduction potential)
- Generates comprehensive report with routing strategy

**Example 2**: No TimeGPT usage yet
- Scans repository, finds only StatsForecast baselines
- Identifies 2 high-value opportunities for TimeGPT
- Recommends selective adoption strategy

For detailed examples, see `resources/EXAMPLES.md`.

For troubleshooting, see `resources/TROUBLESHOOTING.md`.

For best practices, see `resources/BEST_PRACTICES.md`

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
