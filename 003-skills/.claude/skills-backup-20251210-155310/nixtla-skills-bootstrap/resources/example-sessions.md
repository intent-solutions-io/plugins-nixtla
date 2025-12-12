# Example Sessions

## Example 1: First-Time Install

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

## Example 2: Update Existing Skills

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

## Example 3: CLI Not Installed

**User**: "Set up Nixtla skills"

**Skill response**:
```
❌ nixtla-skills CLI not found

The installer needs to be installed first:

```
git clone https://github.com/intent-solutions-io/plugins-nixtla.git
cd claude-code-plugins-nixtla
pip install -e packages/nixtla-claude-skills-installer
```

After installing, run this skill again.
```
