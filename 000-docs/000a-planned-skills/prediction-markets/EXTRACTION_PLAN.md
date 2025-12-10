# Prediction Markets Skills - Script Extraction Plan

**Status**: In Progress
**Created**: 2025-12-08
**Pattern**: Following nixtla-arbitrage-detector model

## Objective

Extract embedded Python code from 9 prediction-markets SKILL.md files into separate script files, then rewrite each SKILL.md to reference scripts using `{baseDir}/scripts/` pattern, keeping total length under 200 lines.

## Skills to Process

1. ✅ nixtla-arbitrage-detector (COMPLETED - reference implementation)
2. ⏳ nixtla-batch-forecaster
3. ⏳ nixtla-contract-schema-mapper
4. ⏳ nixtla-correlation-mapper
5. ⏳ nixtla-event-impact-modeler
6. ⏳ nixtla-forecast-validator
7. ⏳ nixtla-liquidity-forecaster
8. ⏳ nixtla-market-risk-analyzer
9. ⏳ nixtla-model-selector
10. ⏳ nixtla-polymarket-analyst

## Per-Skill Checklist

For each skill:

- [ ] Create `004-scripts/` directory
- [ ] Extract all Python code blocks to individual `.py` files
- [ ] Name files descriptively (e.g., `prepare_data.py`, `forecast.py`, `generate_report.py`)
- [ ] Rewrite SKILL.md to:
  - Keep 8 required sections
  - Use `{baseDir}/scripts/filename.py` references
  - Remove all embedded code
  - Keep under 200 lines
- [ ] Test that scripts are referenced correctly

## Script Extraction Mapping

### nixtla-batch-forecaster (3 scripts)
- `004-scripts/prepare_data.py` - Data loading and validation (lines 40-167)
- `004-scripts/batch_forecast.py` - Main forecasting engine (lines 174-417)
- `004-scripts/generate_report.py` - Report generator (lines 424-541)

### nixtla-contract-schema-mapper (1 script)
- `004-scripts/transform_data.py` - Schema transformation and validation (lines 41-184)

### nixtla-correlation-mapper (5 scripts)
- `004-scripts/prepare_data.py` - Data prep and pivoting (lines 40-147)
- `004-scripts/correlation_analysis.py` - Correlation calculation (lines 154-310)
- `004-scripts/hedge_recommendations.py` - Hedging strategies (lines 317-509)
- `004-scripts/visualize.py` - Heatmaps and plots (lines 516-674)
- `004-scripts/generate_report.py` - Report generation (lines 681-789)

### nixtla-event-impact-modeler (3 scripts)
- `004-scripts/load_data.py` - Data loading (lines 40-113)
- `004-scripts/configure_model.py` - Model configuration (lines 120-205)
- `004-scripts/analyze_impact.py` - Event impact analysis (lines 212-337)

### nixtla-forecast-validator (1 script)
- `004-scripts/validate_forecast.py` - Complete validation pipeline (lines 159-413)

### nixtla-liquidity-forecaster (3 scripts)
- `004-scripts/fetch_data.py` - Polymarket API fetcher (lines 36-105)
- `004-scripts/preprocess_data.py` - Data preprocessing (lines 112-206)
- `004-scripts/forecast_liquidity.py` - Forecasting execution (lines 213-320)

### nixtla-market-risk-analyzer (4 scripts)
- `004-scripts/prepare_data.py` - Data preparation (lines 38-154)
- `004-scripts/risk_metrics.py` - VaR, volatility, drawdown (lines 161-431)
- `004-scripts/position_sizing.py` - Position size calculations (lines 438-665)
- `004-scripts/generate_report.py` - Risk report generation (lines 672-884)

### nixtla-model-selector (4 scripts)
- `004-scripts/load_and_analyze.py` - Data loading and analysis (lines 40-125)
- `004-scripts/select_model.py` - Model selection logic (lines 132-196)
- `004-scripts/execute_forecast.py` - Forecast execution (lines 203-282)
- `004-scripts/generate_output.py` - Output generation (lines 289-335)

### nixtla-polymarket-analyst (4 scripts)
- `004-scripts/fetch_contract.py` - Polymarket data fetcher (lines 36-146)
- `004-scripts/transform_data.py` - Data transformation (lines 153-248)
- `004-scripts/forecast_contract.py` - TimeGPT forecasting (lines 255-503)
- `004-scripts/analyze_polymarket.py` - Complete pipeline (lines 510-644)

## Required SKILL.md Sections (All Skills)

1. **Frontmatter** (YAML with name, description, allowed-tools, version)
2. **Title** (# heading matching skill name)
3. **Overview** (1-2 paragraphs)
4. **Prerequisites** (Tools, Environment, Packages)
5. **Instructions** (Step-by-step workflow referencing scripts)
6. **Output** (Files produced)
7. **Error Handling** (Common errors and solutions)
8. **Examples** (1-2 concrete use cases)

## Next Steps

1. Complete script extraction for remaining 9 skills
2. Rewrite each SKILL.md to reference scripts
3. Validate compliance with skill standard
4. Test all scripts can be located via {baseDir}
5. Commit with descriptive message

## Reference Implementation

See `nixtla-arbitrage-detector/SKILL.md` for the target format. Key points:

- Total length: 149 lines (target: < 200)
- Scripts referenced: `{baseDir}/scripts/detect_arbitrage.py`
- All 8 sections present
- No embedded code blocks
- Clear, actionable instructions

## Estimated Completion

- Per-skill time: 10-15 minutes
- Total remaining: ~2 hours
- Requires: File creation access, careful extraction of code blocks
