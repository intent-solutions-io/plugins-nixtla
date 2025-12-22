---
name: skill-name
description: "Action-oriented description of what the skill does. Use when [scenario 1], [scenario 2], or [scenario 3]. Trigger with 'trigger phrase 1', 'trigger phrase 2', or 'trigger phrase 3'."
allowed-tools: "Read,Write,Glob,Grep,Edit,Bash(python:*)"
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
---

# Skill Title

Brief one-sentence description of what this skill does.

## Overview

High-level description of capabilities:

- **Capability 1**: Description
- **Capability 2**: Description
- **Capability 3**: Description

## Prerequisites

**Required**:
- Python 3.8+
- Required dependencies

**Optional**:
- Optional dependencies
- API keys (if applicable)

**Installation**:
```bash
pip install required-package
```

## Instructions

### Step 1: Preparation

Describe what the user needs to do first.

```bash
# Example preparation command
```

### Step 2: Execution

Execute the main workflow.

```bash
python {baseDir}/scripts/script_name.py \
    --arg1 value1 \
    --arg2 value2
```

### Step 3: Validation

Verify the results.

```bash
# Example validation command
```

## Output

- **output_file.csv**: Description of output
- **metrics.json**: Description of metrics
- **report.html**: Description of report

## Error Handling

1. **Error**: `Error message pattern`
   **Solution**: How to fix this error

2. **Error**: `Another error pattern`
   **Solution**: Resolution steps

3. **Error**: `Third error pattern`
   **Solution**: Troubleshooting approach

## Examples

### Example 1: Basic Usage

```python
# Basic example code
from package import Function

result = Function(data, param=value)
```

### Example 2: Advanced Usage

```python
# Advanced example with multiple features
from package import AdvancedFunction

result = AdvancedFunction(
    data=data,
    param1=value1,
    param2=value2,
    config={
        'option1': True,
        'option2': 'value'
    }
)
```

### Example 3: Integration Example

```bash
# Command-line integration example
python {baseDir}/scripts/script.py \
    --input data.csv \
    --output results/ \
    --config config.json
```

## Resources

- **Official Documentation**: https://docs.example.com/
- **API Reference**: https://api.example.com/
- **Community Forum**: https://forum.example.com/

**Related Skills**:
- `related-skill-1`: Description
- `related-skill-2`: Description

**Scripts**:
- `{baseDir}/scripts/main_script.py`: Main processing script
- `{baseDir}/scripts/helper.py`: Helper utilities
