# Nixtla Claude Skills Installer

Per-project installation and update utility for Nixtla Claude Code skills.

## Installation

### Development Mode (from repo)

```bash
# Clone the nixtla repo
git clone https://github.com/intent-solutions-io/plugins-nixtla.git
cd claude-code-plugins-nixtla

# Install in editable mode
pip install -e packages/nixtla-claude-skills-installer
```

### PyPI (TODO - not yet published)

```bash
pip install nixtla-claude-skills-installer
```

## Usage

### First-Time Install

Install Nixtla skills in your current project:

```bash
cd /path/to/your/project
nixtla-skills init
```

This will:
1. Create `.claude/skills/` directory if it doesn't exist
2. Copy all Nixtla skills from source to `.claude/skills/nixtla-*`
3. List installed skills

**Skills installed**:
- `nixtla-timegpt-lab` - Mode skill for Nixtla-first forecasting
- `nixtla-experiment-architect` - Scaffold forecasting experiments
- `nixtla-schema-mapper` - Transform data to Nixtla schema
- `nixtla-skills-bootstrap` - Install/update skills from within Claude Code
- _(More skills in future phases)_

### Update Existing Skills

Update skills to latest versions:

```bash
cd /path/to/your/project
nixtla-skills update
```

This will:
1. Show preview of which skills will be updated
2. Prompt for confirmation before overwriting
3. Copy latest versions from source
4. List updated skills

**Force update** (skip confirmation):
```bash
nixtla-skills update --force
```

## Per-Project Persistence

Skills are installed **per-project** in `.claude/skills/nixtla-*` and **persist locally** until you explicitly update or remove them.

This allows:
- Different projects to have different skill versions if needed
- Offline usage (skills are local files)
- Full control over when skills update

**Update model**: Opt-in via `nixtla-skills update`

## How It Works

### Directory Structure

```
your-project/
├── .claude/
│   └── skills/
│       ├── nixtla-timegpt-lab/
│       │   └── SKILL.md
│       ├── nixtla-experiment-architect/
│       │   └── SKILL.md
│       ├── nixtla-schema-mapper/
│       │   └── SKILL.md
│       └── nixtla-skills-bootstrap/
│           └── SKILL.md
└── (your project files...)
```

### Skills Source

**Development mode**:
- Skills are copied from `skills-pack/.claude/skills/` in the nixtla repo
- Requires installing this package from the repo (`pip install -e`)

**PyPI mode** (TODO):
- Skills will be bundled as package data
- No repo required, just `pip install nixtla-claude-skills-installer`

## Commands

### `nixtla-skills init`

First-time installation of skills in current project.

**Options**:
- `--force` - Skip confirmation prompts

**Example**:
```bash
nixtla-skills init
```

### `nixtla-skills update`

Update existing skills to latest versions.

**Options**:
- `--force` - Skip confirmation prompts

**Example**:
```bash
nixtla-skills update
```

## Uninstallation

To remove Nixtla skills from a project:

```bash
rm -rf .claude/skills/nixtla-*
```

Or remove individual skills:

```bash
rm -rf .claude/skills/nixtla-timegpt-lab
```

## Troubleshooting

### "Could not locate skills source directory"

**Cause**: Package installed from PyPI but skills not bundled (packaging issue).

**Solution**: Install in development mode from repo:
```bash
git clone https://github.com/intent-solutions-io/plugins-nixtla.git
cd claude-code-plugins-nixtla
pip install -e packages/nixtla-claude-skills-installer
```

### "Permission error"

**Cause**: Insufficient permissions to write to `.claude/skills/`.

**Solution**: Ensure you have write permissions in the current directory.

### Skills not activating in Claude Code

**Cause**: Skills installed but Claude Code not detecting them.

**Solution**:
1. Verify skills exist: `ls .claude/skills/nixtla-*`
2. Restart Claude Code
3. Try triggering manually by mentioning forecasting topics

## Development

### Running from Source

```bash
# Clone repo
git clone https://github.com/intent-solutions-io/plugins-nixtla.git
cd claude-code-plugins-nixtla

# Install in editable mode
pip install -e packages/nixtla-claude-skills-installer

# Use CLI
nixtla-skills init
```

### Building Package

```bash
cd packages/nixtla-claude-skills-installer
python -m build
```

### Publishing to PyPI (TODO)

```bash
# TODO: Bundle skills as package data first
# TODO: Update pyproject.toml with package_data configuration

python -m build
twine upload dist/*
```

## License

MIT License - see LICENSE file in repo root.

## Author

Intent Solutions (Jeremy Longshore)
- Email: jeremy@intentsolutions.io
- GitHub: https://github.com/jeremylongshore

## For Nixtla

Sponsored by Nixtla (Max Mergenthaler)
- Email: max@nixtla.io
- Purpose: Demonstrate plugin value, drive investment decision

## Related

- **Nixtla Repo**: https://github.com/intent-solutions-io/plugins-nixtla
- **Nixtla Docs**: https://docs.nixtla.io
- **Claude Code**: https://claude.ai/code
