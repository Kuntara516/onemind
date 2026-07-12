---
title: Business Services Catalog
document_id: OM-BIZ-013
version: 1.0.0
status: Draft

owner: OneMind Architecture Team
classification: Internal

created: 2026-07-10
last_updated: 2026-07-10

parent: OM-BIZ-011
related:
  - OM-BIZ-010
  - OM-BIZ-011
  - OM-BIZ-012
  - OM-ARCH-021
  - OM-ARCH-022

tags:
  - Business Architecture
  - Business Services
  - Enterprise Architecture
  - OneMind
---

# Business Services Catalog

> **Many Agents. One Mind.**

---

# 1. Purpose

Business Services เป็นชุดบริการทางธุรกิจ (Business-facing Services) ที่ OneMind Platform ให้กับองค์กร

Business Service คือสิ่งที่ผู้ใช้งาน ระบบภายนอก หรือ AI Agents สามารถเรียกใช้เพื่อดำเนินกระบวนการทางธุรกิจ โดยไม่ขึ้นกับเทคโนโลยีหรือการออกแบบระบบภายใน

Business Services ทำหน้าที่เป็นตัวเชื่อมระหว่าง

- Business Capabilities
- Domain Architecture
- Component Architecture
- API Design
- Agent Services

เอกสารนี้กำหนดรายการ Business Services มาตรฐานของ OneMind เพื่อใช้เป็น Enterprise Architecture Baseline

---

# 2. Objectives

Business Services Catalog มีวัตถุประสงค์เพื่อ

- สร้างมาตรฐานบริการของแพลตฟอร์ม
- รองรับการออกแบบ Domain
- รองรับ Service-Oriented Architecture
- รองรับ API First
- รองรับ AI Native Architecture
- รองรับ Multi-Agent Collaboration
- ลดการสร้างบริการซ้ำซ้อน
- สร้าง Service Contract ที่ชัดเจน

---

# 3. Design Principles

Business Services ของ OneMind ยึดหลักการดังต่อไปนี้

- Business First
- Capability Driven
- Domain Oriented
- Platform Independent
- Technology Agnostic
- Reusable
- Discoverable
- Secure by Design
- AI Ready
- Event Ready

---

# 4. Business Service Hierarchy

```
Business Vision
        │
        ▼
Business Capability
        │
        ▼
Business Service
        │
        ▼
Domain Service
        │
        ▼
Application Service
        │
        ▼
Component
        │
        ▼
API
```

Business Services เป็นระดับที่เชื่อม Business กับ Solution Architecture

---

# 5. Business Services Overview

OneMind แบ่ง Business Services ออกเป็น 8 กลุ่มหลัก

| Domain | Service Group |
|----------|--------------|
| Identity | Identity Services |
| Organization | Organization Services |
| People | People Services |
| Knowledge | Knowledge Services |
| Memory | Memory Services |
| Workflow | Workflow Services |
| AI | AI Services |
| Agent | Agent Services |

---

# 6. Identity Services

Business Capability

- Identity Management

Business Services

- Register Identity
- Authenticate User
- Authorize Access
- Manage Roles
- Manage Permissions
- Manage Sessions
- Multi-factor Authentication
- Identity Federation
- Single Sign-On

Consumers

- Human Users
- AI Agents
- External Systems

---

# 7. Organization Services

Business Capability

- Organization Management

Business Services

- Manage Organization
- Manage Business Units
- Manage Departments
- Manage Teams
- Organization Hierarchy
- Organization Policy
- Organization Configuration

Consumers

- HR
- Administration
- AI Agents

---

# 8. People Services

Business Capability

- People Management

Business Services

- Employee Management
- Customer Management
- Resident Management
- Patient Management
- User Profile
- Skills Management
- Competency Management
- Availability Management

Consumers

- HR Systems
- Workflow Engine
- AI Scheduler

---

# 9. Knowledge Services

Business Capability

- Enterprise Knowledge

Business Services

