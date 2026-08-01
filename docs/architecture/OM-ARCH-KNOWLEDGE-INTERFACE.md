# OM-ARCH-KNOWLEDGE-INTERFACE

## Document Information

| Item | Value |
|---|---|
| Project | OneMind |
| Document ID | OM-ARCH-KNOWLEDGE-INTERFACE |
| Domain | Agent Runtime |
| Category | Architecture |
| Status | Draft |
| Version | 1.0 |
| Milestone | M6 Platform Engineering |
| Sprint | Sprint 3 – Memory & Knowledge Foundation |

---

# 1. Purpose

This document defines the interface contract for the OneMind Knowledge Layer.

The Knowledge Interface establishes the architectural boundary between Agent Runtime and knowledge retrieval implementations.

Unlike the Memory Layer, which provides information remembered from previous executions and interactions, the Knowledge Layer retrieves information from external or persistent knowledge sources.

The objective is to ensure that Agent Runtime depends only on a stable retrieval contract and remains independent from:

- vector database
- search engine
- document repository
- embedding model
- retrieval strategy
- indexing technology
- storage implementation

---

# 2. Architectural Context

The Knowledge Interface is a core component of the Context Enrichment architecture.

```
                 Agent Runtime

                       |

               Context Enricher

                       |

             Knowledge Interface

                       |

              Knowledge Provider

                       |

             Retrieval Engine

                       |

              Knowledge Store
```

The runtime communicates only with the Knowledge Interface.

---

# 3. Relationship with Other Layers

Knowledge is one of the information sources used to construct Agent Context.

```
                  Agent Context

                        |

          +-------------+-------------+

          |                           |

    Memory Layer              Knowledge Layer

          |                           |

     Remembered                Retrieved

      Information              Information
```

Memory answers:

> What has OneMind already experienced?

Knowledge answers:

> What information can OneMind retrieve?

---

# 4. Design Principles

## 4.1 Interface First

The runtime depends on contracts rather than implementations.

```
Runtime

    |

Knowledge Interface

    |

Knowledge Provider

    |

Retrieval Engine
```

Replacing the retrieval engine must not require runtime changes.

---

## 4.2 Retrieval Independence

Knowledge retrieval may use different technologies.

Examples:

- Vector Database
- PostgreSQL Full Text Search
- Elasticsearch
- OpenSearch
- Local Documents
- REST APIs
- Graph Database
- Hybrid Retrieval

The runtime must not know which implementation is used.

---

## 4.3 Runtime Isolation

Agents never retrieve knowledge directly.

Correct:

```
Agent

    |

Agent Context

    |

Context Builder

    |

Knowledge Interface
```

Incorrect:

```
Agent

    |

Vector Database
```

---

## 4.4 Provider Abstraction

Knowledge retrieval is performed by providers.

The provider hides:

- retrieval strategy
- ranking
- indexing
- embedding model
- storage technology

---

# 5. Knowledge Layer Responsibilities

The Knowledge Layer is responsible for:

- retrieving relevant documents
- abstracting retrieval engines
- ranking results
- returning normalized knowledge objects
- supporting future retrieval strategies

The Knowledge Layer is not responsible for:

- reasoning
- prompt generation
- memory management
- agent execution
- capability execution
- workflow orchestration

---

# 6. Knowledge Model

The Knowledge Interface consists of four primary concepts.

```
Knowledge Document

        |

Knowledge Query

        |

Knowledge Provider

        |

Knowledge Result
```

---

# 7. Knowledge Document

A Knowledge Document represents a retrieved piece of information.

Logical structure:

```
KnowledgeDocument

├── id

├── title

├── content

├── source

├── metadata

├── score

└── retrieved_at
```

---

## 7.1 id

Unique document identifier.

Example:

```
doc-001
```

---

## 7.2 title

Human-readable document title.

Example:

```
Memory Layer Architecture
```

---

## 7.3 content

Retrieved document content.

Examples:

- policy
- architecture document
- user manual
- specification
- operational procedure

---

## 7.4 source

Origin of the document.

Examples:

```
vector_store

postgres

filesystem

wiki

api
```

---

## 7.5 metadata

Additional document attributes.

Examples:

```
{
    "category": "architecture",
    "owner": "platform-team",
    "version": "1.0"
}
```

---

## 7.6 score

Retrieval relevance score.

Example:

```
0.94
```

---

## 7.7 retrieved_at

Timestamp indicating retrieval time.

---

# 8. Knowledge Query

A Knowledge Query defines retrieval requirements.

Logical structure:

```
KnowledgeQuery

├── query

├── limit

├── filters

├── retrieval_strategy

└── metadata
```

---

## 8.1 query

Search request.

Examples:

```
Find architecture document

Retrieve API specification

Find deployment guide
```

---

## 8.2 limit

Maximum number of documents.

Example:

```
10
```

---

## 8.3 filters

Optional retrieval constraints.

Examples:

```
category

owner

date

language
```

---

## 8.4 retrieval_strategy

Preferred retrieval strategy.

