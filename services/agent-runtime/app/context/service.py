"""
OneMind Context Service Layer.

Provides application-level operations for
the Context Intelligence Layer.

Sprint 4 - Context Intelligence & Retrieval Pipeline
"""

from .interface import ContextBuilder
from .models import ContextRequest, ContextResult


class ContextService:
    """
    Application service for context operations.

    This layer provides a stable API boundary between
    Agent Runtime components and context builder strategies.

    Responsibilities:
    - delegate context construction
    - hide builder implementation details
    - provide future extension point for:
        - retrieval pipeline
        - ranking
        - compression
        - context optimization
    """

    def __init__(
        self,
        builder: ContextBuilder,
    ) -> None:
        """
        Initialize Context Service.

        Args:
            builder:
                Context builder implementation.
        """

        self._builder = builder

    async def build_context(
        self,
        request: ContextRequest,
    ) -> ContextResult:
        """
        Build context from request.

        Args:
            request:
                Context construction request.

        Returns:
            Compiled context result.
        """

        return await self._builder.build(request)
