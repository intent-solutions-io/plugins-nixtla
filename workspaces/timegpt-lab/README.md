# TimeGPT Lab

Experiments with Nixtla's TimeGPT (API usage, forecasting, anomaly detection, prompts). Prototyping workflows before plugins/skills or production use. This workspace is the home base for TimeGPT engineers to design, validate, and refine TimeGPT-specific workflows.

## Structure

- **skills/** - TimeGPT-specific Claude Skills (prototypes for `nixtla-timegpt-*` family)
- **scripts/** - Python scripts for TimeGPT API experimentation (forecasting, anomaly detection, prompt engineering)
- **data/** - Sample datasets, API response caches, TimeGPT experiment data
- **reports/** - Generated markdown/HTML reports from TimeGPT experiments
- **docs/** - Internal guides, best practices, API usage patterns

## Example Future Flows

1. **Design and run TimeGPT experiments** on internal/sample time series
2. **Prototype new TimeGPT features** (e.g., anomaly detection with custom thresholds)
3. **Validate TimeGPT prompts** before packaging into skills-pack or plugins
4. **Benchmark TimeGPT** against StatsForecast baselines for specific domains
5. **Create golden datasets** for TimeGPT smoke tests and CI integration

## Environment Setup

```bash
export NIXTLA_TIMEGPT_API_KEY="your-api-key-here"
pip install nixtla utilsforecast
```

## Promotion Path

When a TimeGPT workflow is stable and validated:
- **Skills**: Promote to `skills-pack/.claude/skills/nixtla-timegpt-*`
- **Scripts**: Integrate into `plugins/nixtla-timegpt-*/` (future MCP server)
- **Docs**: Extract best practices to `000-docs/` with proper NNN-CC-ABCD naming
