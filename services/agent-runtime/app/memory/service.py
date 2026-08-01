"""
OneMind Memory Service Layer.

Provides application-level operations for
the OneMind Memory Foundation.

Sprint 3 - Memory & Knowledge Foundation
"""

from .interface import MemoryInterface
from .models import MemoryQuery, MemoryRecord, MemoryResult


class MemoryService:
    """
    Application service for memory operations.

    This layer provides a stable API boundary between
    Agent Runtime components and memory providers.

    Responsibilities:
    - validate memory operations
    - delegate to provider
    - normalize results
    - hide provider implementation details
    """

    def __init__(self, provider: MemoryInterface) -> None:
        """
        Initialize Memory Service.

        Args:
            provider:
                Memory provider implementation.
        """

        self._provider = provider

    def store(self, memory: MemoryRecord) -> MemoryRecord:
        """
        Store a memory record.

        Args:
            memory:
                Memory record to store.

        Returns:
            Stored memory record.
        """

        if not memory.content:
            raise ValueError("Memory content cannot be empty")

        return self._provider.store(memory)

    def retrieve(self, query: MemoryQuery) -> MemoryResult:
        """
        Retrieve memories.

        Args:
            query:
                Memory retrieval request.

        Returns:
            Memory retrieval result.
        """

        if not query.query:
            raise ValueError("Memory query cannot be empty")

        return self._provider.retrieve(query)

    def delete(self, memory_id: str) -> bool:
        """
        Delete a memory record.

        Args:
            memory_id:
                Identifier of memory to delete.

        Returns:
            True if deletion succeeds.
        """

        if not memory_id:
            raise ValueError("Memory id cannot be empty")

        return self._provider.delete(memory_id)