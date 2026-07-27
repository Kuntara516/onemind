# SPRINT-1-003-AGENT-CONTEXT-LIFECYCLE.md

Document ID: OM-SPRINT-1-003
Version: 1.0.0
Status: Planned
Milestone: M6 Platform Engineering
Sprint: Sprint 1 — Agent Runtime Foundation
Branch: feature/sprint1-agent-runtime

---

# 1. Sprint Overview

## Sprint Name

Agent Context & Execution Lifecycle

## Objective

พัฒนา OneMind Agent Runtime จาก Execution Engine พื้นฐาน ให้รองรับ Runtime Context ซึ่งเป็นรากฐานสำคัญสำหรับ Multi-Agent Architecture ในอนาคต

หลังจาก Sprint 1-002 ระบบสามารถ:

* Register Agent
* Discover Agent
* Execute Agent Task
* Return Execution Result

Sprint นี้เพิ่มความสามารถ:

* สร้าง Agent Context ระหว่าง Execution
* ส่ง Context เข้า Agent
* เก็บ Runtime Metadata
* เตรียมโครงสร้างสำหรับ Memory, Knowledge, Tools และ Execution Trace

---

# 2. Current Architecture (Before)

Current Flow:

```
Client Request

      |
      v

Agent Runtime

      |
      v

Agent Registry

      |
      v

Agent Execute

      |
      v

Result
```

Current Execution Contract:

```python
agent.execute(task)
```

ข้อจำกัด:

* Agent ไม่รู้ Request Identity
* Agent ไม่รู้ Session Information
* Agent ไม่มี User Context
* Agent ไม่มี Runtime Metadata
* ไม่สามารถต่อยอด Memory / Knowledge / Tool Integration ได้

---

# 3. Target Architecture (After)

Target Flow:

```
Client Request

      |
      v

Agent Runtime

      |
      |-- Create Agent Context

      v

Agent Registry

      |
      v

Agent Execute

      |
      v

Result + Context Metadata
```

Execution Contract ใหม่:

```python
agent.execute(
    task,
    context
)
```

---

# 4. Sprint Goals

## Goal 1 — Introduce Agent Context

สร้าง Object สำหรับเก็บ Runtime State ระหว่าง Agent Execution

รองรับ:

* request_id
* session_id
* user_id
* metadata

ตัวอย่าง:

```json
{
    "request_id": "uuid",
    "session_id": null,
    "user_id": null,
    "metadata": {}
}
```

---

## Goal 2 — Upgrade Agent Interface

เปลี่ยน Agent Contract

จาก:

```python
async def execute(
    self,
    task: dict
) -> dict:
```

เป็น:

```python
async def execute(
    self,
    task: dict,
    context
) -> dict:
```

เหตุผล:

Agent ทุกตัวใน OneMind ต้องสามารถเข้าถึง Runtime Context ได้

---

## Goal 3 — Runtime Context Injection

AgentRuntime รับผิดชอบ:

* สร้าง Context
* Inject Context เข้า Agent
* ควบคุม Execution Lifecycle

Agent ไม่ควรสร้าง Context เอง

---

## Goal 4 — Execution Metadata

ทุก Agent Execution ต้องสามารถติดตามได้

Response ต้องรองรับ:

```json
{
    "status": "completed",
    "agent": "demo-agent",
    "request_id": "uuid",
    "result": {}
}
```

---

# 5. Architecture Change

## Before

```
Request

 |

 v

Agent Runtime

 |

 v

Agent Registry

 |

 v

Agent Execute

 |

 v

Result
```

## After

```
Request

 |

 v

Agent Runtime

 |

 +----------------+
 | Create Context |
 +----------------+

 |

 v

Agent Registry

 |

 v

Agent Execute

 |

 v

Result + Context Metadata
```

---

# 6. Implementation Scope

## 6.1 AgentContext

File:

```
services/agent-runtime/app/agents/context.py
```

หน้าที่:

เก็บ execution state ของ Agent

Implementation:

```python
class AgentContext:

    def __init__(
        self,
        request_id,
        session_id=None,
        user_id=None,
        metadata=None
    ):
        self.request_id = request_id
        self.session_id = session_id
        self.user_id = user_id
        self.metadata = metadata or {}
```

---

## 6.2 Update BaseAgent Interface

File:

```
services/agent-runtime/app/agents/base.py
```

เปลี่ยน Interface:

จาก:

```python
async def execute(
    self,
    task: dict
) -> dict:
```

เป็น:

```python
async def execute(
    self,
    task: dict,
    context
) -> dict:
```

ทุก Agent ในอนาคตต้อง implement contract นี้

---

## 6.3 Update AgentRuntime

File:

```
services/agent-runtime/app/runtime.py
```

เพิ่ม Context Lifecycle:

```python
context = AgentContext(
    request_id=request_id
)

result = await agent.execute(
    task,
    context
)
```

Runtime รับผิดชอบ:

* Generate Execution Context
* Resolve Agent
* Execute Agent
* Collect Result
* Return Metadata

---

## 6.4 Update DemoAgent

File:

```
services/agent-runtime/app/agents/demo_agent.py
```

เปลี่ยน:

```python
execute(task)
```

เป็น:

```python
execute(
    task,
    context
)
```

DemoAgent ต้องสามารถเข้าถึง:

```python
context.request_id
```

ตัวอย่าง Result:

```json
{
    "message": "OneMind received: hello",
    "request_id": "uuid"
}
```

---

# 7. Execution Lifecycle

```
1. Receive Request

        |

        v

2. Validate Agent Task

        |

        v

3. Generate Request ID

        |

        v

4. Create Agent Context

        |

        v

5. Resolve Agent From Registry

        |

        v

6. Execute Agent

        |

        v

7. Collect Result

        |

        v

8. Return Response
```

---

# 8. API Contract

Endpoint:

```
POST /execute
```

Request:

```json
{
    "agent": "demo-agent",
    "task": {
        "message": "hello OneMind"
    }
}
```

Response:

```json
{
    "status": "completed",
    "agent": "demo-agent",
    "request_id": "uuid",
    "context": {
        "session_id": null
    },
    "result": {
        "message": "OneMind received"
    }
}
```

---

# 9. File Change Scope

```
services/agent-runtime/app/

├── runtime.py
├── models.py
├── registry.py
│
└── agents/
    ├── base.py
    ├── context.py
    └── demo_agent.py
```

---

# 10. Testing Plan

## Health Check

Command:

```bash
curl http://localhost:8002/health
```

Expected:

```json
{
    "status":"ok",
    "service":"agent-runtime"
}
```

---

## Agent Discovery

Command:

```bash
curl http://localhost:8002/agents
```

Expected:

```json
{
    "agents":[
        "demo-agent"
    ]
}
```

---

## Agent Execution

Command:

```bash
curl -X POST http://localhost:8002/execute \
-H "Content-Type: application/json" \
-d '
{
 "agent":"demo-agent",
 "task":{
   "message":"hello OneMind"
 }
}
'
```

Expected:

```json
{
    "status":"completed",
    "agent":"demo-agent",
    "request_id":"uuid"
}
```

---

# 11. Definition of Done

Sprint 1-003 Completed เมื่อ:

* AgentContext implemented
* BaseAgent contract updated
* AgentRuntime creates Context
* AgentRuntime injects Context
* DemoAgent accepts Context
* Execution response contains metadata
* Docker runtime starts successfully
* Execute API test passes

---

# 12. Engineering Principles

## Runtime Owns Lifecycle

Agent Runtime เป็นผู้ควบคุม:

* Context Creation
* Execution Flow
* Metadata Collection

Agent มีหน้าที่:

* Execute Task
* Apply Agent Logic

---

## Extensible Context

AgentContext เป็น Foundation สำหรับ:

```
AgentContext

 |

 +-- Request Identity

 +-- Session State

 +-- User Profile

 +-- Memory Reference

 +-- Knowledge Reference

 +-- Tool Context

 +-- Execution Trace
```

---

# 13. Future Extension

## Memory Integration

```
Agent

 |

AgentContext

 |

Memory Service
```

---

## Tool Integration

```
Agent

 |

Capability Layer

 |

Tools
```

---

## Multi-Agent Collaboration

```
Agent Runtime

 |

 +-- Agent A

 |

 +-- Agent B

 |

Shared Context
```

---

# 14. Next Sprint

SPRINT-1-004 Agent Capability & Tool Interface

Objective:

สร้าง Capability Layer สำหรับ Agent

รองรับ:

* Internal Tools
* External API
* Knowledge Services
* Future MCP Integration

Architecture:

```
Agent

 |

Capability Interface

 |

+----------------+
| Tools          |
| Knowledge      |
| Memory         |
+----------------+
```

---

End of Document
