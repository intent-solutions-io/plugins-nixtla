---
name: nixtla-universal-validator
description: "Validate Nixtla skills and plugins with deterministic evidence bundles and strict schema gates. Use when auditing changes or enforcing compliance. Trigger with 'run validation' or 'audit validators'."
allowed-tools: "Read,Write,Bash(python:*),Bash(bash:*),Bash(pytest:*)"
version: "1.0.1"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
compatible-with: claude-code
tags: [nixtla, validation, ci, compliance, testing]
---

# Nixtla Universal Validator

## Purpose

Produce deterministic, reviewable validation evidence (reports + JSON + logs) for a repo, plugin, or skill.

## Overview

This skill combines two layers:

- A **multi-phase subagent workflow** (for human-readable analysis + reconciliation)
- A **deterministic validator runner** (for ground-truth logs and machine-readable summaries)

Validation runs as a pipeline with deterministic gates:

- **Discover** what changed and what should be validated
- **Validate schemas/structure** (skills + plugins) using canonical repo validators
- **Run behavioral checks** (tests) when requested
- **Reconcile results** into a single evidence bundle with pass/fail and next actions

This pattern generalizes beyond Nixtla by swapping the check catalog (a list of commands + expected artifacts).

## Prerequisites

- Python 3.11+
- Repo validators available:
  - `004-scripts/validate_skills_v2.py`
  - `004-scripts/validate-all-plugins.sh`
- Optional for plugin validation: `jq`

## Instructions

### Step 1: Create a run directory

Use the built-in runner to create a timestamped evidence bundle under `reports/<project>/<timestamp>/`.

### Step 2: Pick a target scope

Choose one:

1. Repo root: validate everything
2. A plugin folder: `005-plugins/<plugin>`
3. A skill folder: `.claude/skills/<skill>` or `003-skills/.claude/skills/<skill>`

### Step 3: Run the deterministic validator suite

```bash
python {baseDir}/scripts/run_validator_suite.py \
  --target . \
  --project nixtla \
  --out reports/nixtla
```

List built-in profiles:

```bash
python {baseDir}/scripts/run_validator_suite.py \
  --list-profiles \
  --target . \
  --project nixtla \
  --out reports/nixtla
```

To validate a single plugin:
```bash
python {baseDir}/scripts/run_validator_suite.py \
  --target 005-plugins/nixtla-baseline-lab \
  --project nixtla-baseline-lab \
  --out reports/nixtla-baseline-lab
```

### Step 4: (Optional) Include tests

```bash
python {baseDir}/scripts/run_validator_suite.py \
  --target . \
  --project nixtla \
  --out reports/nixtla \
  --run-tests
```

### Step 4b: (Optional) Run an enterprise profile

```bash
python {baseDir}/scripts/run_validator_suite.py \
  --target . \
  --project nixtla \
  --out reports/nixtla \
  --profile enterprise \
  --fail-on-warn \
  --run-tests
```

### Step 5: (Optional) Use the multi-phase subagent workflow

Run phases in order using the prompts in `{baseDir}/agents/` and procedures in `{baseDir}/references/`.
Each phase must write a report file under the run directory and return strict JSON per the phase contract.

## Output

Each run creates a timestamped evidence bundle:

- `reports/<project>/<timestamp>/summary.json`
- `reports/<project>/<timestamp>/report.md`
- `reports/<project>/<timestamp>/checks/*.log`

## Error Handling

1. **Error**: Validator command not found  
   **Solution**: Confirm repo scripts exist and run from the repo root.

2. **Error**: Plugin validation fails due to `jq`  
   **Solution**: Install `jq` or run only skill validation.

3. **Error**: Tests fail after schema passes  
   **Solution**: Treat this as a behavioral regression; fix tests or code, then re-run.

## Examples

Common validations:

```bash
# Strict schema/structure gates
python 004-scripts/validate_skills_v2.py --fail-on-warn
bash 004-scripts/validate-all-plugins.sh .
```

Generate an evidence bundle (profile-driven):

```bash
# Generate a single evidence bundle for a PR
python {baseDir}/scripts/run_validator_suite.py \
  --target . \
  --project pr-1234 \
  --out reports/pr-1234 \
  --run-tests
```

## Resources

- Subagent orchestration pattern: `000-docs/000a-planned-skills/templates/verification-pipeline/README.md`
- Canonical skills validator: `004-scripts/validate_skills_v2.py`
- Canonical plugin validator: `004-scripts/validate-all-plugins.sh`
- Subagent prompts: `{baseDir}/agents/`
- Phase procedures: `{baseDir}/references/`
