# Nixtla Correlation Mapper Scripts

Standalone Python scripts for portfolio correlation analysis and hedge recommendation generation.

## Scripts

1. **prepare_data.py** - Data loading, pivoting, returns calculation
2. **correlation_analysis.py** - Correlation matrix, p-values, rolling correlations
3. **hedge_recommendations.py** - Hedge ratios, portfolio allocation
4. **visualize.py** - Heatmaps, rolling plots, effectiveness charts
5. **generate_report.py** - Comprehensive markdown report

## Requirements

```bash
pip install pandas numpy scipy matplotlib seaborn
```

## Usage

### Complete Pipeline

```bash
# Step 1: Prepare data
python prepare_data.py contracts.csv --method log --output-dir results/

# Step 2: Calculate correlations
python correlation_analysis.py --returns results/returns.csv --output-dir results/

# Step 3: Generate hedge recommendations
python hedge_recommendations.py --returns results/returns.csv --correlation results/correlation_matrix.csv --output-dir results/

# Step 4: Create visualizations
python visualize.py --correlation results/correlation_matrix.csv --output-dir results/

# Step 5: Generate report
python generate_report.py --correlation results/correlation_matrix.csv --output results/correlation_report.md
```

### Individual Scripts

Each script has comprehensive argparse CLI:

```bash
python prepare_data.py --help
python correlation_analysis.py --help
python hedge_recommendations.py --help
python visualize.py --help
python generate_report.py --help
```

## Input Format

CSV file with columns:
- `unique_id`: Contract identifier (string)
- `ds`: Date (ISO format YYYY-MM-DD)
- `y`: Price/value (numeric)

Example:
```csv
unique_id,ds,y
BTC,2024-01-01,42000
ETH,2024-01-01,2200
BTC,2024-01-02,42500
ETH,2024-01-02,2250
```

## Output Files

- `prices_wide.csv` - Pivoted price matrix
- `returns.csv` - Calculated returns
- `correlation_matrix.csv` - Full correlation matrix
- `correlation_pvalues.csv` - Statistical significance
- `high_correlations.json` - Significant pairs
- `rolling_correlations.csv` - Time-series stability
- `hedge_recommendations.csv` - Detailed strategies
- `hedge_recommendations.json` - JSON format recommendations
- `hedged_portfolio.csv` - Portfolio allocation
- `correlation_heatmap.png` - Visual heatmap
- `rolling_correlation.png` - Rolling correlation plot
- `hedge_effectiveness.png` - Effectiveness chart
- `correlation_report.md` - Comprehensive report

## Error Handling

All scripts include:
- Proper exception handling
- Informative error messages
- Input validation
- Progress logging
- Return codes (0=success, 1=error)
