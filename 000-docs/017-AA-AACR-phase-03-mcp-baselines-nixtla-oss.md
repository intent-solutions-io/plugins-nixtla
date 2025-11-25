---
doc_id: 017-AA-AACR-phase-03-mcp-baselines-nixtla-oss
title: Nixtla Baseline Lab – Phase 3 AAR (MCP + Real Nixtla Baselines)
category: After-Action Report (AA-AACR)
status: ACTIVE
classification: Project-Specific
owner: Jeremy Longshore
collaborators:
  - Max Mergenthaler (Nixtla)
related_docs:
  - 015-AA-AACR-phase-01-structure-and-skeleton.md
  - 016-AA-AACR-phase-02-manifest-and-mcp.md
  - 6767-PP-PLAN-nixtla-claude-plugin-poc-baseline-lab.md
  - 6767-OD-ARCH-nixtla-claude-plugin-poc-baseline-lab.md
  - plugins/nixtla-baseline-lab/scripts/nixtla_baseline_mcp.py
  - plugins/nixtla-baseline-lab/commands/nixtla-baseline-m4.md
  - plugins/nixtla-baseline-lab/skills/nixtla-baseline-review/SKILL.md
  - plugins/nixtla-baseline-lab/agents/nixtla-baseline-analyst.md
last_updated: 2025-11-24
---

# Phase 3 AAR – MCP + Real Nixtla Baselines

**Document ID**: 017-AA-AACR-phase-03-mcp-baselines-nixtla-oss
**Phase**: Phase 3 - MCP Server Implementation with Real Nixtla Libraries
**Status**: COMPLETE
**Date**: 2025-11-24

---

## I. Objective

Phase 3 implemented the core MCP server using real Nixtla open-source libraries to run baseline forecasting models on the M4 Daily benchmark dataset.

**Primary Goals**:
- Implement `nixtla_baseline_mcp.py` using `datasetsforecast` and `statsforecast`
- Run real baseline models: SeasonalNaive, AutoETS, AutoTheta
- Calculate real metrics: sMAPE and MASE
- Generate structured output files (CSV + summary)
- Update command/skill/agent docs with concrete behavior
- Validate implementation and record in AAR

**Success Criteria**:
- MCP server implements `run_baselines` tool with real Nixtla logic
- Server loads M4 Daily data and runs three baseline models
- Metrics CSV and summary files are generated with correct schema
- Command describes actual workflow (not stubs)
- Skill provides step-by-step analysis instructions
- Agent provides strategic analysis framework
- Code passes syntax validation

---

## II. Changes Made

### 2.1 Dependencies: `scripts/requirements.txt`

Created Python requirements file with minimal, focused dependencies:

```txt
# Nixtla forecasting libraries
statsforecast>=1.5.0
datasetsforecast>=0.0.8

# Core data science libraries
pandas>=2.0.0
numpy>=1.24.0
```

**Design Decisions**:
- Pinned to stable versions (>=) for reproducibility
- Included only what MCP server actually needs
- Commented optional dependencies (matplotlib, jupyter) for future phases
- Added header explaining purpose and usage

### 2.2 MCP Server Implementation: `scripts/nixtla_baseline_mcp.py`

Implemented complete MCP server with real Nixtla integration:

**Architecture**:
- **JSON-RPC MCP Protocol**: Handles `tools/list` and `tools/call` methods
- **Single Tool**: `run_baselines` with parameters (horizon, series_limit, output_dir)
- **Logging**: DEBUG-level logging to stderr for troubleshooting
- **Error Handling**: Graceful degradation with clear error messages

**Data Loading**:
- Uses `datasetsforecast.m4.M4.load()` to fetch M4 Daily dataset
- Stores data in `plugins/nixtla-baseline-lab/data/` directory
- Samples first `series_limit` series to control runtime
- Splits into train/test sets (last `horizon` points for testing)

**Model Execution**:
- Creates `StatsForecast` instance with three models:
  - `SeasonalNaive(season_length=7)` - weekly seasonality
  - `AutoETS(season_length=7)` - exponential smoothing
  - `AutoTheta(season_length=7)` - Theta method
