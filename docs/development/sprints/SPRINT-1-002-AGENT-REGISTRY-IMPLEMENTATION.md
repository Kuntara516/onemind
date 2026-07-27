# SPRINT-1-002-AGENT-REGISTRY-IMPLEMENTATION.md

**Project:** OneMind  
**Milestone:** Sprint 1 — Agent Runtime Foundation  
**Sprint Task:** S1-002 Agent Registry Implementation  
**Status:** Planned  
**Branch:** feature/sprint1-agent-runtime  
**Date:** 2026-07-27  

---

# 1. Objective

หลังจาก Sprint 1-001 สำเร็จ:

- Agent Runtime Service ทำงานได้
- FastAPI Endpoint พร้อม
- Runtime Layer ถูกสร้าง
- Execute API พร้อมรับ request

แต่ระบบยังไม่มี "Agent จริง"

Sprint นี้มีเป้าหมาย:

> Build the first Agent Registry system that allows OneMind Runtime to discover and execute agents dynamically.

---

# 2. Current Limitation

Current:

```
POST /execute

{
 "agent":"example",
 "task":{}
}
```

Runtime ยังไม่สามารถ:

- รู้ว่า agent มีอยู่หรือไม่
- โหลด agent
- ตรวจสอบ capability
- dispatch execution


---

# 3. Target Architecture


Before:

```
Request

   |
   v

Runtime

   |
   v

Hardcoded execution
```


After:

```
                 Request
                    |
                    v
              Agent Runtime
                    |
                    v
             Agent Registry
                    |
          +---------+---------+
          |                   |
          v                   v

    Agent Metadata       Agent Instance


                    |
                    v

              Agent Execute()

                    |
                    v

                Result
```

---

# 4. Implementation Scope


## Add Agent Interface

Create:

```
services/agent-runtime/app/agents/base.py
```


Purpose:

Define common contract for all agents.



## Add First Agent

Create:

```
services/agent-runtime/app/agents/echo_agent.py
```


Purpose:

First executable agent.

Capability:

Receive message

Return response.



## Upgrade Registry

Modify:

```
services/agent-runtime/app/registry.py
```


Add:

- register()
- get()
- list_agents()


## Upgrade Runtime

Modify:

```
services/agent-runtime/app/runtime.py
```


Flow:

```
execute()

    |

registry.get(agent)

    |

agent.execute(task)

    |

return result
```

---

# 5. Agent Interface Design


File:

```
agents/base.py
```


Expected:


```python
from abc import ABC, abstractmethod


class BaseAgent(ABC):

    name: str
    description: str


    @abstractmethod
    async def execute(self, task: dict):
        pass
```


---

# 6. Echo Agent


File:

```
agents/echo_agent.py
```


Example:


```python
from app.agents.base import BaseAgent


class EchoAgent(BaseAgent):

    name = "echo-agent"

    description = "Simple echo agent"


    async def execute(self, task):

        return {
            "agent": self.name,
            "message": task.get("message")
        }
```


---

# 7. Registry Design


Registry responsibility:


```
Agent Registry

- Store agents
- Find agents
- List agents
```


Example:


```python
registry.register(
    EchoAgent()
)


registry.get(
    "echo-agent"
)
```


---

# 8. API Result


## GET /agents


Before:


```json
{
 "agents":[]
}
```


After:


```json
{
 "agents":[
    {
      "name":"echo-agent",
      "description":"Simple echo agent"
    }
 ]
}
```


---

# 9. Execute Flow


Request:


```json
{
 "agent":"echo-agent",
 "task":{
    "message":"Hello OneMind"
 }
}
```


Processing:


```
API

 |
 v

Agent Runtime

 |
 v

Registry

 |
 v

Echo Agent

 |
 v

Response
```


Response:


```json
{
 "agent":"echo-agent",
 "message":"Hello OneMind"
}
```


---

# 10. Testing


## Check service


```bash
docker compose -f docker/compose/docker-compose.yml ps
```


Expected:

```
agent-runtime

Up
```


---

## Check agents


Command:


```bash
curl http://localhost:8002/agents
```


Expected:


```json
{
 "agents":[
    "echo-agent"
 ]
}
```


---

## Execute Agent


Command:


```bash
curl -X POST http://localhost:8002/execute \
-H "Content-Type: application/json" \
-d '
{
 "agent":"echo-agent",
 "task":{
   "message":"Hello OneMind"
 }
}'
```


Expected:


```json
{
 "agent":"echo-agent",
 "message":"Hello OneMind"
}
```

---

# 11. Definition of Done


[x] Agent interface created

[x] Echo agent created

[x] Registry supports registration

[x] Registry supports lookup

[x] Runtime executes registered agent

[x] /agents returns available agents

[x] /execute executes real agent


---

# 12. Git Workflow


After implementation:


```bash
git status
```


Review changes:


```bash
git diff
```


Commit:


```bash
git add services/agent-runtime

git commit -m "feat: implement agent registry and first agent"

git push
```


---

# 13. Next Sprint


After completion:

## S1-003 Planner to Agent Runtime Integration


Goal:


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

# END OF DOCUMENTcs