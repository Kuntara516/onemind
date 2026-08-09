# S4-NEXT-PHASE-DECISION-GATE

**Status:** FINAL GATE DECISION — SUCCESSOR TASK NOT YET ASSIGNED
**Baseline:** `v0.9.10-s4-context-runtime-control`
**Baseline Commit:** `d6b1253`
**Branch:** `feature/sprint4-context-intelligence`

## 1. Purpose

This document is the planning gate immediately following the frozen Sprint 4 Context Intelligence runtime-control boundary.

Its purpose is to determine the intended next architectural capability **before** assigning or implementing a successor task such as `S4-011-007`.

This document records the final planning reconciliation against the repository implementation.

It is a planning artifact, not an implementation specification.

---

## 2. Frozen Baseline

The current Sprint 4 implementation boundary is:

```text
Context Assembly
    ↓
Retrieval / Ranking / Compression
    ↓
Context Runtime
    ↓
Runtime Observability
    ↓
Context Quality Evaluation
    ↓
Runtime Feedback
    ↓
Feedback Consumer
    ↓
Decision Boundary
    ↓
Decision Execution
    ↓
Runtime Control
    ↓
Context Refresh
```

The following contracts are frozen and must be treated as upstream inputs for any future work:

* Context evaluation contracts
* Runtime feedback contracts
* Feedback consumer contract
* `ContextRuntimeDecisionResult`
* Decision execution contract
* Runtime control contract
* Context refresh engine contract

Future work must not move responsibilities backward into these layers unless a concrete defect is demonstrated.

---

## 3. Repository Reconciliation

The planning gate was reconciled against the actual Agent Runtime and Context Runtime implementation.

### 3.1 Agent Runtime execution path

The current execution lifecycle is:

```text
ExecutionService
    ↓
TaskManager
    ↓
Executor
    ↓
AgentInvocationRequest
    ↓
AgentInvoker
```

`Executor` owns:

* lifecycle coordination
* agent invocation
* result handling
* execution metadata
* execution trace events

`TaskManager` remains responsible for task coordination and tracking.

No Context Runtime decision or control responsibility is currently owned by `Executor`.

---

### 3.2 Existing Agent Runtime context transport boundary

`AgentInvocationRequest` already accepts:

```text
AgentTask
agent_id
AgentContext
```

`AgentContext` already provides a runtime transport object capable of carrying:

```text
assembled_context
runtime metadata
```

The existing Context Runtime integration layer stores assembled context into `AgentContext`.

Therefore, the repository already contains a natural transport boundary:

```text
Context Runtime
      ↓
AgentContext
      ↓
AgentInvocationRequest
      ↓
AgentInvoker
```

No new generic context transport abstraction is required by the current evidence.

---

### 3.3 Existing Context Runtime assembly integration

`ContextRuntimeIntegration` already provides:

```text
Retrieve
    ↓
Rank
    ↓
Select
    ↓
Assemble
    ↓
AgentContext
```

It also integrates Context Runtime observability.

Therefore, the next phase must **not** be defined as a generic "Context Runtime → Agent Runtime integration".

That integration already exists at the context assembly level.

---

### 3.4 Existing runtime-control boundary

The current control architecture is:

```text
ContextRuntimeExecutionResult
        ↓
ContextRuntimeDecisionController
        ↓
ContextRuntimeControlResult
        ↓
ContextRuntimeCoordinator
        ↓
ContextRuntimeState
```

`ContextRuntimeDecisionController` is explicitly responsible for:

* preserving execution artifact identity
* applying explicit actions
* treating `RETAIN` as a no-op
* treating `REVIEW` as a no-op
* delegating `REFRESH` to `ContextRefreshEngine`
* reporting whether refresh was applied

It intentionally does not:

* evaluate context quality
* produce decisions
* retrieve context
* rank context
* select context
* mutate context content
* invoke Agent Runtime

This boundary remains valid and is frozen.

---

## 4. Confirmed Architectural Gap

The repository evidence confirms that the remaining gap is **not another intelligence primitive**.

