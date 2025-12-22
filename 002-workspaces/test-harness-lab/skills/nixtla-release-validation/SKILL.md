---
name: nixtla-release-validation
description: |
  Multi-phase release validation workflow for nixtla. Analyzes git changes, predicts test impact,
  assesses risk, runs pytest verification, provides go/no-go recommendation.
  Trigger: "validate release", "run release validation", "check release readiness"
allowed-tools: Read, Write, Bash, Task
version: 1.0.0
license: MIT
author: Jeremy Longshore <jeremy@intentsolutions.io>
---

# Nixtla Release Validation Workflow

Automated pre-release validation using multi-phase test harness pattern with empirical verification.

## Purpose

Validate nixtla releases (e.g., v1.7.0 → v1.8.0) before shipping by analyzing changes, predicting impact, running tests, and providing evidence-based go/no-go recommendation.

## Overview

This workflow implements the 5-phase validated workflow pattern:

1. **Change Analysis** - Git diff, CHANGELOG, modified files → structured change list
2. **Test Impact Prediction** - For each change, predict which tests might fail
3. **Risk Assessment** - Categorize changes, estimate user impact
4. **Verification (Critical)** - Run pytest suite, compare predictions vs reality
5. **Go/No-Go Recommendation** - Synthesize findings, output release notes

**Phase 4 is the critical phase** - it runs actual scripts to verify Phase 2 predictions.

## Prerequisites

- Git repository with tagged releases
- Python 3.9+ with pytest installed
- `jq` for JSON processing
- Write access to `002-workspaces/test-harness-lab/skills/nixtla-release-validation/reports/`

## Instructions

### Step 1: Create Session Directory

```bash
cd 002-workspaces/test-harness-lab/skills/nixtla-release-validation
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SESSION_DIR="reports/${TIMESTAMP}"
mkdir -p "${SESSION_DIR}"
```

### Step 2: Run Phase 1 - Change Analysis

**Task**: Spawn Phase 1 agent

**Input JSON**:
```json
{
  "session_dir": "<SESSION_DIR>",
  "from_version": "v1.7.0",
  "to_version": "v1.8.0",
  "repo_path": "/home/jeremy/000-projects/nixtla"
}
```

**Expected Output**: `<SESSION_DIR>/phase1-change-analysis.json`

```json
{
  "metadata": {
    "phase": 1,
    "timestamp": "2025-12-22T17:00:00Z"
  },
  "changes": {
    "changed_files": ["src/forecast.py", "tests/test_forecast.py"],
    "changed_apis": ["forecast()", "fit()"],
    "breaking_changes": ["forecast() now requires 'freq' parameter"],
    "new_features": ["Added anomaly detection"]
  }
}
```

### Step 3: Run Phase 2 - Test Impact Prediction

**Task**: Spawn Phase 2 agent

**Input JSON**:
```json
{
  "session_dir": "<SESSION_DIR>",
  "phase1_output": "<SESSION_DIR>/phase1-change-analysis.json"
}
```

**Expected Output**: `<SESSION_DIR>/phase2-test-predictions.json`

```json
{
  "metadata": {
    "phase": 2,
    "timestamp": "2025-12-22T17:05:00Z"
  },
  "test_predictions": [
    {
      "change": "Modified forecast() signature",
      "affected_tests": ["test_forecast_basic", "test_forecast_with_exog"],
      "reason": "Function signature changed, existing calls will fail"
    }
  ]
}
```

### Step 4: Run Phase 3 - Risk Assessment

**Task**: Spawn Phase 3 agent

**Input JSON**:
```json
{
  "session_dir": "<SESSION_DIR>",
  "phase1_output": "<SESSION_DIR>/phase1-change-analysis.json",
  "phase2_output": "<SESSION_DIR>/phase2-test-predictions.json"
}
```

**Expected Output**: `<SESSION_DIR>/phase3-risk-assessment.json`

```json
{
  "metadata": {
    "phase": 3,
    "timestamp": "2025-12-22T17:10:00Z"
  },
  "risk_categories": {
    "high_risk": ["forecast() signature change - breaking"],
    "medium_risk": ["New anomaly detection - needs testing"],
    "low_risk": ["Documentation updates"]
  },
  "go_no_go": "pending"
}
```

### Step 5: Run Phase 4 - VERIFICATION (Critical Phase)

**Task**: Run verification script, compare predictions vs reality

**Script**: `scripts/analyze_test_results.sh`

