# File: `docs/architecture/ADR-001-ASYNC-FIRST-RUNTIME.md`

````markdown
# ADR-001: Async-First Runtime Architecture

- **Status:** Accepted
- **Date:** 2026-08-02
- **Authors:** OneMind Architecture Team
- **Milestone:** M6 Platform Engineering
- **Related Sprint:** Sprint 3 – Memory & Knowledge Foundation

---

# Context

OneMind is designed as an AI operating system composed of multiple cooperating runtime services, including:

- Agent Runtime
- Planner Runtime
- Knowledge Runtime
- Tool Runtime
- Memory Layer
- Embedding Layer
- Vector Storage
- Future MCP integrations
- External LLM providers

Most runtime operations involve I/O-bound workloads:

- HTTP requests to LLM providers
- Embedding generation
- Vector database operations
- Persistent storage
- Tool execution
- Network communication
- Streaming responses

Maintaining synchronous service contracts across the runtime introduces unnecessary blocking, limits concurrency, and complicates integration with asynchronous frameworks such as FastAPI.

---

# Decision

OneMind adopts an **Async-First Runtime Architecture**.

All runtime service interfaces introduced after this ADR SHALL expose asynchronous APIs.

Unless there is a compelling architectural reason otherwise, runtime service contracts SHALL use `async` methods.

Example:

```python
class MemoryInterface(ABC):

    @abstractmethod
    async def store(...):
        ...

    @abstractmethod
    async def retrieve(...):
        ...

    @abstractmethod
    async def delete(...):
        ...
````

---

# Scope

This decision applies to:

* Memory Layer
* Embedding Layer
* Vector Store Layer
* Knowledge Layer
* Tool Layer
* Agent Runtime
* Planner Runtime
* Execution Pipeline
* Future Runtime Services

This ADR does not require utility libraries, pure domain models, or deterministic helper functions to become asynchronous unless they perform I/O.

---

# Design Principles

## 1. Async at Service Boundaries

All runtime service APIs should expose asynchronous methods.

Examples:

* MemoryService
* EmbeddingService
* VectorStoreService
* KnowledgeService
* ToolService

---

## 2. Await Across the Entire Call Chain

Asynchronous execution should propagate naturally through the runtime.

```
FastAPI

    ↓

ExecutionService

    ↓

Agent

    ↓

MemoryService

    ↓

MemoryProvider

    ↓

EmbeddingService

    ↓

VectorStore

    ↓

Qdrant
```

No synchronous wrappers should block asynchronous execution.

---

## 3. Synchronous Implementations May Still Use async

Providers that perform no I/O (for example, an in-memory provider used for testing) should still implement asynchronous interfaces.

Example:

```python
class InMemoryProvider(MemoryInterface):

    async def store(self, memory):
        self._storage[memory.id] = memory
        return memory
```

This keeps all implementations interchangeable while preserving a single public contract.

---

## 4. Avoid Mixed Sync/Async APIs

A runtime layer should not expose both synchronous and asynchronous variants of the same operation.

Example to avoid:

```python
store(...)
store_async(...)
```

Only one public asynchronous interface should exist.

---

## 5. Domain Models Remain Synchronous

Pure data structures remain synchronous.

Examples:

* MemoryRecord
* MemoryQuery
* MemoryResult
* EmbeddingRequest
* EmbeddingResponse
* VectorRecord

These models perform no I/O and require no asynchronous behavior.

---

# Rationale

An async-first architecture provides:

* Better concurrency for LLM workloads
* Improved scalability
* Non-blocking vector database operations
* Efficient streaming support
* Simpler integration with FastAPI
* Cleaner composition across runtime services
* Consistent developer experience

---

# Consequences

## Positive

* Unified runtime programming model
* Improved throughput
* Reduced blocking
* Cleaner future integrations
* Easier support for multiple concurrent agents

## Trade-offs

* Existing synchronous services require migration
* Unit tests become asynchronous
* Additional use of `await` throughout the runtime

These costs are acceptable because the project is still in the platform foundation stage.

---

# Migration Strategy

Migration should be performed vertically within each runtime layer.

For each layer:

1. Service Interface
2. Service Implementation
3. Provider Interface
4. Provider Implementations
5. Integration Tests
6. Runtime Integration

This minimizes temporary mixed-mode architectures.

---

# Sprint Roadmap

## Sprint 3

* Async Memory Layer
* Async Memory Providers
* Async Memory Integration Tests

## Sprint 4

* Async Vector Store Layer
* Async Knowledge Layer

## Sprint 5

* Async Tool Runtime
* Async Agent Runtime

## Sprint 6+

* Fully asynchronous execution pipeline
* Streaming-first execution
* Concurrent multi-agent orchestration

---

# Non-Goals

This ADR does not mandate:

* Asynchronous domain models
* Asynchronous utility functions
* Asynchronous pure computation

Only operations involving runtime service boundaries or potential I/O are affected.

---

# Architecture Compliance

All new runtime services introduced after this ADR shall:

* expose asynchronous public APIs
* avoid synchronous wrapper methods
* support cooperative asynchronous execution
* remain compatible with FastAPI's asynchronous execution model

---

# Status

**Accepted**

This ADR establishes Async-First Runtime Architecture as the architectural standard for all future OneMind runtime services.

```
```
