# Phase 1 – Repo Audit & Plan: NeuralForecast Explainability

**Created**: 2025-12-08
**Auditor**: Claude Code (Staff-Level DevEx + MLOps Engineer)
**Purpose**: Strict, read-first audit to design DX plan for NeuralForecast explainability workflows
**Status**: Phase 1 Complete - Awaiting Review

---

## Executive Summary

This audit examines the Nixtla repo's current state to design a production-grade DX/DevOps plan for integrating NeuralForecast explainability workflows (integrated gradients, SHAP, additivity checks) into the existing Claude Skills infrastructure.

**Key Finding**: The repo has a **mature, well-structured foundation** for time-series forecasting workflows, but **zero neuralforecast/explainability code in production**. References exist only in design docs and archived plugins. This is a greenfield opportunity to implement explainability right the first time.

**Recommendation**: Proceed with phased implementation using existing skills patterns + new explainability-specific structures.

---

## 1. Repository Structure Discovery

### Top-Level Layout

```
nixtla/  (v1.6.0 - Business showcase for Nixtla CEO)
├── 000-docs/                    # Documentation (Doc-Filing v3.0 standard)
│   ├── global/                  #   Executive summaries, DevOps guides
│   ├── planned-skills/          #   21 generated skills (3 categories)
│   ├── planned-plugins/         #   Plugin design specs
│   ├── dev-planning-templates/  #   Templates for new features
│   └── archive/                 #   Historical docs
│
├── skills-pack/                 # Production Claude Skills
│   └── .claude/skills/          #   8 core skills with scripts/ + assets/
│       ├── nixtla-timegpt-lab
│       ├── nixtla-experiment-architect
│       ├── nixtla-schema-mapper
│       ├── nixtla-timegpt-finetune-lab
│       ├── nixtla-prod-pipeline-generator
│       ├── nixtla-usage-optimizer
│       ├── nixtla-skills-bootstrap
│       └── nixtla-skills-index
│
├── plugins/                     # Complete applications (3 working)
│   ├── nixtla-baseline-lab/     #   StatsForecast baselines (M4 benchmarks)
│   ├── nixtla-bigquery-forecaster/  BigQuery Cloud Functions
│   └── nixtla-search-to-slack/  #   Research aggregation + Slack
│
├── packages/                    # Installable packages
│   └── nixtla-claude-skills-installer/  CLI for skill installation
│
├── scripts/                     # Repo-level automation (13 scripts)
│   ├── overnight_skill_generator.py    # Vertex AI Gemini skill generation
│   ├── add_scripts_to_skills.py        # Code extraction automation
│   ├── validate_skills.py              # Strict compliance validator
│   ├── setup-dev-environment.sh
│   └── [9 more scripts]
│
├── demo-project/                # Example/testing workspace
│   ├── data/                    #   Sample datasets (M4, custom)
│   ├── forecasting/             #   Experiment runner
│   └── pipelines/               #   (Empty - planned)
│
├── tests/                       # Integration tests
├── archive/                     # Cleaned-up historical code
├── .github/workflows/           # 8 CI workflows
├── .claude/                     # Claude Code config
├── .vscode/                     # VS Code settings
│
├── pyproject.toml               # Python packaging + tool config
├── requirements.txt             # Core deps (nixtla, pandas, numpy)
├── requirements-dev.txt         # Dev deps (pytest, black, sphinx)
├── CLAUDE.md                    # AI assistant instructions (updated)
├── README.md                    # DevOps-first README
├── CHANGELOG.md                 # Detailed release history
└── VERSION                      # 1.6.0
```

### Structural Patterns

1. **Documentation First**: Doc-Filing v3.0 (`NNN-CC-ABCD-description.md`)
   - `NNN` = Sequential number (000-082)
   - `CC` = Category code (PP=Planning, AT=Architecture, AA=Audits, OD=Overview, DR=Reference)
   - Enforced via scripts, part of DevOps culture

2. **Skills = Scripts + SKILL.md**: Modern pattern (new in v1.6.0)
   - SKILL.md contains frontmatter + instructions
   - `scripts/` contains Python/shell code
   - `assets/templates/` for reusable templates
   - `resources/` for docs, guides, troubleshooting
   - `references/` for external links

3. **Dual Skill Locations**:
   - `skills-pack/.claude/skills/` = 8 production skills (installed by users)
   - `000-docs/planned-skills/` = 21 generated skills (3 categories: core-forecasting, prediction-markets, live)

