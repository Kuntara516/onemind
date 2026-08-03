"""
OneMind Memory Vector Integration Tests.

Validates integration between:
- Memory Layer
- Embedding Layer
- Vector Store Layer

Sprint 3 - Memory & Knowledge Foundation

ADR-001:
Async-First Runtime Architecture
"""

import pytest

from app.embedding.models import EmbeddingRequest
from app.embedding.service import EmbeddingService
from app.embedding.provider import DummyEmbeddingProvider

from app.memory.models import MemoryQuery, MemoryRecord
from app.memory.service import MemoryService
from app.memory.vector_provider import VectorMemoryProvider

from app.vector_store.service import VectorStoreService


@pytest.mark.anyio
async def test_vector_memory_store_and_retrieve():
    """
    Validate storing memory into vector storage
    and retrieving through semantic search flow.
    """

    embedding_service = EmbeddingService(
        provider=DummyEmbeddingProvider(),
    )

    vector_store_service = VectorStoreService()

    provider = VectorMemoryProvider(
        embedding_service=embedding_service,
        vector_store_service=vector_store_service,
    )

    memory_service = MemoryService(provider)

    memory = MemoryRecord(
        content="OneMind memory supports vector based retrieval.",
        metadata={
            "source": "integration-test",
        },
    )

    stored = await memory_service.store(memory)

    assert stored.id == memory.id
    assert stored.content == memory.content

    result = await memory_service.retrieve(
        MemoryQuery(
            query="vector retrieval",
            limit=5,
        )
    )

    assert result.count == 1
    assert len(result.records) == 1
    assert result.records[0].id == memory.id
    assert (
        result.records[0].content
        == "OneMind memory supports vector based retrieval."
    )


@pytest.mark.anyio
async def test_vector_memory_delete():
    """
    Validate deleting memory removes vector representation.
    """

    embedding_service = EmbeddingService(
        provider=DummyEmbeddingProvider(),
    )

    vector_store_service = VectorStoreService()

    provider = VectorMemoryProvider(
        embedding_service=embedding_service,
        vector_store_service=vector_store_service,
    )

    memory_service = MemoryService(provider)

    memory = await memory_service.store(
        MemoryRecord(
            content="Temporary vector memory entry.",
        )
    )

    deleted = await memory_service.delete(
        memory.id,
    )

    assert deleted is True

    result = await memory_service.retrieve(
        MemoryQuery(
            query="Temporary",
        )
    )

    assert result.count == 0