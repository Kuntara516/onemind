---
title: OneMind Business Capability Model
document_id: OM-BIZ-011
category: Business Architecture
version: 1.0.0
status: Draft
owner: OneMind Architecture Team
approver: Chief Architect
classification: Internal

created: 2026-07-09
last_updated: 2026-07-09
next_review: 2026-10-01

milestone: M2
phase: Business Architecture

author:
  - Nonthaphon Vattanataysanun
  - ChatGPT (Architecture Assistant)

related_documents:
  - 10-business-capability-map.md
  - ../vision/20-system-architecture.md
  - ../vision/21-domain-architecture.md
  - 13-business-services.md

tags:
  - Business Capability
  - Capability Model
  - Enterprise Architecture
  - AIOS
  - OneMind
---

# OneMind Business Capability Model

> **Business Capabilities describe what the platform is able to do, independent of technology, implementation, and industry.**

---

# Revision History

| Version | Date | Description |
|----------|------------|----------------|
|1.0.0|2026-07-09|Initial Version|

---

# 1 Purpose

Business Capability Model อธิบายรายละเอียดของแต่ละ Capability ภายใน OneMind

Capability เป็น "ความสามารถทางธุรกิจ"

ไม่ใช่

- Software
- Module
- Database
- API
- Microservice

Capability เป็นภาษาที่ทั้งผู้บริหาร นักวิเคราะห์ธุรกิจ สถาปนิก และนักพัฒนาเข้าใจร่วมกัน

---

# 2 Objectives

Capability Model มีวัตถุประสงค์เพื่อ

- กำหนดขอบเขตของแต่ละ Capability
- ลดความซ้ำซ้อนของความสามารถ
- ใช้ออกแบบ Domain
- ใช้ออกแบบ Component
- ใช้ออกแบบ Services
- ใช้ออกแบบ AI Agents

---

# 3 Capability Meta Model

ทุก Capability ของ OneMind ต้องประกอบด้วยองค์ประกอบมาตรฐานดังนี้

```
Capability

├── Purpose
├── Responsibilities
├── Business Services
├── Business Objects
├── Business Rules
├── Events
├── Consumers
├── Dependencies
├── KPIs
└── Future Evolution
```

---

# 4 Capability Hierarchy

```
Enterprise Platform

↓

Capability

↓

Business Service

↓

Business Function

↓

Business Activity
```

ตัวอย่าง

```
Knowledge

↓

Semantic Search

↓

Vector Search

↓

Similarity Matching
```

---

# 5 Capability Definition Template

ทุก Capability ควรอธิบายด้วยโครงสร้างเดียวกัน

## Purpose

Capability นี้มีไว้เพื่ออะไร

---

## Responsibilities

Capability นี้รับผิดชอบอะไร

---

## Business Services

ให้บริการอะไร

---

## Business Objects

จัดการข้อมูลอะไร

---

## Business Rules

มีกฎทางธุรกิจอะไร

---

## Events

เกิดเหตุการณ์อะไร

---

## Consumers

ใครใช้งาน

---

## Dependencies

ต้องพึ่งพา Capability ไหน

---

## KPIs

วัดผลอย่างไร

---

## Future Evolution

จะขยายอย่างไรในอนาคต

---

# 6 Core Capability Catalog

## 6.1 Identity

### Purpose

บริหารตัวตนของมนุษย์ ระบบ และ AI Agent

### Business Services

- Authentication
- Authorization
- Federation
- Identity Lifecycle

### Business Objects

- User
- Role
- Permission
- Token

### Consumers

ทุกระบบในแพลตฟอร์ม

---

## 6.2 Organization

### Purpose

อธิบายโครงสร้างองค์กร

### Business Services

- Organization Management
- Department Management
- Position Management

### Business Objects

- Organization
- Unit
- Department
- Position

---

## 6.3 People

### Purpose

จัดการข้อมูลบุคลากร

### Business Services

- Personnel Management
- Competency
- Certification
- Skills

### Business Objects

- Person
- Employee
- Resident
- Doctor
- Nurse

---

## 6.4 Knowledge

### Purpose

