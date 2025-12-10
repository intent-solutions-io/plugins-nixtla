# Quickstart

**Requires**: Slack webhook, GitHub token

```bash
# Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure (copy and edit)
cp .env.example .env
# Edit .env with your Slack token and GitHub token

# Run tests (no API keys needed)
pytest tests/ -v
```

**Expected test output:** All tests pass

## What It Does

Claude searches -> Curates -> Posts to Slack

## How It Works

1. **You ask Claude** to search for Nixtla/forecasting content
2. **Claude uses WebSearch** (built-in, free)
3. **Claude curates** results (it IS Claude - no API needed)
4. **Plugin posts** formatted digest to Slack

## Required API Keys

| Key | Purpose | Get it at |
|-----|---------|-----------|
| `SLACK_BOT_TOKEN` | Slack posting | api.slack.com |
| `GITHUB_TOKEN` | GitHub search | github.com/settings/tokens |

**That's it!** No AI API keys needed - this runs inside Claude Code.

## Test Without API Keys

```bash
# Run unit tests only (mocked)
pytest tests/ -v
```

## Files

```
nixtla-search-to-slack/
├── src/nixtla_search_to_slack/
│   ├── main.py               # Entry point
│   ├── search_orchestrator.py
│   ├── ai_curator.py         # Relevance scoring (Claude does AI)
│   ├── slack_publisher.py
│   └── web_search_providers.py  # Stub (Claude does search)
├── skills/                   # 3 Claude skills
├── tests/                    # Full test suite
├── config/                   # YAML configs
├── .env.example              # API key template
└── README.md
```

## Full Setup

See `SETUP_GUIDE.md` for complete configuration.
