# Plugin Architecture Enhancement Plan

**Document ID**: 100-PP-STRAT-cto-plugin-enhancement-plan
**Version**: 2.0.0
**Date**: 2025-12-06
**Status**: Technical Specification

---

## 1. Current State Assessment

### 1.1 Plugin Compliance Audit Results

| Plugin | Compliance | Critical Issues |
|--------|------------|-----------------|
| nixtla-baseline-lab | 85% | Missing LICENSE, repository field format, skill frontmatter |
| nixtla-bigquery-forecaster | 60% | Missing LICENSE, missing declared directories, incomplete structure |
| nixtla-search-to-slack | 50% | Missing LICENSE, non-standard skill format, schema violations |

### 1.2 Prediction Markets Vertical Status

**Documentation Complete**:
- 7 Production Requirement Documents (PRDs)
- 7 Architecture Reference Documents (ARDs)
- Global skill schema specification
- API feasibility analysis (Polymarket, TimeGPT, Kalshi)

**Implementation Status**: None. All documentation, no executable code.

---

## 2. Technical Enhancement Plan

### Phase 1: Compliance Remediation

**Objective**: Bring all existing plugins to 100% specification compliance.

**Scope**:

1. **All Plugins**
   - Add MIT LICENSE file
   - Standardize `repository` field to string format per spec

2. **nixtla-baseline-lab**
   - Agent frontmatter: Replace `capabilities` with standard `tools` field
   - Skill frontmatter: Correct `allowed-tools` from `Read, Grep, Bash` to `"Read,Grep,Bash"`

3. **nixtla-bigquery-forecaster**
   - Create `commands/` directory or remove from manifest
   - Create `.mcp.json` or remove from manifest
   - Move `sponsor` metadata to README

4. **nixtla-search-to-slack**
   - Restructure skills from flat files to `skill-name/SKILL.md` directories
   - Convert `allowed-tools` from YAML array to CSV string
   - Remove non-standard manifest fields or document as extensions

**Estimated Duration**: 2-4 hours

---

### Phase 2: Prediction Markets Plugin Development

**Objective**: Implement working forecasting infrastructure for prediction market time series data.

#### 2.1 Technical Architecture

```
nixtla-polymarket-forecaster/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── forecast.md                 # Generate time series forecast
│   ├── backtest.md                 # Historical accuracy validation
│   └── compare.md                  # Cross-platform price comparison
├── agents/
│   └── analyst.md                  # Market data analysis agent
├── skills/
│   ├── nixtla-polymarket-analyst/
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       ├── fetch_market_data.py
│   │       ├── transform_schema.py
│   │       └── generate_forecast.py
│   └── nixtla-contract-schema-mapper/
│       └── SKILL.md
├── scripts/
│   ├── polymarket_client.py        # GraphQL client for market data
│   ├── timegpt_forecaster.py       # TimeGPT API wrapper with StatsForecast fallback
│   ├── kalshi_client.py            # REST client for comparative data
│   └── metrics.py                  # sMAPE, MASE, directional accuracy
├── tests/
│   ├── test_polymarket_client.py
│   ├── test_forecaster.py
│   └── test_integration.py
├── .mcp.json
├── README.md
├── LICENSE
└── requirements.txt
```

#### 2.2 Data Pipeline

```
Polymarket GraphQL API
        │
        ▼
┌─────────────────────┐
│ fetch_market_data.py│  Extract historical odds (OHLC-style)
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ transform_schema.py │  Convert to Nixtla format (unique_id, ds, y)
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ timegpt_forecaster  │  TimeGPT API call (fallback: StatsForecast)
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ Forecast Output     │  Point forecast + prediction intervals
└─────────────────────┘
```

#### 2.3 API Dependencies

| API | Authentication | Rate Limit | Fallback |
|-----|----------------|------------|----------|
| Polymarket GraphQL | None (public) | 100 req/min | None (primary source) |
| Nixtla TimeGPT | API key required | 1000/month free | StatsForecast (local) |
| Kalshi REST | API key required | 60 req/min | Optional, degraded functionality |

#### 2.4 Forecasting Methodology

**Input**: Historical contract prices as time series
- Frequency: Hourly or daily aggregation
- Minimum history: 30 observations
- Format: `unique_id` (contract slug), `ds` (timestamp), `y` (price 0-1)

