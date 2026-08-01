"""
Ollama embedding provider implementation.

Provides real embedding generation through local Ollama runtime.
"""

import httpx

from app.embedding.interface import EmbeddingProvider
from app.embedding.models import (
    EmbeddingRequest,
    EmbeddingResponse,
)


class OllamaEmbeddingProvider(EmbeddingProvider):
    """
    Embedding provider backed by Ollama.

    Default model:
    bge-m3:latest
    """

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "bge-m3:latest",
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model

    async def embed(
        self,
        request: EmbeddingRequest,
    ) -> EmbeddingResponse:
        """
        Generate embedding vector using Ollama.
        """

        payload = {
            "model": self.model,
            "prompt": request.text,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/embeddings",
                json=payload,
                timeout=60.0,
            )

            response.raise_for_status()

            data = response.json()

        vector = data["embedding"]

        return EmbeddingResponse(
            vector=vector,
            dimension=len(vector),
            provider="ollama",
            model=self.model,
        )