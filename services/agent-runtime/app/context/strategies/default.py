"""
Default context builder strategy.

Provides the initial context construction flow
using the OneMind Memory Service.
"""

from app.context.interface import ContextBuilder
from app.context.models import ContextRequest, ContextResult
from app.memory.models import MemoryQuery


class DefaultContextBuilder(ContextBuilder):
    """
    Default implementation of Context Builder.

    Current responsibility:
    - retrieve relevant memories
    - assemble basic context result

    Future extensions:
    - knowledge retrieval
    - ranking
    - compression
    """

    def __init__(
        self,
        memory_service,
    ) -> None:
        """
        Initialize context builder.

        Args:
            memory_service:
                MemoryService instance.
        """

        self._memory_service = memory_service

    async def build(
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

        memory_result = await self._memory_service.retrieve(
            MemoryQuery(
                query=request.user_input,
            )
        )

        return ContextResult(
            memories=memory_result.records,
        )
