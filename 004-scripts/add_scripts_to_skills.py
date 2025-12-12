#!/usr/bin/env python3
"""
Add Embedded Scripts to Skills - Vertex AI Gemini
==================================================
Updates existing SKILL.md files to include complete, deployable Python scripts.

Uses Vertex AI Gemini to generate production-quality scripts for each skill.

Usage:
    python scripts/add_scripts_to_skills.py
    python scripts/add_scripts_to_skills.py --skill nixtla-contract-schema-mapper
    python scripts/add_scripts_to_skills.py --dry-run

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
from typing import Dict, List, Optional

import vertexai
from vertexai.generative_models import GenerativeModel

# ==============================================================================
# CONFIGURATION
# ==============================================================================

REPO_ROOT = Path(__file__).parent.parent
PLANNED_SKILLS_DIR = REPO_ROOT / "000-docs" / "planned-skills"
PROGRESS_FILE = REPO_ROOT / "scripts" / ".script_generator_progress.json"
LOG_FILE = REPO_ROOT / "scripts" / "script_generator.log"

# Google Cloud config
PROJECT_ID = os.environ.get("PROJECT_ID", "pipelinepilot-prod")
LOCATION = os.environ.get("LOCATION", "us-central1")

# Timing
PAUSE_BETWEEN_SKILLS = 15
PAUSE_ON_ERROR = 60
MAX_RETRIES = 3

# Skills that need script updates (already have basic SKILL.md but need embedded scripts)
SKILLS_NEEDING_SCRIPTS = {
    "prediction-markets": [
        "nixtla-contract-schema-mapper",
        "nixtla-event-impact-modeler",
        "nixtla-forecast-validator",
        "nixtla-liquidity-forecaster",
        "nixtla-model-selector",
    ],
    "live": [
        "nixtla-timegpt-lab",
        "nixtla-timegpt-finetune-lab",
        "nixtla-prod-pipeline-generator",
        "nixtla-usage-optimizer",
        "nixtla-schema-mapper",
        "nixtla-experiment-architect",
    ],
    "core-forecasting": [
        "nixtla-anomaly-detector",
        "nixtla-exogenous-integrator",
        "nixtla-uncertainty-quantifier",
        "nixtla-cross-validator",
        "nixtla-timegpt2-migrator",
    ],
}

# ==============================================================================
# LOGGING
# ==============================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# ==============================================================================
# PROMPT TEMPLATE
# ==============================================================================

SCRIPT_GENERATION_PROMPT = """You are an expert Python developer specializing in time series forecasting with Nixtla libraries.

I have a Claude Code skill file that references scripts but doesn't include the actual code. Your task is to rewrite the SKILL.md file with COMPLETE, PRODUCTION-READY Python scripts embedded in markdown code blocks.

## Current SKILL.md Content:
```markdown
{current_content}
```

## Requirements:

1. **Keep the YAML frontmatter exactly as is** (name, description, allowed-tools, version)

2. **Replace all references to external scripts** like `python {{baseDir}}/scripts/something.py` with complete embedded Python code blocks that Claude can deploy.

3. **Each script must be:**
   - Complete and runnable (no placeholders)
   - Well-documented with docstrings
   - Include proper error handling
   - Use type hints
   - Follow PEP 8 style
   - Include `if __name__ == "__main__":` blocks

4. **For Nixtla-specific code, use these patterns:**

   StatsForecast (no API key needed):
   ```python
   from statsforecast import StatsForecast
   from statsforecast.models import AutoETS, AutoARIMA, SeasonalNaive, AutoTheta
   sf = StatsForecast(models=[AutoETS(), AutoARIMA()], freq='D', n_jobs=-1)
   forecasts = sf.forecast(df=df, h=14)
   ```

   TimeGPT (requires NIXTLA_TIMEGPT_API_KEY):
   ```python
   from nixtla import NixtlaClient
   client = NixtlaClient(api_key=os.getenv('NIXTLA_TIMEGPT_API_KEY'))
   forecast = client.forecast(df=df, h=24, freq='H')
   ```

   Nixtla Data Schema (required for all Nixtla libraries):
   - unique_id: Series identifier (string)
   - ds: Datetime column
   - y: Target variable (numeric)

5. **Structure the skill with these sections:**
   - Overview
   - Prerequisites (packages, environment variables)
   - Instructions with numbered steps
   - Each step should have the COMPLETE Python script
   - Output section describing generated files
   - Error Handling section
   - Examples section
   - Usage section showing how to run

6. **Make scripts 200-400 lines each** - comprehensive and production-ready

7. **Include visualization code** using matplotlib where appropriate

