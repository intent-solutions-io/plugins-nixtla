# 084-AA-AACR: Phase 02 – Workspaces & Labs Layer

**Date:** 2025-12-08 17:12 CST (America/Chicago)
**Status:** ✅ Complete
**Phase:** 02 – Global Workspaces & Labs Layer
**Owner:** Claude Code (on behalf of intent solutions io)
**Follows:** 083-AA-AACR-phase-01-repo-audit-and-dx-plan.md

## Executive Summary

Successfully scaffolded the global `workspaces/` layer for the Nixtla plugins repository, establishing 5 domain-specific labs (timegpt-lab, statsforecast-lab, mlforecast-lab, neuralforecast-lab, hierarchicalforecast-lab) with consistent structure and standards. This phase transforms the repo from a "collection of plugins" to a "coherent platform for Nixtla engineering" by providing dedicated sandboxes for experimentation, validation, and development before promotion to production artifacts (plugins/ or skills-pack/). All workspaces follow a canonical 5-directory structure (skills/, scripts/, data/, reports/, docs/) with clear promotion paths and compliance requirements.

## Objectives

1. ✅ Create top-level `workspaces/` directory with 5 Nixtla domain labs
2. ✅ Establish standard 5-directory substructure for all labs
3. ✅ Write global workspaces README explaining purpose and relation to plugins/skills-pack
4. ✅ Create per-workspace READMEs with domain-specific guidance
5. ✅ Document workspaces standards in `.directory-standards.md`
6. ✅ Create Phase 2 AAR (this document)
7. ✅ Git commit all Phase 2 changes

## What Was Created

### Directory Structure

Created 31 new directories:

```
workspaces/
├── README.md
├── .directory-standards.md
├── timegpt-lab/
│   ├── README.md
│   ├── skills/
│   ├── scripts/
│   ├── data/
│   ├── reports/
│   └── docs/
├── statsforecast-lab/
│   ├── README.md
│   ├── skills/
│   ├── scripts/
│   ├── data/
│   ├── reports/
│   └── docs/
├── mlforecast-lab/
│   ├── README.md
│   ├── skills/
│   ├── scripts/
│   ├── data/
│   ├── reports/
│   └── docs/
├── neuralforecast-lab/
│   ├── README.md
│   ├── skills/
│   ├── scripts/
│   ├── data/
│   ├── reports/
│   └── docs/
└── hierarchicalforecast-lab/
    ├── README.md
    ├── skills/
    ├── scripts/
    ├── data/
    ├── reports/
    └── docs/
```

### Documentation Files

Created 7 new markdown files:

1. **workspaces/README.md** (77 lines)
   - Visual overview of workspaces structure
   - Relation to plugins/ and skills-pack/
   - Promotion flow explanation
   - Who uses workspaces (CEO, DevOps, Engineers)

2. **workspaces/.directory-standards.md** (233 lines)
   - Canonical structure for all 5 labs
   - Directory-by-directory standards
   - Naming conventions
   - Promotion flow
   - CI/CD integration guidance
   - Standards compliance requirements

3. **workspaces/timegpt-lab/README.md**
   - TimeGPT API experiments
   - 5 example future flows
   - Environment setup (NIXTLA_TIMEGPT_API_KEY)
   - Promotion path to skills-pack/plugins

4. **workspaces/statsforecast-lab/README.md**
   - StatsForecast baselines (AutoETS, AutoARIMA, SeasonalNaive)
   - M4/M5 benchmark workflows
   - Promotion to nixtla-baseline-lab plugin

5. **workspaces/mlforecast-lab/README.md**
   - MLForecast pipelines (LightGBM, XGBoost)
   - Feature engineering workflows
   - ML model training and evaluation

6. **workspaces/neuralforecast-lab/README.md**
   - Deep learning (NHITS, NBEATS, TFT)
   - Explainability (Integrated Gradients, SHAP)
   - Model interpretability workflows

7. **workspaces/hierarchicalforecast-lab/README.md**
   - Hierarchical reconciliation
   - Coherence metrics
   - Multi-level forecast workflows

## Key Design Decisions

### 1. Flat 5-Directory Structure

