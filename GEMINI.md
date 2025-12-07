# GEMINI.md

Project context for Gemini Code Assist and Gemini CLI PR reviews.

## Project Overview

**Nixtla Claude Code Plugins** - Experimental showcase demonstrating Claude Code plugins and AI skills for time-series forecasting workflows.

**Status**: Prototype/experimental - NOT production software.

## Tech Stack

- Python 3.10+ (plugins), Python 3.8+ (skills installer)
- StatsForecast, TimeGPT (Nixtla libraries)
- MCP servers for Claude Code integration

## Code Standards

### Python
- PEP-8 style
- Type hints for public APIs
- Google-style docstrings
- Explicit error handling (fail fast)

### Security
- Never commit API keys or secrets
- Use environment variables for credentials
- Validate at system boundaries

### Nixtla Patterns
```python
# DataFrame columns: unique_id, ds, y
from statsforecast import StatsForecast
from statsforecast.models import AutoETS, AutoTheta
sf = StatsForecast(models=[AutoETS()], freq='D')
```

## Review Guidelines

- This is showcase code, not enterprise software
- Prefer simple over clever
- Avoid over-engineering
- Flag security issues as critical
- Be constructive, not pedantic
