# Nixtla Plugin Showcase

Claude Code plugins and AI skills for time-series forecasting with Nixtla's statsforecast and TimeGPT.

**Status:** 3 working plugins | 8 skills | Experimental

---

## Install

### Option 1: Marketplace (Recommended)

Add to `~/.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": [
    {
      "name": "nixtla-plugins",
      "url": "https://raw.githubusercontent.com/intent-solutions-io/plugins-nixtla/main/.claude-plugin/marketplace.json"
    }
  ]
}
```

Then install:

```
/plugin install nixtla-baseline-lab@nixtla-plugins
```

### Option 2: Direct from GitHub

```
/plugin install github:intent-solutions-io/plugins-nixtla/plugins/nixtla-baseline-lab
```

---

## Plugins

| Plugin | Description | Status |
|--------|-------------|--------|
| `nixtla-baseline-lab` | Run statsforecast baselines on M4 data, generate benchmark reports | Working |
| `nixtla-bigquery-forecaster` | Forecast BigQuery data with Cloud Functions | Working |
| `nixtla-search-to-slack` | Search web/GitHub for Nixtla content, post to Slack | MVP |

---

## Quick Start (Baseline Lab)

```bash
git clone https://github.com/intent-solutions-io/plugins-nixtla.git
cd plugins-nixtla/plugins/nixtla-baseline-lab

./scripts/setup_nixtla_env.sh --venv
source .venv-nixtla-baseline/bin/activate
pip install -r scripts/requirements.txt

# In Claude Code:
/nixtla-baseline-m4 demo_preset=m4_daily_small
```

Runs in ~90 seconds, fully offline, zero API costs.

---

## Prerequisites

- Python 3.10+
- Claude Code CLI
- Git

---

## Repository Structure

```
plugins/                    # Working plugins
  nixtla-baseline-lab/      # Benchmarking
  nixtla-bigquery-forecaster/
  nixtla-search-to-slack/
skills-pack/                # Claude Skills (8 skills)
packages/                   # Skills CLI installer
000-docs/                   # All documentation
```

## Documentation

All docs live in `000-docs/` using Doc-Filing v3.0 naming: `NNN-CC-ABCD-description.md`

| Guide | Audience |
|-------|----------|
| [DevOps Skills Guide](000-docs/global/003-GUIDE-devops-nixtla-skills-operations.md) | DevOps / Contributors |
| [Plugin Implementation](000-docs/6767-f-OD-GUIDE-enterprise-plugin-implementation.md) | Plugin developers |
| [Executive Summary](000-docs/global/000-EXECUTIVE-SUMMARY.md) | Stakeholders |

Category codes: `PP` Planning, `AT` Architecture, `OD` Overview, `QA` Quality, `AA` Audits

---

## Development

```bash
# Run tests (baseline lab)
cd plugins/nixtla-baseline-lab
pytest tests/

# Smoke test
python tests/run_baseline_m4_smoke.py
```

CI runs on every PR. Tests must pass before merge.

---

## Contributing

1. Fork the repo
2. Create feature branch: `git checkout -b feature/my-feature`
3. Make changes, add tests
4. Run `pytest` locally
5. Open PR against `main`

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: statsforecast` | Run `pip install -r scripts/requirements.txt` |
| Plugin not found after install | Restart Claude Code |
| Permission denied on setup script | Run `chmod +x scripts/setup_nixtla_env.sh` |

---

## Contact

**Jeremy Longshore** | jeremy@intentsolutions.io

Questions? Open an issue or email.

---

## License

MIT
