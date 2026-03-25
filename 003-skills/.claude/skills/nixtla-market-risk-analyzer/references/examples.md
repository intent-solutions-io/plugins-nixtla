# Market Risk Analyzer Examples

## Example 1: Analyze Stock Risk

Complete workflow for stock portfolio risk analysis with default parameters.

```bash
# Prepare price data and calculate log returns
python {baseDir}/scripts/prepare_data.py AAPL_prices.csv

# Calculate comprehensive risk metrics
python {baseDir}/scripts/risk_metrics.py AAPL_prices.csv

# Determine optimal position sizing
python {baseDir}/scripts/position_sizing.py --account-size 100000 --asset-volatility 0.28

# Generate full report with visualizations
python {baseDir}/scripts/generate_report.py AAPL_prices.csv

# Expected output:
# VaR (95%): -2.15%
# Max Drawdown: -35.2%
# Sharpe Ratio: 0.95
# Recommended Position: $45,000 (45% of account)
```

## Example 2: Prediction Market Contract Analysis

High volatility asset with conservative sizing for prediction market contracts.

```bash
# Calculate risk metrics for volatile contract
python {baseDir}/scripts/risk_metrics.py contract_prices.csv --output contract_risk.json

# Conservative position sizing
python {baseDir}/scripts/position_sizing.py \
  --account-size 50000 \
  --risk-per-trade 0.01 \
  --asset-volatility 0.45 \
  --output contract_sizing.json

# Expected output:
# VaR (95%): -8.5%
# Volatility Regime: HIGH
# Recommended Position: $12,000 (24% of account)
```

## Example 3: Custom Risk Parameters

Comparing conservative vs aggressive position sizing strategies for the same market.

```bash
# Conservative parameters for volatile market
python {baseDir}/scripts/position_sizing.py \
  --account-size 200000 \
  --risk-per-trade 0.01 \
  --stop-loss 0.03 \
  --target-volatility 0.10 \
  --max-var-loss 0.02

# Aggressive parameters for stable market
python {baseDir}/scripts/position_sizing.py \
  --account-size 200000 \
  --risk-per-trade 0.03 \
  --stop-loss 0.07 \
  --target-volatility 0.20 \
  --max-var-loss 0.05
```
