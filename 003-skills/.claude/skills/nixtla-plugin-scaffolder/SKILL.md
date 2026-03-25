---
name: nixtla-plugin-scaffolder
description: "Generate production-ready plugin structures from PRD documents with enterprise-compliant files. Use when scaffolding new plugins, converting PRDs to plugin skeletons, or initializing plugin projects. Trigger with 'scaffold plugin', 'create plugin from PRD', or 'initialize plugin structure'."
allowed-tools: "Write,Glob,Read,Bash(mkdir:*)"
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
compatible-with: claude-code
tags: [nixtla, plugin-development, scaffolding, code-generation, PRD]
---

# Nixtla Plugin Scaffolder

Rapidly scaffold production-ready Claude Code plugin structures from PRD documents, generating all required files with enterprise compliance standards.

## Overview

This skill transforms PRD documents into complete plugin scaffolds. It parses PRD metadata, extracts functional requirements and MCP tool definitions, generates the full plugin directory layout, creates enterprise-compliant templates (plugin.json, SKILL.md, README.md, tests), and accelerates development from days to hours.

**When to use**: Starting a new plugin project, converting a PRD into a working plugin skeleton, or batch-generating scaffolds for multiple planned plugins.

**Trigger phrases**: "scaffold plugin", "create plugin from PRD", "initialize plugin structure", "generate plugin skeleton".

## Prerequisites

**Required**:
- Python 3.8+
- PRD documents in `000-docs/000a-planned-plugins/*/02-PRD.md` format
- Write access to target plugin directory

**Optional**:
- `jq`: For JSON validation (install via `apt install jq` or `brew install jq`)

## Instructions

### Step 1: Identify PRD

Locate the PRD document for the plugin to scaffold:
```bash
ls 000-docs/000a-planned-plugins/*/02-PRD.md
```

### Step 2: Run Scaffold Script

Execute the scaffolding script with the PRD path and target output directory:
```bash
python {baseDir}/scripts/scaffold_plugin.py \
    --prd 000-docs/000a-planned-plugins/implemented/nixtla-roi-calculator/02-PRD.md \
    --output 005-plugins/nixtla-roi-calculator
```

### Step 3: Review Generated Files

The script creates a complete plugin structure:
```
005-plugins/nixtla-roi-calculator/
├── plugin.json               # Plugin metadata and configuration
├── README.md                 # Plugin documentation
├── .claude/
│   ├── skills/
│   │   └── nixtla-roi-calculator/
│   │       └── SKILL.md      # Main skill definition
│   ├── commands/             # Slash commands
│   └── agents/               # Custom agents
├── scripts/
│   └── roi_mcp_server.py     # MCP server implementation
└── tests/
    └── test_roi_calculator.py # Test suite
```

### Step 4: Customize Generated Files

Edit the generated files to match specific requirements. Update `plugin.json` for MCP server configurations, expand `SKILL.md` instructions and examples, add plugin-specific documentation to `README.md`, and implement MCP server logic in the scripts directory.

### Step 5: Validate Plugin Structure

Run the plugin validator to ensure compliance with enterprise standards:
```bash
python 004-scripts/validate_skills_v2.py --verbose
```

## Output

- **Complete plugin scaffold** with all required files and directory structure
- **Enterprise-compliant metadata** including author, license, and version fields
- **MCP server template** ready for implementation with tool stubs
- **Test framework** with example tests and fixture patterns
- **Documentation templates** for README and SKILL.md following project conventions

## Error Handling

| Error | Solution |
|-------|----------|
| PRD file not found | Verify PRD path in `000-docs/000a-planned-plugins/` directory |
| Output directory already exists | Use `--force` flag to overwrite or choose different output path |
| Invalid PRD format | Ensure PRD has required sections: Overview, Functional Requirements, MCP Server Tools |
| Permission denied creating directory | Check write permissions on target directory |
| Missing plugin name in PRD | PRD must specify plugin name in header (e.g., `**Plugin:** nixtla-roi-calculator`) |

## Examples

See [examples](references/examples.md) for detailed usage patterns including single plugin scaffolding, batch processing, and custom template overrides.

## Resources

- **Claude Code Plugin Spec**: https://code.claude.com/docs/en/plugins
- **MCP Protocol**: https://modelcontextprotocol.io/
- **Enterprise Plugin Standard**: `000-docs/6767-e-OD-REF-enterprise-plugin-readme-standard.md`
- **Validator v2**: `004-scripts/validate_skills_v2.py`

**Related Skills**:
- `nixtla-prd-to-code` - Transform PRD into implementation tasks
- `nixtla-demo-generator` - Generate Jupyter notebook demos
- `nixtla-test-generator` - Create comprehensive test suites

**Scripts**:
- `{baseDir}/scripts/scaffold_plugin.py`: Main scaffolding script
- `{baseDir}/assets/templates/plugin.json`: Plugin metadata template
- `{baseDir}/assets/templates/skill_template.md`: SKILL.md template
