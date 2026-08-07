"""
Context Runtime Evaluation Integration Tests

Sprint:
    S4-011-002 Context Evaluation Integration

Coverage:

- SelectedContext evaluation lifecycle
- Evaluator dependency injection
- Metadata propagation
"""

from __future__ import annotations

from app.context_runtime.models import (
    ContextCandidate,
    SelectedContext,
)

from app.context_runtime.evaluation import (
    ContextEvaluationIntegration,
    ContextEvaluationResult,
)


class FakeEvaluator:
    """
    Fake evaluator for dependency injection test.
    """

    def __init__(self):
        self.called = False

    def evaluate(
        self,
        **kwargs,
    ):
        self.called = True

        return ContextEvaluationResult(
            retrieved_items=kwargs[
                "retrieved_items"
            ],
            selected_items=kwargs[
                "selected_items"
            ],
            metadata=kwargs.get(
                "metadata",
                {},
            ),
        )


def test_evaluation_integration_success():
    """
    Verify selected context evaluation.
    """

    context = SelectedContext(
        items=[
            ContextCandidate(
                context_id="ctx-001",
                content="hello",
            ),
            ContextCandidate(
                context_id="ctx-002",
                content="world",
            ),
        ],
        total_tokens=100,
    )

    integration = ContextEvaluationIntegration()

    result = integration.evaluate_context(
        context,
        execution_success=True,
    )

    assert isinstance(
        result,
        ContextEvaluationResult,
    )

    assert result.selected_items == 2
    assert result.retrieved_items == 2

    assert (
        "evaluation"
        in context.metadata
    )


def test_evaluation_integration_custom_evaluator():
    """
    Verify evaluator injection.
    """

    fake = FakeEvaluator()

    integration = ContextEvaluationIntegration(
        evaluator=fake,
    )

    context = SelectedContext(
        items=[
            ContextCandidate(
                context_id="ctx-test",
            )
        ],
        total_tokens=50,
    )

    result = integration.evaluate_context(
        context,
    )

    assert fake.called is True

    assert result.selected_items == 1


def test_evaluation_integration_metadata_propagation():
    """
    Verify evaluation metadata propagation.
    """

    context = SelectedContext(
        items=[
            ContextCandidate(
                context_id="ctx-meta",
            )
        ],
        total_tokens=20,
    )

    metadata = {
        "trace_id": "trace-001",
        "agent_id": "agent-001",
    }

    integration = ContextEvaluationIntegration()

    result = integration.evaluate_context(
        context,
        metadata=metadata,
    )

    assert result.metadata == metadata

    assert (
        "evaluation"
        in context.metadata
    )
    