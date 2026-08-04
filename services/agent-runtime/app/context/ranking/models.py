"""
Context Ranking models.

Defines request and response contracts for the
Context Ranking & Prioritization Layer.

Sprint 4 - Context Intelligence & Retrieval Pipeline
"""

from typing import Any

from pydantic import BaseModel, Field


class ContextCandidate(BaseModel):
    """
    Represents a candidate context item before ranking.

    A candidate may originate from:
    - memory retrieval
    - knowledge retrieval
    - external sources
    """

    id: str

    content: str

    source: str = "unknown"

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class RankingScore(BaseModel):
    """
    Score breakdown for a context candidate.

    Supports future ranking strategies:
    - semantic relevance
    - recency weighting
    - importance weighting
    - source priority
    """

    relevance: float = 0.0

    recency: float = 0.0

    importance: float = 0.0

    priority: float = 0.0

    total: float = 0.0


class RankedContext(BaseModel):
    """
    Context candidate with ranking result.
    """

    candidate: ContextCandidate

    score: RankingScore


class RankingRequest(BaseModel):
    """
    Input request for context ranking.

    Receives retrieved candidates and produces
    prioritized context ordering.
    """

    candidates: list[ContextCandidate] = Field(
        default_factory=list
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class RankingResult(BaseModel):
    """
    Result produced by ranking engine.

    Contains ranked context candidates.
    """

    ranked_contexts: list[RankedContext] = Field(
        default_factory=list
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )
