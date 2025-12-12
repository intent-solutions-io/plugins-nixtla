# Error Handling Guide

## Error: CLI Not Found

If `nixtla-skills` command is not available:

```
❌ nixtla-skills CLI not found

The Nixtla Skills installer needs to be installed first.

Installation Options:

1. Development Mode (from repo):
   ```
   git clone https://github.com/intent-solutions-io/plugins-nixtla.git
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

## Error: CLI Execution Failed

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

## Error: No Skills Installed

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
