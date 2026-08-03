"""
Retrieval models for Context Intelligence Layer.

Defines request and response contracts
used by Retrieval Pipeline implementations.

Sprint 4 - Context Intelligence & Retrieval Pipeline
"""

from typing import Any

from pydantic import BaseModel, Field


class RetrievalRequest(BaseModel):
    """
    Input request for retrieval pipeline.

    Represents a query that requires relevant
    information from available sources.
    """

    query: str

    limit: int = 10

    filters: dict[str, Any] = Field(
        default_factory=dict,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


class RetrievalResult(BaseModel):
    """
    Result produced by retrieval pipeline.

    Designed to support future expansion:
    - memory retrieval
    - knowledge retrieval
    - ranking
    - source attribution
    """

    memories: list[Any] = Field(
        default_factory=list,
    )

    knowledge: list[Any] = Field(
        default_factory=list,
    )

    sources: list[str] = Field(
        default_factory=list,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )
