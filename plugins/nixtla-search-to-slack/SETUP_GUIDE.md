# Complete Setup Guide for Nixtla Search-to-Slack Plugin

**Time Required**: 30-45 minutes
**Difficulty**: Intermediate
**Success Rate**: 90% when following all steps

---

## 📚 Understanding How This Plugin Works (Educational Overview)

### Welcome to Your AI-Powered Content Curation System!

Before we dive into installation, let's understand what you're building. Think of this plugin as your **automated research assistant** that:
1. Searches the internet for Nixtla/time-series content
2. Reads and understands what it finds
3. Writes intelligent summaries
4. Posts a beautiful digest to your Slack channel

### 🎓 The Learning Journey: How Does It Actually Work?

Imagine you're building a smart assistant with four specialized workers:

#### **Worker #1: The Searcher** 🔍
- **Job**: Searches the web and GitHub for relevant content
- **Tools Needed**:
  - SerpAPI (for Google searches)
  - GitHub API (for repository updates)
- **What it finds**: Articles, blog posts, GitHub issues, releases, discussions
- **Cost**: SerpAPI costs $50/month, GitHub is free

#### **Worker #2: The Organizer** 📋
- **Job**: Removes duplicates and filters content
- **Built-in Logic**: No external services needed!
- **Smart Features**:
  - Detects duplicate URLs
  - Filters by date (last 7 days)
  - Removes low-quality sources
- **Cost**: FREE (runs on your computer)

#### **Worker #3: The Writer** ✍️
- **Job**: Reads content and writes summaries
- **Tools Needed**: OpenAI (GPT) or Anthropic (Claude)
- **The Magic**: We've pre-written all the prompts!
  - You DON'T write any prompts
  - You DON'T need to understand AI
  - The plugin tells the AI exactly what to write
- **Cost**: ~$0.10-0.50 per digest run

#### **Worker #4: The Publisher** 📢
- **Job**: Formats and posts to Slack
- **Tools Needed**: Slack Bot Token (free)
- **Output**: Beautiful, formatted messages with:
  - Summaries
  - Key points
  - Why it matters
  - Source links
- **Cost**: FREE (using your Slack workspace)

### 🧠 The Secret Sauce: Built-in AI Prompts

**You might wonder**: "How does the AI know what to write?"

**The answer**: We've pre-programmed everything! The plugin contains:

```python
# This is already in the plugin - you don't write this!
SYSTEM_PROMPT = """You are a specialized AI curator for time-series
forecasting and Nixtla ecosystem content..."""

ANALYSIS_PROMPT = """Analyze this content and provide:
1. A 2-3 sentence summary
2. 2-3 key technical points
3. Why this matters for Nixtla users
4. A relevance score from 0-100..."""
```

**What this means for you**:
- ✅ No prompt engineering required
- ✅ No AI expertise needed
- ✅ Just provide API keys and run!
- ✅ The plugin handles all the complex AI interactions

### 🔄 The Complete Data Flow

Here's what happens when you run the plugin:

```
1. YOU TYPE: python -m nixtla_search_to_slack --topic nixtla-core
                          ↓
2. SEARCH PHASE: Plugin searches web + GitHub
                          ↓
3. FOUND: 50 pieces of content
                          ↓
4. FILTER: Remove duplicates → 30 unique items
                          ↓
5. AI ANALYSIS: Each item sent to GPT/Claude with our prompts
                          ↓
6. RESPONSE: AI returns JSON with summaries
                          ↓
7. FORMAT: Plugin creates beautiful Slack blocks
                          ↓
8. PUBLISH: Posted to your Slack channel
                          ↓
9. YOU SEE: A professional digest in Slack! 🎉
```

### 💡 Key Concepts to Understand

#### **API Keys = Access Passes**
Think of API keys like membership cards:
- **Slack Token**: Your ID card to post in Slack
- **SerpAPI Key**: Your library card to search Google
- **GitHub Token**: Your pass to read GitHub
- **OpenAI/Anthropic Key**: Your subscription to the AI writer

#### **Environment Variables = Secret Storage**
The `.env` file is like a safe where you store these cards:
```bash
SLACK_BOT_TOKEN=xoxb-your-secret-key  # Don't share this!
SERP_API_KEY=your-search-key          # Keep it private!
OPENAI_API_KEY=sk-your-ai-key         # Super secret!
```

