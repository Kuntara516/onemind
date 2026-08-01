"""
OneMind Knowledge Foundation Models.

Defines domain models used by the Knowledge Layer.

Sprint 3 - Memory & Knowledge Foundation
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class KnowledgeItem(BaseModel):
    """
    Represents a knowledge item stored in the knowledge layer.

    A KnowledgeItem is an abstract unit of information that can
    later be enriched with embeddings and semantic metadata.
    """

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    content: str

    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )

    source: Optional[str] = None

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class KnowledgeQuery(BaseModel):
    """
    Represents a knowledge retrieval request.

    Current implementation supports basic query matching.
    Future implementations may support semantic retrieval.
    """

    query: str

    limit: int = 10

    filters: Dict[str, Any] = Field(
        default_factory=dict
    )


class KnowledgeResult(BaseModel):
    """
    Represents knowledge retrieval result.
    """

    items: List[KnowledgeItem] = Field(
        default_factory=list
    )

    count: int = 0

    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )