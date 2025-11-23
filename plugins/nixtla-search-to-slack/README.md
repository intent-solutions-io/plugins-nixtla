# Nixtla Search-to-Slack Digest Plugin (MVP)

**Version**: 0.1.0
**Status**: Construction Kit / Reference Implementation
**Maturity**: MVP - Educational Example

---

## What This Is

This is a **Nixtla-focused Search → AI Summary → Slack digest example plugin**, intended as a construction kit and reference implementation. It demonstrates how to build automated content discovery and curation workflows for time-series forecasting practitioners.

**Key Points:**
- 🔨 **Construction Kit**: Example code for learning and adaptation
- 📚 **Reference Implementation**: Shows patterns for search → AI → Slack workflow
- 🎯 **Nixtla-Focused**: Specifically tuned for time-series/forecasting content
- 🚀 **MVP Demonstration**: Minimal viable features to prove the concept

## What This Is NOT

This plugin is explicitly **NOT**:

- ❌ **A Nixtla Product**: Not endorsed, operated, or supported by Nixtla
- ❌ **A Production Service**: Not a managed, always-on service
- ❌ **A Monitoring System**: Not suitable for critical alerting or observability
- ❌ **A Complete Solution**: Many features intentionally deferred to future phases
- ❌ **Enterprise-Ready**: Requires significant work for production deployment

## Current Capabilities (MVP)

### What's Implemented

✅ **Limited Search Sources**:
- Web search via SerpAPI (Nixtla/time-series queries only)
- GitHub search (Nixtla org + small allowlist of repos)

✅ **Basic Features**:
- Simple URL and title-based deduplication
- AI summaries using OpenAI or Anthropic
- Slack posting with Block Kit formatting
- Manual CLI triggering

✅ **Configuration**:
- YAML-based source and topic configuration
- Environment variables for secrets
- Configurable relevance thresholds

### What's NOT Implemented (Future Work)

❌ **Advanced Sources**: Reddit, Twitter/X, arXiv, YouTube, RSS feeds
❌ **Smart Deduplication**: TF-IDF, semantic similarity, embeddings
❌ **Personalization**: User preferences, reading history
❌ **Persistence**: No database, may re-send duplicates
❌ **Scalability**: Single-threaded, no queue system
❌ **Monitoring**: No metrics, alerting, or observability

## Installation

### Prerequisites

- Python 3.8+
- Slack workspace with bot permissions
- API keys for:
  - SerpAPI (web search)
  - GitHub (repository search)
  - OpenAI or Anthropic (AI summaries)

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/your-org/nixtla-search-to-slack
cd nixtla-search-to-slack
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt

# Choose your LLM provider:
pip install openai  # For OpenAI
# OR
pip install anthropic  # For Anthropic
```

4. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your API keys and tokens
```

5. **Set up Slack bot:**
- Create a new app at https://api.slack.com/apps
- Add OAuth scopes: `chat:write`, `channels:read`
- Install to workspace and copy bot token
- Add bot to target channel(s)

## Configuration

### Environment Variables (.env)

```bash
# Required
SLACK_BOT_TOKEN=xoxb-your-token
SERP_API_KEY=your-serpapi-key
GITHUB_TOKEN=ghp_your-github-token

# Choose one:
OPENAI_API_KEY=sk-your-key
# OR
ANTHROPIC_API_KEY=sk-ant-your-key

# Optional
SLACK_CHANNEL=#nixtla-updates
MAX_ITEMS_PER_DIGEST=10
DEBUG=false
```

### Topics (config/topics.yaml)

Define search topics and their parameters:

```yaml
topics:
  nixtla-core:
    name: "Nixtla Core Updates"
    keywords:
      - TimeGPT
      - StatsForecast
      - MLForecast
    sources: [web, github]
    filters:
      min_relevance: 60
    slack_channel: "#nixtla-updates"
```

### Sources (config/sources.yaml)

Configure search sources and limits:

```yaml
sources:
  web:
    provider: serpapi
    max_results: 10
    time_range: 7d
    exclude_domains: [pinterest.com]

  github:
    organizations: [Nixtla]
    additional_repos: [facebook/prophet]
    max_results: 20
```

## Usage

### Manual Execution

Run a digest for a specific topic:

```bash
python -m nixtla_search_to_slack --topic nixtla-core
```

List available topics:

```bash
python -m nixtla_search_to_slack --list-topics
```

Dry run (no Slack posting):

```bash
python -m nixtla_search_to_slack --topic nixtla-core --dry-run
```

### Scheduling (Examples Only)

