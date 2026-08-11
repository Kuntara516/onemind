# OneMind — S4-011 Context → Execution Integration Decision

**Document:** `S4-011-CONTEXT-EXECUTION-INTEGRATION-DECISION.md`
**Sprint:** S4-011 Context Intelligence / Decision Boundary
**Status:** **ARCHITECTURAL DECISION — BOUNDARY CLOSED**
**Evidence:** C1–C10
**Repository:** `Kuntara516/onemind`
**Branch:** `feature/sprint4-context-intelligence`

---

## 1. Purpose

This document closes the architectural boundary between:

* the **S4 Context Runtime**
* the existing **Agent Runtime execution pipeline**
* the legacy `app/context` orchestration stack

The decision is based on direct inspection of the current implementation and tests, not on intended architecture alone.

The purpose is to establish:

1. where Context Runtime currently exists,
2. where Agent execution currently begins,
3. whether Context Runtime is already integrated into execution,
4. where the integration boundary actually exists,
5. what must remain unchanged,
6. what the next implementation boundary is.

---

# 2. Evidence Summary

The C1–C10 inspection establishes the following facts.

| Evidence | Finding                                                                                          | Architectural implication                                     |
| -------- | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------- |
| C1–C6    | `ContextRuntimeFactory` composes a complete Context Runtime graph                                | Context Runtime has an explicit composition root              |
| C1–C6    | Factory creates retriever, ranker, selector, assembler, policy, observability                    | Context Runtime construction is internally complete           |
| C1–C6    | Factory tests verify fresh dependency graphs and explicit injection                              | Factory boundary is stable                                    |
| C7–C8    | `TaskManager` delegates execution to `Executor`                                                  | TaskManager does not own context intelligence                 |
| C7–C8    | `Executor` delegates agent execution through `AgentInvoker`                                      | Agent invocation remains downstream of execution coordination |
| C8–C9    | `ExecutionService` creates `AgentContext` directly                                               | Current execution entry owns creation of execution context    |
| C9       | `AgentInvoker` consumes `AgentInvocationRequest` containing `AgentContext`                       | Agent context is already an explicit execution dependency     |
| C9       | `AgentInvoker` invokes `agent.execute(input, context, capability_manager)`                       | Agent implementation receives runtime context                 |
| C10      | `ContextRuntimeIntegration.build_context()` exists                                               | Context Runtime can produce assembled runtime context         |
| C10      | `ContextRuntimeIntegration` writes `assembled_context` and `context_runtime` into `AgentContext` | Explicit injection mechanism already exists                   |
| C10      | No execution-path reference to `ContextRuntimeFactory`                                           | Context Runtime is not composed into main execution           |
| C10      | No execution-path call to `ContextRuntimeIntegration.build_context()`                            | Context Runtime is not executed before agent invocation       |
| C10      | Legacy `ContextService` is still used by `app/context/orchestrator`                              | Legacy context stack remains separate                         |
| C10      | `AgentTask.execution_context` exists                                                             | Task contract already has a place for execution metadata      |

---

# 3. Current Execution Architecture

The actual execution path is:

```text
HTTP /execute
    |
    v
ExecutionService.execute(task)
    |
    +--> create ExecutionTrace
    |
    +--> create AgentContext
    |
    +--> TaskManager.create_task(task)
    |
    +--> TaskManager.submit_task(task)
    |
    v
TaskManager.execute_task(...)
    |
    v
Executor.execute(...)
    |
    v
AgentInvoker.invoke(...)
    |
    v
AgentRegistry.get(agent_id)
    |
    v
Agent.execute(
    task.input,
    AgentContext,
    CapabilityManager
)
```

This path is confirmed by:

* `app/main.py`
* `app/runtime.py`
* `app/manager/task_manager.py`
* `app/executor/executor.py`
* `app/runtime/invoker.py`
* `app/runtime/invocation_request.py`
* `tests/test_execution_pipeline.py`

---

# 4. Current Context Runtime Architecture

The S4 Context Runtime has its own internal composition:

```text
ContextRuntimeFactory
        |
        +--> ContextRuntimeCoordinator
        |
        +--> ContextRetriever
        |
        +--> ContextRanker
        |
        +--> ContextSelector
        |
        +--> ContextAssembler
        |
        +--> SelectionPolicy
        |
        +--> ContextRuntimeObservabilityRuntime
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

The important point is that this graph is **internally complete but externally disconnected from Agent execution**.

---

# 5. Factory Boundary

`ContextRuntimeFactory` is confirmed to be a **composition-only factory**.

Its responsibility is:

```text
construct dependencies
        |
        v
return ContextRuntimeIntegration
```

It does **not**:

* retrieve context,
* evaluate context,
* make runtime decisions,
* refresh context,
* invoke agents,
* execute capabilities,
* execute tasks.

The factory tests explicitly verify this property.

Therefore:

> `ContextRuntimeFactory` must remain a construction boundary and must not become an execution coordinator.

This is a closed decision.

---

# 6. Execution Boundary

`ExecutionService` is the current execution entry point.

Current implementation:

```python
trace = ExecutionTrace(...)

context = AgentContext(...)

task_manager.create_task(task)
task_manager.submit_task(task)

result = await task_manager.execute_task(
    task,
    self.agent_invoker,
    context,
    trace,
)

trace.finish()

self.trace_recorder.record(trace)
```

The critical observation is:

```text
ExecutionService
    |
    +--> creates AgentContext
    |
    +--> passes AgentContext downstream
```

But currently there is no:

```text
ContextRuntimeFactory
```

and no:

```text
ContextRuntimeIntegration.build_context(...)
```

in this path.

Therefore:

> **The current execution pipeline is Context-Runtime unaware.**

---

# 7. Agent Invocation Boundary

`AgentInvoker` provides a clean downstream boundary:

```text
Executor
    |
    v
AgentInvoker.invoke(
    AgentInvocationRequest
)
    |
    v
Agent.execute(
    input,
    context,
    capability_manager
)
```

The invocation request already contains:

```python
agent_id
task
context
```

Therefore Context Runtime does not need to modify the Agent implementation contract merely to participate in execution.

The existing `AgentContext` is sufficient as the transport boundary.

---

# 8. Existing Context Injection Mechanism

The most important C10 evidence is inside:

```text
app/context_runtime/integration.py
```

`ContextRuntimeIntegration.build_context(...)` already has the ability to place runtime context into `AgentContext`.

The implementation writes:

```python
agent_context.set(
    "assembled_context",
    ...
)

agent_context.set(
    "context_runtime",
    ...
)
```

Therefore the intended integration shape is already represented by actual code:

```text
ContextRuntime
      |
      v
AssembledContext
      |
      v
AgentContext
      |
      v
AgentInvoker
      |
      v
Agent
```

This is a strong architectural boundary because it avoids coupling the Agent implementation to Context Runtime internals.

---

# 9. Legacy Context Stack Boundary

The repository still contains:

```text
app/context/
```

including:

```text
app/context/service.py
app/context/builder.py
app/context/orchestrator/
app/context/ranking/
app/context/compression/
```

The legacy orchestration strategy explicitly depends on:

```python
from app.context.service import ContextService
```

and calls:

```python
await self._context_service.build_context(...)
```

Therefore the repository currently contains **two context architectures**.

### Legacy Context Stack

```text
ContextOrchestrator
    |
    v
ContextService
    |
    v
ContextBuilder
    |
    v
legacy context pipeline
```

### S4 Context Runtime

```text
ContextRuntimeFactory
    |
    v
ContextRuntimeIntegration
    |
    v
Retrieval
    |
    v
Ranking
    |
    v
Selection
    |
    v
Assembly
    |
    v
Evaluation / Decision / Refresh
```

These must not be implicitly merged.

---

# 10. Decision: Do Not Reuse Legacy ContextService

The evidence does **not** justify replacing or wrapping the S4 Context Runtime with:

```python
ContextService
```

Nor does it justify making:

```text
ContextRuntimeIntegration
    ->
ContextService
```

the primary execution path.

The two stacks have different responsibilities and maturity levels.

Therefore:

> **The S4 Context Runtime remains the authoritative context-intelligence boundary for the new execution integration.**

The legacy `app/context` stack remains untouched unless a separate migration decision explicitly authorizes its replacement.

---

# 11. Decision: AgentContext Is the Integration Transport

The existing execution contract already provides:

```python
AgentContext
```

and `AgentInvoker` already passes it into:

```python
agent.execute(...)
```

The S4 runtime already knows how to enrich it.

Therefore the selected integration boundary is:

```text
ContextRuntimeIntegration
        |
        v
