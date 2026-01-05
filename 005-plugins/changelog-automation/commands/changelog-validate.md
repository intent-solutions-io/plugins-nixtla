---
name: changelog-validate
description: Validate configuration and environment before running changelog generation
---

# Validate Changelog Setup

Validate configuration and environment before running changelog generation.

## Purpose

Run diagnostic checks to ensure:
- Config file exists and is valid
- Required environment variables are set
- Templates exist
- Output path is writable
- API tokens have correct permissions

## Workflow

### Step 1: Check Config File

1. Call MCP tool `get_changelog_config`
2. If error:
   - Config file not found → Suggest creating from example
   - Invalid JSON → Show JSON syntax error
   - Missing required fields → List missing fields
3. If success:
   - Display config summary
   - Proceed to Step 2

### Step 2: Validate Data Sources

For each source in config:

**GitHub Source:**
1. Check environment variable (e.g., GITHUB_TOKEN)
   - Not found → Error with instructions
   - Found → Mask token (show last 4 chars only)
2. Test GitHub API access (mock request to verify token)
   - 401/403 → Invalid token or insufficient permissions
   - Success → Display repo access confirmed

**Slack Source:**
1. Check environment variable (e.g., SLACK_TOKEN)
2. Test Slack API access
3. Verify channel exists

**Git Source:**
1. Check if current directory is a git repository
2. Verify branch exists
3. Test git log command

### Step 3: Validate Template

1. Check template path from config
2. Verify file exists
3. Parse frontmatter placeholders
4. Validate template structure

### Step 4: Validate Output Path

1. Check if output path is writable
2. If file exists, check if writable (overwrite permission)
3. If directory doesn't exist, check parent directory

### Step 5: Display Summary

```
🔍 Validating changelog automation setup...

✅ Config file found: .changelog-config.json
✅ GitHub token: GITHUB_TOKEN (found, valid, ends in ...abc1)
✅ Repository: myorg/myrepo (accessible, 150 PRs found)
✅ Template: changelogs/weekly-template.md (exists, valid)
✅ Output path: CHANGELOG.md (writable)
✅ Quality threshold: 80 (valid range 0-100)

🎉 All checks passed! Ready to generate changelog.

Run: /changelog-weekly to generate changelog for last 7 days
     /changelog-custom to specify custom date range
```

## Error Output

```
❌ Validation failed

Issues found:
  1. GITHUB_TOKEN not found in environment
     → Run: export GITHUB_TOKEN="ghp_..."

  2. Template not found: changelogs/weekly-template.md
     → Create template or update config

  3. Output path not writable: CHANGELOG.md
     → Check file permissions

Fix these issues and run /changelog-validate again.
```

## Success Criteria

All checks must pass:
- ✅ Config file valid
- ✅ At least one data source configured
- ✅ All required tokens present and valid
- ✅ Template exists
- ✅ Output path writable
- ✅ Quality threshold in valid range (0-100)

If all pass, user can proceed with `/changelog-weekly` or `/changelog-custom`.
