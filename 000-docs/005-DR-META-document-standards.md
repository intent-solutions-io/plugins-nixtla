---
doc_id: 005-DR-META-document-standards
title: Document Filing System v3.0 Standards
category: Documentation & Reference
status: Active
classification: Internal
repository: claude-code-plugins-nixtla
related_docs:
  - README.md
---

# Document Filing System v3.0 Standards

**Quick Reference**: Complete guide to the structured documentation filing system
**Last Updated**: Initial version
**Document Status**: Active

## Overview

This document defines the Document Filing System v3.0 used across all projects. This system ensures consistent, searchable, and well-organized documentation.

## File Naming Convention

### Format
```
NNN-CC-ABCD-description.ext
```

### Components

- **NNN**: Zero-padded sequence number (001-999)
  - Enforces chronological ordering
  - Shows document creation timeline
  - Prevents naming conflicts

- **CC**: Two-letter category code (see categories below)
  - Groups related documents
  - Enables quick filtering
  - Standardizes classification

- **ABCD**: Four-letter document type abbreviation
  - Identifies document purpose
  - Consistent across projects
  - Searchable patterns

- **description**: Brief description (1-4 words)
  - Kebab-case, lowercase
  - Clear and specific
  - No special characters

- **ext**: File extension
  - `.md` for markdown
  - `.pdf` for PDFs
  - `.txt` for plain text

## Category Codes (CC)

| Code | Category | Use Cases |
|------|----------|-----------|
| **PP** | Product & Planning | Requirements, roadmaps, feature specs, business planning |
| **AT** | Architecture & Technical | System design, technical decisions, API specs |
| **DC** | Development & Code | Code documentation, module guides, implementation notes |
| **TQ** | Testing & Quality | Test plans, QA reports, bug tracking, quality metrics |
| **OD** | Operations & Deployment | DevOps guides, deployment procedures, monitoring |
| **LS** | Logs & Status | Status updates, progress logs, sprint notes |
| **RA** | Reports & Analysis | Analytics, research, intelligence gathering |
| **MC** | Meetings & Communication | Meeting notes, memos, team updates |
| **PM** | Project Management | Tasks, timelines, resource planning, risks |
| **DR** | Documentation & Reference | Guides, manuals, SOPs, standards |
| **UC** | User & Customer | User documentation, training materials, FAQs |
| **BL** | Business & Legal | Contracts, compliance, licenses, agreements |
| **RL** | Research & Learning | Experiments, POCs, learning notes, exploration |
| **AA** | After Action & Review | Post-mortems, retrospectives, lessons learned |
| **MS** | Miscellaneous | General, drafts, temporary, archives |

## Document Type Abbreviations (ABCD)

### Common Types

| Code | Type | Description |
|------|------|-------------|
| **PLAN** | Planning Document | Project plans, strategic planning |
| **ARCH** | Architecture | System architecture, design docs |
| **SPEC** | Specification | Technical specifications, requirements |
| **GUID** | Guide | User guides, how-to documentation |
| **PROC** | Procedure | Step-by-step procedures, SOPs |
| **TEST** | Test Document | Test plans, test cases, QA docs |
| **REPT** | Report | Status reports, analysis reports |
| **MEET** | Meeting Notes | Meeting minutes, decisions |
| **TASK** | Task Documentation | Task lists, work items |
| **SUMM** | Summary | Executive summaries, overviews |
| **CHKL** | Checklist | Validation checklists, review lists |
| **RELS** | Release Notes | Version updates, changelogs |
| **INTL** | Intelligence | Research, market analysis |
| **META** | Metadata | About documentation itself |
| **ROAD** | Roadmap | Development roadmap, timelines |

## Directory Structure

### Standard Layout
```
project-root/
└── 000-docs/                    # FLAT structure - NO subdirectories
    ├── README.md               # Index of all documents
    ├── 001-PP-PLAN-project-overview.md
    ├── 002-AT-ARCH-system-design.md
    ├── 003-DC-GUID-setup-guide.md
    └── ...
```

### Rules

1. **FLAT Structure**: All documents in single `000-docs/` directory
2. **No Subdirectories**: Keeps structure simple and searchable
3. **Sequential Numbering**: Shows creation order and history
4. **Consistent Naming**: Enables grep/find operations

## Document Header Template

Every document should start with:

```yaml
---
doc_id: NNN-CC-ABCD-description
title: Full Document Title
category: Category Name
status: Active|Draft|Review|Archived
classification: Public|Internal|Confidential
repository: repository-name
related_docs:
  - doc-id-1
  - doc-id-2
---
```