- Fits on training data, forecasts `horizon` steps
- Uses parallel execution (`n_jobs=-1`) for efficiency

**Metric Calculation**:
- **sMAPE**: Symmetric Mean Absolute Percentage Error (0-200%)
  - Formula: `(100 / n) * Σ(|actual - predicted| / ((|actual| + |predicted|) / 2))`
  - Lower is better, < 15% is good for M4 Daily
- **MASE**: Mean Absolute Scaled Error (vs. naive seasonal)
  - Formula: `MAE_forecast / MAE_naive_seasonal`
  - < 1.0 means better than naive baseline

**Output Files**:
- `results_M4_Daily_h{horizon}.csv`: Full metrics table
  - Columns: `series_id`, `model`, `sMAPE`, `MASE`
  - One row per series/model combination
- `summary_M4_Daily_h{horizon}.txt`: Human-readable summary
  - Dataset info, average metrics per model, file list

**MCP Response**:
- Returns JSON with `success`, `message`, `files`, `summary`
- Summary includes average sMAPE/MASE per model for quick review

**Testing Support**:
- Includes `if __name__ == "__main__"` test mode
- Run with `python nixtla_baseline_mcp.py test` for standalone testing
- Executable (`chmod +x`) for direct invocation

**Code Quality**:
- 300+ lines, fully documented with docstrings
- Type hints on all methods
- Defensive programming (handle edge cases, validate data)
- Syntax validated with `python -m py_compile`

### 2.3 Updated Command: `commands/nixtla-baseline-m4.md`

Replaced Phase 2 stub with complete functional documentation:

**Changes**:
- Removed "Phase 2 Status: Stub" notices
- Added "How It Works" section with 6-step workflow:
  1. Load M4 Daily dataset via datasetsforecast
  2. Sample series to limit `series_limit`
  3. Split train/test (last `horizon` points as test)
  4. Run SeasonalNaive, AutoETS, AutoTheta via statsforecast
  5. Calculate sMAPE and MASE metrics
  6. Generate CSV + summary outputs
- Updated parameters with ranges (horizon: 1-60, series_limit: 1-500)
- Added concrete example: `horizon=7 series_limit=25`
- Added "Next Steps" section (interpret results, compare horizons, investigate failures)
- Added "Error Handling" section (dependencies, data download, timeouts)
- Updated documentation links to include Phase 3 AAR

### 2.4 Updated Skill: `skills/nixtla-baseline-review/SKILL.md`

Replaced stub with comprehensive step-by-step instructions:

**New Content**:
- **Step 1: Locate Results Files** - Bash commands to find CSV/summary files
- **Step 2: Load and Parse Metrics** - Read CSV, extract statistics
- **Step 3: Calculate Summary Statistics** - Mean, median, std dev per model
- **Step 4: Interpret Metrics** - Detailed sMAPE/MASE interpretation guide
  - sMAPE ranges: < 10% (good), 10-20% (acceptable), > 20% (poor)
  - MASE interpretation: < 1.0 (better than naive), > 1.0 (worse)
  - Model characteristics (SeasonalNaive, AutoETS, AutoTheta strengths)
- **Step 5: Identify Patterns** - Dominant model, consistency, failure cases
- **Step 6: Generate Structured Explanation** - Template for analysis output

**Three Complete Examples**:
1. Simple query: "Which model was best?"
2. Detailed comparison: AutoETS vs AutoTheta
3. Metric interpretation: "What does sMAPE of 12.3% mean?"

**Error Handling**:
- Missing files → guide user to run `/nixtla-baseline-m4`
- Malformed CSV → suggest re-running command

### 2.5 Updated Agent: `agents/nixtla-baseline-analyst.md`

Replaced stub with detailed strategic analysis framework:

**New Content**:
- **5-Step Workflow**:
  1. Locate and validate results (check files exist, correct schema)
  2. Load and analyze metrics (summary stats, cross-model comparison, failure analysis)
  3. Interpret findings (model strengths, performance context, consistency)
  4. Provide strategic recommendations (production selection, next experiments, investigation priorities)
  5. Document analysis (optional written report in markdown)

