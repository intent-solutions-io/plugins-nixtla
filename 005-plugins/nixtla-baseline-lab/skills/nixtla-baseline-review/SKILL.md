---
name: nixtla-baseline-review
description: Analyze Nixtla baseline forecasting results (sMAPE/MASE on M4 or other
  benchmark datasets). Use when the user asks about baseline performance, model comparisons,
  or metric interpretation for Nixtla time-series experiments. Trigger with "baseline review",
  "interpret sMAPE/MASE", or "compare AutoETS vs AutoTheta".
allowed-tools: Read,Grep,Bash(ls:*)
version: 1.1.0
author: Jeremy Longshore <jeremy@intentsolutions.io>
license: MIT
compatible-with: claude-code
tags: [nixtla, forecasting, benchmarking, time-series, statsforecast]
---

# Nixtla Baseline Review Skill

## Overview

Analyze baseline forecasting results from the `nixtla-baseline-m4` workflow. Interpret metrics, compare models, surface patterns, and recommend next steps.

## When to Use This Skill

Activate this skill when the user:
- Asks "Which baseline model performed best?"
- Requests interpretation of sMAPE or MASE metrics
- Wants to compare AutoETS vs AutoTheta vs SeasonalNaive
- Says "Explain these baseline results"
- Needs guidance on model selection based on baseline performance

## For StatsForecast Power Users

This baseline lab is built on **Nixtla's statsforecast library**. What this plugin provides:
- Real statsforecast models (SeasonalNaive, AutoETS, AutoTheta)
- M4 dataset integration via datasetsforecast
- Standard train/test evaluation with sMAPE and MASE metrics
- Power-user controls: models, freq, season_length parameters
- Demo preset mode for GitHub-style presentations

**Important Disclaimers**:
- This is a **community-built integration**, not an official Nixtla product
- Built to demonstrate Claude Code plugin capabilities with real Nixtla libraries
- For production use cases, always validate against official Nixtla examples

**Advanced Example Questions**:
- "Compare AutoETS vs AutoTheta on MASE only, and show me which series AutoETS loses on"
- "Identify any series where SeasonalNaive still wins on sMAPE - what patterns do they share?"
- "Given these statsforecast metrics, which series would you route to AutoTheta vs AutoETS and why?"

## Prerequisites

- Baseline results must exist in `nixtla_baseline_m4/` directory
- At minimum, `results_*.csv` file must be present
- CSV format: columns `series_id`, `model`, `sMAPE`, `MASE`

## Instructions

### Step 1: Locate Results Files

Use Read or Bash tool to find baseline results:

```bash
# Check for results directory
ls -la nixtla_baseline_m4/

# Identify most recent results file
ls -t nixtla_baseline_m4/results_*.csv | head -1
```

Expected files:
- `results_M4_Daily_h<horizon>.csv` - Full metrics table
- `summary_M4_Daily_h<horizon>.txt` - Text summary (optional)
- `benchmark_report_*.md` - Formatted report (optional)

If files are missing, prompt the user to run `/nixtla-baseline-m4` first.

### Step 2: Load and Parse Metrics

Read the metrics CSV file:

```bash
# View first few rows to confirm format
head -10 nixtla_baseline_m4/results_M4_Daily_h*.csv
```

Expected CSV structure:
```csv
series_id,model,sMAPE,MASE
D1,SeasonalNaive,15.23,1.05
D1,AutoETS,13.45,0.92
D1,AutoTheta,12.34,0.87
D2,SeasonalNaive,18.67,1.23
...
```

### Step 3: Calculate Summary Statistics

For each model (SeasonalNaive, AutoETS, AutoTheta), calculate:
- **Mean sMAPE**: Average across all series
- **Median sMAPE**: Middle value (less sensitive to outliers)
- **Standard Deviation**: Measure of consistency
- **Series Won**: Count how many series each model performed best on

### Step 4: Interpret Metrics

For detailed metric interpretation, see `resources/METRIC_INTERPRETATION.md`.

**Quick Reference**:
- **sMAPE**: 0% (perfect) to 200% (worst). Good: < 15%, Acceptable: 15-20%
- **MASE**: < 1.0 means better than seasonal naive baseline

### Step 5: Generate Structured Explanation

Provide analysis in this format:

```markdown
## Baseline Performance Analysis

Based on {N} series from M4-Daily with horizon={H}:

**Overall Winner**: {ModelName}
- Mean sMAPE: {X.XX}% (vs {Y.YY}% for second place)
- Wins on {N} out of {Total} series ({Percentage}%)
- Consistent performance (std dev {X.X}%)

**Key Insights**:
1. {Insight about winner's strengths}
2. {Insight about other models or patterns}
3. {Insight about failure cases or opportunities}

**Recommendation**: Use {ModelName} as production baseline. {Additional context}

**Next Steps**:
- {Actionable recommendation 1}
- {Actionable recommendation 2}
```

## Examples

For full worked examples (simple query, detailed comparison, metric interpretation), see [examples](resources/examples.md).

## Advanced Features

### Benchmark Reports

If a benchmark report exists (`benchmark_report_*.md`), use Read tool to view formatted summaries suitable for GitHub issues or documentation.

For details on benchmark reports, see the MCP server documentation.

### TimeGPT Showdown

If TimeGPT comparison data is present, incorporate it into the analysis. See `resources/TIMEGPT_COMPARISON.md` for detailed guidance.

**Key points**:
- Check `timegpt_status` field first
- Emphasize limited sample size (typically 3-5 series)
- Use language like "indicative" not "conclusive"
- Never fabricate TimeGPT metrics that don't exist

### GitHub Issue Drafts

Help users create GitHub issue drafts to share results with Nixtla maintainers. See `resources/GITHUB_ISSUES.md` for complete guidance.

**When to suggest**:
- User wants to ask Nixtla maintainers a question
- User suspects a bug or unexpected behavior
- User wants to share benchmark results with the community

## Output

- A structured markdown analysis with an overall winner, key insights, and recommended next steps.
- Optional: a short “power user” section highlighting series-level anomalies and failure cases.

## Error Handling

**If results files are missing**:
```
No baseline results found in nixtla_baseline_m4/.

Run the baseline command first:
`/nixtla-baseline-m4 horizon=14 series_limit=50`

This generates the metrics files needed for analysis.
```

**If CSV is malformed**:
```
The results file exists but appears malformed. Expected columns:
- series_id, model, sMAPE, MASE

Please re-run /nixtla-baseline-m4 to regenerate clean results.
```

## Resources

For detailed information on specific topics:
- **Metric interpretation**: `resources/METRIC_INTERPRETATION.md`
- **TimeGPT comparisons**: `resources/TIMEGPT_COMPARISON.md`
- **GitHub issue drafts**: `resources/GITHUB_ISSUES.md`

For complete technical details, see:
- Architecture: `000-docs/6767-OD-ARCH-nixtla-claude-plugin-poc-baseline-lab.md`
- Planning: `000-docs/6767-PP-PLAN-nixtla-claude-plugin-poc-baseline-lab.md`
- Phase 3 AAR: `000-docs/017-AA-AACR-phase-03-mcp-baselines-nixtla-oss.md`
- Phase 8 AAR: `000-docs/022-AA-AACR-phase-08-timegpt-showdown-and-evals.md`
