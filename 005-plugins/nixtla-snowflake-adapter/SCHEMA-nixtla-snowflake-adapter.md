# Schema: nixtla-snowflake-adapter

**Generated:** 2025-12-12
**Plugin Version:** 0.1.0
**Status:** BUILT (Business Growth)

---

## Directory Tree (Fully Expanded)

```
nixtla-snowflake-adapter/
├── .claude-plugin/
│   └── plugin.json                # Plugin manifest (Anthropic spec)
├── .mcp.json                      # MCP server configuration
├── commands/
│   ├── nixtla-snowflake-forecast.md  # Slash command: Generate forecast
│   └── nixtla-snowflake-setup.md     # Slash command: Setup wizard
├── scripts/
│   ├── requirements.txt           # Python dependencies
│   └── snowflake_mcp.py           # MCP server (4 tools exposed)
├── templates/
│   └── looker_view.lkml           # Looker view template
└── README.md                      # Plugin documentation
```

---

## Plugin Manifest (plugin.json)

| Field | Value |
|-------|-------|
| name | nixtla-snowflake-adapter |
| description | Claude Code wrapper for Nixtla Snowflake Native App |
| version | 0.1.0 |
| author.name | Intent Solutions |

---

## MCP Tools (4)

| Tool Name | Purpose |
|-----------|---------|
| generate_forecast_sql | Generate CALL NIXTLA_FORECAST SQL |
| validate_setup | Validate Native App installation |
| generate_anomaly_sql | Generate anomaly detection SQL |
| export_looker_view | Generate Looker view template |

---

## Slash Commands (2)

| Command | Purpose |
|---------|---------|
| /nixtla-snowflake-forecast | Generate forecast SQL and execute |
| /nixtla-snowflake-setup | Validate installation and permissions |

---

## CSV Inventory Reference

From `plugins_inventory.csv`:

- **Who:** Snowflake users
- **What:** Query Snowflake data and run forecasts via UDF functions
- **When:** Integrated forecasting within SQL
- **Target Goal:** Execute NIXTLA_FORECAST() UDF and return results
- **Production:** true (BUILT)
