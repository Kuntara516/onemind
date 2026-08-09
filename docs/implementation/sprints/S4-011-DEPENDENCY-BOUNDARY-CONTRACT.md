# OneMind — S4-011 Dependency Boundary Contract

## Status

**Sprint:** S4-011 — Decision Boundary
**Phase:** Dependency Boundary / Composition
**Status:** Design Contract
**Repository:** `Kuntara516/onemind`
**Branch:** `feature/sprint4-context-intelligence`

---

## 1. Purpose

This contract defines the dependency boundaries between:

* Context Runtime
* Agent Runtime
* Task Lifecycle
* Executor
* Agent Invocation
* Application Composition

The purpose is to integrate Context Runtime into Agent Runtime execution **without changing the Sprint 2 execution contract**.

This document is authoritative for the implementation of:

1. `ContextRuntimeFactory`
2. optional Context Runtime integration in `ExecutionService`
3. application composition in `app/main.py`

---

## 2. Architectural Invariants

The following invariants MUST remain true.

### 2.1 Sprint 2 Execution Contract Is Frozen

The existing execution chain remains:

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

Context Runtime MUST NOT replace or restructure this chain.

---

### 2.2 Executor Is a Frozen Boundary

`app/executor/executor.py` MUST NOT acquire a dependency on:

* `ContextRuntimeCoordinator`
* `ContextRuntimeIntegration`
* `ContextRuntimeFactory`
* `ContextRuntimeDecisionBoundary`
* `ContextRuntimeDecisionController`
* Context Retriever
* Context Ranker
* Context Selector
* Context Assembler

The Executor continues to receive an already-created `AgentContext`.

Existing contract remains:

```python
await executor.execute(
    task,
    agent_invoker,
    context,
    trace,
)
```

---

### 2.3 TaskManager Is a Frozen Boundary

`app/manager/task_manager.py` MUST remain responsible for:

* task registration
* task submission
* task lifecycle coordination
* delegating execution to Executor
* task tracking

TaskManager MUST NOT construct Context Runtime dependencies.

TaskManager MUST NOT know how Context Runtime is assembled.

---

### 2.4 ExecutionService Owns Integration

`app/runtime/execution.py` is the integration point between:

```text
AgentTask
    |
    v
AgentContext
    |
    v
Context Runtime
    |
    v
TaskManager
```

ExecutionService MAY receive an optional Context Runtime integration dependency.

ExecutionService MUST NOT construct individual Context Runtime components.

---

## 3. Composition Root

`app/main.py` remains the application composition root.

It is responsible for constructing runtime dependencies and injecting them into services.

The intended composition is:

```text
main.py
   |
   +-- AgentRegistry
   +-- CapabilityManager
   +-- AgentInvoker
   +-- TraceRecorder
   +-- Executor
   +-- TaskManager
   |
   +-- ContextRuntimeFactory
   |       |
   |       +-- Retriever
   |       +-- Ranker
   |       +-- Selector
   |       +-- Assembler
   |       +-- Observability Runtime
   |       |
   |       +-- ContextRuntimeIntegration
   |
   +-- ExecutionService
```

`main.py` MAY construct the Context Runtime through the factory.

---

## 4. ContextRuntimeFactory Boundary

The factory SHALL be located at:

```text
app/context_runtime/factory.py
```

Its responsibility is dependency construction only.

The factory SHALL construct:

```text
ContextRetriever
ContextRanker
ContextSelector
ContextAssembler
ContextRuntimeObservabilityRuntime
ContextRuntimeIntegration
```

The factory MUST NOT:

* execute an AgentTask
* create an AgentTask
* invoke an Agent
* execute a capability
* perform a runtime decision
* evaluate context quality
* apply a runtime decision
* mutate AgentContext
* own request/task lifecycle

The factory is a **composition mechanism**, not a runtime service.

---

## 5. Context Runtime Dependency Graph

The Context Runtime dependency graph SHALL remain:

