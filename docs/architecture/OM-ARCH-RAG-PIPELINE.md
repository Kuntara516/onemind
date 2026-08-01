# OM-ARCH-RAG-PIPELINE

## Document Information

| Item | Value |
|---|---|
| Project | OneMind |
| Document ID | OM-ARCH-RAG-PIPELINE |
| Domain | Agent Runtime |
| Category | Architecture |
| Status | Draft |
| Version | 1.0 |
| Milestone | M6 Platform Engineering |
| Sprint | Sprint 3 - Memory & Knowledge Foundation |

---

# 1. Purpose

This document defines the Retrieval-Augmented Generation (RAG) Pipeline architecture for the OneMind platform.

The RAG Pipeline is responsible for orchestrating how execution context, memory, and retrieved knowledge are combined into a single Agent Context before an agent begins reasoning.

The RAG Pipeline does **not** own memory, knowledge, or execution. Its responsibility is orchestration.

---

# 2. Architectural Position

The RAG Pipeline sits between the execution runtime and the agent.

```
Execution Request

        |

Execution Service

        |

Task Manager

        |

Executor

        |

Context Enricher

        |

RAG Pipeline

        |

Agent Context

        |

Agent

        |

Capability Layer
```

The pipeline prepares context before agent execution begins.

---

# 3. Relationship with Other Components

Sprint 3 introduces three complementary architectural layers.

```
Memory Layer

    |

Provides remembered information

--------------------------------

Knowledge Layer

    |

Provides retrieved information

--------------------------------

RAG Pipeline

    |

Combines everything

--------------------------------

Agent Context

    |

Consumed by Agent
```

Each layer has a single responsibility.

---

# 4. Design Principles

## 4.1 Orchestration Only

The RAG Pipeline orchestrates context assembly.

It does not:

- store memory
- retrieve documents directly
- execute agents
- call LLMs
- perform capability execution

---

## 4.2 Stateless

The pipeline maintains no persistent state.

Every execution builds a fresh Agent Context.

---

## 4.3 Provider Independence

The pipeline is independent of:

- vector database
- memory implementation
- embedding model
- storage engine
- external providers

Only interfaces are visible.

---

## 4.4 Deterministic Assembly

Given identical inputs, the pipeline should produce the same Agent Context.

Ranking improvements may be introduced in future milestones.

---

# 5. High-Level Flow

```
Execution Request

        |

Execution Metadata

        |

Context Enricher

        |

+---------------------------+

|                           |

Memory Retrieval     Knowledge Retrieval

|                           |

+-------------+-------------+

              |

      Context Builder

              |

      Agent Context

              |

            Agent
```

---

# 6. Pipeline Stages

## Stage 1 — Receive Execution Request

Input includes:

- execution metadata
- task payload
- agent identity
- runtime metadata

---

## Stage 2 — Retrieve Memory

The Memory Layer provides:

- working memory
- short-term memory
- long-term memory
- user memory
- organization memory

The RAG Pipeline treats all retrieved memory as input only.

---

## Stage 3 — Retrieve Knowledge

The Knowledge Layer provides:

- document retrieval
- vector retrieval
- structured retrieval
- enterprise knowledge
- external providers

Knowledge retrieval is independent from memory retrieval.

---

## Stage 4 — Context Builder

The Context Builder merges all retrieved information.

Logical inputs include:

```
Execution Metadata

+

Runtime Metadata

+

Working Memory

+

Retrieved Memory

+

Retrieved Knowledge

=

Agent Context
```

No reasoning occurs during this stage.

---

## Stage 5 — Agent Execution

The completed Agent Context is passed to the Agent Runtime.

The Agent never communicates directly with Memory or Knowledge.

---

# 7. Agent Context

The Agent receives a single normalized context object.

```
Agent Context

├── Execution Metadata

├── Runtime Metadata

├── Memory

├── Knowledge

├── Parameters

└── Future Extensions
```

