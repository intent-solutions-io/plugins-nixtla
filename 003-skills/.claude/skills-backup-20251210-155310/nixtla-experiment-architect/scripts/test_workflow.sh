#!/bin/bash
# Test workflow for nixtla-experiment-architect scripts
# This script demonstrates the complete workflow with sample data

set -e  # Exit on error

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TEST_DIR="${SCRIPT_DIR}/../test_output"

echo "========================================================"
echo "Nixtla Experiment Architect - Workflow Test"
echo "========================================================"
echo ""

# Clean up previous test output
if [ -d "$TEST_DIR" ]; then
    echo "Cleaning up previous test output..."
    rm -rf "$TEST_DIR"
fi

mkdir -p "$TEST_DIR/data"
echo "Created test directory: $TEST_DIR"
echo ""

# Create sample CSV data
echo "Step 1: Creating sample data..."
cat > "$TEST_DIR/data/sample_sales.csv" << EOF
date,store_id,sales,temperature
2024-01-01,store_1,1500,15.5
2024-01-02,store_1,1650,16.2
2024-01-03,store_1,1720,15.8
2024-01-04,store_1,1850,17.1
2024-01-05,store_1,2100,18.3
2024-01-06,store_1,2300,19.0
2024-01-07,store_1,2200,18.5
2024-01-08,store_1,1550,15.9
2024-01-09,store_1,1680,16.4
2024-01-10,store_1,1750,16.8
2024-01-11,store_1,1880,17.5
2024-01-12,store_1,2150,18.8
2024-01-13,store_1,2350,19.5
2024-01-14,store_1,2250,19.1
2024-01-15,store_1,1600,16.2
2024-01-16,store_1,1700,16.9
2024-01-17,store_1,1800,17.3
2024-01-18,store_1,1950,18.1
2024-01-19,store_1,2200,19.2
2024-01-20,store_1,2400,20.0
2024-01-21,store_1,2300,19.6
2024-01-22,store_1,1650,16.5
2024-01-23,store_1,1750,17.0
2024-01-24,store_1,1850,17.6
2024-01-25,store_1,2000,18.4
2024-01-26,store_1,2250,19.3
2024-01-27,store_1,2450,20.2
2024-01-28,store_1,2350,19.8
EOF
echo "  Created: $TEST_DIR/data/sample_sales.csv (28 rows)"
echo ""

# Step 2: Generate configuration
echo "Step 2: Generating configuration..."
python3 "${SCRIPT_DIR}/generate_config.py" \
    --data "$TEST_DIR/data/sample_sales.csv" \
    --target sales \
    --horizon 7 \
    --freq D \
    --id_col store_id \
    --ds_col date \
    --output "$TEST_DIR/config.yml"

if [ $? -eq 0 ]; then
    echo ""
    echo "Configuration generated successfully!"
    echo ""
else
    echo "Error generating configuration"
    exit 1
fi

# Step 3: Validate configuration
echo "Step 3: Validating configuration and data..."
python3 "${SCRIPT_DIR}/validate_experiment.py" \
    --config "$TEST_DIR/config.yml" \
    --verbose

if [ $? -eq 0 ]; then
    echo ""
    echo "Validation passed!"
    echo ""
else
    echo "Validation failed"
    exit 1
fi

# Step 4: Scaffold experiment
echo "Step 4: Scaffolding experiment..."
python3 "${SCRIPT_DIR}/scaffold_experiment.py" \
    --config "$TEST_DIR/config.yml" \
    --output "$TEST_DIR/experiments.py"

if [ $? -eq 0 ]; then
    echo ""
    echo "Experiment scaffolded successfully!"
    echo ""
else
    echo "Error scaffolding experiment"
    exit 1
fi

# Summary
echo "========================================================"
echo "Workflow Test Complete!"
echo "========================================================"
echo ""
echo "Generated files:"
echo "  - $TEST_DIR/data/sample_sales.csv"
echo "  - $TEST_DIR/config.yml"
echo "  - $TEST_DIR/experiments.py"
echo ""
echo "To run the experiment (requires Nixtla packages):"
echo "  cd $TEST_DIR"
echo "  python experiments.py"
echo ""
echo "To clean up test files:"
echo "  rm -rf $TEST_DIR"
echo ""
