# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the Nixtla time series forecasting integration project. The repository contains Claude Code plugins for Nixtla's forecasting ecosystem (TimeGPT, StatsForecast, MLForecast, NeuralForecast) and comprehensive documentation for integrating these tools into enterprise environments.

## High-Level Architecture

The project consists of three planned Claude Code plugins that accelerate Nixtla workflows:

1. **TimeGPT Quickstart Pipeline Builder** - Generates complete TimeGPT integration code from natural language descriptions
2. **Nixtla Bench Harness Generator** - Creates benchmark harnesses to compare all Nixtla models on user data
3. **Forecast Service Template Builder** - Scaffolds production-ready FastAPI services exposing Nixtla models via REST APIs

### Plugin System Architecture

Plugins follow a structured format with:
- **Command Parser**: Routes natural language to appropriate plugin actions
- **Agent Engine**: Orchestrates multi-step AI workflows
- **Sandboxed Execution**: Isolated environments for secure code generation
- **Integration Layer**: Connects to Nixtla APIs, cloud providers, and data sources

### Nixtla Integration Points

The system integrates with the complete Nixtla ecosystem:
- **TimeGPT API** (`api.nixtla.io/v1/`) - Zero-shot forecasting with transformer models
- **StatsForecast** - Classical statistical methods (AutoARIMA, ETS, etc.)
- **MLForecast** - Machine learning models (LightGBM, XGBoost)
- **NeuralForecast** - Deep learning architectures (NBEATS, TFT, etc.)
- **HierarchicalForecast** - Hierarchical reconciliation methods

## Commands

### Development Setup
```bash
# Set up development environment with all dependencies
./scripts/setup-dev-environment.sh

# Run tests (when plugins are implemented)
pytest

# Validate all plugins structure
./scripts/validate-all-plugins.sh
```

### Nixtla API Integration
```python
# Initialize Nixtla client
from nixtla import NixtlaClient
client = NixtlaClient(api_key='YOUR_API_KEY')

# Generate forecast with TimeGPT
forecast = client.forecast(
    df=data,
    h=24,  # forecast horizon
    freq='H',  # hourly frequency
    level=[80, 90, 95]  # confidence intervals
)

# Detect anomalies
anomalies = client.detect_anomalies(df=data, freq='D')

# Cross-validation
cv_results = client.cross_validation(df=data, h=7, n_windows=5)
```

### StatsForecast Quick Start
```python
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA, AutoETS

# Initialize with models
sf = StatsForecast(
    models=[AutoARIMA(season_length=12), AutoETS(season_length=12)],
    freq='M'
)

# Fit and predict
sf.fit(df)
forecasts = sf.predict(h=12)
```

### MLForecast Pattern
```python
from mlforecast import MLForecast
from sklearn.ensemble import RandomForestRegressor

# Create ML forecaster
mlf = MLForecast(
    models=[RandomForestRegressor()],
    freq='D',
    lags=[1, 7, 14],
    date_features=['dayofweek', 'month']
)

# Train and forecast
mlf.fit(df)
predictions = mlf.predict(h=30)
```

## Document Organization

All documentation follows the Document Filing System v3.0 in `000-docs/`:
- **Format**: `NNN-CC-ABCD-description.ext`
- **Categories**: PP (Product), AT (Architecture), DR (Documentation), etc.
- **Special**: `6767-` prefix for cross-repo canonical standards

Key documents:
- `001-PP-PROD-nixtla-integration-requirements.md` - Complete product requirements
- `002-AT-ARCH-plugin-architecture.md` - Technical plugin architecture
- `005-DR-META-document-standards.md` - Filing system standards

## Plugin Development (Future)

When plugins are implemented, they'll follow this structure:
```
plugins/[plugin-name]/
├── .claude-plugin/plugin.json    # Manifest with permissions
├── commands/                     # Slash commands
├── agents/                       # AI agents for complex workflows
├── hooks/                        # Event hooks
└── scripts/                      # Supporting Python/shell scripts
```

## Security & Permissions

Plugins require explicit permissions defined in manifests:
- **Network**: Allowed hosts for API calls
- **Filesystem**: Read/write paths
- **Environment**: Accessible environment variables
- **Sandboxing**: All execution in isolated environments

## Testing Strategy

Three levels of testing (to be implemented):
1. **Unit Tests** - Individual functions with mocked dependencies
2. **Integration Tests** - Plugin integration with Nixtla APIs
3. **End-to-End Tests** - Complete forecasting workflows

Target coverage: 80% minimum, 90% goal

## Repository Links

- **GitHub**: https://github.com/jeremylongshore/claude-code-plugins-nixtla
- **Documentation**: https://jeremylongshore.github.io/claude-code-plugins-nixtla/
- **Nixtla Docs**: https://docs.nixtla.io
- **TimeGPT Paper**: https://arxiv.org/abs/2310.03589

## Contact

- **Technical Lead**: Jeremy Longshore
- **Email**: jeremy@intentsolutions.io
- **Cell**: 251.213.1115
- **Priority Support**: Dedicated Slack channel at Intent Solutions IO