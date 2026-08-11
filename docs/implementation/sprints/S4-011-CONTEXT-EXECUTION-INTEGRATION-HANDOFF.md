# OneMind — Session Handoff

## S4-011 Context → Execution Integration — Implementation

### Repository

* Project: `OneMind`
* Repo: `Kuntara516/onemind`
* Branch: `feature/sprint4-context-intelligence`
* Working tree: **clean**
* HEAD: `c82cdd6`
* Latest commit: `docs: close context execution integration boundary`

### Frozen Architectural Baseline

ADR:

`docs/implementation/sprints/S4-011-CONTEXT-EXECUTION-INTEGRATION-DECISION.md`

Status:

**ARCHITECTURAL DECISION — BOUNDARY CLOSED**

Do not redesign or reopen this boundary unless new code evidence proves the decision invalid.

---

## Proven Current Architecture

### Context Runtime

```text
ContextRuntimeFactory
        |
        v
ContextRuntimeIntegration
        |
        v
build_context(...)
        |
        +--> Retrieval
        +--> Ranking
        +--> Selection
        +--> Assembly
        +--> Evaluation / Decision / Refresh
        +--> Observability
        |
        v
AgentContext
    +--> assembled_context
    +--> context_runtime
```

### Agent Execution

```text
ExecutionService
        |
        v
TaskManager
        |
        v
Executor
        |
        v
AgentInvoker
        |
        v
Agent
```

### Current Gap

The two pipelines are **not yet connected**.

There is currently no execution-path call from:

```text
ExecutionService
```

to:

```text
ContextRuntimeIntegration.build_context(...)
```

---

# Frozen Integration Boundary

The target architecture is:

```text
Composition Root
      |
      +--> ContextRuntimeFactory
      |        |
      |        v
      |   ContextRuntimeIntegration
      |
      v
ExecutionService
      |
      v
AgentContext
      |
      v
TaskManager
      |
      v
Executor
      |
      v
AgentInvoker
      |
      v
Agent
```

## Responsibility Rules

### ContextRuntimeFactory

**Composition only.**

Must not:

* execute retrieval
* evaluate context
* make decisions
* refresh context
* invoke agents
* execute tasks

### ExecutionService

**Integration boundary.**

Responsible for connecting:

```text
Context Runtime
        ↓
AgentContext
        ↓
Execution Pipeline
```

### AgentContext

**Transport boundary.**

Context Runtime output is exposed through:

```text
assembled_context
context_runtime
```

### TaskManager

Remains responsible for:

* task registration
* lifecycle
* execution delegation
* task tracking

Must remain Context Runtime agnostic.

### Executor

Remains responsible for execution coordination.

Must remain Context Runtime agnostic.

### AgentInvoker

Remains responsible for:

* agent resolution
* agent invocation
* capability injection
* invocation result

Must remain Context Runtime agnostic.

### Agent

Consumes `AgentContext`.

Must not depend on Context Runtime internals.

### Legacy `app/context`

Remain untouched.

Do not migrate, delete, merge, or replace the legacy context stack as part of this task.

---

# Implementation Objective

Implement only:

```text
ExecutionService
        |
        v
ContextRuntimeIntegration.build_context(
    task,
    agent_context,
)
        |
        v
AgentContext enrichment
        |
        v
existing execution pipeline
```

The Context Runtime already exists.

The Factory already exists.

The Integration already exists.

Do **not** rebuild them.

---

# Required Composition

The preferred construction boundary is:

```text
Composition Root
        |
        +--> ContextRuntimeFactory
        |       |
        |       v
        |   ContextRuntimeIntegration
        |
        +--> ExecutionService
                |
                +--> ContextRuntimeIntegration
```

Do not instantiate:

```python
ContextRuntimeFactory().create()
```

inside every execution call.

---

# First Implementation Step

Before modifying code, inspect the current implementation of:

```text
app/runtime.py
app/main.py
app/context_runtime/factory.py
app/context_runtime/integration.py
```

and tests:

```text
tests/test_execution_pipeline.py
tests/test_context_runtime_factory.py
tests/test_context_runtime_integration.py
```

Then determine the smallest production-code change required to inject:

```text
ContextRuntimeIntegration
```

into:

```text
ExecutionService
```

---

# Required Regression Coverage

At minimum, prove:

### 1. Context Runtime is invoked

```text
ExecutionService.execute()
        ↓
ContextRuntimeIntegration.build_context()
```

### 2. AgentContext is enriched

After context integration:

```text
agent_context.get("assembled_context")
```

must contain the assembled context.

And:

```text
agent_context.get("context_runtime")
```

must contain runtime context information where applicable.

### 3. Agent receives enriched context

The final Agent invocation must receive the same `AgentContext` enriched by Context Runtime.

### 4. Existing execution lifecycle remains valid

Existing tests must continue to prove:

```text
CREATED
  ↓
QUEUED
  ↓
COMPLETED / FAILED
```

### 5. Existing trace behavior remains valid

The existing:

```text
ExecutionTrace
TraceRecorder
```

contract must remain intact.

### 6. Factory remains composition-only

Existing factory tests must continue to pass.

---

# Non-Goals

Do **not**:

* redesign `ContextRuntimeIntegration`
* redesign `ContextRuntimeFactory`
* redesign Context Runtime evaluation
* redesign Decision Boundary
* redesign Refresh Control
* modify TaskManager responsibility
* modify Executor responsibility
* modify AgentInvoker responsibility
* modify Agent interface unnecessarily
* replace `AgentContext`
* introduce another context abstraction
* migrate `app/context`
* delete `ContextService`
* merge `app/context` with `app/context_runtime`
* implement S4-011-007
* introduce unrelated refactoring

---

# Acceptance Boundary

Implementation is complete only when:

```text
POST /execute
      |
      v
ExecutionService
      |
      v
ContextRuntimeIntegration
      |
      v
AgentContext
      |
      v
TaskManager
      |
      v
Executor
      |
      v
AgentInvoker
      |
      v
Agent
```

is proven by executable tests.

The proof must demonstrate that the Context Runtime output reaches the Agent through the existing `AgentContext` contract without moving Context Runtime responsibility into downstream execution components.

---

# Git Discipline

The architectural decision is already committed:

```text
c82cdd6
docs: close context execution integration boundary
```

Do not amend or rewrite that commit.

Implementation changes should be committed separately after tests pass.

Recommended implementation commit style:

```text
feat: integrate context runtime with execution pipeline
```

Documentation and implementation should remain separate commits.

---

# Session Start Command

First inspect the frozen baseline:

```bash
git status
git branch --show-current
git log --oneline -5
git show --no-patch --oneline c82cdd6
```

Then inspect the execution/context integration boundary before changing anything.

---

# Final Session Directive

**Start implementation from code evidence.**

Do not assume the architecture is implemented merely because the ADR describes it.

Inspect first.

Change the smallest possible production surface.

Add regression tests.

Run the relevant test suite.

Then run the full regression suite.

Commit implementation separately.

The architectural boundary established by `c82cdd6` remains frozen throughout this session.