Examples:

```
semantic

keyword

hybrid
```

---

## 8.5 metadata

Additional retrieval context.

---

# 9. Knowledge Result

Knowledge Result contains retrieved documents.

Logical structure:

```
KnowledgeResult

├── documents

├── retrieval_metadata

├── execution_info

└── statistics
```

---

## 9.1 documents

Collection of retrieved knowledge documents.

---

## 9.2 retrieval_metadata

Information about retrieval.

Examples:

```
provider

strategy

duration
```

---

## 9.3 execution_info

Execution-related metadata.

---

## 9.4 statistics

Optional retrieval statistics.

Examples:

```
documents_found

documents_returned

average_score
```

---

# 10. Knowledge Provider Contract

Conceptual interface:

```
KnowledgeProvider

+ retrieve(query)

+ exists(document_id)

+ metadata(document_id)
```

The runtime communicates only with this contract.

---

# 11. Retrieve Contract

Purpose:

Retrieve relevant knowledge.

Input:

```
KnowledgeQuery
```

Output:

```
KnowledgeResult
```

Flow:

```
Context Enricher

        |

Knowledge Query

        |

Knowledge Provider

        |

Knowledge Result
```

---

# 12. Exists Contract

Purpose:

Determine whether a document exists.

Input:

```
document_id
```

Output:

```
true / false
```

---

# 13. Metadata Contract

Purpose:

Retrieve document metadata without loading full content.

Input:

```
document_id
```

Output:

```
Document Metadata
```

---

# 14. Retrieval Lifecycle

```
Receive Query

      |

Validate Query

      |

Retrieve Documents

      |

Rank Results

      |

Normalize Results

      |

Return Knowledge Result
```

---

# 15. Retrieval Flow

```
Execution Request

        |

Context Enricher

        |

Knowledge Query

        |

Knowledge Provider

        |

Retrieval Engine

        |

Knowledge Store

        |

Knowledge Result

        |

Context Builder

        |

Agent Context

        |

Agent
```

---

# 16. Retrieval Strategies

The interface supports multiple retrieval strategies.

Examples:

```
Keyword Retrieval

Semantic Retrieval

Hybrid Retrieval

Metadata Retrieval

Filtered Retrieval
```

Future providers may implement one or more strategies.

---

# 17. Ranking

Providers may rank retrieved documents.

Examples:

```
Similarity Score

Keyword Score

Hybrid Score

Business Priority
```

Ranking implementation remains provider-specific.

---

# 18. Error Handling

Knowledge retrieval failures should not terminate runtime execution.

---

## 18.1 Retrieval Failure

Expected behavior:

```
Return empty KnowledgeResult

Continue execution
```

---

## 18.2 Provider Failure

Expected behavior:

```
Record trace event

Apply fallback

Continue execution
```

---

# 19. Observability

Knowledge operations should integrate with the Execution Trace framework.

Suggested events:

```
knowledge.retrieval.started

knowledge.retrieval.finished

knowledge.provider.selected

knowledge.ranking.completed

knowledge.error
```

---

# 20. Security Considerations

Future implementations should support:

- access control
- tenant isolation
- document permissions
- audit logging
- encrypted storage
- source validation

Security remains the responsibility of provider implementations.

---

# 21. Implementation Mapping

Expected Sprint 3 implementation:

```
services/agent-runtime/app/

    knowledge/

        __init__.py

        interface.py

        models.py

        provider.py

        retriever.py
```

Implementation must conform to this contract.

---

# 22. Future Extensions

The Knowledge Interface is designed to support future capabilities.

Examples:

- hybrid retrieval
- semantic ranking
- cross-source retrieval
- federated knowledge search
- graph retrieval
- document summarization
- citation generation
- multi-language retrieval
- retrieval caching
- adaptive ranking

---

# 23. Architectural Constraints

## Agent

Agents never communicate directly with knowledge stores.

---

## Runtime

Runtime depends only on the Knowledge Interface.

---

## Provider

Providers hide retrieval implementation.

---

## Retrieval Engine

Retrieval technology remains replaceable.

---

## Context

Knowledge contributes to Agent Context but does not own it.

---

# 24. Relationship with Memory Interface

The Memory Interface and Knowledge Interface are complementary.

```
                 Agent Context

                       |

          +------------+------------+

          |                         |

    Memory Result          Knowledge Result

          |                         |

  Memory Interface      Knowledge Interface
```

Memory provides previously remembered information.

Knowledge provides externally retrieved information.

The Context Builder combines both into a unified Agent Context.

---

# 25. Summary

The Knowledge Interface defines the architectural contract between OneMind Agent Runtime and all knowledge retrieval implementations.

By introducing a provider-independent interface, OneMind separates runtime orchestration from retrieval technology, allowing knowledge providers, retrieval engines, and storage platforms to evolve independently without impacting Agent Runtime.

Together with the Memory Interface, the Knowledge Interface establishes the foundation for Context Enrichment and the Retrieval-Augmented Generation (RAG) architecture introduced in Sprint 3.