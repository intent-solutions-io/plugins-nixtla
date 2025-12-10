# Skills Test Success Criteria

**Date Created**: 2025-12-10
**Based On**: PRD.md and ARD.md documents per skill
**Total Skills**: 23

## Success Criteria Framework

### Level 1: Structural Validation (MUST PASS)
1. SKILL.md exists and is valid YAML frontmatter
2. All referenced scripts exist (`{baseDir}/scripts/*.py`)
3. Scripts are syntactically valid Python
4. Required frontmatter fields present: name, description, allowed-tools, version

### Level 2: Functional Validation (MUST PASS)
1. Scripts can be imported without errors
2. Scripts have proper CLI interface (--help works)
3. Scripts handle missing dependencies gracefully
4. Scripts return proper exit codes (0=success, non-zero=error)

### Level 3: Integration Validation (SHOULD PASS)
1. Full workflow executes end-to-end with sample data
2. Output files are created in expected locations
3. Output formats match documented schema
4. Error handling works as documented

### Level 4: Quality Validation (MUST PASS)
1. Description quality score >= 100%
2. SKILL.md < 500 lines
3. Execution time within targets
4. All documented examples work

---

## Per-Skill Success Definitions

### Core Forecasting Skills (5)

#### nixtla-anomaly-detector
**Source**: SKILL.md + scripts/detect_anomalies.py
**Success Criteria**:
- [ ] L1: SKILL.md valid, detect_anomalies.py exists
- [ ] L2: Script imports, --help works
- [ ] L3: Detects anomalies in sample time series
- [ ] L4: Outputs anomaly report with timestamps