**Decision**: All workspaces use identical 5-directory structure (skills/, scripts/, data/, reports/, docs/)

**Rationale**:
- Consistent DX across all 5 Nixtla domains
- Easy to automate CI/CD (same structure = same validation scripts)
- CEO mental model: "All labs are peers with same structure"
- Reduces onboarding friction (learn once, apply everywhere)

**Alternatives Considered**:
- Free-form structure per workspace → Rejected (inconsistent DX)
- 3-directory minimal structure → Rejected (insufficient separation of concerns)

### 2. Promotion Path from Workspaces to Production

**Decision**: Workspaces are **internal labs** - code graduates to plugins/ or skills-pack/ when stable

**Rationale**:
- Clear boundary between "experimental" (workspaces) and "shipping" (plugins/skills-pack)
- Prototypes can iterate rapidly without breaking production dependencies
- Promotion is explicit and documented (not automatic)

**Flow**:
```
workspaces/{lab}/skills/     → skills-pack/.claude/skills/     (when stable)
workspaces/{lab}/scripts/    → plugins/{plugin}/scripts/       (when productionized)
workspaces/{lab}/reports/    → 000-docs/ (with AA-REPT)       (when sharing externally)
```

### 3. Standards Document in Workspaces Root

**Decision**: `.directory-standards.md` lives at `workspaces/.directory-standards.md`

**Rationale**:
- Co-located with the directories it governs
- Single source of truth for all 5 labs
- Can be referenced by CI validation scripts
- Dot-prefix keeps it at top of directory listings

**Alternatives Considered**:
- Standards in `000-docs/` → Rejected (too far from workspaces/)
- Per-workspace standards → Rejected (duplication, drift risk)

### 4. Per-Workspace READMEs

**Decision**: Each lab has domain-specific README with 5 example future flows