## Document Sections

### Standard Structure

1. **Title & Metadata**
   - Document header (YAML)
   - Main title
   - Quick reference line
   - Last updated timestamp

2. **Executive Summary**
   - Brief overview
   - Key points
   - Purpose statement

3. **Main Content**
   - Organized sections
   - Clear headings
   - Bullet points for lists

4. **Document Control**
   - Change log
   - Review cycle
   - Approvers
   - Related documents

## Search & Discovery

### Finding Documents

```bash
# Find all planning documents
ls 000-docs/*-PP-*

# Find all architecture documents
ls 000-docs/*-AT-*

# Search for specific content
grep -l "keyword" 000-docs/*.md

# Find documents by type
ls 000-docs/*-ARCH-*
```

### Indexing

The `000-docs/README.md` serves as master index:
- Lists all documents
- Groups by category
- Provides descriptions
- Links to files

## Best Practices

### Do's

1. **Use sequential numbering** - Never skip numbers
2. **Keep descriptions brief** - 1-4 words maximum
3. **Update README.md** - Add new docs to index
4. **Include metadata** - Use header template
5. **Regular reviews** - Keep documents current

### Don'ts

1. **Don't create subdirectories** - Keep flat structure
2. **Don't reuse numbers** - Even if deleting docs
3. **Don't use spaces** - Use kebab-case
4. **Don't skip metadata** - Always include header
5. **Don't mix categories** - One category per doc

## Migration Guide

### From Unstructured to v3.0

1. **Inventory existing docs**
   ```bash
   find . -name "*.md" -o -name "*.pdf" -o -name "*.txt"
   ```

2. **Categorize documents**
   - Review content
   - Assign category code
   - Determine document type

3. **Rename systematically**
   ```bash
   # Example rename
   mv "Project Plan.md" "001-PP-PLAN-initial-project.md"
   ```

4. **Add headers**
   - Insert YAML header
   - Add metadata
   - Link related docs

5. **Update index**
   - Create/update README.md
   - List all documents
   - Group by category

## Examples

### Good Examples

```
001-PP-PLAN-project-kickoff.md
002-AT-ARCH-system-design.md
003-DC-GUID-api-reference.md
004-TQ-TEST-integration-tests.md
005-OD-PROC-deployment-steps.md
```

### Bad Examples

```
project plan.md           # Spaces, no structure
001_project_plan.md      # Wrong separators
PP-project-plan.md       # Missing sequence number
001-plan.md              # Missing category and type
```

## Automation Tools

### Generate Next Number

```bash
#!/bin/bash
# Get next document number
last_num=$(ls 000-docs/ | grep -E "^[0-9]{3}-" | tail -1 | cut -d'-' -f1)
next_num=$(printf "%03d" $((10#$last_num + 1)))
echo "Next number: $next_num"
```

### Validate Naming

```bash
#!/bin/bash
# Check if filename follows convention
if [[ $1 =~ ^[0-9]{3}-[A-Z]{2}-[A-Z]{4}-[a-z0-9-]+\.(md|pdf|txt)$ ]]; then
    echo "Valid filename"
else
    echo "Invalid filename"
fi
```

## Maintenance

### Regular Tasks

1. **Weekly**: Review new documents for compliance
2. **Monthly**: Update index README.md
3. **Quarterly**: Archive outdated documents
4. **Annually**: Review category codes and types

### Document Lifecycle

1. **Draft**: Initial creation
2. **Review**: Peer review and feedback
3. **Active**: Current and maintained
4. **Archived**: Historical reference only

## FAQ

**Q: Can I create subdirectories in 000-docs?**
A: No, maintain flat structure for simplicity.

**Q: What if I need more than 999 documents?**
A: Archive old documents or start new series (1000+).

**Q: Can I change document numbers?**
A: No, numbers are permanent for history tracking.

**Q: How do I handle document versions?**
A: Update in place, maintain change log in document.

**Q: What about binary files?**
A: Follow same naming, store in 000-docs.

---

## Document Control

### Change Log
- Initial version - Complete v3.0 filing system documentation

### Review Cycle
- Reviewed quarterly
- Updated based on usage patterns

### Related Documents
- [000-docs/README.md](./README.md) - Document index
- Project-specific filing guides

### Implementation Status
- **Current Version**: 3.0
- **Adopted**: All new projects
- **Migration**: Ongoing for existing projects