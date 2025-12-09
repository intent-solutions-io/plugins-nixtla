# Enterprise Plugin Showcase - README Standard

**Doc ID:** 6767-OD-REF-enterprise-plugin-readme-standard
**Version:** 1.0.0
**Created:** 2025-11-30
**Author:** Intent Solutions
**Status:** Active Reference
**Classification:** Internal Standard

-----

## Purpose

This document defines how Intent Solutions structures private repositories for enterprise sponsors. These repos demonstrate Claude Code plugin capabilities and serve as business development tools to propose development engagements.

When Claude Code is working in an enterprise plugin showcase repository, it should follow this standard for all README creation, plugin documentation, and repository organization.

-----

## When This Standard Applies

Use this standard when:

- Creating a new private repo for an enterprise sponsor
- Adding plugins to an existing enterprise showcase repo
- Restructuring documentation in a sponsor repo
- The repo name follows the pattern `[company]-plugin-showcase` or similar

Do not use this standard for:

- The main public claude-code-plugins-plus marketplace
- Personal projects or open-source community repos
- Client delivery repos (those have different standards)

-----

## Repository Structure

An enterprise plugin showcase repo should be organized as follows:

```
[company]-plugin-showcase/
├── README.md                              # Navigation hub (follows this standard)
├── CHANGELOG.md                           # Release history
├── VERSION                                # Current version number
│
├── 000-docs/
│   ├── 6767-OD-REF-enterprise-plugin-readme-standard.md  # This document
│   │
│   ├── global/                            # Repo-wide documentation
│   │   ├── 000-EXECUTIVE-SUMMARY.md       # 1-pager for sponsor decision maker
│   │   ├── 001-ENGAGEMENT-OPTIONS.md      # Pricing, timelines, options
│   │   └── 002-DECISION-MATRIX.md         # Which plugin to build first
│   │
│   ├── 002a-planned-plugins/                           # Per-plugin documentation
│   │   └── [plugin-slug]/                 # One folder per plugin
│   │       ├── 01-BUSINESS-CASE.md
│   │       ├── 02-PRD.md
│   │       ├── 03-ARCHITECTURE.md
│   │       ├── 04-USER-JOURNEY.md
│   │       ├── 05-TECHNICAL-SPEC.md
│   │       └── 06-STATUS.md
│   │
│   └── archive/                           # Historical docs, AARs, research
│
├── 005-plugins/                               # Actual plugin source code
│   └── [plugin-slug]/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── commands/
│       ├── skills/
│       ├── scripts/
│       ├── tests/
│       └── README.md                      # Plugin-specific quick start
│
└── templates/                             # Doc templates (optional, for reference)
```

-----

## Plugin Lifecycle States

Every plugin in the showcase moves through these states. Use the appropriate icon in tables and status docs:

| State | Icon | Meaning | Documentation Required |
|-------|------|---------|------------------------|
| **Idea** | 💡 | Concept only, needs discovery | None - just a row in Ideas table |
| **Specified** | 📋 | Full docs written, ready to build | All 6 plugin docs |
| **In Progress** | 🔨 | Actively being developed | All 6 plugin docs + code started |
| **Working** | ✅ | Functional and demo-ready | All 6 plugin docs + working code + tests |
| **Production** | 🚀 | Deployed and maintained | All 6 plugin docs + CI/CD + versioned releases |

-----

## README Structure

The README.md is the navigation hub. It must contain these sections in this order:

### Section 1: Header

```markdown
# [Company] Plugin Showcase

> [One-line value proposition - what this solves for them]

**Sponsor:** [Company] ([Contact Name])
**Prepared by:** Intent Solutions (jeremy@intentsolutions.io)
**Version:** X.Y.Z | **Last Updated:** YYYY-MM-DD
**Status:** [X] working · [Y] specified · [Z] ideas
```

### Section 2: Quick Navigation

A table that routes different audiences to their starting point:

```markdown
## Quick Navigation

| I am a... | Start here |
|-----------|------------|
| 👔 Executive / Decision Maker | [Executive Summary](000-docs/global/000-EXECUTIVE-SUMMARY.md) |
| 💰 Evaluating Investment | [Engagement Options](000-docs/global/001-ENGAGEMENT-OPTIONS.md) |
| 🔧 Technical Evaluator | [Architecture Overview](#architecture-overview) |
| 👤 Potential User | [Demo](#demo) |
```

