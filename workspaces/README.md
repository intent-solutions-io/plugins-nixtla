# Nixtla Workspaces & Labs

This is the top-level playground and lab layer for the Nixtla plugin showcase. Each workspace is a self-contained area for a specific Nixtla domain (TimeGPT, StatsForecast, MLForecast, NeuralForecast, HierarchicalForecast). Unlike `plugins/` and `skills-pack/` which hold shipping artifacts, `workspaces/` is where we design, prototype, and validate workflows before packaging them for production or external distribution.

## Visual Overview

```
workspaces/
├── timegpt-lab/
│   ├── skills/        # TimeGPT-specific Claude Skills (prototypes)
│   ├── scripts/       # Python scripts for TimeGPT experiments
│   ├── data/          # Sample datasets, API response caches
│   ├── reports/       # Generated markdown/HTML reports
│   └── docs/          # Internal guides, best practices
│
├── statsforecast-lab/
│   ├── skills/        # StatsForecast Claude Skills (baselines, benchmarks)
│   ├── scripts/       # M4/M5 benchmark runners, model comparisons
│   ├── data/          # Benchmark datasets (M4, M5, custom)
│   ├── reports/       # Benchmark results, model performance
│   └── docs/          # Baselines documentation
│
├── mlforecast-lab/
│   ├── skills/        # MLForecast Claude Skills (ML pipelines)
│   ├── scripts/       # Feature engineering, training, prediction
│   ├── data/          # Training data, feature stores
│   ├── reports/       # ML model evaluations, hyperparameter tuning
│   └── docs/          # ML best practices
│
├── neuralforecast-lab/
│   ├── skills/        # NeuralForecast Claude Skills (deep learning + explainability)
│   ├── scripts/       # NHITS/NBEATS training, IG/SHAP computation
│   ├── data/          # Training datasets, model checkpoints
│   ├── reports/       # Explainability reports, SHAP visualizations
│   └── docs/          # Deep learning + interpretability guides
│
└── hierarchicalforecast-lab/
    ├── skills/        # HierarchicalForecast Claude Skills (reconciliation)
    ├── scripts/       # Hierarchical forecasting, coherence metrics
    ├── data/          # Multi-level hierarchical datasets
    ├── reports/       # Reconciliation results, coherence analysis
    └── docs/          # Hierarchical forecasting documentation
```

## How workspaces relate to plugins & skills-pack

- **plugins/**: Shipping artifacts (MCP servers, cloud functions, deployable plugins). These are production-ready code that external users can install and run.
- **skills-pack/**: Shared SKILL bundle for external projects. These are stable, well-documented Claude Skills that can be installed via `nixtla-skills init`.
- **workspaces/**: Internal labs where prototypes, scripts, and SKILLs are developed and validated before packaging. This is the "research and development" layer.

**Promotion flow**:
1. Develop and test in `workspaces/<lab>/skills/` or `workspaces/<lab>/scripts/`
2. When stable, promote to:
   - `skills-pack/.claude/skills/` (for reusable SKILLs)
   - `plugins/` (for deployable MCP servers or cloud functions)
3. Update marketplace metadata and release

## Who uses workspaces

- **CEO / Leadership**: Quick mental model of all 5 Nixtla domains in one place. Visual tree shows breadth of capabilities.
- **DevOps Engineers**: Wiring CI smoke tests, environment bootstrap scripts, per-domain validation. Each lab has consistent structure for automation.
- **Nixtla Engineers**: Domain "home base" for daily work. TimeGPT engineers work in `timegpt-lab/`, StatsForecast engineers in `statsforecast-lab/`, etc.

## Getting Started

Each workspace has its own README explaining:
- Purpose and scope of that domain
- How to set up the environment (API keys, dependencies)
- Example workflows and scripts
- How to promote work from the lab to production

Start by reading the workspace README for your domain of interest.

## Standards

All workspaces follow the same structure and standards defined in `.directory-standards.md`. This ensures consistency across all 5 labs and makes it easy to onboard new engineers or add new domains in the future.
