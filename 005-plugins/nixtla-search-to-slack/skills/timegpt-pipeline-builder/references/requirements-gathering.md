# Requirements Gathering

When generating a TimeGPT pipeline, gather the following information.

## Essential Information
- Data source (CSV, database, API, real-time stream)
- Forecast horizon (how many periods ahead)
- Frequency (hourly, daily, weekly, monthly)
- Historical data availability
- Special requirements (holidays, external regressors, confidence intervals)

## Questions to Ask (if not provided)

```markdown
To build the TimeGPT pipeline, these details are needed:

1. **Data Source**: Where is the time series data?
   - CSV file path
   - Database connection
   - API endpoint
   - Other

2. **Forecast Horizon**: How far ahead to predict?
   - Number of periods
   - Time unit (days, weeks, months)

3. **Data Format**: What does the data look like?
   - Date column name
   - Value column name(s)
   - Any grouping columns (multiple series)

4. **Requirements**:
   - Confidence intervals needed? (Yes/No)
   - External regressors? (Yes/No)
   - Holidays/special events? (Yes/No)
   - Visualization needed? (Yes/No)
```
