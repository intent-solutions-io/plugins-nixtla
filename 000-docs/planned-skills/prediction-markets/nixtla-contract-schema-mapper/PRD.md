# Claude Skill PRD: Nixtla Contract Schema Mapper

**Template Version**: 1.0.0
**Based On**: [Anthropic Skills Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)
**Purpose**: Product Requirements Document for Claude Skills
**Status**: Planned

---

## Document Control

| Field | Value |
|-------|-------|
| **Skill Name** | nixtla-contract-schema-mapper |
| **Skill Type** | [ ] Mode Skill [X] Utility Skill |
| **Domain** | Prediction Markets + Time Series Forecasting |
| **Target Users** | Traders, Data Scientists, Skill Developers |
| **Priority** | [X] Critical [ ] High [ ] Medium [ ] Low |
| **Status** | [X] Planned [ ] In Development [ ] Complete |
| **Owner** | Intent Solutions |
| **Last Updated** | 2025-12-05 |

---

## 1. Executive Summary

**One-sentence description**: Transform prediction market contract data from any platform (Polymarket, Kalshi, PredictIt, Manifold Markets) into Nixtla-compatible time series format with automatic platform detection, data quality validation, and multi-outcome support.

**Value Proposition**: Eliminates the manual data wrangling bottleneck that blocks 80% of prediction market forecasting workflows—reducing data preparation time from 30-60 minutes to <10 seconds while ensuring zero data quality errors.

**Key Metrics**:
- Target activation accuracy: 98%
- Expected usage frequency: 10-20 times per day (every forecast workflow requires this)
- Description quality target: 95%+
- Data transformation accuracy: 99.9%+
- Platform detection accuracy: 100%

---

## 2. Problem Statement

### Current State (Without This Skill)

**Pain Points**:
1. **Platform-specific data formats**: Each prediction market has different APIs and data schemas—manual transformation required for each platform
2. **Time-consuming data wrangling**: Converting raw contract odds to Nixtla format takes 30-60 minutes per analysis (80% of total analysis time)
3. **Frequent data quality errors**: Manual transformations introduce errors (missing dates, wrong formats, invalid values) in 40% of cases
4. **No validation infrastructure**: Users discover data quality issues only after forecast fails—wasted API calls and time
5. **Categorical market complexity**: Multi-outcome markets (>2 outcomes) require complex logic that most users don't implement correctly
6. **Repetitive copy-paste code**: Every prediction market skill reimplements the same data transformation logic

**Current Workarounds**:
- Write custom Python scripts for each platform (2-4 hours development time)
- Manual CSV editing in Excel (30-60 minutes, error-prone)
- Copy-paste transformation code across skills (maintenance nightmare, duplicated bugs)

