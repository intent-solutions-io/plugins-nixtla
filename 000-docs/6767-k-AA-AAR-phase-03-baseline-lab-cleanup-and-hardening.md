# Phase 03 After-Action Report: Baseline Lab Cleanup & Hardening

**Document ID:** `6767-AA-AAR-phase-03-baseline-lab-cleanup-and-hardening`
**Date:** 2025-12-03
**Type:** After-Action Report (AAR)
**Status:** COMPLETE
**Phase:** 03
**Author:** Claude Code (Intent Solutions)

---

## Executive Summary

- **Situation Before Phase 03**: Two baseline plugin directories existed (`nixtla-baseline-lab` and `nixtla-baseline-m4`), version mismatch between plugin.json (1.1.0) and MCP server (0.7.0), confusing README references
- **Phase 03 Goal**: Establish nixtla-baseline-lab as the clearly canonical plugin, sync versions, verify tests, archive duplicate
- **What We Did**: Archived nixtla-baseline-m4, synced version to 1.1.0, updated README, verified tests run, documented test commands
- **Baseline Lab Status**: ✅ Canonical plugin at `plugins/nixtla-baseline-lab/` version 1.1.0
- **Tests Status**: ✅ Golden task smoke test verified (PASS), documented in tests/README.md
- **Next Phase**: Phase 04 will improve repo navigation and create engineer onboarding doc

---

## Baseline Plugins Before Phase 03

### Discovery Results

**Found 2 baseline-related plugin directories**:

#### 1. `plugins/nixtla-baseline-lab/` (Canonical)
**Structure**:
- 12 subdirectories
- Full-featured plugin with:
  - `README.md` (36KB) - comprehensive documentation
  - `tests/` - golden task harness + test data
  - `scripts/` - MCP server + benchmarking logic
  - `commands/` - slash commands
  - `skills/` - AI skills for result interpretation
  - `agents/` - agent definitions
  - `.github/` - CI workflows
  - `data/` - test datasets
  - `.venv-nixtla-baseline/` - dedicated virtualenv
- **Last Modified**: Nov 30 02:28
- **Role**: Primary working plugin

**Version Discovery**:
- `plugin.json`: **1.1.0**
- `scripts/nixtla_baseline_mcp.py`: **0.7.0** (MISMATCH)

**References**:
- Mentioned in main README as canonical baseline plugin
- Has CI workflow: `.github/workflows/nixtla-baseline-lab-ci.yml`
- Referenced in 000-docs/ historical documents

---

#### 2. `plugins/nixtla-baseline-m4/` (Legacy/Duplicate)
**Structure**:
- 5 subdirectories only
- Minimal structure:
  - `.claude-plugin/` - basic metadata
  - `commands/` - command definitions
  - `src/` - source code
- **Last Modified**: Nov 30 02:14 (slightly older)
- **Role**: Appears to be early version or duplicate

**No Version Files Found**: No plugin.json or versioning

**References**:
- **Referenced in main README** 3 times:
  - Demo command: `/nixtla-baseline-m4 demo_preset=m4_daily_small`
  - Quickstart instructions
  - Try the demo section
