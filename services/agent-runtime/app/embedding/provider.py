"""
Default embedding provider implementations.

S3-003 provides a deterministic dummy provider
for testing and service validation.

Future providers:
- OllamaEmbeddingProvider
- OpenAIEmbeddingProvider
- SentenceTransformerEmbeddingProvider
"""

from .interface import EmbeddingProvider
from .models import EmbeddingRequest, EmbeddingResponse


class DummyEmbeddingProvider(EmbeddingProvider):
    """
    Deterministic embedding provider for development and testing.

    Generates a fixed-size zero vector without external dependencies.
    """

    DEFAULT_DIMENSION = 384

    async def embed(
        self,
        request: EmbeddingRequest,
    ) -> EmbeddingResponse:
        """
        Generate a dummy embedding vector.

        Args:
            request: Embedding request.

        Returns:
            Deterministic embedding response.
        """

        vector = [0.0] * self.DEFAULT_DIMENSION

        return EmbeddingResponse(
            vector=vector,
            dimension=self.DEFAULT_DIMENSION,
            provider="dummy",
            model="dummy-embedding-384",
        )