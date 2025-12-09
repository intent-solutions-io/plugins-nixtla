# Release v1.7.0

**Date**: 2025-12-09
**Type**: Minor (features + fixes, no breaking changes)
**Previous**: v1.6.0 (2025-12-08)

---

## What Changed

### Scripts (16 new, 6,023 lines)

Implemented all missing Python scripts for 5 production skills. These weren't just placeholders - real working code with CLI, error handling, and security controls.

**nixtla-experiment-architect** (3 scripts, 1,091 lines):
- `generate_config.py`: CLI config generator (YAML output)
- `scaffold_experiment.py`: Template processor for experiments
- `validate_experiment.py`: Data quality checker

**nixtla-prod-pipeline-generator** (3 scripts, 1,756 lines):
- `read_experiment.py`: Config parser
- `generate_pipeline.py`: Multi-platform pipeline generator (Airflow/Prefect/Cron)
- `add_monitoring.py`: Monitoring injection for existing pipelines

**nixtla-schema-mapper** (3 scripts, 1,344 lines):
- `analyze_schema.py`: Auto-detects columns for Nixtla format
- `generate_transform.py`: Creates transformation code
- `create_contract.py`: Schema contract docs

**nixtla-timegpt-finetune-lab** (6 scripts, 1,629 lines):
- Complete fine-tuning workflow from data prep to evaluation
- API submission, monitoring, comparison, metrics

**nixtla-timegpt-lab** (1 script, 203 lines):
- `detect_environment.py`: Library detection + API key check

### Security (10 fixes)

Found and fixed vulnerabilities before they became problems:

**Path Traversal** (3 scripts, CRITICAL):
- Users could access files outside allowed directories
- Fixed with `sanitize_path()` and directory whitelisting
- OWASP A01:2021 - Broken Access Control

**API Key Validation** (5 scripts, HIGH):
- Keys weren't being validated (length, format, placeholders)
- Added proper validation to prevent weak/test keys
- OWASP A07:2021 - Authentication Failures

**Code Injection** (2 scripts, CRITICAL):
- Template values weren't escaped, could inject arbitrary code
- Fixed with `escape_string_for_code()` and pattern detection
- OWASP A03:2021 - Injection

### Validator (4 fixes)

**Path Bug**: Was checking wrong directory (`skills-pack` instead of `003-skills`). Only found 1 of 8 skills.

**Description Formatting**: 6 skills had multiline YAML descriptions, flattened to single-line.

**First-Person Voice**: 2 skills had "I" and "My" in descriptions, changed to third-person.

**License Field**: Added MIT license to all 8 production skills.

**Result**: 8/8 skills now pass (exit code 0)

### Documentation (3 new files)

**097-AA-AUDT-appaudit-devops-playbook.md** (1,056 lines):
- Complete operational guide for DevOps engineers
- Architecture, CI/CD, health checks, troubleshooting
- Ready-to-use runbooks

**098-AA-AUDT-global-reality-check-audit.md**:
- Repository audit findings
- Identified validator bug and vaporware issues

**099-AA-GUIDE-skill-output-controls.md**:
- Explains where script outputs go
- How users control file locations
- CLI flags, redirection, defaults

### Directory Structure

Added letter prefixes to docs subdirectories to separate from numbered docs:
- `skills-schema` → `000a-skills-schema`
- `planned-skills` → `001a-planned-skills`
- `planned-plugins` → `002a-planned-plugins`
- `dev-planning-templates` → `004a-dev-planning-templates`

---

## Numbers

- **Commits**: 20 since v1.6.0
- **Files changed**: 226 (+10,024 / -3,713 lines)
- **Scripts created**: 16 with proper CLI, docs, error handling
- **Security fixes**: 10 (3 critical, 5 high, 2 critical)
- **Validation**: 8/8 pass (was 1/8)
- **Dev time**: ~2 hours (parallel agents)

---

## Technical

**Python**: 3.8+ compatible, all scripts have:
- Argparse CLI with `--help`
- Type hints and docstrings
- Error handling (specific exceptions, not bare `except`)
- Executable permissions

**Security**: OWASP Top 10 2021 compliance
- A01: Path traversal protection
- A03: Code injection prevention
- A07: API key validation

**Code Quality**: 7.8/10 (pre-security fixes, security-auditor review)

---

## Breaking Changes

None. All changes are additive.

---

## Upgrade Notes

1. Pull latest: `git pull origin main`
2. Check out tag: `git checkout v1.7.0`
3. Scripts are in `003-skills/.claude/skills/*/scripts/`
4. Run validator: `python scripts/validate_skills.py` (should see 8/8 pass)

---

## What's Next

The 8 production skills are complete and working. Security vulnerabilities fixed. Validator correctly finds and validates all skills.

---

**Version**: 1.7.0
**Tag**: v1.7.0
**Commit**: b855c78
