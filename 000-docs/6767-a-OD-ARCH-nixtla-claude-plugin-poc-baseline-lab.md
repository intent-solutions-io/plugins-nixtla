---
doc_id: 6767-OD-ARCH-nixtla-claude-plugin-poc-baseline-lab
title: Nixtla Claude Code Plugin PoC - Architecture & Design
category: Operations & Development - Architecture
status: ACTIVE
classification: Canonical Cross-Repo Standard
owner: Jeremy Longshore
collaborators:
  - Max Mergenthaler (Nixtla)
last_updated: 2025-11-24
repository: claude-code-plugins-nixtla
related_docs:
  - 6767-PP-PLAN-nixtla-claude-plugin-poc-baseline-lab.md
  - ARCHITECTURE.md
  - 004-AT-ARCH-plugin-architecture.md
---

# 6767-OD-ARCH: Nixtla Claude Code Plugin - Architecture & Design

**Document Classification**: Canonical Cross-Repo Architecture Standard
**Owner**: Jeremy Longshore (Intent Solutions)
**Status**: ACTIVE
**Last Updated**: 2025-11-24

---

## I. Technical Overview

This document defines the complete technical architecture for the **Nixtla Baseline Lab** Claude Code plugin. The plugin demonstrates a production-ready pattern for integrating Nixtla time series forecasting workflows into Claude Code conversations.

### Core Architecture Principles

1. **Separation of Concerns**
   - Commands handle user interaction
   - MCP tools execute forecasting logic
   - Skills interpret results
   - Agents provide expert analysis

2. **Composability**
   - Each component works independently
   - Components combine for powerful workflows
   - Easy to extend and maintain

3. **Local-First Development**
   - Zero external dependencies during testing
   - Fully reproducible environments
   - Clear debugging pathways

4. **Bob's Brain Patterns**
   - Specialist agent design
   - Golden task validation
   - Guardrails and safety

### Plugin Structure

The plugin lives in the repository at `plugins/nixtla-baseline-lab/`:

```
plugins/nixtla-baseline-lab/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest (REQUIRED)
├── commands/
│   └── nixtla-baseline-m4.md    # Slash command: /nixtla-baseline-m4
├── agents/
│   └── nixtla-baseline-analyst.md  # Subagent for deep analysis
├── skills/
│   └── nixtla-baseline-review/
│       ├── SKILL.md             # Skill definition
│       ├── references/
│       │   └── baseline_metrics_guide.md  # Documentation
│       ├── scripts/
│       │   └── analyze_metrics.py  # Analysis automation
│       └── assets/
│           └── metrics_template.csv  # Example output
├── .mcp.json                    # MCP server configuration
├── scripts/
│   ├── nixtla_baseline_mcp.py   # MCP server implementation
│   └── requirements.txt         # Python dependencies
├── tests/
│   ├── test_mcp_tool.py
│   ├── test_skill_invocation.py
│   └── golden_tasks/
│       └── baseline_m4_h14.yaml
└── README.md                    # Plugin documentation
```

---

## II. Components

### 1. Plugin Manifest: `.claude-plugin/plugin.json`

The manifest defines plugin metadata and component locations.

```json
{
  "name": "nixtla-baseline-lab",
  "version": "0.1.0",
  "displayName": "Nixtla Baseline Lab",
  "description": "Run Nixtla-style baseline forecasting models on public benchmark datasets from inside Claude Code conversations.",
  "author": {
    "name": "Jeremy Longshore",
    "email": "jeremy@intentsolutions.io",
    "url": "https://github.com/jeremylongshore"
  },
  "homepage": "https://github.com/intent-solutions-io/plugins-nixtla",
  "repository": {
    "type": "git",
    "url": "https://github.com/intent-solutions-io/plugins-nixtla.git"
  },
  "license": "MIT",
  "keywords": [
    "nixtla",
    "time-series",
    "forecasting",
    "baseline",
    "statsforecast",
    "m4"
  ],
  "commands": "./commands",
  "agents": "./agents",
  "skills": "./skills",
  "mcpServers": "./.mcp.json"
}
```

**Key Points**:
- `name` must be unique and kebab-case
- `version` follows semantic versioning (0.1.0 for PoC)
- All component paths are relative to plugin root
- `.claude-plugin/` directory must be at plugin root

---

### 2. MCP Server Configuration: `.mcp.json`

Defines the local MCP server for baseline forecasting.

