---
title: OneMind Document Standard

document_id: DOC-011

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
  - documentation
  - standards
  - governance

related_documents:
  - ONEMIND.md
  - PROJECT.md
  - docs/foundation/09-project-folder-standard.md
  - docs/foundation/12-versioning-standard.md

source_of_truth: true
---

# OneMind Document Standard

## Purpose

This document defines the official documentation standard for the OneMind Project.

Its purpose is to ensure that every document is consistent, searchable, versioned, maintainable, and understandable by both humans and AI systems.

This standard applies to every Markdown document in this repository unless explicitly exempted.

---

# Scope

This standard applies to:

- Foundation Documents
- Architecture Documents
- ADRs
- RFCs
- Specifications
- Design Documents
- API Documentation
- Meeting Notes
- Engineering Journals
- Handoff Logs
- Decision Logs
- Project Documentation

---

# Guiding Principles

Documentation shall be:

- Clear
- Concise
- Consistent
- Versioned
- Searchable
- Reusable
- AI-readable
- Single Source of Truth (SSOT)

Documentation is considered part of the software product.

---

# Rule 1 — YAML Front Matter

Every Markdown document SHALL begin with YAML Front Matter.

Example:

```yaml
---
title: Example Document

document_id: DOC-001

document_type: Standard

version: 1.0.0

status: Active

owner: OneMind Core Team

authors:
  - Your Name

reviewers: []

created: YYYY-MM-DD

last_updated: YYYY-MM-DD

review_cycle: Annual

tags: []

related_documents: []

source_of_truth: true
---
```

---

# Rule 2 — Required Metadata

The following metadata fields are mandatory.

| Field | Required |
|---------|----------|
| title | Yes |
| document_id | Yes |
| document_type | Yes |
| version | Yes |
| status | Yes |
| owner | Yes |
| authors | Yes |
| created | Yes |
| last_updated | Yes |
| review_cycle | Yes |
| tags | Yes |
| related_documents | Yes |
| source_of_truth | Yes |

---

# Rule 3 — Document Status

Only the following values are allowed.

| Status | Meaning |
|----------|---------|
| Draft | Work in progress |
| Review | Under review |
| Approved | Accepted |
| Active | Current official version |
| Deprecated | No longer recommended |
| Archived | Historical reference only |

---

# Rule 4 — Versioning

All documents use Semantic Versioning.

Format

```
Major.Minor.Patch
```

Examples

```
1.0.0
1.1.0
1.1.1
2.0.0
```

---

# Rule 5 — Document ID

Every document SHALL have a unique Document ID.

Examples

| Type | Prefix |
|--------|--------|
| Constitution | FND |
| Charter | CHR |
| Vision | VIS |
| Mission | MIS |
| Principles | PRI |
| Manifesto | MAN |
| Design | DSP |
| Engineering | ENG |
| Governance | GOV |
| Document Standard | DOC |
| Version Standard | VER |
| Git Workflow | GIT |
| Decision Process | DCP |
| ADR | ADR |
| RFC | RFC |
| Specification | SPEC |
| Decision | DEC |
| Journal | JRN |
| Handoff | HOF |
| Meeting | MTG |
| Roadmap | RMP |
| Release | REL |

Document IDs SHALL be unique across the repository.

---

# Rule 6 — File Naming

File names shall use lowercase kebab-case.

Correct

```
project-charter.md

engineering-principles.md

docker-deployment.md
```

Incorrect

```
Project Charter.md

My_File.md

MyDocument.md
```

---

# Rule 7 — Document Structure

Documents should follow this structure whenever applicable.

```
# Title

## Purpose

## Scope

## Content

## References
```

Sections may be omitted only when they are not applicable.

---

# Rule 8 — References

Documents SHALL reference other documents rather than duplicate information.

Use:

- related_documents
- Relative file paths

Avoid copy-and-paste documentation.

The Single Source of Truth (SSOT) shall always be maintained.

---

# Rule 9 — Images

Images shall not be stored inside the documentation folders.

Store images in

```
assets/images/
```

Store diagrams in

```
assets/diagrams/
```

---

# Rule 10 — Diagrams

Diagram source files shall always be preserved.

Preferred formats

- draw.io
- PlantUML
- Mermaid
- Excalidraw

Exported images may be

- SVG
- PNG

---

# Rule 11 — Code Blocks

Always specify the language.

Example

```python
print("Hello OneMind")
```

Avoid unlabeled code blocks.

---

# Rule 12 — Tables

Use standard Markdown tables.

Example

| Column | Description |
|---------|-------------|
| Name | Example |

---

# Rule 13 — Source of Truth

Every important topic shall have exactly one authoritative document.

Other documents SHALL reference it instead of duplicating it.

---

# Rule 14 — Definition of Complete Documentation

A document is considered complete only when:

- Metadata exists
- Version is assigned
- Status is defined
- References are included
- Document ID is assigned
- Markdown formatting is valid

---

# Compliance

Documents that do not comply with this standard SHALL be considered incomplete documentation.

Repository maintainers may reject non-compliant documents during review.

---

# Future Changes

This standard is governed by the OneMind Constitution.

Changes require:

1. RFC
2. Review
3. Approval
4. Version update
5. Changelog entry

---

# Revision History

| Version | Date | Description |
|----------|------------|-----------------------------|
| 1.0.0 | 2026-07-07 | Initial release |

---

**End of Document**