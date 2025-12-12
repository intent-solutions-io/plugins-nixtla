# /nixtla-optimize

Analyze and optimize TimeGPT API usage costs.

## Usage

```
/nixtla-optimize [--analyze] [--recommend] [--apply]
```

## Workflow

1. Analyze current API usage patterns
2. Identify optimization opportunities
3. Generate batching recommendations
4. Estimate cost savings
5. Apply optimizations (optional)

## Parameters

- `--analyze`: Analyze usage only (default)
- `--recommend`: Generate optimization plan
- `--apply`: Apply recommended changes
- `--target-reduction`: Target cost reduction %

## Optimizations

- Batch similar forecasts together
- Use StatsForecast for high-volume/low-value series
- Implement caching for repeated requests
- Right-size confidence intervals

## Output

- Usage analysis report
- Optimization recommendations
- Estimated savings (40-60%)
- Implementation guide
