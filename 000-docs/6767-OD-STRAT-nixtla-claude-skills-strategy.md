# Nixtla Claude Skills Strategy (Canonical)

**Document ID**: 6767-OD-STRAT-nixtla-claude-skills-strategy.md
**Status**: Canonical Strategy Document
**Created**: 2025-11-30
**Author**: Intent Solutions (Claude Code)
**For**: Nixtla (Max Mergenthaler)
**Purpose**: Comprehensive skills portfolio strategy spanning OSS adoption, TimeGPT-paid tools, and internal GTM

---

## Executive Summary

This document defines the complete "Nixtla Skills Universe" - a portfolio of Claude Code skills that spans:
- **OSS adoption & education** (free users learning Nixtla libraries)
- **TimeGPT-paid "pro lab" tools** (paying customers getting production value)
- **Internal Nixtla GTM & reliability agents** (solutions engineering, SRE, sales enablement)

**Target**: 11 skills across 4 categories, prioritized P1 → P3
**Audience Matrix**: INT (internal) | OSS (open-source users) | PAY (TimeGPT customers)

---

## Skills Universe Overview

### Category Breakdown

| Category | Skills | Audience Focus | Business Impact |
|----------|--------|----------------|-----------------|
| **Foundation** | 2 | Everyone (INT, OSS, PAY) | Enable all other skills |
| **Core Builders** | 4 | PAY (primary), OSS (secondary) | Main value prop for TimeGPT users |
| **Education** | 2 | OSS (primary), PAY (secondary) | Adoption, marketing, "time-series school" |
| **Ops & GTM** | 3 | INT (primary), PAY (limited) | Internal efficiency, enterprise sales |

### Priority Distribution

- **P1** (Near-term): 5 skills - Foundation + Core builders
- **P1.5** (Early): 1 skill - Production pipelines
- **P2** (Mid-term): 4 skills - Education + optimization
- **P3** (Later): 1 skill - Vertical blueprints + incident SRE

---

## 1. Foundation & "Plumbing" Skills

*These are the foundation everything else sits on.*

---

### 1.1 nixtla-skills-bootstrap

**Audience**: INT ✅ | OSS ✅ | PAY ✅
**Priority**: P1
**Role**: One-shot setup skill

#### What It Does

Runs the Nixtla skills installer and narrates the process:

1. Executes `nixtla-skills init` / `update` in current repo
2. Explains in real-time:
   - "Cloning/updating Nixtla skills source..."
   - "Copying nixtla-* skills into .claude/skills/..."
   - "Installed skills: [list]"
3. Validates installation

#### Output

Working `.claude/skills/nixtla-*` directory in any project.

#### Business Value

- **For OSS**: Zero-friction onboarding to Nixtla ecosystem
- **For PAY**: Fast setup, professional experience
- **For INT**: Standardized deployment across customer projects

---

### 1.2 nixtla-timegpt-lab (Mode Skill)

**Audience**: INT ✅ | OSS ✅* | PAY ✅
**Priority**: P1
**Role**: Global "Nixtla-native" mode switcher

*\*OSS users get Nixtla library defaults even without TimeGPT key*

#### What It Does

Switches Claude into "Nixtla-native" mode for the session:

1. **Library Preferences**:
   - Prefer: `statsforecast`, `mlforecast`, `neuralforecast`, TimeGPT client
   - Avoid: Generic libraries (Prophet, ARIMA without Nixtla wrappers)

2. **Teaching Mode**:
   - Use Nixtla docs/teaching-guide concepts when explaining models/metrics
   - Default to Nixtla stacks when user says "build a forecast"

3. **Code Reasoning**:
   - Applies to all subsequent code generation in session
   - Suggests Nixtla patterns for data prep, CV, metrics

#### Business Value

- **For OSS**: "Nixtla-first" mindset → library adoption
- **For PAY**: Seamless TimeGPT integration by default
- **For INT**: Consistent Nixtla patterns across customer engagements

---

## 2. Core Builder Skills (For Users & Paying Customers)

*Main value props for TimeGPT + Nixtlaverse users.*

---

### 2.1 nixtla-schema-mapper

**Audience**: INT ✅ | OSS ✅ | PAY ✅
**Priority**: P1
**Role**: Get user data into Nixtla-ready schema fast

#### What It Does

1. **Data Inspection**:
   - Reads CSV/SQL/dbt model
   - Infers: `unique_id`, `ds`, `y`, exogenous features

