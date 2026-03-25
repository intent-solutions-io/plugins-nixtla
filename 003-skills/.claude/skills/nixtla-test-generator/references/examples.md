# Test Generator Examples

## Example 1: Generate Full Test Suite

```bash
python {baseDir}/scripts/generate_test_suite.py \
    --prd 000-docs/000a-planned-plugins/implemented/nixtla-roi-calculator/02-PRD.md \
    --output 005-plugins/nixtla-roi-calculator/tests \
    --plugin-name nixtla-roi-calculator
```

**Output**:
```
Parsed PRD: Found 5 functional requirements, 4 MCP tools
Generated tests/test_unit.py (15 test functions)
Generated tests/test_integration.py (4 MCP tool tests)
Generated tests/conftest.py (6 fixtures)
Generated tests/COVERAGE_MATRIX.md
Generated tests/README.md

Test Coverage: 19/19 requirements (100%)
```

## Example 2: Generate Unit Tests Only

Produce only unit tests without integration or MCP tool tests.

```bash
python {baseDir}/scripts/generate_test_suite.py \
    --prd /path/to/PRD.md \
    --output /path/to/tests \
    --unit-only
```

## Example 3: Dry Run (Preview Without Writing)

Preview what files and test counts would be generated without writing to disk.

```bash
python {baseDir}/scripts/generate_test_suite.py \
    --prd /path/to/PRD.md \
    --output /path/to/tests \
    --dry-run
```
