# Nixtla Skills & Standards Documentation Index

**Document ID**: 095-DR-REFF-nixtla-skills-and-standards-index
**Generated**: 2025-12-08
**Type**: Reference Index (DR-REFF)
**Purpose**: Comprehensive index of all skill composition, standards specs, and 6767 documents

---

## Master Standards (Authoritative)

These are the **single source of truth** for skill and plugin development.

### 1. Claude Skills Standard
- **File**: `077-SPEC-MASTER-claude-skills-standard.md`
- **Status**: AUTHORITATIVE
- **Version**: 2.0.0
- **Purpose**: Complete specification for Claude Skills (SKILL.md) structure, frontmatter, and best practices
- **Sources**: Anthropic official docs, Claude Code docs, community resources
- **Sections**:
  - Core concepts (What/When/How/Tools/Model)
  - YAML frontmatter fields (name, description, allowed-tools, version, etc.)
  - Instruction-body best practices
  - Security & safety guidance
  - Production-readiness checklist
  - Canonical SKILL.md template

### 2. Claude Code Plugins Standard
- **File**: `078-SPEC-MASTER-claude-code-plugins-standard.md`
- **Status**: AUTHORITATIVE
- **Purpose**: Complete specification for Claude Code plugins (MCP servers, slash commands, hooks)
- **Sections**: Plugin structure, MCP protocol, configuration, deployment

---

## 6767 Series: Core Standards & Strategy

The **6767 series** represents canonical, cross-repo standards for Nixtla development.

### Document Reference Sheet
- **File**: `001-DR-REFF-6767-canonical-document-reference-sheet.md`
- **Purpose**: Index of all 6767 documents with explanations
- **Key Info**: Naming convention, purpose of 6767 series

### 6767-a: Baseline Lab Architecture
- **File**: `6767-a-OD-ARCH-nixtla-claude-plugin-poc-baseline-lab.md`
- **Type**: Architecture (OD-ARCH)
- **Purpose**: Architecture for nixtla-baseline-lab plugin POC

### 6767-b: Baseline Lab Plan
- **File**: `6767-b-PP-PLAN-nixtla-claude-plugin-poc-baseline-lab.md`
- **Type**: Planning (PP-PLAN)
- **Purpose**: Implementation plan for baseline lab plugin

### 6767-c: Baseline Lab Product Overview
- **File**: `6767-c-OD-OVRV-nixtla-baseline-lab-product-overview.md`
- **Type**: Overview (OD-OVRV)
- **Purpose**: Product-level overview of baseline lab

### 6767-d: Baseline Lab Overview
- **File**: `6767-d-OD-OVRV-nixtla-baseline-lab-overview.md`
- **Type**: Overview (OD-OVRV)
- **Purpose**: Detailed overview of baseline lab functionality

### 6767-e: Enterprise Plugin README Standard
- **File**: `6767-e-OD-REF-enterprise-plugin-readme-standard.md`
- **Type**: Reference (OD-REF)
- **Purpose**: Standard template for enterprise plugin READMEs

### 6767-f: Enterprise Plugin Implementation Guide
- **File**: `6767-f-OD-GUIDE-enterprise-plugin-implementation.md`
- **Type**: Guide (OD-GUIDE)
- **Purpose**: How to implement enterprise-grade plugins

### 6767-g: Enterprise README Standard Implementation
- **File**: `6767-g-OD-STAT-enterprise-readme-standard-implementation.md`
- **Type**: Status (OD-STAT)
- **Purpose**: Implementation status of README standard

### 6767-h: Claude Skills Strategy ⭐
- **File**: `6767-h-OD-STRAT-nixtla-claude-skills-strategy.md`
- **Type**: Strategy (OD-STRAT)
- **Purpose**: High-level strategy for Nixtla Claude Skills development
- **Key Content**: Skills vs plugins, promotion path, versioning strategy

### 6767-i: Phase 01 AAR - Repo Status
- **File**: `6767-i-AA-AAR-phase-01-repo-status-and-testing-scaffold.md`
- **Type**: After-Action Review (AA-AAR)
- **Purpose**: Repository status and testing infrastructure setup

### 6767-j: Phase 02 AAR - Skills Installer E2E
- **File**: `6767-j-AA-AAR-phase-02-skills-installer-e2e-validation.md`
- **Type**: After-Action Review (AA-AAR)
- **Purpose**: Skills installer end-to-end validation

### 6767-k: Phase 03 AAR - Baseline Lab Cleanup
- **File**: `6767-k-AA-AAR-phase-03-baseline-lab-cleanup-and-hardening.md`
- **Type**: After-Action Review (AA-AAR)
- **Purpose**: Baseline lab cleanup and hardening phase

### 6767-m: Claude Skills Frontmatter Schema ⭐
- **File**: `6767-m-DR-STND-claude-skills-frontmatter-schema.md`
- **Type**: Standard (DR-STND)
- **Status**: CANONICAL - Cross-Repo Standard
- **Version**: 1.0.0
- **Purpose**: Authoritative YAML frontmatter schema for SKILL.md files
- **Key Content**:
  - Complete frontmatter field reference
  - Validation rules (name, description, allowed-tools)
  - Examples (valid/invalid)
  - Directory structure and token costs

### 6767-n: Claude Skills Authoring Guide ⭐
- **File**: `6767-n-DR-GUID-claude-skills-authoring-guide.md`
- **Type**: Guide (DR-GUID)
- **Purpose**: Step-by-step guide for writing Claude Skills
- **Key Content**: How to write descriptions, structure instructions, error handling

---

## Skills Implementation History

### Phase 01-03: Initial Implementation
- `019-AA-SUMM-claude-skills-implementation-summary.md` - Implementation summary
- `056-AA-AAR-nixtla-claude-skills-phase-01.md` - Phase 01 AAR
- `057-AA-AAR-nixtla-claude-skills-phase-02.md` - Phase 02 AAR
- `058-AA-AAR-nixtla-claude-skills-phase-03.md` - Phase 03 AAR

### Phase 04: Skills Rollout & Compliance
- `038-AT-ARCH-nixtla-claude-skills-pack.md` - Skills pack architecture
- `039-PP-PLAN-nixtla-skills-4-phase-rollout.md` - 4-phase rollout plan
- `040-AA-REPT-nixtla-claude-skills-phase-04.md` - Phase 04 report
- `041-AA-REPT-nixtla-skills-compliance-phase-01.md` - Compliance phase 01
- `042-AA-REPT-nixtla-skills-compliance-phase-02.md` - Compliance phase 02
- `043-AA-REPT-nixtla-skills-core-implementation-phase-02.md` - Core implementation
- `044-AA-REPT-nixtla-skills-installer-versioning-phase-03.md` - Installer versioning
- `046-AA-REPT-nixtla-skills-phase-04.md` - Phase 04 report

### Compliance Audits
- `047-AA-AUDIT-nixtla-skills-compliance-vs-anthropic-official.md` - Compliance vs Anthropic official
- `048-PP-PLAN-nixtla-skills-compliance-remediation.md` - Compliance remediation plan
- `060-AA-AUDT-generated-skills-compliance-audit.md` - Generated skills audit
- `064-QA-AUDT-claude-skills-compliance-audit.md` - QA compliance audit
- `081-AA-AUDT-planned-skills-audit.md` - Planned skills audit

### Individual Skill Audits & Postmortems

Each skill has paired audit + postmortem documents:

1. **Skill 1: nixtla-timegpt-lab**
   - Audit: `059-AA-AUDIT-skill-1-nixtla-timegpt-lab-individual.md`
   - Postmortem: `060-AA-POSTMORTEM-skill-1-nixtla-timegpt-lab.md`
   - Gap Analysis: `061-AA-GAP-skill-1-strategic-analysis-100-percent.md`

2. **Skill 2: nixtla-experiment-architect**
   - Audit: `062-AA-AUDIT-skill-2-nixtla-experiment-architect-individual.md`
   - Postmortem: `063-AA-POSTMORTEM-skill-2-nixtla-experiment-architect.md`