**Strategic Guidance**:
- Production model selection template with justification
- Next experiments prioritization (MLForecast, NeuralForecast, Ensemble, TimeGPT)
- Investigation priorities for failing series
- Complete example analysis report in markdown format

**Tool Usage**:
- Explicitly lists allowed tools: Read, Grep, Write, Bash (statistical commands)
- Clarifies NOT to use: Glob, Edit (read-only analysis)

**Output Format**:
- Summary section (2-3 sentences)
- Detailed analysis (tables, statistics, insights)
- Recommendations (actionable next steps)
- Optional written report

---

## III. Files Touched

### Created Files

- `plugins/nixtla-baseline-lab/scripts/requirements.txt` - Python dependencies
- `plugins/nixtla-baseline-lab/scripts/nixtla_baseline_mcp.py` - MCP server (300+ lines)
- `000-docs/017-AA-AACR-phase-03-mcp-baselines-nixtla-oss.md` - This AAR

### Modified Files

- `plugins/nixtla-baseline-lab/commands/nixtla-baseline-m4.md` - Replaced stub with real workflow
- `plugins/nixtla-baseline-lab/skills/nixtla-baseline-review/SKILL.md` - Added step-by-step instructions
- `plugins/nixtla-baseline-lab/agents/nixtla-baseline-analyst.md` - Added strategic analysis framework

### File Permissions

- Made `scripts/nixtla_baseline_mcp.py` executable: `chmod +x`

### Directory Structure After Phase 3

```
plugins/nixtla-baseline-lab/
├── .claude-plugin/
│   └── plugin.json              ✅ Phase 2
├── commands/
│   └── nixtla-baseline-m4.md    ✅ Updated (Phase 3)
├── agents/
│   └── nixtla-baseline-analyst.md  ✅ Updated (Phase 3)
├── skills/
│   └── nixtla-baseline-review/
│       ├── SKILL.md             ✅ Updated (Phase 3)
│       ├── references/          (empty - future)
│       └── scripts/             (empty - future)
├── .mcp.json                    ✅ Phase 2
├── scripts/
│   ├── requirements.txt         ✅ Created (Phase 3)
│   └── nixtla_baseline_mcp.py   ✅ Created (Phase 3)
├── data/                        (created on first run by datasetsforecast)
├── tests/
│   └── golden_tasks/            (empty - Phase 4+)
└── README.md                    ✅ Phase 1
```

---

## IV. Risks / Open Questions

### 4.1 M4 Dataset Download Time

**Question**: How long does initial M4 Daily dataset download take?

**Current Approach**: datasetsforecast handles download automatically to `data/` directory on first run.

**Concern**: Large dataset may cause first-run timeout (5-minute MCP timeout).

**Mitigation**:
- Start with small `series_limit` (e.g., 5-10) for testing
- User can pre-download data manually if needed
- Document in error handling: "First run may take longer due to data download"

### 4.2 Memory Usage with Large Series Limits

**Question**: What happens if user sets `series_limit=500` on a low-memory system?

**Current Approach**: statsforecast uses `n_jobs=-1` (all cores), which may amplify memory usage.

**Mitigation**:
- Documented reasonable max (500 series)
- If memory issues occur in Phase 4 testing, reduce default or add memory checks
- Consider adding `n_jobs` parameter for user control

### 4.3 Metric Calculation Accuracy

**Assumption**: Custom sMAPE and MASE implementations match Nixtla's internal calculations.

**Validation Needed**: Compare results with official Nixtla benchmarks to ensure consistency.

**Next Steps**: In Phase 4, run golden task comparing our metrics with published M4 results.

### 4.4 Seasonal Length Assumption

**Current Setting**: All models use `season_length=7` (weekly pattern for daily data).

**Question**: Is this appropriate for all M4 Daily series?

**Context**: M4 Daily may have diverse patterns (some weekly, some monthly, some irregular).

**Future Enhancement**: Could add auto-detection of seasonality or let user specify.

**Phase 3 Decision**: Use 7 as reasonable default per Nixtla examples.

### 4.5 Timeout Appropriateness

**Current MCP Timeout**: 5 minutes (300,000ms) from Phase 2.

**Testing Needed**: Measure actual runtime with varying `series_limit` values.

