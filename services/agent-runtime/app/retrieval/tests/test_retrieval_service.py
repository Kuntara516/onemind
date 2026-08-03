"""
OneMind Retrieval Pipeline Foundation Tests.

Validates the Retrieval Layer implementation.

Sprint 4 - Context Intelligence & Retrieval Pipeline

ADR-001:
Async-First Runtime Architecture
"""

import pytest

from app.memory.models import MemoryRecord
from app.memory.provider import InMemoryProvider
from app.memory.service import MemoryService

from app.retrieval.models import RetrievalRequest
from app.retrieval.service import RetrievalService
from app.retrieval.strategies.default import DefaultRetriever


@pytest.mark.anyio
async def test_default_retriever_retrieves_memory():
    """
    Validate DefaultRetriever retrieves memories
    through MemoryService.
    """

    provider = InMemoryProvider()

    memory_service = MemoryService(
        provider,
    )

    await memory_service.store(
        MemoryRecord(
            content="OneMind retrieval pipeline uses memory foundation.",
        )
    )

    retriever = DefaultRetriever(
        memory_service,
    )

    result = await retriever.retrieve(
        RetrievalRequest(
            query="retrieval pipeline",
        )
    )

    assert len(result.memories) == 1
    assert (
        result.memories[0].content
        == "OneMind retrieval pipeline uses memory foundation."
    )

    assert result.metadata["strategy"] == "default"
    assert result.metadata["memory_count"] == 1


@pytest.mark.anyio
async def test_retrieval_service_builds_result():
    """
    Validate RetrievalService delegates retrieval
    through configured strategy.
    """

    provider = InMemoryProvider()

    memory_service = MemoryService(
        provider,
    )

    await memory_service.store(
        MemoryRecord(
            content="Context intelligence depends on retrieval layer.",
        )
    )

    retriever = DefaultRetriever(
        memory_service,
    )

    service = RetrievalService(
        retriever,
    )

    result = await service.retrieve(
        RetrievalRequest(
            query="context intelligence",
        )
    )

    assert len(result.memories) == 1
    assert (
        result.memories[0].content
        == "Context intelligence depends on retrieval layer."
    )


@pytest.mark.anyio
async def test_retrieval_service_empty_query_validation():
    """
    Validate RetrievalService rejects empty queries.
    """

    provider = InMemoryProvider()

    memory_service = MemoryService(
        provider,
    )

    retriever = DefaultRetriever(
        memory_service,
    )

    service = RetrievalService(
        retriever,
    )

    with pytest.raises(ValueError):
        await service.retrieve(
            RetrievalRequest(
                query="",
            )
        )
