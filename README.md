# Nixtla Plugin Showcase for Max

> **Purpose**: Demonstrate how Claude Code plugins can make Nixtla's team faster and expand Nixtla's business
>
> **Status**: 1 working plugin (Baseline Lab) + 9 complete specifications ready to build
>
> **For Max**: Read `000-docs/078-PP-PROD-nixtla-plugin-business-case.md` first

---

## The Pitch in 60 Seconds

**Claude Code plugins can deliver 2 types of value to Nixtla:**

### 1. Internal Efficiency (Make Your Team Faster)
- **Cost Optimizer**: Reduce unnecessary TimeGPT costs by 30-50%
- **Migration Assistant**: Onboard customers from Prophet in hours, not weeks
- **Forecast Explainer**: Cut support tickets by 40% with self-serve explanations

### 2. Business Growth (Expand Your Market)
- **Airflow Operator**: Reach enterprise data platform teams
- **dbt Package**: Expand into analytics engineering market
- **Snowflake Adapter**: 10x larger enterprise contracts
- **Streaming Monitor**: Open real-time monitoring market

**ROI**: 10x-100x return on plugin development investment

---

## What's Already Built

### Nixtla Baseline Lab (v0.8.0) ✅ WORKING NOW

Try it yourself:
```bash
git clone https://github.com/jeremylongshore/claude-code-plugins-nixtla.git
cd claude-code-plugins-nixtla
# In Claude Code:
/nixtla-baseline-m4 demo_preset=m4_daily_small
```

**What it does:**
- Runs statsforecast baselines on M4 benchmark data
- Generates reproducibility bundles (metrics + versions + configs)
- Creates GitHub issue drafts with complete context
- Optional TimeGPT comparison (opt-in, cost-controlled)

**Business impact:**
- Faster customer issue debugging (complete repro in 1 command)
- Easier issue reporting for users (reduces back-and-forth)
- Benchmark quality demonstration for sales

---

## What's Planned (Specs Ready)

### 9 Complete Plugin Specifications

All detailed specs in `000-docs/050-060-*`:

| # | Plugin | Category | Business Impact |
|---|--------|----------|-----------------|
| 1 | Cost Optimizer | Efficiency | 30-50% API cost reduction |
| 2 | Migration Assistant | Efficiency | Onboarding: weeks → hours |
| 3 | Forecast Explainer | Efficiency | 40% fewer support tickets |
| 4 | VS StatsForecast Benchmark | Growth | Increase TimeGPT adoption |
| 5 | ROI Calculator | Growth | Shorten sales cycles 2-3 months |
| 6 | Airflow Operator | Growth | Enterprise data platform teams |
| 7 | dbt Package | Growth | Analytics engineering market |
| 8 | Snowflake Adapter | Growth | Fortune 500 contracts |
| 9 | Anomaly Streaming Monitor | Growth | Real-time monitoring market |

**Read the business case**: `000-docs/078-PP-PROD-nixtla-plugin-business-case.md`

---

## Repository Structure

```
nixtla-plugin-showcase/
├── plugins/
│   └── nixtla-baseline-lab/        # ✅ Working plugin (v0.8.0)
│       ├── scripts/                # MCP server, benchmarking logic
│       ├── skills/                 # AI skill for result interpretation
│       ├── tests/                  # CI validation (golden task harness)
│       └── README.md               # Complete user manual
│
├── 000-docs/                       # 69 technical documents
│   ├── 050-060-*.md               # 9 plugin specifications (COMPLETE)
│   ├── 078-PP-PROD-nixtla-plugin-business-case.md  # Business case for Max
│   ├── 6767-OD-*.md               # Architecture & planning (4 canonical docs)
│   └── 015-022-AA-*.md            # Phase 1-8 implementation AARs
│
├── scripts/
│   ├── run_nixtla_review_baseline.sh    # 2-minute demo
│   └── cleanup-doc-filing-v3.sh         # Maintenance automation
│
├── CHANGELOG.md                    # Release history (v0.1.0 → v0.8.0)
├── VERSION                         # Current: 0.8.0
└── README.md                       # This file
```

---

## For Max: How to Evaluate This

### Step 1: Try the Working Plugin (5 minutes)
```bash
# Clone repo
git clone https://github.com/jeremylongshore/claude-code-plugins-nixtla.git
cd claude-code-plugins-nixtla/plugins/nixtla-baseline-lab

# Setup Python environment
./scripts/setup_nixtla_env.sh --venv
source .venv-nixtla-baseline/bin/activate
pip install -r scripts/requirements.txt

# In Claude Code:
/nixtla-baseline-m4 demo_preset=m4_daily_small
```

**You'll get:**
- Metrics CSV (sMAPE, MASE per model)
- Human-readable summary
- GitHub-ready benchmark report
- Complete reproducibility bundle

### Step 2: Review the Business Case (10 minutes)
Read: `000-docs/078-PP-PROD-nixtla-plugin-business-case.md`

**Key questions to answer:**
- Which plugins solve your biggest pain points?
- Which plugins expand your market most?
- What's the ROI if you reduce support tickets by 40%?

### Step 3: Pick Your Top 3 Plugins (15 minutes)
Review specs: `000-docs/051-AT-ARCH-*` through `059-AT-ARCH-*`

**Decision framework:**
- **Quick Win**: Which plugin delivers value in 4-6 weeks?
- **High Impact**: Which plugin saves the most money or makes the most money?
- **Strategic**: Which plugin positions Nixtla as a platform (not just a library)?

### Step 4: Let's Talk
- **Email**: jeremy@intentsolutions.io
- **Phone**: 251.213.1115
- **Calendar**: [Schedule 30-min call]

---

## What Makes This Different

### Not Just Code Demos
Every plugin spec includes:
- Business problem statement
- ROI calculation
- Target customer segment
- Competitive positioning

### Not Just Internal Tools
Mix of:
- 33% internal efficiency (make your team faster)
- 67% business growth (expand your market)

### Not Just Ideas
- 1 working plugin (proof of execution)
- 8 completed development phases
- 69 technical documents (audit trail)
- Full CI/CD pipeline

---

## Technical Details

### Architecture
- **Plugin Framework**: Claude Code MCP servers
- **Language**: Python 3.10+
- **Nixtla Stack**: statsforecast, datasetsforecast, nixtla (TimeGPT SDK)
- **Testing**: pytest with golden task harness
- **CI/CD**: GitHub Actions with validation pipeline

### Quality Metrics
- **Test Coverage**: 65%+
- **Documentation**: 69 technical docs (Doc-Filing v3.0 compliant)
- **Version Control**: Semantic versioning (0.8.0)
- **Release Process**: Full AAR for every release

---

## What Intent Solutions Brings

### Proven Track Record
- **253+ plugins** in Claude Code marketplace (claudecodeplugins.io)
- **Deep Claude expertise**: Agent skills, MCP servers, hooks
- **Business thinking**: Plugins designed for ROI, not tech demos

### Speed
- **Baseline Lab**: 0 → working plugin in 8 weeks
- **Plugin specs**: 9 complete specifications ready to build
- **Quality**: Full documentation, CI/CD, test coverage

### Value
- **Lower risk**: Start with 1 plugin, scale what works
- **Clear ROI**: Every plugin has business case
- **Market expansion**: Reach new customer segments (Airflow, dbt, Snowflake)

---

## Next Steps

### For Max (Choose Your Own Adventure)

**Option 1: Low Risk**
- Pick 1 efficiency plugin (e.g., Cost Optimizer)
- 4-6 week timeline to MVP
- Measure productivity gains with your team

**Option 2: High Impact**
- Build 3 plugins in parallel:
  - 1 efficiency (Cost Optimizer)
  - 2 growth (Airflow + Snowflake)
- 12-16 week timeline
- Launch as "Nixtla Developer Platform"

**Option 3: Test First**
- Use Baseline Lab with your team for 30 days
- Measure time saved on customer issues
- Decide based on real data

---

## Context & Expectations

### What This Is
- **Showcase repository**: Demonstrates plugin capabilities to Nixtla CEO
- **Experimental collaboration**: Intent Solutions + Nixtla
- **Business development tool**: Make the case for plugin investment

### What This Is NOT
- Not a production SLA (experimental prototype)
- Not an official Nixtla product (community integration)
- Not over-promising ("guaranteed ROI", "enterprise-ready")

### Development Principles
1. **Business value first**: Every plugin solves a real problem
2. **ROI-driven**: Measure impact, not just features
3. **Customer-focused**: Tools for Nixtla's team AND customers
4. **Quality matters**: Full docs, tests, CI/CD

---

## FAQ for Max

**Q: How much would it cost to build these 9 plugins?**
A: Depends on which ones and how fast. Baseline Lab took 8 weeks. Let's discuss priorities.

**Q: Can we white-label these as official Nixtla products?**
A: Yes. License is MIT. You can brand them however you want.

**Q: What if we only want 2-3 plugins?**
A: Perfect. Start small, prove value, scale what works.

**Q: How do these compare to Prophet/ARIMA tooling?**
A: Prophet/ARIMA have zero AI-native tooling. This positions Nixtla as the modern alternative.

**Q: What's the maintenance burden?**
A: Low. Plugins are self-contained, CI/CD automated, documentation complete.

**Q: Can your team support this if we launch?**
A: Yes. We maintain 253+ plugins already. This is our specialty.

---

## Links & Resources

### Try It Now
- **GitHub**: https://github.com/jeremylongshore/claude-code-plugins-nixtla
- **CHANGELOG**: See version history (v0.1.0 → v0.8.0)

### Read More
- **Business Case**: `000-docs/078-PP-PROD-nixtla-plugin-business-case.md`
- **Plugin Specs**: `000-docs/050-060-*` (9 complete specifications)
- **Architecture**: `000-docs/6767-OD-ARCH-nixtla-claude-plugin-poc-baseline-lab.md`

### Contact
- **Email**: jeremy@intentsolutions.io
- **Phone**: 251.213.1115
- **Intent Solutions**: https://intentsolutions.io/

---

## The Bottom Line

You're not buying plugins.

You're buying:
- **2-3x team productivity** (efficiency plugins)
- **New customer segments** (Airflow, dbt, Snowflake integrations)
- **Competitive positioning** (AI-native tooling vs legacy libraries)

**The question isn't "should we build plugins?"**

**The question is "which 3 plugins deliver the most value in Q1 2026?"**

Let's figure that out together.

---

**Maintained by**: Intent Solutions (Jeremy Longshore)
**Sponsored by**: Nixtla (Max Mergenthaler)
**Version**: 0.8.0
**Last Updated**: 2025-11-30
