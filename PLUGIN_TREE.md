# Nixtla Plugins - Complete Structure

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║         🚀 NIXTLA PLUGINS - PRODUCTION ARCHITECTURE 🚀        ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

## Plugin Directory Structure

```
005-plugins/
│
├── 📄 README.md
├── 🐍 __init__.py
│
├── 🔬 nixtla-baseline-lab/
│   │
│   ├── 📖 README.md
│   │
│   ├── 🤖 agents/
│   │   └── 📝 nixtla-baseline-analyst.md
│   │
│   ├── ⚡ commands/
│   │   ├── 📋 nixtla-baseline-m4.md
│   │   └── 📋 nixtla-baseline-setup.md
│   │
│   ├── 💾 data/
│   │   └── 📊 m4/
│   │       ├── M4-Daily.csv
│   │       ├── M4-Hourly.csv
│   │       ├── M4-Monthly.csv
│   │       └── M4-Weekly.csv
│   │
│   ├── 🔧 scripts/
│   │   ├── 🐍 nixtla_baseline_mcp.py ⭐ (MCP Server)
│   │   ├── 🐍 timegpt_client.py
│   │   ├── 📦 requirements.txt
│   │   └── 🛠️  setup_nixtla_env.sh
│   │
│   ├── 🎯 skills/
│   │   └── 📚 nixtla-baseline-review/
│   │       ├── 📄 SKILL.md
│   │       └── 📁 resources/
│   │
│   └── 🧪 tests/
│       ├── 📂 csv_test/
│       ├── 📂 custom/
│       ├── 📊 data/
│       ├── 🏆 golden_tasks/
│       ├── 📂 m4_test/
│       └── 🐍 run_baseline_m4_smoke.py ✨
│
├── 🌩️  nixtla-bigquery-forecaster/
│   │
│   ├── 📚 000-docs/
│   │   ├── 📄 001-DR-REFR-google-timeseries-insights-api.md
│   │   ├── 📄 002-DR-QREF-max-quick-start-guide.md
│   │   └── 📄 003-AT-ARCH-plugin-architecture.md
│   │
│   ├── 📖 README.md
│   ├── 📦 requirements.txt
│   │
│   ├── 🔧 scripts/
│   │   └── 🐍 test_local.py
│   │
│   └── 💻 src/
│       ├── 🐍 __init__.py
│       ├── 🐍 bigquery_connector.py 🔌
│       ├── 🐍 forecaster.py 📈
│       └── 🐍 main.py ⚡
│
└── 📢 nixtla-search-to-slack/
    │
    ├── 📖 README.md
    ├── 📘 SETUP_GUIDE.md
    ├── 📦 requirements.txt
    │
    ├── ⚙️  config/
    │   ├── 📄 sources.yaml
    │   └── 📄 topics.yaml
    │
    ├── 🎯 skills/
    │   ├── 📊 nixtla-model-benchmarker/
    │   │   ├── 📄 SKILL.md
    │   │   └── 🖼️  assets/
    │   │
    │   ├── 🔍 nixtla-research-assistant/
    │   │   └── 📄 SKILL.md
    │   │
    │   └── 🔨 timegpt-pipeline-builder/
    │       ├── 📄 SKILL.md
    │       └── 🖼️  assets/
    │
    ├── 💻 src/
    │   └── 🐍 nixtla_search_to_slack/
    │       ├── 🤖 ai_curator.py
    │       ├── 📡 content_aggregator.py
    │       ├── ⚙️  config_loader.py
    │       ├── 🎯 search_orchestrator.py
    │       └── 💬 slack_publisher.py
    │
    └── 🧪 tests/
        ├── ⚙️  conftest.py
        ├── 🧪 test_ai_curator.py
        ├── 🧪 test_config_loader.py
        ├── 🧪 test_content_aggregator.py
        ├── 🧪 test_search_orchestrator.py
        └── 🧪 test_slack_publisher.py
```

---

## 📊 Plugin Metrics & Features

### 🔬 nixtla-baseline-lab

**Purpose**: Statistical forecasting baseline comparison and benchmarking

**Key Components**:
- ⭐ **MCP Server** (`nixtla_baseline_mcp.py`) - Model Context Protocol integration
- ⚡ **Slash Commands** (2) - Quick access to M4 benchmarking
- 📊 **M4 Benchmark Data** (4 datasets) - Daily, Hourly, Monthly, Weekly
- 🏆 **Golden Task Tests** - Smoke test suite for reliability
- 🤖 **Agent Integration** - Baseline analyst agent

**Use Cases**:
- Quick baseline model comparisons
- M4 competition benchmarking
- Statistical model evaluation
- Performance analysis

---

### 🌩️ nixtla-bigquery-forecaster

**Purpose**: Cloud-scale forecasting with Google BigQuery integration

**Key Components**:
- 🔌 **BigQuery Connector** - Direct database integration
- 📈 **Forecasting Engine** - Production-ready forecasting pipeline
- 📚 **Architecture Docs** (3 files) - Complete technical documentation
- ⚡ **Production Ready** - Tested and deployable

**Use Cases**:
- Large-scale forecasting (millions of time series)
- Cloud-based forecasting pipelines
- BigQuery data integration
- Enterprise forecasting solutions

---

### 📢 nixtla-search-to-slack

**Purpose**: AI-powered content curation and Slack publishing

**Key Components**:
- 💻 **5 Core Modules** - Complete Python package
  - 🤖 AI Curator - Intelligent content filtering
  - 📡 Content Aggregator - Multi-source data collection
  - ⚙️  Config Loader - YAML-based configuration
  - 🎯 Search Orchestrator - Workflow management
  - 💬 Slack Publisher - Team notifications
- 🎯 **3 Embedded Skills** - Specialized capabilities
- 🧪 **6 Test Files** - Comprehensive test coverage
- ⚙️  **YAML Config** - Easy configuration management

**Use Cases**:
- Automated research aggregation
- Team knowledge sharing
- Content curation pipelines
- Slack notification systems

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     NIXTLA PLUGIN SYSTEM                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────┐  │
│  │  Baseline Lab    │  │  BigQuery        │  │  Search  │  │
│  │  (Benchmarking)  │  │  (Cloud Scale)   │  │  (Slack) │  │
│  └────────┬─────────┘  └────────┬─────────┘  └────┬─────┘  │
│           │                     │                  │         │
│           └─────────────────────┴──────────────────┘         │
│                             │                                │
│                    ┌────────▼────────┐                       │
│                    │  MCP Protocol   │                       │
│                    │  Integration    │                       │
│                    └─────────────────┘                       │
│                             │                                │
│                    ┌────────▼────────┐                       │
│                    │  Claude Code    │                       │
│                    │  CLI Interface  │                       │
│                    └─────────────────┘                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📈 Development Status

| Plugin | Status | Test Coverage | Documentation | Production Ready |
|--------|--------|---------------|---------------|------------------|
| 🔬 Baseline Lab | ✅ Active | 🏆 Golden Tasks | 📖 Complete | ✅ Yes |
| 🌩️ BigQuery Forecaster | ✅ Active | 🧪 Unit Tests | 📚 Detailed | ✅ Yes |
| 📢 Search-to-Slack | ✅ Active | 🧪 6 Test Files | 📘 Setup Guide | ✅ Yes |

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/intent-solutions-io/plugins-nixtla.git
cd plugins-nixtla

# Install baseline lab
cd 005-plugins/nixtla-baseline-lab
./scripts/setup_nixtla_env.sh --venv
source .venv-nixtla-baseline/bin/activate
pip install -r scripts/requirements.txt

# Run smoke test
python tests/run_baseline_m4_smoke.py
```

### Usage

```bash
# Baseline Lab - M4 Benchmarking
/nixtla-baseline-m4 demo_preset=m4_daily_small

# BigQuery Forecaster
python 005-plugins/nixtla-bigquery-forecaster/scripts/test_local.py

# Search-to-Slack
cd 005-plugins/nixtla-search-to-slack
pytest tests/
```

---

## 🔒 Security & Quality

**Security Compliance**:
- ✅ OWASP Top 10 2021 compliance
- ✅ Path traversal protection
- ✅ API key validation
- ✅ Code injection prevention

**Quality Metrics**:
- ✅ All plugins pass CI/CD tests
- ✅ Comprehensive test coverage
- ✅ Production-ready error handling
- ✅ Complete documentation

---

## 📝 Version History

**Current Version**: v1.7.0

**Recent Updates**:
- v1.7.0 (2025-12-09): Production skills implementation + security hardening
- v1.6.0 (2025-12-08): README fixes and documentation updates
- v1.5.0: Initial plugin system release

---

## 🤝 Contributing

See individual plugin READMEs for contribution guidelines:
- [Baseline Lab README](005-plugins/nixtla-baseline-lab/README.md)
- [BigQuery Forecaster README](005-plugins/nixtla-bigquery-forecaster/README.md)
- [Search-to-Slack README](005-plugins/nixtla-search-to-slack/README.md)

---

## 📚 Additional Resources

- **Main Repository**: [plugins-nixtla](https://github.com/intent-solutions-io/plugins-nixtla)
- **Skills Documentation**: [003-skills/.claude/skills/](003-skills/.claude/skills/)
- **Plugin Documentation**: [000-docs/002a-planned-plugins/](000-docs/002a-planned-plugins/)

---

<p align="center">
  <b>Built with ❤️ for the Nixtla CEO showcase</b><br>
  Demonstrating Claude Code plugins for time-series forecasting workflows
</p>

---

**Last Updated**: 2025-12-09
**Repository**: https://github.com/intent-solutions-io/plugins-nixtla
