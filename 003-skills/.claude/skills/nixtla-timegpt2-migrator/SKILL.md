---
name: nixtla-timegpt2-migrator
description: "Analyze and transform code for TimeGPT-1 to TimeGPT-2 migration. Use when upgrading TimeGPT version, migrating client libraries, or updating API calls. Trigger with 'migrate to TimeGPT-2', 'upgrade TimeGPT', or 'TimeGPT migration'."
allowed-tools: "Read,Write,Edit,Glob,Grep"
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
compatible-with: claude-code
tags: [nixtla, time-series, migration, timegpt, upgrade, refactoring]
---

# Nixtla TimeGPT-2 Migrator

Automates the migration process from TimeGPT-1 to TimeGPT-2, identifying compatibility issues and generating updated code.

## Overview

This skill evaluates existing TimeGPT-1 workflows for compatibility with TimeGPT-2. It identifies potential breaking changes and suggests necessary code modifications, employs API checks and data schema validation, provides updated code snippets and configuration examples, and generates a migration report summarizing all changes required.

**When to use**: Upgrading from the legacy TimeGPT-1 SDK to the current NixtlaClient-based TimeGPT-2 API, or auditing a codebase for deprecated API patterns.

**Trigger phrases**: "migrate to TimeGPT-2", "upgrade TimeGPT", "TimeGPT migration", "update Nixtla client", "fix deprecated TimeGPT calls".

## Prerequisites

**Tools**: Read, Write, Edit, Glob, Grep

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install nixtla pandas matplotlib statsforecast pyyaml
```

## Instructions

### Step 1: Analyze Codebase

Scan the codebase for TimeGPT-1 API usage patterns using the analysis script.

**Script**: `{baseDir}/scripts/analyze_codebase.py`

```bash
python {baseDir}/scripts/analyze_codebase.py /path/to/your/codebase
```

The script searches for `timegpt.forecast()`, `timegpt.create_model()`, `timegpt.load_data()`, and `timegpt.train()` calls. It produces `analysis_report.txt` listing all TimeGPT-1 usage instances with file paths and line numbers.

### Step 2: Run Compatibility Check

Execute the compatibility checker to validate data schema and identify unsupported features.

**Script**: `{baseDir}/scripts/compatibility_check.py`

```bash
python {baseDir}/scripts/compatibility_check.py --data sample_data.csv
```

The script validates data schema (unique_id, ds, y columns), data types (datetime for ds, numeric for y), API availability, and unsupported TimeGPT-1 features. It produces `migration_report.txt` with a compatibility assessment.

### Step 3: Apply Migration Changes

Use the migration script to update your codebase with TimeGPT-2 compatible code.

**Script**: `{baseDir}/scripts/apply_migration.py`

```bash
python {baseDir}/scripts/apply_migration.py main.py
```

The script performs automatic replacements:
- `timegpt.forecast()` -> `client.forecast()`
- `from timegpt import TimeGPT` -> `from nixtla import NixtlaClient`
- `timegpt = TimeGPT()` -> `client = NixtlaClient(api_key=...)`
- Removes deprecated `timegpt.create_model()` calls
- Updates data schema conversion code

**Important**: Review all changes before committing to version control. The migration script creates a backup of each modified file.

### Step 4: Generate TimeGPT-2 Configuration

Create a TimeGPT-2 configuration file with recommended settings.

**Script**: `{baseDir}/scripts/generate_config.py`

```bash
python {baseDir}/scripts/generate_config.py
```

Produces `timegpt2_config.yaml` with configuration parameters including API key reference, model name, frequency, and data format settings.

## Output

- **analysis_report.txt**: Summary of all TimeGPT-1 usage found in the codebase with file locations
- **migration_report.txt**: Compatibility assessment and migration plan with risk ratings
- **updated_codebase/**: Modified source code with TimeGPT-2 compatible calls (after applying changes)
- **timegpt2_config.yaml**: Configuration file for TimeGPT-2 with recommended defaults

## Error Handling

| Error | Solution |
|-------|----------|
| TimeGPT-1 API endpoint not found | Ensure TimeGPT-1 API is accessible or skip API validation step |
| Incompatible data schema | Update data input format to match TimeGPT-2 requirements (unique_id, ds, y) |
| Missing API Key | Set the `NIXTLA_TIMEGPT_API_KEY` environment variable |
| Unsupported TimeGPT-1 feature | Refactor code to use equivalent TimeGPT-2 functionality |
| File not found during migration | Verify the file path exists before running the migration script |

## Examples

See [examples](references/examples.md) for detailed usage patterns including basic migration before/after comparisons, configuration updates, and full workflow walkthroughs.

## Resources

- TimeGPT-2 API documentation: https://docs.nixtla.io/
- Migration guide: https://docs.nixtla.io/docs/migration-guide
- NixtlaClient reference: https://nixtlaverse.nixtla.io/nixtla/
- Scripts: `{baseDir}/scripts/` directory contains all migration tools