#### nixtla-cross-validator
**Source**: SKILL.md + scripts/*.py
**Success Criteria**:
- [ ] L1: SKILL.md valid, all scripts exist
- [ ] L2: Scripts import, --help works
- [ ] L3: Runs cross-validation on sample data
- [ ] L4: Outputs CV metrics CSV

#### nixtla-exogenous-integrator
**Source**: SKILL.md + scripts/*.py
**Success Criteria**:
- [ ] L1: SKILL.md valid, all scripts exist
- [ ] L2: Scripts import, --help works
- [ ] L3: Integrates exogenous variables with time series
- [ ] L4: Outputs enhanced forecast

#### nixtla-timegpt2-migrator
**Source**: SKILL.md + scripts/*.py
**Success Criteria**:
- [ ] L1: SKILL.md valid, all scripts exist
- [ ] L2: Scripts import, --help works
- [ ] L3: Analyzes codebase for migration
- [ ] L4: Generates migration report

#### nixtla-uncertainty-quantifier
**Source**: SKILL.md + scripts/*.py
**Success Criteria**:
- [ ] L1: SKILL.md valid, all scripts exist
- [ ] L2: Scripts import, --help works
- [ ] L3: Quantifies forecast uncertainty
- [ ] L4: Outputs confidence intervals

---

### Prediction Markets Skills (10)

#### nixtla-polymarket-analyst
**Source**: PRD.md, ARD.md, SKILL.md
**Success Criteria** (from PRD Section 7):
- [ ] L1: SKILL.md valid, 4 scripts exist (fetch_contract.py, transform_data.py, forecast_contract.py, analyze_polymarket.py)
- [ ] L2: All scripts import, --help works
- [ ] L3: Full 5-step workflow executes with mock data
- [ ] L4: Report generated with forecast visualization
- [ ] L4: Description quality >= 90%
- [ ] L4: Execution < 60 seconds (target from PRD)

#### nixtla-market-risk-analyzer
**Source**: PRD.md, ARD.md, SKILL.md
**Success Criteria**:
- [ ] L1: SKILL.md valid, 4 scripts exist
- [ ] L2: All scripts import, --help works
- [ ] L3: Risk analysis executes with sample forecast
- [ ] L4: Outputs VaR, volatility metrics

#### nixtla-contract-schema-mapper
**Source**: SKILL.md + scripts/*.py
**Success Criteria**:
- [ ] L1: SKILL.md valid, transform_data.py exists
- [ ] L2: Script imports, --help works
- [ ] L3: Maps contract data to Nixtla schema
- [ ] L4: Outputs 3-column CSV (unique_id, ds, y)

#### nixtla-correlation-mapper
**Source**: SKILL.md + scripts/*.py
**Success Criteria**:
- [ ] L1: SKILL.md valid, all scripts exist
- [ ] L2: Scripts import, --help works
- [ ] L3: Computes correlations between series
- [ ] L4: Outputs correlation matrix

#### nixtla-arbitrage-detector
**Source**: SKILL.md + scripts/*.py
**Success Criteria**:
- [ ] L1: SKILL.md valid, all scripts exist
- [ ] L2: Scripts import, --help works
- [ ] L3: Detects price discrepancies
- [ ] L4: Outputs opportunities JSON

#### nixtla-event-impact-modeler
**Source**: SKILL.md + scripts/*.py
**Success Criteria**:
- [ ] L1: SKILL.md valid, all scripts exist
- [ ] L2: Scripts import, --help works
- [ ] L3: Models event impact on forecast
- [ ] L4: Outputs scenario analysis

#### nixtla-liquidity-forecaster
**Source**: SKILL.md + scripts/*.py
**Success Criteria**:
- [ ] L1: SKILL.md valid, all scripts exist
- [ ] L2: Scripts import, --help works
- [ ] L3: Forecasts liquidity metrics
- [ ] L4: Outputs liquidity forecast

#### nixtla-batch-forecaster
**Source**: SKILL.md + scripts/*.py
**Success Criteria**:
- [ ] L1: SKILL.md valid, all scripts exist
- [ ] L2: Scripts import, --help works
- [ ] L3: Batch processes multiple series
- [ ] L4: Outputs batch forecast CSV

#### nixtla-forecast-validator
**Source**: SKILL.md + scripts/*.py
**Success Criteria**:
- [ ] L1: SKILL.md valid, all scripts exist
- [ ] L2: Scripts import, --help works
- [ ] L3: Validates forecast quality
- [ ] L4: Outputs validation report

#### nixtla-model-selector
**Source**: SKILL.md + scripts/*.py
**Success Criteria**:
- [ ] L1: SKILL.md valid, all scripts exist
- [ ] L2: Scripts import, --help works
- [ ] L3: Recommends optimal model
- [ ] L4: Outputs model comparison

---

### Original Skills (8)

#### nixtla-experiment-architect
**Success Criteria**:
- [ ] L1: SKILL.md valid, 3 scripts exist
- [ ] L2: Scripts import, --help works
- [ ] L3: Scaffolds experiment structure
- [ ] L4: Creates experiment config

#### nixtla-prod-pipeline-generator
**Success Criteria**:
- [ ] L1: SKILL.md valid, 3 scripts exist
- [ ] L2: Scripts import, --help works
- [ ] L3: Generates pipeline code
- [ ] L4: Creates production-ready pipeline

#### nixtla-schema-mapper
**Success Criteria**:
- [ ] L1: SKILL.md valid, 2 scripts exist
- [ ] L2: Scripts import, --help works
- [ ] L3: Maps data schema
- [ ] L4: Outputs Nixtla-compatible CSV

#### nixtla-skills-bootstrap
**Success Criteria**:
- [ ] L1: SKILL.md valid
- [ ] L2: Instructions are clear
- [ ] L3: Bootstrap process documented
- [ ] L4: Examples provided

#### nixtla-skills-index
**Success Criteria**:
- [ ] L1: SKILL.md valid
- [ ] L2: Index is accurate
- [ ] L3: All skills listed
- [ ] L4: Descriptions match

#### nixtla-timegpt-finetune-lab
**Success Criteria**:
- [ ] L1: SKILL.md valid, scripts exist
- [ ] L2: Scripts import, --help works
- [ ] L3: Fine-tune workflow documented
- [ ] L4: Examples provided

#### nixtla-timegpt-lab
**Success Criteria**:
- [ ] L1: SKILL.md valid, 3 scripts exist (detect_environment.py, run_forecast.py, evaluate.py)
- [ ] L2: All scripts import, --help works
- [ ] L3: Full workflow executes with sample data
- [ ] L4: Forecast + evaluation complete

#### nixtla-usage-optimizer
**Success Criteria**:
- [ ] L1: SKILL.md valid, scripts exist
- [ ] L2: Scripts import, --help works
- [ ] L3: Analyzes usage patterns
- [ ] L4: Outputs optimization recommendations

---

## Test Execution Commands

```bash
# Run all Level 1 tests (structural)
python tests/skills/test_structural.py

# Run all Level 2 tests (functional)
python tests/skills/test_functional.py

# Run specific skill test
python tests/skills/test_skill.py nixtla-polymarket-analyst
```

---

**Last Updated**: 2025-12-10
