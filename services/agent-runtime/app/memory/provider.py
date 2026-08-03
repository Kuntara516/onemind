"""
OneMind Memory Provider Implementation.

Provides the initial in-memory implementation
of the async Memory Interface contract.

Sprint 3 - Memory & Knowledge Foundation

ADR-001:
Async-First Runtime Architecture
"""

from typing import Dict

from .interface import MemoryInterface
from .models import MemoryQuery, MemoryRecord, MemoryResult


class InMemoryProvider(MemoryInterface):
    """
    Async in-memory implementation of the OneMind Memory Interface.
    """

    def __init__(self) -> None:
        """
        Initialize memory storage.
        """

        self._memories: Dict[str, MemoryRecord] = {}

    async def store(
        self,
        memory: MemoryRecord,
    ) -> MemoryRecord:
        """
        Store a memory record.
        """

        self._memories[memory.id] = memory

        return memory

    async def retrieve(
        self,
        query: MemoryQuery,
    ) -> MemoryResult:
        """
        Retrieve memories matching query.
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

    async def delete(
        self,
        memory_id: str,
    ) -> bool:
        """
        Delete a memory record.
        """

        if memory_id not in self._memories:
            return False

        del self._memories[memory_id]

        return True
