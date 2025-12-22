---
name: nixtla-defi-monitor
description: Monitor DeFi protocols with TimeGPT anomaly detection
---

# /nixtla-defi-monitor

Monitor DeFi protocols with TimeGPT anomaly detection.

## Usage

```
/nixtla-defi-monitor [protocol] [--metrics=tvl,apy] [--alert=telegram]
```

## Workflow

1. Connect to DeFiLlama API
2. Fetch protocol metrics
3. Run TimeGPT anomaly detection
4. Configure alerting
5. Start continuous monitoring

## Parameters

- `protocol`: Protocol name (aave, compound, uniswap, etc.)
- `--metrics`: Metrics to monitor (tvl, apy, volume, liquidity)
- `--threshold`: Anomaly threshold (default: 0.95)
- `--alert`: Alert channel (telegram, discord, email)

## Monitored Metrics

- TVL (Total Value Locked)
- APY/APR changes
- Liquidity depth
- Volume anomalies
- Price deviations

## Output

- Real-time monitoring dashboard
- Anomaly alerts
- Historical analysis
- Risk assessment report
