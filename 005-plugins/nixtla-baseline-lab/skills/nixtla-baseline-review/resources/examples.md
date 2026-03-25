# Baseline Review Examples

## Example 1: Simple Query

**User**: "Which model was best?"

**Response**:
```
Based on the baseline results (50 series, horizon=14):

**AutoTheta won** with average sMAPE of 12.3%
- Outperformed AutoETS (13.5%) and SeasonalNaive (15.2%)
- Most consistent with std dev of 4.2%
- Recommended for production use
```

## Example 2: Detailed Comparison

**User**: "Compare AutoETS vs AutoTheta performance"

**Response**:
```
## AutoETS vs AutoTheta Comparison

| Metric        | AutoETS | AutoTheta | Winner   |
|---------------|---------|-----------|----------|
| Mean sMAPE    | 13.5%   | 12.3%     | Theta    |
| Median sMAPE  | 12.9%   | 11.8%     | Theta    |
| Std Dev       | 5.1%    | 4.2%      | Theta    |
| Series Won    | 18/50   | 32/50     | Theta    |

**Key Differences**:
- Theta handles trends better (exponential smoothing with drift)
- ETS excels on strong seasonality (state space framework)
- Theta more consistent across diverse patterns

**Recommendation**: Use AutoTheta as default, fallback to AutoETS for highly seasonal data.
```

## Example 3: Metric Interpretation

**User**: "What does sMAPE of 12.3% mean?"

**Response**:
```
sMAPE of 12.3% is **good performance** for forecasting:

- This means on average, predictions are off by about 12% from actual values
- For M4 Daily benchmark, anything under 15% is considered good
- This is in the "acceptable" range (10-20%)

Context: If forecasting daily sales of 100 units, a 12.3% sMAPE means the forecast will typically be within +/-12 units of the true value.

For more details, see resources/METRIC_INTERPRETATION.md
```