4. **CI-First Culture**: 8 GitHub Actions workflows
   - Required to merge: `ci.yml` (lint, format, test)
   - Skills validation: `skills-validation.yml`
   - Cost-optimized (Linux-only for pushes, full matrix for PRs)

---

## 2. Tooling & Workflow Inventory

### Python Dependency Management

**Current State**: Modern, conventional Python packaging

- **Package Manager**: setuptools (pyproject.toml-based, PEP 621 compliant)
- **Core Dependencies** (requirements.txt):
  ```
  nixtla>=0.5.0        # TimeGPT client
  pandas>=2.0.0
  numpy>=1.24.0
  requests>=2.31.0
  pydantic>=2.0.0
  python-dotenv>=1.0.0
  click>=8.1.0
  ```
- **Nixtla Ecosystem** (commented out, install as needed):
  ```
  # statsforecast>=1.5.0      ✅ Used in baseline-lab
  # mlforecast>=0.10.0
  # neuralforecast>=1.6.0     ⚠️  NOT YET INSTALLED
  # hierarchicalforecast>=0.3.0
  ```

**Gaps for NeuralForecast Explainability**:
- Missing: `neuralforecast`, `captum` (for IG), `shap`, `matplotlib`, `plotly`
- Missing: `torch`/`pytorch` (neuralforecast dependency)

### CI/CD Workflows

All workflows in `.github/workflows/`:

| Workflow | Trigger | Purpose | Required? |
|----------|---------|---------|-----------|
| `ci.yml` | Push, PR | Lint, format, test | ✅ Yes (blocks merge) |
| `skills-validation.yml` | Push, PR | Strict skill compliance | ✅ Yes |
| `nixtla-baseline-lab-ci.yml` | Push, PR | Plugin smoke tests | Advisory |
| `skills-installer-ci.yml` | Push, PR | Installer E2E tests | Advisory |
| `plugin-validator.yml` | PR | Schema validation | Advisory |
| `gemini-pr-review.yml` | PR | AI code review | Advisory |
| `gemini-daily-audit.yml` | Schedule | Daily automated audit | Advisory |
| `deploy-bigquery-forecaster.yml` | Manual | Cloud Functions deploy | Manual |

**CI Philosophy** (from `ci.yml` header):
```yaml
# COST-OPTIMIZED CI STRATEGY (CTO Directive - December 2025)
# TIER 1 (Every push): Linux + Python 3.11 only (~2 min)
# TIER 2 (PRs to main): Full OS matrix, all Python versions (~15 min)
# TIER 3 (Weekly): Scheduled comprehensive audits
```

### DevEx Helpers

**Present**:
- ✅ `pyproject.toml` with black, isort, mypy, pytest config
- ✅ `.editorconfig` for consistent formatting
- ✅ `.flake8` for linting rules
- ✅ `scripts/setup-dev-environment.sh` (basic setup)
- ✅ `CLAUDE.md` (AI assistant instructions - just updated!)
- ✅ `CONTRIBUTING.md` (contributor guide)
- ✅ `FOR-MAX-QUICKSTART.md` (onboarding for Nixtla CEO)

**Missing**:
- ❌ No `.pre-commit-config.yaml` (pre-commit hooks disabled)
- ❌ No Makefile/justfile/taskfile (no task runner)
- ❌ No `noxfile.py` (no multi-env testing automation)
- ❌ No `pyproject.toml [tool.hatch]` or Poetry lock (sticking with setuptools)

**Developer Onboarding Path** (from README.md):
```bash
# 1. Health Check
python3 --version  # Need 3.10+
git clone ...
pip install -e . && pip install -r requirements-dev.txt

# 2. Smoke Test
pytest -v --tb=short

# 3. Baseline Lab Test (90 sec, offline)
cd plugins/nixtla-baseline-lab
./scripts/setup_nixtla_env.sh --venv
source .venv-nixtla-baseline/bin/activate
python tests/run_baseline_m4_smoke.py
```

---

## 3. Existing Skills + Explainability Code

### 3.1 Production Skills (8)

Located in `skills-pack/.claude/skills/`:

| Skill | Health | Has Scripts? | Relevant to Explainability? |
|-------|--------|--------------|----------------------------|
| `nixtla-timegpt-lab` | ✅ Healthy | Yes (4 scripts) | 🟡 Adjacent - forecasting workflows |
| `nixtla-experiment-architect` | ✅ Healthy | Yes (templates) | 🟢 Directly relevant - experiment design |
| `nixtla-schema-mapper` | ✅ Healthy | Yes (2 scripts) | 🔵 Indirectly - data prep |
| `nixtla-timegpt-finetune-lab` | ✅ Healthy | Yes (templates) | 🔵 Indirectly - model training |
| `nixtla-prod-pipeline-generator` | ✅ Healthy | Yes (templates) | 🟡 Adjacent - pipeline patterns |
| `nixtla-usage-optimizer` | ✅ Healthy | Yes (scripts) | ⚪ Not relevant |
| `nixtla-skills-bootstrap` | ✅ Healthy | Yes (generators) | ⚪ Not relevant (meta) |
| `nixtla-skills-index` | ✅ Healthy | Yes (catalog) | ⚪ Not relevant (meta) |

**Pattern Observed**: All 8 skills follow the new standard:
- YAML frontmatter with `name`, `description`, `allowed-tools`, `version`
- `scripts/` directory with extracted Python code
- `assets/templates/` for reusable code templates
- `resources/` for supporting docs

**Compliance**: 100% pass rate on `scripts/validate_skills.py` (strict mode)

### 3.2 Generated Skills (21)

Located in `000-docs/planned-skills/` (3 categories):

- **core-forecasting** (5): anomaly-detector, exogenous-integrator, uncertainty-quantifier, cross-validator, timegpt2-migrator
- **prediction-markets** (10): polymarket-analyst, arbitrage-detector, batch-forecaster, etc.
- **live** (6): Duplicates of production skills (for testing generation)

**Status**: Recently enhanced by `add_scripts_to_skills.py`:
- 16 skills updated with extracted scripts (Dec 8, 2025)
- File sizes grew 3-8x (scripts extracted from embedded code)
- All now have `scripts/` directories with working Python

**Relevant to Explainability**:
- `nixtla-uncertainty-quantifier` - Confidence intervals, prediction intervals
- `nixtla-cross-validator` - Model validation patterns

### 3.3 NeuralForecast / Explainability Code Search

**Query 1**: `neuralforecast|NeuralForecast|NHITS`
**Results**: 38 files found

**Breakdown**:
- ✅ **Design docs** (2):
  - `000-docs/016-AT-ARCH-plugin-08-nixtla-migration-assistant.md` - Migration patterns from Prophet/ARIMA to NeuralForecast
  - `000-docs/017-AT-ARCH-plugin-09-nixtla-forecast-explainer.md` - **Full explainability architecture spec**

- ✅ **Benchmark template** (1):
  - `plugins/nixtla-search-to-slack/skills/nixtla-model-benchmarker/assets/templates/benchmark_template.py`
  - Contains: `from neuralforecast import NeuralForecast` + `from neuralforecast.models import NHITS, NBEATS`

- ⚪ **Archive mentions** (35): All in `archive/backups-20251108/` (not production code)

**Query 2**: `captum|shap|explainability|interpret` (case-insensitive)
**Results**: 267 files found

**Breakdown**:
- ✅ **Core explainability doc**:
  - `000-docs/017-AT-ARCH-plugin-09-nixtla-forecast-explainer.md` (100 lines)
    - Phase 1: Decomposition (trend, seasonal, residual)
    - Phase 2: Feature Attribution (SHAP)
    - Phase 3: Narrative Generation
    - Phase 4: Visual Report

- 🟡 **Scattered mentions**: Mostly in:
  - Skill SKILL.md files (description text only, no code)
  - Generated skill documentation
  - Troubleshooting guides

- ❌ **Working code**: ZERO production implementations

### 3.4 Key Finding: Explainability Architecture Exists, Code Does Not

**Document**: `000-docs/017-AT-ARCH-plugin-09-nixtla-forecast-explainer.md`

**Summary**:
- **What**: Post-hoc explainability tool for TimeGPT forecasts
- **Why**: Enterprise blocker - risk committees reject black-box models
- **Who**: Finance teams, risk managers, executives, data scientists
- **Status**: Design Phase (not implemented)

**Proposed Components**:
1. Slash commands: `/nixtla-explain`, `/nixtla-quick-explain`, `/nixtla-decompose`
2. Agent skill: `nixtla-explainer-expert`
3. No MCP server (pure Python post-hoc analysis)