```text
ContextRuntimeFactory
        |
        v
ContextRuntimeIntegration
        |
        +-------------------+
        |                   |
        v                   v
    Retriever           Observability
        |
        v
      Ranker
        |
        v
     Selector
        |
        v
     Assembler
```

Context Runtime components SHALL be injected into `ContextRuntimeIntegration`.

`ContextRuntimeIntegration` owns pipeline execution.

The factory owns construction.

---

## 6. AgentContext Boundary

`AgentContext` is the carrier between Context Runtime and Agent Runtime.

The integration path is:

```text
AgentTask
    |
    v
ExecutionService
    |
    v
AgentContext
    |
    v
ContextRuntimeIntegration
    |
    v
AgentContext.metadata
```

Context Runtime MAY enrich `AgentContext` with:

```text
assembled_context
context_runtime
```

The Agent Runtime execution chain then continues using the same `AgentContext`.

Agents MUST NOT be required to import Context Runtime implementation classes.

---

## 7. ExecutionService Integration Contract

ExecutionService MAY accept:

```python
context_runtime=None
```

or an equivalent optional abstraction.

When Context Runtime is not provided:

```text
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
```

This path MUST preserve existing Sprint 2 behavior.

When Context Runtime is provided:

```text
ExecutionService
      |
      v
AgentContext
      |
      v
ContextRuntimeIntegration
      |
      v
AgentContext enriched
      |
      v
TaskManager
      |
      v
Executor
```

The Executor contract remains unchanged in both cases.

---

## 8. Context Runtime Is Optional at the Execution Boundary

Context Runtime integration MUST be additive.

The following behavior is required:

### Context Runtime disabled

```text
context_runtime = None
```

Execution proceeds using the existing AgentContext.

No Context Runtime components are constructed by ExecutionService.

---

### Context Runtime enabled

```text
context_runtime != None
```

ExecutionService invokes the integration boundary to build/enrich runtime context before delegating execution.

The resulting `AgentContext` is passed through the existing TaskManager → Executor chain.

---

## 9. Decision Boundary Separation

The decision path is separate from context assembly.

```text
Evaluation
    |
    v
Feedback
    |
    v
DecisionBoundary
    |
    v
Decision Artifact
    |
    v
DecisionController
    |
    v
RefreshEngine
```

The decision path MUST NOT be embedded into:

* `Executor`
* `TaskManager`
* `ContextRuntimeFactory`
* `ContextRuntimeIntegration.build_context()`

The `ContextRuntimeDecisionController` remains responsible only for applying an explicit execution artifact.

---

## 10. Decision Controller Boundary

`ContextRuntimeDecisionController` SHALL continue to:

* preserve `evaluation_id`
* preserve execution action
* treat `RETAIN` as a no-op
* treat `REVIEW` as a no-op
* delegate `REFRESH` to `ContextRefreshEngine`
* report whether refresh was applied

It SHALL NOT:

* evaluate context
* produce a decision
* retrieve context
* rank context
* select context
* assemble context
* execute an AgentTask

---

## 11. Identity Contract

The following identities remain distinct:

```text
task_id
    |
    +-- identifies AgentTask execution

execution_id
    |
    +-- identifies runtime/context pipeline execution
       where currently derived from task identity

evaluation_id
    |
    +-- identifies context evaluation artifact

trace_id
    |
    +-- identifies observability trace
```

No factory or composition layer may silently replace one identity with another.

Existing `task.task_id` remains the authoritative AgentTask identity.

`evaluation_id` remains owned by the evaluation subsystem.

`trace_id` remains owned by observability.

---

## 12. Forbidden Dependency Direction

The following dependency directions are forbidden:

```text
Executor
    -> ContextRuntime
```

```text
TaskManager
    -> ContextRuntimeFactory
```

```text
Agent
    -> ContextRuntimeFactory
```

```text
Agent
    -> ContextRuntimeIntegration
```

```text
ContextRuntimeFactory
    -> AgentInvoker
```

