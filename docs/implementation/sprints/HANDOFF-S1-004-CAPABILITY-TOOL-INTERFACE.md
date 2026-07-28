# HANDOFF-S1-004-CAPABILITY-TOOL-INTERFACE.md

Document ID: OM-HANDOFF-S1-004  
Version: 1.0.0
Status: Planned
Milestone: M6 Platform Engineering
Sprint: Sprint 1 — Agent Runtime Foundation
Branch: feature/sprint1-agent-runtime

---

# 1. Sprint Summary

## Sprint Name

Agent Capability & Tool Interface

## Objective

สร้าง Capability Layer สำหรับ OneMind Agent Runtime เพื่อแยกความสามารถ (Capabilities) ออกจาก Agent Logic

Capability Layer จะเป็น Foundation สำหรับการเชื่อมต่อ

- Internal Tools
- Knowledge Services
- Memory Services
- LLM Providers
- MCP Servers
- External APIs

แนวคิดหลักคือ

> Agent ไม่ควรรู้ว่าบริการแต่ละตัวทำงานอย่างไร แต่รู้เพียงว่าเรียก Capability อะไร

---

# 2. Background

หลัง Sprint 1-003 Agent Runtime สามารถ

- Register Agent
- Discover Agent
- Execute Agent
- Create AgentContext
- Inject Context
- Track Request ID
- Return Execution Metadata

Current Flow

```text
Client

↓

Runtime

↓

Create Context

↓

Resolve Agent

↓

Agent.execute(task, context)

↓

Result
```

ข้อจำกัด

- Agent เรียก Service ตรงไม่ได้
- ไม่มี Layer สำหรับ Tools
- ไม่มี Layer สำหรับ Memory
- ไม่มี Layer สำหรับ Knowledge
- ไม่มีมาตรฐานการเพิ่ม Capability ใหม่

---

# 3. Sprint Goal

เพิ่ม Capability Layer ระหว่าง Agent กับ Platform Services

Target Architecture

```text
Client

↓

Agent Runtime

↓

Agent Context

↓

Agent

↓

Capability Manager

├──────────────┐
│              │
│              │
Tools      Knowledge
│              │
│              │
Memory      Future MCP
```

---

# 4. Architecture Principles

Capability Layer ต้องมีคุณสมบัติ

- Modular
- Replaceable
- Testable
- Dependency Injection Ready
- Async Native
- Future Plugin Compatible

Agent จะไม่ Import Tool โดยตรง

Agent จะเรียกผ่าน

```python
await capabilities.execute(...)
```

เท่านั้น

---

# 5. New Components

## 5.1 Capability Package

Directory

```text
services/agent-runtime/app/capabilities/
```

ประกอบด้วย

```text
__init__.py
base.py
registry.py
echo.py
```

---

## 5.2 BaseCapability

File

```text
services/agent-runtime/app/capabilities/base.py
```

หน้าที่

กำหนด Interface มาตรฐานของ Capability

Example

```python
class BaseCapability(ABC):

    name: str

    @abstractmethod
    async def execute(self, **kwargs):
        ...
```

---

## 5.3 CapabilityRegistry

File

```text
services/agent-runtime/app/capabilities/registry.py
```

หน้าที่

- Register Capability
- Resolve Capability
- List Capability

Public API

```python
register()

get()

list()
```

รองรับการเพิ่ม Capability ใหม่โดยไม่ต้องแก้ Runtime

---

## 5.4 EchoCapability

File

```text
services/agent-runtime/app/capabilities/echo.py
```

Purpose

Capability ตัวอย่างสำหรับทดสอบ Framework

Example

```python
await execute(
    text="Hello"
)
```

Return

```json
{
  "echo": "Hello"
}
```

---

## 5.5 CapabilityManager

File

```text
services/agent-runtime/app/capability_manager.py
```

หน้าที่

- Own Registry
- Register Default Capabilities
- Execute Capability
- Validate Capability Existence

Public API

```python
await execute(
    capability_name,
    **kwargs
)

list()
```

---

# 6. Runtime Changes

File

```text
services/agent-runtime/app/runtime.py
```

เดิม

```python
agent.execute(
    task,
    context
)
```

ใหม่

```python
agent.execute(
    task,
    context,
    capability_manager
)
```

Runtime จะสร้าง CapabilityManager เพียงครั้งเดียว

---

# 7. Base Agent Contract

File

```text
services/agent-runtime/app/agents/base.py
```

เดิม

```python
execute(
    task,
    context
)
```

ใหม่

```python
execute(
    task,
    context,
    capabilities
)
```

