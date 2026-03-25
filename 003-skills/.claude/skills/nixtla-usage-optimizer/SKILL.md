---
name: nixtla-usage-optimizer
description: "Analyze Nixtla usage and optimize cost-effective forecast routing strategies. Use when auditing API usage or reducing costs. Trigger with 'optimize nixtla costs' or 'audit API usage'."
allowed-tools: "Read,Glob,Grep"
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
compatible-with: claude-code
tags: [nixtla, time-series, forecasting, cost-optimization]
---

# Nixtla Usage Optimizer

Audit Nixtla library usage and recommend cost-effective routing strategies across TimeGPT and baseline models.

## Overview

This skill analyzes and optimizes Nixtla usage across a codebase:

- **Usage scanning**: Find all TimeGPT, StatsForecast, and MLForecast import and call sites
- **Cost analysis**: Identify optimization opportunities where baselines match TimeGPT accuracy
- **Routing recommendations**: Smart model selection based on data complexity and forecast value
- **ROI assessment**: Quantify cost vs accuracy trade-offs to justify API spend

## Prerequisites

**Required**:
- Python 3.8+
- Existing Nixtla codebase to audit

**No Additional Packages**: Uses only Read, Glob, and Grep tools for zero-dependency operation.

## Instructions

### Step 1: Scan Repository

Find all Nixtla library usage across the project to build an inventory of API calls and model instantiations:
```bash
grep -r "NixtlaClient" --include="*.py" .
grep -r "StatsForecast" --include="*.py" .
grep -r "MLForecast" --include="*.py" .
```

### Step 2: Analyze Patterns

Categorize discovered usage by three dimensions:
- **Location**: experiments, pipelines, notebooks, or production scripts
- **Frequency**: how often each call site executes (batch vs. real-time)
- **Data characteristics**: simple seasonal patterns (baseline-suitable) vs. complex patterns (TimeGPT-suitable)

### Step 3: Generate Report

Create `000-docs/nixtla_usage_report.md` containing an executive summary, detailed usage analysis organized by location, specific recommendations with estimated savings, and ROI assessment.

### Step 4: Implement Routing

Apply recommendations from the report:
- Replace TimeGPT with StatsForecast baselines for simple seasonal patterns
- Add TimeGPT for high-value forecasts where accuracy improvement justifies API cost
- Implement fallback chains (TimeGPT -> StatsForecast -> SeasonalNaive)

## Output

- **000-docs/nixtla_usage_report.md**: Comprehensive usage report with findings and recommendations
- **routing_rules.json**: Machine-readable routing logic for automated model selection (optional)

## Error Handling

1. **Error**: `No Nixtla usage found`
   **Solution**: Repository may not use Nixtla yet; recommend adoption starting with StatsForecast baselines

2. **Error**: `Cannot determine cost impact`
   **Solution**: Add usage metrics or API call logging to enable cost analysis

3. **Error**: `Mixed usage patterns`
   **Solution**: Report both optimization and expansion opportunities, prioritize by estimated impact

4. **Error**: `No baseline models found`
   **Solution**: Recommend adding StatsForecast for fallback and cost reduction

## Examples

### Example 1: Audit Existing Project

**Scan results**:
```
Found Nixtla usage:
  - TimeGPT: 12 locations
  - StatsForecast: 5 locations
  - MLForecast: 2 locations
```

**Recommendations**:
```
1. Replace TimeGPT in 4 low-impact areas (save ~40%)
2. Add fallback to StatsForecast baselines
3. Keep TimeGPT for high-value forecasts
```

### Example 2: No TimeGPT Yet

**Scan results**:
```
Found Nixtla usage:
  - StatsForecast: 8 locations
  - TimeGPT: 0 locations
```

**Recommendations**:
```
1. Add TimeGPT for 2 high-value forecasts
2. Keep baselines for simple patterns
3. Implement tiered routing
```

## Resources

- TimeGPT Pricing: https://nixtla.io/pricing
- StatsForecast Docs: https://nixtla.github.io/statsforecast/

**Related Skills**:
- `nixtla-experiment-architect`: Validate routing decisions with A/B experiments
- `nixtla-timegpt-finetune-lab`: Evaluate fine-tuning ROI
- `nixtla-prod-pipeline-generator`: Implement routing in production pipelines
