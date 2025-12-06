# DEPRECATED: nixtla-baseline-m4

**Status**: ⚠️ Archived / Superseded
**Date Archived**: 2025-12-03 (Phase 03)
**Archived By**: Claude Code (Intent Solutions)

---

## ⛔ Do Not Use This Directory

This directory has been **deprecated and archived**. It should not be used for any new work.

---

## Why This Directory Was Archived

This directory contained an early or duplicate version of the Nixtla baseline forecasting plugin. Analysis during Phase 03 cleanup revealed:

1. **Minimal Structure**: Only 5 subdirectories vs. nixtla-baseline-lab's 12
2. **No Active Maintenance**: Last modified Nov 30 02:14 (older than baseline-lab)
3. **No CI Integration**: No workflows targeting this directory
4. **Superseded**: All functionality exists in nixtla-baseline-lab

---

## ✅ Use Instead

**Canonical Plugin**: `plugins/nixtla-baseline-lab/`

**Location**: `../../nixtla-baseline-lab/` (from this directory)

**Version**: 1.1.0 (synchronized as of Phase 03)

**Features**:
- Comprehensive 36KB README
- Golden task test harness
- MCP server for Claude Code integration
- CI/CD validation
- Skills for result interpretation
- Dedicated virtualenv setup

---

## Command Migration

**Note**: The `/nixtla-baseline-m4` command you may see in documentation is **not** this directory!

That command is defined in `plugins/nixtla-baseline-lab/commands/nixtla-baseline-m4.md`.

The command name references the **M4 benchmark dataset**, not this archived directory. It's a confusing naming coincidence.

**To use baseline forecasting**:
```bash
# Setup (one-time)
cd plugins/nixtla-baseline-lab
./scripts/setup_nixtla_env.sh --venv

# In Claude Code
/nixtla-baseline-m4 demo_preset=m4_daily_small

# Or use MCP tools directly via Claude Code conversation
```

---

## Documentation

**Primary Docs**: `plugins/nixtla-baseline-lab/README.md`

**Testing**: `plugins/nixtla-baseline-lab/tests/run_baseline_m4_smoke.py`

**Phase 03 AAR**: `000-docs/6767-AA-AAR-phase-03-baseline-lab-cleanup-and-hardening.md`

---

## If You Need This Code

This archive preserves the original directory structure. If you need to reference old code patterns or understand the evolution of the plugin, it's here.

**But for any active development or usage**, always use:
- `plugins/nixtla-baseline-lab/`

---

## Questions?

See Phase 03 AAR for full analysis and decision rationale:
- `000-docs/6767-AA-AAR-phase-03-baseline-lab-cleanup-and-hardening.md`

Or contact:
- **Maintained by**: Intent Solutions (Jeremy Longshore)
- Email: jeremy@intentsolutions.io

---

**Last Updated**: 2025-12-03 (Phase 03)