**Model Selection**:
- Primary: TimeGPT (foundation model, handles irregularities)
- Fallback: StatsForecast AutoTheta (proven M4 performance)

**Output**:
- Point forecast (h=7 days default)
- Prediction intervals (80%, 95%)
- Forecast uncertainty quantification

**Validation Metrics**:
- sMAPE: Symmetric mean absolute percentage error
- MASE: Mean absolute scaled error (vs seasonal naive)
- Directional accuracy: % correct direction predictions

#### 2.5 Implementation Phases

| Phase | Scope | Validation Criteria |
|-------|-------|---------------------|
| 2a | Polymarket client, schema transformation | Unit tests pass, data flows correctly |
| 2b | TimeGPT integration, fallback logic | Forecasts generated, API errors handled |
| 2c | Commands and skill implementation | `/forecast` command produces valid output |
| 2d | Backtesting infrastructure | Historical accuracy metrics computable |
| 2e | Cross-platform comparison (Kalshi) | Price differential calculation working |

**Estimated Duration**: 5-7 days

---

### Phase 3: Validation and Testing

**Objective**: Establish forecast accuracy baselines and ensure reliability.

#### 3.1 Backtesting Framework

```python
# Expanding window backtest
for t in range(min_history, len(series) - horizon):
    train = series[:t]
    actual = series[t:t+horizon]
    forecast = model.predict(train, h=horizon)
    metrics.append(calculate_metrics(actual, forecast))
```

#### 3.2 Accuracy Benchmarks

Target metrics (based on M4 competition baselines):

| Metric | Target | Interpretation |
|--------|--------|----------------|
| sMAPE | <15% | Acceptable for daily financial data |
| MASE | <1.0 | Better than seasonal naive |
| Directional | >55% | Better than random |

#### 3.3 Test Coverage Requirements

- Unit tests: All utility functions
- Integration tests: End-to-end pipeline
- API mocking: Offline test capability
- Error handling: Graceful degradation on API failures

---

## 3. Deliverables

### Phase 1 Deliverables
- [ ] 3 plugins at 100% spec compliance
- [ ] All LICENSE files added
- [ ] All schema violations corrected

### Phase 2 Deliverables
- [ ] Working `nixtla-polymarket-forecaster` plugin
- [ ] Polymarket data extraction functional
- [ ] TimeGPT forecasting operational
- [ ] StatsForecast fallback implemented
- [ ] Basic backtesting capability

### Phase 3 Deliverables
- [ ] Documented accuracy metrics
- [ ] Test suite with >80% coverage
- [ ] Performance benchmarks

---

## 4. Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| TimeGPT API quota exhaustion | Medium | Medium | StatsForecast fallback, request batching |
| Polymarket schema changes | Low | High | Version pinning, schema validation |
| Low forecast accuracy | Medium | High | Document limitations, focus on methodology |
| Kalshi API approval delay | High | Low | Make Kalshi integration optional |

---

## 5. Success Criteria

1. **Compliance**: All 4 plugins pass automated schema validation
2. **Functionality**: End-to-end forecast generation completes without error
3. **Reliability**: 95%+ success rate on API calls with proper error handling
4. **Reproducibility**: Any forecast can be regenerated with same inputs
5. **Documentation**: Technical documentation sufficient for independent replication

---

## 6. Timeline

| Week | Phase | Milestone |
|------|-------|-----------|
| 1, Days 1-2 | Phase 1 | Compliance remediation complete |
| 1, Days 3-7 | Phase 2a-2c | Core forecasting pipeline working |
| 2, Days 1-3 | Phase 2d-2e | Backtesting and cross-platform complete |
| 2, Days 4-5 | Phase 3 | Validation and documentation |

---

## 7. Dependencies

**Required**:
- Python 3.10+
- `nixtla` SDK (TimeGPT client)
- `statsforecast` (fallback models)
- `requests` (API clients)
- `pandas` (data manipulation)

**Optional**:
- `pytest` (testing)
- `streamlit` (visualization, if needed)

---

## 8. References

- Nixtla TimeGPT Documentation: https://docs.nixtla.io/
- Polymarket API: https://docs.polymarket.com/
- StatsForecast: https://nixtla.github.io/statsforecast/
- M4 Competition Results: Makridakis et al. (2020)

---

**Document Status**: Ready for implementation