ศูนย์กลางองค์ความรู้ขององค์กร

### Business Services

- Document Management
- Knowledge Search
- Semantic Search
- Knowledge Classification
- Version Control
- RAG

### Business Objects

- Knowledge Item
- Document
- SOP
- Policy
- FAQ

---

## 6.5 Memory

### Purpose

เก็บ Context ของ AI และผู้ใช้งาน

### Business Services

- Session Memory
- Working Memory
- Long-term Memory
- Shared Memory

### Business Objects

- Memory
- Context
- Session

---

## 6.6 Workflow

### Purpose

จัดการกระบวนการทำงานขององค์กร

### Business Services

- Workflow Engine
- Approval
- Scheduling
- Automation
- BPMN

### Business Objects

- Process
- Task
- Event

---

## 6.7 AI

### Purpose

ให้บริการ AI Runtime

### Business Services

- Prompt Management
- Model Routing
- Embedding
- Inference

### Business Objects

- Model
- Prompt
- Completion

---

## 6.8 Agents

### Purpose

บริหาร AI Agents

### Business Services

- Agent Registry
- Planning
- Coordination
- Tool Calling
- Delegation

### Business Objects

- Agent
- Skill
- Tool

---

## 6.9 Communication

### Purpose

สื่อสารกับผู้ใช้งาน

### Business Services

- Chat
- Notification
- Email
- Voice

---

## 6.10 Integration

### Purpose

เชื่อมต่อระบบภายนอก

### Business Services

- API Gateway
- MCP
- Event Bus
- Webhook
- MQTT
- HL7
- FHIR

---

## 6.11 Asset

### Purpose

บริหารสินทรัพย์ขององค์กร

### Business Services

- Asset Registry
- Asset Lifecycle
- Maintenance

---

## 6.12 Analytics

### Purpose

สร้างข้อมูลเชิงวิเคราะห์

### Business Services

- Dashboard
- KPI
- Forecast
- Reporting

---

## 6.13 Governance

### Purpose

กำกับดูแลการดำเนินงานของแพลตฟอร์ม

### Business Services

- Policy Management
- Audit
- Compliance
- AI Governance
- PDPA

---

# 7 Capability Dependencies

```
Identity
        │
Organization
        │
People
        │
Workflow
        │
Knowledge
        │
Memory
        │
AI
        │
Agents
        │
Communication
        │
Integration
```

Cross-cutting

```
Governance

Security

Observability
```

ครอบทุก Capability

---

# 8 Mapping to Domains

| Capability | Domain |
|------------|--------|
| Identity | Identity Domain |
| Knowledge | Knowledge Domain |
| Memory | Memory Domain |
| Workflow | Workflow Domain |
| AI | AI Domain |
| Agents | Agent Domain |

---

# 9 Mapping to Components

ตัวอย่าง

| Capability | Component |
|------------|-----------|
| Knowledge | Knowledge Service |
| Memory | Memory Service |
| Workflow | Workflow Engine |
| AI | AI Runtime |
| Agents | Agent Orchestrator |

---

# 10 Maturity Model

Capability สามารถพัฒนาเป็น 5 ระดับ

| Level | Description |
|---------|-------------|
|1|Manual|
|2|Digital|
|3|Integrated|
|4|AI Assisted|
|5|Autonomous|

OneMind มีเป้าหมายในการผลักดัน Capability ทุกตัวไปสู่ระดับ 4 และ 5 ตามความเหมาะสมของแต่ละองค์กร

---

# 11 References

- OM-BIZ-010 Business Capability Map
- OM-ARCH-020 System Architecture
- OM-ARCH-021 Domain Architecture

---

# Summary

Business Capability Model กำหนดโครงสร้างมาตรฐานของทุก Capability ภายใน OneMind ทำให้ทุกฝ่ายในองค์กรใช้ภาษาเดียวกัน ตั้งแต่ผู้บริหาร นักวิเคราะห์ธุรกิจ สถาปนิก ไปจนถึงนักพัฒนา และเป็นสะพานเชื่อมระหว่าง Business Architecture กับ System Architecture อย่างเป็นระบบ