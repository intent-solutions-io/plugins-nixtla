# TimeGPT Fine-Tuning Troubleshooting

## Issue 1: Fine-tuning job fails immediately

**Symptoms**:
- Job submission returns error
- "Invalid API key" or "Quota exceeded"

**Solutions**:

1. **Check API key**:
   ```bash
   echo $NIXTLA_API_KEY
   # Should print your key
   ```

2. **Verify TimeGPT access**:
   ```python
   from nixtla import NixtlaClient
   client = NixtlaClient(api_key=os.getenv('NIXTLA_API_KEY'))

   # Test with simple forecast
   test_df = pd.DataFrame({
       'unique_id': ['series1'] * 100,
       'ds': pd.date_range('2020-01-01', periods=100, freq='D'),
       'y': range(100)
   })
   forecast = client.forecast(df=test_df, h=7)
   print("TimeGPT access OK!")
   ```

3. **Check quota/limits**:
   - Log into https://dashboard.nixtla.io
   - Check usage limits and billing

## Issue 2: Data format errors

**Symptoms**:
- "Missing required columns"
- "Invalid date format"

**Solutions**:

1. **Verify Nixtla schema**:
   ```python
   # Required columns
   required = ['unique_id', 'ds', 'y']

   df = pd.read_csv('data/sales.csv')
   missing = [col for col in required if col not in df.columns]

   if missing:
       print(f"Missing columns: {missing}")
       # Use nixtla-schema-mapper to fix
   ```

2. **Check date format**:
   ```python
   df['ds'] = pd.to_datetime(df['ds'])

   # Verify no NaT values
   assert not df['ds'].isna().any()
   ```

3. **Use schema-mapper skill**:
   - If data not in Nixtla format, invoke `nixtla-schema-mapper` first

## Issue 3: Fine-tuning takes too long

**Symptoms**:
- Job running for hours
- No progress updates

**Solutions**:

1. **Reduce finetune_steps**:
   ```yaml
   # In config.yml
   parameters:
     finetune_steps: 50  # Down from 100
   ```

2. **Use smaller dataset**:
   - Sample data if very large (>1M rows)
   - Focus on recent time periods

3. **Check job status manually**:
   ```python
   from nixtla import NixtlaClient
   client = NixtlaClient(api_key=os.getenv('NIXTLA_API_KEY'))

   status = client.finetune_status(job_id='your-job-id')
   print(status)
   ```

## Issue 4: Fine-tuned model not better than zero-shot

**Symptoms**:
- Fine-tuned SMAPE worse than zero-shot
- No improvement in metrics

**Solutions**:

1. **Check training data quality**:
   - Sufficient history? (Need meaningful patterns)
   - Data issues? (Outliers, missing values)

2. **Adjust fine-tuning parameters**:
   ```yaml
   parameters:
     finetune_steps: 200  # Increase from 100
     finetune_loss: "mse"  # Try different loss
   ```

3. **Review train/val split**:
   - Is validation data representative?
   - Try different split ratios

4. **Compare with baselines**:
   - Maybe StatsForecast is sufficient for this data
   - TimeGPT best for complex patterns, not simple seasonality
