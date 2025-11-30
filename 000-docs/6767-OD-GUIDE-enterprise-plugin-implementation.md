# Implementing the Enterprise Plugin README Standard

**Doc ID:** 6767-OD-GUIDE-enterprise-plugin-implementation
**Version:** 1.0.0
**Created:** 2025-11-30
**Related:** 6767-OD-REF-enterprise-plugin-readme-standard
**Classification:** Internal Guide

-----

## Purpose

This guide tells Claude Code how to implement the Enterprise Plugin README Standard in a repository. Read the reference document first (`6767-OD-REF-enterprise-plugin-readme-standard.md`), then follow these instructions.

-----

## When to Use This Guide

Use this guide when:

- Setting up a new enterprise sponsor repository from scratch
- Restructuring an existing sponsor repo to match the standard
- Asked to "apply the enterprise readme standard" or similar

-----

## Implementation Steps

### Step 1: Assess Current State

Before making changes, understand what exists:

1. Review the current README.md structure
2. List all existing plugins in the `plugins/` directory
3. List all existing documentation in `000-docs/`
4. Identify which plugins have working code vs just specs
5. Note any historical docs (AARs, research) that should be archived

Create a mental map of: What's working? What's specified? What's just an idea?

### Step 2: Create Directory Structure

Ensure these directories exist:

```
000-docs/
├── global/
├── plugins/
└── archive/
```

If restructuring, move existing docs appropriately:

- Repo-wide docs (executive summary, engagement options) → `000-docs/global/`
- Per-plugin docs → `000-docs/plugins/[slug]/`
- Historical docs (AARs, old research, decision logs) → `000-docs/archive/`

### Step 3: Place the Reference Document

Copy `6767-OD-REF-enterprise-plugin-readme-standard.md` to `000-docs/` at the root level (not in a subfolder). This is the canonical reference that explains how the repo is organized.

### Step 4: Create Global Documentation

Create these files in `000-docs/global/`:

**000-EXECUTIVE-SUMMARY.md**

- Write a 1-page summary for the sponsor's decision maker
- Cover: What this is, why it matters, what's ready, recommended next step
- Keep it scannable - use bullets, not paragraphs

**001-ENGAGEMENT-OPTIONS.md**

- Detail the three engagement tiers (Evaluate, Pilot, Platform)
- Include timeline estimates and what's included
- Make it easy to say "let's do the Pilot option"

**002-DECISION-MATRIX.md** (if multiple plugins)

- Create a scoring matrix to help prioritize
- Consider: business impact, effort, risk, dependencies
- Provide a clear recommendation

### Step 5: Organize Plugin Documentation

For each plugin that's Specified, In Progress, or Working:

1. Create `000-docs/plugins/[plugin-slug]/`
2. Create all 6 required documents:
   - 01-BUSINESS-CASE.md
   - 02-PRD.md
   - 03-ARCHITECTURE.md
   - 04-USER-JOURNEY.md
   - 05-TECHNICAL-SPEC.md
   - 06-STATUS.md

If migrating from a different structure:

- Map existing docs to the new 6-doc format
- Consolidate if necessary (e.g., combine multiple architecture docs)
- Fill gaps where documentation is missing

For Ideas (💡), no docs are needed yet - they'll just be listed in the README table.

### Step 6: Rewrite the README

Replace the existing README.md with the standard structure. Include all 14 sections in order:

1. **Header** - Title, value prop, sponsor info, version, status counts
2. **Quick Navigation** - Audience routing table
3. **Portfolio Overview** - Summary metrics
4. **Working Plugins** - Table with doc links
5. **Specified Plugins** - Table with doc links
6. **In Progress** - Table with progress and ETA
7. **Ideas & Backlog** - Concepts not yet specified
8. **Demo** - How to try working plugins
9. **Architecture Overview** - ASCII diagram
10. **Documentation Index** - Explain the 6-doc standard
11. **Engagement Options** - Summary table
12. **Contact** - Jeremy's info
13. **License & Disclaimer** - MIT + caveats
14. **Footer** - Maintained by / Sponsored by

**Critical:** Count plugins accurately for the summary. Double-check all doc links work.

### Step 7: Populate the Ideas Section

Gather any plugin concepts that aren't fully specified:

- Check meeting notes, discussions, or comments in existing docs
- Ask if there are additional ideas to capture
- Add each as a row in the Ideas & Backlog table

Format each idea with:

- Name
- Category (Efficiency or Growth)
- Potential Impact (one phrase)
- What's Needed (discovery call, research, POC, etc.)

### Step 8: Verify and Clean Up

Review the complete repo:

- [ ] All README sections present and in order
- [ ] Summary counts match actual plugins
- [ ] Every doc link works (test by clicking)
- [ ] No placeholder text like `[TODO]` or `[Plugin Name]`
- [ ] Working plugins have functional demo commands
- [ ] Contact info is accurate
- [ ] VERSION file updated
- [ ] CHANGELOG.md updated with restructure entry

### Step 9: Archive Historical Docs

Move any docs that don't fit the new structure to `000-docs/archive/`:

- After Action Reports (AARs)
- Old research documents
- Superseded specifications
- Decision logs
- Meeting notes

Preserve these for reference but keep them out of the main navigation.

-----

## Creating New Plugins

When asked to add a new plugin to an enterprise showcase repo:

### If it's just an idea:

1. Add a row to the Ideas & Backlog table in README
2. No other work needed

### If it should be fully specified:

1. Create `000-docs/plugins/[slug]/` directory
2. Write all 6 docs following the templates in the reference standard:
   - 01-BUSINESS-CASE.md - Focus on ROI and recommendation
   - 02-PRD.md - Define requirements and success metrics
   - 03-ARCHITECTURE.md - Design the system with diagrams
   - 04-USER-JOURNEY.md - Walk through the user experience
   - 05-TECHNICAL-SPEC.md - Detail implementation
   - 06-STATUS.md - Mark as "Not Started" initially
3. Create `plugins/[slug]/` directory with basic structure:
   - `.claude-plugin/plugin.json`
   - `README.md` (quick start)
   - Empty `commands/`, `skills/`, `scripts/`, `tests/` folders
4. Add to Specified Plugins table in README with all doc links
5. Update summary counts

### If building the plugin:

1. Move from Specified to In Progress table
2. Update 06-STATUS.md as work progresses
3. When demo-ready, move to Working table
4. Update summary counts

-----

## Writing Plugin Documentation

When writing the 6 docs for a plugin, follow these guidelines:

### 01-BUSINESS-CASE.md

Start with the problem, not the solution. Be specific about:

- Who feels this pain (job title, company type)
- How often they feel it (daily, weekly, per project)
- What it costs them (time, money, opportunity)

The ROI calculation should be concrete. Use real numbers or reasonable estimates. Show your math.

End with a clear recommendation: Build, Don't Build, or Needs Discovery.

### 02-PRD.md

Write user stories from the user's perspective, not the developer's. Bad: "System shall process data." Good: "As a data scientist, I want to run benchmarks with one command so I can quickly validate model performance."

Separate MVP from future scope. Be ruthless about what's truly needed for v1.

### 03-ARCHITECTURE.md

ASCII diagrams are preferred - they render everywhere and are easy to update. Show:

- Where this plugin fits in the Claude Code ecosystem
- External systems it talks to
- Data flow direction

Be explicit about security - how are API keys handled? What data is logged?

### 04-USER-JOURNEY.md

Write this as if teaching someone who's never used the plugin. Include:

- Exact commands to type
- What output they'll see
- What success looks like

The Complete Example section should be copy-paste ready - a user should be able to follow it verbatim.

### 05-TECHNICAL-SPEC.md

This is for the engineer who will maintain this after you're gone. Include:

- Every dependency and why it's needed
- Configuration options and defaults
- How to run tests
- Common failure modes and fixes

### 06-STATUS.md

Keep this current. It's the first place people look to understand where things stand. Use the status badges consistently:

- 🟢 Complete / Passing / Active
- 🟡 Partial / In Progress / Some Issues
- 🔴 Blocked / Failing / Critical Issues
- ⚪ Not Started / Not Applicable

-----

## Common Mistakes to Avoid

**Don't create empty placeholder docs.** If you don't have content for a doc yet, don't create the file. It's better to have 4 complete docs than 6 half-empty ones.

**Don't duplicate content across docs.** Each doc has a specific purpose. If you're repeating yourself, you're probably in the wrong doc.

**Don't forget the Ideas section.** This is where future possibilities live. An empty Ideas table suggests a lack of vision.

**Don't use relative paths incorrectly.** Doc links from README.md use paths like `000-docs/plugins/slug/01-BUSINESS-CASE.md`. Test every link.

**Don't let status docs go stale.** If 06-STATUS.md says "In Progress" but nothing's happened in weeks, update it to reflect reality.

-----

## Maintaining the Standard

When the standard needs to evolve:

1. Update `6767-OD-REF-enterprise-plugin-readme-standard.md` with changes
2. Update version number and changelog in the reference doc
3. Update this implementation guide if process changes
4. Apply changes to existing repos as time permits

The standard should grow based on what works in practice. If something is consistently awkward or missing, propose an update.

-----

## Questions This Guide Should Answer

**Q: How do I know if a plugin should be an Idea vs Specified?**
A: If you can write all 6 docs with confidence, it's ready to be Specified. If you need to talk to stakeholders, do research, or build a POC first, it's an Idea.

**Q: What if a plugin doesn't need all 6 docs?**
A: It probably does. Even simple plugins have a business case, architecture, and user journey. If truly unnecessary, note why in that doc rather than omitting it.

**Q: How do I handle plugins that span multiple categories?**
A: Pick the primary category (Efficiency or Growth). You can note secondary benefits in the business case.

**Q: What if the sponsor wants a different README structure?**
A: This standard is our baseline. If they have specific preferences, accommodate them while preserving the core navigation and documentation principles.

**Q: Where do meeting notes and ongoing discussions go?**
A: Archive folder for historical notes. For active discussions, consider using GitHub Discussions or Issues rather than cluttering the docs folder.

-----

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-11-30 | Initial guide |
