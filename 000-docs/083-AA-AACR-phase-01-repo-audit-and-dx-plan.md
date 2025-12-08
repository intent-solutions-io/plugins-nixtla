# 083-AA-AACR: Phase 01 – Repo Audit and DX Plan

**Date:** 2025-12-08 17:07 CST (America/Chicago)
**Status:** ✅ Complete
**Phase:** 01 – Repo Audit and DX Plan
**Owner:** Claude Code (on behalf of intent solutions io)

## Executive Summary

Performed comprehensive read-only audit of the Nixtla plugins repository to design a platform-grade structure for Nixtla domain workspaces (TimeGPT, StatsForecast, MLForecast, NeuralForecast, HierarchicalForecast). The repo currently exhibits strong documentation discipline (Doc-Filing v4.2), mature CI/CD (8 workflows, cost-optimized), and production-quality plugin/skills architecture (3 plugins, 8 skills-pack skills, 21 generated skills). However, Nixtla domain code is scattered across plugins and skills without a unified "lab" layer for experimentation and development. The proposed `workspaces/` layer will provide domain-specific sandboxes for prototyping, validation, and promotion to shipping artifacts, transforming the repo from "collection of plugins" to "coherent platform for Nixtla engineering."

## Key Findings

### Strengths

- **Mature Documentation Culture**: Doc-Filing v4.2 with 102+ docs in `000-docs/` (flat structure), enforced via CI validator
- **Clean Plugin Architecture**: 3 working plugins (baseline-lab, bigquery-forecaster, search-to-slack) with MCP servers, golden tasks, smoke tests
- **Production Skills Standard**: 8 skills in `skills-pack/` with extracted scripts, 100% compliance on `validate_skills.py`
- **Cost-Optimized CI/CD**: 8 GitHub Actions workflows with tiered execution (Linux-only → full matrix), all passing
- **Modern Python Packaging**: PEP 621 compliant `pyproject.toml`, clean dependency management (setuptools, Python 3.9-3.12)
- **AI-Assisted Workflows**: Vertex AI Gemini for bulk skill generation (`overnight_skill_generator.py`), automated code extraction (`add_scripts_to_skills.py`)
- **CEO-Friendly Documentation**: `FOR-MAX-QUICKSTART.md`, `CLAUDE.md`, DevOps playbook (`080-AA-AUDT`), executive summaries

### Weaknesses

- **No Unified Workspace Layer**: Nixtla domain code scattered across `plugins/`, `skills-pack/`, `demo-project/` without coherent organization
- **Unclear Experimentation Path**: No obvious "where do I prototype TimeGPT workflows before building a plugin?" location
- **Demo Project Underutilized**: `demo-project/` has only `data/`, `forecasting/`, `pipelines/` (empty) - not domain-structured
- **Domain Silos**: No clear home for:
  - TimeGPT experiments (API usage, prompts, anomaly detection)
  - StatsForecast baselines (M4/M5 benchmarks, model comparisons)
  - MLForecast pipelines (ML models, feature engineering)
  - NeuralForecast training (NHITS, NBEATS, explainability via IG/SHAP)
  - HierarchicalForecast reconciliation (coherent multi-level forecasts)
- **Skill Duplication Risk**: 8 skills-pack + 21 generated skills (3 categories) with some overlap, no clear "production vs experimental" boundary

### Opportunities

- **Create `workspaces/` Layer**: Top-level directory alongside `plugins/`, `skills-pack/`, `packages/` for domain-specific labs
- **Five Domain Labs**: `timegpt-lab/`, `statsforecast-lab/`, `mlforecast-lab/`, `neuralforecast-lab/`, `hierarchicalforecast-lab/`
- **Standard Substructure**: Each lab has `skills/`, `scripts/`, `data/`, `reports/`, `docs/` for consistent DX
- **Clear Promotion Path**: Workspaces → plugins (shipping MCP servers) OR skills-pack (reusable SKILLs)
- **CEO Mental Model**: Single tree visual showing all 5 Nixtla domains as peer "labs"
- **Engineer Home Base**: Each domain engineer has a clear sandbox for daily work

## Proposed Target Structure

