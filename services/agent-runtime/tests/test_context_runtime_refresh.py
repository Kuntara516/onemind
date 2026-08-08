"""
Tests for Default Context Refresh Engine.

Sprint:
S4-011-006-002 Default Context Refresh Engine

Validates:

Context Runtime State
        ↓
Refresh Policy
        ↓
Default Context Refresh Engine
        ↓
Lifecycle Refresh
"""

from datetime import datetime, timedelta, timezone

from app.context_runtime.models import (
    ContextBudget,
    ContextLifecycle,
    ContextRefreshPolicy,
    ContextRuntimeState,
)
from app.context_runtime.refresh import (
    DefaultContextRefreshEngine,
)


def make_state(
    *,
    lifecycle: ContextLifecycle = ContextLifecycle.ACTIVE,
    created_at: datetime | None = None,
    last_refresh: datetime | None = None,
) -> ContextRuntimeState:
    """
    Create deterministic runtime state for refresh tests.
    """

    return ContextRuntimeState(
        context_id="ctx-refresh-test",
        lifecycle=lifecycle,
        budget=ContextBudget(
            max_tokens=16000,
        ),
        created_at=(
            created_at
            or datetime.now(timezone.utc)
        ),
        last_refresh=last_refresh,
    )


def test_refresh_engine_defaults_to_enabled_policy():
    engine = DefaultContextRefreshEngine()

    assert engine.policy.enabled is True
    assert engine.policy.max_age_seconds == 3600
    assert engine.policy.refresh_interval_seconds == 300


def test_should_refresh_returns_false_when_disabled():
    engine = DefaultContextRefreshEngine(
        policy=ContextRefreshPolicy(
            enabled=False,
        )
    )

    state = make_state()

    assert engine.should_refresh(state) is False


def test_should_refresh_returns_false_for_archived_context():
    engine = DefaultContextRefreshEngine()

    state = make_state(
        lifecycle=ContextLifecycle.ARCHIVED,
    )

    assert engine.should_refresh(state) is False


def test_should_refresh_returns_false_for_removed_context():
    engine = DefaultContextRefreshEngine()

    state = make_state(
        lifecycle=ContextLifecycle.REMOVED,
    )

    assert engine.should_refresh(state) is False


def test_should_refresh_returns_true_for_stale_context():
    engine = DefaultContextRefreshEngine()

    state = make_state(
        lifecycle=ContextLifecycle.STALE,
    )

    assert engine.should_refresh(state) is True


def test_should_refresh_uses_max_age_when_never_refreshed():
    engine = DefaultContextRefreshEngine(
        policy=ContextRefreshPolicy(
            max_age_seconds=60,
            refresh_interval_seconds=300,
        )
    )

    state = make_state(
        created_at=(
            datetime.now(timezone.utc)
            - timedelta(seconds=61)
        ),
    )

    assert engine.should_refresh(state) is True


def test_should_refresh_returns_false_for_fresh_context():
    engine = DefaultContextRefreshEngine(
        policy=ContextRefreshPolicy(
            max_age_seconds=3600,
            refresh_interval_seconds=300,
        )
    )

    state = make_state(
        created_at=(
            datetime.now(timezone.utc)
            - timedelta(seconds=30)
        ),
    )

    assert engine.should_refresh(state) is False


def test_should_refresh_uses_refresh_interval_after_first_refresh():
    engine = DefaultContextRefreshEngine(
        policy=ContextRefreshPolicy(
            max_age_seconds=3600,
            refresh_interval_seconds=300,
        )
    )

    state = make_state(
        created_at=(
            datetime.now(timezone.utc)
            - timedelta(seconds=100)
        ),
        last_refresh=(
            datetime.now(timezone.utc)
            - timedelta(seconds=301)
        ),
    )

    assert engine.should_refresh(state) is True


def test_should_refresh_returns_false_before_refresh_interval():
    engine = DefaultContextRefreshEngine(
        policy=ContextRefreshPolicy(
            max_age_seconds=3600,
            refresh_interval_seconds=300,
        )
    )

    state = make_state(
        created_at=(
            datetime.now(timezone.utc)
            - timedelta(seconds=100)
        ),
        last_refresh=(
            datetime.now(timezone.utc)
            - timedelta(seconds=100)
        ),
    )

    assert engine.should_refresh(state) is False