**Hypothesis**:
- 10 series: < 30 seconds
- 50 series: 1-2 minutes
- 500 series: 4-6 minutes (may exceed timeout)

**Phase 4 Action**: Benchmark and adjust timeout if needed.

---

## V. Ready for Next Phase Checklist

### Phase 3 Deliverables ✅

- [x] MCP server (`nixtla_baseline_mcp.py`) implements `run_baselines` tool
- [x] Server uses real `datasetsforecast` to load M4 Daily data
- [x] Server uses real `statsforecast` to run SeasonalNaive, AutoETS, AutoTheta
- [x] Server calculates real sMAPE and MASE metrics
- [x] Server writes `results_*.csv` and `summary_*.txt` files
- [x] Server returns structured JSON response
- [x] Code syntax validated (`python -m py_compile`)
- [x] Command documentation updated with real workflow
- [x] Skill documentation includes step-by-step instructions
- [x] Agent documentation includes strategic analysis framework
- [x] Requirements file created with minimal dependencies
- [x] MCP server made executable (`chmod +x`)
- [x] Phase 3 AAR documented

### Phase 4 Prerequisites ✅

- [x] MCP server is syntactically correct
- [x] Command/skill/agent describe actual behavior (not stubs)
- [x] Clear output schema documented (CSV columns, summary format)
- [x] Error handling defined (missing deps, timeouts, malformed data)
- [x] Testing approach outlined (start small, validate metrics)

### Phase 4 Readiness Assessment

**Status**: READY TO PROCEED (with caveats)

**Can Proceed Immediately**:
- MCP server code is complete and syntactically valid
- Documentation fully updated
- Clear testing strategy defined

**Prerequisites for Live Testing**:
1. Install Python dependencies: `pip install -r scripts/requirements.txt`
2. Verify datasetsforecast can download M4 data
3. Test with small `series_limit` first (e.g., 5 series)
4. Validate CSV output matches schema

**Phase 4 Will Focus On**:
- End-to-end testing with real plugin loading
- Golden task creation and validation
- Benchmark runtime and adjust timeouts if needed
- Compare metrics with published M4 results
- Create test cases for skill and agent invocations

### Remaining Phases (Not Started)

- [ ] Phase 4: Testing, validation, golden tasks
- [ ] Phase 5: Handoff documentation, marketplace polish

---

## VI. Lessons Learned

### What Went Well

1. **Architecture Doc as Blueprint**: 6767-OD-ARCH provided excellent MCP server template
2. **Incremental Complexity**: Started with imports, built up to full workflow
3. **Real Libraries First**: Using actual Nixtla libraries (not mocks) ensures accurate behavior
4. **Comprehensive Documentation**: Command/skill/agent now provide clear guidance
5. **Test Mode Support**: `python script.py test` enables standalone debugging
6. **Defensive Programming**: Error handling for missing deps, malformed data prevents crashes

### What Could Improve

1. **Metric Validation**: Should verify our sMAPE/MASE calculations match Nixtla's official implementation
2. **Performance Benchmarking**: Need actual runtime measurements before finalizing timeout
3. **Edge Case Testing**: Should test with very short series, missing data, extreme outliers
4. **Dependency Lock**: Could create `requirements.lock` for exact reproducibility

### Discoveries During Implementation

1. **M4 API**: `M4.load()` returns tuple, need to unpack first element for DataFrame
2. **Train/Test Split**: Must handle series shorter than horizon gracefully
3. **Forecast Format**: StatsForecast returns forecasts in different format depending on model
4. **MASE Edge Case**: Need to handle train series shorter than season_length

### Recommendations for Future Phases

1. **Phase 4 Testing**:
   - Start with `series_limit=3` to validate full workflow quickly
   - Compare sMAPE/MASE output with published M4 benchmarks
   - Test error cases: missing deps, corrupted data, timeout scenarios
   - Create golden task with known-good inputs and expected outputs

2. **Phase 5 Polish**:
   - Add visualization support (matplotlib plots)
   - Implement Jupyter notebook generation
   - Add more models (MLForecast, NeuralForecast) if time permits
   - Create video tutorial for Nixtla community

