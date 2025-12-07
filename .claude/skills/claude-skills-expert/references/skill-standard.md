# Claude Skills Technical Reference

**Master Standard**: `000-docs/098-SPEC-MASTER-claude-skills-standard.md`

**Sources**:
- [Official Anthropic Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Official Anthropic Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)
- [Lee Han Chung Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)

---

## Complete Frontmatter Schema

```yaml
---
# REQUIRED
name: skill-name                    # 64 chars max, lowercase + hyphens only
description: >                      # 1024 chars max, THIRD PERSON voice
  What it does. Use when [scenarios]. Trigger with "[phrases]".

# OPTIONAL
allowed-tools: "Read,Write,Glob"    # CSV of tools (scoped to execution)
model: inherit                      # or specific model ID
version: "1.0.0"                   # semver
license: "MIT"                     # license ref
mode: false                        # true = mode skill (prominent UI)
disable-model-invocation: false    # true = manual /skill-name only

# UNDOCUMENTED (avoid in production)
when_to_use: >                     # appends to description - status unclear
  Additional context.
---
```

## Skill Tool Architecture

Skills are NOT in the system prompt. They live in a meta-tool:

```javascript
tools: [
  { name: "Read", ... },
  { name: "Write", ... },
  {
    name: "Skill",                    // Meta-tool (capital S)
    inputSchema: { command: string },
    description: "<available_skills>..." // Dynamic list
  }
]
```

This enables dynamic loading without system prompt manipulation.

## Two-Message Injection Pattern

Skills inject **two separate messages**:

### Message 1 - Visible Metadata
```xml
<command-message>The "pdf" skill is loading</command-message>
<command-name>pdf</command-name>
<command-args>report.pdf</command-args>
```
- `isMeta: false` (default)
- Shown to user (~50-200 chars)

### Message 2 - Hidden Prompt
- Full SKILL.md content
- `isMeta: true`
- Hidden from UI, sent to API (~500-5000 words)

**Why two messages?** Single message would either clutter UI (isMeta: false) or hide activation entirely (isMeta: true).

## Three-Stage Execution Pipeline

### Stage 1: VALIDATION
- Syntax checking
- Skill existence verification
- Frontmatter parsing

### Stage 2: PERMISSION EVALUATION
1. Deny rules checked first
2. Allow rules checked second
3. Default: prompt user

### Stage 3: LOADING & INJECTION
1. SKILL.md content loaded
2. Two messages injected
3. Context modifier applied
4. Tool permissions scoped

## Tool Permission Syntax

```yaml
# Multiple tools (comma-separated)
allowed-tools: "Read,Write,Glob,Grep,Edit"

# Scoped bash commands
allowed-tools: "Bash(git:*),Bash(git diff:*),Read,Grep"

# NPM-scoped
allowed-tools: "Bash(npm:*),Bash(npx:*),Read,Write"

# Read-only audit
allowed-tools: "Read,Glob,Grep"
```

**NOTE**: `allowed-tools` only supported in Claude Code, not claude.ai web.

## Discovery Sources (Priority Order)

1. User: `~/.claude/skills/` (lowest)
2. Project: `.claude/skills/`
3. Plugin-provided
4. Built-in (highest)

Later sources override earlier when names conflict.

## Critical Gotchas

1. **Skills NOT in system prompt** - They're in tools array
2. **NOT concurrency-safe** - Avoid simultaneous invocations
3. **`when_to_use` undocumented** - Use detailed `description` instead
4. **Hardcoded paths break portability** - Always use `{baseDir}`
5. **Token budget filtering** - 15,000 chars total for skill descriptions
6. **One-level-deep references** - Claude may partially read nested files

## Token Constraints

| Content | Budget |
|---------|--------|
| All skill descriptions | 15,000 chars |
| SKILL.md body | <500 lines / 5,000 tokens |
| Reference files | Load on-demand |

## Directory Structure

```
skill-name/
├── SKILL.md              # REQUIRED
├── scripts/              # Executable (NO token cost)
├── references/           # Documentation (loaded into context)
└── assets/               # Templates (path reference only)
```

**Scripts execute without loading code into context. Only OUTPUT consumes tokens.**
