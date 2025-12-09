# Skills Schema - Complete Reference

**Purpose**: Single authoritative reference for Claude Skills composition and development.

**Location**: `000-docs/skills-schema/`

---

## Contents

### SKILLS-STANDARD-COMPLETE.md (65KB) ⭐

**The ONLY document you need** for writing/auditing Claude Skills.

This comprehensive reference combines:
1. **Master Skills Standard** (Anthropic official spec)
2. **Appendix A**: Frontmatter Schema Quick Reference
3. **Appendix B**: Authoring Guide & Patterns
4. **Appendix C**: Nixtla Skills Strategy

**Use this for**:
- ✅ Complete SKILL.md structure specification
- ✅ YAML frontmatter fields (name, description, allowed-tools, version, etc.)
- ✅ Instruction-body best practices
- ✅ Security & safety guidance
- ✅ Production-readiness checklist (18-point checklist)
- ✅ Canonical SKILL.md template
- ✅ Description formula & patterns
- ✅ Validation rules with examples
- ✅ Nixtla-specific strategy & conventions

---

## Quick Start

### Writing a New Skill

1. **Read**: `SKILLS-STANDARD-COMPLETE.md` (sections 1-4: Core concepts + SKILL.md spec)
2. **Copy**: Canonical template from section 10
3. **Write**: Description using 3-sentence formula (Appendix B)
4. **Validate**: Use production-readiness checklist (section 8)

### Auditing an Existing Skill

1. **Load**: `SKILLS-STANDARD-COMPLETE.md` (Appendix A: Frontmatter schema)
2. **Check**: Name, description, allowed-tools against validation rules
3. **Verify**: Body structure against section 5
4. **Test**: Run through 18-point checklist (section 8)

---

## Document Structure

### Main Content (Sections 1-13)

1. **Core Concepts** - What/When/How/Tools/Model
2. **Folder & Discovery** - Directory structure, naming conventions
3. **SKILL.md Specification** - Complete structure
4. **YAML Frontmatter Fields** - All field definitions
5. **Instruction-Body Best Practices** - Content guidelines
6. **Security & Safety** - Allowed-tools, permissions
7. **Model Selection** - When to override model
8. **Production-Readiness Checklist** ⭐ - 18-point validation
9. **Versioning & Evolution** - Semantic versioning
10. **Canonical SKILL.md Template** ⭐ - Copy-paste ready
11. **Minimal Example Skill** - PR review helper
12. **Author Checklist** - Step-by-step validation
13. **Open Questions** - Experimental features

### Appendix A: Frontmatter Schema

- Complete YAML schema with comments
- Field reference table
- Validation rules (name/description/allowed-tools)
- Examples (valid vs invalid)
- Directory structure and token costs

### Appendix B: Authoring Guide

- Quick start template
- Description formula: `[Capabilities]. [How]. Use when [scenarios]. Trigger with "[phrases]".`
- Step-by-step skill creation
- Common anti-patterns
- Progressive disclosure patterns
- Security best practices

### Appendix C: Nixtla Strategy

- Skills vs plugins vs slash commands (decision matrix)
- When to create a skill
- Promotion path (lab → 003-skills/ → production)
- Versioning strategy
- Nixtla-specific naming conventions
- Skills universe overview (11 skills across 4 categories)

---

## Compliance Hierarchy

### 1. Anthropic Official (Main Content)
- **Name**: lowercase + hyphens, <= 64 chars, no reserved words
- **Description**: <= 1024 chars, third person, WHAT+WHEN+triggers
- **Body**: <= 500 lines, imperative voice, `{baseDir}` paths
- **Source**: Sections 1-13

### 2. Nixtla Internal (Appendix A + B)
- **Description formula**: 3 sentences (WHAT, HOW, WHEN)
- **Target length**: 300-600 chars (not max 1024)
- **Trigger phrases**: 2-4 key examples (not exhaustive list)
- **Source**: Appendix B

### 3. Nixtla Strategy (Appendix C)
- **Skills**: Guidance/orchestration (read-only, complex reasoning)
- **Plugins**: Execution (MCP servers, real operations)
- **Promotion**: Lab → 003-skills/ when stable
- **Source**: Appendix C

---

## Key Sections Reference

| Need | Section | Page Estimate |
|------|---------|---------------|
| **Quick template** | Section 10 (Canonical Template) | 50% through doc |
| **Validation checklist** | Section 8 (Production-Readiness) | 40% through doc |
| **Field definitions** | Section 4 (YAML Frontmatter) | 20% through doc |
| **Description formula** | Appendix B (Authoring Guide) | 70% through doc |
| **Schema reference** | Appendix A (Frontmatter Schema) | 65% through doc |
| **Strategy guide** | Appendix C (Nixtla Strategy) | 75% through doc |

---

## External References

- [Anthropic Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Anthropic Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Claude Code Skills](https://code.claude.com/docs/en/skills)
- [Anthropic Engineering Blog](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Lee Han Chung Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)

---

## Version History

- **v2.0.0** (2025-12-08): Consolidated 4 separate docs into single SKILLS-STANDARD-COMPLETE.md
- **v1.1.0** (2025-12-08): Added skills-schema folder structure
- **v1.0.0** (2025-12-06): Initial standards documented

---

**Last Updated**: 2025-12-08
**Maintained By**: Intent Solutions (Jeremy Longshore)
**File**: `SKILLS-STANDARD-COMPLETE.md` (65KB, 2488 lines)
**Purpose**: Single source of truth for skill composition
