"""
OneMind Memory Domain Models.

Defines the core data structures used by the Memory Foundation layer.

Sprint 3 - Memory & Knowledge Foundation
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4


@dataclass
class MemoryRecord:
    """
    Represents a single memory item stored by the Memory layer.

    A MemoryRecord is storage-independent and can be persisted
    by different memory providers in the future.
    """

    content: str

    id: str = field(default_factory=lambda: str(uuid4()))

    metadata: Dict[str, Any] = field(default_factory=dict)

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


@dataclass
class MemoryQuery:
    """
    Represents a memory retrieval request.

    This abstraction allows future implementations to support:
    - keyword search
    - semantic search
    - vector retrieval
    - hybrid retrieval
    """

    query: str

    limit: int = 10

    filters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MemoryResult:
    """
    Represents the result returned from a memory retrieval operation.
    """

    records: List[MemoryRecord] = field(default_factory=list)

    count: int = 0

    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """
        Ensure count always reflects returned records
        when count is not explicitly provided.
        """

        if self.count == 0 and self.records:
            self.count = len(self.records)