"""
OneMind Memory Vector Integration Tests.

Validates integration between:
- Memory Layer
- Embedding Service
- Vector Store Service

Sprint 3 - S3-007 Memory Vector Integration
"""

import pytest

from app.embedding.provider import DummyEmbeddingProvider
from app.embedding.service import EmbeddingService
from app.memory.models import MemoryQuery, MemoryRecord
from app.memory.vector_provider import VectorMemoryProvider
from app.vector_store.service import VectorStoreService


@pytest.mark.anyio
async def test_vector_memory_store_and_retrieve():
    """
    Validate memory storage and semantic retrieval flow.
    """

    embedding_service = EmbeddingService(
        provider=DummyEmbeddingProvider(),
    )

    vector_store_service = VectorStoreService(
        backend="memory",
    )

    provider = VectorMemoryProvider(
        embedding_service=embedding_service,
        vector_store_service=vector_store_service,
    )

    memory = MemoryRecord(
        content="OneMind supports semantic memory retrieval.",
    )

    stored = await provider.store(
        memory,
    )

    assert stored.id == memory.id


    result = await provider.retrieve(
        MemoryQuery(
            query="semantic memory",
        )
    )

    assert result.count == 1
    assert result.records[0].id == memory.id
    assert (
        result.records[0].content
        == memory.content
    )


@pytest.mark.anyio
async def test_vector_memory_delete():
    """
    Validate vector-backed memory deletion.
    """

    embedding_service = EmbeddingService(
        provider=DummyEmbeddingProvider(),
    )

    vector_store_service = VectorStoreService(
        backend="memory",
    )

    provider = VectorMemoryProvider(
        embedding_service=embedding_service,
        vector_store_service=vector_store_service,
    )

    memory = MemoryRecord(
        content="Temporary vector memory.",
    )

    await provider.store(
        memory,
    )

    deleted = await provider.delete(
        memory.id,
    )

    assert deleted is True

    vector_record = vector_store_service.get(
        memory.id,
    )

    assert vector_record is None