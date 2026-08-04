"""
Context Compression service facade.

Provides a high-level service interface for
context compression workflows.

Sprint 4 - Context Intelligence & Retrieval Pipeline
"""

from .interface import ContextCompressionInterface
from .models import CompressionRequest, CompressionResult
from .strategies.default import DefaultContextCompressionStrategy


class ContextCompressionService:
    """
    Service facade for context compression.

    Delegates compression execution to a concrete
    compression strategy.

    Future extensions:

    - dynamic strategy selection
    - LLM compression provider
    - token-aware optimization
    - compression telemetry
    """

    def __init__(
        self,
        strategy: ContextCompressionInterface | None = None,
    ):
        """
        Initialize compression service.

        Args:
            strategy:
                Concrete compression implementation.
                Defaults to DefaultContextCompressionStrategy.
        """

        self._strategy = (
            strategy
            or DefaultContextCompressionStrategy()
        )

    async def compress(
        self,
        request: CompressionRequest,
    ) -> CompressionResult:
        """
        Execute context compression.

        Args:
            request:
                Compression request.

        Returns:
            CompressionResult containing compressed context.
        """

        if request is None:
            raise ValueError(
                "compression request cannot be None"
            )

        return await self._strategy.compress(request)
