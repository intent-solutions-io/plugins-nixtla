# Planned Skills Directory

This directory contains specifications for **future Claude Skills** that are planned but not yet implemented.

## Current Status

**Implemented Skills**: 8 (in `skills-pack/.claude/skills/`)
- nixtla-timegpt-lab
- nixtla-experiment-architect
- nixtla-schema-mapper
- nixtla-timegpt-finetune-lab
- nixtla-prod-pipeline-generator
- nixtla-usage-optimizer
- nixtla-skills-bootstrap
- nixtla-skills-index

**Planned Skills**: 0 (this directory is empty - ready for new skill specs)

---

## How to Add a Planned Skill

When planning a new skill, create a folder here with the skill specification:

```
planned-skills/
└── nixtla-<skill-name>/
    ├── SPEC.md                  # Skill specification
    ├── SKILL.md.draft           # Draft SKILL.md (following 041-SPEC standard)
    └── examples/                # Example use cases
```

### Skill Specification Template

```markdown
# Nixtla <Skill Name> - Specification

**Type**: [Mode | Utility | Infrastructure]
**Status**: Planned
**Priority**: [High | Medium | Low]
**Target Release**: vX.Y.Z

## Purpose

What does this skill do? (1-2 sentences)

## Use Cases

- Use case 1
- Use case 2
- Use case 3

## Skill Metadata

**Name**: `nixtla-<short-name>`
**Description**: Action-oriented description with when-to-use context
**Allowed Tools**: "Read,Write,Glob,Grep,Edit" (minimal set)
**Mode**: true/false

## Instructions (High-Level)

1. Step 1
2. Step 2
3. Step 3

## Output

What artifacts does this skill produce?

## Dependencies

- Required tools
- Required APIs
- Required environment variables

## Success Criteria

How do we know this skill is working correctly?

## References

- Related plugins
- Related skills
- External documentation
```

---

## Skill Ideas (To Be Specified)

### Prediction Markets Vertical

1. **nixtla-polymarket-analyst** (Mode)
   - Transform Claude into prediction market analyst
   - Analyze Polymarket/Kalshi contracts with TimeGPT

2. **nixtla-arbitrage-detector** (Mode)
   - Identify mispriced contracts across venues
   - Use TimeGPT anomaly detection

3. **nixtla-contract-schema-mapper** (Utility)
   - Map prediction market data to TimeGPT schema
   - Support Polymarket, Kalshi, PredictIt APIs

4. **nixtla-event-impact-modeler** (Utility)
   - Model exogenous event impact on contract prices
   - Integrate polling, economic, legal data

5. **nixtla-liquidity-forecaster** (Utility)
   - Forecast orderbook depth and spreads
   - Optimize execution timing

6. **nixtla-correlation-mapper** (Utility)
   - Analyze multi-contract correlations
   - Generate hedge recommendations

7. **nixtla-market-risk-analyzer** (Utility)
   - Calculate VaR, volatility, drawdown
   - Position sizing recommendations

### General Forecasting

8. **nixtla-batch-forecaster** (Utility)
   - Run forecasts on multiple series in parallel
   - Batch API optimization

9. **nixtla-model-selector** (Utility)
   - Auto-select best model for dataset
   - Compare StatsForecast vs TimeGPT

10. **nixtla-forecast-validator** (Utility)
    - Validate forecast quality metrics
    - Detect forecast degradation

---

## Adding Skills from Ideas

To move a skill from "Ideas" to active specification:

1. Create folder: `mkdir planned-skills/nixtla-<skill-name>`
2. Write `SPEC.md` using template above
3. Draft `SKILL.md.draft` following `041-SPEC-nixtla-skill-standard.md`
4. Add examples in `examples/`
5. Update this README with status

---

## Related Documentation

- **Skill Standard**: `041-SPEC-nixtla-skill-standard.md`
- **Skills Architecture**: `038-AT-ARCH-nixtla-claude-skills-pack.md`
- **Implemented Skills**: `skills-pack/.claude/skills/`

---

**Last Updated**: 2025-12-05
**Version**: 1.2.0
