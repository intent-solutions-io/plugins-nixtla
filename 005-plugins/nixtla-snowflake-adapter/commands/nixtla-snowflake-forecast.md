---
name: nixtla-snowflake-forecast
description: Generate and execute Nixtla forecasts in Snowflake
---

# /nixtla-snowflake-forecast

Generate and execute Nixtla forecasts in Snowflake.

## Usage

```
/nixtla-snowflake-forecast [table] [--horizon=30] [--freq=D]
```

## Workflow

1. Validate Snowflake connection
2. Check Nixtla Native App installation
3. Generate CALL NIXTLA_FORECAST() SQL
4. Execute and retrieve results
5. Format for BI tools

## Parameters

- `table`: Source table name
- `--horizon`: Forecast horizon (default: 30)
- `--freq`: Frequency (D, H, W, M)
- `--timestamp-col`: Timestamp column name
- `--value-col`: Value column name
- `--group-by`: Grouping column

## Output

- Generated SQL query
- Forecast results table
- Looker/Tableau export templates
