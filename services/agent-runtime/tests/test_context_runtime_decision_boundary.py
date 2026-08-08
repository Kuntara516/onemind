"""
Tests for Context Runtime Decision Boundary.

Sprint:
S4-011-005 Runtime Decision Boundary

Validates:

    Context Evaluation
        ↓
    Runtime Feedback
        ↓
    Decision Boundary
        ↓
    Runtime Decision

The decision boundary must remain a pure decision adapter.
It must not execute refresh or mutate feedback artifacts.
"""

from uuid import UUID

from app.context_runtime.evaluation import (
    ContextRuntimeDecision,
    ContextRuntimeDecisionBoundary,
    ContextRuntimeFeedback,
    ContextRuntimeFeedbackConsumer,
    ContextEvaluator,
)
from app.context_runtime.models import (
    ContextRefreshPolicy,
)


EVALUATION_ID = UUID(
    "00000000-0000-0000-0000-000000000001"
)


def make_evaluation(
    overall_score: float,
):
    """
    Create a deterministic evaluation result.

    The evaluator's calculated score is used through the
    existing evaluation contract.
    """

    evaluator = ContextEvaluator()

    if overall_score >= 0.70:
        return evaluator.evaluate(
            retrieved_items=1,
            selected_items=1,
            relevant_items=1,
            duplicate_items=0,
            original_tokens=100,
            compressed_tokens=100,
            execution_success=True,
            metadata={
                "test_overall_score": overall_score,
            },
        )

    if overall_score >= 0.40:
        return evaluator.evaluate(
            retrieved_items=2,
            selected_items=1,
            relevant_items=1,
            duplicate_items=0,
            original_tokens=100,
            compressed_tokens=100,
            execution_success=False,
            metadata={
                "test_overall_score": overall_score,
            },
        )

    return evaluator.evaluate(
        retrieved_items=4,
        selected_items=1,
        relevant_items=0,
        duplicate_items=1,
        original_tokens=100,
        compressed_tokens=100,
        execution_success=False,
        metadata={
            "test_overall_score": overall_score,
        },
    )


def make_feedback(
    overall_score: float,
):
    """
    Create runtime feedback through the existing feedback generator.
    """

    evaluation = make_evaluation(
        overall_score
    )

    return ContextRuntimeFeedback().generate(
        evaluation
    )


def test_decision_boundary_returns_retain():
    """High-quality feedback must produce RETAIN."""

    feedback = make_feedback(0.90)

    boundary = ContextRuntimeDecisionBoundary()

    result = boundary.decide(feedback)

    assert result.decision == ContextRuntimeDecision.RETAIN


def test_decision_boundary_returns_review():
    """Degraded feedback must produce REVIEW."""

    feedback = make_feedback(0.50)

    boundary = ContextRuntimeDecisionBoundary()

    result = boundary.decide(feedback)

    assert result.decision == ContextRuntimeDecision.REVIEW


def test_decision_boundary_returns_refresh():
    """Poor feedback must produce REFRESH."""

    feedback = make_feedback(0.20)

    boundary = ContextRuntimeDecisionBoundary()

    result = boundary.decide(feedback)

    assert result.decision == ContextRuntimeDecision.REFRESH


def test_decision_boundary_preserves_evaluation_identity():
    """The evaluation ID must survive the decision boundary."""

    feedback = make_feedback(0.90)

    boundary = ContextRuntimeDecisionBoundary()

    result = boundary.decide(feedback)

    assert result.evaluation_id == feedback.evaluation_id


def test_decision_boundary_preserves_feedback_signal():
    """Feedback signal must be preserved."""

    feedback = make_feedback(0.50)

    boundary = ContextRuntimeDecisionBoundary()

    result = boundary.decide(feedback)

    assert result.feedback_signal == feedback.feedback_signal


def test_decision_boundary_preserves_recommended_action():
    """Original recommended action must be preserved."""

    feedback = make_feedback(0.20)

    boundary = ContextRuntimeDecisionBoundary()

    result = boundary.decide(feedback)

    assert (
        result.recommended_action
        == feedback.recommended_action
    )


def test_decision_boundary_does_not_mutate_feedback():
    """Decision creation must not mutate feedback."""

    feedback = make_feedback(0.20)

    original = feedback.model_copy(
        deep=True
    )

    boundary = ContextRuntimeDecisionBoundary()

    result = boundary.decide(feedback)

    assert result.decision == ContextRuntimeDecision.REFRESH
    assert feedback == original


def test_decision_boundary_does_not_execute_refresh():
    """
    REFRESH is represented only as a decision.

    No refresh operation is executed here.
    """

    feedback = make_feedback(0.20)

    boundary = ContextRuntimeDecisionBoundary()

    result = boundary.decide(feedback)

    assert result.decision == ContextRuntimeDecision.REFRESH
    assert (
        feedback.recommended_action.value
        == "refresh"
    )


def test_decision_boundary_respects_injected_consumer_policy():
    """Injected consumer policy must control the decision."""

    consumer = ContextRuntimeFeedbackConsumer(
        refresh_policy=ContextRefreshPolicy(
            enabled=False,
        )
    )

    feedback = make_feedback(0.20)

    boundary = ContextRuntimeDecisionBoundary(
        consumer=consumer
    )

    result = boundary.decide(feedback)

    assert result.decision == ContextRuntimeDecision.REVIEW


def test_decision_boundary_is_deterministic():
    """Repeated decisions from the same feedback must match."""

    feedback = make_feedback(0.50)

    boundary = ContextRuntimeDecisionBoundary()

    first = boundary.decide(feedback)
    second = boundary.decide(feedback)

    assert first == second

