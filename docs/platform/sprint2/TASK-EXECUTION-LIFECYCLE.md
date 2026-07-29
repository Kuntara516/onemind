# OneMind Task Execution Lifecycle Design

**Document ID:** OM-PLAT-S2-003
**Milestone:** M6 Platform Engineering
**Sprint:** Sprint 2 — Agent Execution Engine
**Task:** S2-002 — Task Execution Lifecycle
**Version:** 1.0
**Status:** DESIGN
**Date:** 2026-07-28

---

## 1. Overview

This document defines the Task Execution Lifecycle design for OneMind Sprint 2 — Agent Execution Engine.

Sprint 1 established the foundation of the OneMind Agent Runtime:

- Agent Runtime foundation
- Agent execution context
- Request identity tracking
- Execution metadata
- Capability Registry
- Capability Manager
- Runtime integration with Capability Manager

Sprint 2 S2-001 introduced the execution object: `AgentTask`.

The AgentTask Model defines the structure of a unit of work.

This document defines how an `AgentTask` moves through its execution lifecycle inside the OneMind Agent Runtime.

The Task Execution Lifecycle provides the execution coordination contract between:

- Agent Runtime
- Task Manager
- Executor
- Capability Manager
- Capability implementations

---

## 2. Purpose

The purpose of the Task Execution Lifecycle is to define:

- Task state management
- Execution coordination
- Lifecycle transition rules
- Runtime responsibility boundaries
- Executor interaction model
- Failure handling foundation

The lifecycle ensures that task execution is predictable, observable, and extensible.

---

## 3. Relationship with AgentTask Model

S2-001 created the `AgentTask` execution object. S2-002 defines how that object behaves during execution.

```text
S2-001
AgentTask Model
Defines:
  - task structure
  - execution data
  - lifecycle state field
        |
        v
S2-002
Task Execution Lifecycle
Defines:
  - state transition
  - execution flow
  - runtime behavior
```

---

## 4. Design Principles

OneMind separates execution responsibilities between Agent, Runtime, and Capability.

### Agent

Responsible for:

- Deciding execution intent
- Creating execution request
- Defining required capabilities

Agent does **not** manage execution lifecycle.

### Task Manager

Responsible for:

- Receiving `AgentTask`
- Managing task state
- Coordinating execution lifecycle
- Tracking task progress

Task Manager does **not** execute business actions.

### Executor

Responsible for:

- Executing assigned task
- Resolving required capabilities
- Collecting execution results

Executor does **not** own task lifecycle decisions.

### Capability Manager

Responsible for:

- Capability discovery
- Capability resolution
- Providing executable capabilities

Capability Manager does **not** manage task state.

---

## 5. Execution Architecture

Task execution flow:

```text
User Request
    |
    v
Agent
    |
    v
AgentTask
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

## 6. Task Lifecycle State Model

The lifecycle extends the `AgentTask` status model from S2-001.

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

## 7. Lifecycle State Definition

### CREATED

Initial state after `AgentTask` creation.

Meaning:

- Task object exists
- Task has not entered execution pipeline

Allowed transition:

- `CREATED -> QUEUED`

### QUEUED

Task is accepted by Task Manager and waiting for execution.

Meaning:

- Task validated
- Execution resources not yet allocated

Allowed transition:

- `QUEUED -> RUNNING`

### RUNNING

Task execution is in progress.

Meaning:

- Executor has started processing
- Capability execution may occur

Allowed transitions:

- `RUNNING -> COMPLETED`
- `RUNNING -> FAILED`

### COMPLETED

Execution finished successfully.

Meaning:

- Result collected
- Task lifecycle completed

**Final state.** No further transitions.

### FAILED

Execution failed.

Meaning:

- Execution error occurred
- Result contains failure information

**Final state.** No further transitions.

---

## 8. State Transition Rules

| Current State | Next State | Allowed |
|----------------|------------|---------|
| CREATED        | QUEUED     | Yes     |
| QUEUED         | RUNNING    | Yes     |
| RUNNING        | COMPLETED  | Yes     |
| RUNNING        | FAILED     | Yes     |
| COMPLETED      | Any        | No      |
| FAILED         | Any        | No      |

---

## 9. Task Manager Responsibility

Task Manager owns:

- Task acceptance
- Lifecycle transition
- Execution coordination
- Status update
- Completion tracking

Task Manager does **not** own:

- Business decisions
- Capability implementation
- Reasoning logic

---

## 10. Executor Responsibility

Executor receives: `AgentTask`

Execution sequence:

```text
Receive Task
      |
      v
Validate Task
      |
      v
Update Status (QUEUED -> RUNNING)
      |
      v
Resolve Capability
      |
      v
Execute Capability
      |
      v
Collect Result
      |
      v
Update Task (RUNNING -> COMPLETED or RUNNING -> FAILED)
```

---

## 11. Execution Error Handling

The lifecycle supports controlled failure handling.

Failure sources:

- Invalid task input
- Missing capability
- Capability execution error
- Runtime exception

Failure behavior:

```text
RUNNING
    |
    v
FAILED
```

Failure information should be stored in `AgentTask.result`.

Example:

```json
{
  "error": "capability_not_found",
  "message": "Required capability unavailable"
}
```

---

## 12. Runtime Integration

Task Execution Lifecycle integrates with existing Sprint 1 components.

```text
Agent Runtime
    |
    v
Execution Context
    |
    v
Task Manager
    |
    v
AgentTask
    |
    v
Executor
    |
    v
Capability Manager
```

The lifecycle uses:

- Agent Execution Context
- Capability Manager
- Runtime execution metadata

---

## 13. Implementation Scope

S2-002 includes:

- Task lifecycle management design
- Task state transition rules
- Task Manager foundation
- Executor interaction contract
- Lifecycle validation

---

## 14. Out of Scope

S2-002 does **not** include:

- Database persistence
- Distributed queue
- Message broker
- Worker process
- Retry engine
- Scheduling system
- Workflow orchestration
- Distributed tracing implementation

---

## 15. Expected Code Structure

Implementation target:

```text
services/
└── agent-runtime/
    └── app/
        ├── tasks/
        │   ├── models.py
        │   ├── status.py
        │   └── lifecycle.py
        ├── executor/
        │   └── executor.py
        └── manager/
            └── task_manager.py
```

---

## 16. Acceptance Criteria

S2-002 is completed when:

- Task lifecycle rules are implemented
- Task state transition validation exists
- Task Manager foundation exists
- Executor interaction contract exists
- Lifecycle unit tests pass
- Sprint 1 and S2-001 functionality remain stable

---

## 17. Future Extension Points

The Task Execution Lifecycle should support future extensions:

- Persistent task storage
- Task priority
- Retry policy
- Distributed execution
- Workflow orchestration
- Execution tracing
- Human approval workflow
- Memory integration

These are outside the scope of S2-002.

---

## 18. Design Status

This document defines the design contract for **S2-002 — Task Execution Lifecycle**.

Implementation may proceed after design approval.

**Document Status:** DESIGN

**Next Step:** Implement Task Execution Lifecycle Foundation