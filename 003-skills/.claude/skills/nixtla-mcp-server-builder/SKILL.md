---
name: nixtla-mcp-server-builder
description: "Generate production-ready MCP server implementations from PRD tool specifications with schema validation, error handling, and testing infrastructure. Use when building MCP servers for Nixtla plugins, implementing tool handlers, or scaffolding server infrastructure. Trigger with 'build MCP server', 'generate MCP implementation', or 'scaffold MCP tools'."
allowed-tools: "Write,Read,Glob,Bash(python:*),Bash(mkdir:*)"
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
compatible-with: claude-code
tags: [nixtla, MCP, server-development, code-generation, plugin-development]
---

# Nixtla MCP Server Builder

Generate complete, production-ready MCP (Model Context Protocol) server implementations from PRD tool specifications, enabling rapid development of Claude Code plugin backends.

## Overview

This skill automates MCP server development by parsing PRD documents to extract MCP tool definitions, generating Python server implementations with async tool handlers, creating Pydantic input/output schema validation, implementing error handling and logging, generating test suites for all tools, and scaffolding deployment infrastructure (requirements.txt, .env.example, README).

**When to use**: Building a new MCP server backend for a Nixtla plugin, adding tool handlers to an existing server, or scaffolding the complete server infrastructure from a PRD specification.

**Trigger phrases**: "build MCP server", "generate MCP implementation", "scaffold MCP tools", "create tool handlers", "MCP server from PRD".

**Key Benefits**:
- Reduces MCP server development time from 6-8 hours to 10 minutes
- Ensures consistent server architecture across all plugins
- Auto-generates boilerplate code (validators, error handlers, tests)
- Implements MCP specification best practices

## Prerequisites

- PRD document with MCP Server Tools section (FR-X format)
- Python 3.10+ installed
- MCP SDK (`pip install mcp`)
- Pydantic for schema validation (`pip install pydantic`)

**Expected PRD Structure**:
```markdown
## Functional Requirements

### FR-X: MCP Server Tools
Expose N tools to Claude Code:
1. `tool_name` - Tool description
2. `another_tool` - Another description
```

## Instructions

### Step 1: Parse PRD for Tool Definitions

The script reads the PRD markdown file, extracts MCP tool names and descriptions, infers input/output schemas from tool descriptions, and generates Pydantic models for validation.

```bash
python {baseDir}/scripts/build_mcp_server.py \
    --prd /path/to/PRD.md \
    --output /path/to/mcp_server/ \
    --plugin-name nixtla-plugin-name
```

### Step 2: Generate Server Implementation

The builder creates a complete MCP server with async/await support, Pydantic schema validation, type hints, docstrings from PRD descriptions, structured error handling, and logging for debugging.

See [server template reference](references/server-template.md) for the generated code patterns including main server, tool handlers, schemas, plugin.json, and test suite templates.

### Step 3: Customize Tool Handlers

For each tool, the generator creates a handler stub with input validation (Pydantic model), TODO comments marking where to implement business logic, output schema enforcement, and error handling templates. Replace the placeholder logic with actual implementation.

### Step 4: Run Generated Tests

Execute the test suite to verify server functionality:

```bash
pytest test_mcp_server.py -v
```

### Step 5: Deploy

Start the server using the generated configuration:

```bash
python mcp_server.py
```

## Output

The script generates 7 files in the output directory:

1. **mcp_server.py** - Main server implementation (200-500 lines depending on tool count)
2. **schemas.py** - Pydantic validation models for all tool inputs and outputs
3. **test_mcp_server.py** - Comprehensive async test suite with valid, invalid, and edge case tests
4. **plugin.json** - MCP server configuration with tool schemas
5. **requirements.txt** - Python dependencies (mcp, pydantic, python-dotenv)
6. **README.md** - Server documentation with installation and run instructions
7. **.env.example** - Environment variable template

## Error Handling

| Error | Solution |
|-------|----------|
| PRD not found | Verify PRD path and ensure file exists |
| No MCP tools found | Ensure PRD has `### FR-X: MCP Server Tools` section |
| Invalid tool definition | Ensure all tools have format: `` `tool_name` - Description `` |
| Server startup failure | Check port availability and verify dependencies are installed |

## Best Practices

1. **Review generated code** and customize tool handlers before deploying.
2. **Replace TODO logic** with actual implementation for each tool.
3. **Run the pytest suite** before deploying to catch validation issues.
4. **Use Pydantic models** to catch type errors at the tool boundary.
5. **Never hardcode API keys** in server code; use .env files and environment variables.

## Examples

See [examples](references/examples.md) for detailed usage patterns including complete server generation, dry run previews, minimal server (no tests), and updating existing servers.

See [server template reference](references/server-template.md) for generated code patterns and the complete directory structure.

## Resources

- **Script**: `{baseDir}/scripts/build_mcp_server.py`
- **Template**: `{baseDir}/assets/templates/mcp_server_template.py`
- **Example Server**: `{baseDir}/references/EXAMPLE_MCP_SERVER.py`
- **MCP Specification**: https://modelcontextprotocol.io/
- **Pydantic Docs**: https://docs.pydantic.dev/
- **MCP Python SDK**: https://github.com/modelcontextprotocol/python-sdk

**Related Skills**:
- `nixtla-plugin-scaffolder` - Generate complete plugin structure from PRD
- `nixtla-test-generator` - Create comprehensive test suites from PRD
