# Nixtla Forecast Explainer

Generate plain-English explanations of TimeGPT forecasts.

## Features

- **STL Decomposition**: Trend, seasonal, residual analysis
- **Driver Identification**: Quantify contributing factors
- **Narrative Generation**: Executive summaries
- **Report Export**: PDF, HTML, PowerPoint, Markdown

## Quick Start

```bash
pip install -r scripts/requirements.txt

# In Claude Code:
/nixtla-explain forecast_results.csv --format=executive
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `decompose_forecast` | STL decomposition |
| `identify_drivers` | Calculate driver contributions |
| `generate_narrative` | Plain-English explanation |
| `generate_report` | Export formatted report |
| `assess_risk_factors` | Flag high uncertainty periods |

## Report Formats

| Format | Use Case |
|--------|----------|
| Executive PDF | Board presentations |
| Technical HTML | Data science review |
| Compliance | SOX/Basel III audit |
| Markdown | Technical documentation |

## License

Proprietary - Intent Solutions
