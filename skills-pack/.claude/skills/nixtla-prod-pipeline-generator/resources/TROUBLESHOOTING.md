**Solution**:
```
Run nixtla-experiment-architect first to set up experiments:

1. "Set up a forecasting experiment"
2. Complete experiment setup
3. Run this skill again
```

### Issue 2: Database connection errors

**Symptom**: Extract or load tasks fail with connection errors

**Solution**:
```python
# Test connection strings
import sqlalchemy

# Test source
engine = sqlalchemy.create_engine(os.getenv('FORECAST_DATA_SOURCE'))
engine.connect()  # Should not raise error

# Test destination
engine = sqlalchemy.create_engine(os.getenv('FORECAST_DESTINATION'))
engine.connect()  # Should not raise error
```

### Issue 3: Airflow can't import dependencies

**Symptom**: Tasks fail with "ModuleNotFoundError"

**Solution**:
```
Install dependencies in Airflow environment:

# If using Docker:
docker exec -it airflow-worker pip install nixtla statsforecast

# Or add to requirements.txt and rebuild
echo "nixtla" >> requirements.txt
echo "statsforecast" >> requirements.txt
docker-compose build
```

---

## Best Practices

### 1. Start with Staging Environment

