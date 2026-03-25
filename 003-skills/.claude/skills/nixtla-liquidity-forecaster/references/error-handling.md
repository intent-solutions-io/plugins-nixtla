# Liquidity Forecaster Error Handling

## Invalid Polymarket Market ID

**Cause**: Market ID not recognized by Polymarket API.
**Solution**: Verify the market ID at https://polymarket.com or check API documentation. Market IDs are typically slug-formatted strings matching the URL path on polymarket.com.

## TimeGPT API Key Missing

**Cause**: `NIXTLA_TIMEGPT_API_KEY` environment variable not set.
**Solution**: Export your API key before running forecasts:
```bash
export NIXTLA_TIMEGPT_API_KEY=your_key_here
```

## Insufficient Data from Polymarket API

**Cause**: Empty or incomplete orderbook data for the specified market.
**Solution**: Check data availability for the market ID, try a different market, or verify the API endpoint. Some markets have low liquidity and may not return enough data points for forecasting.

## TimeGPT Forecast Failed

**Cause**: Input data format issues or API connection problems.
**Solution**: Verify preprocessed data has required columns (unique_id, ds, y), check API status at https://status.nixtla.io, and ensure data types are correct (datetime for ds, numeric for y).

## Missing Required Columns

**Cause**: Raw orderbook data lacks price, quantity, or side columns.
**Solution**: Verify Polymarket API response structure matches expected format. The fetch script expects `price`, `quantity`, and `side` fields in the orderbook response. Check for any Polymarket API changes that may have modified field names.
