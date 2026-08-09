# OneMind — S4 Next Phase Decision Gate

## S4-011 Context Intelligence / Decision Boundary

**Document:** `docs/implementation/sprints/S4-NEXT-PHASE-DECISION-GATE.md`
**Project:** OneMind
**Branch:** `feature/sprint4-context-intelligence`
**Purpose:** Freeze the decision boundary before entering runtime-level context control integration.

---

## 1. Decision Status

**Status:** ACCEPTED

**Decision:** `REFRESH` is a runtime control signal for the **next execution**, not an immediate re-execution of the current Agent invocation.

The current execution completes under the context state that was used for that invocation.

If evaluation determines that context should be refreshed, the decision is carried forward as a runtime control artifact. The refresh becomes effective at the **next eligible execution boundary**.

This decision is now the governing contract for the next S4-011 implementation phase.

---

## 2. Current S4-011 Baseline

The Context Runtime already contains the following conceptual layers:

```text
Context Retrieval
      ↓
Context Ranking
      ↓
Context Selection
      ↓
Context Assembly
      ↓
Context Runtime State
      ↓
Context Evaluation
      ↓
Decision
      ↓
Execution Artifact
      ↓
Runtime Control
      ↓
Refresh Engine
```

The current implementation establishes:

* context runtime state
* lifecycle management
* refresh policy
* refresh engine
* evaluation
* feedback classification
* decision generation
* execution artifact
* decision controller
* runtime integration
* observability

The remaining architectural question is **when a runtime control action becomes effective relative to Agent execution**.

---

## 3. Evidence From Current Implementation

### 3.1 Refresh Engine

`services/agent-runtime/app/context_runtime/refresh.py`

`DefaultContextRefreshEngine` is responsible for:

* determining whether refresh is due
* applying lifecycle refresh
* updating refresh timestamps

It explicitly does **not**:

* retrieve context
* rank context
* select context
* modify context content
* evaluate relevance
* invoke Agent Runtime

The engine therefore represents a lifecycle/control primitive rather than an execution restart mechanism.

---

### 3.2 Decision Controller

`services/agent-runtime/app/context_runtime/control.py`

`ContextRuntimeDecisionController` currently maps execution artifacts to runtime actions:

```text
RETAIN
    ↓
no-op

REVIEW
    ↓
no-op

REFRESH
    ↓
ContextRefreshEngine.refresh()
```

The controller reports whether refresh was actually applied.

This establishes a clean boundary:

```text
Evaluation / Decision
        ↓
Execution Artifact
        ↓
Decision Controller
        ↓
Refresh Engine
```

The controller does not evaluate context and does not invoke the Agent.

---

### 3.3 Agent Execution Boundary

The current execution pipeline is:

```text
ExecutionService
    ↓
TaskManager
    ↓
Executor
    ↓
AgentInvoker
    ↓
Agent
```

`ExecutionService` creates `AgentContext` before task execution:

```text
AgentTask
    ↓
AgentContext
    ↓
TaskManager
    ↓
Executor
    ↓
AgentInvoker
    ↓
Agent
```

The existing `AgentContext` is attached to the current invocation.

Therefore, changing the context during an already-running invocation would introduce a new semantic problem:

```text
current invocation
        ↓
context changes
        ↓
same invocation continues
```

That behavior is not currently defined by the runtime contract.

---

## 4. Decision: REFRESH = NEXT EXECUTION

### 4.1 Accepted Semantics

The following semantics are frozen:

```text
Current Execution
      │
      │ context snapshot/state
      ▼
   Agent runs
      │
      ▼
 Execution completes
      │
      ▼
 Evaluation
      │
      ▼
 Decision
      │
      ├── RETAIN
      │      └── no control action
      │
      ├── REVIEW
      │      └── no control action
      │
      └── REFRESH
             │
             ▼
       mark refresh/control intent
             │
             ▼
      NEXT EXECUTION
             │
             ▼
      rebuild / refresh context
```

The important invariant is:

> A `REFRESH` decision does not restart or mutate the current Agent invocation.

---

## 5. Why REFRESH Must Not Re-Execute Immediately

Immediate re-execution would create several undefined behaviors.

### 5.1 Duplicate Agent Execution

A single task could result in:

```text
Invocation #1
    ↓
Evaluation
    ↓
REFRESH
    ↓
Invocation #2
```

Without an explicit retry contract, this would make one user request produce multiple Agent executions.

That is unsafe for operations with side effects.

---

### 5.2 Ambiguous Task Lifecycle

The existing task lifecycle has execution states independent from context lifecycle.

Immediate re-execution would require a new task lifecycle contract describing:

* retry
* replay
* replacement execution
* attempt numbering
* failure semantics
* idempotency
* trace correlation

None of these are currently part of the S4-011 decision boundary.

