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
    Create integration test budget.
    """

    return ContextBudget(
        max_tokens=10000,
        allocation=ContextAllocation(
            system=1000,
            memory=3000,
            knowledge=4000,
            conversation=2000,
        ),
    )


def test_full_context_runtime_flow():
    """
    Verify complete context runtime lifecycle:

    create
        ->
    activate
        ->
    consume
        ->
    archive
        ->
    remove
    """

    coordinator = ContextRuntimeCoordinator()

    context = coordinator.create_context(
        context_id="integration-context-001",
        budget=create_budget(),
    )

    assert context.context_id == (
        "integration-context-001"
    )

    assert context.lifecycle == (
        ContextLifecycle.CREATED
    )

    context = coordinator.activate_context()

    assert context.lifecycle == (
        ContextLifecycle.ACTIVE
    )

    coordinator.consume_tokens(
        4000
    )

    assert coordinator.remaining_budget() == (
        6000
    )

    context = coordinator.archive_context()

    assert context.lifecycle == (
        ContextLifecycle.ARCHIVED
    )

    context = coordinator.remove_context()

    assert context.lifecycle == (
        ContextLifecycle.REMOVED
    )


def test_context_budget_state_consistency():
    """
    Verify budget state remains consistent
    after multiple token consumptions.
    """

    coordinator = ContextRuntimeCoordinator()

    coordinator.create_context(
        context_id="budget-check-001",
        budget=create_budget(),
    )

    coordinator.activate_context()

    coordinator.consume_tokens(
        1000
    )

    coordinator.consume_tokens(
        2000
    )

    assert (
        coordinator.remaining_budget()
        == 7000
    )


def test_context_lifecycle_requires_valid_order():
    """
    Verify lifecycle protection.

    Context cannot archive before activation.
    """

    coordinator = ContextRuntimeCoordinator()

    coordinator.create_context(
        context_id="invalid-flow-001",
        budget=create_budget(),
    )

    try:
        coordinator.archive_context()

    except ValueError:
        assert True

    else:
        assert False, (
            "Expected invalid lifecycle transition"
        )


def test_context_missing_runtime_rejected():
    """
    Verify coordinator rejects operations
    without runtime context.
    """

    coordinator = ContextRuntimeCoordinator()

    try:
        coordinator.consume_tokens(
            100
        )

    except RuntimeError:
        assert True

    else:
        assert False, (
            "Expected missing context error"
        )


def test_context_retrieval():
    """
    Verify current context retrieval.
    """

    coordinator = ContextRuntimeCoordinator()

    created = coordinator.create_context(
        context_id="retrieve-001",
        budget=create_budget(),
    )

    current = coordinator.get_context()

    assert current is created
    assert current.context_id == (
        "retrieve-001"
    )
