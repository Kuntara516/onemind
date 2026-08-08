"""
Context Runtime Feedback

Converts context evaluation results into deterministic runtime feedback.

Sprint:
    S4-011-003 Context Evaluation & Runtime Feedback

Author:
    OneMind Platform

License:
    MIT
"""

from __future__ import annotations

from .feedback_models import (
    ContextFeedbackAction,
    ContextFeedbackSignal,
    ContextQualityLevel,
    ContextRuntimeFeedbackResult,
)
from .models import ContextEvaluationResult


class ContextRuntimeFeedback:
    """
    Generate deterministic runtime feedback from context evaluation.

    This component is intentionally stateless.

    Thresholds:

        >= 0.80 -> excellent / retain
        >= 0.60 -> good      / retain
        >= 0.40 -> degraded  / review
        <  0.40 -> poor      / refresh
    """

    EXCELLENT_THRESHOLD = 0.80
    GOOD_THRESHOLD = 0.60
    DEGRADED_THRESHOLD = 0.40

    def generate(
        self,
        evaluation: ContextEvaluationResult,
    ) -> ContextRuntimeFeedbackResult:
        """Generate runtime feedback from an evaluation result."""

        score = evaluation.score.overall_score

        if score >= self.EXCELLENT_THRESHOLD:
            quality_level = ContextQualityLevel.EXCELLENT
            signal = ContextFeedbackSignal.RETAIN

        elif score >= self.GOOD_THRESHOLD:
            quality_level = ContextQualityLevel.GOOD
            signal = ContextFeedbackSignal.RETAIN

        elif score >= self.DEGRADED_THRESHOLD:
            quality_level = ContextQualityLevel.DEGRADED
            signal = ContextFeedbackSignal.REVIEW

        else:
            quality_level = ContextQualityLevel.POOR
            signal = ContextFeedbackSignal.REFRESH

        return ContextRuntimeFeedbackResult(
            evaluation_id=evaluation.evaluation_id,
            quality_level=quality_level,
            feedback_signal=signal,
            recommended_action=ContextFeedbackAction(signal.value),
            overall_score=score,
        )
