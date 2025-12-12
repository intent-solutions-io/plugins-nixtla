#!/usr/bin/env python3
"""
Overnight Skill Generator - Vertex AI Gemini (ADC Auth)
=======================================================
Generates SKILL.md files for Nixtla skills using Vertex AI with Application Default Credentials.

NO API KEY NEEDED - Uses gcloud ADC authentication.

Standards Compliance:
- 6767-n-DR-GUID-claude-skills-authoring-guide.md
- 6767-m-DR-STND-claude-skills-frontmatter-schema.md

Usage:
    python scripts/overnight_skill_generator.py
    python scripts/overnight_skill_generator.py --resume nixtla-anomaly-detector
    python scripts/overnight_skill_generator.py --dry-run

Prerequisites:
    pip install google-cloud-aiplatform
    gcloud auth application-default login

Author: Intent Solutions
Date: 2025-12-08
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import vertexai
from vertexai.generative_models import GenerativeModel

# ==============================================================================
# CONFIGURATION
# ==============================================================================

REPO_ROOT = Path(__file__).parent.parent
PLANNED_SKILLS_DIR = REPO_ROOT / "000-docs" / "planned-skills"
PROGRESS_FILE = REPO_ROOT / "scripts" / ".skill_generator_progress.json"
LOG_FILE = REPO_ROOT / "scripts" / "skill_generator.log"

# Google Cloud config (uses ADC - no API key needed)
PROJECT_ID = os.environ.get("PROJECT_ID", "pipelinepilot-prod")
LOCATION = os.environ.get("LOCATION", "us-central1")

# Timing (Vertex AI has higher limits than free tier)
PAUSE_BETWEEN_SKILLS = 10
PAUSE_ON_ERROR = 60
MAX_RETRIES = 3

# ==============================================================================
# SKILL DEFINITIONS - 21 skills across 3 categories
# ==============================================================================

SKILLS_TO_GENERATE = {
    "core-forecasting": [
        {
            "name": "nixtla-anomaly-detector",
            "description": "Zero-shot anomaly detection using TimeGPT. Identifies outliers, level shifts, trend breaks.",
            "domain": "Anomaly Detection",
            "apis": ["TimeGPT API"],
            "tools": "Read,Write,Bash,Glob,Grep",
        },
        {
            "name": "nixtla-exogenous-integrator",
            "description": "Incorporates external variables (holidays, weather, events) into TimeGPT forecasts.",
            "domain": "Feature Engineering",
            "apis": ["TimeGPT API"],
            "tools": "Read,Write,Bash,Glob,Grep",
        },
        {
            "name": "nixtla-uncertainty-quantifier",
            "description": "Generates prediction intervals and confidence bands using conformal prediction.",
            "domain": "Risk Assessment",
            "apis": ["TimeGPT API", "StatsForecast"],
            "tools": "Read,Write,Bash,Glob,Grep",
        },
        {
            "name": "nixtla-cross-validator",
            "description": "Performs rigorous time series cross-validation with expanding/sliding windows.",
            "domain": "Model Evaluation",
            "apis": ["TimeGPT API", "StatsForecast"],
            "tools": "Read,Write,Bash,Glob,Grep",
        },
        {
            "name": "nixtla-timegpt2-migrator",
            "description": "Guides migration from TimeGPT-1 to TimeGPT-2 with compatibility checks.",
            "domain": "Migration",
            "apis": ["TimeGPT API"],
            "tools": "Read,Write,Edit,Glob,Grep",
        },
    ],
    "prediction-markets": [
        {
            "name": "nixtla-polymarket-analyst",
            "description": "Analyzes Polymarket contracts. Fetches odds, transforms to time series, forecasts prices.",
            "domain": "Prediction Markets",
            "apis": ["Polymarket API", "TimeGPT API"],
            "tools": "Read,Write,Bash,Glob,Grep,WebFetch",
        },
        {
            "name": "nixtla-arbitrage-detector",
            "description": "Scans cross-platform pricing discrepancies between Polymarket and Kalshi.",
            "domain": "Arbitrage Detection",
            "apis": ["Polymarket API", "Kalshi API"],
            "tools": "Read,Write,Bash,Glob,Grep,WebFetch",
        },
        {
            "name": "nixtla-contract-schema-mapper",
            "description": "Transforms prediction market data to Nixtla format (unique_id, ds, y).",
            "domain": "Data Transformation",
            "apis": [],
            "tools": "Read,Write,Edit,Glob,Grep",
        },
        {
            "name": "nixtla-batch-forecaster",
            "description": "Processes 10-100 contracts in parallel batches with portfolio aggregation.",
            "domain": "Batch Processing",
            "apis": ["TimeGPT API"],
            "tools": "Read,Write,Bash,Glob,Grep",
        },
        {
            "name": "nixtla-event-impact-modeler",
            "description": "Models exogenous event impact on contract prices using TimeGPT.",
            "domain": "Event Analysis",
            "apis": ["TimeGPT API"],
            "tools": "Read,Write,Bash,Glob,Grep,WebSearch",
        },
        {
            "name": "nixtla-forecast-validator",
            "description": "Validates forecast quality metrics (MASE, sMAPE) and detects degradation.",
            "domain": "Quality Assurance",
            "apis": ["TimeGPT API"],
            "tools": "Read,Write,Bash,Glob,Grep",
        },
        {
            "name": "nixtla-model-selector",
            "description": "Auto-selects best model (StatsForecast vs TimeGPT) based on data characteristics.",
            "domain": "Model Selection",
            "apis": ["TimeGPT API", "StatsForecast"],
            "tools": "Read,Write,Bash,Glob,Grep",
        },
        {
            "name": "nixtla-liquidity-forecaster",
            "description": "Forecasts orderbook depth and spreads for trade execution timing.",
            "domain": "Liquidity Analysis",
            "apis": ["Polymarket API", "TimeGPT API"],
            "tools": "Read,Write,Bash,Glob,Grep,WebFetch",
        },
        {
            "name": "nixtla-correlation-mapper",
            "description": "Analyzes multi-contract correlations and generates hedge recommendations.",
            "domain": "Portfolio Analysis",
            "apis": ["TimeGPT API"],
            "tools": "Read,Write,Bash,Glob,Grep",
        },
        {
            "name": "nixtla-market-risk-analyzer",
            "description": "Calculates VaR, volatility, drawdown and position sizing recommendations.",
            "domain": "Risk Management",
            "apis": ["TimeGPT API"],
            "tools": "Read,Write,Bash,Glob,Grep",
        },
    ],
    "live-retroactive": [
        {
            "name": "nixtla-timegpt-lab",
            "description": "Expert forecasting with TimeGPT, StatsForecast, MLForecast integration.",
            "domain": "Forecasting",
            "apis": ["TimeGPT API", "StatsForecast"],
            "tools": "Read,Write,Bash,Glob,Grep",
            "is_live": True,
        },
        {
            "name": "nixtla-experiment-architect",
            "description": "Scaffolds production-ready forecasting experiments with configs.",
            "domain": "Experiment Design",
            "apis": ["TimeGPT API", "StatsForecast"],
            "tools": "Read,Write,Edit,Glob,Grep",
            "is_live": True,
        },
        {
            "name": "nixtla-schema-mapper",
            "description": "Transforms data to Nixtla format (unique_id, ds, y). Auto-infers mappings.",
            "domain": "Data Transformation",
            "apis": [],
            "tools": "Read,Write,Edit,Glob,Grep",
            "is_live": True,
        },
        {
            "name": "nixtla-timegpt-finetune-lab",
            "description": "Fine-tunes TimeGPT on custom datasets with guided workflow.",
            "domain": "Fine-Tuning",
            "apis": ["TimeGPT API"],
            "tools": "Read,Write,Bash,Glob,Grep",
            "is_live": True,
        },
        {
            "name": "nixtla-prod-pipeline-generator",
            "description": "Transforms experiments into production pipelines with Airflow/Prefect.",
            "domain": "Production Deployment",
            "apis": ["TimeGPT API"],
            "tools": "Read,Write,Edit,Glob,Grep",
            "is_live": True,
        },
        {
            "name": "nixtla-usage-optimizer",
            "description": "Audits Nixtla API usage and recommends cost-effective routing.",
            "domain": "Cost Optimization",
            "apis": ["TimeGPT API"],
            "tools": "Read,Glob,Grep",
            "is_live": True,
        },
    ],
}

# ==============================================================================
# PROMPT - Canonical Claude Skills Standard
# ==============================================================================

SKILL_PROMPT = """Create a SKILL.md file following the Claude Skills Canonical Standard EXACTLY.

