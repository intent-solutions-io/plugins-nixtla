#!/bin/bash
# Nixtla Release Validation - Test Results Analysis Script
# Purpose: Run pytest suite and output structured JSON verification report
# Usage: ./analyze_test_results.sh <repo_path> <output_dir>

set -euo pipefail

REPO_PATH="${1:-}"
OUTPUT_DIR="${2:-}"

# Validation
if [ -z "$REPO_PATH" ] || [ -z "$OUTPUT_DIR" ]; then
    echo "Usage: $0 <repo_path> <output_dir>" >&2
    echo "Example: $0 /home/jeremy/000-projects/nixtla ./reports/20251222_170000" >&2
    exit 1
fi

if [ ! -d "$REPO_PATH" ]; then
    echo "Error: Repository path does not exist: $REPO_PATH" >&2
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

echo "=== Nixtla Release Validation - Test Analysis ==="
echo "Repository: $REPO_PATH"
echo "Output: $OUTPUT_DIR"
echo ""

cd "$REPO_PATH"

# Check if pytest is available
if ! command -v pytest &> /dev/null; then
    echo "Error: pytest not found. Install with: pip install pytest pytest-cov pytest-json-report" >&2
    exit 1
fi

# Run full test suite with JSON output
echo "Running pytest suite..."
pytest tests/ \
  --cov \
  --json-report \
  --json-report-file="$OUTPUT_DIR/pytest-results.json" \
  -v \
  --tb=short \
  2>&1 | tee "$OUTPUT_DIR/pytest-output.log" || true

# Check if pytest results exist
if [ ! -f "$OUTPUT_DIR/pytest-results.json" ]; then
    echo "Error: pytest did not generate JSON report" >&2
    exit 1
fi

# Parse test results
echo ""
echo "Parsing test results..."

TOTAL=$(jq -r '.summary.total // 0' "$OUTPUT_DIR/pytest-results.json")
PASSED=$(jq -r '.summary.passed // 0' "$OUTPUT_DIR/pytest-results.json")
FAILED=$(jq -r '.summary.failed // 0' "$OUTPUT_DIR/pytest-results.json")
SKIPPED=$(jq -r '.summary.skipped // 0' "$OUTPUT_DIR/pytest-results.json")

# Generate coverage report if available
COVERAGE="null"
if command -v coverage &> /dev/null; then
    if coverage json -o "$OUTPUT_DIR/coverage.json" 2>/dev/null; then
        COVERAGE=$(jq '.totals.percent_covered' "$OUTPUT_DIR/coverage.json")
    fi
fi

# Extract failed test node IDs
FAILED_TESTS=$(jq -r '.tests[] | select(.outcome == "failed") | .nodeid' "$OUTPUT_DIR/pytest-results.json" 2>/dev/null | jq -R . | jq -s . || echo "[]")

# Create structured verification report
cat > "$OUTPUT_DIR/phase4-verification-report.json" <<EOF
{
  "metadata": {
    "phase": 4,
    "script": "analyze_test_results.sh",
    "timestamp": "$(date -Iseconds)",
    "repo": "$REPO_PATH"
  },
  "results": {
    "tests_run": $TOTAL,
    "tests_passed": $PASSED,
    "tests_failed": $FAILED,
    "tests_skipped": $SKIPPED,
    "coverage_pct": $COVERAGE,
    "failed_tests": $FAILED_TESTS
  },
  "prediction_comparison": {
    "note": "Phase 5 agent will compare these results against Phase 2 predictions",
    "predictions_confirmed": [],
    "predictions_revised": [],
    "unexpected_failures": []
  }
}
EOF

# Display summary
echo ""
echo "=== Test Results Summary ==="
echo "Total tests: $TOTAL"
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo "Skipped: $SKIPPED"
if [ "$COVERAGE" != "null" ]; then
    echo "Coverage: ${COVERAGE}%"
fi
echo ""
echo "Verification report: $OUTPUT_DIR/phase4-verification-report.json"

# Exit with appropriate code
if [ "$FAILED" -gt 0 ]; then
    echo ""
    echo "⚠️  WARNING: $FAILED test(s) failed"
    exit 0  # Don't fail the script, just report
else
    echo ""
    echo "✅ All tests passed!"
    exit 0
fi