**Impact of Problem**:
- Time wasted: 30-60 minutes per analysis (blocks 80% of workflow time)
- Error rate: 40% of manual transformations have data quality issues
- User frustration level: Critical (data wrangling is the #1 complaint in prediction market forecasting)
- Blocked innovation: New prediction market platforms can't be integrated without rewriting transformation logic

### Desired State (With This Skill)

**Transformation**:
- From: Manual 30-60 minute data wrangling with 40% error rate
- To: Automated 10-second transformation with 99.9%+ accuracy and automatic platform detection

**Expected Benefits**:
1. **300x faster data preparation**: 30-60 minutes → 10 seconds (99.5% time reduction)
2. **Near-zero errors**: 40% error rate → <0.1% error rate (99.75% improvement)
3. **Platform-agnostic**: Support 4+ prediction market platforms with zero user configuration
4. **Automatic validation**: Catch data quality issues before forecast API calls (saves API quota + time)
5. **Categorical market support**: Handle multi-outcome markets correctly (unlocks 30% more use cases)
6. **Reusable foundation**: All prediction market skills depend on this utility (DRY principle)

---

## 3. Target Users

### Primary Users

**User Persona 1: Prediction Market Analyst (Skills User)**
- **Background**: Uses other prediction market skills (nixtla-polymarket-analyst, etc.), limited data engineering experience
- **Goals**: Analyze prediction markets without dealing with data wrangling complexity
- **Pain Points**: Data transformation is slow, error-prone, blocks actual analysis work
- **Use Frequency**: Every single forecast workflow (10-20 times per day for active users)
- **Technical Skills**: Understands prediction markets, basic Python, minimal data engineering

**User Persona 2: Skill Developer**
- **Background**: Building new prediction market skills, needs reliable data transformation foundation
- **Goals**: Focus on analysis logic, not reinventing data transformation for each skill
- **Pain Points**: Copy-pasting transformation code, maintaining duplicated logic across skills
- **Use Frequency**: Daily during development, then embedded in their skills
- **Technical Skills**: Expert Python, understands Claude skills architecture

### Secondary Users

**Data Scientists**: Exploring new prediction market platforms, need quick data transformation for experiments
**Researchers**: Analyzing historical prediction market data, need standardized format for comparisons
**Power Traders**: Building custom workflows, need reliable data pipeline foundation

---

## 4. User Stories

**Format**: "As a [user type], I want [capability], so that [benefit]"

### Critical User Stories (Must Have)

1. **As a** prediction market analyst,
   **I want** to automatically detect which platform my data came from (Polymarket, Kalshi, PredictIt, Manifold),
   **So that** I don't have to manually specify platform configuration or understand schema differences.

   **Acceptance Criteria**:
   - [ ] Detects Polymarket JSON format (GraphQL response schema)
   - [ ] Detects Kalshi JSON format (REST API response schema)
   - [ ] Detects PredictIt JSON format (API response schema)
   - [ ] Detects Manifold Markets JSON format (API response schema)
   - [ ] Returns platform name + confidence score (100% for exact match)
   - [ ] Fails gracefully with helpful error if platform unknown

2. **As a** prediction market analyst,
   **I want** the skill to validate data quality automatically (no gaps, proper frequency, 0≤y≤1),
   **So that** I discover data issues before wasting API quota on failed forecast calls.

   **Acceptance Criteria**:
   - [ ] Checks for missing dates (gaps in time series)
   - [ ] Validates all prices are between 0 and 1
   - [ ] Ensures chronological order (no date inversions)
   - [ ] Detects frequency (daily, hourly, etc.) automatically
   - [ ] Warns if insufficient data (<14 days for typical forecasts)
   - [ ] Provides specific error messages with fix suggestions

3. **As a** skill developer,
   **I want** the skill to handle categorical markets (multi-outcome contracts, not just binary YES/NO),
   **So that** I can build skills that work with all prediction market types.

   **Acceptance Criteria**:
   - [ ] Detects binary markets (2 outcomes: YES/NO)
   - [ ] Detects categorical markets (3+ outcomes)
   - [ ] Transforms each outcome into separate time series
   - [ ] Generates unique_id for each outcome
   - [ ] Outputs multiple CSV files (one per outcome) or single multi-series CSV
   - [ ] Validates that outcome probabilities sum to ~1.0

### High-Priority User Stories (Should Have)

4. **As a** data scientist,
   **I want** to specify custom data quality thresholds (e.g., "allow up to 3 missing days"),
   **So that** I can work with imperfect data when necessary.

   **Acceptance Criteria**:
   - [ ] Accepts `--max-missing-days` parameter (default: 0)
   - [ ] Accepts `--min-data-points` parameter (default: 14)
   - [ ] Accepts `--allow-interpolation` flag (default: false)
   - [ ] Logs warnings when thresholds exceeded but processing continues
   - [ ] Adds metadata to output noting data quality compromises

5. **As a** skill developer,
   **I want** the skill to expose a Python API (not just CLI),
   **So that** I can call it programmatically from other skills without subprocess overhead.

   **Acceptance Criteria**:
   - [ ] Provides `transform_contract_data(raw_data, platform=None)` function
   - [ ] Returns structured dict/DataFrame (not just file write)
   - [ ] Accepts both file paths and in-memory data structures
   - [ ] Raises clear exceptions with actionable error messages
   - [ ] Fully typed (Python 3.9+ type hints)

### Nice-to-Have User Stories (Could Have)

6. **As a** researcher,
   **I want** batch processing mode to transform 100+ contracts in one command,
   **So that** I can build historical datasets efficiently.

7. **As a** power user,
   **I want** to add support for new prediction market platforms via JSON config,
   **So that** I don't have to wait for official skill updates.

---

## 5. Functional Requirements

### Core Capabilities (Must Have)

**REQ-1: Platform Auto-Detection**
- **Description**: Automatically identify which prediction market platform produced the raw data by analyzing JSON schema structure
- **Rationale**: Users shouldn't need to know or specify platform—skill should be smart enough to detect
- **Acceptance Criteria**:
  - [ ] Detects Polymarket by GraphQL response structure (`data.contract.oddsHistory`)
  - [ ] Detects Kalshi by REST API structure (`markets[].ticker`, `yes_price`)
  - [ ] Detects PredictIt by API structure (`markets[].contracts[]`)
  - [ ] Detects Manifold Markets by API structure (`bets[]`, `probability`)
  - [ ] Returns detection result: `{"platform": "Polymarket", "confidence": 1.0, "schema_version": "v1"}`
  - [ ] Handles ambiguous cases with confidence scores <1.0
  - [ ] Provides manual override: `--platform Polymarket` flag
- **Dependencies**: Access to sample data from all 4 platforms for schema fingerprinting

**REQ-2: Schema Transformation**
- **Description**: Convert platform-specific JSON to standard 3-column Nixtla CSV format (unique_id, ds, y)
- **Rationale**: Nixtla APIs require this exact format—must be perfect or forecasts fail
- **Acceptance Criteria**:
  - [ ] Extracts timestamp field (various names: `timestamp`, `created_time`, `t`, etc.)
  - [ ] Converts timestamps to ISO 8601 format (`YYYY-MM-DD` for daily, `YYYY-MM-DD HH:MM:SS` for intraday)
  - [ ] Extracts probability/price field (various names: `yes_price`, `probability`, `price`, `avg_price`)
  - [ ] Generates meaningful unique_id from contract metadata (e.g., `BTC_100k_Dec2025`)
  - [ ] Outputs exactly 3 columns: `unique_id,ds,y`
  - [ ] Handles missing/null values (interpolation or error, configurable)
- **Dependencies**: REQ-1 (platform detection)

**REQ-3: Data Quality Validation**
- **Description**: Validate transformed data meets Nixtla requirements and prediction market domain constraints
- **Rationale**: Catch errors early—before wasting API quota on bad data
- **Acceptance Criteria**:
  - [ ] Validates: All `y` values are 0 ≤ y ≤ 1 (probabilities)
  - [ ] Validates: No missing dates (daily frequency has no gaps)
  - [ ] Validates: Chronological order (dates ascending)
  - [ ] Validates: Minimum data points (default: 14 days for forecasting)
  - [ ] Validates: No duplicate timestamps
  - [ ] Warns: Suspicious patterns (constant values, extreme volatility)
  - [ ] Outputs validation report: `data_quality_report.json`
- **Dependencies**: REQ-2 (transformed data)

**REQ-4: Categorical Market Support**
- **Description**: Handle multi-outcome prediction markets (e.g., "Who wins election? Trump/Biden/RFK/Other")
- **Rationale**: 30% of prediction markets are categorical—must support to be comprehensive
- **Acceptance Criteria**:
  - [ ] Detects binary markets (2 outcomes) vs categorical (3+ outcomes)
  - [ ] For categorical: Creates separate time series for each outcome
  - [ ] Generates unique_id per outcome: `Election2024_Trump`, `Election2024_Biden`, etc.
  - [ ] Validates: Outcome probabilities sum to ~1.0 (±0.05 tolerance)
  - [ ] Outputs: Either multiple CSV files or single multi-series CSV (configurable)
  - [ ] Logs: Number of outcomes detected and processed
- **Dependencies**: REQ-2 (schema transformation)

**REQ-5: Output Format Standardization**
- **Description**: Produce Nixtla-compatible CSV file(s) with metadata JSON
- **Rationale**: Downstream skills need consistent, predictable output format
- **Acceptance Criteria**:
  - [ ] Primary output: `timeseries.csv` (3 columns: unique_id, ds, y)
  - [ ] Metadata output: `metadata.json` (platform, contract info, validation status)
  - [ ] Configurable output paths: `--output data/timeseries.csv`
  - [ ] Atomic writes (temp file + rename, never corrupt existing file)
  - [ ] UTF-8 encoding, Unix line endings (LF)
  - [ ] Headers included, no index column
- **Dependencies**: REQ-2, REQ-3, REQ-4

### Integration Requirements

**REQ-API-1: File System Integration**
- **Purpose**: Read raw JSON data, write transformed CSV output
- **Endpoints**: N/A (local filesystem)
- **Authentication**: N/A (file permissions)
- **Rate Limits**: N/A (disk I/O)
- **Error Handling**: Permission errors, disk full, file not found

**REQ-API-2: Python API Integration** (for other skills)
- **Purpose**: Allow other skills to call this skill programmatically
- **Endpoints**: Python function: `transform_contract_data()`
- **Authentication**: N/A (local import)
- **Rate Limits**: N/A (local execution)
- **Error Handling**: Raise typed exceptions, no silent failures

### Data Requirements

**REQ-DATA-1: Input Data Format**
- **Format**: JSON (platform-specific structure)
- **Required Fields**: Varies by platform, but must include:
  - Timestamps (some date/time field)
  - Probabilities/prices (some price field)
  - Contract metadata (question, outcomes, etc.)
- **Optional Fields**: Volume, liquidity, bet counts (ignored if present)
- **Validation Rules**: JSON must be valid (parseable), must match one of 4 known platform schemas

**REQ-DATA-2: Output Data Format**
- **Format**: CSV (Nixtla standard)
- **Fields**:
  - `unique_id` (string): Contract identifier
  - `ds` (ISO 8601 datetime): Timestamp
  - `y` (float): Probability/price (0-1)
- **Quality Standards**: 100% valid rows (no missing, out-of-range, or malformed values)

### Performance Requirements

**REQ-PERF-1: Response Time**
- **Target**: <10 seconds for typical contract (30 days of daily data)
- **Max Acceptable**: <30 seconds
- **Breakdown**:
  - Platform detection: <1 second
  - Schema transformation: <5 seconds
  - Data validation: <3 seconds
  - File write: <1 second

**REQ-PERF-2: Token Budget**
- **Description Size**: <200 characters (fits in 15k token budget with room for other skills)
- **SKILL.md Size**: <300 lines (~1,500 tokens)
- **Total Skill Size**: <2,500 tokens including all references

### Quality Requirements

**REQ-QUAL-1: Description Quality**
- **Target Score**: 95%+ on quality formula
- **Must Include**:
  - [X] Action-oriented verbs: "Transform", "Detects", "Validates"
  - [X] "Use when [scenarios]" clause: "Use when converting prediction market data to Nixtla format"
  - [X] "Trigger with '[phrases]'" examples: "map contract data", "transform to Nixtla format"
  - [X] Domain keywords: "Polymarket", "Kalshi", "time series", "schema", "validation"

**REQ-QUAL-2: Accuracy**
- **Data Transformation Accuracy**: 99.9%+ (zero data corruption)
- **Platform Detection Accuracy**: 100% (for supported platforms)
- **Validation Error Rate**: <0.1% (false positives on valid data)

---

## 6. Non-Goals (Out of Scope)

**What This Skill Does NOT Do**:

1. **Fetching data from prediction market APIs**
   - **Rationale**: This skill transforms existing data, doesn't fetch it (that's the job of analyst skills like nixtla-polymarket-analyst)
   - **Alternative**: Use platform-specific fetch skills, then pass data to this mapper

2. **Forecasting or analysis**
   - **Rationale**: This is a pure data transformation utility—forecasting is handled by other skills
   - **Alternative**: Chain this skill with nixtla-polymarket-analyst or similar

3. **Historical data backfilling**
   - **Rationale**: Utility assumes you already have the raw data
   - **Alternative**: Use platform APIs to fetch historical data first
   - **May be added in**: v2.0 (if user demand is high)

4. **Real-time streaming transformation**
   - **Rationale**: Batch processing only—processes complete datasets
   - **Alternative**: Run skill repeatedly in cron job for quasi-real-time
   - **Depends on**: Streaming API architecture (future enhancement)

---

## 7. Success Metrics

### Skill Activation Metrics

**Metric 1: Activation Accuracy**
- **Definition**: % of times skill activates when it should
- **Target**: 98%+
- **Measurement**: Manual testing with 20+ trigger phrase variations
- **Test Phrases**: "transform contract data to Nixtla format", "map Polymarket data", "convert to time series"

**Metric 2: False Positive Rate**
- **Definition**: % of times skill activates incorrectly
- **Target**: <1%
- **Measurement**: User feedback + monitoring logs

### Quality Metrics

**Metric 3: Description Quality Score**
- **Formula**: 6-criterion weighted scoring (see ARD)
- **Target**: 95%+
- **Components**:
  - Action-oriented: 20% (target: 20/20)
  - Clear triggers: 25% (target: 24/25)
  - Comprehensive: 15% (target: 14/15)
  - Natural language: 20% (target: 19/20)
  - Specificity: 10% (target: 10/10)
  - Technical terms: 10% (target: 10/10)
  - **Total Target**: 95/100

**Metric 4: SKILL.md Size**
- **Target**: <300 lines
- **Max**: 500 lines (hard limit due to token budget)
- **Current**: TBD (to be measured after implementation)

### Usage Metrics

**Metric 5: Adoption Rate**
- **Target**: 100% of prediction market skills depend on this utility within 3 months
- **Measurement**: Skill dependency graph, import statements in other skills

**Metric 6: User Satisfaction**
- **Target**: 4.8/5 rating (higher than analyst skills since this eliminates pain point)
- **Measurement**: Post-transformation survey

### Performance Metrics

**Metric 7: Transformation Accuracy**
- **Domain-Specific**: 0 data corruption errors (99.9%+ accuracy)
- **Target**: <1 error per 1,000 transformations
- **Measurement**: Compare input/output row counts, validate all values in valid ranges

**Metric 8: Platform Detection Accuracy**
- **Target**: 100% accuracy for supported platforms
- **Measurement**: Test with 100 sample files from each platform (400 total)

---

## 8. User Experience Flow

### Typical Usage Flow

1. **User Intent**: Analyst has raw Polymarket data, needs it in Nixtla format for forecasting
2. **Trigger**: User says "Transform this Polymarket data to Nixtla format: data/raw_polymarket.json"
3. **Skill Activation**: Claude recognizes need for `nixtla-contract-schema-mapper` skill
4. **Skill Execution**:
   - Step 1: Read JSON file, auto-detect platform (Polymarket)
   - Step 2: Transform to 3-column CSV format
   - Step 3: Validate data quality (check gaps, ranges, chronology)
   - Step 4: Write output CSV + metadata JSON
5. **Output Delivered**: `timeseries.csv` (ready for forecasting) + validation report
6. **User Action**: Pass `timeseries.csv` to forecasting skill or API

### Example Scenario

**Scenario**: Data scientist converting Kalshi contract data for analysis

**Input**:
```
I have Kalshi data in data/kalshi_btc_contract.json. Transform it to Nixtla format
so I can forecast it.
```

**Claude's Response**:
```
I'll transform this Kalshi contract data to Nixtla time series format using the
nixtla-contract-schema-mapper skill.

[Skill executes 4-step workflow in ~8 seconds]

✓ Platform detected: Kalshi (100% confidence)
✓ Contract: BTC-100K-DEC25 (binary market)
✓ Transformed: 45 days of data (2025-10-21 to 2025-12-04)
✓ Validation passed: No gaps, all prices 0-1, chronological order
✓ Output saved to: data/timeseries.csv (3 columns, 45 rows)
```

**Output** (`data/timeseries.csv`):
```csv
unique_id,ds,y
BTC_100K_DEC25,2025-10-21,0.48
BTC_100K_DEC25,2025-10-22,0.49
BTC_100K_DEC25,2025-10-23,0.52
...
BTC_100K_DEC25,2025-12-04,0.68
```

**Output** (`data/metadata.json`):
```json
{
  "platform": "Kalshi",
  "platform_confidence": 1.0,
  "contract_id": "BTC-100K-DEC25",
  "contract_question": "Will Bitcoin reach $100k by December 2025?",
  "market_type": "binary",
  "outcomes": ["YES", "NO"],
  "data_points": 45,
  "date_range": {"start": "2025-10-21", "end": "2025-12-04"},
  "frequency": "daily",
  "validation_status": "passed",
  "validation_checks": {
    "missing_dates": 0,
    "out_of_range_values": 0,
    "chronology_errors": 0,
    "duplicate_timestamps": 0
  },
  "transformation_time_seconds": 8.2
}
```

**User Benefit**: Transformed data in 8 seconds (vs 30-60 minutes manual work), zero errors, ready for forecasting

---

## 9. Integration Points

### External Systems

