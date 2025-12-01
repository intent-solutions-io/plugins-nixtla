---
name: nixtla-skills-bootstrap
description: "Install or update Nixtla Claude Skills in this project by calling the nixtla-skills CLI and narrating the installation process"
allowed-tools: "Bash,Read,Glob"
version: "1.0.0"
disable-model-invocation: true
---

# Nixtla Skills Bootstrap

This skill **installs or updates Nixtla Claude Skills** in the current project by invoking the `nixtla-skills` CLI and guiding the user through the process.

## When This Skill Activates

**Trigger phrases**:
- "Install Nixtla skills"
- "Set up Nixtla skills in this project"
- "Update Nixtla skills"
- "Add Nixtla forecasting skills"
- "Bootstrap Nixtla environment"

**Manual invocation**:
- User can explicitly mention this skill by name

## What This Skill Does

1. **Asks user**: Init (first-time install) or update (refresh existing)?
2. **Checks for CLI**: Verifies `nixtla-skills` command is available
3. **Runs installer**: Executes `nixtla-skills init` or `nixtla-skills update`
4. **Narrates process**: Explains what's happening during installation
5. **Lists results**: Shows all installed Nixtla skills in the project
6. **Provides guidance**: Next steps and how to use the skills

---

## Skill Behavior

### Step 1: Determine User Intent

When invoked, ask the user what they want to do:

```
I'll help you install or update Nixtla Claude Skills in this project.

What would you like to do?

1. **init** - First-time installation (if you haven't installed Nixtla skills yet)
   - Creates .claude/skills/ directory
   - Copies all Nixtla skills to this project
   - Skills will persist locally until updated

2. **update** - Refresh existing skills (if you already have Nixtla skills installed)
   - Updates skills to latest versions
   - Prompts before overwriting existing files
   - Preserves your local installation

Which action? (init/update)
```

**If user says "init"**: Proceed with first-time installation.

**If user says "update"**: Proceed with update.

**If unclear**: Ask user to clarify.

### Step 2: Check for CLI Tool

Before running anything, verify the `nixtla-skills` CLI is available:

```bash
which nixtla-skills || echo "NOT_FOUND"
```

**If CLI found**: Proceed to Step 3.

**If CLI not found**: Show installation instructions and stop.

### Step 3: Run Installer

Based on user's choice, run the appropriate command:

#### For Init (First-Time Install)

```bash
nixtla-skills init
```

**What happens**:
- CLI locates skills source (from nixtla repo or bundled package data)
- Creates `.claude/skills/` if it doesn't exist
- Shows preview of skills that will be installed
- Prompts for confirmation if any existing skills will be overwritten
- Copies all Nixtla skills to `.claude/skills/nixtla-*`
- Lists installed skills

#### For Update (Refresh Existing)

```bash
nixtla-skills update
```

**What happens**:
- CLI locates skills source
- Checks for existing skills in `.claude/skills/`
- Shows preview of new vs existing skills
- Prompts for confirmation before overwriting
- Updates skills to latest versions
- Lists updated skills

### Step 4: Narrate the Process

While the CLI runs, explain what's happening:

```
🚀 Installing Nixtla Claude Skills...

The nixtla-skills CLI is:
1. Locating the skills source directory
   (From nixtla repo or bundled package data)

2. Preparing .claude/skills/ directory
   (Creating if it doesn't exist)

3. Copying Nixtla skills to this project:
   - nixtla-timegpt-lab (Mode skill for Nixtla-first forecasting)
   - nixtla-experiment-architect (Scaffold forecasting experiments)
   - nixtla-schema-mapper (Transform data to Nixtla schema)
   - nixtla-skills-bootstrap (This skill - install/update helper)

4. These skills will persist locally in:
   .claude/skills/nixtla-*

5. Skills remain until you explicitly update or remove them.
   This allows offline usage and version control.
```

### Step 5: List Installed Skills

After CLI completes, use Glob to verify installation:

```bash
# List all Nixtla skill directories
find .claude/skills -type d -name "nixtla-*" -maxdepth 1 | sort
```

Or:

```bash
ls -1 .claude/skills/nixtla-* 2>/dev/null || echo "No skills found"
```

**Present results to user**:

```
✅ Nixtla Skills Installed Successfully!

Found 4 skills in .claude/skills/:

1. nixtla-timegpt-lab/
   Purpose: Mode skill that biases Claude toward Nixtla forecasting patterns
   Location: .claude/skills/nixtla-timegpt-lab

2. nixtla-experiment-architect/
   Purpose: Scaffold complete forecasting experiments (config + harness)
   Location: .claude/skills/nixtla-experiment-architect

3. nixtla-schema-mapper/
   Purpose: Map raw data to Nixtla schema (unique_id, ds, y)
   Location: .claude/skills/nixtla-schema-mapper

4. nixtla-skills-bootstrap/
   Purpose: Install and update skills (this skill)
   Location: .claude/skills/nixtla-skills-bootstrap

These skills are now active in this project!
```

### Step 6: Provide Next Steps

After installation, guide the user:

