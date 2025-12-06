# Nixtla Claude Code Plugins - Style Guide

## Project Context

This is a **business showcase repository** demonstrating Claude Code plugins and AI skills for time-series forecasting workflows. The audience is the Nixtla CEO and technical stakeholders evaluating the plugin ecosystem.

**Repository Status**: Experimental/prototype - NOT production software.

---

## Language & Stack

### Python (Primary)
- **Version**: Python 3.10+ for plugins, 3.8+ for skills installer
- **Style**: PEP 8, with preference for explicit over implicit
- **Type hints**: Required for public APIs, encouraged elsewhere
- **Docstrings**: Google style for public functions

### Markdown (Skills & Commands)
- YAML frontmatter required for skills (see skill-standard spec)
- Use fenced code blocks with language identifiers
- Keep line lengths reasonable (~100 chars) for readability

### Shell Scripts
- Use `#!/usr/bin/env bash` shebang
- Include `set -euo pipefail` for safety
- Quote all variables: `"$var"` not `$var`

---

## Code Quality Standards

### Fail Fast, Explicit Errors
```python
# Good: Explicit validation
if not api_key:
    raise ValueError("NIXTLA_API_KEY environment variable required")

# Bad: Silent failure
api_key = os.getenv("NIXTLA_API_KEY", "")
```

### Small, Focused Modules
- One MCP tool = one clear responsibility
- Prefer composition over inheritance
- Functions should do one thing well

### No Over-Engineering
- This is showcase code, not enterprise software
- Avoid unnecessary abstractions
- Don't add features "for later"
- Simple > clever

---

## Nixtla-Specific Patterns

### StatsForecast Integration
```python
from statsforecast import StatsForecast
from statsforecast.models import AutoETS, AutoTheta, SeasonalNaive

# Always specify freq explicitly
sf = StatsForecast(models=[AutoETS(), AutoTheta()], freq='D')
forecasts = sf.forecast(df=df_train, h=14)
```

### TimeGPT Integration
```python
from nixtla import NixtlaClient

# Always check for API key presence
client = NixtlaClient(api_key=os.environ.get("NIXTLA_TIMEGPT_API_KEY"))
if not client.api_key:
    raise EnvironmentError("NIXTLA_TIMEGPT_API_KEY not set")
```

### DataFrame Standards
- Use `unique_id`, `ds`, `y` column naming (Nixtla convention)
- Validate DataFrame structure before processing
- Handle missing values explicitly

---

## Testing Requirements

### Every Plugin Needs
1. A smoke test that runs offline (no API calls)
2. Golden task test with reproducible outputs
3. Clear pass/fail criteria

### Test File Locations
- `plugins/{plugin}/tests/` - Plugin-specific tests
- `tests/` - Cross-plugin and integration tests

### Example Test Pattern
```python
def test_baseline_smoke():
    """90-second offline smoke test for baseline lab."""
    result = run_baselines(dataset="m4_daily_small", models=["naive"])
    assert result["status"] == "success"
    assert "metrics" in result
```

---

## Documentation Standards

### Doc-Filing Convention
All docs in `000-docs/` follow: `NNN-CC-ABCD-description.md`
- `NNN`: Sequential number (001-999)
- `CC`: Category code (PP, AT, AA, OD, QA)
- `ABCD`: Unique 4-char identifier

### Skill Frontmatter (Required)
```yaml
name: nixtla-<short-name>
description: >
  Action-oriented description with when-to-use context
version: X.Y.Z
allowed-tools: "Read,Write,Glob,Grep,Edit"
```

**Forbidden fields**: author, priority, audience, when_to_use, license

---

## Security & Secrets

### Never Commit
- API keys or tokens
- `.env` files with real credentials
- Credentials in code comments

### Environment Variables
- `NIXTLA_TIMEGPT_API_KEY` - TimeGPT access
- Use `.env.example` with placeholder values
- Document required env vars in README

---

## Messaging Guidelines

### Use These Terms
- "experimental", "prototype", "showcase"
- "demonstrates value", "proof of concept"

### Avoid These Terms
- "production-ready", "enterprise-grade"
- "guaranteed", "fully tested"
- Marketing hyperbole

---

## Pull Request Expectations

### Before Opening PR
1. Run relevant smoke tests locally
2. Update CHANGELOG.md if user-facing changes
3. Ensure no secrets in diff

### PR Size
- Keep PRs focused and reviewable
- Prefer multiple small PRs over one large PR
- If > 500 lines changed, consider splitting

### Commit Messages
- Use conventional commits: `feat:`, `fix:`, `docs:`, `test:`
- Reference issue numbers when applicable
- Keep subject line under 72 chars
