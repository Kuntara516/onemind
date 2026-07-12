---
title: OneMind Domain Architecture
document_id: OM-ARCH-021
category: Architecture Vision
version: 1.0.0
status: Draft
owner: OneMind Architecture Team
approver: Chief Architect
classification: Internal
created: 2026-07-09
last_updated: 2026-07-09
next_review: 2026-10-01

milestone: M2
phase: Architecture Design

author:
  - Nonthaphon Vattanataysanun
  - ChatGPT (Architecture Assistant)

related_documents:
  - 20-system-architecture.md
  - 22-component-architecture.md
  - ../business/README.md
  - ../application/README.md

tags:
  - Domain Architecture
  - Enterprise Architecture
  - AIOS
  - OneMind
---

# OneMind Domain Architecture

> **Define business capabilities before designing software.**

---

# Revision History

| Version | Date | Description |
|----------|------------|-----------------------------|
|1.0.0|2026-07-09|Initial version|

---

# 1. Purpose

เอกสารนี้กำหนด **Business Domains** ของแพลตฟอร์ม OneMind

Domain หมายถึง "กลุ่มความสามารถทางธุรกิจ (Business Capability)"
ไม่ใช่ Module, Database หรือ Microservice

Domain Architecture เป็นสะพานเชื่อมระหว่าง

- Business Vision
- System Architecture
- Component Architecture

---

# 2. Scope

ครอบคลุม

- Platform Domains
- Responsibilities
- Domain Relationships
- Ownership
- Platform Boundaries

ไม่ครอบคลุม

- Database
- API
- UI
- Deployment

---

# 3. Design Principles

OneMind ออกแบบ Domain ตามหลักต่อไปนี้

- Business Capability First
- Technology Independent
- Domain Agnostic
- High Cohesion
- Loose Coupling
- Reusable Platform Services
- AI Native
- Human Centric

---

# 4. Domain Overview

OneMind ประกอบด้วย 13 Core Domains

```
People
Organization
Identity

Knowledge
Memory
Workflow

AI
Agent

Communication

Integration

Asset

Analytics

Governance
```

ทุก Domain สามารถนำกลับมาใช้ซ้ำได้ในทุกอุตสาหกรรม

---

# 5. Domain Relationship

```
People
      │
Identity ───── Organization
      │
      ▼
Workflow
      │
      ▼
Knowledge ⇄ Memory
      │
      ▼
AI Runtime
      │
      ▼
Agents
      │
      ▼
Communication
      │
      ▼
Integration
      │
      ▼
Enterprise Systems

Analytics
▲
│
Governance
```

---

# 6. Core Domain Descriptions

---

## 6.1 Identity Domain

Purpose

จัดการตัวตนของผู้ใช้ ระบบ และ AI Agent

Responsibilities

- Authentication
- Authorization
- RBAC
- ABAC
- SSO
- Federation
- Agent Identity

Key Objects

- User
- Role
- Permission
- Token

---

## 6.2 Organization Domain

Purpose

อธิบายโครงสร้างองค์กร

Responsibilities

- Company
- Hospital
- Condo
- Department
- Team
- Position

Key Objects

- Organization
- Unit
- Team
- Department

---

## 6.3 People Domain

Purpose

จัดการข้อมูลบุคลากร

Responsibilities

- Employee
- Resident
- Doctor
- Nurse
- Contractor
- Visitor

Key Objects

- Person
- Skill
- Qualification
- License

---

## 6.4 Knowledge Domain

Purpose

ศูนย์กลางองค์ความรู้ขององค์กร

Responsibilities

- Documents
- SOP
- Policies
- Manuals
- FAQ
- Semantic Search
- RAG

Key Objects

- Knowledge Item
- Document
- Tag
- Embedding

---

## 6.5 Memory Domain

Purpose

เก็บ Context ของ AI และผู้ใช้งาน

Responsibilities

- Working Memory
- Long-term Memory
- Conversation Memory
- Agent Memory
- Shared Memory

Key Objects

- Memory
- Session
- Context

---

## 6.6 Workflow Domain

Purpose

จัดการกระบวนการทำงาน

Responsibilities

- BPMN
- Approval
- Scheduling
- Automation
- Escalation

Key Objects

- Workflow
- Task
- Event
- Process

---

## 6.7 AI Domain

Purpose

ให้บริการ AI Runtime ของแพลตฟอร์ม

Responsibilities

- LLM
- Prompt
- Model Routing
- Embedding
- Guardrails

Key Objects

- Model
- Prompt
- Response

---

## 6.8 Agent Domain

Purpose

บริหารจัดการ AI Agent

Responsibilities

- Agent Registry
- Planning
- Coordination
- Tool Calling
- Multi-Agent

Key Objects

- Agent
- Skill
- Tool

---

## 6.9 Communication Domain

Purpose

สื่อสารกับผู้ใช้งาน

Responsibilities

- Chat
- Email
- Notification
- LINE
- SMS
- Voice

---

## 6.10 Integration Domain

Purpose

เชื่อมต่อระบบภายนอก

Responsibilities

- REST
- GraphQL
- MCP
- MQTT
- HL7
- FHIR
- Webhook

---

## 6.11 Asset Domain

Purpose

บริหารสินทรัพย์ขององค์กร

Examples

- Medical Equipment
- Building
- Meeting Room
- IoT Device
- EV Charger

---

## 6.12 Analytics Domain

Purpose

สร้างข้อมูลเชิงวิเคราะห์

Responsibilities

- Dashboard
- KPI
- AI Insight
- Forecast

---

## 6.13 Governance Domain

Purpose

กำกับดูแลข้อมูล AI และการปฏิบัติตามนโยบาย

Responsibilities

- Audit
- Compliance
- PDPA
- AI Governance
- Policy

---

# 7. Domain Classification

| Domain | Type |
|----------|------------|
|Identity|Core|
|Organization|Core|
|People|Core|
|Knowledge|Core|
|Memory|Core|
|Workflow|Core|
|AI|Platform|
|Agent|Platform|
|Communication|Shared|
|Integration|Shared|
|Asset|Business|
|Analytics|Shared|
|Governance|Cross-cutting|

---

# 8. Domain Dependencies

```
Identity

↓

Organization

↓

People

↓

Workflow

↓

Knowledge

↓

Memory

↓

AI

↓

Agents

↓

Communication

↓

Integration
```

Analytics และ Governance ครอบคลุมทุก Domain

---

# 9. Future Evolution

M3 จะต่อยอดเอกสารนี้ด้วย

- Bounded Context
- Service Boundaries
- Event Model
- Domain Events
- Ubiquitous Language

---

# 10. Related Documents

- OM-ARCH-020 OneMind System Architecture
- OM-ARCH-022 Component Architecture
- OM-ARCH-030 Data Architecture
- OM-ARCH-040 AI Runtime

---

# Summary

Domain Architecture คือโครงสร้างเชิงธุรกิจของ OneMind ซึ่งกำหนดขอบเขตความรับผิดชอบของแต่ละความสามารถหลักของแพลตฟอร์ม โดยไม่ผูกติดกับเทคโนโลยีหรืออุตสาหกรรมใดอุตสาหกรรมหนึ่ง ทำให้ OneMind สามารถสร้าง Reference Architecture สำหรับโรงพยาบาล อาคารชุด โรงงาน หรือองค์กรอื่น ๆ ได้จาก Core Platform เดียวกัน