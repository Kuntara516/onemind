# HANDOFF-S1-001-AGENT-RUNTIME-FOUNDATION.md

**Project:** OneMind  
**Milestone:** Sprint 1 — Agent Runtime Foundation  
**Document ID:** S1-001  
**Status:** Completed  
**Branch:** feature/sprint1-agent-runtime  
**Date:** 2026-07-27  
**Author:** OneMind Engineering  

---

# 1. Objective

Sprint 1 มีเป้าหมายเพื่อเริ่มสร้าง Agent Runtime Layer ของ OneMind Platform

หลังจาก Sprint 0 สำเร็จ ซึ่งสามารถทำให้ Platform Runtime เริ่มทำงานได้:

- API Gateway Online
- Planner Runtime Online
- Ollama Integration Online
- PostgreSQL Online
- Redis Online

Sprint 1 จึงเริ่มสร้าง Runtime สำหรับการจัดการ AI Agent จริง

เป้าหมายหลัก:

> Enable OneMind to register, discover, and execute autonomous agents through a unified runtime.

---

# 2. Sprint 1 Scope

Sprint 1 — Agent Runtime Foundation ประกอบด้วย:

## Completed

- Create agent-runtime service
- Add FastAPI runtime service
- Add agent registry foundation
- Add agent execution abstraction
- Add agent task model
- Add Docker service integration
- Verify runtime container startup
- Verify health endpoint
- Verify OpenAPI contract

---

# 3. Repository Changes

เพิ่ม service ใหม่:

```
services/
└── agent-runtime/
    ├── Dockerfile
    ├── requirements.txt
    └── app/
        ├── __init__.py
        ├── main.py
        ├── models.py
        ├── registry.py
        ├── runtime.py
        └── agents/
            └── __init__.py
```

---

# 4. Agent Runtime Architecture

Current architecture:

```
                +----------------+
                |  API Gateway   |
                |    :8000       |
                +--------+-------+
                         |
                         |
                         v

                +----------------+
                | Planner Runtime|
                |    :8001       |
                +--------+-------+
                         |
                         |
                         v

                +----------------+
                | Agent Runtime  |
                |    :8002       |
                +--------+-------+
                         |
          +--------------+--------------+
          |                             |
          v                             v

    Agent Registry              Agent Executor

          |
          v

   Future Agents

   - Knowledge Agent
   - Facility Agent
   - Workflow Agent
   - Data Agent
   - Memory Agent

```

---

# 5. Docker Integration

เพิ่ม service:

```
agent-runtime
```

ใน:

```
docker/compose/docker-compose.yml
```

Configuration:

```yaml
agent-runtime:

  build:
    context: ../../services/agent-runtime

  ports:
    - "8002:8002"

  depends_on:
    - planner-runtime
    - postgres
    - redis
```

---

# 6. Runtime Service

## Container

ตรวจสอบ:

```bash
docker compose -f docker/compose/docker-compose.yml ps
```

Expected:

```
onemind-agent-runtime-1

STATUS:
Up
```

---

# 7. Health Verification

Command:

```bash
curl http://localhost:8002/health
```

Result:

```json
{
  "status": "ok",
  "service": "agent-runtime"
}
```

---

# 8. API Contract

Agent Runtime exposes:

## GET /health

Purpose:

ตรวจสอบ service availability


Response:

```json
{
 "status":"ok",
 "service":"agent-runtime"
}
```

---

## GET /agents

Purpose:

List available agents


Example:

```json
{
 "agents":[]
}
```

Current state:

Registry foundation only.

---

## POST /execute

Purpose:

Execute agent task


Request:

```json
{
 "agent":"example-agent",
 "task":{
    "input":"hello"
 }
}
```

Response:

ขึ้นกับ runtime implementation

---

# 9. Current Source Design


## models.py

Responsibility:

Define API contract models.


Current model:

```python
AgentTask

{
    agent: str,
    task: dict
}
```


---

## registry.py

Responsibility:

Agent registration and discovery.


Current capability:

- Store registered agents
- List available agents


Future:

- Dynamic registration
- Agent metadata
- Capability discovery

---

## runtime.py

Responsibility:

Execute selected agent.


Current capability:

- Receive agent name
- Dispatch execution


Future:

- Agent lifecycle management
- Retry mechanism
- Observability
- Memory integration

---

# 10. Current Limitations

Sprint 1 foundation intentionally keeps implementation minimal.

Not implemented yet:

- Real agent implementations
- Agent memory
- Tool calling
- MCP integration
- Workflow orchestration
- Authentication
- Permission model
- Event bus
- Agent marketplace

These belong to future sprints.

---

# 11. Engineering Decision

## Decision: Agent Runtime as Independent Service

Reason:

OneMind architecture separates responsibilities:

```
Planner Runtime
        |
        |
        v
Agent Runtime
        |
        |
        v
Individual Agents
```

Benefits:

- Independent scaling
- Clear ownership boundary
- Future multi-agent architecture
- Easier observability
- Supports distributed agents

---

# 12. Sprint 1 Definition of Done

Completed:

[x] agent-runtime service created

[x] Docker image builds successfully

[x] Container starts successfully

[x] Health endpoint available

[x] Agent API contract created

[x] Agent registry foundation created

[x] Runtime execution abstraction created


---

# 13. Git Status

Branch:

```
feature/sprint1-agent-runtime
```

Latest commits:

```
4153d8a
Merge branch 'feature/sprint0-bootstrap' into feature/sprint1-agent-runtime

4f8384e
docs: add sprint1 agent runtime foundation
```

---

# 14. Next Sprint Activities

Recommended next tasks:

## S1-002 Agent Registry Implementation

Implement:

- Agent metadata
- Agent capability definition
- Agent registration


Example:

```json
{
"name":"knowledge-agent",
"type":"rag",
"capabilities":[
 "search",
 "summarize"
]
}
```


---

## S1-003 First Real Agent

Create:

```
services/agent-runtime/app/agents/
```

Example:

```
knowledge_agent.py
```

Capabilities:

- Receive task
- Process request
- Return result


---

## S1-004 Planner → Agent Runtime Integration

Connect:

```
Planner Runtime

        |

        v

Agent Runtime

        |

        v

Agent Execution
```

---

# 15. Engineering Workflow Standard Update

จาก Sprint 1 เป็นต้นไป:

เมื่อสร้าง Markdown Document ใหม่

ต้องสร้างเป็น:

```
ONE COMPLETE MARKDOWN FILE
```

ไม่แบ่งส่งหลายข้อความ

รูปแบบการทำงาน:

1. ระบุ filename

Example:

```
docs/development/sprints/SPRINT-X-XXX.md
```

2. ส่ง Markdown ทั้งไฟล์ในครั้งเดียว

3. User copy-paste ลง repository

4. Commit

Example:

```bash
git add <file>

git commit -m "docs: add sprint document"

git push
```

---

# 16. Handoff Summary

Sprint 1 Agent Runtime Foundation สำเร็จแล้ว

Current OneMind Platform:

```
                 OneMind Platform

                      |
                      v

              API Gateway :8000

                      |
                      v

             Planner Runtime :8001

                      |
                      v

              Agent Runtime :8002

                      |
                      v

              Future AI Agents
```

Platform พร้อมเข้าสู่ขั้นตอน:

> Building the first real autonomous agent.


---

END OF DOCUMENT