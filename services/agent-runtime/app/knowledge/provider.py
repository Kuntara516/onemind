"""
OneMind In-Memory Knowledge Provider.

Initial Knowledge storage implementation for
the Knowledge Foundation layer.

Sprint 3 - Memory & Knowledge Foundation
"""

from typing import Dict

from .interface import KnowledgeInterface
from .models import KnowledgeItem, KnowledgeQuery, KnowledgeResult


class InMemoryKnowledgeProvider(KnowledgeInterface):
    """
    In-memory implementation of KnowledgeInterface.

    Purpose:
    - Validate Knowledge architecture
    - Support unit testing
    - Provide development-time knowledge storage

    Future providers may include:
    - PostgreSQL Knowledge Provider
    - Vector Knowledge Provider
    - Hybrid Knowledge Provider
    """

    def __init__(self):
        self._items: Dict[str, KnowledgeItem] = {}

    def add(
        self,
        item: KnowledgeItem,
    ) -> KnowledgeItem:
        """
        Store a knowledge item.
        """

        self._items[item.id] = item

        return item

    def search(
        self,
        query: KnowledgeQuery,
    ) -> KnowledgeResult:
        """
        Search knowledge items.

        Current implementation:
        - Simple text matching

        Future implementation:
        - Semantic similarity search
        - Embedding-based retrieval
        """

        matched_items = []

        search_text = query.query.lower()

        for item in self._items.values():

            if search_text in item.content.lower():
                matched_items.append(item)

        limited_items = matched_items[: query.limit]

        return KnowledgeResult(
            items=limited_items,
            count=len(limited_items),
        )

    def remove(
        self,
        item_id: str,
    ) -> bool:
        """
        Remove a knowledge item.
        """

        if item_id not in self._items:
            return False

        del self._items[item_id]

        return True