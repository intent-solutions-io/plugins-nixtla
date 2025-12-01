# Nixtla Claude Skills: 4-Phase Rollout Plan

**Document ID**: 039-PP-PLAN-nixtla-skills-4-phase-rollout.md
**Created**: 2025-11-30
**Status**: Phase 1 In Progress
**Related**:
- [6767-OD-STRAT-nixtla-claude-skills-strategy.md](6767-OD-STRAT-nixtla-claude-skills-strategy.md) - Full strategy
- [038-AT-ARCH-nixtla-claude-skills-pack.md](038-AT-ARCH-nixtla-claude-skills-pack.md) - Architecture

---

## Executive Summary

This document outlines the **4-phase rollout plan** for the Nixtla Claude Skills Pack, transforming Claude Code into a Nixtla forecasting expert through 11 specialized AI agent skills.

**Timeline**: 8-12 weeks (2-3 weeks per phase)
**Deliverable**: Production-ready skills pack with installer CLI
**Success Metric**: 100+ users with measurable productivity gains

---

## Phase Overview

| Phase | Duration | Focus | Deliverables | Status |
|-------|----------|-------|--------------|--------|
| **Phase 1** | Week 1 | Skeleton + Docs | Directory structure, SKILL.md stubs, planning docs | ✅ In Progress |
| **Phase 2** | Weeks 2-4 | Core Skills | 3 fully implemented skills with examples | 🔲 Not Started |
| **Phase 3** | Weeks 5-7 | Installer + Bootstrap | CLI installer, auto-update mechanism | 🔲 Not Started |
| **Phase 4** | Weeks 8-12 | Advanced + Demo | 8 remaining skills, demo project, user testing | 🔲 Not Started |

---

## Phase 1: Skills Pack Skeleton + Docs

**Duration**: 1 week (Days 1-7)
**Goal**: Establish foundation and directory structure

### Scope

**Directory Structure**:
```
skills-pack/
└── .claude/
    └── skills/
        ├── nixtla-timegpt-lab/
        ├── nixtla-experiment-architect/
        ├── nixtla-schema-mapper/
        ├── nixtla-prod-pipeline-generator/
        ├── nixtla-timegpt-finetune-lab/
        └── nixtla-usage-optimizer/
```

**Documentation**:
- `038-AT-ARCH-nixtla-claude-skills-pack.md` - Architecture document
- `039-PP-PLAN-nixtla-skills-4-phase-rollout.md` - This rollout plan
- `000-docs/aar/2025-11-30-nixtla-claude-skills-phase-01.md` - Phase 1 AAR

**SKILL.md Stubs**: Each skill folder contains:
```yaml
---
name: skill-name
description: "WIP description"
allowed-tools: "Read,Write"
---

# TODO
This skill will be fully implemented in Phase 2.
```

### Success Criteria

- ✅ 6 skill directories created
- ✅ SKILL.md stubs in each directory
- ✅ Architecture document (038) complete
- ✅ Rollout plan (039) complete
- ✅ Phase 1 AAR documenting completion

### Deliverables Checklist

- [x] Create `skills-pack/.claude/skills/` directory structure
- [x] Create 6 skill folders (nixtla-*)
- [x] Write SKILL.md stubs with YAML frontmatter
- [x] Create `038-AT-ARCH-nixtla-claude-skills-pack.md`
- [x] Create `039-PP-PLAN-nixtla-skills-4-phase-rollout.md`
- [ ] Create `000-docs/aar/2025-11-30-nixtla-claude-skills-phase-01.md`
- [ ] Commit with message: `chore(nixtla-skills): complete phase-01-skeleton`

### Git Strategy

**Single commit** with all Phase 1 changes:
```bash
git add skills-pack/ 000-docs/038-* 000-docs/039-* 000-docs/aar/2025-11-30-nixtla-claude-skills-phase-01.md
git commit -m "chore(nixtla-skills): complete phase-01-skeleton"
git push origin main
```

---

## Phase 2: Core Skills Implementation

**Duration**: 3 weeks (Days 8-28)
**Goal**: Implement 3 foundational skills with comprehensive prompts

### Scope

**Skills to Implement** (Priority P1):
1. **nixtla-timegpt-lab** (Week 1)
   - 800+ word prompt
   - Mode skill: switches Claude into Nixtla-first thinking
   - 5+ examples covering TimeGPT, StatsForecast, MLForecast
   - Activation triggers: "forecast", "Nixtla", "TimeGPT"

2. **nixtla-experiment-architect** (Week 2)
   - 600+ word prompt
   - Design multi-model forecasting experiments
   - Generate baseline comparison workflows
   - Scaffold project structure with best practices

