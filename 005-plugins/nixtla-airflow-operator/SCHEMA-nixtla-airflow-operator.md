# Schema: nixtla-airflow-operator

**Generated:** 2025-12-12
**Plugin Version:** 0.1.0
**Status:** BUILT (Business Growth)

---

## Directory Tree (Fully Expanded)

```
nixtla-airflow-operator/
├── .claude-plugin/
│   └── plugin.json                # Plugin manifest (Anthropic spec)
├── .mcp.json                      # MCP server configuration
├── commands/
│   └── nixtla-airflow-dag.md      # Slash command: Generate DAG
├── scripts/
│   ├── airflow_mcp.py             # MCP server (4 tools) with DAG template
│   └── requirements.txt           # Python dependencies
├── templates/                     # DAG templates (empty, templates in code)
├── tests/                         # DAG tests (empty)
└── README.md                      # Plugin documentation
```

---

## Plugin Manifest (plugin.json)

| Field | Value |
|-------|-------|
| name | nixtla-airflow-operator |
| description | Apache Airflow operator for TimeGPT forecasting DAGs |
| version | 0.1.0 |
| author.name | Intent Solutions |

---

## MCP Tools (4)

| Tool Name | Purpose |
|-----------|---------|
| generate_dag | Generate Airflow DAG Python file |
| validate_dag | Validate DAG syntax and connections |
| configure_connection | Set up data source connection |
| generate_tests | Create DAG test file |

---

## Slash Commands (1)

| Command | Purpose |
|---------|---------|
| /nixtla-airflow-dag | Generate production-ready Airflow DAG |

---

## CSV Inventory Reference

From `plugins_inventory.csv`:

- **Who:** Data engineers
- **What:** Native Airflow operator for scheduled forecasting jobs
- **When:** Production pipeline orchestration
- **Target Goal:** DAG runs successfully with forecast output
- **Production:** true (BUILT)