```
nixtla/ (v1.6.0)
├── 000-docs/              # FLAT docs (v4.2 standard, 102+ files)
├── plugins/               # Shipping plugins (3 working)
│   ├── nixtla-baseline-lab/
│   ├── nixtla-bigquery-forecaster/
│   └── nixtla-search-to-slack/
├── skills-pack/           # Reusable SKILLs (8 production)
│   └── .claude/skills/
├── packages/              # Installable packages (skills installer CLI)
├── workspaces/            # 🆕 LABS LAYER (Phase 2+)
│   ├── timegpt-lab/       # TimeGPT API, prompts, anomaly detection
│   │   ├── skills/
│   │   ├── scripts/
│   │   ├── data/
│   │   ├── reports/
│   │   └── docs/
│   ├── statsforecast-lab/ # Classical baselines, M4/M5 benchmarks
│   │   ├── skills/
│   │   ├── scripts/
│   │   ├── data/
│   │   ├── reports/
│   │   └── docs/
│   ├── mlforecast-lab/    # ML pipelines, features, hyperparams
│   │   ├── skills/
│   │   ├── scripts/
│   │   ├── data/
│   │   ├── reports/
│   │   └── docs/
│   ├── neuralforecast-lab/ # NHITS, NBEATS, TFT, IG/SHAP explainability
│   │   ├── skills/
│   │   ├── scripts/
│   │   ├── data/
│   │   ├── reports/
│   │   └── docs/
│   └── hierarchicalforecast-lab/ # Reconciliation, coherence metrics
│       ├── skills/
│       ├── scripts/
│       ├── data/
│       ├── reports/
│       └── docs/
├── demo-project/          # Existing sandbox (can deprecate or merge into workspaces)
├── scripts/               # Repo-level automation (13 scripts)
├── tests/                 # Integration tests
├── .github/workflows/     # 8 CI workflows
└── [standard files]       # README, CLAUDE.md, pyproject.toml, etc.
```

## Proposed Phase Plan

**Phase 2 – Global Workspaces & Labs Layer** (this session, next)
- Scaffold `workspaces/` with 5 domain labs (empty structure)
- Create global README + standards file
- Per-workspace READMEs explaining purpose
- AAR + Git commit

**Phase 3 – Wire TimeGPT Lab**
- Environment bootstrap (NIXTLA_TIMEGPT_API_KEY, sample data)
- First SKILL: `nixtla-timegpt-forecaster` (API usage, basic prompts)
- Sample scripts: `scripts/forecast_sample.py`, `scripts/anomaly_detection.py`
- Golden task test

**Phase 4 – Wire StatsForecast Lab**
- M4/M5 dataset wiring
- SKILLs: `nixtla-statsforecast-baseline` (AutoETS, AutoTheta, SeasonalNaive)
- Scripts: `scripts/run_m4_benchmark.py`, `scripts/compare_models.py`
- CI smoke test integration

**Phase 5 – Wire MLForecast Lab**
- ML pipeline patterns (features, training, prediction)
- SKILLs: `nixtla-mlforecast-trainer` (LightGBM, XGBoost patterns)
- Scripts: `scripts/feature_engineering.py`, `scripts/ml_pipeline.py`

**Phase 6 – Wire NeuralForecast Lab**
- Deep learning training (NHITS, NBEATS, TFT)
- Explainability layer (Integrated Gradients, SHAP, additivity checks)
- SKILLs: `nixtla-neuralforecast-trainer`, `nixtla-explainer`
- Scripts: `scripts/train_nhits.py`, `scripts/compute_ig.py`, `scripts/shap_plots.py`
- Reports: `reports/explainability_report.html`

**Phase 7 – Wire HierarchicalForecast Lab**
- Hierarchical reconciliation workflows
- SKILLs: `nixtla-hierarchical-reconciler`
- Scripts: `scripts/reconcile_forecast.py`, `scripts/coherence_metrics.py`

**Phase 8 – CI Integration & Validation**
- Add workspace smoke tests to `.github/workflows/`
- Extend `scripts/validate_skills.py` to cover workspace SKILLs
- Enforce standards: `{baseDir}` paths, third-person descriptions, imperative voice
- Dashboard/report showing all labs + health status

## Relation to Existing Structure

- **plugins/**: Shipping artifacts (MCP servers, deployables) - stays unchanged
- **skills-pack/**: Shared SKILL bundle for external projects - stays unchanged
- **workspaces/**: Internal labs for prototyping, validation, and development - new, additive
- **Promotion flow**: `workspaces/timegpt-lab/skills/` → `skills-pack/.claude/skills/` (when stable)
- **Promotion flow**: `workspaces/statsforecast-lab/scripts/` → `plugins/nixtla-baseline-lab/` (when productionized)

intent solutions io — confidential IP
Contact: jeremy@intentsolutions.io
