---
title: Coding and Repository Standards
document_id: OM-ARCH-089
version: 1.0.0
status: Approved
owner: OneMind Architecture Team
classification: Internal

created: 2026-07-12
last_updated: 2026-07-12

parent: Architecture Governance
category: Engineering Standards
tags:
  - coding
  - repository
  - git
  - standards
  - governance
---

# Coding and Repository Standards

> **Source code is a long-term knowledge asset. Repository organization, coding conventions, and Git discipline are fundamental to maintaining a sustainable AI-native platform.**

---

# 1. Purpose

This document defines the official Coding and Repository Standards for the OneMind platform.

The objectives are to:

- Improve code quality.
- Standardize repository organization.
- Support AI-assisted development.
- Maintain a clean Git history.
- Enable collaboration.
- Reduce technical debt.

---

# 2. Scope

These standards apply to:

- Source code
- Configuration files
- Infrastructure as Code
- AI Agents
- MCP Servers
- Workflows
- Documentation
- Tests
- Scripts
- Docker assets
- CI/CD pipelines

---

# 3. Engineering Principles

Development shall follow:

- Simplicity
- Readability
- Maintainability
- Reusability
- Testability
- Security by Design
- Documentation by Design

Code is maintained far longer than it is written.

---

# 4. Repository Structure

Top-level repository structure is frozen.

No new top-level folders may be introduced without Architecture Board approval.

New artifacts shall be placed within the approved directory hierarchy.

---

# 5. Repository Organization

Each directory shall have a single responsibility.

Example:

```
ai/
knowledge/
agents/
memory/
mcp/
workflows/
docker/
docs/
tests/
scripts/
```

Avoid duplicate responsibilities across folders.

---

# 6. Naming Conventions

Use:

- lowercase
- snake_case (database)
- kebab-case (files)
- PascalCase (classes)
- camelCase (variables/functions where language conventions apply)

Names shall clearly express intent.

Avoid unnecessary abbreviations.

---

# 7. Source Code Organization

Source code shall be organized by:

- Domain
- Capability
- Feature

Avoid organizing by technology alone.

Preferred:

```
agents/

knowledge/

memory/

workflow/
```

Avoid:

```
controllers/

services/

models/
```

at the repository root.

---

# 8. Code Style

Code shall:

- Follow language-specific style guides.
- Be consistently formatted.
- Avoid dead code.
- Avoid commented-out implementations.
- Prefer self-documenting code.

Automated formatting is encouraged.

---

# 9. Comments

Comments shall explain:

- Why
- Business rationale
- Architectural decisions

Avoid comments describing obvious code behavior.

Outdated comments shall be removed.

---

# 10. Error Handling

Errors shall:

- Be meaningful.
- Use consistent exception handling.
- Avoid exposing internal implementation.
- Include correlation identifiers where appropriate.

Failures shall be observable.

---

# 11. Logging

Logs shall be:

- Structured
- Machine-readable
- Correlated
- Privacy-aware

Log levels:

- DEBUG
- INFO
- WARN
- ERROR
- FATAL

Sensitive information shall never be logged.

---

# 12. Configuration Management

Configuration shall be externalized.

Use:

- Environment variables
- Configuration files
- Secret management systems

Never hard-code:

- Passwords
- Tokens
- API Keys
- Connection strings

---

# 13. Secrets Management

Secrets shall be stored only in approved secret management systems.

Examples include:

- Vault
- Cloud Secret Manager
- Docker Secrets

Secrets shall never be committed to Git.

---

# 14. Dependency Management

Dependencies shall:

- Be approved.
- Be actively maintained.
- Be version controlled.
- Be regularly updated.

Unused dependencies shall be removed.

---

# 15. Testing Standards

Every production component shall include appropriate testing.

Testing levels:

- Unit Tests
- Integration Tests
- End-to-End Tests
- Performance Tests
- Security Tests

Critical business logic shall not be released without automated tests.

---

# 16. Git Workflow

OneMind follows a branch-based development model.

Typical workflow:

```
main

↓

feature/*

↓

pull request

↓

review

↓

merge
```

Direct commits to `main` are prohibited.

---

# 17. Branch Naming

Feature branches:

```
feature/agent-memory

feature/api-gateway
```

Bug fixes:

```
fix/login-timeout
```

Documentation:

```
docs/m3-governance
```

Hotfixes:

```
hotfix/security-patch
```

---

# 18. Commit Standards

Commits shall:

- Be atomic.
- Be meaningful.
- Be traceable.

Recommended format:

```
type(scope): description
```

Examples:

```
docs(governance): add architecture principles

feat(memory): implement semantic memory

fix(api): handle timeout errors

refactor(agent): simplify planner workflow
```

Avoid generic messages such as:

```
update

fix

change
```

---

# 19. Pull Request Standards

Every Pull Request shall include:

- Purpose
- Scope
- Related ADRs
- Related Issues
- Testing evidence
- Review checklist

Architecture-impacting changes shall reference applicable ADRs.

---

# 20. Code Review Standards

Reviews shall verify:

- Readability
- Maintainability
- Security
- Performance
- Architecture compliance
- Testing
- Documentation

Review comments shall remain constructive and actionable.

---

# 21. Documentation Requirements

Every significant feature shall include:

- Technical documentation
- Architecture references
- API documentation (if applicable)
- Configuration instructions
- Operational guidance

Code without documentation is considered incomplete.

---

# 22. CI/CD Standards

Continuous Integration shall include:

- Build
- Lint
- Unit Tests
- Security Scan
- Dependency Scan
- Documentation Validation

Deployment pipelines shall be automated wherever practical.

---

# 23. Repository Hygiene

The repository shall remain:

- Organized
- Consistent
- Free of obsolete artifacts

Generated files shall not be committed unless explicitly required.

Large binary files should be avoided.

---

# 24. AI-Assisted Development

AI-generated code shall:

- Be reviewed by humans.
- Follow architecture principles.
- Follow repository standards.
- Include documentation where appropriate.
- Pass automated testing.

AI shall not bypass governance processes.

---

# 25. Compliance

Compliance shall be verified through:

- Code Review
- Pull Request Review
- CI/CD Validation
- Architecture Review
- Security Review

Non-compliant code shall not be merged.

---

# 26. Definition of Done

Code is considered complete when:

- Standards are followed.
- Tests pass.
- Documentation is updated.
- Architecture compliance is verified.
- Security review is complete.
- Pull Request is approved.
- Changes are committed and pushed.

---

# 27. References

- OM-ARCH-080 Architecture Principles
- OM-ARCH-081 ADR Framework
- OM-ARCH-082 Architecture Review Checklist
- OM-ARCH-085 Documentation Standards
- OM-ARCH-086 Architecture Modeling Standards
- OM-ARCH-087 API Design Standards
- OM-ARCH-088 Database Design Standards
- ONEMIND_RULES.md

---

# 28. Summary

Coding standards and repository discipline are essential to sustaining an enterprise-scale AI platform.

By following consistent engineering practices, maintaining a clean repository structure, enforcing Git governance, and integrating documentation into the development lifecycle, OneMind ensures that its codebase remains understandable, maintainable, secure, and ready for long-term evolution.

---

> **A clean repository reflects a disciplined engineering culture. Consistent code enables sustainable innovation.**