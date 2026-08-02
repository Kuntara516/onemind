from .base import VectorStore
from .memory import InMemoryVectorStore
from .qdrant import QdrantVectorStore


class VectorStoreFactory:
    """
    Factory for creating VectorStore implementations.
    """

    @staticmethod
    def create(backend: str = "memory") -> VectorStore:
        """
        Create a VectorStore instance.

        Supported backends:
        - memory
        - qdrant
        """

        match backend.lower():
            case "memory":
                return InMemoryVectorStore()

            case "qdrant":
                return QdrantVectorStore()

            case _:
                raise ValueError(
                    f"Unsupported vector store backend: {backend}"
                )