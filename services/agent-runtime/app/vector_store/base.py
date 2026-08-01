from abc import ABC, abstractmethod

from .models import VectorRecord


class VectorStore(ABC):
    """
    Abstract interface for vector storage backends.

    Implementations may use:
    - In-memory storage
    - Qdrant
    - Other vector databases
    """

    @abstractmethod
    def add(self, record: VectorRecord) -> None:
        """
        Store a vector record.
        """
        raise NotImplementedError

    @abstractmethod
    def get(self, record_id: str) -> VectorRecord | None:
        """
        Retrieve a vector record by id.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, record_id: str) -> None:
        """
        Delete a vector record by id.
        """
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        vector: list[float],
        limit: int = 5,
    ) -> list[VectorRecord]:
        """
        Search similar vectors.
        """
        raise NotImplementedError