---
title: C4 Level 1 - System Context Diagram
document_id: OM-ARCH-091
version: 1.0.0
status: Draft

owner: OneMind Architecture Team
classification: Internal

created: 2026-07-10
last_updated: 2026-07-10

parent: OM-ARCH-090

related:
  - OM-ARCH-020
  - OM-ARCH-060
  - OM-ARCH-090
  - OM-ARCH-092

diagram:
  - ../../drawio/06-context.drawio

tags:
  - C4
  - Context Diagram
  - Reference Architecture
  - Enterprise Architecture
---

# C4 Level 1 — System Context Diagram

> **Many Agents. One Mind.**

---

# 1. Purpose

เอกสารนี้อธิบาย **C4 Level 1 (System Context)** ของ OneMind Platform

Context Diagram แสดง

- ขอบเขตของ OneMind
- ผู้ใช้งานหลัก
- External Systems
- External Services
- จุดเชื่อมต่อทั้งหมด

โดย **ไม่ลงรายละเอียดภายในระบบ**

---

# 2. Scope

Diagram นี้ตอบคำถามว่า

> "OneMind ติดต่อกับใครบ้าง และติดต่ออย่างไร"

ไม่ได้อธิบาย

- Containers
- Services
- Database
- Internal Components

สิ่งเหล่านี้อยู่ใน C4 Level 2 และ 3

---

# 3. Primary Actors

OneMind รองรับผู้ใช้งานหลายกลุ่ม

| Actor | Description |
|--------|-------------|
| End User | ใช้งานบริการผ่าน Web หรือ Mobile |
| Employee | เจ้าหน้าที่และพนักงานองค์กร |
| Administrator | ดูแลระบบและการกำหนดค่า |
| AI Operator | ดูแล AI Models, Agents และ Runtime |
| External Partner | ระบบหรือองค์กรภายนอกที่เชื่อมต่อผ่าน API |

---

# 4. External Systems

OneMind สามารถเชื่อมต่อกับระบบภายนอก เช่น

| External System | Purpose |
|-----------------|---------|
| Identity Provider | Authentication และ Single Sign-On |
| ERP | ข้อมูลธุรกิจ |
| HR System | บุคลากร |
| HIS / EMR | ข้อมูลโรงพยาบาล |
| CRM | ลูกค้า |
| IoT Platform | อุปกรณ์และเซนเซอร์ |
| Payment Gateway | การชำระเงิน |
| Email / SMS Gateway | การแจ้งเตือน |
| Cloud AI Providers | Cloud LLM Services |

รายการนี้เป็นตัวอย่างอ้างอิง แต่สามารถปรับให้เหมาะกับแต่ละโครงการได้

---

# 5. External Services

บริการภายนอกที่ OneMind อาจใช้งาน

- OpenAI
- Anthropic
- Gemini
- Ollama (Local)
- Microsoft 365
- Google Workspace
- LDAP / Active Directory
- MQTT Brokers
- Object Storage
- GIS Services

การเชื่อมต่อทั้งหมดต้องผ่าน Integration Layer ตาม OM-ARCH-060

---

# 6. System Boundary

OneMind ประกอบด้วยความสามารถหลักภายในขอบเขตของระบบ ได้แก่

- Experience Layer
- Business Services
- AI Runtime
- Workflow Engine
- Integration Layer
- Data Platform
- Security Services
- Platform Services

องค์ประกอบเหล่านี้จะอธิบายใน C4 Level 2

---

# 7. Communication Principles

การสื่อสารระหว่าง OneMind และระบบภายนอกใช้หลักการ

- API First
- Event Driven
- Secure by Default
- Standard Protocols
- Versioned Interfaces

ทุกการเชื่อมต่ออยู่ภายใต้การกำกับของ API Gateway และ Security Architecture

---

# 8. Context View

```text
                     +----------------------+
                     |     End Users        |
                     +----------+-----------+
                                |
                                |
                     +----------v-----------+
                     |      OneMind         |
                     | AI Operating Platform|
                     +----------+-----------+
                                |
        +-----------------------+------------------------+
        |            |            |            |          |
        v            v            v            v          v
+---------------+ +-----------+ +---------+ +--------+ +-------------+
| Identity      | | ERP / HR  | | HIS/EMR | | IoT    | | AI Providers|
| Provider      | | CRM       | |         | |        | | / LLM APIs  |
+---------------+ +-----------+ +---------+ +--------+ +-------------+
```

Diagram ฉบับสมบูรณ์จัดเก็บใน

```
docs/drawio/06-context.drawio
```

---

# 9. Assumptions

Reference Context นี้ตั้งอยู่บนสมมติฐานว่า

- OneMind เป็น Enterprise Platform
- รองรับหลายโดเมนธุรกิจ
- ใช้งานได้ทั้ง Cloud และ On-premises
- รองรับ Local และ Cloud AI
- รองรับ Multi-Agent Architecture

---

# 10. Relationship to Other Documents

เอกสารนี้เชื่อมโยงกับ

| Document | Purpose |
|----------|---------|
| OM-ARCH-090 | Reference Architecture |
| OM-ARCH-092 | C4 Container Diagram |
| OM-ARCH-093 | C4 Component Diagram |
| OM-ARCH-060 | Integration Architecture |
| OM-ARCH-050 | Security Architecture |

---

# 11. Maintenance

System Context Diagram ต้องได้รับการทบทวนเมื่อ

- มี External System ใหม่
- มี Integration ใหม่
- มีการเปลี่ยน Architecture Boundary
- มีการเปลี่ยน Business Scope

การเปลี่ยนแปลงต้องอัปเดตทั้งเอกสารและไฟล์ Draw.io ให้สอดคล้องกัน

---

# 12. Key Takeaways

C4 Level 1 แสดงขอบเขตของ OneMind Platform และความสัมพันธ์กับผู้ใช้งานและระบบภายนอก โดยเน้น "ภาพรวมของระบบ" มากกว่ารายละเอียดภายใน

เอกสารนี้เป็นจุดเริ่มต้นของชุด C4 Model และเป็นพื้นฐานสำหรับการทำความเข้าใจสถาปัตยกรรมในระดับองค์กร ก่อนลงรายละเอียดใน C4 Level 2 และ C4 Level 3

---