```json
{
  "mcpServers": {
    "nixtla-baseline-mcp": {
      "command": "python",
      "args": [
        "${CLAUDE_PLUGIN_ROOT}/scripts/nixtla_baseline_mcp.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      },
      "timeout": 300000
    }
  }
}
```

**Key Points**:
- `${CLAUDE_PLUGIN_ROOT}` ensures portable absolute paths
- `timeout` is 5 minutes (300,000ms) to allow model training
- `PYTHONUNBUFFERED=1` for real-time log streaming
- Server starts automatically when plugin is enabled

---

### 3. Command: `/nixtla-baseline-m4`

Located at `commands/nixtla-baseline-m4.md`

```markdown
---
name: nixtla-baseline-m4
description: Run baseline forecasting models on M4 Daily dataset
model: sonnet
---

# Run Nixtla Baseline Models on M4 Daily Dataset

Execute baseline forecasting models (SeasonalNaive, AutoETS, AutoTheta) on the M4 Daily benchmark dataset using the Nixtla Baseline Lab MCP tool.

## Parameters

- `horizon` (optional, integer): Forecast horizon in days. Default: 14
- `series_limit` (optional, integer): Maximum number of series to process. Default: 50
- `output_dir` (optional, string): Directory for results. Default: `nixtla_baseline_m4/`

## Workflow

1. **Invoke MCP Tool**: Call `nixtla-baseline-mcp` tool `run_baselines` with parameters
2. **Process Dataset**: Load M4 Daily dataset (or use stub data in PoC phase)
3. **Run Models**: Execute SeasonalNaive, AutoETS, AutoTheta on each series
4. **Calculate Metrics**: Compute sMAPE and MASE for each model
5. **Generate Outputs**:
   - `results_M4_Daily_h{horizon}.csv` - Metrics table
   - `summary_M4_Daily_h{horizon}.txt` - Text summary
   - `notebook_M4_Daily_h{horizon}.ipynb` - Jupyter notebook (future)
6. **Return Summary**: Display top-performing models and file locations

## Example Usage

```
User: /nixtla-baseline-m4 horizon=7 series_limit=100
```

## Expected Output

```
✓ Baseline models completed on M4 Daily dataset

Summary:
- Dataset: M4-Daily (100 series)
- Horizon: 7 days
- Models: SeasonalNaive, AutoETS, AutoTheta

Results:
┌──────────────┬────────┬────────┐
│ Model        │ sMAPE  │ MASE   │
├──────────────┼────────┼────────┤
│ AutoTheta    │ 12.34% │ 0.876  │
│ AutoETS      │ 13.21% │ 0.902  │
│ SeasonalNaive│ 15.67% │ 1.023  │
└──────────────┴────────┴────────┘

Files saved to: ./nixtla_baseline_m4/
- results_M4_Daily_h7.csv
- summary_M4_Daily_h7.txt

Use the NixtlaBaselineReview skill to analyze these results.
```

## Error Handling

- **Invalid parameters**: Returns error message with valid ranges
- **MCP tool unavailable**: Graceful degradation with error explanation
- **Execution timeout**: Suggests reducing series_limit or horizon
- **File write errors**: Checks directory permissions, suggests alternatives

## Next Steps

After running this command:
1. Ask Claude to interpret results using the skill
2. Request the baseline analyst agent for deeper analysis
3. Compare with different horizons or series samples
4. Use results to inform model selection for production
```

**Key Points**:
- Frontmatter defines command metadata
- Clear parameter documentation
- Detailed workflow explanation
- Example output shows expected format
- Error handling documented

---

### 4. Agent: `nixtla-baseline-analyst`

Located at `agents/nixtla-baseline-analyst.md`

```markdown
---
name: nixtla-baseline-analyst
description: Expert agent for analyzing Nixtla baseline forecasting results and providing strategic recommendations
capabilities:
  - Interpret baseline model performance metrics
  - Compare statistical forecasting methods
  - Identify seasonality and trend patterns
  - Recommend model selection strategies
  - Explain sMAPE and MASE in business terms
---

# Nixtla Baseline Analyst Agent

You are an expert time series forecasting analyst specializing in Nixtla baseline models and benchmark datasets.

## Role & Expertise

You deeply understand:
- Statistical forecasting methods (ARIMA, ETS, Theta, SeasonalNaive)
- Benchmark datasets (M4, ETTh1, Tourism)
- Evaluation metrics (sMAPE, MASE, MAE, RMSE)
- When to use which baseline model
- How baselines inform production model selection

## When Claude Should Invoke You

Invoke this agent when the user:
- Runs `/nixtla-baseline-m4` and wants interpretation
- Asks "Which baseline model performed best?"
- Requests strategic guidance on model selection
- Wants to understand why a particular model outperformed others
- Needs help comparing results across different horizons or datasets

## Your Workflow

1. **Locate Results**
   - Use Read tool to find metrics files in `nixtla_baseline_m4/`
   - Look for `results_*.csv` files
   - Identify most recent run if multiple exist

2. **Analyze Metrics**
   - Load metrics table (series_id, model, sMAPE, MASE)
   - Calculate summary statistics (mean, median, std)
   - Identify best-performing model overall
   - Check for patterns (e.g., one model dominates certain series)

3. **Interpret Findings**
   - Explain what the metrics mean in plain language
   - Highlight key insights (e.g., "AutoTheta excels on trending series")
   - Note any surprises or anomalies
   - Contextualize performance (is 12% sMAPE good for this dataset?)

4. **Provide Recommendations**
   - Suggest which model to use for production
   - Recommend next experiments (e.g., try different horizon)
   - Identify series where all models struggled (potential data issues)
   - Propose advanced models to try (MLForecast, NeuralForecast)

5. **Document Analysis**
   - Optionally write analysis summary to markdown file
   - Include tables, key findings, recommendations
   - Save to `nixtla_baseline_m4/analysis_report.md`

## Output Format

Provide structured analysis:

```markdown
# Baseline Analysis Report
**Dataset**: M4-Daily
**Horizon**: 14 days
**Series**: 50
**Date**: 2025-11-24

## Summary Statistics
| Model         | Mean sMAPE | Median sMAPE | Std Dev |
|---------------|------------|--------------|---------|
| AutoTheta     | 12.3%      | 11.8%        | 4.2%    |
| AutoETS       | 13.5%      | 12.9%        | 5.1%    |
| SeasonalNaive | 15.2%      | 14.6%        | 6.3%    |

## Key Findings
1. **AutoTheta wins overall** with 12.3% average sMAPE
2. **Consistent performance**: AutoTheta has lowest variance
3. **SeasonalNaive struggles** on non-seasonal series (23 out of 50)

## Recommendations
- ✅ Use AutoTheta as production baseline
- 🔬 Investigate series where all models fail (potential outliers/breaks)
- 📈 Next: Try MLForecast with LightGBM for potential 15-20% improvement
```

## Tools You Can Use

- **Read**: Load metrics CSV, existing analysis files
- **Grep**: Search for specific series or models in results
- **Write**: Save analysis reports
- **Bash**: Run simple stats commands if needed (e.g., `awk`, `sort`)

## Example Invocations

**User**: "Analyze the baseline results from /nixtla-baseline-m4"
**You**: Locate files, load metrics, produce structured analysis report

**User**: "Why did AutoETS outperform Theta on series 42?"
**You**: Filter metrics to series 42, explain model characteristics, review series plot if available

**User**: "Should I use these baselines in production or train a neural network?"
**You**: Discuss baseline performance, dataset characteristics, cost/benefit of complex models
```

**Key Points**:
- Frontmatter lists specific capabilities
- Clear role definition
- Workflow steps guide agent behavior
- Output format ensures consistency
- Tool usage documented

---

### 5. Skill: `NixtlaBaselineReview`

Located at `skills/nixtla-baseline-review/SKILL.md`

```markdown
---
name: nixtla-baseline-review
description: Interpret and explain baseline forecasting results generated by Nixtla models on benchmark datasets. Use when user asks about baseline performance, model comparisons, or metric interpretation.
allowed-tools: Read, Grep, Bash(cat:*,head:*,tail:*)
model: sonnet
---

# Nixtla Baseline Review Skill

## Purpose

This skill helps Claude interpret baseline forecasting results from the `/nixtla-baseline-m4` command. It provides expert analysis of model performance metrics, identifies patterns, and recommends next steps.

## When to Use This Skill

Activate this skill when the user:
- Asks "Which baseline model performed best?"
- Requests interpretation of sMAPE or MASE metrics
- Wants to compare AutoETS vs AutoTheta vs SeasonalNaive
- Says "Explain these baseline results"
- Needs guidance on model selection based on baseline performance

## Prerequisites

- Baseline results must exist in `nixtla_baseline_m4/` directory
- At minimum, `results_*.csv` file must be present
- CSV should have columns: `series_id`, `model`, `sMAPE`, `MASE`

## Instructions

### Step 1: Locate Results Files

Use the **Read** tool to find baseline results:

```bash
# Check for results directory
ls -la nixtla_baseline_m4/

# Identify most recent results file
ls -t nixtla_baseline_m4/results_*.csv | head -1
```

Expected files:
- `results_M4_Daily_h{horizon}.csv` - Metrics table
- `summary_M4_Daily_h{horizon}.txt` - Text summary (optional)

### Step 2: Load and Parse Metrics

Read the metrics CSV:

```python
# Expected CSV structure:
# series_id,model,sMAPE,MASE
# D1,SeasonalNaive,15.23,1.05
# D1,AutoETS,13.45,0.92
# D1,AutoTheta,12.34,0.87
# D2,SeasonalNaive,18.67,1.23
# ...
```

Calculate summary statistics:
- Mean sMAPE per model
- Median sMAPE per model
- Standard deviation
- Best model per series
- Overall best model

### Step 3: Interpret Metrics

**sMAPE (Symmetric Mean Absolute Percentage Error)**:
- Measures average prediction error as percentage
- Range: 0% (perfect) to 200% (worst)
- Good: < 10%, Acceptable: 10-20%, Poor: > 20%
- Symmetric: treats over/under-prediction equally

**MASE (Mean Absolute Scaled Error)**:
- Compares forecast to naive seasonal baseline
- < 1.0: Better than seasonal naive
- 1.0: Same as seasonal naive
- > 1.0: Worse than seasonal naive

### Step 4: Identify Patterns

Look for:
- **Dominant model**: Which model wins most often?
- **Consistency**: Which model has lowest variance?
- **Series-specific patterns**: Do certain models excel on specific types of series?
- **Failure cases**: Where do all models struggle?

### Step 5: Generate Explanation

Provide a natural language explanation:

```markdown
## Baseline Performance Analysis

Based on {N} series from M4-Daily with horizon={H}:

**Overall Winner**: AutoTheta
- Mean sMAPE: 12.3% (vs 13.5% ETS, 15.2% Naive)
- Wins on 32 out of 50 series (64%)
- Consistent performance (std dev 4.2%)

**Key Insights**:
1. AutoTheta excels on trending series with weak seasonality
2. AutoETS performs better on strongly seasonal data
3. SeasonalNaive serves as a robust fallback but rarely wins

**Recommendation**: Use AutoTheta as your production baseline. It provides the best balance of accuracy and consistency across diverse series patterns.

**Next Steps**:
- Try MLForecast with LightGBM for potential 15-20% improvement
- Investigate the 5 series where all models have sMAPE > 25% (potential data quality issues)
- Consider ensemble of AutoTheta + AutoETS for robust predictions
```

## Output Format

Always structure your response with:
1. **Summary Statistics Table**: Model rankings with metrics
2. **Winner Declaration**: Best overall model with justification
3. **Insights**: 2-3 key patterns or findings
4. **Recommendations**: Actionable next steps

## Error Handling

If results files are missing:
- Check if `/nixtla-baseline-m4` was run
- Suggest running the command first
- Provide example invocation

If CSV is malformed:
- Report specific parsing error
- Suggest re-running with different parameters
- Offer to help debug

## Supporting Scripts

Optional: Use `scripts/analyze_metrics.py` for automated analysis:

```bash
python skills/nixtla-baseline-review/scripts/analyze_metrics.py \
  --input nixtla_baseline_m4/results_M4_Daily_h14.csv \
  --output analysis_report.md
```

This generates a structured markdown report you can summarize.

## Examples

### Example 1: Simple Query

**User**: "Which model was best?"

**Response**:
```
Based on the baseline results (50 series, horizon=14):

**AutoTheta won** with average sMAPE of 12.3%
- Outperformed AutoETS (13.5%) and SeasonalNaive (15.2%)
- Most consistent with std dev of 4.2%
- Recommended for production use
```

### Example 2: Detailed Comparison

**User**: "Compare AutoETS vs AutoTheta performance"

**Response**:
```
## AutoETS vs AutoTheta Comparison

| Metric        | AutoETS | AutoTheta | Winner   |
|---------------|---------|-----------|----------|
| Mean sMAPE    | 13.5%   | 12.3%     | Theta ✓  |
| Median sMAPE  | 12.9%   | 11.8%     | Theta ✓  |
| Std Dev       | 5.1%    | 4.2%      | Theta ✓  |
| Series Won    | 18/50   | 32/50     | Theta ✓  |

**Key Differences**:
- Theta handles trends better (exponential smoothing with drift)
- ETS excels on strong seasonality (state space framework)
- Theta more consistent across diverse patterns

**Recommendation**: Use AutoTheta as default, fallback to AutoETS for highly seasonal data.
```

### Example 3: Failure Analysis

**User**: "Why did all models fail on series D42?"

**Response**:
```
Series D42 shows poor performance across all models:
- SeasonalNaive: 45.6% sMAPE
- AutoETS: 42.3% sMAPE
- AutoTheta: 41.8% sMAPE

Potential causes:
1. **Structural break**: Series may have regime change mid-history
2. **Outliers**: Extreme values corrupting model training
3. **Non-stationary**: Trend or variance changing over time

**Recommendation**: Manually inspect series D42 plot, consider:
- Outlier detection/removal
- Shorter training window
- Differencing or log transformation
- Advanced models (LSTM, Prophet) for complex patterns
```
```

**Key Points**:
- Frontmatter specifies allowed tools (Read, Grep, limited Bash)
- Step-by-step instructions guide skill execution
- Detailed metric interpretation
- Multiple examples show variety of use cases
- Error handling documented

---

### 6. MCP Server Implementation: `scripts/nixtla_baseline_mcp.py`

Python MCP server that exposes the `run_baselines` tool.

```python
#!/usr/bin/env python3
"""
Nixtla Baseline Lab MCP Server

Exposes baseline forecasting tools via Model Context Protocol.
"""

import json
import sys
import logging
from pathlib import Path
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)


class NixtlaBaselineMCP:
    """MCP server for Nixtla baseline forecasting."""

    def __init__(self):
        self.version = "0.1.0"
        logger.info(f"Nixtla Baseline MCP Server v{self.version} initializing")

    def get_tools(self) -> List[Dict[str, Any]]:
        """Return list of available tools."""
        return [
            {
                "name": "run_baselines",
                "description": "Run baseline forecasting models (SeasonalNaive, AutoETS, AutoTheta) on M4 Daily dataset",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "horizon": {
                            "type": "integer",
                            "description": "Forecast horizon in days",
                            "default": 14,
                            "minimum": 1,
                            "maximum": 365
                        },
                        "series_limit": {
                            "type": "integer",
                            "description": "Maximum number of series to process",
                            "default": 50,
                            "minimum": 1,
                            "maximum": 1000
                        },
                        "output_dir": {
                            "type": "string",
                            "description": "Directory for output files",
                            "default": "nixtla_baseline_m4"
                        }
                    },
                    "required": []
                }
            }
        ]

    def run_baselines(
        self,
        horizon: int = 14,
        series_limit: int = 50,
        output_dir: str = "nixtla_baseline_m4"
    ) -> Dict[str, Any]:
        """
        Execute baseline forecasting workflow.

        Phase 1 (PoC): Returns stub/placeholder results
        Phase 2 (Future): Integrates real Nixtla libraries
        """
        logger.info(f"Running baselines: horizon={horizon}, series_limit={series_limit}")

        # Create output directory
        out_path = Path(output_dir)
        out_path.mkdir(exist_ok=True)
        logger.debug(f"Output directory: {out_path.absolute()}")

        # Phase 1: Generate stub results
        results = self._generate_stub_results(horizon, series_limit, out_path)

        return {
            "success": True,
            "message": f"Baseline models completed on M4 Daily dataset ({series_limit} series, horizon={horizon})",
            "files": results["files"],
            "summary": results["summary"]
        }

    def _generate_stub_results(
        self,
        horizon: int,
        series_limit: int,
        output_dir: Path
    ) -> Dict[str, Any]:
        """Generate placeholder results for PoC testing."""
        import random
        import csv

        logger.info("Generating stub results (Phase 1 PoC)")

        # Generate synthetic metrics
        models = ["SeasonalNaive", "AutoETS", "AutoTheta"]
        metrics_data = []

        for series_id in range(1, series_limit + 1):
            for model in models:
                # Simulate realistic metrics
                # AutoTheta typically performs best, then AutoETS, then Naive
                base_smape = {
                    "AutoTheta": random.uniform(10.0, 15.0),
                    "AutoETS": random.uniform(11.0, 16.0),
                    "SeasonalNaive": random.uniform(13.0, 18.0)
                }

                base_mase = {
                    "AutoTheta": random.uniform(0.8, 1.0),
                    "AutoETS": random.uniform(0.85, 1.05),
                    "SeasonalNaive": random.uniform(0.95, 1.15)
                }

                metrics_data.append({
                    "series_id": f"D{series_id}",
                    "model": model,
                    "sMAPE": round(base_smape[model], 2),
                    "MASE": round(base_mase[model], 3)
                })

        # Write metrics CSV
        metrics_file = output_dir / f"results_M4_Daily_h{horizon}.csv"
        with open(metrics_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["series_id", "model", "sMAPE", "MASE"])
            writer.writeheader()
            writer.writerows(metrics_data)

        logger.info(f"Wrote metrics to {metrics_file}")

        # Calculate summary statistics
        model_summaries = {}
        for model in models:
            model_metrics = [m for m in metrics_data if m["model"] == model]
            avg_smape = sum(m["sMAPE"] for m in model_metrics) / len(model_metrics)
            avg_mase = sum(m["MASE"] for m in model_metrics) / len(model_metrics)

            model_summaries[model] = {
                "avg_smape": round(avg_smape, 2),
                "avg_mase": round(avg_mase, 3)
            }

        # Write summary text
        summary_file = output_dir / f"summary_M4_Daily_h{horizon}.txt"
        with open(summary_file, 'w') as f:
            f.write(f"Baseline Results Summary\n")
            f.write(f"Dataset: M4-Daily\n")
            f.write(f"Series: {series_limit}\n")
            f.write(f"Horizon: {horizon} days\n\n")
            f.write(f"Average Metrics by Model:\n")
            for model, stats in sorted(model_summaries.items(), key=lambda x: x[1]["avg_smape"]):
                f.write(f"  {model:20s} - sMAPE: {stats['avg_smape']:6.2f}%  MASE: {stats['avg_mase']:.3f}\n")

        logger.info(f"Wrote summary to {summary_file}")

        return {
            "files": [str(metrics_file), str(summary_file)],
            "summary": model_summaries
        }

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP request."""
        method = request.get("method")
        params = request.get("params", {})

        logger.debug(f"Handling request: {method}")

        if method == "tools/list":
            return {"tools": self.get_tools()}

        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})

            if tool_name == "run_baselines":
                result = self.run_baselines(**arguments)
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ]
                }
            else:
                return {"error": f"Unknown tool: {tool_name}"}

        else:
            return {"error": f"Unknown method: {method}"}

    def run(self):
        """Main server loop."""
        logger.info("MCP server started, waiting for requests...")

        for line in sys.stdin:
            try:
                request = json.loads(line)
                response = self.handle_request(request)
                print(json.dumps(response), flush=True)
            except Exception as e:
                logger.error(f"Error handling request: {e}", exc_info=True)
                print(json.dumps({"error": str(e)}), flush=True)


if __name__ == "__main__":
    server = NixtlaBaselineMCP()
    server.run()
```

**Key Points**:
- JSON-RPC style MCP protocol
- Stub implementation for Phase 1 testing
- Clear logging to stderr
- Structured output with metrics CSV and summary
- Ready to replace stub with real Nixtla libraries

---

## III. Data Flow

