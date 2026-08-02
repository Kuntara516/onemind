from .base import VectorStore
from .memory import InMemoryVectorStore


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
        """

        match backend.lower():
            case "memory":
                return InMemoryVectorStore()
            case _:
                raise ValueError(
                    f"Unsupported vector store backend: {backend}"
                )