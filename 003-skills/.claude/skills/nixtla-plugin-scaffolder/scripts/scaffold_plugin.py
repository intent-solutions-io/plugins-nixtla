#!/usr/bin/env python3
"""
Plugin Scaffolder Script

Generates production-ready Claude Code plugin structures from PRD documents.
Creates directory structure, plugin.json, SKILL.md, README, and test files
with enterprise compliance standards.

Usage:
    python scaffold_plugin.py --prd PATH --output DIR [--author NAME] [--license TYPE]

Author: Jeremy Longshore <jeremy@intentsolutions.io>
Version: 1.0.0
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class PRDParser:
    """Parse PRD markdown files and extract plugin metadata."""

    def __init__(self, prd_path: Path):
        self.prd_path = prd_path
        self.content = prd_path.read_text()

    def extract_metadata(self) -> Dict[str, str]:
        """Extract basic plugin metadata from PRD header."""
        metadata = {}

        # Extract plugin name
        plugin_match = re.search(r"\*\*Plugin:\*\*\s+([a-z0-9-]+)", self.content)
        if plugin_match:
            metadata["name"] = plugin_match.group(1)

        # Extract version
        version_match = re.search(r"\*\*Version:\*\*\s+(\d+\.\d+\.\d+)", self.content)
        if version_match:
            metadata["version"] = version_match.group(1)
        else:
            metadata["version"] = "0.1.0"

        # Extract overview (first paragraph after ## Overview)
        overview_match = re.search(
            r"## Overview\s*\n\n(.+?)(?=\n\n---|\n\n##)", self.content, re.DOTALL
        )
        if overview_match:
            metadata["description"] = overview_match.group(1).strip()

        return metadata

    def extract_mcp_tools(self) -> List[Dict[str, str]]:
        """Extract MCP server tools from Functional Requirements."""
        tools = []

        # Look for "MCP Server Tools" or "FR-X: MCP Server Tools" section
        mcp_section_match = re.search(
            r"### (?:FR-\d+:\s*)?MCP Server Tools\s*\n(.+?)(?=\n###|\n---|\Z)",
            self.content,
            re.DOTALL | re.IGNORECASE,
        )

        if mcp_section_match:
            mcp_content = mcp_section_match.group(1)

            # Extract numbered tools (e.g., "1. `tool_name` - Description")
            tool_matches = re.finditer(
                r"\d+\.\s+`([a-z_]+)`\s*-\s*(.+?)(?=\n\d+\.|\Z)", mcp_content, re.DOTALL
            )

            for match in tool_matches:
                tools.append({"name": match.group(1), "description": match.group(2).strip()})

        return tools


class PluginScaffolder:
    """Generate plugin directory structure and files."""

    def __init__(
        self,
        plugin_name: str,
        version: str,
        description: str,
        output_dir: Path,
        author: str = "Jeremy Longshore <jeremy@intentsolutions.io>",
        license_type: str = "MIT",
    ):
        self.plugin_name = plugin_name
        self.version = version
        self.description = description
        self.output_dir = output_dir
        self.author = author
        self.license_type = license_type

    def create_structure(self):
        """Create plugin directory structure."""
        dirs = [
            self.output_dir,
            self.output_dir / ".claude-plugin",
            self.output_dir / "commands",
            self.output_dir / "agents",
            self.output_dir / "skills" / self.plugin_name,
            self.output_dir / "skills" / self.plugin_name / "scripts",
            self.output_dir / "skills" / self.plugin_name / "references",
            self.output_dir / "skills" / self.plugin_name / "assets" / "templates",
            self.output_dir / "tests",
        ]

        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)

        print(f"✓ Created directory structure at {self.output_dir}")

    def _parse_author_object(self) -> Dict[str, str]:
        """
        Convert author string into plugin.json author object.
        Accepts:
          - \"Name <email>\"
          - \"Name\"
        """
        raw = self.author.strip()
        m = re.match(r"^(.*?)\\s*<([^>]+)>\\s*$", raw)
        if m:
            name = m.group(1).strip()
            email = m.group(2).strip()
            out = {"name": name}
            if email:
                out["email"] = email
            return out
        return {"name": raw}

    def generate_plugin_json(self, mcp_tools: List[Dict[str, str]]):
        """Generate .claude-plugin/plugin.json with MCP server configuration."""
        script_name = self.plugin_name.replace("-", "_") + "_mcp_server.py"

        plugin_json = {
            "name": self.plugin_name,
            "version": self.version,
            "description": self.description,
            "author": self._parse_author_object(),
            "license": self.license_type,
            "mcpServers": {
                self.plugin_name: {
                    "command": "python",
                    "args": [f"skills/{self.plugin_name}/scripts/{script_name}"],
                }
            },
        }

        output_path = self.output_dir / ".claude-plugin" / "plugin.json"
        output_path.write_text(json.dumps(plugin_json, indent=2) + "\n")
        print(f"✓ Generated {output_path}")

    def generate_skill_md(self):
        """Generate SKILL.md template."""
        # Create skill description for frontmatter
        skill_description = (
            f"{self.description[:100]}... "
            f"Use when [scenario 1], [scenario 2]. "
            f"Trigger with '{self.plugin_name}' or 'run {self.plugin_name}'."
        )

        purpose = f"Scaffold and operate the {self._title_case(self.plugin_name)} plugin workflows with validated structure and predictable outputs."

        skill_content = f"""---
