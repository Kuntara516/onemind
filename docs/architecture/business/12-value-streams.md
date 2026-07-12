---
title: OneMind Enterprise Value Streams
document_id: OM-BIZ-012
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
  - 11-business-capability-model.md
  - 13-business-services.md
  - ../vision/20-system-architecture.md
  - ../vision/21-domain-architecture.md

tags:
  - Value Streams
  - Business Architecture
  - Enterprise Architecture
  - AIOS
  - OneMind
---

# OneMind Enterprise Value Streams

> **OneMind creates value by orchestrating people, knowledge, workflows, and AI into measurable business outcomes.**

---

# Revision History

| Version | Date | Description |
|----------|------------|----------------|
|1.0.0|2026-07-09|Initial Version|

---

# 1. Purpose

Value Stream คือ "ลำดับของกิจกรรมที่สร้างคุณค่าให้กับผู้รับบริการ"

ใน OneMind Value Stream ไม่ได้อธิบายขั้นตอนของระบบ แต่แสดงให้เห็นว่า Business Capabilities ทำงานร่วมกันอย่างไรเพื่อสร้างผลลัพธ์ที่องค์กรต้องการ

---

# 2. Objectives

เอกสารนี้มีวัตถุประสงค์เพื่อ

- เชื่อมโยง Business Vision กับ Business Capabilities
- อธิบายการสร้างคุณค่าของแพลตฟอร์ม
- ใช้เป็นพื้นฐานของ Workflow และ Process Design
- รองรับการสร้าง Industry-specific Solutions โดยใช้ Core Platform เดียวกัน

---

# 3. Value Stream Principles

OneMind ออกแบบ Value Streams ตามหลักการดังนี้

- Outcome Driven
- Human-Centered
- AI-Native
- Capability-Based
- Technology Independent
- Reusable Across Industries

---

# 4. Generic Enterprise Value Stream

ทุกองค์กรสามารถอธิบายการดำเนินงานผ่านวงจรคุณค่าพื้นฐานนี้

```text
Discover
    ↓
Plan
    ↓
Execute
    ↓
Collaborate
    ↓
Learn
    ↓
Improve
    ↺
```

OneMind สนับสนุนทุกช่วงของวงจรนี้

---

# 5. Core Enterprise Value Streams

## 5.1 Workforce Value Stream

Purpose

บริหารวงจรชีวิตของบุคลากร

```text
Recruit
    ↓
Onboard
    ↓
Train
    ↓
Schedule
    ↓
Operate
    ↓
Evaluate
    ↓
Develop
```

Capabilities ที่เกี่ยวข้อง

- Identity
- People
- Organization
- Workflow
- Knowledge
- AI
- Analytics

---

## 5.2 Knowledge Value Stream

Purpose

เปลี่ยนข้อมูลให้เป็นองค์ความรู้ที่ใช้งานได้

```text
Capture
    ↓
Validate
    ↓
Classify
    ↓
Publish
    ↓
Search
    ↓
Reuse
    ↓
Improve
```

Capabilities

- Knowledge
- Memory
- AI
- Governance

---

## 5.3 Decision Intelligence Value Stream

Purpose

สนับสนุนการตัดสินใจของผู้บริหาร

```text
Collect
    ↓
Analyze
    ↓
Recommend
    ↓
Approve
    ↓
Execute
    ↓
Measure
```

Capabilities

- Analytics
- AI
- Workflow
- Governance

---

## 5.4 Operational Excellence Value Stream

Purpose

เพิ่มประสิทธิภาพการดำเนินงาน

```text
Request
    ↓
Prioritize
    ↓
Execute
    ↓
Monitor
    ↓
Resolve
    ↓
Review
```

Capabilities

- Workflow
- Communication
- Integration
- Analytics

---

## 5.5 Continuous Learning Value Stream

Purpose

ทำให้องค์กรเรียนรู้และพัฒนาอย่างต่อเนื่อง

```text
Experience
    ↓
Capture
    ↓
Reflect
    ↓
Learn
    ↓
Share
    ↓
Standardize
```

Capabilities

- Knowledge
- Memory
- AI
- Governance

---

# 6. Industry Examples

## Hospital

```text
Recruit Staff
      ↓
Train Staff
      ↓
Schedule Staff
      ↓
Deliver Care
      ↓
Review Outcomes
      ↓
Improve Services
```

---

## Smart Building / Condominium

```text
Resident Request
        ↓
Prioritize
        ↓
Assign
        ↓
Maintain
        ↓
Notify
        ↓
Evaluate
```

---

## Manufacturing

```text
Production Plan
        ↓
Operate
        ↓
Inspect
        ↓
Analyze
        ↓
Improve
```

---

ทุกตัวอย่างข้างต้นใช้ Business Capabilities เดียวกัน แต่จัดเรียงตามบริบทของแต่ละอุตสาหกรรม

---

# 7. Capability Mapping

| Value Stream | Primary Capabilities |
|--------------|----------------------|
| Workforce | People, Workflow, Knowledge |
| Knowledge | Knowledge, Memory, AI |
| Decision Intelligence | Analytics, AI, Governance |
| Operations | Workflow, Communication, Integration |
| Continuous Learning | Knowledge, Memory, Governance |

---

# 8. AI in Value Streams

AI ไม่ใช่ Value Stream แยกต่างหาก

AI เป็นตัวเร่ง (Accelerator) ที่ทำงานร่วมกับทุก Value Stream

ตัวอย่าง

```text
Knowledge
     │
     ▼
AI Assistant

Workflow
     │
     ▼
AI Scheduler

Analytics
     │
     ▼
AI Advisor
```

---

# 9. Measuring Value

OneMind สนับสนุนการวัดผลในทุก Value Stream

ตัวอย่าง KPI

| Value Stream | Example KPI |
|--------------|-------------|
| Workforce | Scheduling Accuracy, Training Completion |
| Knowledge | Search Success Rate, Knowledge Reuse |
| Operations | SLA Achievement, Cycle Time |
| Decision | Decision Lead Time |
| Learning | Lessons Reused, SOP Adoption |

---

# 10. Future Evolution

ในระยะถัดไปจะเพิ่มเติม

- Customer Journey Mapping
- Service Blueprints
- Event Storming
- Business Process Models (BPMN)
- Industry-specific Value Streams

---

# References

- OM-BIZ-010 Business Capability Map
- OM-BIZ-011 Business Capability Model
- OM-BIZ-013 Business Services
- OM-ARCH-020 System Architecture
- OM-ARCH-021 Domain Architecture

---

# Summary

Enterprise Value Streams แสดงให้เห็นว่า OneMind สร้างคุณค่าอย่างไรผ่านการประสานงานของ Business Capabilities โดยไม่ผูกติดกับอุตสาหกรรมใดอุตสาหกรรมหนึ่ง ทำให้สามารถนำแพลตฟอร์มเดียวกันไปใช้กับโรงพยาบาล อาคารชุด โรงงาน มหาวิทยาลัย หรือองค์กรภาครัฐได้ เพียงปรับลำดับกิจกรรมของ Value Stream ให้เหมาะกับบริบทของแต่ละองค์กร ขณะที่แกนหลักของแพลตฟอร์มยังคงเหมือนเดิม