# Nixtla Claude Skills Pack Architecture

**Document ID**: 038-AT-ARCH-nixtla-claude-skills-pack.md
**Created**: 2025-11-30
**Status**: Phase 1 - Skeleton Complete
**Related**: [6767-OD-STRAT-nixtla-claude-skills-strategy.md](6767-OD-STRAT-nixtla-claude-skills-strategy.md)

---

## Overview

The **Nixtla Claude Skills Pack** is a collection of AI agent skills that transform Claude Code into a Nixtla forecasting expert. Skills are Claude Code's mechanism for domain-specific intelligence that activates automatically when users need forecasting help.

**Repository**: This Nixtla showcase repository (`/home/jeremy/000-projects/nixtla/`)
**Canonical Source**: `skills-pack/.claude/skills/nixtla-*/`
**User Install Target**: `.claude/skills/nixtla-*/` (in user's home directory)

---

## Architecture Principles

### 1. Canonical Source Model

The `skills-pack/` directory contains the **authoritative implementation** of all Nixtla skills:

```
skills-pack/
└── .claude/
    └── skills/
        ├── nixtla-timegpt-lab/           # Mode: Nixtla-native forecasting
        ├── nixtla-experiment-architect/  # Design forecasting experiments
        ├── nixtla-schema-mapper/         # Data transformation for Nixtla
        ├── nixtla-prod-pipeline-generator/  # Production inference code
        ├── nixtla-timegpt-finetune-lab/  # Fine-tuning workflows
        ├── nixtla-usage-optimizer/       # Cost/performance optimization
        └── [5 more skills coming in Phase 2-3]
```

**Key Characteristics**:
- **Version-controlled**: Skills evolve with git history
- **Testable**: Can be validated before distribution
- **Documented**: Each skill has comprehensive SKILL.md
- **Modular**: Skills can be installed individually or as a pack

### 2. User Installation Model

Users install skills via the `nixtla-skills` CLI (Phase 3):

```bash
# Install all skills (recommended)
nixtla-skills install

# Install specific skill
nixtla-skills install nixtla-timegpt-lab

# Update to latest version
nixtla-skills update

# List installed skills
nixtla-skills list
```

**Installation Process**:
1. Clone/copy skills from canonical source
2. Place in `~/.claude/skills/nixtla-*/`
3. Skills become available in Claude Code immediately
4. No restart required (Claude Code auto-detects)

### 3. Update Mechanism

Skills are **persistent** in user's home directory:

- **Initial Install**: Copy from `skills-pack/` to `~/.claude/skills/`
- **Updates**: `nixtla-skills update` pulls latest from canonical source
- **Versioning**: Each skill tracks version in SKILL.md frontmatter
- **Backward Compatibility**: Breaking changes require new skill name

---

## Skills Universe (11 Total)

### Phase 1: Foundation Skills (6 Skills)

**Status**: Skeleton created (SKILL.md stubs)

| Skill | Priority | Description |
|-------|----------|-------------|
| `nixtla-timegpt-lab` | P1 | Mode skill - switches Claude into Nixtla-native forecasting |
| `nixtla-experiment-architect` | P1 | Design and scaffold complete forecasting experiments |
| `nixtla-schema-mapper` | P1 | Infer schema, generate Nixtla-compatible transformations |
| `nixtla-prod-pipeline-generator` | P1.5 | Generate production-ready inference pipelines |
| `nixtla-timegpt-finetune-lab` | P2 | Guide TimeGPT fine-tuning workflows |
| `nixtla-usage-optimizer` | P2 | Analyze usage, suggest cost/performance optimizations |

### Phase 2-3: Advanced Skills (5 Skills)

**Status**: Not yet created

| Skill | Priority | Description |
|-------|----------|-------------|
| `nixtla-skills-bootstrap` | P1 | Installer CLI (`nixtla-skills install`) |
| `nixtla-tutor` | P2 | Interactive Nixtla learning and troubleshooting |
| `nixtla-docs-to-experiments` | P2-3 | Convert documentation examples to runnable code |
| `nixtla-vertical-blueprint` | P3 | Industry-specific forecasting templates |
| `nixtla-incident-sre` | P3 | Production incident debugging (Nixtla internal) |

---

## Directory Structure (Detailed)

```
skills-pack/
└── .claude/
    └── skills/
        ├── nixtla-timegpt-lab/
        │   ├── SKILL.md              # Skill definition + prompt
        │   ├── examples/             # Usage examples (Phase 2)
        │   └── tests/                # Skill validation (Phase 2)
        │
        ├── nixtla-experiment-architect/
        │   ├── SKILL.md
        │   ├── templates/            # Experiment scaffolds (Phase 2)
        │   └── examples/
        │
        ├── nixtla-schema-mapper/
        │   ├── SKILL.md
        │   ├── schemas/              # Common data patterns (Phase 2)
        │   └── examples/
        │
        ├── nixtla-prod-pipeline-generator/
        │   ├── SKILL.md
        │   ├── templates/            # Deployment configs (Phase 2.5)
        │   └── examples/
        │
        ├── nixtla-timegpt-finetune-lab/
        │   ├── SKILL.md
        │   ├── guides/               # Fine-tuning workflows (Phase 2)
        │   └── examples/
        │
        └── nixtla-usage-optimizer/
            ├── SKILL.md
            ├── analyzers/            # Usage analysis scripts (Phase 2)
            └── examples/
```

**Phase 1 Status**: Only SKILL.md stubs exist (TODO markers)

---

## Skill Activation Model

Skills activate **automatically** when Claude Code detects relevant context:

### Activation Triggers

1. **Keyword Detection**: User mentions "forecast", "TimeGPT", "Nixtla"
2. **File Pattern**: Working with `.py` files containing Nixtla imports
3. **Explicit Invocation**: User types `/nixtla-timegpt-lab` or similar
4. **Project Context**: `requirements.txt` contains `nixtla`, `statsforecast`

### Activation Priority

Skills stack - multiple can activate simultaneously:

```
User: "I need to forecast sales with TimeGPT"

Activated Skills:
1. nixtla-timegpt-lab (mode skill - highest priority)
   → Sets Nixtla-first context
2. nixtla-schema-mapper (data skill)
   → Analyzes user's data format
3. nixtla-experiment-architect (builder skill)
   → Suggests experiment structure
```

---

## Skill Development Workflow

### Creating a New Skill

1. **Create Directory**: `skills-pack/.claude/skills/nixtla-{name}/`
2. **Write SKILL.md**: YAML frontmatter + prompt instructions
3. **Add Examples**: Real-world usage in `examples/`
4. **Write Tests**: Validation in `tests/`
5. **Document**: Usage guide in SKILL.md body
6. **Commit**: Version control in git

### Skill Anatomy (SKILL.md)

```markdown
---
name: nixtla-timegpt-lab
description: "Mode skill for Nixtla-native forecasting"
allowed-tools: "Read,Write,Bash"
version: "1.0.0"
author: "Intent Solutions (Jeremy Longshore)"
---

# Nixtla TimeGPT Lab

You are now in **Nixtla TimeGPT Lab mode**...

[Detailed prompt instructions here]

## Examples
[Usage examples]

## Best Practices
[Nixtla patterns to follow]
```

---

## Integration with Nixtla Ecosystem

### Relationship to Plugins

**Plugins** (commands, MCP servers) vs **Skills** (AI agent modes):

| Feature | Nixtla Baseline Lab Plugin | nixtla-timegpt-lab Skill |
|---------|---------------------------|-------------------------|
| **Type** | Slash command + MCP server | AI agent skill (auto-triggered) |
| **Invocation** | `/nixtla-baseline-m4` | Automatic when user asks about forecasting |
| **Purpose** | Run reproducible benchmarks | Teach Claude Nixtla patterns |
| **Distribution** | Plugin registry | Skills pack installer |
| **Code Execution** | Python MCP server | Claude Code native |

**Complementary**: Plugin provides tools, skill provides intelligence to use them.

### Relationship to Nixtla Libraries

Skills **wrap and guide** Nixtla's Python libraries:

```python
# nixtla-timegpt-lab skill knows to generate this:
from nixtla import NixtlaClient
client = NixtlaClient(api_key=os.getenv('NIXTLA_API_KEY'))
forecast = client.forecast(df=data, h=24, freq='H')

# Instead of generic sklearn or prophet patterns
```

Skills teach Claude:
- **Which library to use**: TimeGPT vs StatsForecast vs MLForecast
- **Best practices**: Nixtla-specific patterns and conventions
- **Error handling**: Common issues and solutions
- **Optimization**: Cost-effective usage patterns

---

## Audience Matrix

Skills serve 3 audiences (from strategy doc):

| Audience | Abbreviation | Example Skills |
|----------|--------------|----------------|
| **Internal (Nixtla Team)** | INT | All skills, especially `nixtla-incident-sre` |
| **Open Source Users** | OSS | `nixtla-experiment-architect`, `nixtla-tutor` |
| **TimeGPT Customers** | PAY | `nixtla-timegpt-finetune-lab`, `nixtla-usage-optimizer` |

**Access Control**: Currently none (all open source), future could add:
- API key validation for TimeGPT-specific skills
- License checks for enterprise features
- Usage analytics for internal skills

---

## Versioning Strategy

### Skill Versions

Each skill tracks version independently:

```yaml
---
name: nixtla-timegpt-lab
version: "1.2.0"  # Semantic versioning
---
```

**Version Bumps**:
- **MAJOR (2.0.0)**: Breaking changes to skill interface
- **MINOR (1.1.0)**: New features, additive changes
- **PATCH (1.0.1)**: Bug fixes, clarifications

### Skills Pack Version

The entire pack has unified release version:

- **Phase 1**: v0.1.0 (skeleton only)
- **Phase 2**: v0.5.0 (core skills implemented)
- **Phase 3**: v1.0.0 (installer + all 11 skills)

Tracked in: `skills-pack/VERSION`

---

## Testing & Validation

### Skill Testing (Phase 2+)

Each skill will include validation tests:

```bash
# Test individual skill
pytest skills-pack/.claude/skills/nixtla-timegpt-lab/tests/

# Test all skills
pytest skills-pack/.claude/skills/*/tests/

# Integration test (requires Claude Code)
./skills-pack/scripts/test-skills-integration.sh
```

### Quality Gates

Before any skill moves from "TODO" to "implemented":

1. ✅ SKILL.md prompt is comprehensive (500+ words)
2. ✅ At least 3 realistic examples included
3. ✅ Tests cover activation triggers
4. ✅ Documentation includes troubleshooting
5. ✅ Peer review by Nixtla team member

---

## Deployment Model

### Phase 1-2: Manual Installation

Users clone this repo and copy skills:

```bash
# Clone Nixtla showcase repo
git clone https://github.com/your-org/nixtla.git
cd nixtla

# Copy skills to Claude Code
cp -r skills-pack/.claude/skills/nixtla-* ~/.claude/skills/

# Verify installation
ls ~/.claude/skills/nixtla-*
```

### Phase 3: Automated Installer

The `nixtla-skills-bootstrap` skill provides CLI:

```bash
# One-command install
npx nixtla-skills install

# Or via Claude Code skill
# (User in Claude Code): "Install Nixtla skills"
# nixtla-skills-bootstrap activates and guides installation
```

**Installer Features**:
- Detect existing skills (avoid duplicates)
- Handle version conflicts
- Validate installation success
- Show post-install usage tips

---

## Maintenance & Updates

### Update Cadence

- **Weekly**: Bug fixes, prompt improvements (PATCH)
- **Monthly**: New features, examples (MINOR)
- **Quarterly**: New skills, breaking changes (MAJOR)

### User Update Experience

```bash
# Check for updates
nixtla-skills check

# Update all skills
nixtla-skills update

# Update specific skill
nixtla-skills update nixtla-timegpt-lab

# Rollback to previous version
nixtla-skills rollback nixtla-timegpt-lab
```

---

## Security & Privacy

### Data Handling

Skills operate within Claude Code's security model:

- **No external API calls** (except TimeGPT via user's API key)
- **User data stays local** (no telemetry)
- **API keys from environment** (never hardcoded)

### Open Source Transparency

All skills are **open source** in this repo:

- **Auditable**: Users can read exact prompts
- **Modifiable**: Users can customize for their needs
- **Trustworthy**: No hidden behavior

---

## Success Metrics

### Phase 1 (Skeleton)
- ✅ 6 skill directories created
- ✅ SKILL.md stubs with TODO markers
- ✅ Architecture documented (this doc)

### Phase 2 (Core Implementation)
- 🔲 3+ skills fully implemented (500+ word prompts)
- 🔲 10+ examples across all skills
- 🔲 User testing with 5+ Nixtla community members

### Phase 3 (Full Release)
- 🔲 All 11 skills implemented
- 🔲 Installer CLI working
- 🔲 100+ users installed skills
- 🔲 5+ case studies documenting value

---

## Related Documents

- [6767-OD-STRAT-nixtla-claude-skills-strategy.md](6767-OD-STRAT-nixtla-claude-skills-strategy.md) - Full strategy
- [039-PP-PLAN-nixtla-skills-4-phase-rollout.md](039-PP-PLAN-nixtla-skills-4-phase-rollout.md) - Rollout plan
- [000-docs/aar/2025-11-30-nixtla-claude-skills-phase-01.md](aar/2025-11-30-nixtla-claude-skills-phase-01.md) - Phase 1 AAR

---

## Appendix: SKILL.md Format Reference

```markdown
---
name: skill-name                    # Folder name, kebab-case
description: "Brief description"    # 1 sentence, appears in skill list
allowed-tools: "Read,Write,Bash"    # Comma-separated tool names
version: "1.0.0"                    # Semantic version
author: "Name/Org"                  # Maintainer
priority: "P1"                      # P1 (critical) to P3 (nice-to-have)
audience: "INT,OSS,PAY"            # See audience matrix
---

# Skill Title

[Main prompt that activates when skill triggers]

## When This Skill Activates

[List triggers: keywords, file patterns, user commands]

## What This Skill Does

[Bullet list of capabilities]

## Examples

### Example 1: [Scenario]
[Step-by-step usage example]

### Example 2: [Scenario]
[Another example]

## Best Practices

[Nixtla-specific patterns to follow]

## Common Issues

[Troubleshooting guide]

## Related Skills

[Other skills that work well with this one]
```

---

**Last Updated**: 2025-11-30
**Phase**: 1 - Skeleton Complete
**Next Phase**: Implement core skill prompts (Phase 2)
**Maintained By**: Intent Solutions (Jeremy Longshore)
**For**: Nixtla (Max Mergenthaler)