name: {self.plugin_name}
description: "{skill_description}"
allowed-tools: "Read,Write,Glob,Grep,Edit,Bash(python:*)"
version: "{self.version}"
author: "{self.author}"
license: {self.license_type}
---

# {self._title_case(self.plugin_name)}

{purpose}

## Overview

This skill provides:

- **Feature 1**: Description
- **Feature 2**: Description
- **Feature 3**: Description

## Prerequisites

**Required**:
- Python 3.8+
- Dependencies (install via `pip install -r requirements.txt`)

**Optional**:
- API keys (if applicable)

## Instructions

### Step 1: Preparation

Describe preparation steps here.

### Step 2: Execution

```bash
python {{baseDir}}/scripts/{self.plugin_name.replace('-', '_')}_mcp_server.py
```

### Step 3: Validation

Verify results here.

## Output

- **File 1**: Description
- **File 2**: Description

## Error Handling

1. **Error**: Description
   **Solution**: Fix description

2. **Error**: Description
   **Solution**: Fix description

## Examples

### Example 1: Basic Usage

```python
# Code example
```

### Example 2: Advanced Usage

```python
# Advanced code example
```

## Resources

- **Official Docs**: [Link]
- **Related Skills**: List related skills
- **Scripts**: `{{baseDir}}/scripts/`
"""

        output_path = self.output_dir / "skills" / self.plugin_name / "SKILL.md"
        output_path.write_text(skill_content)
        print(f"✓ Generated {output_path}")

    def generate_readme(self):
        """Generate README.md for plugin."""
        readme_content = f"""# {self._title_case(self.plugin_name)}

{self.description}

## Installation

```bash
# Install via Claude Code plugin manager
claude-code install {self.plugin_name}
```

## Quick Start

```bash
# Example usage
```

## Features

- Feature 1
- Feature 2
- Feature 3

## Configuration

Configure in `.claude-plugin/plugin.json`:

```json
{{
  "mcpServers": {{
    "{self.plugin_name}": {{
      "command": "python",
      "args": ["skills/{self.plugin_name}/scripts/{self.plugin_name.replace('-', '_')}_mcp_server.py"]
    }}
  }}
}}
```

## Development

```bash
# Run tests
pytest tests/

# Run MCP server locally
python skills/{self.plugin_name}/scripts/{self.plugin_name.replace('-', '_')}_mcp_server.py
```

## License

{self.license_type}

## Author

{self.author}
"""

        output_path = self.output_dir / "README.md"
        output_path.write_text(readme_content)
        print(f"✓ Generated {output_path}")

    def generate_mcp_server_stub(self, mcp_tools: List[Dict[str, str]]):
        """Generate MCP server Python stub."""
        script_name = self.plugin_name.replace("-", "_") + "_mcp_server.py"

        # Generate tool function stubs
        tool_functions = []
        for tool in mcp_tools:
            func_name = tool["name"]
            func_desc = tool["description"]
            tool_functions.append(
                f'''
@server.call_tool()
async def {func_name}(arguments: dict) -> list[types.TextContent]:
    """
    {func_desc}

    Args:
        arguments: Tool arguments from Claude Code

    Returns:
        List of text content results
    """
    # TODO: Implement {func_name} logic
    return [types.TextContent(
        type="text",
        text=f"{func_name} executed with args: {{arguments}}"
    )]
'''
            )

        mcp_content = f'''#!/usr/bin/env python3
"""
{self._title_case(self.plugin_name)} MCP Server

MCP server for {self.plugin_name} plugin.

