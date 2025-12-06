# Nixtla Baseline Lab – Test Coverage Report

**Plugin**: nixtla-baseline-lab
**Version**: 0.6.0
**Date**: 2025-11-25
**Status**: ✅ **VALIDATED**

---

## Executive Summary

This document maps the test plan to the actual implementation, confirming that all critical paths are properly tested, logged, and wired into CI.

**Key Findings**:
- ✅ Baseline M4 path is CI-verified and stable
- ✅ CSV "bring your own data" path is validated with example data
- ✅ Visualization path (PNG plots) is validated
- ✅ TimeGPT is safely gated with structured status codes and graceful degradation
- ✅ CI uploads artifacts with clear step labels
- ✅ Golden task harness provides visual progress indicators and strict exit codes

---

## 1. Logging & Observability

### Python Scripts

**`nixtla_baseline_mcp.py`**:
- **Logger**: `logging.getLogger(__name__)`
- **Level**: `DEBUG` (via `basicConfig`)
- **Format**: `'%(asctime)s - %(name)s - %(levelname)s - %(message)s'`
- **Stream**: `sys.stderr`

**Key Logging Points**:
- `INFO`:
  - Starting runs
  - Dataset type (`m4` vs `csv`)
  - Dataset loading and sampling
  - Model fitting and metrics computation
  - File writing (CSV, summary, plots, showdown reports)
- `WARNING`:
  - TimeGPT requested but `NIXTLA_TIMEGPT_API_KEY` not set
  - Optional features (plots / TimeGPT) skipped when prerequisites missing
- `ERROR`:
  - Missing libraries
  - Invalid dataset type
  - CSV validation failures
  - TimeGPT client errors
  - Unexpected exceptions (`exc_info=True` for stack traces)

**`timegpt_client.py`**:
- **Logger**: `logging.getLogger(__name__)`
- **Key Messages**:
  - `INFO`: Whether API key is detected or not
  - `ERROR`: Import errors or TimeGPT API failures, wrapped in friendly messages

**`run_baseline_m4_smoke.py`** (Golden Task Harness):
- Uses `print()` with visual markers instead of `logging`:
  - `[1/5]`, `[2/5]`, … for step progress
  - `✓` for success
  - `⚠️` for warnings
  - `FAIL:` prefix on failures
- Exit codes:
  - `0` for full pass
  - `1` for any validation failure

### CI Workflow

**`.github/workflows/nixtla-baseline-lab-ci.yml`**:
- **Step Labels**: Clear, human-readable ("Set up Python", "Install Nixtla OSS deps", "Run MCP test", "Run golden task harness")
- **Echo Statements**: "Installing…", "Running…", etc. for quick skim of logs
- **Package Versions**:
  - Prints versions for: `statsforecast`, `datasetsforecast`, `pandas`, `numpy`, `matplotlib`, `nixtla`
- **Artifact Upload**:
  - Uses `if: always()` so artifacts are uploaded even if earlier steps fail
  - Retention: 7 days for test results

---

## 2. Test Matrix Coverage

### Baseline / Core Tests

| ID     | Test                    | Status | CI | Manual | Verified |
|--------|-------------------------|--------|----|--------|----------|
| BL-001 | Setup script basic      | ✅     | ❌ | ✅      | ✅        |
| BL-002 | MCP test (M4)           | ✅     | ✅ | ✅      | ✅        |
| BL-003 | Golden task default     | ✅     | ✅ | ✅      | ✅        |
| BL-004 | Error handling (baseline) | ✅   | ❌ | ✅      | ✅        |

**BL-001: Setup Script Basic**
- **Location**: `plugins/nixtla-baseline-lab/scripts/setup_nixtla_env.sh`
- **Behavior**:
  - Validates Python + `pip`
  - Installs all required packages:
    - `statsforecast`, `datasetsforecast`, `pandas`, `numpy`, `matplotlib`, `nixtla`
  - Color-coded terminal output (`GREEN`, `YELLOW`, `RED`)
  - Prints package versions for verification
- **Exit**: Returns code `0` on success

**BL-002: MCP Test (M4)**
- **Location**: `plugins/nixtla-baseline-lab/scripts/nixtla_baseline_mcp.py test`
- **Behavior**:
  - Loads M4 Daily subset (5 series)
  - Runs SeasonalNaive, AutoETS, AutoTheta with `horizon=7`
  - Computes sMAPE and MASE
  - Writes:
    - `results_M4_Daily_h7.csv`
    - `summary_M4_Daily_h7.txt`
- **Output**: JSON with `success: true`, `files: [...]`, `summary: {...}`
- **Artifacts**: Files created under `nixtla_baseline_m4_test/`
- **Status**: ✅ Verified locally and via CI

