# Claude Skill PRD: [Skill Name]

**Template Version**: 1.0.0
**Based On**: [Anthropic Skills Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)
**Purpose**: Product Requirements Document for Claude Skills
**Status**: Template

---

## Document Control

| Field | Value |
|-------|-------|
| **Skill Name** | nixtla-[short-name] |
| **Skill Type** | [ ] Mode Skill [ ] Utility Skill |
| **Domain** | [e.g., Prediction Markets + Time Series Forecasting] |
| **Target Users** | [e.g., Traders, Data Scientists, Analysts] |
| **Priority** | [ ] Critical [ ] High [ ] Medium [ ] Low |
| **Status** | [ ] Planned [ ] In Development [ ] Complete |
| **Owner** | [Name/Team] |
| **Last Updated** | YYYY-MM-DD |

---

## 1. Executive Summary

**One-sentence description**: [What this skill does in one clear sentence]

**Value Proposition**: [Why this skill matters - the core benefit it delivers]

**Key Metrics**:
- Target activation accuracy: [XX]%
- Expected usage frequency: [X times per Y]
- Description quality target: [80]%+

---

## 2. Problem Statement

### Current State (Without This Skill)

**Pain Points**:
1. [Specific pain point 1]
2. [Specific pain point 2]
3. [Specific pain point 3]

**Current Workarounds**:
- [How users currently solve this without the skill]
- [What makes current solutions inadequate]

**Impact of Problem**:
- Time wasted: [X hours per Y]
- Error rate: [Z]%
- User frustration level: [High/Medium/Low]

### Desired State (With This Skill)

**Transformation**:
- From: [Current manual process]
- To: [Automated/assisted process with skill]

**Expected Benefits**:
1. [Quantifiable benefit 1]
2. [Quantifiable benefit 2]
3. [Quantifiable benefit 3]

---

## 3. Target Users

### Primary Users