2. **Code Generation**:
   - Pandas transform script OR
   - dbt/SQL model to produce Nixtla schema

3. **Documentation**:
   - Creates `NIXTLA_SCHEMA_CONTRACT.md` describing mapping
   - Includes validation rules, edge cases

#### Use Cases

- New TimeGPT users onboarding their first dataset
- Nixtla solution engineers migrating client data
- Self-serve data prep for OSS users

#### Business Value

- **For PAY**: Reduces onboarding time from weeks → hours
- **For OSS**: Lowers barrier to first forecast
- **For INT**: Standardized schema approach across customers

---

### 2.2 nixtla-experiment-architect

**Audience**: INT ✅ | OSS ✅** | PAY ✅
**Priority**: P1
**Role**: Build full benchmark harness

*\*\*OSS version treats TimeGPT as optional candidate model*

#### What It Does

1. **Config Setup**:
   - Asks: dataset path/table, target, horizon, freq
   - Creates/extends `forecasting/config.yml`:
     - Targets, freq, horizon, metrics, CV strategy

2. **Experiment Generation**:
   - Creates `forecasting/experiments.py`:
     - **StatsForecast models**: AutoARIMA, AutoETS, AutoCES, Theta, intermittent, multi-seasonal
     - **MLForecast pipelines**: Global ML models
     - **TimeGPT calls**: via `NixtlaClient` (PAY) or stubbed (OSS)
     - **Cross-validation**: Time-aware CV + metrics table

3. **Results Framework**:
   - Metrics comparison table (sMAPE, MASE, MAE, etc.)
   - Model ranking by accuracy/speed/cost

#### OSS vs PAY Behavior

- **PAY**: Wires real TimeGPT API calls
- **OSS**: TimeGPT calls guarded/stubbed, focus on baselines + ML

#### Business Value

**Single highest-impact skill for external devs.**

- **For PAY**: Proves TimeGPT value with their data
- **For OSS**: Complete forecasting lab without API costs
- **For INT**: Reusable benchmark framework for every customer

---

### 2.3 nixtla-timegpt-finetune-lab

**Audience**: INT ✅ | OSS ❌ | PAY ✅
**Priority**: P2 (after Experiment Architect is solid)
**Role**: Help users set up TimeGPT fine-tuning projects

#### What It Does

1. **Data Splitting**:
   - Define train/val/test splits appropriate for time series
   - Handles multiple series, hierarchical structures

2. **Fine-Tune Generation**:
   - Creates `forecasting/timegpt_finetune_job.py`:
     - Data prep for fine-tuning API
     - Fine-tune job submission
     - Model registry/versioning

3. **Comparison Framework**:
   - Hooks into `experiments.py` to compare:
     - TimeGPT zero-shot
     - TimeGPT fine-tuned
     - Classical/ML baselines

4. **Documentation**:
   - `FINE_TUNE_README.md` explaining:
     - How to launch fine-tune
     - How to re-evaluate
     - When fine-tuning makes sense

#### Business Value

**"Next-level deep" for premium users.**

- **For PAY**: Premium feature, justifies higher pricing
- **For INT**: Advanced customer success playbook
- **Not for OSS**: Requires paid TimeGPT API

---

### 2.4 nixtla-prod-pipeline-generator

**Audience**: INT ✅ | OSS (limited) | PAY ✅
**Priority**: P1.5 (early, after schema/experiment MVP works)
**Role**: Turn experiments into production pipelines

#### What It Does

1. **Pipeline Detection**:
   - Reads `forecasting/config.yml` + experiment results
   - Asks: Airflow? Prefect? dbt? Plain cron?

2. **Orchestration Code Generation**:
   - Creates `pipelines/` directory with:
     - DAG/flow definition (orchestration-specific)
     - Data loading from Nixtla schema
     - TimeGPT and/or StatsForecast/MLForecast calls
     - Forecast output + metadata logging

3. **Monitoring Setup**:
   - Creates `monitoring.py`:
     - Rolling backtests
     - Drift/anomaly checks
     - Fallback to baselines on TimeGPT failure

4. **Documentation**:
   - Deployment guide
   - Monitoring dashboard setup
   - Runbook for common issues

#### OSS vs PAY Behavior

- **PAY**: Full TimeGPT production integration
- **OSS**: Limited to StatsForecast/MLForecast pipelines

#### Business Value

**Shows "we don't just benchmark, we help you ship."**

- **For PAY**: Complete production onboarding
- **For INT**: Repeatable deployment pattern
- **For OSS**: Production-grade open-source pipelines

---

## 3. Education & Onboarding Skills

*Targeted to OSS + PAY for adoption and marketing value.*

---

### 3.1 nixtla-tutor (Teaching Guide Skill)

**Audience**: INT ✅ | OSS ✅ | PAY ✅
**Priority**: P2
**Role**: Teach Nixtla model families like a guided course

#### What It Does

1. **Persona Detection**:
   - Identifies: Data scientist? PM? Engineer?
   - Tailors teaching style accordingly

2. **Curriculum Delivery**:
   - Walks through:
     - Baselines vs classical vs ML vs TimeGPT
     - When to use what
     - Model selection decision trees
   - Uses Nixtla teaching guide + docs

3. **Interactive Exercises**:
   - Small exercises using user's own code/data
   - Optional: generates "lesson notebooks" tailored to repo

4. **Progress Tracking**:
   - Remembers what's been covered
   - Suggests next topics

#### Business Value

**Aligns with "we are the time-series school" positioning.**

- **For OSS**: Educational content marketing
- **For PAY**: Premium onboarding experience
- **For INT**: Standardized training material

---

### 3.2 nixtla-docs-to-experiments

**Audience**: INT ✅ | OSS ⚪ | PAY ⚪
**Priority**: P2–P3
**Role**: Turn doc snippets into tested experiments

#### What It Does

1. **Input Processing**:
   - Takes markdown/doc snippet describing a method
   - Example: "intermittent demand forecasting with ADIDA"

2. **Code Generation**:
   - Produces runnable experiment scripts
   - Includes minimal tests ensuring examples stay in sync

3. **Documentation Sync**:
   - Creates `experiments/from_docs/` directory
   - Links back to original docs

#### Business Value

- **For INT**: De-risks docs drift, keeps examples trustworthy
- **For OSS/PAY**: More reliable example code

---

## 4. Observability, Optimization & GTM Skills

*More for Nixtla's own team + enterprise-facing work.*

---

### 4.1 nixtla-usage-optimizer

**Audience**: INT ✅ | OSS ❌ | PAY ✅ (as review service)
**Priority**: P2
**Role**: Audit usage and propose optimizations

#### What It Does

1. **Code Scanning**:
   - Finds where TimeGPT is used
   - Finds where StatsForecast/MLForecast/NeuralForecast are used
   - Optionally ingests usage logs/metrics

2. **Analysis**:
   - Where TimeGPT is overkill (cheap baseline OK)
   - Where TimeGPT should be used more
   - Recommended routing rules
   - Guardrail/fallback patterns

3. **Report Generation**:
   - Creates `nixtla_usage_report.md`:
     - Cost optimization opportunities
     - Accuracy improvement opportunities
     - Risk mitigation recommendations

#### Business Value

**Internal CSM/solutions tool OR premium review offering.**

- **For INT**: Customer success playbook
- **For PAY**: Premium "optimization review" service
- **For OSS**: Not applicable (no usage logs)

---

### 4.2 nixtla-vertical-blueprint

**Audience**: INT ✅ | OSS ❌ | PAY ✅ (indirectly)
**Priority**: P3
**Role**: Generate vertical solution skeletons

#### What It Does

1. **Vertical Selection**:
   - Choose: Retail? Energy? Fintech? Pharma? Manufacturing?
   - Input sample schema for vertical

2. **Architecture Generation**:
   - Creates `verticals/<vertical>/ARCHITECTURE.md`:
     - Data sources (typical for vertical)
     - Nixtla components (which models/methods)
     - Monitoring/alerting patterns

3. **Starter Code**:
   - Notebooks/pipelines specific to vertical
   - Example datasets (if available)

4. **ROI Story**:
   - Boilerplate for sales decks
   - Typical metrics for vertical
   - Success stories template

#### Business Value

**Part GTM, part solution engineering.**

- **For INT**: Accelerates vertical GTM
- **For PAY**: Faster enterprise onboarding
- **For OSS**: Not applicable

---

### 4.3 nixtla-incident-sre (Optional Later)

**Audience**: INT ✅ | OSS ❌ | PAY ❌
**Priority**: P3
**Role**: Help SRE respond to production incidents

#### What It Does

1. **Log Ingestion**:
   - Reads logs on:
     - Error spikes
     - Accuracy drops
     - Latency/cost anomalies

2. **Root Cause Suggestions**:
   - Where to roll back to baselines
   - Which configs changed recently
   - What experiments to re-run

3. **Runbook Generation**:
   - Creates incident response guide
   - Links to relevant experiments/configs

#### Business Value

**Internal ops agent for Nixtla reliability.**

- **For INT**: SRE efficiency
- **For OSS/PAY**: Not applicable (internal only)

---

## Complete Skills Matrix

| Skill | INT | OSS | PAY | Priority | Category |
|-------|-----|-----|-----|----------|----------|
| **nixtla-skills-bootstrap** | ✅ | ✅ | ✅ | P1 | Foundation |
| **nixtla-timegpt-lab** | ✅ | ✅* | ✅ | P1 | Foundation |
| **nixtla-schema-mapper** | ✅ | ✅ | ✅ | P1 | Core Builder |
| **nixtla-experiment-architect** | ✅ | ✅** | ✅ | P1 | Core Builder |
| **nixtla-prod-pipeline-generator** | ✅ | Limited | ✅ | P1.5 | Core Builder |
| **nixtla-timegpt-finetune-lab** | ✅ | ❌ | ✅ | P2 | Core Builder |
| **nixtla-tutor** | ✅ | ✅ | ✅ | P2 | Education |
| **nixtla-docs-to-experiments** | ✅ | ⚪ | ⚪ | P2–3 | Education |
| **nixtla-usage-optimizer** | ✅ | ❌ | ✅ (review) | P2 | Ops & GTM |
| **nixtla-vertical-blueprint** | ✅ | ❌ | ✅ (via Nixtla) | P3 | Ops & GTM |
| **nixtla-incident-sre** | ✅ | ❌ | ❌ | P3 | Ops & GTM |

**Legend**:
- ✅ = Full support
- ✅* = Works in OSS mode (Nixtla libraries, TimeGPT optional)
- ✅** = TimeGPT treated as optional candidate model
- ⚪ = Limited/indirect value
- ❌ = Not applicable

---

## Phased Rollout Strategy

### Phase 0: Foundation (Week 1-2)
**Goal**: Enable all other skills

- ✅ nixtla-skills-bootstrap
- ✅ nixtla-timegpt-lab

**Deliverable**: Any user can install Nixtla skills and enter "Nixtla mode"

---

### Phase 1: Core Builder MVP (Week 3-6)
**Goal**: Prove TimeGPT value with user data

- ✅ nixtla-schema-mapper
- ✅ nixtla-experiment-architect

**Deliverable**:
- Users can prep their data
- Users can run full benchmark (baselines + ML + TimeGPT)
- Clear accuracy comparison

---

### Phase 1.5: Production Path (Week 7-10)
**Goal**: Show "we help you ship"

- ✅ nixtla-prod-pipeline-generator

**Deliverable**:
- Users can deploy TimeGPT to production
- Monitoring + fallback patterns included

---

### Phase 2: Education & Optimization (Week 11-16)
**Goal**: Deepen adoption and engagement

- ✅ nixtla-tutor
- ✅ nixtla-timegpt-finetune-lab (PAY only)
- ✅ nixtla-usage-optimizer (INT + PAY)

**Deliverable**:
- Guided learning experience
- Advanced fine-tuning for premium users
- Cost optimization playbook

---

### Phase 3: Vertical GTM & Ops (Week 17+)
**Goal**: Enterprise sales enablement + internal reliability

- ✅ nixtla-vertical-blueprint
- ✅ nixtla-docs-to-experiments
- ✅ nixtla-incident-sre

**Deliverable**:
- Vertical solution templates
- Reliable docs examples
- Internal SRE tooling

---

## Business Impact Summary

### For OSS Users (Adoption & Education)
**Skills**: 6 (bootstrap, mode, schema, experiment, tutor, docs-to-experiments)

**Value**:
- Zero-friction onboarding
- Complete forecasting lab
- Educational content
- "Time-series school" positioning

**Conversion Path**: OSS → PAY when they need TimeGPT scale/accuracy

---

### For TimeGPT Paying Customers (Production Value)
**Skills**: 9 (all core builders + optimization)

**Value**:
- Fast onboarding (schema mapper)
- Proven accuracy (experiment architect)
- Production deployment (pipeline generator)
- Advanced features (fine-tuning)
- Cost optimization (usage optimizer)
- Premium review service

**Retention**: Customers get more value from TimeGPT investment

---

### For Nixtla Internal (Efficiency & GTM)
**Skills**: All 11

