---
name: changelog-weekly
description: Generate changelog for the last 7 days using configured data sources
---

# Generate Weekly Changelog

Generate changelog for the last 7 days using configured data sources.

## Workflow

You are the Changelog Orchestrator Agent. Follow the 6-phase workflow to generate a weekly changelog:

### Phase 1: Initialize & Fetch

1. Load config via MCP tool `get_changelog_config`
2. Calculate date range (today - 7 days to today)
3. For each configured source, call MCP tool `fetch_changelog_data` with:
   - source_type: From config
   - start_date: 7 days ago (ISO format)
   - end_date: Today (ISO format)
   - config: Source-specific config from .changelog-config.json
4. Aggregate all items into unified dataset

### Phase 2: Writer Agent - Synthesis

1. Group items by type (features, fixes, breaking, other)
2. Generate narrative summary (2-3 sentences covering key themes)
3. Identify top 3-5 highlights (most impactful changes)
4. Write detailed sections for each type
5. Apply tone guidelines (user-focused, concise, professional)

### Phase 3: Formatter Agent - Compliance

1. Load template from config path
2. Generate frontmatter:
   - date: Today's date (YYYY-MM-DD)
   - version: Extract from latest tag or increment
   - authors: Unique authors from all items
   - categories: Derive from types (features/fixes/etc.)
3. Validate frontmatter via MCP tool `validate_frontmatter`
4. Apply template with variable substitution
5. Run quality check via MCP tool `validate_changelog_quality`

### Phase 4: Reviewer Agent - Quality Gate

1. Review generated changelog for:
   - Completeness (all changes covered)
   - Accuracy (no hallucinations, facts from data)
   - Tone (user-friendly, not too technical)
   - Clarity (easy to understand)
2. Check MCP quality score (must be ≥ threshold from config)
3. If score < threshold:
   - Provide feedback
   - Return to Phase 2 (max 2 iterations)
4. If score ≥ threshold: Approve and proceed

### Phase 5: PR Writer Agent - Repo Ops

1. Write changelog via MCP tool `write_changelog`:
   - content: Final markdown
   - output_path: From config
   - overwrite: true
2. Generate PR description:
   - Summary of date range
   - Item count by type
   - Quality score
   - Reviewer checklist
3. Create PR via MCP tool `create_changelog_pr`:
   - branch_name: changelog-{YYYY-MM-DD}
   - commit_message: docs: add changelog for {YYYY-MM-DD}
   - pr_title: Changelog for Week of {start} to {end}
   - pr_body: Generated description

### Phase 6: User Handoff

1. Display summary:
   - PR URL
   - Quality score
   - Item count
   - Date range
2. Provide next steps:
   - Review PR (link)
   - Merge when ready
   - Iterate if needed

## Output

```
🎉 Changelog PR created successfully!

📋 Summary:
  - Date range: 2025-12-21 to 2025-12-28
  - Changes: 20 items (12 PRs, 8 issues)
  - Quality score: 92/100
  - PR: https://github.com/org/repo/pull/1234

Next steps:
  1. Review PR: Click link above
  2. Merge when ready
  3. Run /changelog-custom for different date ranges
```

## Error Handling

If any phase fails:
- Phase 1 (Data Fetch): Check tokens, API access, date format
- Phase 2 (Synthesis): Retry with simpler prompt
- Phase 3 (Formatting): Check template path, validate frontmatter
- Phase 4 (Quality): Lower threshold or iterate
- Phase 5 (PR Creation): Check GitHub permissions, branch conflicts

Always provide clear error messages with suggested fixes.
