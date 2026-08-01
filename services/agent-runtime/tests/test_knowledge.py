"""
OneMind Knowledge Foundation Tests.

Validates the Knowledge Foundation implementation.

Sprint 3 - Memory & Knowledge Foundation
"""

from app.knowledge.models import (
    KnowledgeItem,
    KnowledgeQuery,
)

from app.knowledge.provider import (
    InMemoryKnowledgeProvider,
)

from app.knowledge.service import (
    KnowledgeService,
)


def test_knowledge_item_creation():
    """
    Validate KnowledgeItem creation.
    """

    item = KnowledgeItem(
        content="OneMind knowledge layer supports agent reasoning."
    )

    assert item.id is not None
    assert item.content == (
        "OneMind knowledge layer supports agent reasoning."
    )
    assert item.metadata == {}
    assert item.source is None
    assert item.created_at is not None
    assert item.updated_at is not None


def test_knowledge_service_add():
    """
    Validate adding knowledge through service layer.
    """

    provider = InMemoryKnowledgeProvider()
    service = KnowledgeService(provider)

    item = KnowledgeItem(
        content="Knowledge foundation enables future RAG pipeline."
    )

    stored = service.add(item)

    assert stored.id == item.id
    assert stored.content == item.content


def test_knowledge_service_search():
    """
    Validate knowledge retrieval.
    """

    provider = InMemoryKnowledgeProvider()
    service = KnowledgeService(provider)

    service.add(
        KnowledgeItem(
            content="Embedding service will enhance knowledge retrieval."
        )
    )

    result = service.search(
        KnowledgeQuery(
            query="Embedding"
        )
    )

    assert result.count == 1
    assert len(result.items) == 1
    assert "Embedding" in result.items[0].content


def test_knowledge_service_remove():
    """
    Validate knowledge removal.
    """

    provider = InMemoryKnowledgeProvider()
    service = KnowledgeService(provider)

    item = service.add(
        KnowledgeItem(
            content="Temporary knowledge entry."
        )
    )

    removed = service.remove(
        item.id
    )

    assert removed is True

    result = service.search(
        KnowledgeQuery(
            query="Temporary"
        )
    )

    assert result.count == 0


def test_knowledge_provider_contract():
    """
    Validate provider implements KnowledgeInterface behavior.
    """

    provider = InMemoryKnowledgeProvider()

    item = KnowledgeItem(
        content="Provider contract validation."
    )

    stored = provider.add(item)

    result = provider.search(
        KnowledgeQuery(
            query="Provider"
        )
    )

    assert stored.id == item.id
    assert result.count == 1