```bash
bash scripts/analyze_test_results.sh \
  "/home/jeremy/000-projects/nixtla" \
  "${SESSION_DIR}"
```

**Expected Output**: `<SESSION_DIR>/phase4-verification-report.json`

```json
{
  "metadata": {
    "phase": 4,
    "script": "analyze_test_results.sh",
    "timestamp": "2025-12-22T17:15:00Z"
  },
  "results": {
    "tests_run": 145,
    "tests_passed": 142,
    "tests_failed": 3,
    "coverage_pct": 87.5,
    "failed_tests": ["test_forecast_basic", "test_forecast_with_exog"]
  },
  "prediction_comparison": {
    "predictions_confirmed": ["test_forecast_basic - FAILED as predicted"],
    "predictions_revised": [],
    "unexpected_failures": ["test_hierarchical - not predicted"]
  }
}
```

### Step 6: Run Phase 5 - Go/No-Go Recommendation

**Task**: Spawn Phase 5 agent

**Input JSON**:
```json
{
  "session_dir": "<SESSION_DIR>",
  "phase3_output": "<SESSION_DIR>/phase3-risk-assessment.json",
  "phase4_output": "<SESSION_DIR>/phase4-verification-report.json"
}
```

**Expected Output**: `<SESSION_DIR>/phase5-final-recommendation.json`

```json
{
  "metadata": {
    "phase": 5,
    "timestamp": "2025-12-22T17:20:00Z"
  },
  "recommendation": "no-go",
  "blockers": [
    "3 test failures must be fixed before release",
    "forecast() breaking change needs migration guide"
  ],
  "release_notes": "...",
  "migration_steps": [...]
}
```

### Step 7: Aggregate Final Report

Create summary markdown report:

```bash
cat > "${SESSION_DIR}/RELEASE-VALIDATION-SUMMARY.md" <<EOF
# Release Validation Summary

**Release**: v1.7.0 → v1.8.0
**Date**: $(date)
**Recommendation**: NO-GO

## Test Results
- Tests Run: 145
- Passed: 142
- Failed: 3

## Blockers
1. forecast() breaking change needs migration guide
2. 3 test failures must be addressed

## Next Steps
1. Fix test_forecast_basic
2. Fix test_forecast_with_exog
3. Fix test_hierarchical
4. Write migration guide for forecast() changes
5. Re-run validation

EOF
```

## Output

**Structured Outputs**:
- `phase1-change-analysis.json` - Git changes analyzed
- `phase2-test-predictions.json` - Impact predictions
- `phase3-risk-assessment.json` - Risk categories
- `phase4-verification-report.json` - Actual test results
- `phase5-final-recommendation.json` - Go/no-go decision
- `RELEASE-VALIDATION-SUMMARY.md` - Human-readable summary

**Evidence Trail**: All outputs in timestamped session directory.

## Error Handling

**If Phase 1-3 fail**: Check JSON syntax, file paths, git tags exist.

**If Phase 4 fails**:
- Verify pytest installed
- Check repo path is valid
- Ensure `scripts/analyze_test_results.sh` exists and is executable

**If Phase 5 fails**: Check Phase 3-4 JSON outputs exist and are valid.

**Validation Failures**: Each phase must write valid JSON to expected path before next phase runs.

## Examples

### Example 1: Run Full Validation

```bash
cd 002-workspaces/test-harness-lab/skills/nixtla-release-validation
SESSION_DIR="reports/$(date +%Y%m%d_%H%M%S)"
mkdir -p "${SESSION_DIR}"

# Phase 1-5: Spawn agents sequentially
# Phase 4: Run verification script
bash scripts/analyze_test_results.sh /home/jeremy/000-projects/nixtla "${SESSION_DIR}"

# Check final recommendation
cat "${SESSION_DIR}/phase5-final-recommendation.json" | jq '.recommendation'
```

### Example 2: Test with v1.6.0 → v1.7.0

```bash
SESSION_DIR="reports/test_v1.6_to_v1.7"
mkdir -p "${SESSION_DIR}"

# Run phases with historical release
# Compare predictions vs actual (known outcome)
```

## Resources

- **NIXTLA-APPLICATIONS.md**: Complete specification
- **Reference Implementation**: `002-workspaces/test-harness-lab/reference-implementation/`
- **Verification Script**: `scripts/analyze_test_results.sh`
- **Phase Agents**: `agents/phase_*.md`
