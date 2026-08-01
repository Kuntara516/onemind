"""
Embedding service layer.

Provides a high-level interface for generating embeddings
without exposing provider implementation details.
"""

from .interface import EmbeddingProvider
from .models import EmbeddingRequest, EmbeddingResponse


class EmbeddingService:
    """
    Embedding service facade.

    Responsible for coordinating embedding requests
    through an injected embedding provider.
    """

    def __init__(
        self,
        provider: EmbeddingProvider,
    ):
        """
        Initialize embedding service.

        Args:
            provider: Embedding provider implementation.
        """
        self.provider = provider

    async def embed(
        self,
        request: EmbeddingRequest,
    ) -> EmbeddingResponse:
        """
        Generate embedding through configured provider.

        Args:
            request: Embedding input.

        Returns:
            Generated embedding response.
        """

        return await self.provider.embed(request)