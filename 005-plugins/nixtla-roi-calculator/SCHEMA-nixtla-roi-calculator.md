# Schema: nixtla-roi-calculator

**Generated:** 2025-12-12
**Plugin Version:** 0.1.0
**Status:** BUILT (Business Growth)

---

## Directory Tree (Fully Expanded)

```
nixtla-roi-calculator/
├── .claude-plugin/
│   └── plugin.json                # Plugin manifest (Anthropic spec)
├── .mcp.json                      # MCP server configuration
├── commands/
│   └── nixtla-roi.md              # Slash command: Calculate ROI wizard
├── data/
│   └── industry_benchmarks.json   # Industry cost benchmarks (retail, finance, etc.)
├── scripts/
│   ├── cost_modeler.py            # TCO calculation engine
│   ├── report_generator.py        # PDF/PPT/Markdown report generation
│   ├── requirements.txt           # Python dependencies
│   └── roi_calculator_mcp.py      # MCP server (4 tools exposed)
├── templates/
│   └── executive_summary.html     # 1-page executive HTML template
└── README.md                      # Plugin documentation
```

---

## Plugin Manifest (plugin.json)

| Field | Value |
|-------|-------|
| name | nixtla-roi-calculator |
| description | Enterprise ROI calculator for TimeGPT value estimation |
| version | 0.1.0 |
| author.name | Intent Solutions |

---

## MCP Tools (4)

| Tool Name | Purpose |
|-----------|---------|
| calculate_roi | Run ROI calculation with inputs |
| generate_report | Create PDF/PowerPoint report |
| compare_scenarios | Compare build vs buy approaches |
| export_salesforce | Export to Salesforce format |

---

## Slash Commands (1)

| Command | Purpose |
|---------|---------|
| /nixtla-roi | Start ROI calculation wizard |

---

## Files Summary

| File | Lines | Purpose |
|------|-------|---------|
| roi_calculator_mcp.py | 145 | MCP server with 4 tools |
| cost_modeler.py | 95 | TCO calculation engine |
| report_generator.py | 85 | Report generation |
| executive_summary.html | 65 | Executive HTML template |
| industry_benchmarks.json | 45 | Industry cost data |

---

## CSV Inventory Reference

From `plugins_inventory.csv`:

- **Who:** Sales teams, finance
- **What:** Interactive calculator for TimeGPT ROI estimation
- **When:** Sales demos, business case validation
- **Target Goal:** Generate ROI estimate from user inputs in <2 seconds
- **Production:** true (BUILT)
