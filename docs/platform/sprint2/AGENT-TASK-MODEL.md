# OneMind Agent Task Model Design

**Document ID:** OM-PLAT-S2-002
**Milestone:** M6 Platform Engineering
**Sprint:** Sprint 2 — Agent Execution Engine
**Task:** S2-001 — Create Agent Task Model
**Version:** 1.0
**Status:** DESIGN
**Date:** 2026-07-28

---

# 1. Overview

This document defines the Agent Task Model design for OneMind Sprint 2 — Agent Execution Engine.

Sprint 1 established the foundation of the OneMind Agent Runtime:

* Agent Runtime foundation
* Agent Execution Context
* Request identity tracking
* Execution metadata
* Capability Registry
* Capability Manager
* Runtime integration with Capability Manager

Sprint 2 introduces the execution object that represents a unit of work assigned to an Agent Runtime:

```text
Agent Task
```

The Agent Task Model defines how execution requests are represented, tracked, processed, and completed within the OneMind execution platform.

---

# 2. Purpose

The purpose of the Agent Task Model is to establish a standard execution contract between:

* Agent Runtime
* Task Manager
* Executor
* Capability Manager
* Capability implementations

The model provides:

* unique task identity
* agent ownership
* execution intent
* input payload
* capability requirements
* execution context
* lifecycle state
* execution result

---

# 3. Design Principles

OneMind separates responsibilities between Agent, Runtime, and Capability.

```text
Agent

Decides WHAT needs to happen


Runtime

Controls HOW execution happens


Capability

Provides WHAT actions are possible
```

The Agent Task belongs to the Runtime execution layer.

The Agent Task Model must not contain:

* business logic
* reasoning logic
* capability implementation
* workflow decision logic

---

# 4. Execution Flow

The Agent Task participates in the execution pipeline:

```text
User Request

      |

      v

Agent

      |

      v

Agent Task

      |

      v

Task Manager

      |

      v

Executor

      |

      v

Capability Manager

      |

      v

Capability

      |

      v

Execution Result
```

---

# 5. AgentTask Entity

## Definition

`AgentTask` represents one unit of work executed by the OneMind Agent Runtime.

---

## Entity Structure

```text
AgentTask

├── task_id
├── agent_id
├── intent
├── input
├── required_capabilities
├── execution_context
├── status
├── result
├── created_at
└── completed_at
```

---

# 6. Field Specification

## 6.1 task_id

| Attribute | Value   |
| --------- | ------- |
| Field     | task_id |
| Type      | string  |
| Required  | Yes     |
| Mutable   | No      |

Description:

Unique identifier of the task execution instance.

Example:

```text
task_001
```

---

## 6.2 agent_id

| Attribute | Value    |
| --------- | -------- |
| Field     | agent_id |
| Type      | string   |
| Required  | Yes      |
| Mutable   | No       |

Description:

Identifier of the Agent responsible for execution.

Example:

```text
assistant-agent
```

---

## 6.3 intent

| Attribute | Value  |
| --------- | ------ |
| Field     | intent |
| Type      | string |
| Required  | Yes    |

Description:

Defines the requested execution objective.

Example:

```text
system_health_check
```

---

## 6.4 input

| Attribute | Value  |
| --------- | ------ |
| Field     | input  |
| Type      | object |
| Required  | Yes    |

Description:

Contains input parameters required for execution.

Example:

```json
{
  "service": "agent-runtime"
}
```

---

## 6.5 required_capabilities

| Attribute | Value                 |
| --------- | --------------------- |
| Field     | required_capabilities |
| Type      | array[string]         |
| Required  | No                    |

Description:

Defines capabilities required to complete the task.

Example:

```json
[
  "system.health.check"
]
```

---

## 6.6 execution_context

| Attribute | Value             |
| --------- | ----------------- |
| Field     | execution_context |
| Type      | object            |
| Required  | No                |

Description:

Contains execution metadata propagated through runtime.

Example:

```json
{
  "request_id": "req-001",
  "source": "api-gateway"
}
```

---

## 6.7 status

| Attribute | Value  |
| --------- | ------ |
| Field     | status |
| Type      | enum   |
| Required  | Yes    |

Description:

Current lifecycle state of the task.