def test_should_refresh_uses_max_age_even_after_previous_refresh():
    engine = DefaultContextRefreshEngine(
        policy=ContextRefreshPolicy(
            max_age_seconds=3600,
            refresh_interval_seconds=300,
        )
    )

    state = make_state(
        created_at=(
            datetime.now(timezone.utc)
            - timedelta(seconds=4000)
        ),
        last_refresh=(
            datetime.now(timezone.utc)
            - timedelta(seconds=4000)
        ),
    )

    assert engine.should_refresh(state) is True


def test_refresh_stale_context_returns_active():
    engine = DefaultContextRefreshEngine()

    state = make_state(
        lifecycle=ContextLifecycle.STALE,
    )

    result = engine.refresh(state)

    assert result.lifecycle == ContextLifecycle.ACTIVE


def test_refresh_stale_context_updates_last_refresh():
    engine = DefaultContextRefreshEngine()

    before = datetime.now(timezone.utc)

    state = make_state(
        lifecycle=ContextLifecycle.STALE,
    )

    result = engine.refresh(state)

    after = datetime.now(timezone.utc)

    assert result.last_refresh is not None
    assert before <= result.last_refresh <= after


def test_refresh_stale_context_updates_updated_at():
    engine = DefaultContextRefreshEngine()

    before = datetime.now(timezone.utc)

    state = make_state(
        lifecycle=ContextLifecycle.STALE,
    )

    result = engine.refresh(state)

    after = datetime.now(timezone.utc)

    assert before <= result.updated_at <= after


def test_refresh_active_expired_context_transitions_through_stale():
    engine = DefaultContextRefreshEngine(
        policy=ContextRefreshPolicy(
            max_age_seconds=60,
        )
    )

    state = make_state(
        lifecycle=ContextLifecycle.ACTIVE,
        created_at=(
            datetime.now(timezone.utc)
            - timedelta(seconds=61)
        ),
    )

    result = engine.refresh(state)

    assert result.lifecycle == ContextLifecycle.ACTIVE
    assert result.last_refresh is not None


def test_refresh_does_not_execute_when_not_due():
    engine = DefaultContextRefreshEngine(
        policy=ContextRefreshPolicy(
            max_age_seconds=3600,
            refresh_interval_seconds=300,
        )
    )

    state = make_state(
        lifecycle=ContextLifecycle.ACTIVE,
        created_at=(
            datetime.now(timezone.utc)
            - timedelta(seconds=30)
        ),
    )

    original_last_refresh = state.last_refresh
    original_updated_at = state.updated_at

    result = engine.refresh(state)

    assert result.lifecycle == ContextLifecycle.ACTIVE
    assert result.last_refresh == original_last_refresh
    assert result.updated_at == original_updated_at


def test_refresh_disabled_policy_does_not_mutate_state():
    engine = DefaultContextRefreshEngine(
        policy=ContextRefreshPolicy(
            enabled=False,
        )
    )

    state = make_state(
        lifecycle=ContextLifecycle.STALE,
    )

    original = state.model_copy(
        deep=True
    )

    result = engine.refresh(state)

    assert result == original


def test_refresh_archived_context_does_not_mutate_state():
    engine = DefaultContextRefreshEngine()

    state = make_state(
        lifecycle=ContextLifecycle.ARCHIVED,
    )

    original = state.model_copy(
        deep=True
    )

    result = engine.refresh(state)

    assert result == original


def test_refresh_removed_context_does_not_mutate_state():
    engine = DefaultContextRefreshEngine()

    state = make_state(
        lifecycle=ContextLifecycle.REMOVED,
    )

    original = state.model_copy(
        deep=True
    )

    result = engine.refresh(state)

    assert result == original


def test_refresh_preserves_context_identity():
    engine = DefaultContextRefreshEngine()

    state = make_state(
        lifecycle=ContextLifecycle.STALE,
    )

    result = engine.refresh(state)

    assert result.context_id == "ctx-refresh-test"


def test_refresh_preserves_budget():
    engine = DefaultContextRefreshEngine()

    state = make_state(
        lifecycle=ContextLifecycle.STALE,
    )

    original_budget = state.budget.model_copy(
        deep=True
    )

    result = engine.refresh(state)

    assert result.budget == original_budget


def test_refresh_is_deterministic_in_lifecycle_result():
    engine = DefaultContextRefreshEngine()

    first_state = make_state(
        lifecycle=ContextLifecycle.STALE,
    )

    second_state = make_state(
        lifecycle=ContextLifecycle.STALE,
    )

    first = engine.refresh(first_state)
    second = engine.refresh(second_state)

    assert first.lifecycle == second.lifecycle
    assert first.context_id == second.context_id
    assert first.budget == second.budget
