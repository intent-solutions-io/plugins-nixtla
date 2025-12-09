# Phase 08 AAR: Cross-Lab Benchmark - TimeGPT vs StatsForecast

**Generated**: 2025-12-08
**Phase**: 08 - Cross-Lab Benchmark Report
**Status**: ✅ Complete
**Type**: After-Action Review (AA-AACR)

---

## Objective

Create a manual aggregator system that compares TimeGPT experiment results against StatsForecast baseline results, generating CEO-friendly comparison reports without re-running experiments.

## What We Built

### 1. Comparison Aggregator Script

**Location**: `004-scripts/compare_timegpt_vs_statsforecast.py` (473 lines)

**Key Design**: Asymmetric dependency handling
- **TimeGPT results**: REQUIRED (hard error if missing, exit code 1)
- **StatsForecast results**: OPTIONAL (warning if missing, TimeGPT-only report, exit code 0)

**Core Functions**:
```python
def check_timegpt_results():
    """REQUIRED: Returns False and prints error if missing"""
    if not TIMEGPT_RESULTS_CSV.exists():
        print("ERROR: TimeGPT Experiments Results Not Found")
        return False
    return True

def check_statsforecast_results():
    """OPTIONAL: Returns False and prints warning if missing"""
    if not STATSFORECAST_RESULTS_CSV.exists():
        print("WARNING: StatsForecast Baseline Results Not Found")
        print("Proceeding with TimeGPT-only report.")
        return False
    return True

def main():
    # TimeGPT missing → exit 1 (hard error)
    if not check_timegpt_results():
        return 1

    # StatsForecast missing → proceed with warning, exit 0
    has_statsforecast = check_statsforecast_results()

    # Generate appropriate report based on available data
    write_markdown_report(df_combined, agg_metrics, has_statsforecast)
    return 0
```

**Data Normalization**:
```python
# TimeGPT CSV schema
experiment_name,unique_id,horizon,eval_window,mae,smape,runtime_seconds

# StatsForecast CSV schema
unique_id,model,horizon,smape,mae

# Normalized to common schema
source,model,series_id,horizon,mae,smape
```

**Exit Codes**:
- `0`: Success (full comparison or TimeGPT-only partial report)
- `1`: TimeGPT results missing (hard error)
- `2`: Parse or processing error

### 2. Dual Output System

**CSV Output**: `004-scripts/compare_outputs/timegpt_vs_statsforecast_metrics.csv`
- Technical format for further analysis
- Combined raw metrics from both labs
- Schema: `source,model,series_id,horizon,mae,smape`

**Markdown Report**: `000-docs/091-RA-REPT-timegpt-vs-statsforecast-baseline.md`
- CEO-friendly comparison report
- Executive summary (2-3 sentences)
- Clear PENDING status when StatsForecast not run
- "How to Reproduce" section for transparency

### 3. First-Class "Pending" State

**When StatsForecast baseline not run**, the report includes:

```markdown
## StatsForecast Baseline Status

**Status**: PENDING

No StatsForecast baseline CSV found at:
```
002-workspaces/statsforecast-lab/reports/statsforecast_baseline_results.csv
```

**To generate baseline metrics**:
```bash
cd 002-workspaces/statsforecast-lab
python scripts/run_statsforecast_baseline.py
```

Once baseline results exist, re-run:
```bash
python 004-scripts/compare_timegpt_vs_statsforecast.py
```
```

**When both labs have results**, the report includes:
- Comparative analysis table
- Best models by metric (lowest sMAPE, lowest MAE)
- Full comparison across both sources

## Test Results

**Initial Run (TimeGPT-only mode)**:
```
✓ Comparison Complete: PARTIAL (TimeGPT only)

Outputs:
  - CSV: 004-scripts/compare_outputs/timegpt_vs_statsforecast_metrics.csv
  - Report: 000-docs/091-RA-REPT-timegpt-vs-statsforecast-baseline.md

Next steps:
  1. Run StatsForecast baseline: cd 002-workspaces/statsforecast-lab && python scripts/run_statsforecast_baseline.py
  2. Re-run this script for full comparison
```

**TimeGPT Results Summary**:
| Model | Horizon | Avg sMAPE | Avg MAE |
|-------|---------|-----------|---------|
| timegpt_baseline_14d | 14d | 3.11% | 6.22 |
| timegpt_baseline_28d | 28d | 5.83% | 11.16 |

**StatsForecast Status**: PENDING (baseline not run yet)

## Critical Design Decisions

### 1. Never Fabricate Baseline Results

**Principle**: Treat "baseline not run yet" as a first-class state, NOT an error.

**User directive**:
> "We don't generate fake StatsForecast numbers. We treat 'baseline not run yet' as a first-class state."

**Implementation**: Script only reads real CSVs, never generates synthetic data.

### 2. Asymmetric Dependency Model

**TimeGPT (required)**:
- User must run experiments first (requires API key)
- Missing results → hard error, exit 1
- Rationale: No comparison possible without at least one data source

**StatsForecast (optional)**:
- Baseline can be run later (no API key, local-only)
- Missing results → warning, partial report, exit 0
- Rationale: TimeGPT-only report still provides value

### 3. No Automatic Re-Runs

**Manual aggregation only**:
- Script reads existing CSVs
- Never calls TimeGPT API
- Never re-runs StatsForecast models
- Rationale: CEO wants to see results, not burn API credits or compute time

### 4. Doc-Filing v4.2 Compliance

**Report location**: `000-docs/091-RA-REPT-timegpt-vs-statsforecast-baseline.md`
- `091`: Next sequential number after `090-AA-AACR-phase-07-statsforecast-lab-bootstrap.md`
- `RA-REPT`: Research Analysis Report (comparison study)
- Generated automatically by aggregator script

