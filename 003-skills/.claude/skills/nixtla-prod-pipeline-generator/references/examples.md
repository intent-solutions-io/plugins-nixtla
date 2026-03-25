## Examples

### Example 1: Airflow DAG

```bash
python {baseDir}/scripts/generate_pipeline.py \
    --config forecasting/config.yml \
    --platform airflow \
    --schedule "0 6 * * *" \
    --output pipelines/
```

**Output**:
```
Generated: pipelines/forecast_dag.py
Schedule: Daily at 6am
Tasks: extract -> transform -> forecast -> load -> monitor
```

### Example 2: Simple Cron Script

```bash
python {baseDir}/scripts/generate_pipeline.py \
    --config forecasting/config.yml \
    --platform cron \
    --output pipelines/
```
