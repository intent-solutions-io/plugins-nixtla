# Claude Skills Authoring Guide

**Document ID**: 6767-n-DR-GUID-claude-skills-authoring-guide
**Version**: 1.0.0
**Status**: CANONICAL - Cross-Repo Standard
**Created**: 2025-12-06
**Updated**: 2025-12-06

**Master Reference**: `000-docs/077-SPEC-MASTER-claude-skills-standard.md`
**Schema Reference**: `000-docs/6767-m-DR-STND-claude-skills-frontmatter-schema.md`

---

## Purpose

Step-by-step guide for creating effective Claude Skills. Covers best practices, common patterns, security guidance, and production readiness.

---

## Quick Start Template

```yaml
---
name: your-skill-name
description: |
  [Primary capabilities]. [Secondary features].
  Use when [3-4 trigger scenarios].
  Trigger with "[phrase 1]", "[phrase 2]", "[phrase 3]".
allowed-tools: "Read,Write,Glob,Grep,Edit"
version: "1.0.0"
---

# [Skill Name]

[1-2 sentence purpose statement.]

## Overview

[3-5 sentences: what, when, capabilities, output]

## Prerequisites

**Required**:
- [Tool/package 1]: [Purpose]

**Environment Variables**:
- `ENV_VAR`: [Description]

## Instructions

### Step 1: [Action Verb]

[Imperative instructions]

### Step 2: [Action Verb]

[More instructions]

## Output

- **[Artifact 1]**: [Description]
- **[Artifact 2]**: [Description]

## Error Handling

1. **Error**: `[Message]`
   **Solution**: [Fix]

2. **Error**: `[Message]`
   **Solution**: [Fix]

## Examples

### Example 1: [Scenario]

**Input**: [Example]
**Output**: [Result]

## Resources

- Reference: `{baseDir}/references/API_REFERENCE.md`
- Script: `{baseDir}/scripts/validate.py`
```

---

## Writing Effective Descriptions

### The Formula

```
[Primary capabilities]. [Secondary features]. Use when [scenarios]. Trigger with "[phrases]".
```

### Quality Checklist

| Criterion | Weight | How to Achieve |
|-----------|--------|----------------|
| **Action-oriented** | 20% | Use strong verbs: "Generates", "Analyzes", "Transforms" |
| **Clear triggers** | 25% | Include "Use when [scenarios]" |
| **Comprehensive** | 15% | Cover what + when + scope |
| **Natural language** | 20% | Include phrases users actually say |
| **Specificity** | 10% | Be specific without being verbose |
| **Technical terms** | 10% | Use domain keywords users naturally use |

### Voice Rules

**ALWAYS use third person** - descriptions are injected into system prompt:

```yaml
# ✅ CORRECT (third person)
description: "Processes Excel files and generates reports"

# ❌ WRONG (first person)
description: "I can help you process Excel files"

# ❌ WRONG (second person)
description: "You can use this to process Excel files"
```

### Good vs Bad Examples

```yaml
# ✅ EXCELLENT (specific, triggers, third person)
description: |
  Analyzes Polymarket prediction market contracts using TimeGPT forecasting.
  Fetches contract odds, transforms to time series, generates price predictions.
  Use when analyzing prediction markets, forecasting contract prices.
  Trigger with 'forecast Polymarket', 'analyze prediction market'.

# ❌ BAD (vague, no triggers)
description: "Helps with prediction markets"

# ❌ BAD (too generic)
description: "Data analysis tool"
```

---

## Content Guidelines

### Size Limits

| Content | Target | Maximum |
|---------|--------|---------|
| SKILL.md body | ~300 lines | **500 lines** |
| Token budget | ~2,500 tokens | 5,000 tokens |
| Description | ~250 chars | 1,024 chars |

### Required Sections