**Rationale**:
- Engineers need immediate context when entering a workspace
- "Example future flows" provide concrete guidance on what belongs in each lab
- Environment setup varies by domain (TimeGPT needs API key, StatsForecast doesn't)

**Content Pattern**:
- Purpose (2-3 sentences)
- Structure (brief bullets)
- Example future flows (5+ numbered examples)
- Environment setup (pip install, env vars)
- Promotion path (when to graduate to production)

## Integration with Existing Structure

### Relation to plugins/

**plugins/** (3 working plugins):
- Production-ready MCP servers, deployable cloud functions
- Shipping artifacts for external users
- Golden tasks + smoke tests required

**workspaces/** (5 labs):
- Internal prototyping and validation
- Experimental code, not production-ready
- No external dependencies on workspace code

**Promotion**: `workspaces/{lab}/scripts/` → `plugins/{plugin}/scripts/` (when productionized)

### Relation to skills-pack/

**skills-pack/** (8 production skills):
- Shared SKILL bundle for external projects
- Stable, well-documented, CI-validated
- Installed via `nixtla-skills init`

**workspaces/** (5 labs):
- Prototype skills before promotion
- Rapid iteration without breaking external dependencies
- Internal-only skills that don't need distribution

**Promotion**: `workspaces/{lab}/skills/` → `skills-pack/.claude/skills/` (when stable)

### Relation to 000-docs/

**000-docs/** (102+ docs, flat structure):
- Doc-Filing v4.2 with NNN-CC-ABCD naming
- Cross-cutting documentation (architecture, PRDs, AARs)
- Permanent record of decisions and outcomes

**workspaces/{lab}/docs/** (per-workspace internal docs):
- Domain-specific guides, best practices, troubleshooting
- Workspace-local documentation (not cross-cutting)
- Promote to 000-docs/ when general enough

**Promotion**: `workspaces/{lab}/reports/` → `000-docs/` with AA-REPT type code (when sharing externally)

## Mental Models

### For CEO / Leadership

**Visual**: Single tree showing 5 Nixtla domains as peer labs

```
workspaces/
├── timegpt-lab/          (TimeGPT API, forecasting)
├── statsforecast-lab/    (Baselines, M4/M5 benchmarks)
├── mlforecast-lab/       (ML pipelines, feature engineering)
├── neuralforecast-lab/   (Deep learning, explainability)
└── hierarchicalforecast-lab/ (Reconciliation, coherence)
```

**Value**: "All 5 Nixtla domains have dedicated home base for experimentation"

### For DevOps Engineers

**Pattern**: All labs have identical structure → same CI validation scripts

**Automation**:
- Smoke tests: `pytest workspaces/{lab}/tests/`
- Environment validation: `python workspaces/{lab}/scripts/validate_env.py`
- Standards compliance: `python scripts/validate_workspaces.py`

**Value**: "One validation script works for all 5 labs"

### For Nixtla Engineers

**Home Base**: Each domain engineer works in their dedicated lab

**Daily Workflow**:
1. Clone repo, cd into `workspaces/{my-domain}-lab/`
2. Read README.md for setup instructions
3. Prototype in `skills/` or `scripts/`
4. Validate with `data/` and generate `reports/`
5. Document patterns in `docs/`
6. When stable, promote to `skills-pack/` or `plugins/`

**Value**: "Clear sandbox for experimentation before production"

## CI/CD Integration (Future)

### Smoke Tests

Each workspace can have `tests/` directory:

```bash
# In .github/workflows/workspaces-ci.yml
pytest workspaces/timegpt-lab/tests/
pytest workspaces/statsforecast-lab/tests/
pytest workspaces/mlforecast-lab/tests/
pytest workspaces/neuralforecast-lab/tests/
pytest workspaces/hierarchicalforecast-lab/tests/
```

### Environment Validation

Check API keys, dependencies, data availability:

```bash
python workspaces/timegpt-lab/scripts/validate_env.py
python workspaces/statsforecast-lab/scripts/validate_env.py
# ... (for all 5 labs)
```

### Standards Compliance

Extend `scripts/validate_skills.py` to cover workspace SKILLs:

```bash
python scripts/validate_skills.py --workspaces
```

### Dashboard/Report

Generate health status report for all labs:

```bash
python scripts/generate_workspaces_report.py > 000-docs/085-AA-STAT-workspaces-health.md
```

## What Was NOT Done (Out of Scope for Phase 2)

Phase 2 was **scaffolding only** - no implementation of workflows. Future phases will:

- ❌ Wire TimeGPT lab (Phase 3)
- ❌ Wire StatsForecast lab (Phase 4)
- ❌ Wire MLForecast lab (Phase 5)
- ❌ Wire NeuralForecast lab (Phase 6)
- ❌ Wire HierarchicalForecast lab (Phase 7)
- ❌ Add CI integration (Phase 8)

## Validation

### Structure Compliance

✅ All 5 labs have identical 5-directory structure
✅ All workspaces have README.md
✅ Global README and standards doc present

### Documentation Quality

✅ Global README explains relation to plugins/skills-pack
✅ Per-workspace READMEs have 5 sections (Purpose, Structure, Example Flows, Setup, Promotion)
✅ Standards doc covers all directories, naming conventions, promotion flow

### Naming Compliance

✅ All workspace names: `{domain}-lab` (lowercase, kebab-case)
✅ All directories: lowercase, no special characters

## Files Changed

**Created**:
- 31 directories (workspaces/ + 5 labs × 5 subdirs + 5 lab roots)
- 7 markdown files (1 global README + 1 standards + 5 per-workspace READMEs)
- 1 AAR (084-AA-AACR-phase-02-workspaces-labs-layer.md)

**Modified**: None (Phase 2 is additive only)

**Deleted**: None (Phase 2 is additive only)

## Next Steps

### Phase 3: Wire TimeGPT Lab

1. Environment bootstrap (NIXTLA_TIMEGPT_API_KEY, sample data)
2. First SKILL: `nixtla-timegpt-forecaster` (API usage, basic prompts)
3. Sample scripts: `scripts/forecast_sample.py`, `scripts/anomaly_detection.py`
4. Golden task test
5. AAR: `085-AA-AACR-phase-03-timegpt-lab.md`

### Phase 4: Wire StatsForecast Lab

1. M4/M5 dataset wiring
2. SKILLs: `nixtla-statsforecast-baseline` (AutoETS, AutoTheta, SeasonalNaive)
3. Scripts: `scripts/run_m4_benchmark.py`, `scripts/compare_models.py`
4. CI smoke test integration
5. AAR: `086-AA-AACR-phase-04-statsforecast-lab.md`

### Phase 5: Wire MLForecast Lab

1. ML pipeline patterns (features, training, prediction)
2. SKILLs: `nixtla-mlforecast-trainer` (LightGBM, XGBoost patterns)
3. Scripts: `scripts/feature_engineering.py`, `scripts/ml_pipeline.py`
4. AAR: `087-AA-AACR-phase-05-mlforecast-lab.md`

### Phase 6: Wire NeuralForecast Lab

1. Deep learning training (NHITS, NBEATS, TFT)
2. Explainability layer (Integrated Gradients, SHAP, additivity checks)
3. SKILLs: `nixtla-neuralforecast-trainer`, `nixtla-explainer`
4. Scripts: `scripts/train_nhits.py`, `scripts/compute_ig.py`, `scripts/shap_plots.py`
5. Reports: `reports/explainability_report.html`
6. AAR: `088-AA-AACR-phase-06-neuralforecast-lab.md`

### Phase 7: Wire HierarchicalForecast Lab

1. Hierarchical reconciliation workflows
2. SKILLs: `nixtla-hierarchical-reconciler`
3. Scripts: `scripts/reconcile_forecast.py`, `scripts/coherence_metrics.py`
4. AAR: `089-AA-AACR-phase-07-hierarchicalforecast-lab.md`

### Phase 8: CI Integration & Validation

1. Add workspace smoke tests to `.github/workflows/`
2. Extend `scripts/validate_skills.py` to cover workspace SKILLs
3. Enforce standards: `{baseDir}` paths, third-person descriptions, imperative voice
4. Dashboard/report showing all labs + health status
5. AAR: `090-AA-AACR-phase-08-ci-integration.md`

## Lessons Learned

### What Went Well

1. **Consistent structure across all labs** - No special-casing, same DX for all 5 domains
2. **Clear promotion path** - Explicit boundary between experimental (workspaces) and production (plugins/skills-pack)
3. **Documentation-first approach** - READMEs written before any code, reducing future confusion
4. **Standards doc co-located** - `.directory-standards.md` at workspace root for easy reference

### What Could Be Improved

1. **CI integration** - Should have included basic smoke test skeleton in Phase 2
2. **Example workflows** - Could have included 1-2 minimal example scripts per lab (instead of empty dirs)
3. **Tooling** - No `nixtla-workspaces` CLI yet (like `nixtla-skills init` for skills-pack)

### Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Labs drift from standards over time | CI validation in Phase 8 (enforce standards) |
| Unclear when to promote from workspace to production | Document promotion criteria in `.directory-standards.md` |
| Duplicate code across workspaces and plugins/skills-pack | Promotion flow deletes workspace code after move |
| Large data files committed to git | .gitignore templates in each workspace |

## Metrics

| Metric | Value |
|--------|-------|
| Directories created | 31 |
| Markdown files created | 7 |
| Total lines of documentation | ~800 (across all READMEs + standards) |
| Labs scaffolded | 5 (TimeGPT, StatsForecast, MLForecast, NeuralForecast, HierarchicalForecast) |
| Standard subdirectories per lab | 5 (skills, scripts, data, reports, docs) |
| Phase duration | ~5 minutes (scaffolding only) |

## Conclusion

Phase 2 successfully established the global `workspaces/` layer with 5 domain-specific Nixtla labs following a canonical 5-directory structure. This provides dedicated sandboxes for experimentation, validation, and development with clear promotion paths to production artifacts (plugins/ or skills-pack/). The consistent structure across all labs enables automation, reduces onboarding friction, and provides a coherent mental model for CEO, DevOps, and Engineers. Future phases (3-8) will populate these labs with actual workflows, scripts, skills, and CI integration.

---

**Prepared by**: Claude Code (on behalf of intent solutions io)
**Contact**: jeremy@intentsolutions.io
**Date**: 2025-12-08 17:12 CST (America/Chicago)