**Architecture Phases**:
```
TimeGPT Forecast (Black Box)
         ↓
Forecast Explainer (Glass Box)
  Phase 1: Decomposition
  Phase 2: Feature Attribution (SHAP)
  Phase 3: Narrative Generation
  Phase 4: Visual Report
         ↓
Explained Forecast Output
```

**Critical Insight**: This doc is 6+ months old, never implemented. Perfect foundation for our work.

---

## 4. DX & Structure Gap Analysis

### 4.1 Strengths (What's Working)

1. **Mature Documentation Culture**
   - Doc-Filing v3.0 enforced via scripts
   - 82 sequential docs (000-082) covering all aspects
   - Clear ownership: "Business showcase for Nixtla CEO"

2. **Modern Python Packaging**
   - PEP 621 compliant `pyproject.toml`
   - Clean dependency management
   - Tool configs consolidated (black, isort, mypy, pytest)

3. **Well-Defined Skill Pattern**
   - New standard (v1.6.0): SKILL.md + scripts/ + assets/ + resources/
   - 100% compliance on production skills
   - Automated validation via `scripts/validate_skills.py`

4. **Cost-Optimized CI**
   - Tiered approach (Linux-only → full matrix)
   - CTO directive enforced in YAML
   - 8 workflows covering all bases

5. **Working Example Code**
   - `plugins/nixtla-baseline-lab/` - Full MCP server, golden tasks, smoke tests
   - `demo-project/` - Data + experiment runner
   - Pattern library in existing skills

6. **AI-Assisted Workflows**
   - `overnight_skill_generator.py` - Vertex AI Gemini for bulk generation
   - `add_scripts_to_skills.py` - Automated code extraction
   - Recently improved 16 skills in one run

7. **Clear Entry Points**
   - `CLAUDE.md` - AI assistant instructions (just updated to v1.6.0)
   - `README.md` - DevOps-first structure
   - `FOR-MAX-QUICKSTART.md` - CEO onboarding

### 4.2 Weaknesses / Risks

1. **No NeuralForecast Production Code**
   - Library commented out in `requirements.txt`
   - Only 1 benchmark template file has imports
   - Zero working explainability implementations
   - Risk: Starting from scratch, no patterns to follow

2. **Dual Skill Locations (Confusing)**
   - Production: `skills-pack/.claude/skills/` (8 skills)
   - Generated: `000-docs/planned-skills/` (21 skills)
   - Some duplicates between locations
   - Risk: New engineers won't know where to put new skills

3. **No Task Runner**
   - No Makefile, justfile, or noxfile
   - Every command is raw bash in README
   - Risk: Inconsistent dev workflows, "works on my machine"

4. **Demo Project Underutilized**
   - `demo-project/pipelines/` is empty
   - No explainability examples
   - Risk: New patterns have nowhere to prototype

5. **Missing Explainability Dependencies**
   - No `neuralforecast`, `captum`, `shap`, `torch`
   - No plotting libraries for visual reports
   - Risk: Can't run any explainability code today

6. **Validation Script Duplication**
   - `scripts/validate_skills.py` exists
   - Old `tests/basic_validator.py` referenced in CLAUDE.md (now fixed)
   - Risk: Confusion about which validator to use

7. **Hardcoded Paths in Some Scripts**
   - Some automation scripts use absolute paths
   - Risk: Breaks Claude Skills' `{baseDir}` pattern

### 4.3 Opportunities / Quick Wins

1. **Leverage Existing Skill Pattern**
   - `nixtla-experiment-architect` = perfect template
   - Copy structure: SKILL.md + scripts/ + assets/templates/
   - Opportunity: 80% of boilerplate already solved

2. **Use Demo Project as Explainability Sandbox**
   - Add `demo-project/explain/` for prototyping
   - Add `demo-project/plots/` for visual outputs
   - Add `demo-project/reports/` for generated PDFs
   - Opportunity: Safe place to fail fast

3. **Extend Existing Benchmark Template**
   - `plugins/nixtla-search-to-slack/.../benchmark_template.py`
   - Already imports `NeuralForecast`, `NHITS`, `NBEATS`
   - Opportunity: Add IG/SHAP to working code

4. **Create Makefile for Common Tasks**
   - `make setup` - Install deps
   - `make test` - Run pytest
   - `make explain-demo` - Run explainability example
   - Opportunity: Standardize DX, onboard Nixtla engineers faster

