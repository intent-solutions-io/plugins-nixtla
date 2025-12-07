# Gemini Code Review Integration Guide

**Document ID**: 097-OD-GUID
**Version**: 1.0.0
**Status**: Active
**Created**: 2025-12-07
**Updated**: 2025-12-07

---

## Overview

This document describes the Gemini Code Assist and Gemini Vertex AI integration for automated code review in the Nixtla Claude Code Plugins repository.

### Components

| Component | Purpose | Trigger |
|-----------|---------|---------|
| Gemini Code Assist (App) | Inline PR comments, suggestions | PR open/update |
| Gemini PR Review (Action) | AI-powered approval/comment | PR open/update |
| Gemini Daily Audit (Action) | 24h change audit | Scheduled 6am CST |

---

## 1. Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Repository                         │
│              intent-solutions-io/plugins-nixtla              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Pull Request Opened                                         │
│        │                                                     │
│        ├──► Gemini Code Assist (GitHub App)                 │
│        │         │                                           │
│        │         └──► Inline comments + suggestions          │
│        │                                                     │
│        └──► gemini-pr-review.yml (GitHub Action)            │
│                  │                                           │
│                  ├──► WIF Auth ──► Vertex AI                │
│                  │                     │                     │
│                  │                     └──► Gemini 3 Pro    │
│                  │                                           │
│                  └──► Approve or Comment on PR              │
│                                                              │
│  Daily 6am CST                                              │
│        │                                                     │
│        └──► gemini-daily-audit.yml                          │
│                  │                                           │
│                  ├──► Get 24h commits                       │
│                  ├──► WIF Auth ──► Vertex AI                │
│                  │                     │                     │
│                  │                     └──► Gemini 3 Pro    │
│                  │                                           │
│                  └──► Create Issue if problems found        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Authentication

### 2.1 Workload Identity Federation (WIF)

Keyless authentication from GitHub Actions to Google Cloud.

| Setting | Value |
|---------|-------|
| GCP Project | `nixtla-playground-01` |
| WIF Pool | `github-pool` |
| WIF Provider | `github-provider` |
| Service Account | `nixtla-github-deployer@nixtla-playground-01.iam.gserviceaccount.com` |

### 2.2 Service Account Permissions

```
roles/aiplatform.user          # Vertex AI API access
roles/iam.workloadIdentityUser # WIF impersonation
```

### 2.3 WIF Principal Binding

```
principalSet://iam.googleapis.com/projects/859338910722/locations/global/workloadIdentityPools/github-pool/attribute.repository/intent-solutions-io/plugins-nixtla
```

---

## 3. Workflows

### 3.1 PR Review Workflow

**File**: `.github/workflows/gemini-pr-review.yml`

**Triggers**:
- `pull_request: [opened, synchronize, reopened]`

**Model**: `gemini-3-pro-preview` (global location)

**Behavior**:
1. Checkout repository
2. Authenticate via WIF
3. Get PR diff
4. Send to Gemini for review
5. Post approve/comment based on response

**Cost**: ~$0.01-0.02 per PR

### 3.2 Daily Audit Workflow

**File**: `.github/workflows/gemini-daily-audit.yml`

**Triggers**:
- `schedule: cron '0 12 * * *'` (6am CST = 12:00 UTC)
- `workflow_dispatch` (manual)

**Model**: `gemini-3-pro-preview` (global location)

**Behavior**:
1. Get commits from last 24 hours
2. Generate diff of all changes
3. Send to Gemini for audit
4. If issues found → Create GitHub Issue
5. If clean → Log success

**Cost**: ~$0.01-0.02 per day (~$0.30-0.60/month)

---

## 4. Configuration Files

### 4.1 Gemini Code Assist

**Directory**: `.gemini/`

| File | Purpose |
|------|---------|
| `config.yaml` | Review settings (severity, auto-review, max comments) |
| `style-guide.md` | Project coding standards for Gemini |

### 4.2 Project Context

**File**: `GEMINI.md` (repo root)

Provides project context to Gemini CLI and Code Assist:
- Project overview
- Tech stack
- Code standards
- Review guidelines

---

## 5. Models

### 5.1 Gemini 3 Pro Preview

- **Model ID**: `gemini-3-pro-preview`
- **Location**: `global` (required for Gemini 3 previews)
- **Features**: Adaptive thinking, 1M token context, grounding
- **Status**: Public Preview (GA expected Q2 2026)

### 5.2 Fallback Models

If Gemini 3 Pro is unavailable:

| Model | Location | Use Case |
|-------|----------|----------|
| `gemini-2.5-pro-preview-05-06` | us-central1 | High quality |
| `gemini-2.0-flash-001` | us-central1 | Fast, cheap |

---

## 6. Cost Analysis

### 6.1 Gemini 3 Pro Preview Pricing (Vertex AI)

| Metric | Price |
|--------|-------|
| Input tokens | ~$1.25 / 1M tokens |
| Output tokens | ~$5.00 / 1M tokens |

### 6.2 Estimated Monthly Costs

| Workflow | Frequency | Est. Cost |
|----------|-----------|-----------|
| PR Review | ~10 PRs/month | $0.10-0.20 |
| Daily Audit | 30 runs/month | $0.30-0.60 |
| **Total** | | **$0.40-0.80/month** |

*Covered by Google Cloud startup credits*

---

## 7. Slash Commands

Available in PR comments:

| Command | Action |
|---------|--------|
| `/gemini review` | Trigger full review |
| `/gemini summary` | Generate PR summary |
| `/gemini help` | List commands |
| `/gemini <question>` | Ask about PR |

---

## 8. Troubleshooting

### 8.1 WIF Authentication Fails

**Error**: `Permission 'iam.serviceAccounts.getAccessToken' denied`

**Fix**: Grant WIF principal access to service account:
```bash
gcloud iam service-accounts add-iam-policy-binding \
  nixtla-github-deployer@nixtla-playground-01.iam.gserviceaccount.com \
  --project=nixtla-playground-01 \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/859338910722/locations/global/workloadIdentityPools/github-pool/attribute.repository/intent-solutions-io/plugins-nixtla"
```

### 8.2 Vertex AI API Disabled

**Error**: `Vertex AI API has not been used in project`

**Fix**:
```bash
gcloud services enable aiplatform.googleapis.com --project=nixtla-playground-01
```

### 8.3 Model Not Found

**Error**: `Model not found` or `thinking not supported`

**Fix**: Ensure using correct model ID and location:
- Gemini 3 previews: `locations/global`
- Gemini 2.x: `locations/us-central1`

---

## 9. Related Documents

- [041-SPEC-nixtla-skill-standard.md](041-SPEC-nixtla-skill-standard.md) - Skill compliance standard
- [GEMINI.md](../GEMINI.md) - Project context for Gemini
- [.gemini/config.yaml](../.gemini/config.yaml) - Code Assist configuration
- [.gemini/style-guide.md](../.gemini/style-guide.md) - Coding standards

---

## 10. APIs Enabled

```bash
# Required GCP APIs for this integration
gcloud services enable \
  aiplatform.googleapis.com \
  cloudaicompanion.googleapis.com \
  developerconnect.googleapis.com \
  geminicodeassistmanagement.googleapis.com \
  --project=nixtla-playground-01
```

---

**Last Updated**: 2025-12-07
**Maintained By**: Intent Solutions (Jeremy Longshore)
**For**: Nixtla (Max Mergenthaler)