3. **Skill 3: nixtla-schema-mapper**
   - Audit: `065-AA-AUDIT-skill-3-nixtla-schema-mapper-individual.md`
   - Postmortem: `066-AA-POSTMORTEM-skill-3-nixtla-schema-mapper.md`

4. **Skill 4: nixtla-timegpt-finetune-lab**
   - Audit: `067-AA-AUDIT-skill-4-nixtla-timegpt-finetune-lab-individual.md`
   - Postmortem: `068-AA-POSTMORTEM-skill-4-nixtla-timegpt-finetune-lab.md`

5. **Skill 5: nixtla-prod-pipeline-generator**
   - Audit: `069-AA-AUDIT-skill-5-nixtla-prod-pipeline-generator-individual.md`
   - Postmortem: `070-AA-POSTMORTEM-skill-5-nixtla-prod-pipeline-generator.md`

6. **Skill 6: nixtla-usage-optimizer**
   - Audit: `071-AA-AUDIT-skill-6-nixtla-usage-optimizer-individual.md`
   - Postmortem: `072-AA-POSTMORTEM-skill-6-nixtla-usage-optimizer.md`

7. **Skill 7: nixtla-skills-bootstrap**
   - Audit: `073-AA-AUDIT-skill-7-nixtla-skills-bootstrap-individual.md`
   - Postmortem: `074-AA-POSTMORTEM-skill-7-nixtla-skills-bootstrap.md`

### Phase 10: Skills Standardization (Latest)
- `094-AA-AACR-phase-10-skills-standardization-nixtla-timegpt.md` - TimeGPT skills audit & fixes
- **Status**: ✅ Complete (2025-12-08)
- **Result**: 1 skill audited and fixed for Anthropic compliance

---

## Operational Guides

### Skills Operations
- `045-OD-DEVOPS-nixtla-skills-operations-guide.md` - Skills DevOps guide
- `global/003-GUIDE-devops-nixtla-skills-operations.md` - Global DevOps guide

### Comprehensive Guides
- `063-OD-GUID-comprehensive-plugins-skills-learning-guide.md` - Plugins + Skills learning
- `064-OD-GUID-skills-comprehensive-guide.md` - Comprehensive skills guide

---

## Release Documentation

- `075-OD-RELS-v1-2-0-claude-skills-pack-release.md` - v1.2.0 skills pack release

---

## Planned Skills (000-docs/planned-skills/)

### Core Forecasting Skills
Located in `000-docs/planned-skills/core-forecasting/`:
- `nixtla-anomaly-detector/SKILL.md` - Anomaly detection
- `nixtla-cross-validator/SKILL.md` - Cross-validation
- `nixtla-exogenous-integrator/SKILL.md` - Exogenous variables integration
- `nixtla-timegpt2-migrator/SKILL.md` - TimeGPT v1 → v2 migration
- `nixtla-uncertainty-quantifier/SKILL.md` - Uncertainty quantification

### Live Skills
Located in `000-docs/planned-skills/live/`:
- `nixtla-experiment-architect/SKILL.md` - Experiment design
- `nixtla-prod-pipeline-generator/SKILL.md` - Production pipeline generation
- `nixtla-schema-mapper/SKILL.md` - Data schema mapping
- `nixtla-timegpt-finetune-lab/SKILL.md` - TimeGPT fine-tuning
- `nixtla-timegpt-lab/SKILL.md` - TimeGPT lab environment
- `nixtla-usage-optimizer/SKILL.md` - API usage optimization

### Prediction Markets Skills
Located in `000-docs/planned-skills/prediction-markets/`:
- `nixtla-arbitrage-detector/SKILL.md` - Arbitrage opportunity detection
- `nixtla-batch-forecaster/SKILL.md` - Batch forecasting
- `nixtla-contract-schema-mapper/SKILL.md` - Contract schema mapping
- `nixtla-correlation-mapper/SKILL.md` - Correlation analysis
- `nixtla-event-impact-modeler/SKILL.md` - Event impact modeling
- `nixtla-forecast-validator/SKILL.md` - Forecast validation
- `nixtla-liquidity-forecaster/SKILL.md` - Liquidity forecasting
- `nixtla-market-risk-analyzer/SKILL.md` - Market risk analysis
- `nixtla-model-selector/SKILL.md` - Model selection
- `nixtla-polymarket-analyst/SKILL.md` - Polymarket analysis