5. **Unify Skill Locations**
   - Decide: Production = `skills-pack/`, Experimental = `000-docs/planned-skills/`
   - Document in CLAUDE.md
   - Opportunity: Reduce confusion for contributors

6. **Add Pre-Commit Hooks**
   - Black, isort, flake8 already configured
   - Just need `.pre-commit-config.yaml`
   - Opportunity: Catch issues before CI

7. **Resurrect Explainer Plugin Design**
   - `000-docs/017-AT-ARCH-plugin-09-nixtla-forecast-explainer.md` is complete
   - Just needs implementation
   - Opportunity: Clear roadmap already exists

---

## 5. Target Structure & Phase Plan

### 5.1 Proposed Directory Layout

```
{baseDir}/  (= /home/jeremy/000-projects/nixtla/)

Production Skills (User-Facing)
├── skills-pack/.claude/skills/
│   ├── nixtla-explain-lab/          # NEW - Phase 2
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   │   ├── decompose_forecast.py
│   │   │   ├── compute_ig.py        # Integrated Gradients
│   │   │   ├── compute_shap.py
│   │   │   └── generate_report.py
│   │   ├── assets/templates/
│   │   │   ├── explain_workflow.py
│   │   │   └── comparison_template.py
│   │   └── resources/
│   │       ├── EXAMPLES.md
│   │       ├── BEST_PRACTICES.md
│   │       └── TROUBLESHOOTING.md
│   │
│   └── [existing 8 skills...]

Experimental/Prototype Skills
├── 000-docs/planned-skills/
│   ├── explainability/              # NEW - Phase 3
│   │   ├── nixtla-additivity-checker/
│   │   ├── nixtla-explainer-comparator/
│   │   └── nixtla-shap-plotter/
│   └── [existing 3 categories...]

Demo/Sandbox Environment
├── demo-project/
│   ├── data/                        # Existing - sample datasets
│   ├── forecasting/                 # Existing - experiment runner
│   ├── explain/                     # NEW - Phase 2
│   │   ├── run_ig_example.py
│   │   ├── run_shap_example.py
│   │   ├── run_additivity_check.py
│   │   └── config.yml
│   ├── plots/                       # NEW - Phase 3
│   │   ├── decomposition/
│   │   ├── shap/
│   │   └── ig/
│   └── reports/                     # NEW - Phase 4
│       ├── html/
│       ├── pdf/
│       └── markdown/

DevEx Improvements
├── Makefile                         # NEW - Phase 2
├── .pre-commit-config.yaml          # NEW - Phase 2
└── scripts/
    ├── install-explainability-deps.sh  # NEW - Phase 2
    ├── validate-explainability-env.sh  # NEW - Phase 2
    └── [existing scripts...]

Documentation
├── 000-docs/
│   ├── 083-DR-GUID-explainability-quick-start.md  # NEW - Phase 3
│   ├── 084-DR-STND-explainability-patterns.md      # NEW - Phase 4
│   └── [existing docs...]

Tests
├── tests/
│   ├── test_explainability_skills.py  # NEW - Phase 3
│   └── [existing tests...]

CI/CD
├── .github/workflows/
│   ├── explainability-ci.yml       # NEW - Phase 4 (strict validator)
│   └── [existing 8 workflows...]
```

### 5.2 Phase Plan

---

#### **Phase 2: Foundation + Bootstrap Environment**

**Goal**: Set up explainability dependencies, DevEx helpers, and demo sandbox without touching production skills.

**Areas Modified**:
- `requirements.txt` - Add neuralforecast, captum, shap, matplotlib, plotly
- `demo-project/explain/` - NEW directory with example scripts
- `Makefile` - NEW task runner
- `.pre-commit-config.yaml` - NEW (optional but recommended)
- `scripts/install-explainability-deps.sh` - NEW helper script

**Deliverables**:
1. ✅ `requirements.txt` updated with explainability stack
2. ✅ `demo-project/explain/` with 3 working examples:
   - `run_ig_example.py` - Integrated Gradients on NHITS
   - `run_shap_example.py` - SHAP values for NeuralForecast
   - `run_additivity_check.py` - Verify IG additivity property
3. ✅ `Makefile` with targets:
   - `make setup` - Install all deps
   - `make setup-explain` - Install explainability deps only
   - `make test` - Run pytest
   - `make explain-demo` - Run all 3 examples
   - `make validate` - Run skills validator
