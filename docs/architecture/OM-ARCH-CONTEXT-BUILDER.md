# OM-ARCH-CONTEXT-BUILDER

## Document Information

| Item | Value |
|---|---|
| Project | OneMind |
| Document ID | OM-ARCH-CONTEXT-BUILDER |
| Domain | Agent Runtime |
| Category | Architecture |
| Status | Draft |
| Version | 1.0 |
| Milestone | M6 Platform Engineering |
| Sprint | Sprint 3 – Memory & Knowledge Foundation |

---

## 1. Purpose

This document defines the architecture and interface contract for the OneMind Context Builder.

The Context Builder is responsible for combining runtime information, memory information, and retrieved knowledge into a unified execution context for agents.

The Context Builder establishes the boundary between:

- Agent Runtime execution
- Memory Layer
- Knowledge Layer
- Embedding and Retrieval infrastructure
- Agent invocation

The objective is to provide agents with enriched context without requiring agents to understand:

- Memory retrieval
- Knowledge retrieval
- Embedding generation
- Storage technology
- Retrieval strategy

---

## 2. Architectural Position

The Context Builder is the final aggregation layer before Agent execution.

```text
Execution Request
      ↓
Execution Context
      ↓
Context Builder
      ↓
┌─────────────┬─────────────┐
↓             ↓             ↓
Runtime      Memory      Knowledge
Context      Result      Result
└─────────────┴─────────────┘
      ↓
Agent Context
      ↓
Agent
```

---

## 3. Relationship with Existing Runtime Architecture

Sprint 2 introduced:

```text
FastAPI
  ↓
ExecutionService
  ↓
TaskManager
  ↓
Executor
  ↓
AgentInvoker
  ↓
Agent
```

Sprint 3 extends this flow:

```text
FastAPI
  ↓
ExecutionService
  ↓
TaskManager
  ↓
Executor
  ↓
Context Builder
  ↓
AgentContext
  ↓
AgentInvoker
  ↓
Agent
```

---

## 4. Design Principles

### 4.1 Context Before Execution

Agents should receive a complete execution context before reasoning.

```text
Request
  ↓
Context Enrichment
  ↓
Agent Execution
```

### 4.2 Agent Isolation

Agents should not know where context comes from.

**Correct:**

```text
Agent
  ↓
AgentContext
```

**Incorrect:**

```text
Agent
  ├── Memory Database
  ├── Vector Store
  └── Knowledge API
```

### 4.3 Context Normalization

Different sources must be normalized.

- Input: `MemoryResult`, `KnowledgeResult`, `ExecutionMetadata`
- Output: `AgentContext`

### 4.4 Extensible Context Model

The design must support future context sources, for example:

- Memory
- Knowledge
- User Profile
- Organization Policy
- Environment State
- External APIs

---

## 5. Context Builder Responsibilities

The Context Builder **is** responsible for:

- Receiving execution context
- Requesting memory enrichment
- Requesting knowledge enrichment
- Combining information sources
- Creating `AgentContext`
- Validating context completeness

The Context Builder **is not** responsible for:

- Agent reasoning
- LLM execution
- Memory storage
- Knowledge storage
- Embedding generation
- Retrieval implementation

---

## 6. Context Model

The Context Builder works with four primary concepts.

```text
Execution Context
      ↓
Enrichment Request
      ↓
Context Builder
      ↓
Agent Context
```

---

## 7. Execution Context

Execution Context contains runtime information.

Logical structure:

```text
ExecutionContext
├── execution_id
├── task_id
├── agent_id
├── request
├── metadata
└── created_at
```

### 7.1 Execution Context Attributes

**`execution_id`** — Unique execution identifier. Example: `exec-001`

**`task_id`** — Reference to Agent Task. Example: `task-001`

**`agent_id`** — Target agent identifier. Example: `assistant-agent`

**`request`** — Original execution request. Example: user instruction

**`metadata`** — Additional runtime information, e.g. `tenant_id`, `session_id`, `trace_id`

---

## 8. Context Enrichment Request

Defines information required during context building.

Logical structure:

```text
ContextEnrichmentRequest
├── execution_context
├── memory_query
├── knowledge_query
└── options
```

**`execution_context`** — Current execution information.

**`memory_query`** — Optional memory retrieval request. Provided to `Memory Interface`.

**`knowledge_query`** — Optional knowledge retrieval request. Provided to `Knowledge Interface`.

**`options`** — Context construction options, e.g. `include_memory=true`, `include_knowledge=true`

---

## 9. Agent Context

Agent Context is the final context provided to an agent.

Logical structure:

```text
AgentContext
├── execution
├── memories
├── knowledge
├── metadata
└── created_at
```

---

## 10. Agent Context Components

### 10.1 Execution Information

Contains: `ExecutionContext`

Purpose: provide runtime awareness.

### 10.2 Memory Information

Contains: `MemoryResult`

Purpose: provide remembered information. Examples:

- Previous interactions
- Previous decisions
- Historical execution results

### 10.3 Knowledge Information

Contains: `KnowledgeResult`

