# Nixtla Skills Demo Project

**Welcome!** This demo project showcases the **Nixtla Claude Skills Pack** - a collection of AI-powered skills for Claude Code that accelerate time series forecasting workflows.

## What You'll Learn

By following this walkthrough, you'll:

1. Install Nixtla skills into this project
2. Run quick TimeGPT experiments on sample data
3. Compare TimeGPT vs baseline models (AutoETS, SeasonalNaive, etc.)
4. Set up fine-tuning workflows (optional)
5. Generate production-ready forecasting pipelines (optional)
6. Audit your Nixtla usage and optimize costs (optional)

**Time to complete**: 15-30 minutes

---

## Prerequisites

### Required

- **Python 3.10+** with pip
- **Claude Code** (claude.ai/code) - Get access at [claude.ai/code](https://claude.ai/code)
- **Nixtla API Key** (for TimeGPT features):
  - Sign up at [nixtla.io](https://nixtla.io)
  - Get your API key from the dashboard
  - Set environment variable: `export NIXTLA_API_KEY='your-key-here'`

### Optional (for advanced features)

- Docker (for production pipeline examples)
- Apache Airflow (for pipeline orchestration)
- PostgreSQL or BigQuery (for production data sources)

---

## Step 1: Install Nixtla Skills

The Nixtla Skills Pack includes 6 specialized skills for forecasting workflows:

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| **nixtla-timegpt-lab** | Quick TimeGPT experiments | First-time testing, rapid prototyping |
| **nixtla-schema-mapper** | Map your data to Nixtla format | You have real data to forecast |
| **nixtla-experiment-architect** | Compare models systematically | Need rigorous model comparison |
| **nixtla-timegpt-finetune-lab** | Fine-tune TimeGPT on your data | Advanced: Improve accuracy |
| **nixtla-prod-pipeline-generator** | Generate production pipelines | Advanced: Deploy to production |
| **nixtla-usage-optimizer** | Audit usage, optimize costs | Advanced: Cost optimization |

### Installation

```bash
# Navigate to this demo project
cd demo-project/

# Install the Nixtla Skills installer (hypothetical - adjust when installer is released)
pip install nixtla-claude-skills-installer

# Initialize skills in this project (copies skills to .claude/skills/)
nixtla-skills init

# Verify installation
ls -la .claude/skills/
# You should see:
# nixtla-timegpt-lab/
# nixtla-schema-mapper/
# nixtla-experiment-architect/
# nixtla-timegpt-finetune-lab/
# nixtla-prod-pipeline-generator/
# nixtla-usage-optimizer/
```

**What just happened?**

- The installer copied all 6 skills to `.claude/skills/` in this project
- These skills are now available whenever you open this project in Claude Code
- Skills persist until you update or remove them (per-project installation)

---

## Step 2: Open Project in Claude Code

```bash
# Open Claude Code and navigate to this directory
# In Claude Code's terminal:
cd /path/to/nixtla/demo-project
```

**Verify skills are loaded:**

In Claude Code, type:
```
Can you list the available Nixtla skills?
```

Claude should respond with all 6 skills.

---

## Step 3: Quick TimeGPT Experiment

Let's run a quick forecast on the sample data using **nixtla-timegpt-lab**.

### Activate the Skill

In Claude Code, say:
```
Use nixtla-timegpt-lab to run a quick TimeGPT experiment on data/sample_series.csv
```

**What happens:**

1. Claude asks for your preferences:
   - Dataset path: `data/sample_series.csv` (already provided)
   - Target column: `y` (default)
   - Horizon: `14` (forecast 14 days ahead)
   - Frequency: `D` (daily data)
   - Experiment name: `demo_quick_timegpt`

2. Claude generates:
   - `forecasting/config.yml` - Experiment configuration
   - `forecasting/experiments.py` - Experiment runner script
   - Instructions to run the experiment

3. Run the experiment:
   ```bash
   python3 forecasting/experiments.py
   ```

4. View results:
   ```bash
   cat forecasting/artifacts/demo_quick_timegpt/forecast.csv
   cat forecasting/artifacts/demo_quick_timegpt/metrics.json
   ```

**Expected Output:**

- Forecast CSV with predictions for 14 days ahead (3 series x 14 days = 42 rows)
- Metrics JSON with SMAPE, MAE, MASE scores
- Forecast plot (if matplotlib installed)

---

## Step 4: Compare TimeGPT vs Baselines

Now let's systematically compare TimeGPT against baseline models using **nixtla-experiment-architect**.

### Activate the Skill

In Claude Code, say:
```
Use nixtla-experiment-architect to compare TimeGPT against AutoETS, AutoTheta, and SeasonalNaive
```

**What happens:**

1. Claude reads your existing `forecasting/config.yml`
2. Extends it with baseline model configurations
3. Updates `forecasting/experiments.py` to run all models
4. Generates comparison plots and metric tables

5. Run the comparison:
   ```bash
   python3 forecasting/experiments.py --experiment all_models_comparison
   ```

6. View results:
   ```bash
   # Metrics table showing SMAPE, MAE, MASE for each model
   cat forecasting/artifacts/all_models_comparison/metrics_comparison.csv

   # Best model per series
   cat forecasting/artifacts/all_models_comparison/best_models.json

   # Comparison plot
   open forecasting/artifacts/all_models_comparison/forecast_comparison.png
   ```

**Expected Output:**

- Comparison table showing TimeGPT vs 3 baselines across 3 series
- Best model identification per series
- Forecast plots overlaying all model predictions

**Typical Results:**

- Product A (strong trend): TimeGPT often wins
- Product B (strong seasonality): AutoETS and TimeGPT tie
- Product C (high noise): SeasonalNaive may suffice

---

## Step 5: Map Your Own Data (Optional)

If you have real data to forecast, use **nixtla-schema-mapper**.

### Activate the Skill

In Claude Code, say:
```
Use nixtla-schema-mapper to help me convert my data to Nixtla format
```

**What happens:**

1. Claude asks for your data file path and inspects it
2. Identifies columns: time column, value column, grouping columns
3. Generates a mapping script: `data_processing/nixtla_mapper.py`
4. Validates the transformed data against Nixtla schema
5. Outputs clean data ready for forecasting

**Nixtla Format Requirements:**

```csv
unique_id,ds,y
series_1,2023-01-01,100.5
series_1,2023-01-02,102.3
series_2,2023-01-01,200.1
series_2,2023-01-02,198.7
```

- `unique_id`: Series identifier (string)
- `ds`: Timestamp (datetime)
- `y`: Value to forecast (numeric)

---

## Step 6: Fine-Tune TimeGPT (Advanced)

For advanced users, fine-tune TimeGPT on your specific data using **nixtla-timegpt-finetune-lab**.

### When to Fine-Tune

Fine-tuning is useful when:
- You have domain-specific patterns
- Standard TimeGPT underperforms
- You have sufficient historical data (6+ months recommended)
- Accuracy improvement justifies the cost

### Activate the Skill

In Claude Code, say:
```
Use nixtla-timegpt-finetune-lab to fine-tune TimeGPT on the sample data
```

**What happens:**

1. Claude asks for fine-tuning parameters:
   - Dataset path: `data/sample_series.csv`
   - Train/val split: `time` (use 2023-01-01 to 2023-11-30 for training)
   - Fine-tune steps: `100` (fewer = faster, more = better accuracy)
   - Model name: `demo_finetuned_v1`

2. Claude extends `forecasting/config.yml` with fine-tune section
3. Generates `forecasting/timegpt_finetune_job.py` to run fine-tuning
4. Updates experiments to compare zero-shot vs fine-tuned vs baselines

5. Run the fine-tuning job:
   ```bash
   python3 forecasting/timegpt_finetune_job.py
   ```

6. View fine-tuned model ID:
   ```bash
   cat forecasting/artifacts/timegpt_finetune/finetune_job_results.json
   ```

7. Run comparison experiment:
   ```bash
   python3 forecasting/experiments.py --experiment finetune_comparison
   ```

**Expected Output:**

- Fine-tuned model ID saved to artifacts
- Comparison showing zero-shot TimeGPT, fine-tuned TimeGPT, and baselines
- Typically: fine-tuned improves SMAPE by 5-15% on validation set

---

## Step 7: Generate Production Pipeline (Advanced)

Ready to deploy? Use **nixtla-prod-pipeline-generator** to create production-ready pipelines.

### When to Use

Use this skill when:
- You've validated model performance
- Ready to deploy to production
- Need automated, scheduled forecasts
- Want monitoring and fallback mechanisms

### Activate the Skill

In Claude Code, say:
```
Use nixtla-prod-pipeline-generator to create an Airflow DAG for production forecasts
```

**What happens:**

1. Claude asks for production requirements:
   - Orchestration platform: `Airflow` (or Prefect, cron)
   - Data source: PostgreSQL, BigQuery, S3, GCS, or CSV
   - Output destination: PostgreSQL, BigQuery, S3, GCS, or CSV
   - Schedule: `daily` (or hourly, weekly)
   - Model preference: `TimeGPT` with fallback to `StatsForecast`

2. Claude reads `forecasting/config.yml` and experiments
3. Generates production pipeline:
   - `pipelines/timegpt_forecast_dag.py` - Airflow DAG
   - `pipelines/monitoring.py` - Backtest checks, drift detection
   - `pipelines/README.md` - Deployment instructions

4. Review the pipeline:
   ```bash
   cat pipelines/timegpt_forecast_dag.py
   cat pipelines/monitoring.py
   ```

5. Deploy to Airflow:
   ```bash
   # Copy DAG to Airflow DAGs folder
   cp pipelines/timegpt_forecast_dag.py ~/airflow/dags/

   # Restart Airflow scheduler
   airflow scheduler
   ```

**Pipeline Features:**

- **Extract**: Pulls data from production source
- **Transform**: Converts to Nixtla schema, validates
- **Forecast**: Runs TimeGPT (or fallback to baselines)
- **Load**: Saves forecasts to destination
- **Monitor**: Backtests recent forecasts, detects data drift

**Fallback Logic:**

```
Try TimeGPT → If fails → Try MLForecast → If fails → Use StatsForecast
```

---

## Step 8: Optimize Costs (Advanced)

Audit your Nixtla usage and find cost savings using **nixtla-usage-optimizer**.

### When to Use

Use this skill when:
- You're using TimeGPT heavily
- Want to reduce API costs
- Need to justify TimeGPT ROI
- Designing routing strategies

### Activate the Skill

In Claude Code, say:
```
Use nixtla-usage-optimizer to analyze my TimeGPT usage and suggest optimizations
```

**What happens:**

1. Claude scans the repository for:
   - TimeGPT API calls (`NixtlaClient`, `.forecast()`, `.finetune()`)
   - Baseline library usage (StatsForecast, MLForecast, NeuralForecast)
   - Experiment configurations
   - Production pipelines

2. Analyzes usage patterns:
   - Where TimeGPT is used heavily (high-value or over-used?)
   - Where baselines might suffice (cost savings)
   - Where TimeGPT should be added (accuracy improvement)
   - Missing guardrails or fallback mechanisms

3. Generates comprehensive report:
   - Creates `000-docs/nixtla_usage_report.md`
   - Sections: Executive Summary, Usage Analysis, Recommendations, ROI

4. View the report:
   ```bash
   cat 000-docs/nixtla_usage_report.md
   ```

**Typical Recommendations:**

- **Batching**: Batch multiple series in single API call (~40% cost reduction)
- **Routing**: Use baselines for simple patterns, TimeGPT for complex (~30-50% savings)
- **Fallbacks**: Add fallback chain to prevent failures (improved reliability)
- **Upgrade opportunities**: Identify where TimeGPT could improve critical forecasts

**Example Routing Strategy:**

```python
def choose_model(complexity, horizon, business_impact):
    if business_impact == "high":
        return "TimeGPT"
    elif complexity == "simple" and horizon < 7:
        return "StatsForecast-AutoETS"
    else:
        return "MLForecast"
```

---

## Troubleshooting

### Issue: Skills not showing up in Claude Code

**Solution:**
1. Verify installation: `ls -la .claude/skills/`
2. Restart Claude Code
3. Ensure you're in the correct project directory

### Issue: "NIXTLA_API_KEY not set"

**Solution:**
```bash
# Set API key for current session
export NIXTLA_API_KEY='your-api-key-here'

# Or add to ~/.bashrc or ~/.zshrc for persistence
echo 'export NIXTLA_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### Issue: "nixtla package not installed"

**Solution:**
```bash
pip install nixtla statsforecast mlforecast
```

### Issue: Experiments fail with "No data found"

**Solution:**
1. Check data path in `forecasting/config.yml`
2. Verify CSV has required columns: `unique_id`, `ds`, `y`
3. Check date format: `YYYY-MM-DD` or `YYYY-MM-DD HH:MM:SS`

### Issue: Fine-tuning job times out

**Solution:**
- Reduce `finetune_steps` in config (try 50 instead of 100)
- Use smaller dataset for initial tests
- Check Nixtla API status at [status.nixtla.io](https://status.nixtla.io)

---

## What's Next?

### Learning Resources

- **Nixtla Documentation**: [docs.nixtla.io](https://docs.nixtla.io)
- **TimeGPT Tutorials**: [nixtla.io/tutorials](https://nixtla.io/tutorials)
- **StatsForecast Guide**: [nixtla.github.io/statsforecast](https://nixtla.github.io/statsforecast)
- **MLForecast Guide**: [nixtla.github.io/mlforecast](https://nixtla.github.io/mlforecast)

### Community

- **Slack**: [nixtla-community.slack.com](https://nixtla-community.slack.com)
- **GitHub Discussions**: [github.com/Nixtla/nixtla/discussions](https://github.com/Nixtla/nixtla/discussions)
- **Twitter**: [@nixtlainc](https://twitter.com/nixtlainc)

### Real-World Use Cases

After validating skills in this demo:

1. **Demand Forecasting**: Inventory planning, supply chain optimization
2. **Sales Forecasting**: Revenue planning, quota setting
3. **Energy Load Forecasting**: Grid management, capacity planning
4. **Web Traffic Forecasting**: Infrastructure scaling, ad revenue projection
5. **Financial Forecasting**: Cash flow, budget planning

---

## Important Notes

### This is a Demonstration

⚠️ **Not Production-Ready**: This demo showcases skill capabilities, but production deployments require:

- Robust error handling and logging
- Authentication and authorization
- Data validation and quality checks
- Monitoring and alerting
- Backup and disaster recovery
- Compliance and data governance
- Performance optimization and scaling
- Comprehensive testing (unit, integration, end-to-end)

### Cost Considerations

💰 **TimeGPT API Costs**:

- TimeGPT is a paid API (free tier available)
- Fine-tuning incurs additional costs
- Production pipelines should implement:
  - Batching to reduce API calls
  - Routing to use baselines where appropriate
  - Cost monitoring and alerts
  - Fallback mechanisms to prevent runaway costs

### Security

🔒 **API Key Safety**:

- Never commit API keys to git
- Use environment variables or secret managers
- Rotate keys regularly
- Restrict key permissions (read-only if possible)
- Monitor API usage for anomalies

### Support

This demo project is maintained as part of the **Nixtla Claude Skills Pack** initiative. For questions or issues:

- **Skills-related**: File an issue in the skills repository
- **Nixtla product**: Contact Nixtla support at support@nixtla.io
- **Claude Code**: Visit [claude.ai/support](https://claude.ai/support)

---

## Project Structure

```
demo-project/
├── data/
│   ├── sample_series.csv              # 3 synthetic time series (365 days each)
│   └── generate_sample_data.py        # Data generation script
│
├── forecasting/                        # Created by skills
│   ├── config.yml                     # Experiment configuration
│   ├── experiments.py                 # Experiment runner
│   ├── timegpt_finetune_job.py       # Fine-tuning job (if used)
│   └── artifacts/                     # Experiment results
│       ├── demo_quick_timegpt/
│       ├── all_models_comparison/
│       └── timegpt_finetune/
│
├── pipelines/                          # Created by prod-pipeline-generator
│   ├── timegpt_forecast_dag.py        # Airflow DAG
│   ├── monitoring.py                  # Backtest and drift detection
│   └── README.md                      # Deployment instructions
│
├── 000-docs/                           # Created by usage-optimizer
│   └── nixtla_usage_report.md         # Usage audit and recommendations
│
├── .claude/                            # Claude Code skills
│   └── skills/
│       ├── nixtla-timegpt-lab/
│       ├── nixtla-schema-mapper/
│       ├── nixtla-experiment-architect/
│       ├── nixtla-timegpt-finetune-lab/
│       ├── nixtla-prod-pipeline-generator/
│       └── nixtla-usage-optimizer/
│
├── .gitignore
└── README.md                           # This file
```

---

## License

This demo project is provided as-is for educational and demonstration purposes.

- **Nixtla Skills Pack**: Maintained by Intent Solutions (Jeremy Longshore)
- **Nixtla Libraries**: Licensed by Nixtla (see individual library licenses)
- **Sample Data**: Synthetic data, no real-world data

---

## Feedback

We'd love to hear about your experience with Nixtla skills!

- **What worked well?**
- **What was confusing?**
- **What features would you like to see?**
- **How did skills improve your workflow?**

Share your feedback:
- Email: jeremy@intentsolutions.io
- GitHub: [File an issue or discussion](https://github.com/your-repo/issues)
- Twitter: [@intent_solutions](https://twitter.com/intent_solutions)

---

**Happy Forecasting! 🚀📈**

---

*Last updated: 2025-11-30*
*Demo project version: 1.0.0*
*Nixtla Skills Pack version: 0.8.0*
