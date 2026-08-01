"""
Embedding provider interface.

Defines the contract that all embedding providers
must implement.
"""

from abc import ABC, abstractmethod

from .models import EmbeddingRequest, EmbeddingResponse


class EmbeddingProvider(ABC):
    """
    Abstract embedding provider.

    Implementations may connect to:
    - Ollama
    - OpenAI
    - Sentence Transformers
    - Other embedding backends
    """

    @abstractmethod
    async def embed(
        self,
        request: EmbeddingRequest,
    ) -> EmbeddingResponse:
        """
        Generate an embedding vector from input text.

        Args:
            request: Embedding input request.

        Returns:
            Embedding response containing vector and metadata.
        """
        raise NotImplementedError