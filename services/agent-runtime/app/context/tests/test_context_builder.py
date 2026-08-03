"""
OneMind Context Builder Tests.

Validates the Context Intelligence Layer foundation.

Sprint 4 - Context Intelligence & Retrieval Pipeline

ADR-001:
Async-First Runtime Architecture
"""

import pytest

from app.context.models import ContextRequest
from app.context.service import ContextService
from app.context.strategies.default import DefaultContextBuilder

from app.memory.models import MemoryRecord
from app.memory.provider import InMemoryProvider
from app.memory.service import MemoryService


@pytest.mark.anyio
async def test_default_context_builder_retrieves_memory():
    """
    Validate DefaultContextBuilder retrieves memories
    through MemoryService.
    """

    provider = InMemoryProvider()

    memory_service = MemoryService(
        provider,
    )

    await memory_service.store(
        MemoryRecord(
            content="OneMind context layer uses memory retrieval.",
        )
    )

    builder = DefaultContextBuilder(
        memory_service,
    )

    result = await builder.build(
        ContextRequest(
            user_input="context",
        )
    )

    assert len(result.memories) == 1
    assert (
        "context"
        in result.memories[0].content
    )


@pytest.mark.anyio
async def test_context_service_build_context():
    """
    Validate ContextService delegates context building.
    """

    provider = InMemoryProvider()

    memory_service = MemoryService(
        provider,
    )

    await memory_service.store(
        MemoryRecord(
            content="Context service delegates to builder.",
        )
    )

    builder = DefaultContextBuilder(
        memory_service,
    )

    service = ContextService(
        builder,
    )

    result = await service.build_context(
        ContextRequest(
            user_input="delegates",
        )
    )

    assert len(result.memories) == 1
    assert (
        result.memories[0].content
        == "Context service delegates to builder."
    )


@pytest.mark.anyio
async def test_context_builder_empty_result():
    """
    Validate empty context result handling.
    """

    provider = InMemoryProvider()

    memory_service = MemoryService(
        provider,
    )

    builder = DefaultContextBuilder(
        memory_service,
    )

    result = await builder.build(
        ContextRequest(
            user_input="unknown query",
        )
    )

    assert result.memories == []
