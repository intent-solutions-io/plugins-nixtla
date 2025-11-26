---
name: nixtla-baseline-review
description: Analyze Nixtla baseline forecasting results (sMAPE/MASE on M4 or other benchmark datasets). Use when the user asks about baseline performance, model comparisons, or metric interpretation for Nixtla time-series experiments.
allowed-tools: Read, Grep, Bash
---

# Nixtla Baseline Review Skill

## Purpose

This skill helps Claude interpret baseline forecasting results from the `/nixtla-baseline-m4` command. It provides expert analysis of model performance metrics, identifies patterns, and recommends next steps.

## When to Use This Skill

Activate this skill when the user:
- Asks "Which baseline model performed best?"
- Requests interpretation of sMAPE or MASE metrics
- Wants to compare AutoETS vs AutoTheta vs SeasonalNaive
- Says "Explain these baseline results"
- Needs guidance on model selection based on baseline performance

## For StatsForecast Power Users

This baseline lab is built on **Nixtla's statsforecast library**. If you're familiar with statsforecast, M4 benchmarks, or Nixtla's time series ecosystem, you'll feel right at home.

**What This Plugin Provides**:
- Real statsforecast models (SeasonalNaive, AutoETS, AutoTheta)
- M4 dataset integration via datasetsforecast
- Standard train/test evaluation pipeline
- sMAPE and MASE metrics (MASE uses seasonal naive as baseline with configurable season_length)
- Power-user controls: models, freq, season_length parameters
- Demo preset mode for GitHub-style presentations

**Important Disclaimers**:
- This is a **community-built integration**, not an official Nixtla product
- Built to demonstrate Claude Code plugin capabilities with real Nixtla libraries
- Meant as a baseline exploration tool, not a certified benchmarking suite
- For production use cases, always validate against official Nixtla examples

**Advanced Example Questions** (use these to test the plugin):
- "Compare AutoETS vs AutoTheta on MASE only, and show me which series AutoETS loses on"
- "Identify any series where SeasonalNaive still wins on sMAPE - what patterns do they share?"
- "Given these statsforecast metrics, which series would you route to AutoTheta vs AutoETS and why?"
- "Run baselines with models=['AutoTheta'] freq='M' season_length=12 for monthly data"
- "Show me the demo_preset='m4_daily_small' for a quick GitHub walkthrough"

**Power-User Parameters**:
- `models`: Array of model names - ["SeasonalNaive", "AutoETS", "AutoTheta"]
- `freq`: Frequency string - "D" (daily), "M" (monthly), "H" (hourly), etc.
- `season_length`: Seasonal period - 7 for weekly pattern in daily data, 12 for yearly pattern in monthly
- `demo_preset`: "m4_daily_small" for quick demos (overrides other params)

## Prerequisites

- Baseline results must exist in `nixtla_baseline_m4/` directory
- At minimum, `results_*.csv` file must be present
- CSV format: columns `series_id`, `model`, `sMAPE`, `MASE`

## Instructions

### Step 1: Locate Results Files

Use the **Read** tool to find baseline results:

```bash
# Check for results directory (use Bash tool)
ls -la nixtla_baseline_m4/

# Identify most recent results file
ls -t nixtla_baseline_m4/results_*.csv | head -1
```

Expected files:
- `results_M4_Daily_h{horizon}.csv` - Full metrics table
- `summary_M4_Daily_h{horizon}.txt` - Text summary (optional)

If files are missing, inform the user they need to run `/nixtla-baseline-m4` first.

### Step 2: Load and Parse Metrics

Read the metrics CSV file:

```bash
# View first few rows to confirm format
head -10 nixtla_baseline_m4/results_M4_Daily_h*.csv

# Or use Read tool to load the full file
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

Calculate summary statistics manually or with bash:
- Count total series: `cut -d, -f1 results_*.csv | sort -u | wc -l`
- Extract model metrics: `grep "AutoTheta" results_*.csv`

### Step 3: Calculate Summary Statistics

For each model (SeasonalNaive, AutoETS, AutoTheta), calculate:
- **Mean sMAPE**: Average across all series
- **Median sMAPE**: Middle value (less sensitive to outliers)
- **Standard Deviation**: Measure of consistency
- **Series Won**: Count how many series each model performed best on

### Step 4: Interpret Metrics

**sMAPE (Symmetric Mean Absolute Percentage Error)**:
- Range: 0% (perfect) to 200% (worst)
- Good: < 10%, Acceptable: 10-20%, Poor: > 20%

**MASE (Mean Absolute Scaled Error)**:
- < 1.0: Better than seasonal naive baseline
- 1.0: Same as seasonal naive
- > 1.0: Worse than seasonal naive
- Interpretation: "MASE of 0.85 means this model is 15% better than naive seasonal"

**Model Characteristics**:
- **SeasonalNaive**: Simplest baseline, repeats seasonal pattern. Good for stable series.
- **AutoETS**: Exponential smoothing with automatic parameter selection. Good for trend + seasonality.
- **AutoTheta**: Theta method with optimization. Often wins on M4 benchmarks, handles trends well.

### Step 5: Identify Patterns

Look for:
- **Dominant model**: Which model wins most often?
- **Consistency**: Which model has lowest standard deviation in sMAPE?
- **Series-specific patterns**: Are there series types where certain models excel?
- **Failure cases**: Where do ALL models struggle? (sMAPE > 30%, MASE > 1.5)

### Step 6: Generate Structured Explanation

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

**Recommendation**: Use {ModelName} as production baseline. {Additional context about when to consider alternatives}

**Next Steps**:
- {Actionable recommendation 1}
- {Actionable recommendation 2}
```

