---

title: OneMind Document ID Convention
document_id: OM-STD-001
category: Engineering Standard
version: 1.0.0
status: Approved
owner: OneMind Architecture Team
classification: Internal
created: 2026-07-09
last_updated: 2026-07-09
------------------------

# OneMind Document ID Convention

## Purpose

กำหนดมาตรฐานการตั้งรหัสเอกสาร (Document ID) สำหรับโครงการ OneMind เพื่อให้เอกสารทุกฉบับสามารถอ้างอิง เชื่อมโยง และติดตามเวอร์ชันได้อย่างเป็นระบบ รองรับการเติบโตจากโครงการขนาดเล็กสู่ Enterprise AI Platform

---

# Principles

Document ID ต้อง

* เป็น Unique
* ไม่เปลี่ยนเมื่อเปลี่ยนชื่อไฟล์
* ใช้อ้างอิงระหว่างเอกสารได้
* ใช้อ้างอิงใน ADR
* ใช้อ้างอิงใน Pull Request
* ใช้อ้างอิงใน Issue
* ใช้อ้างอิงใน Presentation
* ใช้อ้างอิงใน Architecture Review

---

# Structure

Document ID ใช้รูปแบบ

```
OM-<CATEGORY>-<NUMBER>
```

ตัวอย่าง

```
OM-ARCH-020
```

ประกอบด้วย

| ส่วน     | ความหมาย       |
| -------- | -------------- |
| OM       | OneMind        |
| CATEGORY | ประเภทเอกสาร   |
| NUMBER   | Running Number |

---

# Category Codes

## Foundation

| ID     | Description          |
| ------ | -------------------- |
| OM-FND | Foundation Documents |

ตัวอย่าง

```
OM-FND-001
```

---

## Vision

| ID     | Description      |
| ------ | ---------------- |
| OM-VSN | Vision Documents |

ตัวอย่าง

```
OM-VSN-001
```

---

## Architecture

| ID      | Description                |
| ------- | -------------------------- |
| OM-ARCH | Architecture Specification |

ตัวอย่าง

```
OM-ARCH-020
```

---

## Architecture Decision Record

| ID     | Description                  |
| ------ | ---------------------------- |
| OM-ADR | Architecture Decision Record |

ตัวอย่าง

```
OM-ADR-001
```

---

## Reference Architecture

| ID     | Description            |
| ------ | ---------------------- |
| OM-REF | Reference Architecture |

ตัวอย่าง

```
OM-REF-001
```

---

## Standards

| ID     | Description           |
| ------ | --------------------- |
| OM-STD | Engineering Standards |

ตัวอย่าง

```
OM-STD-001
```

---

## Governance

| ID     | Description          |
| ------ | -------------------- |
| OM-GOV | Governance Documents |

---

## API

| ID     | Description        |
| ------ | ------------------ |
| OM-API | API Specifications |

---

## Data

| ID     | Description       |
| ------ | ----------------- |
| OM-DAT | Data Architecture |

---

## AI

| ID    | Description     |
| ----- | --------------- |
| OM-AI | AI Architecture |

---

## Security

| ID     | Description           |
| ------ | --------------------- |
| OM-SEC | Security Architecture |

---

## Integration

| ID     | Description              |
| ------ | ------------------------ |
| OM-INT | Integration Architecture |

---

## Deployment

| ID     | Description             |
| ------ | ----------------------- |
| OM-DEP | Deployment Architecture |

---

## Business

| ID     | Description           |
| ------ | --------------------- |
| OM-BIZ | Business Architecture |

---

## Application

| ID     | Description              |
| ------ | ------------------------ |
| OM-APP | Application Architecture |

---

## Knowledge

| ID      | Description         |
| ------- | ------------------- |
| OM-KNOW | Knowledge Documents |

---

## Research

| ID     | Description     |
| ------ | --------------- |
| OM-RSR | Research Papers |

---

## Executive

| ID     | Description         |
| ------ | ------------------- |
| OM-EXE | Executive Documents |

---

# Numbering Rules

ใช้เลข 3 หลัก

ตัวอย่าง

```
001
002
003
...
099
100
```

ไม่ใช้

```
1
2
3
```

---

# File Name

ชื่อไฟล์สามารถเปลี่ยนได้

แต่ Document ID ต้องไม่เปลี่ยน

ตัวอย่าง

```
20-system-architecture.md
```

Document ID

```
OM-ARCH-020
```

แม้ภายหลังเปลี่ยนชื่อไฟล์เป็น

```
system-architecture.md
```

Document ID ยังคงเดิม

---

# Header Example

ทุกเอกสารควรมี Header

```yaml
title: OneMind System Architecture
document_id: OM-ARCH-020
version: 1.0.0
status: Draft
owner: OneMind Architecture Team
classification: Internal
```

---

# Cross Reference

ใช้ Document ID อ้างอิง

ตัวอย่าง

```
See OM-ADR-001
```

แทน

```
ดูไฟล์ ADR-001-postgresql.md
```

เพราะชื่อไฟล์อาจเปลี่ยนได้

---

# Versioning

Document ID

ไม่เปลี่ยน

Version

เปลี่ยนได้

ตัวอย่าง

```
OM-ARCH-020

v1.0

v1.1

v2.0
```

---

# Reserved Number Ranges

เพื่อรองรับการขยายในอนาคต

| Range   | Usage               |
| ------- | ------------------- |
| 000–099 | Vision & Foundation |
| 100–199 | Business            |
| 200–299 | Application         |
| 300–399 | Data                |
| 400–499 | AI                  |
| 500–599 | Security            |
| 600–699 | Integration         |
| 700–799 | Deployment          |
| 800–899 | Governance          |
| 900–999 | Future Expansion    |

---

# Best Practices

* ใช้ Document ID เป็นตัวอ้างอิงหลัก
* ไม่อ้างอิงด้วยชื่อไฟล์
* ไม่เปลี่ยน Document ID หลังประกาศใช้งาน
* ทุก Architecture Review ต้องระบุ Document ID
* ทุก ADR ต้องอ้างอิง Document ID ที่เกี่ยวข้อง
* ทุก Presentation ควรแสดง Document ID ของเอกสารต้นทาง

---

# Summary

Document ID เป็นตัวระบุถาวรของเอกสารในโครงการ OneMind ช่วยให้การอ้างอิง การติดตาม และการบริหารจัดการเอกสารมีความสอดคล้อง รองรับการเติบโตของแพลตฟอร์มในระยะยาว และเป็นพื้นฐานสำคัญของ Enterprise Architecture Repository
