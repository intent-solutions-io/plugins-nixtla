# Liquidity Forecaster Examples

## Example 1: Forecast depth for presidential election market

Predict orderbook depth 6 periods ahead for a political prediction market.

**Commands**:
```bash
python {baseDir}/scripts/fetch_data.py --market_id trump_election_2024
python {baseDir}/scripts/preprocess_data.py --input_file orderbook_data.csv
python {baseDir}/scripts/forecast_liquidity.py --input_file preprocessed_data.csv --horizon 6
```

**Expected output**: `depth_forecast.csv` with 6 forecasted depth values, plot showing trend, summary report.

## Example 2: Forecast spread for cryptocurrency market

Predict bid-ask spread 24 periods ahead for an Ethereum price prediction market.

**Commands**:
```bash
python {baseDir}/scripts/fetch_data.py --market_id eth_price_3000 --output eth_orderbook.csv
python {baseDir}/scripts/preprocess_data.py --input_file eth_orderbook.csv --output eth_preprocessed.csv
python {baseDir}/scripts/forecast_liquidity.py --input_file eth_preprocessed.csv --horizon 24 --output eth_spread_forecast.csv --plot_prefix eth_spread
```

**Expected output**: `eth_spread_forecast.csv` with 24 forecasted values, plot named `eth_spread_forecast.png`, summary report.

## Example 3: Quick workflow for sports outcome market

End-to-end workflow for a sports prediction market using default file names.

**Commands**:
```bash
python {baseDir}/scripts/fetch_data.py --market_id superbowl_winner_2025
python {baseDir}/scripts/preprocess_data.py --input_file orderbook_data.csv
python {baseDir}/scripts/forecast_liquidity.py --input_file preprocessed_data.csv --horizon 12
```

**Expected output**: Standard output files (depth_forecast.csv, depth_forecast.png, report.txt) with 12-period forecast.
