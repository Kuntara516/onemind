# OneMind Sprint 4 — Context Intelligence

# HANDOFF-S4-011-006-CONTEXT-RUNTIME-CONTROL

**Sprint:** S4-011-006
**Title:** Context Runtime Decision Execution & Control
**Status:** ✅ COMPLETED — CONTRACT FROZEN
**Branch:** `feature/sprint4-context-intelligence`
**Baseline:** `v0.9.9-s4-context-decision-boundary`
**Baseline HEAD:** `799b7a9`
**Date:** 2026-08-09

---

## 1. Executive Summary

S4-011-006 completes the downstream runtime-control side of the Context Intelligence evaluation loop established by S4-011-005.

The phase consolidates three implementation boundaries:

1. Decision Execution Foundation
2. Default Context Refresh Engine
3. Runtime Decision → Refresh Control Integration

The resulting runtime path is:

```text
Context Evaluation
        ↓
Runtime Feedback
        ↓
Feedback Consumer
        ↓
Decision Boundary
        ↓
ContextRuntimeDecisionResult
        ↓
Decision Executor
        ↓
ContextRuntimeExecutionResult
        ↓
Decision Controller
        ↓
ContextRefreshEngine
        ↓
ContextRuntimeControlResult
        ↓
ContextRuntimeCoordinator
        ↓
Runtime State
```

The central architectural invariant is:

```text
Decision ≠ Execution ≠ Runtime State
```

Decision generation remains deterministic and side-effect free. Execution produces an explicit artifact. Runtime control applies that artifact. The coordinator remains the owner of runtime state.

---

## 2. Sprint Objective

The objective of S4-011-006 is to provide an explicit, testable, and bounded runtime-control layer capable of consuming the frozen `ContextRuntimeDecisionResult` produced by S4-011-005.

The phase must:

* translate a runtime decision into an execution artifact
* provide a dedicated refresh lifecycle implementation
* apply runtime decisions without moving evaluation logic into the control layer
* preserve runtime state ownership inside `ContextRuntimeCoordinator`
* preserve execution-artifact immutability
* keep context retrieval, ranking, selection, and evaluation outside runtime control

The phase must not collapse decision, execution, control, and state ownership into one component.

---

## 3. Architecture Position

S4-011-005 established the decision boundary:

```text
ContextRuntimeDecisionResult
        ↓
       STOP
```

S4-011-006 extends that boundary downstream:

```text
ContextRuntimeDecisionResult
        ↓
ContextRuntimeDecisionExecutor
        ↓
ContextRuntimeExecutionResult
        ↓
ContextRuntimeDecisionController
        ↓
ContextRefreshEngine
        ↓
ContextRuntimeControlResult
        ↓
ContextRuntimeCoordinator
```

The runtime-control layer is therefore a consumer of the frozen decision artifact. It must not bypass the evaluation or decision layers.

---

## 4. Subtasks

### 4.1 S4-011-006-001 — Decision Execution Foundation

**Status:** ✅ COMPLETED

Primary implementation:

```text
services/agent-runtime/app/context_runtime/evaluation/execution.py
```

Primary tests:

```text
services/agent-runtime/tests/test_context_runtime_decision_execution.py
```

Responsibilities:

* consume `ContextRuntimeDecisionResult`
* preserve evaluation identity
* map the decision to a runtime feedback action
* produce `ContextRuntimeExecutionResult`
* avoid executing refresh
* avoid mutating the decision artifact

The executor is intentionally an adapter, not an action executor.

Conceptually:

```text
ContextRuntimeDecisionResult
        ↓
ContextRuntimeDecisionExecutor
        ↓
ContextRuntimeExecutionResult
```

The execution artifact represents what should be executed, not proof that runtime state has already changed.

---

### 4.2 S4-011-006-002 — Default Context Refresh Engine

**Status:** ✅ COMPLETED

Primary implementation:

```text
services/agent-runtime/app/context_runtime/refresh.py
```

The `DefaultContextRefreshEngine` implements:

