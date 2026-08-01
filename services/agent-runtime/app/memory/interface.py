"""
OneMind Memory Interface Contract.

Defines the abstraction boundary between
Agent Runtime and Memory Providers.

Sprint 3 - Memory & Knowledge Foundation
"""

from abc import ABC, abstractmethod

from .models import MemoryQuery, MemoryRecord, MemoryResult


class MemoryInterface(ABC):
    """
    Abstract contract for all OneMind memory providers.

    Implementations may include:
    - InMemoryProvider
    - Persistent Memory Provider
    - Vector Memory Provider
    - Hybrid Memory Provider
    """

    @abstractmethod
    def store(self, memory: MemoryRecord) -> MemoryRecord:
        """
        Store a memory record.

        Args:
            memory:
                Memory record to store.

        Returns:
            Stored memory record.
        """
        raise NotImplementedError

    @abstractmethod
    def retrieve(self, query: MemoryQuery) -> MemoryResult:
        """
        Retrieve memories based on query.

        Args:
            query:
                Memory retrieval request.

        Returns:
            Retrieval result containing matching memories.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, memory_id: str) -> bool:
        """
        Delete a memory record.

        Args:
            memory_id:
                Identifier of memory to delete.

        Returns:
            True if deletion succeeds, otherwise False.
        """
        raise NotImplementedError