# Nixtla Migration Assistant

Automated migration from Prophet/statsmodels to Nixtla.

## Features

- **Code Analysis**: AST-based pattern detection
- **Data Transformation**: Convert to Nixtla format
- **Code Generation**: Generate equivalent Nixtla code
- **Accuracy Comparison**: Side-by-side metrics

## Quick Start

```bash
pip install -r scripts/requirements.txt

# In Claude Code:
/nixtla-migrate path/to/prophet_model.py --target=timegpt
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `analyze_code` | Detect forecasting patterns |
| `generate_plan` | Create migration plan |
| `transform_data` | Convert data format |
| `generate_code` | Generate Nixtla code |
| `compare_accuracy` | Side-by-side comparison |

## Supported Migrations

| Source | Target | Support |
|--------|--------|---------|
| Prophet | TimeGPT | Full |
| Prophet | StatsForecast | Full |
| statsmodels ARIMA | StatsForecast | Full |
| statsmodels ETS | StatsForecast | Full |
| sklearn | StatsForecast | Partial |

## Safety Features

- Read-only analysis (never modifies original)
- Dry-run mode by default
- Automatic backup before changes
- Rollback instructions included

## License

Proprietary - Intent Solutions