## SKILL DETAILS
- Name: {name}
- Domain: {domain}
- Description: {description}
- APIs: {apis}
- Allowed Tools: {tools}

## MANDATORY FORMAT

### YAML FRONTMATTER
```yaml
---
name: {name}
description: |
  [Capabilities in 1-2 sentences, THIRD PERSON voice].
  Use when [3-4 trigger scenarios].
  Trigger with "[phrase 1]", "[phrase 2]", "[phrase 3]".
allowed-tools: "{tools}"
version: "1.0.0"
---
```

### REQUIRED SECTIONS (in order)
1. **Title** - # Skill Name
2. **Purpose** - 1-2 sentences
3. **Overview** - 3-5 sentences (what, when, capabilities, output)
4. **Prerequisites** - Tools, packages, env vars
5. **Instructions** - 4 steps, IMPERATIVE voice ("Run", "Analyze", "Generate")
6. **Output** - Bullet list of artifacts
7. **Error Handling** - EXACTLY 4 errors with solutions
8. **Examples** - EXACTLY 2 input/output pairs
9. **Resources** - Using {{baseDir}} for paths

### RULES
- Description: THIRD PERSON ("Analyzes data", NOT "I analyze")
- Instructions: IMPERATIVE ("Run the script", NOT "You should run")
- Paths: ALL use {{baseDir}}: `{{baseDir}}/scripts/tool.py`
- Size: Under 250 lines total

