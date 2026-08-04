import pytest

from app.context_runtime.coordinator import (
    ContextRuntimeCoordinator,
)
from app.context_runtime.models import (
    ContextAllocation,
    ContextBudget,
    ContextLifecycle,
)


def create_budget() -> ContextBudget:
    """
    Create default context budget.
    """

    return ContextBudget(
        max_tokens=8000,
        allocation=ContextAllocation(
            system=1000,
            memory=2000,
            knowledge=3000,
            conversation=2000,
        ),
    )


def test_create_context():
    """
    Verify context creation.
    """

    coordinator = ContextRuntimeCoordinator()

    context = coordinator.create_context(
        context_id="context-001",
        budget=create_budget(),
    )

    assert context.context_id == "context-001"
    assert context.budget.max_tokens == 8000


def test_activate_context():
    """
    Verify context activation through coordinator.
    """

    coordinator = ContextRuntimeCoordinator()

    coordinator.create_context(
        context_id="context-001",
        budget=create_budget(),
    )

    context = coordinator.activate_context()

    assert context.lifecycle == ContextLifecycle.ACTIVE


def test_consume_tokens():
    """
    Verify token consumption is delegated
    through coordinator.
    """

    coordinator = ContextRuntimeCoordinator()

    coordinator.create_context(
        context_id="context-001",
        budget=create_budget(),
    )

    coordinator.consume_tokens(
        3000
    )

    assert (
        coordinator.remaining_budget()
        == 5000
    )


def test_archive_context():
    """
    Verify context archive flow.
    """

    coordinator = ContextRuntimeCoordinator()

    coordinator.create_context(
        context_id="context-001",
        budget=create_budget(),
    )

    coordinator.activate_context()

    context = coordinator.archive_context()

    assert context.lifecycle == ContextLifecycle.ARCHIVED


def test_remove_context():
    """
    Verify context removal flow.
    """

    coordinator = ContextRuntimeCoordinator()

    coordinator.create_context(
        context_id="context-001",
        budget=create_budget(),
    )

    coordinator.activate_context()

    coordinator.archive_context()

    context = coordinator.remove_context()

    assert context.lifecycle == ContextLifecycle.REMOVED


def test_operation_without_context():
    """
    Verify coordinator rejects operations
    without created context.
    """

    coordinator = ContextRuntimeCoordinator()

    with pytest.raises(RuntimeError):
        coordinator.activate_context()
