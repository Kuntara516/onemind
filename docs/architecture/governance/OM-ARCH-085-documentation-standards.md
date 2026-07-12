---
title: Documentation Standards
document_id: OM-ARCH-085
version: 1.0.0
status: Approved
owner: OneMind Architecture Team
classification: Internal

created: 2026-07-12
last_updated: 2026-07-12

parent: Architecture Governance
category: Engineering Standards
tags:
  - documentation
  - standards
  - governance
---

# Documentation Standards

> **Consistent documentation is essential for preserving architectural knowledge, ensuring traceability, and enabling collaboration across people and AI assistants.**

---

# 1. Purpose

This document defines the official documentation standards for the OneMind repository.

The objectives are to:

- Standardize all documentation.
- Improve readability.
- Preserve long-term maintainability.
- Enable consistent AI-assisted authoring.
- Support enterprise governance.
- Maintain repository integrity.

All documentation within the OneMind repository shall comply with this standard.

---

# 2. Scope

These standards apply to:

- Architecture documents
- ADRs
- Business documents
- Technical specifications
- Standards
- Governance documents
- Design documents
- AI documentation
- API documentation
- Deployment documentation
- Markdown documents

---

# 3. Documentation Principles

Documentation shall be:

- Clear
- Accurate
- Consistent
- Traceable
- Version controlled
- Reviewable
- Technology-neutral where possible

Documentation is considered part of the product and shall be maintained with the same discipline as source code.

---

# 4. Repository Structure

Documentation shall be organized according to the approved repository structure.

Top-level folders are frozen and shall not be modified without explicit approval.

New documents shall be added within the existing directory hierarchy.

---

# 5. Document Metadata

Every document shall begin with a YAML metadata block.

Required fields:

```yaml
title:
document_id:
version:
status:
owner:
classification:
created:
last_updated:
parent:
category:
tags:
```

Optional fields:

```yaml
reviewer:
approved_by:
related_documents:
related_adrs:
```

---

# 6. Document Status

Allowed status values are:

- Draft
- Review
- Approved
- Deprecated
- Archived

Only **Approved** documents are considered authoritative.

---

# 7. Versioning

Documentation shall follow Semantic Versioning.

| Version | Meaning |
|----------|---------|
| Major | Significant structural or conceptual change |
| Minor | New sections or substantial enhancements |
| Patch | Editorial corrections or clarifications |

Examples:

- 1.0.0
- 1.1.0
- 1.1.1
- 2.0.0

---

# 8. Document ID Convention

Every controlled document shall have a unique identifier.

Format:

```
OM-ARCH-###
```

Examples:

```
OM-ARCH-080
OM-ARCH-081
OM-ARCH-090
```

Document IDs are permanent.

They shall never be reused.

---

# 9. File Naming Convention

File names shall:

- Use lowercase.
- Use hyphens.
- Avoid spaces.
- Be descriptive.
- Match the document title.

Example:

```
om-arch-085-documentation-standards.md
```

Repository numbering shall remain consistent with the Document ID.

---

# 10. Section Numbering

Documents shall use hierarchical numbering.

Example:

```
1.
1.1
1.2

2.
2.1

3.
```

This enables stable cross-referencing.

---

# 11. Writing Standards

Documentation shall:

- Use concise language.
- Avoid unnecessary repetition.
- Define technical terms.
- Use active voice where appropriate.
- Maintain a professional tone.
- Use consistent terminology from OM-ARCH-083.

---

# 12. Markdown Standards

Preferred elements:

- Headings
- Tables
- Bullet lists
- Numbered lists
- Code blocks
- Blockquotes

Avoid excessive formatting.

Markdown should remain readable in plain text.

---

# 13. Tables

Tables shall be used for:

- Comparisons
- Responsibilities
- Standards
- Decision matrices

Example:

| Item | Description |
|------|-------------|

---

# 14. Diagrams

Preferred formats:

- Mermaid
- Draw.io
- C4 Model
- BPMN
- ERD
- Sequence Diagram

Diagram source files shall be version controlled.

---

# 15. Images

Images shall:

- Support understanding.
- Have descriptive filenames.
- Be stored within the repository.
- Be referenced relative to the document.

Images shall not replace architectural explanations.

---

# 16. Cross References

Related documents shall be referenced by:

- Document ID
- Document title

Example:

- OM-ARCH-080 Architecture Principles
- OM-ARCH-081 ADR Framework

Avoid hard-coded URLs where possible.

---

# 17. Change History

Significant document updates shall be recorded in CHANGELOG.md.

Major revisions should summarize:

- What changed
- Why it changed
- Related ADRs

---

# 18. AI Authoring Standards

AI-generated documentation shall:

- Follow this standard.
- Respect frozen repository structures.
- Use approved terminology.
- Preserve document traceability.
- Avoid speculative content.
- Identify assumptions explicitly.

AI shall not introduce undocumented architectural changes.

---

# 19. Human Review

Architecture documents shall be reviewed for:

- Technical accuracy
- Business alignment
- Governance compliance
- Terminology consistency
- Cross-reference validity
- Editorial quality

---

# 20. Repository Rules

Documentation contributors shall:

- Respect frozen repository structures.
- Preserve Document IDs.
- Preserve naming conventions.
- Commit documentation changes promptly.
- Maintain a clean Git history.

---

# 21. Definition of Done

A document is complete when:

- Metadata is complete.
- Document ID is assigned.
- Version is assigned.
- Content is technically reviewed.
- Cross references are validated.
- Naming conventions are followed.
- File is committed to Git.
- Repository is synchronized.

---

# 22. References

- OM-ARCH-080 Architecture Principles
- OM-ARCH-081 Architecture Decision Record Framework
- OM-ARCH-082 Architecture Review Checklist
- OM-ARCH-083 Architecture Glossary
- OM-ARCH-084 Architecture Compliance Framework
- ONEMIND_RULES.md

---

# 23. Summary

Consistent documentation preserves architectural knowledge, improves collaboration, and enables sustainable platform evolution.

By following these standards, OneMind ensures that documentation remains accurate, traceable, maintainable, and valuable throughout the lifecycle of the platform.

---

> **Code evolves. Architecture evolves. Documentation must evolve with them.**
