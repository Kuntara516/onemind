"""
OneMind Vector Memory Provider.

Provides semantic memory storage using:
- EmbeddingService
- VectorStoreService
- Qdrant backend

Sprint 3 - S3-007 Memory Vector Integration
"""

from app.embedding.models import EmbeddingRequest
from app.embedding.service import EmbeddingService
from app.vector_store.service import VectorStoreService

from .interface import MemoryInterface
from .mapper import MemoryVectorMapper
from .models import MemoryQuery, MemoryRecord, MemoryResult


class VectorMemoryProvider(MemoryInterface):
    """
    Vector-backed memory provider.

    Stores MemoryRecord as embeddings
    inside VectorStore.
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store_service: VectorStoreService,
    ) -> None:
        """
        Initialize vector memory provider.

        Args:
            embedding_service:
                Service used to generate embeddings.

            vector_store_service:
                Vector storage abstraction.
        """

        self._embedding_service = embedding_service
        self._vector_store_service = vector_store_service

    async def store(
        self,
        memory: MemoryRecord,
    ) -> MemoryRecord:
        """
        Store memory as vector representation.
        """

        embedding = await self._embedding_service.embed(
            EmbeddingRequest(
                text=memory.content,
            )
        )

        vector_record = MemoryVectorMapper.to_vector_record(
            memory=memory,
            vector=embedding.vector,
        )

        self._vector_store_service.add(
            vector_record,
        )

        return memory

    async def retrieve(
        self,
        query: MemoryQuery,
    ) -> MemoryResult:
        """
        Retrieve memories using semantic similarity.
        """

        embedding = await self._embedding_service.embed(
            EmbeddingRequest(
                text=query.query,
            )
        )

        vector_records = self._vector_store_service.search(
            vector=embedding.vector,
            limit=query.limit,
        )

        memories = [
            MemoryVectorMapper.to_memory_record(
                record,
            )
            for record in vector_records
        ]

        return MemoryResult(
            records=memories,
            count=len(memories),
            metadata={
                "provider": "vector",
                "query": query.query,
            },
        )

    async def delete(
        self,
        memory_id: str,
    ) -> bool:
        """
        Delete vector-backed memory.
        """

        existing = self._vector_store_service.get(
            memory_id,
        )

        if existing is None:
            return False

        self._vector_store_service.delete(
            memory_id,
        )

        return True