"""
Context Ranking Engine

S4-007-002

Responsible for ranking retrieved context candidates
based on relevance scoring.
"""

from abc import ABC, abstractmethod

from .models import ContextCandidate
from .scoring import (
    ContextScore,
    calculate_budget_score,
    calculate_lifecycle_score,
    calculate_query_match_score,
)


class ContextRanker(ABC):
    """
    Abstract context ranking interface.

    Ranking implementations may use:
    - keyword scoring
    - embedding similarity
    - vector search score
    - LLM based reranking
    """

    @abstractmethod
    def rank(
        self,
        candidates: list[ContextCandidate],
        query: str,
        limit: int = 5,
    ) -> list[ContextCandidate]:
        """
        Rank context candidates.

        Args:
            candidates:
                Candidate contexts.

            query:
                User query.

            limit:
                Maximum returned candidates.

        Returns:
            Ranked context candidates.
        """
        raise NotImplementedError


class DefaultContextRanker(ContextRanker):
    """
    Default deterministic context ranking.

    Phase 1:
    - query keyword matching
    - lifecycle priority
    - remaining budget availability

    Future:
    - embedding similarity
    - Qdrant score
    - LLM reranking
    """

    def rank(
        self,
        candidates: list[ContextCandidate],
        query: str,
        limit: int = 5,
    ) -> list[ContextCandidate]:
        """
        Rank candidates and return top-k results.
        """

        scored_candidates = []

        for candidate in candidates:
            score = self.score(
                candidate=candidate,
                query=query,
            )

            scored_candidates.append(
                (
                    score.total_score,
                    candidate,
                )
            )

        scored_candidates.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            candidate
            for _, candidate in scored_candidates[:limit]
        ]

    def score(
        self,
        candidate: ContextCandidate,
        query: str,
    ) -> ContextScore:
        """
        Calculate context relevance score.
        """

        query_match = calculate_query_match_score(
            candidate=candidate,
            query=query,
        )

        lifecycle = calculate_lifecycle_score(
            candidate=candidate,
        )

        budget = calculate_budget_score(
            candidate=candidate,
        )

        total = (
            query_match * 0.5
            + lifecycle * 0.3
            + budget * 0.2
        )

        return ContextScore(
            query_match=query_match,
            lifecycle_score=lifecycle,
            budget_score=budget,
            total_score=total,
        )
