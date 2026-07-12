---
title: Database Design Standards
document_id: OM-ARCH-088
version: 1.0.0
status: Approved
owner: OneMind Architecture Team
classification: Internal

created: 2026-07-12
last_updated: 2026-07-12

parent: Architecture Governance
category: Engineering Standards
tags:
  - database
  - data
  - postgresql
  - qdrant
  - standards
  - governance
---

# Database Design Standards

> **Data is a strategic asset. Database design shall optimize correctness, integrity, scalability, and knowledge evolution rather than simply storing information.**

---

# 1. Purpose

This document defines the official Database Design Standards for the OneMind platform.

The objectives are to:

- Standardize database design.
- Preserve data integrity.
- Support AI-native architecture.
- Enable long-term scalability.
- Promote data interoperability.
- Ensure security and governance.

---

# 2. Scope

These standards apply to every persistent data store used by OneMind, including:

- PostgreSQL
- pgvector
- Qdrant
- Redis
- Object Storage
- Knowledge Repositories
- Future Graph Database (e.g., Neo4j)
- Cache Stores
- Metadata Repositories

Temporary in-memory data structures are outside the scope of this document.

---

# 3. Database Design Principles

Every database shall be:

- Business-oriented
- Domain-driven
- Secure by Design
- Scalable
- Observable
- Version controlled
- Fully documented

Database design shall follow the principles defined in OM-ARCH-080.

---

# 4. Polyglot Persistence

OneMind adopts **Polyglot Persistence**.

Each database technology shall be selected according to its strengths.

| Database | Primary Responsibility |
|----------|------------------------|
| PostgreSQL | System of Record (Transactional Data) |
| pgvector | Lightweight Semantic Search |
| Qdrant | AI Memory & Large-scale Vector Search |
| Redis | Cache / Session / Queue |
| Object Storage | Documents & Binary Assets |
| Graph Database (Future) | Knowledge Graph & Relationships |

A single database technology shall not be forced to solve every problem.

---

# 5. Database Selection Guidelines

Use PostgreSQL when:

- ACID transactions are required.
- Business entities are managed.
- Relational integrity is important.
- Reporting is required.

Use pgvector when:

- Small semantic search is sufficient.
- Embeddings remain closely coupled to relational records.

Use Qdrant when:

- Millions of vectors are expected.
- Agent Memory is required.
- Semantic retrieval is a core capability.
- High-performance similarity search is required.

Use Redis when:

- Low-latency access is required.
- Data is ephemeral.
- Distributed locking or caching is needed.

---

# 6. Data Ownership

Every dataset shall have:

- Business Owner
- Technical Owner
- Domain
- Classification
- Retention Policy

Ownership shall be explicitly documented.

---

# 7. Domain-Oriented Data

Each domain shall own its data.

Cross-domain access shall occur through:

- APIs
- Events
- Approved data sharing mechanisms

Direct cross-domain database access is prohibited.

---

# 8. Data Classification

Every dataset shall be classified.

| Classification | Description |
|---------------|-------------|
| Public | Publicly available |
| Internal | Internal operational data |
| Confidential | Restricted business data |
| Sensitive | Personal or regulated information |

Classification determines security controls.

---

# 9. Relational Database Standards

Relational schemas shall:

- Use normalized structures (minimum Third Normal Form unless justified).
- Define primary keys.
- Define foreign keys.
- Enforce referential integrity.
- Avoid duplicated business data.
- Use surrogate keys where appropriate.

Denormalization requires documented justification.

---

# 10. Naming Conventions

Database objects shall use snake_case.

Examples:

```
users
user_profiles
workflow_tasks
knowledge_articles
agent_memory
```

Primary keys:

```
id
```

Foreign keys:

```
user_id
agent_id
workflow_id
```

Timestamp fields:

```
created_at
updated_at
deleted_at
```

---

# 11. Audit Columns

Every business table shall include:

```
created_at
updated_at
created_by
updated_by
```

Where soft deletion is used:

```
deleted_at
deleted_by
```

Audit data shall never be removed without policy approval.

---

# 12. Data Integrity

The following shall be enforced where applicable:

- Primary Keys
- Foreign Keys
- Unique Constraints
- Check Constraints
- NOT NULL Constraints
- Transaction Integrity

Business rules shall not rely solely on application logic.

---

# 13. Vector Database Standards

Vector collections shall define:

- Collection name
- Embedding model
- Embedding dimensions
- Distance metric
- Metadata schema
- Retention policy

Vector metadata shall remain synchronized with the source of truth.

---

# 14. Embedding Standards

Each embedding shall include metadata such as:

- Source ID
- Source Type
- Domain
- Owner
- Language
- Version
- Created Timestamp
- Embedding Model

Embeddings shall be regenerated when the underlying content changes significantly.

---

# 15. AI Memory Standards

Long-term AI Memory shall be stored separately from transactional data.

Memory records shall identify:

- Agent
- User
- Session
- Context
- Confidence
- Expiration Policy
- Privacy Classification

Memory lifecycle shall comply with the Memory Architecture.

---

# 16. Knowledge Repository Standards

Knowledge repositories shall support:

- Versioning
- Metadata
- Source Traceability
- Document Ownership
- Classification
- Semantic Indexing

Knowledge shall never exist without provenance.

---

# 17. Performance Standards

Database design shall consider:

- Indexing
- Query optimization
- Partitioning
- Connection pooling
- Caching
- Compression

Performance optimizations shall not compromise data integrity.

---

# 18. Backup and Recovery

Every persistent data store shall define:

- Backup frequency
- Retention period
- Recovery Point Objective (RPO)
- Recovery Time Objective (RTO)
- Restore verification procedure

Backup restoration shall be tested periodically.

---

# 19. Security Standards

Databases shall implement:

- Encryption at rest
- Encryption in transit
- Authentication
- Role-based access control
- Audit logging
- Secret management

Administrative access shall be restricted.

---

# 20. Privacy Standards

Personal data shall comply with:

- PDPA
- Privacy by Design
- Data minimization
- Retention policies
- Right to erasure where applicable

Sensitive data shall be masked or encrypted.

---

# 21. Data Lifecycle

The lifecycle shall include:

```
Create

↓

Validate

↓

Store

↓

Use

↓

Archive

↓

Dispose
```

Lifecycle policies shall be documented for every major dataset.

---

# 22. Documentation Requirements

Every database shall have documentation covering:

- Purpose
- Owner
- Schema
- Relationships
- Data Dictionary
- Backup Strategy
- Security Controls
- Related ADRs

ER diagrams shall accompany relational schemas.

---

# 23. Definition of Done

A database design is complete when:

- Domain ownership is defined.
- Schema is documented.
- Naming standards are followed.
- Integrity constraints are implemented.
- Security controls are defined.
- Backup strategy is documented.
- Related ADRs are referenced.
- Architecture Review is approved.

---

# 24. References

- OM-ARCH-080 Architecture Principles
- OM-ARCH-081 Architecture Decision Record Framework
- OM-ARCH-085 Documentation Standards
- OM-ARCH-087 API Design Standards
- OM-DATA-030 Data Architecture
- OM-DATA-031 Memory Architecture
- OM-DATA-032 Knowledge Architecture
- ADR-001 PostgreSQL
- ADR-002 Qdrant

---

# 25. Summary

OneMind adopts a polyglot persistence strategy in which each database technology serves a specific architectural responsibility.

Relational databases provide transactional integrity, vector databases enable semantic intelligence, memory stores support AI agents, and future graph databases will model complex knowledge relationships. Together, these technologies form a unified enterprise data platform that supports both operational excellence and AI-native capabilities.

---

> **Choose the right database for the right responsibility. Data architecture is about fitness for purpose, not technology preference.**