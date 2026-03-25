# Benchmark Reporter Error Handling

## Missing Metrics File

```
Error: Benchmark results not found at /path/to/results.csv
Solution: Verify path and ensure CSV file exists
```

## Invalid CSV Structure

```
Error: Required columns missing: series_id, model, sMAPE
Solution: Ensure CSV has minimum required columns
```

## Empty Results

```
Warning: No metrics found in CSV file
Solution: Verify CSV has data rows (not just headers)
```

## Regression Threshold Exceeded

```
REGRESSION DETECTED: AutoTheta sMAPE degraded by 12.5%
  Baseline: 12.3%
  Current: 13.8%
  Threshold: 5.0%
Solution: Review recent model changes, check data quality
```

## Best Practices

1. **Version Control Reports**: Commit generated reports to track performance over time
2. **Automate in CI/CD**: Generate reports automatically on every benchmark run
3. **Set Regression Thresholds**: Use `--threshold` to catch regressions early (recommend 3-5%)
4. **Include Timestamps**: Reports automatically include generation date/time
5. **Document Assumptions**: Reports include metadata about benchmark setup
6. **Share with Stakeholders**: Markdown reports render nicely on GitHub/GitLab
7. **Archive Baselines**: Keep historical baseline CSVs for regression comparison
