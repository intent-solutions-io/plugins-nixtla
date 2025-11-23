# 6767 Canonical Document Reference Sheet

**Created:** 2025-11-23
**Version:** 1.0.0
**Purpose:** Quick reference guide for 6767 canonical document filing system v3.0
**Status:** ✅ Active Reference

---

## 🎯 WHAT ARE 6767 DOCUMENTS?

**6767 Series = Cross-Repository Canonical Standards (SOPs)**

These are **global, reusable standards** that apply across ALL projects:
- bobs-brain (ADK agent department)
- DiagnosticPro (repair platform)
- Hustle (youth sports app)
- Nixtla (forecasting plugins)
- ALL Intent Solutions projects

**Key Rule:** 6767 docs define universal patterns, NOT project-specific implementations.

---

## ✅ CORRECT v3.0 FORMAT

```
6767-CC-ABCD-short-description.ext
```

**Components:**
- **6767** = Fixed canonical prefix (used ONCE, no extra numbers!)
- **CC** = Category code (DR, AT, OD, RB, etc.)
- **ABCD** = 4-letter document type (STND, GUID, ARCH, etc.)
- **short-description** = kebab-case, 1-5 words

### ✅ CORRECT Examples (v3.0)
```
6767-DR-STND-document-filing-system-standard-v3.md
6767-DR-STND-adk-agent-engine-spec.md
6767-DR-INDEX-standards-catalog.md
6767-RB-OPS-deployment-runbook.md
6767-AT-ARCH-microservices-pattern.md
```

### ❌ WRONG Examples (Pre-v3.0)
```
❌ 6767-000-DR-INDEX-catalog.md       # NO numeric ID after 6767-
❌ 6767-120-DR-STND-agent-spec.md     # NO numeric ID after 6767-
❌ 6767-121-DR-STND-a2a-spec.md       # NO numeric ID after 6767-
```

---

## 📋 COMMON 6767 CATEGORY CODES

| Code | Category | Typical Use |
|------|----------|------------|
| **DR** | Documentation & Reference | Standards, guides, indexes |
| **AT** | Architecture & Technical | Global architecture patterns |
| **RB** | Runbook | Operations procedures |
| **OD** | Operations & Deployment | Deployment standards |
| **PM** | Project Management | Cross-project PM standards |
| **TQ** | Testing & Quality | Universal testing patterns |

---

## 📚 COMMON 6767 DOCUMENT TYPES

| Code | Full Name | Usage |
|------|-----------|-------|
| **STND** | Standard | Canonical standard/specification |
| **INDEX** | Index/Catalog | Directory of standards |
| **GUID** | Guide | Cross-repo implementation guide |
| **ARCH** | Architecture | Global architecture pattern |
| **SOPS** | Standard Operating Procedure | Universal procedure |
| **OPS** | Operations | Operational standard |
| **SPEC** | Specification | Technical specification |

---

## 🔄 RELATIONSHIP TO NNN DOCS

| Document Type | Format | Example |
|--------------|---------|---------|
| **Global SOP/Standard** | `6767-CC-ABCD-desc.ext` | 6767-DR-STND-filing-system.md |
| **Project-Specific** | `NNN-CC-ABCD-desc.ext` | 001-PP-PROD-nixtla-requirements.md |

**Simple Rule:**
- **Use 6767** → Global standard applying to multiple projects
- **Use NNN** → Project-specific, phase-specific, sprint-specific

---

## 🏷️ OPTIONAL TOPIC PREFIXES

Some 6767 docs use topic prefixes to group related standards:

```
6767-INLINE-DR-STND-inline-deployment.md
     ^^^^^^ Topic prefix

6767-LAZY-DR-STND-lazy-loading-pattern.md
     ^^^^ Topic prefix

6767-SLKDEV-DR-GUID-slack-integration.md
     ^^^^^^ Topic prefix
```

**Rule:** Topic prefixes are optional clustering mechanisms for related standards.

---

## 📝 DOCUMENT IDs vs FILENAMES