AgentContext
        |
        v
TaskManager / Executor
        |
        v
AgentInvoker
        |
        v
Agent
```

No new context parameter needs to be added to:

```text
AgentInvoker.invoke()
AgentInvocationRequest
Agent.execute()
```

for the initial integration.

---

# 12. Decision: ExecutionService Is the Integration Point

The current `ExecutionService.execute()` is the first stable boundary where all required information is available:

```text
AgentTask
AgentContext
ExecutionTrace
AgentInvoker
TaskManager
```

It is therefore the correct location to introduce Context Runtime integration.

The intended flow becomes:

```text
ExecutionService.execute(task)
        |
        v
create AgentContext
        |
        v
ContextRuntimeIntegration.build_context(
    task,
    agent_context,
)
        |
        v
AgentContext enriched with:
    - assembled_context
    - context_runtime
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

This establishes a clean dependency direction:

```text
Execution
    |
    v
Context Intelligence
    |
    v
Agent execution
```

rather than allowing Agent implementations to construct or control Context Runtime.

---

# 13. Decision: TaskManager Must Not Own Context Runtime

`TaskManager` currently owns:

* task registration,
* lifecycle transition,
* execution delegation,
* task tracking.

Its contract explicitly states that it does not:

* execute agents directly,
* execute capabilities directly,
* contain business logic.

Context Runtime should therefore **not** be injected into `TaskManager`.

The correct boundary is above `TaskManager`:

```text
ExecutionService
    |
    +--> Context Runtime
    |
    v
TaskManager
```

not:

```text
TaskManager
    |
    +--> Context Runtime
```

---

# 14. Decision: Executor Must Not Own Context Runtime

`Executor` is responsible for execution coordination and Agent invocation through the existing execution contract.

Context assembly is an upstream concern.

Therefore:

```text
Executor
```

must remain unaware of:

```text
ContextRuntimeFactory
ContextRuntimeIntegration
ContextRetriever
ContextRanker
ContextSelector
ContextAssembler
```

The Executor receives the already-prepared `AgentContext`.

---

# 15. Decision: AgentInvoker Must Not Own Context Runtime

`AgentInvoker` owns:

* Agent resolution,
* Agent execution,
* capability injection,
* invocation result construction.

It must not become a Context Runtime coordinator.

The correct flow remains:

```text
AgentInvoker
    |
    v
Agent
```

with Context Runtime data transported through:

```text
AgentInvocationRequest.context
```

---

# 16. Decision: Context Runtime Factory Must Be Injected

The next integration should not instantiate Context Runtime dependencies directly inside `ExecutionService`.

Avoid:

```python
ContextRuntimeFactory().create()
```

inside every execution call.

The preferred composition is:

```text
Main Composition Root
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

This preserves dependency inversion and keeps construction outside runtime execution.

---

# 17. Target Composition Root

The composition root should eventually resemble:

```text
app/main.py
    |
    +--> registry
    +--> capability_manager
    +--> agent_invoker
    +--> trace_recorder
    +--> executor
    +--> task_manager
    |
    +--> context_runtime_factory
    |       |
    |       v
    |   context_runtime
    |
    +--> execution_service
            |
            +--> task_manager
            +--> agent_invoker
            +--> trace_recorder
            +--> context_runtime
```

The exact implementation may use another composition root in the future, but the architectural principle remains:

> construction belongs to the composition root; execution belongs to runtime services.

---

# 18. Target Runtime Flow

The next authorized execution flow is:

```text
POST /execute
      |
      v
ExecutionService.execute(task)
      |
      +----------------------+
      |                      |
      v                      v
ExecutionTrace          AgentContext
                             |
                             v
                  ContextRuntimeIntegration
                             |
                             v
                  Context Intelligence Pipeline
                             |
              +--------------+--------------+
              |              |              |
              v              v              v
          Retrieval       Ranking       Selection
              |              |              |
              +--------------+--------------+
                             |
                             v
                         Assembly
                             |
                             v
                     Evaluation / Decision
                             |
                             v
                        Refresh Control
                             |
                             v
                     AgentContext.set(...)
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

