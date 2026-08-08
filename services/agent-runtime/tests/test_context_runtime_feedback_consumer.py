"""
Tests for Context Runtime Feedback Consumer.

Sprint:
S4-011-004 Feedback Consumer
"""

from uuid import UUID

from app.context_runtime.evaluation import (
    ContextFeedbackAction,
    ContextQualityLevel,
    ContextRuntimeDecision,
    ContextRuntimeFeedbackConsumer,
    ContextRuntimeFeedbackResult,
)


def make_feedback(
    action: ContextFeedbackAction,
) -> ContextRuntimeFeedbackResult:
    return ContextRuntimeFeedbackResult(
        evaluation_id=UUID(
            "00000000-0000-0000-0000-000000000001"
        ),
        quality_level=ContextQualityLevel.EXCELLENT,
        feedback_signal=action,
        recommended_action=action,
        overall_score=0.9,
    )


def test_retain_feedback_produces_retain_decision():
    consumer = ContextRuntimeFeedbackConsumer()

    result = consumer.consume(
        make_feedback(ContextFeedbackAction.RETAIN)
    )

    assert result == ContextRuntimeDecision.RETAIN


def test_review_feedback_produces_review_decision():
    consumer = ContextRuntimeFeedbackConsumer()

    result = consumer.consume(
        make_feedback(ContextFeedbackAction.REVIEW)
    )

    assert result == ContextRuntimeDecision.REVIEW


def test_refresh_feedback_produces_refresh_decision():
    consumer = ContextRuntimeFeedbackConsumer()

    result = consumer.consume(
        make_feedback(ContextFeedbackAction.REFRESH)
    )

    assert result == ContextRuntimeDecision.REFRESH


def test_disabled_refresh_policy_downgrades_refresh_to_review():
    from app.context_runtime.models import ContextRefreshPolicy

    consumer = ContextRuntimeFeedbackConsumer(
        refresh_policy=ContextRefreshPolicy(
            enabled=False,
        )
    )

    result = consumer.consume(
        make_feedback(ContextFeedbackAction.REFRESH)
    )

    assert result == ContextRuntimeDecision.REVIEW


def test_consumer_does_not_mutate_feedback():
    consumer = ContextRuntimeFeedbackConsumer()

    feedback = make_feedback(
        ContextFeedbackAction.REFRESH
    )

    original_action = feedback.recommended_action

    result = consumer.consume(feedback)

    assert result == ContextRuntimeDecision.REFRESH
    assert feedback.recommended_action == original_action

