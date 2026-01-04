# Nixtla Plugin Showcase

Claude Code plugins and AI skills for time-series forecasting with Nixtla's statsforecast and TimeGPT.

**Version**: 1.7.0 | **Status**: Experimental | **Plugins**: 3 | **Skills**: 8

---

## TL;DR (30 Seconds)

| Question | Answer |
|----------|--------|
| **What** | Claude Code plugins + AI skills for time-series forecasting |
| **Who** | Business showcase for Nixtla CEO |
| **Status** | Experimental (not production) |
| **Stack** | Python 3.10+, statsforecast, TimeGPT API |
| **Entry Point** | `005-plugins/nixtla-baseline-lab/` |

---

## Health Check (Run First)

```bash
# 1. Python version OK?
python3 --version  # Need 3.10+

# 2. Clone and install
git clone https://github.com/intent-solutions-io/plugins-nixtla.git
cd plugins-nixtla
pip install -e . && pip install -r requirements-dev.txt

# 3. Tests pass?
pytest -v --tb=short

# 4. Baseline lab smoke test (90 sec, offline, no API key needed)
cd 005-plugins/nixtla-baseline-lab
./scripts/setup_nixtla_env.sh --venv
source .venv-nixtla-baseline/bin/activate
python tests/run_baseline_m4_smoke.py
```

All pass? You're ready. Something failed? See [Troubleshooting](#troubleshooting).

---

## Directory Map

```
nixtla/
├── 000-docs/                    # ALL documentation (Doc-Filing v3.0)
│   ├── 001a-planned-skills/     #   Generated skill specs (prediction markets)
│   ├── 004a-dev-planning-templates/  #   Development templates
│   └── archive/                 #   Historical docs
│
├── 003-skills/                  # Claude Skills (AI behavior mods)
│   └── .claude/skills/          #   8 production skills
│
├── 005-plugins/                 # WORKING PLUGINS (start here)
│   ├── nixtla-baseline-lab/     #   Main showcase - M4 benchmarks
│   ├── nixtla-bigquery-forecaster/   BigQuery integration
│   └── nixtla-search-to-slack/  #   Slack notifications
│
├── packages/                    # Installable packages
│   └── nixtla-claude-skills-installer/  # CLI: nixtla-skills
│
├── scripts/                     # Repo-level automation
├── tests/                       # Integration tests
├── .github/workflows/           # CI/CD pipelines (7 workflows)
│
├── CLAUDE.md                    # AI assistant instructions
├── README.md                    # You are here
├── CHANGELOG.md                 # Release history
└── VERSION                      # Current version: 1.7.0
```

### Entry Points by Role

| Role | Start Here |
|------|------------|
| **Developer** | [005-plugins/nixtla-baseline-lab/](005-plugins/nixtla-baseline-lab/) |
| **Plugin Author** | [000-docs/6767-f-OD-GUIDE-enterprise-plugin-implementation.md](000-docs/6767-f-OD-GUIDE-enterprise-plugin-implementation.md) |
| **Skill Author** | [000-docs/6767-m-DR-STND-claude-skills-frontmatter-schema.md](000-docs/6767-m-DR-STND-claude-skills-frontmatter-schema.md) |

---

## Environment Variables

| Variable | Required | Purpose | Where Used |
|----------|----------|---------|------------|
| `NIXTLA_TIMEGPT_API_KEY` | For TimeGPT only | Nixtla API access | TimeGPT skills/plugins |
| `PROJECT_ID` | For GCP | Google Cloud project | BigQuery forecaster |
| `LOCATION` | For GCP | GCP region (default: us-central1) | BigQuery forecaster |

**Quick Setup**:

```bash
# Minimal (baseline lab - no API key needed)
# statsforecast runs fully offline

# Full setup (TimeGPT features)
export NIXTLA_TIMEGPT_API_KEY='your-key-here'

# GCP features
export PROJECT_ID='your-gcp-project'
export LOCATION='us-central1'
```

---

## Quick Commands

### Install & Setup

```bash
# Clone
git clone https://github.com/intent-solutions-io/plugins-nixtla.git
cd plugins-nixtla

# Install (editable + dev deps)
pip install -e .
pip install -r requirements-dev.txt
```

### Run Tests

```bash
pytest -v                          # All tests
pytest 005-plugins/ -v             # Plugin tests only
pytest --cov=005-plugins -v        # With coverage
python tests/run_baseline_m4_smoke.py  # Baseline lab smoke test
```

### Lint & Format

```bash
black --check .                    # Check formatting
black .                            # Fix formatting
isort --check-only .               # Check imports
isort .                            # Fix imports
flake8 .                           # Lint check
```

### Skills Installer

```bash
pip install -e packages/nixtla-claude-skills-installer
cd /path/to/your/project
nixtla-skills init                 # Install all skills
nixtla-skills update               # Update to latest
nixtla-skills --version            # Check version
```

