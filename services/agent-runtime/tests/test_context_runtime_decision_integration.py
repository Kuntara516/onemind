"""
Context Runtime Decision Integration Tests

Sprint:
S4-011 Context Evaluation & Runtime Feedback

Coverage:
- Evaluation -> Feedback -> Decision -> Execution -> Runtime Control
- Decision actions flow through the runtime coordinator
- Coordinator remains the owner of runtime state
- Execution artifacts remain immutable
"""

from __future__ import annotations

from app.context_runtime.coordinator import (
    ContextRuntimeCoordinator,
)
from app.context_runtime.evaluation import (
    ContextEvaluationIntegration,
    ContextEvaluationResult,
    ContextQualityScore,
)
from app.context_runtime.evaluation.feedback_models import (
    ContextFeedbackAction,
)
from app.context_runtime.models import (
    ContextAllocation,
    ContextBudget,
    ContextLifecycle,
    ContextRuntimeState,
    ContextCandidate,
    SelectedContext,
)


class FixedScoreEvaluator:
    """
    Test evaluator that preserves the real evaluation integration
    while allowing deterministic decision-boundary scores.
    """

    def __init__(self, score: float) -> None:
        self.score = score

    def evaluate(self, **kwargs) -> ContextEvaluationResult:
        score = ContextQualityScore(
            relevance_score=self.score,
            coverage_score=self.score,
            diversity_score=self.score,
            compression_score=self.score,
            utility_score=self.score,
            overall_score=self.score,
        )

        return ContextEvaluationResult(
            score=score,
            retrieved_items=kwargs["retrieved_items"],
            selected_items=kwargs["selected_items"],
            metadata=kwargs.get("metadata", {}),
        )


def create_runtime() -> ContextRuntimeCoordinator:
    coordinator = ContextRuntimeCoordinator()

    coordinator.create_context(
        context_id="decision-integration-001",
        budget=ContextBudget(
            max_tokens=10000,
            allocation=ContextAllocation(
                system=1000,
                memory=3000,
                knowledge=4000,
                conversation=2000,
            ),
        ),
    )

    coordinator.activate_context()

    return coordinator


def create_evaluation(
    *,
    quality_score: float,
) -> ContextEvaluationResult:
    """
    Create a real evaluation through the existing
    ContextEvaluationIntegration contract.
    """

    context = SelectedContext(
        items=[
            ContextCandidate(
                context_id="decision-context-001",
                content="decision integration test context",
            )
        ],
        total_tokens=100,
    )

    integration = ContextEvaluationIntegration(
        evaluator=FixedScoreEvaluator(
            quality_score
        ),
    )

    return integration.evaluate_context(
        context,
        execution_success=True,
    )


def create_execution(
    evaluation: ContextEvaluationResult,
):
    """
    Run the existing evaluation -> feedback ->
    decision -> execution pipeline.
    """

    integration = ContextEvaluationIntegration()

    feedback = integration.generate_feedback(
        evaluation
    )

    from app.context_runtime.evaluation import (
        ContextRuntimeDecisionBoundary,
        ContextRuntimeDecisionExecutor,
    )

    decision = ContextRuntimeDecisionBoundary().decide(
        feedback
    )

    return ContextRuntimeDecisionExecutor().execute(
        decision
    )


def test_retain_decision_flows_to_runtime_without_refresh() -> None:
    coordinator = create_runtime()

    evaluation = create_evaluation(
        quality_score=0.95,
    )

    execution = create_execution(
        evaluation
    )

    assert execution.action == (
        ContextFeedbackAction.RETAIN
    )

    result = coordinator.apply_decision(
        execution
    )

    assert result.action == (
        ContextFeedbackAction.RETAIN
    )

    assert result.state is coordinator.get_context()


def test_review_decision_flows_to_runtime_without_refresh() -> None:
    coordinator = create_runtime()

    evaluation = create_evaluation(
        quality_score=0.50,
    )

    execution = create_execution(
        evaluation
    )

    assert execution.action == (
        ContextFeedbackAction.REVIEW
    )

    result = coordinator.apply_decision(
        execution
    )

    assert result.action == (
        ContextFeedbackAction.REVIEW
    )

    assert result.state is coordinator.get_context()


def test_refresh_decision_flows_to_runtime_and_refreshes_state() -> None:
    coordinator = create_runtime()

    evaluation = create_evaluation(
        quality_score=0.20,
    )

    execution = create_execution(
        evaluation
    )

    assert execution.action == (
        ContextFeedbackAction.REFRESH
    )

    original_state = coordinator.get_context()
    assert original_state is not None

    original_last_refresh = (
        original_state.last_refresh
    )

    original_state.lifecycle = (
        ContextLifecycle.STALE
    )

    result = coordinator.apply_decision(
        execution
    )

    assert result.action == (
        ContextFeedbackAction.REFRESH
    )

    assert result.executed is True

    assert result.state is coordinator.get_context()

    assert result.state.lifecycle == (
        ContextLifecycle.ACTIVE
    )

    assert result.state.last_refresh is not None
    assert result.state.last_refresh != (
        original_last_refresh
    )

def test_runtime_state_remains_owned_by_coordinator() -> None:
    coordinator = create_runtime()

    evaluation = create_evaluation(
        quality_score=0.20,
    )

    execution = create_execution(
        evaluation
    )

    result = coordinator.apply_decision(
        execution
    )

    current = coordinator.get_context()

    assert current is result.state
    assert isinstance(
        current,
        ContextRuntimeState,
    )


def test_execution_artifact_is_not_mutated_by_runtime_flow() -> None:
    coordinator = create_runtime()

    evaluation = create_evaluation(
        quality_score=0.20,
    )

    execution = create_execution(
        evaluation
    )

    original = execution.model_copy(
        deep=True
    )

    coordinator.apply_decision(
        execution
    )

    assert execution == original
