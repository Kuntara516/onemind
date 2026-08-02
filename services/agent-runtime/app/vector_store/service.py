from .factory import VectorStoreFactory
from .models import VectorRecord


class VectorStoreService:
    """
    Service layer for vector storage operations.

    Keeps application logic independent from
    concrete vector store implementations.
    """

    def __init__(self, backend: str = "memory") -> None:
        self._store = VectorStoreFactory.create(backend)

    def add(self, record: VectorRecord) -> None:
        """
        Store a vector record.
        """
        self._store.add(record)

    def get(self, record_id: str) -> VectorRecord | None:
        """
        Retrieve a vector record.
        """
        return self._store.get(record_id)

    def delete(self, record_id: str) -> None:
        """
        Delete a vector record.
        """
        self._store.delete(record_id)

    def search(
        self,
        vector: list[float],
        limit: int = 5,
    ) -> list[VectorRecord]:
        """
        Search vector records.
        """
        return self._store.search(vector, limit)