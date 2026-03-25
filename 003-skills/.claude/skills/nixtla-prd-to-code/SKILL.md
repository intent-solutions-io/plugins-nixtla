---
name: nixtla-prd-to-code
description: "Transform PRD documents into actionable implementation tasks with TodoWrite integration. Use when planning development work, converting requirements to tasks, or creating implementation roadmaps. Trigger with 'PRD to tasks', 'plan implementation from PRD', or 'create task list'."
allowed-tools: "Read,Write,Glob,TodoWrite"
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
compatible-with: claude-code
tags: [nixtla, plugin-development, PRD, task-planning, project-management]
---

# Nixtla PRD to Code

Transform Product Requirements Documents into comprehensive implementation task lists with automatic TodoWrite integration for seamless development planning.

## Overview

This skill bridges the gap between requirements and code. It parses PRD documents to extract functional requirements, non-functional requirements, and technical specifications. It identifies task dependencies and ordering constraints, generates detailed prioritized implementation tasks, integrates with Claude's TodoWrite tool for in-conversation task tracking, and maintains a clear roadmap from idea to working code.

**When to use**: Planning development work from a PRD, converting requirements into actionable tasks, or bootstrapping a project implementation plan with dependency tracking.

**Trigger phrases**: "PRD to tasks", "plan implementation from PRD", "create task list", "convert requirements to tasks", "generate implementation plan".

## Prerequisites

**Required**:
- Python 3.8+
- PRD documents in standardized format (Overview, Functional Requirements, Technical Spec)
- Access to TodoWrite tool in conversation context

**Optional**:
- `pyyaml`: For YAML task list export (install via `pip install pyyaml`)

## Instructions

### Step 1: Identify PRD Document

Locate the PRD file to transform:
```bash
ls 000-docs/000a-planned-plugins/*/02-PRD.md
```

### Step 2: Parse PRD

Execute the PRD parser to extract requirements and generate structured tasks:
```bash
python {baseDir}/scripts/parse_prd.py \
    --prd 000-docs/000a-planned-plugins/implemented/nixtla-roi-calculator/02-PRD.md \
    --output tasks.json
```

### Step 3: Review Generated Tasks

The script generates a structured task list with task titles and descriptions, priority levels (P0, P1, P2), dependencies between tasks, estimated complexity ratings, and implementation notes tied to specific functional requirements.

### Step 4: Populate TodoWrite

Automatically populate Claude's todo list for in-conversation tracking:
```bash
python {baseDir}/scripts/parse_prd.py \
    --prd 000-docs/000a-planned-plugins/implemented/nixtla-roi-calculator/02-PRD.md \
    --populate-todo
```

### Step 5: Begin Implementation

Follow the generated task list in priority order, marking items complete as work progresses. The dependency graph ensures tasks are completed in the correct sequence.

## Output

- **tasks.json**: Structured task list in JSON format with IDs, priorities, and dependencies
- **tasks.yaml**: Human-readable task list (if pyyaml is installed)
- **implementation_plan.md**: Markdown checklist organized by phase and priority for manual tracking
- **TodoWrite integration**: Automatic task population in the active conversation context

## Error Handling

| Error | Solution |
|-------|----------|
| PRD file not found | Verify PRD path in `000-docs/000a-planned-plugins/` directory |
| Missing Functional Requirements section | Ensure PRD has `## Functional Requirements` heading with FR-X items |
| TodoWrite tool not available | TodoWrite only works in conversation context, not standalone script execution |
| Invalid PRD format | PRD must have standard sections: Overview, Goals, Functional Requirements, Technical Spec |
| Circular dependency detected | Review task dependencies and remove circular references (Task A -> B -> A) |

## Examples

See [examples](references/examples.md) for detailed usage patterns including single PRD parsing, TodoWrite auto-population, markdown checklist generation, and batch processing of multiple PRDs.

## Resources

- **PRD Standard**: `000-docs/000a-planned-plugins/README.md` (PRD structure specification)
- **TodoWrite Documentation**: Use `AskUserQuestion` to learn about TodoWrite tool capabilities
- **Task Management**: Beads (`bd` CLI) for advanced task tracking across sessions

**Related Skills**:
- `nixtla-plugin-scaffolder` - Generate plugin structure from PRD
- `nixtla-demo-generator` - Create Jupyter demos for implementation
- `nixtla-test-generator` - Build test suites from PRD requirements

**Scripts**:
- `{baseDir}/scripts/parse_prd.py`: Main PRD parsing and task generation script
- `{baseDir}/assets/templates/task_template.json`: Task structure template
