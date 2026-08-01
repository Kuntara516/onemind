"""
OneMind Knowledge Interface Contract.

Defines the abstraction boundary between
Knowledge Service and Knowledge Providers.

Sprint 3 - Memory & Knowledge Foundation
"""

from abc import ABC, abstractmethod

from .models import KnowledgeItem, KnowledgeQuery, KnowledgeResult


class KnowledgeInterface(ABC):
    """
    Abstract contract for knowledge storage providers.

    The Knowledge Service depends on this interface,
    not on a concrete provider implementation.
    """

    @abstractmethod
    def add(
        self,
        item: KnowledgeItem,
    ) -> KnowledgeItem:
        """
        Store a knowledge item.

        Args:
            item:
                Knowledge item to store.

        Returns:
            Stored knowledge item.
        """
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        query: KnowledgeQuery,
    ) -> KnowledgeResult:
        """
        Retrieve knowledge items.

        Args:
            query:
                Knowledge retrieval request.

        Returns:
            Knowledge retrieval result.
        """
        raise NotImplementedError

    @abstractmethod
    def remove(
        self,
        item_id: str,
    ) -> bool:
        """
        Remove a knowledge item.

        Args:
            item_id:
                Identifier of knowledge item.

        Returns:
            True when removed successfully.
        """
        raise NotImplementedError