---

# 19. Important Boundary: Context Runtime Does Not Execute Agents

The Context Runtime may decide:

* what context should be used,
* whether context quality is sufficient,
* whether refresh is required,
* what context package should be exposed.

It must not:

* resolve the Agent,
* call `agent.execute()`,
* execute capabilities,
* change task lifecycle,
* own `ExecutionTrace` lifecycle.

Those responsibilities remain in the Agent Runtime execution stack.

---

# 20. Important Boundary: Execution Does Not Reimplement Context Intelligence

Conversely, `ExecutionService` must not implement:

* retrieval,
* ranking,
* selection,
* assembly,
* context evaluation,
* decision policy,
* refresh policy.

It should delegate those responsibilities to:

```text
ContextRuntimeIntegration
```

This prevents the execution layer from becoming a second Context Runtime.

---

# 21. `AgentTask.execution_context`

`AgentTask` already contains:

```python
execution_context: dict[str, Any]
```

This field is part of the task execution contract.

However, C10 demonstrates that the current S4 integration mechanism already uses:

```text
AgentContext
```

as the runtime context transport.

Therefore the initial Context Runtime integration should **not duplicate the assembled context into `AgentTask.execution_context` unless a concrete execution contract requires it**.

The preferred separation is:

```text
AgentTask.execution_context
    = task-level execution metadata

AgentContext
    = runtime execution context

AgentContext["assembled_context"]
    = Context Runtime output
```

This avoids creating two competing sources of runtime context.

---

# 22. Architectural Invariants

The following invariants are now established.

### Invariant 1 — Factory Is Composition Only

```text
ContextRuntimeFactory
```

constructs the graph and performs no runtime execution.

### Invariant 2 — ExecutionService Is the Integration Boundary

Context Runtime enters the execution pipeline at:

```text
ExecutionService
```

### Invariant 3 — AgentContext Is the Transport Boundary

Context Runtime output is exposed through:

```text
AgentContext
```

### Invariant 4 — TaskManager Remains Context-Agnostic

Task lifecycle and Context Intelligence remain separate.

### Invariant 5 — Executor Remains Context-Agnostic

Executor receives prepared runtime context and performs execution.

### Invariant 6 — AgentInvoker Remains Context-Agnostic

AgentInvoker passes context to the Agent but does not construct it.

### Invariant 7 — Agents Remain Context-Runtime Agnostic

Agents consume `AgentContext`; they do not depend on Context Runtime internals.

### Invariant 8 — Legacy Context Stack Remains Separate

`app/context` is not implicitly replaced by S4 Context Runtime.

### Invariant 9 — No Duplicate Context Pipeline

The execution layer must not reproduce retrieval/ranking/selection/assembly logic.

### Invariant 10 — One Context Authority

For the new execution path, S4 `ContextRuntimeIntegration` is the authoritative context-intelligence provider.

---

# 23. What Is Proven Today

The following is already proven by code and tests:

```text
[PROVEN]

ContextRuntimeFactory
    |
    v
complete Context Runtime graph

[PROVEN]

ContextRuntimeIntegration
    |
    v
assembled_context
    |
    v
AgentContext

[PROVEN]

AgentContext
    |
    v
AgentInvocationRequest
    |
    v
AgentInvoker
    |
    v
Agent.execute()

[PROVEN]

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

[PROVEN]

No current connection:

ExecutionService
    X
ContextRuntimeFactory / ContextRuntimeIntegration
```

---

# 24. What Is Not Yet Implemented

The following capability is **not yet implemented**:

```text
ExecutionService
        |
        v
ContextRuntimeIntegration.build_context(...)
        |
        v
AgentContext enrichment
        |
        v
Task execution
```

There is also no evidence that:

```text
app/main.py
```

currently constructs:

```text
ContextRuntimeFactory
```

or injects:

```text
ContextRuntimeIntegration
```

into:

```text
ExecutionService
```

Therefore this document does **not** claim that execution integration is complete.

---

# 25. Next Implementation Boundary

The next implementation task should be narrowly defined as:

> **Integrate the already-existing Context Runtime into the Agent Runtime execution entry without moving Context Runtime responsibilities into TaskManager, Executor, or AgentInvoker.**