**Value**:
- Solution engineering productivity (2-3x faster)
- Customer success playbooks
- Vertical GTM acceleration
- Sales enablement (ROI stories)
- SRE reliability tooling

**Impact**: Team can support 5-10x more customers

---

## Success Metrics

### Adoption Metrics (OSS)
- Skills installation rate (bootstrap)
- Session mode activation (timegpt-lab)
- Experiment creation rate (experiment-architect)
- Tutorial completion rate (nixtla-tutor)

### Conversion Metrics (OSS → PAY)
- TimeGPT trial starts from OSS users
- Experiment → TimeGPT upgrade rate
- Fine-tuning adoption (PAY only feature)

### Retention Metrics (PAY)
- Production pipeline deployments
- Usage optimization reviews conducted
- Customer-reported time savings
- Churn reduction in TimeGPT customers

### Internal Metrics (INT)
- Customer onboarding time (target: 50% reduction)
- Solution engineer capacity (target: 3x projects/engineer)
- Vertical GTM velocity (time to first vertical deal)
- SRE incident resolution time

---

## Competitive Differentiation

### vs Prophet/ARIMA (OSS)
**Nixtla Advantage**:
- Comprehensive skill ecosystem
- Guided learning (nixtla-tutor)
- Production-ready pipelines
- "Time-series school" positioning

### vs Forecast.io, DataRobot (Commercial)
**Nixtla Advantage**:
- Open-source foundation (OSS skills work without API)
- Developer-first (Claude Code integration)
- Transparent experimentation (experiment-architect)
- Flexible deployment (not locked to platform)

### vs Building In-House
**Nixtla Advantage**:
- Pre-built skills (weeks → hours)
- Battle-tested patterns (schema, pipelines, monitoring)
- Ongoing updates (skills evolve with Nixtla libraries)
- ROI calculator (usage-optimizer)

---

## Next Steps

### For Immediate Implementation
1. **Create skills repository structure** (`nixtla-claude-skills/`)
2. **Implement Phase 0** (bootstrap + mode skills)
3. **Test with pilot users** (Nixtla team + 2-3 friendly customers)
4. **Document skill API contracts** (input/output specs)

### For Max (Decision Point)
1. **Review this strategy document**
2. **Prioritize audience**: OSS adoption vs PAY retention vs INT efficiency
3. **Budget allocation**: Which phases to fund in Q1 2026
4. **Success criteria**: What metrics matter most

### For Future Expansion
1. **Community contributions** (OSS skills from users)
2. **Marketplace positioning** (Claude Code plugin hub)
3. **Enterprise packaging** (skills + support SLA)
4. **Vertical expansion** (more verticals in Phase 3)

---

## Questions for Max

1. **Audience Priority**: OSS adoption vs PAY retention vs INT efficiency?
2. **Timeline**: Full rollout (16+ weeks) or MVP only (6-8 weeks)?
3. **Resources**: Build in-house vs partner with Intent Solutions?
4. **Packaging**: Free OSS skills + premium PAY skills? Or all free with TimeGPT upsell?
5. **Success Definition**: What does "skills success" look like in 6 months?

---

## Appendices

### A. Skills Naming Convention
- `nixtla-<domain>-<role>` (e.g., `nixtla-timegpt-lab`, `nixtla-schema-mapper`)
- Domain: `timegpt`, `schema`, `experiment`, `prod`, `tutor`, `usage`, `vertical`, `incident`
- Role: `lab`, `mapper`, `architect`, `generator`, `optimizer`, `blueprint`, `sre`

### B. Technical Architecture
- **Skill Type**: Agent skills (not just prompt templates)
- **Dependencies**: Nixtla libraries, Claude Code SDK
- **Storage**: `.claude/skills/nixtla-*/`
- **Activation**: Auto-trigger or manual `/skill nixtla-*`

### C. Documentation Structure
```
nixtla-claude-skills/
├── README.md (this strategy)
├── skills/
│   ├── nixtla-skills-bootstrap/
│   ├── nixtla-timegpt-lab/
│   ├── nixtla-schema-mapper/
│   └── ... (11 total)
├── docs/
│   ├── SKILL_API_CONTRACTS.md
│   ├── INSTALLATION_GUIDE.md
│   └── CONTRIBUTION_GUIDE.md
└── examples/
    └── (per-skill examples)
```

---

**Last Updated**: 2025-11-30
**Status**: Canonical Strategy - Awaiting Max's Review
**Next Review**: After Phase 0 implementation (2 weeks)

