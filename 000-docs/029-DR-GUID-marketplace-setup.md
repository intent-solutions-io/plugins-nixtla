# Claude Code Marketplace Setup Guide

**Version**: 0.2.0
**Purpose**: Complete guide for installing and using Nixtla plugins via Claude Code Marketplace

---

## Table of Contents

1. [What is Claude Code Marketplace?](#what-is-claude-code-marketplace)
2. [Prerequisites](#prerequisites)
3. [Installing the Marketplace](#installing-the-marketplace)
4. [Available Plugins](#available-plugins)
5. [Plugin Setup Guides](#plugin-setup-guides)
6. [Updating Plugins](#updating-plugins)
7. [Troubleshooting](#troubleshooting)
8. [Support](#support)

---

## What is Claude Code Marketplace?

The Claude Code Marketplace allows you to extend Claude Code with custom plugins that add new capabilities. The Nixtla marketplace provides specialized plugins for time-series forecasting and Nixtla ecosystem tools.

### How Marketplaces Work

1. **Marketplace**: A collection of related plugins (like `nixtla-plugins`)
2. **Plugins**: Individual tools within a marketplace (like `nixtla-search-to-slack`)
3. **Installation**: Add marketplace → Install specific plugins → Configure → Use

---

## Prerequisites

Before installing, ensure you have:

### Required
- ✅ **Claude Code CLI** installed and configured
- ✅ **Git** for repository cloning
- ✅ **Python 3.8+** (for the Search-to-Slack plugin)

### How to Check
```bash
# Check Claude Code CLI
claude --version

# Check Python
python --version  # Should be 3.8 or higher

# Check Git
git --version
```

---

## Installing the Marketplace

### Step 1: Add the Nixtla Marketplace

In your Claude Code terminal, run:

```bash
claude marketplace add https://github.com/intent-solutions-io/plugins-nixtla.git
```

This registers the Nixtla marketplace with your Claude Code installation.

### Step 2: Verify Installation

List available marketplaces:

```bash
claude marketplace list
```

You should see:
```
Available Marketplaces:
- nixtla-plugins (0.2.0) - Nixtla time-series forecasting plugins
```

### Step 3: View Available Plugins

List plugins in the Nixtla marketplace:

```bash
claude plugin list --marketplace nixtla-plugins
```

Output:
```
Available Plugins:
✅ nixtla-search-to-slack - Automated content discovery and Slack digests
⏳ nixtla-timegpt-builder - Generate TimeGPT pipelines (coming soon)
⏳ nixtla-bench-harness - Compare Nixtla models (coming soon)
⏳ nixtla-service-template - FastAPI service scaffolding (coming soon)
```

---

## Available Plugins

### 1. Nixtla Search-to-Slack (AVAILABLE NOW)

**Purpose**: Automatically search for Nixtla/time-series content and post digests to Slack

**Installation**:
```bash
claude plugin install nixtla-search-to-slack
```

**Key Features**:
- 🔍 Searches web and GitHub for relevant content
- 🤖 AI-powered summaries (supports FREE options!)
- 📢 Posts formatted digests to Slack
- ⚙️ Fully configurable topics and sources

**Setup Required**:
- Slack bot token (free)
- Search API key (SerpAPI - $50/month)
- LLM API key (Gemini FREE or others)
- GitHub token (free)

**[📚 Complete Setup Guide →](../005-plugins/nixtla-search-to-slack/SETUP_GUIDE.md)**

### 2. TimeGPT Pipeline Builder (COMING SOON)

**Purpose**: Generate complete TimeGPT integration code from requirements

**Planned Features**:
- Generate Python/R/Julia code
- Handle data preprocessing
- Include error handling
- Add visualization

### 3. Nixtla Bench Harness (COMING SOON)

**Purpose**: Compare TimeGPT, StatsForecast, MLForecast, and NeuralForecast

**Planned Features**:
- Automated benchmarking
- Performance metrics
- Visualization reports
- Cost analysis

### 4. Forecast Service Template (COMING SOON)

**Purpose**: Scaffold production-ready FastAPI services for Nixtla models

**Planned Features**:
- REST API endpoints
- Docker configuration
- Authentication
- Deployment scripts

---

## Plugin Setup Guides

### Setting Up Search-to-Slack Plugin

After installation, follow these steps:

#### 1. Navigate to Plugin Directory
```bash
cd ~/.claude/005-plugins/nixtla-search-to-slack
# or wherever Claude Code installed it
```

#### 2. Install Python Dependencies
```bash
pip install -r requirements.txt

# For FREE AI option (recommended):
pip install google-generativeai

# Or for other options:
pip install groq      # Free tier
pip install openai    # Paid
pip install anthropic # Paid
```

#### 3. Configure Environment
```bash
cp .env.example .env
nano .env  # Edit with your API keys
```

#### 4. Get FREE API Keys

**Google Gemini (FREE - Recommended)**:
1. Visit https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy and add to `.env`: `GEMINI_API_KEY=your-key`

**Groq (FREE tier)**:
1. Visit https://console.groq.com/
2. Sign up and go to API Keys
3. Create key and add to `.env`: `GROQ_API_KEY=your-key`

**Other Required Keys**:
- **Slack Bot**: https://api.slack.com/apps (free)
- **GitHub**: https://github.com/settings/tokens (free)
- **SerpAPI**: https://serpapi.com/ ($50/month)

#### 5. Test Your Setup
```bash
# List available topics
python -m nixtla_search_to_slack --list-topics

# Run a dry run (no Slack posting)
python -m nixtla_search_to_slack --topic nixtla-core --dry-run

# Run for real
python -m nixtla_search_to_slack --topic nixtla-core
```

**[📖 Detailed Setup Instructions →](../005-plugins/nixtla-search-to-slack/SETUP_GUIDE.md)**

---

## Updating Plugins

### Update Entire Marketplace
```bash
claude marketplace update nixtla-plugins
```

### Update Specific Plugin
```bash
claude plugin update nixtla-search-to-slack
```

### Check for Updates
```bash
claude plugin check-updates --marketplace nixtla-plugins
```

---

## Troubleshooting

### Common Issues

#### 1. Marketplace Not Found
```
Error: Could not find marketplace at URL
```
**Solution**: Ensure the repository is public or you have access rights

#### 2. Plugin Installation Fails
```
Error: Plugin nixtla-search-to-slack not found
```
**Solution**: Update the marketplace first:
```bash
claude marketplace update nixtla-plugins
```

#### 3. Python Dependencies Error
```
ModuleNotFoundError: No module named 'google.generativeai'
```
**Solution**: Install the required package:
```bash
pip install google-generativeai  # For Gemini
pip install groq                  # For Groq
```

#### 4. API Key Issues
```
ValueError: No LLM provider configured
```
**Solution**: Ensure at least one LLM API key is set in `.env`:
- `GEMINI_API_KEY` (free)
- `GROQ_API_KEY` (free tier)
- `OPENAI_API_KEY` (paid)
- `ANTHROPIC_API_KEY` (paid)

### Manual Installation (Alternative)

If marketplace installation fails, install manually:

```bash
# 1. Clone the repository
git clone https://github.com/intent-solutions-io/plugins-nixtla.git
cd claude-code-plugins-nixtla

# 2. Install plugin locally
claude plugin install --dev ./005-plugins/nixtla-search-to-slack

# 3. Continue with setup as above
```

---

## Support

### Getting Help

1. **Documentation**:
   - [Main README](../README.md)
   - [Plugin Setup Guide](../005-plugins/nixtla-search-to-slack/SETUP_GUIDE.md)
   - [Educational Resources](027-UC-GUID-educational-resources.md)

2. **GitHub Issues**:
   - Report bugs: https://github.com/intent-solutions-io/plugins-nixtla/issues
   - Request features: Use "enhancement" label

3. **Community**:
   - GitHub Discussions: https://github.com/intent-solutions-io/plugins-nixtla/discussions

### Contact

- **Maintainer**: Jeremy Longshore
- **Email**: jeremy@intentsolutions.io
- **Response Time**: Same-day for Nixtla-related inquiries

### Important Notes

⚠️ **Disclaimers**:
- This is NOT an official Nixtla product
- Plugins are provided as educational examples
- You are responsible for API costs
- No warranty or support SLA provided

✅ **What We Provide**:
- Working example code
- Comprehensive documentation
- Configuration templates
- Community support

---

## Next Steps

1. **Install the Search-to-Slack plugin** (it's ready now!)
2. **Get your FREE Gemini API key** (no credit card needed)
3. **Set up Slack bot** (takes 5 minutes)
4. **Run your first digest** and see it work!

The entire setup takes about 30-45 minutes, and then you'll have an automated AI research assistant posting to your Slack daily!

---

**Last Updated**: November 23, 2025
**Version**: 0.2.0
**Status**: First plugin released and working!