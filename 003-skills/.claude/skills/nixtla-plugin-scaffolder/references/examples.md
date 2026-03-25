# Plugin Scaffolder Examples

## Example 1: Scaffold ROI Calculator Plugin

Generate a complete plugin from the ROI calculator PRD with custom author and license settings.

```bash
python {baseDir}/scripts/scaffold_plugin.py \
    --prd 000-docs/000a-planned-plugins/implemented/nixtla-roi-calculator/02-PRD.md \
    --output 005-plugins/nixtla-roi-calculator \
    --author "Jeremy Longshore <jeremy@intentsolutions.io>" \
    --license MIT
```

**Generated plugin.json**:
```json
{
  "name": "nixtla-roi-calculator",
  "version": "0.1.0",
  "description": "Enterprise ROI calculator for TimeGPT vs. build-in-house analysis",
  "author": { "name": "Jeremy Longshore", "email": "jeremy@intentsolutions.io" },
  "license": "MIT",
  "mcpServers": {
    "nixtla-roi-calculator": {
      "command": "python",
      "args": ["scripts/nixtla_roi_calculator_mcp_server.py"]
    }
  }
}
```

## Example 2: Scaffold Multiple Plugins in Batch

Process all PRDs in the planned-plugins directory and generate scaffolds for each one.

```bash
for prd in 000-docs/000a-planned-plugins/*/02-PRD.md; do
    plugin_name=$(basename $(dirname "$prd"))
    python {baseDir}/scripts/scaffold_plugin.py \
        --prd "$prd" \
        --output "005-plugins/$plugin_name"
done
```

## Example 3: Scaffold with Custom Template

Override the default plugin template with a custom one for project-specific requirements.

```bash
python {baseDir}/scripts/scaffold_plugin.py \
    --prd 000-docs/000a-planned-plugins/implemented/nixtla-forecast-explainer/02-PRD.md \
    --output 005-plugins/nixtla-forecast-explainer \
    --template {baseDir}/assets/templates/plugin_custom.json
```