3. **Production Deployment**:
   - Document system requirements (RAM, CPU)
   - Provide Docker container for reproducibility
   - Add monitoring/logging hooks
   - Create troubleshooting guide

---

## VII. Technical Implementation Notes

### Metric Calculation Details

**sMAPE Implementation**:
```python
def _calculate_smape(actual, predicted):
    numerator = np.abs(actual - predicted)
    denominator = (np.abs(actual) + np.abs(predicted)) / 2.0
    # Avoid division by zero
    denominator = np.where(denominator == 0, 1e-10, denominator)
    return 100.0 * np.mean(numerator / denominator)
```

**MASE Implementation**:
```python
def _calculate_mase(actual, predicted, train_series, season_length=7):
    mae_forecast = np.mean(np.abs(actual - predicted))

    # Seasonal naive on training data
    if len(train_series) > season_length:
        naive_errors = np.abs(train_series[season_length:] - train_series[:-season_length])
    else:
        naive_errors = np.abs(np.diff(train_series))

    mae_naive = np.mean(naive_errors)
    return mae_forecast / max(mae_naive, 1e-10)
```

### Data Flow Through MCP Server

1. Claude invokes MCP tool: `{"method": "tools/call", "params": {"name": "run_baselines", "arguments": {...}}}`
2. Server parses parameters: `horizon=14, series_limit=50, output_dir="nixtla_baseline_m4"`
3. Load M4 Daily: `df, *_ = M4.load(directory="data/", group="Daily")`
4. Sample series: `df_sample = df[df['unique_id'].isin(unique_ids[:series_limit])]`
5. Split train/test: Last `horizon` points for testing
6. Create models: `[SeasonalNaive(7), AutoETS(7), AutoTheta(7)]`
7. Fit and forecast: `forecasts = sf.forecast(df=df_train, h=horizon)`
8. Calculate metrics: Loop through series/models, compute sMAPE and MASE
9. Write outputs: `results_*.csv` and `summary_*.txt`
10. Return response: `{"success": true, "files": [...], "summary": {...}}`

---

## VIII. Git Commit Message

```
Phase 3: implement nixtla-baseline MCP with real Nixtla baselines

Added MCP server using datasetsforecast M4 and statsforecast baselines:
- scripts/nixtla_baseline_mcp.py: Full MCP server (300+ lines)
- Uses real M4 Daily data, runs SeasonalNaive/AutoETS/AutoTheta
- Calculates sMAPE and MASE metrics, writes CSV + summary files
- scripts/requirements.txt: Python dependencies (statsforecast, datasetsforecast)

Updated command, skill, and agent docs to describe real baseline workflow:
- commands/nixtla-baseline-m4.md: Complete workflow documentation
- skills/nixtla-baseline-review/SKILL.md: Step-by-step analysis instructions
- agents/nixtla-baseline-analyst.md: Strategic analysis framework

Recorded Phase 3 AAR for MCP + Nixtla OSS integration.

Related: 6767-PP-PLAN, 6767-OD-ARCH, 016-AA-AACR
```

---

## IX. Next Steps

**Immediate**: Await explicit approval to proceed to Phase 4

**Phase 4 Focus**:
- Install Nixtla dependencies: `pip install -r scripts/requirements.txt`
- Test MCP server in standalone mode: `python scripts/nixtla_baseline_mcp.py test`
- Validate plugin loads in Claude Code
- Create golden task with known inputs/outputs
- Benchmark runtime with various `series_limit` values
- Test skill and agent invocations end-to-end
- Compare metrics with published M4 benchmarks
- Adjust timeouts if needed
- Document any issues or edge cases

**Phase 4 Success Criteria**:
- Plugin loads without errors in Claude Code
- `/nixtla-baseline-m4` command executes successfully
- Metrics match expected ranges from M4 literature
- Skill correctly analyzes results
- Agent provides strategic recommendations
- Golden task validates full workflow
- All tests pass

---

**AAR Version**: 1.0.0
**Completed**: 2025-11-24
**Author**: Jeremy Longshore (jeremy@intentsolutions.io)
**Reviewed By**: Pending (Max Mergenthaler)