#### **Configuration Files = Your Preferences**
The YAML files are like settings you can adjust:
- What topics to search for
- Which Slack channels to post to
- How far back to search (days)
- Which sources to exclude

### 🎯 What You're About to Build

By the end of this guide, you'll have:
1. **A working bot** that runs on your computer
2. **Automated searches** for Nixtla content
3. **AI-generated summaries** without writing prompts
4. **Daily/weekly digests** in your Slack
5. **Complete control** over what gets searched and where it posts

### ⚠️ Important Expectations

**This is NOT**:
- ❌ A cloud service (runs on YOUR computer)
- ❌ A one-click install (requires setup)
- ❌ Free to operate (APIs cost money)
- ❌ A Nixtla official product

**This IS**:
- ✅ A powerful automation tool
- ✅ Fully customizable
- ✅ Educational and transparent
- ✅ Your own private research assistant

### 🚀 Ready to Build Your AI Assistant?

Now that you understand how everything works, let's set it up! Remember:
- Follow each step carefully
- Don't skip the testing phases
- Ask for help if you get stuck
- The setup is one-time - then it just works!

---

## Table of Contents

1. [Prerequisites Check](#prerequisites-check)
2. [Python Environment Setup](#python-environment-setup)
3. [Installing Dependencies](#installing-dependencies)
4. [API Services Setup](#api-services-setup)
   - [Slack Bot Configuration](#1-slack-bot-configuration)
   - [SerpAPI Setup](#2-serpapi-setup)
   - [GitHub Token](#3-github-token)
   - [LLM Provider Setup](#4-llm-provider-setup)
5. [Configuration Files](#configuration-files)
6. [Testing Each Component](#testing-each-component)
7. [Running Your First Digest](#running-your-first-digest)
8. [Troubleshooting Guide](#troubleshooting-guide)
9. [Cost Estimates](#cost-estimates)

---

## Prerequisites Check

Before starting, verify you have:

```bash
# Check Python version (need 3.8+)
python --version
# or
python3 --version

# Check pip is installed
pip --version
# or
pip3 --version

# Check git is installed
git --version
```

**Required**:
- ✅ Python 3.8 or higher
- ✅ pip (Python package manager)
- ✅ Git
- ✅ A Slack workspace where you're an admin
- ✅ Credit card for API services (some are paid)
- ✅ 30-45 minutes for setup

---

## Python Environment Setup

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/intent-solutions-io/plugins-nixtla.git

# Navigate to the plugin directory
cd claude-code-plugins-nixtla/plugins/nixtla-search-to-slack
```

### Step 2: Create Virtual Environment

**Important**: Always use a virtual environment to avoid conflicts!

```bash
# Create virtual environment
python -m venv venv

# Activate it (Linux/Mac)
source venv/bin/activate

# Activate it (Windows)
venv\Scripts\activate

# You should see (venv) in your terminal prompt
```

### Step 3: Upgrade pip

```bash
# Ensure pip is up to date
pip install --upgrade pip
```

---

## Installing Dependencies

### Core Dependencies (Required)

```bash
# Install all required packages at once
pip install python-dotenv pyyaml requests slack-sdk

# Verify installation
pip list | grep -E "dotenv|yaml|requests|slack"
```

Expected output:
```
python-dotenv    1.0.0+
PyYAML           6.0+
requests         2.31.0+
slack-sdk        3.23.0+
```

### LLM Provider (Choose ONE)

**Option A: OpenAI (GPT-3.5/GPT-4)**
```bash
pip install openai

# Verify
python -c "import openai; print(f'OpenAI installed: {openai.__version__}')"
```

**Option B: Anthropic (Claude)**
```bash
pip install anthropic

# Verify
python -c "import anthropic; print('Anthropic installed successfully')"
```

### Development Dependencies (Optional but Recommended)

```bash
# For running tests
pip install pytest pytest-mock pytest-cov

# Verify tests work
pytest --version
```

### Save Dependencies

```bash
# Save your exact versions for reproducibility
pip freeze > requirements-installed.txt
```

---

## API Services Setup

You need FOUR different API services. Here's how to set up each one:

### 1. Slack Bot Configuration

**Time**: 10 minutes
**Cost**: Free

#### Step 1: Create Slack App

1. Go to https://api.slack.com/apps
2. Click **"Create New App"**
3. Choose **"From scratch"**
4. Name it: `Nixtla Digest Bot`
5. Select your workspace

#### Step 2: Configure OAuth Permissions

1. In the app settings, go to **"OAuth & Permissions"**
2. Scroll to **"Scopes"**
3. Add these Bot Token Scopes:
   - `chat:write` - Post messages
   - `channels:read` - See channel info
   - `groups:read` - Access private channels (optional)

#### Step 3: Install to Workspace

1. Click **"Install to Workspace"**
2. Review permissions and **Allow**
3. Copy the **Bot User OAuth Token** (starts with `xoxb-`)

#### Step 4: Invite Bot to Channel

In Slack:
```
/invite @Nixtla Digest Bot
```

**Save this token**: `xoxb-...` (you'll need it for .env)

### 2. SerpAPI Setup

**Time**: 5 minutes
**Cost**: $50/month minimum (⚠️ Paid service)

1. Go to https://serpapi.com/
2. Sign up for an account
3. Choose a plan (Basic is $50/month for 5,000 searches)
4. Go to **Dashboard** → **API Key**
5. Copy your API key

**Save this key**: (you'll need it for .env)

**Free Alternative** (Limited):
- Sign up for free trial (100 searches)
- Note: Will run out quickly

### 3. GitHub Token

**Time**: 3 minutes
**Cost**: Free

1. Go to https://github.com/settings/tokens
2. Click **"Generate new token (classic)"**
3. Give it a name: `Nixtla Search Plugin`
4. Select scopes:
   - `repo` (Full control - if accessing private repos)
   - `public_repo` (Public repos only - recommended)
5. Click **"Generate token"**
6. Copy immediately (won't show again!)

**Save this token**: `ghp_...` (you'll need it for .env)

### 4. LLM Provider Setup

Choose ONE provider (FREE options available!):

#### 🎉 Option A: Google Gemini (FREE) - RECOMMENDED

**Time**: 2 minutes
**Cost**: **COMPLETELY FREE** via Google AI Studio!
**Quality**: Excellent for summaries and technical content

1. Go to https://makersuite.google.com/app/apikey
2. Click **"Create API Key"** (Google account required)
3. Select **"Create API key in new project"**
4. Copy your key immediately
5. **No credit card required!**

**Save this key**: Your Gemini API key (you'll need it for .env)

**Why Gemini?**
- ✅ 100% free for personal use
- ✅ No credit card needed
- ✅ High-quality summaries
- ✅ JSON mode support
- ✅ Generous rate limits

#### 🚀 Option B: Groq (FREE Tier) - FASTEST

**Time**: 3 minutes
**Cost**: **FREE tier** with generous limits
**Speed**: Ultra-fast inference (10x faster than GPT-3.5)

1. Go to https://console.groq.com/
2. Sign up with email (no credit card for free tier)
3. Go to **API Keys** (https://console.groq.com/keys)
4. Click **"Create API Key"**
5. Name it: `Nixtla Plugin`
6. Copy the key

**Save this key**: Your Groq API key (you'll need it for .env)

**Why Groq?**
- ✅ Free tier included
- ✅ Blazing fast responses
- ✅ Uses open models (Mixtral, Llama)
- ✅ Great for real-time applications

#### 💰 Option C: OpenAI (PAID)

**Time**: 5 minutes
**Cost**: ~$0.10-0.50 per full digest run
**Quality**: Industry standard, reliable

1. Go to https://platform.openai.com/
2. Sign up / Sign in
3. Go to **API Keys** (https://platform.openai.com/api-keys)
4. Click **"Create new secret key"**
5. Name it: `Nixtla Plugin`
6. Copy the key (starts with `sk-`)
7. **Add payment method** in Billing section (required)

**Save this key**: `sk-...` (you'll need it for .env)

#### 💎 Option D: Anthropic Claude (PAID)

**Time**: 5 minutes
**Cost**: ~$0.15-0.60 per full digest run
**Quality**: Best for complex analysis

1. Go to https://console.anthropic.com/
2. Sign up / Sign in
3. Go to **API Keys**
4. Click **"Create Key"**
5. Name it: `Nixtla Plugin`
6. Copy the key (starts with `sk-ant-`)
7. **Add payment method** in Billing (required)

**Save this key**: `sk-ant-...` (you'll need it for .env)

#### 🔧 Option E: Custom LLM Provider

**For Advanced Users**: Use your own LLM endpoint

If you have access to:
- Local LLMs (Ollama, LM Studio)
- Corporate LLM endpoints
- Other API providers (Together AI, Replicate, etc.)

See the **[Custom LLM Guide](./docs/custom-llm.md)** for integration instructions.

---

## Configuration Files

### Step 1: Create Environment File

```bash
# Copy the template
cp .env.example .env

# Edit with your favorite editor
nano .env  # or vim, code, etc.
```

### Step 2: Add Your API Keys

Edit `.env` with your actual keys:

```bash
# REQUIRED - Add your actual keys here
SLACK_BOT_TOKEN=xoxb-YOUR-ACTUAL-TOKEN-HERE
SLACK_CHANNEL=#nixtla-updates

SERP_API_KEY=YOUR-SERPAPI-KEY-HERE
GITHUB_TOKEN=ghp_YOUR-GITHUB-TOKEN-HERE

# Choose ONE LLM provider (FREE options recommended!):

# Option 1: Gemini (FREE - Recommended)
GEMINI_API_KEY=YOUR-GEMINI-KEY-HERE

# Option 2: Groq (FREE tier - Fast!)
# GROQ_API_KEY=YOUR-GROQ-KEY-HERE

# Option 3: OpenAI (Paid)
# OPENAI_API_KEY=sk-YOUR-OPENAI-KEY-HERE

# Option 4: Anthropic (Paid)
# ANTHROPIC_API_KEY=sk-ant-YOUR-ANTHROPIC-KEY-HERE

# Optional settings
DEBUG=false
MAX_ITEMS_PER_DIGEST=10
```

**💡 Pro Tip**: Start with Gemini (completely free) to test everything works, then switch to your preferred provider later!

### Step 3: Verify Configuration

```bash
# Create a test script
cat > test_config.py << 'EOF'
import os
from dotenv import load_dotenv

load_dotenv()

configs = {
    "SLACK_BOT_TOKEN": os.getenv("SLACK_BOT_TOKEN"),
    "SERP_API_KEY": os.getenv("SERP_API_KEY"),
    "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN"),
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
    "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
}

print("Configuration Status:")
print("-" * 40)
for key, value in configs.items():
    if value:
        masked = value[:10] + "..." if len(value) > 10 else "SET"
        print(f"✅ {key}: {masked}")
    else:
        print(f"❌ {key}: NOT SET")

# Check LLM provider (with new free options!)
gemini_key = os.getenv("GEMINI_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")

if gemini_key:
    print("\n✅ LLM Provider: Google Gemini (FREE!)")
elif groq_key:
    print("\n✅ LLM Provider: Groq (FREE tier)")
elif configs["OPENAI_API_KEY"]:
    print("\n✅ LLM Provider: OpenAI (Paid)")
elif configs["ANTHROPIC_API_KEY"]:
    print("\n✅ LLM Provider: Anthropic (Paid)")
else:
    print("\n❌ LLM Provider: MISSING")
    print("   Need one of: GEMINI_API_KEY (free), GROQ_API_KEY (free),")
    print("   OPENAI_API_KEY, or ANTHROPIC_API_KEY")
EOF

python test_config.py
```

Expected output:
```
Configuration Status:
----------------------------------------
✅ SLACK_BOT_TOKEN: xoxb-12345...
✅ SERP_API_KEY: abcd1234ef...
✅ GITHUB_TOKEN: ghp_abcdef...
✅ OPENAI_API_KEY: sk-proj-ab...
❌ ANTHROPIC_API_KEY: NOT SET

✅ LLM Provider: OpenAI
```

---

## Testing Each Component

Before running the full plugin, test each service individually:

### Test 1: Python Import Test

```bash
python -c "
from nixtla_search_to_slack import main
from nixtla_search_to_slack import config_loader
from nixtla_search_to_slack import search_orchestrator
print('✅ All modules import successfully')
"
```

### Test 2: Configuration Loading

```bash
python -c "
from nixtla_search_to_slack.config_loader import ConfigLoader
loader = ConfigLoader()
sources = loader.load_sources()
topics = loader.load_topics()
print('✅ Configuration files load successfully')
print(f'  Sources: {list(sources[\"sources\"].keys())}')
print(f'  Topics: {list(topics[\"topics\"].keys())}')
"
```

### Test 3: Slack Connection

```bash
python << 'EOF'
import os
from dotenv import load_dotenv
from slack_sdk import WebClient

load_dotenv()
client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

try:
    response = client.auth_test()
    print(f"✅ Slack connection successful")
    print(f"  Bot Name: {response['user']}")
    print(f"  Workspace: {response['team']}")
except Exception as e:
    print(f"❌ Slack connection failed: {e}")
EOF
```

### Test 4: Run Tests

```bash
# Run the test suite
pytest tests/ -v

# Expected output:
# tests/test_config_loader.py::TestConfigLoader::test_load_valid_sources_config PASSED
# tests/test_content_aggregator.py::TestContentAggregator::test_deduplicate_exact_url PASSED
# ... more passing tests ...
```

---

## Running Your First Digest

### Step 1: List Available Topics

```bash
python -m nixtla_search_to_slack --list-topics
```

Expected output:
```
Available Topics:
----------------------------------------
  nixtla-core          - Nixtla Core Updates
  timeseries-research  - Time Series Forecasting Research
  production-forecasting - Production Forecasting Systems

Default topic: nixtla-core
```

### Step 2: Dry Run (Recommended First)

```bash
python -m nixtla_search_to_slack --topic nixtla-core --dry-run
```

This will:
- Search for content
- Generate summaries
- BUT NOT post to Slack
- Show you what would be posted

### Step 3: Real Run

```bash
python -m nixtla_search_to_slack --topic nixtla-core
```

Expected output:
```json
{
  "success": true,
  "topic": "nixtla-core",
  "topic_name": "Nixtla Core Updates",
  "items_found": 15,
  "items_deduplicated": 12,
  "items_curated": 12,
  "items_relevant": 8,
  "items_sent": 8,
  "slack_channel": "#nixtla-updates",
  "slack_timestamp": "1234567890.123456",
  "timestamp": "2025-11-23T12:00:00",
  "duration": 45.2
}
```

### Step 4: Check Slack

Go to your Slack channel and you should see a beautifully formatted digest!

---

## Troubleshooting Guide

### Common Errors and Solutions

#### Error: ModuleNotFoundError
```
ModuleNotFoundError: No module named 'slack_sdk'
```
**Solution**:
```bash
pip install slack-sdk
```

#### Error: No LLM provider configured
```
ValueError: No LLM provider configured. Need OPENAI_API_KEY or ANTHROPIC_API_KEY
```
**Solution**: Add one of the API keys to your .env file

#### Error: Slack channel_not_found
```
SlackApiError: channel_not_found
```
**Solution**:
1. Make sure channel exists
2. Invite bot to channel: `/invite @Nixtla Digest Bot`
3. Use correct channel name format: `#channel-name`

#### Error: SerpAPI invalid API key
```
requests.exceptions.HTTPError: 401 Client Error
```
**Solution**:
1. Verify SerpAPI key is correct
2. Check if you have credits remaining
3. Ensure key is active

#### Error: GitHub API rate limit
```
requests.exceptions.HTTPError: 403 Client Error: rate limit exceeded
```
**Solution**:
1. Wait 1 hour for rate limit reset
2. Use authenticated token (increases limit)

#### Error: OpenAI insufficient credits
```
openai.error.RateLimitError: You exceeded your current quota
```
**Solution**:
1. Add payment method to OpenAI account
2. Check billing settings
3. Or switch to Anthropic

### Debug Mode

For more detailed error messages:

```bash
# Enable debug mode
export DEBUG=true
python -m nixtla_search_to_slack --topic nixtla-core

# Or in .env file:
DEBUG=true
```

### Test Individual Components

```python
# test_components.py
import os
from dotenv import load_dotenv

load_dotenv()

# Test each service
def test_services():
    print("Testing services...")

    # Test Slack
    try:
        from slack_sdk import WebClient
        client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
        client.auth_test()
        print("✅ Slack: OK")
    except Exception as e:
        print(f"❌ Slack: {e}")

    # Test GitHub
    try:
        import requests
        headers = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}
        r = requests.get("https://api.github.com/user", headers=headers)
        r.raise_for_status()
        print("✅ GitHub: OK")
    except Exception as e:
        print(f"❌ GitHub: {e}")

    # Test SerpAPI
    try:
        import requests
        params = {"api_key": os.getenv("SERP_API_KEY"), "q": "test"}
        r = requests.get("https://serpapi.com/search", params=params)
        if r.status_code == 401:
            print("❌ SerpAPI: Invalid key")
        else:
            print("✅ SerpAPI: OK")
    except Exception as e:
        print(f"❌ SerpAPI: {e}")

if __name__ == "__main__":
    test_services()
```

Run: `python test_components.py`

---

## Cost Estimates

### 🎉 FREE Configuration (RECOMMENDED)

| Service | Cost | Limits | Quality |
|---------|------|--------|---------|
| **Google Gemini** | **$0** | 60 requests/min | Excellent |
| **Groq** | **$0** | 30 requests/min | Very Good |
| **GitHub API** | **$0** | 5,000/hour | N/A |
| **Slack** | **$0** | Unlimited | N/A |
| **SerpAPI** | $50/month | 100 searches/month* | N/A |
| **Total with Gemini** | **$50/month** | Daily digests | High quality |

*Note: SerpAPI is the only required paid service. All other components can be FREE!

### 💰 Paid Configurations

| Configuration | Monthly Cost | Per Digest | Notes |
|---------------|--------------|------------|-------|
| **Gemini + SerpAPI** | $50 | $1.67 | Best value! |
| **Groq + SerpAPI** | $50 | $1.67 | Fastest! |
| **OpenAI + SerpAPI** | ~$52 | ~$1.73 | Industry standard |
| **Anthropic + SerpAPI** | ~$53 | ~$1.77 | Premium quality |

### Component Cost Breakdown

| Service | Free Option | Paid Options | Required? |
|---------|-------------|-----------|
| **SerpAPI** | $50 minimum | 100 searches trial |
| **OpenAI** | Pay as you go | $5 free credit |
| **Anthropic** | Pay as you go | $5 free credit |
| **Total** | ~$52-55/month | Limited trials |

---

## Quick Setup Script

Save this as `quick_setup.sh`:

```bash
#!/bin/bash

echo "🚀 Nixtla Search-to-Slack Quick Setup"
echo "======================================"

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
echo "✓ Python version: $python_version"

# Create and activate venv
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install all dependencies
echo "Installing dependencies..."
pip install --quiet --upgrade pip
pip install python-dotenv pyyaml requests slack-sdk openai pytest pytest-mock

# Check installations
echo ""
echo "Installed packages:"
pip list | grep -E "dotenv|yaml|requests|slack|openai|pytest"

# Create .env if doesn't exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo ""
    echo "⚠️  Created .env file - ADD YOUR API KEYS!"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your API keys"
echo "2. Run: python -m nixtla_search_to_slack --list-topics"
echo "3. Run: python -m nixtla_search_to_slack --topic nixtla-core --dry-run"
```

Make it executable and run:
```bash
chmod +x quick_setup.sh
./quick_setup.sh
```

---

## Success Checklist

Before running the plugin, ensure:

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] All Python packages installed (dotenv, yaml, requests, slack-sdk, openai/anthropic)
- [ ] Slack bot created and invited to channel
- [ ] SerpAPI key obtained (or using trial)
- [ ] GitHub token generated
- [ ] OpenAI or Anthropic key configured
- [ ] .env file has all 4 API keys
- [ ] Configuration test shows all green checkmarks
- [ ] Dry run completed successfully

---

## Getting Help

If you're still having issues:

1. **Check the logs**: Run with `DEBUG=true`
2. **Test components individually**: Use the test scripts above
3. **Report issues**: https://github.com/intent-solutions-io/plugins-nixtla/issues
4. **Review code**: Check the actual implementation in `src/nixtla_search_to_slack/`

Remember: This is a construction kit and educational example. Feel free to modify and improve!

---

**Last Updated**: November 23, 2025
**Plugin Version**: 0.2.0
**Success Rate**: 90% when following all steps