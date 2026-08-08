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


class FakeFeedback:
    """
    Fake runtime feedback generator for dependency injection test.
    """

    def __init__(self):
        self.called = False
        self.received_evaluation = None

    def generate(self, evaluation):
        self.called = True
        self.received_evaluation = evaluation

        from app.context_runtime.evaluation import (
            ContextRuntimeFeedbackResult,
            ContextFeedbackAction,
            ContextFeedbackSignal,
            ContextQualityLevel,
        )

        return ContextRuntimeFeedbackResult(
            evaluation_id=evaluation.evaluation_id,
            quality_level=ContextQualityLevel.EXCELLENT,
            feedback_signal=ContextFeedbackSignal.RETAIN,
            recommended_action=ContextFeedbackAction.RETAIN,
            overall_score=evaluation.score.overall_score,
        )


def test_evaluation_integration_generates_runtime_feedback():
    """
    Verify evaluation results can be converted into runtime feedback.
    """

    context = SelectedContext(
        items=[
            ContextCandidate(
                context_id="ctx-feedback-001",
                content="hello",
            ),
            ContextCandidate(
                context_id="ctx-feedback-002",
                content="world",
            ),
        ],
        total_tokens=100,
    )

    integration = ContextEvaluationIntegration()

    evaluation = integration.evaluate_context(
        context,
        execution_success=True,
    )

    feedback = integration.generate_feedback(
        evaluation,
    )

    from app.context_runtime.evaluation import (
        ContextFeedbackSignal,
        ContextQualityLevel,
        ContextRuntimeFeedbackResult,
    )

    assert isinstance(
        feedback,
        ContextRuntimeFeedbackResult,
    )

    assert feedback.evaluation_id == (
        evaluation.evaluation_id
    )

    assert feedback.overall_score == (
        evaluation.score.overall_score
    )

    assert feedback.quality_level == (
        ContextQualityLevel.EXCELLENT
    )

    assert feedback.feedback_signal == (
        ContextFeedbackSignal.RETAIN
    )


def test_evaluation_integration_feedback_dependency_injection():
    """
    Verify runtime feedback dependency injection.
    """

    fake_feedback = FakeFeedback()

    integration = ContextEvaluationIntegration(
        feedback=fake_feedback,
    )

    context = SelectedContext(
        items=[
            ContextCandidate(
                context_id="ctx-feedback-di",
            )
        ],
        total_tokens=50,
    )

    evaluation = integration.evaluate_context(
        context,
    )

    feedback = integration.generate_feedback(
        evaluation,
    )

    assert fake_feedback.called is True

    assert (
        fake_feedback.received_evaluation
        is evaluation
    )

    assert feedback.evaluation_id == (
        evaluation.evaluation_id
    )


def test_evaluation_integration_preserves_existing_evaluation_contract():
    """
    Verify S4-011-002 evaluation behavior remains unchanged.
    """

    context = SelectedContext(
        items=[
            ContextCandidate(
                context_id="ctx-contract-001",
                content="hello",
            ),
            ContextCandidate(
                context_id="ctx-contract-002",
                content="world",
            ),
        ],
        total_tokens=100,
    )

    metadata = {
        "trace_id": "trace-feedback-001",
        "agent_id": "agent-feedback-001",
    }

    integration = ContextEvaluationIntegration()

    evaluation = integration.evaluate_context(
        context,
        execution_success=True,
        metadata=metadata,
    )

    assert isinstance(
        evaluation,
        ContextEvaluationResult,
    )

    assert evaluation.retrieved_items == 2
    assert evaluation.selected_items == 2
    assert evaluation.metadata == metadata

    assert "evaluation" in context.metadata

    feedback = integration.generate_feedback(
        evaluation,
    )

    assert feedback.evaluation_id == (
        evaluation.evaluation_id
    )

    assert evaluation.retrieved_items == 2
    assert evaluation.selected_items == 2
    assert evaluation.metadata == metadata