### Section 3: Portfolio Overview

Summary metrics showing plugin counts by state:

```markdown
## Portfolio Overview

| Status | Count | Description |
|--------|-------|-------------|
| ✅ Working | X | Ready to use now |
| 📋 Specified | Y | Full docs, ready to build |
| 🔨 In Progress | Z | Currently building |
| 💡 Ideas | W | Needs discovery |
| **Total** | **N** | |
```

### Section 4: Working Plugins Table

For each working plugin, show name, category, impact, and doc links:

```markdown
### ✅ Working Plugins

| Plugin | Category | Impact | Docs |
|--------|----------|--------|------|
| [Baseline Lab](005-plugins/baseline-lab/) | Efficiency | Faster debugging | [BC](000-docs/002a-planned-plugins/baseline-lab/01-BUSINESS-CASE.md) · [PRD](000-docs/002a-planned-plugins/baseline-lab/02-PRD.md) · [Arch](000-docs/002a-planned-plugins/baseline-lab/03-ARCHITECTURE.md) · [UJ](000-docs/002a-planned-plugins/baseline-lab/04-USER-JOURNEY.md) · [Tech](000-docs/002a-planned-plugins/baseline-lab/05-TECHNICAL-SPEC.md) |
```

The doc links use this compact format: `[BC] · [PRD] · [Arch] · [UJ] · [Tech]`

### Section 5: Specified Plugins Table

Same format as working plugins, for plugins with complete docs but no code yet.

### Section 6: In Progress Table

For plugins currently being built:

```markdown
### 🔨 In Progress

| Plugin | Category | Progress | ETA | Docs |
|--------|----------|----------|-----|------|
| Cost Optimizer | Efficiency | 60% | 2 weeks | [BC] · [PRD] · [Arch] · [UJ] · [Tech] |
```

### Section 7: Ideas & Backlog

This is where half-formed concepts live before they're fully specified:

```markdown
## 💡 Ideas & Backlog

Concepts that need discovery before specification.

| Idea | Category | Potential Impact | What's Needed |
|------|----------|------------------|---------------|
| Snowflake Adapter | Growth | Fortune 500 contracts | Discovery call with data team |
| Real-time Monitor | Growth | New market segment | POC with streaming data |
| Custom Model Trainer | Growth | Enterprise differentiation | Research on fine-tuning APIs |

**Have an idea?** Add it to this table. Once discovery is complete, create full docs and move to Specified.
```

This section is critical - it captures future possibilities without requiring full documentation effort.

### Section 8: Demo

Show how to try working plugins:

```markdown
## Demo

### Try It Now

\`\`\`bash
git clone [repo-url]
cd [repo]/005-plugins/[working-plugin]

# Setup if needed
[setup commands]

# In Claude Code:
/[command] [demo_params]
\`\`\`

### What You Get

- Concrete output 1
- Concrete output 2
- Concrete output 3
```

### Section 9: Architecture Overview

High-level ASCII diagram plus links to details:

```markdown
## Architecture Overview

\`\`\`
┌─────────────────────────────────────────────────────────────┐
│                      Claude Code CLI                         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Plugin 1   │  │  Plugin 2   │  │  Plugin N   │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
│         ▼                ▼                ▼                 │
│  ┌─────────────────────────────────────────────────────────┐│
│  │              [Company] APIs / SDKs                       ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
\`\`\`

See individual plugin [Architecture docs](000-docs/002a-planned-plugins/) for details.
```

### Section 10: Documentation Index

Explain the 6-doc standard:

```markdown
## Documentation Index

Every specified plugin includes 6 standard documents:

| Doc | Audience | Purpose |
|-----|----------|---------|
| 01-BUSINESS-CASE.md | Executive | ROI, market opportunity, recommendation |
| 02-PRD.md | Product | Requirements, user stories, success metrics |
| 03-ARCHITECTURE.md | Tech Lead | System design, integrations, constraints |
| 04-USER-JOURNEY.md | End User | Step-by-step experience with examples |
| 05-TECHNICAL-SPEC.md | Engineer | APIs, dependencies, implementation |
| 06-STATUS.md | Everyone | Current state, blockers, next steps |

### Global Documentation

| Doc | Purpose |
|-----|---------|
| [000-EXECUTIVE-SUMMARY.md](000-docs/global/000-EXECUTIVE-SUMMARY.md) | 1-page overview for sponsor |
| [001-ENGAGEMENT-OPTIONS.md](000-docs/global/001-ENGAGEMENT-OPTIONS.md) | Pricing, timelines, decision framework |
```

### Section 11: Engagement Options

```markdown
## Engagement Options

| Option | Scope | Timeline | Risk |
|--------|-------|----------|------|
| 🧪 **Evaluate** | Use working demos for 30 days | No commitment | None |
| 🎯 **Pilot** | 1 plugin to production | 4-6 weeks | Low |
| 🚀 **Platform** | 3+ plugins | 12-16 weeks | Medium |

**Details:** [Engagement Options](000-docs/global/001-ENGAGEMENT-OPTIONS.md)
```

### Section 12: Contact

```markdown
## Contact

**Jeremy Longshore** | Intent Solutions
📧 jeremy@intentsolutions.io
📞 251.213.1115
📅 [Schedule Call](https://calendly.com/intentconsulting)
```

### Section 13: License & Disclaimer

```markdown
## License & Disclaimer

**License:** MIT — You own what we build together.

**This is:**
- ✅ Experimental collaboration
- ✅ Business development prototype
- ✅ Proof of execution capability

**This is NOT:**
- ❌ Production SLA
- ❌ Official [Company] product
- ❌ Guaranteed ROI
```

### Section 14: Footer

```markdown
---

*Maintained by Intent Solutions | Sponsored by [Company]*
```

-----

## Per-Plugin Documentation Standard

When a plugin moves from Idea (💡) to Specified (📋), create all 6 docs in `000-docs/002a-planned-plugins/[plugin-slug]/`.

### 01-BUSINESS-CASE.md

**Audience:** Executive
**Purpose:** Justify investment in building this plugin

**Required sections:**

- **Problem Statement** - What pain point does this solve? Who feels it? What's the cost?
- **Target Customer** - Primary and secondary beneficiaries
- **Market Opportunity** - Size, competitive landscape, differentiation
- **ROI Calculation** - Table with before/after metrics and estimated value
- **Competitive Positioning** - Alternatives and why this is better
- **Risks & Mitigations** - What could go wrong and how to handle it
- **Recommendation** - Build / Don't Build / Needs Discovery, with rationale

### 02-PRD.md

**Audience:** Product Manager
**Purpose:** Define what to build

**Required sections:**

- **Overview** - One paragraph summary
- **Goals & Non-Goals** - What we're building and explicitly what we're not
- **User Stories** - Table format: As a [role], I want [action], So that [benefit]
- **Functional Requirements** - Table with IDs and priorities
- **Non-Functional Requirements** - Performance, reliability, usability targets
- **Success Metrics** - How we measure if this worked
- **Scope** - MVP (Phase 1) vs Future (Phase 2+)

### 03-ARCHITECTURE.md

**Audience:** Technical Lead
**Purpose:** Design the system

**Required sections:**

- **System Context** - Where this fits in the ecosystem (ASCII diagram)
- **Component Design** - Major components and responsibilities
- **Data Flow** - Input → Processing → Output
- **Integrations** - External systems, APIs, auth methods
- **Technical Constraints** - Limitations and rationale
- **Security Considerations** - Auth, data handling, secrets
- **Scalability** - Current limits and future scaling

### 04-USER-JOURNEY.md

**Audience:** End User
**Purpose:** Show the complete experience

**Required sections:**

- **Persona** - Name, role, technical level, goal
- **Prerequisites** - What they need before starting
- **Journey Steps** - Numbered steps with commands, outputs, and what to expect
- **Complete Example** - Full walkthrough with real inputs/outputs
- **Error Scenarios** - What can go wrong and how to recover
- **FAQ** - Common questions and answers

### 05-TECHNICAL-SPEC.md

**Audience:** Engineer
**Purpose:** Implementation guide

**Required sections:**

- **Technology Stack** - Languages, frameworks, versions
- **Dependencies** - Required packages and services
- **API Reference** - Commands, parameters, return values
- **Configuration** - Environment variables, config files
- **File Structure** - Directory layout with explanations
- **Testing** - How to run tests, coverage targets
- **Deployment** - Installation and setup
- **Troubleshooting** - Common issues and solutions

