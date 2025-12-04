# Common Scenarios

Real-world scenario patterns for Nixtla experiment setup.

## Scenario 1: Single CSV File

**User**: "I have sales.csv with columns: date, product_id, sales"

**Your response**:
1. Create `forecasting/config.yml` with:
   - `source: "sales.csv"`
   - `unique_id: "product_id"`
   - `ds: "date"`
   - `y: "sales"`
2. Generate `experiments.py` with CSV loading
3. Set freq based on date inspection (likely 'D' for daily)

## Scenario 2: SQL Database

**User**: "Data is in PostgreSQL table 'public.sales'"

**Your response**:
1. Add TODO in experiments.py:
   ```python
   # TODO: Set DATABASE_URL environment variable
   # export DATABASE_URL='postgresql://user:pass@host/db'
   from sqlalchemy import create_engine
   engine = create_engine(os.getenv('DATABASE_URL'))
   df = pd.read_sql("SELECT * FROM public.sales", engine)
   ```
2. Update config.yml: `source: "SELECT * FROM public.sales"`

## Scenario 3: dbt Project

**User**: "I'm using dbt, data is in {{ ref('fct_daily_sales') }}"

**Your response**:
1. Add TODO in experiments.py:
   ```python
   # TODO: Run dbt first to materialize model
   # dbt run --select fct_daily_sales
   # Then load the result (check dbt target directory)
   df = pd.read_parquet('target/fct_daily_sales.parquet')
   ```
2. Update config.yml: `source: "{{ ref('fct_daily_sales') }}"`

## Scenario 4: TimeGPT Comparison

**User**: "Compare TimeGPT to baselines"

**Your response**:
1. Set `timegpt.enabled: true` in config.yml
2. Add note in output:
   ```
   💡 TimeGPT requires API key. Set environment variable:
      export NIXTLA_API_KEY='your-key-here'

      Get key at: https://dashboard.nixtla.io
   ```
