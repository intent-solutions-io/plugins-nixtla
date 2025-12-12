# Nixtla Snowflake Adapter

Claude Code wrapper for Nixtla Snowflake Native App.

## Features

- **SQL Generation**: CALL NIXTLA_FORECAST() SQL
- **Setup Validation**: Check Native App installation
- **BI Export**: Looker/Tableau templates

## Quick Start

```bash
pip install -r scripts/requirements.txt

# In Claude Code:
/nixtla-snowflake-forecast SALES_HISTORY --horizon=30 --freq=D
```

## Prerequisites

1. Snowflake account with Nixtla Native App installed
2. Appropriate permissions on database/schema

## MCP Tools

| Tool | Description |
|------|-------------|
| `generate_forecast_sql` | Generate CALL NIXTLA_FORECAST SQL |
| `validate_setup` | Validate Native App installation |
| `generate_anomaly_sql` | Generate anomaly detection SQL |
| `export_looker_view` | Generate Looker view template |

## Environment Variables

```bash
SNOWFLAKE_ACCOUNT=myorg.snowflakecomputing.com
SNOWFLAKE_USER=analytics_user
SNOWFLAKE_PASSWORD=...
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=ANALYTICS
SNOWFLAKE_SCHEMA=FORECASTS
```

## License

Proprietary - Intent Solutions
