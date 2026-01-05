---
name: changelog-custom
description: Generate changelog for a custom date range using configured data sources
---

# Generate Custom Changelog

Generate changelog for a custom date range using configured data sources.

## Parameters

- `start_date` (required): ISO 8601 date (YYYY-MM-DD)
- `end_date` (required): ISO 8601 date (YYYY-MM-DD)

## Usage

```
/changelog-custom start_date=2025-12-01 end_date=2025-12-15
```

## Workflow

Follow the same 6-phase workflow as `/changelog-weekly`, but use the provided date range instead of calculating "last 7 days".

### Validation

Before starting:
1. Parse `start_date` and `end_date` parameters
2. Validate date format (must be YYYY-MM-DD)
3. Ensure start_date < end_date
4. Warn if date range > 90 days (too large, may be slow)

If validation fails, return error with correct usage example.

### Phase 1: Initialize & Fetch

Use provided date range instead of calculating:
- start_date: From parameter
- end_date: From parameter

All other phases identical to `/changelog-weekly`.

## Examples

```bash
# Monthly changelog
/changelog-custom start_date=2025-12-01 end_date=2025-12-31

# Sprint changelog (2 weeks)
/changelog-custom start_date=2025-12-15 end_date=2025-12-29

# Quarterly changelog
/changelog-custom start_date=2025-10-01 end_date=2025-12-31
```

## Error Handling

Additional validation errors:
- Missing parameters: "Required: start_date and end_date"
- Invalid format: "Date must be YYYY-MM-DD format"
- Invalid range: "start_date must be before end_date"
- Range too large: "Date range exceeds 90 days (performance warning)"
