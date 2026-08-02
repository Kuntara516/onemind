from app.vector_store.models import VectorRecord
from app.vector_store.qdrant import QdrantVectorStore


TEST_COLLECTION = "onemind_test_memory"


def create_store() -> QdrantVectorStore:
    return QdrantVectorStore(
        host="localhost",
        port=6333,
        collection=TEST_COLLECTION,
    )


def test_qdrant_add_and_get():
    store = create_store()

    record = VectorRecord(
        id="qdrant-001",
        collection=TEST_COLLECTION,
        vector=[0.1, 0.2, 0.3],
        payload={
            "name": "test",
        },
        metadata={
            "source": "test",
        },
    )

    store.add(record)

    result = store.get("qdrant-001")

    assert result is not None
    assert result.id == "qdrant-001"
    assert result.payload["name"] == "test"


def test_qdrant_search():
    store = create_store()

    store.add(
        VectorRecord(
            id="qdrant-search-001",
            collection=TEST_COLLECTION,
            vector=[1.0, 0.0, 0.0],
        )
    )

    results = store.search(
        [1.0, 0.0, 0.0],
        limit=1,
    )

    assert len(results) == 1
    assert results[0].id == "qdrant-search-001"


def test_qdrant_delete():
    store = create_store()

    store.add(
        VectorRecord(
            id="qdrant-delete-001",
            collection=TEST_COLLECTION,
            vector=[0.5, 0.5, 0.5],
        )
    )

    store.delete("qdrant-delete-001")

    result = store.get("qdrant-delete-001")

    assert result is None
