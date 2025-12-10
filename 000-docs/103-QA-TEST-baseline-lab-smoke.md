# Test Record: Baseline Lab Smoke Test

**Document ID**: 103-QA-TEST-baseline-lab-smoke
**Date**: 2025-12-10
**Status**: PASS
**Tester**: Claude Code

---

## Test Purpose

Verify the baseline-lab MCP server correctly runs forecasting models on M4 sample data and produces valid metrics.

---

## Environment

| Component | Version |
|-----------|---------|
| Python | 3.12.3 |
| statsforecast | 2.0.3 |
| datasetsforecast | 1.0.0 |
| pandas | 2.3.3 |
| numpy | 2.3.5 |

**Location**: `/home/jeremy/000-projects/nixtla/005-plugins/nixtla-baseline-lab`
**Virtual Environment**: `.venv-nixtla-baseline`

---

## Test Configuration

```
Horizon: 7 days
Series Limit: 5
Dataset: M4 Daily (4227 total series, sampled 5)
Models: SeasonalNaive, AutoETS, AutoTheta
TimeGPT: Disabled (no API key required for this test)
```

---

## Test Command

```bash
.venv-nixtla-baseline/bin/python -c "
import sys, json
sys.path.insert(0, 'scripts')
from nixtla_baseline_mcp import NixtlaBaselineMCP

server = NixtlaBaselineMCP()
result = server.run_baselines(
    horizon=7,
    series_limit=5,
    output_dir='nixtla_baseline_m4_test',
    enable_plots=False,
    dataset_type='m4',
    include_timegpt=False
)
print(json.dumps(result, indent=2))
"
```

---

## Results

### Model Performance (Average Across 5 Series)

| Model | sMAPE | MASE | Rank |
|-------|-------|------|------|
| **AutoETS** | 0.77% | 0.422 | 1st (Winner) |
| AutoTheta | 0.85% | 0.454 | 2nd |
| SeasonalNaive | 1.49% | 0.898 | 3rd (Baseline) |

### Winner Selection

**AutoETS** wins with lowest sMAPE (0.77%) - correct model selection behavior.

### Output Files Generated

| File | Size | Content |
|------|------|---------|
| `results_M4_Daily_h7.csv` | 438 bytes | Per-series metrics |
| `summary_M4_Daily_h7.txt` | 416 bytes | Human-readable summary |
| `compat_info.json` | 228 bytes | Library versions |
| `run_manifest.json` | 460 bytes | Reproducibility info |

---

## Validations Performed

1. **MCP Server Initialization** - Server created successfully
2. **M4 Data Loading** - Loaded 4227 series, sampled 5
3. **Model Execution** - All 3 models ran without errors
4. **Metrics Calculation** - sMAPE and MASE computed for all model/series combinations
5. **File Generation** - All 4 output files created
6. **Metric Ranges** - All sMAPE values in (0, 200), all MASE values > 0

---

## Raw Output (Summary)

```
Baseline Results Summary
========================

Dataset: M4 Daily
Series: 5
Horizon: 7 days

Average Metrics by Model:
------------------------------------------------------------
  AutoETS              - sMAPE:   0.77%  MASE: 0.422
  AutoTheta            - sMAPE:   0.85%  MASE: 0.454
  SeasonalNaive        - sMAPE:   1.49%  MASE: 0.898
```

---

## Conclusion

**PASS** - Baseline-lab smoke test completed successfully. The MCP server correctly:
- Loads M4 benchmark data
- Runs 3 forecasting models
- Calculates standard metrics (sMAPE, MASE)
- Identifies winning model by lowest sMAPE
- Generates reproducibility bundle

---

**Timestamp**: 2025-12-10T02:42:06Z
