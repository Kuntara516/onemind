# OM-ARCH-KNOWLEDGE-ARCHITECTURE

## Document Information

| Item | Value |
|---|---|
| Project | OneMind |
| Document ID | OM-ARCH-KNOWLEDGE-ARCHITECTURE |
| Domain | Agent Runtime |
| Category | Architecture |
| Status | Draft |
| Version | 1.0 |
| Milestone | M6 Platform Engineering |
| Sprint | Sprint 3 - Memory & Knowledge Foundation |

---

# 1. Purpose

This document defines the Knowledge Layer architecture for the OneMind platform.

The Knowledge Layer provides a unified abstraction for retrieving information from structured and unstructured knowledge sources without coupling Agent Runtime to any specific retrieval technology.

The architecture establishes the foundation for:

- Enterprise knowledge
- Document retrieval
- Vector search
- Structured data access
- External knowledge providers
- Retrieval-Augmented Generation (RAG)

The Knowledge Layer complements the Memory Layer.

Memory answers:

> What does the system remember?

Knowledge answers:

> What can the system retrieve?

---

# 2. Relationship to Memory Layer

Memory and Knowledge are separate architectural domains.

```
                Agent Context

                     |

     +---------------+---------------+

     |                               |

Memory Layer                Knowledge Layer

     |                               |

Remembered State          Retrieved Information
```

Memory stores information that belongs to the runtime.

Knowledge retrieves information that exists outside the runtime.

This separation keeps responsibilities clear while allowing both layers to contribute to Agent Context.

---

# 3. Design Principles

## 3.1 Retrieval First

The Knowledge Layer is retrieval-oriented.

It is not responsible for:

- reasoning
- planning
- prompt generation
- LLM execution

Its responsibility ends when relevant knowledge has been retrieved.

---

## 3.2 Source Independence

Knowledge retrieval must not depend on a specific storage technology.

Supported sources may include:

- Local documents
- Markdown
- PDF
- Databases
- APIs
- Vector databases
- Enterprise systems
- MCP providers
- Cloud services

Runtime behavior must remain unchanged regardless of the source.

---

## 3.3 Interface First

Agents never communicate directly with knowledge sources.

```
Agent

    |

Knowledge Interface

    |

Knowledge Provider

    |

Knowledge Source
```

Replacing the provider must not affect agent logic.

---

## 3.4 Extensibility

Every retrieval technology should be implemented as a provider.

Examples:

```
Knowledge Provider

    |

+-----------+-----------+

|           |           |

Qdrant    PostgreSQL   API

                        |

                    MCP Provider
```

---

# 4. Architecture Position

Sprint 3 extends the runtime pipeline.

```
Execution Request

        |

Execution Service

        |

Executor

        |

Context Enricher

        |

+-------------------------------+

|                               |

Memory Layer            Knowledge Layer

|                               |

+---------------+---------------+

                |

         Context Builder

                |

             Agent Context

                |

               Agent
```

Knowledge contributes information to Context Builder.

It never communicates directly with the Agent.

---

# 5. Responsibilities

The Knowledge Layer is responsible for:

- retrieving information
- abstracting data sources
- ranking retrieval results
- returning normalized knowledge objects
- hiding implementation details

The Knowledge Layer is not responsible for:

- memory management
- execution lifecycle
- prompt construction
- capability execution
- persistence of runtime state

---

# 6. Knowledge Model

Knowledge is categorized by source.

```
Knowledge

├── Documents

├── Structured Data

├── Enterprise Knowledge

├── External APIs

├── Vector Knowledge

└── Future MCP Sources
```

Each source may require different retrieval strategies while sharing a common interface.

---

# 7. Knowledge Sources

## 7.1 Document Knowledge

Examples:

- Markdown
- PDF
- Word
- Text
- Documentation

---

## 7.2 Structured Knowledge

Examples:

- PostgreSQL
- MySQL
- SQLite

Structured retrieval focuses on exact information.

---

## 7.3 Enterprise Knowledge

Examples:

- Internal standards
- Policies
- Procedures
- Architecture documents
- SOPs

---

## 7.4 External Knowledge

Examples:

- REST APIs
- Cloud services
- Third-party integrations

---

## 7.5 Vector Knowledge

Semantic search over embedded content.

Examples:

- Documentation
- Manuals
- Design documents
- Meeting notes

Initial Sprint 3 direction:

- Ollama Embeddings
- Qdrant

---

# 8. Knowledge Lifecycle

Knowledge retrieval occurs during execution.

```
Execution Request

        |

Context Enricher

        |

Knowledge Retrieval

        |

Context Builder

        |

Agent Execution
```

Knowledge itself is not modified during retrieval.

Knowledge ingestion belongs to a separate lifecycle.

---

# 9. Knowledge Ingestion

Knowledge enters the system independently from runtime execution.

```
Knowledge Source

        |

Ingestion Pipeline

        |

Preprocessing

        |

Embedding

        |

Knowledge Store
```

Sprint 3 focuses only on retrieval architecture.

Ingestion implementation is deferred.

---

# 10. Knowledge Interfaces

The Knowledge Layer is composed of abstraction interfaces.

```
Knowledge Provider

        |

Retriever

        |

Knowledge Repository

        |

Storage Adapter
```

Responsibilities:

Knowledge Provider

- Runtime abstraction

Retriever

- Retrieval strategy

Repository

- Source abstraction

Storage Adapter

- Technology implementation

---

# 11. Retrieval Flow

```
Task

    |

Context Enricher

    |

Knowledge Provider

    |

Retriever

    |

Repository

    |

Knowledge Source

    |

Knowledge Result

    |

Context Builder

    |

Agent
```

The Agent receives normalized knowledge only.

---

# 12. Retrieval Strategies

Different strategies may be implemented.

Examples:

## Exact Match

Deterministic retrieval.

Suitable for:

- IDs
- Codes
- Structured data

---

## Keyword Search

Traditional search.

Suitable for:

- Documentation
- Manuals

---

## Semantic Retrieval

Embedding similarity search.

Suitable for:

- Large document collections
- Enterprise knowledge
- Natural language questions

---

## Hybrid Retrieval

Combines multiple retrieval strategies.

Example:

```
Keyword Search

        +

Semantic Search

        +

Business Rules

        =

Ranked Results
```

Hybrid retrieval is outside Sprint 3 scope.

---

# 13. Knowledge Objects

Knowledge returned to the runtime should follow a normalized structure.

Logical attributes include:

- identifier
- source
- content
- relevance
- metadata

The runtime should not depend on provider-specific formats.

---

# 14. Error Handling

Knowledge retrieval failures must not terminate execution.

Recommended behavior:

- return empty results
- log failure
- record trace event
- continue execution

The runtime remains resilient even if knowledge is unavailable.

---

# 15. Future Extensions

The architecture intentionally supports future capabilities.

Examples:

- Multi-source retrieval
- Enterprise search
- Hybrid search
- Semantic ranking
- Knowledge graph integration
- MCP connectors
- Cross-organization federation
- Incremental indexing
- Streaming retrieval
- Policy-aware retrieval

These extensions should not require changes to Agent Runtime.

---

# 16. Architectural Constraints

The following constraints apply.

## Runtime

Knowledge is a runtime service.

---

## Agent

Agents never communicate directly with storage.

---

## Storage

Knowledge sources remain replaceable.

---

## Retrieval

Retrieval logic must remain independent from execution logic.

---

## Context

Knowledge contributes to Agent Context but does not own it.

---

# 17. Relationship to RAG

The Knowledge Layer is one component of Retrieval-Augmented Generation.

```
Memory Layer

        |

Knowledge Layer

        |

Context Builder

        |

RAG Pipeline

        |

Agent
```

The Knowledge Layer retrieves information.

The RAG Pipeline decides how retrieved information is incorporated into Agent Context.

This separation keeps retrieval independent from orchestration.

---

# 18. Sprint 3 Deliverables

Sprint 3 establishes the architectural foundation for:

- Knowledge abstraction
- Knowledge interfaces
- Retrieval contracts
- Provider architecture
- Runtime integration point

Knowledge ingestion pipelines, indexing, ranking, and optimization are intentionally deferred.

---

# 19. Summary

The Knowledge Layer establishes a technology-independent retrieval architecture that allows OneMind agents to access information from diverse sources through a unified interface.

By separating retrieval from memory, execution, and orchestration, the platform remains modular, extensible, and adaptable to future enterprise integrations.

Together with the Memory Layer, the Knowledge Layer forms the information foundation of the OneMind Agent Runtime, enabling the next architectural stage: the Retrieval-Augmented Generation (RAG) Pipeline.