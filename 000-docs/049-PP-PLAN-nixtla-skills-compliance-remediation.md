# Nixtla Skills Compliance Remediation Plan

**Document ID**: 049-PP-PLAN-nixtla-skills-compliance-remediation.md  
**Type**: PP - Planning & Product  
**Status**: Ultra-Think Planning  
**Reference**: 048-AA-AUDIT (Audit), 6767-OD-CANON (Official Standard)  
**Date**: 2025-12-03

---

## Executive Summary

**Objective**: Achieve 100% compliance with official Anthropic Agent Skills standard

**Current Compliance**: 40% ⚠️  
**Target Compliance**: 100% ✅  
**Estimated Effort**: 7 hours  
**Priority**: CRITICAL

---

## Ultra-Think Analysis

### Problem Statement

Nixtla Skills Pack was implemented using custom frontmatter fields and patterns that are **not part of the official Anthropic specification**. This creates:

1. **Compatibility Risk**: Custom fields may conflict with future Anthropic features
2. **Performance Overhead**: Unnecessary tokens in Level 1 metadata
3. **Portability Issues**: Skills less portable across Claude surfaces
4. **Token Budget Violations**: 3 skills exceed 5,000 token limit

### Root Cause

**Issue**: Implemented skills before official Anthropic documentation was fully understood

**Contributing Factors**:
- Assumed extra frontmatter fields were standard
- Prioritized feature richness over spec compliance
- No validation against official documentation

### Strategic Approach

**Philosophy**: Compliance first, features second

**Principles**:
1. **Official spec is authoritative** - Remove anything not documented
2. **Progressive disclosure** - Split large content into referenced files
3. **Trigger clarity** - Every description must include "Use when [conditions]"
4. **Token efficiency** - Keep SKILL.md under 5,000 tokens

---

## Remediation Strategy

### Phase 1: Critical Compliance (Quick Wins)

**Goal**: Fix high-severity issues with minimal effort

**Timeline**: 2 hours

**Actions**:
1. Remove non-compliant frontmatter fields (all 7 skills)
2. Add "Use when [conditions]" to descriptions (all 7 skills)
3. Verify naming compliance (already compliant, no action)

**Impact**: Moves from 40% → 70% compliance

### Phase 2: Performance Optimization (Medium Effort)

**Goal**: Fix token budget violations

**Timeline**: 5 hours

**Actions**:
1. Split `nixtla-prod-pipeline-generator` (1146 → 600 lines)
2. Split `nixtla-timegpt-finetune-lab` (942 → 600 lines)
3. Split `nixtla-timegpt-lab` (877 → 600 lines)

**Impact**: Moves from 70% → 100% compliance

---

## Detailed Execution Plan

### Phase 1, Step 1: Remove Non-Compliant Frontmatter

**Affected Skills**: All 7 skills

**Current Frontmatter** (BEFORE):
```yaml
---
name: nixtla-timegpt-lab
description: "Mode skill that transforms Claude into a Nixtla TimeGPT forecasting expert"
allowed-tools: "Read,Write,Glob,Grep,Edit"     # ❌ REMOVE
mode: true                                      # ❌ REMOVE
model: inherit                                  # ❌ REMOVE
disable-model-invocation: false                 # ❌ REMOVE
version: "0.4.0"                               # ❌ REMOVE
license: "Proprietary - Nixtla Internal Use Only"  # ❌ REMOVE
---
```

**Target Frontmatter** (AFTER):
```yaml
---
name: nixtla-timegpt-lab
description: "Transforms Claude into Nixtla forecasting expert with TimeGPT-first guidance. Use when user needs forecasting, time series analysis, or TimeGPT assistance."
---
```

**Action**:
```bash
# For each skill, edit SKILL.md:
# 1. Keep: name, description
# 2. Remove: allowed-tools, mode, model, disable-model-invocation, version, license
```

**Validation**:
```bash
# Check frontmatter has only 2 fields
grep -A 10 "^---$" skills-pack/.claude/skills/nixtla-*/SKILL.md | grep ":" | wc -l
# Should show 14 (2 fields × 7 skills)
```

### Phase 1, Step 2: Add "Use when" Trigger Conditions

**Pattern**: "Does X, Y, Z. Use when [conditions]."

**Skill-by-Skill Updates**:

1. **nixtla-timegpt-lab**:
   - OLD: "Mode skill that transforms Claude into a Nixtla TimeGPT forecasting expert, biasing all suggestions toward Nixtla libraries and patterns"
   - NEW: "Transforms Claude into Nixtla forecasting expert with TimeGPT-first guidance and library recommendations. Use when user needs forecasting, time series analysis, or TimeGPT assistance."

2. **nixtla-experiment-architect**:
   - OLD: "Scaffold complete forecasting experiments with Nixtla libraries - creates config files, experiment harness, and evaluation workflows"
   - NEW: "Scaffolds complete forecasting experiments with config files, experiment harness, and evaluation workflows. Use when user wants to set up forecasting experiments, compare models, or create experiment structure."

