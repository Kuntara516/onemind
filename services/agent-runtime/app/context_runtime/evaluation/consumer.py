"""
Context Runtime Feedback Consumer

Consumes deterministic runtime feedback and converts it into
an explicit runtime decision.

Sprint:
S4-011-004 Feedback Consumer
"""

from __future__ import annotations

from enum import Enum

from app.context_runtime.models import ContextRefreshPolicy

from .feedback_models import (
    ContextFeedbackAction,
    ContextRuntimeFeedbackResult,
)


class ContextRuntimeDecision(str, Enum):
    """Runtime decision derived from context feedback."""

    RETAIN = "retain"
    REVIEW = "review"
    REFRESH = "refresh"


class ContextRuntimeFeedbackConsumer:
    """
    Consume ContextRuntimeFeedbackResult.

    Responsibilities:
    - interpret frozen S4-011-003 feedback
    - apply runtime refresh policy
    - produce an explicit runtime decision

    This component does not:
    - mutate SelectedContext
    - perform retrieval
    - perform refresh
    - modify ranking
    - modify selection
    - modify evaluation results
    """

    def __init__(
        self,
        refresh_policy: ContextRefreshPolicy | None = None,
    ) -> None:
        self.refresh_policy = (
            refresh_policy
            or ContextRefreshPolicy()
        )

    def consume(
        self,
        feedback: ContextRuntimeFeedbackResult,
    ) -> ContextRuntimeDecision:
        """
        Convert runtime feedback into a runtime decision.
        """

        if (
            feedback.recommended_action
            == ContextFeedbackAction.RETAIN
        ):
            return ContextRuntimeDecision.RETAIN

        if (
            feedback.recommended_action
            == ContextFeedbackAction.REVIEW
        ):
            return ContextRuntimeDecision.REVIEW

        if (
            feedback.recommended_action
            == ContextFeedbackAction.REFRESH
        ):
            if self.refresh_policy.enabled:
                return ContextRuntimeDecision.REFRESH

            return ContextRuntimeDecision.REVIEW

        raise ValueError(
            f"Unsupported feedback action: "
            f"{feedback.recommended_action}"
        )