Therefore they must not be introduced implicitly by `REFRESH`.

---

### 5.3 Context Mutation During Invocation

An Agent invocation receives an `AgentContext`.

If refresh mutates the context while the Agent is executing, the meaning of:

```text
context
```

would become time-dependent.

The same invocation could observe different context states at different moments.

That violates the desired execution boundary:

```text
Invocation
    ↓
stable context
    ↓
Agent execution
    ↓
result
```

---

## 6. New Runtime Contract

The accepted runtime contract is:

### Current Execution

The current execution uses the context available at its execution boundary.

```text
Context prepared
      ↓
Invocation starts
      ↓
Context remains stable
      ↓
Invocation completes
```

### Post-Execution Evaluation

After execution:

```text
Execution Result
      ↓
Context Evaluation
      ↓
Decision
```

### REFRESH

If the decision is:

```text
REFRESH
```

the runtime records that the context should be refreshed before the next eligible execution.

It does not:

* restart the current task
* invoke the Agent again
* mutate the current invocation context
* replace the current execution result

---

## 7. Effective State Model

The runtime should conceptually distinguish:

```text
CURRENT EXECUTION STATE
        +
PENDING CONTEXT CONTROL
```

For example:

```text
Context Runtime State
---------------------
lifecycle
last_refresh
updated_at
metadata

Pending Control
---------------
action = REFRESH
evaluation_id
```

The exact persistence model is implementation-specific and is intentionally deferred to S4-011-007.

---

## 8. Decision Artifact Semantics

The existing execution artifact remains authoritative for the control decision.

Conceptually:

```text
ContextRuntimeExecutionResult
```

contains:

```text
evaluation_id
action
metadata
```

The accepted interpretation is:

| Action    | Current Execution | Next Execution                                 |
| --------- | ----------------- | ---------------------------------------------- |
| `RETAIN`  | Continue normally | Continue with existing context policy          |
| `REVIEW`  | Continue normally | Requires no automatic refresh                  |
| `REFRESH` | Continue normally | Refresh context before next eligible execution |

The key distinction is:

```text
REFRESH ≠ RETRY
```

and:

```text
REFRESH ≠ RE-EXECUTE
```

---

## 9. Decision Controller Boundary

`ContextRuntimeDecisionController` remains responsible for applying the decision artifact to runtime control.

Its architectural responsibility is:

```text
Decision Artifact
      ↓
Control Interpretation
      ↓
Runtime Control State
```

It must not become responsible for:

* Agent invocation
* task retry
* task replay
* context retrieval
* context ranking
* context selection
* context evaluation

The controller therefore remains deliberately narrow.

---

## 10. Refresh Engine Boundary

`DefaultContextRefreshEngine` remains responsible for the actual lifecycle refresh operation.

Its contract remains:

```text
should_refresh(state)
        ↓
      bool

refresh(state)
        ↓
ContextRuntimeState
```

The refresh engine does not determine:

```text
why refresh was requested
```

and does not determine:

```text
whether the Agent should execute again
```

Those decisions belong to higher runtime control layers.

---

## 11. Next Phase

The next implementation phase is:

# S4-011-007 — Runtime-Level Context Control Integration

The purpose of S4-011-007 is to connect the existing decision/control layer to the Agent Runtime execution boundary without violating the newly frozen semantics.

The integration target is:

```text
Agent Execution
      ↓
Evaluation
      ↓
Decision
      ↓
Control
      ↓
Pending Refresh
      ↓
NEXT EXECUTION
      ↓
Context Refresh / Rebuild
      ↓
Agent Execution
```

The key architectural change is therefore **not** to restart execution.

The change is to make the runtime aware of pending context control before the next eligible execution.

---

## 12. S4-011-007 Scope

The next phase should investigate and implement only the following:

### 12.1 Execution Boundary

Identify the exact point where `AgentContext` is constructed and determine where pending context control should be consulted.

Current location:

```text
services/agent-runtime/app/runtime/execution.py
```

---

### 12.2 Pending Control

Define the runtime representation of a pending:

```text
REFRESH
```

control action.

The representation must preserve:

* action
* evaluation identity
* context identity where available
* control timestamp where required

---

### 12.3 Next-Execution Application

Before constructing the effective context for a new execution:

```text
pending REFRESH
      ↓
apply refresh policy
      ↓
obtain refreshed runtime state
      ↓
assemble effective context
      ↓
invoke Agent
```

---

### 12.4 Current Execution Isolation

The implementation must prove that:

```text
REFRESH
```

does not cause:

* second Agent invocation
* task retry
* task replay
* duplicate side effects
* mutation of the active invocation context

---

### 12.5 Test Coverage

S4-011-007 must add tests proving at minimum:

1. `RETAIN` does not create pending refresh.
2. `REVIEW` does not create pending refresh.
3. `REFRESH` creates pending refresh/control state.
4. Current execution completes exactly once.
5. Next execution observes the pending refresh.
6. Refresh occurs before the next Agent invocation.
7. The refreshed context is the one supplied to the next invocation.
8. Pending refresh is consumed exactly once.
9. A completed refresh does not cause duplicate refresh.
10. Current invocation context remains unchanged after a post-execution `REFRESH` decision.

---

## 13. Explicit Non-Goals

S4-011-007 must not introduce:

### Retry Engine

No automatic retry semantics.

### Replay Engine

No replay of an existing task.

### Agent Re-Invocation

No second Agent call caused by `REFRESH` during the same execution.

### Context Hot-Swap

No mutation of active invocation context.

### New Evaluation Policy

Evaluation semantics are already established.

### New Decision Policy

Decision semantics are already established.

### New Retrieval Strategy

Retrieval remains outside the control layer.

---

## 14. Architectural Invariants

The following invariants are frozen for subsequent implementation.

### Invariant 1 — One Invocation

One execution request produces one Agent invocation unless a future explicit retry contract says otherwise.

```text
request
  ↓
one invocation
  ↓
one result
```

---

### Invariant 2 — Stable Invocation Context

The context supplied to an Agent remains stable for that invocation.

```text
Invocation Start
      ↓
Context Snapshot
      ↓
Agent
      ↓
Invocation End
```

---

### Invariant 3 — REFRESH Is Deferred

```text
REFRESH
```

means:

> refresh context before the next eligible execution.

It does not mean:

> execute this task again.

---

### Invariant 4 — Evaluation Does Not Invoke

Evaluation determines a decision.

```text
evaluation
    ↓
decision
```

It does not execute the Agent.

---

### Invariant 5 — Decision Does Not Execute

The decision layer determines:

```text
RETAIN
REVIEW
REFRESH
```

It does not directly execute the Agent.

---

### Invariant 6 — Control Does Not Evaluate

The control layer applies an already-created execution artifact.

It does not recalculate context quality.

---

### Invariant 7 — Refresh Does Not Retrieve

The refresh engine manages lifecycle refresh semantics.

Context retrieval/reconstruction remains a separate runtime responsibility.

---

## 15. Target Architecture

The target S4-011 architecture is:

```text
                    ┌─────────────────────┐
                    │   Agent Execution   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Context Runtime   │
                    │   Integration       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Context Assembly    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Agent Invocation    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Execution Result    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Context Evaluation  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Decision            │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Runtime Control     │
                    └──────────┬──────────┘
                               │
                         REFRESH only
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Pending Control     │
                    └──────────┬──────────┘
                               │
                        next execution
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Refresh / Rebuild   │
                    │ Context             │
                    └─────────────────────┘
```

---

## 16. Decision Gate Outcome

### ACCEPT

The following decision is frozen:

```text
REFRESH = NEXT EXECUTION
```

Therefore:

```text
REFRESH
    ≠
RETRY
```

```text
REFRESH
    ≠
REPLAY
```

```text
REFRESH
    ≠
IMMEDIATE RE-EXECUTION
```

Instead:

```text
REFRESH
    =
PENDING CONTEXT CONTROL
FOR THE NEXT ELIGIBLE EXECUTION
```

---

## 17. Implementation Order

The implementation sequence after this decision gate is:

```text
S4-011-007-001
Inspect execution boundary and pending-control insertion point

        ↓

S4-011-007-002
Define pending refresh/control runtime state

        ↓

S4-011-007-003
Integrate pending control into next execution context preparation

        ↓

S4-011-007-004
Prove current execution isolation

        ↓

S4-011-007-005
Add next-execution refresh integration tests

        ↓

S4-011-007-006
Run full regression

        ↓

Decision / Release Gate
```

No implementation should proceed beyond the existing decision boundary without preserving the invariants defined in this document.

---

## 18. Final Decision Record

**Decision:** `REFRESH = NEXT EXECUTION`

**Effective behavior:**

```text
Current execution
    ↓
complete normally
    ↓
evaluate context
    ↓
produce REFRESH decision
    ↓
record pending control
    ↓
current execution ends
    ↓
next execution begins
    ↓
apply refresh
    ↓
build effective context
    ↓
invoke Agent
```

**Rejected behavior:**

```text
Current execution
    ↓
REFRESH
    ↓
invoke Agent again
```

**Reason for rejection:**

The rejected behavior conflates context maintenance with task retry/replay and would introduce undefined execution semantics, duplicate side effects, and unstable invocation context.

---

## 19. Gate Closure

This document closes the decision gate for the timing semantics of `REFRESH`.

The next phase is implementation work only:

```text
S4-011-007 — Runtime-Level Context Control Integration
```

The implementation must treat this document as the governing decision record for `REFRESH` timing.
