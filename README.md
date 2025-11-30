# Nixtla Plugin Showcase

> Claude Code plugins that make Nixtla's team 2-3x more productive and expand market reach to Airflow, dbt, and Snowflake customers

**Sponsor:** Nixtla (Max Mergenthaler)
**Prepared by:** Intent Solutions (jeremy@intentsolutions.io)
**Version:** 1.0.0 | **Last Updated:** 2025-11-30
**Status:** 1 working · 9 specified · 0 ideas

---

## Quick Navigation

| I am a... | Start here |
|-----------|------------|
| 👔 Executive / Decision Maker | [Executive Summary](000-docs/global/000-EXECUTIVE-SUMMARY.md) |
| 💰 Evaluating Investment | [Engagement Options](000-docs/global/001-ENGAGEMENT-OPTIONS.md) |
| 🔧 Technical Evaluator | [Architecture Overview](#architecture-overview) |
| 👤 Potential User | [Demo](#demo) |

---

## Portfolio Overview

| Status | Count | Description |
|--------|-------|-------------|
| ✅ Working | 1 | Ready to use now |
| 📋 Specified | 9 | Full docs, ready to build |
| 🔨 In Progress | 0 | Currently building |
| 💡 Ideas | 0 | Needs discovery |
| **Total** | **10** | |

---

## ✅ Working Plugins

| Plugin | Category | Impact | Docs |
|--------|----------|--------|------|
| [Baseline Lab](plugins/nixtla-baseline-lab/) | Efficiency | Faster customer issue debugging | [BC](000-docs/plugins/nixtla-baseline-lab/01-BUSINESS-CASE.md) · Status: [Working](000-docs/plugins/nixtla-baseline-lab/06-STATUS.md) |

---

## 📋 Specified Plugins (Ready to Build)

**Internal Efficiency** (Make Your Team Faster)

| Plugin | Impact | Status |
|--------|--------|--------|
| [Cost Optimizer](000-docs/plugins/nixtla-cost-optimizer/) | 30-50% API cost reduction | [📋 Specified](000-docs/plugins/nixtla-cost-optimizer/06-STATUS.md) |
| [Migration Assistant](000-docs/plugins/nixtla-migration-assistant/) | Onboarding: weeks → hours | [📋 Specified](000-docs/plugins/nixtla-migration-assistant/06-STATUS.md) |
| [Forecast Explainer](000-docs/plugins/nixtla-forecast-explainer/) | 40% fewer support tickets | [📋 Specified](000-docs/plugins/nixtla-forecast-explainer/06-STATUS.md) |

**Business Growth** (Expand Your Market)

| Plugin | Impact | Status |
|--------|--------|--------|
| [Nixtla vs Benchmark](000-docs/plugins/nixtla-vs-statsforecast-benchmark/) | Increase TimeGPT adoption | [📋 Specified](000-docs/plugins/nixtla-vs-statsforecast-benchmark/06-STATUS.md) |
| [ROI Calculator](000-docs/plugins/nixtla-roi-calculator/) | Shorten sales cycles 2-3 months | [📋 Specified](000-docs/plugins/nixtla-roi-calculator/06-STATUS.md) |
| [Airflow Operator](000-docs/plugins/nixtla-airflow-operator/) | Enterprise data platform teams | [📋 Specified](000-docs/plugins/nixtla-airflow-operator/06-STATUS.md) |
| [dbt Package](000-docs/plugins/nixtla-dbt-package/) | Analytics engineering market | [📋 Specified](000-docs/plugins/nixtla-dbt-package/06-STATUS.md) |
| [Snowflake Adapter](000-docs/plugins/nixtla-snowflake-adapter/) | Fortune 500 contracts | [📋 Specified](000-docs/plugins/nixtla-snowflake-adapter/06-STATUS.md) |
| [Anomaly Monitor](000-docs/plugins/nixtla-anomaly-streaming-monitor/) | Real-time monitoring market | [📋 Specified](000-docs/plugins/nixtla-anomaly-streaming-monitor/06-STATUS.md) |

**Full specifications** available in [000-docs/plugins/](000-docs/plugins/)

---

## Demo

### Try the Working Plugin Now

**Nixtla Baseline Lab** runs statsforecast benchmarks on M4 data with complete reproducibility.

```bash
# Clone the repository
git clone https://github.com/jeremylongshore/claude-code-plugins-nixtla.git
cd claude-code-plugins-nixtla/plugins/nixtla-baseline-lab

# Setup Python environment
./scripts/setup_nixtla_env.sh --venv
source .venv-nixtla-baseline/bin/activate
pip install -r scripts/requirements.txt

# In Claude Code, run:
/nixtla-baseline-m4 demo_preset=m4_daily_small
```

### What You Get

- ✅ Metrics CSV (sMAPE, MASE per model)
- ✅ Human-readable summary with interpretation
- ✅ GitHub-ready issue draft with full context
- ✅ Complete reproducibility bundle (versions, configs, data)

**Demo runs in ~90 seconds** with zero API costs (fully offline baseline mode).

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      Claude Code CLI                         │
├─────────────────────────────────────────────────────────────┤
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐   │
│  │  Baseline Lab │  │ Cost Optimizer│  │ ROI Calculator│   │
│  │   (Working)   │  │  (Specified)  │  │  (Specified)  │   │
│  └───────┬───────┘  └───────┬───────┘  └───────┬───────┘   │
│          │                  │                  │            │
│          ▼                  ▼                  ▼            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │        Nixtla Ecosystem                             │   │
│  │  statsforecast · datasetsforecast · nixtla SDK      │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Plugin Architecture:**
- **MCP Servers**: Expose forecasting operations to Claude Code
- **Slash Commands**: `/nixtla-*` commands for direct invocation
- **Agent Skills**: Auto-triggered when Claude detects forecasting discussions
- **Python Backend**: statsforecast, datasetsforecast, nixtla SDK integration

**Detailed architecture**: See [individual plugin docs](000-docs/plugins/)

---

## Documentation Index

### Per-Plugin Documentation

Every specified plugin includes standardized documentation:

| Doc | Audience | Purpose |
|-----|----------|---------|
| 01-BUSINESS-CASE.md | Executive | ROI, market opportunity, recommendation |
| 02-PRD.md | Product | Requirements, user stories, success metrics |
| 03-ARCHITECTURE.md | Tech Lead | System design, integrations, constraints |
| 04-USER-JOURNEY.md | End User | Step-by-step experience with examples |
| 05-TECHNICAL-SPEC.md | Engineer | APIs, dependencies, implementation |
| 06-STATUS.md | Everyone | Current state, blockers, next steps |

**Status**: Baseline Lab has full docs. Specified plugins have comprehensive architecture specs (051-059 series) + STATUS docs.

### Global Documentation

| Doc | Purpose |
|-----|---------|
| [000-EXECUTIVE-SUMMARY.md](000-docs/global/000-EXECUTIVE-SUMMARY.md) | 1-page overview for Max |
| [001-ENGAGEMENT-OPTIONS.md](000-docs/global/001-ENGAGEMENT-OPTIONS.md) | Pricing, timelines, decision framework |
| [002-DECISION-MATRIX.md](000-docs/global/002-DECISION-MATRIX.md) | Which plugin to build first |

---

## Engagement Options

| Option | Scope | Timeline | Risk |
|--------|-------|----------|------|
| 🧪 **Evaluate** | Use working demos for 30 days | No commitment | None |
| 🎯 **Pilot** | 1 plugin to production | 4-6 weeks | Low |
| 🚀 **Platform** | 3+ plugins | 12-16 weeks | Medium |

### Recommended Quick Wins

**For Pilot** (Choose 1):
- **Cost Optimizer** (Score: 4.6/5) - Immediate ROI, low risk
- **ROI Calculator** (Score: 4.4/5) - Easiest to build, enables sales

**For Platform** (Choose 3):
- **Bundle A**: Cost Optimizer + ROI Calculator + Airflow Operator (quick wins + market expansion)
- **Bundle B**: Cost Optimizer + Nixtla vs Benchmark + Migration Assistant (strategic differentiation)

**Details:** [Engagement Options](000-docs/global/001-ENGAGEMENT-OPTIONS.md) | [Decision Matrix](000-docs/global/002-DECISION-MATRIX.md)

---

## Quality Standards

| Metric | Target | Current (Baseline Lab) |
|--------|--------|------------------------|
| Test Coverage | 65%+ | 67% |
| Docs per Plugin | 6 (or comprehensive spec) | ✅ Complete |
| CI/CD | All plugins | ✅ Active (Baseline Lab) |
| Reproducibility | 100% | ✅ Full repro bundles |

**Baseline Lab** meets all quality standards with CI/CD validation via golden task harness.

---

## Adding Plugins

### Add an Idea

1. Add row to "Ideas & Backlog" section above (currently empty - all concepts are specified)

### Specify a Plugin

```bash
./scripts/new-plugin.sh <slug> "<Name>" <category>
# Example: ./scripts/new-plugin.sh cost-optimizer "Cost Optimizer" efficiency
```

This creates:
- `plugins/<slug>/` directory structure
- `000-docs/plugins/<slug>/` with all 6 doc templates
- Plugin README with quick start guide

### Validate Documentation

```bash
./scripts/validate-docs.sh
```

Checks for:
- Global docs exist (Executive Summary, Engagement Options)
- Each plugin has required docs
- No unfilled placeholders
- README has required sections

---

## Repository Structure

```
nixtla-plugin-showcase/
├── README.md                              # This file
├── CHANGELOG.md                           # Release history (v0.1.0 → v0.8.0)
├── VERSION                                # Current: 0.8.0
│
├── 000-docs/
│   ├── global/
│   │   ├── 000-EXECUTIVE-SUMMARY.md       # For Max
│   │   ├── 001-ENGAGEMENT-OPTIONS.md      # Pilot/Platform options
│   │   └── 002-DECISION-MATRIX.md         # Plugin prioritization
│   │
│   ├── plugins/
│   │   ├── nixtla-baseline-lab/           # Working plugin docs
│   │   ├── nixtla-cost-optimizer/         # Specified
│   │   ├── nixtla-migration-assistant/    # Specified
│   │   ├── nixtla-forecast-explainer/     # Specified
│   │   └── [6 more specified plugins]/
│   │
│   ├── archive/                           # Historical AARs, research
│   │
│   └── 6767-OD-REF-*                      # Reference standards
│
├── plugins/
│   └── nixtla-baseline-lab/               # Working plugin code (v0.8.0)
│       ├── .claude-plugin/
│       ├── commands/
│       ├── skills/
│       ├── scripts/
│       └── tests/
│
├── templates/                             # Doc templates for new plugins
│   ├── 01-BUSINESS-CASE-TEMPLATE.md
│   ├── 02-PRD-TEMPLATE.md
│   ├── 03-ARCHITECTURE-TEMPLATE.md
│   ├── 04-USER-JOURNEY-TEMPLATE.md
│   ├── 05-TECHNICAL-SPEC-TEMPLATE.md
│   └── 06-STATUS-TEMPLATE.md
│
└── scripts/
    ├── new-plugin.sh                      # Scaffold new plugin
    └── validate-docs.sh                   # Validate completeness
```

---

## Technology Stack

**Languages:** Python 3.10+
**Nixtla Libraries:** statsforecast, datasetsforecast, nixtla (TimeGPT SDK)
**Testing:** pytest with golden task harness
**CI/CD:** GitHub Actions with validation pipeline
**Documentation:** Doc-Filing v3.0 compliant markdown

---

## What Intent Solutions Brings

- **Speed**: 1 working plugin in 8 weeks (Baseline Lab)
- **Quality**: 70+ technical documents, full CI/CD, test coverage
- **Business Thinking**: Plugins designed for ROI, not just tech demos
- **Claude Code Expertise**: Deep integration with Claude ecosystem (253+ plugins in marketplace)

---

## Contact

**Jeremy Longshore** | Intent Solutions
📧 jeremy@intentsolutions.io
📞 251.213.1115
📅 [Schedule Call](https://calendly.com/intentconsulting)

**Next Steps for Max:**
1. ⏱️ **Try the demo** (5 min): `/nixtla-baseline-m4 demo_preset=m4_daily_small`
2. 📖 **Read business case** (10 min): [Executive Summary](000-docs/global/000-EXECUTIVE-SUMMARY.md)
3. 🎯 **Pick top 3 plugins** (15 min): [Decision Matrix](000-docs/global/002-DECISION-MATRIX.md)
4. 📞 **Schedule call**: Discuss priorities, timeline, ROI

---

## License & Disclaimer

**License:** MIT — You own what we build together.

**This is:**
- ✅ Experimental collaboration
- ✅ Business development prototype
- ✅ Proof of execution capability

**This is NOT:**
- ❌ Production SLA
- ❌ Official Nixtla product
- ❌ Guaranteed ROI

All plugins are prototypes demonstrating feasibility. Production deployment requires proper testing, security review, and maintenance agreements.

---

*Maintained by Intent Solutions | Sponsored by Nixtla*

**Version 1.0.0** | Built with 8 weeks of development, 70+ technical documents, and 1 working plugin to prove execution capability.
