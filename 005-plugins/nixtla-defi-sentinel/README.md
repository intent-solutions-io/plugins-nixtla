# Nixtla DeFi Sentinel

DeFi protocol monitoring with TimeGPT anomaly detection.

## Features

- **Protocol Monitoring**: Track TVL, APY, volume, liquidity
- **Anomaly Detection**: Real-time TimeGPT analysis
- **Alerting**: Telegram, Discord, Email notifications
- **Risk Reports**: Protocol risk assessments

## Quick Start

```bash
pip install -r scripts/requirements.txt

# In Claude Code:
/nixtla-defi-monitor aave --metrics=tvl,apy --alert=telegram
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `monitor_protocol` | Start monitoring a protocol |
| `get_protocol_status` | Get current status |
| `configure_alerts` | Set up alerting |
| `run_anomaly_scan` | Run anomaly detection |
| `generate_risk_report` | Generate risk assessment |
| `compare_protocols` | Compare multiple protocols |

## Supported Protocols

- Aave
- Compound
- Uniswap
- Curve
- MakerDAO
- Lido
- Convex
- Yearn
- Balancer
- SushiSwap

## Metrics

| Metric | Description |
|--------|-------------|
| TVL | Total Value Locked |
| APY | Annual Percentage Yield |
| Volume | Trading volume |
| Liquidity | Available liquidity |
| Price | Token prices |

## Environment Variables

```bash
NIXTLA_TIMEGPT_API_KEY=...
DEFILLAMA_API_KEY=...
TELEGRAM_BOT_TOKEN=...
```

## License

Proprietary - Intent Solutions
