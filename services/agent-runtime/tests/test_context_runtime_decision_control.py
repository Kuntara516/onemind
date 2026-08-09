from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from app.context_runtime.control import (
    ContextRuntimeDecisionController,
)
from app.context_runtime.evaluation.consumer import (
    ContextRuntimeDecision,
)
from app.context_runtime.evaluation.execution import (
    ContextRuntimeExecutionResult,
)
from app.context_runtime.evaluation.feedback_models import (
    ContextFeedbackAction,
)
from app.context_runtime.interface import ContextRefreshEngine
from app.context_runtime.models import (
    ContextBudget,
    ContextLifecycle,
    ContextRuntimeState,
)


class SpyRefreshEngine(ContextRefreshEngine):
    def __init__(self, *, should_refresh: bool) -> None:
        self._should_refresh = should_refresh
        self.should_refresh_calls = 0
        self.refresh_calls = 0

    def should_refresh(
        self,
        state: ContextRuntimeState,
    ) -> bool:
        self.should_refresh_calls += 1
        return self._should_refresh

    def refresh(
        self,
        state: ContextRuntimeState,
    ) -> ContextRuntimeState:
        self.refresh_calls += 1

        if not self._should_refresh:
            return state

        now = datetime.now(timezone.utc)
        state.lifecycle = ContextLifecycle.ACTIVE
        state.last_refresh = now
        state.updated_at = now

        return state


def make_state() -> ContextRuntimeState:
    return ContextRuntimeState(
        context_id="ctx-001",
        budget=ContextBudget(max_tokens=1000),
        lifecycle=ContextLifecycle.ACTIVE,
    )


def make_execution(
    action: ContextFeedbackAction,
) -> ContextRuntimeExecutionResult:
    return ContextRuntimeExecutionResult(
        evaluation_id=uuid4(),
        decision=ContextRuntimeDecision(action.value),
        action=action,
        executed=False,
    )


def test_retain_is_explicit_noop() -> None:
    engine = SpyRefreshEngine(should_refresh=True)
    controller = ContextRuntimeDecisionController(engine)
    state = make_state()
    execution = make_execution(ContextFeedbackAction.RETAIN)

    result = controller.apply(execution, state)

    assert result.evaluation_id == execution.evaluation_id
    assert result.action == ContextFeedbackAction.RETAIN
    assert result.executed is False
    assert result.state is state
    assert engine.should_refresh_calls == 0
    assert engine.refresh_calls == 0


def test_review_is_explicit_noop() -> None:
    engine = SpyRefreshEngine(should_refresh=True)
    controller = ContextRuntimeDecisionController(engine)
    state = make_state()
    execution = make_execution(ContextFeedbackAction.REVIEW)

    result = controller.apply(execution, state)

    assert result.evaluation_id == execution.evaluation_id
    assert result.action == ContextFeedbackAction.REVIEW
    assert result.executed is False
    assert result.state is state
    assert engine.should_refresh_calls == 0
    assert engine.refresh_calls == 0


def test_refresh_delegates_to_refresh_engine() -> None:
    engine = SpyRefreshEngine(should_refresh=True)
    controller = ContextRuntimeDecisionController(engine)
    state = make_state()
    execution = make_execution(ContextFeedbackAction.REFRESH)

    result = controller.apply(execution, state)

    assert result.evaluation_id == execution.evaluation_id
    assert result.action == ContextFeedbackAction.REFRESH
    assert result.executed is True
    assert result.state is state
    assert engine.refresh_calls == 1


def test_refresh_not_required_is_not_reported_as_executed() -> None:
    engine = SpyRefreshEngine(should_refresh=False)
    controller = ContextRuntimeDecisionController(engine)
    state = make_state()
    original_last_refresh = state.last_refresh
    execution = make_execution(ContextFeedbackAction.REFRESH)

    result = controller.apply(execution, state)

    assert result.executed is False
    assert result.state is state
    assert result.state.last_refresh == original_last_refresh
    assert engine.refresh_calls == 1


def test_execution_artifact_remains_unchanged() -> None:
    engine = SpyRefreshEngine(should_refresh=True)
    controller = ContextRuntimeDecisionController(engine)
    state = make_state()
    execution = make_execution(ContextFeedbackAction.REFRESH)

    original_evaluation_id = execution.evaluation_id
    original_action = execution.action
    original_executed = execution.executed

    controller.apply(execution, state)

    assert execution.evaluation_id == original_evaluation_id
    assert execution.action == original_action
    assert execution.executed == original_executed


def test_refresh_preserves_context_identity() -> None:
    engine = SpyRefreshEngine(should_refresh=True)
    controller = ContextRuntimeDecisionController(engine)
    state = make_state()
    execution = make_execution(ContextFeedbackAction.REFRESH)

    result = controller.apply(execution, state)

    assert result.state is state
    assert result.state.context_id == "ctx-001"
