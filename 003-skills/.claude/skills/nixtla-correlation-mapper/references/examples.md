## Examples

### Example 1: Crypto Portfolio

**Input** (portfolio.csv):
```csv
unique_id,ds,y
BTC,2024-01-01,42000
ETH,2024-01-01,2200
BTC,2024-01-02,42500
ETH,2024-01-02,2250
```

**Workflow**:
```bash
python scripts/prepare_data.py portfolio.csv
python scripts/correlation_analysis.py
python scripts/hedge_recommendations.py
python scripts/visualize.py
python scripts/generate_report.py
```

**Result**: Correlation 0.85 between BTC-ETH, hedge ratio -0.95, variance reduction 72%

### Example 2: Prediction Market Contracts

**Input**: 5 election-related prediction market contracts

**Command**:
```bash
python scripts/prepare_data.py elections.csv --output-dir election_analysis/
python scripts/correlation_analysis.py --threshold 0.7 --output-dir election_analysis/
python scripts/hedge_recommendations.py --top-n 5 --output-dir election_analysis/
python scripts/visualize.py --output-dir election_analysis/
python scripts/generate_report.py --output election_analysis/report.md
```

**Result**: Identified 3 pairs with correlation > 0.7, top hedge reduces variance by 62%
