# MLForecast Lab

Machine learning pipelines (LightGBM, XGBoost, feature engineering) for production-grade ML forecasting. This workspace is the home base for MLForecast engineers to design, validate, and refine ML-based forecasting workflows.

## Structure

- **skills/** - MLForecast Claude Skills (ML pipeline builders, feature engineers)
- **scripts/** - Feature engineering, model training, hyperparameter tuning, prediction pipelines
- **data/** - Training datasets, feature stores, ML experiment data, model checkpoints
- **reports/** - ML model evaluations, hyperparameter tuning results, feature importance analysis
- **docs/** - ML best practices, feature engineering guides, model selection strategies

## Example Future Flows

1. **Design and run ML forecasting pipelines** with LightGBM/XGBoost
2. **Prototype feature engineering workflows** (lag features, rolling windows, calendar features)
3. **Validate hyperparameter tuning strategies** before production deployment
4. **Benchmark ML models** against StatsForecast baselines
5. **Create feature engineering templates** for reusable ML workflows

## Environment Setup

```bash
pip install mlforecast utilsforecast lightgbm xgboost
# Optional: scikit-learn for additional models
```

## Promotion Path

When an MLForecast workflow is stable and validated:
- **Skills**: Promote to `skills-pack/.claude/skills/nixtla-mlforecast-*`
- **Scripts**: Integrate into `plugins/nixtla-mlforecast-*/` (future MCP server)
- **Docs**: Extract feature engineering patterns to `000-docs/` with proper naming
