"""
Context Runtime Decision Boundary

Provides the explicit decision boundary between
runtime feedback consumption and downstream execution.

Sprint:
S4-011-005 Runtime Decision Boundary

Author:
OneMind Platform

License:
MIT
"""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field

from .consumer import (
    ContextRuntimeDecision,
    ContextRuntimeFeedbackConsumer,
)
from .feedback_models import (
    ContextFeedbackAction,
    ContextFeedbackSignal,
    ContextRuntimeFeedbackResult,
)


class ContextRuntimeDecisionResult(BaseModel):
    """
    Immutable-style artifact representing a runtime decision.

    The result preserves the identity and feedback information
    that produced the decision.

    This artifact does not execute the decision.
    """

    evaluation_id: UUID = Field(
        description="Evaluation identifier that produced the decision.",
    )

    feedback_signal: ContextFeedbackSignal = Field(
        description="Feedback signal consumed by the decision boundary.",
    )

    recommended_action: ContextFeedbackAction = Field(
        description="Original action recommended by runtime feedback.",
    )

    decision: ContextRuntimeDecision = Field(
        description="Explicit runtime decision.",
    )

    overall_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Overall context quality score.",
    )


class ContextRuntimeDecisionBoundary:
    """
    Converts runtime feedback into an explicit decision artifact.

    Responsibilities:

    - consume runtime feedback
    - apply the existing runtime feedback consumer
    - preserve evaluation identity
    - preserve feedback metadata
    - return an explicit decision artifact

    This component intentionally does not:

    - perform context retrieval
    - perform context refresh
    - modify ranking
    - modify selection
    - mutate evaluation results
    - mutate feedback results
    - execute runtime actions
    """

    def __init__(
        self,
        consumer: ContextRuntimeFeedbackConsumer | None = None,
    ) -> None:
        self.consumer = (
            consumer
            or ContextRuntimeFeedbackConsumer()
        )

    def decide(
        self,
        feedback: ContextRuntimeFeedbackResult,
    ) -> ContextRuntimeDecisionResult:
        """
        Convert runtime feedback into an explicit decision artifact.

        The supplied feedback remains unchanged.
        """

        decision = self.consumer.consume(
            feedback
        )

        return ContextRuntimeDecisionResult(
            evaluation_id=feedback.evaluation_id,
            feedback_signal=feedback.feedback_signal,
            recommended_action=feedback.recommended_action,
            decision=decision,
            overall_score=feedback.overall_score,
        )