The implementation should therefore focus on:

1. composing `ContextRuntimeFactory` at the composition root,
2. injecting `ContextRuntimeIntegration` into `ExecutionService`,
3. invoking `build_context(task, agent_context)` at the correct point,
4. preserving the existing execution lifecycle,
5. preserving the existing `AgentInvocationRequest` contract,
6. verifying that Agents receive enriched `AgentContext`,
7. adding execution-level integration tests.

---

# 26. Explicit Non-Goals

The next integration must **not**:

* rewrite `ContextRuntimeIntegration`,
* redesign the Context Runtime pipeline,
* reimplement retrieval,
* reimplement ranking,
* reimplement selection,
* reimplement assembly,
* move context logic into `TaskManager`,
* move context logic into `Executor`,
* move context logic into `AgentInvoker`,
* modify Agent implementations unnecessarily,
* replace `app/context`,
* delete `ContextService`,
* merge legacy and S4 context packages,
* add another context builder abstraction,
* make `ContextRuntimeFactory` execute runtime behavior,
* introduce S4-011-007 implicitly.

---

# 27. S4-011 Boundary Decision

## Decision

**APPROVED ARCHITECTURAL BOUNDARY**

The S4 Context Runtime is ready to be integrated into the existing Agent Runtime execution path through:

```text
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

The Context Runtime remains a separate subsystem with its own composition boundary.

The Agent Runtime remains the owner of task execution.

The `AgentContext` remains the transport boundary between them.

---

# 28. Final Architecture

The resulting architecture is:

```text
                         COMPOSITION ROOT
                               |
              +----------------+----------------+
              |                                 |
              v                                 v
     ContextRuntimeFactory              Agent Runtime Wiring
              |                                 |
              v                                 |
     ContextRuntimeIntegration                  |
              |                                 |
              |                                 v
              |                         ExecutionService
              |                                 |
              |                    +------------+------------+
              |                    |                         |
              v                    v                         v
       Context Intelligence   AgentContext             ExecutionTrace
              |                    |
              |                    |
              +-------> enriched <-+
                       context
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

The architectural principle is:

> **Context Intelligence prepares runtime context. Agent Runtime executes the task. AgentContext connects the two.**

---

# 29. Boundary Status

| Boundary                                 | Status                                        |
| ---------------------------------------- | --------------------------------------------- |
| Context Runtime internal composition     | **CLOSED**                                    |
| Context Runtime Factory responsibility   | **CLOSED**                                    |
| Context Runtime → AgentContext mechanism | **CLOSED**                                    |
| TaskManager responsibility               | **CLOSED**                                    |
| Executor responsibility                  | **CLOSED**                                    |
| AgentInvoker responsibility              | **CLOSED**                                    |
| Legacy `app/context` relationship        | **CLOSED**                                    |
| ExecutionService integration point       | **CLOSED**                                    |
| Actual execution integration             | **NOT YET IMPLEMENTED**                       |
| Next implementation scope                | **AUTHORIZED FOR EXECUTION-INTEGRATION ONLY** |

---

# 30. Source Evidence

Primary evidence inspected:

```text
app/context_runtime/factory.py
app/context_runtime/integration.py

app/manager/task_manager.py
app/runtime.py
app/runtime/invoker.py
app/runtime/invocation_request.py
app/agents/context.py

app/tasks/models.py
app/main.py

app/context/service.py
app/context/orchestrator/strategies/default.py

tests/test_context_runtime_factory.py
tests/test_context_runtime_integration.py
tests/test_execution_pipeline.py
tests/test_executor.py
```

The decision in this document is derived from these implementation and test artifacts.

---

# 31. Final Decision Statement

**S4 Context Runtime architectural boundary is now closed.**

The codebase proves that:

```text
Context Runtime
    !=
Task Execution
```

but also proves that:

```text
Context Runtime
    ->
AgentContext
    ->
Agent Execution
```

is already structurally supported.

Therefore the next step is **not another Context Runtime redesign**.

The next step is the narrow integration of the existing Context Runtime into `ExecutionService`, with construction performed by the composition root and runtime context transported through `AgentContext`.

No other architectural boundary is authorized to change as part of this integration.