3. **nixtla-schema-mapper** (Week 2-3)
   - 500+ word prompt
   - Infer unique_id, ds, y columns from user data
   - Generate transformation code for Nixtla compatibility
   - Handle CSV, Parquet, SQL, JSON formats

### Implementation Checklist (Per Skill)

- [ ] Write comprehensive SKILL.md prompt (500+ words)
- [ ] Add 5+ realistic usage examples
- [ ] Create `examples/` directory with working code
- [ ] Write activation trigger tests
- [ ] Document common issues and troubleshooting
- [ ] Internal testing with Nixtla team (3+ testers)
- [ ] User testing with OSS community (5+ testers)

### Success Criteria

- 3 skills fully implemented (replace TODO with real prompts)
- 15+ total examples across all skills
- Positive feedback from 8+ testers
- All activation triggers validated
- Documentation includes troubleshooting guides

### Deliverables

- Updated SKILL.md files (no more TODO markers)
- `examples/` directories with working code
- Test suite in `tests/` for each skill
- Phase 2 AAR: `000-docs/aar/2025-11-30-nixtla-claude-skills-phase-02.md`

### Git Strategy

**3 commits** (one per skill):
```bash
# After nixtla-timegpt-lab complete
git commit -m "feat(skills): implement nixtla-timegpt-lab core prompt"

# After nixtla-experiment-architect complete
git commit -m "feat(skills): implement nixtla-experiment-architect"

# After nixtla-schema-mapper complete
git commit -m "feat(skills): implement nixtla-schema-mapper"
```

---

## Phase 3: Installer CLI + Bootstrap Skill

**Duration**: 3 weeks (Days 29-49)
**Goal**: Build automated installer for easy distribution

### Scope

**New Skill**: `nixtla-skills-bootstrap`
- Installer CLI: `nixtla-skills install`
- Update mechanism: `nixtla-skills update`
- Skill management: `nixtla-skills list`, `nixtla-skills uninstall`

**Features**:
1. **One-Command Install**: `npx nixtla-skills install`
2. **Dependency Detection**: Check for Claude Code installation
3. **Conflict Resolution**: Handle existing skills gracefully
4. **Version Management**: Track installed vs available versions
5. **Selective Install**: `nixtla-skills install nixtla-timegpt-lab`

### Implementation Details

**Technology Stack**:
- **Language**: Node.js (npx compatibility)
- **CLI Framework**: Commander.js or Yargs
- **File Operations**: fs-extra for copying skills
- **Config Storage**: `~/.nixtla-skills/config.json`

**Directory Structure**:
```
nixtla-skills-bootstrap/
├── package.json
├── bin/
│   └── nixtla-skills.js          # CLI entry point
├── src/
│   ├── installer.js              # Copy skills to ~/.claude/skills/
│   ├── updater.js                # Check for new versions
│   ├── validator.js              # Verify installation success
│   └── config.js                 # Manage user config
└── tests/
    └── integration.test.js       # E2E installer tests
```

**SKILL.md** (for Claude Code integration):
```yaml
---
name: nixtla-skills-bootstrap
description: "Install and manage Nixtla Claude skills"
allowed-tools: "Read,Write,Bash"
---

# Nixtla Skills Bootstrap

You are now in **Nixtla Skills Installer mode**.

When the user says "install Nixtla skills" or similar:
1. Check if npx is available
2. Run: npx nixtla-skills install
3. Verify installation success
4. Show post-install tips
```

### Success Criteria

- Installer works on macOS, Linux, Windows
- One-command install: `npx nixtla-skills install`
- Handles edge cases (existing skills, permissions, no Claude Code)
- Clear error messages and troubleshooting guidance
- 20+ successful test installations

### Deliverables

- `nixtla-skills-bootstrap/` npm package
- Published to npm registry
- `nixtla-skills` command available globally
- Phase 3 AAR: `000-docs/aar/2025-11-30-nixtla-claude-skills-phase-03.md`

### Git Strategy

```bash
git commit -m "feat(installer): implement nixtla-skills-bootstrap CLI"
git tag -a v1.0.0-beta -m "Beta release with installer"
git push origin main --tags
```

---

## Phase 4: Advanced Skills + Demo Project

**Duration**: 4 weeks (Days 50-78)
**Goal**: Complete remaining 8 skills, create showcase demo

### Scope

**Skills to Implement** (Priority P1.5-P3):

**Week 1-2**:
4. **nixtla-prod-pipeline-generator** (P1.5)
   - Generate production-ready inference code
   - Docker containers, Cloud Run configs, Airflow DAGs
   - Monitoring and alerting templates

