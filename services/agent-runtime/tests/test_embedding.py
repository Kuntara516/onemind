"""
Tests for OneMind Embedding Service.

Validates:
- Embedding models
- Provider contract
- Embedding service delegation
"""

import pytest

from app.embedding import (
    EmbeddingRequest,
    EmbeddingService,
)
from app.embedding.provider import DummyEmbeddingProvider


@pytest.mark.anyio
async def test_embedding_request_creation():
    """
    Verify embedding request can be created.
    """

    request = EmbeddingRequest(
        text="hello OneMind",
    )

    assert request.text == "hello OneMind"


@pytest.mark.anyio
async def test_dummy_embedding_provider_returns_vector():
    """
    Verify dummy provider returns expected embedding.
    """

    provider = DummyEmbeddingProvider()

    request = EmbeddingRequest(
        text="test embedding",
    )

    response = await provider.embed(request)

    assert response.provider == "dummy"
    assert response.dimension == 384
    assert len(response.vector) == 384


@pytest.mark.anyio
async def test_embedding_service_delegates_to_provider():
    """
    Verify embedding service delegates execution
    to injected provider.
    """

    provider = DummyEmbeddingProvider()

    service = EmbeddingService(
        provider=provider,
    )

    request = EmbeddingRequest(
        text="service test",
    )

    response = await service.embed(request)

    assert response.model == "dummy-embedding-384"
    assert response.dimension == 384


@pytest.mark.anyio
async def test_embedding_vector_dimension_matches_metadata():
    """
    Verify vector length matches declared dimension.
    """

    service = EmbeddingService(
        provider=DummyEmbeddingProvider(),
    )

    response = await service.embed(
        EmbeddingRequest(
            text="dimension check",
        )
    )

    assert len(response.vector) == response.dimension