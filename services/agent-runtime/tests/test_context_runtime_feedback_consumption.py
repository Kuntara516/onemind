"""
Tests for Context Runtime Feedback Consumption.

Sprint:
S4-011-004 Feedback Consumer

Validates the end-to-end decision boundary:

    Context Evaluation
        ↓
    Runtime Feedback
        ↓
    Feedback Consumer
        ↓
    Runtime Decision

The consumer must remain a decision-only component.
It must not mutate evaluation or feedback artifacts,
perform context retrieval, or execute refresh operations.
"""

from uuid import UUID

from app.context_runtime.evaluation import (
    ContextEvaluationResult,
    ContextQualityScore,
    ContextRuntimeDecision,
    ContextRuntimeFeedback,
    ContextRuntimeFeedbackConsumer,
)
from app.context_runtime.models import ContextRefreshPolicy


EVALUATION_ID = UUID(
    "00000000-0000-0000-0000-000000000001"
)


def make_evaluation(
    overall_score: float,
) -> ContextEvaluationResult:
    """Create a deterministic evaluation result for integration tests."""

    return ContextEvaluationResult(
        evaluation_id=EVALUATION_ID,
        score=ContextQualityScore(
            overall_score=overall_score,
        ),
        retrieved_items=1,
        selected_items=1,
    )


def test_evaluation_to_feedback_to_retain_decision():
    """High-quality evaluation must produce a RETAIN decision."""

    evaluation = make_evaluation(0.90)

    feedback = ContextRuntimeFeedback().generate(
        evaluation
    )

    consumer = ContextRuntimeFeedbackConsumer()

    decision = consumer.consume(feedback)

    assert decision == ContextRuntimeDecision.RETAIN


def test_evaluation_to_feedback_to_review_decision():
    """Degraded evaluation must produce a REVIEW decision."""

    evaluation = make_evaluation(0.50)

    feedback = ContextRuntimeFeedback().generate(
        evaluation
    )

    consumer = ContextRuntimeFeedbackConsumer()

    decision = consumer.consume(feedback)

    assert decision == ContextRuntimeDecision.REVIEW


def test_evaluation_to_feedback_to_refresh_decision():
    """Poor evaluation must produce a REFRESH decision."""

    evaluation = make_evaluation(0.20)

    feedback = ContextRuntimeFeedback().generate(
        evaluation
    )

    consumer = ContextRuntimeFeedbackConsumer()

    decision = consumer.consume(feedback)

    assert decision == ContextRuntimeDecision.REFRESH


def test_refresh_feedback_respects_disabled_refresh_policy():
    """Disabled refresh policy must downgrade REFRESH to REVIEW."""

    evaluation = make_evaluation(0.20)

    feedback = ContextRuntimeFeedback().generate(
        evaluation
    )

    consumer = ContextRuntimeFeedbackConsumer(
        refresh_policy=ContextRefreshPolicy(
            enabled=False,
        )
    )

    decision = consumer.consume(feedback)

    assert decision == ContextRuntimeDecision.REVIEW


def test_feedback_consumption_preserves_evaluation_identity():
    """Feedback consumption must preserve the originating evaluation ID."""

    evaluation = make_evaluation(0.90)

    feedback = ContextRuntimeFeedback().generate(
        evaluation
    )

    assert feedback.evaluation_id == EVALUATION_ID

    consumer = ContextRuntimeFeedbackConsumer()

    consumer.consume(feedback)

    assert feedback.evaluation_id == EVALUATION_ID


def test_feedback_consumption_does_not_mutate_feedback():
    """Consumer must not mutate the frozen feedback artifact."""

    evaluation = make_evaluation(0.20)

    feedback = ContextRuntimeFeedback().generate(
        evaluation
    )

    original_feedback = feedback.model_copy(
        deep=True
    )

    consumer = ContextRuntimeFeedbackConsumer()

    decision = consumer.consume(feedback)

    assert decision == ContextRuntimeDecision.REFRESH
    assert feedback == original_feedback


def test_feedback_consumer_is_deterministic():
    """Repeated consumption of the same feedback must yield the same decision."""

    evaluation = make_evaluation(0.50)

    feedback = ContextRuntimeFeedback().generate(
        evaluation
    )

    consumer = ContextRuntimeFeedbackConsumer()

    first = consumer.consume(feedback)
    second = consumer.consume(feedback)

    assert first == ContextRuntimeDecision.REVIEW
    assert second == ContextRuntimeDecision.REVIEW
    assert first == second


def test_refresh_decision_is_not_refresh_execution():
    """
    REFRESH consumption produces only a decision.

    The consumer must not execute context refresh itself.
    """

    evaluation = make_evaluation(0.20)

    feedback = ContextRuntimeFeedback().generate(
        evaluation
    )

    consumer = ContextRuntimeFeedbackConsumer()

    decision = consumer.consume(feedback)

    assert decision == ContextRuntimeDecision.REFRESH
    assert feedback.recommended_action.value == "refresh"


def test_consumer_uses_explicit_refresh_policy():
    """Consumer must honor the explicitly supplied refresh policy."""

    evaluation = make_evaluation(0.20)

    feedback = ContextRuntimeFeedback().generate(
        evaluation
    )

    enabled_consumer = ContextRuntimeFeedbackConsumer(
        refresh_policy=ContextRefreshPolicy(
            enabled=True,
        )
    )

    disabled_consumer = ContextRuntimeFeedbackConsumer(
        refresh_policy=ContextRefreshPolicy(
            enabled=False,
        )
    )

    assert (
        enabled_consumer.consume(feedback)
        == ContextRuntimeDecision.REFRESH
    )

    assert (
        disabled_consumer.consume(feedback)
        == ContextRuntimeDecision.REVIEW
    )