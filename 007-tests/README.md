# Tests Directory

**Status**: Basic validation scaffold (Phase 01)
**Purpose**: Quick sanity checks and repo structure validation for Nixtla engineers

This directory provides a starting point for validating the Nixtla plugin repository. For deeper plugin-specific tests, see individual plugin directories (e.g., `plugins/nixtla-baseline-lab/tests/`).

---

## For Nixtla Engineers

### Quick Start: Validate Repo Health

Run this single command to check if the repo is healthy:

```bash
# From repo root
python tests/basic_validator.py
```

**Expected output** (if repo is healthy):
```
========================================
Nixtla Repo Structure Validator
========================================

[PASS] Critical directories present
[PASS] 4 plugin directories found
[PASS] 8 Claude Skills found
[PASS] 9 canonical 6767 docs found
[PASS] 4 CI workflows present

========================================
✅ VALIDATION RESULT: PASS
========================================
```

**If validation fails**, the script will tell you exactly what's missing or wrong.

---

## What Gets Tested

### 1. Basic Validator (`basic_validator.py`)
**Purpose**: Instant repo structure sanity check (<1 second)

**Checks**:
- ✅ Critical directories exist (plugins/, 000-docs/, skills-pack/)
- ✅ Expected plugin directories present (4 plugins)
- ✅ Claude Skills present (8 skills in skills-pack/)
- ✅ Canonical reference docs present (9 "6767-" docs)
- ✅ CI workflows present (4 workflow files)

**Does NOT check**:
- ❌ Code quality (linting, types) - handled by CI
- ❌ Test coverage - handled by pytest with --cov
- ❌ Dependencies installed - handled by requirements.txt
- ❌ Plugin functionality - handled by plugin-specific tests

---

### 2. Placeholder Tests (`test_placeholder.py`)
**Purpose**: Basic pytest infrastructure

**Tests**:
- Simple assertion test (always passes)
- Core dependencies import test (pandas, numpy, pydantic)
- Integration test marker example

---

### 3. Skills Installer E2E Test (`test_skills_installer_e2e.py`)
**Purpose**: Validate Nixtla skills installer works in fresh projects

**Prerequisites**:
```bash
# Install installer package in editable mode first
pip install -e packages/nixtla-claude-skills-installer
```

**Run Test**:
```bash
# From repo root
python tests/test_skills_installer_e2e.py

# Or with pytest
pytest tests/test_skills_installer_e2e.py -v
```

**What It Tests**:
- ✅ Creates fresh temporary directory (isolated test)
- ✅ Runs `nixtla-skills init --force` in temp directory
- ✅ Validates `.claude/skills/` structure created
- ✅ Verifies all 8 Nixtla skills installed
- ✅ Checks each skill has `SKILL.md` file
- ✅ Fast: completes in <5 seconds

**Expected Output** (if passing):
```
========================================
Nixtla Skills Installer E2E Test
========================================

[STEP 1/4] Locating repository root...
✓ Repo root: /path/to/nixtla

[STEP 2/4] Verifying installer package...
✓ Package 'nixtla-claude-skills-installer' is installed

[STEP 3/4] Running installer in temp directory...
✓ Created temp directory: /tmp/...
✓ Installer executed successfully

[STEP 4/4] Validating skills structure...
✓ .claude directory exists
✓ .claude/skills directory exists
✓ Found 8 Nixtla skills:
   [... 8 skills listed ...]

✓ All 8 skills have SKILL.md files

========================================
✅ E2E TEST RESULT: PASS
========================================
```

**Troubleshooting**:
- **Problem**: "Package 'nixtla-claude-skills-installer' is not installed"
  - **Solution**: Run `pip install -e packages/nixtla-claude-skills-installer`
- **Problem**: "nixtla-skills command not found"
  - **Solution**: Reinstall package or check virtualenv activated
- **Problem**: Test times out
  - **Solution**: Check that `skills-pack/.claude/skills/` has 8 nixtla-* directories

**CI Status**: This test runs automatically in `.github/workflows/skills-installer-ci.yml`

---

### 4. Baseline Lab Tests (Plugin-Specific)
**Purpose**: Deep validation of baseline forecasting plugin functionality

**Location**: `plugins/nixtla-baseline-lab/tests/`

**Prerequisites**:
```bash
# One-time setup: create dedicated virtualenv
cd plugins/nixtla-baseline-lab
./scripts/setup_nixtla_env.sh --venv
```

