
## Architecture

```
[Data Source] → Extract → Transform → Forecast → Load → Monitor → [Destination]
                                        ↓
                                  (Fallback to
                                   baselines)
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
# Required
export NIXTLA_API_KEY='your-api-key'
export FORECAST_DATA_SOURCE='postgresql://...'
export FORECAST_DESTINATION='postgresql://...'

# Optional
export ENVIRONMENT='production'  # dev/staging/production
```

### 3. Deploy to Airflow

```bash
# Copy DAG to Airflow dags folder
cp pipelines/timegpt_forecast_dag.py /opt/airflow/dags/

# Copy monitoring module
cp pipelines/monitoring.py /opt/airflow/dags/pipelines/

# Copy config
cp forecasting/config.yml /opt/airflow/dags/forecasting/

# Restart Airflow
docker-compose restart airflow-scheduler
```

## Testing

Test pipeline locally before deploying:

```python
# Test extract
python -c "from timegpt_forecast_dag import extract_production_data; extract_production_data()"

# Test transform
python -c "from timegpt_forecast_dag import transform_to_nixtla_schema; transform_to_nixtla_schema()"

# Test forecast
python -c "from timegpt_forecast_dag import run_timegpt_forecast; run_timegpt_forecast()"
```

## Monitoring

Pipeline emits logs and metrics at each step:
- Extract: Row count, date range
- Transform: Schema validation
- Forecast: Model used (TimeGPT or fallback)
- Load: Rows written
- Monitor: SMAPE, drift detection

### Alerts

Configure alerts in Airflow UI for:
- Task failures (automatic retry 2x)
- Forecast quality degradation (SMAPE > threshold)
- Data drift detection

## Troubleshooting

### TimeGPT API errors
- Check API key: `echo $NIXTLA_API_KEY`
- Verify quota: https://dashboard.nixtla.io
- Pipeline will fallback to StatsForecast baselines

### Data source connection errors
- Verify connection string
- Check network access from Airflow
- Test connection: `python -c "import sqlalchemy; engine = sqlalchemy.create_engine('$FORECAST_DATA_SOURCE'); engine.connect()"`

### Forecast quality issues
- Check backtest metrics in monitoring step
- Review data for anomalies or drift
- Consider retraining fine-tuned models
```

**Tell the user**:
- "Created `pipelines/README.md` with deployment guide"
- Highlight setup steps, testing, monitoring
- Provide troubleshooting guidance

---

## Handling Different Orchestration Platforms

### Prefect (Alternative)

