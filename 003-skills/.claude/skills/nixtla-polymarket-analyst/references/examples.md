# Polymarket Analyst Examples

## Example 1: Election Contract Analysis

**User Request**: "Analyze the 2024 election contract 0x1234abcd with 48-hour forecast"

**Agent Actions**:
```bash
python {baseDir}/scripts/analyze_polymarket.py 0x1234abcd --horizon 48 --days 60
```

**Expected Output**:
```
Contract: "Will candidate X win the 2024 election?"
Current Price: $0.4500
Forecast Price: $0.5200
Expected Change: +15.56%
Signal: BUY (BULLISH)
95% CI: [0.4800, 0.5600]
```

**Interpretation**: The model predicts a 15.56% increase in the "yes" price, suggesting growing confidence in the outcome. The tight confidence interval indicates reasonable certainty.

## Example 2: Crypto Price Contract

**User Request**: "What's the forecast for the ETH price contract?"

**Agent Actions**:
```bash
python {baseDir}/scripts/analyze_polymarket.py 0xdef456 --horizon 24 --days 14
```

**Expected Output**:
```
Contract: "Will ETH be above $3000 on Dec 31?"
Current Price: $0.6800
Forecast Price: $0.6500
Expected Change: -4.41%
Signal: HOLD (NEUTRAL)
95% CI: [0.6000, 0.7000]
```

**Interpretation**: The model predicts a slight decrease, but within the neutral range. Wide confidence interval suggests uncertainty. No strong trading signal.

## Example 3: Step-by-Step Analysis

Run the analysis pipeline step by step for more control over intermediate outputs.

```bash
# Step 1: Fetch contract data
python {baseDir}/scripts/fetch_contract.py 0xabc789 --days 30

# Step 2: Transform to Nixtla format
python {baseDir}/scripts/transform_data.py contract_0xabc789_data.json

# Step 3: Generate forecast with custom horizon
python {baseDir}/scripts/forecast_contract.py contract_0xabc789_nixtla.csv \
  --horizon 72 \
  --freq H \
  --output my_analysis
```
