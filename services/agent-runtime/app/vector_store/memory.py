from .base import VectorStore
from .models import VectorRecord


class InMemoryVectorStore(VectorStore):
    """
    Simple in-memory implementation of VectorStore.

    Intended for testing and local development.
    """

    def __init__(self) -> None:
        self._records: dict[str, VectorRecord] = {}

    def add(self, record: VectorRecord) -> None:
        self._records[record.id] = record

    def get(self, record_id: str) -> VectorRecord | None:
        return self._records.get(record_id)

    def delete(self, record_id: str) -> None:
        self._records.pop(record_id, None)

    def search(
        self,
        vector: list[float],
        limit: int = 5,
    ) -> list[VectorRecord]:
        """
        Placeholder implementation.

        Proper vector similarity search will be implemented
        in the Qdrant backend during S3-006.
        """
        return list(self._records.values())[:limit]