The actual boundary is:

```text
Context Runtime Control
        ↓
?????????????????????????
        ↓
Agent Runtime Execution Lifecycle
```

More specifically:

```text
ContextRuntimeControlResult
        ↓
Execution Integration Boundary
        ↓
AgentContext / Agent Runtime lifecycle
```

The existing Context Runtime control capability is currently exercised within the Context Runtime domain.

The Agent Runtime `Executor` does not currently consume or observe that control outcome.

Therefore, the remaining gap is:

> **Runtime-level integration of the existing Context Runtime control capability with the Agent Runtime execution lifecycle.**

---

## 5. Final Gate Decision

### Decision: CONTINUE

Sprint 4 should continue beyond `v0.9.10`.

### Approved Planning Direction

**Runtime-Level Context Control Integration**

The intended capability is:

> Wire the existing Context Runtime control capability into the Agent Runtime execution lifecycle through an explicit downstream integration boundary, without moving Context Intelligence ownership into the Executor or AgentInvoker.

This is approved as a **planning direction only**.

It is not yet an implementation authorization.

---

## 6. Integration Ownership

The repository evidence indicates the following ownership model:

```text
Agent Runtime
    │
    ▼
Executor
    │
    │ execution integration
    ▼
AgentContext / invocation boundary
    │
    ▼
AgentInvoker
```

while Context Runtime remains responsible for:

```text
ContextRuntimeCoordinator
    │
    ├── ContextRuntimeState
    ├── Budget
    ├── Lifecycle
    └── Decision Control
            │
            ▼
      ContextRuntimeControlResult
```

The successor design must preserve this separation.

### Executor must not own:

* context quality evaluation
* feedback interpretation
* decision generation
* refresh policy
* context lifecycle policy
* direct `ContextRuntimeState` mutation

### Context Runtime must not own:

* Agent invocation
* Agent lifecycle
* task lifecycle
* execution orchestration

The successor boundary must connect these domains without collapsing their responsibilities.

---

## 7. Existing Transport Boundary

The existing transport boundary is:

```text
Context Runtime
      ↓
AgentContext
      ↓
AgentInvocationRequest
      ↓
AgentInvoker
```

`AgentContext` is therefore the primary existing runtime context carrier.

A successor task may extend the information carried across this boundary only if required by an explicitly approved contract.

No new transport abstraction should be introduced without demonstrating a concrete need.

---

## 8. Runtime Control Semantics

The existing action semantics are:

### RETAIN

```text
Decision
  ↓
RETAIN
  ↓
No runtime mutation
  ↓
Execution may continue
```

### REVIEW

```text
Decision
  ↓
REVIEW
  ↓
No runtime mutation
  ↓
Execution may continue
```

### REFRESH

```text
Decision
  ↓
REFRESH
  ↓
ContextRuntimeCoordinator
  ↓
ContextRuntimeControlResult
  ↓
Execution lifecycle
```

The final arrow remains the unresolved architectural decision.

---

## 9. Remaining Architectural Decision — Refresh Timing

Before assigning a concrete successor task ID, the project must explicitly define the temporal semantics of `REFRESH`.

The possible semantics are:

```text
A. Current execution
B. Next execution
C. Both current and next execution
```

The current `DefaultContextRefreshEngine` performs lifecycle-oriented refresh:

```text
ACTIVE → STALE → ACTIVE
```

or:

```text
STALE → ACTIVE
```

and updates refresh timestamps.

It does **not** currently rebuild assembled context content.

Therefore:

> A `REFRESH` control outcome must not automatically be interpreted as "the current Agent invocation receives newly retrieved context" unless a future contract explicitly defines and implements that behavior.

This distinction must be resolved before implementation.

---

## 10. Recommended Successor Contract Shape

If the refresh timing decision is approved, the successor capability should conceptually follow:

```text
ContextRuntimeDecisionResult
        ↓
ContextRuntimeExecutionResult
        ↓
ContextRuntimeControlResult
        ↓
Execution Integration Boundary
        ↓
Agent Runtime Lifecycle
```

The integration boundary should consume the frozen control artifacts.

It must not reconstruct decisions from:

* evaluation metrics
* feedback
* retrieval results
* ranking results
* selection results

The existing Context Runtime decision/control chain remains the authoritative source of runtime control intent.

---

## 11. Explicit Non-Goals

The planning direction does not authorize:

* creation of `S4-011-007` yet
* implementation changes
* modification of frozen S4-011 contracts
* moving decision logic into `Executor`
* moving refresh policy into `Executor`
* direct mutation of `ContextRuntimeState` by Agent Runtime
* adaptive context policy
* automatic retrieval strategy mutation
* multi-agent context coordination
* new persistence requirements
* changes to Context Selector
* changes to Context Ranker
* changes to Context Compressor
* creation of a new generic context transport abstraction without demonstrated need

---

## 12. Successor Task Preconditions

A concrete successor task may be created only after the following are explicitly decided:

```text
1. Refresh timing semantics
2. Current execution vs next execution behavior
3. Exact execution integration owner
4. Exact data crossing the integration boundary
5. Control outcome observability requirements
6. Failure behavior at the integration boundary
7. Tests proving the boundary without coupling
   execution to evaluation internals
8. Whether the work remains Sprint 4
```

Only after these decisions are frozen should a task ID be assigned.

---

## 13. Proposed Successor Scope

Subject to the remaining architectural decision, the successor scope is expected to be:

```text
Runtime-Level Context Control Integration

Objective:
Connect the frozen Context Runtime control capability
to the Agent Runtime execution lifecycle.

Dependencies:
- v0.9.10-s4-context-runtime-control
- ContextRuntimeExecutionResult
- ContextRuntimeControlResult
- ContextRuntimeCoordinator
- AgentContext
- AgentInvocationRequest
- Executor

Must preserve:
- Context Runtime ownership
- Agent Runtime ownership
- decision/control separation
- deterministic execution semantics
- existing frozen contracts
```

No concrete class name, API, file path, or task ID is frozen by this document.

---

## 14. Final Planning State

```text
Implementation status:       FROZEN
Baseline:                    v0.9.10-s4-context-runtime-control

Planning decision:           CONTINUE
Recommended direction:       Runtime-Level Context Control Integration

Integration owner:           Agent Runtime execution boundary
Existing transport:          AgentContext / AgentInvocationRequest
Control owner:               ContextRuntimeCoordinator

Remaining decision:          REFRESH timing semantics

Successor task ID:           NOT ASSIGNED
Implementation:              NOT AUTHORIZED
```

---

## 15. Roadmap State

The roadmap is now:

```text
v0.9.10
FROZEN
   ↓
FINAL PLANNING GATE
   ↓
CONTINUE
   ↓
Runtime-Level Context Control Integration
   ↓
Resolve Refresh Timing Semantics
   ↓
Define Successor Contract
   ↓
Assign Successor Task ID
   ↓
Implementation
```

Until the remaining refresh-timing decision is resolved:

```text
NO S4-011-007
NO IMPLEMENTATION
```

---

## 16. Final Decision Record

**Decision:** Continue Sprint 4.

**Direction:** Runtime-Level Context Control Integration.

**Reason:** Repository reconciliation confirms that Context Runtime assembly and runtime-control capabilities already exist, while their control outcomes are not yet integrated into the actual Agent Runtime execution lifecycle.

**Ownership:** Agent Runtime owns execution integration; Context Runtime owns context state and control.

**Transport:** Existing `AgentContext` / `AgentInvocationRequest` boundary is the natural integration surface.

**Constraint:** Frozen S4-011 evaluation, feedback, decision, execution, control, and refresh contracts remain upstream and must not be reimplemented downstream.

**Remaining blocker:** Define whether `REFRESH` affects the current execution, the next execution, or both.

**Task assignment:** Deferred until the remaining contract decision is frozen.

**Implementation authorization:** Not yet granted.

*End of Document*