### 06-STATUS.md

**Audience:** Everyone
**Purpose:** Current state and next steps

**Required sections:**

- **Current Status** - Overall status badge (🟢🟡🔴⚪) plus status per aspect (Code, Tests, Docs, CI/CD)
- **Current State** - Narrative of what's done, in progress, not started
- **Recent Changes** - Table of recent updates
- **Blockers** - What's blocking progress, who owns it, ETA
- **Next Steps** - Prioritized action items
- **Decisions Needed** - Open questions requiring stakeholder input

-----

## Adding New Plugins

### Adding an Idea

When someone has a plugin concept that isn't fully formed:

1. Add a row to the "Ideas & Backlog" table in README.md
2. Include: Idea name, Category (Efficiency/Growth), Potential Impact, What's Needed (discovery call, research, POC, etc.)
3. No documentation required at this stage

### Specifying a Plugin

When ready to fully document a plugin:

1. Create folder: `000-docs/002a-planned-plugins/[plugin-slug]/`
2. Create all 6 documents following the standards above
3. Create plugin code folder: `005-plugins/[plugin-slug]/` with basic structure
4. Move the plugin from Ideas table to Specified table in README
5. Add doc links in the compact format: `[BC] · [PRD] · [Arch] · [UJ] · [Tech]`
6. Update the summary counts

### Building a Plugin

When actively developing:

1. Move from Specified to In Progress table
2. Add Progress percentage and ETA columns
3. Update 06-STATUS.md as work progresses
4. When functional, move to Working table
5. Update summary counts

-----

## Global Documentation

### 000-EXECUTIVE-SUMMARY.md

A single page that a busy executive can read in 5 minutes. Include:

- What this is (2-3 sentences)
- Why it matters to their business (3-5 bullets)
- What's ready now vs what's proposed
- Recommended next step (single clear action)
- Contact info

### 001-ENGAGEMENT-OPTIONS.md

Detailed breakdown of working together:

- Option 1: Evaluate (no commitment, try demos)
- Option 2: Pilot (one plugin, 4-6 weeks, low risk)
- Option 3: Platform (multiple plugins, 12-16 weeks)
- What's included in each option
- How to get started

### 002-DECISION-MATRIX.md

Help the sponsor decide which plugin to build first:

- Criteria: Business impact, development effort, risk, dependencies
- Scoring for each plugin
- Recommended priority order
- Quick wins vs strategic bets

-----

## Quality Checklist

Before sharing a repo with a sponsor, verify:

- [ ] README has all 14 sections in correct order
- [ ] Summary counts are accurate
- [ ] All doc links work
- [ ] Every Specified/Working plugin has all 6 docs
- [ ] No unfilled placeholder text like [Plugin Name] or [TODO]
- [ ] Demo commands actually work
- [ ] Contact info is current
- [ ] Version and date are updated

-----

## Examples

### Good Ideas Table Entry

```markdown
| Snowflake Adapter | Growth | Fortune 500 contracts, 10x deal sizes | Discovery call with enterprise data team to understand integration points |
```

### Good Plugin Table Entry

```markdown
| [Cost Optimizer](005-plugins/cost-optimizer/) | Efficiency | 30-50% API cost reduction | [BC](000-docs/002a-planned-plugins/cost-optimizer/01-BUSINESS-CASE.md) · [PRD](000-docs/002a-planned-plugins/cost-optimizer/02-PRD.md) · [Arch](000-docs/002a-planned-plugins/cost-optimizer/03-ARCHITECTURE.md) · [UJ](000-docs/002a-planned-plugins/cost-optimizer/04-USER-JOURNEY.md) · [Tech](000-docs/002a-planned-plugins/cost-optimizer/05-TECHNICAL-SPEC.md) |
```

### Good Status Badge

```markdown
| **Overall** | 🟡 In Progress |
| **Code** | 🟢 Complete |
| **Tests** | 🟡 Partial (65%) |
| **Docs** | 🟢 Complete |
| **CI/CD** | ⚪ Not Started |
```

-----

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-11-30 | Initial standard |

-----

## Related Documents

- Doc-Filing v3 specification (for document naming and organization)
- Claude Code Plugin Development Guide (for plugin code structure)
- Intent Solutions Engagement Templates (for pricing and SOWs)
