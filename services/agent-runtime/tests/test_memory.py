"""
OneMind Memory Foundation Tests.

Validates the Memory Foundation implementation.

Sprint 3 - Memory & Knowledge Foundation

ADR-001:
Async-First Runtime Architecture
"""

import pytest

from app.memory.models import MemoryQuery, MemoryRecord
from app.memory.provider import InMemoryProvider
from app.memory.service import MemoryService


@pytest.mark.anyio
async def test_memory_record_creation():
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


@pytest.mark.anyio
async def test_memory_service_store():
    """
    Validate storing memory through service layer.
    """

    provider = InMemoryProvider()
    service = MemoryService(provider)

    memory = MemoryRecord(
        content="OneMind uses interface driven architecture."
    )

    stored = await service.store(memory)

    assert stored.id == memory.id
    assert stored.content == memory.content


@pytest.mark.anyio
async def test_memory_service_retrieve():
    """
    Validate memory retrieval.
    """

    provider = InMemoryProvider()
    service = MemoryService(provider)

    await service.store(
        MemoryRecord(
            content="Memory layer supports future RAG integration."
        )
    )

    result = await service.retrieve(
        MemoryQuery(
            query="RAG"
        )
    )

    assert result.count == 1
    assert len(result.records) == 1
    assert "RAG" in result.records[0].content


@pytest.mark.anyio
async def test_memory_service_delete():
    """
    Validate memory deletion.
    """

    provider = InMemoryProvider()
    service = MemoryService(provider)

    memory = await service.store(
        MemoryRecord(
            content="Temporary memory entry."
        )
    )

    deleted = await service.delete(memory.id)

    assert deleted is True

    result = await service.retrieve(
        MemoryQuery(
            query="Temporary"
        )
    )

    assert result.count == 0


@pytest.mark.anyio
async def test_memory_provider_contract():
    """
    Validate provider implements MemoryInterface behavior.
    """

    provider = InMemoryProvider()

    memory = MemoryRecord(
        content="Provider contract validation."
    )

    stored = await provider.store(memory)

    result = await provider.retrieve(
        MemoryQuery(
            query="Provider"
        )
    )

    assert stored.id == memory.id
    assert result.count == 1