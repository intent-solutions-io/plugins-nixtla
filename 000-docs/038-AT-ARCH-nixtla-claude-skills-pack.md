# Nixtla Claude Skills Pack Architecture

**Document ID**: 038-AT-ARCH-nixtla-claude-skills-pack.md
**Created**: 2025-11-30
**Status**: Phase 4 - Advanced Skills + Demo Complete
**Related**: [6767-OD-STRAT-nixtla-claude-skills-strategy.md](6767-OD-STRAT-nixtla-claude-skills-strategy.md)

---

## Nixtla SKILL Standard

All Nixtla skills conform to the **Nixtla SKILL Standard** defined in:

📋 **[041-SPEC-nixtla-skill-standard.md](041-SPEC-nixtla-skill-standard.md)**

### Key Requirements

**Frontmatter** (required fields):
```yaml
name: nixtla-<short-name>
description: "Action-oriented description with when-to-use context"
allowed-tools: "Read,Write,Glob,Grep,Edit"  # Minimal set only
version: "1.0.0"
```

**Directory Structure** (all skills):
```
nixtla-<skill-name>/
├── SKILL.md           # Core prompt (<5,000 words)
├── scripts/           # Executable code (Bash invocation)
├── references/        # Long-form docs (Read tool)
└── assets/            # Templates/configs (path reference)
```

**Skill Classification**:
| Type | mode | disable-model-invocation | Example |
|------|------|-------------------------|---------|
| Mode | `true` | `false` | nixtla-timegpt-lab |
| Utility | `false` | `false` | nixtla-schema-mapper |
| Infra | `false` | `true` | nixtla-skills-bootstrap |

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

### 2. Per-Project Installation Model (Phase 3)

**Implemented**: Phase 3 introduces a Python-based installer CLI that provides **per-project persistence**.

Users install skills via the `nixtla-skills` CLI or the `nixtla-skills-bootstrap` skill:

```bash
# First-time installation in current project
cd /path/to/your/project
nixtla-skills init

# Update existing skills to latest versions
nixtla-skills update

# Force update without confirmation
nixtla-skills update --force
```

**Installation Process**:
1. User runs `nixtla-skills init` (or invokes bootstrap skill in Claude Code)
2. CLI locates skills source from `skills-pack/.claude/skills/` (dev mode)
3. Creates `.claude/skills/` directory in current working directory
4. Copies all Nixtla skills to `.claude/skills/nixtla-*/`
5. Skills become available in Claude Code immediately
6. No restart required (Claude Code auto-detects)

**Key Characteristics**:
- **Per-project**: Skills installed in project's `.claude/skills/`, not global `~/.claude/skills/`
- **Persistent**: Skills remain until explicitly updated or removed
- **Version-isolated**: Different projects can have different skill versions
- **Offline-capable**: Skills are local files, work without internet

### 3. Update Mechanism

Skills are **persistent** in project's `.claude/skills/` directory:

- **Initial Install**: `nixtla-skills init` copies from `skills-pack/` to `.claude/skills/nixtla-*/`
- **Opt-in Updates**: `nixtla-skills update` pulls latest from canonical source
- **Preview & Confirmation**: Shows which skills will be overwritten before proceeding
- **Versioning**: Each skill tracks version in SKILL.md frontmatter
- **Backward Compatibility**: Breaking changes require new skill name

**Update Workflow**:
1. User runs `nixtla-skills update` in project directory
2. CLI compares installed skills vs. source skills
3. Shows preview: new skills, existing skills (will be overwritten)
4. Prompts for confirmation (unless `--force` flag used)
5. Copies latest versions from source
6. Lists updated skills with locations

### 4. Installer CLI Implementation (Phase 3)

**Package**: `packages/nixtla-claude-skills-installer/`

The installer CLI is a Python package that provides the `nixtla-skills` command:

```bash
# Installation (development mode)
pip install -e packages/nixtla-claude-skills-installer

# Verify installation
which nixtla-skills
nixtla-skills --help
```

**Architecture**:

```
packages/nixtla-claude-skills-installer/
├── pyproject.toml              # Package definition, console script entry point
├── nixtla_skills_installer/
│   ├── __init__.py             # Package exports, version info
│   ├── core.py                 # Core logic: locate source, copy skills, preview
│   └── cli.py                  # CLI commands: init, update
└── README.md                   # User-facing documentation
```

