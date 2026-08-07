"""
Context Runtime Evaluation Models

Pydantic models for Context Quality Evaluation.

Sprint:
    S4-011-001 Context Quality Evaluation Foundation

Author:
    OneMind Platform

License:
    MIT
"""

from __future__ import annotations

from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ContextQualityScore(BaseModel):
    """
    Quality score for evaluated context.

    All scores are normalized between 0 and 1.
    """

    relevance_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="How relevant selected context is.",
    )

    coverage_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="How much required information is covered.",
    )

    diversity_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Context diversity score.",
    )

    compression_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Token efficiency score.",
    )

    utility_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Execution usefulness score.",
    )

    overall_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Aggregated context quality score.",
    )


class ContextEvaluationResult(BaseModel):
    """
    Result returned from ContextEvaluator.
    """

    evaluation_id: UUID = Field(
        default_factory=uuid4,
        description="Unique evaluation identifier.",
    )

    score: ContextQualityScore = Field(
        default_factory=ContextQualityScore,
    )

    retrieved_items: int = Field(
        default=0,
        ge=0,
    )

    selected_items: int = Field(
        default=0,
        ge=0,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )
