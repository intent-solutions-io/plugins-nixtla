# Nixtla DeFi Sentinel - Product Requirements Document

**Plugin ID:** nixtla-defi-sentinel
**Version:** 1.0
**Created:** 2025-12-01
**Owner:** Intent Solutions
**Status:** Specified

---

## Overview

Nixtla DeFi Sentinel is a Claude Code plugin that provides AI-powered security monitoring for DeFi smart contracts using Nixtla's time-series forecasting and anomaly detection capabilities. It monitors blockchain metrics in real-time, detects anomalous behavior, and alerts users to potential exploits before they occur.

**Core Value Proposition:**
- **For DeFi protocols:** Continuous AI monitoring that detects exploits before attackers do
- **Using Nixtla's proven models:** TimeGPT anomaly detection + StatsForecast baselines
- **Unlike manual audits:** Real-time, adaptive, and cost-effective ($50/contract/month vs $200K/year security team)

---

## Goals & Success Criteria

### Primary Goals

| Goal | Success Metric | Target |
|------|---------------|--------|
| **G1:** Detect pre-exploit anomalies | True positive rate on historical exploits | >70% |
| **G2:** Minimize false alarms | False positive rate | <5% |
| **G3:** Achieve real-time performance | Alert latency from anomaly occurrence | <30 seconds |
| **G4:** Validate market demand | Plugin-to-paid conversion rate | >10% |
| **G5:** Drive TimeGPT API adoption | % of users adopting TimeGPT for production | >30% |

### Secondary Goals

| Goal | Success Metric | Target |
|------|---------------|--------|
| **G6:** Build DeFi credibility | Case studies of prevented exploits | 3+ in Year 1 |
| **G7:** Expand Nixtla's market | Revenue from DeFi segment | $100K+ ARR |
| **G8:** Enable self-service | Users onboard without sales calls | >60% |

---

## Non-Goals

### Explicitly Out of Scope

1. **❌ Smart contract auditing:** We detect runtime anomalies, not pre-deployment code review
2. **❌ Automated remediation:** We alert humans; we don't auto-patch contracts
3. **❌ Social engineering detection:** Only on-chain/code vulnerabilities
4. **❌ CEX (centralized exchange) monitoring:** DeFi protocols only (Phase 1)
5. **❌ Historical forensics:** Real-time monitoring only, not post-mortem analysis
6. **❌ Multi-chain bridge monitoring:** Single-chain focus initially
7. **❌ Gas optimization:** Security monitoring, not performance tuning

### Why These Are Non-Goals

- **Auditing:** Different skillset, competitive with partners (CertiK, Trail of Bits)
- **Auto-remediation:** Too risky; humans must approve contract changes
- **CEX monitoring:** Different data sources, regulatory complexity
- **Historical forensics:** Crowded market (Chainalysis, Elliptic)

---

## User Stories

### Primary User: DeFi Protocol Security Lead

| ID | User Story | Acceptance Criteria |
|----|------------|-------------------|
| **US-1** | As a security lead, I want to monitor my protocol's smart contracts for anomalies so I can detect exploits early | - Contracts added to monitoring in <5 min<br>- Anomaly alerts via Slack/Discord/Email<br>- Visual dashboard showing contract health |
| **US-2** | As a security lead, I want to set custom alert thresholds so I can balance false positives vs detection rate | - Adjustable sensitivity (Low/Med/High)<br>- Threshold customization per metric<br>- A/B test different configurations |
| **US-3** | As a security lead, I want to understand why an alert fired so I can assess if it's a real threat | - Alert includes anomaly score<br>- Historical baseline comparison<br>- Suggested next steps |
| **US-4** | As a security lead, I want to test the system against historical exploits so I can validate its effectiveness | - Simulate mode with historical data<br>- Report showing detection rate<br>- Benchmark against known exploits |

### Secondary User: DeFi Protocol Developer

| ID | User Story | Acceptance Criteria |
|----|------------|-------------------|
| **US-5** | As a developer, I want to pre-launch test my contracts so I can find vulnerabilities before mainnet deployment | - Test mode using forked blockchain<br>- Report of detected issues<br>- Integration with CI/CD pipeline |
| **US-6** | As a developer, I want to see forecasts of my contract's expected behavior so I can validate my logic | - Time-series predictions for TVL, tx volume<br>- Confidence intervals<br>- Comparison to similar contracts |

### Tertiary User: Institutional Crypto Investor

| ID | User Story | Acceptance Criteria |
|----|------------|-------------------|
| **US-7** | As an investor, I want to monitor protocols where I have deposits so I can withdraw before exploits occur | - Multi-protocol portfolio view<br>- Risk score per protocol<br>- Emergency exit recommendations |

---

## Functional Requirements

### FR-1: Contract Monitoring

| ID | Requirement | Priority |
|----|-------------|----------|
| **FR-1.1** | System SHALL ingest on-chain data from Ethereum, BSC, and Base blockchains | P0 (Must Have) |
| **FR-1.2** | System SHALL monitor these metrics per contract:<br>- TVL (Total Value Locked)<br>- Transaction volume/frequency<br>- Gas usage<br>- Token balance changes<br>- Function call patterns<br>- Event emission patterns | P0 (Must Have) |
| **FR-1.3** | System SHALL refresh data every 12 seconds (1 block time) | P0 (Must Have) |
| **FR-1.4** | System SHALL support monitoring up to 100 contracts per user | P1 (Should Have) |
| **FR-1.5** | System SHALL persist 90 days of historical data per contract | P1 (Should Have) |

### FR-2: Anomaly Detection

| ID | Requirement | Priority |
|----|-------------|----------|
| **FR-2.1** | System SHALL use Nixtla TimeGPT API for anomaly detection on all monitored metrics | P0 (Must Have) |
| **FR-2.2** | System SHALL use StatsForecast models as fallback when TimeGPT is unavailable | P0 (Must Have) |
| **FR-2.3** | System SHALL detect these anomaly types:<br>- Sudden TVL drops (>10% in 1 block)<br>- Transaction volume spikes (>3 std dev)<br>- Unusual gas consumption patterns<br>- Abnormal function call sequences<br>- Large transfers to new addresses | P0 (Must Have) |
| **FR-2.4** | System SHALL assign anomaly severity (Low/Medium/High/Critical) | P0 (Must Have) |
| **FR-2.5** | System SHALL learn baseline behavior per contract (7-day training window) | P1 (Should Have) |
| **FR-2.6** | System SHALL support custom anomaly rules (e.g., "alert if >$1M transfer") | P2 (Nice to Have) |

### FR-3: Alerting

| ID | Requirement | Priority |
|----|-------------|----------|
| **FR-3.1** | System SHALL send alerts via:<br>- Slack webhook<br>- Discord webhook<br>- Email<br>- SMS (Twilio) | P0 (Must Have) |
| **FR-3.2** | System SHALL include in each alert:<br>- Contract address<br>- Anomaly type and severity<br>- Metric values (expected vs actual)<br>- Timestamp<br>- Blockchain explorer link | P0 (Must Have) |
| **FR-3.3** | System SHALL support alert routing rules (e.g., "Critical → SMS, Low → Email") | P1 (Should Have) |
| **FR-3.4** | System SHALL rate-limit alerts (max 1 per contract per 5 minutes) to prevent spam | P0 (Must Have) |
| **FR-3.5** | System SHALL support alert suppression/snooze (1hr, 8hr, 24hr) | P2 (Nice to Have) |

### FR-4: Dashboard & Visualization

| ID | Requirement | Priority |
|----|-------------|----------|
| **FR-4.1** | System SHALL provide web dashboard showing:<br>- List of monitored contracts<br>- Real-time health status per contract<br>- Recent alerts feed<br>- Time-series charts for key metrics | P1 (Should Have) |
| **FR-4.2** | System SHALL show forecast predictions (next 24hr) for TVL and transaction volume | P2 (Nice to Have) |
| **FR-4.3** | System SHALL allow historical playback (scrub timeline to see past anomalies) | P2 (Nice to Have) |

### FR-5: Claude Code Plugin Integration

| ID | Requirement | Priority |
|----|-------------|----------|
| **FR-5.1** | Plugin SHALL implement MCP server exposing tools:<br>- `monitor_contract(address, chain)`<br>- `get_contract_status(address)`<br>- `list_monitored_contracts()`<br>- `get_recent_alerts(limit)`<br>- `forecast_contract_metrics(address, horizon)` | P0 (Must Have) |
| **FR-5.2** | Plugin SHALL provide slash command: `/nixtla-defi-sentinel` | P0 (Must Have) |
| **FR-5.3** | Plugin SHALL include AI skill for interpreting anomalies (plain-English explanations) | P1 (Should Have) |
| **FR-5.4** | Plugin SHALL generate incident reports (markdown format) | P1 (Should Have) |

### FR-6: Configuration & Setup

| ID | Requirement | Priority |
|----|-------------|----------|
| **FR-6.1** | System SHALL require only contract address + chain to start monitoring | P0 (Must Have) |
| **FR-6.2** | System SHALL auto-detect contract type (ERC-20, ERC-721, DEX, lending, etc.) | P1 (Should Have) |
| **FR-6.3** | System SHALL support `.env` configuration for API keys and webhook URLs | P0 (Must Have) |
| **FR-6.4** | System SHALL provide guided setup wizard in Claude Code | P1 (Should Have) |

---

## Non-Functional Requirements

### NFR-1: Performance

| ID | Requirement | Target |
|----|------------|--------|
| **NFR-1.1** | Anomaly detection latency | <30 seconds from on-chain event |
| **NFR-1.2** | Alert delivery latency | <5 seconds after anomaly detected |
| **NFR-1.3** | Dashboard load time | <2 seconds initial load |
| **NFR-1.4** | API response time (p95) | <500ms |
| **NFR-1.5** | System uptime | 99.5% (43.8 hours downtime/year) |

### NFR-2: Scalability

| ID | Requirement | Target |
|----|------------|--------|
| **NFR-2.1** | Concurrent users supported | 1,000 users |
| **NFR-2.2** | Contracts monitored (system-wide) | 10,000 contracts |
| **NFR-2.3** | Events processed per second | 1,000 events/sec |
| **NFR-2.4** | Data retention | 90 days (10TB estimated) |

### NFR-3: Reliability

| ID | Requirement | Target |
|----|------------|--------|
| **NFR-3.1** | False positive rate | <5% |
| **NFR-3.2** | True positive rate (on historical exploits) | >70% |
| **NFR-3.3** | Alert delivery success rate | >99% |
| **NFR-3.4** | Data accuracy (vs on-chain source) | 100% |

### NFR-4: Security & Privacy

| ID | Requirement | Target |
|----|------------|--------|
| **NFR-4.1** | API keys encrypted at rest | AES-256 |
| **NFR-4.2** | Webhook URLs not logged | Redacted in logs |
| **NFR-4.3** | User data isolated (multi-tenant) | Per-user database namespacing |
| **NFR-4.4** | SOC 2 Type II compliance | Within 12 months |

### NFR-5: Usability

| ID | Requirement | Target |
|----|------------|--------|
| **NFR-5.1** | Time to first monitored contract | <5 minutes |
| **NFR-5.2** | Setup steps required | <5 steps |
| **NFR-5.3** | Documentation completeness | 100% API coverage |
| **NFR-5.4** | Support response time | <4 hours (business hours) |

---

## Success Metrics & KPIs

### Product Metrics

| Metric | Target (3 months) | Target (6 months) | Target (12 months) |
|--------|-------------------|-------------------|-------------------|
| **Adoption** | | | |
| Plugin installs | 100 | 500 | 2,000 |
| Active users (MAU) | 20 | 100 | 500 |
| Monitored contracts | 50 | 300 | 1,500 |
| **Engagement** | | | |
| Daily active users | 10 | 50 | 200 |
| Alerts sent | 500 | 3,000 | 15,000 |
| Dashboard sessions/user/week | 3 | 5 | 7 |
| **Quality** | | | |
| True positive rate | 60% | 70% | 80% |
| False positive rate | <10% | <5% | <3% |
| Alert response time | <60s | <30s | <15s |

### Business Metrics

| Metric | Target (3 months) | Target (6 months) | Target (12 months) |
|--------|-------------------|-------------------|-------------------|
| **Revenue** | | | |
| Paying customers | 3 | 10 | 25 |
| MRR | $10K | $50K | $150K |
| ARR | - | $600K | $1.8M |
| Plugin-to-paid conversion | 5% | 10% | 15% |
| **Market Validation** | | | |
| Customer testimonials | 2 | 5 | 10 |
| Case studies published | 1 | 2 | 5 |
| Prevented exploits (documented) | 0 | 1 | 3 |
| **Strategic** | | | |
| TimeGPT API adoption rate | 20% | 30% | 40% |
| Enterprise customers (>$50K/yr) | 0 | 1 | 3 |

---

## Scope & Phasing

### Phase 1: MVP (Months 1-3) - "Prove It Works"

**Goal:** Validate technical feasibility and market demand

**In Scope:**
- ✅ Monitor Ethereum + BSC only
- ✅ Basic anomaly detection (TVL, tx volume)
- ✅ Slack/Email alerts
- ✅ Claude Code plugin (MCP server)
- ✅ 10 contracts per user limit
- ✅ StatsForecast models only (no TimeGPT yet)

**Success Criteria:**
- 50+ plugin installs
- 70%+ true positive rate on historical exploits
- 3+ paying pilot customers

### Phase 2: Production (Months 4-6) - "Make It Reliable"

**Goal:** Production-ready for paying customers

**In Scope:**
- ✅ TimeGPT API integration
- ✅ Base blockchain support
- ✅ Web dashboard
- ✅ Advanced anomaly types (gas, function calls)
- ✅ Custom alert rules
- ✅ 100 contracts per user limit
- ✅ Discord/SMS alerts

**Success Criteria:**
- 99% uptime
- <5% false positive rate
- 10+ paying customers
- $50K+ MRR

### Phase 3: Scale (Months 7-12) - "Expand Market"

**Goal:** Market leader in DeFi AI security

**In Scope:**
- ✅ Multi-chain (Polygon, Arbitrum, Optimism)
- ✅ Forecast predictions (24hr horizon)
- ✅ Historical playback
- ✅ Custom ML models per customer
- ✅ White-label offering
- ✅ API for external integrations

**Success Criteria:**
- 20+ paying customers
- $100K+ MRR
- Top 10 DeFi protocol as customer
- 3+ documented prevented exploits

---

## Open Questions

### Technical Questions

| ID | Question | Decision Needed | Blocker For |
|----|----------|----------------|-------------|
| **Q1** | Which blockchain node provider? (Alchemy, Infura, QuickNode) | Week 1 | FR-1.1 |
| **Q2** | TimeGPT rate limits sufficient for real-time monitoring? | Week 1 | FR-2.1 |
| **Q3** | Use local StatsForecast or hosted? | Week 2 | FR-2.2 |
| **Q4** | Database: PostgreSQL vs TimescaleDB vs InfluxDB? | Week 2 | FR-1.5 |
| **Q5** | Self-hosted or Cloud Run/Lambda for processing? | Week 2 | NFR-2.2 |

### Product Questions

