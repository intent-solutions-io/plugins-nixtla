---
name: nixtla-baseline-m4
description: Run baseline forecasting models on M4 Daily dataset
model: sonnet
---

# Run Nixtla Baseline Models on M4 Daily Dataset

Execute baseline forecasting models (SeasonalNaive, AutoETS, AutoTheta) on the M4 Daily benchmark dataset using real Nixtla open-source libraries.

## Parameters

- `horizon` (optional, integer): Forecast horizon in days. Default: 14, Range: 1-60
- `series_limit` (optional, integer): Maximum number of series to process. Default: 50, Range: 1-500
- `output_dir` (optional, string): Directory for results. Default: `nixtla_baseline_m4/`

## How It Works

This command invokes the `nixtla-baseline-mcp` MCP tool to run a complete baseline forecasting workflow:

1. **Load M4 Daily Dataset**: Uses `datasetsforecast` to load the M4 Daily benchmark dataset (publicly available time series data)
2. **Sample Series**: Limits to first `series_limit` series to keep runtime manageable
3. **Split Train/Test**: Uses last `horizon` points as test set for metric calculation
4. **Run Baseline Models**: Executes three classical forecasting methods via `statsforecast`:
   - **SeasonalNaive**: Simple seasonal baseline (repeats values from one season ago)
   - **AutoETS**: Exponential smoothing state space model with automatic parameter selection
   - **AutoTheta**: Theta method with optimization
   - All use `season_length=7` (weekly patterns for daily data)
5. **Calculate Metrics**: Computes two standard forecasting metrics for each model/series:
   - **sMAPE** (Symmetric Mean Absolute Percentage Error): 0-200%, lower is better
   - **MASE** (Mean Absolute Scaled Error): < 1.0 means better than seasonal naive
6. **Generate Outputs**:
   - `results_M4_Daily_h{horizon}.csv` - Full metrics table (series_id, model, sMAPE, MASE)
   - `summary_M4_Daily_h{horizon}.txt` - Human-readable summary with average metrics

## Example Usage

```
/nixtla-baseline-m4 horizon=7 series_limit=25
```

This will:
- Process 25 series from M4 Daily
- Forecast 7 days ahead
- Output results to `nixtla_baseline_m4/` directory

## Expected Output

```
✓ Baseline models completed on M4 Daily dataset

Summary:
- Dataset: M4-Daily (100 series)
- Horizon: 7 days
- Models: SeasonalNaive, AutoETS, AutoTheta

Results:
┌──────────────┬────────┬────────┐
│ Model        │ sMAPE  │ MASE   │
├──────────────┼────────┼────────┤
│ AutoTheta    │ 12.34% │ 0.876  │
│ AutoETS      │ 13.21% │ 0.902  │
│ SeasonalNaive│ 15.67% │ 1.023  │
└──────────────┴────────┴────────┘

Files saved to: ./nixtla_baseline_m4/
- results_M4_Daily_h7.csv
- summary_M4_Daily_h7.txt

Use the NixtlaBaselineReview skill to analyze these results.
```

## Next Steps

After running this command:
1. **Ask Claude to interpret results**: "Which model performed best?" - activates the NixtlaBaselineReview skill
2. **Request deeper analysis**: "Use nixtla-baseline-analyst to analyze these results" - invokes expert agent
3. **Compare different horizons**: Try horizon=7 vs horizon=14 to see how accuracy degrades
4. **Examine specific series**: Ask about individual series performance or failure cases

## Error Handling

If you encounter errors:
- **Missing dependencies**: Install with `pip install -r scripts/requirements.txt`
- **M4 data not found**: First run will download data to `data/` directory (may take a moment)
- **Timeout**: Reduce `series_limit` to process fewer series
- **Memory issues**: Run with smaller `series_limit` or increase system resources

## Documentation

For complete technical details, see:
- Architecture: `000-docs/6767-OD-ARCH-nixtla-claude-plugin-poc-baseline-lab.md`
- Planning: `000-docs/6767-PP-PLAN-nixtla-claude-plugin-poc-baseline-lab.md`
- Phase 3 AAR: `000-docs/017-AA-AACR-phase-03-mcp-baselines-nixtla-oss.md`
