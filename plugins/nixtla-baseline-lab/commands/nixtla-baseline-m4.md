---
name: nixtla-baseline-m4
description: Run baseline forecasting models on M4 Daily dataset
model: sonnet
---

# Run Nixtla Baseline Models on M4 Daily Dataset

Execute baseline forecasting models (SeasonalNaive, AutoETS, AutoTheta) on the M4 Daily benchmark dataset using the Nixtla Baseline Lab MCP tool.

## Phase 2 Status: Stub Implementation

This command is currently a **Phase 2 stub**. The MCP server and real Nixtla baseline logic will be implemented in Phase 3.

## Parameters

- `horizon` (optional, integer): Forecast horizon in days. Default: 14
- `series_limit` (optional, integer): Maximum number of series to process. Default: 50
- `output_dir` (optional, string): Directory for results. Default: `nixtla_baseline_m4/`

## Planned Workflow (Phase 3)

1. **Invoke MCP Tool**: Call `nixtla-baseline-mcp` tool `run_baselines` with parameters
2. **Process Dataset**: Load M4 Daily dataset
3. **Run Models**: Execute SeasonalNaive, AutoETS, AutoTheta on each series
4. **Calculate Metrics**: Compute sMAPE and MASE for each model
5. **Generate Outputs**:
   - `results_M4_Daily_h{horizon}.csv` - Metrics table
   - `summary_M4_Daily_h{horizon}.txt` - Text summary
6. **Return Summary**: Display top-performing models and file locations

## TODO - Phase 3

- [ ] Implement MCP tool invocation
- [ ] Add real statsforecast model execution
- [ ] Integrate datasetsforecast M4 data loading
- [ ] Add metric calculation logic
- [ ] Generate formatted output files
- [ ] Add error handling and validation

## Expected Output (Phase 3)

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

## Documentation

For complete technical details, see:
- Architecture: `000-docs/6767-OD-ARCH-nixtla-claude-plugin-poc-baseline-lab.md`
- Planning: `000-docs/6767-PP-PLAN-nixtla-claude-plugin-poc-baseline-lab.md`