**Local Cron (Linux/Mac):**
```cron
# Daily at 9 AM
0 9 * * * /path/to/venv/bin/python -m nixtla_search_to_slack --topic nixtla-core
```

**GitHub Actions (Template):**
```yaml
name: Daily Digest
on:
  schedule:
    - cron: '0 14 * * *'  # 2 PM UTC
jobs:
  digest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: pip install -e .
      - run: python -m nixtla_search_to_slack
        env:
          SLACK_BOT_TOKEN: ${{ secrets.SLACK_BOT_TOKEN }}
          # Add other secrets...
```

**Note**: Scheduling mechanisms are documented but not fully implemented. You must set up your own scheduler.

## Example Output

```
📊 Nixtla & Time Series Digest
Generated: Nov 23, 2025 at 9:00 AM PST | Items: 5

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. TimeGPT 2.0 Released with Multivariate Support
Source: GitHub • Relevance: 95%

> TimeGPT now supports multivariate time series forecasting
> with automatic feature selection and improved accuracy.

Key Points:
• Handles up to 100 variables simultaneously
• 15% accuracy improvement on M5 data
• New Python SDK with async support

Why this matters: Enables enterprise forecasting scenarios
previously requiring custom solutions.

[View Source →]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=nixtla_search_to_slack --cov-report=term-missing

# Specific test file
pytest tests/test_content_aggregator.py
```

### Code Quality

```bash
# Format code
black src/

# Lint
flake8 src/

# Type checking
mypy src/
```

### Project Structure

```
plugins/nixtla-search-to-slack/
├── src/nixtla_search_to_slack/
│   ├── main.py                 # Entry point
│   ├── search_orchestrator.py  # Search coordination
│   ├── content_aggregator.py   # Deduplication
│   ├── ai_curator.py          # AI summaries
│   ├── slack_publisher.py     # Slack posting
│   └── config_loader.py       # Configuration
├── config/
│   ├── sources.yaml           # Source config
│   └── topics.yaml           # Topic definitions
├── tests/                     # Unit tests
├── README.md                  # This file
├── requirements.txt           # Dependencies
└── .env.example              # Environment template
```

## Limitations & Disclaimers

### Technical Limitations

- **Search Coverage**: Limited to 2 sources (web + GitHub)
- **Deduplication**: Basic string matching only
- **Scalability**: Single-threaded, no queue system
- **Error Recovery**: Basic retry, may miss content on failures
- **History**: No persistence, may re-send duplicates
- **API Costs**: Each digest incurs API costs (search + LLM)

### Operational Limitations

- **No SLA**: No uptime or reliability guarantees
- **No Support**: Community-driven, best-effort only
- **No Hosting**: You must deploy and run it yourself
- **No Monitoring**: You must implement your own observability

### Legal Disclaimers

**This plugin is:**
- Provided "AS IS" without warranty of any kind
- Not affiliated with, endorsed by, or supported by Nixtla
- Your responsibility to operate in compliance with API terms
- Subject to rate limits and costs from external services

## Roadmap (Not Implemented)

### Phase 2: Enhanced Features
- [ ] Advanced deduplication (TF-IDF, embeddings)
- [ ] Additional sources (RSS, newsletters, arXiv)
- [ ] User personalization and preferences
- [ ] Slack threading for updates
- [ ] Engagement metrics and analytics

### Phase 3: Scale & Reliability
- [ ] Queue-based architecture (Celery/RQ)
- [ ] Database persistence (PostgreSQL)
- [ ] Multi-channel support
- [ ] Error recovery and dead letter queues
- [ ] Monitoring and alerting

### Phase 4: Intelligence
- [ ] Fine-tuned models for time-series domain
- [ ] Trend detection and anomaly alerting
- [ ] Recommendation engine
- [ ] Multi-language support

**Note**: These features are documented for future development but are NOT part of the current MVP implementation.

## Contributing

This is an example implementation. Feel free to:
- Fork and adapt for your needs
- Submit issues for bugs in the example code
- Share your adaptations with the community

However, please understand:
- This is not an actively maintained product
- Feature requests for the roadmap items won't be implemented
- Support is community-driven

## License

MIT License - See LICENSE file for details

## Credits

- Developed by Intent Solutions io as an example implementation
- Inspired by Nixtla's time-series forecasting tools
- Not endorsed or supported by Nixtla

---

**Remember**: This is a construction kit and learning resource, not a production service. Use it to understand the patterns and build your own solution tailored to your needs.

---

**Last Updated**: November 23, 2025
**Version**: 0.1.0 (MVP)