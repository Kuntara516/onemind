"""
Context Ranking interface.

Defines the contract between Context Ranking Service
and concrete ranking strategy implementations.

Sprint 4 - Context Intelligence & Retrieval Pipeline
"""

from abc import ABC, abstractmethod

from .models import RankingRequest, RankingResult


class ContextRankingInterface(ABC):
    """
    Abstract contract for context ranking.

    Implementations may provide different ranking
    strategies such as:

    - relevance based ranking
    - recency weighted ranking
    - importance based ranking
    - hybrid ranking
    """

    @abstractmethod
    async def rank(
        self,
        request: RankingRequest,
    ) -> RankingResult:
        """
        Rank context candidates.

        Args:
            request:
                Ranking input containing context candidates.

        Returns:
            RankingResult containing prioritized contexts.
        """

        raise NotImplementedError
