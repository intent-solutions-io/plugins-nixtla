# Schema: nixtla-cost-optimizer

**Generated:** 2025-12-12
**Plugin Version:** 0.1.0
**Status:** BUILT (Internal Efficiency)

---

## Directory Tree (Fully Expanded)

```
nixtla-cost-optimizer/
├── .claude-plugin/
│   └── plugin.json                # Plugin manifest (Anthropic spec)
├── .mcp.json                      # MCP server configuration
├── commands/
│   └── nixtla-optimize.md         # Slash command: Optimize costs
├── scripts/
│   ├── cost_optimizer_mcp.py      # MCP server (5 tools exposed)
│   └── requirements.txt           # Python dependencies
├── templates/                     # Report templates (empty)
├── tests/                         # Test files (empty)
└── README.md                      # Plugin documentation
```

---

## Plugin Manifest (plugin.json)

| Field | Value |
|-------|-------|
| name | nixtla-cost-optimizer |
| description | Optimize TimeGPT API usage costs by 40-60% |
| version | 0.1.0 |
| author.name | Intent Solutions |

---

## MCP Tools (5)

| Tool Name | Purpose |
|-----------|---------|
| analyze_usage | Analyze TimeGPT API usage patterns |
| recommend_optimizations | Generate optimization recommendations |
| simulate_batching | Simulate batching strategy impact |
| generate_hybrid_strategy | Create SF + TimeGPT hybrid |
| export_report | Export optimization report |

---

## Slash Commands (1)

| Command | Purpose |
|---------|---------|
| /nixtla-optimize | Analyze and optimize API costs |

---

## CSV Inventory Reference

From `plugins_inventory.csv`:

- **Who:** Data science teams
- **What:** Analyze and optimize TimeGPT API usage
- **When:** Cost optimization, budget planning
- **Target Goal:** 40-60% cost reduction recommendations
- **Production:** true (BUILT)
