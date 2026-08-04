from datetime import datetime

import pytest
from pydantic import ValidationError

from app.context_runtime.models import (
    ContextAllocation,
    ContextBudget,
    ContextLifecycle,
    ContextRefreshPolicy,
    ContextRuntimeState,
)


def test_context_allocation_defaults():
    allocation = ContextAllocation()

    assert allocation.system == 0
    assert allocation.memory == 0
    assert allocation.knowledge == 0
    assert allocation.conversation == 0
    assert allocation.reserved == 0


def test_context_budget_creation():
    budget = ContextBudget(
        max_tokens=16000,
        allocation=ContextAllocation(
            system=2000,
            memory=4000,
            knowledge=6000,
            conversation=4000,
        ),
    )

    assert budget.max_tokens == 16000
    assert budget.used_tokens == 0
    assert budget.allocation.memory == 4000
    assert budget.allocation.knowledge == 6000


def test_context_runtime_state_defaults():
    state = ContextRuntimeState(
        context_id="ctx-test-001",
        budget=ContextBudget(max_tokens=16000),
    )

    assert state.context_id == "ctx-test-001"
    assert state.lifecycle == ContextLifecycle.ACTIVE
    assert state.importance_score == 1.0
    assert state.last_refresh is None
    assert isinstance(state.created_at, datetime)


def test_context_refresh_policy_defaults():
    policy = ContextRefreshPolicy()

    assert policy.enabled is True
    assert policy.relevance_threshold == 0.6
    assert policy.refresh_interval_seconds == 300


def test_context_lifecycle_enum():
    assert ContextLifecycle.ACTIVE.value == "active"
    assert ContextLifecycle.STALE.value == "stale"
    assert ContextLifecycle.ARCHIVED.value == "archived"
    assert ContextLifecycle.REMOVED.value == "removed"


def test_invalid_token_budget():
    with pytest.raises(ValidationError):
        ContextBudget(
            max_tokens=0,
        )


def test_invalid_relevance_threshold():
    with pytest.raises(ValidationError):
        ContextRefreshPolicy(
            relevance_threshold=1.5,
        )