- Knowledge Repository
- Document Management
- Semantic Search
- Knowledge Retrieval
- Knowledge Classification
- Knowledge Versioning
- Knowledge Publishing
- Knowledge Governance

Consumers

- AI
- Users
- Agents
- RAG Engine

---

# 10. Memory Services

Business Capability

- Enterprise Memory

Business Services

- Conversation Memory
- Episodic Memory
- Long-term Memory
- Working Memory
- Memory Retrieval
- Memory Consolidation
- Memory Retention Policy

Consumers

- AI Runtime
- Agents

---

# 11. Workflow Services

Business Capability

- Workflow Management

Business Services

- Workflow Definition
- Workflow Execution
- Task Assignment
- Task Monitoring
- Approval
- Escalation
- Notification
- SLA Monitoring

Consumers

- Business Users
- AI Agents

---

# 12. AI Services

Business Capability

- AI Platform

Business Services

- Prompt Management
- LLM Gateway
- Embedding Service
- Model Selection
- AI Orchestration
- AI Evaluation
- AI Monitoring
- AI Guardrails

Consumers

- Applications
- AI Agents

---

# 13. Agent Services

Business Capability

- Multi-Agent Platform

Business Services

- Agent Registry
- Agent Discovery
- Agent Communication
- Agent Collaboration
- Agent Delegation
- Agent Memory
- Agent Lifecycle
- Agent Monitoring

Consumers

- AI Runtime
- Applications

---

# 14. Cross-cutting Services

Business Services ที่ใช้งานร่วมกันทุก Domain

## Security

- Authentication
- Authorization
- Audit
- Encryption
- Key Management

## Governance

- Policy Enforcement
- Compliance
- Approval
- Risk Management

## Integration

- API Gateway
- Event Bus
- Message Queue
- Webhook
- MCP Gateway

## Observability

- Logging
- Metrics
- Monitoring
- Tracing
- Alerting

---

# 15. Business Service Mapping

| Business Capability | Primary Business Service |
|----------------------|--------------------------|
| Identity | Identity Services |
| Organization | Organization Services |
| People | People Services |
| Knowledge | Knowledge Services |
| Memory | Memory Services |
| Workflow | Workflow Services |
| AI | AI Services |
| Agent | Agent Services |

---

# 16. Service Characteristics

Business Services ของ OneMind ต้องมีคุณสมบัติดังนี้

- Stateless Interface
- Well-defined Contract
- Versionable
- Secure
- Observable
- Discoverable
- Reusable
- Event-enabled
- AI Compatible

---

# 17. Relationship with Architecture

Business Services เป็นจุดเชื่อมระหว่าง Business Architecture และ Solution Architecture

```
Business Capability
        │
        ▼
Business Service
        │
        ▼
Domain
        │
        ▼
Component
        │
        ▼
API
        │
        ▼
Microservice
```

Business Services จะถูกนำไปแตกเป็น

- Domain Services
- Application Services
- APIs
- MCP Tools
- AI Skills
- Agent Capabilities

ในเอกสารถัดไป

- OM-ARCH-022 Component Architecture

---

# 18. Future Evolution

Business Services Catalog จะขยายเพิ่มเติมใน Milestone ถัดไปเพื่อรองรับ

- Healthcare AIOS
- Smart Building AIOS
- Manufacturing AIOS
- Government AIOS
- University AIOS

โดยยังคงใช้ Core Business Services ชุดเดียวกัน

---

# 19. Key Takeaways

Business Services Catalog เป็นสะพานเชื่อมระหว่าง Business Capabilities และ Technical Architecture

Business Services เป็นมาตรฐานกลางที่ทุก Domain ใช้งานร่วมกัน และเป็นพื้นฐานสำหรับการออกแบบ Domain, Components, APIs, AI Agents และ MCP Services ใน OneMind Platform

เอกสารนี้ถือเป็น Enterprise Architecture Baseline สำหรับการออกแบบ Service-Oriented และ AI Native Platform ของ OneMind

---