The Agent remains unaware of the origin of individual information.

---

# 8. Context Enrichment

Context Enrichment prepares information before execution.

```
Execution Request

        |

Context Enricher

        |

Memory

+

Knowledge

+

Runtime Metadata

        |

Agent Context
```

Context Enrichment completes before the Agent starts reasoning.

---

# 9. Component Responsibilities

| Component | Responsibility |
|---|---|
| Executor | Execute task |
| Context Enricher | Prepare execution context |
| Memory Layer | Retrieve remembered information |
| Knowledge Layer | Retrieve external information |
| Context Builder | Assemble Agent Context |
| Agent | Perform reasoning |
| Capability Layer | Execute capabilities |

Responsibilities are intentionally isolated.

---

# 10. Interface Boundaries

The RAG Pipeline communicates only through interfaces.

```
Executor

    |

Context Enricher

    |

Memory Interface

Knowledge Interface

    |

Context Builder

    |

Agent Context
```

No component bypasses another layer.

---

# 11. Error Handling

Pipeline failures should degrade gracefully.

Examples:

Memory unavailable

```
Continue with empty memory.
```

Knowledge unavailable

```
Continue with empty knowledge.
```

Provider failure

```
Record trace event.

Continue execution.
```

Execution should only fail if the Agent itself cannot continue.

---

# 12. Observability

The RAG Pipeline should emit trace events.

Suggested events:

```
context.started

memory.retrieval.started

memory.retrieval.finished

knowledge.retrieval.started

knowledge.retrieval.finished

context.builder.started

context.builder.finished

context.completed
```

These events integrate with the existing Execution Trace framework introduced in Sprint 2.

---

# 13. Future Extensions

The architecture intentionally supports future capabilities.

Examples:

- Memory ranking
- Semantic retrieval
- Hybrid retrieval
- Knowledge graph integration
- Context compression
- Prompt optimization
- Streaming retrieval
- Incremental context updates
- Multi-agent context sharing
- Policy-aware context assembly

None of these enhancements should require changes to the Agent interface.

---

# 14. Architectural Constraints

The following constraints apply.

## Agent

The Agent receives only Agent Context.

---

## Memory

Memory never communicates directly with the Agent.

---

## Knowledge

Knowledge never communicates directly with the Agent.

---

## Pipeline

The pipeline performs orchestration only.

---

## Runtime

Runtime owns the execution lifecycle.

---

# 15. Repository Alignment

Sprint 3 implementation is expected to introduce:

```
services/

    agent-runtime/

        app/

            rag/

                context_builder.py

                enricher.py

                pipeline.py
```

Implementation details may evolve without changing this architecture.

---

# 16. Sprint 3 Deliverables

Sprint 3 establishes the architectural foundation for:

- Context Enricher
- Context Builder
- Agent Context
- RAG orchestration
- Runtime integration point

Prompt construction, advanced ranking, and optimization are deferred.

---

# 17. Architecture Overview

```
                    Execution Request

                            |

                    Execution Service

                            |

                        Task Manager

                            |

                         Executor

                            |

                    Context Enricher

                            |

          +-----------------+-----------------+

          |                                   |

      Memory Layer                   Knowledge Layer

          |                                   |

          +-----------------+-----------------+

                            |

                     Context Builder

                            |

                      Agent Context

                            |

                           Agent

                            |

                     Capability Layer
```

---

# 18. Summary

The RAG Pipeline is the orchestration layer that transforms execution metadata, runtime state, memory, and retrieved knowledge into a unified Agent Context.

Unlike the Memory Layer and Knowledge Layer, which are responsible for retrieving information, the RAG Pipeline is responsible for composition. It provides a clean architectural boundary between information retrieval and agent reasoning.

With the completion of the Memory Layer, Knowledge Layer, and RAG Pipeline architectures, Sprint 3 establishes the complete information architecture required for context-aware execution in OneMind while preserving the modular, interface-first design principles established in earlier milestones.