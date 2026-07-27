# SPRINT-1-AGENT-RUNTIME-FOUNDATION.md

**Project:** OneMind  
**Milestone:** M6 — Platform Engineering  
**Sprint:** Sprint 1  
**Branch:** feature/sprint1-agent-runtime  
**Status:** Planned  
**Version:** 0.1.0  

---

# Sprint 1 — Agent Runtime Foundation

## 1. Sprint Objective

สร้างพื้นฐานของ Agent Runtime Layer สำหรับ OneMind Platform เพื่อให้ระบบสามารถ:

- รับคำสั่งจาก Planner Runtime
- สร้าง Agent Execution Context
- เรียกใช้งาน Agent ตาม Capability
- จัดการ Agent Lifecycle
- ส่งผลลัพธ์กลับไปยัง Orchestrator

Sprint นี้เป็นก้าวแรกจาก Platform Bootstrap ไปสู่ระบบ Multi-Agent Runtime จริง

เป้าหมายหลัก:

> "OneMind can create, execute and manage intelligent agents."

---

# 2. Current Platform State

จาก Sprint 0 ระบบสามารถ:

## Infrastructure

สถานะปัจจุบัน:

| Component | Status |
|---|---|
| Docker Compose | Online |
| PostgreSQL | Running |
| Redis | Running |
| API Gateway | Running |
| Planner Runtime | Running |
| Ollama Integration | Working |

Runtime Endpoint:

```
API Gateway
http://localhost:8000

Planner Runtime
http://localhost:8001
```

Planner สามารถเรียก LLM ผ่าน Ollama ได้แล้ว

Example:

```
POST /plan

{
  "prompt": "Explain what OneMind is"
}
```

Response:

```json
{
  "model": "qwen2.5:3b",
  "response": "..."
}
```

---

# 3. Sprint Goal

สร้าง Agent Runtime Foundation Layer

Architecture Target:

```
User
 |
API Gateway
 |
Planner Runtime
 |
Agent Runtime
 |
Agent Executor
 |
LLM / Tools / Knowledge
```

---

# 4. Scope

## In Scope

Sprint นี้จะสร้าง:

### 4.1 Agent Runtime Service

สร้าง service สำหรับ:

- Agent registration
- Agent discovery
- Agent execution
- Agent state management


Target structure:

```
services/

agent-runtime/

├── app
│   ├── main.py
│   ├── runtime.py
│   ├── registry.py
│   ├── models.py
│   └── agents
│       └── base.py
│
├── requirements.txt
└── Dockerfile
```

---

## 4.2 Base Agent Interface

สร้าง Agent Contract กลาง


Example:

```python
class BaseAgent:

    name: str

    async def execute(self, task):
        raise NotImplementedError
```


ทุก Agent ใน OneMind ต้อง implement interface นี้

---

## 4.3 Agent Registry

สร้างระบบเก็บรายการ Agent


ตัวอย่าง:

```json
{
  "agents": [
    {
      "name": "planner-agent",
      "type": "planner",
      "status": "active"
    }
  ]
}
```


Registry จะเป็น source of truth สำหรับ Agent Runtime

---

## 4.4 Agent Execution Context

สร้าง execution context สำหรับแต่ละ task


Example:

```json
{
  "task_id": "task-001",
  "agent": "planner-agent",
  "input": {},
  "status": "running"
}
```

---

## 4.5 Connect Planner Runtime

Planner Runtime ต้องสามารถ:

ส่ง task ไป Agent Runtime

Flow:

```
Planner Runtime

POST

Agent Runtime
/api/v1/execute
```

---

# 5. Out of Scope

ยังไม่ทำใน Sprint นี้:

- Long Term Memory
- Vector Search
- MCP Server
- Tool Calling
- Multi Agent Collaboration
- Workflow Engine
- Human Approval Flow
- UI Dashboard

สิ่งเหล่านี้จะเข้าสู่ Sprint ถัดไป

---

# 6. Proposed API

## Agent Runtime Health

```
GET /health
```

Response:

```json
{
 "status":"ok"
}
```

---

## List Agents

```
GET /agents
```

Response:

```json
{
 "agents":[
   {
    "name":"planner-agent",
    "status":"active"
   }
 ]
}
```

---

## Execute Agent

```
POST /execute
```

Request:

```json
{
 "agent":"planner-agent",
 "task":{
    "prompt":"Create project plan"
 }
}
```

Response:

```json
{
 "agent":"planner-agent",
 "status":"completed",
 "result":"..."
}
```

---

# 7. Docker Integration

เพิ่ม service:

```
docker/compose/docker-compose.yml
```

เพิ่ม:

```yaml
agent-runtime:
  build:
    context: ../../services/agent-runtime
  ports:
    - "8002:8002"
  depends_on:
    - redis
    - postgres
```

Expected:

```
docker compose up
```

ต้องมี:

```
api-gateway
planner-runtime
agent-runtime
postgres
redis
```

---

# 8. Development Tasks

## Task S1-001

Create Agent Runtime service

Deliverables:

- Dockerfile
- requirements.txt
- FastAPI application


---

## Task S1-002

Create Agent Model


File:

```
models.py
```


Define:

- Agent
- Task
- ExecutionResult


---

## Task S1-003

Create Base Agent Interface


File:

```
agents/base.py
```


---

## Task S1-004

Create Agent Registry


File:

```
registry.py
```


---

## Task S1-005

Create Execution Engine


File:

```
runtime.py
```


Responsibilities:

- receive task
- select agent
- execute
- return result


---

## Task S1-006

Integrate Planner Runtime


Planner:

```
8001
```

calls:

```
8002
```

---

# 9. Definition of Done

Sprint 1 Complete เมื่อ:

## Runtime

- [ ] agent-runtime container starts
- [ ] health endpoint works
- [ ] API documented in OpenAPI


## Agent System

- [ ] BaseAgent exists
- [ ] Agent Registry works
- [ ] Agent execution works


## Integration

- [ ] Planner Runtime can call Agent Runtime
- [ ] End-to-end execution succeeds


## Git

- [ ] All changes committed
- [ ] Branch pushed
- [ ] Sprint handoff created

---

# 10. Expected Repository Changes

New files:

```
services/agent-runtime/

docs/development/sprints/

SPRINT-1-AGENT-RUNTIME-FOUNDATION.md
```

Modified:

```
docker/compose/docker-compose.yml

services/planner-runtime/
```

---

# 11. Commit Strategy

Commit ทุก logical step


Examples:

```
feat: add agent runtime service skeleton

feat: implement base agent interface

feat: add agent registry

feat: integrate planner runtime with agent runtime

docs: add sprint1 agent runtime foundation
```

---

# 12. Sprint Output

เมื่อ Sprint นี้เสร็จ OneMind จะมี:

```
OneMind Platform

        API Gateway
             |
        Planner Runtime
             |
        Agent Runtime
             |
     -----------------
     |       |       |
 Agent1  Agent2  Agent3
```

เป็นพื้นฐานสำหรับ:

- Multi-Agent System
- Autonomous Workflow
- Knowledge Agent
- Enterprise AI Operating Platform


---

# 13. Next Sprint Preview

Sprint 2:

## Memory + Knowledge Foundation

เป้าหมาย:

- Agent Memory
- Vector Knowledge Store
- RAG Pipeline
- Context Retrieval

---

**End of Sprint Definition**