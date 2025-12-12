# Schema: nixtla-defi-sentinel

**Generated:** 2025-12-12
**Plugin Version:** 0.1.0
**Status:** BUILT (Vertical DeFi)

---

## Directory Tree (Fully Expanded)

```
nixtla-defi-sentinel/
├── .claude-plugin/
│   └── plugin.json                # Plugin manifest (Anthropic spec)
├── .mcp.json                      # MCP server configuration
├── commands/
│   └── nixtla-defi-monitor.md     # Slash command: Start monitoring
├── scripts/
│   ├── defi_sentinel_mcp.py       # MCP server (6 tools exposed)
│   └── requirements.txt           # Python dependencies
├── templates/                     # Report templates (empty)
├── tests/                         # Test files (empty)
└── README.md                      # Plugin documentation
```

---

## Plugin Manifest (plugin.json)

| Field | Value |
|-------|-------|
| name | nixtla-defi-sentinel |
| description | DeFi protocol monitoring with TimeGPT anomaly detection |
| version | 0.1.0 |
| author.name | Intent Solutions |

---

## MCP Tools (6)

| Tool Name | Purpose |
|-----------|---------|
| monitor_protocol | Start monitoring a DeFi protocol |
| get_protocol_status | Get current status |
| configure_alerts | Set up alerting rules |
| run_anomaly_scan | Run anomaly detection scan |
| generate_risk_report | Generate risk assessment |
| compare_protocols | Compare multiple protocols |

---

## Slash Commands (1)

| Command | Purpose |
|---------|---------|
| /nixtla-defi-monitor | Start DeFi protocol monitoring |

---

## Supported Protocols

| Protocol | Metrics |
|----------|---------|
| Aave | TVL, APY, Volume, Liquidity |
| Compound | TVL, APY, Volume, Liquidity |
| Uniswap | TVL, Volume, Liquidity |
| Curve | TVL, APY, Volume |
| MakerDAO | TVL, Collateralization |
| Lido | TVL, Staking APY |

---

## CSV Inventory Reference

From `plugins_inventory.csv`:

- **Who:** DeFi traders, protocol analysts
- **What:** Real-time DeFi protocol monitoring
- **When:** Risk assessment, anomaly detection
- **Target Goal:** Detect TVL/APY anomalies within 5 minutes
- **Production:** true (BUILT)
