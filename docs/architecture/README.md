# OneMind Architecture Repository

> Enterprise Architecture for the OneMind AI Operating Platform

---

# Purpose

โฟลเดอร์นี้เป็นศูนย์กลางของ Enterprise Architecture ของ OneMind

Architecture ถูกแบ่งตาม Domain เพื่อให้สามารถขยาย ดูแล และอ้างอิงได้ง่าย โดยอิงแนวคิดจาก TOGAF, Domain-Driven Design (DDD), C4 Model และ AI Native Architecture

---

# Architecture Structure

```text
architecture/

├── vision/
├── business/
├── system/
├── data/
├── ai/
├── security/
├── integration/
├── technology/
├── deployment/
└── reference/
```

---

# Architecture Domains

| Domain | Purpose | Status |
|---------|---------|--------|
| Vision | Vision และ Blueprint | ✅ |
| Business | Business Architecture | ✅ |
| System | System & Component Architecture | ✅ |
| Data | Data, Memory และ Knowledge | ✅ |
| AI | AI Runtime และ Agent Architecture | ✅ |
| Security | Security, PDPA, Governance, Zero Trust | ✅ |
| Integration | API และ Event Architecture | ✅ |
| Technology | Technology Reference Architecture | 🚧 |
| Deployment | Deployment & Infrastructure | ⏳ |
| Reference | C4 และ Reference Models | ⏳ |

---

# Document Index

## Vision

- 00 OneMind Blueprint
- 11 Platform Capability Matrix

## Business

- OM-BIZ Series

## System

- OM-ARCH-020 System Architecture
- OM-ARCH-021 Domain Architecture
- OM-ARCH-022 Component Architecture

## Data

- OM-ARCH-030 Data Architecture
- OM-ARCH-031 Memory Architecture
- OM-ARCH-032 Knowledge Architecture

## AI

- OM-ARCH-040 AI Runtime
- OM-ARCH-041 Agent Architecture
- OM-ARCH-042 LLM Gateway

## Security

- OM-ARCH-050 Security Architecture
- OM-ARCH-051 PDPA Architecture
- OM-ARCH-052 AI Governance
- OM-ARCH-053 Zero Trust

## Integration

- OM-ARCH-060 Integration Architecture
- OM-ARCH-061 API Architecture
- OM-ARCH-062 Event-Driven Architecture

## Technology

- OM-ARCH-080 Technology Architecture

## Deployment

Reserved for Deployment Architecture (M2)

---

# Architecture Principles

OneMind Architecture ยึดหลัก

- Business Driven
- Domain Driven
- AI Native
- API First
- Event First
- Security by Design
- Privacy by Design
- Zero Trust
- Vendor Neutral
- Cloud Agnostic

---

# Related Documents

- ARCHITECTURE_GUIDE.md
- ONEMIND.md
- ROADMAP.md
- VISION.md

---

# Status

| Milestone | Status |
|-----------|--------|
| M1 | ✅ Completed |
| M2 | 🚧 In Progress |
| M3 | ⏳ Planned |

Current Completion (M2)

███████████████████████████░░░░
≈ 85%

---