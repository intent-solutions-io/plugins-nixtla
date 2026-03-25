# Market Risk Analyzer Error Handling

## No Date Column Found

**Cause**: CSV file does not contain a recognized date column.
**Solution**: Ensure CSV has a column named `ds`, `date`, or `timestamp`. The script auto-detects these names case-insensitively. Rename your date column to one of these recognized names if using a custom format.

## No Price Column Found

**Cause**: CSV file does not contain a recognized price column.
**Solution**: Ensure CSV has a column named `y`, `price`, or `close`. The script checks for these column names to identify the price series for risk calculations.

## Insufficient Data for Analysis

**Cause**: Too few price observations for reliable statistical analysis.
**Solution**: Provide at least 30 price points for reliable VaR and volatility estimates. For rolling window calculations, 60+ observations are recommended. Short series produce unreliable confidence intervals.

## Module Not Found: matplotlib

**Cause**: Visualization dependency not installed.
**Solution**: Install visualization dependencies: `pip install matplotlib`. The core risk metrics calculation works without matplotlib, but the report generation step requires it for chart creation.

## NIXTLA_TIMEGPT_API_KEY Not Set

**Cause**: Environment variable not configured for optional volatility forecasting.
**Solution**: Only needed for optional forward-looking volatility forecasting. Core risk analysis (VaR, drawdown, Sharpe) works without it. Set the key with: `export NIXTLA_TIMEGPT_API_KEY=your_key` if volatility forecasting is desired.
