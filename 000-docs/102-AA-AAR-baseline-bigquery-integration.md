# AAR: Three-Plugin Workflow Integration

**Document ID**: 102-AA-AAR-baseline-bigquery-integration
**Date**: 2025-12-10
**Status**: IN PROGRESS (Feature Branch)
**Branch**: `feature/baseline-bigquery-integration`

---

## What This Is

We have 3 plugins that work together as a forecasting workflow:

1. **baseline-lab** - Test different models, find which one works best
2. **bigquery-forecaster** - Run the winning model on your real BigQuery data
3. **results-notifier** (formerly search-to-slack) - Send forecast results to Slack/email

The documentation said these plugins "integrate" but the actual code to connect them didn't exist. This work builds that connection.

**Current State**: Code written, baseline-lab tested and verified. Full workflow pending GCP access.

---

## Context

### The Problem

The docs said the plugins work together, but they didn't actually connect. The CEO has these docs. DevOps is testing this week.

### Why It Matters

You can't test models on one dataset (M4 benchmark data) and then use the "winner" on different data (your BigQuery data). That's not a fair comparison - the model that wins on M4 might lose on your actual data.

### The Fix

Test models on a sample of YOUR actual data, then run the winner on all of it:

```
Your BigQuery Data
        │
        ├── Take a sample (100 time series)
        │       │
        │       └── Test 3 models → AutoETS wins!
        │
        └── Run AutoETS on ALL your data → Forecasts
```

Same data source = fair comparison.

---

## What Was Built

### New Files Created

| File | Purpose |
|------|---------|
| `bigquery-forecaster/scripts/extract_sample.py` | Pull representative sample from BigQuery → CSV |
| `bigquery-forecaster/scripts/full_workflow.py` | Orchestration script for complete pipeline |
| `bigquery-forecaster/commands/nixtla-full-workflow.md` | Slash command documentation |

### Files Modified

| File | Changes |
|------|---------|
| `baseline-lab/scripts/nixtla_baseline_mcp.py` | Added `export_winning_model_config()` tool |
| `bigquery-forecaster/src/main.py` | Added `model_config_path` parameter support |

### Integration Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│  STEP 1: SAMPLE EXTRACTION                                              │
│  bigquery-forecaster/scripts/extract_sample.py                         │
│                                                                         │
│  BigQuery → sample.csv (100 series, 30+ points each)                   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  STEP 2: BASELINE TESTING                                               │
│  baseline-lab/scripts/nixtla_baseline_mcp.py                           │
│                                                                         │
│  sample.csv → [AutoETS, AutoTheta, SeasonalNaive] → metrics.csv        │
│  Same data, 3 different models, compare sMAPE/MASE                     │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  STEP 3: WINNER EXPORT                                                  │
│  baseline-lab/scripts/nixtla_baseline_mcp.py (export_winning_model)    │
│                                                                         │
│  metrics.csv → winning_model_config.json                               │
│  {                                                                      │
│    "winning_model": {"name": "AutoETS", "smape": 0.77, "mase": 0.42}  │
│  }                                                                      │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  STEP 4: PRODUCTION FORECAST                                            │
│  bigquery-forecaster/src/main.py                                       │
│                                                                         │
│  winning_model_config.json + Full BigQuery data → Forecasts            │
│  Run only the winning model at scale                                   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  STEP 5: RESULTS NOTIFICATION                                           │
│  results-notifier (formerly search-to-slack)                           │
│                                                                         │
│  Forecasts → Slack channel + Email                                     │
│  "Your forecasts are ready" - delivery layer for the workflow          │
└─────────────────────────────────────────────────────────────────────────┘
```

### New MCP Tool: `export_winning_model_config`

Added to baseline-lab MCP server:

```python
{
    "name": "export_winning_model_config",
    "description": "Export winning model configuration for bigquery-forecaster",
    "inputSchema": {
        "properties": {
            "metrics_csv_path": {"type": "string"},
            "output_path": {"type": "string"}
        }
    }
}
```

Output format (`winning_model_config.json`):

```json
{
  "version": "1.0",
  "generated_by": "nixtla-baseline-lab",
  "generated_at": "2025-12-10T12:00:00Z",
  "winning_model": {
    "name": "AutoETS",
    "smape": 0.77,
    "mase": 0.422
  },
  "all_models": [
    {"name": "AutoETS", "smape": 0.77, "mase": 0.422},
    {"name": "AutoTheta", "smape": 0.85, "mase": 0.454},
    {"name": "SeasonalNaive", "smape": 1.49, "mase": 0.898}
  ],
  "config": {
    "freq": "D",
    "season_length": 7,
    "horizon": 7
  }
}
```

---

## Test Results (2025-12-10)

### Baseline Lab Smoke Test: PASSED

Verified the MCP server correctly runs forecasting models on M4 sample data.

**Environment**:
- Python 3.12.3
- statsforecast 2.0.3
- datasetsforecast 1.0.0

**Results** (5 series, horizon=7):

| Model | sMAPE | MASE | Rank |
|-------|-------|------|------|
| **AutoETS** | 0.77% | 0.422 | 1st (Winner) |
| AutoTheta | 0.85% | 0.454 | 2nd |
| SeasonalNaive | 1.49% | 0.898 | 3rd |

**Verified**:
- Model comparison working correctly
- Winner selection by lowest sMAPE
- `export_winning_model_config()` generates valid JSON

**Test Record**: `000-docs/103-QA-TEST-baseline-lab-smoke.md`

---

## Also Completed (Same Branch)

### Results-Notifier Plugin (formerly Search-to-Slack)

**Reconceived purpose**: The third plugin is now the "results-notifier" - it sends forecast results to Slack/email, not news search.

Removed unnecessary external API dependencies:

| Removed | Reason |
|---------|--------|
| SerpAPI | Claude Code has built-in WebSearch |
| Anthropic API | Claude Code IS Claude |
| OpenAI API | Not needed |
| Google/Bing/Brave APIs | Claude Code WebSearch handles this |

**Files modified:**
- `search-to-slack/ai_curator.py` - Simplified to keyword-based scoring
- `search-to-slack/main.py` - Removed AI API key requirements
- `search-to-slack/web_search_providers.py` - Stub that defers to Claude Code
- `search-to-slack/.env.example` - Only Slack + GitHub tokens needed
- `search-to-slack/requirements.txt` - Removed anthropic, openai dependencies

**New API key requirements:**
- Slack bot token (required)
- GitHub token (required)
- ~~Anthropic API key~~ (removed)
- ~~SerpAPI key~~ (removed)

---

## Outstanding Work

### Not Yet Completed

| Task | Status | Blockers |
|------|--------|----------|
| End-to-end testing | Pending | Needs GCP credentials with BigQuery access |
| Update plugin-docs | Pending | Waiting for test validation |
| Push to remote | Blocked | Awaiting user approval |

### Testing Requirements

To test the full workflow:

```bash
# Requires GCP credentials
python scripts/full_workflow.py \
    --project YOUR_PROJECT \
    --dataset YOUR_DATASET \
    --table YOUR_TABLE \
    --timestamp-col date \
    --value-col value \
    --group-by series_id
