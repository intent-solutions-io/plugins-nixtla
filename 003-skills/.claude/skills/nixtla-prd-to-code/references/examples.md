# PRD to Code Examples

## Example 1: Parse ROI Calculator PRD

Generate a structured task list from the ROI calculator PRD with verbose output.

```bash
python {baseDir}/scripts/parse_prd.py \
    --prd 000-docs/000a-planned-plugins/implemented/nixtla-roi-calculator/02-PRD.md \
    --output roi_tasks.json \
    --verbose
```

**Generated tasks.json**:
```json
{
  "tasks": [
    {
      "id": "roi-001",
      "title": "Implement cost input collection",
      "description": "Build input form for infrastructure costs, forecasting volume, team composition",
      "priority": "P0",
      "dependencies": [],
      "complexity": "medium",
      "functional_requirement": "FR-1"
    },
    {
      "id": "roi-002",
      "title": "Build ROI calculation engine",
      "description": "5-year TCO calculation for build vs. buy scenarios",
      "priority": "P0",
      "dependencies": ["roi-001"],
      "complexity": "high",
      "functional_requirement": "FR-2"
    }
  ]
}
```

## Example 2: Auto-Populate TodoWrite

When used in conversation context, directly populate the Claude todo list.

```python
# In Claude Code conversation
from parse_prd import PRDParser

parser = PRDParser('000-docs/000a-planned-plugins/implemented/nixtla-roi-calculator/02-PRD.md')
tasks = parser.extract_tasks()

# Automatically populates TodoWrite
for task in tasks:
    TodoWrite(content=task['title'], activeForm=f"Working on {task['title']}", status="pending")
```

## Example 3: Generate Markdown Checklist

Export an implementation plan as a markdown checklist for manual tracking.

```bash
python {baseDir}/scripts/parse_prd.py \
    --prd 000-docs/000a-planned-plugins/implemented/nixtla-forecast-explainer/02-PRD.md \
    --output-format markdown \
    --output implementation_plan.md
```

**Generated implementation_plan.md**:
```markdown
# Nixtla Forecast Explainer - Implementation Plan

## Phase 1: Core Infrastructure (P0)
- [ ] Set up project structure and dependencies
- [ ] Create MCP server scaffold
- [ ] Implement SHAP explainability integration

## Phase 2: Feature Development (P0)
- [ ] Build feature importance calculation
- [ ] Implement counterfactual analysis
- [ ] Add time-based contribution decomposition

## Phase 3: Visualization (P1)
- [ ] Generate waterfall charts
- [ ] Create interactive dashboards
- [ ] Export to PDF reports
```

## Example 4: Batch Process Multiple PRDs

Generate task plans for all available PRDs at once.

```bash
for prd in 000-docs/000a-planned-plugins/*/02-PRD.md; do
    plugin_name=$(basename $(dirname "$prd"))
    python {baseDir}/scripts/parse_prd.py \
        --prd "$prd" \
        --output "009-temp-data/task-plans/${plugin_name}_tasks.json"
done
```
