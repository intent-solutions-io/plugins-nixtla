# Nixtla Schema Mapper Scripts

Production-ready Python scripts for analyzing data sources and generating Nixtla-compatible schema transformations.

## Scripts Overview

| Script | Purpose | Lines | Inputs | Outputs |
|--------|---------|-------|--------|---------|
| `analyze_schema.py` | Auto-detect column types for Nixtla schema | 329 | CSV/Parquet file | JSON mapping + console analysis |
| `generate_transform.py` | Generate transformation Python module | 446 | Mapping JSON or explicit columns | Python transformation module |
| `create_contract.py` | Create schema contract documentation | 569 | Mapping JSON or explicit columns | Markdown contract document |

## Quick Start

### Workflow 1: Full Pipeline (Recommended)

```bash
# Step 1: Analyze your data and detect columns
python analyze_schema.py --input data/sales.csv --output mapping.json

# Step 2: Generate transformation code
python generate_transform.py --mapping mapping.json --output transform_sales.py

# Step 3: Create schema contract documentation
python create_contract.py --mapping mapping.json --output SALES_CONTRACT.md

# Step 4: Test the transformation
python transform_sales.py
```

### Workflow 2: Manual Column Specification

```bash
# If auto-detection fails, specify columns manually
python analyze_schema.py \
    --input data/sales.csv \
    --id_col store_id \
    --date_col transaction_date \
    --target_col revenue \
    --output mapping.json

# Then continue with steps 2-4 from Workflow 1
```

### Workflow 3: Quick Transform (No Mapping File)

```bash
# Generate transformation directly without mapping file
python generate_transform.py \
    --input data/sales.csv \
    --id_col store_id \
    --date_col date \
    --target_col sales \
    --exog price,promotion,holiday \
    --output transform_sales.py
```

## Script Details

### analyze_schema.py

**Purpose**: Automatically detect timestamp, target, series ID, and exogenous columns in your data.

**Features**:
- Auto-detects datetime columns (by dtype or common names)
- Identifies numeric target columns
- Finds series identifier columns with reasonable cardinality
- Detects exogenous feature columns
- Outputs JSON mapping for use in other scripts

**Usage**:
```bash
# Auto-detect everything
python analyze_schema.py --input data/sales.csv

# Save mapping to file
python analyze_schema.py --input data/sales.csv --output mapping.json

# Override specific columns
python analyze_schema.py \
    --input data/sales.csv \
    --id_col store_id \
    --target_col revenue
```

**Output Example**:
```
============================================================
Nixtla Schema Analysis
============================================================

Source: data/sales.csv
Rows analyzed: 10,000
Total columns: 8

--- Detected Column Mapping ---
  unique_id: 'store_id' (object)
  ds:        'date' (object)
  y:         'sales' (float64)

--- Statistics ---
  Series count: 50
  Date range:   2023-01-01 to 2023-12-31
  Target range: 0.00 to 15000.00 (mean: 2500.50)

--- Exogenous Variables ---
  price: float64
  promotion: int64
  day_of_week: int64
  holiday: int64
```

### generate_transform.py

**Purpose**: Generate production-ready Python transformation module with validation and error handling.

**Features**:
- Creates reusable transformation function
- Includes data quality checks (nulls, duplicates, sorting)
- Adds validation function
- Generates executable script with summary output
- Supports CSV and Parquet formats

**Usage**:
```bash
# From mapping file
python generate_transform.py --mapping mapping.json --output transform.py

# From explicit parameters
python generate_transform.py \
    --input data/sales.csv \
    --id_col store_id \
    --date_col date \
    --target_col sales \
    --output transform.py

# Include exogenous variables
python generate_transform.py \
    --input data/sales.csv \
    --id_col store_id \
    --date_col date \
    --target_col sales \
    --exog price,promotion,holiday
```

**Generated Module**:
The output is a complete Python module that can be:
- Imported: `from transform import to_nixtla_schema`
- Executed directly: `python transform.py`
- Integrated into data pipelines

### create_contract.py

**Purpose**: Generate comprehensive schema contract documentation with validation rules and usage examples.

