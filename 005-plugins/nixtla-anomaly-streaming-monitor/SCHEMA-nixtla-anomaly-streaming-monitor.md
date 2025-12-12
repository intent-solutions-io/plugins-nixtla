# Schema: nixtla-anomaly-streaming-monitor

**Generated:** 2025-12-12
**Plugin Version:** 0.1.0
**Status:** BUILT (Business Growth)

---

## Directory Tree (Fully Expanded)

```
nixtla-anomaly-streaming-monitor/
├── .claude-plugin/
│   └── plugin.json                # Plugin manifest (Anthropic spec)
├── .mcp.json                      # MCP server configuration (TypeScript)
├── commands/
│   └── nixtla-stream-monitor.md   # Slash command: Start monitoring
├── config/
│   └── grafana_dashboard.json     # Grafana dashboard template
├── src/
│   ├── mcp-server/
│   │   └── index.ts               # TypeScript MCP server (6 tools)
│   └── python-worker/
│       └── anomaly_detector.py    # Nixtla TimeGPT integration
├── tests/                         # Test files (empty)
└── README.md                      # Plugin documentation
```

---

## Plugin Manifest (plugin.json)

| Field | Value |
|-------|-------|
| name | nixtla-anomaly-streaming-monitor |
| description | Real-time streaming anomaly detection for Kafka/Kinesis |
| version | 0.1.0 |
| author.name | Intent Solutions |

---

## MCP Tools (6)

| Tool Name | Purpose |
|-----------|---------|
| stream_monitor_start | Start monitoring a stream |
| stream_monitor_stop | Stop monitoring |
| stream_health_check | Check consumer health |
| configure_alerts | Set up alerting rules |
| get_anomaly_stats | Get real-time statistics |
| export_dashboard_config | Generate Grafana dashboard |

---

## Architecture (Hybrid)

| Component | Language | Purpose |
|-----------|----------|---------|
| MCP Server | TypeScript | Stream processing, alerting |
| Anomaly Worker | Python | Nixtla API calls, detection |

---

## CSV Inventory Reference

From `plugins_inventory.csv`:

- **Who:** FinTech teams, SRE teams, E-commerce, IoT platforms
- **What:** Real-time streaming anomaly detection for Kafka/Kinesis
- **When:** Payment fraud, infrastructure monitoring, sensor streams
- **Target Goal:** Detect anomaly within 30 seconds of occurrence
- **Production:** true (BUILT)
