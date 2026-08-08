"""
Context Runtime Feedback Models

Models for converting context evaluation results into deterministic
runtime feedback signals.

Sprint:
    S4-011-003 Context Evaluation & Runtime Feedback

Author:
    OneMind Platform

License:
    MIT
"""

from __future__ import annotations

from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class ContextQualityLevel(str, Enum):
    """Normalized qualitative classification of context quality."""

    EXCELLENT = "excellent"
    GOOD = "good"
    DEGRADED = "degraded"
    POOR = "poor"


class ContextFeedbackSignal(str, Enum):
    """Deterministic signal emitted from evaluated context quality."""

    RETAIN = "retain"
    REVIEW = "review"
    REFRESH = "refresh"


class ContextFeedbackAction(str, Enum):
    """Recommended downstream runtime action for the feedback signal."""

    RETAIN = "retain"
    REVIEW = "review"
    REFRESH = "refresh"


class ContextRuntimeFeedbackResult(BaseModel):
    """Runtime feedback derived from a ContextEvaluationResult."""

    evaluation_id: UUID = Field(
        description="Evaluation identifier that produced this feedback.",
    )

    quality_level: ContextQualityLevel = Field(
        description="Qualitative classification of the overall context score.",
    )

    feedback_signal: ContextFeedbackSignal = Field(
        description="Deterministic feedback signal for downstream consumers.",
    )

    recommended_action: ContextFeedbackAction = Field(
        description="Recommended runtime action represented by the signal.",
    )

    overall_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Overall context quality score used for classification.",
    )
