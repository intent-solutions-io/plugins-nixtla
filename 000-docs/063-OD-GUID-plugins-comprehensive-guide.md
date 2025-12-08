# Comprehensive Plugins Guide: Nixtla Claude Code Plugins

**Document ID**: 063-OD-GUID-plugins-comprehensive-guide
**Version**: 1.0.0
**Created**: 2025-12-08
**Updated**: 2025-12-08
**Audience**: Developers, DevOps, Plugin Authors, Technical Stakeholders
**Companion Document**: 064-OD-GUID-skills-comprehensive-guide.md

---

# Table of Contents

1. [Introduction](#part-1-introduction)
2. [Plugin Architecture Overview](#part-2-plugin-architecture-overview)
3. [Plugin 1: Nixtla Baseline Lab](#part-3-plugin-1-nixtla-baseline-lab)
4. [Plugin 2: Nixtla BigQuery Forecaster](#part-4-plugin-2-nixtla-bigquery-forecaster)
5. [Plugin 3: Nixtla Search-to-Slack](#part-5-plugin-3-nixtla-search-to-slack)
6. [MCP Server Development Guide](#part-6-mcp-server-development-guide)
7. [Testing Plugins](#part-7-testing-plugins)
8. [Deployment and CI/CD](#part-8-deployment-and-cicd)
9. [Troubleshooting Guide](#part-9-troubleshooting-guide)
10. [Best Practices](#part-10-best-practices)
11. [Appendices](#part-11-appendices)

---

# Part 1: Introduction

## 1.1 What Are Claude Code Plugins?

Claude Code plugins are **complete applications** that extend Claude's capabilities by providing access to external tools, APIs, and services. Unlike skills (which modify Claude's behavior through prompts), plugins are full-stack applications with:

- **Backend code** (Python, Node.js, etc.)
- **MCP servers** (Model Context Protocol) that expose tools
- **Configuration files** (JSON, YAML)
- **Tests** (unit, integration, smoke tests)
- **Documentation** (README, architecture docs)
- **Commands** (slash commands that users invoke)

## 1.2 Why Plugins Matter

Plugins transform Claude from a text-based assistant into a **capable agent** that can:

1. **Execute real code** - Not just generate code, but run it
2. **Access external systems** - Databases, APIs, cloud services
3. **Process data** - Transform, analyze, visualize
4. **Produce artifacts** - Files, reports, charts
5. **Integrate workflows** - Connect multiple services

## 1.3 The Three Plugins in This Repository

| Plugin | Purpose | Complexity | API Key Required |
|--------|---------|------------|------------------|
| **Nixtla Baseline Lab** | Run statsforecast benchmarks on M4 data | High | No (offline) |
| **Nixtla BigQuery Forecaster** | Forecast BigQuery data via Cloud Functions | Medium | Yes (GCP) |
| **Nixtla Search-to-Slack** | Content curation and Slack posting | Medium | Yes (multiple) |

## 1.4 How to Read This Guide

This guide is organized into three main sections:

1. **Deep Dives** (Parts 3-5): Complete documentation for each plugin
2. **Development** (Parts 6-8): How to build, test, and deploy plugins
3. **Operations** (Parts 9-10): Troubleshooting and best practices

Each plugin section follows a consistent structure:

```
Plugin Section
├── Overview (purpose, status, requirements)
├── Architecture (directory structure, components)
├── Configuration (all config files explained)
├── Code Deep Dive (key files with full code)
├── Tools Reference (all MCP tools documented)
├── Commands Reference (all slash commands)
├── Usage Examples (real-world scenarios)
├── Testing (how to test the plugin)
├── Troubleshooting (common issues and solutions)
└── Extension Points (how to customize)
```

---

# Part 2: Plugin Architecture Overview

## 2.1 The Model Context Protocol (MCP)

MCP is the communication protocol between Claude Code and plugins. It allows:

- **Tool Discovery**: Claude asks "what tools do you have?"
- **Tool Invocation**: Claude calls tools with parameters
- **Result Handling**: Claude receives structured responses

### 2.1.1 MCP Message Format

```json
// Request (Claude → Plugin)
{
  "method": "tools/call",
  "params": {
    "name": "run_baselines",
    "arguments": {
      "horizon": 14,
      "series_limit": 50
    }
  }
}

// Response (Plugin → Claude)
{
  "content": [
    {
      "type": "text",
      "text": "{\"success\": true, \"files\": [\"results.csv\"]}"
    }
  ]
}
```

### 2.1.2 MCP Server Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                    PLUGIN STARTUP                                │
├─────────────────────────────────────────────────────────────────┤
│  1. Claude Code reads .mcp.json                                 │
│  2. Spawns MCP server process (python script.py)                │
│  3. Server enters stdin/stdout loop                             │
│  4. Claude sends "tools/list" to discover tools                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    TOOL INVOCATION                               │
├─────────────────────────────────────────────────────────────────┤
│  1. User asks Claude to perform action                          │
│  2. Claude determines which tool to call                        │
│  3. Claude sends "tools/call" with arguments                    │
│  4. MCP server executes tool                                    │
│  5. Server returns result as JSON                               │
│  6. Claude interprets result and responds to user               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PLUGIN SHUTDOWN                               │
├─────────────────────────────────────────────────────────────────┤
│  1. Claude Code session ends                                    │
│  2. MCP server process terminated                               │
│  3. Resources cleaned up                                        │
└─────────────────────────────────────────────────────────────────┘
```

## 2.2 Plugin Directory Structure

Every plugin follows this standard structure:

```
plugins/plugin-name/
│
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest (required)
│
├── .mcp.json                    # MCP server configuration (required for tools)
│
├── commands/                    # Slash commands (optional)
│   ├── command-one.md
│   └── command-two.md
│
├── skills/                      # Plugin-specific skills (optional)
│   └── skill-name/
│       └── SKILL.md
│
├── agents/                      # AI subagents (optional)
│   └── agent-name/
│       └── AGENT.md
│
├── scripts/                     # Backend code (required for tools)
│   ├── mcp_server.py            # MCP server implementation
│   ├── requirements.txt         # Python dependencies
│   └── helper_modules.py
│
├── tests/                       # Test suite (recommended)
│   ├── test_unit.py
│   ├── test_integration.py
│   └── run_smoke_test.py
│
├── 000-docs/                    # Plugin documentation (optional)
│   └── architecture.md
│
├── data/                        # Data files (optional)
│   └── sample_data.csv
│
├── README.md                    # Plugin documentation (required)
└── CHANGELOG.md                 # Version history (recommended)
```

## 2.3 Plugin Manifest (plugin.json)

The plugin manifest defines metadata:

```json
{
  "name": "nixtla-baseline-lab",
  "version": "1.0.0",
  "description": "Run Nixtla statsforecast baselines on M4 benchmark data",
  "author": "Intent Solutions",
  "homepage": "https://github.com/intent-solutions-io/plugins-nixtla",
  "license": "MIT",
  "engines": {
    "claude-code": ">=1.0.0"
  },
  "keywords": [
    "nixtla",
    "forecasting",
    "time-series",
    "statsforecast",
    "m4"
  ],
  "repository": {
    "type": "git",
    "url": "https://github.com/intent-solutions-io/plugins-nixtla"
  }
}
```

### 2.3.1 Manifest Fields Reference

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique plugin identifier (lowercase, hyphens) |
| `version` | Yes | Semver version string |
| `description` | Yes | One-line description |
| `author` | No | Author name or organization |
| `homepage` | No | Plugin homepage URL |
| `license` | No | SPDX license identifier |
| `engines` | No | Claude Code version compatibility |
| `keywords` | No | Search keywords |
| `repository` | No | Source code repository |

## 2.4 MCP Configuration (.mcp.json)

The MCP configuration tells Claude Code how to start the server:

```json
{
  "mcpServers": {
    "nixtla-baseline-mcp": {
      "command": "python",
      "args": ["scripts/nixtla_baseline_mcp.py"],
      "cwd": "${workspaceFolder}/plugins/nixtla-baseline-lab",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/plugins/nixtla-baseline-lab"
      },
      "timeout": 300000
    }
  }
}
```

### 2.4.1 MCP Configuration Fields

| Field | Required | Description |
|-------|----------|-------------|
| `command` | Yes | Executable to run (python, node, etc.) |
| `args` | Yes | Command arguments (script path, flags) |
| `cwd` | No | Working directory |
| `env` | No | Environment variables |
| `timeout` | No | Request timeout in milliseconds |

### 2.4.2 Variable Substitution

| Variable | Expands To |
|----------|------------|
| `${workspaceFolder}` | Root of the current workspace |
| `${env:VAR_NAME}` | Environment variable value |

---

# Part 3: Plugin 1 - Nixtla Baseline Lab

## 3.1 Overview

### 3.1.1 Purpose

The Nixtla Baseline Lab is the **flagship plugin** that demonstrates how Claude Code can execute real forecasting workflows using Nixtla's open-source libraries. It:

- Runs **statsforecast** models (SeasonalNaive, AutoETS, AutoTheta)
- Uses the **M4 Daily benchmark dataset** (standard forecasting benchmark)
- Calculates **industry-standard metrics** (sMAPE, MASE)
- Generates **reproducible results** with version tracking

### 3.1.2 Key Features

| Feature | Description |
|---------|-------------|
| **Offline Operation** | No API key required - uses open-source statsforecast |
| **M4 Benchmark** | Industry-standard forecasting competition dataset |
| **Multiple Models** | SeasonalNaive, AutoETS, AutoTheta |
| **Metric Calculation** | sMAPE, MASE with proper scaling |
| **Reproducibility** | Version tracking, run manifests, compat info |
| **Visualization** | Optional PNG forecast plots |
| **TimeGPT Comparison** | Optional API-based comparison (requires key) |

### 3.1.3 Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.10 | 3.11+ |
| RAM | 2GB | 4GB+ |
| Disk | 500MB | 1GB |
| API Key | None | NIXTLA_TIMEGPT_API_KEY (for TimeGPT) |

### 3.1.4 Status

- **Stability**: Production-ready
- **Test Coverage**: 100%
- **Documentation**: 1200+ lines
- **Last Updated**: 2025-12-08

## 3.2 Architecture

### 3.2.1 Directory Structure

```
plugins/nixtla-baseline-lab/
│
├── .claude-plugin/
│   └── plugin.json                    # Plugin manifest
│
├── .mcp.json                          # MCP server configuration
│
├── commands/
│   ├── nixtla-baseline-m4.md          # Main command: /nixtla-baseline-m4
│   └── nixtla-baseline-setup.md       # Setup command: /nixtla-baseline-setup
│
├── agents/
│   └── nixtla-baseline-analyst/
│       └── AGENT.md                   # AI analyst subagent
│
├── skills/
│   └── nixtla-baseline-review/
│       └── SKILL.md                   # Result interpretation skill
│
├── scripts/
│   ├── nixtla_baseline_mcp.py         # MCP server (1777 lines)
│   ├── timegpt_client.py              # TimeGPT API client
│   ├── setup_nixtla_env.sh            # Environment setup script
│   └── requirements.txt               # Python dependencies
│
├── tests/
│   ├── run_baseline_m4_smoke.py       # Golden task smoke test
│   ├── test_mcp_server.py             # MCP server unit tests
│   └── conftest.py                    # pytest fixtures
│
├── data/                              # Downloaded M4 data (auto-created)
│   └── M4/Daily/
│
├── 000-docs/
│   ├── 003-AT-ARCH-plugin-architecture.md
│   └── architecture-diagrams/
│
├── README.md                          # 1200 lines of documentation
└── CHANGELOG.md                       # Version history
```

### 3.2.2 Component Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         NIXTLA BASELINE LAB PLUGIN                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐      │
│  │   COMMANDS       │    │   MCP SERVER     │    │   SKILLS         │      │
│  ├──────────────────┤    ├──────────────────┤    ├──────────────────┤      │
│  │ /nixtla-baseline │───▶│ nixtla_baseline  │───▶│ nixtla-baseline  │      │
│  │ -m4              │    │ _mcp.py          │    │ -review          │      │
│  │                  │    │                  │    │                  │      │
│  │ /nixtla-baseline │    │ 4 tools:         │    │ Interprets       │      │
│  │ -setup           │    │ - run_baselines  │    │ metrics and      │      │
│  │                  │    │ - get_compat_info│    │ explains results │      │
│  │                  │    │ - gen_report     │    │                  │      │
│  │                  │    │ - gen_issue_draft│    │                  │      │
│  └──────────────────┘    └────────┬─────────┘    └──────────────────┘      │
│                                   │                                         │
│                                   ▼                                         │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                         NIXTLA LIBRARIES                              │  │
│  ├──────────────────────────────────────────────────────────────────────┤  │
│  │                                                                       │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │  │
│  │  │ statsforecast│  │datasetsforecast│  │   nixtla    │               │  │
│  │  ├──────────────┤  ├──────────────┤  ├──────────────┤               │  │
│  │  │ SeasonalNaive│  │ M4.load()    │  │ TimeGPT API │               │  │
│  │  │ AutoETS      │  │ M3.load()    │  │ (optional)  │               │  │
│  │  │ AutoTheta    │  │              │  │              │               │  │
│  │  │ AutoARIMA    │  │              │  │              │               │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘               │  │
│  │                                                                       │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2.3 Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DATA FLOW DIAGRAM                                  │
└─────────────────────────────────────────────────────────────────────────────┘

1. USER INVOKES COMMAND
   ┌─────────────────────────────────────────────────────────────────────────┐
   │  User: /nixtla-baseline-m4 demo_preset=m4_daily_small                   │
   └─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
2. CLAUDE READS COMMAND DEFINITION
   ┌─────────────────────────────────────────────────────────────────────────┐
   │  commands/nixtla-baseline-m4.md                                         │
   │  - Parameter definitions                                                │
   │  - Tool invocation instructions                                         │
   └─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
3. MCP TOOL INVOCATION
   ┌─────────────────────────────────────────────────────────────────────────┐
   │  Claude calls: run_baselines(demo_preset="m4_daily_small")              │
   │                                                                          │
   │  Resolved parameters:                                                    │
   │  - dataset_type: "m4"                                                   │
   │  - models: ["SeasonalNaive", "AutoETS", "AutoTheta"]                    │
   │  - series_limit: 5                                                      │
   │  - horizon: 7                                                           │
   └─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
4. DATA LOADING
   ┌─────────────────────────────────────────────────────────────────────────┐
   │  from datasetsforecast.m4 import M4                                     │
   │  df, *_ = M4.load(directory="data/", group="Daily")                     │
   │                                                                          │
   │  Result: DataFrame with 4,227 daily time series                         │
   │  Columns: unique_id, ds, y                                              │
   └─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
5. DATA SAMPLING
   ┌─────────────────────────────────────────────────────────────────────────┐
   │  unique_ids = df["unique_id"].unique()[:5]  # First 5 series            │
   │  df_sample = df[df["unique_id"].isin(unique_ids)]                       │
   └─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
6. TRAIN/TEST SPLIT
   ┌─────────────────────────────────────────────────────────────────────────┐
   │  For each series:                                                       │
   │    train = series[:-horizon]  # All but last 7 points                   │
   │    test = series[-horizon:]   # Last 7 points                           │
   └─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
7. MODEL FITTING AND FORECASTING
   ┌─────────────────────────────────────────────────────────────────────────┐
   │  from statsforecast import StatsForecast                                │
   │  from statsforecast.models import SeasonalNaive, AutoETS, AutoTheta     │
   │                                                                          │
   │  sf = StatsForecast(                                                    │
   │      models=[                                                           │
   │          SeasonalNaive(season_length=7),                                │
   │          AutoETS(season_length=7),                                      │
   │          AutoTheta(season_length=7)                                     │
   │      ],                                                                 │
   │      freq='D',                                                          │
   │      n_jobs=-1                                                          │
   │  )                                                                      │
   │                                                                          │
   │  forecasts = sf.forecast(df=df_train, h=7)                              │
   └─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
8. METRIC CALCULATION
   ┌─────────────────────────────────────────────────────────────────────────┐
   │  For each series and model:                                             │
   │                                                                          │
   │  sMAPE = 100 * mean(|actual - pred| / ((|actual| + |pred|) / 2))       │
   │                                                                          │
   │  MASE = MAE / MAE_naive_seasonal                                        │
   │       where MAE_naive_seasonal = mean(|y[t] - y[t-season_length]|)      │
   └─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
9. OUTPUT GENERATION
   ┌─────────────────────────────────────────────────────────────────────────┐
   │  Files written to nixtla_baseline_m4/:                                  │
   │                                                                          │
   │  results_M4_Daily_h7.csv     # Per-series metrics                       │
   │  summary_M4_Daily_h7.txt     # Human-readable summary                   │
   │  compat_info.json            # Library versions                         │
   │  run_manifest.json           # Run parameters                           │
   │  benchmark_report_*.md       # Nixtla-style report                      │
   └─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
10. SKILL ACTIVATION
   ┌─────────────────────────────────────────────────────────────────────────┐
   │  nixtla-baseline-review skill activates                                 │
   │  Claude interprets metrics and explains:                                │
   │                                                                          │
   │  "AutoETS performed best with an average sMAPE of 0.77% and             │
   │   MASE of 0.422. This means it reduced error by 58% compared            │
   │   to the seasonal naive baseline..."                                    │
   └─────────────────────────────────────────────────────────────────────────┘
```

## 3.3 Configuration Files

### 3.3.1 Plugin Manifest (plugin.json)

**Location**: `plugins/nixtla-baseline-lab/.claude-plugin/plugin.json`

```json
{
  "name": "nixtla-baseline-lab",
  "version": "1.0.0",
  "description": "Run Nixtla statsforecast baselines on M4 benchmark data. Demonstrates Claude Code executing real forecasting workflows with reproducible results.",
  "author": "Intent Solutions",
  "homepage": "https://github.com/intent-solutions-io/plugins-nixtla",
  "license": "MIT",
  "engines": {
    "claude-code": ">=1.0.0"
  },
  "keywords": [
    "nixtla",
    "forecasting",
    "time-series",
    "statsforecast",
    "m4",
    "benchmark",
    "AutoETS",
    "AutoTheta",
    "SeasonalNaive"
  ],
  "repository": {
    "type": "git",
    "url": "https://github.com/intent-solutions-io/plugins-nixtla"
  },
  "bugs": {
    "url": "https://github.com/intent-solutions-io/plugins-nixtla/issues"
  },
  "funding": {
    "type": "github",
    "url": "https://github.com/sponsors/intent-solutions-io"
  }
}
```

### 3.3.2 MCP Configuration (.mcp.json)

**Location**: `plugins/nixtla-baseline-lab/.mcp.json`

```json
{
  "mcpServers": {
    "nixtla-baseline-mcp": {
      "command": "python",
      "args": [
        "scripts/nixtla_baseline_mcp.py"
      ],
      "cwd": "${workspaceFolder}/plugins/nixtla-baseline-lab",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/plugins/nixtla-baseline-lab:${workspaceFolder}/plugins/nixtla-baseline-lab/scripts",
        "NIXTLA_BASELINE_DATA_DIR": "${workspaceFolder}/plugins/nixtla-baseline-lab/data"
      },
      "timeout": 300000
    }
  }
}
```

### 3.3.3 Python Requirements (requirements.txt)

**Location**: `plugins/nixtla-baseline-lab/scripts/requirements.txt`

```text
# Nixtla OSS Libraries
statsforecast>=1.7.0
datasetsforecast>=0.0.8

# Data Processing
pandas>=2.0.0
numpy>=1.24.0

# Visualization (optional)
matplotlib>=3.7.0

# TimeGPT API (optional)
nixtla>=0.5.0

# Utilities
tqdm>=4.65.0
```

### 3.3.4 Environment Setup Script

**Location**: `plugins/nixtla-baseline-lab/scripts/setup_nixtla_env.sh`

```bash
#!/bin/bash
#
# Nixtla Baseline Lab Environment Setup
#
# Usage:
#   ./setup_nixtla_env.sh --venv     # Create virtual environment
#   ./setup_nixtla_env.sh --global   # Install globally
#   ./setup_nixtla_env.sh --check    # Check existing installation
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$(dirname "$SCRIPT_DIR")"
VENV_NAME=".venv-nixtla-baseline"
VENV_PATH="$PLUGIN_DIR/$VENV_NAME"
REQUIREMENTS="$SCRIPT_DIR/requirements.txt"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
        MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
        MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

        if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 10 ]; then
            print_status "Python $PYTHON_VERSION found"
            return 0
        else
            print_error "Python 3.10+ required, found $PYTHON_VERSION"
            return 1
        fi
    else
        print_error "Python 3 not found"
        return 1
    fi
}

check_installation() {
    echo "Checking Nixtla installation..."
    echo ""

    # Check Python
    check_python || return 1

    # Check if venv exists
    if [ -d "$VENV_PATH" ]; then
        print_status "Virtual environment found at $VENV_PATH"
        source "$VENV_PATH/bin/activate"
    else
        print_warning "Virtual environment not found"
    fi

    # Check required packages
    echo ""
    echo "Checking packages:"

    python3 -c "import statsforecast; print(f'  statsforecast: {statsforecast.__version__}')" 2>/dev/null && \
        print_status "statsforecast installed" || print_error "statsforecast not installed"

    python3 -c "import datasetsforecast; print(f'  datasetsforecast: {datasetsforecast.__version__}')" 2>/dev/null && \
        print_status "datasetsforecast installed" || print_error "datasetsforecast not installed"

    python3 -c "import pandas; print(f'  pandas: {pandas.__version__}')" 2>/dev/null && \
        print_status "pandas installed" || print_error "pandas not installed"

    python3 -c "import numpy; print(f'  numpy: {numpy.__version__}')" 2>/dev/null && \
        print_status "numpy installed" || print_error "numpy not installed"

    # Optional packages
    echo ""
    echo "Optional packages:"

    python3 -c "import matplotlib; print(f'  matplotlib: {matplotlib.__version__}')" 2>/dev/null && \
        print_status "matplotlib installed (plotting enabled)" || print_warning "matplotlib not installed (plotting disabled)"

    python3 -c "import nixtla; print(f'  nixtla: {nixtla.__version__}')" 2>/dev/null && \
        print_status "nixtla installed (TimeGPT enabled)" || print_warning "nixtla not installed (TimeGPT disabled)"

    echo ""
}

create_venv() {
    echo "Creating virtual environment..."

    check_python || exit 1

    if [ -d "$VENV_PATH" ]; then
        print_warning "Virtual environment already exists at $VENV_PATH"
        read -p "Delete and recreate? [y/N] " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$VENV_PATH"
        else
            print_status "Using existing environment"
            source "$VENV_PATH/bin/activate"
            pip install -r "$REQUIREMENTS"
            return 0
        fi
    fi

    python3 -m venv "$VENV_PATH"
    print_status "Created virtual environment at $VENV_PATH"

    source "$VENV_PATH/bin/activate"
    print_status "Activated virtual environment"

    pip install --upgrade pip
    print_status "Upgraded pip"

    pip install -r "$REQUIREMENTS"
    print_status "Installed requirements"

    echo ""
    echo "=========================================="
    echo "Setup complete!"
    echo ""
    echo "To activate the environment:"
    echo "  source $VENV_PATH/bin/activate"
    echo ""
    echo "To run the smoke test:"
    echo "  python tests/run_baseline_m4_smoke.py"
    echo "=========================================="
}

install_global() {
    echo "Installing packages globally..."

    check_python || exit 1

    pip install -r "$REQUIREMENTS"
    print_status "Installed requirements globally"

    check_installation
}

# Main
case "$1" in
    --venv)
        create_venv
        ;;
    --global)
        install_global
        ;;
    --check)
        check_installation
        ;;
    *)
        echo "Nixtla Baseline Lab Environment Setup"
        echo ""
        echo "Usage:"
        echo "  $0 --venv     Create virtual environment and install packages"
        echo "  $0 --global   Install packages globally"
        echo "  $0 --check    Check existing installation"
        echo ""
        ;;
esac
```

## 3.4 MCP Server Deep Dive

### 3.4.1 Server Class Structure

The MCP server is implemented in `scripts/nixtla_baseline_mcp.py` (1777 lines). Here's the complete class structure:

```python
#!/usr/bin/env python3
"""
Nixtla Baseline Lab MCP Server

Exposes baseline forecasting tools via Model Context Protocol.
Uses Nixtla's open-source libraries to run classical forecasting baselines
on the M4 Daily benchmark dataset.

Author: Intent Solutions
Version: 1.1.0
"""

import csv
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List

# Configure logging to stderr (stdout is reserved for MCP)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)


class NixtlaBaselineMCP:
    """MCP server for Nixtla baseline forecasting.

    This class implements the Model Context Protocol to expose
    forecasting tools to Claude Code. It provides four tools:

    1. run_baselines - Execute statsforecast models on M4/CSV data
    2. get_nixtla_compatibility_info - Get library versions
    3. generate_benchmark_report - Create markdown report
    4. generate_github_issue_draft - Create GitHub issue template

    Attributes:
        version (str): Server version string

    Example:
        >>> server = NixtlaBaselineMCP()
        >>> result = server.run_baselines(horizon=7, series_limit=5)
        >>> print(result["success"])
        True
    """

    def __init__(self):
        """Initialize the MCP server."""
        self.version = "1.1.0"
        logger.info(f"Nixtla Baseline MCP Server v{self.version} initializing")

    # =========================================================================
    # TOOL DEFINITIONS
    # =========================================================================

    def get_tools(self) -> List[Dict[str, Any]]:
        """Return list of available tools with JSON Schema definitions.

        This method is called when Claude requests tool discovery via
        the "tools/list" MCP method.

        Returns:
            List of tool definitions, each containing:
            - name: Tool identifier
            - description: Human-readable description
            - inputSchema: JSON Schema for parameters
        """
        return [
            {
                "name": "run_baselines",
                "description": "Run baseline forecasting models (SeasonalNaive, AutoETS, AutoTheta) on M4 Daily dataset or custom CSV",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "horizon": {
                            "type": "integer",
                            "description": "Forecast horizon in days",
                            "default": 14,
                            "minimum": 1,
                            "maximum": 60,
                        },
                        "series_limit": {
                            "type": "integer",
                            "description": "Maximum number of series to process",
                            "default": 50,
                            "minimum": 1,
                            "maximum": 500,
                        },
                        "output_dir": {
                            "type": "string",
                            "description": "Directory for output files",
                            "default": "nixtla_baseline_m4",
                        },
                        "enable_plots": {
                            "type": "boolean",
                            "description": "Generate PNG forecast plots for a sample of series",
                            "default": False,
                        },
                        "dataset_type": {
                            "type": "string",
                            "description": "Dataset type: 'm4' for M4 Daily dataset or 'csv' for custom CSV file",
                            "default": "m4",
                            "enum": ["m4", "csv"],
                        },
                        "csv_path": {
                            "type": "string",
                            "description": "Path to custom CSV file (required when dataset_type='csv'). Must have columns: unique_id, ds, y",
                        },
                        "models": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": ["SeasonalNaive", "AutoETS", "AutoTheta"],
                            },
                            "description": "List of statsforecast models to run",
                            "default": ["SeasonalNaive", "AutoETS", "AutoTheta"],
                        },
                        "freq": {
                            "type": "string",
                            "description": "Frequency string for time series (D=daily, M=monthly, H=hourly)",
                            "default": "D",
                        },
                        "season_length": {
                            "type": "integer",
                            "description": "Seasonal period length (e.g., 7 for weekly pattern in daily data)",
                            "default": 7,
                            "minimum": 1,
                        },
                        "demo_preset": {
                            "type": ["string", "null"],
                            "description": "Demo preset: 'm4_daily_small' for quick demo",
                            "enum": ["m4_daily_small", None],
                            "default": None,
                        },
                        "generate_repro_bundle": {
                            "type": "boolean",
                            "description": "Write reproducibility files (compat_info.json, run_manifest.json)",
                            "default": True,
                        },
                        "include_timegpt": {
                            "type": "boolean",
                            "description": "Include TimeGPT comparison (requires NIXTLA_TIMEGPT_API_KEY)",
                            "default": False,
                        },
                        "timegpt_max_series": {
                            "type": "integer",
                            "description": "Maximum series for TimeGPT (cost control)",
                            "default": 5,
                            "minimum": 1,
                            "maximum": 20,
                        },
                    },
                    "required": [],
                },
            },
            {
                "name": "get_nixtla_compatibility_info",
                "description": "Get version information for Nixtla OSS libraries and dependencies",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
            {
                "name": "generate_benchmark_report",
                "description": "Generate a Nixtla-style benchmark report in Markdown format from metrics CSV",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "metrics_csv_path": {
                            "type": "string",
                            "description": "Path to metrics CSV file",
                        },
                        "dataset_label": {
                            "type": "string",
                            "description": "Dataset name for the report",
                            "default": "",
                        },
                        "horizon": {
                            "type": "integer",
                            "description": "Forecast horizon",
                            "default": 0,
                        },
                    },
                    "required": [],
                },
            },
            {
                "name": "generate_github_issue_draft",
                "description": "Generate a GitHub issue draft with benchmark results and reproducibility info",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "metrics_csv_path": {
                            "type": "string",
                            "description": "Path to metrics CSV file",
                        },
                        "benchmark_report_path": {
                            "type": "string",
                            "description": "Path to benchmark report Markdown file",
                        },
                        "compat_info_path": {
                            "type": "string",
                            "description": "Path to compat_info.json",
                        },
                        "run_manifest_path": {
                            "type": "string",
                            "description": "Path to run_manifest.json",
                        },
                        "issue_type": {
                            "type": "string",
                            "description": "Type of issue: 'question', 'bug', or 'benchmark'",
                            "enum": ["question", "bug", "benchmark"],
                            "default": "question",
                        },
                    },
                    "required": [],
                },
            },
        ]

    # =========================================================================
    # TOOL IMPLEMENTATIONS
    # =========================================================================

    def run_baselines(
        self,
        horizon: int = 14,
        series_limit: int = 50,
        output_dir: str = "nixtla_baseline_m4",
        enable_plots: bool = False,
        dataset_type: str = "m4",
        csv_path: str = None,
        models: List[str] = None,
        freq: str = "D",
        season_length: int = 7,
        demo_preset: str = None,
        generate_repro_bundle: bool = True,
        include_timegpt: bool = False,
        timegpt_max_series: int = 5,
        timegpt_mode: str = "comparison",
    ) -> Dict[str, Any]:
        """Execute baseline forecasting workflow.

        This is the main tool that runs statsforecast models on time series data.
        It supports both M4 benchmark data and custom CSV files.

        Args:
            horizon: Forecast horizon in days (1-60)
            series_limit: Maximum number of series to process (1-500)
            output_dir: Directory for output files
            enable_plots: Generate PNG forecast visualizations
            dataset_type: 'm4' for M4 Daily or 'csv' for custom data
            csv_path: Path to CSV file (required if dataset_type='csv')
            models: List of model names to run
            freq: Frequency string (D, M, H, W, etc.)
            season_length: Seasonal period for models
            demo_preset: 'm4_daily_small' applies quick demo settings
            generate_repro_bundle: Write reproducibility files
            include_timegpt: Run TimeGPT comparison (requires API key)
            timegpt_max_series: Limit series sent to TimeGPT
            timegpt_mode: TimeGPT mode ('comparison')

        Returns:
            Dictionary containing:
            - success: Boolean indicating success/failure
            - message: Human-readable result message
            - files: List of generated file paths
            - summary: Model performance summary
            - Additional metadata fields

        Example:
            >>> result = server.run_baselines(
            ...     demo_preset="m4_daily_small"
            ... )
            >>> result["success"]
            True
            >>> result["summary"]["AutoETS"]["avg_smape"]
            0.77
        """
        # Apply demo preset if specified
        if demo_preset == "m4_daily_small":
            logger.info("🎬 Running GitHub-style demo: M4 Daily subset")
            dataset_type = "m4"
            models = ["SeasonalNaive", "AutoETS", "AutoTheta"]
            freq = "D"
            season_length = 7
            series_limit = 5
            horizon = 7
            logger.info("Demo preset applied: 5 series, 7-day horizon")

        # Set default models
        if models is None:
            models = ["SeasonalNaive", "AutoETS", "AutoTheta"]

        # Validate models
        ALLOWED_MODELS = {"SeasonalNaive", "AutoETS", "AutoTheta"}
        invalid_models = [m for m in models if m not in ALLOWED_MODELS]
        if invalid_models:
            return {
                "success": False,
                "message": f"Invalid models: {invalid_models}. Allowed: {sorted(ALLOWED_MODELS)}",
            }

        logger.info(f"Running baselines: horizon={horizon}, series_limit={series_limit}")

        try:
            # Import Nixtla libraries
            import numpy as np
            import pandas as pd
            from datasetsforecast.m4 import M4
            from statsforecast import StatsForecast
            from statsforecast.models import AutoETS, AutoTheta, SeasonalNaive

            # Create output directory
            out_path = Path(output_dir)
            out_path.mkdir(exist_ok=True)

            # Load dataset
            if dataset_type == "csv":
                if not csv_path:
                    return {
                        "success": False,
                        "message": "csv_path required when dataset_type='csv'",
                    }
                df = pd.read_csv(csv_path)
                dataset_name = "Custom CSV"
            else:
                plugin_root = Path(__file__).parent.parent
                data_root = plugin_root / "data"
                data_root.mkdir(exist_ok=True)
                df, *_ = M4.load(directory=str(data_root), group="Daily")
                dataset_name = "M4 Daily"

            # Sample series
            unique_ids = df["unique_id"].unique()[:series_limit]
            df_sample = df[df["unique_id"].isin(unique_ids)].copy()

            # Build model instances
            MODEL_MAP = {
                "SeasonalNaive": SeasonalNaive,
                "AutoETS": AutoETS,
                "AutoTheta": AutoTheta,
            }
            model_instances = [
                MODEL_MAP[name](season_length=season_length)
                for name in models
            ]

            # Create StatsForecast instance
            sf = StatsForecast(models=model_instances, freq=freq, n_jobs=-1)

            # Split train/test
            df_train = []
            df_test = []
            for uid in unique_ids:
                series = df_sample[df_sample["unique_id"] == uid].sort_values("ds")
                if len(series) <= horizon:
                    continue
                df_train.append(series.iloc[:-horizon])
                df_test.append(series.iloc[-horizon:])

            df_train = pd.concat(df_train, ignore_index=True)
            df_test = pd.concat(df_test, ignore_index=True)

            # Fit and forecast
            forecasts_df = sf.forecast(df=df_train, h=horizon)

            # Calculate metrics
            metrics_data = []
            for uid in df_train["unique_id"].unique():
                test_values = df_test[df_test["unique_id"] == uid]["y"].values
                forecast_row = forecasts_df[forecasts_df["unique_id"] == uid]

                for model in models:
                    if model not in forecast_row.columns:
                        continue

                    pred_values = forecast_row[model].values
                    min_len = min(len(test_values), len(pred_values))
                    actual = test_values[:min_len]
                    predicted = pred_values[:min_len]

                    smape = self._calculate_smape(actual, predicted)
                    train_values = df_train[df_train["unique_id"] == uid]["y"].values
                    mase = self._calculate_mase(actual, predicted, train_values, season_length)

                    metrics_data.append({
                        "series_id": uid,
                        "model": model,
                        "sMAPE": round(smape, 2),
                        "MASE": round(mase, 3),
                    })

            # Write results
            dataset_label = "M4_Daily" if dataset_type == "m4" else "Custom"
            metrics_file = out_path / f"results_{dataset_label}_h{horizon}.csv"
            with open(metrics_file, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["series_id", "model", "sMAPE", "MASE"])
                writer.writeheader()
                writer.writerows(metrics_data)

            # Calculate summaries
            model_summaries = {}
            for model in models:
                model_metrics = [m for m in metrics_data if m["model"] == model]
                if model_metrics:
                    model_summaries[model] = {
                        "avg_smape": round(sum(m["sMAPE"] for m in model_metrics) / len(model_metrics), 2),
                        "avg_mase": round(sum(m["MASE"] for m in model_metrics) / len(model_metrics), 3),
                        "series_count": len(model_metrics),
                    }

            # Write summary
            summary_file = out_path / f"summary_{dataset_label}_h{horizon}.txt"
            with open(summary_file, "w") as f:
                f.write(f"Baseline Results Summary\n")
                f.write(f"========================\n\n")
                f.write(f"Dataset: {dataset_name}\n")
                f.write(f"Series: {len(df_train['unique_id'].unique())}\n")
                f.write(f"Horizon: {horizon} days\n\n")
                for model, stats in sorted(model_summaries.items(), key=lambda x: x[1]["avg_smape"]):
                    f.write(f"  {model:20s} - sMAPE: {stats['avg_smape']:6.2f}%  MASE: {stats['avg_mase']:.3f}\n")

            return {
                "success": True,
                "message": f"Completed on {dataset_name} ({len(unique_ids)} series, h={horizon})",
                "files": [str(metrics_file), str(summary_file)],
                "summary": model_summaries,
            }

        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
            return {"success": False, "message": str(e)}

    def _calculate_smape(self, actual, predicted) -> float:
        """Calculate Symmetric Mean Absolute Percentage Error."""
        import numpy as np
        actual = np.array(actual)
        predicted = np.array(predicted)
        denominator = (np.abs(actual) + np.abs(predicted)) / 2.0
        denominator = np.where(denominator == 0, 1e-10, denominator)
        return 100.0 * np.mean(np.abs(actual - predicted) / denominator)

    def _calculate_mase(self, actual, predicted, train_series, season_length=7) -> float:
        """Calculate Mean Absolute Scaled Error."""
        import numpy as np
        actual = np.array(actual)
        predicted = np.array(predicted)
        train_series = np.array(train_series)

        mae_forecast = np.mean(np.abs(actual - predicted))

        if len(train_series) <= season_length:
            naive_errors = np.abs(np.diff(train_series))
        else:
            naive_errors = np.abs(train_series[season_length:] - train_series[:-season_length])

        mae_naive = np.mean(naive_errors) if len(naive_errors) > 0 else 1e-10
        return mae_forecast / max(mae_naive, 1e-10)

    # ... Additional methods for other tools ...

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP request."""
        method = request.get("method")
        params = request.get("params", {})

        if method == "tools/list":
            return {"tools": self.get_tools()}
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})

            if tool_name == "run_baselines":
                result = self.run_baselines(**arguments)
            elif tool_name == "get_nixtla_compatibility_info":
                result = self.get_nixtla_compatibility_info()
            elif tool_name == "generate_benchmark_report":
                result = self.generate_benchmark_report(**arguments)
            elif tool_name == "generate_github_issue_draft":
                result = self.generate_github_issue_draft(**arguments)
            else:
                return {"error": f"Unknown tool: {tool_name}"}

            return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}

        return {"error": f"Unknown method: {method}"}

    def run(self):
        """Main server loop - reads JSON from stdin, writes to stdout."""
        logger.info("MCP server started, waiting for requests...")
        for line in sys.stdin:
            try:
                request = json.loads(line)
                response = self.handle_request(request)
                print(json.dumps(response), flush=True)
            except Exception as e:
                logger.error(f"Error: {e}", exc_info=True)
                print(json.dumps({"error": str(e)}), flush=True)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        server = NixtlaBaselineMCP()
        result = server.run_baselines(horizon=7, series_limit=5, output_dir="test_output")
        print(json.dumps(result, indent=2))
    else:
        server = NixtlaBaselineMCP()
        server.run()
```

## 3.5 Tools Reference

### 3.5.1 run_baselines

**Purpose**: Execute statsforecast models on time series data

**Full Parameter Reference**:

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `horizon` | integer | 14 | 1-60 | Forecast horizon in days |
| `series_limit` | integer | 50 | 1-500 | Maximum series to process |
| `output_dir` | string | "nixtla_baseline_m4" | - | Output directory path |
| `enable_plots` | boolean | false | - | Generate PNG visualizations |
| `dataset_type` | string | "m4" | "m4", "csv" | Data source type |
| `csv_path` | string | null | - | Path to custom CSV |
| `models` | array | ["SeasonalNaive", "AutoETS", "AutoTheta"] | - | Models to run |
| `freq` | string | "D" | D, M, H, W, Q, Y | Time series frequency |
| `season_length` | integer | 7 | 1+ | Seasonal period |
| `demo_preset` | string | null | "m4_daily_small", null | Quick demo configuration |
| `generate_repro_bundle` | boolean | true | - | Write reproducibility files |
| `include_timegpt` | boolean | false | - | Run TimeGPT comparison |
| `timegpt_max_series` | integer | 5 | 1-20 | Limit TimeGPT series |

**Response Format**:

```json
{
  "success": true,
  "message": "Completed on M4 Daily (5 series, h=7)",
  "files": [
    "nixtla_baseline_m4/results_M4_Daily_h7.csv",
    "nixtla_baseline_m4/summary_M4_Daily_h7.txt",
    "nixtla_baseline_m4/compat_info.json",
    "nixtla_baseline_m4/run_manifest.json"
  ],
  "summary": {
    "AutoETS": {
      "avg_smape": 0.77,
      "avg_mase": 0.422,
      "series_count": 5
    },
    "AutoTheta": {
      "avg_smape": 0.85,
      "avg_mase": 0.454,
      "series_count": 5
    },
    "SeasonalNaive": {
      "avg_smape": 1.49,
      "avg_mase": 0.898,
      "series_count": 5
    }
  },
  "plots_generated": 0,
  "resolved_models": ["SeasonalNaive", "AutoETS", "AutoTheta"],
  "resolved_freq": "D",
  "resolved_season_length": 7,
  "demo_preset": "m4_daily_small",
  "repro_bundle_generated": true,
  "timegpt_status": {
    "enabled": false,
    "reason": "disabled"
  }
}
```

**Example Invocations**:

```python
# Quick demo (90 seconds)
run_baselines(demo_preset="m4_daily_small")

# Full M4 benchmark
run_baselines(
    horizon=14,
    series_limit=200,
    models=["AutoETS", "AutoTheta"],
    enable_plots=True
)

# Custom CSV data
run_baselines(
    dataset_type="csv",
    csv_path="/path/to/sales.csv",
    horizon=30,
    freq="D",
    season_length=7
)

# With TimeGPT comparison
run_baselines(
    demo_preset="m4_daily_small",
    include_timegpt=True,
    timegpt_max_series=3
)
```

### 3.5.2 get_nixtla_compatibility_info

**Purpose**: Get library versions for reproducibility

**Parameters**: None

**Response Format**:

```json
{
  "success": true,
  "engine": "nixtla.statsforecast",
  "library_versions": {
    "statsforecast": "1.7.3",
    "datasetsforecast": "0.0.8",
    "pandas": "2.1.0",
    "numpy": "1.24.3"
  },
  "notes": "Versions importable by the MCP server"
}
```

### 3.5.3 generate_benchmark_report

**Purpose**: Create Nixtla-style markdown report from metrics CSV

**Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `metrics_csv_path` | string | auto-detect | Path to metrics CSV |
| `dataset_label` | string | inferred | Dataset name for report |
| `horizon` | integer | inferred | Forecast horizon |

**Response Format**:

```json
{
  "success": true,
  "report_path": "nixtla_baseline_m4/benchmark_report_M4_Daily_h7.md",
  "message": "Benchmark report generated",
  "dataset": "M4 Daily",
  "horizon": 7,
  "series_count": 5,
  "models_evaluated": 3
}
```

**Generated Report Example**:

```markdown
# Nixtla Baseline Lab – StatsForecast Benchmark Report

- **Dataset**: M4 Daily
- **Horizon**: 7
- **Series**: 5
- **StatsForecast Version**: 1.7.3
- **Generated At**: 2025-12-08T12:00:00Z

## Average Metrics by Model

| Model | sMAPE (%) | MASE | Series |
|-------|-----------|------|--------|
| AutoETS       |      0.77 | 0.422 |      5 |
| AutoTheta     |      0.85 | 0.454 |      5 |
| SeasonalNaive |      1.49 | 0.898 |      5 |

## Highlights

- **AutoETS** performed best on average sMAPE (0.77%)
- All models achieved sMAPE < 1.5%
- AutoETS, AutoTheta beat SeasonalNaive baseline (MASE < 1.0)

## Notes

- Generated by Nixtla Baseline Lab (Claude Code plugin)
- Uses Nixtla's statsforecast and datasetsforecast libraries
```

### 3.5.4 generate_github_issue_draft

**Purpose**: Create GitHub issue template with reproducibility info

**Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `metrics_csv_path` | string | auto-detect | Path to metrics CSV |
| `benchmark_report_path` | string | auto-detect | Path to benchmark report |
| `compat_info_path` | string | auto-detect | Path to compat_info.json |
| `run_manifest_path` | string | auto-detect | Path to run_manifest.json |
| `issue_type` | string | "question" | "question", "bug", "benchmark" |

**Response Format**:

```json
{
  "success": true,
  "issue_path": "nixtla_baseline_m4/github_issue_draft.md",
  "message": "GitHub issue draft generated",
  "issue_type": "benchmark",
  "includes_benchmark": true,
  "includes_repro_info": true
}
```

## 3.6 Commands Reference

### 3.6.1 /nixtla-baseline-m4

**Location**: `plugins/nixtla-baseline-lab/commands/nixtla-baseline-m4.md`

**Purpose**: Run statsforecast baselines on M4 Daily data

**Usage**:

```
/nixtla-baseline-m4 [parameters]
```

**Parameters**:

| Parameter | Description | Example |
|-----------|-------------|---------|
| `demo_preset` | Quick demo mode | `demo_preset=m4_daily_small` |
| `horizon` | Forecast horizon | `horizon=14` |
| `series_limit` | Max series | `series_limit=100` |
| `models` | Models to run | `models=AutoETS,AutoTheta` |
| `enable_plots` | Generate plots | `enable_plots=true` |

**Examples**:

```
# Quick demo (recommended for first run)
/nixtla-baseline-m4 demo_preset=m4_daily_small

# Custom configuration
/nixtla-baseline-m4 horizon=14 series_limit=100 enable_plots=true

# Single model
/nixtla-baseline-m4 models=AutoETS horizon=30
```

**Command Definition**:

```markdown
---
name: nixtla-baseline-m4
description: |
  Run Nixtla statsforecast baseline models on M4 Daily benchmark data.
  Use demo_preset=m4_daily_small for a quick ~90 second demo.
---

# Nixtla Baseline M4 Benchmark

## Instructions

Call the `run_baselines` MCP tool with the following parameters:

### Quick Demo
```json
{
  "demo_preset": "m4_daily_small"
}
```

### Custom Run
```json
{
  "horizon": {{horizon | default: 14}},
  "series_limit": {{series_limit | default: 50}},
  "models": {{models | default: ["SeasonalNaive", "AutoETS", "AutoTheta"]}},
  "enable_plots": {{enable_plots | default: false}}
}
```

## After Execution

1. Read the summary file to understand results
2. Use nixtla-baseline-review skill to interpret metrics
3. Generate benchmark report if sharing results
```

### 3.6.2 /nixtla-baseline-setup

**Location**: `plugins/nixtla-baseline-lab/commands/nixtla-baseline-setup.md`

**Purpose**: Set up the Python environment for the baseline lab

**Usage**:

```
/nixtla-baseline-setup
```

**What It Does**:

1. Checks Python version (3.10+ required)
2. Creates virtual environment
3. Installs dependencies
4. Runs verification

## 3.7 Usage Examples

### 3.7.1 First Run: Quick Demo

```
User: /nixtla-baseline-m4 demo_preset=m4_daily_small

Claude: I'll run the Nixtla baseline demo. This will:
- Load 5 series from M4 Daily dataset
- Run SeasonalNaive, AutoETS, and AutoTheta models
- Generate metrics and summary

[Executes run_baselines tool]

Results:

| Model | Avg sMAPE | Avg MASE |
|-------|-----------|----------|
| AutoETS | 0.77% | 0.422 |
| AutoTheta | 0.85% | 0.454 |
| SeasonalNaive | 1.49% | 0.898 |

**Winner: AutoETS** achieved the lowest error on this sample.

Key observations:
- AutoETS reduced error by ~48% vs SeasonalNaive (sMAPE: 0.77% vs 1.49%)
- Both AutoETS and AutoTheta beat the naive baseline (MASE < 1.0)
- All models performed well on this subset of M4 Daily

Files generated:
- results_M4_Daily_h7.csv (per-series metrics)
- summary_M4_Daily_h7.txt (human-readable summary)
```

### 3.7.2 Custom CSV Data

```
User: I have sales data in /data/sales.csv. Can you forecast the next 30 days?

Claude: I'll analyze your sales data and run forecasts. First, let me check
the data format.

[Reads /data/sales.csv]

Your data has columns: store_id, date, revenue

I need to transform this to Nixtla format (unique_id, ds, y). Then I'll
run the baseline models.

[Executes run_baselines with:
  dataset_type="csv"
  csv_path="/data/sales.csv"
  horizon=30
  freq="D"
]

Results for your sales data:

| Model | Avg sMAPE | Avg MASE |
|-------|-----------|----------|
| AutoTheta | 3.2% | 0.67 |
| AutoETS | 3.5% | 0.71 |
| SeasonalNaive | 5.1% | 1.00 |

Recommendation: Use AutoTheta for your 30-day forecasts. It achieved:
- 3.2% average error (sMAPE)
- 33% improvement over naive baseline (MASE = 0.67)
```

### 3.7.3 Comparative Analysis with TimeGPT

```
User: How does TimeGPT compare to statistical baselines on M4?

Claude: I'll run a comparison between statsforecast models and TimeGPT.
Note: This requires your NIXTLA_TIMEGPT_API_KEY environment variable.

[Executes run_baselines with:
  demo_preset="m4_daily_small"
  include_timegpt=True
  timegpt_max_series=5
]

Comparison Results:

**Statistical Models (statsforecast)**:
| Model | Avg sMAPE | Avg MASE |
|-------|-----------|----------|
| AutoETS | 0.77% | 0.422 |
| AutoTheta | 0.85% | 0.454 |

**Foundation Model (TimeGPT)**:
| Model | Avg sMAPE | Avg MASE |
|-------|-----------|----------|
| TimeGPT | 0.82% | 0.441 |

**Winner: AutoETS** (by a small margin)

Analysis:
- On this 5-series sample, AutoETS slightly outperformed TimeGPT
- TimeGPT performed comparably to AutoTheta
- All advanced models significantly beat SeasonalNaive

Note: This is a limited comparison. TimeGPT often excels on:
- Longer horizons
- Data with complex patterns
- Zero-shot scenarios (no hyperparameter tuning)
```

## 3.8 Testing

### 3.8.1 Smoke Test

**Location**: `plugins/nixtla-baseline-lab/tests/run_baseline_m4_smoke.py`

```python
#!/usr/bin/env python3
"""
Golden Task Smoke Test for Nixtla Baseline Lab

This test verifies that the baseline lab can:
1. Load M4 Daily data
2. Run all three models
3. Generate correct output files
4. Calculate metrics within expected ranges

Usage:
    python tests/run_baseline_m4_smoke.py
"""

import json
import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from nixtla_baseline_mcp import NixtlaBaselineMCP


def run_smoke_test():
    """Execute the golden task smoke test."""
    print("=" * 60)
    print("Nixtla Baseline Lab - Golden Task Smoke Test")
    print("=" * 60)
    print()

    # Initialize server
    print("1. Initializing MCP server...")
    server = NixtlaBaselineMCP()
    print(f"   Server version: {server.version}")
    print()

    # Check compatibility
    print("2. Checking library compatibility...")
    compat = server.get_nixtla_compatibility_info()
    if not compat["success"]:
        print(f"   FAILED: {compat.get('message', 'Unknown error')}")
        return False

    versions = compat["library_versions"]
    print(f"   statsforecast: {versions.get('statsforecast', 'not installed')}")
    print(f"   datasetsforecast: {versions.get('datasetsforecast', 'not installed')}")
    print(f"   pandas: {versions.get('pandas', 'not installed')}")
    print(f"   numpy: {versions.get('numpy', 'not installed')}")
    print()

    # Run baselines
    print("3. Running baseline models (demo preset)...")
    print("   This may take 60-90 seconds on first run (data download)...")

    result = server.run_baselines(
        demo_preset="m4_daily_small",
        output_dir="nixtla_baseline_m4_smoke_test"
    )

    if not result["success"]:
        print(f"   FAILED: {result.get('message', 'Unknown error')}")
        return False

    print(f"   SUCCESS: {result['message']}")
    print()

    # Verify files
    print("4. Verifying output files...")
    for file_path in result["files"]:
        path = Path(file_path)
        if path.exists():
            size = path.stat().st_size
            print(f"   ✓ {path.name} ({size} bytes)")
        else:
            print(f"   ✗ {path.name} (MISSING)")
            return False
    print()

    # Verify metrics
    print("5. Verifying metrics...")
    summary = result["summary"]

    for model, stats in summary.items():
        smape = stats["avg_smape"]
        mase = stats["avg_mase"]

        # Sanity checks
        if smape < 0 or smape > 100:
            print(f"   ✗ {model}: sMAPE out of range ({smape})")
            return False
        if mase < 0 or mase > 10:
            print(f"   ✗ {model}: MASE out of range ({mase})")
            return False

        print(f"   ✓ {model}: sMAPE={smape:.2f}%, MASE={mase:.3f}")

    print()

    # Generate report
    print("6. Generating benchmark report...")
    report_result = server.generate_benchmark_report()

    if report_result["success"]:
        print(f"   ✓ Report: {report_result['report_path']}")
    else:
        print(f"   ✗ Report generation failed: {report_result.get('message')}")

    print()
    print("=" * 60)
    print("SMOKE TEST PASSED")
    print("=" * 60)

    return True


if __name__ == "__main__":
    success = run_smoke_test()
    sys.exit(0 if success else 1)
```

### 3.8.2 Running Tests

```bash
# Smoke test (recommended first)
cd plugins/nixtla-baseline-lab
python tests/run_baseline_m4_smoke.py

# Unit tests
pytest tests/test_mcp_server.py -v

# Integration tests
pytest tests/test_integration.py -v

# All tests with coverage
pytest tests/ --cov=scripts --cov-report=term -v
```

## 3.9 Troubleshooting

### 3.9.1 Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError: statsforecast` | Dependencies not installed | `pip install -r scripts/requirements.txt` |
| `ModuleNotFoundError: datasetsforecast` | Dependencies not installed | `pip install datasetsforecast` |
| `TypeError: M4.load()` | Old datasetsforecast version | `pip install --upgrade datasetsforecast` |
| `PermissionError: data/` | Can't create data directory | `chmod 755 data/` or run with sudo |
| Slow first run | M4 data downloading (~30MB) | Wait for download, subsequent runs are fast |
| `JSONDecodeError` in MCP | Malformed request | Check stdin/stdout handling |
| Metrics all zero | Empty test set | Increase series_limit or check data |

### 3.9.2 Debug Mode

Enable debug logging:

```bash
# Set log level
export NIXTLA_LOG_LEVEL=DEBUG

# Run with verbose output
python scripts/nixtla_baseline_mcp.py test 2>&1 | tee debug.log
```

### 3.9.3 Verify Installation

```bash
# Run the setup check
./scripts/setup_nixtla_env.sh --check

# Or manually verify
python3 -c "import statsforecast; print(f'statsforecast: {statsforecast.__version__}')"
python3 -c "import datasetsforecast; print(f'datasetsforecast: {datasetsforecast.__version__}')"
```

## 3.10 Extension Points

### 3.10.1 Adding New Models

To add a new statsforecast model:

1. **Import the model** in `nixtla_baseline_mcp.py`:

```python
from statsforecast.models import AutoARIMA  # New model
```

2. **Add to ALLOWED_MODELS**:

```python
ALLOWED_MODELS = {"SeasonalNaive", "AutoETS", "AutoTheta", "AutoARIMA"}
```

3. **Add to MODEL_MAP**:

```python
MODEL_MAP = {
    "SeasonalNaive": SeasonalNaive,
    "AutoETS": AutoETS,
    "AutoTheta": AutoTheta,
    "AutoARIMA": AutoARIMA,  # New model
}
```

4. **Update tool schema** in `get_tools()`:

```python
"enum": ["SeasonalNaive", "AutoETS", "AutoTheta", "AutoARIMA"]
```

### 3.10.2 Adding New Datasets

To add a new benchmark dataset:

1. **Add dataset loading logic**:

```python
if dataset_type == "m3":
    from datasetsforecast.m3 import M3
    df, *_ = M3.load(directory=str(data_root), group="Monthly")
    dataset_name = "M3 Monthly"
```

2. **Update dataset_type enum**:

```python
"enum": ["m4", "m3", "csv"]
```

### 3.10.3 Adding New Tools

To add a new MCP tool:

1. **Add tool definition** in `get_tools()`:

```python
{
    "name": "new_tool_name",
    "description": "What the tool does",
    "inputSchema": {
        "type": "object",
        "properties": {
            # ... parameter definitions
        }
    }
}
```

2. **Implement the tool method**:

```python
def new_tool_name(self, param1: str, param2: int = 10) -> Dict[str, Any]:
    """Implementation."""
    # ... your code
    return {"success": True, "result": "..."}
```

3. **Add to request handler**:

```python
elif tool_name == "new_tool_name":
    result = self.new_tool_name(**arguments)
```

---

# Part 4: Plugin 2 - Nixtla BigQuery Forecaster

## 4.1 Overview

### 4.1.1 Purpose

The BigQuery Forecaster demonstrates **enterprise cloud integration** by running Nixtla statsforecast models on data stored in Google BigQuery. It deploys as a Cloud Function that can be triggered via HTTP.

### 4.1.2 Key Features

| Feature | Description |
|---------|-------------|
| **BigQuery Integration** | Query data directly from BigQuery tables |
| **Serverless** | Cloud Functions auto-scale |
| **Public Datasets** | Works with BigQuery public data (Chicago Taxi, etc.) |
| **HTTP API** | RESTful interface for forecasting |
| **Batch Processing** | Handles 100K+ rows efficiently |

### 4.1.3 Requirements

| Requirement | Description |
|-------------|-------------|
| GCP Account | Google Cloud Platform account |
| BigQuery Access | Permission to query datasets |
| Cloud Functions | Permission to deploy functions |
| Service Account | With BigQuery and Cloud Functions roles |

### 4.1.4 Status

- **Stability**: Working
- **Documentation**: Complete
- **Deployment**: GitHub Actions automated

## 4.2 Architecture

### 4.2.1 Directory Structure

```
plugins/nixtla-bigquery-forecaster/
│
├── src/
│   ├── main.py                    # Cloud Function entry point
│   ├── bigquery_connector.py      # BigQuery data I/O
│   ├── forecaster.py              # Nixtla statsforecast wrapper
│   └── schema_transformer.py      # Data transformation
│
├── scripts/
│   ├── deploy.sh                  # Manual deployment script
│   ├── test_local.py              # Local testing
│   └── setup_gcp.sh               # GCP setup helper
│
├── 000-docs/
│   ├── 001-BUSINESS-CASE.md
│   ├── 002-PRD.md
│   └── 003-AT-ARCH-plugin-architecture.md
│
├── tests/
│   ├── test_bigquery_connector.py
│   ├── test_forecaster.py
│   └── test_integration.py
│
├── requirements.txt               # Python dependencies
├── README.md                      # Documentation
└── CHANGELOG.md
```

### 4.2.2 System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      BIGQUERY FORECASTER ARCHITECTURE                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐     HTTP POST      ┌─────────────────────────────────────┐
│                 │ ─────────────────▶ │                                     │
│  Client         │                    │  Google Cloud Functions             │
│  (Claude Code)  │                    │  ┌─────────────────────────────┐   │
│                 │ ◀───────────────── │  │  main.py                    │   │
│                 │     JSON Response  │  │  - forecast_handler()       │   │
└─────────────────┘                    │  │  - validate_request()       │   │
                                       │  │  - format_response()        │   │
                                       │  └──────────────┬──────────────┘   │
                                       │                 │                   │
                                       │                 ▼                   │
                                       │  ┌─────────────────────────────┐   │
                                       │  │  bigquery_connector.py      │   │
                                       │  │  - query_timeseries()       │   │
                                       │  │  - write_forecasts()        │   │
                                       │  └──────────────┬──────────────┘   │
                                       │                 │                   │
                                       └─────────────────┼───────────────────┘
                                                         │
                                                         ▼
                                       ┌─────────────────────────────────────┐
                                       │  Google BigQuery                    │
                                       │  ┌─────────────────────────────┐   │
                                       │  │  bigquery-public-data       │   │
                                       │  │  └── chicago_taxi_trips     │   │
                                       │  │      └── taxi_trips         │   │
                                       │  │          (200M+ rows)       │   │
                                       │  └─────────────────────────────┘   │
                                       │  ┌─────────────────────────────┐   │
                                       │  │  your-project               │   │
                                       │  │  └── forecasts              │   │
                                       │  │      └── output_table       │   │
                                       │  └─────────────────────────────┘   │
                                       └─────────────────────────────────────┘
```

## 4.3 Core Components

### 4.3.1 Cloud Function Entry Point (main.py)

```python
#!/usr/bin/env python3
"""
Nixtla BigQuery Forecaster - Cloud Function Entry Point

This Cloud Function:
1. Receives HTTP POST requests with forecasting parameters
2. Queries time series data from BigQuery
3. Runs statsforecast models (AutoETS, AutoTheta)
4. Returns forecasts as JSON

Environment Variables:
    PROJECT_ID: GCP project ID
    LOCATION: GCP region (default: us-central1)
"""

import json
import logging
import os
from typing import Any, Dict, List

import functions_framework
from flask import Request, Response

from bigquery_connector import BigQueryConnector
from forecaster import NixtlaForecaster
from schema_transformer import transform_to_nixtla_schema

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@functions_framework.http
def forecast_handler(request: Request) -> Response:
    """
    HTTP Cloud Function entry point for forecasting.

    Request Body (JSON):
    {
        "project_id": "bigquery-public-data",
        "dataset": "chicago_taxi_trips",
        "table": "taxi_trips",
        "timestamp_col": "trip_start_timestamp",
        "value_col": "trip_total",
        "group_by": "payment_type",  # Optional: creates multiple series
        "horizon": 7,
        "models": ["AutoETS", "AutoTheta"],  # Optional
        "freq": "D"  # Optional
    }

    Response (JSON):
    {
        "status": "success",
        "metadata": {
            "rows_read": 1000,
            "unique_series": 5,
            "forecast_points_generated": 35
        },
        "forecasts": [
            {
                "unique_id": "Cash",
                "ds": "2023-02-01",
                "AutoETS": 69918.06,
                "AutoTheta": 70123.45
            }
        ]
    }
    """
    # CORS headers
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }

    # Handle CORS preflight
    if request.method == "OPTIONS":
        return Response("", status=204, headers=headers)

    # Parse request
    try:
        request_json = request.get_json(silent=True)
        if not request_json:
            return Response(
                json.dumps({"status": "error", "message": "No JSON body provided"}),
                status=400,
                headers=headers,
                mimetype="application/json"
            )
    except Exception as e:
        return Response(
            json.dumps({"status": "error", "message": f"Invalid JSON: {str(e)}"}),
            status=400,
            headers=headers,
            mimetype="application/json"
        )

    # Validate required fields
    required_fields = ["project_id", "dataset", "table", "timestamp_col", "value_col"]
    missing_fields = [f for f in required_fields if f not in request_json]
    if missing_fields:
        return Response(
            json.dumps({
                "status": "error",
                "message": f"Missing required fields: {missing_fields}"
            }),
            status=400,
            headers=headers,
            mimetype="application/json"
        )

    # Extract parameters
    project_id = request_json["project_id"]
    dataset = request_json["dataset"]
    table = request_json["table"]
    timestamp_col = request_json["timestamp_col"]
    value_col = request_json["value_col"]
    group_by = request_json.get("group_by")
    horizon = request_json.get("horizon", 7)
    models = request_json.get("models", ["AutoETS", "AutoTheta"])
    freq = request_json.get("freq", "D")

    try:
        # Connect to BigQuery
        logger.info(f"Connecting to BigQuery: {project_id}.{dataset}.{table}")
        connector = BigQueryConnector(project_id=os.environ.get("PROJECT_ID", project_id))

        # Query data
        logger.info("Querying time series data...")
        df = connector.query_timeseries(
            source_project=project_id,
            dataset=dataset,
            table=table,
            timestamp_col=timestamp_col,
            value_col=value_col,
            group_by=group_by
        )

        logger.info(f"Retrieved {len(df)} rows")

        # Transform to Nixtla schema
        df_nixtla = transform_to_nixtla_schema(
            df=df,
            timestamp_col=timestamp_col,
            value_col=value_col,
            group_col=group_by
        )

        # Run forecaster
        logger.info(f"Running forecasts: horizon={horizon}, models={models}")
        forecaster = NixtlaForecaster(models=models, freq=freq)
        forecasts_df = forecaster.forecast(df=df_nixtla, horizon=horizon)

        # Format response
        forecasts_list = forecasts_df.to_dict(orient="records")

        response_body = {
            "status": "success",
            "metadata": {
                "rows_read": len(df),
                "unique_series": df_nixtla["unique_id"].nunique(),
                "forecast_points_generated": len(forecasts_df),
                "models_used": models,
                "horizon": horizon,
                "frequency": freq
            },
            "forecasts": forecasts_list
        }

        return Response(
            json.dumps(response_body, default=str),
            status=200,
            headers=headers,
            mimetype="application/json"
        )

    except Exception as e:
        logger.error(f"Forecasting error: {str(e)}", exc_info=True)
        return Response(
            json.dumps({
                "status": "error",
                "message": str(e)
            }),
            status=500,
            headers=headers,
            mimetype="application/json"
        )
```

### 4.3.2 BigQuery Connector

```python
#!/usr/bin/env python3
"""
BigQuery Connector for Nixtla BigQuery Forecaster

Handles all BigQuery data operations:
- Querying time series data
- Writing forecast results
- Schema validation
"""

from typing import Optional

import pandas as pd
from google.cloud import bigquery


class BigQueryConnector:
    """
    Connector for BigQuery data operations.

    Attributes:
        client: BigQuery client instance
        project_id: GCP project ID
    """

    def __init__(self, project_id: str):
        """
        Initialize BigQuery connector.

        Args:
            project_id: GCP project ID for the client
        """
        self.project_id = project_id
        self.client = bigquery.Client(project=project_id)

    def query_timeseries(
        self,
        source_project: str,
        dataset: str,
        table: str,
        timestamp_col: str,
        value_col: str,
        group_by: Optional[str] = None,
        limit: int = 100000
    ) -> pd.DataFrame:
        """
        Query time series data from BigQuery.

        Args:
            source_project: Project containing the data
            dataset: BigQuery dataset name
            table: BigQuery table name
            timestamp_col: Column containing timestamps
            value_col: Column containing values to forecast
            group_by: Optional column for grouping into multiple series
            limit: Maximum rows to return

        Returns:
            DataFrame with timestamp, value, and optional group columns

        Example:
            >>> connector = BigQueryConnector("my-project")
            >>> df = connector.query_timeseries(
            ...     source_project="bigquery-public-data",
            ...     dataset="chicago_taxi_trips",
            ...     table="taxi_trips",
            ...     timestamp_col="trip_start_timestamp",
            ...     value_col="trip_total",
            ...     group_by="payment_type"
            ... )
        """
        # Build query
        if group_by:
            query = f"""
                SELECT
                    {group_by} AS group_id,
                    DATE({timestamp_col}) AS ds,
                    SUM({value_col}) AS y
                FROM `{source_project}.{dataset}.{table}`
                WHERE {timestamp_col} IS NOT NULL
                    AND {value_col} IS NOT NULL
                    AND {group_by} IS NOT NULL
                GROUP BY {group_by}, DATE({timestamp_col})
                ORDER BY {group_by}, ds
                LIMIT {limit}
            """
        else:
            query = f"""
                SELECT
                    DATE({timestamp_col}) AS ds,
                    SUM({value_col}) AS y
                FROM `{source_project}.{dataset}.{table}`
                WHERE {timestamp_col} IS NOT NULL
                    AND {value_col} IS NOT NULL
                GROUP BY DATE({timestamp_col})
                ORDER BY ds
                LIMIT {limit}
            """

        # Execute query
        df = self.client.query(query).to_dataframe()

        return df

    def write_forecasts(
        self,
        df: pd.DataFrame,
        dataset: str,
        table: str,
        if_exists: str = "replace"
    ) -> int:
        """
        Write forecast results to BigQuery.

        Args:
            df: DataFrame containing forecasts
            dataset: Target dataset name
            table: Target table name
            if_exists: 'replace', 'append', or 'fail'

        Returns:
            Number of rows written
        """
        table_ref = f"{self.project_id}.{dataset}.{table}"

        job_config = bigquery.LoadJobConfig(
            write_disposition=(
                bigquery.WriteDisposition.WRITE_TRUNCATE
                if if_exists == "replace"
                else bigquery.WriteDisposition.WRITE_APPEND
            )
        )

        job = self.client.load_table_from_dataframe(
            df,
            table_ref,
            job_config=job_config
        )
        job.result()  # Wait for completion

        return len(df)
```

### 4.3.3 Forecaster Module

```python
#!/usr/bin/env python3
"""
Nixtla Forecaster Module

Wrapper around statsforecast for running forecasts on DataFrames.
"""

from typing import List, Optional

import pandas as pd
from statsforecast import StatsForecast
from statsforecast.models import AutoETS, AutoTheta, SeasonalNaive


class NixtlaForecaster:
    """
    Forecaster using Nixtla statsforecast library.

    Attributes:
        models: List of model names to use
        freq: Time series frequency
        season_length: Seasonal period
    """

    MODEL_MAP = {
        "SeasonalNaive": SeasonalNaive,
        "AutoETS": AutoETS,
        "AutoTheta": AutoTheta,
    }

    def __init__(
        self,
        models: List[str] = None,
        freq: str = "D",
        season_length: int = 7
    ):
        """
        Initialize forecaster.

        Args:
            models: List of model names (default: AutoETS, AutoTheta)
            freq: Frequency string (D, M, H, W)
            season_length: Seasonal period for models
        """
        self.model_names = models or ["AutoETS", "AutoTheta"]
        self.freq = freq
        self.season_length = season_length

        # Validate model names
        invalid = [m for m in self.model_names if m not in self.MODEL_MAP]
        if invalid:
            raise ValueError(f"Invalid models: {invalid}. Valid: {list(self.MODEL_MAP.keys())}")

        # Build model instances
        self.models = [
            self.MODEL_MAP[name](season_length=season_length)
            for name in self.model_names
        ]

        # Create StatsForecast instance
        self.sf = StatsForecast(
            models=self.models,
            freq=freq,
            n_jobs=-1
        )

    def forecast(
        self,
        df: pd.DataFrame,
        horizon: int = 7
    ) -> pd.DataFrame:
        """
        Generate forecasts for all series in DataFrame.

        Args:
            df: DataFrame with columns (unique_id, ds, y)
            horizon: Forecast horizon

        Returns:
            DataFrame with forecasts for each model

        Example:
            >>> forecaster = NixtlaForecaster(models=["AutoETS"])
            >>> df = pd.DataFrame({
            ...     "unique_id": ["A"] * 100,
            ...     "ds": pd.date_range("2023-01-01", periods=100),
            ...     "y": np.random.randn(100)
            ... })
            >>> forecasts = forecaster.forecast(df, horizon=7)
        """
        # Validate input
        required_cols = {"unique_id", "ds", "y"}
        missing = required_cols - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        # Run forecast
        forecasts_df = self.sf.forecast(df=df, h=horizon)

        return forecasts_df
```

## 4.4 Deployment

### 4.4.1 Manual Deployment

```bash
#!/bin/bash
# scripts/deploy.sh

# Configuration
PROJECT_ID="${PROJECT_ID:-your-project-id}"
REGION="${REGION:-us-central1}"
FUNCTION_NAME="nixtla-bigquery-forecaster"
RUNTIME="python310"
MEMORY="512MB"
TIMEOUT="300s"

# Deploy
gcloud functions deploy $FUNCTION_NAME \
    --project=$PROJECT_ID \
    --region=$REGION \
    --runtime=$RUNTIME \
    --memory=$MEMORY \
    --timeout=$TIMEOUT \
    --trigger-http \
    --allow-unauthenticated \
    --entry-point=forecast_handler \
    --source=src/ \
    --set-env-vars="PROJECT_ID=$PROJECT_ID"

# Get URL
FUNCTION_URL=$(gcloud functions describe $FUNCTION_NAME \
    --project=$PROJECT_ID \
    --region=$REGION \
    --format='value(httpsTrigger.url)')

echo "Deployed to: $FUNCTION_URL"
```

### 4.4.2 GitHub Actions Deployment

```yaml
# .github/workflows/deploy-bigquery-forecaster.yml

name: Deploy BigQuery Forecaster

on:
  push:
    branches: [main]
    paths:
      - 'plugins/nixtla-bigquery-forecaster/**'
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest

    permissions:
      contents: read
      id-token: write

    steps:
      - uses: actions/checkout@v4

      - id: auth
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
          service_account: ${{ secrets.WIF_SERVICE_ACCOUNT }}

      - uses: google-github-actions/setup-gcloud@v2

      - name: Deploy Cloud Function
        run: |
          cd plugins/nixtla-bigquery-forecaster
          gcloud functions deploy nixtla-bigquery-forecaster \
            --gen2 \
            --runtime=python310 \
            --region=us-central1 \
            --source=src/ \
            --entry-point=forecast_handler \
            --trigger-http \
            --allow-unauthenticated
```

## 4.5 Usage Examples

### 4.5.1 Basic Request

```bash
curl -X POST "https://REGION-PROJECT_ID.cloudfunctions.net/nixtla-bigquery-forecaster" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "bigquery-public-data",
    "dataset": "chicago_taxi_trips",
    "table": "taxi_trips",
    "timestamp_col": "trip_start_timestamp",
    "value_col": "trip_total",
    "group_by": "payment_type",
    "horizon": 7
  }'
```

### 4.5.2 Response

```json
{
  "status": "success",
  "metadata": {
    "rows_read": 210,
    "unique_series": 7,
    "forecast_points_generated": 49,
    "models_used": ["AutoETS", "AutoTheta"],
    "horizon": 7,
    "frequency": "D"
  },
  "forecasts": [
    {
      "unique_id": "Cash",
      "ds": "2023-02-01",
      "AutoETS": 69918.06,
      "AutoTheta": 70123.45
    },
    {
      "unique_id": "Cash",
      "ds": "2023-02-02",
      "AutoETS": 71234.56,
      "AutoTheta": 71456.78
    }
  ]
}
```

## 4.6 Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `403 Forbidden` | Missing permissions | Grant BigQuery Data Viewer role |
| `404 Table not found` | Wrong project/dataset/table | Verify table path |
| `Timeout` | Query too slow | Add WHERE clause, reduce data |
| `Memory exceeded` | Too much data | Increase memory or add LIMIT |

---

# Part 5: Plugin 3 - Nixtla Search-to-Slack

## 5.1 Overview

### 5.1.1 Purpose

Search-to-Slack is a **content curation pipeline** that:
1. Searches for Nixtla-related content (web, GitHub)
2. Aggregates and deduplicates results
3. Generates AI summaries
4. Posts formatted digests to Slack

### 5.1.2 Status

- **Stability**: MVP (Minimum Viable Product)
- **Use Case**: Learning/adaptation reference
- **Production Ready**: No (proof of concept)

## 5.2 Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      SEARCH-TO-SLACK PIPELINE                                │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   SEARCH     │───▶│  AGGREGATE   │───▶│   CURATE     │───▶│   PUBLISH    │
├──────────────┤    ├──────────────┤    ├──────────────┤    ├──────────────┤
│ SerpAPI      │    │ Deduplicate  │    │ AI Summary   │    │ Slack API    │
│ GitHub API   │    │ by URL       │    │ OpenAI/      │    │ Formatted    │
│              │    │ by Title     │    │ Claude       │    │ Digest       │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

## 5.3 Configuration

### 5.3.1 Topics Configuration

```yaml
# config/topics.yaml

topics:
  nixtla-core:
    name: "Nixtla Core Updates"
    description: "Updates about TimeGPT, StatsForecast, and MLForecast"
    keywords:
      - TimeGPT
      - StatsForecast
      - MLForecast
      - Nixtla
    sources:
      - web
      - github
    slack_channel: "#nixtla-updates"
    schedule: "0 9 * * 1-5"  # 9am weekdays

  forecasting-research:
    name: "Forecasting Research"
    description: "Academic papers and research on time series forecasting"
    keywords:
      - time series forecasting
      - neural forecasting
      - transformer forecasting
    sources:
      - web
    slack_channel: "#research"
    schedule: "0 10 * * 1"  # Mondays at 10am
```

### 5.3.2 Sources Configuration

```yaml
# config/sources.yaml

sources:
  web:
    type: serpapi
    api_key_env: SERPAPI_API_KEY
    max_results: 20
    filters:
      - site:arxiv.org
      - site:medium.com
      - site:towardsdatascience.com

  github:
    type: github
    api_key_env: GITHUB_TOKEN
    search_types:
      - repositories
      - issues
      - discussions
    max_results: 10
    filters:
      language: python
      stars: ">10"
```

## 5.4 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SERPAPI_API_KEY` | Yes | SerpAPI key for web search |
| `GITHUB_TOKEN` | No | GitHub personal access token |
| `SLACK_BOT_TOKEN` | Yes | Slack bot OAuth token |
| `OPENAI_API_KEY` | No | For AI summaries (optional) |

## 5.5 Limitations

- Basic MVP - not production-ready
- No persistence (may re-send duplicates)
- Single-threaded execution
- Limited to 2 search sources

---

# Part 6: MCP Server Development Guide

## 6.1 Creating a New MCP Server

### 6.1.1 Basic Template

```python
#!/usr/bin/env python3
"""
MCP Server Template

Replace this with your server description.
"""

import json
import logging
import sys
from typing import Any, Dict, List

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)


class MyMCPServer:
    """Your MCP server implementation."""

    def __init__(self):
        self.version = "1.0.0"

    def get_tools(self) -> List[Dict[str, Any]]:
        """Return available tools."""
        return [
            {
                "name": "my_tool",
                "description": "What my tool does",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "param1": {
                            "type": "string",
                            "description": "First parameter"
                        }
                    },
                    "required": ["param1"]
                }
            }
        ]

    def my_tool(self, param1: str) -> Dict[str, Any]:
        """Implement your tool."""
        return {"success": True, "result": f"Processed: {param1}"}

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP requests."""
        method = request.get("method")
        params = request.get("params", {})

        if method == "tools/list":
            return {"tools": self.get_tools()}
        elif method == "tools/call":
            name = params.get("name")
            args = params.get("arguments", {})

            if name == "my_tool":
                result = self.my_tool(**args)
                return {"content": [{"type": "text", "text": json.dumps(result)}]}

        return {"error": f"Unknown: {method}"}

    def run(self):
        """Main loop."""
        for line in sys.stdin:
            response = self.handle_request(json.loads(line))
            print(json.dumps(response), flush=True)


if __name__ == "__main__":
    MyMCPServer().run()
```

## 6.2 JSON Schema for Tools

### 6.2.1 Type Reference

| JSON Schema Type | Python Type | Example |
|------------------|-------------|---------|
| `string` | str | `"hello"` |
| `integer` | int | `42` |
| `number` | float | `3.14` |
| `boolean` | bool | `true` |
| `array` | list | `[1, 2, 3]` |
| `object` | dict | `{"key": "value"}` |
| `null` | None | `null` |

### 6.2.2 Validation Keywords

| Keyword | Applies To | Description |
|---------|------------|-------------|
| `minimum` | integer, number | Minimum value |
| `maximum` | integer, number | Maximum value |
| `minLength` | string | Minimum string length |
| `maxLength` | string | Maximum string length |
| `pattern` | string | Regex pattern |
| `enum` | any | Allowed values |
| `default` | any | Default value |

---

# Part 7: Testing Plugins

## 7.1 Test Types

| Type | Purpose | Location |
|------|---------|----------|
| Unit | Test individual functions | `tests/test_*.py` |
| Integration | Test component interactions | `tests/test_integration.py` |
| Smoke | Verify basic functionality | `tests/run_*_smoke.py` |
| E2E | Full workflow testing | `tests/test_e2e.py` |

## 7.2 pytest Configuration

```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

---

# Part 8: Deployment and CI/CD

## 8.1 GitHub Actions Workflows

| Workflow | File | Purpose |
|----------|------|---------|
| Main CI | `ci.yml` | Lint, format, test |
| Baseline Lab | `nixtla-baseline-lab-ci.yml` | Plugin tests |
| BigQuery Deploy | `deploy-bigquery-forecaster.yml` | Cloud Functions |

---

# Part 9: Troubleshooting Guide

## 9.1 Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| MCP server won't start | Wrong Python path | Check .mcp.json cwd |
| Tool not found | Typo in tool name | Match exactly |
| Timeout | Slow execution | Increase timeout |
| JSON parse error | Logging to stdout | Log to stderr |

---

# Part 10: Best Practices

## 10.1 MCP Server Development

1. **Log to stderr** - stdout is for MCP communication
2. **Return structured data** - JSON with success/error fields
3. **Validate inputs** - Check required params, types, ranges
4. **Handle errors gracefully** - Return error objects, don't crash
5. **Document tools** - Clear descriptions, examples

## 10.2 Plugin Organization

1. **Follow standard structure** - plugin.json, .mcp.json, scripts/
2. **Include tests** - Smoke test at minimum
3. **Write documentation** - README with examples
4. **Version appropriately** - Semver for changes

---

# Part 11: Appendices

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| MCP | Model Context Protocol - communication between Claude and tools |
| Tool | Function exposed via MCP that Claude can call |
| Skill | Markdown file that modifies Claude's behavior |
| Command | Slash command that users invoke |
| Plugin | Complete application with MCP server and tools |

## Appendix B: File Locations

| Component | Path |
|-----------|------|
| Baseline Lab | `plugins/nixtla-baseline-lab/` |
| BigQuery Forecaster | `plugins/nixtla-bigquery-forecaster/` |
| Search-to-Slack | `plugins/nixtla-search-to-slack/` |
| CI Workflows | `.github/workflows/` |

## Appendix C: Environment Variables

| Variable | Plugin | Purpose |
|----------|--------|---------|
| `NIXTLA_TIMEGPT_API_KEY` | Baseline Lab | TimeGPT API |
| `PROJECT_ID` | BigQuery | GCP project |
| `SLACK_BOT_TOKEN` | Search-to-Slack | Slack API |
| `SERPAPI_API_KEY` | Search-to-Slack | Web search |

---

**Document Created**: 2025-12-08
**Version**: 1.0.0
**Lines**: ~5000
