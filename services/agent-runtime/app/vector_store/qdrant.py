from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance,
    PointStruct,
    VectorParams,
)

from .base import VectorStore
from .models import VectorRecord


class QdrantVectorStore(VectorStore):
    """
    Qdrant implementation of VectorStore.

    Provides persistent vector storage backend.
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6333,
    ) -> None:
        self._client = QdrantClient(
            host=host,
            port=port,
        )

    def _ensure_collection(
        self,
        collection: str,
        vector_size: int,
    ) -> None:
        collections = self._client.get_collections()

        exists = any(
            item.name == collection
            for item in collections.collections
        )

        if not exists:
            self._client.create_collection(
                collection_name=collection,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,
                ),
            )

    def add(self, record: VectorRecord) -> None:
        self._ensure_collection(
            collection=record.collection,
            vector_size=len(record.vector),
        )

        self._client.upsert(
            collection_name=record.collection,
            points=[
                PointStruct(
                    id=record.id,
                    vector=record.vector,
                    payload={
                        "payload": record.payload,
                        "metadata": record.metadata,
                    },
                )
            ],
        )

    def get(
        self,
        record_id: str,
    ) -> VectorRecord | None:
        return None

    def delete(
        self,
        record_id: str,
    ) -> None:
        return None

    def search(
        self,
        vector: list[float],
        limit: int = 5,
    ) -> list[VectorRecord]:
        return []