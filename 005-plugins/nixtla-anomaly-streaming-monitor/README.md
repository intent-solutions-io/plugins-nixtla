# Nixtla Anomaly Streaming Monitor

Real-time streaming anomaly detection for Kafka/Kinesis with alerting.

## Features

- **Stream Sources**: Kafka, AWS Kinesis, HTTP Webhooks
- **Real-time Detection**: <1 second latency
- **Alerting**: PagerDuty, Slack, Email
- **Monitoring**: Grafana dashboard, Prometheus metrics

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Kafka/    │────▶│   MCP Server │────▶│  TimeGPT    │
│   Kinesis   │     │  (TypeScript)│     │   API       │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   Alerting   │
                    │  (PagerDuty) │
                    └──────────────┘
```

## Quick Start

```bash
# Install dependencies
npm install
pip install -r src/python-worker/requirements.txt

# In Claude Code:
/nixtla-stream-monitor kafka --topic=events --threshold=0.95
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `stream_monitor_start` | Start monitoring a stream |
| `stream_monitor_stop` | Stop monitoring |
| `stream_health_check` | Check consumer health |
| `configure_alerts` | Set up alerting rules |
| `get_anomaly_stats` | Get real-time statistics |
| `export_dashboard_config` | Generate Grafana dashboard |

## License

Proprietary - Intent Solutions