```

---

## Risk Assessment

### Mitigated Risks

| Risk | Mitigation |
|------|------------|
| Breaking existing baseline-lab | Feature branch, main untouched |
| Invalid model comparison | Fixed by sampling from same data source |
| Documentation mismatch | AAR documents current state |

### Remaining Risks

| Risk | Impact | Probability |
|------|--------|-------------|
| GCP permissions issues during testing | Medium | Medium |
| Full workflow performance unknown | Low | Low |
| CEO sees unfinished work | High | Low (feature branch) |

---

## Git Status

**Branch**: `feature/baseline-bigquery-integration`
**Base**: `main`
**Pushed**: No

```
Modified files:
  M 005-plugins/nixtla-baseline-lab/scripts/nixtla_baseline_mcp.py
  M 005-plugins/nixtla-bigquery-forecaster/src/main.py
  M 005-plugins/nixtla-search-to-slack/.env.example
  M 005-plugins/nixtla-search-to-slack/QUICKSTART.md
  M 005-plugins/nixtla-search-to-slack/requirements.txt
  M 005-plugins/nixtla-search-to-slack/src/nixtla_search_to_slack/ai_curator.py
  M 005-plugins/nixtla-search-to-slack/src/nixtla_search_to_slack/main.py
  M 005-plugins/nixtla-search-to-slack/src/nixtla_search_to_slack/web_search_providers.py

New files:
  ?? 005-plugins/nixtla-bigquery-forecaster/commands/
  ?? 005-plugins/nixtla-bigquery-forecaster/scripts/extract_sample.py
  ?? 005-plugins/nixtla-bigquery-forecaster/scripts/full_workflow.py
```

---

## Next Steps

1. **Test locally** with GCP credentials (if available)
2. **Update plugin-docs** to reflect actual integration
3. **Review with user** before pushing
4. **Merge to main** when ready for DevOps testing

---

## Lessons Learned

1. **Documentation claims must match implementation** - Aspirational features should be clearly marked
2. **Scientific validity matters** - Model comparison requires same data source
3. **Claude Code plugins can leverage built-in tools** - No need for separate API keys for search/AI

---

**Report prepared by**: Claude Code
**Initial**: 2025-12-10T02:30:00Z
**Updated**: 2025-12-10T02:45:00Z (added test results, corrected third plugin purpose)
