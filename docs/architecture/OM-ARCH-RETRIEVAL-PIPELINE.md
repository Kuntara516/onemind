# OneMind Retrieval Pipeline Architecture

## Document Information

| Field | Value |
|---|---|
| Document | Retrieval Pipeline Architecture |
| Version | v0.8.2 |
| Sprint | Sprint 4 - Context Intelligence & Retrieval Pipeline |
| Status | Foundation Complete |
| Related Components | Context Builder, Memory Foundation, Knowledge Foundation |
| ADR | ADR-001 Async-First Runtime Architecture |

---

# 1. Overview

The Retrieval Pipeline is a core component of the OneMind Context Intelligence Layer.

Its responsibility is to provide a unified retrieval abstraction for obtaining relevant information required during agent execution.

The Retrieval Pipeline separates:

- Context construction
- Information retrieval
- Data storage implementation

This allows OneMind agents to consume contextual information without knowing where the information originates.

---

# 2. Problem Statement

Before Retrieval Pipeline:


Context Builder

  |
  v

Memory Service


The Context Builder directly depended on a specific information source.

This creates limitations:

- difficult to add new retrieval sources
- difficult to combine memory and knowledge
- difficult to introduce ranking and optimization
- tight coupling between context and storage

---

# 3. Retrieval Pipeline Goal

After Retrieval Pipeline:


Context Builder

    |
    v

Retrieval Service

    |
    v

Retrieval Strategy

    |
    +----------------+
    |                |
    v                v

Memory Retrieval Knowledge Retrieval


The Context Layer consumes retrieval results without dependency on underlying implementations.

---

# 4. Architecture Position

The Retrieval Pipeline is located between Context Intelligence and Foundation Layers.


+--------------------------------+
| Agent Runtime |
+--------------------------------+

          |
          v

+--------------------------------+
| Context Intelligence |
| |
| Context Builder |
| |
+--------------------------------+

          |
          v

+--------------------------------+
| Retrieval Pipeline |
| |
| Retrieval Service |
| Retrieval Interface |
| Retrieval Strategies |
| |
+--------------------------------+

          |
          v

+--------------------------------+
| Foundation Layer |
| |
| Memory Service |
| Knowledge Service |
| Vector Store |
| Embedding Service |
| |
+--------------------------------+


---

# 5. Core Components

## 5.1 Retrieval Request

Location:


services/agent-runtime/app/retrieval/models.py


Purpose:

Represents retrieval requirements from upper layers.

Structure:

```python
RetrievalRequest

- query
- limit
- filters
- metadata

Example:

RetrievalRequest(
    query="user preference",
    limit=5
)
5.2 Retrieval Result

Purpose:

Provides normalized retrieval output.

Structure:

RetrievalResult

- memories
- knowledge
- sources
- metadata

The result intentionally does not expose storage implementation details.

6. Retrieval Interface

Location:

services/agent-runtime/app/retrieval/interface.py

The interface defines the retrieval contract.

RetrievalInterface

        |
        +-- retrieve()


Example:

async def retrieve(
    request: RetrievalRequest,
) -> RetrievalResult:
    ...
7. Default Retrieval Strategy

Location:

services/agent-runtime/app/retrieval/strategies/default.py

Current implementation:

DefaultRetriever

        |
        v

MemoryService

        |
        v

Memory Provider

Responsibilities:

receive retrieval request
translate request into memory query
retrieve memories
normalize output
8. Retrieval Service Layer

Location:

services/agent-runtime/app/retrieval/service.py

The Retrieval Service provides the application boundary.

Responsibilities:

validate retrieval requests
delegate retrieval operation
hide strategy implementation
provide stable API for Context Layer

Flow:

Context Builder

        |
        v

RetrievalService

        |
        v

RetrievalInterface

        |
        v

DefaultRetriever
9. Dependency Rules
Allowed Dependencies
Context Builder
        |
        v
Retrieval Service
        |
        v
Retrieval Strategy
        |
        v
Memory / Knowledge Services
Forbidden Dependencies

Context Layer must not directly access:

X Memory Provider
X Qdrant
X Vector Store
X Embedding Provider
X Database

All access must go through service boundaries.

10. Async Runtime Design

Retrieval Pipeline follows ADR-001:

async request

      |
      v

RetrievalService

      |
      v

await retrieve()

      |
      v

RetrievalResult

All retrieval operations are designed for future:

vector search
hybrid search
distributed retrieval
external knowledge sources
11. Future Extensions
Hybrid Retrieval

Future:

Retrieval Pipeline

        |
        +----------------+
        |                |
        v                v

 Keyword Search     Vector Search

        |
        v

 Ranking Layer
Knowledge Retrieval

Future:

Retrieval Strategy

        |
        +----------------+
        |
        v

Knowledge Service
Context Optimization

Future pipeline:

Retrieval

    |
    v

Ranking

    |
    v

Compression

    |
    v

Context Builder
12. Current Implementation Status

Sprint 4 - S4-002

[✓] Retrieval package structure

[✓] Retrieval models

[✓] Retrieval interface

[✓] Default retrieval strategy

[✓] Retrieval service facade

[✓] Retrieval tests

[✓] Regression validation
13. Test Validation

Current regression:

56 passed
0 failed

Retrieval tests validate:

retrieval strategy execution
service delegation
request validation
memory retrieval integration
14. Conclusion

The Retrieval Pipeline establishes the foundation for OneMind Context Intelligence.

It introduces:

retrieval abstraction
strategy-based extensibility
service boundary isolation
future RAG compatibility

This enables OneMind agents to consume intelligent context without coupling to underlying knowledge sources.


บันทึกไฟล์นี้ที่:

```text
docs/architecture/OM-ARCH-RETRIEVAL-PIPELINE.md