Purpose: provide retrieved information. Examples:

- Documents
- Policies
- Technical references

### 10.4 Metadata

Contains context metadata, e.g. `trace_id`, `agent_id`, `context_version`

---

## 11. Context Builder Contract

Conceptual interface:

```text
ContextBuilder
  build(request)
  enrich(context)
  validate(context)
```

---

## 12. Build Operation

**Purpose:** Create enriched Agent Context.

- Input: `ContextEnrichmentRequest`
- Output: `AgentContext`

Flow:

```text
Execution Context
      ↓
Context Builder
      ↓
Memory Retrieval
      ↓
Knowledge Retrieval
      ↓
Agent Context
```

---

## 13. Enrich Operation

**Purpose:** Add additional information to existing context.

- Input: `AgentContext`
- Output: `AgentContext`

Possible enrichment: Memory, Knowledge, User Information

---

## 14. Validate Operation

**Purpose:** Ensure context is ready for execution.

Validation examples:

- Required execution metadata exists
- Agent identity exists
- Context format is valid

Output: `Validation Result`

---

## 15. Context Building Flow

```text
Execution Request
      ↓
Execution Context
      ↓
Context Builder
      ↓
┌─────────────┴─────────────┐
↓                            ↓
Memory Query          Knowledge Query
↓                            ↓
Memory Layer          Knowledge Layer
↓                            ↓
Memory Result         Knowledge Result
└─────────────┬─────────────┘
              ↓
       Agent Context
              ↓
      Agent Invocation
```

---

## 16. Integration with Memory Layer

Context Builder consumes: `Memory Interface`

Flow:

```text
Context Builder
      ↓
Memory Query
      ↓
Memory Provider
      ↓
Memory Result
      ↓
Agent Context
```

---

## 17. Integration with Knowledge Layer

Context Builder consumes: `Knowledge Interface`

Flow:

```text
Context Builder
      ↓
Knowledge Query
      ↓
Knowledge Provider
      ↓
Knowledge Result
      ↓
Agent Context
```

---

## 18. Integration with Embedding Service

The Context Builder does not directly generate embeddings.

Embedding usage belongs to: Memory Provider, Knowledge Provider, Retrieval Pipeline

Architecture:

```text
Context Builder
      ↓
Knowledge Interface
      ↓
Retriever
      ↓
Embedding Service
```

---

## 19. Error Handling

Context enrichment failures should be isolated.

### 19.1 Memory Failure

Behavior:

- Log Error
- Return Context Without Memory
- Continue Execution

### 19.2 Knowledge Failure

Behavior:

- Log Error
- Return Context Without Knowledge
- Continue Execution

### 19.3 Context Validation Failure

Behavior:

- Reject Execution
- Return Validation Error

---

## 20. Observability

Context Builder integrates with Execution Trace.

Suggested events:

- `context.build.started`
- `context.memory.enriched`
- `context.knowledge.enriched`
- `context.build.completed`
- `context.validation.failed`

Metadata: `execution_id`, `agent_id`, `memory_count`, `knowledge_count`, `duration`

---

## 21. Security Considerations

Future implementations should support:

- Context access control
- Tenant isolation
- Sensitive information filtering
- Audit logging
- Context expiration

Security belongs to the runtime and provider layers.

---

## 22. Implementation Mapping

Expected Sprint 3 implementation:

```text
services/agent-runtime/app/
└── context/
    ├── __init__.py
    ├── builder.py
    ├── models.py
    └── enrichment.py
```

Implementation must follow this contract.

---

## 23. Future Extensions

The Context Builder supports future capabilities:

- Dynamic context selection
- Context compression
- Context ranking
- Context budgeting
- Token optimization
- Multi-agent context sharing
- Policy-aware enrichment
- Adaptive retrieval

---

## 24. Architectural Constraints

| Component | Constraint |
|---|---|
| Agent | Agent receives `AgentContext` only |
| Runtime | Runtime controls context creation |
| Memory | Memory provides remembered information |
| Knowledge | Knowledge provides retrieved information |
| Embedding | Embedding provides vector transformation |
| Context Builder | Combines information but does not own source data |

---

## 25. Complete Sprint 3 Contract Architecture

After this document, Sprint 3 interface contracts are complete.

```text
Agent Runtime
      ↓
Context Builder
      ↓
┌─────────────────┴─────────────────┐
↓                                    ↓
Memory Interface           Knowledge Interface
↓                                    ↓
Memory Provider            Knowledge Provider
↓                                    ↓
Memory Store               Retrieval Engine
└─────────────────┬─────────────────┘
                   ↓
          Embedding Service
```

---

## 26. Summary

The Context Builder defines the contract that transforms raw runtime information, memory information, and knowledge information into a unified Agent Context.

Together with:

- Memory Interface
- Knowledge Interface
- Embedding Service

the Context Builder completes the Sprint 3 foundation required for context-aware agents and Retrieval-Augmented Generation.

This architecture enables OneMind agents to reason with historical experience, retrieved knowledge, and execution awareness while maintaining clean separation between runtime, intelligence, and infrastructure layers.