**User Persona 1**: [e.g., Prediction Market Trader]
- **Background**: [Experience level, technical skills]
- **Goals**: [What they're trying to achieve]
- **Pain Points**: [What frustrates them currently]
- **Use Frequency**: [Daily/Weekly/Monthly]

**User Persona 2**: [e.g., Data Scientist]
- **Background**: [Experience level, technical skills]
- **Goals**: [What they're trying to achieve]
- **Pain Points**: [What frustrates them currently]
- **Use Frequency**: [Daily/Weekly/Monthly]

### Secondary Users

[Any additional user types who might benefit]

---

## 4. User Stories

**Format**: "As a [user type], I want [capability], so that [benefit]"

### Critical User Stories (Must Have)

1. **As a** [user type],
   **I want** [specific capability],
   **So that** [concrete benefit].

   **Acceptance Criteria**:
   - [ ] [Criterion 1]
   - [ ] [Criterion 2]
   - [ ] [Criterion 3]

2. **As a** [user type],
   **I want** [specific capability],
   **So that** [concrete benefit].

   **Acceptance Criteria**:
   - [ ] [Criterion 1]
   - [ ] [Criterion 2]

3. [Additional critical stories...]

### High-Priority User Stories (Should Have)

1. [Story]
2. [Story]

### Nice-to-Have User Stories (Could Have)

1. [Story]
2. [Story]

---

## 5. Functional Requirements

### Core Capabilities (Must Have)

**REQ-1**: [Requirement Title]
- **Description**: [Detailed description of what the skill must do]
- **Rationale**: [Why this is necessary]
- **Acceptance Criteria**:
  - [ ] [Specific, measurable criterion]
  - [ ] [Specific, measurable criterion]
- **Dependencies**: [What this requires]

**REQ-2**: [Requirement Title]
- **Description**: [Detailed description]
- **Rationale**: [Why necessary]
- **Acceptance Criteria**:
  - [ ] [Criterion]
  - [ ] [Criterion]
- **Dependencies**: [Requirements]

[Continue for all core requirements...]

### Integration Requirements

**REQ-API-1**: [API Integration Name - e.g., Polymarket API]
- **Purpose**: [What data/functionality this provides]
- **Endpoints**: [Specific endpoints used]
- **Authentication**: [API key/OAuth/etc.]
- **Rate Limits**: [X requests per Y]
- **Error Handling**: [How to handle failures]

**REQ-API-2**: [e.g., Nixtla TimeGPT API]
- **Purpose**: [What this provides]
- **Endpoints**: [Specific endpoints]
- **Authentication**: [Method]
- **Rate Limits**: [Limits]
- **Cost Considerations**: [API costs]

### Data Requirements

**REQ-DATA-1**: Input Data Format
- **Format**: [CSV/JSON/etc.]
- **Required Fields**: [Field list]
- **Optional Fields**: [Field list]
- **Validation Rules**: [How to validate]

**REQ-DATA-2**: Output Data Format
- **Format**: [What format skill produces]
- **Fields**: [What's included]
- **Quality Standards**: [Accuracy requirements]

### Performance Requirements

**REQ-PERF-1**: Response Time
- **Target**: [X seconds for Y operation]
- **Max Acceptable**: [Z seconds]

**REQ-PERF-2**: Token Budget
- **Description Size**: <250 characters (fits in 15k token budget)
- **SKILL.md Size**: <500 lines (~2,500 tokens)
- **Total Skill Size**: <5,000 tokens including all references

### Quality Requirements

**REQ-QUAL-1**: Description Quality
- **Target Score**: 80%+ on quality formula
- **Must Include**:
  - [ ] Action-oriented verbs
  - [ ] "Use when [scenarios]" clause
  - [ ] "Trigger with '[phrases]'" examples
  - [ ] Domain keywords

**REQ-QUAL-2**: Accuracy
- **Forecast Accuracy**: [Target MAPE/RMSE]
- **Data Parsing Accuracy**: [99]%+
- **Error Rate**: <[X]%

---

## 6. Non-Goals (Out of Scope)

**What This Skill Does NOT Do**:

1. **[Out of scope item 1]**
   - **Rationale**: [Why this is excluded]
   - **Alternative**: [How users can accomplish this instead]

2. **[Out of scope item 2]**
   - **Rationale**: [Why excluded]
   - **Alternative**: [Alternative approach]

3. **[Future enhancements]**
   - **May be added in**: [Version X.Y]
   - **Depends on**: [What needs to happen first]

---

## 7. Success Metrics

### Skill Activation Metrics

**Metric 1**: Activation Accuracy
- **Definition**: % of times skill activates when it should
- **Target**: 90%+
- **Measurement**: Manual testing with trigger phrases

**Metric 2**: False Positive Rate
- **Definition**: % of times skill activates incorrectly
- **Target**: <5%
- **Measurement**: User feedback + monitoring

### Quality Metrics

**Metric 3**: Description Quality Score
- **Formula**: 6-criterion weighted scoring (see ARD)
- **Target**: 80%+
- **Components**:
  - Action-oriented: 20%
  - Clear triggers: 25%
  - Comprehensive: 15%
  - Natural language: 20%
  - Specificity: 10%
  - Technical terms: 10%

**Metric 4**: SKILL.md Size
- **Target**: <500 lines
- **Max**: 800 lines (token budget limit)
- **Current**: [TBD]

### Usage Metrics

**Metric 5**: Adoption Rate
- **Target**: [X]% of target users activate skill within first month
- **Measurement**: Skill invocation logs

**Metric 6**: User Satisfaction
- **Target**: [X]/5 rating
- **Measurement**: User surveys

### Performance Metrics

**Metric 7**: Accuracy
- **Domain-Specific**: [e.g., Forecast MAPE <10%]
- **Target**: [Specific target]
- **Measurement**: [How to measure]

---

## 8. User Experience Flow

### Typical Usage Flow

1. **User Intent**: [User wants to accomplish X]
2. **Trigger**: User says "[trigger phrase]"
3. **Skill Activation**: Claude recognizes need for skill
4. **Skill Execution**: [Step-by-step what happens]
5. **Output Delivered**: [What user receives]
6. **User Action**: [What user does with output]

### Example Scenario

**Scenario**: [Concrete example of skill usage]

**Input**:
```
[Exact user request]
```

**Claude's Response**:
```
[What Claude says/does with skill active]
```

**Output**:
```
[Concrete output produced]
```

**User Benefit**: [What value user derived]

---

## 9. Integration Points

### External Systems

**System 1**: [e.g., Polymarket API]
- **Purpose**: [What data/functionality]
- **Integration Type**: [REST API/GraphQL/SDK]
- **Authentication**: [Method]
- **Data Flow**: [Skill → API → Skill]

**System 2**: [e.g., Nixtla TimeGPT]
- **Purpose**: [What it provides]
- **Integration Type**: [API type]
- **Authentication**: [Method]
- **Cost**: [Per-call costs]

### Internal Dependencies

**Dependency 1**: [e.g., Nixtla Schema Standard]
- **What it provides**: [Data format standard]
- **Why needed**: [Reason]

**Dependency 2**: [e.g., Python Libraries]
- **Libraries**: pandas, requests, nixtla
- **Versions**: [Minimum versions]

---

## 10. Constraints & Assumptions

### Technical Constraints

1. **Token Budget**: Must fit in 15k char skill discovery limit
2. **API Rate Limits**: [Specific limits]
3. **Processing Time**: [Max acceptable time]
4. **Dependencies**: [Required libraries/APIs must be available]

### Business Constraints

1. **API Costs**: [Budget limitations]
2. **Timeline**: [When skill must be ready]
3. **Resources**: [Team availability]

### Assumptions

1. **Assumption 1**: [e.g., Users have Polymarket API access]
   - **Risk if false**: [Impact]
   - **Mitigation**: [How to handle]

2. **Assumption 2**: [e.g., Users understand prediction markets]
   - **Risk if false**: [Impact]
   - **Mitigation**: [How to handle]

---

## 11. Risk Assessment

### Technical Risks

**Risk 1**: API Rate Limiting
- **Probability**: [High/Medium/Low]
- **Impact**: [High/Medium/Low]
- **Mitigation**: [How to handle]

**Risk 2**: Forecast Accuracy
- **Probability**: [Probability]
- **Impact**: [Impact]
- **Mitigation**: [Mitigation strategy]

### User Experience Risks

**Risk 1**: Skill Over-Triggering (False Positives)
- **Probability**: [Probability]
- **Impact**: [Impact]
- **Mitigation**: [Precise description writing]

**Risk 2**: Skill Under-Triggering (False Negatives)
- **Probability**: [Probability]
- **Impact**: [Impact]
- **Mitigation**: [Comprehensive trigger phrases]

---

## 12. Open Questions

**Questions Requiring Decisions**:

1. **Question**: [Open question needing answer]
   - **Options**: [Option A, Option B]
   - **Decision Needed By**: [Date]
   - **Owner**: [Who decides]

2. **Question**: [Open question]
   - **Options**: [Options]
   - **Decision Needed By**: [Date]
   - **Owner**: [Who decides]

---

## 13. Appendix: Examples

### Example 1: [Scenario Name]

**User Request**:
```
[Exact user input]
```

**Expected Skill Behavior**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Output**:
```
[Exact output format]
```

### Example 2: [Edge Case]

**User Request**:
```
[Input]
```

**Expected Behavior**:
[How skill handles this]

---

## 14. Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | YYYY-MM-DD | Initial PRD | [Name] |

---

## 15. Approval

| Role | Name | Approval Date | Signature |
|------|------|---------------|-----------|
| Product Owner | [Name] | [Date] | [Signature] |
| Tech Lead | [Name] | [Date] | [Signature] |
| User Representative | [Name] | [Date] | [Signature] |

---

**Template maintained by**: Intent Solutions
**For**: Nixtla Skills Pack + Global Standard
**Last Updated**: 2025-12-05
