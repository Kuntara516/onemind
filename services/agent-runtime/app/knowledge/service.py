"""
OneMind Knowledge Service Layer.

Provides application-level operations for
the Knowledge Foundation layer.

Sprint 3 - Memory & Knowledge Foundation
"""

from .interface import KnowledgeInterface
from .models import KnowledgeItem, KnowledgeQuery, KnowledgeResult


class KnowledgeService:
    """
    Application service for knowledge operations.

    The service depends on KnowledgeInterface,
    allowing provider implementations to be replaced
    without affecting application logic.
    """

    def __init__(
        self,
        provider: KnowledgeInterface,
    ):
        self._provider = provider

    def add(
        self,
        item: KnowledgeItem,
    ) -> KnowledgeItem:
        """
        Add knowledge item.

        Args:
            item:
                Knowledge item to store.

        Returns:
            Stored knowledge item.
        """

        return self._provider.add(item)

    def search(
        self,
        query: KnowledgeQuery,
    ) -> KnowledgeResult:
        """
        Search knowledge.

        Args:
            query:
                Knowledge retrieval request.

        Returns:
            Knowledge retrieval result.
        """

        return self._provider.search(query)

    def remove(
        self,
        item_id: str,
    ) -> bool:
        """
        Remove knowledge item.

        Args:
            item_id:
                Knowledge identifier.

        Returns:
            True if removed successfully.
        """

        return self._provider.remove(item_id)