| ID | Question | Decision Needed | Blocker For |
|----|----------|----------------|-------------|
| **Q6** | Free tier limits? (contracts, alerts, data retention) | Month 1 | Pricing |
| **Q7** | Default alert sensitivity? (optimize for low FP or high recall?) | Month 1 | FR-2.4 |
| **Q8** | Should we support private/non-verified contracts? | Month 2 | FR-6.2 |
| **Q9** | Incident response consulting service? (upsell opportunity) | Month 3 | Revenue model |

### Business Questions

| ID | Question | Decision Needed | Blocker For |
|----|----------|----------------|-------------|
| **Q10** | Partner with existing audit firms or compete? | Month 1 | Go-to-market |
| **Q11** | White-label offering for enterprises? | Month 3 | Enterprise strategy |
| **Q12** | Open source any components? | Month 2 | Community building |

---

## Dependencies

### Internal Dependencies

| Dependency | Owner | Status | Risk |
|------------|-------|--------|------|
| TimeGPT anomaly detection API access | Nixtla Engineering | Available | Low |
| StatsForecast library updates | Nixtla OSS team | Ongoing | Low |
| Nixtla branding/logo approval | Nixtla Marketing | Needed | Low |
| TimeGPT pricing for high-volume use | Nixtla Sales | TBD | Medium |

### External Dependencies

| Dependency | Provider | Status | Risk |
|------------|----------|--------|------|
| Blockchain node access | Alchemy/Infura | Available | Low |
| Web3.py library | Open source | Stable | Low |
| Claude Code MCP protocol | Anthropic | Stable | Low |
| Smart contract ABI parsing | etherscan API | Available | Low |

---

## Assumptions

### Technical Assumptions

1. **Blockchain data availability:** Historical data available via node providers (7+ days)
2. **Model performance:** TimeGPT anomaly detection works on blockchain metrics (needs validation)
3. **Latency acceptable:** 30-second detection latency acceptable for most exploits
4. **Rate limits sufficient:** Nixtla API rate limits support 1000+ contracts monitored
5. **Data quality:** On-chain data accurate enough for modeling (no missing blocks)

### Market Assumptions

1. **DeFi protocols willing to pay:** $1K-10K/month budget for security monitoring
2. **Claude Code adoption:** Developers using Claude Code for smart contract work
3. **Urgency exists:** SCONE-bench creates buying urgency in next 6 months
4. **Trust in AI:** Customers trust AI anomaly detection vs manual monitoring
5. **No major competitor launch:** 6-month window before well-funded competitors

### Business Assumptions

1. **Plugin-to-paid conversion:** 10% of plugin users convert to paid
2. **Customer acquisition cost:** <$5K per customer (mostly inbound)
3. **Churn rate:** <20% annual churn (high switching cost)
4. **Sales cycle:** <30 days (bottoms-up adoption)
5. **TimeGPT upsell:** 30% of customers upgrade to TimeGPT API

---

## Appendix

### Related Documents

- [01-BUSINESS-CASE.md](01-BUSINESS-CASE.md) - Market opportunity and ROI
- [03-ARCHITECTURE.md](03-ARCHITECTURE.md) - System design
- [04-USER-JOURNEY.md](04-USER-JOURNEY.md) - User experience flow
- [05-TECHNICAL-SPEC.md](05-TECHNICAL-SPEC.md) - Implementation details
- [06-STATUS.md](06-STATUS.md) - Current development status

### References

- [Anthropic SCONE-bench Research](https://red.anthropic.com/2025/smart-contracts/)
- [Nixtla TimeGPT Anomaly Detection Docs](https://docs.nixtla.io/timegpt)
- [Nixtla StatsForecast Documentation](https://nixtla.github.io/statsforecast/)
- [DeFi Security Best Practices](https://consensys.github.io/smart-contract-best-practices/)

---

**Document Version:** 1.0
**Last Updated:** 2025-12-01
**Next Review:** 2025-12-15
**Status:** ✅ Ready for Architecture Phase
