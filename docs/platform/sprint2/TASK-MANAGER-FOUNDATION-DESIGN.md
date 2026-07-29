# OneMind Task Manager Foundation Design

**Document ID:** OM-PLAT-S2-004
**Milestone:** M6 Platform Engineering
**Sprint:** Sprint 2 — Agent Execution Engine
**Task:** S2-004 — Task Manager Foundation
**Version:** 1.0
**Status:** DESIGN
**Date:** 2026-07-29

---

# 1. Overview

This document defines the Task Manager Foundation design for OneMind Sprint 2 — Agent Execution Engine.

Sprint 1 established the OneMind Agent Runtime foundation:

* Agent Runtime foundation
* Agent Execution Context
* Request identity tracking
* Execution metadata
* Capability Registry
* Capability Manager
* Runtime integration with Capability Manager

Sprint 2 introduced the execution foundation:

* S2-001 AgentTask Model
* S2-002 Task Execution Lifecycle
* S2-003 Executor Foundation

The current execution pipeline supports:

* task representation
* lifecycle validation
* capability execution

This document defines the Task Manager component responsible for coordinating AgentTask execution between:

* Agent Runtime
* Task Lifecycle
* Executor
* Capability Manager

The Task Manager provides the orchestration layer responsible for:

* receiving tasks
* managing task lifecycle
* coordinating execution
* tracking execution state
* returning execution results

---

# 2. Purpose

The purpose of the Task Manager Foundation is to establish the execution coordination contract between:

* Agent Runtime
* AgentTask
* TaskLifecycle
* Executor
* Capability Manager

The Task Manager provides:

* task submission interface
* task execution coordination
* lifecycle state management
* execution result handling
* runtime execution control

The Task Manager does not contain:

* business logic
* agent reasoning logic
* capability implementation
* workflow decision logic

---

# 3. Relationship with Existing Components

S2-001, S2-002, and S2-003 established the execution building blocks.

S2-004 connects these components together.

```text
S2-001

AgentTask Model

Defines:

- task structure
- execution input
- execution context
- task status


        |

        v


S2-002

Task Execution Lifecycle

Defines:

- valid state transition
- lifecycle rules


        |

        v


S2-003

Executor Foundation

Defines:

- capability execution
- execution result


        |

        v


S2-004

Task Manager Foundation

Defines:

- task coordination
- execution orchestration
- status tracking
```

---

# 4. Design Principles

OneMind separates responsibilities between Agent, Task Manager, Executor, and Capability.

## 4.1 Agent

Responsible for:

* understanding user intent
* creating execution request
* defining required capabilities

Agent does not manage:

* task state
* execution lifecycle
* capability execution

---

## 4.2 Task Manager

Responsible for:

* accepting AgentTask
* controlling task lifecycle
* coordinating execution
* tracking execution result

Task Manager does not:

* execute capabilities directly
* implement business rules
* make reasoning decisions

---

## 4.3 Executor

Responsible for:

* executing assigned tasks
* resolving capabilities
* collecting execution results

Executor does not:

* own task submission
* manage external lifecycle state

---

## 4.4 Capability Manager

Responsible for:

* capability discovery
* capability resolution
* providing executable capabilities

Capability Manager does not:

* manage task lifecycle
* coordinate execution flow

---

# 5. Task Manager Position in Architecture

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

TaskManager

    |

    +----------------+

    |                |

    v                v

TaskLifecycle     Executor

                     |

                     v

             CapabilityManager

                     |

                     v

               Capability

                     |

                     v

             Execution Result
```

---

# 6. Task Manager Responsibilities

Task Manager owns:

* task acceptance
* task validation
* task submission
* lifecycle transition coordination
* executor invocation
* execution result collection
* completion tracking

Task Manager does not own:

* business decisions
* agent reasoning
* capability implementation

---

# 7. Task Execution Flow

```text
Receive AgentTask

        |

        v

Validate Task

        |

        v

Submit Task

        |

        v

CREATED -> QUEUED

        |

        v

Invoke Executor

        |

        v

Execute Capability

        |

        v

Collect Result

        |

        v

COMPLETED / FAILED
```

---

# 8. Task Manager Internal Contract

Task Manager provides internal operations:

```text
create_task()

submit_task()

execute_task()

get_task_status()
```

---

# 9. create_task()

Purpose:

Create a new AgentTask execution object.

Input:

```text
AgentTask
```

Output:

```text
AgentTask
```

Responsibilities:

* validate task structure
* initialize execution object
* maintain initial state

Initial state:

```text
CREATED
```

---

# 10. submit_task()

Purpose:

Submit task into execution pipeline.

Input:

```text
AgentTask
```

Output:

```text
AgentTask
```

Responsibilities:

* validate lifecycle transition
* move task into execution queue

State transition:

```text
CREATED -> QUEUED
```

---

# 11. execute_task()

Purpose:

Coordinate execution through Executor.

Input:

```text
AgentTask
```

Output:

```text
AgentTask
```

Responsibilities:

* invoke Executor
* monitor execution result
* update task state

Execution flow:

```text
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

# 12. get_task_status()

Purpose:

Retrieve current task execution state.

Input:

```text
task_id
```

Output:

```text
TaskStatus
```

Responsibilities:

* provide current lifecycle state
* support future monitoring

---

# 13. Error Handling

Task Manager handles execution coordination errors.

Error sources:

* invalid task
* invalid lifecycle transition
* executor failure
* missing capability
* runtime exception

Failure behavior:

```text
RUNNING

   |

   v

FAILED
```

Failure information is stored in:

```text
AgentTask.result
```

Example:

```json
{
  "error": "execution_failed",
  "message": "Executor failed during capability execution"
}
```

---

# 14. Integration with Existing Components

Task Manager integrates with:

* AgentTask
* TaskLifecycle
* Executor
* Capability Manager

Architecture:

```text
TaskManager

    |

    +----------------+

    |                |

    v                v

AgentTask       TaskLifecycle

    |

    v

Executor

    |

    v

CapabilityManager
```

---

# 15. Implementation Scope

S2-004 includes:

* TaskManager class
* task creation flow
* task submission flow
* Executor integration
* lifecycle coordination
* task result handling
* unit tests

---

# 16. Out of Scope

S2-004 does not include:

* database persistence
* distributed queue
* message broker
* worker process
* retry mechanism
* scheduling system
* workflow engine
* distributed tracing

---

# 17. Expected Code Structure

```text
services/

└── agent-runtime/

    └── app/

        ├── manager/

        │   ├── __init__.py
        │   └── task_manager.py

        ├── tasks/

        │   ├── models.py
        │   ├── status.py
        │   └── lifecycle.py

        └── executor/

            ├── __init__.py
            └── executor.py
```

---

# 18. Acceptance Criteria

S2-004 is completed when:

* TaskManager implementation exists
* Task creation flow works
* Task submission flow works
* Executor integration works
* Lifecycle transition is enforced
* Execution result is returned
* Unit tests pass
* Existing Sprint 2 tests remain stable

---

# 19. Future Extension Points

The Task Manager should support future extensions:

* persistent task storage
* task queue backend
* priority scheduling
* retry policy
* distributed workers
* execution monitoring
* workflow orchestration
* human approval workflow
* memory integration

These are outside the scope of S2-004.

---

# 20. Design Status

This document defines the design contract for:

```text
S2-004 — Task Manager Foundation
```

Implementation may proceed after design approval.

Document Status:

```text
DESIGN
```

Next Step:

```text
Implement Task Manager Foundation
```