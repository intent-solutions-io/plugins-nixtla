# Nixtla Skills Developer Guide

**Last Updated**: 2025-12-07
**For**: New developers onboarding to the Nixtla Skills ecosystem

---

## Quick Start for New Devs

```bash
# Install the skills CLI
pip install -e 006-packages/nixtla-claude-skills-installer

# Install skills into your project
cd /path/to/your/project
nixtla-skills init

# Update to latest
nixtla-skills update
```

---

## Skills Overview

| Category | Count | Status |
|----------|-------|--------|
| **Live Skills** | 8 | Production-ready in `003-skills/` |
| **Planned Skills** | 8 | Specs only in `000-docs/planned-skills/` |

---

## 8 Live Skills (Production Ready)

These skills are implemented and ready to use. Located in `003-skills/.claude/skills/`.

### Core Forecasting

| Skill | Purpose | Trigger Phrases |
|-------|---------|-----------------|
| **nixtla-timegpt-lab** | Expert forecasting with TimeGPT, StatsForecast, MLForecast. Generates forecasts, analyzes trends, compares models. | "forecast my data", "predict sales", "analyze time series" |
| **nixtla-experiment-architect** | Scaffolds production-ready forecasting experiments. Creates configs, experiment harnesses, cross-validation workflows. | "set up forecasting experiment", "compare models", "benchmark TimeGPT" |
| **nixtla-timegpt-finetune-lab** | Fine-tune TimeGPT on custom datasets. Guides dataset prep, job submission, model comparison. | "fine-tune TimeGPT", "train custom model", "optimize accuracy" |

### Data & Schema

| Skill | Purpose | Trigger Phrases |
|-------|---------|-----------------|
| **nixtla-schema-mapper** | Transforms data to Nixtla format (`unique_id`, `ds`, `y`). Infers column mappings, validates data quality. | "map data to Nixtla schema", "transform CSV", "convert to Nixtla format" |

### Production & Operations

| Skill | Purpose | Trigger Phrases |
|-------|---------|-----------------|
| **nixtla-prod-pipeline-generator** | Transforms experiments into production pipelines with Airflow/Prefect/cron orchestration. | "deploy to production", "create pipeline", "schedule forecasts" |
| **nixtla-usage-optimizer** | Audits Nixtla usage and recommends cost-effective routing strategies. | "optimize TimeGPT costs", "audit usage", "reduce API costs" |

### Meta/Utility

| Skill | Purpose | Trigger Phrases |
|-------|---------|-----------------|
| **nixtla-skills-bootstrap** | Installs/updates Nixtla skills via CLI. | "install Nixtla skills", "update skills", "set up Nixtla" |
| **nixtla-skills-index** | Lists all installed Nixtla skills with usage guidance. | "list skills", "what Nixtla skills exist", "which skill should I use" |

### Source Files

```
003-skills/.claude/skills/
├── nixtla-timegpt-lab/SKILL.md
├── nixtla-experiment-architect/SKILL.md
├── nixtla-timegpt-finetune-lab/SKILL.md
├── nixtla-schema-mapper/SKILL.md
├── nixtla-prod-pipeline-generator/SKILL.md
├── nixtla-usage-optimizer/SKILL.md
├── nixtla-skills-bootstrap/SKILL.md
└── nixtla-skills-index/SKILL.md
```

---

## 8 Planned Skills (Specs Ready for Development)

These skills have comprehensive PRD + ARD documentation but no implementation yet.
**Domain**: Prediction Markets + Time Series Forecasting

### Skill Specifications

| Skill | PRD | ARD | Description | Priority |
|-------|-----|-----|-------------|----------|
| **nixtla-polymarket-analyst** | [PRD](prediction-markets/nixtla-polymarket-analyst/PRD.md) | [ARD](prediction-markets/nixtla-polymarket-analyst/ARD.md) | Fetches Polymarket odds, forecasts with TimeGPT, generates analysis reports | Critical |
| **nixtla-arbitrage-detector** | [PRD](prediction-markets/nixtla-arbitrage-detector/PRD.md) | [ARD](prediction-markets/nixtla-arbitrage-detector/ARD.md) | Scans cross-platform pricing discrepancies (Polymarket vs Kalshi) | Critical |
| **nixtla-contract-schema-mapper** | [PRD](prediction-markets/nixtla-contract-schema-mapper/PRD.md) | [ARD](prediction-markets/nixtla-contract-schema-mapper/ARD.md) | Transforms prediction market data to Nixtla format | Critical |
| **nixtla-batch-forecaster** | [PRD](prediction-markets/nixtla-batch-forecaster/PRD.md) | [ARD](prediction-markets/nixtla-batch-forecaster/ARD.md) | Processes 10-100 contracts in parallel batches | High |
| **nixtla-event-impact-modeler** | [PRD](prediction-markets/nixtla-event-impact-modeler/PRD.md) | [ARD](prediction-markets/nixtla-event-impact-modeler/ARD.md) | Models exogenous event impact on contract prices | High |
| **nixtla-forecast-validator** | [PRD](prediction-markets/nixtla-forecast-validator/PRD.md) | [ARD](prediction-markets/nixtla-forecast-validator/ARD.md) | Validates forecast quality metrics, detects degradation | Medium |
| **nixtla-model-selector** | [PRD](prediction-markets/nixtla-model-selector/PRD.md) | [ARD](prediction-markets/nixtla-model-selector/ARD.md) | Auto-selects best model (StatsForecast vs TimeGPT) | Medium |
| **nixtla-liquidity-forecaster** | [PRD](prediction-markets/nixtla-liquidity-forecaster/PRD.md) | ❌ Missing | Forecasts orderbook depth and spreads | Low |

