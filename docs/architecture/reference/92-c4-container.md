---
title: C4 Level 2 - Container Diagram
document_id: OM-ARCH-092
version: 1.0.0
status: Draft

owner: OneMind Architecture Team
classification: Internal

created: 2026-07-10
last_updated: 2026-07-10

parent: OM-ARCH-091

related:
  - OM-ARCH-022
  - OM-ARCH-040
  - OM-ARCH-060
  - OM-ARCH-070
  - OM-ARCH-090
  - OM-ARCH-093

diagram:
  - ../../drawio/07-container.drawio

tags:
  - C4
  - Container Diagram
  - Reference Architecture
  - Enterprise Architecture
---

# C4 Level 2 — Container Diagram

> **Many Agents. One Mind.**

---

# 1. Purpose

เอกสารนี้อธิบาย **C4 Level 2 (Container Diagram)** ของ OneMind Platform

Container Diagram แสดงการแบ่งระบบออกเป็นส่วนประกอบหลัก (Containers) พร้อมความสัมพันธ์และการสื่อสารระหว่างกัน โดยยังไม่ลงรายละเอียดระดับโค้ดหรือคลาส

---

# 2. Scope

Container Diagram แสดง

- Application Containers
- AI Containers
- Data Containers
- Integration Containers
- Infrastructure Services

ไม่ครอบคลุม

- Internal Components
- Classes
- Source Code

รายละเอียดดังกล่าวอยู่ใน C4 Level 3

---

# 3. Container Principles

OneMind ออกแบบ Containers ตามหลัก

- Single Responsibility
- Loose Coupling
- High Cohesion
- API First
- Event Driven
- Stateless by Default
- Independent Deployment
- Observable by Design

---

# 4. Container Overview

```text
                    Users
                      │
                      ▼
          ┌─────────────────────┐
          │ Experience Layer    │
          │ Web / Mobile / API  │
          └──────────┬──────────┘
                     │
                     ▼
          ┌─────────────────────┐
          │ API Gateway         │
          └──────────┬──────────┘
                     │
      ┌──────────────┼──────────────┐
      ▼              ▼              ▼
┌────────────┐ ┌────────────┐ ┌────────────┐
│ Business   │ │ AI Runtime │ │ Workflow   │
│ Services   │ │ & Agents   │ │ Engine     │
└─────┬──────┘ └─────┬──────┘ └─────┬──────┘
      │              │              │
      └──────────────┼──────────────┘
                     ▼
          ┌─────────────────────┐
          │ Integration Layer   │
          │ API • Events • MCP  │
          └──────────┬──────────┘
                     ▼
          ┌─────────────────────┐
          │ Data Platform       │
          │ SQL • Vector • KB   │
          └──────────┬──────────┘
                     ▼
          ┌─────────────────────┐
          │ Infrastructure      │
          │ Docker • Kubernetes │
          └─────────────────────┘
```

---

# 5. Core Containers

## Experience Layer

ให้บริการแก่ผู้ใช้งานผ่าน

- Web Application
- Mobile Application
- Admin Portal
- Developer Portal

---

## API Gateway

หน้าที่

- Authentication
- Authorization
- API Routing
- Rate Limiting
- Request Validation
- API Versioning

เป็นจุดเข้าเพียงจุดเดียวของบริการภายนอก

---

## Business Services

ประกอบด้วยบริการตาม Business Domain เช่น

- HR
- Asset
- Facility
- Workflow
- Knowledge
- Notification

แต่ละบริการสามารถพัฒนาและปรับใช้ได้อย่างอิสระ

---

## AI Runtime

รับผิดชอบ

- Agent Runtime
- Agent Orchestration
- Prompt Execution
- Tool Calling
- Memory Access
- LLM Gateway Integration

อ้างอิง OM-ARCH-040 และ OM-ARCH-041

---

## Workflow Engine

จัดการ

- Business Process
- Automation
- Human Tasks
- Long-running Workflows
- Event Orchestration

รองรับทั้ง Workflow ที่กำหนดไว้ล่วงหน้าและ AI-assisted Workflow

---

## Integration Layer

เชื่อมต่อกับระบบภายนอกผ่าน

- REST APIs
- GraphQL
- Webhooks
- Event Bus
- MCP
- Messaging

อ้างอิง OM-ARCH-060 ถึง OM-ARCH-062

---

## Data Platform

ประกอบด้วย

- Relational Database
- Vector Database
- Memory Store
- Knowledge Repository
- Object Storage
- Metadata Store

รองรับทั้งข้อมูลเชิงธุรกรรมและข้อมูลสำหรับ AI

---

## Infrastructure Platform

บริการพื้นฐาน เช่น

- Kubernetes
- Docker
- Identity Provider
- Secrets Management
- Monitoring
- Logging
- Object Storage

รองรับการติดตั้งทั้ง On-premises และ Cloud

---

# 6. Communication Patterns

Containers สื่อสารผ่าน

- REST APIs
- Event Bus
- Message Queue
- MCP
- Streaming
- Internal Service APIs

หลีกเลี่ยงการเชื่อมต่อแบบ Point-to-Point

---

# 7. Deployment Characteristics

Containers ทุกตัวควร

- Deploy แยกได้
- Scale แยกได้
- Monitor แยกได้
- Version แยกได้
- Replace ได้โดยไม่กระทบระบบทั้งหมด

---

# 8. Cross-Cutting Services

ทุก Container ใช้บริการร่วมกัน

- Identity & Access Management
- Audit Logging
- Configuration Management
- Secret Management
- Observability
- Notification
- Policy Enforcement

---

# 9. Relationship to Other Documents

| Document | Purpose |
|----------|---------|
| OM-ARCH-022 | Component Architecture |
| OM-ARCH-040 | AI Runtime Architecture |
| OM-ARCH-060 | Integration Architecture |
| OM-ARCH-070 | Deployment Architecture |
| OM-ARCH-090 | Reference Architecture |
| OM-ARCH-093 | C4 Component Diagram |

---

# 10. Maintenance

Container Diagram ต้องได้รับการอัปเดตเมื่อ

- เพิ่ม Container ใหม่
- เปลี่ยน Architecture Boundary
- เพิ่ม Shared Platform Services
- เปลี่ยนรูปแบบการสื่อสารหลัก

การเปลี่ยนแปลงต้องสะท้อนทั้งในเอกสารและไฟล์ Draw.io

---

# 11. Key Takeaways

C4 Level 2 แสดงโครงสร้างหลักของ OneMind Platform ในระดับ Container โดยแบ่งระบบออกเป็น Experience Layer, API Gateway, Business Services, AI Runtime, Workflow Engine, Integration Layer, Data Platform และ Infrastructure Platform

เอกสารนี้เป็นสะพานเชื่อมระหว่างภาพรวมระดับองค์กร (C4 Level 1) และรายละเอียดเชิงเทคนิคของแต่ละองค์ประกอบ (C4 Level 3) ทำให้ทีมพัฒนา สถาปนิก และทีมปฏิบัติการมีมุมมองร่วมกันเกี่ยวกับโครงสร้างของแพลตฟอร์ม

---
