#!/usr/bin/env python3
"""
Changelog Automation MCP Server

Exposes 6 tools for changelog generation:
1. fetch_changelog_data - Fetch data from GitHub/Slack/Git
2. validate_frontmatter - Validate YAML frontmatter against schema
3. write_changelog - Write changelog to file with safety checks
4. create_changelog_pr - Create GitHub PR with changelog
5. validate_changelog_quality - Run deterministic quality checks
6. get_changelog_config - Load and validate config file
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# MCP imports
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

# Version for reproducibility
VERSION = "0.1.0"


class ChangelogMCPServer:
    """MCP server for changelog automation tools."""

    def __init__(self):
        self.server = Server("changelog-mcp")
        self.setup_tools()

    def setup_tools(self):
        """Register all MCP tools."""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List available tools."""
            return [
                Tool(
                    name="fetch_changelog_data",
                    description="Fetch structured data from configured sources (GitHub/Slack/Git)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "source_type": {
                                "type": "string",
                                "enum": ["github", "slack", "git"],
                                "description": "Data source type",
                            },
                            "start_date": {
                                "type": "string",
                                "description": "Start date (ISO 8601 format: YYYY-MM-DD)",
                            },
                            "end_date": {
                                "type": "string",
                                "description": "End date (ISO 8601 format: YYYY-MM-DD)",
                            },
                            "config": {
                                "type": "object",
                                "description": "Source-specific configuration",
                            },
                        },
                        "required": ["source_type", "start_date", "end_date", "config"],
                    },
                ),
                Tool(
                    name="validate_frontmatter",
                    description="Validate YAML frontmatter against JSON Schema",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "frontmatter": {
                                "type": "object",
                                "description": "YAML frontmatter as dictionary",
                            },
                            "schema_path": {
                                "type": "string",
                                "description": "Path to JSON Schema (optional)",
                            },
                        },
                        "required": ["frontmatter"],
                    },
                ),
                Tool(
                    name="get_changelog_config",
                    description="Load and validate .changelog-config.json",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "config_path": {
                                "type": "string",
                                "description": "Path to config file (default: .changelog-config.json)",
                            }
                        },
                    },
                ),
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """Handle tool invocations."""
            try:
                if name == "fetch_changelog_data":
                    result = await self.fetch_changelog_data(**arguments)
                elif name == "validate_frontmatter":
                    result = await self.validate_frontmatter(**arguments)
                elif name == "get_changelog_config":
                    result = await self.get_changelog_config(**arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")

                return [TextContent(type="text", text=json.dumps(result, indent=2))]

            except Exception as e:
                error_result = {"status": "error", "error": str(e), "tool": name}
                return [TextContent(type="text", text=json.dumps(error_result, indent=2))]

    async def fetch_changelog_data(
        self, source_type: str, start_date: str, end_date: str, config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Fetch structured data from configured sources.

        Args:
            source_type: One of "github", "slack", "git"
            start_date: ISO 8601 date (YYYY-MM-DD)
            end_date: ISO 8601 date (YYYY-MM-DD)
            config: Source-specific configuration

        Returns:
            {
                "status": "success",
                "data": {
                    "items": [...],
                    "count": int,
                    "source": str,
                    "date_range": str
                }
            }
        """
        # TODO: Implement data source fetching (Week 2)
        # For now, return mock data for testing
        return {
            "status": "success",
            "data": {
                "items": [
                    {
                        "id": "mock-1",
                        "title": "Example change",
                        "type": "feature",
                        "author": "test@example.com",
                        "labels": ["enhancement"],
                        "url": "https://example.com/pr/1",
                        "timestamp": start_date,
                    }
                ],
                "count": 1,
                "source": source_type,
                "date_range": f"{start_date} to {end_date}",
            },
            "version": VERSION,
            "timestamp": datetime.utcnow().isoformat(),
        }

    async def validate_frontmatter(
        self, frontmatter: Dict[str, Any], schema_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Validate YAML frontmatter against JSON Schema.

        Args:
            frontmatter: YAML frontmatter as dictionary
            schema_path: Path to JSON Schema (optional)

        Returns:
            {
                "status": "success",
                "valid": bool,
                "errors": [...],
                "warnings": [...]
            }
        """
        # TODO: Implement JSON Schema validation (Week 1)
        # For now, basic validation
        required_fields = ["date", "version"]
        errors = []
        warnings = []

        for field in required_fields:
            if field not in frontmatter:
                errors.append(f"Missing required field: {field}")

        optional_fields = ["authors", "categories"]
        for field in optional_fields:
            if field not in frontmatter:
                warnings.append(f"Optional field '{field}' not provided")

        return {
            "status": "success",
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "version": VERSION,
        }

    async def get_changelog_config(
        self, config_path: str = ".changelog-config.json"
    ) -> Dict[str, Any]:
        """
        Load and validate .changelog-config.json.

        Args:
            config_path: Path to config file

        Returns:
            {
                "status": "success",
                "config": {...},
                "validation": {
                    "valid": bool,
                    "errors": [...]
                }
            }
        """
        try:
            # Resolve path relative to current working directory
            config_file = Path(config_path)

            if not config_file.exists():
                return {
                    "status": "error",
                    "error": f"Config file not found: {config_path}",
                    "suggestion": "Run /changelog-validate to create example config",
                }

            # Load config
            with open(config_file, "r") as f:
                config = json.load(f)

            # TODO: Validate against JSON Schema (Week 1)
            # For now, basic validation
            required_fields = ["sources", "template", "output_path"]
            errors = []

            for field in required_fields:
                if field not in config:
                    errors.append(f"Missing required field: {field}")

            return {
                "status": "success",
                "config": config,
                "validation": {"valid": len(errors) == 0, "errors": errors},
                "version": VERSION,
                "config_path": str(config_file.absolute()),
            }

        except json.JSONDecodeError as e:
            return {
                "status": "error",
                "error": f"Invalid JSON in config file: {e}",
                "config_path": config_path,
            }

    async def run(self):
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream, write_stream, self.server.create_initialization_options()
            )


def main():
    """Main entry point."""
    server = ChangelogMCPServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