```
📝 Next Steps:

1. Skills are now active and will auto-trigger when you:
   - Mention forecasting topics
   - Work with time series data
   - Ask about Nixtla libraries

2. You can also invoke skills manually:
   - "Use nixtla-timegpt-lab skill" (enters Nixtla mode)
   - "Map my data to Nixtla schema" (triggers schema-mapper)
   - "Set up a forecasting experiment" (triggers experiment-architect)

3. Skills persist in this project:
   - They're local files in .claude/skills/nixtla-*
   - They won't update automatically
   - Update manually with: nixtla-skills update

4. To update skills in the future:
   - Run this skill again and choose "update"
   - Or run directly: nixtla-skills update in terminal

Want to test a skill now? Try:
"I have daily sales data and need to forecast next 30 days"

This will activate nixtla-timegpt-lab (mode skill) and suggest
Nixtla-specific forecasting approaches!
```

---

## Error Handling

### Error: CLI Not Found

If `nixtla-skills` command is not available:

```
❌ nixtla-skills CLI not found

The Nixtla Skills installer needs to be installed first.

Installation Options:

1. Development Mode (from repo):
   ```
   git clone https://github.com/jeremylongshore/claude-code-plugins-nixtla.git
   cd claude-code-plugins-nixtla
   pip install -e packages/nixtla-claude-skills-installer
   ```

2. PyPI (TODO - not yet published):
   ```
   pip install nixtla-claude-skills-installer
   ```

After installing, run this skill again to install Nixtla skills in your project.

⚠️  I cannot proceed without the CLI installed.
   This ensures safe, controlled installation of skills.
```

**Do not attempt any file operations** if CLI is missing.

### Error: CLI Execution Failed

If the CLI runs but fails:

```
❌ nixtla-skills installation failed

Error output:
[Show CLI error output]

Common causes:
1. Permissions issue - Check write permissions in current directory
2. Skills source not found - Verify CLI is installed correctly
3. User cancelled operation - Confirmation prompt declined

Troubleshooting:
- Try running manually: nixtla-skills init
- Check CLI help: nixtla-skills --help
- Verify installation: which nixtla-skills
```

### Error: No Skills Installed

If CLI runs but no skills end up installed:

```
⚠️  Installation completed but no skills found in .claude/skills/

Possible causes:
1. User cancelled during confirmation prompt
2. No Nixtla skills in source directory
3. Installation was interrupted

Try again:
- Run this skill again and confirm prompts
- Or run manually: nixtla-skills init --force (skips prompts)
```

---

## Examples

### Example 1: First-Time Install

**User**: "Install Nixtla skills in this project"

**Skill response**:
```
I'll help you install Nixtla Claude Skills.

What would you like to do?
1. init - First-time installation
2. update - Refresh existing skills

Which action? (init/update)
```

**User**: "init"

**Skill response**:
```
Running: nixtla-skills init

🚀 Installing Nixtla Claude Skills...

[CLI output streams here...]

✅ Successfully installed 4 Nixtla skills!

Found in .claude/skills/:
1. nixtla-timegpt-lab (Mode skill)
2. nixtla-experiment-architect (Experiment scaffolding)
3. nixtla-schema-mapper (Data transformation)
4. nixtla-skills-bootstrap (This skill)

Skills are now active! Try asking: "I need to forecast daily sales"
```

### Example 2: Update Existing Skills

**User**: "Update Nixtla skills to latest version"

**Skill response**:
```
Running: nixtla-skills update

🔄 Updating Nixtla Claude Skills...

Preview:
- Existing skills will be updated to latest versions
- You'll be prompted to confirm before overwriting

[CLI output streams here...]

✅ Successfully updated 4 Nixtla skills!

All skills are now up to date.
```

### Example 3: CLI Not Installed

**User**: "Set up Nixtla skills"

**Skill response**:
```
❌ nixtla-skills CLI not found

The installer needs to be installed first:

```
git clone https://github.com/jeremylongshore/claude-code-plugins-nixtla.git
cd claude-code-plugins-nixtla
pip install -e packages/nixtla-claude-skills-installer
```

After installing, run this skill again.
```

---

## Persistence Model

**Critical concept to explain to users**:

Skills installed by this tool are **per-project** and **persistent**:

1. **Installation**: Skills copied to `.claude/skills/nixtla-*` in current project
2. **Persistence**: Skills remain there until explicitly updated or removed
3. **Updates**: Opt-in via `nixtla-skills update` (not automatic)
4. **Offline**: Skills are local files, work without internet
5. **Version control**: Different projects can have different skill versions

**Benefits**:
- Predictable behavior (skills don't change unexpectedly)
- Offline usage (skills are local)
- Project isolation (changes in one project don't affect others)

**Trade-off**:
- Manual updates required (run `nixtla-skills update` to get latest)

---

## Summary

This skill makes it **easy to install and update Nixtla skills** by:

1. **Guiding users** through init vs update choice
2. **Checking prerequisites** (CLI availability)
3. **Running the installer** (nixtla-skills command)
4. **Narrating the process** (explaining what's happening)
5. **Verifying results** (listing installed skills)
6. **Providing next steps** (how to use the skills)

**Key value**: Users don't need to understand the installer CLI - this skill does it for them and explains everything in plain language.

**Installed location**: `.claude/skills/nixtla-skills-bootstrap/`
**Self-referential**: This skill can update itself via `nixtla-skills update`
