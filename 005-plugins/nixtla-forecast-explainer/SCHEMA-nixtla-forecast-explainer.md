# Schema: nixtla-forecast-explainer

**Generated:** 2025-12-12
**Plugin Version:** 0.1.0
**Status:** BUILT (Internal Efficiency)

---

## Directory Tree (Fully Expanded)

```
nixtla-forecast-explainer/
├── .claude-plugin/
│   └── plugin.json                # Plugin manifest (Anthropic spec)
├── .mcp.json                      # MCP server configuration
├── commands/
│   ├── nixtla-decompose.md        # Slash command: STL decomposition
│   └── nixtla-explain.md          # Slash command: Generate explanation
├── scripts/
│   ├── explainer_mcp.py           # MCP server (5 tools exposed)
│   └── requirements.txt           # Python dependencies
├── skills/
│   └── nixtla-explain-analyst/
│       └── SKILL.md               # AI skill for interpretation
├── templates/                     # Report templates (empty)
└── README.md                      # Plugin documentation
```

---

## Plugin Manifest (plugin.json)

| Field | Value |
|-------|-------|
| name | nixtla-forecast-explainer |
| description | Post-hoc explainability for TimeGPT forecasts |
| version | 0.1.0 |
| author.name | Intent Solutions |

---

## MCP Tools (5)

| Tool Name | Purpose |
|-----------|---------|
| decompose_forecast | STL decomposition (trend/seasonal/residual) |
| identify_drivers | Calculate contribution percentages |
| generate_narrative | Plain-English explanation |
| generate_report | PDF/HTML/PPTX export |
| assess_risk_factors | Flag high uncertainty periods |

---

## Slash Commands (2)

| Command | Purpose |
|---------|---------|
| /nixtla-explain | Generate full explanation report |
| /nixtla-decompose | Time series decomposition only |

---

## AI Skill (1)

| Skill | Purpose |
|-------|---------|
| nixtla-explain-analyst | AI skill for forecast interpretation |

---

## CSV Inventory Reference

From `plugins_inventory.csv`:

- **Who:** Business analysts, non-technical users
- **What:** Generate plain-English explanations of forecast results
- **When:** Communicate forecasts to business teams
- **Target Goal:** Generate explanation readable by non-technical user
- **Production:** true (BUILT)
