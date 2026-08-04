"""
Context Compression models.

Defines request, candidate, and result contracts
for the Context Compression Layer.

Sprint 4 - Context Intelligence & Retrieval Pipeline
"""

from typing import Any

from pydantic import BaseModel, Field


class CompressionCandidate(BaseModel):
    """
    Candidate context item for compression.

    Represents an individual context fragment
    that can be evaluated and retained or removed
    during compression.
    """

    content: str

    priority_score: float = 0.0

    estimated_tokens: int = 0

    metadata: dict[str, Any] = Field(default_factory=dict)


class CompressionRequest(BaseModel):
    """
    Input request for context compression.

    Contains ranked context candidates and
    compression constraints.
    """

    candidates: list[CompressionCandidate] = Field(
        default_factory=list
    )

    token_budget: int | None = None

    compression_policy: str = "default"

    metadata: dict[str, Any] = Field(default_factory=dict)


class CompressionResult(BaseModel):
    """
    Result produced by Context Compression.

    Provides compressed context output together
    with compression metrics.
    """

    compressed_candidates: list[CompressionCandidate] = Field(
        default_factory=list
    )

    original_token_count: int = 0

    compressed_token_count: int = 0

    removed_candidates: int = 0

    metadata: dict[str, Any] = Field(default_factory=dict)
