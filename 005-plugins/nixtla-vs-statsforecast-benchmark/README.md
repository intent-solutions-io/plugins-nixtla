# Nixtla vs StatsForecast Benchmark

Head-to-head comparison of TimeGPT vs StatsForecast on your data.

## Features

- **Accuracy Comparison**: sMAPE, MASE, RMSE metrics
- **Speed Benchmark**: Execution time comparison
- **Cost Analysis**: API cost vs compute cost
- **Automated Reports**: Markdown/HTML/PDF output

## Quick Start

```bash
pip install -r scripts/requirements.txt

# In Claude Code:
/nixtla-benchmark data.csv --horizon=14 --freq=D
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `run_benchmark` | Execute head-to-head comparison |
| `load_data` | Load and validate time series data |
| `generate_report` | Create comparison report |
| `get_recommendations` | Get migration recommendations |

## Supported Models

### TimeGPT
- TimeGPT (default)
- TimeGPT-long-horizon

### StatsForecast
- AutoETS
- AutoTheta
- AutoARIMA
- SeasonalNaive
- CrostonOptimized

## License

Proprietary - Intent Solutions