**System 1: File System (Input)**
- **Purpose**: Read raw prediction market data files
- **Integration Type**: File I/O (JSON files)
- **Authentication**: File permissions
- **Data Flow**: Skill reads from user-specified path

**System 2: File System (Output)**
- **Purpose**: Write transformed CSV + metadata JSON
- **Integration Type**: File I/O (CSV, JSON files)
- **Authentication**: File permissions
- **Data Flow**: Skill writes to user-specified path (or default: `data/timeseries.csv`)

### Internal Dependencies

**Dependency 1: Nixtla Schema Standard**
- **What it provides**: 3-column time series format specification
- **Why needed**: Must produce exact format required by Nixtla APIs

**Dependency 2: Python Libraries**
- **Libraries**: `pandas`, `json`, `datetime`
- **Versions**:
  - pandas >= 2.0.0 (data manipulation)
  - json (stdlib, for parsing)
  - datetime (stdlib, for timestamp conversion)

**Dependency 3: Other Prediction Market Skills** (indirect)
- **What it provides**: This skill serves as foundation for all prediction market skills
- **Why needed**: DRY principle—avoid duplicating transformation logic across skills

---

## 10. Constraints & Assumptions

### Technical Constraints

1. **Token Budget**: Must fit in 2,500 token limit (utility skills should be lightweight)
2. **Platform Support**: Limited to 4 platforms initially (Polymarket, Kalshi, PredictIt, Manifold)
3. **File Size Limits**: Assumes input files <50 MB (typical contract data ~5-50 KB)
4. **Processing Time**: Must complete in <30 seconds for typical datasets

### Business Constraints

1. **Development Timeline**: Must be ready before analyst skills launch (foundational dependency)
2. **Maintenance Burden**: Must be stable—breaking changes impact all dependent skills
3. **Documentation**: Must be exceptionally clear (utility skill used by skill developers)

### Assumptions

1. **Assumption 1: Users have raw prediction market data in JSON format**
   - **Risk if false**: Skill can't process CSV, XML, or other formats
   - **Mitigation**: Document supported input formats clearly, provide conversion examples

2. **Assumption 2: Platform schemas remain stable over time**
   - **Risk if false**: Skill breaks when platforms update APIs
   - **Mitigation**: Version platform schemas, add auto-update mechanism or manual override

3. **Assumption 3: 4 platforms cover 90%+ of use cases**
   - **Risk if false**: Users demand support for obscure platforms
   - **Mitigation**: Design extensible architecture, document how to add new platforms

4. **Assumption 4: Data quality issues are detectable via statistical checks**
   - **Risk if false**: Subtle data corruption passes validation
   - **Mitigation**: Conservative validation rules, warn on suspicious patterns

---

## 11. Risk Assessment

### Technical Risks

**Risk 1: Platform Schema Changes**
- **Probability**: High (APIs evolve frequently)
- **Impact**: High (skill breaks for that platform)
- **Mitigation**:
  - Version platform schemas (detect v1 vs v2)
  - Graceful degradation (manual override flag)
  - Monitor platform API changelogs

**Risk 2: Ambiguous Platform Detection**
- **Probability**: Medium (some platforms may have similar schemas)
- **Impact**: Medium (wrong transformation applied)
- **Mitigation**:
  - Use confidence scores, require >95% to auto-detect
  - Provide manual override: `--platform Kalshi`
  - Log detection decision for debugging

**Risk 3: Data Quality False Positives**
- **Probability**: Low (conservative validation rules)
- **Impact**: Medium (blocks valid data from processing)
- **Mitigation**:
  - Configurable validation thresholds
  - Warning vs error distinction
  - Override flags for power users

### User Experience Risks

**Risk 1: Skill Over-Triggering (False Positives)**
- **Probability**: Low (very specific use case)
- **Impact**: Low (utility skill, no harm in activating)
- **Mitigation**: Precise description with narrow trigger phrases

**Risk 2: Skill Under-Triggering (False Negatives)**
- **Probability**: Medium (users may use non-standard phrasing)
- **Impact**: High (blocks entire workflow if not activated)
- **Mitigation**: Comprehensive trigger phrases, document exact invocation examples

---

## 12. Open Questions

**Questions Requiring Decisions**:

1. **Question**: Should categorical markets output multiple CSV files (one per outcome) or single multi-series CSV?
   - **Options**:
     - Option A: Multiple files (`timeseries_trump.csv`, `timeseries_biden.csv`)
     - Option B: Single file with multiple unique_id values
   - **Decision Needed By**: Before development starts
   - **Owner**: Technical Lead

2. **Question**: What should default data quality thresholds be (max missing days, min data points)?
   - **Options**:
     - Strict: 0 missing days, 30 min data points
     - Moderate: 3 missing days, 14 min data points
     - Lenient: 10 missing days, 7 min data points
   - **Decision Needed By**: Before v1.0 release
   - **Owner**: Product Lead + User feedback

3. **Question**: Should we support CSV input in addition to JSON?
   - **Options**:
     - JSON only (simpler, covers 90% of cases)
     - JSON + CSV (more flexible, higher complexity)
   - **Decision Needed By**: v1.0 or v1.1
   - **Owner**: Product Lead

**Recommended Decisions**:
1. Single multi-series CSV (Option B) - easier for forecasting APIs
2. Moderate thresholds (configurable via CLI flags)
3. JSON only for v1.0 (CSV in v1.1 if demand exists)

---

## 13. Appendix: Examples

### Example 1: Polymarket Binary Market

**User Request**:
```
Transform data/polymarket_btc.json to Nixtla format
```

**Expected Skill Behavior**:
1. Read JSON file
2. Detect platform: Polymarket (GraphQL schema with `data.contract.oddsHistory`)
3. Extract yes_price as target variable
4. Generate unique_id: `BTC_100k_Dec2025`
5. Validate: 30 days, no gaps, 0≤y≤1
6. Write `data/timeseries.csv` + `data/metadata.json`

**Expected Output** (`timeseries.csv`):
```csv
unique_id,ds,y
BTC_100k_Dec2025,2025-11-05,0.52
BTC_100k_Dec2025,2025-11-06,0.54
BTC_100k_Dec2025,2025-11-07,0.53
...
```

### Example 2: Kalshi Categorical Market

**User Request**:
```
Map this Kalshi election data to Nixtla: data/kalshi_election.json
```

**Expected Skill Behavior**:
1. Read JSON
2. Detect platform: Kalshi
3. Detect market type: Categorical (4 outcomes: Trump/Biden/RFK/Other)
4. Transform each outcome to separate time series
5. Generate unique_ids: `Election2024_Trump`, `Election2024_Biden`, etc.
6. Validate: Probabilities sum to ~1.0 (±0.05)
7. Write single CSV with 4 unique_id values

**Expected Output** (`timeseries.csv`):
```csv
unique_id,ds,y
Election2024_Trump,2025-11-05,0.42
Election2024_Biden,2025-11-05,0.35
Election2024_RFK,2025-11-05,0.18
Election2024_Other,2025-11-05,0.05
Election2024_Trump,2025-11-06,0.43
Election2024_Biden,2025-11-06,0.34
...
```

### Example 3: Data Quality Error Detection

**User Request**:
```
Transform data/bad_quality.json
```

**Expected Behavior**:
1. Read JSON
2. Detect platform
3. Transform data
4. Validation detects issues:
   - Missing dates: 2025-11-10 to 2025-11-15 (6 days)
   - Out-of-range value: y=1.23 on 2025-11-20 (>1.0)
5. Fail with detailed error message

**Expected Error**:
```
ERROR: Data quality validation failed

Issues detected:
1. Missing dates (6 gaps):
   - 2025-11-10 to 2025-11-15 (6 days missing)
   Suggestion: Fill gaps with interpolation or exclude this range

2. Out-of-range values (1 occurrence):
   - 2025-11-20: y=1.23 (must be 0≤y≤1)
   Suggestion: Check source data for corruption

Transformation aborted. Fix data quality issues and retry.
```

---

## 14. Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2025-12-05 | Initial PRD | Intent Solutions |

---

## 15. Approval

| Role | Name | Approval Date | Signature |
|------|------|---------------|-----------|
| Product Owner | Jeremy Longshore | 2025-12-05 | [Pending] |
| Tech Lead | Jeremy Longshore | 2025-12-05 | [Pending] |
| User Representative | Prediction Markets Community | TBD | [Pending] |

---

**Template maintained by**: Intent Solutions
**For**: Nixtla Skills Pack + Global Standard
**Last Updated**: 2025-12-05
