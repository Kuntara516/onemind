# OneMind Architecture Document

# Context Orchestration Layer Architecture

**Document ID:** OM-ARCH-CONTEXT-ORCHESTRATION  
**Version:** 1.0  
**Status:** Frozen Candidate  
**Sprint:** Sprint 4 - Context Intelligence & Retrieval Pipeline  

---

# 1. Overview

Context Orchestration Layer เป็นส่วนหนึ่งของ OneMind Context Intelligence Architecture

หน้าที่หลักคือทำหน้าที่เป็น coordinator ระหว่าง:

- Context Request
- Context Builder
- Retrieval Pipeline
- Memory Layer
- Knowledge Layer

เพื่อสร้าง context ที่เหมาะสมสำหรับ Agent Runtime

Context Orchestration ไม่รับผิดชอบการค้นหาข้อมูลโดยตรง แต่ทำหน้าที่ควบคุม workflow และ composition ของ context pipeline

---

# 2. Architectural Position

Context Orchestration อยู่เหนือ Context Builder Layer

             Agent Runtime
                   |
                   |
                   v
    Context Orchestration Layer
                   |
                   |
                   v
         Context Builder Layer
                   |
                   |
                   v
      Retrieval Pipeline Layer
          /                 \
         /                   \
        v                     v
Memory Service        Knowledge Service
        |
        |
        v

Embedding + Vector Store


---

# 3. Design Principles

## 3.1 Separation of Responsibility

แต่ละ layer มีหน้าที่เฉพาะ

| Layer | Responsibility |
|---|---|
| Context Orchestrator | Coordinate context workflow |
| Context Builder | Assemble context object |
| Retrieval Service | Retrieve relevant information |
| Memory Service | Manage agent/user memories |
| Knowledge Service | Manage domain knowledge |

---

## 3.2 Interface Driven Design

Orchestration Layer ใช้ interface เป็น boundary


ContextOrchestrator
|
|
v
Concrete Strategy


ทำให้สามารถเปลี่ยน orchestration strategy ได้โดยไม่กระทบ Agent Runtime

---

# 4. Component Structure

Repository structure:


services/agent-runtime/app/context/orchestrator

├── init.py
├── exceptions.py
├── interface.py
├── models.py
├── service.py
├── strategies
│ └── default.py
└── tests
└── test_context_orchestrator.py


---

# 5. Core Components

## 5.1 Orchestration Models

File:


context/orchestrator/models.py


Defines:

- OrchestrationRequest
- OrchestrationResult


Flow:


OrchestrationRequest

    |
    v

ContextRequest

    |
    v

Context Builder

    |
    v

ContextResult

    |
    v

OrchestrationResult


---

# 6. Context Orchestrator Interface

File:


context/orchestrator/interface.py


Contract:

```python
class ContextOrchestrator(ABC):

    async def orchestrate(
        request: OrchestrationRequest
    ) -> OrchestrationResult:
        ...

Responsibilities:

receive orchestration request
execute context workflow
return assembled result
7. Service Layer

File:

context/orchestrator/service.py

ContextOrchestrationService provides application boundary.

Responsibilities:

validate request
delegate execution
normalize result
hide implementation details

Flow:

Agent Runtime

      |
      v

ContextOrchestrationService

      |
      v

ContextOrchestrator

      |
      v

OrchestrationResult
8. Default Strategy

File:

context/orchestrator/strategies/default.py

Initial implementation:

DefaultContextOrchestrator
          |
          v
ContextService
          |
          v
Context Builder
          |
          v
ContextResult

Current responsibilities:

execute context building
collect execution trace
attach orchestration metadata

Example trace:

[
"context_orchestration_started",
"context_builder_executed",
"context_orchestration_completed"
]
9. Runtime Flow

Complete execution flow:

User Request
      |
      v
Agent Runtime
      |
      v
OrchestrationRequest
      |
      v
ContextOrchestrationService
      |
      v
DefaultContextOrchestrator
      |
      v
ContextService
      |
      v
ContextBuilder
      |
      v
RetrievalService
      |
      +----------------+
      |                |
      v                v
 Memory          Knowledge
 Service         Service
      |
      v
Vector Store / Qdrant
      |
      v
ContextResult
      |
      v
OrchestrationResult
10. Extension Points

Future enhancements:

10.1 Multi Source Orchestration

รองรับ:

memory retrieval
knowledge retrieval
external data sources
10.2 Context Ranking

เพิ่ม:

relevance score
source priority
confidence score
10.3 Context Compression

รองรับ:

token budget management
summarization
context pruning
10.4 Execution Trace Integration

เชื่อมกับ:

Agent Execution Trace
Observability Layer
11. Testing Strategy

Test file:

context/orchestrator/tests/test_context_orchestrator.py

Coverage:

default orchestration flow
service delegation
request validation

Current status:

3 passed
12. Sprint 4 Relationship

Context Orchestration completes the integration between:

Sprint 3

Memory Foundation
Knowledge Foundation
Embedding
Vector Storage


          +

Sprint 4

Context Builder
Retrieval Pipeline
Context Orchestration

Result:

OneMind gains the first complete Context Intelligence pipeline.

13. Future Roadmap

Planned evolution:

S4-003
Context Orchestration
        |
        v
S4-004
Context Ranking
        |
        v
S4-005
Context Compression
        |
        v
S5
Advanced Agent Reasoning
Status

Current state:

Context Orchestration Layer

FOUNDATION COMPLETE

Document maintained as part of OneMind Architecture Documentation.