1. **Purpose** (1-2 sentences)
2. **Overview** (3-5 sentences)
3. **Prerequisites** (tools, packages, env vars)
4. **Instructions** (step-by-step, imperative voice)
5. **Output** (what artifacts are produced)
6. **Error Handling** (4+ common failures with solutions)
7. **Examples** (2-3 concrete input/output pairs)
8. **Resources** (links to bundled files)

### Imperative Voice

Use imperative voice for instructions:

```markdown
# ✅ CORRECT (imperative)
### Step 1: Analyze the input data
Run the validation script to check data format.

# ❌ WRONG (passive/descriptive)
### Step 1: Input data analysis
The input data should be analyzed for format issues.
```

---

## Progressive Disclosure

### When to Split Content

Split SKILL.md when it exceeds **400 lines**:

**Pattern 1: High-level guide with references**
```markdown
# PDF Processing

## Quick start
[Basic instructions - 50 lines]

## Advanced features
**Form filling**: See [FORMS.md](FORMS.md)
**API reference**: See [REFERENCE.md](REFERENCE.md)
```

**Pattern 2: Domain-specific organization**
```
bigquery-skill/
├── SKILL.md (overview - 200 lines)
└── reference/
    ├── finance.md (revenue metrics)
    ├── sales.md (pipeline data)
    └── product.md (usage analytics)
```

### Critical Rule: One-Level-Deep References

**AVOID deeply nested references** - Claude may only partially read nested files.

```
# ❌ BAD (too deep)
SKILL.md → advanced.md → details.md → actual_info.md

# ✅ GOOD (one level)
SKILL.md → advanced.md
SKILL.md → reference.md
SKILL.md → examples.md
```

---

## Path References

### Always Use `{baseDir}`

**NEVER hardcode absolute paths** - breaks portability:

```markdown
# ✅ CORRECT
Run: `python {baseDir}/scripts/validate.py`
See: `{baseDir}/references/API_DOCS.md`

# ❌ WRONG
Run: `python /home/user/skills/my-skill/scripts/validate.py`
```

### Forward Slashes Only

```markdown
# ✅ CORRECT (works everywhere)
{baseDir}/scripts/helper.py

# ❌ WRONG (breaks on Unix)
{baseDir}\scripts\helper.py
```

---

## Security Best Practices

### Principle of Least Privilege

Grant ONLY tools the skill actually needs:

```yaml
# ✅ GOOD - Minimal necessary tools
allowed-tools: "Read,Glob,Grep"              # Read-only audit
allowed-tools: "Read,Write,Edit"             # File transformation
allowed-tools: "Bash(git:*),Read,Grep"       # Git operations only

# ❌ BAD - Overly permissive
allowed-tools: "Bash,Read,Write,Edit,Glob,Grep,WebSearch,Task,Agent"
allowed-tools: "Bash"                        # Unscoped = all commands
```

### When to Use `disable-model-invocation: true`

Set this flag for skills that:
- Perform **destructive operations** (delete files, drop databases)
- **Deploy to production**
- Access **sensitive credentials**
- Run **irreversible commands**
- Should **NEVER auto-activate**

```yaml
---
name: deploy-production
description: Deploy to production. Dangerous - requires explicit invocation.
disable-model-invocation: true
allowed-tools: "Bash(deploy:*),Read,Glob"
---
```

### Security Audit Checklist

Before using untrusted skills:
- [ ] Review all bundled files (SKILL.md, scripts, resources)
- [ ] Check for unusual network calls
- [ ] Inspect scripts for malicious code
- [ ] Verify tool invocations match stated purpose
- [ ] Validate external URLs (if any)

---

## Model Selection

### When to Override

| Scenario | Recommendation |
|----------|----------------|
| Most skills | `model: inherit` or omit |
| Complex reasoning | `claude-opus-4-*` |
| Fast, simple tasks | `claude-haiku-*` |
| Balanced | `claude-sonnet-4-*` |

### Testing Across Models

**Always test with all models you plan to use:**