**BL-003: Golden Task Default**
- **Location**: `plugins/nixtla-baseline-lab/tests/run_baseline_m4_smoke.py`
- **Behavior**:
  - `[1/5]` Runs MCP test with default arguments (M4, horizon=7, series_limit=5)
  - `[2/5]` Verifies output directory exists
  - `[3/5]` Validates CSV schema and row count (≥ 15 rows for 5 series × 3 models)
  - `[4/5]` Validates summary contents
  - `[5/5]` Final sanity checks
- **Output**: `GOLDEN TASK PASSED` and exit code `0` when all checks pass
- **CI**: ✅ Runs on every push/PR to main

**BL-004: Error Handling (Baseline)**
- **Scenarios**:
  - Missing required libraries → JSON with `success: false` and `"Missing required library: ..."`
  - Invalid dataset type → JSON with `success: false` and clear message
  - Unexpected errors → logged at `ERROR` with stack trace; surfaced as failure in golden harness
- **Status**: ✅ Verified manually

---

### CSV / Custom Data Tests

| ID      | Test                  | Status | CI | Manual | Verified |
|---------|-----------------------|--------|----|--------|----------|
| CSV-001 | CSV happy path        | ✅     | ❌ | ✅      | ✅        |
| CSV-002 | CSV missing columns   | ✅     | ❌ | ✅      | ⚠️        |
| CSV-003 | CSV bad path          | ✅     | ❌ | ✅      | ✅        |

**CSV-001: CSV Happy Path**
- **Command** (example):
  ```bash
  cd plugins/nixtla-baseline-lab
  python3 tests/run_baseline_m4_smoke.py \
    --dataset-type csv \
    --csv-path tests/data/example_timeseries.csv \
    --horizon 5 \
    --series-limit 2 \
    --output-dir nixtla_test_custom
  ```
- **Data**: `tests/data/example_timeseries.csv` (3 series × 21 days, columns: `unique_id`, `ds`, `y`)
- **Expected**:
  - Output directory `nixtla_test_custom/`
  - `results_Custom_h5.csv` with at least 6 rows (2 series × 3 models)
  - `summary_Custom_h5.txt` with dataset label "Custom CSV" and per-model metrics
- **Status**: ✅ Verified per Phase 7 execution

**CSV-002: CSV Missing Columns**
- **Behavior**:
  - If required columns (`unique_id`, `ds`, `y`) are missing:
    - MCP returns `success: false`
    - `message` lists missing columns
  - Golden harness reports the failure and exits with code `1`
- **Status**: ⚠️ Logic implemented; no dedicated malformed CSV fixture checked into `tests/data/` yet

**CSV-003: CSV Bad Path**
- **Command**:
  ```bash
  python3 tests/run_baseline_m4_smoke.py \
    --dataset-type csv \
    --csv-path /nonexistent/foo.csv
  ```
- **Output**:
  - `FAIL: MCP test reported failure. Message: CSV file not found: /nonexistent/foo.csv`
  - Exit code `1`
- **Status**: ✅ Verified

---

### Visualization Tests

| ID     | Test                  | Status | CI | Manual | Verified |
|--------|-----------------------|--------|----|--------|----------|
| PLOT-001| Plots enabled, libs OK| ✅     | ❌ | ✅      | ✅        |
| PLOT-002| Plots with missing matplotlib| ✅| ❌ | ✅      | ⚠️        |

**PLOT-001: Plots Enabled**
- **Command**:
  ```bash
  cd plugins/nixtla-baseline-lab
  python3 scripts/nixtla_baseline_mcp.py test --enable-plots
  ```
- **Behavior**:
  - Uses matplotlib with Agg backend
  - Generates PNG files (e.g., `plot_series_D1.png`, `plot_series_D10.png`)
  - Adds them to the `files` array in JSON output
  - Sets `plots_generated` in the result
- **Status**: ✅ Verified (plots generated successfully; PNG sizes ~50–80 KB)

**PLOT-002: Missing Matplotlib**
- **Behavior**:
  - Plotting code is wrapped in `try/except ImportError`
  - If matplotlib is missing:
    - Logs a `WARNING` and returns an empty list of plots
    - Baseline forecast run continues and succeeds
- **Status**: ⚠️ Behavior implemented; explicit "no matplotlib installed" scenario not scripted as a separate test yet

---

### TimeGPT Tests

| ID    | Test                    | Status | CI | Manual | Verified |
|-------|-------------------------|--------|----|--------|----------|
| TG-001| TimeGPT disabled        | ✅     | ✅ | ✅      | ✅        |
| TG-002| include_timegpt, no key | ✅     | ❌ | ✅      | ✅        |
| TG-003| include_timegpt, bad key| ✅     | ❌ | ✅      | ⚠️        |
| TG-004| include_timegpt, valid key| ✅   | ❌ | ⚠️      | ⚠️        |
| TG-005| Skill reads showdown    | ✅     | ❌ | ⚠️      | ⚠️        |

