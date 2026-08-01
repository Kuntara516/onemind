"""
Embedding data models.

Defines request and response models used by the embedding layer.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class EmbeddingRequest:
    """
    Input request for generating an embedding vector.
    """

    text: str


@dataclass(frozen=True)
class EmbeddingResponse:
    """
    Result returned from an embedding provider.
    """

    vector: list[float]
    dimension: int
    provider: str
    model: str