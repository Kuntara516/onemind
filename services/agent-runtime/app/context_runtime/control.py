"""
Context Runtime Decision Control

Applies an explicit runtime execution artifact to the context runtime
without moving decision-making or evaluation responsibilities into the
control layer.

Sprint:
S4-011-006-003 Runtime Decision -> Refresh Control Integration
"""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field

from app.context_runtime.evaluation.execution import (
    ContextRuntimeExecutionResult,
)
from app.context_runtime.evaluation.feedback_models import (
    ContextFeedbackAction,
)
from app.context_runtime.interface import ContextRefreshEngine
from app.context_runtime.models import ContextRuntimeState


class ContextRuntimeControlResult(BaseModel):
    """Result of applying an execution artifact to runtime state."""

    evaluation_id: UUID = Field(
        description="Evaluation identifier carried from the decision artifact.",
    )

    action: ContextFeedbackAction = Field(
        description="Execution action applied by the control layer.",
    )

    executed: bool = Field(
        default=False,
        description="Whether the requested runtime action was applied.",
    )

    state: ContextRuntimeState = Field(
        description="Runtime state after the control operation.",
    )


class ContextRuntimeDecisionController:
    """
    Apply a runtime execution artifact to context runtime state.

    Responsibilities:
    - preserve execution artifact identity and action
    - treat RETAIN and REVIEW as explicit no-op actions
    - delegate REFRESH to ContextRefreshEngine
    - report whether refresh was actually applied

    This component intentionally does not:
    - evaluate context quality
    - produce a runtime decision
    - retrieve context
    - rank context
    - select context
    - mutate context content
    """

    def __init__(
        self,
        refresh_engine: ContextRefreshEngine,
    ) -> None:
        self._refresh_engine = refresh_engine

    def apply(
        self,
        execution: ContextRuntimeExecutionResult,
        state: ContextRuntimeState,
    ) -> ContextRuntimeControlResult:
        """Apply the explicit execution action to runtime state."""

        if execution.action in (
            ContextFeedbackAction.RETAIN,
            ContextFeedbackAction.REVIEW,
        ):
            return ContextRuntimeControlResult(
                evaluation_id=execution.evaluation_id,
                action=execution.action,
                executed=False,
                state=state,
            )

        if execution.action == ContextFeedbackAction.REFRESH:
            before_last_refresh = state.last_refresh
            refreshed = self._refresh_engine.refresh(state)

            executed = (
                refreshed.last_refresh != before_last_refresh
            )

            return ContextRuntimeControlResult(
                evaluation_id=execution.evaluation_id,
                action=execution.action,
                executed=executed,
                state=refreshed,
            )

        raise ValueError(
            f"Unsupported execution action: {execution.action}"
        )