**Features**:
- Documents schema mapping and transformations
- Includes validation script
- Provides StatsForecast and TimeGPT usage examples
- Documents data quality rules and assumptions
- Troubleshooting guide

**Usage**:
```bash
# From mapping file
python create_contract.py --mapping mapping.json --output CONTRACT.md

# From explicit parameters
python create_contract.py \
    --input data/sales.csv \
    --id_col store_id \
    --date_col date \
    --target_col sales \
    --output SALES_CONTRACT.md
```

**Contract Sections**:
1. Overview and metadata
2. Schema mapping table
3. Series and temporal statistics
4. Exogenous variables
5. Data quality rules
6. Validation script
7. Usage examples (StatsForecast, TimeGPT, cross-validation)
8. Known issues and assumptions
9. Troubleshooting guide

## Requirements

**Python**: 3.8+

**Dependencies**:
```bash
pip install pandas
```

**Optional** (for Parquet support):
```bash
pip install pyarrow
```

## Common Use Cases

### Use Case 1: Sales Forecasting

```bash
# Analyze sales data
python analyze_schema.py --input monthly_sales.csv --output sales_mapping.json

# Generate transformation
python generate_transform.py --mapping sales_mapping.json --output transform_sales.py

# Create documentation
python create_contract.py --mapping sales_mapping.json --output SALES_CONTRACT.md

# Transform and forecast
python transform_sales.py  # Creates nixtla-compatible dataset
```

### Use Case 2: Multi-Store Inventory

```bash
# Specify columns for inventory data
python generate_transform.py \
    --input inventory.parquet \
    --id_col warehouse_id \
    --date_col stock_date \
    --target_col quantity \
    --exog reorder_point,lead_time \
    --output transform_inventory.py
```

### Use Case 3: Web Traffic Analytics

```bash
# Daily page views per site
python analyze_schema.py \
    --input web_analytics.csv \
    --id_col site_id \
    --date_col visit_date \
    --target_col page_views \
    --output web_mapping.json
```

## Error Handling

### Error: "No timestamp column detected"

**Solution**: Specify manually
```bash
python analyze_schema.py --input data.csv --date_col your_date_column
```

### Error: "Multiple target candidates"

**Solution**: Specify target explicitly
```bash
python analyze_schema.py --input data.csv --target_col your_target_column
```

### Error: "Missing required columns"

**Solution**: Check column names in source file
```bash
# View available columns
python -c "import pandas as pd; print(pd.read_csv('data.csv').columns.tolist())"
```

## Best Practices

1. **Always analyze first**: Run `analyze_schema.py` to understand your data before generating transformations
2. **Save mappings**: Use `--output mapping.json` to create reusable configuration
3. **Review generated code**: Inspect the generated transformation module before using in production
4. **Test transformations**: Run the generated module directly to verify it works with your data
5. **Version control**: Check schema contracts and transformations into git for reproducibility

## Integration Examples

### Example 1: Import in Forecasting Pipeline

```python
from transform_sales import to_nixtla_schema
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA

# Transform
df = to_nixtla_schema("data/sales.csv")

# Forecast
sf = StatsForecast(models=[AutoARIMA()], freq='D')
forecasts = sf.forecast(df=df, h=30)
```

### Example 2: Automated Data Pipeline

```python
import subprocess

# Step 1: Generate mapping
subprocess.run([
    "python", "analyze_schema.py",
    "--input", "data/new_source.csv",
    "--output", "mapping.json"
])

# Step 2: Generate transformation
subprocess.run([
    "python", "generate_transform.py",
    "--mapping", "mapping.json",
    "--output", "transform.py"
])

# Step 3: Execute transformation
from transform import to_nixtla_schema
df = to_nixtla_schema("data/new_source.csv")
```

## Troubleshooting

### Script won't execute

Make scripts executable:
```bash
chmod +x *.py
```

### Import errors

Install required dependencies:
```bash
pip install pandas pyarrow
```

### Date parsing fails

Specify format explicitly in generated code:
```python
to_nixtla_schema(source_path="data.csv", date_format="%Y-%m-%d")
```

## Version

Scripts version: 1.0.0 (Generated 2025-12-09)

Part of nixtla-schema-mapper skill v1.1.0
