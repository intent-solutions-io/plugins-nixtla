---
name: nixtla-usage-optimizer
description: |
  Audits Nixtla API usage and recommends cost-effective routing.
  Use when optimizing TimeGPT API costs, understanding API usage patterns, or reducing expenses.
  Trigger with "optimize Nixtla costs", "analyze TimeGPT usage", "reduce API expenses".
allowed-tools: "Read,Glob,Grep"
version: "1.0.0"
---

# Nixtla Usage Optimizer

Analyzes Nixtla API usage to provide cost optimization recommendations.

## Overview

This skill audits your TimeGPT API usage by analyzing API logs and configurations. It identifies potential areas for cost savings, such as inefficient routing or unnecessary API calls. The skill recommends alternative configurations or routing strategies to minimize expenses. The output includes a detailed report of your current usage and actionable suggestions for optimization.

## Prerequisites

**Tools**: Read, Glob, Grep

**Environment**: `NIXTLA_API_LOG_PATH`, `NIXTLA_API_CONFIG_PATH`

**Packages**:
```bash
pip install pandas matplotlib nixtla
```

## Instructions

### Step 1: Gather data

Read API logs from `NIXTLA_API_LOG_PATH` and configuration from `NIXTLA_API_CONFIG_PATH`.

```bash
export NIXTLA_API_LOG_PATH=/path/to/api_logs.json
export NIXTLA_API_CONFIG_PATH=/path/to/api_config.json

python {baseDir}/scripts/gather_data.py
```

**Log format**: JSON lines with fields: timestamp, region, endpoint, etc.

**Config format**: JSON with fields: regions, caching_enabled, data_retention_policy

### Step 2: Analyze usage

Identify usage patterns: frequency, region, and API endpoint.

```bash
python {baseDir}/scripts/analyze_usage.py \
  --log_path $NIXTLA_API_LOG_PATH
```

**Outputs**:
- api_call_frequency.png (hourly call frequency chart)
- api_usage_by_region.png (calls by region)
- api_usage_by_endpoint.png (calls by endpoint)
- usage_patterns.json (patterns data)

### Step 3: Generate recommendations

Based on the analysis, suggest cost-effective routing and configuration changes.

```bash
python {baseDir}/scripts/generate_recommendations.py \
  --usage_patterns usage_patterns.json \
  --api_config $NIXTLA_API_CONFIG_PATH
```

**Output**: recommendations.json (list of optimization suggestions)

### Step 4: Output report

Create a report with current usage statistics and optimization recommendations.

```bash
python {baseDir}/scripts/generate_report.py \
  --usage_patterns usage_patterns.json \
  --recommendations recommendations.json \
  --output_dir reports
```

**Outputs**:
- reports/usage_report.txt (detailed usage statistics)
- reports/optimization_recommendations.txt (specific recommendations)
- reports/potential_savings.txt (estimated cost savings)

## Output

- **usage_report.txt**: Detailed usage statistics and analysis
- **optimization_recommendations.txt**: Specific recommendations for cost optimization
- **potential_savings.txt**: Estimated cost savings from implementing recommendations
- **api_call_frequency.png**: Hourly API call frequency visualization
- **api_usage_by_region.png**: API usage by region visualization
- **api_usage_by_endpoint.png**: API usage by endpoint visualization

## Error Handling

1. **Error**: `NIXTLA_API_LOG_PATH not set`
   **Solution**: `export NIXTLA_API_LOG_PATH=/path/to/your/api_logs.log`

2. **Error**: `NIXTLA_API_CONFIG_PATH not set`
   **Solution**: `export NIXTLA_API_CONFIG_PATH=/path/to/your/api_config.json`

3. **Error**: `Invalid log format`
   **Solution**: Ensure logs are in a readable format (JSON or CSV with required columns)

4. **Error**: `Insufficient data for analysis`
   **Solution**: Ensure API logs cover a reasonable time period (at least 7 days recommended)

5. **Error**: `Failed to load API logs or configuration`
   **Solution**: Verify file paths are correct and files are accessible

## Examples

### Example 1: High latency routing

**Input**: API logs showing high latency from US region to EU server

**Command**:
```bash
python {baseDir}/scripts/generate_recommendations.py \
  --usage_patterns usage_patterns.json \
  --api_config api_config.json
```

**Output**: Recommends routing US requests to US-based server to reduce latency and cost

### Example 2: Unnecessary API calls

**Input**: API logs showing redundant calls to the same TimeGPT endpoint

**Command**:
```bash
python {baseDir}/scripts/analyze_usage.py --log_path api_logs.json
```

**Output**: Recommends caching results or optimizing API call frequency to reduce unnecessary usage

## Resources

- Data gatherer: `{baseDir}/scripts/gather_data.py`
- Usage analyzer: `{baseDir}/scripts/analyze_usage.py`
- Recommendations generator: `{baseDir}/scripts/generate_recommendations.py`
- Report generator: `{baseDir}/scripts/generate_report.py`