5. **nixtla-timegpt-finetune-lab** (P2)
   - Guide TimeGPT fine-tuning workflows
   - Dataset preparation and validation
   - Compare base vs fine-tuned performance

6. **nixtla-usage-optimizer** (P2)
   - Analyze TimeGPT API usage patterns
   - Identify cost optimization opportunities
   - Generate usage reports and recommendations

**Week 3**:
7. **nixtla-tutor** (P2)
   - Interactive Nixtla learning and troubleshooting
   - Answer "how do I..." questions with runnable examples
   - Explain Nixtla concepts (conformal intervals, cross-validation)

8. **nixtla-docs-to-experiments** (P2-3)
   - Convert documentation examples to runnable code
   - Adapt Nixtla docs for user's specific data
   - Generate Jupyter notebooks from markdown examples

**Week 4**:
9. **nixtla-vertical-blueprint** (P3)
   - Industry-specific forecasting templates
   - Retail, finance, energy, healthcare use cases
   - Pre-built pipelines for common scenarios

10. **nixtla-incident-sre** (P3)
    - Production incident debugging (Nixtla internal)
    - Diagnose TimeGPT API errors
    - Analyze forecast quality issues

### Demo Project: "Nixtla Skills Showcase"

**Purpose**: Demonstrate all 11 skills in action

**Scenario**: E-commerce sales forecasting project
1. User starts with raw sales CSV
2. **nixtla-timegpt-lab** activates (mode skill)
3. **nixtla-schema-mapper** infers data structure
4. **nixtla-experiment-architect** designs multi-model comparison
5. **nixtla-prod-pipeline-generator** creates production deployment
6. **nixtla-usage-optimizer** suggests cost optimizations
7. Final result: Production-ready forecasting pipeline

**Deliverables**:
- `demo-project/` directory with complete example
- Video walkthrough (5-10 minutes)
- Blog post: "How Nixtla Skills Made Me 10x More Productive"
- User testimonials from beta testers

### Success Criteria

- All 11 skills implemented (no TODO markers)
- 50+ total examples across all skills
- Demo project working end-to-end
- 100+ users installed skills
- 5+ case studies documenting value
- Phase 4 AAR with metrics and feedback

### Deliverables

- 8 additional skills fully implemented
- Demo project in `demo-project/`
- User documentation (README, tutorials)
- Phase 4 AAR: `000-docs/aar/2025-11-30-nixtla-claude-skills-phase-04.md`
- **v1.0.0 release** (production-ready)

### Git Strategy

```bash
# After each skill
git commit -m "feat(skills): implement nixtla-[skill-name]"

# Final release
git tag -a v1.0.0 -m "Production release - 11 skills complete"
git push origin main --tags
```

---

## Risk Management

### Phase 1 Risks (Current)
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Unclear scope | Low | Low | This plan document clarifies all phases |
| Directory structure wrong | Low | Medium | Based on Claude Code standards, validated |

### Phase 2 Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Prompts too generic | Medium | High | Test with real Nixtla users, iterate based on feedback |
| Activation triggers fail | Low | Medium | Comprehensive testing, multiple trigger keywords |
| Examples don't work | Low | High | Run all examples in isolation, validate outputs |

### Phase 3 Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Installer incompatible | Medium | High | Test on macOS, Linux, Windows before release |
| Permissions issues | Medium | Medium | Provide sudo-free installation option |
| npm publish fails | Low | Low | Test publish to private registry first |

### Phase 4 Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Timeline overruns | High | Medium | Prioritize P1-P2 skills, defer P3 if needed |
| User adoption low | Medium | High | Marketing via Nixtla Slack, blog posts, demos |
| Quality inconsistent | Medium | High | Code review all skills, peer testing |

---

## Resource Requirements

### Personnel

| Role | Phases | Time Commitment |
|------|--------|-----------------|
| **Lead Developer** (Jeremy) | All | Full-time (40 hrs/week) |
| **Nixtla Reviewer** (Max or team) | 2-4 | 5 hrs/week (testing, feedback) |
| **Beta Testers** (Community) | 2-4 | 2 hrs/week (usage, bug reports) |

### Infrastructure

- **Git Repository**: GitHub (already available)
- **npm Registry**: For installer distribution
- **Testing Environment**: macOS, Linux, Windows VMs
- **Documentation**: Markdown in `000-docs/`

### Budget

**Estimated Costs** (if commercial):
- Developer time: ~320 hours @ $100/hr = $32,000
- Testing infrastructure: ~$500
- Marketing/outreach: ~$1,000
- **Total**: ~$33,500

