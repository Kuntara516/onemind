"""
Context Runtime Feedback Tests

Sprint:
    S4-011-003 Context Evaluation & Runtime Feedback

Coverage:

- quality classification
- retain signal
- review signal
- refresh signal
- evaluation identity propagation
- stateless behavior
"""

from __future__ import annotations

from uuid import uuid4

from app.context_runtime.evaluation import (
    ContextEvaluationResult,
    ContextFeedbackAction,
    ContextFeedbackSignal,
    ContextQualityLevel,
    ContextQualityScore,
    ContextRuntimeFeedback,
)


def make_evaluation(score: float) -> ContextEvaluationResult:
    """Create an evaluation result with the supplied overall score."""

    return ContextEvaluationResult(
        evaluation_id=uuid4(),
        score=ContextQualityScore(
            overall_score=score,
        ),
    )


def test_excellent_context_generates_retain_feedback():
    evaluation = make_evaluation(0.90)

    result = ContextRuntimeFeedback().generate(evaluation)

    assert result.quality_level == ContextQualityLevel.EXCELLENT
    assert result.feedback_signal == ContextFeedbackSignal.RETAIN
    assert result.recommended_action == ContextFeedbackAction.RETAIN
    assert result.overall_score == 0.90


def test_good_context_generates_retain_feedback():
    evaluation = make_evaluation(0.70)

    result = ContextRuntimeFeedback().generate(evaluation)

    assert result.quality_level == ContextQualityLevel.GOOD
    assert result.feedback_signal == ContextFeedbackSignal.RETAIN
    assert result.recommended_action == ContextFeedbackAction.RETAIN


def test_degraded_context_generates_review_feedback():
    evaluation = make_evaluation(0.50)

    result = ContextRuntimeFeedback().generate(evaluation)

    assert result.quality_level == ContextQualityLevel.DEGRADED
    assert result.feedback_signal == ContextFeedbackSignal.REVIEW
    assert result.recommended_action == ContextFeedbackAction.REVIEW


def test_poor_context_generates_refresh_feedback():
    evaluation = make_evaluation(0.20)

    result = ContextRuntimeFeedback().generate(evaluation)

    assert result.quality_level == ContextQualityLevel.POOR
    assert result.feedback_signal == ContextFeedbackSignal.REFRESH
    assert result.recommended_action == ContextFeedbackAction.REFRESH


def test_evaluation_identity_is_preserved():
    evaluation = make_evaluation(0.75)

    result = ContextRuntimeFeedback().generate(evaluation)

    assert result.evaluation_id == evaluation.evaluation_id


def test_feedback_generator_is_stateless():
    generator = ContextRuntimeFeedback()

    first = make_evaluation(0.90)
    second = make_evaluation(0.20)

    first_result = generator.generate(first)
    second_result = generator.generate(second)

    assert first_result.feedback_signal == ContextFeedbackSignal.RETAIN
    assert second_result.feedback_signal == ContextFeedbackSignal.REFRESH
    assert first_result.evaluation_id != second_result.evaluation_id


def test_threshold_boundaries():
    generator = ContextRuntimeFeedback()

    assert (
        generator.generate(make_evaluation(0.80)).quality_level
        == ContextQualityLevel.EXCELLENT
    )

    assert (
        generator.generate(make_evaluation(0.60)).quality_level
        == ContextQualityLevel.GOOD
    )

    assert (
        generator.generate(make_evaluation(0.40)).quality_level
        == ContextQualityLevel.DEGRADED
    )