```text
ContextRuntimeFactory
    -> TaskManager
```

```text
ContextRuntimeFactory
    -> Executor
```

The factory must remain below the application composition root and independent of the execution orchestration chain.

---

## 13. Required Dependency Direction

The allowed direction is:

```text
main.py
   |
   +--------------------------+
   |                          |
   v                          v
ContextRuntimeFactory     Agent Runtime
   |                          |
   v                          v
ContextRuntimeIntegration  ExecutionService
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

Context Runtime communicates with Agent Runtime through the explicit integration boundary and `AgentContext`.

---

## 14. Backward Compatibility Requirement

Existing Sprint 2 tests MUST continue to pass without modification to their architectural contract.

In particular:

```text
tests/test_execution_pipeline.py
tests/test_executor.py
tests/test_task_manager.py
```

must continue to validate the existing execution chain.

The implementation MUST NOT require existing callers to construct Context Runtime components manually.

---

## 15. Factory API Contract

The initial factory API SHOULD remain minimal.

Target shape:

```python
class ContextRuntimeFactory:

    @staticmethod
    def create() -> ContextRuntimeIntegration:
        ...
```

The factory should expose a single composition operation.

Individual component construction should remain an implementation detail unless a later architectural requirement explicitly requires configurable providers.

---

## 16. Implementation Sequence

The implementation SHALL proceed in this order:

### Step 1 — Contract

Create and freeze this dependency-boundary contract.

### Step 2 — Factory

Create:

```text
app/context_runtime/factory.py
```

Implement:

```python
ContextRuntimeFactory.create()
```

### Step 3 — Factory Tests

Verify:

* integration object is created
* required pipeline components are wired
* observability dependency is present
* factory does not execute runtime behavior

### Step 4 — ExecutionService Integration

Add optional Context Runtime integration to:

```text
app/runtime/execution.py
```

Do not modify:

```text
app/manager/task_manager.py
app/executor/executor.py
```

### Step 5 — Composition Root

Wire the factory from:

```text
app/main.py
```

### Step 6 — Regression

Run the existing Sprint 2 execution tests plus S4-011 tests.

---

## 17. Acceptance Criteria

This boundary is considered correctly implemented only when all conditions are true:

* [ ] `ContextRuntimeFactory` exists under `app/context_runtime/`
* [ ] Factory constructs `ContextRuntimeIntegration`
* [ ] Factory does not execute runtime behavior
* [ ] `ExecutionService` is the Context Runtime integration point
* [ ] Context Runtime is optional at the ExecutionService boundary
* [ ] `TaskManager` remains unchanged
* [ ] `Executor` remains unchanged
* [ ] `AgentInvoker` remains unchanged
* [ ] `AgentContext` remains the runtime context carrier
* [ ] Decision Boundary remains separate from context assembly
* [ ] Decision Controller remains separate from execution orchestration
* [ ] Existing Sprint 2 execution tests continue to pass
* [ ] No Context Runtime dependency is introduced into Executor
* [ ] No Context Runtime dependency is introduced into TaskManager
* [ ] Top-level repository structure remains unchanged

---

## 18. Final Boundary Contract

The architectural rule for S4-011 is:

> **Context Runtime is composed at the application boundary, integrated by ExecutionService, carried through AgentContext, and consumed by the existing Sprint 2 execution chain without modifying TaskManager or Executor contracts.**

Therefore:

```text
Composition
    = main.py

Construction
    = ContextRuntimeFactory

Context Pipeline
    = ContextRuntimeIntegration

Execution Integration
    = ExecutionService

Task Lifecycle
    = TaskManager

Execution
    = Executor

Agent Invocation
    = AgentInvoker

Runtime Context Carrier
    = AgentContext

Decision Production
    = ContextRuntimeDecisionBoundary

Decision Application
    = ContextRuntimeDecisionController
```

This contract is the prerequisite for implementing `ContextRuntimeFactory`.
