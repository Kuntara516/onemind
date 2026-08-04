"""
Tests for context runtime retriever.
"""

import pytest

from app.context_runtime.models import (
    ContextAllocation,
    ContextBudget,
    ContextLifecycle,
)
from app.context_runtime.coordinator import ContextRuntimeCoordinator
from app.context_runtime.retriever import DefaultContextRetriever


def create_budget() -> ContextBudget:
    """
    Create test context budget.
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


def test_retrieve_created_context():
    """
    Verify retriever can retrieve created context.
    """

    coordinator = ContextRuntimeCoordinator()

    created = coordinator.create_context(
        context_id="retrieve-created-001",
        budget=create_budget(),
    )

    retriever = DefaultContextRetriever(
        coordinator=coordinator,
    )

    context = retriever.get_context(
        "retrieve-created-001"
    )

    assert context is not None
    assert context.context_id == (
        created.context_id
    )

    assert context.lifecycle == (
        ContextLifecycle.CREATED
    )


def test_retrieve_active_context():
    """
    Verify retriever returns active context.
    """

    coordinator = ContextRuntimeCoordinator()

    coordinator.create_context(
        context_id="retrieve-active-001",
        budget=create_budget(),
    )

    coordinator.activate_context()

    retriever = DefaultContextRetriever(
        coordinator=coordinator,
    )

    context = retriever.get_context(
        "retrieve-active-001"
    )

    assert context.lifecycle == (
        ContextLifecycle.ACTIVE
    )


def test_retrieve_missing_context():
    """
    Verify missing context returns None.
    """

    coordinator = ContextRuntimeCoordinator()

    retriever = DefaultContextRetriever(
        coordinator=coordinator,
    )

    context = retriever.get_context(
        "missing-context-001"
    )

    assert context is None


def test_retrieve_current_context():
    """
    Verify current context retrieval.
    """

    coordinator = ContextRuntimeCoordinator()

    coordinator.create_context(
        context_id="current-context-001",
        budget=create_budget(),
    )

    coordinator.activate_context()

    retriever = DefaultContextRetriever(
        coordinator=coordinator,
    )

    context = retriever.get_current()

    assert context is not None
    assert context.context_id == (
        "current-context-001"
    )

    assert context.lifecycle == (
        ContextLifecycle.ACTIVE
    )


def test_retrieve_context_after_token_consumption():
    """
    Verify retrieved context keeps budget state.
    """

    coordinator = ContextRuntimeCoordinator()

    coordinator.create_context(
        context_id="budget-context-001",
        budget=create_budget(),
    )

    coordinator.activate_context()

    coordinator.consume_tokens(
        2500
    )

    retriever = DefaultContextRetriever(
        coordinator=coordinator,
    )

    context = retriever.get_current()

    assert context is not None

    assert context.budget.used_tokens == (
        2500
    )

    assert context.budget.remaining_tokens == (
        7500
    )
