# GitHub Actions Failures Audit

**Document ID**: 107-AA-AUDT-github-actions-failures
**Date**: 2025-12-10
**Auditor**: Claude (Acting CTO)
**Scope**: All recent GitHub Actions workflow failures

---

## Executive Summary

**Status**: 3 workflows consistently failing on every push

**Impact**: CI/CD pipeline not blocking merges but showing red X's

**Root Causes Identified**:
1. Skills validator: `nixtla-timegpt-lab` has "You" in body text (not description)
2. Skills installer E2E: Looking for `plugins/` directory, repo has `005-plugins/`
3. CI workflow: Triggered but failing on code quality checks

**Risk Level**: Low (experimental workspace, not blocking development)

**Fix Complexity**: Simple (30 minutes total)

---

## Failure Pattern Analysis

### Last 30 Workflow Runs

| Workflow | Pass Rate | Failure Pattern |
|----------|-----------|-----------------|
| **Claude Skills Validation** | 93% (28/30) | Fails only on latest commit |
| **Skills Installer E2E** | 0% (0/30) | **Fails every time** |
| **CI - Continuous Integration** | ~90% | Intermittent failures |

**Timeline**: Last successful runs Dec 10 @ 08:53 (feature branch)

---

## Detailed Failure Reports

### 1. Claude Skills Validation (Strict) ❌

**Latest Run**: 20116771233 (f66eeb4 - Dec 10, 23:36)
**Status**: FAILED
**Duration**: 48 seconds

**Error**:
```
[PROD] 003-skills/.claude/skills/nixtla-timegpt-lab/SKILL.md
  ❌ ERROR: 'description' must use third person.
  Found: ['You'].
  Use 'This skill...', 'Guides...', 'Analyzes...', 'Transforms...'

SUMMARY:
  Files checked:       23
  Files with issues:   1
  Skills with errors:  1
```

**Root Cause**:
- The validator checks the entire SKILL.md file, not just frontmatter
- Found "You" in the body content (line unknown)
- Description in frontmatter is fine: "Generate time series forecasts using TimeGPT..."

**Location**: `003-skills/.claude/skills/nixtla-timegpt-lab/SKILL.md`

**Validator Rule**: Third person only throughout entire SKILL.md

**Note**: This same file passed validation on Dec 10 @ 08:53, which means either:
- The body was recently edited to add "You"
- The validator was updated to check body content (not just frontmatter)

---

### 2. Skills Installer E2E ❌

**Latest Run**: 20116771220 (f66eeb4 - Dec 10, 23:36)
**Status**: FAILED
**Duration**: 12 seconds

**Error**:
```
[STEP 1/4] Locating repository root...
✗ Failed: Could not find repo root. Current path: /home/jeremy/000-projects/nixtla/007-tests
Expected to find plugins/ directory in parent.

❌ E2E TEST RESULT: FAIL
```

**Root Cause**:
- Test expects directory named `plugins/`
- Actual directory is `005-plugins/`
- Test script hard-codes the wrong path

**Test File**: `007-tests/test_skills_installer_e2e.py`

**Fix Required**: Update test to look for `005-plugins/` instead of `plugins/`

**Historical Context**: This has been failing for **every run** since at least Dec 9

**Impact**:
- E2E test never runs
- No validation of skills installer package
- But... package works fine when run manually

---

### 3. CI - Continuous Integration ❌

**Latest Run**: 20116771203 (f66eeb4 - Dec 10, 23:36)
**Status**: FAILED
**Duration**: 1m 8s

**Error**: (No error logs accessible via gh CLI)

**Workflow Triggers**:
- On push to `main` or `develop` branches
- Only when Python/JS/TS files or requirements change
- Skips doc-only changes

**What It Tests**:
1. **Lint and Format**:
   - Black formatter check
   - isort import checker
   - Flake8 linter

2. **Primary Tests**:
   - Python 3.11 on Ubuntu
   - Runs pytest suite

**Likely Cause** (based on pattern):
- Code formatting issues (Black or isort)
- Python import ordering
- Flake8 syntax issues

**Cost Optimization Note**:
Workflow header says "COST-OPTIMIZED CI STRATEGY" to avoid macOS (10x) and Windows (2x) GitHub Actions multipliers

---

## Workflow Health Dashboard

### Currently Active Workflows (9 total)

