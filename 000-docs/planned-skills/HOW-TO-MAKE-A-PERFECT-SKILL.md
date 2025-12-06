# How to Make a Perfect Claude Skill

**Document Purpose**: Master guide for creating Claude Skills that follow official Anthropic standards and Nixtla quality benchmarks

**Last Updated**: 2025-12-05
**Version**: 1.0.0
**Standards Reference**:
- [Anthropic Official Docs](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [041-SPEC-nixtla-skill-standard.md](../041-SPEC-nixtla-skill-standard.md)
- [Compliance Audit 048](../048-AA-AUDIT-nixtla-skills-compliance-vs-anthropic-official.md)

---

## 🎯 What You'll Learn

1. **Official Anthropic Standards** - What actually matters vs. what doesn't
2. **Lessons from Failures** - How Nixtla got it wrong (and fixed it)
3. **The Perfect Formula** - Proven pattern that achieves 90%+ quality scores
4. **Common Mistakes** - What to avoid based on 7 skill remediations

---

## 📚 Background: What Claude Skills Actually Are

### NOT What You Think

❌ **Skills are NOT**:
- Executable code plugins (that's MCP servers)
- Slash commands (that's commands/)
- Tools that Claude uses (that's Read, Write, Bash, etc.)

✅ **Skills ARE**:
- **Prompt packages** that modify Claude's reasoning
- **Auto-activating** based on LLM reasoning (no manual triggers)
- **Progressive disclosure** - load only when needed
- **Persistent** - installed once, available forever

### Key Insight from Anthropic

> "Skills are organized packages of instructions, executable code, and resources that give Claude specialized capabilities for specific tasks."

**Translation**: Skills make Claude smarter about your domain. They're instructions, not tools.

---

## 🏗️ Skill Architecture (3 Levels of Progressive Disclosure)

### Level 1: Discovery (Always Loaded - Keep Tiny!)

```yaml
---
name: skill-name
description: "Short description that helps Claude decide if this skill is relevant"
---
```

**Token Budget**: ~100 tokens MAX
**Purpose**: Help Claude quickly decide "Do I need this skill?"

### Level 2: Activation (Loaded When Skill Activates)

- Full `SKILL.md` body (200-500 lines)
- Contains all instructions, workflows, examples
- Modifies Claude's behavior for that session

**Token Budget**: <5,000 tokens (~500 lines) - **HARD LIMIT**

### Level 3: Resources (Loaded On-Demand)

```
skill-name/
├── SKILL.md              # Level 2
├── scripts/              # Python/Bash code Claude executes
├── references/           # Docs Claude reads into context
└── assets/               # Templates Claude references
```

**Token Budget**: Unlimited (loaded only when Claude needs them)

---

## ⚠️ Lessons from Nixtla's Compliance Failures

### Failure #1: Using Undocumented Frontmatter Fields

**What we did wrong**:
```yaml
---
name: nixtla-timegpt-lab
description: "..."
allowed-tools: "Read,Write,Bash"      # ❌ NOT IN OFFICIAL SPEC
mode: true                             # ❌ NOT IN OFFICIAL SPEC
model: inherit                         # ❌ NOT IN OFFICIAL SPEC
disable-model-invocation: false        # ❌ NOT IN OFFICIAL SPEC
version: "0.4.0"                      # ❌ NOT IN OFFICIAL SPEC
license: "Proprietary"                 # ❌ NOT IN OFFICIAL SPEC
---
```

**Impact**:
- All 7 Nixtla skills were non-compliant
- Wasted 50-80 tokens per skill at Level 1
- Risk of future conflicts with official Anthropic fields
- Made skills less portable

**The Fix**:
```yaml
---
name: nixtla-timegpt-lab
description: "Transforms Claude into Nixtla forecasting expert..."
---
```

**Official Rule**: **ONLY use `name` and `description`**. Everything else goes in SKILL.md body.

### Failure #2: Poor Description Quality

**What we did wrong**:
```yaml
description: "Mode skill that transforms Claude into a Nixtla TimeGPT forecasting expert, biasing all suggestions toward Nixtla libraries and patterns"
```

**Quality Score**: 17/100 (Very Poor)

**Problems**:
- ❌ No "Use when" trigger conditions
- ❌ No natural language phrases users would say
- ❌ Vague verbs ("biasing suggestions")
- ❌ Meta language ("mode skill") - users don't care
- ❌ Missing user vocabulary ("forecast sales", "predict demand")

**The Fix**:
```yaml
description: "Provides expert Nixtla forecasting using TimeGPT, StatsForecast, and MLForecast. Generates time series forecasts, analyzes trends, compares models, performs cross-validation, and recommends best practices. Use when user needs forecasting, time series analysis, sales prediction, demand planning, revenue forecasting, or M4 benchmarking. Trigger with 'forecast my data', 'predict sales', 'analyze time series', 'estimate demand', 'compare models'."
```

**Quality Score**: 95/100 (Excellent)

### Failure #3: Token Budget Violations

**What we did wrong**:
- `nixtla-prod-pipeline-generator`: 1,146 lines (~5,700 tokens) - **14% over limit**
- `nixtla-timegpt-finetune-lab`: 942 lines (~4,700 tokens) - Close to limit
- `nixtla-timegpt-lab`: 877 lines (~4,400 tokens) - Close to limit

**Impact**:
- Excessive context window usage
- Slower skill loading
- May hit platform limits on certain Claude surfaces

**The Fix**: Use progressive disclosure

**Before**:
```
nixtla-timegpt-lab/
└── SKILL.md (877 lines)
```

**After**:
```
nixtla-timegpt-lab/
├── SKILL.md (548 lines)          # Core instructions
└── resources/
    ├── ADVANCED_PATTERNS.md      # Advanced features
    └── EXAMPLES.md               # Detailed examples
```

**Result**: 37% size reduction, better Haiku compatibility

---

## ✅ The Perfect Skill Formula

### Step 1: Craft a High-Quality Description

**Formula**:
```
[What it does]. [Key capabilities]. Use when [conditions]. Trigger with "[phrases]".
```

**6 Quality Criteria** (must score 80%+):

| Criterion | Weight | How to Achieve |
|-----------|--------|----------------|
| **Action-Oriented** | 20% | Use strong verbs: "Generates", "Analyzes", "Transforms" |
| **Clear Triggers** | 25% | Include "Use when [scenarios]" |
| **Comprehensive** | 15% | Cover what + when + scope |
| **Natural Language** | 20% | Include phrases users say: "forecast my sales" |
| **Specificity** | 10% | Be specific without being verbose (<250 chars) |
| **Technical Terms** | 10% | Use domain keywords users naturally use |

**Example (95/100 quality)**:
```yaml
description: "Analyzes Polymarket prediction market contracts using TimeGPT forecasting. Fetches contract odds, transforms to time series, generates price predictions with confidence intervals, and detects arbitrage opportunities. Use when analyzing prediction markets, forecasting contract prices, identifying mispriced contracts, or comparing Polymarket vs Kalshi odds. Trigger with 'forecast Polymarket odds', 'analyze prediction market', 'find arbitrage opportunities'."
```

**Breakdown**:
- ✅ Action verbs: "Analyzes", "Fetches", "Transforms", "Generates", "Detects"
- ✅ Capabilities: odds fetching, time series transformation, predictions, arbitrage
- ✅ "Use when" clause with 4 scenarios
- ✅ Natural phrases: "forecast Polymarket odds", "find arbitrage opportunities"
- ✅ Specific: Mentions Polymarket, Kalshi, TimeGPT
- ✅ Technical terms: prediction markets, arbitrage, time series, confidence intervals

### Step 2: Structure SKILL.md Body (Mandatory Sections)

```markdown
---
name: skill-name
description: "[Perfect description from Step 1]"
---

# [Skill Name]

[1-2 sentence purpose statement]

## Overview

[What this skill does, when to use it, key capabilities - 3-5 sentences]

## Prerequisites

**Required**:
- [Tool/API/library 1]
- [Tool/API/library 2]

**Environment Variables**:
- `API_KEY_NAME`: [Description]

**Optional**:
- [Nice-to-have dependency]

## Instructions

### Step 1: [Action Verb]

[Clear instructions in imperative voice]

### Step 2: [Action Verb]

[More instructions]

### Step 3: [Action Verb]

[More instructions]

## Output

This skill produces:
- [File/artifact 1]
- [File/artifact 2]
- [Report/visualization]

## Error Handling

**Common Failures**:

1. **Error**: API rate limit exceeded
   **Solution**: Wait 60 seconds and retry

2. **Error**: Invalid data schema
   **Solution**: Check that data has `ds`, `y`, `unique_id` columns

## Examples

### Example 1: [Scenario]

**Input**:
```
[Example input]
```

**Output**:
```
[Example output]
```

### Example 2: [Advanced Scenario]

[Another example]

## Resources

**Additional Documentation**:
- Advanced patterns: `{baseDir}/resources/ADVANCED_PATTERNS.md`
- API reference: `{baseDir}/resources/API_DOCS.md`

**Scripts**:
- Data fetcher: `{baseDir}/scripts/fetch_data.py`
```

**Guidelines**:
- Use **imperative voice** ("Analyze data", not "You should analyze")
- Use **{baseDir}** for all paths (portability)
- Include **2-3 concrete examples**
- Keep under **500 lines** (split to resources/ if longer)

### Step 3: Implement Progressive Disclosure

**When SKILL.md exceeds 400 lines**, split content:

**Move to `resources/`**:
- Advanced patterns → `resources/ADVANCED_PATTERNS.md`
- Detailed examples → `resources/EXAMPLES.md`
- API reference → `resources/API_REFERENCE.md`
- Troubleshooting → `resources/TROUBLESHOOTING.md`

**Move to `scripts/`**:
- Data fetching → `scripts/fetch_data.py`
- Transformations → `scripts/transform.py`
- Validation → `scripts/validate.py`

**Move to `assets/`**:
- Config templates → `assets/config-template.yml`
- Sample data → `assets/sample-data.csv`

**Reference in SKILL.md**:
```markdown
## Resources

For advanced patterns, see `{baseDir}/resources/ADVANCED_PATTERNS.md`
```

---

## 🎯 Nixtla Prediction Market Skills Template

### Example: nixtla-polymarket-analyst

**Type**: Mode skill (transforms Claude's behavior)
**Domain**: Prediction markets + time series forecasting

**Perfect Frontmatter**:
```yaml
---
name: nixtla-polymarket-analyst
description: "Analyzes Polymarket prediction market contracts using TimeGPT forecasting. Fetches contract odds, transforms to time series, generates price predictions with confidence intervals, and detects arbitrage opportunities. Use when analyzing prediction markets, forecasting contract prices, identifying mispriced contracts, or comparing Polymarket vs Kalshi odds. Trigger with 'forecast Polymarket odds', 'analyze prediction market', 'find arbitrage opportunities'."
---
```

**SKILL.md Body** (350-450 lines target):

```markdown
# Nixtla Polymarket Analyst

Transform Claude into a prediction market analyst specializing in Polymarket contract forecasting using Nixtla's TimeGPT.

## Overview

This mode skill transforms Claude's behavior to treat prediction markets as time series forecasting problems. When activated, Claude will:
- Fetch Polymarket contract odds via API
- Transform odds data to Nixtla schema (ds, y, unique_id)
- Generate TimeGPT forecasts with confidence intervals
- Compare against StatsForecast baselines
- Detect arbitrage opportunities across venues

**When to use**: Analyzing prediction markets, forecasting contract prices, identifying mispriced contracts

## Prerequisites

**Required APIs**:
- Polymarket API access (free tier available)
- Nixtla TimeGPT API key (`NIXTLA_API_KEY`)

**Required Python Libraries**:
```bash
pip install nixtla statsforecast pandas requests
```

**Optional**:
- Kalshi API (for cross-venue comparison)
- PredictIt API (for arbitrage detection)

## Instructions

### Step 1: Fetch Contract Data

Use Polymarket API to retrieve historical odds:

```python
import requests

contract_id = "trump-2024-election"
url = f"https://api.polymarket.com/contracts/{contract_id}/history"
response = requests.get(url)
odds_data = response.json()
```

### Step 2: Transform to Nixtla Schema

Convert odds to time series format:

```python
import pandas as pd

df = pd.DataFrame({
    'ds': pd.to_datetime(odds_data['timestamps']),
    'y': odds_data['yes_prices'],  # Contract "Yes" price
    'unique_id': contract_id
})
```

### Step 3: Generate TimeGPT Forecast

Run TimeGPT forecast with 7-day horizon:

```python
from nixtla import NixtlaClient

client = NixtlaClient(api_key=os.getenv('NIXTLA_API_KEY'))
forecast = client.forecast(
    df=df,
    h=7,  # 7-day forecast
    freq='D',  # Daily frequency
    level=[80, 95]  # Confidence intervals
)
```

### Step 4: Compare to Baselines

Benchmark against StatsForecast:

```python
from statsforecast import StatsForecast
from statsforecast.models import SeasonalNaive, AutoETS

sf = StatsForecast(
    models=[SeasonalNaive(season_length=7), AutoETS()],
    freq='D'
)
baseline = sf.forecast(df=df, h=7)
```

### Step 5: Detect Arbitrage

Compare forecasts to current market odds:

```python
current_price = 0.52  # Current "Yes" price
forecast_mean = forecast['TimeGPT'].mean()

if abs(forecast_mean - current_price) > 0.05:
    print(f"Arbitrage opportunity: {forecast_mean:.2f} vs {current_price:.2f}")
```

## Output

This skill produces:

**Forecasts**:
- TimeGPT 7-day predictions with 80% and 95% confidence intervals
- StatsForecast baseline comparisons
- Forecast accuracy metrics (MAPE, RMSE)

**Analysis**:
- Trend direction (upward/downward/sideways)
- Volatility assessment
- Arbitrage opportunities (if detected)

**Visualization** (optional):
- Price history + forecast chart
- Confidence interval bands

## Error Handling

**Common Failures**:

1. **Error**: `NIXTLA_API_KEY not found`
   **Solution**: Set environment variable: `export NIXTLA_API_KEY=your_key`

2. **Error**: Polymarket API rate limit (429)
   **Solution**: Wait 60 seconds, then retry. Free tier: 100 requests/hour

3. **Error**: Insufficient data for forecast
   **Solution**: Need minimum 14 days of historical odds. Use `SeasonalNaive` if less data available.

4. **Error**: Invalid contract ID
   **Solution**: Check contract exists: `https://polymarket.com/event/{contract_id}`

## Examples

### Example 1: Basic Contract Forecast

**User Request**: "Forecast Trump 2024 election odds for next week"

**Claude Response**:
```
Analyzing Polymarket contract: "Trump 2024 Election"

Current Odds: 52% (Yes)
TimeGPT 7-Day Forecast: 54% ±3% (80% CI: 51-57%)
Trend: Upward momentum
Baseline (SeasonalNaive): 53%

Recommendation: Slight upside expected. TimeGPT predicts +2pp increase.
```

### Example 2: Arbitrage Detection

**User Request**: "Find arbitrage between Polymarket and Kalshi for Fed rate decision"

**Claude Response**:
```
Arbitrage Opportunity Detected!

Contract: Fed Rate Cut December 2024
- Polymarket: 68% (Yes)
- Kalshi: 61% (Yes)
- Spread: 7pp

TimeGPT Forecast: 65% ±4%

Strategy: Polymarket appears overpriced vs forecast. Consider short position.
```

## Resources

**Advanced Patterns**:
- Multi-contract correlation analysis: `{baseDir}/resources/CORRELATION_ANALYSIS.md`
- Event impact modeling: `{baseDir}/resources/EVENT_IMPACT.md`
- Liquidity forecasting: `{baseDir}/resources/LIQUIDITY_FORECAST.md`

**API Documentation**:
- Polymarket API reference: `{baseDir}/resources/POLYMARKET_API.md`
- Kalshi API reference: `{baseDir}/resources/KALSHI_API.md`

**Scripts**:
- Batch contract fetcher: `{baseDir}/scripts/fetch_all_contracts.py`
- Arbitrage scanner: `{baseDir}/scripts/scan_arbitrage.py`
```

**Key Features**:
- ✅ 420 lines (well under 500-line limit)
- ✅ Clear structure with all mandatory sections
- ✅ Concrete code examples (not pseudocode)
- ✅ Error handling for all common failures
- ✅ 2 realistic examples with expected output
- ✅ Progressive disclosure (references to resources/)

---

## 📋 Pre-Flight Checklist

Before considering a skill "done", validate against this checklist:

### Compliance (Must Pass All)

- [ ] **Frontmatter has ONLY `name` and `description`** (no other fields)
- [ ] **Description scores 80%+** on quality formula (see Step 1)
- [ ] **SKILL.md is <500 lines** (split to resources/ if needed)
- [ ] **All paths use `{baseDir}`** (never hardcode)
- [ ] **Includes all mandatory sections** (Purpose, Overview, Prerequisites, Instructions, Output, Error Handling, Examples, Resources)

### Quality (Should Pass Most)

- [ ] **2-3 concrete examples** with real input/output
- [ ] **Error handling covers 4+ common failures**
- [ ] **Instructions use imperative voice** ("Analyze data", not "You should analyze")
- [ ] **Prerequisites list all dependencies** (APIs, env vars, libraries)
- [ ] **Resources directory exists** if SKILL.md >400 lines

### Testing (Recommended)

- [ ] **Trigger phrases activate skill** (test in Claude Code)
- [ ] **Scripts execute without errors** (if using scripts/)
- [ ] **Examples produce expected output** (manual validation)
- [ ] **Skill doesn't over-trigger** (false positives)

---

## 🚀 Quick Start Template

Copy this template to start any new skill:

```markdown
---
name: nixtla-[skill-name]
description: "[What]. [Capabilities]. Use when [scenarios]. Trigger with '[phrases]'."
---

# Nixtla [Skill Name]

[1-2 sentence purpose]

## Overview

[What + when + key capabilities]

## Prerequisites

**Required**:
- [Dependency 1]

**Environment**:
- `ENV_VAR`: [Description]

## Instructions

### Step 1: [Action]

[Instructions]

### Step 2: [Action]

[Instructions]

## Output

- [Artifact 1]
- [Artifact 2]

## Error Handling

1. **Error**: [Common failure]
   **Solution**: [How to fix]

## Examples

### Example 1: [Scenario]

**Input**: [Example]
**Output**: [Result]

## Resources

- Advanced: `{baseDir}/resources/ADVANCED.md`
```

---

## 📚 Additional References

**Official Anthropic**:
- [Agent Skills Introduction](https://www.anthropic.com/news/skills)
- [Engineering Deep Dive](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Claude Console Skills](https://console.anthropic.com/workspaces/default/skills)

**Nixtla Standards**:
- [041-SPEC-nixtla-skill-standard.md](../041-SPEC-nixtla-skill-standard.md)
- [048-AA-AUDIT (Compliance Audit)](../048-AA-AUDIT-nixtla-skills-compliance-vs-anthropic-official.md)
- [050-AA-AUDIT (Description Quality)](../050-AA-AUDIT-nixtla-descriptions-quality-deep-dive.md)

**Remediation Case Studies**:
- [082-AA-POSTMORTEM (Skill 1)](../082-AA-POSTMORTEM-skill-1-nixtla-timegpt-lab.md)
- [085-AA-POSTMORTEM (Skill 2)](../085-AA-POSTMORTEM-skill-2-nixtla-experiment-architect.md)
- [087-AA-POSTMORTEM (Skill 3)](../087-AA-POSTMORTEM-skill-3-nixtla-schema-mapper.md)

---

**Last Updated**: 2025-12-05
**Maintained By**: Intent Solutions (Jeremy Longshore)
**For**: Nixtla Skills Pack v1.2.0+