**TG-001: TimeGPT Disabled (Regression)**
- **Behavior**:
  - Default use (no `include_timegpt` flag) behaves exactly like Phase 7
  - No `timegpt_*` fields appear in JSON
- **CI**: ✅ All CI runs use this path
- **Status**: ✅ Verified

**TG-002: include_timegpt with No API Key**
- **Command**:
  ```bash
  cd plugins/nixtla-baseline-lab
  unset NIXTLA_TIMEGPT_API_KEY
  python3 tests/run_baseline_m4_smoke.py --include-timegpt
  ```
- **Expected**:
  - Prints: `⚠️ TimeGPT requested but API key not found - will skip TimeGPT checks`
  - Under the hood: MCP returns `timegpt_status: "skipped_no_api_key"`
  - Golden task still prints `GOLDEN TASK PASSED` and exits with `0`
- **Status**: ✅ Verified

**TG-003: include_timegpt with Invalid API Key**
- **Expected**:
  - Baseline `success: true`
  - `timegpt_status: "error"`
  - Message is a user-friendly error from the TimeGPT client (no raw trace)
- **Status**: ⚠️ Logic is present; requires deliberate run with an invalid key (would hit real API)

**TG-004: include_timegpt with Valid API Key**
- **Expected**:
  - JSON includes:
    - `timegpt_summary` (avg metrics, winner)
    - `timegpt_per_series` (per-series comparison)
    - `timegpt_showdown_file` (path to showdown TXT)
  - Showdown file contains:
    - Dataset label
    - Horizon
    - Number of series compared
    - Per-series winners
    - Overall winner
    - Explicit disclaimer about small sample size
- **Status**: ⚠️ Requires a real TimeGPT key and paid API calls to verify end-to-end

**TG-005: Skill Reads Showdown**
- **Behavior**:
  - Skill (`nixtla-baseline-review/SKILL.md`) is instructed to:
    - Look for `timegpt_showdown_*.txt`
    - Summarize TimeGPT vs baseline performance if present
    - Emphasize limited sample size and "illustrative, not benchmark" framing
- **Status**: ⚠️ Needs explicit manual test in Claude Code with a generated showdown file

---

### Marketplace Tests

| ID    | Test                    | Status | CI | Manual | Verified |
|-------|-------------------------|--------|----|--------|----------|
| MP-001| Marketplace + plugin install| ✅  | ❌ | ⚠️      | ⚠️        |

**MP-001: Marketplace + Plugin Install**
- **Configuration**:
  - `.claude-plugin/marketplace.json` describes `nixtla-baseline-lab`
  - `.claude/settings.json` registers `nixtla-dev-marketplace` pointing to this repo
- **Expected Flow in Claude Code**:
  1. User clones repo
  2. User trusts repo folder
  3. Claude auto-registers `nixtla-dev-marketplace` from `.claude/settings.json`
  4. User installs plugin:
     ```
     /plugin install nixtla-baseline-lab@nixtla-dev-marketplace
     ```
- **Status**: ⚠️ Wiring is correct on disk; requires a quick manual install smoke test

---

## 3. TimeGPT Status Code Mapping

TimeGPT handling is non-breaking and fully structured:

| Scenario | Status Code | Message Field | Exit Code |
|----------|-------------|---------------|-----------|
| TimeGPT disabled (default) | (field absent) | N/A | 0 |
| Flag set, no API key | `"skipped_no_api_key"` | `"NIXTLA_TIMEGPT_API_KEY environment variable not set"` | 0 |
| Flag set, import error | `"error"` | `"Missing TimeGPT dependencies: {e}"` | 0 |
| Flag set, invalid key/API error | `"error"` | User-friendly message from TimeGPT client wrapper | 0 |
| Flag set, success | `"ok"` | Showdown data populated (JSON + TXT) | 0 |

**Design Principle**: TimeGPT can never cause the baseline path to fail. As long as baselines succeed, the overall process exits with `0`; TimeGPT is additive, not required.

---

## 4. CI Verification

### Current CI Coverage

**Workflow**: `.github/workflows/nixtla-baseline-lab-ci.yml`

**Triggers**:
- Push to `main` (paths: `plugins/nixtla-baseline-lab/**`, or the workflow YAML)
- Pull requests targeting `main` that touch those paths

**Steps**:
1. ✅ Checkout repository
2. ✅ Set up Python 3.12 with pip caching
3. ✅ Install dependencies from `scripts/requirements.txt`
4. ✅ Print installed package versions (including `nixtla` and `matplotlib`)
5. ✅ Run MCP test (`python scripts/nixtla_baseline_mcp.py test`)
6. ✅ Run golden task harness (`python tests/run_baseline_m4_smoke.py`)
7. ✅ Upload test artifacts (always, even on failure)

