from prefect.flow_runners import SubprocessFlowRunner

@task(retries=2, retry_delay_seconds=300)
def extract_data():
    # Same extraction logic
    pass

@task
def transform_data(raw_data):
    # Same transformation logic
    pass

@task
def forecast(transformed_data):
    # Same forecasting logic
    pass

@task
def load_forecasts(forecasts):
    # Same loading logic
    pass

@task
def monitor_quality(data, forecasts):
    # Same monitoring logic
    pass

@flow(name="timegpt-forecast-production")
def timegpt_forecast_pipeline():
    raw_data = extract_data()
    transformed = transform_data(raw_data)
    forecasts = forecast(transformed)
    load_forecasts(forecasts)
    monitor_quality(transformed, forecasts)

# Deployment
DeploymentSpec(
    flow=timegpt_forecast_pipeline,
    name="production",
    schedule="0 6 * * *",  # Daily at 6am
    flow_runner=SubprocessFlowRunner(),
    tags=["forecasting", "production"]
)
```

### Cron (Simplest Option)

If user chooses cron, generate standalone script:

```python
