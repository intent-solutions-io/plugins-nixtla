#!/usr/bin/env python3
"""MCP Server for Nixtla ROI Calculator.

Exposes 4 tools:
- calculate_roi: Run ROI calculation with inputs
- generate_report: Create PDF/PowerPoint report
- compare_scenarios: Compare build vs buy approaches
- export_salesforce: Export to Salesforce format
"""

import json
from dataclasses import dataclass
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

app = Server("nixtla-roi-calculator")


@dataclass
class ROIInputs:
    """ROI calculation inputs."""
    current_tool_cost: float = 0.0
    fte_hours_per_week: float = 0.0
    fte_hourly_rate: float = 75.0
    infrastructure_cost: float = 0.0
    forecast_volume_monthly: int = 1000
    timegpt_price_per_1k: float = 0.10


def calculate_roi_internal(inputs: ROIInputs) -> dict[str, Any]:
    """Calculate 3-year ROI comparison."""
    # Current annual costs
    current_tool_annual = inputs.current_tool_cost * 12
    current_fte_annual = inputs.fte_hours_per_week * 52 * inputs.fte_hourly_rate
    current_infra_annual = inputs.infrastructure_cost * 12
    current_total_annual = current_tool_annual + current_fte_annual + current_infra_annual

    # TimeGPT annual costs
    timegpt_annual = (inputs.forecast_volume_monthly * 12 * inputs.timegpt_price_per_1k) / 1000
    timegpt_fte_reduction = 0.7  # 70% reduction in FTE time
    timegpt_fte_annual = current_fte_annual * (1 - timegpt_fte_reduction)
    timegpt_total_annual = timegpt_annual + timegpt_fte_annual

    # ROI calculation
    annual_savings = current_total_annual - timegpt_total_annual
    roi_percentage = (annual_savings / current_total_annual) * 100 if current_total_annual > 0 else 0
    payback_months = 1 if annual_savings > 0 else float('inf')

    return {
        "current_costs": {
            "tool_annual": current_tool_annual,
            "fte_annual": current_fte_annual,
            "infrastructure_annual": current_infra_annual,
            "total_annual": current_total_annual,
            "total_3year": current_total_annual * 3
        },
        "timegpt_costs": {
            "api_annual": timegpt_annual,
            "fte_annual": timegpt_fte_annual,
            "total_annual": timegpt_total_annual,
            "total_3year": timegpt_total_annual * 3
        },
        "savings": {
            "annual": annual_savings,
            "3year": annual_savings * 3,
            "roi_percentage": roi_percentage,
            "payback_months": payback_months
        }
    }


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available ROI calculator tools."""
    return [
        Tool(
            name="calculate_roi",
            description="Calculate TimeGPT ROI based on current costs",
            inputSchema={
                "type": "object",
                "properties": {
                    "current_tool_cost": {"type": "number", "description": "Monthly tool/license cost"},
                    "fte_hours_per_week": {"type": "number", "description": "Data scientist hours/week on forecasting"},
                    "fte_hourly_rate": {"type": "number", "description": "Hourly rate (default: $75)"},
                    "infrastructure_cost": {"type": "number", "description": "Monthly infrastructure cost"},
                    "forecast_volume_monthly": {"type": "integer", "description": "Monthly forecast API calls"}
                },
                "required": ["current_tool_cost", "forecast_volume_monthly"]
            }
        ),
        Tool(
            name="generate_report",
            description="Generate PDF/PowerPoint ROI report",
            inputSchema={
                "type": "object",
                "properties": {
                    "roi_data": {"type": "object", "description": "ROI calculation results"},
                    "format": {"type": "string", "enum": ["pdf", "pptx"], "description": "Output format"},
                    "output_path": {"type": "string", "description": "Output file path"}
                },
                "required": ["roi_data", "format"]
            }
        ),
        Tool(
            name="compare_scenarios",
            description="Compare build vs buy scenarios",
            inputSchema={
                "type": "object",
                "properties": {
                    "scenarios": {"type": "array", "items": {"type": "string"}, "description": "Scenarios to compare"}
                },
                "required": ["scenarios"]
            }
        ),
        Tool(
            name="export_salesforce",
            description="Export ROI data to Salesforce opportunity format",
            inputSchema={
                "type": "object",
                "properties": {
                    "roi_data": {"type": "object", "description": "ROI calculation results"},
                    "opportunity_name": {"type": "string", "description": "Salesforce opportunity name"}
                },
                "required": ["roi_data", "opportunity_name"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Execute ROI calculator tool."""
    if name == "calculate_roi":
        inputs = ROIInputs(
            current_tool_cost=arguments.get("current_tool_cost", 0),
            fte_hours_per_week=arguments.get("fte_hours_per_week", 0),
            fte_hourly_rate=arguments.get("fte_hourly_rate", 75),
            infrastructure_cost=arguments.get("infrastructure_cost", 0),
            forecast_volume_monthly=arguments.get("forecast_volume_monthly", 1000)
        )
        result = calculate_roi_internal(inputs)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "generate_report":
        # Placeholder - would use reportlab/python-pptx
        return [TextContent(type="text", text="Report generation not yet implemented")]

    elif name == "compare_scenarios":
        scenarios = arguments.get("scenarios", [])
        return [TextContent(type="text", text=f"Comparing scenarios: {', '.join(scenarios)}")]

    elif name == "export_salesforce":
        return [TextContent(type="text", text="Salesforce export not yet implemented")]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
