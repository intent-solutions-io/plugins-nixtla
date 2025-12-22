# Nixtla Release Validation Workflow

**Location**: `002-workspaces/test-harness-lab/skills/nixtla-release-validation/`

**Purpose**: Automated pre-release validation using multi-phase test harness pattern.

## Quick Start

```bash
cd 002-workspaces/test-harness-lab/skills/nixtla-release-validation

# Create session directory
SESSION_DIR="reports/$(date +%Y%m%d_%H%M%S)"
mkdir -p "${SESSION_DIR}"

# Run verification script (Phase 4)
bash scripts/analyze_test_results.sh \
  /home/jeremy/000-projects/nixtla \
  "${SESSION_DIR}"

# Check results
cat "${SESSION_DIR}/phase4-verification-report.json" | jq '.'
```

## Structure

```
nixtla-release-validation/
├── SKILL.md                  # Main workflow definition
├── README.md                 # This file
├── scripts/
│   └── analyze_test_results.sh  # Phase 4 verification script
├── agents/                   # Phase agent definitions (future)
│   ├── phase_1.md           # Change analysis
│   ├── phase_2.md           # Test impact prediction
│   ├── phase_3.md           # Risk assessment
│   ├── phase_4.md           # Verification coordinator
│   └── phase_5.md           # Go/no-go recommendation
├── references/               # Supporting documentation (future)
└── reports/                  # Session outputs
    └── YYYYMMDD_HHMMSS/     # Timestamped session directory
        ├── phase1-change-analysis.json
        ├── phase2-test-predictions.json
        ├── phase3-risk-assessment.json
        ├── phase4-verification-report.json
        ├── phase5-final-recommendation.json
        └── RELEASE-VALIDATION-SUMMARY.md
```

## 5-Phase Workflow

### Phase 1: Change Analysis
**Input**: Git tags (v1.7.0 → v1.8.0)
**Output**: `phase1-change-analysis.json`
**Task**: Analyze git diff, CHANGELOG, modified files

### Phase 2: Test Impact Prediction
**Input**: Phase 1 output
**Output**: `phase2-test-predictions.json`
**Task**: Predict which tests might fail based on changes

### Phase 3: Risk Assessment
**Input**: Phase 1 + 2 outputs
**Output**: `phase3-risk-assessment.json`
**Task**: Categorize changes (high/medium/low risk)

### Phase 4: VERIFICATION ★
**Input**: Nixtla repository path
**Output**: `phase4-verification-report.json`
**Task**: **Run actual pytest suite**, compare vs predictions

**Script**: `scripts/analyze_test_results.sh`

```bash
bash scripts/analyze_test_results.sh <repo_path> <output_dir>
```

**What it does**:
1. Runs `pytest tests/ --cov --json-report`
2. Parses test results
3. Generates coverage report
4. Outputs structured JSON

### Phase 5: Go/No-Go Recommendation
**Input**: Phase 3 + 4 outputs
**Output**: `phase5-final-recommendation.json`
**Task**: Synthesize findings, recommend go/no-go

## Testing

**Test with current repository**:

```bash
cd /home/jeremy/000-projects/nixtla/002-workspaces/test-harness-lab/skills/nixtla-release-validation

SESSION="reports/test_$(date +%s)"
mkdir -p "$SESSION"

bash scripts/analyze_test_results.sh \
  /home/jeremy/000-projects/nixtla \
  "$SESSION"

# Check output
ls -la "$SESSION"
cat "$SESSION/phase4-verification-report.json" | jq '.results'
```

**Expected output files**:
- `pytest-results.json` - Raw pytest JSON report
- `pytest-output.log` - Pytest console output
- `coverage.json` - Coverage data (if available)
- `phase4-verification-report.json` - Structured verification report

## Integration with Test Harness Lab

This skill follows the **multi-phase validated workflow pattern** from:
- `002-workspaces/test-harness-lab/reference-implementation/`
- `002-workspaces/test-harness-lab/docs/NIXTLA-APPLICATIONS.md`

**Key Pattern**: Phase 4 runs deterministic scripts to verify LLM predictions from Phase 2.

## Requirements

- Python 3.9+
- `pytest` with `pytest-cov` and `pytest-json-report`
- `jq` for JSON processing
- Git repository with tagged releases

**Install dependencies**:

```bash
pip install pytest pytest-cov pytest-json-report
```

## Status

**Current Implementation**: Phase 4 verification script complete and tested

**Future Work**:
- Create agent definitions for Phases 1, 2, 3, 5
- Add reference documentation
- Test with historical releases (v1.6.0 → v1.7.0)

## See Also

- Main specification: `002-workspaces/test-harness-lab/docs/NIXTLA-APPLICATIONS.md`
- Reference pattern: `002-workspaces/test-harness-lab/reference-implementation/`
- Test harness guides: `002-workspaces/test-harness-lab/guides/`
