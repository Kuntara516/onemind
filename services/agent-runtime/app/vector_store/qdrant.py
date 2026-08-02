from uuid import NAMESPACE_URL, uuid5

from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance,
    PointStruct,
    VectorParams,
    PointIdsList,
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
        collection: str = "onemind_memory",
    ) -> None:
        self._client = QdrantClient(
            host=host,
            port=port,
            check_compatibility=False,
        )

        self._collection = collection

    def _point_id(
        self,
        record_id: str,
    ) -> str:
        """
        Convert OneMind record id into Qdrant compatible UUID.
        """

        return str(
            uuid5(
                NAMESPACE_URL,
                f"onemind:{record_id}",
            )
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

    def add(
        self,
        record: VectorRecord,
    ) -> None:
        collection = record.collection or self._collection

        self._ensure_collection(
            collection=collection,
            vector_size=len(record.vector),
        )

        self._client.upsert(
            collection_name=collection,
            points=[
                PointStruct(
                    id=self._point_id(record.id),
                    vector=record.vector,
                    payload={
                        "_record_id": record.id,
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
        points = self._client.retrieve(
            collection_name=self._collection,
            ids=[
                self._point_id(record_id),
            ],
            with_payload=True,
            with_vectors=True,
        )

        if not points:
            return None

        point = points[0]

        payload = point.payload or {}

        return VectorRecord(
            id=payload.get(
                "_record_id",
                record_id,
            ),
            collection=self._collection,
            vector=point.vector or [],
            payload=payload.get(
                "payload",
                {},
            ),
            metadata=payload.get(
                "metadata",
                {},
            ),
        )

    def delete(
        self,
        record_id: str,
    ) -> None:
        self._client.delete(
            collection_name=self._collection,
            points_selector=PointIdsList(
                points=[
                    self._point_id(record_id),
                ],
            ),
        )

    def search(
        self,
        vector: list[float],
        limit: int = 5,
    ) -> list[VectorRecord]:
        result = self._client.query_points(
            collection_name=self._collection,
            query=vector,
            limit=limit,
            with_payload=True,
            with_vectors=True,
        )

        records: list[VectorRecord] = []

        for point in result.points:
            payload = point.payload or {}

            records.append(
                VectorRecord(
                    id=payload.get(
                        "_record_id",
                        str(point.id),
                    ),
                    collection=self._collection,
                    vector=point.vector or [],
                    payload=payload.get(
                        "payload",
                        {},
                    ),
                    metadata=payload.get(
                        "metadata",
                        {},
                    ),
                )
            )

        return records