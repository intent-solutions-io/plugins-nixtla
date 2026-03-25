# MCP Server Builder Examples

## Example 1: Generate Complete MCP Server

```bash
python {baseDir}/scripts/build_mcp_server.py \
    --prd 000-docs/000a-planned-plugins/implemented/nixtla-roi-calculator/02-PRD.md \
    --output 005-plugins/nixtla-roi-calculator/mcp_server \
    --plugin-name nixtla-roi-calculator \
    --verbose
```

**Output**:
```
Parsed PRD: Found 4 MCP tools
  - calculate_roi
  - generate_report
  - compare_scenarios
  - export_salesforce
Generated mcp_server.py (412 lines)
Generated schemas.py (8 Pydantic models)
Generated test_mcp_server.py (16 test functions)
Generated plugin.json
Generated supporting files (README, requirements.txt, .env.example)

Server ready! Start with: python mcp_server.py
```

## Example 2: Dry Run (Preview Without Writing)

Preview generated output counts and file sizes without writing any files.

```bash
python {baseDir}/scripts/build_mcp_server.py \
    --prd PRD.md \
    --output mcp_server/ \
    --dry-run
```

**Output**:
```
[DRY RUN] Would generate:
  - mcp_server/mcp_server.py (estimate: 350 lines)
  - mcp_server/schemas.py (4 tools, 8 models)
  - mcp_server/test_mcp_server.py (12 test functions)
  - mcp_server/plugin.json
  - mcp_server/README.md
  - mcp_server/requirements.txt
  - mcp_server/.env.example
```

## Example 3: Generate Minimal Server (No Tests)

Create a server implementation without the test suite for rapid prototyping.

```bash
python {baseDir}/scripts/build_mcp_server.py \
    --prd PRD.md \
    --output mcp_server/ \
    --no-tests
```

## Example 4: Update Existing Server

Add new tools to an existing MCP server while preserving previous implementations.

```bash
python {baseDir}/scripts/build_mcp_server.py \
    --prd updated_PRD.md \
    --output existing_mcp_server/ \
    --update \
    --backup
```

**Output**:
```
Existing server detected. Creating backup...
Backup created: existing_mcp_server.backup.20251221_223000/
Updated mcp_server.py (added 2 new tools)
Updated schemas.py (added 4 new models)
Updated test_mcp_server.py (added 8 new tests)
```
