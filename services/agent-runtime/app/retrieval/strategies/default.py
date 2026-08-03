"""
Default retrieval strategy.

Provides the initial retrieval pipeline implementation
using OneMind Memory Service.

Sprint 4 - Context Intelligence & Retrieval Pipeline
"""

from app.memory.models import MemoryQuery

from app.retrieval.interface import RetrievalInterface
from app.retrieval.models import RetrievalRequest, RetrievalResult


class DefaultRetriever(RetrievalInterface):
    """
    Default retrieval implementation.

    Current responsibility:
    - retrieve relevant memories
    - normalize retrieval result

    Future extensions:
    - knowledge retrieval
    - hybrid retrieval
    - ranking
    - source attribution
    """

    def __init__(
        self,
        memory_service,
    ) -> None:
        """
        Initialize default retriever.

        Args:
            memory_service:
                MemoryService instance.
        """

        self._memory_service = memory_service

    async def retrieve(
        self,
        request: RetrievalRequest,
    ) -> RetrievalResult:
        """
        Retrieve information using default strategy.

        Args:
            request:
                Retrieval request.

        Returns:
            Retrieval result.
        """

        memory_result = await self._memory_service.retrieve(
            MemoryQuery(
                query=request.query,
                limit=request.limit,
                filters=request.filters,
            )
        )

        return RetrievalResult(
            memories=memory_result.records,
            metadata={
                "strategy": "default",
                "memory_count": memory_result.count,
            },
        )