### Complete Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ 1. USER INITIATES                                           │
│    /nixtla-baseline-m4 horizon=14 series_limit=50          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. COMMAND PROCESSING                                       │
│    - Parse parameters                                       │
│    - Validate inputs                                        │
│    - Prepare MCP tool invocation                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. MCP TOOL EXECUTION                                       │
│    Tool: nixtla-baseline-mcp::run_baselines                │
│    - Load M4 Daily dataset (or stub)                       │
│    - Run SeasonalNaive, AutoETS, AutoTheta                 │
│    - Calculate sMAPE and MASE metrics                      │
│    - Generate outputs                                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. FILE GENERATION                                          │
│    nixtla_baseline_m4/                                     │
│    ├── results_M4_Daily_h14.csv                            │
│    └── summary_M4_Daily_h14.txt                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. COMMAND RESPONSE                                         │
│    - Display summary table                                  │
│    - List file locations                                    │
│    - Suggest next steps (use skill/agent)                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. USER FOLLOW-UP                                           │
│    "Which model performed best?"                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. SKILL ACTIVATION                                         │
│    - Claude matches query to NixtlaBaselineReview skill    │
│    - Skill loads results_*.csv                             │
│    - Calculates summary statistics                         │
│    - Generates natural language explanation                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 8. SKILL RESPONSE                                           │
│    "AutoTheta won with 12.3% sMAPE..."                     │
│    [Structured analysis with insights]                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 9. OPTIONAL: AGENT DEEP DIVE                                │
│    User: "Use nixtla-baseline-analyst for full analysis"  │
│    - Agent reads files                                      │
│    - Produces comprehensive report                          │
│    - Writes analysis_report.md                             │
└─────────────────────────────────────────────────────────────┘
```

### Data Formats

**Metrics CSV** (`results_M4_Daily_h14.csv`):
```csv
series_id,model,sMAPE,MASE
D1,SeasonalNaive,15.23,1.05
D1,AutoETS,13.45,0.92
D1,AutoTheta,12.34,0.87
D2,SeasonalNaive,18.67,1.23
D2,AutoETS,14.21,0.98
D2,AutoTheta,13.89,0.95
...
```

**Summary Text** (`summary_M4_Daily_h14.txt`):
```
Baseline Results Summary
Dataset: M4-Daily
Series: 50
Horizon: 14 days

Average Metrics by Model:
  AutoTheta            - sMAPE:  12.34%  MASE: 0.876
  AutoETS              - sMAPE:  13.21%  MASE: 0.902
  SeasonalNaive        - sMAPE:  15.67%  MASE: 1.023
```

---

## IV. Local Testing & Debugging

### Phase 1: Plugin Loading

**Enable the plugin**:
```bash
# Install plugin locally
cd nixtla-baseline-lab
claude plugins install .

# Verify installation
claude plugins list | grep nixtla-baseline-lab

# Enable with debug logging
claude --debug
```

**Expected output**:
```
✓ Plugin nixtla-baseline-lab loaded
  - Commands: 1 (/nixtla-baseline-m4)
  - Agents: 1 (nixtla-baseline-analyst)
  - Skills: 1 (nixtla-baseline-review)
  - MCP Servers: 1 (nixtla-baseline-mcp)
```

**Debug checks**:
```bash
# Check MCP server started
ps aux | grep nixtla_baseline_mcp

# Check logs
tail -f ~/.claude/logs/plugin-nixtla-baseline-lab.log
```

---

### Phase 2: Command Execution

**Run the command**:
```bash
# In Claude Code conversation
/nixtla-baseline-m4 horizon=7 series_limit=10
```

**Verify outputs**:
```bash
# Check files created
ls -la nixtla_baseline_m4/
# Should see:
# - results_M4_Daily_h7.csv
# - summary_M4_Daily_h7.txt

# Inspect CSV
head nixtla_baseline_m4/results_M4_Daily_h7.csv

# Check summary
cat nixtla_baseline_m4/summary_M4_Daily_h7.txt
```

**Debug MCP communication**:
```bash
# Check MCP server logs (stderr)
# Look for:
# - "Running baselines: horizon=7, series_limit=10"
# - "Wrote metrics to ..."
# - "Wrote summary to ..."
```

---

### Phase 3: Skill Invocation

**Trigger the skill**:
```
User: Which baseline model performed best on the M4 dataset?
```

**Verify skill activation**:
```bash
# Check Claude logs for:
# "Activating skill: nixtla-baseline-review"
# "Reading file: nixtla_baseline_m4/results_M4_Daily_h7.csv"
```

**Expected response format**:
- Summary statistics table
- Winner declaration
- Key insights (2-3 bullet points)
- Recommendations

**Test variations**:
```
- "Compare AutoETS and AutoTheta"
- "Explain what sMAPE means in these results"
- "Why did all models fail on series D5?"
```

---

### Phase 4: Agent Testing

**Invoke the agent**:
```
User: Use the nixtla-baseline-analyst to analyze these results in detail
```

**Verify agent behavior**:
- Agent loads using Read tool
- Calculates summary statistics
- Produces structured markdown report
- Optionally writes analysis_report.md

**Check agent output**:
```bash
# If agent wrote report
cat nixtla_baseline_m4/analysis_report.md
```

---

### Debugging Tips

**MCP server not starting**:
```bash
# Manually test MCP server
cd scripts
python nixtla_baseline_mcp.py

