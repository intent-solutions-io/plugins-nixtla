# Research Assistant Examples

## Example 1: Recent Updates Request

**User**: "What's new with TimeGPT?"

**Response structure**:

```markdown
# TimeGPT Recent Updates

Searching for recent TimeGPT developments...

## 1. TimeGPT API v2.0 Released (Nov 20, 2025)
**Source**: GitHub Release | **Relevance**: High

### Summary
TimeGPT API v2.0 introduces multivariate forecasting support, improved accuracy on
irregular time series, and a new Python SDK with async/await capabilities.

### Key Points
- Multivariate support: Handle up to 100 related time series simultaneously
- 15% accuracy improvement on M5 competition benchmarks
- New async Python client for better performance
- Breaking change: Old SDK deprecated, migration guide available

### Why This Matters
Enables enterprise use cases requiring multi-series forecasting without building
custom solutions. The async client significantly speeds up batch predictions.

[View Release Notes](https://github.com/Nixtla/nixtla/releases/tag/v2.0.0)

---

Found 3 more relevant updates. Would you like me to continue with the rest?
```

## Example 2: Model Comparison

**User**: "Compare StatsForecast and TimeGPT for retail forecasting"

Provide a detailed comparison table with pros/cons, use cases, and code examples.

## Example 3: Triggering Automated Digest

**User**: "Run a Nixtla digest and post to Slack"

Execute: `python -m nixtla_search_to_slack --topic nixtla-core`

See [slack-integration](slack-integration.md) for full integration commands.