**Actual Cost** (open source showcase):
- $0 (volunteer development by Intent Solutions)

---

## Success Metrics

### Phase 1 (Skeleton)
- ✅ Directory structure created
- ✅ 6 SKILL.md stubs
- ✅ Architecture doc complete
- ✅ Rollout plan complete

### Phase 2 (Core Skills)
- 🔲 3 skills fully implemented
- 🔲 15+ examples
- 🔲 8+ tester approvals
- 🔲 Zero activation failures in testing

### Phase 3 (Installer)
- 🔲 One-command install working
- 🔲 20+ successful installations
- 🔲 Published to npm registry
- 🔲 Zero critical bugs in installer

### Phase 4 (Complete)
- 🔲 All 11 skills implemented
- 🔲 100+ users installed
- 🔲 5+ case studies published
- 🔲 4.5+ star average rating (if applicable)
- 🔲 v1.0.0 tagged and released

---

## Communication Plan

### Internal (Nixtla Team)

- **Weekly Updates**: Email to Max with progress summary
- **Demo Sessions**: Live walkthrough at end of each phase
- **Slack Channel**: #nixtla-skills for daily coordination

### External (OSS Community)

- **Blog Posts**: Announce each phase completion
- **Twitter/X**: Share examples and tips
- **Reddit**: Post in r/MachineLearning, r/datascience
- **Nixtla Slack**: Invite beta testers, gather feedback

---

## Acceptance Criteria (Per Phase)

### Phase 1: Skeleton
- All directory structure created
- All SKILL.md stubs present
- Architecture doc peer-reviewed
- Rollout plan approved by Max

### Phase 2: Core Skills
- 3 skills pass internal testing (Nixtla team)
- 3 skills pass user testing (OSS community)
- All examples run without errors
- Documentation complete with troubleshooting

### Phase 3: Installer
- Installer works on 3 platforms (macOS, Linux, Windows)
- 20+ successful beta installations
- Published to npm registry
- Post-install experience validated

### Phase 4: Complete
- All 11 skills reviewed and approved
- Demo project working end-to-end
- 5+ user testimonials collected
- v1.0.0 release tagged

**Max's Approval Required**: End of each phase before proceeding to next.

---

## Timeline Visualization

```
Week 1        Week 2-4           Week 5-7           Week 8-12
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
│             │                  │                  │
│  Phase 1    │    Phase 2       │    Phase 3       │  Phase 4
│  Skeleton   │    Core Skills   │    Installer     │  Advanced + Demo
│             │                  │                  │
│ • Directory │ • timegpt-lab    │ • Bootstrap CLI  │ • 8 more skills
│ • SKILL.md  │ • experiment-    │ • npm publish    │ • Demo project
│ • Docs      │   architect      │ • Auto-update    │ • Case studies
│             │ • schema-mapper  │                  │ • v1.0.0 release
│             │                  │                  │
▼             ▼                  ▼                  ▼
AAR           AAR                AAR                AAR
```

---

## Post-Launch Roadmap (Beyond Phase 4)

### Continuous Improvement
- **Monthly releases**: Bug fixes, new examples
- **Quarterly feature releases**: New skills, major improvements
- **User feedback loops**: GitHub issues, Nixtla Slack

### Potential Future Skills (Phase 5+)
- **nixtla-mlops-auditor**: Validate production pipelines
- **nixtla-data-quality-monitor**: Detect data drift
- **nixtla-benchmark-runner**: Automated M4/M5 comparisons
- **nixtla-conformal-tuner**: Optimize prediction intervals

---

## Related Documents

- **Strategy**: [6767-OD-STRAT-nixtla-claude-skills-strategy.md](6767-OD-STRAT-nixtla-claude-skills-strategy.md)
- **Architecture**: [038-AT-ARCH-nixtla-claude-skills-pack.md](038-AT-ARCH-nixtla-claude-skills-pack.md)
- **Phase 1 AAR**: [000-docs/aar/2025-11-30-nixtla-claude-skills-phase-01.md](aar/2025-11-30-nixtla-claude-skills-phase-01.md)

---

## Sign-Off

**Created By**: Intent Solutions (Jeremy Longshore)
**Date**: 2025-11-30
**Status**: Phase 1 in progress
**Approved By**: Pending Max review

**Next Review**: End of Phase 1 (expected: 2025-12-07)

---

**Last Updated**: 2025-11-30
**Phase**: 1 - Skeleton (80% complete)
**Next Milestone**: Complete Phase 1 AAR and commit
**Maintained By**: Intent Solutions (Jeremy Longshore)
**For**: Nixtla (Max Mergenthaler)
