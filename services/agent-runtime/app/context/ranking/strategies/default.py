"""
Default context ranking strategy.

Provides the initial ranking implementation
for Context Intelligence Layer.

Sprint 4 - Context Intelligence & Retrieval Pipeline
"""

from app.context.ranking.interface import ContextRankingInterface
from app.context.ranking.models import (
    RankedContext,
    RankingRequest,
    RankingResult,
    RankingScore,
)


class DefaultContextRanking(ContextRankingInterface):
    """
    Default context ranking implementation.

    Current responsibility:
    - calculate basic ranking score
    - order candidates by score

    Future extensions:
    - semantic relevance scoring
    - recency weighting
    - importance modeling
    - source prioritization
    """

    async def rank(
        self,
        request: RankingRequest,
    ) -> RankingResult:
        """
        Rank context candidates.

        Args:
            request:
                Ranking request containing candidates.

        Returns:
            Ranked context result.
        """

        ranked_contexts: list[RankedContext] = []

        for candidate in request.candidates:
            score = self._calculate_score(
                candidate,
            )

            ranked_contexts.append(
                RankedContext(
                    candidate=candidate,
                    score=score,
                )
            )

        ranked_contexts.sort(
            key=lambda item: item.score.total,
            reverse=True,
        )

        return RankingResult(
            ranked_contexts=ranked_contexts,
        )

    def _calculate_score(
        self,
        candidate,
    ) -> RankingScore:
        """
        Calculate ranking score.

        Initial implementation uses
        metadata-based signals.

        Args:
            candidate:
                Context candidate.

        Returns:
            Ranking score breakdown.
        """

        relevance = float(
            candidate.metadata.get(
                "relevance",
                1.0,
            )
        )

        recency = float(
            candidate.metadata.get(
                "recency",
                0.0,
            )
        )

        importance = float(
            candidate.metadata.get(
                "importance",
                0.0,
            )
        )

        priority = float(
            candidate.metadata.get(
                "priority",
                0.0,
            )
        )

        total = (
            relevance
            + recency
            + importance
            + priority
        )

        return RankingScore(
            relevance=relevance,
            recency=recency,
            importance=importance,
            priority=priority,
            total=total,
        )
