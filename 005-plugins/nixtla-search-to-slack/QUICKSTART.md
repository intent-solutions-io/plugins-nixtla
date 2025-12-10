# Quickstart

**Requires**: Slack webhook, Anthropic API key (web search via Claude Code)

```bash
# Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure (copy and edit)
cp .env.example .env
# Edit .env with your API keys

# Run tests (no API keys needed)
pytest tests/ -v

# Run search (requires API keys)
python -m nixtla_search_to_slack.main
```

**Expected test output:** All tests pass

## What It Does

Search web/GitHub → AI summarizes → Posts to Slack

## Required API Keys

| Key | Purpose | Get it at |
|-----|---------|-----------|
| `SLACK_WEBHOOK_URL` | Slack posting | api.slack.com |
| `ANTHROPIC_API_KEY` | AI summaries | console.anthropic.com |

**Web search**: Uses Claude Code's built-in WebSearch (no API key needed)

## Test Without API Keys

```bash
# Run unit tests only (mocked)
pytest tests/ -v -k "not integration"
```

## Files

```
nixtla-search-to-slack/
├── src/nixtla_search_to_slack/
│   ├── main.py              # Entry point
│   ├── search_orchestrator.py
│   ├── ai_curator.py
│   └── slack_publisher.py
├── skills/                  # 3 Claude skills
├── tests/                   # Full test suite
├── config/                  # YAML configs
├── .env.example             # API key template
└── README.md
```

## Full Setup

See `SETUP_GUIDE.md` for complete configuration (942 lines).