## EXAMPLE

```yaml
---
name: nixtla-forecast-skill
description: |
  Generates time series forecasts using TimeGPT foundation model.
  Use when forecasting sales, demand, prices, or any time series.
  Trigger with "forecast this", "predict values", "time series analysis".
allowed-tools: "Read,Write,Bash,Glob,Grep"
version: "1.0.0"
---

# Forecast Skill

Produces accurate forecasts from historical time series data using Nixtla TimeGPT.

## Overview

Transforms raw time series into predictions with confidence intervals. Handles
data validation, frequency detection, and model configuration automatically.
Use when historical data needs future predictions. Outputs CSV forecasts and plots.

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install nixtla pandas
```

## Instructions

### Step 1: Load data

Read input CSV and verify columns (unique_id, ds, y).

### Step 2: Configure parameters

Set horizon (prediction length) and frequency (D, W, M, H).

### Step 3: Execute forecast

Run: `python {{baseDir}}/scripts/forecast.py --input data.csv --horizon 14`

### Step 4: Generate output

Save forecast CSV and create visualization plot.

## Output

- **forecast.csv**: Predictions with confidence intervals
- **plot.png**: Actual vs predicted visualization
- **metrics.json**: Accuracy metrics (MASE, sMAPE)

## Error Handling

1. **Error**: `NIXTLA_TIMEGPT_API_KEY not set`
   **Solution**: `export NIXTLA_TIMEGPT_API_KEY=your_key`

2. **Error**: `Missing column: ds`
   **Solution**: Rename date column to 'ds'

3. **Error**: `Insufficient data`
   **Solution**: Need minimum 10 data points

4. **Error**: `Invalid frequency`
   **Solution**: Use --freq parameter (D, W, M, H)

## Examples

### Example 1: Daily sales

**Input**:
```
unique_id,ds,y
store_1,2024-01-01,100
store_1,2024-01-02,120
```

**Output**:
```
unique_id,ds,TimeGPT,TimeGPT-lo-90,TimeGPT-hi-90
store_1,2024-02-01,145,130,160
```

### Example 2: Hourly demand

**Input**:
```
unique_id,ds,y
grid_1,2024-01-01 00:00,5000
```

**Output**:
```
unique_id,ds,TimeGPT
grid_1,2024-01-02 00:00,5100
```

## Resources