**AAR location**: `000-docs/092-AA-AACR-phase-08-cross-lab-benchmark.md`
- `092`: Next sequential number
- `AA-AACR`: After-Action Review

## Files Created/Modified

### New Files
1. `004-scripts/compare_timegpt_vs_statsforecast.py` (473 lines)
   - Main aggregator with asymmetric handling
   - Data normalization layer
   - Dual output generation (CSV + Markdown)

2. `004-scripts/compare_outputs/timegpt_vs_statsforecast_metrics.csv` (6 lines)
   - Combined metrics from TimeGPT lab
   - Currently 4 result rows (2 experiments × 2 series)

3. `000-docs/091-RA-REPT-timegpt-vs-statsforecast-baseline.md` (68 lines)
   - Auto-generated comparison report
   - Currently in TimeGPT-only mode with PENDING status

4. `000-docs/092-AA-AACR-phase-08-cross-lab-benchmark.md` (this file)
   - Phase 08 after-action review

### Modified Files
None (aggregator reads existing files, doesn't modify them)

## Lessons Learned

### What Worked Well
1. **Asymmetric handling** - Treating optional vs required dependencies differently makes the tool more useful
2. **Clear user messaging** - Explicit PENDING status vs vague "not found" errors
3. **Exit code discipline** - Exit 0 for partial success maintains CI/CD compatibility
4. **No auto-runs** - Manual aggregation avoids surprise API charges

### What Could Be Improved
1. **Lab README updates** - Should add cross-comparison section to both lab READMEs (deferred)
2. **Metric validation** - Could add sanity checks (e.g., sMAPE > 200% indicates error)
3. **Historical tracking** - Could archive previous comparison reports for trend analysis

### Critical User Feedback Incorporated
**User correction**: "We don't generate fake StatsForecast numbers"
- **Impact**: Changed from "error when missing" to "pending state when missing"
- **Implementation**: `has_statsforecast` boolean flag drives report content
- **Result**: Tool is useful even before baseline run

## Integration Points

### Upstream Dependencies (Input CSVs)
1. **TimeGPT Lab**: `002-workspaces/timegpt-lab/reports/timegpt_experiments_results.csv`
   - Generated by: `002-workspaces/timegpt-lab/scripts/run_experiment.py`
   - Status: ✅ Exists (4 rows from Phase 05/06)

2. **StatsForecast Lab**: `002-workspaces/statsforecast-lab/reports/statsforecast_baseline_results.csv`
   - Generated by: `002-workspaces/statsforecast-lab/scripts/run_statsforecast_baseline.py`
   - Status: ❌ Not run yet (PENDING)

### Downstream Outputs
1. **Technical CSV**: `004-scripts/compare_outputs/timegpt_vs_statsforecast_metrics.csv`
   - For further analysis, plotting, or data science workflows

2. **Executive Report**: `000-docs/091-RA-REPT-timegpt-vs-statsforecast-baseline.md`
   - For CEO presentation, stakeholder updates, business decisions

## Usage Workflow

### Typical Flow
```bash
# 1. Run TimeGPT experiments (requires API key)
cd 002-workspaces/timegpt-lab
export NIXTLA_TIMEGPT_API_KEY='your_key_here'
python scripts/run_experiment.py

# 2. (Optional) Run StatsForecast baselines (local, no API)
cd 002-workspaces/statsforecast-lab
python scripts/run_statsforecast_baseline.py

# 3. Generate comparison report
cd /home/jeremy/000-projects/nixtla
python 004-scripts/compare_timegpt_vs_statsforecast.py
# → Creates 091-RA-REPT-timegpt-vs-statsforecast-baseline.md

# 4. Review outputs
cat 000-docs/091-RA-REPT-timegpt-vs-statsforecast-baseline.md
```

### Re-Run After Baseline Completion
```bash
# After StatsForecast baseline is run, simply re-run aggregator
python 004-scripts/compare_timegpt_vs_statsforecast.py

# Report automatically upgrades from "PENDING" to "FULL COMPARISON"
# Includes comparative analysis, best model rankings, etc.
```

## Success Criteria: Met ✅

- [x] Aggregator script reads existing CSVs only (no auto-runs)
- [x] TimeGPT results missing → hard error, exit 1
- [x] StatsForecast results missing → warning, TimeGPT-only report, exit 0
- [x] Dual outputs: CSV (technical) + Markdown (CEO-friendly)
- [x] Clear PENDING status when baseline not run
- [x] Never fabricates or simulates data
- [x] Normalizes metrics across both labs
- [x] Generates reproducible outputs
- [x] Doc-Filing v4.2 compliant (091-RA-REPT, 092-AA-AACR)
- [x] Script runs successfully in TimeGPT-only mode

## Next Steps (Optional)

### Immediate (Phase 08 Complete)
None required - aggregator is fully functional.

### Future Enhancements (Not Blocking)
1. Update lab READMEs with cross-comparison section
2. Add metric sanity validation (sMAPE range checks)
3. Create historical comparison archive
4. Add plotting utilities for visual comparison

### Proceed to Phase 09
Once Phase 08 is committed:
- Create `.github/workflows/timegpt-real-smoke.yml`
- Weekly scheduled CI job with real API calls
- GitHub Actions secret management
- See Phase 09 prompt for details

---

**Phase 08 Status**: ✅ COMPLETE
**Blocking Issues**: None
**Ready for Commit**: Yes
**Ready for Phase 09**: Yes

**Last Updated**: 2025-12-08
**Owner**: jeremy@intentsolutions.io