**Key Functions** (`core.py`):

- `locate_skills_source()`: Finds `skills-pack/.claude/skills/` in development mode
  - Future: Use `importlib.resources` for bundled package data (PyPI distribution)
- `ensure_skills_directory()`: Creates `.claude/skills/` in project if not exists
- `preview_install()`: Compares source vs. installed skills, returns (new, existing, all)
- `confirm_overwrite()`: Prompts user before overwriting existing skills
- `copy_skills_to_project()`: Copies skills using `shutil.copytree`
- `list_installed_skills()`: Lists all `nixtla-*` directories in `.claude/skills/`

**CLI Commands** (`cli.py`):

1. **`nixtla-skills init`**: First-time installation
   - Locates skills source
   - Creates `.claude/skills/` directory
   - Shows preview of skills to install
   - Prompts for confirmation if any existing skills
   - Copies all skills
   - Lists installed skills with locations

2. **`nixtla-skills update`**: Refresh existing skills
   - Same workflow as `init`
   - Emphasizes "updating" in messaging
   - Shows which skills are new vs. existing
   - Prompts before overwriting existing skills

Both commands support `--force` flag to skip confirmation prompts.

**Distribution Models**:

- **Development Mode (Current)**: Installed from repo with `pip install -e`
  - Skills source: `skills-pack/.claude/skills/` relative to repo root
  - Requires nixtla repo cloned locally

- **PyPI Mode (TODO)**: Installed from PyPI with `pip install nixtla-claude-skills-installer`
  - Skills source: Bundled as package data
  - No repo required
  - Uses `importlib.resources` to access bundled skills

### 5. Bootstrap Skill (Phase 3)

**Skill**: `nixtla-skills-bootstrap`

The bootstrap skill provides a **conversational interface** to the installer CLI from within Claude Code.

**Activation Triggers**:
- "Install Nixtla skills"
- "Set up Nixtla skills in this project"
- "Update Nixtla skills"
- "Add Nixtla forecasting skills"
- "Bootstrap Nixtla environment"

**Workflow**:

1. **Ask user**: Init (first-time) or update (refresh existing)?
2. **Check for CLI**: Runs `which nixtla-skills` to verify CLI availability
   - If not found: Shows installation instructions, stops
3. **Run installer**: Executes `nixtla-skills init` or `nixtla-skills update` via Bash tool
4. **Narrate process**: Explains what's happening during installation
5. **List results**: Uses Glob to find `.claude/skills/nixtla-*` directories
6. **Provide guidance**: Next steps and how to use the skills

**Error Handling**:

- **CLI not found**: Shows `pip install` instructions, does NOT attempt file operations
- **CLI execution failed**: Shows error output, troubleshooting tips
- **No skills installed**: Explains possible causes (user cancelled, no skills in source)

**Tools Used**:
- `Bash`: Invoke `nixtla-skills` CLI, check CLI availability
- `Read`: Verify skill directories exist
- `Glob`: List installed skills (`find .claude/skills -type d -name "nixtla-*"`)

**User Experience**:

```
User: "Install Nixtla skills in this project"

Bootstrap Skill:
1. Asks: "Init (first-time) or update (refresh)?"
2. User responds: "init"
3. Checks CLI availability
4. Runs: nixtla-skills init
5. Streams CLI output (preview, confirmation, copying)
6. Lists installed skills:
   ✅ nixtla-timegpt-lab
   ✅ nixtla-experiment-architect
   ✅ nixtla-schema-mapper
   ✅ nixtla-skills-bootstrap
7. Provides next steps: "Try: 'I need to forecast daily sales'"
```

---

## Skills Universe (9 Implemented)

### Implemented Skills (9 Skills)

**Status**: All implemented and compliant with Nixtla SKILL Standard

| Skill | Type | Description |
|-------|------|-------------|
| `nixtla-timegpt-lab` | Mode | Transforms Claude into Nixtla forecasting expert |
| `nixtla-experiment-architect` | Utility | Design and scaffold complete forecasting experiments |
| `nixtla-schema-mapper` | Utility | Infer schema, generate Nixtla-compatible transformations |
| `nixtla-prod-pipeline-generator` | Utility | Generate production-ready inference pipelines |
| `nixtla-timegpt-finetune-lab` | Utility | Guide TimeGPT fine-tuning workflows |
| `nixtla-usage-optimizer` | Utility | Analyze usage, suggest cost/performance optimizations |
| `nixtla-skills-bootstrap` | Infra | Install/update skills via nixtla-skills CLI |
| `nixtla-skills-index` | Utility | List all installed Nixtla skills and usage guidance |