---

# 8. Demo Agent Update

File

```text
services/agent-runtime/app/agents/demo_agent.py
```

ตัวอย่าง

```python
tool_result = await capabilities.execute(
    "echo",
    text=task["message"]
)
```

Return

```json
{
  "message": "Hello OneMind",
  "request_id": "...",
  "tool_result": {
    "echo": "Hello OneMind"
  }
}
```

---

# 9. Directory Structure

หลัง Sprint นี้

```text
services/

└── agent-runtime/

    app/

        runtime.py

        capability_manager.py

        capabilities/

            __init__.py

            base.py

            registry.py

            echo.py

        agents/

            base.py

            context.py

            demo_agent.py
```

---

# 10. Execution Flow

ก่อน Sprint

```text
Client

↓

Runtime

↓

Agent

↓

Business Logic
```

หลัง Sprint

```text
Client

↓

Runtime

↓

Context

↓

Agent

↓

Capability Manager

↓

Capability

↓

Result
```

---

# 11. API Example

Request

```http
POST /execute
```

Payload

```json
{
  "agent": "demo-agent",
  "task": {
    "message": "Hello OneMind"
  }
}
```

Expected Response

```json
{
  "status": "completed",
  "agent": "demo-agent",
  "request_id": "...",
  "context": {
    "session_id": null,
    "user_id": null
  },
  "result": {
    "message": "Hello OneMind",
    "request_id": "...",
    "tool_result": {
      "echo": "Hello OneMind"
    }
  }
}
```

---

# 12. Validation Plan

## Docker

```bash
docker compose -f docker/compose/docker-compose.yml up --build -d
```

Expected

PASS

---

## Agent Discovery

```bash
curl http://localhost:8002/agents
```

Expected

```json
{
  "agents": [
    "demo-agent"
  ]
}
```

PASS

---

## Execute Agent

```bash
curl -X POST http://localhost:8002/execute \
-H "Content-Type: application/json" \
-d '{
  "agent":"demo-agent",
  "task":{
    "message":"Hello OneMind"
  }
}'
```

Expected

- Context ถูกสร้าง
- Capability ถูกเรียก
- EchoCapability ทำงาน
- Response มี tool_result

PASS

---

# 13. Files to Create

```text
services/agent-runtime/app/capability_manager.py

services/agent-runtime/app/capabilities/

    __init__.py
    base.py
    registry.py
    echo.py
```

---

# 14. Files to Modify

```text
services/agent-runtime/app/runtime.py

services/agent-runtime/app/agents/base.py

services/agent-runtime/app/agents/demo_agent.py
```

---

# 15. Definition of Done

Completed เมื่อ

- [ ] Capability Package ถูกสร้าง
- [ ] BaseCapability ทำงาน
- [ ] CapabilityRegistry ทำงาน
- [ ] CapabilityManager ทำงาน
- [ ] EchoCapability ทำงาน
- [ ] BaseAgent Contract ถูกอัปเดต
- [ ] Runtime Inject CapabilityManager
- [ ] DemoAgent ใช้งาน Capability ได้
- [ ] Docker Build ผ่าน
- [ ] Execute API ผ่าน
- [ ] Commit แล้ว
- [ ] Push แล้ว

---

# 16. Architecture Impact

Sprint นี้สร้าง Foundation สำคัญของ Platform

```text
Agent

↓

Capability Manager

├─────────────┐
│             │
│             │
Tools     Knowledge
│             │
│             │
Memory     MCP
│             │
│             │
LLM      External APIs
```

หลังจากนี้ Agent จะสามารถเรียกบริการทุกประเภทผ่าน Interface เดียว

ทำให้ Runtime มีความยืดหยุ่นและสามารถเพิ่ม Capability ใหม่ได้โดยไม่ต้องแก้ไข Agent

---

# 17. Future Capability Roadmap

Sprint ถัดไปสามารถเพิ่ม

- MemoryCapability
- KnowledgeCapability
- LLMCapability
- WebSearchCapability
- MCPClientCapability
- PlannerCapability
- WorkflowCapability

โดยใช้ Framework เดียวกัน

---

# 18. Expected Outcome

เมื่อ Sprint นี้เสร็จ OneMind จะมี

- Standard Capability Interface
- Capability Registry
- Capability Manager
- Tool Invocation Framework
- Agent Runtime ที่พร้อมรองรับ Memory, Knowledge และ MCP

Capability Layer นี้จะเป็น Foundation สำคัญสำหรับการพัฒนา Multi-Agent Platform ตามวิสัยทัศน์

**Many Agents. One Mind.**