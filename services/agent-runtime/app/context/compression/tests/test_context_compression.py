"""
Context Compression tests.

Tests Context Compression Layer behavior.

Sprint 4 - Context Intelligence & Retrieval Pipeline
"""

import pytest

from app.context.compression.models import (
    CompressionCandidate,
    CompressionRequest,
)
from app.context.compression.service import (
    ContextCompressionService,
)
from app.context.compression.strategies.default import (
    DefaultContextCompressionStrategy,
)


@pytest.mark.asyncio
async def test_default_compression_respects_token_budget():
    """
    Verify compression keeps candidates within token budget.
    """

    service = ContextCompressionService()

    request = CompressionRequest(
        candidates=[
            CompressionCandidate(
                content="important context",
                priority_score=1.0,
                estimated_tokens=5,
            ),
            CompressionCandidate(
                content="secondary context",
                priority_score=0.5,
                estimated_tokens=10,
            ),
        ],
        token_budget=5,
    )

    result = await service.compress(request)

    assert len(result.compressed_candidates) == 1
    assert result.compressed_token_count == 5
    assert result.removed_candidates == 1


@pytest.mark.asyncio
async def test_default_compression_keeps_high_priority_candidates():
    """
    Verify higher priority candidates are selected first.
    """

    strategy = DefaultContextCompressionStrategy()

    request = CompressionRequest(
        candidates=[
            CompressionCandidate(
                content="low priority",
                priority_score=0.1,
                estimated_tokens=5,
            ),
            CompressionCandidate(
                content="high priority",
                priority_score=0.9,
                estimated_tokens=5,
            ),
        ],
        token_budget=5,
    )

    result = await strategy.compress(request)

    assert (
        result.compressed_candidates[0].content
        == "high priority"
    )


@pytest.mark.asyncio
async def test_compression_service_delegates_to_strategy():
    """
    Verify compression service delegates to strategy.
    """

    class MockCompressionStrategy:
        def __init__(self):
            self.called = False

        async def compress(self, request):
            self.called = True

            from app.context.compression.models import (
                CompressionResult,
            )

            return CompressionResult(
                metadata={
                    "strategy": "mock"
                }
            )

    strategy = MockCompressionStrategy()

    service = ContextCompressionService(
        strategy=strategy,
    )

    request = CompressionRequest()

    result = await service.compress(request)

    assert strategy.called is True
    assert result.metadata["strategy"] == "mock"


@pytest.mark.asyncio
async def test_compression_empty_candidates():
    """
    Verify empty candidate list returns valid result.
    """

    service = ContextCompressionService()

    request = CompressionRequest(
        candidates=[]
    )

    result = await service.compress(request)

    assert result.compressed_candidates == []
    assert result.original_token_count == 0
    assert result.compressed_token_count == 0
    assert result.removed_candidates == 0
