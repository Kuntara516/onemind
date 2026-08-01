"""
OneMind Memory Provider Implementation.

Provides the initial in-memory implementation
of the Memory Interface contract.

Sprint 3 - Memory & Knowledge Foundation
"""

from typing import Dict

from .interface import MemoryInterface
from .models import MemoryQuery, MemoryRecord, MemoryResult


class InMemoryProvider(MemoryInterface):
    """
    In-memory implementation of the OneMind Memory Interface.

    This provider is intended for:
    - development
    - testing
    - architecture validation

    Future providers may replace this implementation with:
    - persistent storage
    - vector database
    - hybrid memory storage
    """

    def __init__(self) -> None:
        """
        Initialize memory storage.
        """

        self._memories: Dict[str, MemoryRecord] = {}

    def store(self, memory: MemoryRecord) -> MemoryRecord:
        """
        Store a memory record.

        Args:
            memory:
                Memory record to store.

        Returns:
            Stored memory record.
        """

        self._memories[memory.id] = memory

        return memory

    def retrieve(self, query: MemoryQuery) -> MemoryResult:
        """
        Retrieve memories matching query.

        Current implementation:
        - simple keyword matching
        - no semantic search
        - no embedding

        Args:
            query:
                Memory retrieval request.

        Returns:
            MemoryResult containing matched memories.
        """

        matched_records = []

        keyword = query.query.lower()

        for memory in self._memories.values():
            if keyword in memory.content.lower():
                matched_records.append(memory)

            if len(matched_records) >= query.limit:
                break

        return MemoryResult(
            records=matched_records,
            count=len(matched_records),
            metadata={
                "provider": "in-memory",
                "query": query.query,
            },
        )

    def delete(self, memory_id: str) -> bool:
        """
        Delete a memory record.

        Args:
            memory_id:
                Identifier of memory to delete.

        Returns:
            True if memory exists and was deleted.
        """

        if memory_id not in self._memories:
            return False

        del self._memories[memory_id]

        return True