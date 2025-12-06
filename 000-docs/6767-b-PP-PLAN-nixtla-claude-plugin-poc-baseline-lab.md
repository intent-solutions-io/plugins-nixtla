---
doc_id: 6767-PP-PLAN-nixtla-claude-plugin-poc-baseline-lab
title: Nixtla Claude Code Plugin PoC - Baseline Lab
category: Planning & Product
status: PLANNING
classification: Canonical Cross-Repo Standard
owner: Jeremy Longshore
collaborators:
  - Max Mergenthaler (Nixtla)
last_updated: 2025-11-24
repository: claude-code-plugins-nixtla
related_docs:
  - 6767-OD-ARCH-nixtla-claude-plugin-poc-baseline-lab.md
  - 001-PP-PROD-nixtla-integration-requirements.md
  - 004-AT-ARCH-plugin-architecture.md
---

# 6767-PP-PLAN: Nixtla Claude Code Plugin PoC - Baseline Lab

**Document Classification**: Canonical Cross-Repo Planning Standard
**Owner**: Jeremy Longshore (Intent Solutions)
**Status**: PLANNING
**Last Updated**: 2025-11-24

---

## I. Executive Summary

This document defines the **Proof of Concept (PoC)** for the first Nixtla Claude Code plugin: **Nixtla Baseline Lab**. The PoC demonstrates a complete, locally testable plugin that:

- Integrates Nixtla time series forecasting workflows into Claude Code
- Showcases all major plugin components: commands, agents, skills, and MCP servers
- Uses public benchmark datasets (M4, ETTh1, etc.) for testing
- Establishes patterns for future Nixtla agent development

**Core Value Proposition**: Enable Nixtla engineers and researchers to generate baseline forecasts on benchmark datasets directly from Claude Code conversations, with automated analysis and interpretation.

**Technical Approach**: Build a minimal but complete plugin following Bob's Brain architecture principles—orchestrator patterns, golden tasks, CI-only guardrails—adapted for time series forecasting workflows.

---

## II. Goals & Non-Goals

### Goals (MUST Achieve)

1. **Demonstrate Full Plugin Architecture**
   - One slash command (`/nixtla-baseline-m4`)
   - One subagent (`nixtla-baseline-analyst`)
   - One skill (`NixtlaBaselineReview`)
   - One MCP server/tool (`nixtla-baseline-mcp` with `run_baselines`)

2. **Local Testing First**
   - Zero external dependencies during initial development
   - 100% locally reproducible without API keys
   - Clear debugging and validation workflows

3. **Public Data Only**
   - Use M4 Daily dataset (or similar from `datasetsforecast`)
   - No customer data, no production systems
   - Educational and demonstrative focus

4. **Production Patterns**
   - Follow Bob's Brain architectural principles
   - Document everything with 6767 standards
   - Prepare for future scale (multi-agent, CI integration)

5. **Validation & Quality**
   - Golden task framework for testing
   - Clear success criteria
   - Reproducible results

### Non-Goals (Explicitly OUT of Scope)

1. **Production Deployment**
   - Not deploying to Claude Code marketplace yet
   - Not integrating with Nixtla customer environments
   - Not touching production TimeGPT infrastructure

2. **Complex Multi-Agent Orchestration**
   - No orchestrator agent in PoC
   - No cross-agent communication protocols (A2A deferred)
   - Single plugin, single workflow focus

3. **Full Nixtlaverse Coverage**
   - Not covering all libraries (StatsForecast, MLForecast, NeuralForecast, Hierarchical, etc.)
   - Focus on baseline patterns only
   - Extensibility documented, not implemented

4. **UI/UX Polish**
   - Terminal-based interaction only
   - Minimal formatting and visualizations
   - Functionality over aesthetics

---

## III. PoC Scope

### Plugin: `nixtla-baseline-lab`

**Purpose**: Run Nixtla-style baseline forecasting models on public benchmark datasets from inside Claude Code conversations.

### Components

#### 1. Slash Command: `/nixtla-baseline-m4`
- **What it does**: Runs baseline forecasting models (SeasonalNaive, ETS, Theta) on M4 Daily dataset
- **Parameters**:
  - `horizon` (optional, default: 14): Forecast horizon
  - `series_limit` (optional, default: 50): Number of series to sample
- **Output**:
  - Metrics CSV file (`results_M4_Daily_h14.csv`)
  - Summary notebook (`.ipynb` format)
  - Console summary with top models

#### 2. Subagent: `nixtla-baseline-analyst`
- **What it does**: Analyzes baseline forecasting results and provides expert interpretation
- **When invoked**: After `/nixtla-baseline-m4` completes, or when user asks questions about results
- **Capabilities**:
  - Reads metrics tables
  - Compares model performance
  - Identifies patterns (seasonality, trend handling)
  - Recommends next steps

