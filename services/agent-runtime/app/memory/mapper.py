"""
OneMind Memory Vector Mapper.

Provides conversion between:
- MemoryRecord
- VectorRecord

Sprint 3 - S3-007 Memory Vector Integration
"""

from .models import MemoryRecord
from app.vector_store.models import VectorRecord


class MemoryVectorMapper:
    """
    Mapper between memory domain objects
    and vector storage records.
    """

    DEFAULT_COLLECTION = "onemind_memory"

    @staticmethod
    def to_vector_record(
        memory: MemoryRecord,
        vector: list[float],
        collection: str = DEFAULT_COLLECTION,
    ) -> VectorRecord:
        """
        Convert MemoryRecord into VectorRecord.

        Args:
            memory:
                Source memory domain object.

            vector:
                Generated embedding vector.

            collection:
                Vector storage collection name.

        Returns:
            VectorRecord ready for VectorStore.
        """

        return VectorRecord(
            id=memory.id,
            collection=collection,
            vector=vector,
            payload={
                "memory_id": memory.id,
                "content": memory.content,
                "created_at": memory.created_at.isoformat(),
                "updated_at": memory.updated_at.isoformat(),
            },
            metadata=memory.metadata,
        )

    @staticmethod
    def to_memory_record(
        record: VectorRecord,
    ) -> MemoryRecord:
        """
        Convert VectorRecord back into MemoryRecord.

        Args:
            record:
                Vector storage record.

        Returns:
            MemoryRecord domain object.
        """

        payload = record.payload

        return MemoryRecord(
            id=payload.get(
                "memory_id",
                record.id,
            ),
            content=payload.get(
                "content",
                "",
            ),
            metadata=record.metadata,
        )