**Artifacts**:
- **Name**: `nixtla-baseline-test-results`
- **Path**: `plugins/nixtla-baseline-lab/nixtla_baseline_m4_test/`
- **Retention**: 7 days

### What CI Tests

✅ **Covered in CI**:
- Baseline M4 forecast path (3 models × 5 series)
- Output directory creation
- CSV schema and row-count checks
- Summary file creation and basic content checks
- Golden task pass/fail control via exit codes
- Package install sanity (including `nixtla` and `matplotlib`)

❌ **Not Covered in CI** (by design):
- TimeGPT API calls (requires paid key)
- Custom CSV runs (covered manually via `example_timeseries.csv`)
- Plotting under no-matplotlib environment
- Claude Code marketplace integration

---

## 5. Gaps and Recommendations

### Low-Priority Gaps (Optional Enhancements)

1. **Malformed CSV Fixture (CSV-002)**
   - Add a dedicated malformed CSV (e.g., missing `ds`) under `tests/data/`
   - Wire up a short harness run that expects a specific "missing columns" error

2. **Explicit "No Matplotlib" Test (PLOT-002)**
   - Add a script or documented procedure to run without matplotlib installed
   - Capture and document the warning + behavior

3. **TimeGPT Edge-Case Tests (TG-003/004/005)**
   - One test with an invalid key (to exercise the error path)
   - One controlled test with a valid key to generate a real showdown file
   - Have the Skill consume that showdown file and summarize it

4. **Marketplace Smoke Test (MP-001)**
   - Run a one-time manual test in Claude Code:
     - Trust repo → install via marketplace → run baseline once
   - Capture that as a short note or AAR snippet

### Medium-Term Recommendations

1. **Test IDs in Logs**
   - Prefix selected log lines with IDs like `[BL-002]`, `[CSV-001]` to align logs with this report

2. **Structured Logs (Optional)**
   - Offer an environment flag to emit JSON logs for deeper CI/system integration

3. **Automated Coverage Report**
   - Add a script that runs `run_baseline_m4_smoke.py` and regenerates this markdown report automatically

4. **Mocked TimeGPT Client for CI**
   - Add a test mode that swaps in a fake TimeGPT client so CI can cover "ok" and "error" paths without real API calls

### Current Assessment

**Overall Status**: ✅ **PRODUCTION-READY**

The plugin currently has:
- ✅ Robust error handling with structured statuses
- ✅ Clear, actionable logging
- ✅ CI coverage for all critical OSS baseline functionality
- ✅ Validated CSV and plotting paths
- ✅ Safe, opt-in TimeGPT add-on with graceful degradation
- ✅ Golden task harness that enforces correctness and provides human-friendly output
- ✅ CI artifacts for debugging when things go wrong

**For Nixtla review**, the core baseline + CSV + visualization flows are stable and well-tested, with TimeGPT and marketplace integrations wired, documented, and ready for further validation as needed.

---

## 6. Test Execution Evidence (2025-11-25)

**BL-002: MCP Test (M4)**
```bash
cd plugins/nixtla-baseline-lab
python3 scripts/nixtla_baseline_mcp.py test
# Output: JSON with success: true, CSV + summary written to nixtla_baseline_m4_test/
```

**BL-003: Golden Task Default**
```bash
python3 tests/run_baseline_m4_smoke.py
# Output: GOLDEN TASK PASSED
# Exit code: 0
```

**CSV-001: CSV Happy Path**
```bash
python3 tests/run_baseline_m4_smoke.py \
  --dataset-type csv \
  --csv-path tests/data/example_timeseries.csv \
  --horizon 5 \
  --series-limit 2 \
  --output-dir nixtla_test_custom
# Output: GOLDEN TASK PASSED
# Exit code: 0
```

**CSV-003: CSV Bad Path**
```bash
python3 tests/run_baseline_m4_smoke.py \
  --dataset-type csv \
  --csv-path /nonexistent/foo.csv
# Output: FAIL: CSV file not found: /nonexistent/foo.csv
# Exit code: 1
```

**TG-002: TimeGPT No API Key**
```bash
unset NIXTLA_TIMEGPT_API_KEY
python3 tests/run_baseline_m4_smoke.py --include-timegpt
# Output: ⚠️ TimeGPT requested but API key not found - will skip TimeGPT checks
# GOLDEN TASK PASSED
# Exit code: 0
```

---

## 7. Contact

**Maintainer**: Jeremy Longshore
**Email**: jeremy@intentsolutions.io
**Repository**: https://github.com/intent-solutions-io/plugins-nixtla

For questions about test coverage or validation, use GitHub issues or email.

---

**Test Coverage Report**: ✅ **COMPLETE**
**Ready for Nixtla Review**: ✅ **YES**
**Version**: 0.6.0
**Date**: 2025-11-25