### Future Skills (Planned)

| Skill | Type | Description |
|-------|------|-------------|
| `nixtla-tutor` | Utility | Interactive Nixtla learning and troubleshooting |
| `nixtla-docs-to-experiments` | Utility | Convert documentation examples to runnable code |
| `nixtla-vertical-blueprint` | Utility | Industry-specific forecasting templates |
| `nixtla-incident-sre` | Infra | Production incident debugging (Nixtla internal) |

---

## Directory Structure (Detailed)

```
skills-pack/
└── .claude/
    └── skills/
        ├── nixtla-timegpt-lab/
        │   ├── SKILL.md              # Core prompt (<5,000 words target)
        │   ├── scripts/              # Executable Python/Bash
        │   ├── references/           # Long-form docs, schemas
        │   └── assets/               # Templates, configs
        │
        ├── nixtla-experiment-architect/
        │   ├── SKILL.md
        │   ├── scripts/
        │   ├── references/
        │   └── assets/
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

### Phase 1-2: Manual Installation (Deprecated)

**Note**: Manual installation is deprecated in favor of the automated installer CLI (Phase 3).

For development/testing purposes only:

```bash
# Clone Nixtla showcase repo
git clone https://github.com/your-org/nixtla.git
cd nixtla

# Copy skills to project's .claude/skills/ directory
mkdir -p .claude/skills
cp -r skills-pack/.claude/skills/nixtla-* .claude/skills/

# Verify installation
ls .claude/skills/nixtla-*
```

### Phase 3: Automated Installer (Implemented)

**Recommended Method**: Use the `nixtla-skills` CLI for automated installation.

**Step 1: Install the CLI**

```bash
# Clone Nixtla showcase repo
git clone https://github.com/your-org/nixtla.git
cd nixtla

# Install installer CLI in development mode
pip install -e packages/nixtla-claude-skills-installer

# Verify installation
which nixtla-skills
```

**Step 2: Install Skills in Your Project**

```bash
# Navigate to your project
cd /path/to/your/forecasting-project

# First-time installation
nixtla-skills init

# Or update existing skills
nixtla-skills update
```

**Alternative: Use Bootstrap Skill in Claude Code**

```
User (in Claude Code): "Install Nixtla skills"

Bootstrap skill activates and:
1. Asks: Init or update?
2. Checks for nixtla-skills CLI
3. Runs appropriate command
4. Lists installed skills
5. Provides next steps
```

**Installer Features** (Implemented):
- ✅ Per-project installation (`.claude/skills/nixtla-*` in current directory)
- ✅ Preview before overwriting existing skills
- ✅ Confirmation prompts (skip with `--force`)
- ✅ Validate installation success (lists installed skills)
- ✅ Post-install usage tips (via bootstrap skill)
- ✅ Offline-capable (skills are local files)

**Future Enhancements** (TODO):
- 🔲 PyPI distribution (`pip install nixtla-claude-skills-installer`)
- 🔲 Bundled skills as package data (no repo required)
- 🔲 Version checking and conflict detection
- 🔲 Individual skill installation (`nixtla-skills init nixtla-timegpt-lab`)
- 🔲 Rollback to previous versions

---

## Maintenance & Updates

### Update Cadence

- **Weekly**: Bug fixes, prompt improvements (PATCH)
- **Monthly**: New features, examples (MINOR)
- **Quarterly**: New skills, breaking changes (MAJOR)

### User Update Experience (Phase 3)

**Implemented Commands**:

```bash
# Update all skills to latest versions
cd /path/to/your/project
nixtla-skills update

# Force update without confirmation prompts
nixtla-skills update --force
```

**Update Workflow**:
1. Navigate to project directory
2. Run `nixtla-skills update`
3. CLI shows preview: new skills, existing skills (will be overwritten)
4. Confirm to proceed (or use `--force` to skip)
5. CLI copies latest versions from source
6. Lists updated skills with locations

**Future Commands** (TODO):
```bash
# Check for updates without installing
nixtla-skills check

