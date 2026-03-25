# Benchmark Reporter Output Formats

## Standard Report (`report.md`)

Contains these sections in order:
1. Executive Summary (1-2 paragraphs)
2. Model Comparison Table (all metrics)
3. Statistical Analysis (means, std devs, percentiles)
4. Winner Declaration with justification
5. Per-Series Breakdown (optional)
6. Recommendations for production use
7. Failure Case Analysis (series with sMAPE > 30%)

## Regression Report (if baseline provided)

Generated when `--baseline` flag is used:
1. Regression Summary (models degraded)
2. Severity Analysis (% change per model)
3. Affected Series List
4. GitHub Issue Template

## GitHub Issue Template

Generated with `--format github`:

```markdown
---
title: "Performance Regression Detected: {model_name}"
labels: ["regression", "performance"]
assignees: ["team-lead"]
---

## Regression Summary
Model: {model_name}
Metric: sMAPE degraded by {X}%
Baseline: {baseline_value}%
Current: {current_value}%

## Affected Series
- {series_1}: {baseline}% -> {current}% ({delta}%)
- {series_2}: {baseline}% -> {current}% ({delta}%)
...

## Acceptance Criteria
- [ ] Investigate root cause
- [ ] Restore performance to within 2% of baseline
- [ ] Add regression test to CI/CD
```

## Executive Summary (1-page)

Generated with `--format executive`:

```bash
python {baseDir}/scripts/generate_benchmark_report.py \
    --results metrics.csv \
    --format executive \
    --output summary.md
```

## Report Customization Commands

**Standard Report** (default):
```bash
python {baseDir}/scripts/generate_benchmark_report.py --results metrics.csv
```

**GitHub Issue Template**:
```bash
python {baseDir}/scripts/generate_benchmark_report.py \
    --results metrics.csv \
    --format github \
    --output .github/ISSUE_TEMPLATE/regression.md
```
