"""
Context Ranking Service.

Provides application-level operations for
the Context Ranking & Prioritization Layer.

Sprint 4 - Context Intelligence & Retrieval Pipeline
"""

from app.context.ranking.interface import ContextRankingInterface
from app.context.ranking.models import (
    RankingRequest,
    RankingResult,
)


class ContextRankingService:
    """
    Application service for context ranking.

    Responsibilities:
    - validate ranking requests
    - delegate ranking operation
    - normalize ranking results
    - hide strategy implementation details
    """

    def __init__(
        self,
        strategy: ContextRankingInterface,
    ) -> None:
        """
        Initialize Context Ranking Service.

        Args:
            strategy:
                Context ranking strategy implementation.
        """

        self._strategy = strategy

    async def rank(
        self,
        request: RankingRequest,
    ) -> RankingResult:
        """
        Rank context candidates.

        Args:
            request:
                Ranking request.

        Returns:
            Ranked context result.

        Raises:
            ValueError:
                When request is invalid.
        """

        if request is None:
            raise ValueError(
                "Ranking request cannot be None"
            )

        return await self._strategy.rank(
            request,
        )