4. ✅ `scripts/validate-explainability-env.sh` - Check deps installed
5. 📝 `000-docs/082-AA-AUDT-repo-audit-neuralforecast-explainability.md` (this doc)

**Gate**: Soft (advisory)
- Examples run without errors
- Dependencies install cleanly
- Documentation reviewed by Nixtla team

---

#### **Phase 3: Production Skill + Explainability Patterns**

**Goal**: Create first production explainability skill following existing patterns. Introduce strict validation.

**Areas Modified**:
- `skills-pack/.claude/skills/nixtla-explain-lab/` - NEW skill
- `000-docs/083-DR-GUID-explainability-quick-start.md` - NEW user guide
- `tests/test_explainability_skills.py` - NEW test suite
- `scripts/validate_skills.py` - Update to check explainability-specific patterns

**Deliverables**:
1. ✅ `nixtla-explain-lab` skill with:
   - SKILL.md with proper frontmatter
   - `scripts/decompose_forecast.py` - Trend/seasonal/residual
   - `scripts/compute_ig.py` - Integrated Gradients implementation
   - `scripts/compute_shap.py` - SHAP values implementation
   - `scripts/generate_report.py` - Markdown/HTML report generator
   - `assets/templates/explain_workflow.py` - Reusable workflow template
   - `resources/` with docs, examples, troubleshooting
2. ✅ Quick-start guide (10-minute read for Nixtla engineers)
3. ✅ Test coverage for all scripts (pytest + golden tasks)
4. ✅ Validator updated to enforce explainability patterns

**Gate**: Strict (hard blocker)
- `pytest tests/test_explainability_skills.py` passes
- `python scripts/validate_skills.py` passes
- Manual review: Nixtla engineer tests skill successfully

---

#### **Phase 4: Advanced Skills + Visual Reports**

**Goal**: Add SHAP plotting, additivity checker, explainer comparison. Introduce CI enforcement.

**Areas Modified**:
- `000-docs/planned-skills/explainability/` - NEW directory with 3 skills
- `demo-project/plots/` - NEW directory for generated visuals
- `demo-project/reports/` - NEW directory for PDF/HTML outputs
- `.github/workflows/explainability-ci.yml` - NEW workflow
- `000-docs/084-DR-STND-explainability-patterns.md` - NEW standards doc

**Deliverables**:
1. ✅ Three new experimental skills:
   - `nixtla-additivity-checker` - Verify IG sums to (y_pred - y_baseline)
   - `nixtla-explainer-comparator` - Compare IG vs SHAP vs LIME
   - `nixtla-shap-plotter` - Generate waterfall/force/summary plots
2. ✅ Visual output directory structure
3. ✅ PDF report generation (C-suite ready)
4. ✅ CI workflow enforcing explainability tests
5. ✅ Standards document (patterns, anti-patterns, gotchas)

**Gate**: Strict (CI must pass)
- `.github/workflows/explainability-ci.yml` green
- All 3 skills pass validation
- Visual outputs generated successfully in demo

---

#### **Phase 5: Integration + Packaging**

**Goal**: Integrate explainability into existing TimeGPT workflows. Package for installation.

**Areas Modified**:
- `skills-pack/.claude/skills/nixtla-timegpt-lab/` - Add explain option
- `packages/nixtla-claude-skills-installer/` - Add explainability skills
- `plugins/nixtla-baseline-lab/` - Add explainability to baselines

**Deliverables**:
1. ✅ `nixtla-timegpt-lab` enhanced with `/explain` flag
2. ✅ Skills installer updated to install explainability pack
3. ✅ Baseline lab enhanced with explainability metrics
4. ✅ End-to-end workflow:
   ```bash
   nixtla-skills init --include explainability
   ```

**Gate**: Strict (E2E test required)
- User can install + run explainability end-to-end
- Integration tests pass
- Documentation complete

---

#### **Phase 6: Production Hardening + Enterprise Features**

**Goal**: Make explainability enterprise-ready (performance, scale, compliance).

**Areas Modified**:
- `scripts/` - Add batch processing scripts
- `000-docs/` - Add compliance docs (SOX, Basel III mappings)
- `.github/workflows/` - Add performance benchmarks

**Deliverables**:
1. ✅ Batch explainability for 1000+ forecasts
2. ✅ Compliance documentation templates
3. ✅ Performance benchmarks (IG/SHAP computation time)
4. ✅ Caching layer for expensive computations
5. ✅ Multi-model explainability (NHITS, NBEATS, TFT)

**Gate**: Hard (business requirement)
- Nixtla CRO approves compliance docs
- Performance meets SLA (< 30s for single forecast explain)
- Tested on real customer data

---

### 5.3 Phase-Specific Skill Introductions

| Phase | Skill | Type | Purpose |
|-------|-------|------|---------|
| **Phase 2** | *(Bootstrap only)* | - | Demo examples, no skills yet |
| **Phase 3** | `nixtla-explain-lab` | Production | Core explainability (IG, SHAP, reports) |
| **Phase 4** | `nixtla-additivity-checker` | Experimental | Validation/debugging tool |
| **Phase 4** | `nixtla-explainer-comparator` | Experimental | IG vs SHAP vs LIME comparison |
| **Phase 4** | `nixtla-shap-plotter` | Experimental | Visual SHAP reports |
| **Phase 5** | *(Integration)* | - | Enhance existing skills |
| **Phase 6** | *(Enterprise)* | - | Batch processing, compliance |

---

## 6. Critical Decisions & Recommendations

### 6.1 Where to Put New Skills?

**Recommendation**: Use two-tier system (already in place):

1. **Production Skills** → `skills-pack/.claude/skills/`
   - User-facing, installed via `nixtla-skills init`
   - Must pass strict validation
   - Versioned, stable API
   - Example: `nixtla-explain-lab` (Phase 3)

2. **Experimental Skills** → `000-docs/planned-skills/explainability/`
   - Prototype/testing phase
   - Can break, iterate fast
   - Promoted to production when stable
   - Example: `nixtla-additivity-checker` (Phase 4)

**Rationale**: This pattern already exists (8 production + 21 generated), just needs documentation in CLAUDE.md.

### 6.2 NeuralForecast vs TimeGPT Explainability?

