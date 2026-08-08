"""
Tests for Context Runtime Decision Execution Contract.

Sprint:
S4-011-006-001 Decision Execution Foundation

Validates:

Context Evaluation
    ↓
Runtime Feedback
    ↓
Decision Boundary
    ↓
Runtime Decision
    ↓
Execution Contract

The execution contract must remain an adapter.
It must not execute refresh or mutate the decision artifact.
"""

from app.context_runtime.evaluation import (
    ContextEvaluator,
    ContextRuntimeDecision,
    ContextRuntimeDecisionBoundary,
    ContextRuntimeDecisionExecutor,
    ContextRuntimeFeedback,
    ContextRuntimeExecutionResult,
)


def make_feedback(overall_score: float):
    """
    Create deterministic runtime feedback.
    """

    evaluator = ContextEvaluator()

    if overall_score >= 0.70:
        evaluation = evaluator.evaluate(
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

    elif overall_score >= 0.40:
        evaluation = evaluator.evaluate(
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

    else:
        evaluation = evaluator.evaluate(
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

    return ContextRuntimeFeedback().generate(
        evaluation
    )


def make_decision(overall_score: float):
    """
    Create a runtime decision through the existing
    decision boundary.
    """

    feedback = make_feedback(
        overall_score
    )

    return ContextRuntimeDecisionBoundary().decide(
        feedback
    )


def test_execution_contract_for_retain():
    """
    RETAIN decision must produce a RETAIN execution action.
    """

    decision = make_decision(0.90)

    result = ContextRuntimeDecisionExecutor().execute(
        decision
    )

    assert result.decision == ContextRuntimeDecision.RETAIN
    assert result.action.value == "retain"
    assert result.executed is False


def test_execution_contract_for_review():
    """
    REVIEW decision must produce a REVIEW execution action.
    """

    decision = make_decision(0.50)

    result = ContextRuntimeDecisionExecutor().execute(
        decision
    )

    assert result.decision == ContextRuntimeDecision.REVIEW
    assert result.action.value == "review"
    assert result.executed is False


def test_execution_contract_for_refresh():
    """
    REFRESH decision must produce a REFRESH execution action.
    """

    decision = make_decision(0.20)

    result = ContextRuntimeDecisionExecutor().execute(
        decision
    )

    assert result.decision == ContextRuntimeDecision.REFRESH
    assert result.action.value == "refresh"
    assert result.executed is False


def test_execution_contract_preserves_evaluation_identity():
    """
    Evaluation identity must survive execution contract creation.
    """

    decision = make_decision(0.90)

    result = ContextRuntimeDecisionExecutor().execute(
        decision
    )

    assert result.evaluation_id == decision.evaluation_id


def test_execution_contract_does_not_mutate_decision():
    """
    Creating an execution artifact must not mutate the decision.
    """

    decision = make_decision(0.20)

    original = decision.model_copy(
        deep=True
    )

    result = ContextRuntimeDecisionExecutor().execute(
        decision
    )

    assert result.decision == ContextRuntimeDecision.REFRESH
    assert decision == original


def test_execution_contract_is_not_execution():
    """
    006-001 must only produce an execution contract.

    No refresh operation is executed.
    """

    decision = make_decision(0.20)

    result = ContextRuntimeDecisionExecutor().execute(
        decision
    )

    assert result.action.value == "refresh"
    assert result.executed is False


def test_execution_contract_is_deterministic():
    """
    Repeated execution-contract creation must produce
    equivalent results.
    """

    decision = make_decision(0.50)

    executor = ContextRuntimeDecisionExecutor()

    first = executor.execute(decision)
    second = executor.execute(decision)

    assert first == second


def test_execution_result_is_explicit_artifact():
    """
    The executor must return the declared execution artifact.
    """

    decision = make_decision(0.90)

    result = ContextRuntimeDecisionExecutor().execute(
        decision
    )

    assert isinstance(
        result,
        ContextRuntimeExecutionResult,
    )
