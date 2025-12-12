# Nixtla Cost Optimizer

Optimize TimeGPT API usage costs by 40-60%.

## Features

- **Usage Analysis**: Identify optimization opportunities
- **Batching Simulation**: Test aggregation strategies
- **Hybrid Strategy**: StatsForecast + TimeGPT routing
- **Report Generation**: Executive summaries

## Quick Start

```bash
pip install -r scripts/requirements.txt

# In Claude Code:
/nixtla-optimize --analyze
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `analyze_usage` | Analyze API usage patterns |
| `recommend_optimizations` | Generate recommendations |
| `simulate_batching` | Test batching strategies |
| `generate_hybrid_strategy` | Create SF + TimeGPT hybrid |
| `export_report` | Export optimization report |

## Optimization Strategies

### 1. Batching (40-50% savings)
Aggregate single-series calls into batches of 100.

### 2. Caching (15-20% savings)
Cache identical requests for 1 hour.

### 3. Hybrid Routing (20-30% savings)
Use StatsForecast for low-value series.

## License

Proprietary - Intent Solutions
