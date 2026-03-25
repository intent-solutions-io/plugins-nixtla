# User Scenarios

## Scenario 1: Quick Comparison
User has CSV data and wants to see which model performs best.
- Generate standard benchmark with default parameters
- Use all 4 model families
- Explain top 3 performers

## Scenario 2: Production Selection
User needs to choose a model for deployment.
- Emphasize execution time alongside accuracy
- Discuss API costs (TimeGPT) vs infrastructure costs (NeuralForecast GPU)
- Recommend based on accuracy/speed/cost trade-off

## Scenario 3: Academic Research
User wants comprehensive evaluation.
- Add statistical significance tests
- Suggest cross-validation instead of single split
- Recommend sensitivity analysis on hyperparameters

## Example Interaction

**User**: "Compare all Nixtla models on my sales data. It's daily data with 2 years of history."

**Workflow**:
1. Read the template from `assets/templates/benchmark_template.py`
2. Set HORIZON = 30 (reasonable for daily data)
3. Set FREQ = "D"
4. Set season_length = 7 (weekly patterns in sales)
5. Write customized script to `benchmark_nixtla_sales.py`
6. Explain: "Run with `python benchmark_nixtla_sales.py`. The script trains 9+ models and ranks them by RMSE. Results saved to CSV and PNG files."