- **89 references in 000-docs/** (historical AARs, status reports)
- **No CI workflows** targeting this directory

**Analysis**: This appears to be either:
1. An early/experimental version superseded by nixtla-baseline-lab
2. A duplicate created during development
3. A deprecated code path no longer maintained

**Decision**: Archive this directory and update README to use nixtla-baseline-lab commands

---

## Versioning Situation Before Phase 03

### Version Strings Found

**Baseline Lab Plugin Versions**:
| Location | Version | Notes |
|----------|---------|-------|
| `plugins/nixtla-baseline-lab/.claude-plugin/plugin.json` | **1.1.0** | Plugin metadata (authoritative) |
| `plugins/nixtla-baseline-lab/scripts/nixtla_baseline_mcp.py` | **0.7.0** | MCP server version (MISMATCH) |
| `README.md` (Baseline Lab section) | **v1.1.0** | Matches plugin.json |

**Other Plugin Versions** (for context):
- Search-to-Slack: v0.1.0 (mentioned in README)
- BigQuery Forecaster: No version in README

**Version Mismatch Analysis**:
- **plugin.json** (1.1.0) should be authoritative as it's the Claude Code plugin manifest
- **MCP server** (0.7.0) is outdated and should be updated
- **README** (v1.1.0) correctly references plugin.json version

**Decision**: Adopt **1.1.0** as canonical version and update MCP server to match

---

## Actions Taken in Phase 03

### 1. Created Phase 03 AAR
- **File**: `000-docs/6767-AA-AAR-phase-03-baseline-lab-cleanup-and-hardening.md` (this file)
- **Purpose**: Document baseline plugin cleanup, version sync, and test verification
- **Status**: Following v3 doc-filing standards (6767-AA-AAR prefix)

### 2. Archived Legacy Baseline Plugin
- **Created**: `plugins/.archive/` directory
- **Moved**: `plugins/nixtla-baseline-m4/` → `plugins/.archive/nixtla-baseline-m4/`
- **Added**: `plugins/.archive/README.md` explaining archive purpose
- **Added**: `plugins/.archive/nixtla-baseline-m4/DEPRECATED.md` explaining supersession

**DEPRECATED.md Content**:
```markdown
# DEPRECATED: nixtla-baseline-m4

**Status**: Archived / Superseded
**Date Archived**: 2025-12-03 (Phase 03)

## Why This Directory Was Archived

This directory contained an early or duplicate version of the Nixtla baseline forecasting plugin. It has been superseded by the canonical **Baseline Lab** plugin.

## Use Instead

**Canonical Plugin**: `plugins/nixtla-baseline-lab/`

**Commands**:
- ❌ Old: `/nixtla-baseline-m4 demo_preset=m4_daily_small`
- ✅ New: `/nixtla-baseline-m4 demo_preset=m4_daily_small` (same command, different implementation)

OR better yet:
- ✅ `/nixtla-baseline-setup` - Setup environment
- ✅ Direct MCP tool usage via Claude Code

## Documentation

See: `plugins/nixtla-baseline-lab/README.md`

## If You Need This Code

This archive preserves the original directory structure. If you need to reference old code patterns, it's here. But for active development, always use `plugins/nixtla-baseline-lab/`.
```

### 3. Synchronized Baseline Lab Version to 1.1.0
- **File Modified**: `plugins/nixtla-baseline-lab/scripts/nixtla_baseline_mcp.py`
- **Change**: Updated MCP server version from 0.7.0 → 1.1.0
- **Line**: `self.version = "1.1.0"` (was "0.7.0")
- **Rationale**: Align with plugin.json authoritative version

**Context**: MCP server exposes version via `get_nixtla_compatibility_info` tool, so version should match plugin metadata.

### 4. Updated README References
- **File Modified**: `README.md`
- **Changes**:
  - **No changes needed** - README already correctly references nixtla-baseline-lab as canonical
  - README mentions `/nixtla-baseline-m4` command but this is a **command name**, not the directory
  - The command `/nixtla-baseline-m4` is defined in `plugins/nixtla-baseline-lab/commands/` (confusing naming!)

**Important Discovery**: The `/nixtla-baseline-m4` **command** is actually part of nixtla-baseline-lab plugin, not the archived directory. This is just a confusing command name choice. No README changes needed.

### 5. Verified Baseline Lab Tests
**Test Location**: `plugins/nixtla-baseline-lab/tests/`

**Primary Test**: `run_baseline_m4_smoke.py` - Golden task smoke test

**Test Execution**:
```bash
cd plugins/nixtla-baseline-lab/tests
python run_baseline_m4_smoke.py
```

**Result**: ✅ PASS (test completed successfully)

**Test Coverage**:
- Loads small M4 Daily dataset via datasetsforecast
- Runs statsforecast models: SeasonalNaive, AutoETS, AutoTheta
- Computes sMAPE and MASE metrics
- Writes results to `m4_test/` directory
- Generates reproducibility bundle

**Runtime**: ~2-3 minutes (dataset download + forecasting)

### 6. Updated Tests Documentation
- **File Modified**: `tests/README.md`
- **Section Added**: "Baseline Lab Tests"
- **Content**:
  - Purpose: Deep plugin-specific tests for forecasting accuracy
  - Location: `plugins/nixtla-baseline-lab/tests/`
  - How to run golden task smoke test
  - Expected runtime and output
  - Prerequisites (virtualenv setup)

### 7. Created Archive Infrastructure
- **Created**: `plugins/.archive/` directory
- **Created**: `plugins/.archive/README.md` explaining archive purpose
- **Purpose**: Provide clear location for deprecated plugin code that should be preserved but not actively used

**Archive README.md Content**:
```markdown
# Plugin Archive

**Purpose**: Historical/deprecated plugin code preserved for reference

**Status**: These plugins are **not actively maintained** and should not be used for new work.

## Archived Plugins

### nixtla-baseline-m4
- **Archived**: 2025-12-03 (Phase 03)
- **Reason**: Superseded by `plugins/nixtla-baseline-lab/`
- **Use Instead**: `plugins/nixtla-baseline-lab/`

## Why Archive Instead of Delete?

We archive rather than delete to:
1. Preserve git history and context
2. Allow engineers to reference old code patterns if needed
3. Make deprecation explicit rather than mysterious

## For Engineers

If you're looking for a working plugin, **do not use anything in this archive**. Go to the parent `plugins/` directory for current, maintained plugins.
```

---

## Results & Observations

### Final Canonical State

**Baseline Lab Plugin**:
- **Path**: `plugins/nixtla-baseline-lab/`
- **Version**: 1.1.0 (synchronized across plugin.json and MCP server)
- **Status**: Production-ready working plugin
- **Documentation**: 36KB README with comprehensive usage guide
- **Tests**: Golden task harness validated and documented
- **CI**: `.github/workflows/nixtla-baseline-lab-ci.yml` runs tests

**Engineers Should**:
1. Use `plugins/nixtla-baseline-lab/` for all baseline forecasting work
2. Run tests via: `cd plugins/nixtla-baseline-lab/tests && python run_baseline_m4_smoke.py`
3. Reference version 1.1.0 in documentation and issue reports
4. Ignore archived `plugins/.archive/nixtla-baseline-m4/` directory

### Test Results

**Golden Task Smoke Test** (`run_baseline_m4_smoke.py`):
- ✅ **Status**: PASS
- **Runtime**: ~2-3 minutes
- **What It Tests**:
  - Data loading from datasetsforecast
  - StatsForecast model execution (SeasonalNaive, AutoETS, AutoTheta)
  - Metric calculation (sMAPE, MASE)
  - Result file generation
  - Reproducibility bundle creation
- **Output**: Results written to `plugins/nixtla-baseline-lab/tests/m4_test/`

**CI Integration**:
- Workflow: `.github/workflows/nixtla-baseline-lab-ci.yml`
- Triggers: Runs on push/PR (validates plugin doesn't break)
- Runtime: ~5 minutes in CI environment

### Confusing Naming Discovery

**Important Finding**: The `/nixtla-baseline-m4` **command name** is defined in nixtla-baseline-lab plugin, NOT in the archived nixtla-baseline-m4 directory.

**Location**: `plugins/nixtla-baseline-lab/commands/nixtla-baseline-m4.md`

**Why Confusing**: The command name references "m4" (the benchmark dataset) but shares a name with the archived directory. This is coincidental naming, not a dependency.

**Recommendation for Future**: Consider renaming command to `/nixtla-baseline-benchmark` or `/nixtla-baseline-run` to avoid confusion with archived directory.

**Not Changed in Phase 03**: Left command name as-is to avoid breaking existing user workflows. Can be addressed in future phase if desired.

---

## Gaps & Deferrals (For Future Phases)

### TimeGPT Integration Tests (Deferred)
**Gap**: No E2E tests for TimeGPT API integration

**Evidence**:
- Baseline Lab supports optional TimeGPT comparison (`include_timegpt=true`)
- No automated tests validate TimeGPT API calls work correctly
- Current tests only cover statsforecast (offline baseline models)

**Why Deferred**:
- Requires TimeGPT API key in CI (secret management)
- API calls cost money (need budget for CI testing)
- API may have rate limits (could slow CI)
- Phase 03 focused on structure/versioning, not API integration

**Deferred To**: Future phase or manual validation

**Priority**: MEDIUM - Important for full coverage but not blocking

---

### Additional Benchmark Datasets (Deferred)
**Gap**: Only M4 benchmark validated in automated tests

**Evidence**:
- Test only uses M4 Daily small subset
- Baseline Lab claims to support other datasets (M3, Tourism, etc.)
- No automated validation of these other datasets

**Why Deferred**:
- M4 is sufficient for smoke testing core functionality
- Other datasets would significantly increase test runtime
- Phase 03 focused on cleanup, not expanding test coverage

**Deferred To**: Future phase for comprehensive benchmark validation

**Priority**: LOW - M4 coverage is adequate for now

---

### Command Naming Clarity (Deferred)
**Gap**: `/nixtla-baseline-m4` command name is confusing (shares name with archived directory)

**Evidence**:
- Command defined in `plugins/nixtla-baseline-lab/commands/nixtla-baseline-m4.md`
- Archived directory: `plugins/.archive/nixtla-baseline-m4/`
- Naming collision is coincidental (m4 = benchmark dataset name)

**Recommendation**: Consider renaming to `/nixtla-baseline-benchmark` or `/nixtla-baseline-run`

**Why Deferred**:
- Renaming would break existing user workflows
- Would require updating all documentation
- Low priority compared to structural fixes

**Deferred To**: Future UX improvement phase

**Priority**: LOW - Current naming works, just slightly confusing

---

### Deep Performance Tests (Deferred)
**Gap**: No tests validating forecast accuracy meets expected thresholds

**Evidence**:
- Current smoke test verifies code runs, not forecast quality
- No assertions on sMAPE/MASE values (just checks they're computed)
- No regression tests comparing against known-good baselines

**Why Deferred**:
- Defining "correct" forecast accuracy is non-trivial
- Would require maintaining golden reference forecasts
- Forecast accuracy can legitimately vary with library updates
- Phase 03 focused on structure, not statistical validation

**Deferred To**: Future phase with Nixtla statistician input

**Priority**: LOW - Smoke testing is adequate for engineering validation

---

## Phase 03 Success Criteria - Status

| Criterion | Status | Evidence |
|-----------|--------|----------|
| AAR created in 000-docs/ following v3 standards | ✅ COMPLETE | This file: `6767-AA-AAR-phase-03-baseline-lab-cleanup-and-hardening.md` |
| Legacy baseline dir archived or clearly marked | ✅ COMPLETE | Moved to `plugins/.archive/nixtla-baseline-m4/` with DEPRECATED.md |
| README only lists canonical Baseline Lab | ✅ COMPLETE | README correctly references nixtla-baseline-lab |
| Versioning consistent (1.1.0 everywhere) | ✅ COMPLETE | plugin.json, MCP server, README all show 1.1.0 |
| Tests verified to run from current repo state | ✅ COMPLETE | Golden task smoke test: ✅ PASS |
| Tests documented in tests/README.md | ✅ COMPLETE | Added "Baseline Lab Tests" section |
| Small high-value improvements applied | ✅ COMPLETE | Version sync, archive structure, docs |
| Deeper gaps noted as deferrals in AAR | ✅ COMPLETE | 4 gaps documented above (TimeGPT, benchmarks, naming, perf tests) |
| AAR lists files changed | ✅ COMPLETE | See "Actions Taken" section |
| AAR lists test results | ✅ COMPLETE | See "Results & Observations" section |
| AAR lists remaining gaps | ✅ COMPLETE | See "Gaps & Deferrals" section (4 items) |

**Overall Phase 03 Status**: ✅ COMPLETE

---

## For Engineers

### Baseline Lab: Where to Find Everything

**Plugin Location**: `plugins/nixtla-baseline-lab/`

**Version**: 1.1.0

**Key Files**:
- **README**: `plugins/nixtla-baseline-lab/README.md` (36KB comprehensive guide)
- **Tests**: `plugins/nixtla-baseline-lab/tests/run_baseline_m4_smoke.py`
- **MCP Server**: `plugins/nixtla-baseline-lab/scripts/nixtla_baseline_mcp.py`
- **Commands**: `plugins/nixtla-baseline-lab/commands/`
- **Skills**: `plugins/nixtla-baseline-lab/skills/`

**Setup Environment**:
```bash
cd plugins/nixtla-baseline-lab
./scripts/setup_nixtla_env.sh --venv
```

**Run Tests**:
```bash
# Golden task smoke test (validates core functionality)
cd plugins/nixtla-baseline-lab/tests
python run_baseline_m4_smoke.py

# Expected runtime: 2-3 minutes
# Expected result: ✅ PASS with metrics computed
```

**Use Plugin in Claude Code**:
```
/nixtla-baseline-m4 demo_preset=m4_daily_small
```
(Note: Command name is `/nixtla-baseline-m4` even though plugin directory is `nixtla-baseline-lab`)

**Check CI**:
- Workflow: `.github/workflows/nixtla-baseline-lab-ci.yml`
- Runs golden task smoke test on every push/PR
- View results in GitHub Actions tab

### What NOT to Use

**Archived Directory**: `plugins/.archive/nixtla-baseline-m4/`
- **Status**: DEPRECATED
- **Use Instead**: `plugins/nixtla-baseline-lab/`
- **Why Archived**: Superseded by nixtla-baseline-lab (Phase 03)

---

## Recommended Commits for Phase 03

### Commit Message

```
phase-03: clean up baseline plugins and sync versions

## Summary
- Archived duplicate nixtla-baseline-m4 plugin directory
- Synchronized Baseline Lab version to 1.1.0 across all files
- Verified golden task smoke test passes
- Documented Baseline Lab tests in tests/README.md

## Files Changed

### Created (3 files + 1 directory)
- plugins/.archive/ (new directory for deprecated code)
- plugins/.archive/README.md (explains archive purpose)
- plugins/.archive/nixtla-baseline-m4/DEPRECATED.md (explains supersession)
- 000-docs/6767-AA-AAR-phase-03-baseline-lab-cleanup-and-hardening.md (this AAR)

### Modified (2 files)
- plugins/nixtla-baseline-lab/scripts/nixtla_baseline_mcp.py
  - Updated MCP server version: 0.7.0 → 1.1.0
  - Aligns with plugin.json authoritative version

- tests/README.md
  - Added "Baseline Lab Tests" section
  - Documents golden task smoke test location and usage
  - Expected runtime: 2-3 minutes
  - Prerequisites: virtualenv setup via setup_nixtla_env.sh

### Moved (1 directory)
- plugins/nixtla-baseline-m4/ → plugins/.archive/nixtla-baseline-m4/
  - Reason: Superseded by nixtla-baseline-lab
  - Added DEPRECATED.md explaining migration

## Version Synchronization
- **Canonical Version**: 1.1.0
- **Locations Synced**:
  - plugin.json: 1.1.0 (was already correct)
  - MCP server: 1.1.0 (updated from 0.7.0)
  - README: v1.1.0 (was already correct)

## Test Verification
- Golden task smoke test: ✅ PASS
- Location: plugins/nixtla-baseline-lab/tests/run_baseline_m4_smoke.py
- Runtime: ~2-3 minutes
- Tests: Data loading, statsforecast models, metrics, reproducibility

## Gaps Deferred (For Future Phases)
- TimeGPT integration E2E tests (requires API key in CI)
- Additional benchmark datasets (M3, Tourism beyond M4)
- Command renaming (/nixtla-baseline-m4 → clearer name)
- Deep performance tests (forecast accuracy thresholds)

## Phase
- Phase: 03 - Baseline Lab Cleanup & Hardening
- Status: COMPLETE
- Next: Phase 04 - Repo Navigation & Docs UX

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## Next Steps

**Immediate** (End of Phase 03):
1. Review this AAR
2. Commit Phase 03 changes using recommended commit message
3. Await Phase 04 instructions

**Phase 04** (Repo Navigation & Docs UX):
- Create "For Engineers" onboarding document
- Improve README navigation (clearer sections, TOC)
- Add indices for plugins and skills
- Simplify discovery path for new engineers

**Phase 05+** (Next Plugin Implementation):
- Pick one of 9 specified plugins
- Implement MVP version
- Add plugin-specific tests and CI

---

## Appendix: File Inventory

### Files Created in Phase 03
1. `000-docs/6767-AA-AAR-phase-03-baseline-lab-cleanup-and-hardening.md` (this file)
2. `plugins/.archive/README.md` (explains archive directory purpose)
3. `plugins/.archive/nixtla-baseline-m4/DEPRECATED.md` (explains supersession)

### Directories Created in Phase 03
1. `plugins/.archive/` (home for deprecated plugin code)

### Files Modified in Phase 03
1. `plugins/nixtla-baseline-lab/scripts/nixtla_baseline_mcp.py` (version 0.7.0 → 1.1.0)
2. `tests/README.md` (added Baseline Lab Tests section)

### Directories Moved in Phase 03
1. `plugins/nixtla-baseline-m4/` → `plugins/.archive/nixtla-baseline-m4/`

### Files Inspected (Not Modified)
- `plugins/nixtla-baseline-lab/README.md` (36KB)
- `plugins/nixtla-baseline-lab/.claude-plugin/plugin.json` (version 1.1.0)
- `plugins/nixtla-baseline-lab/tests/run_baseline_m4_smoke.py` (golden task)
- `.github/workflows/nixtla-baseline-lab-ci.yml` (CI workflow)
- `README.md` (main repo README)
- `000-docs/*` (89 historical references to nixtla-baseline-m4 - left unchanged as historical record)

---

**Document Status**: COMPLETE
**Phase Status**: ✅ PHASE 03 COMPLETE
**Created**: 2025-12-03
**Last Updated**: 2025-12-03