### What's in Each PRD/ARD?

**PRD (Product Requirements Document)**:
- User personas and stories
- Functional requirements (REQ-1, REQ-2, etc.)
- Success metrics and acceptance criteria
- SKILL.md frontmatter example (copy-paste ready)

**ARD (Architecture & Requirements Document)**:
- 5-step workflow with code examples
- API integration details (endpoints, auth, rate limits)
- Data flow architecture
- Error handling and fallback strategies
- Token budget analysis (<5,000 tokens)

### Directory Structure

```
000-docs/planned-skills/
├── README.md                          # This file
├── _templates/
│   ├── PRD-TEMPLATE.md               # Template for new PRDs
│   ├── ARD-TEMPLATE.md               # Template for new ARDs
│   └── AUDITOR-CHECKLIST.md          # Quality audit checklist
└── prediction-markets/
    ├── nixtla-polymarket-analyst/
    │   ├── PRD.md                    # Product requirements
    │   └── ARD.md                    # Architecture document
    ├── nixtla-arbitrage-detector/
    │   ├── PRD.md
    │   └── ARD.md
    ├── nixtla-contract-schema-mapper/
    │   ├── PRD.md
    │   └── ARD.md
    ├── nixtla-batch-forecaster/
    │   ├── PRD.md
    │   └── ARD.md
    ├── nixtla-event-impact-modeler/
    │   ├── PRD.md
    │   └── ARD.md
    ├── nixtla-forecast-validator/
    │   ├── PRD.md
    │   └── ARD.md
    ├── nixtla-model-selector/
    │   ├── PRD.md
    │   └── ARD.md
    └── nixtla-liquidity-forecaster/
        └── PRD.md                    # ⚠️ Missing ARD
```

---

## Developer Workflow

### To Work on a LIVE Skill

1. Navigate to `003-skills/.claude/skills/nixtla-{skill-name}/`
2. Edit `SKILL.md` (the skill definition)
3. Test by running `nixtla-skills init` in a test project
4. Run smoke tests: `python tests/test_skills_installer_e2e.py`

### To Implement a PLANNED Skill

1. Read the PRD: `000-docs/planned-skills/prediction-markets/nixtla-{skill}/PRD.md`
2. Read the ARD: `000-docs/planned-skills/prediction-markets/nixtla-{skill}/ARD.md`
3. Copy the SKILL.md frontmatter from PRD Section "SKILL.md Frontmatter Example"
4. Create: `003-skills/.claude/skills/nixtla-{skill}/SKILL.md`
5. Implement scripts in `003-skills/.claude/skills/nixtla-{skill}/scripts/`
6. Add references in `003-skills/.claude/skills/nixtla-{skill}/references/`
7. Update `003-skills/README.md` to include the new skill

### To Create a NEW Planned Skill

1. Use templates in `_templates/`
2. Create folder: `prediction-markets/nixtla-{skill-name}/`
3. Write PRD.md using `_templates/PRD-TEMPLATE.md`
4. Write ARD.md using `_templates/ARD-TEMPLATE.md`
5. Validate with `_templates/AUDITOR-CHECKLIST.md`

---

## Standards Reference

| Document | Location | Purpose |
|----------|----------|---------|
| **Global Standard** | `000-docs/077-SPEC-MASTER-claude-skills-standard.md` | Master spec for all skills |
| **Skill Standard** | `000-docs/041-SPEC-nixtla-skill-standard.md` | Nixtla-specific requirements |
| **Audit Report** | `000-docs/081-AA-AUDT-planned-skills-audit.md` | Latest audit of planned skills |
| **Skills Architecture** | `000-docs/038-AT-ARCH-nixtla-claude-skills-pack.md` | Overall architecture |

---

## Quick Links

- **Live Skills**: `003-skills/.claude/skills/`
- **Skills Installer**: `006-packages/nixtla-claude-skills-installer/`
- **Smoke Tests**: `tests/test_skills_installer_e2e.py`
- **CI Workflow**: `.github/workflows/skills-installer-ci.yml`

---

## Contact

**Maintainer**: Intent Solutions
**For**: Nixtla Plugin Showcase
