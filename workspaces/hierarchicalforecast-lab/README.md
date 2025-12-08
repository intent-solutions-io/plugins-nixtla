# HierarchicalForecast Lab

Hierarchical reconciliation (multi-level forecasts, coherence metrics, bottom-up/top-down strategies). This workspace is the home base for HierarchicalForecast engineers to design, validate, and refine hierarchical forecasting workflows.

## Structure

- **skills/** - HierarchicalForecast Claude Skills (reconciliation builders, coherence analyzers)
- **scripts/** - Hierarchical forecasting, reconciliation algorithms, coherence metrics, visualization
- **data/** - Multi-level hierarchical datasets, reconciliation experiment data
- **reports/** - Reconciliation results, coherence analysis, hierarchy visualizations
- **docs/** - Hierarchical forecasting documentation, reconciliation best practices

## Example Future Flows

1. **Design and run hierarchical reconciliation** on multi-level datasets
2. **Prototype reconciliation strategies** (bottom-up, top-down, MinTrace, ERM)
3. **Validate coherence metrics** for hierarchical forecasts
4. **Benchmark reconciliation algorithms** on domain-specific hierarchies
5. **Create hierarchy visualization templates** for stakeholder presentations

## Environment Setup

```bash
pip install hierarchicalforecast utilsforecast
# Hierarchical datasets can be constructed from flat data or imported
```

## Promotion Path

When a HierarchicalForecast workflow is stable and validated:
- **Skills**: Promote to `skills-pack/.claude/skills/nixtla-hierarchical-*`
- **Scripts**: Integrate into `plugins/nixtla-hierarchical-*/` (future MCP server)
- **Docs**: Extract reconciliation patterns to `000-docs/` with proper naming