- **Haiku**: Does the skill provide sufficient guidance?
- **Sonnet**: Is content clear and efficient?
- **Opus**: Are instructions avoiding over-explanation?

What works for Opus may need more detail for Haiku.

---

## Common Patterns

### Pattern 1: Script Automation

```markdown
### Step 1: Fetch Data
Run: `python {baseDir}/scripts/fetch_data.py --output data.json`

### Step 2: Transform
Run: `python {baseDir}/scripts/transform.py --input data.json`

### Step 3: Report
Run: `python {baseDir}/scripts/generate_report.py`
```

### Pattern 2: Validation Loop

```markdown
### Step 1: Make changes
Edit the configuration file.

### Step 2: Validate
Run: `python {baseDir}/scripts/validate.py`

### Step 3: Fix and repeat
If validation fails, fix issues and run validation again.
Only proceed when validation passes.
```

### Pattern 3: Workflow with Checklist

```markdown
## Workflow

Copy this checklist and track progress:

```
- [ ] Step 1: Analyze input
- [ ] Step 2: Transform data
- [ ] Step 3: Validate output
- [ ] Step 4: Generate report
```
```

---

## Production Readiness Checklist

### Naming & Description

- [ ] `name` matches folder name (lowercase + hyphens)
- [ ] `name` under 64 characters
- [ ] `description` under 1024 characters
- [ ] `description` uses **third person** voice
- [ ] `description` includes what + when + trigger phrases
- [ ] No reserved words (`anthropic`, `claude`)

### Structure & Tools

- [ ] SKILL.md at root of skill folder
- [ ] Body under **500 lines**
- [ ] Uses `{baseDir}` for all paths
- [ ] No hardcoded absolute paths
- [ ] `allowed-tools` includes only necessary tools
- [ ] Forward slashes in all paths

### Instructions Quality

- [ ] Has all required sections
- [ ] Uses **imperative voice**
- [ ] **2-3 concrete examples** with input/output
- [ ] **4+ common errors** documented with solutions
- [ ] One-level-deep file references only

### Testing

- [ ] Tested with Haiku, Sonnet, and Opus
- [ ] Trigger phrases activate skill correctly
- [ ] Does NOT trigger on unrelated requests
- [ ] Scripts execute without errors
- [ ] Examples produce expected output

### Security

- [ ] No secrets or credentials in skill
- [ ] Tools appropriately scoped
- [ ] Dangerous operations require explicit invocation
- [ ] External dependencies audited

---

## Versioning

### Semantic Versioning

```
MAJOR.MINOR.PATCH
  │     │     └── Bug fixes, clarifications
  │     └──────── New features, additive changes
  └────────────── Breaking changes to interface
```

### Changelog in SKILL.md

```markdown
## Version History

- **v2.0.0** (2025-12-01): Breaking - Changed output format to JSON
- **v1.1.0** (2025-11-15): Added batch processing support
- **v1.0.0** (2025-11-01): Initial release
```

### Deprecation Strategy

1. Add deprecation notice to description:
   ```yaml
   description: "[DEPRECATED - Use new-skill instead] Original description..."
   ```
2. Set `disable-model-invocation: true`
3. Keep available for manual invocation during transition
4. Remove in next major version

---

## Critical Gotchas

1. **Skills NOT in system prompt** - They're in the tools array as part of Skill meta-tool

2. **NOT concurrency-safe** - Avoid simultaneous skill invocations

3. **`when_to_use` is undocumented** - Use detailed `description` instead

4. **Hardcoded paths break portability** - Always use `{baseDir}`

5. **Token budget filtering** - 15,000 chars total for all skill descriptions; verbose skills may be silently filtered

6. **One-level-deep references only** - Claude may partially read nested files

7. **`allowed-tools` only in Claude Code** - Not supported on claude.ai web version

---

## Sources

- [Official Anthropic Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Official Anthropic Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)
- [Lee Han Chung Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)

---

**Last Updated**: 2025-12-06
**Status**: CANONICAL - Cross-Repo Standard