3. **nixtla-schema-mapper**:
   - OLD: "Infer data schema and generate Nixtla-compatible transformations from CSV, SQL, Parquet, or dbt sources"
   - NEW: "Infers data schema and generates Nixtla-compatible transformations from CSV, SQL, Parquet, or dbt sources. Use when user has data in non-Nixtla format, needs schema mapping, or wants data transformation guidance."

4. **nixtla-timegpt-finetune-lab**:
   - OLD: "Guide users through TimeGPT fine-tuning workflows - from dataset prep to comparison experiments"
   - NEW: "Guides TimeGPT fine-tuning workflows from dataset prep to comparison experiments with evaluation. Use when user wants to fine-tune TimeGPT, improve model accuracy with custom data, or compare fine-tuned vs zero-shot performance."

5. **nixtla-prod-pipeline-generator**:
   - OLD: "Transform experiment workflows into production-ready inference pipelines with orchestration"
   - NEW: "Transforms experiments into production-ready Airflow/Prefect/cron pipelines with monitoring and fallback strategies. Use when user wants to deploy forecasts to production, automate inference, or operationalize models."

6. **nixtla-usage-optimizer**:
   - OLD: "Audit Nixtla library usage and suggest cost/performance routing strategies"
   - NEW: "Audits Nixtla library usage patterns and suggests cost/performance routing strategies with ROI analysis. Use when user wants to optimize TimeGPT costs, improve routing logic, or reduce API spending."

7. **nixtla-skills-bootstrap**:
   - OLD: "Install or update Nixtla Claude Skills in this project by calling the nixtla-skills CLI and narrating the installation process"
   - NEW: "Installs or updates Nixtla Claude Skills via nixtla-skills CLI with guided wizard and version tracking. Use when user wants to install skills, update skills, manage versions, or troubleshoot skill installation."

### Phase 2: Token Budget Remediation

#### Skill 1: nixtla-prod-pipeline-generator (1146 lines → 600 lines)

**Current Structure**:
```
nixtla-prod-pipeline-generator/
└── SKILL.md (1146 lines, ~5,700 tokens) ❌ OVER BUDGET
```

**Target Structure**:
```
nixtla-prod-pipeline-generator/
├── SKILL.md (600 lines, ~3,000 tokens) ✅
└── resources/
    ├── AIRFLOW_EXAMPLE.md (300 lines)
    ├── PREFECT_EXAMPLE.md (150 lines)
    └── MONITORING.md (96 lines)
```

**Content Split**:

**Keep in SKILL.md** (600 lines):
- Core workflow instructions
- When to use (trigger conditions)
- Orchestration platform decision tree
- High-level workflow (Extract → Transform → Forecast → Load → Monitor)
- Key patterns and best practices
- Reference to detailed examples

**Move to resources/AIRFLOW_EXAMPLE.md** (300 lines):
- Complete Airflow DAG code example
- Task definitions
- Airflow-specific configuration

**Move to resources/PREFECT_EXAMPLE.md** (150 lines):
- Complete Prefect flow example
- Prefect-specific patterns

**Move to resources/MONITORING.md** (96 lines):
- Monitoring module code
- Backtest functions
- Drift detection code

**SKILL.md will reference**:
```markdown
For complete Airflow DAG example, see `resources/AIRFLOW_EXAMPLE.md`.
For Prefect flow example, see `resources/PREFECT_EXAMPLE.md`.
For monitoring implementation, see `resources/MONITORING.md`.
```

#### Skill 2: nixtla-timegpt-finetune-lab (942 lines → 600 lines)

**Current Structure**:
```
nixtla-timegpt-finetune-lab/
└── SKILL.md (942 lines, ~4,700 tokens) ⚠️  NEAR LIMIT
```

**Target Structure**:
```
nixtla-timegpt-finetune-lab/
├── SKILL.md (600 lines, ~3,000 tokens) ✅
└── resources/
    ├── FINETUNE_JOB_TEMPLATE.py (200 lines)
    ├── TROUBLESHOOTING.md (92 lines)
    └── BEST_PRACTICES.md (50 lines)
```

**Content Split**:

**Keep in SKILL.md** (600 lines):
- Core fine-tuning workflow
- Requirements gathering questions
- Config.yml extension pattern
- High-level job submission steps
- Comparison experiment setup

**Move to resources/FINETUNE_JOB_TEMPLATE.py** (200 lines):
- Complete fine-tuning job script
- Executable Python code

**Move to resources/TROUBLESHOOTING.md** (92 lines):
- Common issues (5 scenarios)
- Solutions and workarounds

**Move to resources/BEST_PRACTICES.md** (50 lines):
- Fine-tuning best practices
- Model versioning
- Cost awareness

#### Skill 3: nixtla-timegpt-lab (877 lines → 600 lines)