### ✅ ALLOWED: IDs in Document Headers
```markdown
# Agent Engine Standard

**Document ID:** 6767-120  ← OK in header
**Type:** 6767-DR-STND
```

### ❌ FORBIDDEN: IDs in Filenames
```
❌ 6767-120-DR-STND-agent-engine.md  ← WRONG
✅ 6767-DR-STND-agent-engine.md      ← CORRECT
```

**Key Point:** Document IDs help with cross-referencing but NEVER appear in filenames.

---

## 🚀 QUICK DECISION GUIDE

**Should I use 6767 or NNN?**

Ask yourself:
1. **Is this reusable across multiple projects?** → 6767
2. **Is it a global standard/pattern/SOP?** → 6767
3. **Is it project-specific implementation?** → NNN
4. **Is it phase/sprint-specific?** → NNN
5. **Is it an After-Action Report?** → NNN
6. **Is it a canonical architecture pattern?** → 6767

---

## 📍 WHERE 6767 DOCS LIVE

**Typical Locations:**
```
project-root/
├── 000-docs/
│   ├── 001-PP-PROD-project-requirements.md  # NNN project doc
│   ├── 002-AT-ARCH-system-design.md         # NNN project doc
│   ├── 6767-DR-STND-filing-system-v3.md     # 6767 canonical
│   └── 6767-RB-OPS-deployment-runbook.md    # 6767 canonical
```

Or in master standards repos:
```
prompts-intent-solutions/
└── master-systems/
    └── 6767-standards/
```

---

## ⚠️ CRITICAL v3.0 RULES

1. **NO numeric IDs after 6767- in filenames**
2. **6767 appears ONCE at the start**
3. **Always use 4-letter type codes**
4. **Keep descriptions kebab-case**
5. **Document IDs stay in headers, not filenames**

---

## 🔍 REAL EXAMPLES FROM PRODUCTION

### bobs-brain ADK Department
```
6767-DR-STND-adk-agent-engine-spec-and-hardmode-rules.md
6767-DR-STND-agentcards-and-a2a-contracts.md
6767-DR-INDEX-bobs-brain-standards-catalog.md
6767-RB-OPS-adk-department-operations-runbook.md
6767-INLINE-DR-STND-inline-source-deployment.md
```

### Cross-Project Standards
```
6767-DR-STND-document-filing-system-standard-v3.md
6767-AT-ARCH-microservices-communication-pattern.md
6767-TQ-TEST-universal-testing-framework.md
6767-PM-RISK-cross-project-risk-assessment.md
```

---

## 📊 MIGRATION CHECKLIST

Converting pre-v3.0 6767 files:

- [ ] Remove numeric IDs from filenames
- [ ] Keep document IDs in headers if needed
- [ ] Verify 4-letter type codes
- [ ] Update references in other docs
- [ ] Git mv (not delete/recreate) to preserve history

**Example Migration:**
```bash
# OLD (pre-v3.0)
6767-120-DR-STND-agent-engine.md

# NEW (v3.0)
6767-DR-STND-agent-engine.md
```

---

## 📚 REFERENCE LINKS

- **Full Standard:** `/home/jeremy/000-projects/iams/bobs-brain/000-docs/6767-DR-STND-document-filing-system-standard-v3.md`
- **Master Standards:** `/home/jeremy/prompts-intent-solutions/master-systems/`
- **Version:** Document Filing System v3.0 (2025-11-21)

---

## 💡 PRO TIPS

1. **When in doubt:** If it's reusable → 6767, if it's specific → NNN
2. **Search pattern:** `grep "6767-" */000-docs/*.md` finds all canonical docs
3. **Validation:** No numbers should appear between "6767-" and category code
4. **Cross-references:** Use document IDs in content, not filenames
5. **Topic clusters:** Use optional prefixes (INLINE-, LAZY-) for related standards

---

**Last Updated:** 2025-11-23
**Reference Version:** 1.0.0
**Based on:** Document Filing System Standard v3.0