```text
should_refresh(state) -> bool
refresh(state) -> ContextRuntimeState
```

Responsibilities:

* determine refresh eligibility
* enforce `ContextRefreshPolicy`
* execute lifecycle-only refresh behavior
* update refresh timestamps
* delegate lifecycle transitions to `ContextLifecycleManager`

The refresh engine intentionally does not:

* retrieve context
* rank context
* select context
* modify context content
* evaluate context relevance
* invoke Agent Runtime

Refresh lifecycle behavior is:

```text
ACTIVE
  ↓
STALE
  ↓
ACTIVE
```

or, for an already stale state:

```text
STALE
  ↓
ACTIVE
```

`refresh()` is itself policy-guarded through `should_refresh()`. This keeps refresh-policy ownership inside the Refresh Engine rather than duplicating policy decisions in the control layer.

---

## 5. Runtime Decision Control Contract

Primary implementation:

```text
services/agent-runtime/app/context_runtime/control.py
```

The control layer consumes:

```text
ContextRuntimeExecutionResult
```

and returns:

```text
ContextRuntimeControlResult
```

The deterministic action mapping is:

| Runtime Decision | Control Action | Runtime Effect                     |
| ---------------- | -------------- | ---------------------------------- |
| `RETAIN`         | `RETAIN`       | explicit no-op                     |
| `REVIEW`         | `REVIEW`       | explicit no-op                     |
| `REFRESH`        | `REFRESH`      | delegate to `ContextRefreshEngine` |

The control layer does not reinterpret context quality. It does not calculate scores, create decisions, retrieve context, rank context, select context, or modify context content.

---

## 6. Runtime Control Result

`ContextRuntimeControlResult` is the runtime-control outcome artifact.

It preserves:

```text
evaluation_id
action
executed
state
```

The semantic distinction is:

```text
ContextRuntimeExecutionResult
    = requested runtime action

ContextRuntimeControlResult
    = outcome of applying that action to runtime state
```

This distinction must remain explicit.

The execution artifact must not be mutated to record runtime outcome.

---

## 7. Runtime State Ownership

`ContextRuntimeCoordinator` remains the sole owner of runtime context state.

The control layer receives the current state and returns a control result. The coordinator then stores the resulting state.

Conceptually:

```text
Decision Controller
        ↓
ContextRuntimeControlResult
        ↓
ContextRuntimeCoordinator
        ↓
self._context
```

The control layer must not become a second state owner.

This preserves the existing coordinator boundary established by earlier Context Runtime work.

---

## 8. Refresh Control Boundary

The following responsibility split is frozen:

```text
Decision Boundary
    = decides

Decision Executor
    = creates execution artifact

Decision Controller
    = applies runtime action

Refresh Engine
    = owns refresh eligibility + refresh lifecycle

Coordinator
    = owns runtime state
```

The controller must not call `should_refresh()` separately before calling `refresh()`.

The Refresh Engine owns that policy guard internally:

```text
DecisionController
        ↓
RefreshEngine.refresh()
        ↓
RefreshEngine.should_refresh()
        ↓
policy / lifecycle checks
        ↓
refresh lifecycle
```

This avoids duplicating refresh-policy ownership across components.

---

## 9. Explicit Non-Responsibilities

### 9.1 Evaluation

Runtime control must not calculate context quality scores or reinterpret evaluation results.

### 9.2 Feedback

Runtime control must not generate or consume runtime feedback to produce a new decision.

### 9.3 Decision Generation

Runtime control must not bypass `ContextRuntimeDecisionBoundary`.

### 9.4 Retrieval

Runtime control must not invoke `ContextRetriever`.

### 9.5 Ranking

Runtime control must not invoke or modify `ContextRanker`.

### 9.6 Selection

Runtime control must not invoke or modify `ContextSelector`.

### 9.7 Context Mutation

Runtime control must not modify the selected context contents.

### 9.8 Agent Execution

Runtime control must not invoke Agent Runtime execution as part of the decision-control contract.

