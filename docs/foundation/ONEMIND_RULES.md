---
title: OneMind Project Rules
document_id: OM-RULE-001
version: 1.0.0
status: Active
owner: OneMind Core Team
classification: Internal

created: 2026-07-11
last_updated: 2026-07-11
---

# OneMind Project Rules

> This document defines the working rules for developing the OneMind platform.
>
> These rules apply to all contributors, including human developers and AI assistants.

---

# 1. Purpose

The objective of these rules is to ensure that the OneMind project evolves consistently without introducing architectural drift, repository inconsistency, or undocumented changes.

These rules are mandatory unless explicitly overridden by the project owner.

---

# 2. Source of Truth

The Git repository is the single source of truth.

AI assistants shall never assume repository contents.

All recommendations shall be based on the current repository structure and approved architecture documents.

---

# 3. Repository Freeze Policy

Once a repository structure has been approved and frozen:

- Top-level folders shall not be renamed.
- Top-level folders shall not be relocated.
- Existing document IDs shall not be changed.
- Existing folder names shall not be changed.

New work shall extend the existing structure instead of reorganizing it.

Any improvement proposals shall be added to the Architecture Backlog rather than changing the repository.

---

# 4. Architecture Freeze Policy

Once a milestone is declared Frozen:

- Architecture shall not be redesigned.
- Repository structure shall remain unchanged.
- Document naming conventions shall remain unchanged.
- Document numbering shall remain unchanged.

Enhancements shall be implemented only in future milestones or recorded in the Architecture Backlog.

---

# 5. Markdown Document Rules

Whenever a new Markdown document is created, the AI assistant shall always provide the following information before the document content.

Mandatory format:

Status

File

Location

Document ID

Version

Example

Status:
✅ New File

File:
OM-ARCH-081-architecture-decision-record-framework.md

Location:
docs/architecture/governance/

Document ID:
OM-ARCH-081

Version:
1.0.0

No Markdown document shall be delivered without this header.

---

# 6. Git Commit Rule

Every completed Markdown document shall be followed by a Git commit.

The AI assistant shall always propose an appropriate Conventional Commit message.

Example

git add <file>

git commit -m "docs(governance): add OM-ARCH-081 ADR framework"

git push

No completed document should remain uncommitted.

---

# 7. One File at a Time

The project shall progress one completed document at a time.

Recommended workflow:

1. Create document
2. Save document
3. Git add
4. Git commit
5. Git push
6. Continue with the next document

This keeps the repository synchronized with the project history.

---

# 8. No Hidden Improvements

If an improvement is considered foundational, it shall be included in the current document immediately.

The AI assistant shall not intentionally postpone critical architectural content to future revisions.

---

# 9. Backlog Rule

If an idea conflicts with a frozen architecture, repository structure, or milestone baseline:

- Do not redesign.
- Do not rename.
- Do not relocate.

Instead:

Record the idea in the Architecture Backlog for future evaluation.

---

# 10. Working Principles

The AI assistant shall prioritize:

1. Consistency over novelty
2. Stability over unnecessary optimization
3. Architecture integrity over technology preference
4. Business objectives over implementation details
5. Repository consistency over personal opinion

---

# 11. Collaboration Principles

The AI assistant shall:

- Respect frozen decisions.
- Preserve conceptual integrity.
- Avoid repeated redesign proposals.
- Follow the approved document conventions.
- Maintain traceability across all documents.

---

# 12. Definition of Done

A document is considered complete only when:

- The document has been written.
- The filename has been specified.
- The storage location has been specified.
- The document ID has been specified.
- The version has been specified.
- The Git commit command has been provided.
- The document has been committed.
- The repository is clean.

Only then may work continue to the next document.

---

# Closing Statement

OneMind is developed through disciplined architectural evolution.

Every contributor is responsible for preserving the integrity of the platform by following these rules consistently.

> Build carefully.
> Build consistently.
> Build OneMind.

13. Verify Before Suggesting

Before proposing any repository, architecture, or documentation change,
the AI assistant shall first verify the current repository state.

The AI assistant shall not assume the existence or absence of files,
folders, branches, or documents without verification.
14. Think Before Deliver

Before delivering any foundational document, the AI assistant shall perform an internal completeness review.

The AI assistant shall identify missing principles, governance rules, standards, or foundational content before presenting the document.

Foundational improvements shall be incorporated into the current version instead of being proposed after delivery.

The objective is to minimize iterative corrections and produce documents that are ready for immediate repository commit.
15. Repository Verification

Before proposing any repository, architecture, branch, file, or documentation change, the AI assistant shall verify the current repository state whenever possible.

The AI assistant shall not assume the existence or absence of files, folders, branches, commits, or documents.

Recommendations shall be based on verified repository information rather than assumptions.