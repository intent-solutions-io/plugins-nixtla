# Nixtla ROI Calculator

Enterprise ROI calculator for TimeGPT value estimation.

## Features

- **ROI Calculation**: Calculate build vs buy costs
- **Report Generation**: Executive PDF/PowerPoint reports
- **Scenario Comparison**: Compare multiple approaches
- **Salesforce Export**: CRM-ready opportunity data

## Quick Start

```bash
# Install dependencies
pip install -r scripts/requirements.txt

# In Claude Code, use the slash command:
/nixtla-roi
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `calculate_roi` | Run ROI calculation with inputs |
| `generate_report` | Create PDF/PowerPoint report |
| `compare_scenarios` | Compare build vs buy approaches |
| `export_salesforce` | Export to Salesforce format |

## Usage

### Calculate ROI

```
/nixtla-roi

Current monthly tool cost: $5000
Data scientist hours/week: 20
Monthly forecast volume: 50000
```

### Output

- Annual savings estimate
- 3-year TCO comparison
- Executive summary PDF
- Salesforce-ready export

## Industry Benchmarks

Default benchmarks for:
- Retail
- Finance
- Manufacturing
- Energy
- Healthcare

## License

Proprietary - Intent Solutions