## Example Interactions

### Example 1: Simple Query

**User**: "Which model was best?"

**Response**:
```
Based on the baseline results (50 series, horizon=14):

**AutoTheta won** with average sMAPE of 12.3%
- Outperformed AutoETS (13.5%) and SeasonalNaive (15.2%)
- Most consistent with std dev of 4.2%
- Recommended for production use
```

### Example 2: Detailed Comparison

**User**: "Compare AutoETS vs AutoTheta performance"

**Response**:
```
## AutoETS vs AutoTheta Comparison

| Metric        | AutoETS | AutoTheta | Winner   |
|---------------|---------|-----------|----------|
| Mean sMAPE    | 13.5%   | 12.3%     | Theta ✓  |
| Median sMAPE  | 12.9%   | 11.8%     | Theta ✓  |
| Std Dev       | 5.1%    | 4.2%      | Theta ✓  |
| Series Won    | 18/50   | 32/50     | Theta ✓  |

**Key Differences**:
- Theta handles trends better (exponential smoothing with drift)
- ETS excels on strong seasonality (state space framework)
- Theta more consistent across diverse patterns

**Recommendation**: Use AutoTheta as default, fallback to AutoETS for highly seasonal data.
```

### Example 3: Metric Interpretation

**User**: "What does sMAPE of 12.3% mean?"

**Response**:
```
sMAPE of 12.3% is **good performance** for forecasting:

- This means on average, predictions are off by about 12% from actual values
- For M4 Daily benchmark, anything under 15% is considered good
- This is in the "acceptable" range (10-20%)

Context: If you're forecasting daily sales of 100 units, a 12.3% sMAPE means your forecast will typically be within ±12 units of the true value.

MASE provides additional context - if MASE < 1.0, this forecast beats a simple "repeat last year" baseline.
```

## Error Handling

**If results files are missing**:
```
I don't see baseline results in nixtla_baseline_m4/.

Please run the baseline command first:
/nixtla-baseline-m4 horizon=14 series_limit=50

This will generate the metrics files I need to analyze.
```

**If CSV is malformed**:
```
The results file exists but appears malformed. Expected columns:
- series_id, model, sMAPE, MASE

Please re-run /nixtla-baseline-m4 to regenerate clean results.
```

## TimeGPT Showdown (Optional)

If TimeGPT comparison data is present, incorporate it into your analysis.

**Files to check**:
- `timegpt_showdown_M4_Daily_h{horizon}.txt` - Showdown summary report
- JSON response may include `timegpt_summary`, `timegpt_per_series` fields

**How to interpret**:

When TimeGPT comparison exists:
1. **Read the showdown file** using Read or Bash tool
2. **Note the comparison scope**: This is a small-sample comparison (typically 3-5 series), NOT a comprehensive M4 benchmark
3. **Include in your response**:
   - Overall winner (baseline vs TimeGPT)
   - Average sMAPE for each
   - Note that it's an illustrative comparison on a subset
4. **Example language**:
   ```
   TimeGPT Comparison (Limited Sample):
   - Tested on {N} series (subset for cost/time)
   - TimeGPT avg sMAPE: {X.XX}%
   - Baseline best avg sMAPE: {Y.YY}%
   - Winner on this subset: {WINNER}

   ⚠️ Note: This is an illustrative comparison on a small sample, not a full benchmark.
   TimeGPT performance may vary significantly on the complete dataset.
   ```

**When NOT available**:
- Don't mention TimeGPT unless the user explicitly asks
- If asked, explain: "TimeGPT comparison was not run. Use `include_timegpt=true` to enable."

**Key points to emphasize**:
- TimeGPT is Nixtla's hosted foundation model for time series
- Comparison is for illustration/exploration, not production claims
- Small sample size means results are directional, not conclusive
- For production decisions, run on larger representative samples

## Benchmark Reports (Optional)

If a **benchmark report Markdown file** exists in the results directory (e.g., `benchmark_report_M4_Daily_h7.md`), you may read and use it to provide formatted summaries.

**When to use benchmark reports**:
- User asks to "generate and share a benchmark report"
- User wants formatted output for GitHub issues, documentation, or papers
- User requests a summary suitable for external sharing with Nixtla or research community

**How to handle benchmark reports**:
1. Check if a benchmark report exists: `ls nixtla_baseline_m4*/benchmark_report_*.md`
2. If found, use the **Read** tool to view the contents
3. The report already includes:
   - Dataset and horizon details
   - StatsForecast version (for reproducibility)
   - Average metrics table (sorted by performance)
   - Highlights section with key insights
   - Timestamp

**Example user question**:
- "Generate and summarize a benchmark report I can paste into a GitHub issue for statsforecast"
- "Create a benchmark report from the last run and show me the highlights"

**Guidance**:
- Prefer using the benchmark report + metrics CSV combo when summarizing performance for external sharing
- The report format is designed for copy-paste into GitHub, documentation, or papers
- If no report exists, you can suggest: "Use the `generate_benchmark_report` tool to create a formatted report"

## Documentation

For complete technical details, see:
- Architecture: `000-docs/6767-OD-ARCH-nixtla-claude-plugin-poc-baseline-lab.md`
- Planning: `000-docs/6767-PP-PLAN-nixtla-claude-plugin-poc-baseline-lab.md`
- Phase 3 AAR: `000-docs/017-AA-AACR-phase-03-mcp-baselines-nixtla-oss.md`
- Phase 8 AAR: `000-docs/022-AA-AACR-phase-08-timegpt-showdown-and-evals.md`
