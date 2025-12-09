# TimeGPT Experiments Summary - DRY RUN MODE

**Generated**: 2025-12-08 21:25:16
**Mode**: DRY RUN
**Note**: Metrics are against naive baseline (last-value), not TimeGPT. Validates workflow, not accuracy.
**Config**: experiments/timegpt_experiments.json

## Configuration

- **Total experiments defined**: 3
- **Enabled experiments**: 2
- **Disabled experiments**: 1

## Results by Experiment

### timegpt_baseline_14d

**Description**: Baseline 14-day forecast matching Phase 04 smoke test behavior. Uses the last 14 points as holdout for evaluation.
**Horizon**: 14 steps
**Eval Window**: 14 steps
**Runtime**: 0.01s

| Series | MAE | SMAPE |
|--------|-----|-------|
| series_1 | 7.2857 | 4.09% |
| series_2 | 5.1500 | 2.12% |

**Aggregate Metrics**:
- Average MAE: 6.2179
- Average SMAPE: 3.11%

### timegpt_baseline_28d

**Description**: Longer 28-day forecast to test TimeGPT performance on extended horizons. Uses the last 28 points as holdout.
**Horizon**: 28 steps
**Eval Window**: 28 steps
**Runtime**: 0.00s

| Series | MAE | SMAPE |
|--------|-----|-------|
| series_1 | 13.3214 | 7.86% |
| series_2 | 9.0000 | 3.79% |

**Aggregate Metrics**:
- Average MAE: 11.1607
- Average SMAPE: 5.83%

## Comparative Analysis

| Experiment | Avg MAE | Avg SMAPE | Runtime |
|------------|---------|-----------|---------|
| timegpt_baseline_14d | 6.2179 | 3.11% | 0.01s |
| timegpt_baseline_28d | 11.1607 | 5.83% | 0.00s |

**Insights**:
- Lowest MAE: `timegpt_baseline_14d`
- Lowest SMAPE: `timegpt_baseline_14d`
- Horizon range: 14-28 days
- Longer horizons typically have higher error (expected behavior)

---

**Lab**: 002-workspaces/timegpt-lab/
**Phase**: 05 - TimeGPT Experiment Workflows