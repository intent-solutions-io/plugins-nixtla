# Nixtla Usage Optimizer - Troubleshooting

## Issue 1: Can't find any Nixtla usage

**Symptom**: Scan returns zero results

**Solution**:
- Verify repository is correct
- Check if code uses different import patterns
- Look in notebooks: `find . -name "*.ipynb"`
- May be a new project - recommend starting with experiment architect

---

## Issue 2: Report too generic

**Symptom**: Recommendations not specific enough

**Solution**:
- Manually review key files for context
- Ask user for business impact information
- Focus on specific code patterns found
- Provide concrete code examples in recommendations
