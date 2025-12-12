# Schema: nixtla-migration-assistant

**Generated:** 2025-12-12
**Plugin Version:** 0.1.0
**Status:** BUILT (Internal Efficiency)

---

## Directory Tree (Fully Expanded)

```
nixtla-migration-assistant/
├── .claude-plugin/
│   └── plugin.json                # Plugin manifest (Anthropic spec)
├── .mcp.json                      # MCP server configuration
├── commands/
│   ├── nixtla-migrate-analyze.md  # Slash command: Analysis only
│   └── nixtla-migrate.md          # Slash command: Run migration
├── scripts/
│   ├── migration_mcp.py           # MCP server (5 tools exposed)
│   └── requirements.txt           # Python dependencies
├── templates/
│   └── prophet_to_timegpt.py      # Prophet → TimeGPT template
├── tests/                         # Test files (empty)
└── README.md                      # Plugin documentation
```

---

## Plugin Manifest (plugin.json)

| Field | Value |
|-------|-------|
| name | nixtla-migration-assistant |
| description | Automated migration from Prophet/statsmodels to Nixtla |
| version | 0.1.0 |
| author.name | Intent Solutions |

---

## MCP Tools (5)

| Tool Name | Purpose |
|-----------|---------|
| analyze_code | Parse and detect forecasting patterns |
| generate_plan | Create migration plan with estimates |
| transform_data | Convert data to Nixtla format |
| generate_code | Generate equivalent Nixtla code |
| compare_accuracy | Run side-by-side accuracy test |

---

## Slash Commands (2)

| Command | Purpose |
|---------|---------|
| /nixtla-migrate | Full migration workflow |
| /nixtla-migrate --analyze-only | Analysis and planning only |

---

## Migration Patterns Supported

| Source | Target | Support Level |
|--------|--------|---------------|
| Prophet | TimeGPT | Full |
| Prophet | StatsForecast | Full |
| statsmodels.tsa.arima | StatsForecast | Full |
| statsmodels.tsa.exponential_smoothing | StatsForecast | Full |
| sklearn time series | StatsForecast | Partial |

---

## CSV Inventory Reference

From `plugins_inventory.csv`:

- **Who:** Organizations migrating from other tools
- **What:** Guided migration from legacy forecasting systems to TimeGPT
- **When:** Simplify conversion process
- **Target Goal:** Convert Prophet/SARIMA code to TimeGPT equivalent
- **Production:** true (BUILT)
