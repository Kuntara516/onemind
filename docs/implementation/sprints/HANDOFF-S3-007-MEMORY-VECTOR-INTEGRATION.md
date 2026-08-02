---

# HANDOFF S3-007 — Memory Vector Integration

## Document Information

| Item | Value |
| --- | --- |
| **Project** | OneMind |
| **Milestone** | M6 — Platform Engineering |
| **Sprint** | Sprint 3 — Memory & Knowledge Foundation |
| **Status** | READY FOR NEXT IMPLEMENTATION |
| **Previous Frozen Checkpoint** | `v0.7.0-sprint3-qdrant` |

---

## 1. Overview

Sprint 3 established the foundation for persistent memory storage through vector-based retrieval. The Qdrant Vector Backend Foundation has been completed and frozen.

This handoff continues from the following architecture:

```text
Memory Layer ──> Vector Store Abstraction ──> Qdrant Vector Backend ──> Persistent Vector Storage

```

The next implementation phase is integrating Memory services with vector storage.

---

## 2. Completed Sprint 3 Work

### 2.1 Vector Store Abstraction

* **Target Package:** `services/agent-runtime/app/vector_store/`
* **Package Structure:**
```text
vector_store/
├── base.py
├── models.py
├── service.py
└── qdrant.py

```


* **Capabilities:** `VectorStore` interface, `VectorRecord` model, `VectorStoreService` layer, and `Qdrant` backend implementation.

---

## 3. Qdrant Backend Foundation (Frozen)

### 3.1 Implementation

* **Location:** `services/agent-runtime/app/vector_store/qdrant.py`
* **Implemented Capabilities:** Qdrant client initialization, Collection lifecycle management, Vector insertion, Vector retrieval, Vector deletion, and Similarity search.

### 3.2 Supported Operations

* **Add Vector:**
```text
VectorRecord ──> Qdrant PointStruct ──> Collection Storage

```


* **Retrieve Vector:**
* Input: `record_id`
* Output: `VectorRecord | None`


* **Delete Vector:**
* Input: `record_id`
* Action: Remove point from collection


* **Similarity Search:**
* Input: Query vector, `limit`
* Output: `list[VectorRecord]`



---

## 4. Infrastructure Integration

Completed Docker integration.

* **File Location:** `docker/compose/docker-compose.yml`
* **Service Definition:**
```yaml
qdrant:
  image: qdrant/qdrant:latest
  ports:
    - "6333:6333"
  volumes:
    - qdrant-data:/qdrant/storage

```


* **Persistent Volume:** `qdrant-data`

---

## 5. Test Coverage

* **Command:**
```bash
python -m pytest

```


* **Result:** `54 passed`
* **Coverage Scope:**
```text
tests/
├── test_vector_store.py
├── test_vector_store_service.py
└── test_qdrant_vector_store.py

```



---

## 6. Dependency Environment

Frozen dependency snapshot added at: `services/agent-runtime/requirements.lock.txt`

### Key Dependency Versions

* `fastapi==0.141.1`
* `pydantic==2.13.4`
* `qdrant-client==1.18.0`
* `grpcio==1.83.0`
* `protobuf==7.35.1`
* `pytest==9.1.1`

> **Purpose:** Ensure a reproducible development environment, prevent dependency drift, and prepare the CI pipeline.

---

## 7. Git Checkpoint

* **Frozen Tag:** `v0.7.0-sprint3-qdrant`
* **Commit Baseline:** `ac42509 chore: freeze agent runtime dependency environment`

### Included Commits

* `ac42509` chore: freeze agent runtime dependency environment
* `40f693f` infra: add qdrant service to onemind compose
* `335f318` docs: freeze sprint3 qdrant vector backend foundation
* `17e785c` test: add qdrant vector store integration tests
* `54c52a5` feat: implement qdrant vector store crud operations
* `92e8473` feat: add qdrant collection lifecycle
* `c228bcb` feat: register qdrant vector store backend

---

## 8. Next Objective — S3-007 Memory Vector Integration

**Goal:** Connect the existing Memory Layer with Vector Storage.

### Target Architecture

```text
            Agent Runtime
                  │
                  ▼
            Memory Service
                  │
          ┌───────┴───────┐
          ▼               ▼
     Memory Store   Vector Store
                          │
                          ▼
                       Qdrant

```

---

## 9. Planned Components

### 9.1 Memory Vector Adapter

* **New File Location:** `services/agent-runtime/app/memory/vector_memory.py`
* **Responsibilities:** Convert memory records into vector records, store embeddings, retrieve semantic memories, and synchronize metadata.

### 9.2 Memory Retrieval Flow

```text
User Input ──> Embedding Service ──> Query Vector ──> Qdrant Search ──> Relevant Memories ──> Agent Context Injection

```

---

## 10. Integration Requirements

S3-007 should preserve existing boundaries. Do not bypass the defined service layers:

```text
Memory Service ──> VectorStoreService ──> QdrantVectorStore

```

> **Warning:** Direct Qdrant client calls from the Memory layer should not be introduced.

---

## 11. Expected New Tests

* **Target File:** `tests/test_memory_vector_integration.py`

### Required Scenarios

* **Store Memory Flow:** `Memory ──> Embedding ──> Vector Store ──> Qdrant`
* **Retrieve Memory Flow:** `Query ──> Embedding ──> Similarity Search ──> Memory Result`
* **Metadata Preservation:** Verify that `memory_id`, `agent_id`, `timestamp`, and `metadata` remain fully intact and available after retrieval.

---

## 12. Open Questions

Before implementation, consider the following points:

1. Memory record schema finalization.
2. **Embedding ownership decision:**
* **Recommended Path:** `Memory Service` owns semantic memory creation ──> `Embedding Service` provides vector generation ──> `Vector Store` persists vectors.



---

## 13. Definition of Done

S3-007 is complete when:

* [ ] Memory records can generate embeddings successfully.
* [ ] Embeddings are correctly stored in Qdrant.
* [ ] Semantic memory retrieval works as expected.
* [ ] Metadata survives the storage round-trip without loss.
* [ ] Agent runtime can consume retrieved memories seamlessly.
* [ ] All new integration tests pass successfully.
* [ ] Documentation is updated and frozen.

---

## 14. Next Branch State

* **Current Branch:** `feature/sprint3-memory-foundation`
* **Starting Point Tag:** `v0.7.0-sprint3-qdrant`
* **Next Active Work:** `S3-007 Memory Vector Integration`

---

*End of Handoff*
## Known Warnings

### protobuf / qdrant-client Deprecation Warning
During `pytest` execution, the following warnings are observed:

```text
DeprecationWarning: Type google._upb._message.MessageMapContainer uses PyType_Spec with a metaclass that has custom tp_new.
DeprecationWarning: Type google._upb._message.ScalarMapContainer uses PyType_Spec with a metaclass that has custom tp_new.
Source:

qdrant-client dependency stack

protobuf runtime

Impact:

No impact to OneMind implementation

No failed tests

No runtime issue observed

Current Decision:

Ignore during Sprint 3

Do not suppress warnings

Do not pin/downgrade protobuf dependency

Future Action: Review during dependency upgrade / platform hardening cycle.

