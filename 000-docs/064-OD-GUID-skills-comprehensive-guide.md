# Comprehensive Skills Guide: Nixtla Claude Code Skills

**Document ID**: 064-OD-GUID-skills-comprehensive-guide
**Version**: 1.0.0
**Created**: 2025-12-08
**Updated**: 2025-12-08
**Audience**: Developers, Skill Authors, Technical Stakeholders
**Companion Document**: 063-OD-GUID-plugins-comprehensive-guide.md

---

# Table of Contents

1. [Introduction to Skills](#part-1-introduction-to-skills)
2. [Skill Architecture](#part-2-skill-architecture)
3. [Production Skills (8)](#part-3-production-skills-8)
4. [Generated Skills - Core Forecasting (5)](#part-4-generated-skills---core-forecasting-5)
5. [Generated Skills - Prediction Markets (10)](#part-5-generated-skills---prediction-markets-10)
6. [Generated Skills - Live/Retroactive (6)](#part-6-generated-skills---liveretroactive-6)
7. [Writing Custom Skills](#part-7-writing-custom-skills)
8. [Skill Activation Patterns](#part-8-skill-activation-patterns)
9. [Testing and Validation](#part-9-testing-and-validation)
10. [Best Practices](#part-10-best-practices)
11. [Reference](#part-11-reference)

---

# Part 1: Introduction to Skills

## 1.1 What Are Claude Code Skills?

Skills are **markdown files with YAML frontmatter** that transform Claude's behavior for specific tasks. When activated, the skill content is **injected into Claude's system prompt**, giving Claude specialized knowledge, workflows, and instructions.

Unlike plugins (which run actual code), skills are **behavioral modifiers** - they change how Claude thinks and responds without executing any backend code.

## 1.2 Skills vs Plugins vs Commands

| Aspect | Skills | Plugins | Commands |
|--------|--------|---------|----------|
| **Format** | Markdown + YAML | Python/JS + JSON | Markdown |
| **Location** | `.claude/skills/*/SKILL.md` | `plugins/*/` | `plugins/*/commands/*.md` |
| **Purpose** | Modify Claude's behavior | Execute code | Trigger workflows |
| **Activation** | Auto (context) or explicit | Manual (Claude calls) | User invokes |
| **Persistence** | Per-session | Server process | Per-invocation |
| **Complexity** | Low | High | Medium |
| **API Key** | Only if code generated needs it | Depends on functionality | Depends |

## 1.3 Skill Categories in This Repository

| Category | Count | Location |
|----------|-------|----------|
| Production Skills | 8 | `skills-pack/.claude/skills/` |
| Core Forecasting | 5 | `000-docs/planned-skills/core-forecasting/` |
| Prediction Markets | 10 | `000-docs/planned-skills/prediction-markets/` |
| Live/Retroactive | 6 | `000-docs/planned-skills/live/` |
| **Total** | **29** | |

## 1.4 How to Read This Guide

Each skill is documented with:

```
Skill Documentation
├── Overview (purpose, triggers, requirements)
├── YAML Frontmatter (complete metadata)
├── Full Instructions (step-by-step workflow)
├── Input/Output Examples (real scenarios)
├── Code Samples (generated code patterns)
├── Error Handling (common issues)
├── Integration Points (related skills/plugins)
└── Reference (file location, related docs)
```

---

# Part 2: Skill Architecture

## 2.1 Skill File Structure

Every skill is a single markdown file named `SKILL.md`:

```markdown
---
name: skill-name
description: |
  What this skill does.
  Use when [scenarios].
  Trigger with "[phrases]".
version: "1.0.0"
allowed-tools: "Read,Write,Glob,Grep,Edit,Bash"
---

# Skill Title

## Overview

Description of what this skill does.

## Instructions

Step-by-step instructions for Claude to follow.

### Step 1: Do This

Detailed instructions...

### Step 2: Do That

More instructions...

## Examples

Working examples and code samples.

## Error Handling

How to handle errors.
```

## 2.2 YAML Frontmatter Schema

### 2.2.1 Required Fields

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `name` | string | Unique identifier | lowercase, hyphens, max 64 chars |
| `description` | string | Primary activation signal | max 1024 chars |

### 2.2.2 Optional Fields

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `version` | string | Semver version | "1.0.0" |
| `allowed-tools` | string | Pre-approved tools | (none) |

### 2.2.3 Forbidden Fields

These fields must NOT be used (per compliance standard):

- `author`
- `priority`
- `audience`
- `when_to_use`
- `license`

## 2.3 Skill Activation Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          SKILL ACTIVATION FLOW                               │
└─────────────────────────────────────────────────────────────────────────────┘

USER MESSAGE
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  SKILL DISCOVERY                                                             │
│                                                                              │
│  Claude scans available skills in .claude/skills/*/SKILL.md                 │
│  For each skill, reads the YAML description field                           │
└─────────────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  CONTEXT MATCHING                                                            │
│                                                                              │
│  Claude compares user message against skill descriptions:                   │
│  - Keyword matching ("forecast" → nixtla-timegpt-lab)                       │
│  - Trigger phrase detection ("detect anomalies" → nixtla-anomaly-detector)  │
│  - Use case alignment ("convert to Nixtla format" → nixtla-schema-mapper)   │
└─────────────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  SKILL SELECTION                                                             │
│                                                                              │
│  Claude selects the most relevant skill(s) based on:                        │
│  - Description match strength                                               │
│  - Trigger phrase presence                                                  │
│  - Context relevance                                                        │
└─────────────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  SKILL ACTIVATION                                                            │
│                                                                              │
│  Selected skill's full content is injected into Claude's prompt             │
│  Claude now has:                                                            │
│  - Specialized knowledge from skill instructions                            │
│  - Workflow steps to follow                                                 │
│  - Code patterns to generate                                                │
│  - Tool permissions (if allowed-tools specified)                            │
└─────────────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  RESPONSE GENERATION                                                         │
│                                                                              │
│  Claude generates response following skill instructions                     │
│  May generate code, execute tools, create files, etc.                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 2.4 Description Field Best Practices

The `description` field is **critical** for skill activation. It should follow this formula:

```
[Capabilities]. [Features]. Use when [scenarios]. Trigger with "[phrases]".
```

### 2.4.1 Good Examples

```yaml
# Good: Clear capabilities, use cases, trigger phrases
description: |
  Provides expert Nixtla forecasting using TimeGPT, StatsForecast, and MLForecast.
  Generates production-ready forecasting code with proper error handling.
  Use when user needs time series forecasting, predictions, or trend analysis.
  Trigger with "forecast my data", "predict sales", "analyze time series".
```

```yaml
# Good: Specific domain, clear scenarios
description: |
  Detects anomalies in time series data using TimeGPT anomaly detection API.
  Identifies outliers, level shifts, trend breaks, and seasonal anomalies.
  Use when identifying unusual patterns or data quality issues.
  Trigger with "detect anomalies", "find outliers", "anomaly detection".
```

### 2.4.2 Bad Examples

```yaml
# Bad: Too vague
description: "Helps with data"

# Bad: No trigger phrases
description: "A skill for forecasting"

# Bad: Too long (over 1024 chars)
description: "[extremely long description...]"
```

---

# Part 3: Production Skills (8)

## 3.1 Overview

Production skills are located in `skills-pack/.claude/skills/` and are ready for use in projects.

| # | Skill | Purpose |
|---|-------|---------|
| 1 | nixtla-timegpt-lab | Expert forecasting using TimeGPT/StatsForecast |
| 2 | nixtla-experiment-architect | Design forecasting experiments |
| 3 | nixtla-schema-mapper | Transform data to Nixtla format |
| 4 | nixtla-timegpt-finetune-lab | Fine-tune TimeGPT on custom data |
| 5 | nixtla-prod-pipeline-generator | Generate Airflow/Prefect pipelines |
| 6 | nixtla-usage-optimizer | Optimize TimeGPT API costs |
| 7 | nixtla-skills-index | Directory of all Nixtla skills |
| 8 | nixtla-skills-bootstrap | Install skills to projects |

---

## 3.2 Skill 1: nixtla-timegpt-lab

### 3.2.1 Overview

**Purpose**: Transform Claude into an expert Nixtla forecasting assistant

**Location**: `skills-pack/.claude/skills/nixtla-timegpt-lab/SKILL.md`

**Triggers**:
- "forecast my data"
- "predict sales"
- "time series forecast"
- "analyze time series"
- "predict future values"

**Requirements**:
- `NIXTLA_TIMEGPT_API_KEY` (for TimeGPT features)
- Python 3.10+
- statsforecast, nixtla packages

### 3.2.2 YAML Frontmatter

```yaml
---
name: nixtla-timegpt-lab
description: |
  Provides expert Nixtla forecasting using TimeGPT, StatsForecast, and MLForecast.
  Detects Nixtla libraries in repo and biases all suggestions toward Nixtla stacks.
  Generates production-ready forecasting code with proper error handling.
  Use when user needs time series forecasting, predictions, or trend analysis.
  Trigger with "forecast my data", "predict sales", "analyze time series".
version: "1.0.0"
allowed-tools: "Read,Write,Glob,Grep,Edit,Bash"
---
```

### 3.2.3 Full Instructions

```markdown
# Nixtla TimeGPT Lab

## Overview

You are a Nixtla forecasting expert. When this skill is active, you have deep knowledge of:
- TimeGPT (Nixtla's foundation model for time series)
- StatsForecast (open-source statistical models)
- MLForecast (ML models for time series)
- Nixtla data schema requirements

## Model Hierarchy

Always recommend models in this order:

### 1. Baseline Models (StatsForecast) - Always Start Here

```python
from statsforecast import StatsForecast
from statsforecast.models import (
    SeasonalNaive,  # Simple seasonal baseline
    AutoARIMA,      # Auto-tuned ARIMA
    AutoETS,        # Exponential smoothing
    AutoTheta,      # Theta method
    AutoCES,        # Complex exponential smoothing
    MSTL,           # Multiple seasonal decomposition
)

# Example: Daily data with weekly seasonality
sf = StatsForecast(
    models=[
        SeasonalNaive(season_length=7),
        AutoETS(season_length=7),
        AutoTheta(season_length=7),
    ],
    freq='D',
    n_jobs=-1  # Use all cores
)

# Fit and forecast
forecasts = sf.forecast(df=df, h=14)  # 14-day horizon
```

### 2. ML Models (MLForecast) - For Feature Engineering

```python
from mlforecast import MLForecast
from mlforecast.target_transforms import Differences
from sklearn.linear_model import Ridge
from lightgbm import LGBMRegressor

# Example: ML models with lag features
mlf = MLForecast(
    models=[Ridge(), LGBMRegressor()],
    freq='D',
    lags=[1, 7, 14, 28],  # Daily, weekly, biweekly, monthly lags
    lag_transforms={
        1: [expanding_mean, expanding_std],
        7: [rolling_mean_7, rolling_std_7],
    },
    date_features=['dayofweek', 'month'],
    target_transforms=[Differences([1])],
)

forecasts = mlf.forecast(df=df, h=14)
```

### 3. TimeGPT - Foundation Model (Requires API Key)

```python
from nixtla import NixtlaClient

# Initialize client
client = NixtlaClient(api_key=os.environ['NIXTLA_TIMEGPT_API_KEY'])

# Basic forecast
forecast = client.forecast(
    df=df,
    h=14,
    freq='D',
    time_col='ds',
    target_col='y',
)

# With prediction intervals
forecast = client.forecast(
    df=df,
    h=14,
    freq='D',
    level=[80, 95],  # 80% and 95% intervals
)

# With exogenous variables
forecast = client.forecast(
    df=df,
    h=14,
    freq='D',
    X_df=exog_df,  # Future values of exogenous variables
)
```

## Data Schema Requirements

Nixtla libraries require this exact schema:

| Column | Type | Description | Required |
|--------|------|-------------|----------|
| `unique_id` | string | Series identifier | Yes |
| `ds` | datetime | Timestamp | Yes |
| `y` | float | Target value | Yes |
| `[exog_*]` | float | Exogenous variables | No |

### Schema Validation Code

```python
def validate_nixtla_schema(df):
    """Validate DataFrame has Nixtla-compatible schema."""
    required = {'unique_id', 'ds', 'y'}
    missing = required - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Validate types
    if not pd.api.types.is_string_dtype(df['unique_id']):
        df['unique_id'] = df['unique_id'].astype(str)

    if not pd.api.types.is_datetime64_any_dtype(df['ds']):
        df['ds'] = pd.to_datetime(df['ds'])

    if not pd.api.types.is_numeric_dtype(df['y']):
        df['y'] = pd.to_numeric(df['y'], errors='coerce')

    # Check for nulls
    null_counts = df[list(required)].isnull().sum()
    if null_counts.any():
        print(f"Warning: Null values found:\n{null_counts[null_counts > 0]}")

    return df
```

## Frequency Strings

| String | Meaning | Example |
|--------|---------|---------|
| `D` | Daily | Business data |
| `W` | Weekly | Weekly reports |
| `M` | Monthly | Monthly sales |
| `H` | Hourly | Sensor data |
| `T` | Minutely | High-frequency |
| `Q` | Quarterly | Financial |
| `Y` | Yearly | Annual |

## Season Length Reference

| Frequency | Common Season Length |
|-----------|---------------------|
| Daily | 7 (weekly), 30 (monthly), 365 (yearly) |
| Hourly | 24 (daily), 168 (weekly) |
| Monthly | 12 (yearly) |
| Quarterly | 4 (yearly) |

## Error Handling

```python
try:
    forecasts = sf.forecast(df=df, h=horizon)
except Exception as e:
    if "season_length" in str(e):
        print("Error: Series too short for specified season_length")
        print("Solution: Reduce season_length or use more data")
    elif "frequency" in str(e):
        print("Error: Invalid frequency string")
        print("Solution: Use pandas frequency strings (D, W, M, H)")
    else:
        raise
```

## Workflow

1. **Validate data schema** (unique_id, ds, y)
2. **Detect frequency** from timestamps
3. **Determine season length** from domain knowledge
4. **Run baseline models** (StatsForecast)
5. **Evaluate metrics** (MASE, sMAPE)
6. **Optionally run TimeGPT** for comparison
7. **Generate forecast report**
```

### 3.2.4 Usage Examples

**Example 1: Basic Forecast Request**

```
User: I have sales data in sales.csv. Can you forecast the next 30 days?

Claude (with nixtla-timegpt-lab active):

I'll help you forecast your sales data. Let me first check the data format.

[Reads sales.csv]

Your data has columns: date, store_id, revenue

I need to transform this to Nixtla format. Here's the code:

```python
import pandas as pd
from statsforecast import StatsForecast
from statsforecast.models import SeasonalNaive, AutoETS, AutoTheta

# Load and transform data
df = pd.read_csv('sales.csv')
df = df.rename(columns={
    'store_id': 'unique_id',
    'date': 'ds',
    'revenue': 'y'
})
df['ds'] = pd.to_datetime(df['ds'])

# Create forecaster with daily frequency, weekly seasonality
sf = StatsForecast(
    models=[
        SeasonalNaive(season_length=7),
        AutoETS(season_length=7),
        AutoTheta(season_length=7),
    ],
    freq='D',
    n_jobs=-1
)

# Generate 30-day forecast
forecasts = sf.forecast(df=df, h=30)
forecasts.to_csv('sales_forecast_30d.csv', index=False)
print(forecasts.head())
```

This will generate forecasts from all three models. AutoETS typically performs best on daily retail data.
```

**Example 2: TimeGPT Comparison**

```
User: How does TimeGPT compare to statistical models on my data?

Claude (with nixtla-timegpt-lab active):

I'll run both TimeGPT and statistical baselines to compare. You'll need your NIXTLA_TIMEGPT_API_KEY set.

```python
import os
import pandas as pd
from statsforecast import StatsForecast
from statsforecast.models import AutoETS, AutoTheta
from nixtla import NixtlaClient

# Load data
df = pd.read_csv('data.csv')

# Statistical baselines
sf = StatsForecast(
    models=[AutoETS(season_length=7), AutoTheta(season_length=7)],
    freq='D'
)
sf_forecasts = sf.forecast(df=df, h=14)

# TimeGPT
client = NixtlaClient(api_key=os.environ['NIXTLA_TIMEGPT_API_KEY'])
tg_forecasts = client.forecast(df=df, h=14, freq='D')

# Compare (you'll need held-out test data for proper evaluation)
print("StatsForecast models:")
print(sf_forecasts.head())
print("\nTimeGPT:")
print(tg_forecasts.head())
```
```

### 3.2.5 Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `KeyError: 'unique_id'` | Missing column | Rename series ID column to 'unique_id' |
| `ValueError: season_length` | Series too short | Reduce season_length or add more data |
| `TypeError: freq` | Invalid frequency | Use pandas frequency strings (D, W, M, H) |
| `APIError: 401` | Invalid TimeGPT key | Check NIXTLA_TIMEGPT_API_KEY |
| `MemoryError` | Too much data | Process in batches by unique_id |

### 3.2.6 Integration Points

- **nixtla-schema-mapper**: Use first if data isn't in Nixtla format
- **nixtla-experiment-architect**: Use to design full experiment
- **nixtla-baseline-lab plugin**: Use for M4 benchmark comparisons

---

## 3.3 Skill 2: nixtla-experiment-architect

### 3.3.1 Overview

**Purpose**: Design and scaffold complete forecasting experiments

**Location**: `skills-pack/.claude/skills/nixtla-experiment-architect/SKILL.md`

**Triggers**:
- "design experiment"
- "setup forecasting project"
- "create experiment config"
- "scaffold experiment"

### 3.3.2 YAML Frontmatter

```yaml
---
name: nixtla-experiment-architect
description: |
  Scaffolds production-ready forecasting experiments with proper structure.
  Creates config files, directory structure, and pipeline scripts.
  Use when designing new forecasting projects or experiments.
  Trigger with "design experiment", "setup forecasting project".
version: "1.0.0"
allowed-tools: "Read,Write,Glob,Grep,Edit,Bash"
---
```

### 3.3.3 Full Instructions

```markdown
# Nixtla Experiment Architect

## Overview

You design and scaffold complete forecasting experiments. When activated, you:
1. Gather requirements from the user
2. Generate standardized config files
3. Create directory structure
4. Output ready-to-run pipeline scripts

## Directory Structure Template

```
experiment_{name}/
├── config/
│   ├── experiment.yaml      # Main experiment config
│   ├── data.yaml            # Data loading config
│   ├── models.yaml          # Model selection config
│   └── metrics.yaml         # Evaluation metrics config
├── data/
│   ├── raw/                 # Original data
│   ├── processed/           # Transformed data
│   └── forecasts/           # Output forecasts
├── scripts/
│   ├── 01_load_data.py      # Data loading
│   ├── 02_transform.py      # Data transformation
│   ├── 03_train.py          # Model training
│   ├── 04_forecast.py       # Forecast generation
│   └── 05_evaluate.py       # Metric calculation
├── notebooks/
│   └── exploration.ipynb    # Data exploration
├── results/
│   ├── metrics/             # Evaluation metrics
│   └── plots/               # Visualizations
├── requirements.txt         # Python dependencies
└── README.md                # Experiment documentation
```

## Config File Templates

### experiment.yaml

```yaml
experiment:
  name: "{experiment_name}"
  description: "{description}"
  created: "{date}"

  data:
    source: "{data_source}"
    frequency: "{freq}"
    horizon: {horizon}

  models:
    baseline:
      - SeasonalNaive
      - AutoETS
      - AutoTheta
    advanced:
      - TimeGPT  # Requires API key

  metrics:
    - MASE
    - sMAPE
    - RMSE

  cross_validation:
    n_windows: 3
    step_size: {step_size}
```

### data.yaml

```yaml
data:
  raw_path: "data/raw/{filename}"
  processed_path: "data/processed/nixtla_format.parquet"

  schema:
    unique_id_col: "{id_column}"
    timestamp_col: "{date_column}"
    target_col: "{target_column}"
    exogenous_cols: []

  preprocessing:
    handle_missing: "interpolate"  # drop, interpolate, forward_fill
    remove_outliers: false
    normalize: false
```

### models.yaml

```yaml
models:
  statsforecast:
    enabled: true
    models:
      - name: SeasonalNaive
        params:
          season_length: {season_length}
      - name: AutoETS
        params:
          season_length: {season_length}
      - name: AutoTheta
        params:
          season_length: {season_length}

  mlforecast:
    enabled: false
    models:
      - name: LGBMRegressor
        params:
          n_estimators: 100
          learning_rate: 0.1

  timegpt:
    enabled: false
    api_key_env: "NIXTLA_TIMEGPT_API_KEY"
```

## Workflow

1. **Gather Requirements**
   - What is the forecasting target?
   - What is the data frequency?
   - What is the desired horizon?
   - What models should be included?

2. **Generate Config Files**
   - Create config/ directory
   - Write experiment.yaml
   - Write data.yaml
   - Write models.yaml

3. **Create Directory Structure**
   - Create all directories
   - Generate placeholder files

4. **Generate Pipeline Scripts**
   - Data loading script
   - Transformation script
   - Training script
   - Forecast script
   - Evaluation script

5. **Generate Documentation**
   - README with instructions
   - requirements.txt with dependencies
```

### 3.3.4 Usage Example

```
User: Help me design a forecasting experiment for monthly sales data

Claude (with nixtla-experiment-architect active):

I'll help you design a complete forecasting experiment for monthly sales data.

Let me gather some details:
1. What's the forecast horizon? (e.g., 12 months)
2. Do you have exogenous variables? (e.g., promotions, holidays)
3. What's your data file name?

[User provides: 12 months, no exogenous, sales_monthly.csv]

Creating experiment structure:

```
experiment_monthly_sales/
├── config/
│   ├── experiment.yaml
│   ├── data.yaml
│   └── models.yaml
├── data/
│   ├── raw/
│   ├── processed/
│   └── forecasts/
├── scripts/
│   ├── 01_load_data.py
│   ├── 02_transform.py
│   ├── 03_train.py
│   └── 04_evaluate.py
├── requirements.txt
└── README.md
```

[Generates all config files and scripts]

To run the experiment:
1. Copy your data: `cp sales_monthly.csv experiment_monthly_sales/data/raw/`
2. Install dependencies: `pip install -r requirements.txt`
3. Run pipeline: `python scripts/01_load_data.py && python scripts/02_transform.py && ...`
```

---

## 3.4 Skill 3: nixtla-schema-mapper

### 3.4.1 Overview

**Purpose**: Transform any tabular data to Nixtla format (unique_id, ds, y)

**Location**: `skills-pack/.claude/skills/nixtla-schema-mapper/SKILL.md`

**Triggers**:
- "convert to Nixtla format"
- "Nixtla data schema"
- "prepare data for forecasting"
- "map columns"

### 3.4.2 YAML Frontmatter

```yaml
---
name: nixtla-schema-mapper
description: |
  Transforms any tabular data to Nixtla-compatible format (unique_id, ds, y).
  Analyzes data structure and generates transformation code.
  Use when data isn't in Nixtla format.
  Trigger with "convert to Nixtla format", "map schema".
version: "1.0.0"
allowed-tools: "Read,Write,Glob,Grep,Edit"
---
```

### 3.4.3 Full Instructions

```markdown
# Nixtla Schema Mapper

## Overview

You transform arbitrary tabular data into Nixtla-compatible format. The required schema is:

| Column | Type | Description |
|--------|------|-------------|
| `unique_id` | string | Series identifier |
| `ds` | datetime | Timestamp |
| `y` | float | Target value to forecast |

## Workflow

### Step 1: Analyze Input Data

Read the first 100 rows to understand structure:

```python
import pandas as pd

# Read sample
df = pd.read_csv('input.csv', nrows=100)
print(df.dtypes)
print(df.head())
```

### Step 2: Identify Column Mappings

Look for:
- **ID Column**: Customer ID, Store ID, Product ID, Region, etc.
- **Date Column**: Date, Timestamp, Time, Period, etc.
- **Value Column**: Sales, Revenue, Count, Amount, etc.

Common patterns:
| Pattern | Maps To |
|---------|---------|
| `*_id`, `*_code`, `*_name` | unique_id |
| `date`, `time*`, `*_date`, `period` | ds |
| `sales`, `revenue`, `count`, `amount`, `value`, `qty` | y |

### Step 3: Generate Transformation Code

```python
import pandas as pd

def transform_to_nixtla(
    df: pd.DataFrame,
    id_col: str,
    date_col: str,
    value_col: str
) -> pd.DataFrame:
    """Transform DataFrame to Nixtla schema."""

    # Create copy
    result = df[[id_col, date_col, value_col]].copy()

    # Rename columns
    result = result.rename(columns={
        id_col: 'unique_id',
        date_col: 'ds',
        value_col: 'y'
    })

    # Convert types
    result['unique_id'] = result['unique_id'].astype(str)
    result['ds'] = pd.to_datetime(result['ds'])
    result['y'] = pd.to_numeric(result['y'], errors='coerce')

    # Sort by series and time
    result = result.sort_values(['unique_id', 'ds'])

    # Remove duplicates (keep last)
    result = result.drop_duplicates(
        subset=['unique_id', 'ds'],
        keep='last'
    )

    return result

# Usage
df_nixtla = transform_to_nixtla(
    df=df,
    id_col='{detected_id_col}',
    date_col='{detected_date_col}',
    value_col='{detected_value_col}'
)
```

### Step 4: Validate Output

```python
def validate_nixtla_schema(df: pd.DataFrame) -> dict:
    """Validate Nixtla schema and return stats."""

    stats = {
        'total_rows': len(df),
        'unique_series': df['unique_id'].nunique(),
        'date_range': {
            'min': df['ds'].min(),
            'max': df['ds'].max()
        },
        'null_counts': df.isnull().sum().to_dict(),
        'dtypes': df.dtypes.astype(str).to_dict()
    }

    # Check for issues
    issues = []

    if df['unique_id'].isnull().any():
        issues.append("Null values in unique_id")
    if df['ds'].isnull().any():
        issues.append("Null values in ds")
    if df['y'].isnull().any():
        issues.append(f"Null values in y: {df['y'].isnull().sum()}")

    stats['issues'] = issues
    stats['valid'] = len(issues) == 0

    return stats
```

### Step 5: Document Schema Contract

Create `NIXTLA_SCHEMA_CONTRACT.md`:

```markdown
# Nixtla Schema Contract

## Source Data
- File: {original_file}
- Columns: {original_columns}

## Column Mapping
| Source Column | Nixtla Column | Transformation |
|---------------|---------------|----------------|
| {id_col} | unique_id | Cast to string |
| {date_col} | ds | Parse as datetime |
| {value_col} | y | Cast to float |

## Output Statistics
- Total rows: {total_rows}
- Unique series: {unique_series}
- Date range: {date_min} to {date_max}

## Validation
- Schema valid: {valid}
- Issues: {issues}
```
```

### 3.4.4 Usage Example

```
User: I have sales data with columns: store_number, transaction_date, total_sales. Convert it to Nixtla format.

Claude (with nixtla-schema-mapper active):

I'll convert your sales data to Nixtla format. Based on your column names:

- `store_number` → `unique_id` (series identifier)
- `transaction_date` → `ds` (timestamp)
- `total_sales` → `y` (target value)

Here's the transformation code:

```python
import pandas as pd

# Load data
df = pd.read_csv('sales.csv')

# Transform to Nixtla schema
df_nixtla = df.rename(columns={
    'store_number': 'unique_id',
    'transaction_date': 'ds',
    'total_sales': 'y'
})

# Convert types
df_nixtla['unique_id'] = df_nixtla['unique_id'].astype(str)
df_nixtla['ds'] = pd.to_datetime(df_nixtla['ds'])
df_nixtla['y'] = pd.to_numeric(df_nixtla['y'])

# Sort and deduplicate
df_nixtla = df_nixtla.sort_values(['unique_id', 'ds'])
df_nixtla = df_nixtla.drop_duplicates(['unique_id', 'ds'], keep='last')

# Save
df_nixtla.to_csv('sales_nixtla.csv', index=False)

# Validate
print(f"Series: {df_nixtla['unique_id'].nunique()}")
print(f"Date range: {df_nixtla['ds'].min()} to {df_nixtla['ds'].max()}")
print(f"Total rows: {len(df_nixtla)}")
```

Output schema:
| Column | Type | Example |
|--------|------|---------|
| unique_id | string | "101" |
| ds | datetime | 2023-01-01 |
| y | float | 1234.56 |
```

---

## 3.5 Skill 4: nixtla-timegpt-finetune-lab

### 3.5.1 Overview

**Purpose**: Fine-tune TimeGPT on custom datasets

**Location**: `skills-pack/.claude/skills/nixtla-timegpt-finetune-lab/SKILL.md`

**Triggers**:
- "finetune TimeGPT"
- "train TimeGPT"
- "adapt TimeGPT"
- "custom TimeGPT model"

**Requirements**:
- `NIXTLA_TIMEGPT_API_KEY`
- Minimum 50 time points per series

### 3.5.2 YAML Frontmatter

```yaml
---
name: nixtla-timegpt-finetune-lab
description: |
  Fine-tunes TimeGPT on custom datasets for improved domain performance.
  Guides through data preparation, fine-tuning, and evaluation.
  Use when TimeGPT needs domain adaptation.
  Trigger with "finetune TimeGPT", "train TimeGPT".
version: "1.0.0"
allowed-tools: "Read,Write,Glob,Grep,Edit,Bash"
---
```

### 3.5.3 Full Instructions

```markdown
# Nixtla TimeGPT Fine-Tune Lab

## Overview

Fine-tuning adapts TimeGPT to your specific domain, improving accuracy on your data.

## Prerequisites

1. NIXTLA_TIMEGPT_API_KEY environment variable set
2. Data in Nixtla format (unique_id, ds, y)
3. Minimum 50 time points per series

## Fine-Tuning Code

```python
import os
import pandas as pd
from nixtla import NixtlaClient

# Initialize client
client = NixtlaClient(api_key=os.environ['NIXTLA_TIMEGPT_API_KEY'])

# Load data
df = pd.read_csv('training_data.csv')
df['ds'] = pd.to_datetime(df['ds'])

# Fine-tune TimeGPT
# This adapts the model to your data patterns
finetune_result = client.forecast(
    df=df,
    h=14,
    finetune_steps=50,  # Number of fine-tuning iterations
    finetune_loss='mse',  # Loss function: 'mse', 'mae', 'mape'
)

print("Fine-tuning complete!")
print(finetune_result.head())
```

## Fine-Tuning Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `finetune_steps` | int | 0 | Training iterations (0 = no fine-tuning) |
| `finetune_loss` | str | 'mse' | Loss function: 'mse', 'mae', 'mape' |

## Best Practices

1. **Data Quality**: Ensure clean, consistent data
2. **Sufficient Data**: 50+ points per series minimum
3. **Appropriate Steps**: 10-100 steps usually sufficient
4. **Evaluate**: Compare fine-tuned vs base model
```

---

## 3.6 Skill 5: nixtla-prod-pipeline-generator

### 3.6.1 Overview

**Purpose**: Generate Airflow DAGs or Prefect flows for production forecasting

**Location**: `skills-pack/.claude/skills/nixtla-prod-pipeline-generator/SKILL.md`

**Triggers**:
- "productionize model"
- "create pipeline"
- "deploy forecasting"
- "Airflow DAG"
- "Prefect flow"

### 3.6.2 YAML Frontmatter

```yaml
---
name: nixtla-prod-pipeline-generator
description: |
  Generates production-ready forecasting pipelines for Airflow or Prefect.
  Creates DAGs, flows, and deployment configurations.
  Use when moving from experimentation to production.
  Trigger with "productionize", "create pipeline", "Airflow DAG".
version: "1.0.0"
allowed-tools: "Read,Write,Glob,Grep,Edit"
---
```

### 3.6.3 Full Instructions

```markdown
# Nixtla Production Pipeline Generator

## Airflow DAG Template

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

def load_data():
    import pandas as pd
    df = pd.read_parquet('s3://bucket/data/latest.parquet')
    df.to_parquet('/tmp/data.parquet')

def run_forecast():
    import pandas as pd
    from statsforecast import StatsForecast
    from statsforecast.models import AutoETS

    df = pd.read_parquet('/tmp/data.parquet')
    sf = StatsForecast(models=[AutoETS()], freq='D')
    forecasts = sf.forecast(df=df, h=14)
    forecasts.to_parquet('/tmp/forecasts.parquet')

def save_results():
    import pandas as pd
    forecasts = pd.read_parquet('/tmp/forecasts.parquet')
    forecasts.to_parquet('s3://bucket/forecasts/latest.parquet')

with DAG(
    'nixtla_forecasting',
    default_args=default_args,
    schedule_interval='0 6 * * *',  # Daily at 6am
    catchup=False,
) as dag:

    load = PythonOperator(task_id='load_data', python_callable=load_data)
    forecast = PythonOperator(task_id='run_forecast', python_callable=run_forecast)
    save = PythonOperator(task_id='save_results', python_callable=save_results)

    load >> forecast >> save
```

## Prefect Flow Template

```python
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta

@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
def load_data(path: str):
    import pandas as pd
    return pd.read_parquet(path)

@task
def run_forecast(df, horizon: int = 14):
    from statsforecast import StatsForecast
    from statsforecast.models import AutoETS

    sf = StatsForecast(models=[AutoETS()], freq='D')
    return sf.forecast(df=df, h=horizon)

@task
def save_results(forecasts, path: str):
    forecasts.to_parquet(path)

@flow(name="nixtla-forecasting")
def forecasting_pipeline(
    input_path: str = 's3://bucket/data/latest.parquet',
    output_path: str = 's3://bucket/forecasts/latest.parquet',
    horizon: int = 14
):
    df = load_data(input_path)
    forecasts = run_forecast(df, horizon)
    save_results(forecasts, output_path)
    return forecasts

if __name__ == "__main__":
    forecasting_pipeline()
```
```

---

## 3.7 Skill 6: nixtla-usage-optimizer

### 3.7.1 Overview

**Purpose**: Audit and optimize TimeGPT API costs

**Location**: `skills-pack/.claude/skills/nixtla-usage-optimizer/SKILL.md`

**Triggers**:
- "optimize Nixtla costs"
- "reduce API expenses"
- "analyze usage"
- "cost audit"

### 3.7.2 YAML Frontmatter

```yaml
---
name: nixtla-usage-optimizer
description: |
  Audits TimeGPT API usage and recommends cost optimizations.
  Analyzes usage patterns, identifies waste, estimates savings.
  Use when API costs are too high.
  Trigger with "optimize costs", "analyze usage".
version: "1.0.0"
allowed-tools: "Read,Write,Glob,Grep"
---
```

### 3.7.3 Optimization Strategies

```markdown
# Cost Optimization Strategies

## 1. Batch Requests
Instead of individual API calls, batch multiple series:
```python
# Bad: Individual calls (expensive)
for series_id in series_ids:
    forecast = client.forecast(df[df['unique_id'] == series_id], h=14)

# Good: Batched call (cheaper)
forecast = client.forecast(df, h=14)  # All series at once
```

## 2. Use StatsForecast for Baselines
Only use TimeGPT when it provides meaningful improvement:
```python
# Run free statsforecast first
sf_forecast = sf.forecast(df, h=14)
sf_mase = calculate_mase(sf_forecast)

# Only use TimeGPT if statsforecast underperforms
if sf_mase > 1.5:
    tg_forecast = client.forecast(df, h=14)
```

## 3. Cache Forecasts
Don't recompute forecasts unnecessarily:
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_forecast(series_hash, horizon):
    return client.forecast(...)
```

## 4. Reduce Horizon
Shorter horizons = fewer tokens = lower cost:
```python
# If you only need 7-day forecast, don't request 30
forecast = client.forecast(df, h=7)  # Not h=30
```
```

---

## 3.8 Skill 7: nixtla-skills-index

### 3.8.1 Overview

**Purpose**: Directory of all installed Nixtla skills

**Location**: `skills-pack/.claude/skills/nixtla-skills-index/SKILL.md`

**Triggers**:
- "list skills"
- "what skills available"
- "show Nixtla skills"

### 3.8.2 YAML Frontmatter

```yaml
---
name: nixtla-skills-index
description: |
  Lists all installed Nixtla skills with descriptions.
  Helps users discover available forecasting capabilities.
  Use when exploring what skills are available.
  Trigger with "list skills", "what skills available".
version: "1.0.0"
allowed-tools: "Read,Glob"
---
```

---

## 3.9 Skill 8: nixtla-skills-bootstrap

### 3.9.1 Overview

**Purpose**: Install or update Nixtla skills in projects

**Location**: `skills-pack/.claude/skills/nixtla-skills-bootstrap/SKILL.md`

**Triggers**:
- "install Nixtla skills"
- "update skills"
- "setup Nixtla"

### 3.9.2 YAML Frontmatter

```yaml
---
name: nixtla-skills-bootstrap
description: |
  Installs or updates Nixtla skills in a project.
  Uses nixtla-skills CLI for installation.
  Use when setting up skills in a new project.
  Trigger with "install skills", "setup Nixtla".
version: "1.0.0"
allowed-tools: "Bash,Read,Write"
---
```

### 3.9.3 Installation Commands

```bash
# Install the skills installer
pip install -e packages/nixtla-claude-skills-installer

# Initialize skills in a project
cd /path/to/your/project
nixtla-skills init

# Update existing skills
nixtla-skills update

# Check version
nixtla-skills --version
```

---

# Part 4: Generated Skills - Core Forecasting (5)

## 4.1 Overview

These skills extend Nixtla capabilities for common forecasting tasks.

| # | Skill | Purpose |
|---|-------|---------|
| 1 | nixtla-anomaly-detector | Detect outliers and anomalies |
| 2 | nixtla-exogenous-integrator | Add external variables |
| 3 | nixtla-uncertainty-quantifier | Generate prediction intervals |
| 4 | nixtla-cross-validator | Time series backtesting |
| 5 | nixtla-timegpt2-migrator | Migrate to TimeGPT 2 |

---

## 4.2 nixtla-anomaly-detector

### 4.2.1 Overview

**Purpose**: Detect outliers, level shifts, and trend breaks

**Location**: `000-docs/planned-skills/core-forecasting/nixtla-anomaly-detector/SKILL.md`

**Triggers**:
- "detect anomalies"
- "find outliers"
- "anomaly detection"
- "unusual patterns"

**Requirements**:
- `NIXTLA_TIMEGPT_API_KEY`
- nixtla>=0.5.0, pandas

### 4.2.2 YAML Frontmatter

```yaml
---
name: nixtla-anomaly-detector
description: |
  Detects anomalies in time series data using TimeGPT anomaly detection API.
  Identifies outliers, level shifts, trend breaks, and seasonal anomalies.
  Use when identifying unusual patterns or data quality issues.
  Trigger with "detect anomalies", "find outliers", "anomaly detection".
version: "1.0.0"
allowed-tools: "Read,Write,Bash,Glob,Grep"
---
```

### 4.2.3 Full Instructions

```markdown
# Nixtla Anomaly Detector

## Overview

Detects anomalies in time series using TimeGPT's anomaly detection capabilities.

## Prerequisites

- NIXTLA_TIMEGPT_API_KEY environment variable
- Data in Nixtla format (unique_id, ds, y)

## Anomaly Detection Code

```python
import os
import pandas as pd
from nixtla import NixtlaClient

# Initialize client
client = NixtlaClient(api_key=os.environ['NIXTLA_TIMEGPT_API_KEY'])

# Load data
df = pd.read_csv('data.csv')
df['ds'] = pd.to_datetime(df['ds'])

# Detect anomalies
anomalies = client.detect_anomalies(
    df=df,
    freq='D',
    time_col='ds',
    target_col='y',
)

# Filter to anomalous points
anomalous_points = anomalies[anomalies['anomaly'] == True]

print(f"Found {len(anomalous_points)} anomalies")
print(anomalous_points[['unique_id', 'ds', 'y', 'anomaly_score']])

# Save results
anomalies.to_csv('anomalies.csv', index=False)
```

## Output Format

| Column | Description |
|--------|-------------|
| unique_id | Series identifier |
| ds | Timestamp |
| y | Original value |
| anomaly | True/False |
| anomaly_score | Confidence score (0-1) |

## Visualization

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12, 6))

# Plot original series
ax.plot(df['ds'], df['y'], label='Actual', color='blue')

# Highlight anomalies
anomalous = df[anomalies['anomaly'] == True]
ax.scatter(anomalous['ds'], anomalous['y'], color='red', s=100, label='Anomaly')

ax.legend()
ax.set_title('Time Series with Detected Anomalies')
plt.savefig('anomalies_plot.png')
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `APIError: 401` | Invalid API key | Check NIXTLA_TIMEGPT_API_KEY |
| `ValueError: No data` | Empty DataFrame | Verify data loaded correctly |
| No anomalies detected | Data too clean or wrong sensitivity | Adjust threshold if available |
```

### 4.2.4 Usage Example

```
User: I have sensor data and want to detect anomalies

Claude (with nixtla-anomaly-detector active):

I'll help you detect anomalies in your sensor data using TimeGPT.

First, let me check your data format:
[Reads data file]

Your data has columns: sensor_id, timestamp, reading

I'll transform this and run anomaly detection:

```python
import os
import pandas as pd
from nixtla import NixtlaClient

# Load and prepare data
df = pd.read_csv('sensor_data.csv')
df = df.rename(columns={
    'sensor_id': 'unique_id',
    'timestamp': 'ds',
    'reading': 'y'
})
df['ds'] = pd.to_datetime(df['ds'])

# Detect anomalies
client = NixtlaClient(api_key=os.environ['NIXTLA_TIMEGPT_API_KEY'])
anomalies = client.detect_anomalies(df=df, freq='H')

# Results
print(f"Total data points: {len(df)}")
print(f"Anomalies detected: {anomalies['anomaly'].sum()}")

# Save
anomalies.to_csv('sensor_anomalies.csv', index=False)
```

This will flag any unusual readings that deviate from expected patterns.
```

---

## 4.3 nixtla-exogenous-integrator

### 4.3.1 Overview

**Purpose**: Add external variables (holidays, weather, events) to forecasts

**Location**: `000-docs/planned-skills/core-forecasting/nixtla-exogenous-integrator/SKILL.md`

**Triggers**:
- "include holidays"
- "add weather data"
- "exogenous variables"
- "external factors"

### 4.3.2 YAML Frontmatter

```yaml
---
name: nixtla-exogenous-integrator
description: |
  Integrates exogenous variables (holidays, weather, events) into forecasts.
  Improves accuracy by incorporating external factors.
  Use when forecasts should account for external influences.
  Trigger with "include holidays", "add weather", "exogenous variables".
version: "1.0.0"
allowed-tools: "Read,Write,Bash,Glob,Grep"
---
```

### 4.3.3 Full Instructions

```markdown
# Nixtla Exogenous Integrator

## Overview

Exogenous variables are external factors that influence your target but aren't predicted themselves (weather, holidays, promotions).

## StatsForecast with Exogenous

```python
import pandas as pd
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA

# Historical data with exogenous
df = pd.read_csv('sales_with_features.csv')
# Columns: unique_id, ds, y, temperature, is_holiday, promotion

# Future exogenous values (MUST provide these)
future_exog = pd.read_csv('future_features.csv')
# Columns: unique_id, ds, temperature, is_holiday, promotion

# Fit with exogenous
sf = StatsForecast(models=[AutoARIMA()], freq='D')
forecasts = sf.forecast(
    df=df,
    h=14,
    X_df=future_exog  # Future exogenous values
)
```

## TimeGPT with Exogenous

```python
from nixtla import NixtlaClient

client = NixtlaClient(api_key=os.environ['NIXTLA_TIMEGPT_API_KEY'])

# Historical with exogenous columns included
forecasts = client.forecast(
    df=df,  # Must include exogenous columns
    h=14,
    freq='D',
    X_df=future_exog  # Future values of exogenous
)
```

## Common Exogenous Variables

| Type | Examples | Notes |
|------|----------|-------|
| Calendar | day_of_week, month, is_weekend | Can be auto-generated |
| Holidays | is_holiday, days_to_holiday | Use holidays library |
| Weather | temperature, precipitation | Need forecasted weather |
| Business | promotion, price, marketing_spend | Need planned values |

## Auto-Generate Calendar Features

```python
def add_calendar_features(df):
    """Add calendar-based exogenous features."""
    df['day_of_week'] = df['ds'].dt.dayofweek
    df['month'] = df['ds'].dt.month
    df['is_weekend'] = df['ds'].dt.dayofweek >= 5
    df['day_of_month'] = df['ds'].dt.day
    return df

# For future dates
def generate_future_calendar(start_date, periods, freq='D'):
    """Generate future calendar features."""
    future_dates = pd.date_range(start=start_date, periods=periods, freq=freq)
    future_df = pd.DataFrame({'ds': future_dates})
    return add_calendar_features(future_df)
```

## Important Notes

1. **Must provide future values**: Exogenous variables need to be known/forecasted for the forecast horizon
2. **Same columns**: Training and future data must have identical exogenous columns
3. **No nulls**: Exogenous variables cannot have null values
```

---

## 4.4 nixtla-uncertainty-quantifier

### 4.4.1 Overview

**Purpose**: Generate prediction intervals and confidence bands

**Location**: `000-docs/planned-skills/core-forecasting/nixtla-uncertainty-quantifier/SKILL.md`

**Triggers**:
- "prediction intervals"
- "confidence bands"
- "forecast uncertainty"
- "quantile forecasts"

### 4.4.2 YAML Frontmatter

```yaml
---
name: nixtla-uncertainty-quantifier
description: |
  Generates prediction intervals and confidence bands for forecasts.
  Quantifies forecast uncertainty using various methods.
  Use when you need uncertainty estimates, not just point forecasts.
  Trigger with "prediction intervals", "confidence bands", "uncertainty".
version: "1.0.0"
allowed-tools: "Read,Write,Bash,Glob,Grep"
---
```

### 4.4.3 Full Instructions

```markdown
# Nixtla Uncertainty Quantifier

## TimeGPT Prediction Intervals

```python
from nixtla import NixtlaClient

client = NixtlaClient(api_key=os.environ['NIXTLA_TIMEGPT_API_KEY'])

# Request prediction intervals at 80% and 95% confidence
forecasts = client.forecast(
    df=df,
    h=14,
    freq='D',
    level=[80, 95]  # Confidence levels
)

# Output columns:
# - TimeGPT: point forecast
# - TimeGPT-lo-80: lower 80% bound
# - TimeGPT-hi-80: upper 80% bound
# - TimeGPT-lo-95: lower 95% bound
# - TimeGPT-hi-95: upper 95% bound
```

## StatsForecast Prediction Intervals

```python
from statsforecast import StatsForecast
from statsforecast.models import AutoETS

sf = StatsForecast(
    models=[AutoETS(season_length=7)],
    freq='D'
)

# Request prediction intervals
forecasts = sf.forecast(
    df=df,
    h=14,
    level=[80, 95]
)
```

## Visualization

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12, 6))

# Plot point forecast
ax.plot(forecasts['ds'], forecasts['TimeGPT'], label='Forecast', color='blue')

# Plot confidence bands
ax.fill_between(
    forecasts['ds'],
    forecasts['TimeGPT-lo-95'],
    forecasts['TimeGPT-hi-95'],
    alpha=0.2,
    label='95% CI'
)
ax.fill_between(
    forecasts['ds'],
    forecasts['TimeGPT-lo-80'],
    forecasts['TimeGPT-hi-80'],
    alpha=0.4,
    label='80% CI'
)

ax.legend()
plt.savefig('forecast_with_intervals.png')
```
```

---

## 4.5 nixtla-cross-validator

### 4.5.1 Overview

**Purpose**: Backtest models using time series cross-validation

**Location**: `000-docs/planned-skills/core-forecasting/nixtla-cross-validator/SKILL.md`

**Triggers**:
- "cross validate"
- "backtest model"
- "time series CV"
- "evaluate forecast"

### 4.5.2 YAML Frontmatter

```yaml
---
name: nixtla-cross-validator
description: |
  Performs time series cross-validation for model evaluation.
  Backtests models using expanding or sliding windows.
  Use when evaluating forecast model performance.
  Trigger with "cross validate", "backtest", "evaluate model".
version: "1.0.0"
allowed-tools: "Read,Write,Bash,Glob,Grep"
---
```

### 4.5.3 Full Instructions

```markdown
# Nixtla Cross-Validator

## StatsForecast Cross-Validation

```python
from statsforecast import StatsForecast
from statsforecast.models import AutoETS, AutoTheta

sf = StatsForecast(
    models=[AutoETS(), AutoTheta()],
    freq='D'
)

# Time series cross-validation
cv_results = sf.cross_validation(
    df=df,
    h=14,              # Forecast horizon
    step_size=7,       # Days between folds
    n_windows=5        # Number of folds
)

# cv_results contains actual vs predicted for each fold
print(cv_results.head())
```

## Calculate Metrics

```python
from datasetsforecast.losses import mase, smape

# Group by cutoff (fold)
metrics = []
for cutoff in cv_results['cutoff'].unique():
    fold = cv_results[cv_results['cutoff'] == cutoff]

    for model in ['AutoETS', 'AutoTheta']:
        fold_mase = mase(fold['y'], fold[model], fold['y'], seasonality=7)
        fold_smape = smape(fold['y'], fold[model])

        metrics.append({
            'cutoff': cutoff,
            'model': model,
            'MASE': fold_mase,
            'sMAPE': fold_smape
        })

metrics_df = pd.DataFrame(metrics)
print(metrics_df.groupby('model').mean())
```

## Cross-Validation Diagram

```
Full Time Series: |----------------------------------------------->

Fold 1:  Train: |----------|  Test: |--|
Fold 2:  Train: |-------------|  Test: |--|
Fold 3:  Train: |----------------|  Test: |--|
Fold 4:  Train: |-------------------|  Test: |--|
Fold 5:  Train: |----------------------|  Test: |--|
```
```

---

## 4.6 nixtla-timegpt2-migrator

### 4.6.1 Overview

**Purpose**: Migrate from TimeGPT-1 to TimeGPT-2

**Location**: `000-docs/planned-skills/core-forecasting/nixtla-timegpt2-migrator/SKILL.md`

**Triggers**:
- "migrate to TimeGPT-2"
- "upgrade TimeGPT"
- "TimeGPT compatibility"

### 4.6.2 YAML Frontmatter

```yaml
---
name: nixtla-timegpt2-migrator
description: |
  Assists with migration from TimeGPT-1 to TimeGPT-2.
  Identifies breaking changes and generates updated code.
  Use when upgrading to TimeGPT 2.
  Trigger with "migrate TimeGPT-2", "upgrade TimeGPT".
version: "1.0.0"
allowed-tools: "Read,Write,Glob,Grep,Edit"
---
```

---

# Part 5: Generated Skills - Prediction Markets (10)

## 5.1 Overview

These skills apply Nixtla to prediction market analysis.

| # | Skill | Purpose |
|---|-------|---------|
| 1 | nixtla-polymarket-analyst | Forecast Polymarket contracts |
| 2 | nixtla-arbitrage-detector | Find cross-market opportunities |
| 3 | nixtla-contract-schema-mapper | Transform market data |
| 4 | nixtla-batch-forecaster | Parallel batch forecasting |
| 5 | nixtla-event-impact-modeler | Model event effects |
| 6 | nixtla-forecast-validator | Validate forecast quality |
| 7 | nixtla-model-selector | Auto-select best model |
| 8 | nixtla-liquidity-forecaster | Predict trading volume |
| 9 | nixtla-correlation-mapper | Find contract correlations |
| 10 | nixtla-market-risk-analyzer | VaR and position sizing |

---

## 5.2 nixtla-polymarket-analyst

### 5.2.1 Overview

**Purpose**: Forecast Polymarket contract prices

**Location**: `000-docs/planned-skills/prediction-markets/nixtla-polymarket-analyst/SKILL.md`

**Triggers**:
- "Polymarket analysis"
- "predict contract odds"
- "forecast Polymarket"
- "prediction market forecast"

### 5.2.2 YAML Frontmatter

```yaml
---
name: nixtla-polymarket-analyst
description: |
  Analyzes and forecasts Polymarket contract prices using Nixtla.
  Fetches historical prices, transforms to time series, generates forecasts.
  Use for prediction market analysis and trading signals.
  Trigger with "Polymarket analysis", "predict contract", "forecast market".
version: "1.0.0"
allowed-tools: "Read,Write,Bash,Glob,Grep"
---
```

### 5.2.3 Full Instructions

```markdown
# Nixtla Polymarket Analyst

## Overview

Forecasts Polymarket contract prices using TimeGPT or StatsForecast.

## Workflow

### Step 1: Fetch Contract Data

```python
import requests
import pandas as pd

def fetch_polymarket_data(contract_id: str) -> pd.DataFrame:
    """Fetch historical prices from Polymarket API."""
    url = f"https://clob.polymarket.com/prices-history"
    params = {"market": contract_id, "interval": "1d"}

    response = requests.get(url, params=params)
    data = response.json()

    df = pd.DataFrame(data['history'])
    df['ds'] = pd.to_datetime(df['t'], unit='s')
    df['y'] = df['p']  # Price
    df['unique_id'] = contract_id

    return df[['unique_id', 'ds', 'y']]
```

### Step 2: Run Forecast

```python
from statsforecast import StatsForecast
from statsforecast.models import AutoETS, AutoTheta

# Fetch data
df = fetch_polymarket_data('0x123...')

# Forecast
sf = StatsForecast(
    models=[AutoETS(), AutoTheta()],
    freq='D'
)
forecasts = sf.forecast(df=df, h=14)

print(forecasts)
```

### Step 3: Interpret Results

Contract prices are between 0 and 1 (probability).
- 0.70 = 70% implied probability
- Forecast trending up = market becoming more confident
- Forecast trending down = market becoming less confident

## Limitations

- Prediction markets are not pure time series (events affect prices)
- Past performance doesn't guarantee future results
- Use as one input among many for trading decisions
```

---

## 5.3-5.11 Additional Prediction Market Skills

[Each skill follows the same detailed format with YAML frontmatter, full instructions, code examples, and usage scenarios. Due to length, providing abbreviated versions:]

### 5.3 nixtla-arbitrage-detector
- Compares prices across Polymarket and Kalshi
- Identifies profitable discrepancies
- Generates arbitrage opportunity reports

### 5.4 nixtla-contract-schema-mapper
- Transforms prediction market data to Nixtla format
- Handles various market data formats
- Validates schema compliance

### 5.5 nixtla-batch-forecaster
- Forecasts multiple contracts in parallel
- Manages API rate limits
- Aggregates results into portfolio view

### 5.6 nixtla-event-impact-modeler
- Models how events affect contract prices
- Uses causal inference techniques
- Generates event-adjusted forecasts

### 5.7 nixtla-forecast-validator
- Validates forecast quality metrics
- Compares against historical performance
- Alerts on forecast degradation

### 5.8 nixtla-model-selector
- Auto-selects best model based on data characteristics
- Considers data length, frequency, seasonality
- Outputs selection explanation

### 5.9 nixtla-liquidity-forecaster
- Predicts orderbook depth and spreads
- Forecasts trading volume
- Identifies liquidity risk

### 5.10 nixtla-correlation-mapper
- Analyzes correlations between contracts
- Identifies hedging opportunities
- Generates correlation matrix

### 5.11 nixtla-market-risk-analyzer
- Calculates Value at Risk (VaR)
- Measures portfolio volatility
- Recommends position sizing

---

# Part 6: Generated Skills - Live/Retroactive (6)

## 6.1 Overview

These skills support interactive and production forecasting workflows.

| # | Skill | Purpose |
|---|-------|---------|
| 1 | nixtla-timegpt-lab | Interactive forecasting |
| 2 | nixtla-experiment-architect | Design experiments |
| 3 | nixtla-schema-mapper | Data transformation |
| 4 | nixtla-timegpt-finetune-lab | Model fine-tuning |
| 5 | nixtla-prod-pipeline-generator | Pipeline generation |
| 6 | nixtla-usage-optimizer | Cost optimization |

[These overlap with production skills - the generated versions have similar functionality with minor variations in implementation details.]

---

# Part 7: Writing Custom Skills

## 7.1 Skill Template

```markdown
---
name: my-custom-skill
description: |
  [What this skill does - 1-2 sentences].
  [Key capabilities and features].
  Use when [specific scenarios].
  Trigger with "[phrase 1]", "[phrase 2]", "[phrase 3]".
version: "1.0.0"
allowed-tools: "Read,Write,Glob,Grep,Edit,Bash"
---

# [Skill Title]

## Overview

[2-3 sentences explaining what this skill does and why]

## Prerequisites

- [Requirement 1]
- [Requirement 2]

## Instructions

### Step 1: [First Step Name]

[Detailed instructions]

```python
# Code example
```

### Step 2: [Second Step Name]

[More instructions]

## Examples

### Example 1: [Scenario Name]

[Description and code]

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| [Error 1] | [Cause] | [Solution] |

## Related Skills

- [skill-1]: [Why related]
- [skill-2]: [Why related]
```

## 7.2 Description Best Practices

1. **Start with action verb**: "Detects", "Transforms", "Generates"
2. **Be specific**: "forecasting using TimeGPT" not "helps with forecasting"
3. **Include trigger phrases**: "Trigger with 'detect anomalies', 'find outliers'"
4. **Keep under 1024 chars**: Claude has description length limits

## 7.3 Instruction Best Practices

1. **Step-by-step**: Number each step clearly
2. **Include code**: Working examples Claude can adapt
3. **Handle errors**: Document common issues
4. **Be complete**: Don't assume Claude knows specifics

---

# Part 8: Skill Activation Patterns

## 8.1 Explicit Activation

User explicitly names the skill:
```
User: Use nixtla-timegpt-lab to forecast this data
```

## 8.2 Trigger Phrase Activation

User uses a phrase from description:
```
User: Can you forecast my sales data?
→ Activates nixtla-timegpt-lab (matches "forecast" trigger)
```

## 8.3 Context Activation

Claude detects relevant context:
```
User: I have a CSV with columns date, store, revenue
→ May activate nixtla-schema-mapper (detects data transformation need)
```

## 8.4 Chain Activation

Multiple skills activate in sequence:
```
User: Transform my data and forecast next month

1. nixtla-schema-mapper activates (transform)
2. nixtla-timegpt-lab activates (forecast)
```

---

# Part 9: Testing and Validation

## 9.1 Skill Compliance Validation

```python
import yaml
import re
from pathlib import Path

def validate_skill(skill_path: Path) -> dict:
    """Validate a skill file against standards."""

    content = skill_path.read_text()

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {"valid": False, "error": "No YAML frontmatter"}

    frontmatter = yaml.safe_load(match.group(1))

    errors = []

    # Required fields
    if 'name' not in frontmatter:
        errors.append("Missing required field: name")
    if 'description' not in frontmatter:
        errors.append("Missing required field: description")

    # Forbidden fields
    forbidden = ['author', 'priority', 'audience', 'when_to_use', 'license']
    for field in forbidden:
        if field in frontmatter:
            errors.append(f"Forbidden field: {field}")

    # Name format
    if 'name' in frontmatter:
        name = frontmatter['name']
        if not re.match(r'^[a-z][a-z0-9-]*$', name):
            errors.append("Name must be lowercase with hyphens only")
        if len(name) > 64:
            errors.append("Name exceeds 64 characters")

    # Description length
    if 'description' in frontmatter:
        if len(frontmatter['description']) > 1024:
            errors.append("Description exceeds 1024 characters")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "frontmatter": frontmatter
    }
```

## 9.2 Running Validation

```bash
# Validate all skills
python tests/basic_validator.py

# Validate specific skill
python tests/validate_skill.py skills-pack/.claude/skills/nixtla-timegpt-lab/SKILL.md
```

---

# Part 10: Best Practices

## 10.1 Skill Design

1. **Single responsibility**: One skill, one clear purpose
2. **Clear triggers**: Specific phrases that activate the skill
3. **Complete instructions**: Everything Claude needs to execute
4. **Working code**: Examples that actually run
5. **Error handling**: Document common issues

## 10.2 Description Writing

1. **Action-oriented**: Start with verbs
2. **Specific**: Mention libraries, methods, outputs
3. **Include triggers**: "Trigger with '[phrase]'"
4. **Under 1024 chars**: Hard limit

## 10.3 Instruction Writing

1. **Step-by-step**: Clear numbered steps
2. **Code examples**: Working Python snippets
3. **Expected output**: Show what results look like
4. **Prerequisites**: List requirements upfront

---

# Part 11: Reference

## 11.1 Skill Locations

| Category | Location |
|----------|----------|
| Production Skills | `skills-pack/.claude/skills/` |
| Core Forecasting | `000-docs/planned-skills/core-forecasting/` |
| Prediction Markets | `000-docs/planned-skills/prediction-markets/` |
| Live/Retroactive | `000-docs/planned-skills/live/` |

## 11.2 Related Documentation

| Document | Location |
|----------|----------|
| Frontmatter Schema | `000-docs/6767-m-DR-STND-claude-skills-frontmatter-schema.md` |
| Authoring Guide | `000-docs/6767-n-DR-GUID-claude-skills-authoring-guide.md` |
| Compliance Audit | `000-docs/060-AA-AUDT-generated-skills-compliance-audit.md` |
| Plugins Guide | `000-docs/063-OD-GUID-plugins-comprehensive-guide.md` |

## 11.3 All 29 Skills Quick Reference

### Production Skills (8)
| Skill | Purpose | Triggers |
|-------|---------|----------|
| nixtla-timegpt-lab | Expert forecasting | "forecast", "predict" |
| nixtla-experiment-architect | Scaffold experiments | "design experiment" |
| nixtla-schema-mapper | Transform data | "Nixtla format" |
| nixtla-timegpt-finetune-lab | Fine-tune TimeGPT | "finetune" |
| nixtla-prod-pipeline-generator | Generate pipelines | "productionize" |
| nixtla-usage-optimizer | Optimize costs | "reduce costs" |
| nixtla-skills-index | List skills | "list skills" |
| nixtla-skills-bootstrap | Install skills | "install skills" |

### Core Forecasting (5)
| Skill | Purpose | Triggers |
|-------|---------|----------|
| nixtla-anomaly-detector | Detect anomalies | "outliers", "anomaly" |
| nixtla-exogenous-integrator | Add external vars | "holidays", "weather" |
| nixtla-uncertainty-quantifier | Prediction intervals | "confidence", "uncertainty" |
| nixtla-cross-validator | Backtest models | "cross validate", "backtest" |
| nixtla-timegpt2-migrator | Migrate to v2 | "migrate", "upgrade" |

### Prediction Markets (10)
| Skill | Purpose | Triggers |
|-------|---------|----------|
| nixtla-polymarket-analyst | Forecast Polymarket | "Polymarket", "contract" |
| nixtla-arbitrage-detector | Find arbitrage | "arbitrage", "opportunity" |
| nixtla-contract-schema-mapper | Transform market data | "market data", "transform" |
| nixtla-batch-forecaster | Batch forecasting | "batch", "parallel" |
| nixtla-event-impact-modeler | Model events | "event impact", "causal" |
| nixtla-forecast-validator | Validate forecasts | "validate", "quality" |
| nixtla-model-selector | Auto-select model | "best model", "select" |
| nixtla-liquidity-forecaster | Predict liquidity | "liquidity", "volume" |
| nixtla-correlation-mapper | Find correlations | "correlation", "hedge" |
| nixtla-market-risk-analyzer | Calculate risk | "VaR", "risk", "position" |

### Live/Retroactive (6)
| Skill | Purpose | Triggers |
|-------|---------|----------|
| nixtla-timegpt-lab | Interactive forecasting | "forecast", "predict" |
| nixtla-experiment-architect | Design experiments | "experiment", "design" |
| nixtla-schema-mapper | Transform data | "schema", "format" |
| nixtla-timegpt-finetune-lab | Fine-tune models | "finetune", "adapt" |
| nixtla-prod-pipeline-generator | Generate pipelines | "Airflow", "Prefect" |
| nixtla-usage-optimizer | Optimize API costs | "optimize", "costs" |

---

**Document Created**: 2025-12-08
**Version**: 1.0.0
**Lines**: ~5000