**Primary Test**: Golden Task Smoke Test
```bash
# From repo root
cd plugins/nixtla-baseline-lab/tests
python run_baseline_m4_smoke.py
```

**What It Tests**:
- ✅ Data loading from datasetsforecast (M4 Daily small subset)
- ✅ StatsForecast model execution (SeasonalNaive, AutoETS, AutoTheta)
- ✅ Metric calculation (sMAPE, MASE)
- ✅ Result file generation
- ✅ Reproducibility bundle creation
- ✅ Runtime: ~2-3 minutes (includes dataset download)

**Expected Output**:
```
Running Nixtla Baseline Lab smoke test...
Loading M4 Daily dataset...
✓ Dataset loaded (X series, Y datapoints)
Running baseline models...
  ✓ SeasonalNaive
  ✓ AutoETS
  ✓ AutoTheta
Computing metrics...
  ✓ sMAPE: X.XX
  ✓ MASE: X.XX
Writing results to m4_test/...
✓ Test complete
```

**Test Structure** (`plugins/nixtla-baseline-lab/tests/`):
```
tests/
├── run_baseline_m4_smoke.py    # Golden task (primary test)
├── m4_test/                    # Output directory
├── csv_test/                   # CSV data tests
├── custom/                     # Custom dataset tests
├── data/                       # Test fixtures
└── golden_tasks/               # Reference golden outputs
```

**Troubleshooting**:
- **Problem**: "ModuleNotFoundError: No module named 'statsforecast'"
  - **Solution**: Run setup script: `cd plugins/nixtla-baseline-lab && ./scripts/setup_nixtla_env.sh --venv`
- **Problem**: Test hangs during dataset download
  - **Solution**: Check internet connection, datasetsforecast requires downloading M4 data
- **Problem**: Import errors or version mismatches
  - **Solution**: Recreate virtualenv: `rm -rf .venv-nixtla-baseline && ./scripts/setup_nixtla_env.sh --venv`

**CI Status**: This test runs automatically in `.github/workflows/nixtla-baseline-lab-ci.yml`

**Version**: Tests validated against Baseline Lab v1.1.0 (Phase 03)

---

## Test Execution Flow

For Nixtla engineers validating the repo:

**Level 1: Quick Sanity (5 seconds)**
```bash
python tests/basic_validator.py
```
Validates repo structure only.

**Level 2: Baseline Lab Validation (2-3 minutes)**
```bash
cd plugins/nixtla-baseline-lab/tests
python run_baseline_m4_smoke.py
```
Tests core forecasting functionality with M4 benchmark data.

**Level 3: Full Test Suite (5-10 minutes)**
```bash
pytest
```
Runs all pytest-based tests across the repo.

---

## Planned Future Test Structure

```
tests/
├── basic_validator.py              # ✅ Phase 01 - Done
├── test_placeholder.py              # ✅ Pre-existing
├── test_skills_installer_e2e.py     # ✅ Phase 02 - Done
├── unit/                            # 🔜 Future - Unit tests
├── integration/                     # 🔜 Future - Integration tests
├── fixtures/                        # 🔜 Future - Test data/mocks
└── validation/                      # 🔜 Future - Advanced validation
```

---

## Troubleshooting

**Problem**: `python tests/basic_validator.py` fails with "directory not found"

**Solution**: Make sure you're running from the repo root:
```bash
cd /path/to/claude-code-plugins-nixtla
python tests/basic_validator.py
```

---

**Problem**: Validator passes but you want deeper validation

**Solution**: Run plugin-specific tests:
```bash
cd plugins/nixtla-baseline-lab/tests
python run_baseline_m4_smoke.py
```

---

**Problem**: Want to run all pytest tests

**Solution**: From repo root:
```bash
pytest
# Or with coverage:
pytest --cov=plugins --cov-report=term-missing
```

---

## Testing Philosophy

**This directory (`tests/`)**:
- Basic, fast, structural validation
- Entry point for engineers new to the repo
- "Is this repo healthy?" checks

**Plugin directories** (`plugins/*/tests/`):
- Deep, plugin-specific tests
- Forecasting accuracy, API integration, error handling
- What engineers run before merging plugin changes

**CI workflows** (`.github/workflows/`):
- Automated validation on every commit
- Runs both basic validator and plugin-specific tests
- Prevents broken code from reaching main branch

---

**Last Updated**: 2025-12-03 (Phase 03)
**Next Update**: Phase 04 (Repo navigation & docs UX)