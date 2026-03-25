---
name: nixtla-test-generator
description: "Generate comprehensive pytest test suites from PRD functional requirements with fixtures, parameterization, and coverage tracking. Use when creating tests for new plugins, validating PRD requirements, or scaffolding test infrastructure. Trigger with 'generate tests from PRD', 'create test suite', or 'scaffold pytest tests'."
allowed-tools: "Write,Read,Glob,Bash(python:*),Bash(pytest:*)"
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
compatible-with: claude-code
tags: [nixtla, testing, pytest, code-generation, PRD, test-automation]
---

# Nixtla Test Generator

Generate production-ready pytest test suites from PRD (Product Requirements Document) functional requirements, ensuring comprehensive test coverage for Nixtla plugins.

## Overview

This skill automates the tedious process of creating test infrastructure for new plugins. It parses PRD documents to extract functional requirements (FR-X items), generates pytest test files with proper structure (test_unit.py, test_integration.py), creates pytest fixtures for common test scenarios, includes parameterized tests for multiple input scenarios, generates conftest.py with shared fixtures, and creates test documentation with a coverage matrix mapping each test to its requirement.

**When to use**: Starting test development for a new plugin, ensuring every PRD functional requirement has test coverage, or bootstrapping test infrastructure with consistent patterns.

**Trigger phrases**: "generate tests from PRD", "create test suite", "scaffold pytest tests", "generate test coverage", "build test infrastructure".

**Key Benefits**:
- Reduces test scaffolding time from 2-3 hours to 2 minutes
- Ensures consistent test structure across all plugins
- Auto-generates test stubs for every functional requirement
- Includes best practices (fixtures, markers, parameterization)

## Prerequisites

- PRD document with structured functional requirements (FR-X format)
- Python 3.8+ with pytest installed
- Target plugin directory structure exists

## Instructions

### Step 1: Parse PRD for Requirements

The script automatically reads the PRD markdown file, extracts all functional requirements (FR-1, FR-2, etc.), identifies MCP tools from FR-X sections, and captures acceptance criteria from user stories.

**Expected PRD Structure**:
```markdown
## Functional Requirements

### FR-1: Feature Name
- Requirement detail 1
- Requirement detail 2

### FR-2: Another Feature
- More requirements
```

### Step 2: Generate Test Structure

Run the generator to create the full test suite:

```bash
python {baseDir}/scripts/generate_test_suite.py \
    --prd 000-docs/000a-planned-plugins/implemented/nixtla-roi-calculator/02-PRD.md \
    --output 005-plugins/nixtla-roi-calculator/tests \
    --plugin-name nixtla-roi-calculator
```

See [test patterns reference](references/test-patterns.md) for generated file templates (test_unit.py, test_integration.py, conftest.py) and the coverage matrix format.

### Step 3: Add Pytest Markers

Generated tests include appropriate markers for selective execution:
- `@pytest.mark.unit` - Fast, isolated tests (< 100ms each)
- `@pytest.mark.integration` - Tests with external dependencies
- `@pytest.mark.slow` - Long-running tests (> 1 second)
- `@pytest.mark.parametrize` - Multiple input scenarios

### Step 4: Run Generated Tests

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests with verbose output
pytest tests/ -v

# Run with coverage reporting
pytest tests/ --cov=plugin_name --cov-report=html

# Run only unit tests
pytest tests/ -m unit
```

## Output

1. **tests/test_unit.py** - Unit tests for all FR-X requirements with happy path and error handling
2. **tests/test_integration.py** - Integration tests for MCP tools with async/await patterns
3. **tests/conftest.py** - Shared pytest fixtures for sample data, mock API clients, and test setup
4. **tests/COVERAGE_MATRIX.md** - Test-to-requirement mapping ensuring complete coverage
5. **tests/README.md** - Test suite documentation with run instructions

## Error Handling

| Error | Solution |
|-------|----------|
| PRD not found | Verify PRD path and ensure the file exists |
| No FR-X sections found | Ensure PRD has `### FR-X: Title` format sections |
| Generated test syntax errors | Run `black` formatter on generated files |
| Import errors in tests | Update import paths to match actual module structure |

## Examples

See [examples](references/examples.md) for detailed usage patterns including full suite generation, unit-only mode, and dry run previews.

## Resources

- **Script**: `{baseDir}/scripts/generate_test_suite.py`
- **Template**: `{baseDir}/assets/templates/pytest_template.py`
- **Example PRD**: `000-docs/000a-planned-plugins/implemented/nixtla-roi-calculator/02-PRD.md`
- **Pytest Docs**: https://docs.pytest.org/
- **Coverage Guide**: https://coverage.readthedocs.io/

**Related Skills**:
- `nixtla-prd-to-code` - Transform PRD into implementation tasks
- `nixtla-plugin-scaffolder` - Generate plugin structure from PRD
