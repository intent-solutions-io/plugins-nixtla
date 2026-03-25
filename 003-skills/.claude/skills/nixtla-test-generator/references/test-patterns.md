# Test Generator Patterns and Templates

## Generated Test Structure

### test_unit.py - Unit tests for individual functions
```python
import pytest
from plugin_name.core import function_name

class TestFR1FeatureName:
    """Test FR-1: Feature Name"""

    def test_basic_functionality(self):
        """Test basic happy path for FR-1"""
        result = function_name(input_data)
        assert result.success

    def test_error_handling(self):
        """Test error handling for FR-1"""
        with pytest.raises(ValueError):
            function_name(invalid_input)
```

### test_integration.py - Integration tests for MCP tools
```python
import pytest
from mcp_server import ToolName

class TestMCPToolName:
    """Test MCP tool: tool_name"""

    @pytest.mark.integration
    def test_tool_execution(self, mock_api_client):
        """Test tool_name MCP tool end-to-end"""
        result = ToolName.execute(params)
        assert result["status"] == "success"
```

### conftest.py - Shared fixtures
```python
import pytest

@pytest.fixture
def sample_data():
    """Provide sample test data"""
    return {"series": [...], "horizon": 14}

@pytest.fixture
def mock_api_client(monkeypatch):
    """Mock external API calls"""
    class MockClient:
        def forecast(self, **kwargs):
            return {"predictions": [...]}
    return MockClient()
```

## Coverage Matrix Template

The generated `tests/COVERAGE_MATRIX.md` maps each test function back to its PRD requirement:

| Requirement | Test File | Test Function | Status |
|-------------|-----------|---------------|--------|
| FR-1: Feature Name | test_unit.py | test_basic_functionality | Covered |
| FR-2: Another Feature | test_unit.py | test_feature_2 | Covered |
| MCP: tool_name | test_integration.py | test_tool_execution | Covered |

## Pytest Markers

Generated tests include appropriate markers for selective execution:
- `@pytest.mark.unit` - Fast, isolated tests (< 100ms each)
- `@pytest.mark.integration` - Tests with external dependencies
- `@pytest.mark.slow` - Long-running tests (> 1 second)
- `@pytest.mark.parametrize` - Multiple input scenarios

## Best Practices

1. **Review generated tests** and customize placeholder assertions with actual validation logic.
2. **Add real assertions** to replace generic `assert result.success` patterns.
3. **Mock external APIs** using fixtures to avoid hitting TimeGPT or BigQuery in tests.
4. **Parameterize edge cases** with `@pytest.mark.parametrize` for boundary conditions.
5. **Document test intent** by keeping docstrings that explain what each test validates.
6. **Run tests locally** before committing to verify they pass.
7. **Track coverage** and aim for 80%+ code coverage on core logic.
