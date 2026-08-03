"""
OneMind Retrieval Service Layer.

Provides application-level operations for
the Retrieval Pipeline Foundation.

Sprint 4 - Context Intelligence & Retrieval Pipeline

ADR-001:
Async-First Runtime Architecture
"""

from app.retrieval.interface import RetrievalInterface
from app.retrieval.models import RetrievalRequest, RetrievalResult


class RetrievalService:
    """
    Application service for retrieval operations.

    This layer provides a stable API boundary between
    Context Intelligence components and retrieval strategies.

    Responsibilities:
    - validate retrieval requests
    - delegate to retrieval provider
    - normalize results
    - hide strategy implementation details
    """

    def __init__(
        self,
        provider: RetrievalInterface,
    ) -> None:
        """
        Initialize Retrieval Service.

        Args:
            provider:
                Retrieval implementation.
        """

        self._provider = provider

    async def retrieve(
        self,
        request: RetrievalRequest,
    ) -> RetrievalResult:
        """
        Retrieve relevant information.

        Args:
            request:
                Retrieval request.

        Returns:
            Retrieval result.
        """

        if not request.query:
            raise ValueError("Retrieval query cannot be empty")

        if request.limit <= 0:
            raise ValueError("Retrieval limit must be greater than zero")

        return await self._provider.retrieve(
            request,
        )