Allowed values:

```text
CREATED
QUEUED
RUNNING
COMPLETED
FAILED
```

---

## 6.8 result

| Attribute | Value  |
| --------- | ------ |
| Field     | result |
| Type      | object |
| Required  | No     |

Description:

Stores execution output.

Example:

```json
{
  "status": "healthy"
}
```

---

## 6.9 created_at

| Attribute | Value      |
| --------- | ---------- |
| Field     | created_at |
| Type      | datetime   |
| Required  | Yes        |

Description:

Timestamp when the task was created.

---

## 6.10 completed_at

| Attribute | Value        |
| --------- | ------------ |
| Field     | completed_at |
| Type      | datetime     |
| Required  | No           |

Description:

Timestamp when the task reached a final state.

---

# 7. Task Lifecycle

The Agent Runtime manages task lifecycle.

```text
CREATED

   |

   v

QUEUED

   |

   v

RUNNING

   |

   +----------------+

   |                |

   v                v

COMPLETED        FAILED
```

---

# 8. Lifecycle State Definition

## CREATED

Initial state after task creation.

Meaning:

Task exists but execution has not started.

Transition:

```text
CREATED -> QUEUED
```

---

## QUEUED

Task is waiting for execution.

Transition:

```text
QUEUED -> RUNNING
```

---

## RUNNING

Task is actively executing.

Transitions:

```text
RUNNING -> COMPLETED

RUNNING -> FAILED
```

---

## COMPLETED

Execution completed successfully.

Final state.

---

## FAILED

Execution failed.

Final state.

---

# 9. State Transition Rules

| Current State | Next State | Allowed |
| ------------- | ---------- | ------- |
| CREATED       | QUEUED     | Yes     |
| QUEUED        | RUNNING    | Yes     |
| RUNNING       | COMPLETED  | Yes     |
| RUNNING       | FAILED     | Yes     |
| COMPLETED     | Any        | No      |
| FAILED        | Any        | No      |

---

# 10. Runtime Responsibility

Agent Runtime owns:

* task creation
* lifecycle management
* execution coordination
* result collection
* status tracking

Agent Runtime does not own:

* business decisions
* domain rules
* capability implementation

---

# 11. Executor Interaction

Executor consumes:

```text
AgentTask
```

Execution sequence:

```text
Receive Task

      |

Validate Task

      |

Resolve Capability

      |

Execute Capability

      |

Collect Result

      |

Update Task
```

---

# 12. Serialization Example

```json
{
  "task_id": "task_001",
  "agent_id": "assistant-agent",
  "intent": "system_health_check",
  "input": {},
  "required_capabilities": [
    "system.health.check"
  ],
  "execution_context": {
    "request_id": "req-001",
    "source": "api-gateway"
  },
  "status": "CREATED",
  "result": null,
  "created_at": "2026-07-28T10:00:00Z",
  "completed_at": null
}
```

---

# 13. Implementation Scope

S2-001 includes:

* AgentTask model
* Task status enumeration
* Field validation
* Serialization support
* Unit test foundation

---

# 14. Out of Scope

S2-001 does not include:

* API endpoint
* Task persistence
* Database integration
* Queue system
* Distributed execution
* Workflow engine
* Retry mechanism
* Scheduling system

---

# 15. Expected Code Structure

```text
services/

└── agent-runtime/

    └── app/

        └── tasks/

            ├── __init__.py
            ├── models.py
            └── status.py
```

---

# 16. Acceptance Criteria

S2-001 is completed when:

* [ ] AgentTask model exists
* [ ] Required fields are implemented
* [ ] Status enum exists
* [ ] Lifecycle states are defined
* [ ] Validation rules exist
* [ ] Serialization works
* [ ] Unit tests pass
* [ ] Sprint 1 functionality remains stable

---

# 17. Future Extension Points

The Agent Task Model should support future extensions:

* task persistence
* task priority
* retry policy
* distributed execution
* workflow orchestration
* execution tracing
* memory integration

These are outside the scope of S2-001.

---

# 18. Design Status

This document defines the design contract for:

```text
S2-001 — Create Agent Task Model
```

Implementation may proceed after design approval.

---

**Document Status:** DESIGN

**Next Step:** Implement Agent Task Model
