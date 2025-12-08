# NeuralForecast Lab

Deep learning models (NHITS, NBEATS, TFT) with explainability (Integrated Gradients, SHAP). This workspace is the home base for NeuralForecast engineers to design, validate, and refine deep learning forecasting workflows with interpretability.

## Structure

- **skills/** - NeuralForecast Claude Skills (deep learning trainers, explainability analyzers)
- **scripts/** - NHITS/NBEATS/TFT training, IG/SHAP computation, additivity checks, visualization
- **data/** - Training datasets, model checkpoints, explainability artifacts
- **reports/** - Explainability reports, SHAP visualizations, model performance analysis
- **docs/** - Deep learning best practices, explainability guides, model architecture docs

## Example Future Flows

1. **Train NHITS/NBEATS/TFT models** on domain-specific time series
2. **Compute Integrated Gradients** for model interpretability
3. **Generate SHAP visualizations** for stakeholder presentations
4. **Validate additivity checks** for attribution quality
5. **Prototype explainability workflows** before integrating into plugins

## Environment Setup

```bash
pip install neuralforecast utilsforecast
# Optional: shap for SHAP analysis (if not using built-in IG)
```

## Promotion Path

When a NeuralForecast workflow is stable and validated:
- **Skills**: Promote to `skills-pack/.claude/skills/nixtla-neuralforecast-*`
- **Scripts**: Integrate into `plugins/nixtla-neuralforecast-*/` (future MCP server)
- **Reports**: Archive explainability reports to `000-docs/` with AA-REPT type codes
