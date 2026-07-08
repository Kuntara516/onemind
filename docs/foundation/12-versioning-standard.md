---
title: OneMind Versioning Standard

document_id: VER-012

document_type: Standard

version: 1.0.0

status: Active

owner: OneMind Core Team

authors:
  - OneMind Founders

reviewers: []

created: 2026-07-07

last_updated: 2026-07-07

review_cycle: Annual

tags:
  - versioning
  - semantic-versioning
  - governance

related_documents:
  - ONEMIND.md
  - docs/foundation/11-document-standard.md

source_of_truth: true
---

# OneMind Versioning Standard

## Purpose

This document defines the official versioning policy for all OneMind artifacts.

Versioning ensures consistency, traceability, compatibility, and controlled evolution across the entire platform.

---

# Scope

This standard applies to:

- Documentation
- APIs
- Platform Components
- Applications
- AI Agents
- Prompts
- Workflows
- MCP Servers
- Database Schemas
- Infrastructure
- Docker Images
- SDKs

---

# Semantic Versioning

OneMind adopts Semantic Versioning (SemVer).

```
MAJOR.MINOR.PATCH
```

Example

```
1.0.0
1.2.0
1.2.5
2.0.0
```

---

# MAJOR

Increase when introducing breaking changes.

Examples

- API incompatible
- Database incompatible
- Architecture redesign

---

# MINOR

Increase when adding backward-compatible functionality.

Examples

- New feature
- New AI Agent
- New module
- New integration

---

# PATCH

Increase for backward-compatible fixes.

Examples

- Documentation updates
- Bug fixes
- Performance improvements
- Security patches

---

# Document Versioning

Every Markdown document SHALL contain

```
version:
```

Example

```
version: 1.0.0
```

---

# API Versioning

REST APIs shall use

```
/api/v1/
```

Major version only.

---

# Database Versioning

Database migrations SHALL be incremental.

Example

```
V001__init.sql
V002__create_users.sql
V003__add_indexes.sql
```

---

# Docker Images

```
onemind-api:1.0.0
```

Avoid using

```
latest
```

in production.

---

# AI Prompt Versioning

Prompts SHALL be versioned.

Example

```
prompt-user-summary-v1.0.0.md
```

---

# Workflow Versioning

Every workflow SHALL include

```
version
```

inside its metadata.

---

# Release Tags

Git tags SHALL follow

```
v1.0.0
v1.1.0
v2.0.0
```

---

# Breaking Changes

Breaking changes require

- RFC
- ADR (if architecture changes)
- Changelog update
- Migration guide

---

# Revision History

| Version | Date | Description |
|----------|------------|-------------|
| 1.0.0 | 2026-07-07 | Initial release |

---

**End of Document**