# HANDOFF-S4-007-003-CONTEXT-SELECTOR

## OneMind Context Intelligence

Sprint:
- S4 Context Intelligence & Retrieval Pipeline

Phase:
- S4-007 Context Intelligence Pipeline

Task:
- S4-007-003 Context Selector

Status:
- FROZEN

Date:
- 2026-08-05


---

# 1. Overview

S4-007-003 implements the Context Selection Layer.

The purpose of Context Selector is to transform ranked context candidates into the final context package consumed by downstream runtime components.

The selection layer is responsible for:

- applying selection policies
- enforcing context budget constraints
- filtering low-value candidates
- preserving ranking priority
- producing deterministic selected context output


The completed pipeline:

```
User Query
    |
    v
Context Retriever
    |
    v
ContextCandidate[]
    |
    v
Context Ranker
    |
    v
Ranked ContextCandidate[]
    |
    v
Context Selector
    |
    v
SelectedContext
    |
    v
Agent Runtime
```


---

# 2. Scope

## Included

Implemented:

- Context selection policy model
- Default context selector implementation
- SelectedContext runtime model
- Selector unit tests
- Ranker → Selector integration validation


## Excluded

Not implemented:

- LLM based context compression
- Dynamic selection policy generation
- Multi-agent context negotiation
- Long-term context assembly strategy
- Context summarization


These belong to future Context Intelligence phases.


---

# 3. Architecture

## Context Selection Flow


```
                Ranked Candidates

                      |
                      v

        +-----------------------------+
        |    DefaultContextSelector   |
        +-----------------------------+

                      |
        +-------------+-------------+
        |             |             |
        v             v             v

   Min Score     Max Items     Token Budget

                      |
                      v

              SelectedContext
```


---

# 4. Implemented Components


## 4.1 Selection Policy

File:

```
services/agent-runtime/app/context_runtime/policies.py
```


Purpose:

Defines deterministic selection constraints.


Responsibilities:

- minimum relevance threshold
- maximum selected items
- maximum token budget


Example:

```python
SelectionPolicy(
    min_score=0.5,
    max_items=5,
    max_tokens=2000,
)
```


---

## 4.2 Context Selector

File:

```
services/agent-runtime/app/context_runtime/selector.py
```


Implementation:

```
DefaultContextSelector
```


Responsibilities:

- consume ranked ContextCandidate list
- apply SelectionPolicy
- stop when token budget is exceeded
- produce SelectedContext


Selection algorithm:

```
for candidate in ranked_candidates:

    check minimum score

    check max items

    check token budget

    append candidate

return SelectedContext
```


---

## 4.3 Runtime Models

File:

```
services/agent-runtime/app/context_runtime/models.py
```


Added:

```
SelectedContext
```


Purpose:

Represents final selected context package.


Contains:

- selected items
- total tokens
- total score
- selection metadata


Example:

```python
SelectedContext(
    items=[...],
    total_tokens=1200,
    total_score=0.87,
    metadata={
        "selector": "default"
    }
)
```


---

# 5. Test Coverage


## Unit Tests

File:

```
services/agent-runtime/tests/test_context_selector.py
```


Coverage:


## Selection Limit

Test:

```
test_select_top_k
```

Validates:

- max_items enforcement


---

## Minimum Score Filtering

Test:

```
test_filter_min_score
```

Validates:

- low relevance candidates are removed


---

## Token Budget Enforcement

Test:

```
test_select_by_token_budget
```

Validates:

- selector stops when budget is exceeded


---

## Rank Preservation

Test:

```
test_preserve_rank_order
```

Validates:

- selector does not reorder ranked candidates


---

## Metadata Output

Test:

```
test_return_selection_metadata
```

Validates:

- selection metadata is exposed


---

# 6. Pipeline Integration Validation


File:

```
services/agent-runtime/tests/test_context_selection_pipeline.py
```


Validated flow:


```
ContextCandidate

        |
        v

DefaultContextRanker

        |
        v

Ranked Candidates

        |
        v

DefaultContextSelector

        |
        v

SelectedContext
```


Tests:


## Ranker → Selector Pipeline

```
test_ranker_to_selector_pipeline
```


## Budget Enforcement

```
test_pipeline_respects_selection_budget
```


## Ordering Preservation

```
test_pipeline_preserves_rank_priority
```


## Final Context Package

```
test_pipeline_returns_context_package
```


Result:

```
4 passed
```


---

# 7. Git History


## Selection Policy Foundation

Commit:

```
b15e978 feat: add context selection policy foundation
```


Files:

```
services/agent-runtime/app/context_runtime/policies.py
```


---

## Default Selector Implementation

Commit:

```
e168953 feat: implement default context selector
```


Files:

```
services/agent-runtime/app/context_runtime/selector.py
```


---

## Selector Tests

Commit:

```
ca13218 test: align context selector tests with runtime models
```


Files:

```
services/agent-runtime/tests/test_context_selector.py
```


---

## Pipeline Integration Test

Commit:

```
<pending>
```


Files:

```
services/agent-runtime/tests/test_context_selection_pipeline.py
```


---

# 8. Current Context Runtime State


Completed:

```
S4-007-001 Context Retriever
        |
        v
S4-007-002 Context Ranker
        |
        v
S4-007-003 Context Selector
```


Status:

```
Retriever       ✅ Frozen
Ranker          ✅ Frozen
Selector        ✅ Frozen
```


---

# 9. Design Decisions


## Deterministic Selection First

The first implementation intentionally avoids LLM-based decisions.

Reasons:

- predictable behavior
- easy testing
- controllable token budget
- stable runtime performance


Future versions may introduce:

- learned ranking signals
- LLM reranking
- adaptive policies


---

## Selector Does Not Re-Rank

Selector responsibility:

```
Filter + Allocate
```


Not:

```
Rank + Score
```


Ranking remains owned by Context Ranker.


---

## Budget Is Enforced At Selection Boundary

Reason:

Context budget should be enforced before context enters Agent Runtime.

This prevents:

- token overflow
- uncontrolled context growth
- runtime instability


---

# 10. Next Recommended Phase


Next:

```
S4-007-004 Context Assembly
```


Objectives:

- combine SelectedContext with runtime prompt context
- integrate memory + knowledge + conversation context
- prepare final context payload for Agent execution


---

# End of Handoff

S4-007-003 Context Selector is frozen.

The Context Intelligence pipeline now supports:

Retrieve → Rank → Select

as a deterministic runtime pipeline.
```