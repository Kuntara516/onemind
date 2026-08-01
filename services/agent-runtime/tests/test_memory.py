"""
OneMind Memory Foundation Tests.

Validates the Memory Foundation implementation.

Sprint 3 - Memory & Knowledge Foundation
"""

from app.memory.models import MemoryQuery, MemoryRecord
from app.memory.provider import InMemoryProvider
from app.memory.service import MemoryService


def test_memory_record_creation():
    """
    Validate MemoryRecord creation.
    """

    memory = MemoryRecord(
        content="User prefers concise technical explanations."
    )

    assert memory.id is not None
    assert memory.content == "User prefers concise technical explanations."
    assert memory.metadata == {}
    assert memory.created_at is not None
    assert memory.updated_at is not None


def test_memory_service_store():
    """
    Validate storing memory through service layer.
    """

    provider = InMemoryProvider()
    service = MemoryService(provider)

    memory = MemoryRecord(
        content="OneMind uses interface driven architecture."
    )

    stored = service.store(memory)

    assert stored.id == memory.id
    assert stored.content == memory.content


def test_memory_service_retrieve():
    """
    Validate memory retrieval.
    """

    provider = InMemoryProvider()
    service = MemoryService(provider)

    service.store(
        MemoryRecord(
            content="Memory layer supports future RAG integration."
        )
    )

    result = service.retrieve(
        MemoryQuery(
            query="RAG"
        )
    )

    assert result.count == 1
    assert len(result.records) == 1
    assert "RAG" in result.records[0].content


def test_memory_service_delete():
    """
    Validate memory deletion.
    """

    provider = InMemoryProvider()
    service = MemoryService(provider)

    memory = service.store(
        MemoryRecord(
            content="Temporary memory entry."
        )
    )

    deleted = service.delete(memory.id)

    assert deleted is True

    result = service.retrieve(
        MemoryQuery(
            query="Temporary"
        )
    )

    assert result.count == 0


def test_memory_provider_contract():
    """
    Validate provider implements MemoryInterface behavior.
    """

    provider = InMemoryProvider()

    memory = MemoryRecord(
        content="Provider contract validation."
    )

    stored = provider.store(memory)

    result = provider.retrieve(
        MemoryQuery(
            query="Provider"
        )
    )

    assert stored.id == memory.id
    assert result.count == 1