#### 3. Skill: `NixtlaBaselineReview`
- **What it does**: Model-invoked capability for interpreting baseline results
- **Trigger phrases**: User asks about baseline metrics, model comparisons, performance analysis
- **Inputs**: Metrics CSV, summary statistics
- **Outputs**: Natural language explanations, performance rankings, insights

#### 4. MCP Server/Tool: `nixtla-baseline-mcp`
- **Server**: Local Python MCP server bundled with plugin
- **Tool**: `run_baselines` - Executes baseline forecasting workflow
- **Implementation**: Python script with placeholder/stub logic initially
- **Future**: Will integrate actual Nixtla libraries (statsforecast, etc.)

### Data Strategy

**Phase 1 (PoC)**: Stub/Placeholder
- Generate synthetic metrics tables
- Simulate baseline model runs
- Focus on workflow validation

**Phase 2 (Future)**: Real Nixtla Integration
- Load M4 from `datasetsforecast`
- Run actual StatsForecast models (SeasonalNaive, AutoETS, AutoTheta)
- Generate real metrics and visualizations

---

## IV. Architecture Overview (High-Level)

### Component Interaction Flow

```
User → /nixtla-baseline-m4 command
  ↓
Command invokes nixtla-baseline-mcp tool (run_baselines)
  ↓
MCP server executes Python script
  ↓
Script generates metrics CSV + notebook
  ↓
Command returns summary + file paths
  ↓
User asks: "Which model performed best?"
  ↓
Claude invokes NixtlaBaselineReview skill
  ↓
Skill loads metrics, analyzes, explains
  ↓
User decides next steps
```

### Directory Structure

The plugin is located at `plugins/nixtla-baseline-lab/`:

```
plugins/nixtla-baseline-lab/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
├── commands/
│   └── nixtla-baseline-m4.md    # Slash command definition
├── agents/
│   └── nixtla-baseline-analyst.md  # Subagent prompt
├── skills/
│   └── nixtla-baseline-review/
│       ├── SKILL.md             # Skill definition
│       ├── references/
│       │   └── baseline_metrics_guide.md
│       └── scripts/
│           └── analyze_metrics.py
├── .mcp.json                    # MCP server configuration
├── scripts/
│   └── nixtla_baseline_mcp.py   # MCP server implementation
└── README.md                    # Plugin documentation
```

---

## V. Local Testing Strategy (High-Level)

### Phase 1: Skeleton Validation
**Goal**: Verify plugin loads and components are discoverable

1. Enable plugin in Claude Code
2. Verify `claude --debug` shows plugin registered
3. Check `/nixtla-baseline-m4` appears in command list
4. Confirm MCP server starts without errors

**Success Criteria**:
- Plugin shows in `claude plugins list`
- No errors in debug logs
- MCP server process spawns

### Phase 2: Stub Execution
**Goal**: Command executes and produces output

1. Run `/nixtla-baseline-m4` with default parameters
2. Verify stub script executes
3. Check output files created in expected location
4. Validate metrics CSV has expected structure

**Success Criteria**:
- Command completes without errors
- Files exist: `nixtla_baseline_m4/results_M4_Daily_h14.csv`
- CSV has columns: `series_id`, `model`, `sMAPE`, `MASE`

### Phase 3: Skill Invocation
**Goal**: Skill activates and interprets results

1. After running command, ask: "Which baseline model performed best?"
2. Verify skill activates (check logs for skill invocation)
3. Review explanation quality
4. Test multiple question types

**Success Criteria**:
- Skill invokes automatically
- Reads metrics file correctly
- Provides coherent analysis
- Handles edge cases (missing files, invalid data)

### Phase 4: Agent Integration
**Goal**: Subagent provides deeper analysis

1. Explicitly invoke: "Use nixtla-baseline-analyst to analyze these results"
2. Verify agent loads and executes
3. Check for tool usage (Read, Grep for finding files)
4. Validate comprehensive analysis output

**Success Criteria**:
- Agent activates on explicit request
- Correctly identifies result files
- Produces structured analysis report
- Recommends actionable next steps

---

## VI. Phase Plan

### Phase 1: Skeleton Plugin + 6767 Docs ✅
**Duration**: 1 day
**Deliverables**:
- [x] 6767-PP-PLAN document (this file)
- [x] 6767-OD-ARCH document (architecture)
- [ ] Plugin skeleton with all directories
- [ ] Placeholder plugin.json, .mcp.json, command, agent, skill

**Validation**: Documentation reviewed by Max, structure approved

---

### Phase 2: Implement Baseline Command + MCP Tool Stub
**Duration**: 2-3 days
**Deliverables**:
- [ ] Working `/nixtla-baseline-m4` command
- [ ] MCP server with `run_baselines` tool (stub implementation)
- [ ] Output files: metrics CSV, notebook (minimal)
- [ ] Local testing script
- [ ] Golden task: baseline command execution

**Validation**: Command runs locally, produces valid output files