---

## Document Naming Conventions

### NNN-CC-ABCD Format
- `NNN`: Sequential number (001-999)
- `CC`: Category code (DR, OD, PP, AA, QA, AT, etc.)
- `ABCD`: Type code (REFF, SPEC, STND, GUID, ARCH, PLAN, AAR, AUDT, etc.)

### 6767 Prefix
- Indicates **cross-repo canonical standard**
- Used for documents that apply across multiple Nixtla projects
- Followed by letter suffix (a-z) for sequence

### Category Codes
- `DR`: Design/Reference
- `OD`: Operational Documentation
- `PP`: Planning/Process
- `AA`: After-Action (Review/Report/Audit/Postmortem)
- `QA`: Quality Assurance
- `AT`: Architecture/Technical
- `SPEC`: Specification
- `STND`: Standard
- `GUID`: Guide
- `REFF`: Reference
- `AAR`: After-Action Review
- `AACR`: After-Action Comprehensive Review
- `AUDT`: Audit
- `SUMM`: Summary
- `ARCH`: Architecture
- `PLAN`: Plan
- `REPT`: Report

---

## Quick Reference: Key Documents

### For Writing New Skills
1. Start here: `077-SPEC-MASTER-claude-skills-standard.md` (complete spec)
2. Frontmatter: `6767-m-DR-STND-claude-skills-frontmatter-schema.md` (schema)
3. Authoring: `6767-n-DR-GUID-claude-skills-authoring-guide.md` (how-to)
4. Strategy: `6767-h-OD-STRAT-nixtla-claude-skills-strategy.md` (when to create)

### For Auditing Existing Skills
1. Checklist: `077-SPEC-MASTER-claude-skills-standard.md` (section 8: Production-Readiness Checklist)
2. Example: `094-AA-AACR-phase-10-skills-standardization-nixtla-timegpt.md` (audit template)
3. Compliance: `047-AA-AUDIT-nixtla-skills-compliance-vs-anthropic-official.md`

### For Plugin Development
1. Plugin spec: `078-SPEC-MASTER-claude-code-plugins-standard.md`
2. Enterprise standard: `6767-e-OD-REF-enterprise-plugin-readme-standard.md`
3. Implementation guide: `6767-f-OD-GUIDE-enterprise-plugin-implementation.md`

---

## Document Status

### Authoritative (Single Source of Truth)
- `077-SPEC-MASTER-claude-skills-standard.md` ✅
- `078-SPEC-MASTER-claude-code-plugins-standard.md` ✅
- `6767-m-DR-STND-claude-skills-frontmatter-schema.md` ✅

### Active References
- All 6767-series documents
- Phase 10 skills standardization AAR (latest)

### Historical/Archived
- Individual skill audits (059-074 series) - completed phases
- Early implementation reports (038-048 series) - historical context

---

## Total Document Count

- **6767 Series**: 11 documents (a-k, m, n)
- **Skill-Related**: 61 documents (specs, audits, guides, reports)
- **Master Standards**: 2 (077, 078)
- **Planned Skills**: 16 SKILL.md files (planned-skills/)
- **Active Skills**: 1 SKILL.md (002-workspaces/timegpt-lab/)

---

## Related Resources

### External
- Anthropic Agent Skills: https://platform.claude.com/docs/en/agents-and-tools/agent-skills
- Claude Code Skills: https://code.claude.com/docs/en/skills
- Anthropic Blog: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills

### Internal
- Repo root: `.claude/CLAUDE.md` - Project overview
- Skills pack: `skills-pack/.claude/skills/` - Production skills (when promoted)
- Plugins: `plugins/` - MCP servers and slash commands

---

**Last Updated**: 2025-12-08
**Maintained By**: Intent Solutions (Jeremy Longshore)
**Purpose**: Central index for all skill and standard documentation
**Status**: Living Document - Update when new standards or skills are created