- Scripts: `{{baseDir}}/scripts/`
- Docs: `{{baseDir}}/references/`
```

NOW GENERATE SKILL.md FOR: {name}

Output ONLY the SKILL.md content starting with the YAML frontmatter (---).
Do NOT wrap in markdown code fences.
"""

# ==============================================================================
# GENERATOR CLASS
# ==============================================================================


class SkillGenerator:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.model = None
        self.progress = self._load_progress()

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
        )
        self.logger = logging.getLogger(__name__)

    def _load_progress(self) -> dict:
        if PROGRESS_FILE.exists():
            return json.loads(PROGRESS_FILE.read_text())
        return {"completed": [], "failed": [], "started_at": None}

    def _save_progress(self):
        PROGRESS_FILE.write_text(json.dumps(self.progress, indent=2))

    def initialize(self):
        self.logger.info("Initializing Vertex AI...")
        self.logger.info(f"Project: {PROJECT_ID}")
        self.logger.info(f"Location: {LOCATION}")

        if not self.dry_run:
            # Initialize Vertex AI with ADC (no API key needed)
            vertexai.init(project=PROJECT_ID, location=LOCATION)
            self.model = GenerativeModel("gemini-2.0-flash-exp")
            self.logger.info("Gemini model ready (gemini-2.0-flash-exp)")

        self.progress["started_at"] = datetime.now().isoformat()
        self._save_progress()

    def generate(self, prompt: str) -> str:
        if self.dry_run:
            return f"[DRY RUN] {len(prompt)} chars"

        for attempt in range(MAX_RETRIES):
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                self.logger.warning(f"Attempt {attempt+1} failed: {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(PAUSE_ON_ERROR * (attempt + 1))
                else:
                    raise
        return ""

    def generate_skill(self, skill: dict, category: str) -> bool:
        name = skill["name"]

        if name in self.progress["completed"]:
            self.logger.info(f"Skipping {name} (done)")
            return True

        self.logger.info(f"{'='*50}")
        self.logger.info(f"Generating: {name} [{category}]")

        # Output directory
        if category == "live-retroactive":
            output_dir = PLANNED_SKILLS_DIR / "live" / name
        else:
            output_dir = PLANNED_SKILLS_DIR / category / name
        output_dir.mkdir(parents=True, exist_ok=True)

        try:
            self.logger.info("  Generating SKILL.md...")
            prompt = SKILL_PROMPT.format(
                name=skill["name"],
                domain=skill["domain"],
                description=skill["description"],
                apis=", ".join(skill.get("apis", ["None"])),
                tools=skill.get("tools", "Read,Write,Glob,Grep"),
            )

            skill_content = self.generate(prompt)

            # Clean markdown fences if present
            if skill_content.startswith("```"):
                lines = skill_content.split("\n")
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]
                skill_content = "\n".join(lines)

            (output_dir / "SKILL.md").write_text(skill_content)
            self.logger.info(f"  Saved ({len(skill_content)} chars)")

            self.progress["completed"].append(name)
            self._save_progress()
            self.logger.info(f"  DONE: {name}")
            return True

        except Exception as e:
            self.logger.error(f"  FAILED: {name} - {e}")
            self.progress["failed"].append({"name": name, "error": str(e)})
            self._save_progress()
            return False

    def run(self, resume_from: Optional[str] = None):
        self.initialize()

        total = sum(len(s) for s in SKILLS_TO_GENERATE.values())
        self.logger.info(f"Total skills: {total}")
        self.logger.info(f"Estimated time: ~{total * 15 / 60:.0f} minutes")

        skip = resume_from is not None
        generated = 0

        for category, skills in SKILLS_TO_GENERATE.items():
            self.logger.info(f"\n=== {category.upper()} ({len(skills)} skills) ===")

            for skill in skills:
                if skip:
                    if skill["name"] == resume_from:
                        skip = False
                    else:
                        continue

                if self.generate_skill(skill, category):
                    generated += 1

                if not self.dry_run:
                    self.logger.info(f"Pausing {PAUSE_BETWEEN_SKILLS}s...")
                    time.sleep(PAUSE_BETWEEN_SKILLS)

        self.logger.info(f"\n{'='*50}")
        self.logger.info(f"COMPLETE: {generated} generated, {len(self.progress['failed'])} failed")
        return len(self.progress["failed"]) == 0


def main():
    parser = argparse.ArgumentParser(description="Generate Nixtla skills using Vertex AI Gemini")
    parser.add_argument("--dry-run", action="store_true", help="Don't make API calls")
    parser.add_argument("--resume", type=str, help="Resume from specific skill name")
    args = parser.parse_args()

    gen = SkillGenerator(dry_run=args.dry_run)
    success = gen.run(resume_from=args.resume)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
