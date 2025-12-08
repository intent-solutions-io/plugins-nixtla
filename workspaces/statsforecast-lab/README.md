# StatsForecast Lab

Classical statistical baselines (AutoETS, AutoARIMA, SeasonalNaive) for M4/M5 benchmarking and model comparisons. This workspace is the home base for StatsForecast engineers to design, validate, and refine baseline forecasting workflows.

## Structure

- **skills/** - StatsForecast Claude Skills (baseline forecasters, benchmark runners)
- **scripts/** - M4/M5 benchmark runners, model comparison utilities, evaluation harnesses
- **data/** - M4/M5 datasets, custom benchmark datasets, baseline experiment data
- **reports/** - Benchmark results, model performance comparisons, sMAPE/MASE analysis
- **docs/** - Baselines documentation, benchmark setup guides, evaluation best practices

## Example Future Flows

1. **Run M4/M5 benchmarks** with full suite of StatsForecast models
2. **Compare baselines** (AutoETS vs AutoARIMA vs SeasonalNaive) on domain-specific data
3. **Prototype new baseline models** before integrating into `nixtla-baseline-lab` plugin
4. **Validate benchmark harness** for StatsForecast CI smoke tests
5. **Generate benchmark reports** for Nixtla CEO/stakeholders

## Environment Setup

```bash
pip install statsforecast utilsforecast
# M4/M5 datasets will be auto-downloaded by scripts
```

## Promotion Path

When a StatsForecast workflow is stable and validated:
- **Skills**: Promote to `skills-pack/.claude/skills/nixtla-statsforecast-*`
- **Scripts**: Integrate into `plugins/nixtla-baseline-lab/scripts/`
- **Reports**: Archive to `000-docs/` with AA-REPT or AA-STAT type codes
