# Nixtla DeFi Sentinel - User Journey Maps

**Plugin ID:** nixtla-defi-sentinel
**Category:** Growth - New Market Entry
**Created:** 2025-12-02
**Status:** Specified
**Version:** 1.0

---

## Executive Summary

This document maps the end-to-end user journeys for all **Nixtla DeFi Sentinel** personas, from initial discovery through long-term usage and expansion. Each journey identifies key touchpoints, emotional states, pain points, and opportunities for product improvement.

**Primary Persona:** DeFi Protocol Security Lead
**Secondary Personas:** Institutional Crypto Trader, Blockchain Analytics Firm, Crypto Insurance Protocol

---

## Table of Contents

1. [Persona Overview](#persona-overview)
2. [Journey Map 1: DeFi Protocol Security Lead](#journey-map-1-defi-protocol-security-lead)
3. [Journey Map 2: Institutional Crypto Trader](#journey-map-2-institutional-crypto-trader)
4. [Journey Map 3: Blockchain Analytics Firm](#journey-map-3-blockchain-analytics-firm)
5. [Journey Map 4: Crypto Insurance Protocol](#journey-map-4-crypto-insurance-protocol)
6. [Cross-Persona Insights](#cross-persona-insights)
7. [Touchpoint Analysis](#touchpoint-analysis)
8. [Opportunity Map](#opportunity-map)

---

## Persona Overview

### Persona 1: DeFi Protocol Security Lead (Primary)

**Demographics:**
- **Role**: Head of Security, CTO, VP Engineering
- **Company Size**: 20-100 employees
- **Protocol TVL**: $50M - $5B
- **Budget Authority**: $500K - $2M annual security spend
- **Technical Depth**: High (Solidity, blockchain architecture)

**Goals:**
- Prevent exploits before they happen
- Reduce manual security monitoring workload
- Provide audit trail for compliance
- Sleep better at night knowing threats are monitored 24/7

**Pain Points:**
- Manual audits take weeks, only cover code (not runtime behavior)
- No real-time visibility into on-chain anomalies
- Alert fatigue from rule-based monitoring tools (too many false positives)
- Post-exploit forensics are time-consuming and embarrassing

**Motivations:**
- Career risk: A major exploit could end their career
- Reputation: Want to be known as the "secure protocol"
- Efficiency: Tired of manual log analysis and alert triage

---

### Persona 2: Institutional Crypto Trader

**Demographics:**
- **Role**: Portfolio Manager, Risk Analyst
- **Company**: Crypto hedge fund, family office
- **AUM**: $10M - $500M
- **Positions**: 20-50 active DeFi positions across protocols
- **Technical Depth**: Medium (understands DeFi mechanics, not Solidity)

**Goals:**
- Early warning of protocol risks (exit before exploit)
- Portfolio-level risk monitoring (aggregate exposure)
- Automated alerts for abnormal behavior
- Justification for investment decisions (data-driven)

**Pain Points:**
- No aggregated view of risks across portfolio
- Manual checking of protocol dashboards (time-consuming)
- Learn about exploits after TVL crashes (too late to exit)
- Difficulty explaining risk management to LPs

**Motivations:**
- Performance: Avoiding losses is as important as gains
- Compliance: LPs require risk management documentation
- Competitive edge: Early information = better decisions

---

### Persona 3: Blockchain Analytics Firm

**Demographics:**
- **Role**: Director of Research, Data Science Lead
- **Company**: Blockchain intelligence/analytics provider
- **Customers**: Crypto exchanges, protocols, institutions
- **Revenue Model**: Subscription data feeds ($5K-50K/month per customer)
- **Technical Depth**: Very High (data engineering, ML)

**Goals:**
- Differentiated data products (not available elsewhere)
- Real-time threat intelligence feeds
- White-label solutions for customers
- Expand service offerings beyond transaction tracking

**Pain Points:**
- Competing with Chainalysis, Elliptic (commodity market)
- Difficult to build in-house anomaly detection (ML expertise required)
- Customers want predictive intelligence, not just historical data
- Integration challenges (every customer has different data stack)

**Motivations:**
- Revenue growth: New product lines increase ARPU
- Market differentiation: AI-powered features justify premium pricing
- Operational efficiency: Buy vs build for anomaly detection

---

### Persona 4: Crypto Insurance Protocol

**Demographics:**
- **Role**: Chief Risk Officer, Underwriting Lead
- **Company**: DeFi insurance protocol (Nexus Mutual, InsurAce)
- **Policies Issued**: 1,000+ active policies
- **Total Cover**: $50M - $500M
- **Technical Depth**: High (smart contract risks, DeFi mechanics)

**Goals:**
- Accurate risk pricing (avoid under-pricing policies)
- Real-time risk adjustment (pause coverage for risky protocols)
- Automated claims validation (reduce fraud)
- Expand coverage to more protocols (data-driven confidence)

**Pain Points:**
- Manual underwriting is slow (weeks per protocol)
- No real-time monitoring of insured protocols
- Claims are difficult to validate (was it exploit or user error?)
- Limited historical exploit data for actuarial modeling

**Motivations:**
- Profitability: Accurate pricing prevents losses
- Scale: Automated risk assessment enables more policies
- Trust: Data-driven claims process reduces disputes

---

## Journey Map 1: DeFi Protocol Security Lead

### Stage 1: Discovery

**Scenario:** Security lead hears about SCONE-bench research showing AI agents exploiting contracts.

| Phase | Touchpoint | User Action | Emotional State | Pain Point | Opportunity |
|-------|-----------|-------------|-----------------|-----------|-------------|
| **Awareness** | Twitter / Crypto News | Reads Anthropic SCONE-bench article | 😰 Anxious | "Are we vulnerable to AI attacks?" | Content marketing: "How to defend against AI attackers" |
| **Research** | Google Search | Searches "AI DeFi security monitoring" | 🤔 Curious | Too many options, unclear differentiation | SEO: Rank for "AI DeFi security", "TimeGPT smart contracts" |
| **Evaluation** | Nixtla DeFi Sentinel website | Reads business case, watches demo | 😃 Hopeful | Need to justify budget to CFO | ROI calculator tool (input TVL, get projected savings) |
| **Trial** | Claude Code plugin | Installs plugin, scans their contracts | 😮 Impressed | How accurate are these anomaly detections? | Free tier: 5 contracts, 30 days trial |

**Key Insight:** Security leads are motivated by fear (exploit risk) + curiosity (new AI tech). Show them concrete threat mitigation, not just features.

---

### Stage 2: Onboarding

**Scenario:** Security lead signs up for Professional tier ($5K/month, 20 contracts).

| Phase | Touchpoint | User Action | Emotional State | Pain Point | Opportunity |
|-------|-----------|-------------|-----------------|-----------|-------------|
| **Sign-Up** | Dashboard | Creates account, enters payment | 😬 Cautious | "Will this actually work in production?" | Social proof: Logos of other protocols using Sentinel |
| **Configuration** | Contract Setup | Adds 5 critical contracts to monitor | 🤓 Engaged | "Which metrics should I monitor?" | Smart defaults: Auto-configure thresholds based on contract type (DEX, lending, etc.) |
| **Integration** | Alert Channels | Connects Slack workspace | 😌 Relieved | "Don't want to miss critical alerts" | Pre-built Slack templates with rich formatting |
| **Validation** | Historical Analysis | Reviews last 30 days of data | 🤨 Skeptical | "Would this have caught past incidents?" | Show historical anomalies that preceded known exploits |

**Key Insight:** Onboarding must prove value immediately. Historical analysis shows "what we would have caught" to build confidence.

---

### Stage 3: Daily Usage

**Scenario:** Security lead uses Sentinel for ongoing monitoring over 3 months.

| Phase | Touchpoint | User Action | Emotional State | Pain Point | Opportunity |
|-------|-----------|-------------|-----------------|-----------|-------------|
| **Morning Check** | Dashboard | Reviews overnight anomalies | ☕ Routine | Too many low-severity alerts (noise) | Machine learning: Learn user's threshold preferences over time |
| **Alert Triage** | Slack Notification | Receives "High Severity: TVL drop 15%" | 😨 Alarmed | "Is this a real threat or false positive?" | Context: Compare to other protocols, show historical patterns |
| **Investigation** | Claude Code Plugin | Asks Claude: "Analyze 0xabc123 anomaly" | 🕵️ Investigating | Manual on-chain analysis is time-consuming | AI assistant: Auto-generate investigation runbook |
| **Resolution** | Dashboard | Marks alert as "False Positive: Expected" | 😮‍💨 Relieved | "Need to prevent this false alarm next time" | Feedback loop: "Why was this a false positive?" → tune model |

**Key Insight:** Daily usage reveals the false positive problem. Build feedback loops to improve accuracy over time.

---

### Stage 4: Advanced Usage

**Scenario:** Security lead becomes power user, leverages advanced features (Phase 2+).

| Phase | Touchpoint | User Action | Emotional State | Pain Point | Opportunity |
|-------|-----------|-------------|-----------------|-----------|-------------|
| **Forecasting** | Dashboard | Enables 1-hour ahead TVL forecasts | 🔮 Empowered | "Want to predict exploits before they happen" | Early warning alerts: "TVL forecast shows 20% drop in next hour" |
| **Custom Models** | API | Uploads historical incident data, fine-tunes TimeGPT | 🧑‍🔬 Expert | "Need protocol-specific anomaly detection" | Custom model marketplace: Share models with other protocols |
| **Automation** | Webhook Integration | Connects to Safe multisig for auto-pause | 🤖 Confident | "Want to respond to threats in seconds, not minutes" | Pre-built runbooks: "If TVL drops > 20%, pause deposits" |
| **Reporting** | PDF Export | Generates monthly security report for board | 📊 Professional | "Board wants proof we're monitoring risks" | White-label reports: Include company branding |

**Key Insight:** Power users want automation and customization. Provide APIs and integrations for advanced workflows.

---

### Stage 5: Renewal & Expansion

**Scenario:** Security lead renews annual contract, expands to Enterprise tier.

| Phase | Touchpoint | User Action | Emotional State | Pain Point | Opportunity |
|-------|-----------|-------------|-----------------|-----------|-------------|
| **Renewal Decision** | Dashboard | Reviews usage stats: 12 exploits prevented | 🎉 Validated | "Need to justify renewal to CFO" | ROI report: "Sentinel prevented $X in losses, saved Y engineer hours" |
| **Upsell** | Sales Call | Upgrades to Enterprise tier (50 contracts) | 🤝 Trusting | "We're launching 10 new contracts this quarter" | Volume pricing: Discount for 50+ contracts |
| **Referral** | Conference | Recommends Sentinel to peer protocols | 😎 Advocate | None (delighted customer) | Referral program: $500 credit per referral |
| **Case Study** | Marketing Collab | Agrees to co-authored blog post | 🏆 Proud | None (wants to showcase security leadership) | Customer spotlight: Feature on Nixtla blog |

**Key Insight:** Delighted customers become advocates. Provide them with tools to share their success (reports, referrals, case studies).

---

## Journey Map 2: Institutional Crypto Trader

### Stage 1: Discovery

**Scenario:** Trader loses 10% of portfolio value in a DeFi exploit, wants early warning system.

| Phase | Touchpoint | User Action | Emotional State | Pain Point | Opportunity |
|-------|-----------|-------------|-----------------|-----------|-------------|
| **Trigger Event** | Portfolio Loss | Exits position after 15% TVL drop | 😡 Frustrated | "Why didn't I see this coming?" | Retargeting ads: "Never miss a DeFi exploit again" |
| **Research** | Crypto Twitter | Sees Sentinel mentioned by influencer | 🤔 Curious | "Do other traders use this?" | Influencer partnerships: Sponsor crypto analysts |
| **Evaluation** | Demo Video | Watches 2-minute walkthrough | 😃 Hopeful | "Will this integrate with my portfolio tracker?" | Integration docs: Show CSV export, API access |
| **Trial** | API Access | Tests API with 5 portfolio positions | 😮 Impressed | "How fast are the alerts?" | Latency guarantee: <30 seconds anomaly detection |

---

### Stage 2: Onboarding

**Scenario:** Trader subscribes to Starter tier ($1K/month, 5 contracts).

| Phase | Touchpoint | User Action | Emotional State | Pain Point | Opportunity |
|-------|-----------|-------------|-----------------|-----------|-------------|
| **Sign-Up** | API Dashboard | Creates API key, tests endpoint | 🤓 Engaged | "Need to automate this into my trading bot" | Sample code: Python script for portfolio monitoring |
| **Configuration** | Contract List | Imports 20 DeFi protocols from CSV | 😬 Cautious | "Don't want to monitor all 20, which are highest risk?" | Risk scoring: Auto-rank protocols by risk level |
| **Integration** | Trading Bot | Connects API to custom Python script | 💻 Productive | "Need to trigger sell orders on critical alerts" | Webhook examples: "On critical alert → sell 50% position" |
| **Validation** | Backtest | Runs historical analysis on past 6 months | 🤨 Skeptical | "Would this have saved me money?" | Backtest report: "$150K losses prevented if using Sentinel" |

---

### Stage 3: Daily Usage

**Scenario:** Trader monitors 20 DeFi positions, receives 2-3 alerts per week.

| Phase | Touchpoint | User Action | Emotional State | Pain Point | Opportunity |
|-------|-----------|-------------|-----------------|-----------|-------------|
| **Pre-Market** | Email Digest | Reviews overnight alerts | ☕ Routine | "Too many low-priority alerts" | Digest customization: Only send critical + high |
| **Alert Response** | SMS | Receives "Critical: Aave TVL drop 10%" | 😨 Alarmed | "Need to decide: exit or hold?" | Context: "Similar alerts in past were false 60% of time" |
| **Portfolio Rebalance** | Trading Platform | Reduces Aave position by 30% | 😌 Relieved | "Did I overreact?" | Performance tracking: Track P&L impact of alert-driven trades |
| **Monthly Review** | Dashboard | Reviews alert accuracy, P&L impact | 📊 Analytical | "Are these alerts actually profitable?" | ROI dashboard: "Alerts saved $X vs cost of false exits" |

---

### Stage 4: Advanced Usage

**Scenario:** Trader builds automated risk management system on top of Sentinel API.

| Phase | Touchpoint | User Action | Emotional State | Pain Point | Opportunity |
|-------|-----------|-------------|-----------------|-----------|-------------|
| **API Automation** | Custom Script | Builds Python bot: alert → auto-reduce position | 🤖 Empowered | "Need historical alert feed for backtesting" | Historical API: Access 1 year of past alerts |
| **Risk Analytics** | Jupyter Notebook | Analyzes correlation between alerts and price drops | 🧑‍🔬 Expert | "Want to combine Sentinel data with on-chain metrics" | Data exports: CSV, Parquet, Snowflake connector |
| **Portfolio Optimization** | Custom Model | Trains ML model to predict exploit risk using Sentinel features | 🔮 Innovative | "Sentinel API is great, but I need more granular data" | Premium API tier: Real-time metric streams (not just alerts) |

---

### Stage 5: Renewal & Expansion

**Scenario:** Trader upgrades to Professional tier, refers other traders.

| Phase | Touchpoint | User Action | Emotional State | Pain Point | Opportunity |
|-------|-----------|-------------|-----------------|-----------|-------------|
| **ROI Analysis** | Spreadsheet | Calculates: Saved $200K losses, paid $12K for Sentinel | 🎉 Validated | None (clear ROI) | Testimonial: "Sentinel paid for itself 16x over" |
| **Expansion** | Upgrade | Adds 15 more contracts (now monitoring 50 total) | 🤝 Trusting | "Need better portfolio-level risk view" | Portfolio dashboard: Aggregate risk score across all positions |
| **Community** | Discord | Joins Sentinel Discord, shares trading strategies | 😎 Advocate | None (community member) | User community: Monthly AMA with Nixtla data scientists |

---

## Journey Map 3: Blockchain Analytics Firm

### Stage 1: Discovery

**Scenario:** Analytics firm's largest customer requests "AI-powered threat intelligence" feature.

| Phase | Touchpoint | User Action | Emotional State | Pain Point | Opportunity |
|-------|-----------|-------------|-----------------|-----------|-------------|
| **Customer Request** | Sales Call | Hears "We want predictive security, not just historical data" | 😰 Pressured | "We don't have ML expertise in-house" | Whitepaper: "Build vs Buy: DeFi Anomaly Detection" |
| **Market Research** | Competitive Analysis | Evaluates 5 anomaly detection vendors | 🤔 Evaluating | "Need white-label solution, not branded product" | Partner program: White-label Sentinel API |
| **Technical Evaluation** | API Docs | Reviews API endpoints, data schemas | 🤓 Engaged | "How does this integrate with our data pipeline?" | Integration guide: Snowflake, BigQuery, Databricks |
| **POC** | Trial Account | Tests API with 100 contracts (customer's portfolio) | 🧑‍🔬 Experimenting | "Need to prove ROI to customer" | Success metrics: "85% anomaly detection accuracy" |

---

### Stage 2: Onboarding

**Scenario:** Analytics firm signs white-label partnership ($10K/month + 20% revenue share).

| Phase | Touchpoint | User Action | Emotional State | Pain Point | Opportunity |
|-------|-----------|-------------|-----------------|-----------|-------------|
| **Contract Negotiation** | Legal Call | Negotiates white-label terms, SLAs | 🤝 Collaborative | "Need 99.9% uptime SLA for enterprise customers" | Enterprise SLA: Dedicated infrastructure, 24/7 support |
| **Technical Onboarding** | Kickoff Call | Receives API keys, integration documentation | 💻 Productive | "How do we customize alert logic?" | Custom model training: Provide training data, get fine-tuned TimeGPT |
| **Integration** | Data Pipeline | Builds ETL: Sentinel API → Snowflake → Customer Dashboards | 🏗️ Building | "Need real-time streaming, not batch API" | WebSocket API: Stream anomalies in real-time |
| **Go-to-Market** | Marketing Collab | Co-authors case study: "How [Firm] Added AI Threat Intel" | 📣 Excited | "How do we position this vs competitors?" | Competitive messaging: "Only AI-native solution" |

---

### Stage 3: Daily Usage

**Scenario:** Analytics firm operates Sentinel as white-label service for 20 customers.

| Phase | Touchpoint | User Action | Emotional State | Pain Point | Opportunity |
|-------|-----------|-------------|-----------------|-----------|-------------|
| **Customer Onboarding** | Internal Dashboard | Onboards new customer's 50 contracts | ☕ Routine | "Manual onboarding takes 2 hours per customer" | Self-serve API: Customers can add contracts via UI |
| **Alert Distribution** | Data Pipeline | Routes Sentinel alerts → 20 customer Slack channels | 😌 Reliable | "Need to filter alerts by customer's contract list" | Multi-tenant API: Each customer sees only their contracts |
| **Support Escalation** | Support Ticket | Customer reports false positive, forwards to Sentinel | 😬 Concerned | "We don't understand the ML model, hard to explain to customers" | Partner training: Monthly ML explainability sessions |
| **Billing** | Invoice | Receives monthly usage report: 50K API calls, $10K flat + $2K overage | 💰 Calculating | "Unpredictable overage costs hurt margins" | Predictable pricing: Flat fee per contract, no overage |

---

### Stage 4: Advanced Usage

**Scenario:** Analytics firm builds custom ML models on top of Sentinel data.

| Phase | Touchpoint | User Action | Emotional State | Pain Point | Opportunity |
|-------|-----------|-------------|-----------------|-----------|-------------|
| **Data Export** | API | Exports 1 year of historical anomaly data | 📊 Analytical | "Need raw time-series data, not just anomalies" | Data marketplace: Sell raw metric streams (extra revenue for Nixtla) |
| **Custom Models** | ML Pipeline | Trains proprietary exploit prediction model using Sentinel features | 🧑‍🔬 Expert | "Want to combine Sentinel data with our transaction graph data" | Feature engineering API: Expose derived features (TVL velocity, etc.) |
| **Productization** | Customer Dashboard | Launches "AI Exploit Risk Score" powered by Sentinel + custom models | 🚀 Launching | "How do we differentiate from raw Sentinel alerts?" | Partner co-marketing: "Powered by Nixtla TimeGPT" badge |

---

### Stage 5: Renewal & Expansion

**Scenario:** Analytics firm expands to 50 customers, negotiates volume discount.

| Phase | Touchpoint | User Action | Emotional State | Pain Point | Opportunity |
|-------|-----------|-------------|-----------------|-----------|-------------|
| **Growth** | Internal Metrics | Reviews: 50 customers, $50K MRR from AI features | 🎉 Celebrating | "Sentinel costs are growing faster than revenue" | Volume discount: 30% off for 1,000+ contracts |
| **Renewal Negotiation** | Partner Call | Negotiates: $20K/month flat + 15% revenue share (down from 20%) | 🤝 Collaborative | "Want more control over infrastructure" | Self-hosted option: Deploy Sentinel in customer's cloud |
| **Strategic Partnership** | Joint Roadmap | Co-develops new features: fraud detection, MEV monitoring | 🤜🤛 Partners | None (strategic alignment) | Co-innovation: Share 50% of new product revenue |

---

## Journey Map 4: Crypto Insurance Protocol

### Stage 1: Discovery

**Scenario:** Insurance protocol's underwriting team is overwhelmed with manual risk assessments.

| Phase | Touchpoint | User Action | Emotional State | Pain Point | Opportunity |
|-------|-----------|-------------|-----------------|-----------|-------------|
| **Pain Point** | Underwriting Backlog | Takes 2 weeks to underwrite 1 new protocol | 😰 Overwhelmed | "We're turning away policies due to capacity" | Content: "Automate DeFi Underwriting with AI" |
| **Research** | LinkedIn | Sees Sentinel mentioned in underwriter group | 🤔 Curious | "How accurate is AI risk assessment?" | Thought leadership: Host webinar with insurance experts |
| **Evaluation** | Demo Call | Sees live demo: Historical anomaly detection | 😮 Impressed | "Would this have predicted past claims?" | Claims analysis: Show Sentinel caught 80% of past exploits |
| **POC** | Trial | Tests on 10 insured protocols | 🧑‍🔬 Experimenting | "How do we integrate this into underwriting workflow?" | Underwriting API: Risk score + recommended premium pricing |

---

### Stage 2: Onboarding

**Scenario:** Insurance protocol subscribes to Enterprise tier ($25K/month, unlimited contracts).

| Phase | Touchpoint | User Action | Emotional State | Pain Point | Opportunity |
|-------|-----------|-------------|-----------------|-----------|-------------|
| **Sign-Up** | Enterprise Contract | Signs annual contract, negotiates custom SLA | 🤝 Committed | "Need 99.95% uptime, insurance payouts depend on this" | Dedicated infrastructure: Isolated tenant, guaranteed capacity |
| **Configuration** | API Integration | Connects Sentinel API to underwriting system | 💻 Technical | "Need to automate: Sentinel risk score → premium pricing" | Actuarial API: Convert anomaly history → loss probability |
| **Training** | Onboarding Call | Trains 5 underwriters on interpreting Sentinel alerts | 📚 Learning | "Underwriters don't understand ML terminology" | Training materials: "ML for Insurance Underwriters" course |
| **Validation** | Historical Analysis | Backtests: Sentinel would've prevented 8 out of 10 past claims | 🎉 Validated | None (proven value) | Case study: "$5M claims prevented with Sentinel" |

---

### Stage 3: Daily Usage

**Scenario:** Insurance protocol monitors 200 insured contracts, adjusts coverage in real-time.

| Phase | Touchpoint | User Action | Emotional State | Pain Point | Opportunity |
|-------|-----------|-------------|-----------------|-----------|-------------|
| **Policy Issuance** | Underwriting System | Issues new policy, auto-adds contract to Sentinel | ☕ Routine | "Need to set coverage limits based on risk score" | Risk-based pricing API: Recommend coverage limits |
| **Real-Time Monitoring** | Slack Alert | Receives "Critical: Insured protocol TVL drop 20%" | 😨 Alarmed | "Should we pause coverage or increase premium?" | Dynamic pricing: Auto-adjust premium based on real-time risk |
| **Claims Validation** | Investigation | Uses Sentinel data to validate claim: "Was this exploit?" | 🕵️ Investigating | "Claimants provide incomplete information" | Claims API: Generate incident report with evidence |
| **Monthly Review** | Dashboard | Reviews: 200 contracts monitored, 5 alerts, 0 false claims | 📊 Satisfied | "Need to prove ROI to board" | ROI report: "Sentinel reduced claims by 40%" |

---

### Stage 4: Advanced Usage

**Scenario:** Insurance protocol builds automated claims processing powered by Sentinel.

| Phase | Touchpoint | User Action | Emotional State | Pain Point | Opportunity |
|-------|-----------|-------------|-----------------|-----------|-------------|
| **Claims Automation** | Smart Contract | Auto-triggers payout if Sentinel confirms exploit | 🤖 Innovative | "Need cryptographic proof of anomaly (for audit trail)" | Signed API responses: Use blockchain attestation |
| **Actuarial Modeling** | Data Export | Exports 2 years of anomaly data for loss modeling | 📊 Analytical | "Need to correlate anomalies with actual exploit losses" | Actuarial dataset: Historical anomalies + exploit outcomes |
| **Product Expansion** | New Product | Launches "Real-Time Coverage" (cheaper, AI-monitored) | 🚀 Launching | "How do we market this vs traditional coverage?" | Co-marketing: "AI-powered insurance by Sentinel" |

---

### Stage 5: Renewal & Expansion

**Scenario:** Insurance protocol renews, expands to cover 500 contracts across 3 chains.

| Phase | Touchpoint | User Action | Emotional State | Pain Point | Opportunity |
|-------|-----------|-------------|-----------------|-----------|-------------|
| **Growth** | Internal Metrics | Reviews: $50M total cover, 500 contracts, 40% claim reduction | 🎉 Celebrating | "Sentinel is critical infrastructure, need 24/7 support" | Dedicated success manager: Monthly strategic review |
| **Renewal** | Enterprise Call | Renews annual contract, negotiates multi-year discount | 🤝 Trusting | "Want to lock in pricing before volume growth" | Multi-year contract: 20% discount for 3-year commitment |
| **Strategic Partnership** | Joint PR | Co-announces: "First AI-Insured DeFi Protocols" | 📣 Excited | None (mutual benefit) | Joint case study: "How AI Reduced Insurance Claims by 40%" |

---

## Cross-Persona Insights

### Common Pain Points (All Personas)

| Pain Point | Personas Affected | Current Solutions (Inadequate) | Sentinel Solution |
|-----------|-------------------|-------------------------------|-------------------|
| **False Positives** | Security Lead, Trader | Rule-based alerts (threshold breaches) | AI anomaly detection with confidence scores |
| **Alert Fatigue** | Security Lead, Trader | Too many alerts, manual triage | Smart prioritization, ML-based severity scoring |
| **Manual Analysis** | All | Manual on-chain investigation (hours) | Claude Code plugin: AI-assisted investigation |
| **No Early Warning** | All | Reactive (detect after exploit starts) | Forecasting: Predict anomalies 1 hour ahead |
| **Lack of Context** | Security Lead, Trader | Alerts lack "why" and "what to do" | Rich context: Compare to historical patterns, suggest actions |
| **Integration Friction** | Analytics Firm, Insurance | Custom integrations take weeks | Pre-built integrations: Slack, API, Snowflake |

### Common Motivations (All Personas)

1. **Risk Reduction**: Prevent financial losses (exploits, portfolio drawdowns, insurance claims)
2. **Efficiency**: Automate manual security/risk workflows
3. **Competitive Advantage**: Use AI to outperform competitors
4. **Compliance**: Provide audit trails, reports for regulators/boards
5. **Trust**: Data-driven decisions > gut instinct

### Emotional Journey (Common Pattern)

```
Discovery:    😰 Anxious (fear of exploits)
              ↓
Evaluation:   🤔 Curious (can AI help?)
              ↓
Onboarding:   😬 Cautious (will this work?)
              ↓
Validation:   😮 Impressed (historical analysis proves value)
              ↓
Daily Use:    😌 Relieved (monitoring is automated)
              ↓
Advanced Use: 🤖 Empowered (building on top of Sentinel)
              ↓
Renewal:      🎉 Validated (clear ROI, delighted)
              ↓
Advocacy:     😎 Evangelist (referring others)
```

**Key Insight:** The emotional shift from "Anxious" to "Evangelist" happens when users see **historical proof** that Sentinel would have prevented past incidents.

---

## Touchpoint Analysis

### Critical Touchpoints (Highest Impact)

| Touchpoint | Stage | Personas | Impact | Current Experience | Desired Experience |
|-----------|-------|----------|--------|-------------------|-------------------|
| **Historical Analysis** | Onboarding | All | 🔥 Very High | Manual: User must analyze past data themselves | Automated: "Sentinel would've caught 8/10 exploits in past 6 months" |
| **First Alert** | Daily Use | All | 🔥 Very High | Generic: "Anomaly detected on contract X" | Rich context: "TVL drop 15% (similar to Balancer exploit Nov 2025)" |
| **False Positive Feedback** | Daily Use | Security Lead, Trader | 🔥 High | No feedback loop: Same false positives repeat | Learning system: "Why was this false positive?" → tune model |
| **ROI Report** | Renewal | All | 🔥 Very High | Manual: User must calculate ROI themselves | Automated: "Sentinel prevented $X losses, saved Y hours" |
| **API Integration** | Onboarding | Analytics Firm, Insurance | 🔥 High | Generic docs: "Read API reference" | Code samples: Python scripts for common use cases |

### Opportunity Touchpoints (Under-Optimized)

1. **Pre-Trial Education**: Many users don't understand anomaly detection before trial
   - **Opportunity**: Create "Anomaly Detection 101" course (10-minute video)

2. **Trial-to-Paid Conversion**: Users end trial without clear value proof
   - **Opportunity**: Auto-generate "Trial Results Report" on last day (how many anomalies caught, estimated value)

3. **Community Building**: No user community for sharing insights
   - **Opportunity**: Discord server, monthly AMAs, user-submitted dashboards

4. **Referral Program**: Delighted customers don't have easy way to refer others
   - **Opportunity**: In-app referral link, $500 credit for referrer + referee

---

## Opportunity Map

### Quick Wins (High Impact, Low Effort)

| Opportunity | Impact | Effort | Personas | Rationale |
|------------|--------|--------|----------|-----------|
| **Historical Analysis Report** | 🔥🔥🔥 | ⚙️ Low | All | Auto-generate "What we would've caught" report in onboarding |
| **Alert Context Enrichment** | 🔥🔥🔥 | ⚙️ Low | Security Lead, Trader | Add "Similar to [past exploit]" to alerts |
| **False Positive Feedback** | 🔥🔥 | ⚙️ Low | Security Lead, Trader | Single-click "Why false?" → improve model |
| **ROI Dashboard** | 🔥🔥🔥 | ⚙️ Medium | All | Auto-calculate: Prevented losses, saved hours |
| **Code Samples** | 🔥🔥 | ⚙️ Low | Analytics Firm, Trader | Python scripts for common integrations |

### Strategic Investments (High Impact, High Effort)

| Opportunity | Impact | Effort | Personas | Timeline |
|------------|--------|--------|----------|----------|
| **Forecasting (1-hour ahead)** | 🔥🔥🔥 | ⚙️⚙️⚙️ High | All | Phase 2 (Months 4-6) |
| **Custom Model Training** | 🔥🔥 | ⚙️⚙️⚙️ High | Security Lead, Analytics Firm | Phase 3 (Months 7-12) |
| **White-Label Solution** | 🔥🔥🔥 | ⚙️⚙️⚙️ High | Analytics Firm | Phase 3 (Months 7-12) |
| **Automated Incident Response** | 🔥🔥 | ⚙️⚙️ Medium | Security Lead, Insurance | Phase 2 (Months 4-6) |
| **Self-Hosted Deployment** | 🔥 | ⚙️⚙️⚙️ High | Analytics Firm, Insurance | Phase 3 (Months 7-12) |

### Innovation Bets (High Risk, High Reward)

| Opportunity | Impact | Risk | Personas | Rationale |
|------------|--------|------|----------|-----------|
| **AI Security Assistant (Claude Code Plugin)** | 🔥🔥🔥 | 🎲🎲 Medium | Security Lead | Developer-focused distribution channel |
| **Exploit Signature Library** | 🔥🔥 | 🎲🎲 Medium | All | "This looks like Balancer exploit" pattern matching |
| **Dynamic Insurance Pricing** | 🔥🔥 | 🎲🎲🎲 High | Insurance | Regulatory uncertainty, complex actuarial modeling |
| **MEV Attack Detection** | 🔥🔥 | 🎲🎲 Medium | Security Lead, Trader | MEV is different attack vector, requires different models |

---

## Conclusion

### Key Findings

1. **All personas share a common pain**: Manual security/risk analysis is time-consuming and reactive (not predictive)

2. **The "Aha!" moment**: When users see historical analysis showing "Sentinel would've caught past exploits" → instant value proof

3. **False positives are the #1 daily pain point**: Must build feedback loops to improve accuracy over time

4. **Advanced users want to build on top**: API-first architecture is critical for Analytics Firms and power users

5. **ROI must be quantified**: Auto-generate ROI reports showing prevented losses + time saved

### Recommended Product Priorities (Based on Journey Analysis)

**Phase 1 (MVP - Months 1-3):**
1. ✅ Basic anomaly detection (TimeGPT + StatsForecast)
2. ✅ Historical analysis report (auto-generated in onboarding)
3. ✅ Alert context enrichment (compare to past patterns)
4. ✅ Claude Code plugin (AI security assistant)

**Phase 2 (Production - Months 4-6):**
5. Forecasting (1-hour ahead early warnings)
6. False positive feedback loop (ML model improvement)
7. ROI dashboard (auto-calculate prevented losses)
8. Automated incident response (webhook integrations)

**Phase 3 (Scale - Months 7-12):**
9. Custom model training (fine-tune TimeGPT with customer data)
10. White-label solution (for Analytics Firms)
11. Self-hosted deployment (for enterprise customers)
12. Exploit signature library (pattern matching)

---

**Prepared by:** Intent Solutions
**For:** Nixtla (Max Mergenthaler)
**Date:** 2025-12-02
**Version:** 1.0