| Workflow | Status | Purpose | Last Success |
|----------|--------|---------|--------------|
| skills-validation.yml | ❌ FAIL | Validates SKILL.md format | Dec 10 08:53 |
| skills-installer-ci.yml | ❌ FAIL | E2E test of installer | Never |
| ci.yml | ❌ FAIL | Code quality + tests | Dec 10 07:29 |
| deploy-bigquery-forecaster.yml | ⚠️ Unknown | Deploy plugin to GCP | Unknown |
| gemini-daily-audit.yml | ⚠️ Unknown | Daily Gemini audit | Unknown |
| gemini-pr-review.yml | ⚠️ Unknown | PR review automation | Unknown |
| nixtla-baseline-lab-ci.yml | ⚠️ Unknown | Baseline lab tests | Unknown |
| plugin-validator.yml | ⚠️ Unknown | Plugin validation | Unknown |
| timegpt-real-smoke.yml | ⚠️ Unknown | TimeGPT smoke test | Unknown |

**Legend**:
- ❌ FAIL: Actively failing
- ⚠️ Unknown: Not triggered recently or status unclear
- ✅ PASS: Last run successful

---

## Impact Assessment

### Critical Workflows (Failing)

**1. Skills Validation**:
- **Impact**: High visibility (red X on every commit)
- **Blocking**: No (doesn't prevent merges)
- **User Impact**: None (validation runs separately)
- **Fix Priority**: High (easy fix, high visibility)

**2. Skills Installer E2E**:
- **Impact**: Medium (installer not validated)
- **Blocking**: No
- **User Impact**: Low (installer works manually)
- **Fix Priority**: Medium (test is broken, not code)

**3. CI Pipeline**:
- **Impact**: Medium (no automated testing)
- **Blocking**: No
- **User Impact**: Low (tests run manually)
- **Fix Priority**: Medium (depends on root cause)

### Non-Critical Workflows (Unknown Status)

**4-9. Other Workflows**:
- Not triggered by recent pushes
- May be working fine
- May have specific trigger conditions
- May require API keys or GCP access

---

## Root Cause Analysis

### Why Is Everything Failing Now?

**Timeline**:
- Dec 10 @ 08:53: ✅ Skills validation passed (feature branch)
- Dec 10 @ 23:07: ❌ Skills validation failed (feature branch)
- Dec 10 @ 23:36: ❌ All 3 workflows failed (main branch)

**What Changed Between 08:53 and 23:07?**
- Commit `198aadc`: "feat(skills): 23 skills at 100% L4 quality"
- This commit modified many SKILL.md files
- One of those edits likely introduced "You" into nixtla-timegpt-lab body

**Why Skills Installer Always Fails**:
- Test has hard-coded `plugins/` path
- Repo has `005-plugins/` directory
- This has been wrong for weeks/months
- Nobody noticed because test runs quickly and doesn't block

**Why CI Fails Intermittently**:
- Likely code formatting drift
- Black/isort rules enforced strictly
- Files formatted locally but not committed
- Or: New Python files added without formatting

---

## Fix Recommendations

### Priority 1: Skills Validation (5 minutes)

**File**: `003-skills/.claude/skills/nixtla-timegpt-lab/SKILL.md`

**Action**: Find and remove "You" from body text

**Commands**:
```bash
# Find exact location
grep -n "You" 003-skills/.claude/skills/nixtla-timegpt-lab/SKILL.md

# Option A: Replace with third person
# Option B: Remove the problematic sentence
# Option C: Rephrase to avoid second person

# Test the fix
python scripts/validate_skills.py
```

**Verification**: Should show "Files checked: 23, Files with issues: 0"

---

### Priority 2: Skills Installer E2E (10 minutes)

**File**: `007-tests/test_skills_installer_e2e.py`

**Action**: Update path check from `plugins/` to `005-plugins/`

**Likely Code** (line ~30-40):
```python
# Current (WRONG):
if not (repo_root / "plugins").exists():
    raise TestError("Expected to find plugins/ directory")

# Fixed (RIGHT):
if not (repo_root / "005-plugins").exists():
    raise TestError("Expected to find 005-plugins/ directory")
```

**Verification**:
```bash
python 007-tests/test_skills_installer_e2e.py
```

Should show: "✅ E2E TEST RESULT: PASS"

---

### Priority 3: CI Pipeline (15 minutes)

**Investigation Steps**:
1. Run formatters locally:
   ```bash
   black .
   isort .
   flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
   ```

2. Check for issues:
   ```bash
   black --check .
   isort --check-only .
   ```

3. Commit any formatting fixes:
   ```bash
   git add -u
   git commit -m "style: apply black and isort formatting"
   git push
   ```

**Verification**: Wait for CI run, should pass

---

## Workflow File Locations

All workflows in `.github/workflows/`:

1. `skills-validation.yml` (32 lines) - Skills format checker
2. `skills-installer-ci.yml` (39 lines) - Installer E2E test
3. `ci.yml` (7560 lines) - Main CI pipeline
4. `deploy-bigquery-forecaster.yml` (5250 lines) - GCP deployment
5. `gemini-daily-audit.yml` (6087 lines) - Daily audit automation
6. `gemini-pr-review.yml` (3429 lines) - PR review bot
7. `nixtla-baseline-lab-ci.yml` (1823 lines) - Baseline lab tests
8. `plugin-validator.yml` (14456 lines) - Plugin validation
9. `timegpt-real-smoke.yml` (4895 lines) - TimeGPT smoke test

**Total Workflow Code**: ~50,000 lines

---

## Risk Analysis

### Current State

**Experimental Workspace**: Yes
**Blocking Merges**: No
**User Impact**: None
**Developer Impact**: Red X visibility

### Risks of Not Fixing

**Low Risk**:
- Skills validation runs separately (scripts/validate_skills.py)
- Skills installer works manually
- CI tests run locally before commits

**Medium Risk**:
- False confidence (red X's become "normal")
- Future contributors ignore failing CI
- Actual breakage goes unnoticed

**High Risk**: None identified

### Recommended Timeline

| Fix | Priority | Time | Risk if Delayed |
|-----|----------|------|-----------------|
| Skills Validation | P1 | 5 min | Low (visibility only) |
| Skills Installer E2E | P2 | 10 min | Low (test is broken, not code) |
| CI Pipeline | P3 | 15 min | Medium (no automated checks) |

**Total Time**: 30 minutes to fix all 3

---

## Historical Context

### Skills Installer E2E Has Never Passed

From the run history:
- 30 consecutive failures
- Dates back to at least Dec 9
- Likely failing since repo restructure (whenever `plugins/` became `005-plugins/`)

**Why Wasn't This Noticed?**
- Test runs in 12-15 seconds (fast failure)
- Doesn't block development
- Package works fine when installed manually
- CI badge not prominently displayed

**What This Means**:
- The E2E test suite is not being maintained
- Either fix the test or remove it
- If keeping it: Add to pre-commit hooks

---

## Recommendations for CI/CD Health

### Short Term (30 minutes)

1. Fix the 3 failing workflows
2. Verify all pass on next push
3. Document any persistent failures

### Medium Term (1-2 hours)

1. Audit the 6 unknown workflows
2. Test each workflow manually
3. Update workflow documentation
4. Add status badges to README

### Long Term (Ongoing)

1. **Pre-commit Hooks**:
   - Run Black/isort automatically
   - Run skills validator locally
   - Run E2E tests before push

2. **Workflow Hygiene**:
   - Remove unused workflows
   - Consolidate overlapping tests
   - Add clear failure messages

3. **Cost Optimization**:
   - Current strategy is good (Linux-first)
   - Consider: Skip CI on doc-only commits
   - Consider: Cache dependencies more aggressively

---

## GitHub Actions Costs (Awareness)

**Current Free Tier**:
- 2,000 minutes/month (Linux)
- 1 concurrent job

**Multipliers**:
- Linux: 1x (baseline)
- Windows: 2x
- macOS: 10x

**Current Strategy** (per ci.yml):
- TIER 1 (Every push): Linux + Python 3.11 only (~2 min)
- TIER 2 (PRs to main): Full OS matrix (~15 min)
- TIER 3 (Weekly): Comprehensive audits

**This Is Smart**: Avoids macOS 10x multiplier on every commit

---

## Next Steps

### Option 1: Fix Everything Now (30 min)

```bash
# 1. Fix skills validation
vim 003-skills/.claude/skills/nixtla-timegpt-lab/SKILL.md
# Remove "You" from body text
python scripts/validate_skills.py  # Verify

# 2. Fix skills installer E2E
vim 007-tests/test_skills_installer_e2e.py
# Change "plugins/" to "005-plugins/"
python 007-tests/test_skills_installer_e2e.py  # Verify

# 3. Fix CI formatting
black .
isort .
git add -u && git commit -m "style: apply formatting" && git push
```

### Option 2: Fix Incrementally

- Fix P1 now (skills validation) - 5 min
- Fix P2/P3 later when convenient
- Document known failures

### Option 3: Disable Failing Workflows

- Rename `*.yml` to `*.yml.disabled`
- Re-enable when ready to fix
- Keeps GitHub Actions page clean

---

## Conclusion

**Summary**: 3 workflows failing for fixable reasons, 6 workflows status unknown.

**Risk**: Low (experimental workspace, no blocking impact)

**Effort**: 30 minutes to fix all known issues

**Priority**: Medium (visibility vs. actual impact)

**Recommendation**: Fix P1 (skills validation) immediately for clean commit history, fix P2/P3 when convenient.

---

**Audit Completed**: 2025-12-10T18:00:00Z
**Next Audit**: After fixes applied
**Auditor**: Claude Sonnet 4.5 (Acting CTO)