## Output:
Return ONLY the complete updated SKILL.md content with all embedded scripts. No explanations before or after.
"""

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================


def load_progress() -> Dict:
    """Load progress from checkpoint file."""
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text())
    return {"completed": [], "failed": [], "last_run": None}


def save_progress(progress: Dict) -> None:
    """Save progress to checkpoint file."""
    progress["last_run"] = datetime.now().isoformat()
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2))


def read_skill_file(category: str, skill_name: str) -> Optional[str]:
    """Read current SKILL.md content."""
    skill_path = PLANNED_SKILLS_DIR / category / skill_name / "SKILL.md"
    if skill_path.exists():
        return skill_path.read_text()
    return None


def write_skill_file(category: str, skill_name: str, content: str) -> None:
    """Write updated SKILL.md content."""
    skill_path = PLANNED_SKILLS_DIR / category / skill_name / "SKILL.md"
    skill_path.parent.mkdir(parents=True, exist_ok=True)
    skill_path.write_text(content)
    logger.info(f"Updated {skill_path}")


def generate_scripts_with_gemini(current_content: str, model: GenerativeModel) -> Optional[str]:
    """Use Gemini to generate embedded scripts for a skill."""
    prompt = SCRIPT_GENERATION_PROMPT.format(current_content=current_content)

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": 8192,
                "temperature": 0.2,
            },
        )

        if response.text:
            # Clean up the response
            text = response.text.strip()

            # Remove markdown code fences if present
            if text.startswith("```markdown"):
                text = text[len("```markdown") :].strip()
            if text.startswith("```"):
                text = text[3:].strip()
            if text.endswith("```"):
                text = text[:-3].strip()

            return text

        return None

    except Exception as e:
        logger.error(f"Gemini generation error: {e}")
        return None


# ==============================================================================
# MAIN PROCESSING
# ==============================================================================


def process_skill(
    category: str, skill_name: str, model: GenerativeModel, dry_run: bool = False
) -> bool:
    """Process a single skill - add embedded scripts."""
    logger.info(f"Processing {category}/{skill_name}...")

    # Read current content
    current_content = read_skill_file(category, skill_name)
    if not current_content:
        logger.warning(f"No SKILL.md found for {skill_name}")
        return False

    # Check if already has substantial scripts (>5000 chars usually means scripts present)
    if len(current_content) > 8000:
        logger.info(
            f"Skill {skill_name} already has scripts (size: {len(current_content)}), skipping"
        )
        return True

    if dry_run:
        logger.info(f"[DRY RUN] Would generate scripts for {skill_name}")
        return True

    # Generate new content with embedded scripts
    for attempt in range(MAX_RETRIES):
        try:
            new_content = generate_scripts_with_gemini(current_content, model)

            if new_content and len(new_content) > len(current_content):
                write_skill_file(category, skill_name, new_content)
                logger.info(
                    f"Successfully updated {skill_name} ({len(current_content)} -> {len(new_content)} chars)"
                )
                return True
            else:
                logger.warning(f"Generated content too short or empty for {skill_name}")

        except Exception as e:
            logger.error(f"Attempt {attempt + 1} failed for {skill_name}: {e}")
            time.sleep(PAUSE_ON_ERROR)

    return False


def main():
    parser = argparse.ArgumentParser(description="Add embedded scripts to skill files using Gemini")
    parser.add_argument("--skill", help="Process only this specific skill")
    parser.add_argument("--category", help="Process only this category")
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be done without making changes"
    )
    parser.add_argument(
        "--resume", action="store_true", help="Resume from last progress checkpoint"
    )
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("SKILL SCRIPT GENERATOR - Vertex AI Gemini")
    logger.info("=" * 60)

    # Initialize Vertex AI
    logger.info(f"Initializing Vertex AI (project: {PROJECT_ID}, location: {LOCATION})")
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    model = GenerativeModel("gemini-2.0-flash")

    # Load progress
    progress = load_progress() if args.resume else {"completed": [], "failed": [], "last_run": None}

    # Build list of skills to process
    skills_to_process = []

    for category, skills in SKILLS_NEEDING_SCRIPTS.items():
        if args.category and category != args.category:
            continue

        for skill_name in skills:
            if args.skill and skill_name != args.skill:
                continue

            if args.resume and skill_name in progress["completed"]:
                logger.info(f"Skipping {skill_name} (already completed)")
                continue

            skills_to_process.append((category, skill_name))

    logger.info(f"Skills to process: {len(skills_to_process)}")

    # Process skills
    for i, (category, skill_name) in enumerate(skills_to_process):
        logger.info(f"\n[{i+1}/{len(skills_to_process)}] Processing {category}/{skill_name}")

        success = process_skill(category, skill_name, model, args.dry_run)

        if success:
            progress["completed"].append(skill_name)
        else:
            progress["failed"].append(skill_name)

        save_progress(progress)

        # Pause between skills
        if i < len(skills_to_process) - 1:
            logger.info(f"Pausing {PAUSE_BETWEEN_SKILLS}s before next skill...")
            time.sleep(PAUSE_BETWEEN_SKILLS)

    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("SUMMARY")
    logger.info("=" * 60)
    logger.info(f"Completed: {len(progress['completed'])}")
    logger.info(f"Failed: {len(progress['failed'])}")
    if progress["failed"]:
        logger.info(f"Failed skills: {progress['failed']}")

    return 0 if not progress["failed"] else 1


if __name__ == "__main__":
    sys.exit(main())
