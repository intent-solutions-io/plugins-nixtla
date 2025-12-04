# Nixtla Usage Optimizer - Examples

## Example 1: Audit Existing Project

**User**: "Analyze our TimeGPT usage and find cost savings"

**Response**:
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

---

## Example 2: No TimeGPT Usage Yet

**User**: "Should we be using TimeGPT?"

**Response**:
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
