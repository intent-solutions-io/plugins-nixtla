# Schema: nixtla-vs-statsforecast-benchmark

**Generated:** 2025-12-12
**Plugin Version:** 0.1.0
**Status:** BUILT (Business Growth)

---

## Directory Tree (Fully Expanded)

```
nixtla-vs-statsforecast-benchmark/
├── .claude-plugin/
│   └── plugin.json                # Plugin manifest (Anthropic spec)
├── .mcp.json                      # MCP server configuration
├── commands/
│   └── nixtla-benchmark.md        # Slash command: Run benchmark
├── data/                          # Sample benchmark data (empty)
├── scripts/
│   ├── benchmark_mcp.py           # MCP server (4 tools exposed)
│   └── requirements.txt           # Python dependencies
├── templates/                     # Report templates (empty)
└── README.md                      # Plugin documentation
```

---

## Plugin Manifest (plugin.json)

| Field | Value |
|-------|-------|
| name | nixtla-vs-statsforecast-benchmark |
| description | Head-to-head comparison of TimeGPT vs StatsForecast |
| version | 0.1.0 |
| author.name | Intent Solutions |

---

## MCP Tools (4)

| Tool Name | Purpose |
|-----------|---------|
| run_benchmark | Execute head-to-head comparison |
| load_data | Load and validate time series data |
| generate_report | Create comparison report |
| get_recommendations | Get migration recommendations |

---

## Slash Commands (1)

| Command | Purpose |
|---------|---------|
| /nixtla-benchmark | Run TimeGPT vs StatsForecast benchmark |

---

## CSV Inventory Reference

From `plugins_inventory.csv`:

- **Who:** Enterprises comparing solutions
- **What:** Head-to-head comparison with user's data
- **When:** Decision making, POC evaluation
- **Target Goal:** Side-by-side accuracy and performance comparison
- **Production:** true (BUILT)