# Update specific skill only
nixtla-skills update nixtla-timegpt-lab

# Rollback to previous version
nixtla-skills rollback nixtla-timegpt-lab

# List installed skills
nixtla-skills list
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

### Phase 1 (Skeleton) - ✅ COMPLETE
- ✅ 6 skill directories created
- ✅ SKILL.md stubs with TODO markers
- ✅ Architecture documented (this doc)

### Phase 2 (Core Implementation) - ✅ COMPLETE
- ✅ 3 core skills fully implemented (500+ word prompts each)
  - `nixtla-timegpt-lab` (670 lines)
  - `nixtla-experiment-architect` (877 lines)
  - `nixtla-schema-mapper` (750 lines)
- ✅ 15+ examples across the 3 implemented skills
- ✅ Phase 2 AAR documented

### Phase 3 (Installer CLI + Bootstrap) - ✅ COMPLETE
- ✅ Installer CLI implemented (`nixtla-skills` Python package)
  - `nixtla-skills init` command working
  - `nixtla-skills update` command working
  - Preview and confirmation workflow implemented
  - Per-project persistence model working
- ✅ Bootstrap skill implemented (`nixtla-skills-bootstrap`)
  - Conversational interface to installer CLI
  - Error handling and troubleshooting guidance
  - Activation triggers defined
- ✅ Architecture docs updated with Phase 3 details
- ✅ README for installer package created

### Phase 4 (Advanced Skills + DevOps) - ✅ COMPLETE
- ✅ 3 advanced skills implemented:
  - `nixtla-timegpt-finetune-lab` (945 lines)
  - `nixtla-prod-pipeline-generator` (1,149 lines)
  - `nixtla-usage-optimizer` (586 lines)
- ✅ Demo project with end-to-end walkthrough (`demo-project/`)
  - Sample data: 3 synthetic time series (365 days each)
  - Comprehensive README with step-by-step guide
  - Project structure ready for skills usage
- ✅ DevOps education guide created (`000-docs/global/003-GUIDE-devops-nixtla-skills-operations.md`)
  - Conversational, video-script style
  - Lifecycle, security, best practices
  - Troubleshooting and operations guide
- 🔲 User testing with 5+ Nixtla community members (TODO: post-delivery)

### Future (Post-Phase 4) - 🔲 NOT STARTED
- 🔲 PyPI distribution of installer (`pip install nixtla-claude-skills-installer`)
- 🔲 100+ users installed skills
- 🔲 5+ case studies documenting value

---

## Related Documents

- [6767-OD-STRAT-nixtla-claude-skills-strategy.md](6767-OD-STRAT-nixtla-claude-skills-strategy.md) - Full strategy
- [039-PP-PLAN-nixtla-skills-4-phase-rollout.md](039-PP-PLAN-nixtla-skills-4-phase-rollout.md) - Rollout plan
- [000-docs/aar/2025-11-30-nixtla-claude-skills-phase-01.md](aar/2025-11-30-nixtla-claude-skills-phase-01.md) - Phase 1 AAR
- [000-docs/aar/2025-11-30-nixtla-claude-skills-phase-02.md](aar/2025-11-30-nixtla-claude-skills-phase-02.md) - Phase 2 AAR
- [000-docs/aar/2025-11-30-nixtla-claude-skills-phase-03.md](aar/2025-11-30-nixtla-claude-skills-phase-03.md) - Phase 3 AAR
- [000-docs/aar/040-AA-REPT-nixtla-claude-skills-phase-04.md](aar/040-AA-REPT-nixtla-claude-skills-phase-04.md) - Phase 4 AAR
- [packages/nixtla-claude-skills-installer/README.md](../packages/nixtla-claude-skills-installer/README.md) - Installer CLI documentation
- [demo-project/README.md](../demo-project/README.md) - Demo project walkthrough
- [000-docs/global/003-GUIDE-devops-nixtla-skills-operations.md](global/003-GUIDE-devops-nixtla-skills-operations.md) - DevOps operations guide

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
**Phase**: 4 - Advanced Skills + Demo Complete
**Next Phase**: PyPI distribution and user testing (Post-Phase 4)
**Maintained By**: Intent Solutions (Jeremy Longshore)
**For**: Nixtla (Max Mergenthaler)
