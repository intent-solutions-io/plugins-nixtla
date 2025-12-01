# Baseline Lab - Technical Specification

**Plugin:** nixtla-baseline-lab
**Version:** 0.8.0
**Last Updated:** 2025-11-30

---

## Technology Stack

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Language | Python | 3.10+ | Core implementation |
| Forecasting Library | statsforecast | ≥1.5.0 | Baseline models (AutoETS, AutoTheta, SeasonalNaive) |
| Dataset Library | datasetsforecast | ≥0.0.8 | M4 benchmark data |
| TimeGPT SDK (optional) | nixtla | ≥0.5.0 | Optional TimeGPT comparison |
| MCP Framework | Claude Code MCP | Latest | Tool exposure to Claude |
| Testing | pytest | ≥7.0.0 | Unit and integration tests |
| Shell Scripting | Bash | 4.0+ | Setup automation |

---

## Dependencies

### Python Dependencies
```
# scripts/requirements.txt
statsforecast>=1.5.0
datasetsforecast>=0.0.8
nixtla>=0.5.0          # Optional (TimeGPT comparison)
pandas>=1.5.0
numpy>=1.24.0
python-dotenv>=1.0.0   # API key management
```

### System Dependencies
- Python 3.10 or higher
- pip package manager
- Virtual environment support (recommended)

### External Services
| Service | Required | Purpose |
|---------|----------|---------|
| Nixtla TimeGPT API | No | Optional comparative benchmarking |

**Note:** TimeGPT API is opt-in only. Baseline mode works fully offline with no external dependencies.

---

## File Structure

```
plugins/nixtla-baseline-lab/
├── .claude-plugin/
│   └── plugin.json                 # Plugin manifest
├── commands/
│   ├── nixtla-baseline-m4.md       # Main slash command
│   └── nixtla-baseline-setup.md    # Setup automation command
├── skills/
│   └── nixtla-baseline-review/
│       └── SKILL.md                # AI skill for metric interpretation
├── scripts/
│   ├── mcp_server.py               # MCP server (benchmarking logic)
│   ├── setup_nixtla_env.sh         # Automated environment setup
│   └── requirements.txt            # Python dependencies
├── tests/
│   ├── run_baseline_m4_smoke.py    # Golden task smoke test
│   ├── test_mcp_server.py          # Unit tests
│   └── fixtures/                   # Test data
│       └── sample_m4_data.csv
└── README.md                       # Plugin documentation
```

---

## API Reference

### Command: `/nixtla-baseline-m4`

**Description:** Run statsforecast baseline benchmarks on M4 dataset

**Usage:**
```
/nixtla-baseline-m4 demo_preset=<preset_name> [include_timegpt=<true|false>]
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `demo_preset` | string | Yes | - | M4 dataset preset (m4_daily_small, m4_weekly_full, etc.) |
| `include_timegpt` | boolean | No | false | Whether to include TimeGPT comparison (requires API key) |

**Available Presets:**
- `m4_daily_small` - M4 Daily subset (~4,200 series)
- `m4_daily_full` - M4 Daily complete (~4,227 series)
- `m4_weekly_small` - M4 Weekly subset
- `m4_weekly_full` - M4 Weekly complete
- `m4_monthly_small` - M4 Monthly subset
- `m4_monthly_full` - M4 Monthly complete

**Returns:**

```json
{
  "status": "success",
  "metrics_csv": "nixtla_baseline_m4_20251130_143022.csv",
  "repro_bundle": "repro_bundle_20251130_143022.txt",
  "summary": {
    "dataset": "M4 Daily",
    "series_count": 4227,
    "models": ["SeasonalNaive", "AutoETS", "AutoTheta"],
    "runtime_seconds": 90
  }
}
```

**Example:**

```bash
/nixtla-baseline-m4 demo_preset=m4_daily_small

