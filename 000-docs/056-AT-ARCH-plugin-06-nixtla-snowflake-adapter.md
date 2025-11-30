# Plugin #6: Nixtla Snowflake Native Adapter
**Technical Architecture & Implementation Specification**

**Created**: 2025-11-30
**Status**: Design Phase
**Priority**: Tier 2 (INTEGRATION WIN)
**Addresses**: Integration Tax (Friction #4)

---

## Executive Summary

### What It Is
A Claude Code plugin that wraps Nixtla's existing Snowflake Native App integration, providing one-command SQL-native forecasting with automatic setup and error handling.

### Why It Exists
Nixtla already has Snowflake integration, but:
> "Marketing copy attacks Python infrastructure requirements. This plugin makes the native integration discoverable and easy to use from Claude Code."

**This plugin is a wrapper/helper for the existing Nixtla Snowflake integration.**

### Who It's For
- **Snowflake users** wanting SQL-native forecasting
- **SQL analysts** without Python skills
- **Data teams** standardizing on Snowflake
- **BI teams** needing forecasts in Looker/Tableau

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  CLAUDE CODE INTERFACE                                      │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │Slash Command │  │ Agent Skill  │                        │
│  │/snowflake    │  │(Auto-invoke) │                        │
│  └──────────────┘  └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘
         │                    │
         ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│  PLUGIN HELPERS (Python)                                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  - SQL generator (CALL NIXTLA_FORECAST(...))        │  │
│  │  - Connection validator                              │  │
│  │  - Error parser                                      │  │
│  │  - Result formatter                                  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  SNOWFLAKE NATIVE APP (Existing Nixtla Integration)        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Nixtla functions available in Snowflake:            │  │
│  │  - CALL NIXTLA_FORECAST(...)                         │  │
│  │  - CALL NIXTLA_DETECT_ANOMALIES(...)                │  │
│  │  - CALL NIXTLA_CROSS_VALIDATE(...)                  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Plugin Type
**AI Instruction** (Pure Python helpers)

### Components

1. **Slash Commands** (2)
   - `/nixtla-snowflake-setup` - Validate Snowflake connection
   - `/nixtla-snowflake-forecast` - Generate forecast SQL

2. **Agent Skill** (1)
   - `nixtla-snowflake-expert` - Auto-generates SQL for Snowflake

3. **No MCP Server** - Pure SQL generation helpers

---

## API Keys & User Requirements

### Required
```bash
# Snowflake connection
SNOWFLAKE_ACCOUNT=myorg.snowflakecomputing.com
SNOWFLAKE_USER=analytics_user
SNOWFLAKE_PASSWORD=...
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=ANALYTICS
SNOWFLAKE_SCHEMA=FORECASTS

# Nixtla Snowflake app must be installed
# (Done once by Snowflake admin)
```

### User Requirements

#### Minimum
- **Snowflake account** with Nixtla Native App installed
- **Python 3.10+** for connection helpers
- **Read access** to source tables
- **Write access** to forecast output tables

#### Installation (One-Time, by Admin)
```sql
-- Snowflake admin installs Nixtla Native App
USE ROLE ACCOUNTADMIN;
CREATE DATABASE NIXTLA FROM SHARE NIXTLA_PROVIDER.NIXTLA_APP;
GRANT USAGE ON DATABASE NIXTLA TO ROLE ANALYTICS;
```

---

## Code Implementation

### Core: snowflake_helper.py

```python
"""
Helper for Nixtla Snowflake Native App integration
"""
import snowflake.connector
from typing import Optional, Dict, List
from rich.console import Console
from rich.syntax import Syntax


console = Console()


class NixtlaSnowflakeAdapter:
    """Generate and execute Nixtla SQL in Snowflake"""

    def __init__(
        self,
        account: str,
        user: str,
        password: str,
        warehouse: str,
        database: str,
        schema: str
    ):
        self.conn = snowflake.connector.connect(
            account=account,
            user=user,
            password=password,
            warehouse=warehouse,
            database=database,
            schema=schema
        )

    def generate_forecast_sql(
        self,
        source_table: str,
        timestamp_col: str,
        value_col: str,
        group_by: Optional[str] = None,
        horizon: int = 30,
        freq: str = 'D'
    ) -> str:
        """Generate Snowflake SQL for forecasting"""

        if group_by:
            sql = f"""
-- Forecast with grouping by {group_by}
CALL NIXTLA.FORECAST(
    INPUT_TABLE => '{source_table}',
    TIMESTAMP_COL => '{timestamp_col}',
    VALUE_COL => '{value_col}',
    GROUP_BY_COL => '{group_by}',
    HORIZON => {horizon},
    FREQUENCY => '{freq}',
    LEVEL => ARRAY_CONSTRUCT(80, 90, 95)
);
"""
        else:
            sql = f"""
-- Forecast single series
CALL NIXTLA.FORECAST(
    INPUT_TABLE => '{source_table}',
    TIMESTAMP_COL => '{timestamp_col}',
    VALUE_COL => '{value_col}',
    HORIZON => {horizon},
    FREQUENCY => '{freq}',
    LEVEL => ARRAY_CONSTRUCT(80, 90, 95)
);
"""

        return sql.strip()

    def execute_forecast(self, sql: str) -> Dict:
        """Execute forecast and return results"""
        cursor = self.conn.cursor()

        try:
            cursor.execute(sql)
            results = cursor.fetchall()

            return {
                'status': 'success',
                'row_count': len(results),
                'results': results
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
        finally:
            cursor.close()

    def validate_connection(self) -> bool:
        """Test Snowflake connection and Nixtla app availability"""
        cursor = self.conn.cursor()

        try:
            # Test connection
            cursor.execute("SELECT CURRENT_VERSION()")
            version = cursor.fetchone()[0]
            console.print(f"✅ Connected to Snowflake {version}")

            # Test Nixtla app
            cursor.execute("SHOW DATABASES LIKE 'NIXTLA'")
            nixtla_db = cursor.fetchone()

            if nixtla_db:
                console.print("✅ Nixtla Native App installed")
                return True
            else:
                console.print("❌ Nixtla Native App not found")
                console.print("   Install: https://app.snowflake.com/marketplace/listing/GZTYZF0O5Y")
                return False

        except Exception as e:
            console.print(f"❌ Connection failed: {e}")
            return False
        finally:
            cursor.close()
```

---

## Example Usage

```python
# User runs slash command
/nixtla-snowflake-forecast --table SALES_HISTORY --horizon 30

# Claude Code generates:
"""
-- Generated Nixtla Snowflake forecast SQL
CALL NIXTLA.FORECAST(
    INPUT_TABLE => 'SALES_HISTORY',
    TIMESTAMP_COL => 'DATE',
    VALUE_COL => 'REVENUE',
    GROUP_BY_COL => 'PRODUCT_ID',
    HORIZON => 30,
    FREQUENCY => 'D',
    LEVEL => ARRAY_CONSTRUCT(80, 90, 95)
);

-- Results will be in NIXTLA.FORECAST_RESULTS table
SELECT * FROM NIXTLA.FORECAST_RESULTS
WHERE FORECAST_DATE > CURRENT_DATE
ORDER BY PRODUCT_ID, FORECAST_DATE;
"""
```

---

## User Journey

### Journey 1: SQL Analyst Uses Snowflake Forecasting

**Persona**: James, SQL Analyst
**Goal**: Add forecasts to Looker dashboard
**Context**: Only knows SQL, has Snowflake access

**Steps**:

1. **Discover Plugin**
   ```
   James: "I need sales forecasts in my Looker dashboard"

   Claude: [Skill auto-activates]

           I can help you generate forecasts using Nixtla's
           Snowflake Native App. Let me check your setup...

           Testing Snowflake connection...
           ✅ Connected to Snowflake 8.15.2
           ✅ Nixtla Native App installed

           Ready to forecast!
   ```

2. **Generate Forecast SQL**
   ```
   James: "Forecast sales for next 30 days by region"

   Claude: Here's your SQL:

           ```sql
           -- Forecast sales by region (30 days)
           CALL NIXTLA.FORECAST(
               INPUT_TABLE => 'ANALYTICS.SALES_HISTORY',
               TIMESTAMP_COL => 'SALE_DATE',
               VALUE_COL => 'REVENUE_USD',
               GROUP_BY_COL => 'REGION',
               HORIZON => 30,
               FREQUENCY => 'D',
               LEVEL => ARRAY_CONSTRUCT(80, 90, 95)
           );

           -- View results
           SELECT
               REGION,
               FORECAST_DATE,
               FORECAST_VALUE,
               LOWER_BOUND_80,
               UPPER_BOUND_80
           FROM NIXTLA.FORECAST_RESULTS
           WHERE FORECAST_DATE > CURRENT_DATE
           ORDER BY REGION, FORECAST_DATE;
           ```

           Run this in Snowflake Worksheet or copy to Looker SQL Runner.
   ```

3. **Use in Looker**
   ```
   James: [Copies SQL to Looker]

   Looker: ✅ Query successful (900 rows)

   Dashboard: [Shows forecast chart with confidence intervals]
   ```

**Outcome**: James adds forecasts to Looker in 5 minutes using only SQL.

---

## Dependencies

```txt
# requirements.txt
snowflake-connector-python>=3.0.0
rich>=13.9.4
click>=8.1.8
python-dotenv>=1.0.1
```

---

**Document Version**: 1.0.0
**Last Updated**: 2025-11-30
**Language**: Pure Python (No TypeScript)
**Note**: Wrapper for existing Nixtla Snowflake Native App
