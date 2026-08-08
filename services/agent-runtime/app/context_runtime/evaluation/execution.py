"""
Context Runtime Decision Execution Contract

Defines the execution artifact produced from an explicit
runtime decision.

Sprint:
S4-011-006-001 Decision Execution Foundation

Author:
OneMind Platform

License:
MIT
"""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field

from .consumer import ContextRuntimeDecision
from .decision import ContextRuntimeDecisionResult
from .feedback_models import ContextFeedbackAction


class ContextRuntimeExecutionResult(BaseModel):
    """
    Explicit execution artifact derived from a runtime decision.

    This artifact represents what downstream execution should do.
    It does not perform the action itself.
    """

    evaluation_id: UUID = Field(
        description="Evaluation identifier that produced the decision.",
    )

    decision: ContextRuntimeDecision = Field(
        description="Explicit runtime decision.",
    )

    action: ContextFeedbackAction = Field(
        description="Action to be handled by downstream execution.",
    )

    executed: bool = Field(
        default=False,
        description="Whether the runtime action has actually executed.",
    )


class ContextRuntimeDecisionExecutor:
    """
    Converts a runtime decision into an execution artifact.

    Responsibilities:
    - preserve decision identity
    - map decision to an execution action
    - produce an explicit execution contract

    This component intentionally does not:
    - execute context refresh
    - mutate runtime context
    - retrieve context
    - modify ranking
    - modify selection
    - invoke Agent Runtime Executor
    """

    def execute(
        self,
        decision: ContextRuntimeDecisionResult,
    ) -> ContextRuntimeExecutionResult:
        """
        Convert a runtime decision into an execution artifact.

        No runtime action is executed at this stage.
        """

        action = ContextFeedbackAction(
            decision.decision.value
        )

        return ContextRuntimeExecutionResult(
            evaluation_id=decision.evaluation_id,
            decision=decision.decision,
            action=action,
            executed=False,
        )
