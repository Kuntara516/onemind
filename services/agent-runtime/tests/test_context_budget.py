import pytest

from app.context_runtime.budget import (
    DefaultContextBudgetManager,
)
from app.context_runtime.models import (
    ContextAllocation,
    ContextBudget,
)


def create_budget() -> ContextBudget:
    return ContextBudget(
        max_tokens=8000,
        allocation=ContextAllocation(
            system=1000,
            memory=2000,
            knowledge=3000,
            conversation=2000,
        ),
    )


def test_manager_allocate():

    manager = DefaultContextBudgetManager()

    result = manager.allocate(
        create_budget()
    )

    assert result.max_tokens == 8000
    assert result.used_tokens == 0


def test_manager_consume_tokens():

    manager = DefaultContextBudgetManager()

    manager.allocate(
        create_budget()
    )

    result = manager.consume(
        3000
    )

    assert result.used_tokens == 3000


def test_manager_remaining_tokens():

    manager = DefaultContextBudgetManager()

    manager.allocate(
        create_budget()
    )

    manager.consume(
        3000
    )

    assert manager.remaining() == 5000


def test_manager_consume_over_budget():

    manager = DefaultContextBudgetManager()

    manager.allocate(
        create_budget()
    )

    with pytest.raises(ValueError):
        manager.consume(
            9000
        )


def test_manager_negative_consume():

    manager = DefaultContextBudgetManager()

    manager.allocate(
        create_budget()
    )

    with pytest.raises(ValueError):
        manager.consume(
            -1
        )
