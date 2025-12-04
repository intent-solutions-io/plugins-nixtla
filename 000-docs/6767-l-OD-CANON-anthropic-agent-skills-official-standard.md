# Anthropic Agent Skills - Official Standard (Canonical Reference)

**Document ID**: 6767-OD-CANON-anthropic-agent-skills-official-standard.md
**Type**: OD - Overview & Documentation (Canonical)
**Status**: Authoritative Reference
**Source**: Official Anthropic Documentation (5 sources)
**Created**: 2025-12-03
**Last Updated**: 2025-12-04
**Version**: 2.0.0 (Comprehensive from 5 official sources)

---

## Purpose

This document captures the **complete official Anthropic Agent Skills standard** as defined in:

1. [Claude Platform Docs: Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
2. [Anthropic Engineering Blog: Equipping Agents for the Real World](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
3. [Claude Platform Docs: Agent Skills Quickstart](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/quickstart)
4. [Claude Platform Docs: Agent Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
5. [Claude Platform Docs: Build with Claude Skills Guide](https://platform.claude.com/docs/en/build-with-claude/skills-guide)

**This is the single source of truth for Agent Skills implementation.**

---

## Table of Contents

1. [What Are Agent Skills?](#what-are-agent-skills)
2. [Skill Structure](#skill-structure-official)
3. [SKILL.md Format](#skillmd-format-official)
4. [Progressive Disclosure Architecture](#progressive-disclosure-architecture)
5. [Description Writing Guidelines](#description-writing-guidelines-critical)
6. [Token Budget & File Organization](#token-budget--file-organization)
7. [Code Execution Patterns](#code-execution-patterns)
8. [Skill Types & Management](#skill-types--management)
9. [Platform Availability](#platform-availability)
10. [Best Practices](#best-practices-official-guidance)
11. [Anti-Patterns](#anti-patterns-what-to-avoid)
12. [Security Considerations](#security-considerations)
13. [Evaluation & Testing](#evaluation--testing)
14. [Quick Reference Card](#appendix-quick-reference-card)

---

## What Are Agent Skills?

Agent Skills are **modular, filesystem-based capabilities** that extend Claude's functionality with domain-specific expertise.

**Core Concept**: "Building a skill for an agent is like putting together an onboarding guide for a new hire." Skills transform general-purpose agents into specialized tools by packaging procedural knowledge into composable resources.

**Key Characteristics**:
- Filesystem-based (directories with files)
- Auto-discovered by Claude at startup
- Dynamically loaded when relevant (progressive disclosure)
- Can include executable code, templates, and reference materials
- Work across Claude API, Claude.ai, Claude Code, and Agent SDK

**Fundamental Philosophy**: "Skills are a simple concept with a correspondingly simple format. This simplicity makes it easier for organizations, developers, and end users to build customized agents and give them new capabilities."

---

## Skill Structure (Official)

### Required Structure

```
skill-name/
├── SKILL.md          # REQUIRED - Instructions with YAML frontmatter
├── scripts/          # OPTIONAL - Executable code (Python, bash)
├── resources/        # OPTIONAL - Reference materials, templates
└── [other].md        # OPTIONAL - Additional context files
```

**Critical**: `SKILL.md` is the **only required file**. Everything else is optional.

### Directory Naming Conventions

**Name field requirements**:
- Maximum **64 characters**
- **Lowercase letters, numbers, and hyphens only**
- No XML tags
- Cannot include reserved words: `"anthropic"`, `"claude"`

**Recommended naming pattern**: Use **gerund form** (verb + "-ing") for clarity:
- ✅ `processing-pdfs`, `analyzing-spreadsheets`, `managing-databases`
- ✅ Acceptable: Noun phrases or action-oriented forms
- ❌ Avoid: Vague names (`helper`, `utils`), overly generic terms

**Examples**:
- ✅ `pdf-extractor`
- ✅ `data-schema-mapper`
- ✅ `timegpt-forecasting-lab`
- ❌ `PDF_Extractor` (uppercase)
- ❌ `claude-helper` (reserved word)
- ❌ `helper` (too vague)

### File Organization Patterns

**Three organizational patterns** for scaling:

1. **High-level guide with references**: Quick start in SKILL.md; detailed features in FORMS.md, REFERENCE.md, EXAMPLES.md
2. **Domain-specific organization**: Separate files by domain (finance.md, sales.md, product.md) to avoid loading irrelevant context
3. **Conditional details**: Basic content inline; advanced content linked in collapsible sections

**Critical rule**: **One-level-deep references only**. Avoid nested references (SKILL.md → file1.md → file2.md). Claude may only partially read nested files.

### File Path Standards

- **Always use forward slashes**: `scripts/helper.py`, not `scripts\helper.py` (Windows paths break)
- **Name files descriptively**: `form_validation_rules.md`, not `doc2.md`
- **Organize by domain or feature** for easy discovery

---

## SKILL.md Format (Official)

### Complete Template

```markdown
---
name: your-skill-name
description: What this Skill does and when to use it
---

# Your Skill Name

## Instructions

[Step-by-step guidance for Claude]

## Examples

[Concrete usage examples]
```

### Frontmatter Requirements

#### `name` field (REQUIRED)

**Constraints**:
- Maximum **64 characters**
- **Lowercase letters, numbers, and hyphens only**
- No XML tags
- Cannot include reserved words: `"anthropic"`, `"claude"`

#### `description` field (REQUIRED)

**Constraints**:
- Non-empty
- Maximum **1024 characters**
- No XML tags
- **Must specify both functionality AND trigger conditions**

**Official template**: "Does X, Y, Z. Use when [conditions]."

**Critical**: Use **third person** (injected into system prompt):
- ✅ "Processes Excel files and generates reports"
- ❌ "I can help you..." or "You can use this to..."

#### Other Frontmatter Fields

**Official specification mentions ONLY `name` and `description`.**

**No mention of**:
- `version` ❌
- `allowed-tools` ❌
- `mode` ❌
- `model` ❌
- `disable-model-invocation` ❌
- `license` ❌

**Implication**: These fields are **NOT part of the official standard**. Including them may confuse Claude or break compatibility.

**Recommendation**: **Stick to official `name` and `description` only.**

---

## Progressive Disclosure Architecture

Skills load in **three levels**, consuming tokens only when necessary:

### Level 1: Metadata (Always Loaded)

**Content**: `name` and `description` from YAML frontmatter
**When**: At startup, pre-loaded into system prompt
**Token Cost**: ~100 tokens per skill

**Purpose**: Claude knows all available skills and can decide which to activate.

**Critical insight**: "At startup, agents preload this metadata into their system prompt, enabling them to recognize when each skill is relevant."

### Level 2: Instructions (On-Demand)

**Content**: Full `SKILL.md` body (everything after frontmatter)
**When**: When Claude determines skill is relevant
**Token Cost**: **Under 5,000 tokens** (recommended limit)

**Purpose**: Provide step-by-step guidance for using the skill.

**Loading mechanism**: "Claude invokes tools (like Bash) to read relevant `SKILL.md` files" when triggered.

**Critical**: Keep SKILL.md focused. Under 5k tokens means roughly **3,000-4,000 words** or **~500 lines of content** (official best practice recommends **under 500 lines**).

### Level 3: Resources (As Referenced)

**Content**: Additional files (`REFERENCE.md`, `scripts/`, `resources/`)
**When**: As referenced in SKILL.md or by Claude's judgment
**Token Cost**: Minimal - scripts execute without loading contents

**Purpose**: Provide detailed references, templates, and executable code.

**Key benefit**: "Claude selectively loads additional bundled files as needed" - not everything loads at once.

### Progressive Disclosure Benefit

**Official statement**: "Claude loads information in stages as needed, rather than consuming context upfront."

This design allows:
- Hundreds of skills installed without context bloat
- Efficient token usage across all skill levels
- Scalable skill libraries
- Unbounded context bundling through filesystem access

**Engineering blog**: "Agents with a filesystem and code execution tools don't need to read the entirety of a skill into their context window when working on a particular task."

---

## Description Writing Guidelines (CRITICAL)

### Core Requirements

**Descriptions are Level 1 metadata** - the ONLY information Claude sees before deciding to activate a skill. If your description doesn't match the user's request, the skill **will never trigger**.

**Critical insight**: "There is no algorithmic skill selection - Claude reads ALL descriptions and uses native language understanding."

### Effective Description Pattern

**Template**:
```yaml
description: "[Capabilities]. [Features]. Use when [trigger scenarios]. Trigger with [example phrases]."
```

**Formula breakdown**:
1. **Primary capabilities** as action verbs (what does it do?)
2. **Secondary features** with specifics (how does it work?)
3. **"Use when [3-4 explicit trigger scenarios]"** (when should Claude activate it?)
4. **"Trigger with [example phrases]"** (what will users say?)

### Examples from Official Docs

**Good example** (PDF skill):
```yaml
description: "Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDFs or document extraction."
```

**Why it works**:
- Action verbs: "Extract", "fill", "merge"
- Specific features: "text and tables", "forms"
- Clear triggers: "working with PDFs", "document extraction"
- Natural language: "PDFs", "forms", "documents"

**Bad example**:
```yaml
description: "Helps with forecasting"
```

**Why it fails**:
- Vague verb: "helps with"
- No specific features
- No trigger conditions
- No natural language examples

### Third Person Voice (CRITICAL)

**Always use third person** - descriptions are injected into system prompt:

✅ **Good**:
- "Processes Excel files and generates reports"
- "Analyzes time series data and creates forecasts"
- "Extracts text from PDFs and fills forms"

❌ **Bad**:
- "I can help you process Excel files"
- "You can use this to analyze data"
- "This skill processes documents"

### Include Key Terms for Activation

**Strategy**: Include variations of how users phrase requests.

**Example for forecasting skill**:
- Primary terms: "forecast", "predict", "time series"
- User phrases: "forecast my sales", "predict revenue", "analyze time series"
- Related terms: "demand planning", "sales prediction", "trend analysis"

**Official guidance**: "Pay special attention to skill name and description, as Claude uses these when deciding whether to trigger the skill."

### Avoid Ambiguity

**Problematic patterns**:
- ❌ "Helps with documents" (which documents? what operations?)
- ❌ "Processes data" (what kind of data? how?)
- ❌ "Does stuff with files" (completely useless)

**Better patterns**:
- ✅ "Converts CSV files to Parquet format with schema validation"
- ✅ "Analyzes M4 competition datasets and generates accuracy metrics"
- ✅ "Creates Airflow DAGs from experiment configurations"

---

## Token Budget & File Organization

### SKILL.md Size Limits

| Content | Target | Maximum |
|---------|--------|---------|
| Frontmatter | ~50 tokens | 100 tokens |
| Instructions | 2,000-3,000 tokens | 5,000 tokens |
| **Total** | **2,500 tokens** | **5,000 tokens** |

**Official best practice**: **Keep SKILL.md under 500 lines** for optimal performance.

**Rule**: If SKILL.md exceeds 5,000 tokens (~800 lines), split into referenced files.

### When to Split Files

**Official guidance**: "When `SKILL.md` becomes unwieldy, split content across separate files."

**Splitting strategy**:

1. **Keep in SKILL.md** (core workflow):
   - Core workflow instructions
   - Common examples
   - When-to-use guidance
   - Quick reference

2. **Move to REFERENCE.md** (detailed specs):
   - API documentation
   - Detailed parameter lists
   - Comprehensive examples
   - Technical specifications

3. **Move to domain-specific files** (mutually exclusive):
   - Separate workflows (e.g., `AIRFLOW.md`, `PREFECT.md`)
   - Domain-specific deep-dives
   - Large example sets

**Reference pattern**:
```markdown
For detailed API documentation, see `resources/API_REFERENCE.md`.
For Airflow examples, see `resources/AIRFLOW_EXAMPLE.md`.
```

### Table of Contents for Long Files

**Official requirement**: Reference files **longer than 100 lines need a table of contents**.

**Why**: "This ensures Claude can see full scope even with partial reads."

### Context Window Impact

**Official guidance**: "Claude's context window is shared across system prompts, conversation history, other Skills, and user requests."

**Challenge every piece of information**:
- "Does Claude need this explanation?"
- "Can I assume Claude knows this?"

**Example**: Don't explain what PDFs are or how libraries work - assume foundational knowledge.

---

## Code Execution Patterns

### Scripts Should Execute, Not Be Read

**Official pattern**:
```markdown
## Instructions

1. Run the form extraction script:
   ```bash
   python scripts/extract_forms.py input.pdf
   ```
2. Review the output and proceed with form filling.
```

**Official reasoning**: "Large language models excel at many tasks, but certain operations are better suited for traditional code execution."

**Benefits**:
- Saves tokens (code not loaded into context)
- Ensures reliability and consistency ("consistent and repeatable" workflows)
- Avoids generation variability
- Deterministic execution

### When to Include Code in Context

**Only when Claude needs to**:
- Understand code structure for modification
- Learn patterns for generation
- Debug or analyze existing code

**Default**: **Execute, don't read.**

### Pre-Written Scripts: Advantages

**Official guidance**: "Skills can bundle executable code that Claude runs at its discretion."

**Advantages over generated code**:
- More reliable than generated implementations
- Save tokens (no in-context code)
- Save time (no generation required)
- Ensure consistency across executions

**Example from PDF skill**: "Includes pre-written Python scripts that extract form fields without loading the script or document into context."

### Solve Problems, Don't Punt

**Official anti-pattern**: Scripts that fail and ask Claude to fix.

**Better pattern**: Handle errors explicitly:
- Create missing files with defaults instead of FileNotFoundError
- Provide alternatives when access denied
- Include explicit error messages for debugging

**Avoid "voodoo constants"** (Ousterhout's law). Document why values are chosen:
- ✅ "HTTP requests typically complete within 30 seconds; longer timeout accounts for slow connections"
- ❌ "TIMEOUT = 47" (why 47?)

### Validation Before Execution

**Official pattern**: "plan-validate-execute"

1. Claude creates structured plan (JSON file)
2. Validation script checks plan before execution
3. Execute only after validation passes

**Benefit**: "Catches errors early on non-destructive plans rather than after irreversible changes."

### Package Dependencies

**Critical consideration**: List required packages and verify availability.

**Environment constraints**:
- **Claude.ai**: Can install from npm, PyPI, GitHub at runtime
- **Anthropic API**: **No network access**; **no runtime installation**; pre-installed packages only

**Official warning**: "Don't assume packages are installed; include installation steps"

### Visual Analysis for PDFs

**Official recommendation**: "Convert PDFs/images to visual format when layout understanding is critical. Claude's vision can identify fields and structures visually."

---

## Skill Types & Management

### Anthropic-Managed Skills (Pre-Built)

**Four official pre-built skills**:

| Skill ID | Display Title | Purpose |
|----------|---------------|---------|
| `pptx` | PowerPoint | Create presentations, edit slides, analyze content |
| `xlsx` | Excel | Create spreadsheets, analyze data, generate reports |
| `docx` | Word | Create documents, edit content, format text |
| `pdf` | PDF | Generate formatted PDF documents and reports |

**Characteristics**:
- Short IDs: `pptx`, `xlsx`, `docx`, `pdf`
- Date-based versions: `20251013` or `latest`
- Available immediately on Claude API and Claude.ai
- Pre-built and maintained by Anthropic

**Usage pattern**:
```python
container={
    "skills": [{
        "type": "anthropic",
        "skill_id": "pptx",
        "version": "latest"
    }]
}
```

### Custom Skills (User-Created)

**Characteristics**:
- Generated IDs: `skill_01AbCdEfGhIjKlMnOpQrStUv`
- Epoch timestamp versions: `1759178010641129` or `latest`
- Uploaded and managed via Skills API
- Private to workspace

**Upload requirements**:
- Must include SKILL.md at root level
- All files must share common root directory in paths
- Maximum upload: **8MB total**

**Upload methods**:
```python
files_from_dir() helper (Python)
Zip file containing skill structure
Individual file tuples with MIME types
```

### Skill Composition

**Multi-skill usage**: Up to **8 skills per request** enable complex workflows.

**Example**: Combine Excel analysis with PowerPoint creation:
```python
container={
    "skills": [
        {"type": "anthropic", "skill_id": "xlsx", "version": "latest"},
        {"type": "anthropic", "skill_id": "pptx", "version": "latest"}
    ]
}
```

**Official guidance**: "Avoid including unused skills—they impact performance" (metadata loaded for all skills).

### Multi-Turn Conversations

**Pattern**: Reuse containers across messages by specifying container ID.

**Benefit**: Maintains state throughout conversation without re-uploading skills.

---

## Platform Availability

### Where Skills Work

| Platform | Custom Skills | Pre-Built Skills | Network Access | Sharing | Installation |
|----------|---------------|------------------|----------------|---------|--------------|
| **Claude API** | ✅ | ✅ | ❌ No | Workspace-wide | Upload via API |
| **Claude.ai** | ✅ | ✅ | ⚠️ Variable | User-specific | Zip upload |
| **Claude Code** | ✅ | ❌ | ✅ Full | Personal/project | Filesystem |
| **Claude Agent SDK** | ✅ | ❌ | ⚠️ Configurable | Per-agent | Filesystem |

### Installation Paths

**Claude Code**:
- Global: `~/.claude/skills/skill-name/`
- Project: `/path/to/project/.claude/skills/skill-name/`

**Claude Agent SDK**:
- Project: `.claude/skills/skill-name/`
- Enable: Add `"Skill"` to `allowed_tools` in agent config

**Claude API**:
- Upload via Skills API with beta headers:
  - `code-execution-2025-08-25`
  - `skills-2025-10-02`
  - `files-api-2025-04-14`

### Platform-Specific Constraints

**Claude API**:
- **No network access** - can't make external API calls
- **No runtime package installation** - only pre-installed packages
- Fresh container per request

**Claude.ai**:
- Can install packages from npm, PyPI, GitHub at runtime
- Individual user scope - no org-wide admin management

**Claude Code**:
- Full network access and package installation
- Personal or project scope

---

## Best Practices (Official Guidance)

### 1. Start with Evaluation

**Official process**:
1. Run agents on representative tasks
2. Note where they struggle or need extra context
3. Build skills incrementally to address observed gaps

**Anti-pattern**: "Don't build skills speculatively. Build for real needs."

**Official recommendation**: "Create evaluations BEFORE extensive documentation. This prevents documenting imaginary use cases."

**Process**:
1. Identify gaps (run Claude on tasks without Skill; document failures)
2. Create three test scenarios
3. Establish baseline without Skill
4. Write minimal instructions to pass evaluations
5. Iterate and refine

**Key insight**: "Evaluations are your source of truth for Skill effectiveness."

### 2. Structure for Scale

**Keep SKILL.md focused**:
- Core workflow only
- Split large content into referenced files
- Separate mutually exclusive contexts
- Use progressive disclosure

**Official example**:
```
skill-name/
├── SKILL.md              # Core workflow (500 lines)
├── REFERENCE.md          # API docs (1,000 lines)
├── ADVANCED.md           # Advanced patterns (500 lines)
└── scripts/
    └── extract.py        # Executable code
```

**Official guidance**: "Keep mutually exclusive contexts separate to reduce token usage."

### 3. Think from Claude's Perspective

**Monitor real usage**:
- Watch which skills Claude activates
- Note when it fails to activate appropriate skills
- Observe unexpected activation patterns

**Official recommendation**: "Iterate based on observations, not assumptions."

**Observation patterns to watch**:
- **Unexpected paths**: Files read in unanticipated order signals unclear structure
- **Missed connections**: Failed references suggest links aren't prominent enough
- **Overreliance**: Repeated file reads indicate content should move to main SKILL.md
- **Ignored content**: Unused bundled files may be unnecessary or poorly signaled

### 4. Iterate with Claude

**Collaborative development pattern**:
- Ask Claude to capture successful approaches into skill context
- Request self-reflection on failures
- Use Claude to draft skill instructions

**Official pattern**: "If Claude goes off-track, ask it what context would have prevented the mistake."

**Hierarchical development**:
- **Claude A** (expert): Creates and refines the Skill
- **Claude B** (agent): Tests the Skill on real tasks
- **You** (observer): Note where Claude B struggles and report back to Claude A

**Process**:
1. Complete a task normally with Claude A; note what context you repeatedly provide
2. Ask Claude A to create a Skill capturing that pattern
3. Review for conciseness; request better information architecture
4. Test on similar tasks with Claude B
5. Iterate based on Claude B's success/failure patterns

### 5. Code for Determinism

**Prefer executable code over generated code**:
- Use scripts for repetitive, deterministic tasks
- Let Claude generate only when variability is needed
- Execute, don't load into context

**Official statement**: "Certain operations are better suited for traditional code execution."

### 6. Appropriate Freedom Levels

**Match specificity to task fragility**:

- **High freedom** (text instructions): Multiple valid approaches exist; heuristics guide decisions
- **Medium freedom** (pseudocode/scripts with parameters): Preferred patterns exist; some variation acceptable
- **Low freedom** (specific scripts, few parameters): Operations are fragile; consistency critical; exact sequence required

**Official analogy**: "Think of Claude as navigating paths: narrow bridges with cliffs need guardrails; open fields allow exploration."

### 7. Cross-Model Testing

**Official requirement**: "Test Skills with all intended models"

- **Haiku**: Does the Skill provide sufficient guidance?
- **Sonnet**: Is content clear and efficient?
- **Opus**: Avoid over-explaining?

**Official warning**: "What works for Opus may need more detail for Haiku."

### 8. Workflows & Feedback Loops

**Use workflows for complex tasks**: Break operations into clear sequential steps.

**Checklist pattern**:
```markdown
Task Progress:
- [ ] Step 1: Description
- [ ] Step 2: Description
```

**Feedback loop pattern**: Validator → Fix errors → Repeat

**Common approaches**:
- **Style guide compliance**: Draft → Review against checklist → Revise → Re-review
- **Document editing**: Make edits → Validate immediately → Fix issues → Rebuild only when validation passes

**Official benefit**: "Validation loops catch errors early and prevent skipped critical steps."

### 9. Consistent Terminology

**Official requirement**: Choose one term and use it throughout.

**Why**: "Inconsistency confuses Claude"

**Examples**:
- ✅ Pick: API endpoint, field, extract (and use consistently)
- ❌ Not: Mix "endpoint," "URL," "route"; "field," "box," "element"; "extract," "pull," "get"

### 10. Examples and Templates

**Examples pattern**: Provide input/output pairs demonstrating desired format and detail level:
- Show 3+ concrete examples
- Include edge cases
- Demonstrate style and complexity expectations

**Template pattern**:
- **Strict templates** (API responses, data formats): "ALWAYS use this exact structure"
- **Flexible templates** (analysis reports): "Use this sensible default but adapt as needed"

### 11. Conditional Workflows

**Guide through decision points**:
```markdown
1. Determine type:
   Creating new? → Follow "Creation workflow"
   Editing existing? → Follow "Editing workflow"
2. [Details for each path]
```

### 12. Conciseness

**Official principle**: "Challenge every piece of information: 'Does Claude need this explanation?' 'Can I assume Claude knows this?'"

**Example**: Assume foundational knowledge - don't explain what PDFs or libraries are.

**Goal**: ~50 tokens vs. 150 tokens of verbose explanation.

### 13. Avoid Time-Sensitive Information

**Official guidance**: "Don't reference specific dates or version timelines that will become outdated."

**Better pattern**: Use "Old patterns" sections with collapsed details for deprecated approaches.

---

## Anti-Patterns (What to Avoid)

### ❌ Bloated SKILL.md

**Problem**: SKILL.md is 2,000+ lines, exceeding 5k token limit

**Solution**: Split into referenced files

**Official rule**: Keep SKILL.md under 500 lines

### ❌ Reading Code into Context

**Problem**: SKILL.md includes 500 lines of code examples

**Solution**: Move to `scripts/` and execute, or to `REFERENCE.md`

**Official reasoning**: "Code executes deterministically. No need to load it into context."

### ❌ Ambiguous Descriptions

**Problem**: `description: "Helps with forecasting"`

**Solution**: `description: "Generate time series forecasts using TimeGPT and StatsForecast. Use when user needs forecasting, prediction, or time series analysis."`

**Why it matters**: Skill will never trigger if description doesn't match user's natural language.

### ❌ Generic Names

**Problem**: `name: helper`, `name: utils`

**Solution**: `name: timegpt-forecasting`, `name: data-schema-mapper`

**Official guidance**: Use gerund form or action-oriented names

### ❌ Adding Unneeded Frontmatter

**Problem**: Including fields not in official spec (`version`, `license`, `mode`, `allowed-tools`, `model`, `disable-model-invocation`)

**Risk**: May confuse Claude or break compatibility

**Recommendation**: **Stick to official `name` and `description` only**

### ❌ Windows Paths

**Problem**: `scripts\helper.py`

**Solution**: `scripts/helper.py`

**Official rule**: "Use forward slashes only"

### ❌ Too Many Options

**Problem**: "You can use pypdf, pdfplumber, PyMuPDF, pdf2image..."

**Why it fails**: Causes decision paralysis

**Solution**: Provide one default approach; mention alternatives only when necessary

### ❌ Vague Instructions

**Problem**: Generic advice without specific guidance

**Solution**: Clear, actionable steps with specific tools and methods

### ❌ Assumed Tools

**Problem**: Assuming packages are installed

**Solution**: Include installation steps; verify package availability

### ❌ Deeply Nested References

**Problem**: SKILL.md → file1.md → file2.md

**Why it fails**: "Claude may only partially read nested files"

**Solution**: Keep all references one level deep from SKILL.md

### ❌ First or Second Person Descriptions

**Problem**: "I can help you...", "You can use this to..."

**Why it fails**: Descriptions are injected into system prompt

**Solution**: Always use third person: "Processes files and generates reports"

---

## Security Considerations

### Critical Warning

**Official statement**: "We strongly recommend using Skills only from trusted sources: those you created yourself or obtained from Anthropic."

**Risk level**: "Skills provide Claude with new capabilities through instructions and code. While this makes them powerful, it also means that malicious skills may introduce vulnerabilities."

### Audit Checklist

**Before installing a skill**:

- [ ] Review all bundled files (`SKILL.md`, scripts, resources)
- [ ] Check for unusual network calls or data exfiltration attempts
- [ ] Verify tool invocations match stated purpose
- [ ] Inspect scripts for malicious code
- [ ] Validate external URLs (if any) are trustworthy

**Official guidance**: "Treat skill installation like installing software" - it grants Claude new capabilities.

### Vulnerability Vectors

**Malicious skills could**:
- Exfiltrate data via network calls
- Access unauthorized files
- Misuse tools (e.g., Bash for system manipulation)
- Inject instructions that override safety guidelines

---

## Evaluation & Testing

### Build Evaluations First

**Official recommendation**: "Create evaluations BEFORE extensive documentation."

**Why**: "This prevents documenting imaginary use cases."

**Process**:
1. Identify gaps (run Claude without Skill; document failures)
2. Create three test scenarios
3. Establish baseline without Skill
4. Write minimal instructions to pass evaluations
5. Iterate and refine

**Key insight**: "Evaluations are your source of truth for Skill effectiveness."

### Cross-Model Testing

**Official requirement**: Test with Haiku, Sonnet, and Opus

**Questions to ask**:
- **Haiku**: Does the Skill provide sufficient guidance?
- **Sonnet**: Is content clear and efficient?
- **Opus**: Avoid over-explaining?

### Real-World Testing

**Official pattern**: "Continue cycle with real workflows, not test scenarios."

**Testing checklist**:
- [ ] At least three evaluations created
- [ ] Tested with Haiku, Sonnet, Opus
- [ ] Real usage scenarios tested
- [ ] Team feedback incorporated

---

## Evolution & Future Direction

### Current Status

Agent Skills are in active development with full support across:
- Claude.ai
- Claude Code
- Claude Agent SDK
- Claude Developer Platform

### Coming Features

**Announced**:
- Full lifecycle support (create, edit, discover, share, use)
- Complementary integration with Model Context Protocol (MCP)
- Agent-driven skill creation and self-evaluation

### Long-Term Vision

**Official goal**: Enable agents to autonomously:
- Create new skills
- Edit existing skills
- Evaluate skill effectiveness
- Codify behavior patterns into reusable capabilities

**Philosophy**: "Skills as 'executable documentation' that agents can evolve."

---

## Resources

### Official Documentation

- **Claude Platform Docs**: [platform.claude.com/docs/en/agents-and-tools/agent-skills/overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- **Engineering Blog**: [anthropic.com/engineering/equipping-agents-for-the-real-world](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- **Quickstart Guide**: [platform.claude.com/docs/en/agents-and-tools/agent-skills/quickstart](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/quickstart)
- **Best Practices**: [platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- **Skills Building Guide**: [platform.claude.com/docs/en/build-with-claude/skills-guide](https://platform.claude.com/docs/en/build-with-claude/skills-guide)
- **Claude Cookbooks**: Practical skill examples and implementations

### Support

For questions or issues with Agent Skills:
- Claude documentation portal
- Anthropic support channels
- Community forums

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2025-12-03 | 1.0.0 | Initial canonical document created from 2 official sources |
| 2025-12-04 | 2.0.0 | Comprehensive update from ALL 5 official Anthropic sources |

---

## Appendix: Quick Reference Card

### Minimal Skill Structure

```
my-skill/
└── SKILL.md
```

### SKILL.md Template

```yaml
---
name: my-skill-name
description: Does X, Y, Z. Use when [conditions]. Trigger with "phrase 1", "phrase 2".
---

# My Skill Name

## Instructions

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Examples

Example 1: [Description with input/output]
Example 2: [Description with input/output]
```

### Size Limits

| Element | Limit |
|---------|-------|
| `name` | 64 chars |
| `description` | 1,024 chars |
| SKILL.md body | 5,000 tokens (~500 lines recommended) |
| Total upload | 8MB |

### Required Fields (ONLY)

- ✅ `name` (lowercase, hyphens, 64 chars max)
- ✅ `description` (third person, includes "Use when" and trigger phrases)

### Optional Elements

- Additional `.md` files (REFERENCE.md, EXAMPLES.md, etc.)
- `scripts/` directory (executable code)
- `resources/` directory (templates, data files)

### Critical Rules

1. **Descriptions must include**: What it does + "Use when" + trigger phrases
2. **Use third person** in descriptions (injected into system prompt)
3. **Keep SKILL.md under 500 lines** (progressive disclosure)
4. **No custom frontmatter fields** (only `name` and `description`)
5. **Forward slashes only** in file paths
6. **One-level-deep references** (avoid nested files)
7. **Execute code, don't read** (scripts save tokens)
8. **Test with all models** (Haiku, Sonnet, Opus)

### Description Quality Formula

```yaml
description: |
  [Primary capabilities as action verbs].
  [Secondary features with specifics].
  Use when [3-4 explicit trigger scenarios].
  Trigger with "[example phrase 1]", "[example 2]", "[example 3]".
```

---

**Document Status**: Authoritative Reference
**Compliance**: Official Anthropic Standard
**Sources**: 5 official Anthropic documentation pages
**Last Verified**: 2025-12-04
