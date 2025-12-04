environments:
  staging:
    data_source: "postgresql://staging-db/..."
    destination: "postgresql://staging-db/..."
  production:
    data_source: "postgresql://prod-db/..."
    destination: "postgresql://prod-db/..."
```

### 2. Implement Proper Logging

All tasks should log key metrics:
```python
logging.info(f"Extracted {row_count} rows")
logging.info(f"Forecast SMAPE: {smape:.2f}%")
logging.warning(f"Drift detected: {drift_pct:.1f}% change")
```

### 3. Configure Alerts

Set up alerts for failures and quality issues:
- Airflow: email_on_failure in DAG config
- Prefect: Automation rules
- Cron: Pipe errors to monitoring system

### 4. Version Control Pipeline Code

Treat pipeline code as production code:
```bash
git add pipelines/
git commit -m "feat(pipelines): add TimeGPT production pipeline"
git push
```

### 5. Monitor Costs

TimeGPT API calls cost money:
- Track API usage via Nixtla dashboard
- Implement fallback to free baselines
- Set budget alerts

---

## Related Skills

Works well with:
- **nixtla-experiment-architect**: Creates the experiments this skill productionizes
- **nixtla-timegpt-finetune-lab**: Fine-tuned models can be deployed in pipelines