# Send test request (stdin):
{"method": "tools/list", "params": {}}

# Should return tools list
```

**Skill not activating**:
- Check skill description in frontmatter
- Try more explicit trigger phrases
- Review Claude logs for skill matching

**Files not found**:
- Verify output_dir parameter
- Check file permissions
- Look for error messages in MCP logs

---

## V. Future Extensions

### Phase 2: Real Nixtla Integration

Replace stub implementation with actual libraries:

```python
# In nixtla_baseline_mcp.py
from statsforecast import StatsForecast
from statsforecast.models import SeasonalNaive, AutoETS, AutoTheta
from datasetsforecast.m4 import M4

def _run_real_baselines(self, horizon, series_limit, output_dir):
    """Run actual Nixtla baseline models."""

    # Load M4 Daily dataset
    df, *_ = M4.load(directory='data', group='Daily')
    df = df.head(series_limit)  # Sample series

    # Define models
    models = [
        SeasonalNaive(season_length=7),
        AutoETS(season_length=7),
        AutoTheta(season_length=7)
    ]

    # Run StatsForecast
    sf = StatsForecast(
        models=models,
        freq='D',
        n_jobs=-1
    )

    # Fit and forecast
    forecasts = sf.forecast(h=horizon, df=df)

    # Calculate metrics
    metrics = self._calculate_metrics(df, forecasts, horizon)

    return metrics
```

### Phase 3: Multi-Dataset Support

Extend command to support multiple datasets:

```markdown
---
name: nixtla-baseline
description: Run baseline models on any benchmark dataset
---

## Parameters
- `dataset`: M4-Daily, M4-Monthly, ETTh1, Tourism, Traffic
- `horizon`: Forecast steps
- `models`: Comma-separated list (naive,ets,theta,arima)
```

### Phase 4: Visualization

Add plotting capabilities:

```python
def _generate_plots(self, df, forecasts, output_dir):
    """Generate forecast plots."""
    import matplotlib.pyplot as plt

    # Plot top 5 series
    for series_id in df['unique_id'].unique()[:5]:
        fig, ax = plt.subplots()
        # Plot historical + forecasts
        # ...
        fig.savefig(output_dir / f'plot_{series_id}.png')
```

### Phase 5: Bob's Brain Integration

Connect to orchestrator agent:

- A2A protocol for agent communication
- Golden tasks for automated validation
- CI integration for regression testing
- Slack notifications for results

---

## VI. Appendices

### A. Dependencies

**Python Requirements** (`scripts/requirements.txt`):
```
# Phase 1 (PoC)
# No dependencies - uses stdlib only

# Phase 2 (Real Integration)
statsforecast>=1.5.0
datasetsforecast>=0.0.8
pandas>=2.0.0
numpy>=1.24.0

# Optional
matplotlib>=3.7.0  # For visualizations
jupyter>=1.0.0     # For notebooks
```

### B. Testing Framework

**Golden Task** (`tests/golden_tasks/baseline_m4_h14.yaml`):
```yaml
name: baseline_m4_h14
description: Validate baseline command with horizon=14
steps:
  - action: run_command
    command: /nixtla-baseline-m4
    params:
      horizon: 14
      series_limit: 10
    expect:
      - file_exists: nixtla_baseline_m4/results_M4_Daily_h14.csv
      - file_exists: nixtla_baseline_m4/summary_M4_Daily_h14.txt
      - csv_has_rows: 30  # 10 series * 3 models
      - csv_has_columns: [series_id, model, sMAPE, MASE]

  - action: ask_question
    query: "Which model performed best?"
    expect:
      - skill_activated: nixtla-baseline-review
      - response_contains: ["AutoTheta", "sMAPE", "MASE"]
```

### C. File Permissions

Ensure scripts are executable:
```bash
chmod +x scripts/nixtla_baseline_mcp.py
chmod +x skills/nixtla-baseline-review/scripts/analyze_metrics.py
```

### D. Environment Variables

Optional configuration:
```bash
# Increase MCP timeout for large datasets
export CLAUDE_MCP_TIMEOUT=600000  # 10 minutes

# Debug logging
export CLAUDE_DEBUG=1
export PYTHONUNBUFFERED=1
```

---

**Document Version**: 1.0.0
**Created**: 2025-11-24
**Next Review**: After Phase 2 implementation
**Maintainer**: Jeremy Longshore (jeremy@intentsolutions.io)
