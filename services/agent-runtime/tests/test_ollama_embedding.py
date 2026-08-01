"""
Tests for Ollama Embedding Provider.

Uses mocked HTTP responses.
No real Ollama runtime dependency.
"""

import pytest
import httpx

from app.embedding.models import EmbeddingRequest
from app.embedding.ollama_provider import (
    OllamaEmbeddingProvider,
)


@pytest.mark.anyio
async def test_ollama_embedding_provider_creation():
    """
    Verify provider initialization.
    """

    provider = OllamaEmbeddingProvider()

    assert provider.base_url == "http://localhost:11434"
    assert provider.model == "bge-m3:latest"


@pytest.mark.anyio
async def test_ollama_provider_returns_embedding(
    monkeypatch,
):
    """
    Verify Ollama response is converted
    into EmbeddingResponse.
    """

    async def mock_post(
        self,
        url,
        json,
        timeout,
    ):
        request = httpx.Request(
            "POST",
            url,
        )

        return httpx.Response(
            status_code=200,
            json={
                "embedding": [
                    0.1,
                    0.2,
                    0.3,
                ]
            },
            request=request,
        )

    monkeypatch.setattr(
        httpx.AsyncClient,
        "post",
        mock_post,
    )

    provider = OllamaEmbeddingProvider()

    response = await provider.embed(
        EmbeddingRequest(
            text="OneMind test",
        )
    )

    assert response.provider == "ollama"
    assert response.model == "bge-m3:latest"
    assert response.dimension == 3
    assert len(response.vector) == 3


@pytest.mark.anyio
async def test_ollama_provider_uses_custom_model():

    provider = OllamaEmbeddingProvider(
        model="nomic-embed-text:latest",
    )

    assert provider.model == "nomic-embed-text:latest"


@pytest.mark.anyio
async def test_ollama_vector_dimension_matches_metadata(
    monkeypatch,
):
    """
    Verify dimension matches vector size.
    """

    async def mock_post(
        self,
        url,
        json,
        timeout,
    ):
        request = httpx.Request(
            "POST",
            url,
        )

        return httpx.Response(
            status_code=200,
            json={
                "embedding": [
                    0.01,
                    0.02,
                    0.03,
                    0.04,
                ]
            },
            request=request,
        )

    monkeypatch.setattr(
        httpx.AsyncClient,
        "post",
        mock_post,
    )

    provider = OllamaEmbeddingProvider()

    response = await provider.embed(
        EmbeddingRequest(
            text="dimension check",
        )
    )

    assert len(response.vector) == response.dimension