**Finding**: Current repo focuses on:
- TimeGPT (Nixtla's commercial API)
- StatsForecast (open-source baselines)

NeuralForecast mentioned in:
- Design docs (migration assistant, explainer)
- Benchmark template (NHITS, NBEATS)

**Recommendation**: Start with **NeuralForecast explainability** (Phase 2-4) because:
- Open-source, no API costs
- Integrated Gradients built into PyTorch models
- SHAP works with any model
- Can apply learnings to TimeGPT later (Phase 5-6)

**Note**: TimeGPT is a black-box API. True IG requires model gradients (not available). For TimeGPT, we're limited to:
- SHAP (model-agnostic)
- Decomposition (statsmodels)
- Permutation importance

### 6.3 Should We Use MCP Server Pattern?

**Current MCP Server**: `plugins/nixtla-baseline-lab/scripts/nixtla_baseline_mcp.py`

**Recommendation**: **No MCP server for Phase 2-3**
- Explainability is post-hoc analysis (not real-time forecasting)
- Pure Python scripts in `demo-project/explain/` are sufficient
- MCP adds complexity without benefit for prototyping

**Revisit in Phase 5**: If integrating with Claude Desktop, then yes.

### 6.4 Plotting Library Choice?

**Options**:
1. `matplotlib` - Standard, static plots
2. `plotly` - Interactive, web-friendly
3. `shap.plots` - Built-in SHAP visualizations

**Recommendation**: **All three**
- `matplotlib` - For PDF reports (Phase 4)
- `plotly` - For HTML reports (Phase 4)
- `shap.plots` - For SHAP-specific visuals (Phase 3-4)

Already in `requirements-dev.txt`: None. Need to add to `requirements.txt`.

### 6.5 Testing Strategy?

**Current Test Structure**:
- `tests/` - Integration tests
- `plugins/nixtla-baseline-lab/tests/` - Plugin-specific tests
- Golden tasks pattern (YAML-driven smoke tests)

**Recommendation**: Follow golden tasks pattern for explainability
```yaml
# tests/golden_tasks/explainability_ig.yaml
name: "Integrated Gradients - NHITS M4 Daily"
model: "NHITS"
dataset: "M4-Daily-sample"
explainer: "integrated_gradients"
expected_properties:
  - additivity: true  # IG should sum to (y_pred - y_baseline)
  - runtime_seconds: < 10
  - output_format: "markdown"
```

### 6.6 Documentation Naming Convention?

**Existing Pattern**: Doc-Filing v3.0 (`NNN-CC-ABCD-description.md`)

**Recommendation**: Continue using it
- This audit: `082-AA-AUDT-repo-audit-neuralforecast-explainability.md`
- Quick-start (Phase 3): `083-DR-GUID-explainability-quick-start.md`
- Standards (Phase 4): `084-DR-STND-explainability-patterns.md`

**Rationale**: Already enforced in repo, part of DevOps culture.

---

## 7. Files Touched in Phase 1 (This Audit)

**Created**:
- ✅ `/home/jeremy/000-projects/nixtla/000-docs/082-AA-AUDT-repo-audit-neuralforecast-explainability.md` (this file)

**Modified**:
- ❌ None (read-only phase)

**Confirmed**:
- No structural changes (no renames, moves, deletes)
- No code changes
- No dependency changes

---

## 8. Next Steps (After Review)

1. **Stakeholder Review**: Share this audit with:
   - Nixtla CEO (Max)
   - Jeremy Longshore (intent solutions io)
   - Any Nixtla engineers who will implement

2. **Decision Points**:
   - Approve Phase 2 structure?
   - Confirm NeuralForecast-first approach?
   - Agree on production vs experimental skill locations?

3. **Phase 2 Kickoff** (if approved):
   - Create `demo-project/explain/` with 3 examples
   - Update `requirements.txt` with explainability deps
   - Write `Makefile` for task automation
   - Run smoke tests

4. **Timeline** (estimated, not promised):
   - Phase 2: 1-2 days (bootstrap, no production code)
   - Phase 3: 3-5 days (first production skill + tests)
   - Phase 4: 3-5 days (advanced skills + visuals)
   - Phase 5: 2-3 days (integration)
   - Phase 6: 5-7 days (enterprise hardening)

---

## Appendix A: Risk Register

| Risk | Severity | Mitigation |
|------|----------|------------|
| NeuralForecast breaking changes | Medium | Pin versions in requirements.txt |
| PyTorch install issues on M1 Macs | Medium | Use CPU-only torch, document in README |
| Captum not maintained (last update 2023) | Low | SHAP is primary, Captum backup |
| SHAP slow on large datasets | High | Implement sampling, caching in Phase 6 |
| IG requires model retraining for baselines | Medium | Cache baseline models in demo-project/data/ |
| Explainability patterns fight Claude Skills `{baseDir}` | Low | Use relative paths everywhere |
| No Nixtla engineer to test | High | Jeremy Longshore validates initially |

---

## Appendix B: Explainability Stack

**Must Install (Phase 2)**:
```txt
# Core forecasting
neuralforecast>=1.6.0

# Deep learning
torch>=2.0.0
captum>=0.7.0  # Integrated Gradients

# Model-agnostic explainability
shap>=0.45.0

# Visualization
matplotlib>=3.7.0
plotly>=5.18.0
seaborn>=0.13.0

# Report generation
Jinja2>=3.1.0  # HTML templates
weasyprint>=60.0  # PDF from HTML (optional)
```

**Already Installed**:
- `pandas>=2.0.0` ✅
- `numpy>=1.24.0` ✅

---

## Appendix C: Explainability Methods Overview

| Method | Type | Pros | Cons | Use Case |
|--------|------|------|------|----------|
| **Integrated Gradients** | Gradient-based | Precise, satisfies axioms (additivity, sensitivity) | Requires model gradients, slow | Deep learning models (NHITS, NBEATS) |
| **SHAP** | Model-agnostic | Works with any model, theoretically sound | Slow on large datasets | TimeGPT (black box) |
| **Decomposition** | Statistical | Fast, interpretable | Assumes additive components | Classical time series (ARIMA, ETS) |
| **Permutation Importance** | Model-agnostic | Simple, fast | Unstable with correlated features | Feature selection |

**Recommendation for Nixtla**:
- **NeuralForecast** (NHITS, NBEATS): Start with IG (Phase 3), add SHAP (Phase 4)
- **TimeGPT**: SHAP only (no gradients available)
- **StatsForecast** (ETS, Theta): Decomposition (already implicit in models)

---

**End of Audit - Phase 1 Complete**

**Author**: Claude Code (Staff-Level DevEx + MLOps Engineer)
**Date**: 2025-12-08
**Status**: Ready for stakeholder review
