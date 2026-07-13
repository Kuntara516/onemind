# OM-DES-204

## Naming & Design Conventions

**Document ID:** OM-DES-204

**Document Title:** Naming & Design Conventions

**Domain:** Solution Design

**Version:** 1.0

**Status:** Draft

**Owner:** OneMind Architecture Team

**Classification:** Internal

---

# 1. Purpose

This document establishes the naming conventions and design conventions used throughout the OneMind Enterprise AI Operating Platform.

Consistent naming improves readability, traceability, maintainability, and communication across architecture, design, implementation, operations, and documentation.

These conventions apply to all future Solution Design documents and implementation artifacts unless explicitly overridden by an approved standard.

---

# 2. Scope

This standard applies to:

* Documents
* Domains
* Components
* Services
* APIs
* Events
* Agents
* Workflows
* Prompts
* Knowledge Assets
* Data Models
* Infrastructure
* Source Code References

---

# 3. General Naming Principles

Names should be:

* Clear
* Meaningful
* Consistent
* Stable
* Technology Neutral
* Business Oriented

Avoid:

* Temporary names
* Personal abbreviations
* Vendor-specific terminology
* Ambiguous acronyms
* Version numbers in names

---

# 4. Repository Conventions

Repository folders shall remain stable.

```text
docs/
core/
agents/
knowledge/
memory/
rag/
mcp/
workflows/
docker/
ui/
```

Top-level repository structure is considered frozen and shall not be changed without an approved architecture decision.

---

# 5. Document Naming

## Document ID

```text
OM-DES-###
```

Example

```text
OM-DES-221
```

---

## File Name

```text
OM-DES-221-Agent-Runtime-Component.md
```

Rules

* Title Case
* Hyphen Separated
* Markdown (.md)
* No spaces
* No underscores
* No version number in filename

---

# 6. Domain Naming

Domains shall use business-oriented nouns.

Examples

```text
Identity

Knowledge

Memory

Workflow

Agent

Administration

Analytics

Notification
```

Avoid names based solely on technology.

---

# 7. Component Naming

Component names shall follow:

```text
<Noun> Service
```

Examples

```text
Knowledge Service

Workflow Service

Memory Service

Notification Service

Identity Service
```

Runtime components may use:

```text
Agent Runtime

Workflow Runtime

Knowledge Runtime
```

---

# 8. API Naming

REST resources should use plural nouns.

Examples

```text
/api/v1/agents

/api/v1/workflows

/api/v1/prompts

/api/v1/memories

/api/v1/users
```

Rules

* lowercase
* hyphen-separated
* nouns only
* versioned
* resource oriented

---

# 9. Event Naming

Event format

```text
Domain.Entity.Action
```

Examples

```text
Workflow.Created

Workflow.Completed

Knowledge.Indexed

Prompt.Published

Agent.Started

Agent.Completed

Memory.Updated
```

Events shall be written in past tense where they describe completed actions.

---

# 10. Agent Naming

Agents shall follow:

```text
<Role> Agent
```

Examples

```text
Planner Agent

Coordinator Agent

Research Agent

Validator Agent

Developer Agent

Reviewer Agent

Executor Agent
```

Avoid implementation-specific names.

---

# 11. Workflow Naming

Workflow names shall describe the business objective.

Examples

```text
Incident Resolution

Customer Onboarding

Knowledge Approval

Document Classification

Expense Approval
```

Avoid technical names such as:

```text
Workflow A

Flow 1

Pipeline X
```

---

# 12. Prompt Naming

Prompt format

```text
<Category>-<Purpose>
```

Examples

```text
Planning-Task-Breakdown

Support-Customer-Response

Coding-Code-Review

Research-Web-Search

Knowledge-Summarization
```

Prompts shall be:

* Version Controlled
* Reusable
* Reviewable
* Traceable

---

# 13. Data Naming

Entities

```text
User

Agent

Workflow

Conversation

KnowledgeItem

MemoryEntry
```

Primary Keys

```text
UserId

WorkflowId

AgentId

ConversationId
```

Foreign Keys

```text
CreatedBy

UpdatedBy

KnowledgeId
```

---

# 14. Configuration Naming

Environment variables

```text
UPPER_CASE
```

Examples

```text
DATABASE_URL

OPENAI_API_KEY

OLLAMA_HOST

VECTOR_DB_URL

LOG_LEVEL
```

---

# 15. Container Naming

Containers

```text
onemind-api

onemind-agent

onemind-worker

onemind-postgres

onemind-qdrant

onemind-redis
```

Networks

```text
onemind-network
```

Volumes

```text
onemind-data

onemind-memory

onemind-models
```

---

# 16. Logging Conventions

Log entries should include:

* Timestamp
* Correlation ID
* Component
* Severity
* Message

Severity levels

```text
DEBUG

INFO

WARN

ERROR

FATAL
```

---

# 17. Error Code Convention

Format

```text
OM-<DOMAIN>-<NUMBER>
```

Examples

```text
OM-AUTH-001

OM-WORKFLOW-014

OM-AGENT-003

OM-MEMORY-021
```

Error messages should be:

* Human readable
* Actionable
* Traceable

---

# 18. Documentation Cross-References

Cross-document references shall use:

```text
OM-BIZ

OM-ARCH

OM-SOL

OM-DES
```

Avoid referencing filenames in narrative text. Use permanent document identifiers whenever possible.

---

# 19. Design Decision Records

Major design decisions should be documented using a consistent identifier.

Format

```text
DDR-001

DDR-002

DDR-003
```

Each Design Decision Record should contain:

* Context
* Decision
* Alternatives Considered
* Consequences
* Related Documents

---

# 20. Traceability Convention

Every Solution Design document should identify:

* Parent Architecture Document(s)
* Related Design Standards
* Related Design Principles
* Applicable Design Patterns
* Future Implementation References

This maintains end-to-end traceability across the repository.

---

# 21. Future Compatibility

These conventions are designed to support future implementation artifacts including:

* Source Code
* API Specifications
* Infrastructure as Code
* CI/CD Pipelines
* Test Specifications
* Operational Runbooks
* Developer Documentation

Consistent naming enables automation, documentation generation, and repository scalability.

---

# 22. Summary

The OneMind Naming & Design Conventions provide a common language for architecture, design, development, and operations.

By following these conventions, all repository artifacts remain predictable, traceable, and maintainable throughout the lifecycle of the platform.

---

**End of Document**

**Document ID:** OM-DES-204

**Version:** 1.0

**Status:** Draft

**Milestone:** M5 – Solution Design

**Many Agents. One Mind.**