---

### Phase 3: Add Skill and Subagent
**Duration**: 2-3 days
**Deliverables**:
- [ ] NixtlaBaselineReview skill with SKILL.md
- [ ] Supporting scripts in skills/nixtla-baseline-review/scripts/
- [ ] nixtla-baseline-analyst agent prompt
- [ ] Test cases for skill invocation
- [ ] Golden task: skill interpretation

**Validation**: Skill activates on relevant queries, agent provides analysis

---

### Phase 4: Enrich with Nixtla Baseline Logic
**Duration**: 3-5 days
**Deliverables**:
- [ ] Replace stub with real statsforecast integration
- [ ] Load actual M4 Daily dataset
- [ ] Run SeasonalNaive, AutoETS, AutoTheta
- [ ] Generate real metrics (sMAPE, MASE)
- [ ] Create notebook with visualizations
- [ ] Comprehensive test suite

**Validation**: Real Nixtla models run, metrics match expected ranges

---

### Phase 5: Documentation & Handoff (Future)
**Duration**: 2 days
**Deliverables**:
- [ ] User guide for plugin
- [ ] Developer guide for extending
- [ ] Video walkthrough
- [ ] Handoff to Max and Nixtla team

**Validation**: External user can run plugin successfully

---

## VII. Success Metrics

### Technical Metrics
- **Plugin Load Time**: < 500ms
- **Command Execution Time**: < 30 seconds (stub), < 2 minutes (real models)
- **Skill Activation Accuracy**: > 90% on test queries
- **Test Coverage**: > 80% for MCP tool, 100% for golden tasks

### Quality Metrics
- **Documentation Completeness**: All 6767 docs complete, reviewed
- **Local Reproducibility**: 100% success rate on fresh environment
- **Error Handling**: Graceful degradation, clear error messages
- **Code Quality**: Passes linting (black, flake8), type checking (mypy)

### User Experience Metrics
- **Command Discoverability**: Appears in command autocomplete
- **Skill Relevance**: Activates on appropriate queries
- **Agent Value**: Provides insights beyond basic metrics display

---

## VIII. Risk Assessment

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| MCP server doesn't start | Medium | High | Extensive local testing, fallback to direct script execution |
| Skill doesn't activate | Medium | Medium | Clear description writing, test with multiple phrasings |
| Performance issues with real models | Low | Medium | Start with small dataset samples, add timeout handling |
| Claude Code API changes | Low | High | Pin to stable version, monitor release notes |

### Process Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Scope creep | Medium | Medium | Strict adherence to non-goals, phase gating |
| Documentation drift | Low | Medium | 6767 docs as source of truth, update with code changes |
| Testing gaps | Medium | High | Golden tasks framework, mandatory test coverage |

---

## IX. Future Extensions (Post-PoC)

After PoC validation, this plugin can expand to:

1. **Multi-Dataset Support**
   - M4 Monthly, Quarterly, Yearly
   - ETTh1, ETTm1 (electricity)
   - Tourism, Traffic datasets

2. **More Nixtla Libraries**
   - MLForecast with LightGBM/XGBoost
   - NeuralForecast with NBEATS/NHITS
   - HierarchicalForecast with reconciliation

3. **Advanced Features**
   - Cross-validation workflows
   - Hyperparameter tuning
   - Ensemble methods
   - Custom dataset upload

4. **Bob's Brain Integration**
   - Orchestrator agent coordination
   - A2A protocol for agent communication
   - CI integration for automated testing
   - Slack notifications for results

5. **Marketplace Release**
   - Polish UX and documentation
   - Security review
   - Community beta testing
   - Public plugin marketplace listing

---

## X. Appendices

### A. Glossary

- **Baseline Models**: Simple forecasting methods (SeasonalNaive, ETS, Theta) used as performance benchmarks
- **Golden Tasks**: Canonical test cases that must pass for plugin validation
- **MCP**: Model Context Protocol - standard for exposing tools to LLMs
- **sMAPE**: Symmetric Mean Absolute Percentage Error - accuracy metric
- **MASE**: Mean Absolute Scaled Error - scale-independent accuracy metric

### B. References

- [Claude Code Plugins Reference](https://code.claude.com/docs/en/plugins-reference)
- [Claude Skills Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)
- [Bob's Brain Architecture](https://github.com/jeremylongshore/bobs-brain)
- [Nixtla Documentation](https://docs.nixtla.io/)
- [M4 Competition](https://www.sciencedirect.com/science/article/pii/S0169207019301128)

### C. Contact Information

- **Project Lead**: Jeremy Longshore (jeremy@intentsolutions.io)
- **Nixtla Collaboration**: Max Mergenthaler (max@nixtla.io)
- **Repository**: https://github.com/intent-solutions-io/plugins-nixtla

---

**Document Version**: 1.0.0
**Created**: 2025-11-24
**Next Review**: After Phase 1 completion