---

## CI/CD Reference

| Workflow | File | Trigger | Purpose |
|----------|------|---------|---------|
| **Main CI** | `ci.yml` | PR, push | Lint, format, test |
| **Baseline Lab** | `nixtla-baseline-lab-ci.yml` | PR, push | Plugin tests |
| **Skills Installer** | `skills-installer-ci.yml` | PR, push | Installer tests |
| **BigQuery Deploy** | `deploy-bigquery-forecaster.yml` | Manual | Cloud Functions |
| **Plugin Validator** | `plugin-validator.yml` | PR | Schema validation |
| **Gemini PR Review** | `gemini-pr-review.yml` | PR | AI code review |
| **Gemini Daily Audit** | `gemini-daily-audit.yml` | Schedule | Daily audit |

**Location**: `.github/workflows/`

**Required to Merge**: `ci.yml` must pass

---

## Plugins

| Plugin | Purpose | Status | API Key |
|--------|---------|--------|---------|
| `nixtla-baseline-lab` | Run statsforecast baselines on M4 data | Working | No |
| `nixtla-bigquery-forecaster` | Forecast BigQuery data via Cloud Functions | Working | Yes |
| `nixtla-search-to-slack` | Search web/GitHub, post to Slack | MVP | Yes |

### Quick Start (Baseline Lab)

```bash
cd 005-plugins/nixtla-baseline-lab
./scripts/setup_nixtla_env.sh --venv
source .venv-nixtla-baseline/bin/activate
pip install -r scripts/requirements.txt

# In Claude Code:
/nixtla-baseline-m4 demo_preset=m4_daily_small
```

Runs in ~90 seconds, fully offline, zero API costs.

---

## Documentation

| Document | Audience | Link |
|----------|----------|------|
| Plugin Implementation | Developers | [6767-f-OD-GUIDE-enterprise-plugin-implementation.md](000-docs/6767-f-OD-GUIDE-enterprise-plugin-implementation.md) |
| Skill Frontmatter Schema | Skill Authors | [6767-m-DR-STND-claude-skills-frontmatter-schema.md](000-docs/6767-m-DR-STND-claude-skills-frontmatter-schema.md) |
| Skill Authoring Guide | Skill Authors | [6767-n-DR-GUID-claude-skills-authoring-guide.md](000-docs/6767-n-DR-GUID-claude-skills-authoring-guide.md) |
| Skill Output Controls | Developers | [099-AA-GUIDE-skill-output-controls.md](000-docs/099-AA-GUIDE-skill-output-controls.md) |

**Doc-Filing System**: `NNN-CC-ABCD-description.md`
- `PP` = Planning, `AT` = Architecture, `AA` = Audits, `OD` = Overview, `DR` = Reference

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: statsforecast` | `pip install -r scripts/requirements.txt` |
| `ModuleNotFoundError` (general) | `pip install -e . && pip install -r requirements-dev.txt` |
| Tests fail with import error | `export PYTHONPATH=$PWD` |
| Permission denied on script | `chmod +x scripts/*.sh` |
| Plugin not found after install | Restart Claude Code |
| Smoke test timeout | First run downloads M4 data (~30MB) |
| `NIXTLA_TIMEGPT_API_KEY not set` | Only needed for TimeGPT features, not baseline lab |
| Python version error | Need Python 3.10+ (`python3 --version`) |

**Still stuck?** Open an issue or email jeremy@intentsolutions.io

---

## Contributing

1. Fork the repo
2. Create feature branch: `git checkout -b feature/my-feature`
3. Make changes, add tests
4. Run `pytest` and `black .` locally
5. Open PR against `main`

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## Contact

**Jeremy Longshore** | jeremy@intentsolutions.io

Questions? Open an issue or email.

---

## Prototypes & Research

### ERCOT Grid Forecasting

**Location**: [`002-workspaces/energy-grid-prototype/`](002-workspaces/energy-grid-prototype/)

48-hour electricity load forecasting for the Texas (ERCOT) grid with interactive map visualization.

| Component | Description |
|-----------|-------------|
| `ercot_grid_forecast.py` | Statsforecast + TimeGPT forecasting |
| `ercot_map_viz.py` | Interactive Texas grid map (folium) |
| `ERCOT_Grid_Forecast_Demo.ipynb` | Complete Jupyter demo |

**Results**: SeasonalNaive wins at **4.28% MAPE** on 48h holdout.

```bash
cd 002-workspaces/energy-grid-prototype
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python ercot_grid_forecast.py
```

**Research**: See [121-AA-REPT-energy-grid-forecasting-opportunity-research.md](000-docs/121-AA-REPT-energy-grid-forecasting-opportunity-research.md)

---

## License

MIT