Author: {self.author}
Version: {self.version}
"""

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types


# Initialize MCP server
server = Server("{self.plugin_name}")

{"".join(tool_functions)}

async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
'''

        output_path = self.output_dir / "skills" / self.plugin_name / "scripts" / script_name
        output_path.write_text(mcp_content)
        output_path.chmod(0o755)  # Make executable
        print(f"✓ Generated {output_path}")

    def generate_test_stub(self):
        """Generate pytest test stub."""
        test_name = f"test_{self.plugin_name.replace('-', '_')}.py"

        test_content = f'''"""
Tests for {self.plugin_name}

Author: {self.author}
Version: {self.version}
"""

import pytest
from pathlib import Path


def test_plugin_structure():
    """Test that plugin has required structure."""
    plugin_dir = Path(__file__).parent.parent

    # Check required files exist
    assert (plugin_dir / '.claude-plugin' / 'plugin.json').exists()
    assert (plugin_dir / 'README.md').exists()
    assert (plugin_dir / 'skills' / '{self.plugin_name}' / 'SKILL.md').exists()
    assert (plugin_dir / 'skills' / '{self.plugin_name}' / 'scripts' / '{self.plugin_name.replace('-', '_')}_mcp_server.py').exists()


def test_plugin_json_valid():
    """Test that plugin.json is valid JSON."""
    import json
    plugin_dir = Path(__file__).parent.parent
    plugin_json = plugin_dir / '.claude-plugin' / 'plugin.json'

    with open(plugin_json) as f:
        data = json.load(f)

    assert data['name'] == '{self.plugin_name}'
    assert data['version'] == '{self.version}'
    assert 'mcpServers' in data


# TODO: Add functional tests for MCP tools
'''

        output_path = self.output_dir / "tests" / test_name
        output_path.write_text(test_content)
        print(f"✓ Generated {output_path}")

    def _title_case(self, kebab_name: str) -> str:
        """Convert kebab-case to Title Case."""
        return " ".join(word.capitalize() for word in kebab_name.split("-"))

    def scaffold(self, mcp_tools: List[Dict[str, str]]):
        """Execute full scaffolding process."""
        print(f"\nScaffolding plugin: {self.plugin_name} v{self.version}")
        print(f"Output directory: {self.output_dir}\n")

        self.create_structure()
        self.generate_plugin_json(mcp_tools)
        self.generate_skill_md()
        self.generate_readme()
        self.generate_mcp_server_stub(mcp_tools)
        self.generate_test_stub()

        print(f"\n✓ Plugin scaffold complete!")
        print(f"\nNext steps:")
        print(f"1. Review generated files in {self.output_dir}")
        print(f"2. Implement MCP server logic in skills/{self.plugin_name}/scripts/")
        print(f"3. Expand SKILL.md instructions and examples")
        print(f"4. Add functional tests to tests/")
        print(f"5. Run validator: python 004-scripts/validate_skills_v2.py")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Scaffold Claude Code plugin from PRD document")
    parser.add_argument("--prd", type=Path, required=True, help="Path to PRD markdown file")
    parser.add_argument(
        "--output", type=Path, required=True, help="Output directory for plugin scaffold"
    )
    parser.add_argument(
        "--author",
        default="Jeremy Longshore <jeremy@intentsolutions.io>",
        help="Plugin author (default: Jeremy Longshore)",
    )
    parser.add_argument("--license", default="MIT", help="Plugin license (default: MIT)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing output directory")

    args = parser.parse_args()

    # Validate PRD exists
    if not args.prd.exists():
        print(f"ERROR: PRD file not found: {args.prd}", file=sys.stderr)
        return 1

    # Check output directory
    if args.output.exists() and not args.force:
        print(f"ERROR: Output directory exists: {args.output}", file=sys.stderr)
        print("Use --force to overwrite", file=sys.stderr)
        return 1

    try:
        # Parse PRD
        parser = PRDParser(args.prd)
        metadata = parser.extract_metadata()
        mcp_tools = parser.extract_mcp_tools()

        if "name" not in metadata:
            print("ERROR: Could not extract plugin name from PRD", file=sys.stderr)
            print("Ensure PRD has '**Plugin:** plugin-name' in header", file=sys.stderr)
            return 1

        # Scaffold plugin
        scaffolder = PluginScaffolder(
            plugin_name=metadata["name"],
            version=metadata["version"],
            description=metadata.get("description", "Plugin description"),
            output_dir=args.output,
            author=args.author,
            license_type=args.license,
        )
        scaffolder.scaffold(mcp_tools)

        return 0

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
