Standalone forecasting script for cron

Run with: python pipelines/run_forecast.py
Schedule with crontab: 0 6 * * * python /path/to/run_forecast.py
"""

import logging

logging.basicConfig(level=logging.INFO)

def main():
    try:
        # Extract
        logging.info("Extracting data...")
        data = extract_production_data()

        # Transform
        logging.info("Transforming data...")
        transformed = transform_to_nixtla_schema(data)

        # Forecast
        logging.info("Running forecast...")
        forecasts = run_timegpt_forecast(transformed)

        # Load
        logging.info("Loading forecasts...")
        load_forecasts_to_destination(forecasts)

        # Monitor
        logging.info("Monitoring quality...")
        monitor_forecast_quality(transformed, forecasts)

        logging.info("✅ Pipeline completed successfully")

    except Exception as e:
        logging.error(f"❌ Pipeline failed: {e}")
        raise

if __name__ == '__main__':
    main()
```

---

## Examples

### Example 1: Generate Airflow Pipeline

