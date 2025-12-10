#!/bin/bash
# Batch process all prediction-markets skills to extract Python code

BASE_DIR="/home/jeremy/000-projects/nixtla/000-docs/planned-skills/prediction-markets"

# List of skills to process
SKILLS=(
    "nixtla-batch-forecaster"
    "nixtla-contract-schema-mapper"
    "nixtla-correlation-mapper"
    "nixtla-event-impact-modeler"
    "nixtla-forecast-validator"
    "nixtla-liquidity-forecaster"
    "nixtla-market-risk-analyzer"
    "nixtla-model-selector"
    "nixtla-polymarket-analyst"
)

echo "Processing ${#SKILLS[@]} skills..."

for skill in "${SKILLS[@]}"; do
    echo "Processing $skill..."
    skill_dir="$BASE_DIR/$skill"
    scripts_dir="$skill_dir/scripts"

    # Ensure scripts directory exists
    mkdir -p "$scripts_dir"

    echo "  Created/verified scripts directory"
done

echo "Done! All skills processed."