---

## 10. Dependency Injection

The runtime-control components preserve dependency injection where appropriate.

The decision executor accepts a decision artifact directly.

The decision controller accepts a `ContextRefreshEngine` dependency, allowing deterministic testing and future replacement of refresh implementations without changing the control contract.

The coordinator therefore composes the runtime-control boundary rather than embedding refresh policy inside itself.

---

## 11. Deterministic Behavior

Given identical inputs and identical runtime policy/state, the following behavior must remain deterministic:

```text
RETAIN → no-op
REVIEW  → no-op
REFRESH → refresh engine delegation
```

The decision executor itself does not execute runtime actions.

The Refresh Engine owns policy evaluation and lifecycle transition behavior.

No external provider is required for the decision-control contract.

---

## 12. Immutability / Artifact Rules

The following artifacts must not be mutated as part of downstream control:

```text
ContextEvaluationResult
ContextRuntimeFeedbackResult
ContextRuntimeDecisionResult
ContextRuntimeExecutionResult
```

Runtime outcome belongs in:

```text
ContextRuntimeControlResult
```

This preserves provenance and makes the control boundary auditable.

---

## 13. Test Coverage

S4-011-006 is covered by the following focused integration surfaces:

```text
services/agent-runtime/tests/test_context_runtime_decision_execution.py
services/agent-runtime/tests/test_context_runtime_decision_control.py
services/agent-runtime/tests/test_context_runtime_decision_integration.py
services/agent-runtime/tests/test_context_runtime_refresh.py
services/agent-runtime/tests/test_context_runtime_integration.py
```

Coverage includes:

* RETAIN execution artifact creation
* REVIEW execution artifact creation
* REFRESH execution artifact creation
* evaluation identity preservation
* decision artifact non-mutation
* deterministic execution artifact creation
* refresh policy behavior
* refresh lifecycle transitions
* refresh delegation
* RETAIN no-op behavior
* REVIEW no-op behavior
* REFRESH runtime integration
* coordinator state ownership
* execution artifact non-mutation through runtime control

---

## 14. Integration Validation

The complete runtime path is validated as:

```text
Context Evaluation
      ↓
Runtime Feedback
      ↓
Decision Boundary
      ↓
Decision Execution
      ↓
Runtime Decision Control
      ↓
Refresh Engine
      ↓
Runtime Coordinator
```

The frozen baseline entering this handoff is:

```text
HEAD: 799b7a9
tag:  v0.9.9-s4-context-decision-boundary
branch: feature/sprint4-context-intelligence
working tree: clean
```

Focused decision/runtime integration validation:

```text
11 passed
```

Full regression:

```text
234 passed in 1.42s
```

No known test failures remain at the baseline used for this handoff.

---

## 15. Implementation History

Relevant implementation commits in the current S4-011 line:

```text
7a8cd01 feat: integrate decision execution with refresh control
3ad1240 feat: integrate decision controller with runtime coordinator
20493d8 fix: export runtime decision boundary contracts
799b7a9 test: add context runtime decision integration coverage
```

The preceding frozen decision-boundary release is:

```text
v0.9.9-s4-context-decision-boundary
```

The preceding observability release is:

```text
v0.9.8-s4-context-runtime-observability
```

---

## 16. Frozen Contracts

The following contracts are frozen at the S4-011-006 boundary.

### Decision Execution

```text
ContextRuntimeDecisionExecutor.execute(
    decision
) -> ContextRuntimeExecutionResult
```

### Refresh Engine

```text
ContextRefreshEngine.should_refresh(
    state
) -> bool

ContextRefreshEngine.refresh(
    state
) -> ContextRuntimeState
```

### Runtime Decision Control

```text
ContextRuntimeDecisionController.apply(
    execution,
    state
) -> ContextRuntimeControlResult
```

### Runtime Coordinator

```text
ContextRuntimeCoordinator.apply_decision(
    execution
) -> ContextRuntimeControlResult
```