# Output:
Running Nixtla Baseline Lab benchmark...
📊 Dataset: M4 Daily (4,227 series)
✅ SeasonalNaive: sMAPE 15.7%, MASE 1.14
✅ AutoETS: sMAPE 12.3%, MASE 0.85
✅ AutoTheta: sMAPE 13.1%, MASE 0.92
Results saved: nixtla_baseline_m4_20251130_143022.csv
```

---

### Command: `/nixtla-baseline-setup`

**Description:** Automated Python environment setup

**Usage:**
```
/nixtla-baseline-setup
```

**What it does:**
1. Checks Python 3.10+ availability
2. Offers choice: current environment or dedicated virtualenv
3. Installs dependencies from `scripts/requirements.txt`
4. Validates installation

**Returns:** Setup status and next steps

---

### MCP Tool: `run_baselines`

**Description:** Core forecasting tool exposed to Claude via MCP server

**Parameters:**
```python
{
  "demo_preset": "m4_daily_small",
  "include_timegpt": false
}
```

**Implementation:** See `scripts/mcp_server.py` - `run_baselines()` function

---

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `NIXTLA_TIMEGPT_API_KEY` | No | None | API key for TimeGPT comparison (opt-in feature) |

### Config File

**Location:** `.env` file in plugin root (gitignored)

```bash
# .env (optional - only needed for TimeGPT)
NIXTLA_TIMEGPT_API_KEY=your_api_key_here
```

**Note:** Never commit `.env` files. Use `.env.example` as template.

---

## Testing

### Run All Tests
```bash
cd plugins/nixtla-baseline-lab
pytest tests/ -v
```

### Run Specific Test
```bash
pytest tests/test_mcp_server.py::test_run_baselines_success -v
```

### Test Coverage
```bash
pytest tests/ --cov=scripts --cov-report=html
```

**Coverage Target:** 65%+
**Current Coverage:** 67%

### Golden Task (CI Validation)
```bash
cd tests
python run_baseline_m4_smoke.py
```

This runs a minimal M4 Daily benchmark to validate end-to-end functionality.

---

## Deployment

### Local Installation

**Automated:**
```bash
git clone https://github.com/jeremylongshore/claude-code-plugins-nixtla.git
cd claude-code-plugins-nixtla/plugins/nixtla-baseline-lab
./scripts/setup_nixtla_env.sh --venv
source .venv-nixtla-baseline/bin/activate
```

**Manual:**
```bash
python -m venv .venv-nixtla-baseline
source .venv-nixtla-baseline/bin/activate
pip install -r scripts/requirements.txt
```

### Claude Code Installation

```bash
# In Claude Code:
/plugin marketplace add ./
/plugin install nixtla-baseline-lab@nixtla-dev-marketplace
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError: statsforecast` | Dependencies not installed | Run `./scripts/setup_nixtla_env.sh` |
| `Python version 3.10+ required` | Python too old | Install Python 3.10+ or use pyenv |
| `TimeGPT API key missing` | No API key set | Set `NIXTLA_TIMEGPT_API_KEY` in `.env` (opt-in feature) |
| `MemoryError` during benchmark | Dataset too large | Use smaller preset: `m4_daily_small` |
| MCP server not starting | Port conflict | Check logs, restart Claude Code |

### Debug Mode

Enable verbose logging:
```bash
export NIXTLA_DEBUG=1
/nixtla-baseline-m4 demo_preset=m4_daily_small
```

### Common Errors

**Error:** `FileNotFoundError: M4 dataset not found`
**Cause:** datasetsforecast not properly installed or dataset cache corrupted
**Fix:** Reinstall datasetsforecast: `pip install --upgrade --force-reinstall datasetsforecast`

**Error:** `TimeGPT API call failed: 401 Unauthorized`
**Cause:** Invalid or missing API key
**Fix:** Verify `NIXTLA_TIMEGPT_API_KEY` is set correctly in `.env`

---

## Performance Considerations

| Operation | Expected Time | Memory | Notes |
|-----------|--------------|--------|-------|
| M4 Daily Small (4,227 series) | ~90 seconds | ~500MB | Recommended for testing |
| M4 Daily Full (4,227 series) | ~90 seconds | ~500MB | Same as small (same dataset) |
| M4 Weekly Full (359 series) | ~15 seconds | ~100MB | Smaller dataset, faster |
| M4 Monthly Full (48,000 series) | ~8 minutes | ~1.5GB | Large dataset |
| TimeGPT API call | +30 seconds | +100MB | Per comparison |

**Optimization Tips:**
- Use virtual environment to isolate dependencies
- Cache M4 datasets (datasetsforecast handles this automatically)
- Start with small presets for testing

---

## Security Notes

- **No Customer Data:** Plugin only uses public M4 benchmark datasets
- **API Keys:** TimeGPT API key stored in gitignored `.env` file (never committed)
- **Local Execution:** All forecasting runs locally in user's environment
- **No Telemetry:** Plugin does not send usage data or metrics externally
- **Sandboxed:** MCP server runs in Claude Code's sandboxed environment

---

## CI/CD Integration

**GitHub Actions Validation:**
```yaml
# .github/workflows/validate-baseline-lab.yml
name: Validate Baseline Lab
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r plugins/nixtla-baseline-lab/scripts/requirements.txt
      - run: pytest plugins/nixtla-baseline-lab/tests/ --cov
      - run: python plugins/nixtla-baseline-lab/tests/run_baseline_m4_smoke.py
```

**Current CI Status:** ✅ Passing (GitHub Actions enabled)

---

## Maintenance

**Dependency Updates:**
```bash
pip list --outdated
pip install --upgrade statsforecast datasetsforecast nixtla
pip freeze > scripts/requirements.txt
```

**Version Compatibility:**
- statsforecast: Pin minor version (breaking changes rare but possible)
- datasetsforecast: Stable API, safe to upgrade
- nixtla SDK: Backwards compatible (TimeGPT is opt-in)

---

## Related Documentation

- **Plugin README:** [`plugins/nixtla-baseline-lab/README.md`](../../../plugins/nixtla-baseline-lab/README.md)
- **Architecture:** [`03-ARCHITECTURE.md`](03-ARCHITECTURE.md)
- **User Journey:** [`04-USER-JOURNEY.md`](04-USER-JOURNEY.md)
- **Canonical Arch:** [`6767-OD-ARCH-nixtla-claude-plugin-poc-baseline-lab.md`](../../6767-OD-ARCH-nixtla-claude-plugin-poc-baseline-lab.md)
