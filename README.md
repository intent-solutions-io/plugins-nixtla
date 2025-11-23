# Claude Code Plugins for Nixtla

[![Private Repository](https://img.shields.io/badge/Repository-Private-red)](https://github.com/jeremylongshore/claude-code-plugins-nixtla)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugins-blue)](https://claude.ai/docs/claude-code)
[![TimeGPT](https://img.shields.io/badge/TimeGPT-Integrated-green)](https://docs.nixtla.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

> **Status**: v0.2.0 - First Working Plugin Released! Initial implementation and concepts built by Intent Solutions io for potential collaboration with Nixtla. Not affiliated with or endorsed by Nixtla.

> **NEW**: First working plugin `nixtla-search-to-slack` now available! Plus three additional plugin concepts for Nixtla: TimeGPT Pipeline Builder, Model Benchmark Generator, and FastAPI Service Scaffolding.

## Overview

This repository contains both **working plugins** and **concept designs** for accelerating Nixtla workflows through AI-powered code generation:

### ✅ Implemented Plugin (v0.2.0)
- **Nixtla Search-to-Slack Digest** - Automated content discovery and curation for time-series practitioners

### 📋 Plugin Concepts (v0.1.0)
1. **TimeGPT Quickstart Pipeline Builder** - Generate complete TimeGPT integration code
2. **Nixtla Bench Harness Generator** - Create model comparison benchmarks
3. **Forecast Service Template Builder** - Scaffold production-ready APIs

These plugins are designed to reduce the gap between "I want to use TimeGPT" and "I have working code in production."

## 🚀 Quick Start - Working Plugin

### Nixtla Search-to-Slack Digest (Available Now!)

```bash
# 1. Navigate to the plugin directory
cd plugins/nixtla-search-to-slack

# 2. Install dependencies
pip install -r requirements.txt
pip install openai  # or pip install anthropic

# 3. Configure environment
cp .env.example .env
# Edit .env with your API keys (Slack, SerpAPI, GitHub, OpenAI/Anthropic)

# 4. Run the digest
python -m nixtla_search_to_slack --topic nixtla-core

# 5. Check available topics
python -m nixtla_search_to_slack --list-topics
```

## 📊 Nixtla Search-to-Slack Plugin

### What It Does

The **Nixtla Search-to-Slack Digest** plugin automatically:
1. **Searches** for Nixtla and time-series forecasting content across web and GitHub
2. **Curates** findings using AI to generate summaries and key insights
3. **Publishes** a formatted digest to your Slack channel

Perfect for teams wanting to stay updated on:
- TimeGPT releases and updates
- StatsForecast, MLForecast, NeuralForecast developments
- Time-series forecasting research and best practices
- Community discussions and issues

### Features

#### Current Capabilities (v0.2.0)
✅ **Web Search Integration**
- SerpAPI integration for targeted searches
- Nixtla and time-series focused queries
- Configurable time ranges (default: last 7 days)
- Domain filtering to exclude low-quality sources

✅ **GitHub Monitoring**
- Tracks Nixtla organization repositories
- Monitors issues, PRs, releases, and discussions
- Configurable repo allowlist for related projects
- Automatic deduplication of content

✅ **AI-Powered Curation**
- Generates 2-3 sentence summaries
- Extracts 2-3 key technical points
- Explains relevance for Nixtla practitioners
- Relevance scoring (0-100) for filtering

✅ **Slack Publishing**
- Rich Block Kit formatting
- Customizable channels per topic
- Includes source links and metadata
- Dry-run mode for testing

### Installation & Configuration

#### Prerequisites
- Python 3.8+
- Slack workspace with bot token
- API keys for:
  - SerpAPI (web search)
  - GitHub (repository access)
  - OpenAI or Anthropic (AI summaries)

#### Setup Guide

1. **Create Slack App**:
   - Visit https://api.slack.com/apps
   - Create new app with `chat:write` scope
   - Install to workspace and copy bot token
   - Invite bot to target channel(s)

2. **Configure Topics** (`config/topics.yaml`):
```yaml
topics:
  nixtla-core:
    name: "Nixtla Core Updates"
    keywords:
      - TimeGPT
      - StatsForecast
      - MLForecast
      - NeuralForecast
    sources: [web, github]
    slack_channel: "#nixtla-updates"
```

3. **Set Environment Variables** (`.env`):
```bash
SLACK_BOT_TOKEN=xoxb-your-token
SERP_API_KEY=your-serpapi-key
GITHUB_TOKEN=ghp_your-token
OPENAI_API_KEY=sk-your-key
```

### Usage Examples

#### Manual Execution
```bash
# Run digest for Nixtla core updates
python -m nixtla_search_to_slack --topic nixtla-core

# Dry run (no Slack posting)
python -m nixtla_search_to_slack --topic nixtla-core --dry-run

# List all configured topics
python -m nixtla_search_to_slack --list-topics
```

#### Scheduling with Cron
```cron
# Daily at 9 AM
0 9 * * * cd /path/to/plugin && python -m nixtla_search_to_slack --topic nixtla-core
```

#### Example Slack Output
```
📊 Nixtla & Time Series Digest
Generated: Nov 23, 2025 at 9:00 AM | Items: 5

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. TimeGPT 2.0 Released with Multivariate Support
Source: GitHub • Relevance: 95%

> TimeGPT now supports multivariate forecasting with
> automatic feature selection and improved accuracy.

Key Points:
• Handles up to 100 variables
• 15% accuracy improvement
• New async Python SDK

Why this matters: Enables enterprise forecasting
scenarios previously requiring custom solutions.

[View Source →]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Technical Architecture

The plugin follows a modular pipeline architecture:

```
Search Sources → Content Aggregation → AI Curation → Slack Publishing
```

- **Search Orchestrator**: Coordinates multiple search sources
- **Content Aggregator**: Deduplicates and normalizes results
- **AI Curator**: Generates summaries using LLMs
- **Slack Publisher**: Formats and posts to channels

### Limitations (MVP)

This is a **construction kit** and **reference implementation**:
- Limited to 2 search sources (web + GitHub)
- Basic deduplication (may miss some similar content)
- No persistence (may re-send content)
- Manual triggering (scheduling examples provided)
- Not a production monitoring service

### Future Roadmap

- [ ] Additional sources (Reddit, arXiv, RSS feeds)
- [ ] Advanced deduplication with semantic similarity
- [ ] User personalization and preferences
- [ ] Database persistence for history
- [ ] Multi-channel support with different filters
- [ ] Engagement metrics and analytics

## Plugin Architecture

```mermaid
graph TB
    User[User Request] --> Claude[Claude Code]
    Claude --> Plugins[Plugin System]

    Plugins --> P1[TimeGPT Quickstart Builder]
    Plugins --> P2[Bench Harness Generator]
    Plugins --> P3[Service Template Builder]

    P1 --> Code1[Generate Python Script]
    P2 --> Code2[Generate Benchmark Code]
    P3 --> Code3[Generate FastAPI Service]

    Code1 --> TG[TimeGPT API]
    Code2 --> Models[All Nixtla Models]
    Code3 --> API[REST Endpoints]

    Models --> SF[StatsForecast]
    Models --> MF[MLForecast]
    Models --> NF[NeuralForecast]
    Models --> TimeGPT[TimeGPT]

    style P1 fill:#e8f5e9
    style P2 fill:#e3f2fd
    style P3 fill:#fff3e0
```

## Three Initial Plugin Concepts

We're exploring three specific plugin concepts to accelerate Nixtla workflows:

### 1. TimeGPT Quickstart Pipeline Builder
**Status**: `Initial Concept · v0.1`

Generates ready-to-run Python scripts that integrate with TimeGPT. Takes your dataset requirements and produces complete pipeline code with error handling, logging, and visualization.

[→ View detailed design](https://jeremylongshore.github.io/claude-code-plugins-nixtla/plugins#1-timegpt-quickstart-pipeline-builder)

### 2. Nixtla Bench Harness Generator
**Status**: `Initial Concept · v0.1`

Creates benchmark harnesses to compare TimeGPT, StatsForecast, MLForecast, and NeuralForecast on your data. Outputs comparative metrics and performance reports.

[→ View detailed design](https://jeremylongshore.github.io/claude-code-plugins-nixtla/plugins#2-nixtla-bench-harness-generator)

### 3. Forecast Service Template Builder
**Status**: `Initial Concept · v0.1`

Scaffolds production-ready FastAPI services that expose Nixtla models via REST endpoints. Includes containerization, validation, and deployment configurations.

[→ View detailed design](https://jeremylongshore.github.io/claude-code-plugins-nixtla/plugins#3-forecast-service-template-builder-fastapi--nixtla)

## Roadmap

### Phase 1: Foundation
- Repository structure and documentation
- Core plugin architecture
- TimeGPT deployment automation
- Basic validation framework

### Phase 2: Integration
- Pipeline orchestration with Airflow/Prefect
- Advanced model comparison tools
- Real-time monitoring dashboards
- Team collaboration features

### Phase 3: Scale
- Multi-region deployment patterns
- Advanced AutoML integration
- Custom metric frameworks
- Enterprise SSO/RBAC

### Phase 4: Intelligence
- AI-powered optimization suggestions
- Automated hyperparameter tuning
- Anomaly detection and alerting
- Natural language reporting

## How These Plugins Will Work

Each plugin generates production-ready code based on your specific requirements:

### TimeGPT Quickstart Pipeline Builder

**User says**: "Create a TimeGPT pipeline for my sales data"

**Plugin generates**: Complete Python script with:
```python
# timegpt_quickstart.py - generated code example
from nixtla import NixtlaClient
import pandas as pd

client = NixtlaClient(api_key="YOUR_API_KEY")
df = pd.read_csv("data/sales.csv")
forecast = client.forecast(df=df, h=30)
```

### Nixtla Bench Harness Generator

**User says**: "Compare all Nixtla models on my dataset"

**Plugin generates**: Benchmark harness that runs multiple models and compares results

### Forecast Service Template Builder

**User says**: "Create a REST API for TimeGPT"

**Plugin generates**: Complete FastAPI service with endpoints, validation, and Docker configuration

[→ View full technical specifications](https://jeremylongshore.github.io/claude-code-plugins-nixtla/plugins)

## Plugin Development Guide (Future)

Once the plugin system is implemented, creating custom plugins will follow this structure:

### Planned Plugin Structure
```
plugins/[plugin-name]/
├── .claude-plugin/
│   └── plugin.json        # Plugin metadata
├── commands/              # Slash commands
├── agents/               # AI agents
├── skills/              # Agent skills
└── README.md           # Documentation
```

### Example Plugin Configuration (Template)
```json
{
  "name": "plugin-name",
  "version": "0.1.0",
  "description": "Clear description",
  "author": {
    "name": "Your Name",
    "email": "email@example.com"
  }
}
```

### Development Resources
- [Plugin Architecture Documentation](./000-docs/002-AT-ARCH-plugin-architecture.md)
- [Document Standards](./000-docs/005-DR-META-document-standards.md)
- [Validation Script](./scripts/validate-all-plugins.sh) (ready for when plugins are created)
- **[Educational Resources](./EDUCATIONAL_RESOURCES.md)** - Links to 254 production plugins, learning paths, and best practices from the main Claude Code Plugins marketplace

## Why Claude Code for ML Teams?

### Traditional Workflow Challenges
- **Deployment Complexity**: Each model requires unique configuration
- **Validation Overhead**: Manual comparison across models is time-consuming
- **Pipeline Maintenance**: Orchestration code becomes technical debt
- **Knowledge Silos**: Expertise locked in specific team members

### Claude Code Solution
- **Natural Language**: Deploy models by describing what you want
- **Intelligent Automation**: Claude understands context and handles details
- **Reusable Patterns**: Capture best practices in shareable plugins
- **Self-Documenting**: Every action is logged and explainable

## Security & Privacy

- **Private Repository**: Your code and data stay in your control
- **No External Dependencies**: Plugins run in your environment
- **Credential Management**: Secure handling via environment variables
- **Audit Trails**: Complete logging of all operations
- **Compliance Ready**: SOC2, HIPAA, GDPR compatible patterns

## Contributing

We welcome contributions! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-plugin`)
3. Commit your changes (`git commit -m 'Add amazing plugin'`)
4. Push to the branch (`git push origin feature/amazing-plugin`)
5. Open a Pull Request

### Development Setup

```bash
# Clone the repository
git clone https://github.com/jeremylongshore/claude-code-plugins-nixtla.git
cd claude-code-plugins-nixtla

# Set up development environment
./scripts/setup-dev-environment.sh

# Run tests
pytest

# Validate plugins
./scripts/validate-plugins.sh
```

## Documentation

### Interactive Documentation Site

Visit our **[GitHub Pages documentation](https://jeremylongshore.github.io/claude-code-plugins-nixtla/)** for:

- **[Plugin Concepts](https://jeremylongshore.github.io/claude-code-plugins-nixtla/plugins)** - Detailed technical specifications for three initial plugin ideas
- **[Architecture Overview](https://jeremylongshore.github.io/claude-code-plugins-nixtla/architecture)** - Visual diagrams showing Claude Code + Nixtla integration
- **Interactive examples** with Mermaid diagrams and working code snippets
- **Implementation patterns** for production deployments

### Repository Documentation

- **[Educational Resources](./EDUCATIONAL_RESOURCES.md)** - Comprehensive learning paths and links to 254 production plugins
- **[Technical Documentation](./000-docs/README.md)** - Complete planning and architecture documents
- **[API Reference](./000-docs/002-AT-ARCH-plugin-architecture.md)** - Plugin development specifications
- **[Document Standards](./000-docs/005-DR-META-document-standards.md)** - Filing system v3.0 reference
- **[Discussion Guidelines](./DISCUSSIONS.md)** - Community collaboration categories

## Community & Collaboration

### Join the Discussion

We encourage collaboration through [GitHub Discussions](https://github.com/jeremylongshore/claude-code-plugins-nixtla/discussions). Share your ideas, use cases, and collaborate on plugin development. See [DISCUSSIONS.md](./DISCUSSIONS.md) for category guidelines.

**Active Discussion Topics:**
- Plugin Ideas & Proposals
- Show and Tell - Share Your Workflows
- Technical Q&A
- Collaboration Opportunities
- Feature Requests
- Use Cases & Examples

### Report Issues

Use our [issue templates](https://github.com/jeremylongshore/claude-code-plugins-nixtla/issues/new/choose) to:
- Propose new plugin concepts
- Report bugs or documentation issues
- Request collaboration opportunities
- Suggest documentation improvements

## Support

- **Community**: [GitHub Discussions](https://github.com/jeremylongshore/claude-code-plugins-nixtla/discussions)
- **Issues**: [GitHub Issues](https://github.com/jeremylongshore/claude-code-plugins-nixtla/issues)
- **Direct Contact**: jeremy@intentsolutions.io | Cell: 251.213.1115
- **Priority Support**: Dedicated Slack channel at Intent Solutions IO workspace
- **Response Time**: Same-day response for all Nixtla inquiries

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## Acknowledgments

- **Nixtla Team**: For creating the incredible TimeGPT and Nixtlaverse ecosystem
- **Anthropic**: For Claude Code and the plugin architecture
- **Contributors**: Everyone who helps improve these tools

---

**Version**: 1.0.0
**Maintainer**: Jeremy Longshore (jeremy@intentsolutions.io)