The coordinator remains responsible for storing the returned runtime state.

---

## 17. Architectural Invariants

The following invariants are frozen:

**Invariant 1** — Evaluation remains independent from runtime control.

**Invariant 2** — Feedback remains independent from runtime execution.

**Invariant 3** — Decision generation remains deterministic and side-effect free.

**Invariant 4** — Decision execution creates an artifact and does not mutate the decision.

**Invariant 5** — Execution artifacts do not represent runtime state mutation.

**Invariant 6** — RETAIN is an explicit no-op.

**Invariant 7** — REVIEW is an explicit no-op.

**Invariant 8** — REFRESH is delegated to `ContextRefreshEngine`.

**Invariant 9** — Refresh policy ownership remains inside `ContextRefreshEngine`.

**Invariant 10** — Runtime control does not retrieve, rank, select, or evaluate context.

**Invariant 11** — Runtime control does not mutate context content.

**Invariant 12** — Runtime state remains owned by `ContextRuntimeCoordinator`.

**Invariant 13** — Execution artifacts remain unmodified after runtime control.

**Invariant 14** — Runtime control does not bypass the frozen Decision Boundary.

---

## 18. Sprint Completion Criteria

| Criterion                                                    | Status |
| ------------------------------------------------------------ | ------ |
| Decision execution contract implemented                      | ✅      |
| Execution artifact implemented                               | ✅      |
| Execution artifact does not execute refresh                  | ✅      |
| Default refresh engine implemented                           | ✅      |
| Refresh policy enforced inside refresh engine                | ✅      |
| Refresh lifecycle transitions delegated to lifecycle manager | ✅      |
| Runtime decision controller implemented                      | ✅      |
| RETAIN explicit no-op                                        | ✅      |
| REVIEW explicit no-op                                        | ✅      |
| REFRESH delegated to refresh engine                          | ✅      |
| Runtime state remains coordinator-owned                      | ✅      |
| Execution artifact remains unmodified                        | ✅      |
| Evaluation/retrieval/ranking/selection excluded from control | ✅      |
| Focused integration coverage                                 | ✅      |
| Full regression: 234 passed                                  | ✅      |
| Working tree baseline clean                                  | ✅      |
| Runtime Control contract consolidated                        | ✅      |
| Handoff documented                                           | ✅      |

---

## 19. Freeze Decision

S4-011-006 is considered **contract-complete and ready to freeze** at the current implementation boundary.

No implementation refactor is required solely for consolidation.

Future work must consume the frozen contracts rather than moving responsibilities backward into evaluation, feedback, decision generation, or execution artifacts.

The next phase may extend runtime behavior only through explicit downstream contracts.

---

## 20. Next Extension Point

The natural next extension after S4-011-006 is runtime-level integration beyond lifecycle refresh, if required by the Sprint 4 plan.

Any future phase must begin from:

```text
ContextRuntimeExecutionResult
        ↓
ContextRuntimeControlResult
        ↓
ContextRuntimeCoordinator
```

and must preserve the frozen ownership boundaries established here.

---

## 21. Final Status

S4-011-006 Context Runtime Decision Execution & Control is:

```text
✅ IMPLEMENTED
✅ TESTED
✅ INTEGRATED
✅ CONTRACT-CONSOLIDATED
✅ ARCHITECTURALLY BOUNDED
✅ READY TO FREEZE
```

The completed Context Intelligence runtime control path is:

```text
Context Evaluation
        ↓
Runtime Feedback
        ↓
Decision Boundary
        ↓
Decision Execution
        ↓
Runtime Decision Control
        ↓
Refresh Engine
        ↓
Runtime Coordinator
        ↓
RETAIN / REVIEW / REFRESH
```

The key OneMind boundary remains:

```text
Evaluation
    ≠
Feedback
    ≠
Decision
    ≠
Execution
    ≠
Control
    ≠
Runtime State
```

S4-011-006 therefore closes the Runtime Control contract without collapsing these responsibilities into a single runtime component.
