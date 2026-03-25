## Examples

### Example 1: Promotion impact analysis

**Scenario**: Quantify price increase during promotional campaign.

**Input**:
- `prices.csv`: Daily prices for 30 days
- `events.csv`: Single promotion event on day 15

**Command sequence**:
```bash
python scripts/prepare_data.py --prices prices.csv --events events.csv
python scripts/configure_model.py --prices prepared_prices.csv --events prepared_events.csv --window-days 5
python scripts/analyze_impact.py --prices configured_prices.csv --events prepared_events.csv --niter 2000
python scripts/generate_report.py --impact-results impact_results.csv --adjusted-forecast adjusted_forecast.csv
```

**Output**: `impact_results.csv` shows 15% relative price increase during promotion period.

### Example 2: Natural disaster impact

**Scenario**: Assess price drop following natural disaster.

**Input**:
- `prices.csv`: Weekly prices for 52 weeks
- `events.csv`: Disaster event on week 26

**Command sequence**:
```bash
python scripts/prepare_data.py --prices prices.csv --events events.csv
python scripts/configure_model.py --prices prepared_prices.csv --events prepared_events.csv --window-days 7
python scripts/analyze_impact.py --prices configured_prices.csv --events prepared_events.csv
python scripts/generate_report.py --impact-results impact_results.csv --adjusted-forecast adjusted_forecast.csv --title "Disaster Impact Analysis"
```

**Output**: `impact_report.md` documents price recovery timeline and total economic impact.
