---
title: C4 Level 3 - Component Diagram
document_id: OM-ARCH-093
version: 1.0.0
status: Draft

owner: OneMind Architecture Team
classification: Internal

created: 2026-07-10
last_updated: 2026-07-10

parent: OM-ARCH-092

related:
  - OM-ARCH-022
  - OM-ARCH-040
  - OM-ARCH-041
  - OM-ARCH-042
  - OM-ARCH-060
  - OM-ARCH-090
  - OM-ARCH-094

diagram:
  - ../../drawio/08-component.drawio

tags:
  - C4
  - Component Diagram
  - Enterprise Architecture
  - AI Operating Platform
  - OneMind
---

# C4 Level 3 — Component Diagram

> **Many Agents. One Mind.**

---

# 1. Purpose

เอกสารนี้อธิบาย **C4 Level 3 (Component Diagram)** ของ OneMind Platform โดยแสดงองค์ประกอบภายใน Container หลัก ความรับผิดชอบของแต่ละ Component และรูปแบบการสื่อสารระหว่างกัน

Component Diagram เป็นระดับที่ใช้สำหรับการออกแบบเชิงเทคนิคก่อนเข้าสู่การพัฒนา

---

# 2. Scope

Component Diagram ครอบคลุม

- Business Components
- AI Components
- Integration Components
- Data Access Components
- Shared Platform Components

ไม่ครอบคลุม

- Source Code
- Classes
- Functions
- Database Schema

รายละเอียดเหล่านี้อยู่ในเอกสารระดับการออกแบบและการพัฒนา

---

# 3. Component Design Principles

ทุก Component ต้องยึดหลัก

- Single Responsibility
- High Cohesion
- Loose Coupling
- Interface-based Design
- Stateless by Default
- Dependency Injection
- Replaceable Components
- Testability

---

# 4. Component View

```text
                API Gateway
                     │
                     ▼
          +----------------------+
          | Application Service  |
          +----------+-----------+
                     │
      +--------------+--------------+
      │              │              │
      ▼              ▼              ▼
+-------------+ +-------------+ +-------------+
| Business    | | AI Service  | | Workflow    |
| Component   | | Component   | | Component   |
+------+------+ +------+------+ +------+------+
       │               │               │
       ├───────────────┼───────────────┤
       ▼               ▼               ▼
+------------------------------------------------+
| Shared Platform Components                     |
| Identity • Config • Audit • Notification       |
+------------------------------------------------+
       │
       ▼
+------------------------------------------------+
| Data Access Layer                              |
| Repository • Memory • Knowledge • Vector DB    |
+------------------------------------------------+
```

---

# 5. Core Components

## Application Service

รับผิดชอบ

- Request Handling
- Validation
- Authorization
- Orchestration
- Transaction Coordination

เป็นจุดเริ่มต้นของ Business Flow ภายในระบบ

---

## Business Components

ประกอบด้วย Logic ตาม Business Capability เช่น

- User Management
- Asset Management
- Workflow Management
- Knowledge Management
- Scheduling
- Notification

Business Components ไม่ควรมีการพึ่งพาโดยตรงกับเทคโนโลยีเฉพาะ

---

## AI Components

ประกอบด้วย

- Agent Coordinator
- Prompt Manager
- LLM Gateway Client
- Tool Executor
- Memory Manager
- Context Builder
- Response Processor

AI Components ทำงานผ่าน AI Runtime และไม่เรียกใช้ผู้ให้บริการ LLM โดยตรง

---

## Workflow Components

รับผิดชอบ

- Process Execution
- Task Routing
- Human Approval
- Event Handling
- Automation Rules

Workflow สามารถทำงานร่วมกับ AI Components และ Business Components ได้

---

## Shared Platform Components

บริการที่ทุก Component ใช้ร่วมกัน เช่น

- Identity & Access Management
- Configuration Service
- Audit Logging
- Notification Service
- Policy Engine
- Observability

บริการเหล่านี้เป็น Cross-Cutting Components

---

## Data Access Layer

ประกอบด้วย

- Repository Pattern
- Database Access
- Vector Database Access
- Memory Store Access
- Knowledge Repository Access
- Object Storage Access

Business Components ไม่เข้าถึงฐานข้อมูลโดยตรง

---

# 6. Component Communication

การสื่อสารภายในระบบใช้

- Internal APIs
- Domain Events
- Dependency Injection
- Repository Interfaces

หลีกเลี่ยงการสร้างการพึ่งพาแบบวงจร (Circular Dependencies)

---

# 7. Dependency Rules

การพึ่งพาระหว่าง Component ต้องเป็นไปตามลำดับ

```text
Application Service
        │
        ▼
Business / AI / Workflow Components
        │
        ▼
Shared Platform Services
        │
        ▼
Data Access Layer
        │
        ▼
Infrastructure
```

ห้าม Component ชั้นล่างเรียกใช้ Component ชั้นบนโดยตรง

---

# 8. Component Responsibilities

| Component | Responsibility |
|----------|----------------|
| Application Service | ประสานการทำงานของ Use Case |
| Business Component | Business Logic |
| AI Component | AI Processing และ Agent Coordination |
| Workflow Component | Process Automation |
| Shared Platform | บริการส่วนกลาง |
| Data Access Layer | การเข้าถึงข้อมูลและแหล่งความรู้ |

---

# 9. Cross-Cutting Concerns

ทุก Component ต้องรองรับ

- Authentication
- Authorization
- Audit Logging
- Metrics
- Distributed Tracing
- Error Handling
- Configuration
- Policy Enforcement

การจัดการประเด็นเหล่านี้ควรทำผ่าน Shared Platform Components

---

# 10. Relationship to Other Documents

| Document | Purpose |
|----------|---------|
| OM-ARCH-022 | Component Architecture |
| OM-ARCH-040 | AI Runtime Architecture |
| OM-ARCH-041 | Agent Architecture |
| OM-ARCH-042 | LLM Gateway Architecture |
| OM-ARCH-060 | Integration Architecture |
| OM-ARCH-092 | C4 Container Diagram |
| OM-ARCH-094 | Infrastructure Reference Model |

---

# 11. Maintenance

Component Diagram ต้องได้รับการอัปเดตเมื่อ

- เพิ่มหรือยกเลิก Component
- เปลี่ยนขอบเขตความรับผิดชอบ
- เพิ่ม Shared Platform Services
- เปลี่ยนรูปแบบการสื่อสารภายใน

Diagram และเอกสารต้องสอดคล้องกับ Component Architecture และโค้ดที่ใช้งานจริง

---

# 12. Key Takeaways

C4 Level 3 แสดงโครงสร้างภายในของ Container หลักใน OneMind โดยแบ่งเป็น Application Service, Business Components, AI Components, Workflow Components, Shared Platform Components และ Data Access Layer

เอกสารนี้ช่วยให้ทีมพัฒนาเข้าใจการแบ่งความรับผิดชอบของแต่ละส่วน ลดการเชื่อมโยงที่ไม่จำเป็น และสนับสนุนการพัฒนาระบบที่สามารถขยาย ดูแลรักษา และทดสอบได้ในระยะยาว

---