**Current Structure**:
```
nixtla-timegpt-lab/
└── SKILL.md (877 lines, ~4,400 tokens) ⚠️  NEAR LIMIT
```

**Target Structure**:
```
nixtla-timegpt-lab/
├── SKILL.md (600 lines, ~3,000 tokens) ✅
└── resources/
    ├── ADVANCED_PATTERNS.md (177 lines)
    └── API_REFERENCE.md (100 lines)
```

**Content Split**:

**Keep in SKILL.md** (600 lines):
- Mode activation and behavior
- Core TimeGPT workflows
- Common patterns
- When-to-use guidance
- Basic examples

**Move to resources/ADVANCED_PATTERNS.md** (177 lines):
- Advanced TimeGPT patterns
- Complex use cases
- Edge case handling

**Move to resources/API_REFERENCE.md** (100 lines):
- TimeGPT API parameter reference
- Detailed API documentation

---

## Implementation Sequence

### Execution Order

1. **Phase 1, Step 1**: Remove non-compliant frontmatter (30 min)
2. **Phase 1, Step 2**: Add "Use when" clauses (1 hour)
3. **Checkpoint**: Validate Phase 1 (15 min)
4. **Phase 2, Skill 1**: Split prod-pipeline-generator (2 hours)
5. **Phase 2, Skill 2**: Split timegpt-finetune-lab (1.5 hours)
6. **Phase 2, Skill 3**: Split timegpt-lab (1.5 hours)
7. **Final Validation**: Re-audit all skills (30 min)

**Total Estimated Time**: 7 hours

### Validation Checkpoints

**After Phase 1**:
- [ ] All 7 skills have only `name` and `description` in frontmatter
- [ ] All 7 descriptions include "Use when [conditions]"
- [ ] No XML tags or reserved words

**After Phase 2**:
- [ ] All 7 skills under 5,000 tokens (~800 lines)
- [ ] Referenced files exist and contain moved content
- [ ] SKILL.md references new resource files

**Final Audit**:
- [ ] 100% compliance with 6767 canonical standard
- [ ] All skills load correctly in Claude Code
- [ ] Token budgets verified

---

## Risk Mitigation

### Risk 1: Breaking Existing Functionality

**Mitigation**:
- Back up all skills before changes
- Test each skill after modification
- Verify Claude can still activate skills

### Risk 2: Loss of Important Metadata

**Issue**: Removing `version`, `license`, `allowed-tools` fields

**Mitigation**:
- Document versions in installer CLI (keep in pyproject.toml)
- Move licensing info to repo README
- Trust Claude's tool selection (no manual restrictions)

### Risk 3: Content References Break

**Issue**: Moving content to `resources/` may break internal references

**Mitigation**:
- Update all internal links
- Test skills after splitting
- Verify Claude can read referenced files

---

## Success Criteria

### Quantitative Metrics

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Frontmatter compliance | 0% | 100% | ⏳ |
| Description "Use when" | 0% | 100% | ⏳ |
| Token budget compliance | 57% (4/7) | 100% (7/7) | ⏳ |
| Overall compliance | 40% | 100% | ⏳ |

### Qualitative Success

- [ ] Skills activate when appropriate
- [ ] Performance improves (faster loading)
- [ ] No regression in functionality
- [ ] Claude understands trigger conditions better

---

## Before/After Comparison (Summary)

**Full before/after report will be created post-implementation.**

### Frontmatter Comparison

**BEFORE** (Non-Compliant):
```yaml
---
name: nixtla-timegpt-lab
description: "..."
allowed-tools: "..."    # ❌
mode: true              # ❌
model: inherit          # ❌
disable-model-invocation: false  # ❌
version: "0.4.0"       # ❌
license: "..."         # ❌
---
```

**AFTER** (Compliant):
```yaml
---
name: nixtla-timegpt-lab
description: "Transforms Claude into Nixtla forecasting expert. Use when user needs forecasting or TimeGPT assistance."
---
```

### Token Budget Comparison

| Skill | Before (lines) | After (lines) | Reduction |
|-------|----------------|---------------|-----------|
| prod-pipeline-generator | 1146 | 600 | -48% |
| timegpt-finetune-lab | 942 | 600 | -36% |
| timegpt-lab | 877 | 600 | -32% |

---

## Next Steps

1. ✅ **Canonical document created** (6767)
2. ✅ **Audit complete** (048-AA-AUDIT)
3. ✅ **Plan created** (this document)
4. ⏳ **Execute Phase 1** (frontmatter + descriptions)
5. ⏳ **Execute Phase 2** (token budget fixes)
6. ⏳ **Create before/after report**
7. ⏳ **Re-audit and verify**

---

**Plan Status**: COMPLETE - Ready for Execution  
**Estimated Effort**: 7 hours  
**Priority**: CRITICAL  
**Date**: 2025-12-03
