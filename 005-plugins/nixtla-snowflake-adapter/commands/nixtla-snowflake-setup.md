---
name: nixtla-snowflake-setup
description: Validate Nixtla Snowflake Native App installation
---

# /nixtla-snowflake-setup

Validate Nixtla Snowflake Native App installation.

## Usage

```
/nixtla-snowflake-setup
```

## Workflow

1. Test Snowflake connection
2. Verify Nixtla Native App installed
3. Check required permissions
4. Validate sample forecast
5. Generate setup report

## Checks

- Connection: Account, user, warehouse
- App: NIXTLA app installed and accessible
- Permissions: USAGE on database/schema
- Functions: NIXTLA_FORECAST, NIXTLA_DETECT_ANOMALIES

## Output

- Setup validation report
- Permission fix commands (if needed)
- Sample forecast SQL
