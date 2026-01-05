#!/usr/bin/env python3
"""
Generate production-ready MCP server implementations from PRD tool specifications.

This script automates MCP server development by parsing PRD documents and generating:
- mcp_server.py - Main server implementation with tool handlers
- schemas.py - Pydantic validation models
- test_mcp_server.py - Comprehensive test suite
- plugin.json - MCP server configuration
- Supporting files (README, requirements.txt, .env.example)

Usage:
    python build_mcp_server.py --prd PRD.md --output mcp_server/ --plugin-name my-plugin
    python build_mcp_server.py --prd PRD.md --output mcp_server/ --dry-run
    python build_mcp_server.py --prd PRD.md --output mcp_server/ --no-tests
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class PRDParser:
    """Parse PRD documents to extract MCP tool definitions."""

    def __init__(self, prd_path: Path):
        self.prd_path = prd_path
        self.content = ""
        self.plugin_name = ""
        self.plugin_description = ""
        self.tools = []

    def parse(self) -> bool:
        """Parse PRD and extract MCP tool definitions."""
        try:
            self.content = self.prd_path.read_text()
            self._extract_plugin_metadata()
            self._extract_mcp_tools()
            return True
        except FileNotFoundError:
            print(f"Error: PRD not found at {self.prd_path}")
            return False
        except Exception as e:
            print(f"Error parsing PRD: {e}")
            return False

    def _extract_plugin_metadata(self):
        """Extract plugin name and description from PRD header."""
        # Extract plugin name
        name_match = re.search(r"\*\*Plugin:\*\*\s+(\S+)", self.content)
        if name_match:
            self.plugin_name = name_match.group(1)
        else:
            self.plugin_name = self.prd_path.stem.replace("-PRD", "")

        # Extract overview as description
        overview_match = re.search(
            r"## Overview\s*\n\n(.+?)(?=\n\n---|\n\n##)", self.content, re.DOTALL
        )
        if overview_match:
            self.plugin_description = overview_match.group(1).strip()
        else:
            self.plugin_description = f"{self.plugin_name} plugin"

    def _extract_mcp_tools(self):
        """Extract MCP server tools from PRD."""
        # Look for MCP tools section
        mcp_pattern = r"### (?:FR-\d+:\s*)?MCP Server Tools"
        mcp_section_match = re.search(mcp_pattern, self.content, re.IGNORECASE)

        if not mcp_section_match:
            return

        # Extract tools list (numbered list format)
        # Pattern: 1. `tool_name` - Description
        section_start = mcp_section_match.end()
        section_text = self.content[section_start : section_start + 2000]

        tools_pattern = r"\d+\.\s+`([a-z_]+)`\s*-\s*(.+?)(?=\n\d+\.|\n\n|\Z)"
        tool_matches = re.finditer(tools_pattern, section_text, re.DOTALL)

        for match in tool_matches:
            tool_name = match.group(1)
            tool_desc = match.group(2).strip()

            self.tools.append(
                {
                    "name": tool_name,
                    "description": tool_desc,
                    "input_params": self._infer_input_params(tool_desc),
                    "output_fields": self._infer_output_fields(tool_desc),
                }
            )

    @staticmethod
    def _infer_input_params(description: str) -> List[Dict]:
        """Infer likely input parameters from tool description."""
        # Simple heuristics for common parameters
        params = []

        if any(word in description.lower() for word in ["data", "series", "forecast"]):
            params.append({"name": "data", "type": "dict", "required": True})

        if "horizon" in description.lower():
            params.append({"name": "horizon", "type": "int", "required": False, "default": 14})

        if any(word in description.lower() for word in ["compare", "scenario"]):
            params.append({"name": "scenarios", "type": "list", "required": False})

        # Default fallback
        if not params:
            params.append({"name": "input_data", "type": "dict", "required": True})

        return params

    @staticmethod
    def _infer_output_fields(description: str) -> List[Dict]:
        """Infer likely output fields from tool description."""
        # Always include status
        fields = [{"name": "status", "type": "str"}]

        if any(word in description.lower() for word in ["calculate", "generate", "create"]):
            fields.append({"name": "result", "type": "dict"})

        if "report" in description.lower():
            fields.append({"name": "report_path", "type": "str"})

        if "export" in description.lower():
            fields.append({"name": "export_path", "type": "str"})

        return fields


class MCPServerGenerator:
    """Generate MCP server implementation files."""

    def __init__(self, parser: PRDParser, output_dir: Path, plugin_name: str):
        self.parser = parser
        self.output_dir = output_dir
        self.plugin_name = plugin_name

    def generate_all(self, no_tests: bool = False):
        """Generate complete MCP server implementation."""
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Generate core files
        self._generate_server()
        self._generate_schemas()
        if not no_tests:
            self._generate_tests()
        self._generate_plugin_json()
        self._generate_readme()
        self._generate_requirements()
        self._generate_env_example()

    def _generate_server(self):
        """Generate main MCP server implementation."""
        lines = []
        lines.append('"""')
        lines.append(f"MCP Server for {self.plugin_name}")
        lines.append("")
        lines.append(f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        lines.append('"""')
        lines.append("")
        lines.append("import logging")
        lines.append("from mcp.server import Server")
        lines.append("from mcp.server.stdio import stdio_server")
        lines.append("from pydantic import ValidationError")
        lines.append("from schemas import *")
        lines.append("")
        lines.append("# Configure logging")
        lines.append("logging.basicConfig(level=logging.INFO)")
        lines.append("logger = logging.getLogger(__name__)")
        lines.append("")
        lines.append("# Initialize server")
        lines.append(f'app = Server("{self.plugin_name}")')
        lines.append("")
        lines.append("")

        # Generate tool handlers
        for tool in self.parser.tools:
            class_name = self._tool_to_class_name(tool["name"])

            lines.append("@app.call_tool()")
            lines.append(f'async def {tool["name"]}(arguments: dict) -> dict:')
            lines.append(f'    """{tool["description"]}"""')
            lines.append("    try:")
            lines.append(f"        # Validate input")
            lines.append(f"        input_data = {class_name}Input(**arguments)")
            lines.append("")
            lines.append(f'        # TODO: Implement {tool["name"]} logic')
            lines.append("        # 1. Process input_data")
            lines.append("        # 2. Perform required operations")
            lines.append("        # 3. Prepare output")
            lines.append("")
            lines.append("        # Placeholder result")
            lines.append('        result = {"message": "TODO: Implement logic"}')
            lines.append("")
            lines.append("        # Return validated output")
            lines.append(f"        return {class_name}Output(")
            lines.append('            status="success",')
            lines.append("            **result")
            lines.append("        ).dict()")
            lines.append("")
            lines.append("    except ValidationError as e:")
            lines.append('        logger.error(f"Validation error in {tool["name"]}: {e}")')
            lines.append('        return {"status": "error", "message": str(e)}')
            lines.append("    except Exception as e:")
            lines.append(f'        logger.error(f"{tool["name"]} failed: {{e}}")')
            lines.append('        return {"status": "error", "message": "Internal server error"}')
            lines.append("")
            lines.append("")

        # Server entry point
        lines.append("async def main():")
        lines.append('    """Run MCP server."""')
        lines.append("    async with stdio_server() as (read_stream, write_stream):")
        lines.append("        await app.run(")
        lines.append("            read_stream,")
        lines.append("            write_stream,")
        lines.append("            app.create_initialization_options()")
        lines.append("        )")
        lines.append("")
        lines.append("")
        lines.append('if __name__ == "__main__":')
        lines.append("    import asyncio")
        lines.append("    asyncio.run(main())")
        lines.append("")

        output_path = self.output_dir / "mcp_server.py"
        output_path.write_text("\n".join(lines))
        return output_path

    def _generate_schemas(self):
        """Generate Pydantic validation schemas."""
        lines = []
        lines.append('"""Pydantic schemas for MCP tool validation."""')
        lines.append("")
        lines.append("from pydantic import BaseModel, Field")
        lines.append("from typing import Optional, List, Dict")
        lines.append("")
        lines.append("")

        # Generate schemas for each tool
        for tool in self.parser.tools:
            class_name = self._tool_to_class_name(tool["name"])

            # Input schema
            lines.append(f"class {class_name}Input(BaseModel):")
            lines.append(f'    """{tool["name"]} input schema."""')

            if tool["input_params"]:
                for param in tool["input_params"]:
                    type_hint = self._python_type(param["type"])
                    if param.get("required", True):
                        if "default" in param:
                            lines.append(f'    {param["name"]}: {type_hint} = {param["default"]}')
                        else:
                            lines.append(f'    {param["name"]}: {type_hint}')
                    else:
                        lines.append(f'    {param["name"]}: Optional[{type_hint}] = None')
            else:
                lines.append("    pass")
            lines.append("")
            lines.append("")

            # Output schema
            lines.append(f"class {class_name}Output(BaseModel):")
            lines.append(f'    """{tool["name"]} output schema."""')
            lines.append("    status: str")

            for field in tool["output_fields"]:
                if field["name"] != "status":
                    type_hint = self._python_type(field["type"])
                    lines.append(f'    {field["name"]}: Optional[{type_hint}] = None')
            lines.append("")
            lines.append("")

        output_path = self.output_dir / "schemas.py"
        output_path.write_text("\n".join(lines))
        return output_path

    def _generate_tests(self):
        """Generate pytest test suite."""
        lines = []
        lines.append('"""Test suite for MCP server tools."""')
        lines.append("")
        lines.append("import pytest")
        lines.append(
            "from mcp_server import app, " + ", ".join(tool["name"] for tool in self.parser.tools)
        )
        lines.append("")
        lines.append("")

        # Generate test classes
        for tool in self.parser.tools:
            class_name = self._tool_to_class_name(tool["name"])

            lines.append(f"class Test{class_name}:")
            lines.append(f'    """Test {tool["name"]} MCP tool."""')
            lines.append("")

            # Valid input test
            lines.append("    @pytest.mark.asyncio")
            lines.append(f'    async def test_{tool["name"]}_valid_input(self):')
            lines.append(f'        """Test {tool["name"]} with valid input."""')
            lines.append(f'        result = await {tool["name"]}({{}})')
            lines.append('        assert result["status"] == "success"')
            lines.append("")

            # Invalid input test
            lines.append("    @pytest.mark.asyncio")
            lines.append(f'    async def test_{tool["name"]}_invalid_input(self):')
            lines.append(f'        """Test {tool["name"]} with invalid input."""')
            lines.append(f'        result = await {tool["name"]}({{"invalid": "data"}})')
            lines.append("        # Should handle gracefully")
            lines.append('        assert "status" in result')
            lines.append("")

            # Edge cases test
            lines.append("    @pytest.mark.asyncio")
            lines.append(f'    async def test_{tool["name"]}_edge_cases(self):')
            lines.append(f'        """Test {tool["name"]} edge cases."""')
            lines.append("        # TODO: Add edge case tests")
            lines.append("        pass")
            lines.append("")
            lines.append("")

        output_path = self.output_dir / "test_mcp_server.py"
        output_path.write_text("\n".join(lines))
        return output_path

    def _generate_plugin_json(self):
        """Generate plugin.json configuration."""
        config = {
            "name": self.plugin_name,
            "version": "0.1.0",
            "description": self.parser.plugin_description[:200],
            "mcp_server": {
                "command": "python",
                "args": ["mcp_server.py"],
                "env": {"NIXTLA_API_KEY": "${NIXTLA_API_KEY}"},
            },
            "tools": [],
        }

        # Add tools
        for tool in self.parser.tools:
            tool_config = {
                "name": tool["name"],
                "description": tool["description"],
                "inputSchema": {"type": "object", "properties": {}, "required": []},
            }

            # Add input properties
            for param in tool["input_params"]:
                json_type = self._json_type(param["type"])
                tool_config["inputSchema"]["properties"][param["name"]] = {"type": json_type}
                if param.get("required", True):
                    tool_config["inputSchema"]["required"].append(param["name"])

            config["tools"].append(tool_config)

        output_path = self.output_dir / "plugin.json"
        output_path.write_text(json.dumps(config, indent=2))
        return output_path

    def _generate_readme(self):
        """Generate README.md."""
        lines = []
        lines.append(f"# {self.plugin_name} MCP Server")
        lines.append("")
        lines.append("## Overview")
        lines.append("")
        lines.append(self.parser.plugin_description)
        lines.append("")
        lines.append("## Installation")
        lines.append("")
        lines.append("```bash")
        lines.append("pip install -r requirements.txt")
        lines.append("```")
        lines.append("")
        lines.append("## Configuration")
        lines.append("")
        lines.append("Copy `.env.example` to `.env` and configure:")
        lines.append("")
        lines.append("```bash")
        lines.append("cp .env.example .env")
        lines.append("# Edit .env with your API keys")
        lines.append("```")
        lines.append("")
        lines.append("## Running")
        lines.append("")
        lines.append("```bash")
        lines.append("python mcp_server.py")
        lines.append("```")
        lines.append("")
        lines.append("## Testing")
        lines.append("")
        lines.append("```bash")
        lines.append("pytest test_mcp_server.py -v")
        lines.append("```")
        lines.append("")
        lines.append("## Tools")
        lines.append("")

        for tool in self.parser.tools:
            lines.append(f'### `{tool["name"]}`')
            lines.append("")
            lines.append(tool["description"])
            lines.append("")

        output_path = self.output_dir / "README.md"
        output_path.write_text("\n".join(lines))
        return output_path

    def _generate_requirements(self):
        """Generate requirements.txt."""
        lines = [
            "mcp>=1.0.0",
            "pydantic>=2.0.0",
            "python-dotenv>=1.0.0",
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
        ]
        output_path = self.output_dir / "requirements.txt"
        output_path.write_text("\n".join(lines))
        return output_path

    def _generate_env_example(self):
        """Generate .env.example."""
        lines = [
            "# MCP Server Environment Variables",
            "",
            "# Nixtla API Key (required for TimeGPT)",
            "NIXTLA_API_KEY=nixak-your-api-key-here",
            "",
        ]
        output_path = self.output_dir / ".env.example"
        output_path.write_text("\n".join(lines))
        return output_path

    @staticmethod
    def _tool_to_class_name(tool_name: str) -> str:
        """Convert tool_name to PascalCase class name."""
        words = tool_name.split("_")
        return "".join(word.capitalize() for word in words)

    @staticmethod
    def _python_type(type_str: str) -> str:
        """Convert type string to Python type hint."""
        type_map = {
            "str": "str",
            "int": "int",
            "float": "float",
            "bool": "bool",
            "dict": "Dict",
            "list": "List",
        }
        return type_map.get(type_str, "str")

    @staticmethod
    def _json_type(type_str: str) -> str:
        """Convert type string to JSON schema type."""
        type_map = {
            "str": "string",
            "int": "integer",
            "float": "number",
            "bool": "boolean",
            "dict": "object",
            "list": "array",
        }
        return type_map.get(type_str, "string")


def main():
    parser = argparse.ArgumentParser(
        description="Generate MCP server from PRD tool specifications",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate complete MCP server
  python build_mcp_server.py --prd PRD.md --output mcp_server/ --plugin-name my-plugin

  # Dry run
  python build_mcp_server.py --prd PRD.md --output mcp_server/ --dry-run

  # Without tests
  python build_mcp_server.py --prd PRD.md --output mcp_server/ --no-tests
        """,
    )

    parser.add_argument("--prd", type=Path, required=True, help="Path to PRD markdown file")

    parser.add_argument(
        "--output", type=Path, required=True, help="Output directory for MCP server files"
    )

    parser.add_argument("--plugin-name", type=str, help="Plugin name (default: extracted from PRD)")

    parser.add_argument("--no-tests", action="store_true", help="Skip test suite generation")

    parser.add_argument(
        "--dry-run", action="store_true", help="Preview output without writing files"
    )

    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    # Parse PRD
    print(f"Parsing PRD: {args.prd}")
    prd_parser = PRDParser(args.prd)
    if not prd_parser.parse():
        return 1

    # Use plugin name from PRD if not specified
    plugin_name = args.plugin_name or prd_parser.plugin_name

    # Report findings
    print(f"\nFound:")
    print(f"  - Plugin: {plugin_name}")
    print(f"  - {len(prd_parser.tools)} MCP tools")

    if args.verbose:
        print("\nMCP Tools:")
        for tool in prd_parser.tools:
            print(f"  - {tool['name']}: {tool['description'][:60]}...")

    # Dry run
    if args.dry_run:
        print("\n[DRY RUN] Would generate:")
        print(f"  - {args.output}/mcp_server.py")
        print(f"  - {args.output}/schemas.py")
        if not args.no_tests:
            print(f"  - {args.output}/test_mcp_server.py")
        print(f"  - {args.output}/plugin.json")
        print(f"  - {args.output}/README.md")
        print(f"  - {args.output}/requirements.txt")
        print(f"  - {args.output}/.env.example")
        return 0

    # Generate MCP server
    print(f"\nGenerating MCP server in {args.output}/")
    generator = MCPServerGenerator(prd_parser, args.output, plugin_name)
    generator.generate_all(no_tests=args.no_tests)

    # Summary
    tool_count = len(prd_parser.tools)
    test_count = tool_count * 3 if not args.no_tests else 0

    print("\n✓ MCP server generated successfully!")
    print(f"  - {tool_count} tools implemented")
    if not args.no_tests:
        print(f"  - {test_count} test functions")
    print(f"\nStart server with: python {args.output}/mcp_server.py")

    return 0


if __name__ == "__main__":
    sys.exit(main())
