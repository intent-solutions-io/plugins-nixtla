# TimeGPT-2 Migrator Examples

## Example 1: Basic Migration

**Before (TimeGPT-1)**:
```python
from timegpt import TimeGPT
timegpt = TimeGPT()
forecast = timegpt.forecast(data, h=24)
```

**After (TimeGPT-2)**:
```python
from nixtla import NixtlaClient
import os
client = NixtlaClient(api_key=os.getenv('NIXTLA_TIMEGPT_API_KEY'))
forecast = client.forecast(df=data, h=24, freq='H')
```

## Example 2: Configuration Update

**Before (config.json)**:
```json
{
  "model": "timegpt-1",
  "horizon": 24
}
```

**After (timegpt2_config.yaml)**:
```yaml
api_key: YOUR_API_KEY_HERE
model_name: TimeGPT-2
frequency: H
forecast_horizon: 24
data_format: Nixtla
```

## Example 3: Full Migration Workflow

Execute all migration steps in sequence for a complete codebase migration.

```bash
# Step 1: Analyze codebase for TimeGPT-1 usage
python {baseDir}/scripts/analyze_codebase.py ./my_project

# Step 2: Check data schema compatibility
python {baseDir}/scripts/compatibility_check.py --data ./data/sample.csv

# Step 3: Apply migration (review migration_report.txt first)
python {baseDir}/scripts/apply_migration.py ./my_project/main.py

# Step 4: Generate updated configuration
python {baseDir}/scripts/generate_config.py
```

## Example 4: Partial Migration (Single File)

Migrate a single script file while preserving the rest of the codebase.

```bash
# Analyze just one file
python {baseDir}/scripts/analyze_codebase.py ./my_project/forecaster.py

# Apply migration to that file only
python {baseDir}/scripts/apply_migration.py ./my_project/forecaster.py
```

Review the generated `migration_report.txt` before committing changes to version control. The report lists all automated replacements made and any manual changes still required.
