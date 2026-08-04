import pytest

from app.context_runtime.lifecycle import (
    DefaultContextLifecycleManager,
)
from app.context_runtime.models import (
    ContextAllocation,
    ContextBudget,
    ContextLifecycle,
    ContextRuntimeState,
)


def create_context() -> ContextRuntimeState:
    """
    Create default runtime context state.
    """

    return ContextRuntimeState(
        context_id="test-context-001",
        budget=ContextBudget(
            max_tokens=8000,
            allocation=ContextAllocation(
                system=1000,
                memory=2000,
                knowledge=3000,
                conversation=2000,
            ),
        ),
    )


def test_activate_context():
    """
    Verify context can be activated.
    """

    manager = DefaultContextLifecycleManager()

    context = create_context()

    result = manager.activate(
        context
    )

    assert result.lifecycle == ContextLifecycle.ACTIVE


def test_mark_context_stale():
    """
    Verify active context can become stale.
    """

    manager = DefaultContextLifecycleManager()

    context = create_context()

    manager.activate(
        context
    )

    result = manager.mark_stale(
        context
    )

    assert result.lifecycle == ContextLifecycle.STALE


def test_archive_context():
    """
    Verify active context can be archived.
    """

    manager = DefaultContextLifecycleManager()

    context = create_context()

    manager.activate(
        context
    )

    result = manager.archive(
        context
    )

    assert result.lifecycle == ContextLifecycle.ARCHIVED


def test_remove_context():
    """
    Verify archived context can be removed.
    """

    manager = DefaultContextLifecycleManager()

    context = create_context()

    manager.activate(
        context
    )

    manager.archive(
        context
    )

    result = manager.remove(
        context
    )

    assert result.lifecycle == ContextLifecycle.REMOVED


def test_invalid_transition():
    """
    Verify invalid lifecycle transition is rejected.
    """

    manager = DefaultContextLifecycleManager()

    context = create_context()

    context.lifecycle = ContextLifecycle.ARCHIVED

    with pytest.raises(ValueError):
        manager.mark_stale(
            context
        )
