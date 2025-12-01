# Baseline Lab - Architecture

**Plugin:** nixtla-baseline-lab
**Version:** 0.8.0
**Last Updated:** 2025-11-30

---

## System Context

Nixtla Baseline Lab integrates statsforecast baseline models into Claude Code for rapid benchmarking and reproducibility analysis.

```
┌─────────────────────────────────────────────────────────────┐
│                      User's Terminal                         │
├─────────────────────────────────────────────────────────────┤
│                      Claude Code CLI                         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐   │
│  │           Nixtla Baseline Lab Plugin                │   │
│  │  ┌───────────┐  ┌──────────┐  ┌─────────────────┐  │   │
│  │  │  Command  │  │  Skill   │  │   MCP Server    │  │   │
│  │  │/nixtla-*  │  │(Review)  │  │  (run_baselines)│  │   │
│  │  └─────┬─────┘  └────┬─────┘  └────────┬────────┘  │   │
│  └────────┼─────────────┼─────────────────┼───────────┘   │
│           │             │                 │                │
│           ▼             ▼                 ▼                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Nixtla OSS Ecosystem                    │   │
│  │  ┌─────────────────┐  ┌──────────────────────────┐  │   │
│  │  │ statsforecast   │  │  datasetsforecast (M4)   │  │   │
│  │  │ (AutoETS, etc.) │  │  (Daily, Weekly, etc.)   │  │   │
│  │  └─────────────────┘  └──────────────────────────┘  │   │
│  │                                                      │   │
│  │  ┌──────────────────────────────────────────────┐   │   │
│  │  │  nixtla SDK (TimeGPT) - Optional, Opt-In     │   │   │
│  │  └──────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Full Technical Details:** See [`6767-OD-ARCH-nixtla-claude-plugin-poc-baseline-lab.md`](../../6767-OD-ARCH-nixtla-claude-plugin-poc-baseline-lab.md)

---

## Component Design

### Components

| Component | Responsibility | Location |
|-----------|---------------|----------|
| **Slash Command** | User entry point (`/nixtla-baseline-m4`) | `commands/nixtla-baseline-m4.md` |
| **MCP Server** | Expose `run_baselines` tool to Claude | `scripts/mcp_server.py` |
| **Benchmarking Logic** | Run statsforecast models, calculate metrics | `scripts/mcp_server.py` |
| **Agent Skill** | AI-powered metric interpretation | `skills/nixtla-baseline-review/` |
| **Setup Script** | Automated Python environment setup | `scripts/setup_nixtla_env.sh` |

### Component Interactions

```
User types /nixtla-baseline-m4
        │
        ▼
Claude invokes MCP tool run_baselines
        │
        ▼
MCP Server loads M4 data + runs statsforecast
        │
        ▼
Results returned (CSV + summary + repro bundle)
        │
        ▼
Nixtla Baseline Review skill interprets metrics
        │
        ▼
Human-readable analysis delivered to user
```

---

## Data Flow

### Input
- **User Parameters**: `demo_preset` (m4_daily_small, m4_weekly_full, etc.)
- **Optional**: `include_timegpt=true` (triggers TimeGPT comparison)

### Processing
1. Load M4 dataset from datasetsforecast
2. Run statsforecast models (AutoETS, AutoTheta, SeasonalNaive)
3. Calculate metrics (sMAPE, MASE)
4. Generate reproducibility bundle (library versions, config)
5. Create GitHub issue draft (optional)
6. If `include_timegpt=true`: Run TimeGPT API call and compare

### Output
- **Metrics CSV**: `nixtla_baseline_m4_[timestamp].csv`
- **Summary Markdown**: Human-readable interpretation
- **Repro Bundle**: `repro_bundle_[timestamp].txt`
- **GitHub Issue Draft**: Pre-filled template with results

---

## Integrations

| System | Type | Direction | Purpose | Auth Method |
|--------|------|-----------|---------|-------------|
| statsforecast | Python Library | Inbound | Baseline forecasting | None (local) |
| datasetsforecast | Python Library | Inbound | M4 benchmark data | None (local) |
| nixtla SDK | API (optional) | Outbound | TimeGPT comparison | API Key (env var) |
| Claude Code MCP | Framework | Bidirectional | Tool invocation | Built-in |

---

## Technical Constraints

- **Python Version**: 3.10+ required (statsforecast dependency)
- **Memory**: ~500MB for M4 Daily Small dataset
- **Disk**: ~100MB for cached datasets
- **Network**: Offline by default (TimeGPT opt-in requires internet)
- **Performance**: ~90 seconds for M4 Daily Small (4000 series)

---

## Security Considerations

### Authentication
**Local Execution:** No authentication required for baseline mode (statsforecast only)
**TimeGPT Mode:** API key via `NIXTLA_TIMEGPT_API_KEY` environment variable

### Authorization
No authorization checks - plugin runs locally in user's environment

### Data Handling
- **Public Datasets Only**: M4 benchmark data (no customer/proprietary data)
- **API Keys**: Never logged or committed (gitignored .env files)
- **Results**: Saved locally in user's workspace

### Secrets Management
- TimeGPT API key stored in `.env` file (gitignored)
- Setup script warns if API key missing (opt-in TimeGPT mode)

---

## Scalability

### Current Limits
| Resource | Limit | Mitigation if exceeded |
|----------|-------|----------------------|
| M4 Dataset Size | 100,000 series | Use demo presets (smaller subsets) |
| RAM Usage | ~2GB max | Batch processing (not yet implemented) |
| API Rate Limits | TimeGPT quota | Cost controls, opt-in only |

### Future Scaling
- Batch processing for large datasets
- Parallel model execution
- Caching previous results to avoid re-computation

---

## Error Handling

| Error Type | Detection | Response | Recovery |
|------------|-----------|----------|----------|
| Missing dependencies | Import check | Clear error message + setup instructions | Run `/nixtla-baseline-setup` |
| Invalid dataset | Dataset load failure | Error message with valid presets | Retry with valid preset |
| TimeGPT API failure | HTTP error | Graceful degradation (baselines only) | Continue without TimeGPT comparison |
| Out of memory | Python MemoryError | Suggest smaller dataset preset | Use m4_daily_small instead of m4_daily_full |

---

## Observability

### Logging
- **Level**: INFO by default
- **Location**: Console output (Claude Code terminal)
- **Content**: Model execution progress, metrics, errors

### Metrics
- Execution time per model
- Dataset size (series count)
- Metrics values (sMAPE, MASE)
- TimeGPT API usage (if enabled)

### Alerting
No automated alerting (local development tool)

---

## Deployment Architecture

**Deployment Type:** Local plugin (no server deployment)

**Components:**
- Python virtualenv (`.venv-nixtla-baseline/`)
- MCP server process (spawned by Claude Code)
- Dependencies installed via pip

**CI/CD:**
- GitHub Actions validate golden tasks
- Test coverage measured via pytest
- No production deployment (showcase/prototype)

---

## Related Documentation

- **Planning Doc**: [`6767-PP-PLAN-nixtla-claude-plugin-poc-baseline-lab.md`](../../6767-PP-PLAN-nixtla-claude-plugin-poc-baseline-lab.md)
- **Technical Architecture**: [`6767-OD-ARCH-nixtla-claude-plugin-poc-baseline-lab.md`](../../6767-OD-ARCH-nixtla-claude-plugin-poc-baseline-lab.md)
- **Plugin README**: [`plugins/nixtla-baseline-lab/README.md`](../../../plugins/nixtla-baseline-lab/README.md)
