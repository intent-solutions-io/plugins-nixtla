# MCP Server Template Reference

## Main Server Implementation (mcp_server.py)

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from pydantic import BaseModel

# Tool schemas
class ToolNameInput(BaseModel):
    param1: str
    param2: int = 14

class ToolNameOutput(BaseModel):
    status: str
    result: dict

# Server initialization
app = Server("plugin-name")

@app.call_tool()
async def tool_name(arguments: dict) -> dict:
    """Tool description from PRD"""
    input_data = ToolNameInput(**arguments)
    result = {"data": "placeholder"}
    return ToolNameOutput(status="success", result=result).dict()
```

## Tool Handler Template

```python
@app.call_tool()
async def calculate_roi(arguments: dict) -> dict:
    """Calculate ROI comparing TimeGPT vs. build-in-house."""
    try:
        input_data = CalculateRoiInput(**arguments)

        # TODO: Implement ROI calculation logic
        # 1. Parse input parameters
        # 2. Calculate 5-year TCO
        # 3. Generate comparison metrics

        result = {
            "roi": 245.0,
            "payback_months": 6,
            "total_savings": 500000
        }

        return CalculateRoiOutput(
            status="success",
            roi_percentage=result["roi"],
            details=result
        ).dict()

    except ValidationError as e:
        return {"status": "error", "message": str(e)}
    except Exception as e:
        logging.error(f"calculate_roi failed: {e}")
        return {"status": "error", "message": "Internal server error"}
```

## Schema Validation (schemas.py)

```python
from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class CalculateRoiInput(BaseModel):
    """Input schema for calculate_roi tool."""
    current_infrastructure_cost: float = Field(..., description="Annual cost in USD")
    forecast_volume: int = Field(..., description="Number of series to forecast")
    team_size: int = Field(default=0, description="Current data science team size")

class CalculateRoiOutput(BaseModel):
    """Output schema for calculate_roi tool."""
    status: str
    roi_percentage: float
    payback_months: int
    details: Dict
```

## Server Configuration (plugin.json)

```json
{
  "name": "nixtla-plugin-name",
  "version": "0.1.0",
  "description": "Plugin description from PRD",
  "mcp_server": {
    "command": "python",
    "args": ["mcp_server.py"],
    "env": { "NIXTLA_API_KEY": "${NIXTLA_API_KEY}" }
  },
  "tools": [
    {
      "name": "calculate_roi",
      "description": "Calculate ROI comparing TimeGPT vs. build-in-house",
      "inputSchema": {
        "type": "object",
        "properties": {
          "current_infrastructure_cost": {"type": "number"},
          "forecast_volume": {"type": "integer"}
        },
        "required": ["current_infrastructure_cost", "forecast_volume"]
      }
    }
  ]
}
```

## Test Suite Template (test_mcp_server.py)

```python
import pytest
from mcp_server import app, calculate_roi

class TestCalculateRoiTool:
    """Test calculate_roi MCP tool."""

    @pytest.mark.asyncio
    async def test_valid_input(self):
        result = await calculate_roi({
            "current_infrastructure_cost": 100000,
            "forecast_volume": 1000,
            "team_size": 5
        })
        assert result["status"] == "success"
        assert "roi_percentage" in result

    @pytest.mark.asyncio
    async def test_invalid_input(self):
        result = await calculate_roi({})
        assert result["status"] == "error"

    @pytest.mark.asyncio
    async def test_edge_cases(self):
        result = await calculate_roi({
            "current_infrastructure_cost": 0,
            "forecast_volume": 1000000
        })
        assert result["status"] == "success"
```

## Deployment Files

**requirements.txt**:
```
mcp>=1.0.0
pydantic>=2.0.0
python-dotenv>=1.0.0
```

**.env.example**:
```bash
NIXTLA_API_KEY=nixak-your-api-key-here
```

## Generated Directory Structure

```
mcp_server/
├── mcp_server.py          # Main server
├── schemas.py             # Validation schemas
├── test_mcp_server.py     # Tests
├── plugin.json            # Configuration
├── requirements.txt       # Dependencies
├── README.md              # Documentation
└── .env.example           # Environment template
```
